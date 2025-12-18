"""
name: cli.py
date: 2025-12-08
author: githubonline1396529
description: Command-line interface for I Ching divination.
"""

# Import necessary modules.
import argparse
import re
from hexagram import generate_hexagram

# Import custom display messages as global constants.
# See `display.py` for WELCOME_MESSAGE and HELP_MESSAGE.
from display import WELCOME_MESSAGE, HELP_MESSAGE


class DivinationTable:
    """Interactive Divination Table for I Ching."""

    def __init__(self, no_color=False):
        """Initialize the divination table.

        Args:
            no_color (bool): If True, disable colored output.
        """
        self.original_hexagram = None
        self.changed_hexagram = None
        self.no_color = no_color
        self.running = True

    def display_prompt(self):
        """Display prompt.

        This function displays a `divination table >>>` prompt every time the
        user is expected to input a command.
        """
        print("\ndivination table >>> ", end="", flush=True)

    def run(self):
        """Run interactive divination table.

        Start to run the divination table, print `WELCOME_MESSAGE` and enter a
        read-eval loop. Read user's input and process commands.
        """
        print(WELCOME_MESSAGE)

        while self.running:
            self.display_prompt()
            try:
                command = input().strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExit the divination table.")
                break

            self.process_command(command)

    def process_command(self, command):
        """Process user command.

        This function processes the user command input in the divination table.

        Args:
            command (str): The command input by the user.
        """
        if not command:
            return

        cmd = command.lower().split()[0] if " " in command else command.lower()

        if cmd in ["q", "quit", "exit", "system"]:
            self.running = False
            print("Return to terminal...")

        elif cmd in ["g", "get"]:
            self.get_hexagram()

        elif cmd in ["c", "change"]:
            self.change_hexagram(command)

        elif cmd in ["h", "help"]:
            self.show_help()

        elif cmd in ["s", "show"]:
            self.show_current()

        elif cmd in ["clear", "reset"]:
            self.reset_table()

        else:
            print(f"Unknown command: {command}.")
            print("Type 'h' for help.")

    def get_hexagram(self):
        """Get a new original hexagram.

        This function generates a new original hexagram, resets the changed
        hexagram to None, and displays the new hexagram along with its
        interpretation.
        """

        self.original_hexagram = generate_hexagram()
        self.changed_hexagram = None  # Reset changed hexagram to be None.

        self.original_hexagram.display(colored=not self.no_color)

        self.original_hexagram.display_interpretation()

    def change_hexagram(self, command):
        """Process changing hexagram command."""
        if not self.original_hexagram:
            print("Please get an original hexagram first using 'g' command.")
            return

        # Analyze the position of the changing yao.
        try:
            # Extract the numeric part.
            nums_part = (
                command[command.index(" ") + 1 :] if " " in command else ""
            )

            if not nums_part:
                print("Usage: c <Yao position> or change <Yao position>")
                print("For example: c 1,3,5 or change 2 4 6")
                return

            # Extract all the numbers with regex.
            numbers = re.findall(r"\d+", nums_part)
            if not numbers:
                print("No valid numbers found.")
                return

            # Convert to integers and remove duplicates
            positions = list(set(int(num) for num in numbers))

            # Chack if the yao positions given to be changed are between 1 and
            # 6. If not, throw out an error message and return.
            for pos in positions:
                if pos < 1 or pos > 6:
                    print(
                        f"Error: The yao position must between 1-6, "
                        f"given {pos}."
                    )
                    return

            # Chack if the asigned changing yao positions are valid.
            changing_positions = []
            for pos in positions:
                yao = self.original_hexagram.yaos[pos - 1]
                if not yao.changing:
                    print(
                        f"Warning: The Yao {pos} "
                        f"({'Yang' if yao.value else 'Yin'}) is not changing "
                        f"(less {'Yang' if yao.value else 'Yin'})."
                    )
                else:
                    changing_positions.append(pos)

            # If there's no changeable Yao, just return.
            if not changing_positions:
                print("No changeable Yao. Remain the original hexagram.")
                return

            print(f"Changing positions: {changing_positions}")

            # Generate changing hexagram.
            self.changed_hexagram = (
                self.original_hexagram.get_changing_hexagram(changing_positions)
            )

            print("\nChanging Hexagram:")
            self.changed_hexagram.display(colored=not self.no_color)

            print("\nChanging Hexagram Interpretation:")
            self.changed_hexagram.display_interpretation()

        except Exception as e:
            print(f"Parsing error: {e}")
            print("Correct usage: c 1,3,5 or change 2 4 6")

    def show_help(self):
        """Display help information"""
        print(HELP_MESSAGE)

    def show_current(self):
        """Display current hexagrams"""
        if not self.original_hexagram:
            print(
                "No hexagram available. Use 'g' to generate an original hexagram."
            )
            return

        print("\nCurrent Hexagrams:")
        print("\nOriginal Hexagram:")
        self.original_hexagram.display(colored=not self.no_color)

        if self.changed_hexagram:
            print("\nChanging Hexagram:")
            self.changed_hexagram.display(colored=not self.no_color)

    def reset_table(self):
        """Reset the divination table"""
        self.original_hexagram = None
        self.changed_hexagram = None
        print("Divination table has been cleared.")


def main():
    """The main function."""

    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        description="Interactive I Ching divination table in command line."
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colorful output."
    )
    parser.add_argument("--question", "-q", help="Question to be divined.")

    args = parser.parse_args()

    # Create the interactive divination table.
    table = DivinationTable(no_color=args.no_color)

    # If there is a question argument, display it directly.
    if args.question:
        print(f"Question: {args.question}")
        print("-" * 40)

    # Run the interactive divination table.
    table.run()
