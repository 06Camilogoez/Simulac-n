import os
import sys
import time
from typing import List

from colorama import init, Fore, Style
from yahtzee_core import YahtzeeGame, CATEGORIES, CATEGORY_NAMES_ES, calculate_score
from markov_montecarlo import simulate_ai_turn

init(autoreset=True)

DICE_ASCII = {
    1: [
        "+-------+",
        "|       |",
        "|   o   |",
        "|       |",
        "+-------+"
    ],
    2: [
        "+-------+",
        "| o     |",
        "|       |",
        "|     o |",
        "+-------+"
    ],
    3: [
        "+-------+",
        "| o     |",
        "|   o   |",
        "|     o |",
        "+-------+"
    ],
    4: [
        "+-------+",
        "| o   o |",
        "|       |",
        "| o   o |",
        "+-------+"
    ],
    5: [
        "+-------+",
        "| o   o |",
        "|   o   |",
        "| o   o |",
        "+-------+"
    ],
    6: [
        "+-------+",
        "| o   o |",
        "| o   o |",
        "| o   o |",
        "+-------+"
    ]
}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    print(f"{Fore.CYAN}======================================================================")
    print("  SIMULADOR DE YAHTZEE - 2 JUGADORES (DISTRIBUCION U{1,6})")
    print(f"======================================================================{Style.RESET_ALL}")


def render_dice(dice: List[int], held: List[bool] = None):
    if held is None:
        held = [False] * len(dice)

    lines = ["", "", "", "", ""]
    for i, val in enumerate(dice):
        color = Fore.YELLOW if held[i] else Fore.WHITE
        if val in DICE_ASCII:
            face_lines = DICE_ASCII[val]
            for row in range(5):
                lines[row] += f"  {color}{face_lines[row]}{Style.RESET_ALL} "
        else:
            for row in range(5):
                lines[row] += "  [ ? ]  "

    print("\n".join(lines))
    labels = ""
    for i, is_held in enumerate(held):
        status = f"{Fore.GREEN}[Conservado]{Style.RESET_ALL}" if is_held else f"{Fore.LIGHTBLACK_EX}[Relanzable]{Style.RESET_ALL}"
        labels += f"    Dado #{i+1} {status}   "
    print(labels)
    print()


def display_scorecard(game: YahtzeeGame):
    p1 = game.players[0]
    p2 = game.players[1]

    header = f"{Fore.BLUE}{'CATEGORIA':<26} | {Fore.YELLOW}{p1.player_name:^14} | {Fore.GREEN}{p2.player_name:^14}{Style.RESET_ALL}"
    separator = "-" * 60
    print(separator)
    print(header)
    print(separator)

    print(f"{Fore.MAGENTA}--- SECCION SUPERIOR ---{Style.RESET_ALL}")
    for cat in CATEGORIES[:6]:
        name = CATEGORY_NAMES_ES[cat]
        s1 = str(p1.scores[cat]) if p1.scores[cat] is not None else "-"
        s2 = str(p2.scores[cat]) if p2.scores[cat] is not None else "-"
        print(f"{name:<26} | {s1:^14} | {s2:^14}")

    print(f"{'Subtotal Superior':<26} | {str(p1.get_upper_section_total()):^14} | {str(p2.get_upper_section_total()):^14}")
    print(f"{'Bono Superior (>=63)':<26} | {str(p1.get_upper_section_bonus()):^14} | {str(p2.get_upper_section_bonus()):^14}")
    print(separator)

    print(f"{Fore.MAGENTA}--- SECCION INFERIOR ---{Style.RESET_ALL}")
    for cat in CATEGORIES[6:]:
        name = CATEGORY_NAMES_ES[cat]
        s1 = str(p1.scores[cat]) if p1.scores[cat] is not None else "-"
        s2 = str(p2.scores[cat]) if p2.scores[cat] is not None else "-"
        print(f"{name:<26} | {s1:^14} | {s2:^14}")

    print(separator)
    print(f"{Fore.CYAN}{'PUNTAJE TOTAL':<26} | {str(p1.get_total_score()):^14} | {str(p2.get_total_score()):^14}{Style.RESET_ALL}")
    print(separator)


