"""
name: display.py
date: 2025-12-08
author: githubonline1396529
description: Display utilities for I Ching divination.
"""

import sys


# Define global display messages.
HELP_MESSAGE = """
I Ching divination table commands:

  g / get               - Get a new original hexagram
  c / change <Position> - Generate a changing hexagram by specifying changing 
    yao positions (1-6). For example: c 1,3,5 or change 2 4 6.
  s / show              - Show current hexagram
  clear / reset         - Clear current divination table.
  h / help              - Show this help message.
  q / quit / exit       - Exit the divination table.
"""


# Define welcome message. Beginning with an ASCII art.
WELCOME_MESSAGE = """
      _ ___ ___ _    _           
   __| |_ _/ __| |_ (_)_ _  __ _ 
  / _| || | (__| ' \| | ' \/ _` |
  \__|_|___\___|_||_|_|_||_\__, |
                           |___/ 

clIChing - An I Ching Divination Table in command line.

Author: githubonline1396529. Current version 0.1.0.0.
- Type 'h' or 'help' to see available commands.
- Type 'q' or 'quit' to exit.
"""


class Color:
    """ANSI color code class.
    
    This class provides ANSI escape codes for colored output in the terminal.
    Each color is represented as a class variable, and can be used to format 
    strings.
    
    Examples:
    
      >>> print(f"{Color.RED}This text is red{Color.END}")
    """

    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    END = "\033[0m"
    BOLD = "\033[1m"


def colored_yao(coins: tuple, value: int, changing: bool) -> str:
    """Return colored Yao string based on the coin results.

    Args:
        coins (tuple): A tuple of three integers (0 or 1) representing the coin
            results.
        value (int): The value of the Yao (0 for Yin, 1 for Yang).
        changing (bool): Whether the Yao is changing.

    Returns:
        str: The colored Yao string.
    """
    
    sum_coins = sum(coins)

    if sum_coins == 0:  # Three 0 -> old Yin.
        symbol = "### ###"
        color = Color.BLUE
        marker = " x" if changing else ""
    elif sum_coins == 1:  # Two 0, One 1 -> young Yang.
        symbol = "#######"
        color = Color.RED
        marker = ""
    elif sum_coins == 2:  # Two 1, One 0 -> young Yin.
        symbol = "### ###"
        color = Color.RED
        marker = ""
    elif sum_coins == 3:  # Three 1 -> old Yang.
        symbol = "#######"
        color = Color.BLUE
        marker = " o" if changing else ""

    return f"{color}{symbol}{Color.END}{marker}"
