from collections import Counter
import itertools
import math
import os
import random
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from yahtzee_core import YahtzeeGame, CATEGORIES, calculate_score, roll_dice


def get_dice_state(dice: List[int]) -> int:
    counts = Counter(dice)
    return max(counts.values())


def calculate_theoretical_first_roll_distribution() -> np.ndarray:
    total_outcomes = 6**5
    state_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for roll in itertools.product(range(1, 7), repeat=5):
        s = get_dice_state(list(roll))
        state_counts[s] += 1

    return np.array([state_counts[i] / total_outcomes for i in range(1, 6)])


def calculate_empirical_transition_matrix(n_simulations: int = 100000) -> np.ndarray:
    transitions = np.zeros((5, 5))

    for state_i in range(1, 6):
        if state_i == 5:
            transitions[4, 4] = n_simulations
            continue

        for _ in range(n_simulations):
            kept = [6] * state_i
            rerolled = [random.randint(1, 6) for _ in range(5 - state_i)]
            all_dice = kept + rerolled

            counts = Counter(all_dice)
            target_count = counts[6]
            max_any = max(counts.values())
            next_state = max(target_count, max_any)

            transitions[state_i - 1, next_state - 1] += 1

    row_sums = transitions.sum(axis=1, keepdims=True)
    return transitions / row_sums


def run_markov_analysis():
    pi_0 = calculate_theoretical_first_roll_distribution()
    P = calculate_empirical_transition_matrix(n_simulations=100000)

    pi_1 = pi_0 @ P
    pi_2 = pi_0 @ (P @ P)

    return {
        "pi_0": pi_0,
        "P": P,
        "pi_1": pi_1,
        "pi_2": pi_2,
        "prob_yahtzee_roll_1": pi_0[4],
        "prob_yahtzee_roll_2": pi_1[4],
        "prob_yahtzee_roll_3": pi_2[4]
    }


def simulate_ai_turn(game: YahtzeeGame, player_idx: int) -> int:
    dice = game.roll()

    for _ in range(2):
        counts = Counter(dice)
        if 5 in counts.values() and not game.current_player.is_category_filled("YAHTZEE"):
            break

        avail = game.current_player.get_available_categories()
        unique_dice = sorted(list(set(dice)))
        if "LARGE_STRAIGHT" in avail and len(unique_dice) >= 4:
            keep_indices = []
            for idx, val in enumerate(dice):
                if val in unique_dice:
                    keep_indices.append(idx)
                    unique_dice.remove(val)
            dice = game.roll(keep_indices[:4])
            continue

        most_common_val, most_common_count = counts.most_common(1)[0]
        for val, count in counts.items():
            if count == most_common_count and val > most_common_val:
                most_common_val = val

        keep_indices = [idx for idx, val in enumerate(dice) if val == most_common_val]
        dice = game.roll(keep_indices)

    avail = game.current_player.get_available_categories()
    best_category = avail[0]
    best_score = -1
    best_diff = -999

    for cat in avail:
        score = calculate_score(cat, dice)
        if cat == "YAHTZEE" and score == 50:
            best_category = cat
            break
        if cat == "LARGE_STRAIGHT" and score == 40:
            best_category = cat
            break
        if cat == "SMALL_STRAIGHT" and score == 30:
            best_category = cat
            best_score = score
            continue
        if cat == "FULL_HOUSE" and score == 25:
            best_category = cat
            best_score = score
            continue

        if cat in ["ACES", "TWOS", "THREES", "FOURS", "FIVES", "SIXES"]:
            req_val = {"ACES": 1, "TWOS": 2, "THREES": 3, "FOURS": 4, "FIVES": 5, "SIXES": 6}[cat]
            if score >= req_val * 3:
                diff = score - (req_val * 3)
                if diff > best_diff:
                    best_diff = diff
                    best_category = cat
                    best_score = score
                    continue

        if score > best_score:
            best_score = score
            best_category = cat

    if best_score <= 0:
        sacrifices = ["ACES", "TWOS", "YAHTZEE", "FOUR_OF_A_KIND", "THREE_OF_A_KIND", "THREES"]
        for sac in sacrifices:
            if sac in avail:
                best_category = sac
                break

    return game.choose_category(best_category)


def run_monte_carlo_matches(num_matches: int = 10000) -> Dict:
    p1_scores = []
    p2_scores = []
    p1_wins = 0
    p2_wins = 0
    ties = 0
    p1_bonuses = 0
    p2_bonuses = 0
    yahtzee_counts = 0

    for _ in range(num_matches):
        game = YahtzeeGame("Jugador 1", "Jugador 2")
        while not game.game_over:
            simulate_ai_turn(game, game.current_player_idx)

        s1 = game.players[0].get_total_score()
        s2 = game.players[1].get_total_score()
        p1_scores.append(s1)
        p2_scores.append(s2)

        if game.players[0].get_upper_section_bonus() > 0:
            p1_bonuses += 1
        if game.players[1].get_upper_section_bonus() > 0:
            p2_bonuses += 1

        if (game.players[0].scores.get("YAHTZEE") or 0) > 0:
            yahtzee_counts += 1
        if (game.players[1].scores.get("YAHTZEE") or 0) > 0:
            yahtzee_counts += 1

        if s1 > s2:
            p1_wins += 1
        elif s2 > s1:
            p2_wins += 1
        else:
            ties += 1

    p1_arr = np.array(p1_scores)
    p2_arr = np.array(p2_scores)

    return {
        "num_matches": num_matches,
        "p1_scores": p1_arr,
        "p2_scores": p2_arr,
        "p1_mean": float(np.mean(p1_arr)),
        "p2_mean": float(np.mean(p2_arr)),
        "p1_std": float(np.std(p1_arr)),
        "p2_std": float(np.std(p2_arr)),
        "p1_max": int(np.max(p1_arr)),
        "p2_max": int(np.max(p2_arr)),
        "p1_min": int(np.min(p1_arr)),
        "p2_min": int(np.min(p2_arr)),
        "p1_win_rate": p1_wins / num_matches,
        "p2_win_rate": p2_wins / num_matches,
        "tie_rate": ties / num_matches,
        "p1_bonus_rate": p1_bonuses / num_matches,
        "p2_bonus_rate": p2_bonuses / num_matches,
        "yahtzee_success_rate": yahtzee_counts / (2 * num_matches)
    }