def play_human_turn(game: YahtzeeGame):
    player = game.current_player
    print(f"\n{Fore.GREEN}Turno de: {player.player_name} (Ronda {game.current_round}/13){Style.RESET_ALL}")

    input(f"{Fore.WHITE}Presiona [ENTER] para el lanzamiento #1...{Style.RESET_ALL}")
    dice = game.roll()
    render_dice(dice)

    for roll_idx in [2, 3]:
        choice = input(f"{Fore.CYAN}Lanzamiento #{roll_idx}: ¿Relanzar dados? (s/n): {Style.RESET_ALL}").strip().lower()
        if choice != 's':
            break

        while True:
            raw = input(f"{Fore.YELLOW}Indices de dados a conservar (1-5 separados por espacio, o 'ninguno'): {Style.RESET_ALL}").strip()
            if raw.lower() == 'ninguno' or raw == '':
                keep_indices = []
                break
            try:
                nums = [int(x) - 1 for x in raw.split()]
                if all(0 <= n <= 4 for n in nums):
                    keep_indices = list(set(nums))
                    break
                else:
                    print(f"{Fore.RED}Numeros validos: 1 al 5.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Entrada invalida. Ejemplo: 1 2 5{Style.RESET_ALL}")

        dice = game.roll(keep_indices)
        render_dice(dice, game.held_dice)

    avail = player.get_available_categories()
    print(f"\n{Fore.YELLOW}Categorias disponibles:{Style.RESET_ALL}")
    for idx, cat in enumerate(avail, 1):
        potential_score = calculate_score(cat, dice)
        print(f"  [{idx:2d}] {CATEGORY_NAMES_ES[cat]:<25} -> {potential_score:2d} pts")

    while True:
        try:
            sel_str = input(f"\n{Fore.GREEN}Selecciona categoria: {Style.RESET_ALL}").strip()
            sel_idx = int(sel_str) - 1
            if 0 <= sel_idx < len(avail):
                selected_cat = avail[sel_idx]
                score = game.choose_category(selected_cat)
                print(f"{Fore.GREEN}Anotado: {score} puntos en {CATEGORY_NAMES_ES[selected_cat]}{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Opcion fuera de rango.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Ingresa un numero valido.{Style.RESET_ALL}")


def main_game_loop():
    clear_screen()
    print_banner()

    print("Modo de juego:")
    print("  [1] Humano vs Humano")
    print("  [2] Humano vs IA")
    print("  [3] IA vs IA")

    mode = input("\nOpcion (1, 2 o 3) [defecto 1]: ").strip()
    if mode == "2":
        p1_name = input("Nombre del Jugador 1: ").strip() or "Jugador 1"
        p2_name = "IA"
        is_p2_ai = True
        is_p1_ai = False
    elif mode == "3":
        p1_name = "IA 1"
        p2_name = "IA 2"
        is_p1_ai = True
        is_p2_ai = True
    else:
        p1_name = input("Nombre del Jugador 1: ").strip() or "Jugador 1"
        p2_name = input("Nombre del Jugador 2: ").strip() or "Jugador 2"
        is_p1_ai = False
        is_p2_ai = False

    game = YahtzeeGame(p1_name, p2_name)

    while not game.game_over:
        clear_screen()
        print_banner()
        display_scorecard(game)

        curr_is_ai = (game.current_player_idx == 0 and is_p1_ai) or (game.current_player_idx == 1 and is_p2_ai)

        if curr_is_ai:
            if not (is_p1_ai and is_p2_ai):
                time.sleep(0.5)
            simulate_ai_turn(game, game.current_player_idx)
        else:
            play_human_turn(game)
            input(f"\n{Fore.WHITE}Presiona [ENTER] para continuar...{Style.RESET_ALL}")

    clear_screen()
    print_banner()
    print(f"\n{Fore.YELLOW}PARTIDA FINALIZADA{Style.RESET_ALL}\n")
    display_scorecard(game)

    winner, s1, s2 = game.get_winner()
    if winner:
        print(f"\n{Fore.GREEN}Ganador: {winner.player_name} con {winner.get_total_score()} puntos.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.CYAN}Empate con {s1} puntos.{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        main_game_loop()
    except KeyboardInterrupt:
        print("\nJuego cancelado.")
        sys.exit(0)
