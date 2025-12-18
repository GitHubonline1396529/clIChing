"""
name: hexagram.py
date: 2025-12-08
author: githubonline1396529
description: Hexagram generation and manipulation for I Ching divination.
"""

# Import necessary modules.
import random
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Yao:
    value: bool  # 0: Yin, 1: Yang.
    changing: bool  # Whether to be changeable (for old Yin/Yang).
    coins: Tuple[int, int, int]  # Result of the three coins.

    def display(self, colored=True) -> str:
        """Display the Yao hexagram."""
        from display import colored_yao

        if colored:
            return colored_yao(self.coins, self.value, self.changing)
        else:
            # No-color display.
            if self.value == 0:  # Yin Yao.
                return "### ###" if self.changing else "#######"
            else:  # Yang Yao.
                return "#######" if self.changing else "### ###"


class Hexagram:
    def __init__(self, yaos: List[Yao]):
        self.yaos = yaos  # List of six Yao objects, from First Yao to Top Yao.
        self._calculate_hexagram()

    def _calculate_hexagram(self):
        """Calculate the hexagram number and binary representation."""
        # Calculate number: First Yao is the least significant bit, Top Yao is
        # the most significant bit
        self.original_number = 0
        # i from 0 to 5, corresponding to First Yao to Top Yao.
        for i, yao in enumerate(self.yaos):
            if yao.value == 1:
                self.original_number += 1 << i  # 2 to the power of i
        # Generate binary string from Top Yao to First Yao (6 bits, padded with
        # 0 if needed)
        self.original_binary = format(self.original_number, "06b")

    def display(self, colored=True):
        """Display the hexagram (from top to bottom)"""
        for i in range(5, -1, -1):  # From Top Yao (6) to First Yao (1)
            yao = self.yaos[i]
            print(yao.display(colored))

    def get_changing_hexagram(self, positions: List[int]) -> "Hexagram":
        """Generate a changing hexagram based on specified Yao positions.

        Args:
            positions: List of Yao positions to change (1-6)

        Returns:
            A new Hexagram object (changing hexagram).
        """
        new_yaos = []
        for idx, yao in enumerate(self.yaos):
            position = idx + 1  # Yao position (1-6).

            # Judge if the user's input is within 1~6.
            if position in positions and yao.changing:
                # Changing Yao: Old Yin changes to Young Yang, Old Yang changes
                # to Young Yin. Then exchange Yin and Yang.
                new_value = 1 if yao.value == 0 else 0
                # Generate new coin results (consistent with the changed
                # Yin/Yang)
                if new_value == 0:  # Change to Young Yin
                    new_coins = (0, 1, 1)  # Two 1s and one 0
                else:  # Change to Young Yang
                    new_coins = (1, 0, 0)  # Two 0s and one 1
                new_changing = False
                # After change, it becomes Young Yin/Young Yang, no longer
                # changeable.
            else:
                # Unchanged Yao
                new_value = yao.value
                new_coins = yao.coins
                new_changing = yao.changing

            new_yaos.append(Yao(new_value, new_changing, new_coins))

        return Hexagram(new_yaos)

    def _get_data_path(self, filename: str) -> Path:
        """Get the data file path."""
        return Path(__file__).parent / "data" / "hexagrams" / filename

    def get_interpretation(self, hexagram_number: int) -> str:
        """Read the hexagram interpretation file."""
        filepath = self._get_data_path(f"{hexagram_number:02d}.txt")
        if filepath.exists():
            try:
                return filepath.read_text(encoding="utf-8")
            except:
                return filepath.read_text(encoding="gbk")
        return (  # The string is warped here for better readability (80 cols).
            f"Hexagram interpretation file {hexagram_number:02d}.txt not "
            "found."
        )

    def display_interpretation(self):
        """Display the hexagram interpretation."""
        print(self.get_interpretation(self.original_number))


def generate_hexagram() -> Hexagram:
    """Generate a six-yao hexagram."""
    yaos = []
    for _ in range(6):
        coins = tuple(random.randint(0, 1) for _ in range(3))
        sum_coins = sum(coins)

        # Determine Yao based on rules
        if sum_coins == 0:  # Three 0s -> Old Yin (changeable)
            yao = Yao(0, True, coins)
        elif sum_coins == 1:  # Two 0s and one 1 -> Young Yang (unchangeable)
            yao = Yao(1, False, coins)
        elif sum_coins == 2:  # Two 1s and one 0 -> Young Yin (unchangeable)
            yao = Yao(0, False, coins)
        else:  # Three 1s -> Old Yang (changeable)
            yao = Yao(1, True, coins)

        yaos.append(yao)

    return Hexagram(yaos)
