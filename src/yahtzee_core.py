from collections import Counter
import random
from typing import List, Dict, Optional, Tuple

CATEGORIES = [
    "ACES",
    "TWOS",
    "THREES",
    "FOURS",
    "FIVES",
    "SIXES",
    "THREE_OF_A_KIND",
    "FOUR_OF_A_KIND",
    "FULL_HOUSE",
    "SMALL_STRAIGHT",
    "LARGE_STRAIGHT",
    "YAHTZEE",
    "CHANCE"
]

CATEGORY_NAMES_ES = {
    "ACES": "Unos (1)",
    "TWOS": "Doses (2)",
    "THREES": "Treses (3)",
    "FOURS": "Cuatros (4)",
    "FIVES": "Cincos (5)",
    "SIXES": "Seises (6)",
    "THREE_OF_A_KIND": "Trío (3 iguales)",
    "FOUR_OF_A_KIND": "Póker (4 iguales)",
    "FULL_HOUSE": "Full House (25 pts)",
    "SMALL_STRAIGHT": "Escalera Menor (30 pts)",
    "LARGE_STRAIGHT": "Escalera Mayor (40 pts)",
    "YAHTZEE": "Yahtzee (50 pts)",
    "CHANCE": "Azar (Suma total)"
}


def roll_dice(num_dice: int = 5) -> List[int]:
    return [random.randint(1, 6) for _ in range(num_dice)]


def calculate_score(category: str, dice: List[int]) -> int:
    if len(dice) != 5:
        raise ValueError("Se requieren 5 dados para evaluar.")

    counts = Counter(dice)
    dice_sorted = sorted(dice)
    dice_sum = sum(dice)

    if category == "ACES":
        return counts[1] * 1
    elif category == "TWOS":
        return counts[2] * 2
    elif category == "THREES":
        return counts[3] * 3
    elif category == "FOURS":
        return counts[4] * 4
    elif category == "FIVES":
        return counts[5] * 5
    elif category == "SIXES":
        return counts[6] * 6
    elif category == "THREE_OF_A_KIND":
        return dice_sum if any(c >= 3 for c in counts.values()) else 0
    elif category == "FOUR_OF_A_KIND":
        return dice_sum if any(c >= 4 for c in counts.values()) else 0
    elif category == "FULL_HOUSE":
        counts_list = sorted(list(counts.values()))
        return 25 if (counts_list == [2, 3] or counts_list == [5]) else 0
    elif category == "SMALL_STRAIGHT":
        straights = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        dice_set = set(dice)
        return 30 if any(s.issubset(dice_set) for s in straights) else 0
    elif category == "LARGE_STRAIGHT":
        return 40 if (dice_sorted == [1, 2, 3, 4, 5] or dice_sorted == [2, 3, 4, 5, 6]) else 0
    elif category == "YAHTZEE":
        return 50 if any(c == 5 for c in counts.values()) else 0
    elif category == "CHANCE":
        return dice_sum
    else:
        raise ValueError(f"Categoría desconocida: {category}")


class Scorecard:
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.scores: Dict[str, Optional[int]] = {cat: None for cat in CATEGORIES}
        self.yahtzee_bonus_count: int = 0

    def is_category_filled(self, category: str) -> bool:
        return self.scores.get(category) is not None

    def fill_category(self, category: str, dice: List[int]) -> int:
        if self.is_category_filled(category):
            raise ValueError(f"La categoría {category} ya fue utilizada.")

        if category != "YAHTZEE" and self.scores.get("YAHTZEE") == 50:
            if any(c == 5 for c in Counter(dice).values()):
                self.yahtzee_bonus_count += 1

        score = calculate_score(category, dice)
        self.scores[category] = score
        return score

    def get_upper_section_total(self) -> int:
        upper_cats = ["ACES", "TWOS", "THREES", "FOURS", "FIVES", "SIXES"]
        return sum(self.scores[cat] for cat in upper_cats if self.scores[cat] is not None)

    def get_upper_section_bonus(self) -> int:
        return 35 if self.get_upper_section_total() >= 63 else 0

    def get_lower_section_total(self) -> int:
        lower_cats = [
            "THREE_OF_A_KIND", "FOUR_OF_A_KIND", "FULL_HOUSE",
            "SMALL_STRAIGHT", "LARGE_STRAIGHT", "YAHTZEE", "CHANCE"
        ]
        return sum(self.scores[cat] for cat in lower_cats if self.scores[cat] is not None)

    def get_total_score(self) -> int:
        return (
            self.get_upper_section_total() +
            self.get_upper_section_bonus() +
            self.get_lower_section_total() +
            (self.yahtzee_bonus_count * 100)
        )

    def is_complete(self) -> bool:
        return all(score is not None for score in self.scores.values())

    def get_available_categories(self) -> List[str]:
        return [cat for cat, val in self.scores.items() if val is None]


class YahtzeeGame:
    def __init__(self, player1_name: str = "Jugador 1", player2_name: str = "Jugador 2"):
        self.players = [Scorecard(player1_name), Scorecard(player2_name)]
        self.current_player_idx = 0
        self.current_round = 1
        self.current_roll = 0
        self.current_dice = [0, 0, 0, 0, 0]
        self.held_dice = [False, False, False, False, False]
        self.game_over = False

    @property
    def current_player(self) -> Scorecard:
        return self.players[self.current_player_idx]

    def roll(self, keep_indices: Optional[List[int]] = None) -> List[int]:
        if self.game_over:
            raise RuntimeError("El juego ha finalizado.")
        if self.current_roll >= 3:
            raise RuntimeError("Límite de 3 lanzamientos alcanzado.")

        if keep_indices is None or self.current_roll == 0:
            self.current_dice = roll_dice(5)
            self.held_dice = [False] * 5
        else:
            new_dice = self.current_dice.copy()
            for i in range(5):
                if i not in keep_indices:
                    new_dice[i] = random.randint(1, 6)
            self.current_dice = new_dice
            self.held_dice = [i in keep_indices for i in range(5)]

        self.current_roll += 1
        return self.current_dice

    def choose_category(self, category: str) -> int:
        if self.current_roll == 0:
            raise RuntimeError("Debe lanzar los dados antes de elegir categoría.")

        score = self.current_player.fill_category(category, self.current_dice)

        self.current_roll = 0
        self.current_dice = [0, 0, 0, 0, 0]
        self.held_dice = [False] * 5

        if self.current_player_idx == 1:
            self.current_player_idx = 0
            self.current_round += 1
        else:
            self.current_player_idx = 1

        if self.players[0].is_complete() and self.players[1].is_complete():
            self.game_over = True

        return score

    def get_winner(self) -> Tuple[Optional[Scorecard], int, int]:
        p1 = self.players[0]
        p2 = self.players[1]
        score1 = p1.get_total_score()
        score2 = p2.get_total_score()
        if score1 > score2:
            return p1, score1, score2
        elif score2 > score1:
            return p2, score1, score2
        else:
            return None, score1, score2
