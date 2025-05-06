import logging
import argparse
import os
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Handle arguments
def handle_args():
    parser = argparse.ArgumentParser(
        prog="Automated Credit Card Checker",
        description="Determine validity of a card on a target Card Number",
        epilog="""Example: cardscan -n 378282246310005""",
        formatter_class=argparse.MetavarTypeHelpFormatter
    )

    # Add arguments
    parser.add_argument("-n", "--number",
                        help="Credit Card number (or use CARD_NUMBER env)",
                        type=str)

    args = parser.parse_args()

    number_str = args.number or os.getenv("CARD_NUMBER")
    if not number_str:
        logger.error("No card number provided. Use -n or set CARD_NUMBER environment variable")
        sys.exit(1)

    return number_str

class CreditCard:
    def __init__(self, number: str):
        self.number_str = number.strip()
        if not self.number_str.isdigit():
            raise ValueError("Card number must contain only digits.")
        self.number_int = int(self.number_str)
        self.length = len(self.number_str)

    def is_valid(self) -> bool:
        """Validate using Luhn’s algorithm."""
        sum_of_doubled_digits = 0
        sum_of_remaining_digits = 0
        # Process every second digit from the right, starting from second-to-last
        for i in range(self.length - 2, -1, -2):
            digit = int(self.number_str[i])
            doubled = digit * 2
            if doubled > 9:
                doubled = 1 + (doubled % 10)
            sum_of_doubled_digits += doubled
        # Process the remaining digits
        for i in range(self.length - 1, -1, -2):
            digit = int(self.number_str[i])
            sum_of_remaining_digits += digit
        total = sum_of_doubled_digits + sum_of_remaining_digits
        return total % 10 == 0

    def get_type(self) -> str:
        """Determine the card type based on prefix and length."""
        first_two = int(self.number_str[:2])
        first_one = int(self.number_str[0])

        if first_two in [34, 37] and self.length == 15:
            return "AMEX"
        elif 51 <= first_two <= 55 and self.length == 16:
            return "MASTERCARD"
        elif first_one == 4 and self.length in [13, 16]:
            return "VISA"
        else:
            return "INVALID"

    def masked(self) -> str:
        """Return the masked version of the card number."""
        return '*' * (self.length - 4) + self.number_str[-4:]


def main():
    try:
        card_number = handle_args()
        card = CreditCard(card_number)
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return

    if card.is_valid():
        print("\n{}: {}".format(card.get_type(), card.masked()))
    else:
        logger.error("INVALID")

if __name__ == "__main__":
    main()