def generate_all_plots(markov_res: Dict, mc_res: Dict, output_dir: str = "results"):
    os.makedirs(output_dir, exist_ok=True)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    # Distribucion de puntajes
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(mc_res["p1_scores"], bins=30, alpha=0.6, label=f'Jugador 1 (Media: {mc_res["p1_mean"]:.1f})', color='#1f77b4', density=True)
    ax.hist(mc_res["p2_scores"], bins=30, alpha=0.5, label=f'Jugador 2 (Media: {mc_res["p2_mean"]:.1f})', color='#2ca02c', density=True)
    ax.set_title(f'Distribución de Puntajes ({mc_res["num_matches"]:,} Partidas)', fontsize=12)
    ax.set_xlabel('Puntaje Total')
    ax.set_ylabel('Densidad')
    ax.legend()
    plt.tight_layout()
    plot1_path = os.path.join(output_dir, "distribucion_puntajes.png")
    plt.savefig(plot1_path, dpi=300)
    plt.close()

    # Matriz de transicion
    fig, ax = plt.subplots(figsize=(6, 5))
    P = markov_res["P"]
    cax = ax.matshow(P, cmap='Blues')
    fig.colorbar(cax)

    states = ["E1", "E2", "E3", "E4", "E5"]
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xticklabels(states)
    ax.set_yticklabels(states)

    for i in range(5):
        for j in range(5):
            val = P[i, j]
            color = "white" if val > 0.5 else "black"
            ax.text(j, i, f'{val:.3f}', ha='center', va='center', color=color)

    ax.set_title('Matriz de Transición P', fontsize=12, pad=15)
    ax.set_xlabel('Estado Siguiente')
    ax.set_ylabel('Estado Actual')
    plt.tight_layout()
    plot2_path = os.path.join(output_dir, "matriz_transicion_markov.png")
    plt.savefig(plot2_path, dpi=300)
    plt.close()

    # Probabilidad acumulada por tiro
    fig, ax = plt.subplots(figsize=(6, 4))
    rolls = ['Tiro 1', 'Tiro 2', 'Tiro 3']
    probs = [
        markov_res["prob_yahtzee_roll_1"] * 100,
        markov_res["prob_yahtzee_roll_2"] * 100,
        markov_res["prob_yahtzee_roll_3"] * 100
    ]
    bars = ax.bar(rolls, probs, color=['#7f7f7f', '#1f77b4', '#2ca02c'], width=0.5)
    ax.set_title('Probabilidad de Yahtzee por Tiro', fontsize=12)
    ax.set_ylabel('Probabilidad (%)')
    ax.set_ylim(0, max(probs) * 1.25)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plot3_path = os.path.join(output_dir, "probabilidad_yahtzee_markov.png")
    plt.savefig(plot3_path, dpi=300)
    plt.close()

    # Distribucion inicial
    fig, ax = plt.subplots(figsize=(6, 4))
    states_labels = ['E1', 'E2', 'E3', 'E4', 'E5']
    pi_0_pct = markov_res["pi_0"] * 100
    bars0 = ax.bar(states_labels, pi_0_pct, color='#9467bd', width=0.5)
    ax.set_title(r'Distribución Inicial de Estados $\pi^{(0)}$', fontsize=12)
    ax.set_ylabel('Probabilidad (%)')
    ax.set_ylim(0, max(pi_0_pct) * 1.15)

    for bar in bars0:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plot4_path = os.path.join(output_dir, "distribucion_estados_iniciales.png")
    plt.savefig(plot4_path, dpi=300)
    plt.close()

    return [plot1_path, plot2_path, plot3_path, plot4_path]


if __name__ == "__main__":
    markov_res = run_markov_analysis()
    mc_res = run_monte_carlo_matches(num_matches=10000)
    generate_all_plots(markov_res, mc_res, output_dir="results")

    print(f"P(Yahtzee T1): {markov_res['prob_yahtzee_roll_1']*100:.3f}%")
    print(f"P(Yahtzee T2): {markov_res['prob_yahtzee_roll_2']*100:.3f}%")
    print(f"P(Yahtzee T3): {markov_res['prob_yahtzee_roll_3']*100:.3f}%")
    print(f"Promedio J1: {mc_res['p1_mean']:.2f}")
    print(f"Promedio J2: {mc_res['p2_mean']:.2f}")
    print(f"Victorias J1: {mc_res['p1_win_rate']*100:.2f}% | J2: {mc_res['p2_win_rate']*100:.2f}%")
