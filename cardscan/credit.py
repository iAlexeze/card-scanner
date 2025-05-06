import logging
import argparse
import os
import sys
import requests
import re

KNOWN_TEST_NUMBERS = {
    "4111111111111111", "4012888888881881",
    "378282246310005", "5555555555554444",
}

TEST_PREFIXES = ["4111", "4012", "6011", "3782", "5555"]


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

    parser.add_argument("--deep-check", help="Perform BIN lookup and fraud checks", action="store_true")

    args = parser.parse_args()

    number_str = args.number or os.getenv("CARD_NUMBER")
    if not number_str:
        logger.error("No card number provided. Use -n or set CARD_NUMBER environment variable")
        sys.exit(1)
    
    return number_str, args.deep_check

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

    def is_format_valid(self) -> bool:
        """Validate digits between 13 and 19."""
        return bool(re.fullmatch(r"\d{13,19}", self.number_str))
    
    def is_test_card(self) -> bool:
        """Check for known test cards"""
        return self.number_str in KNOWN_TEST_NUMBERS

    def is_likely_test_card(self) -> bool:
        """Check for likely test cards"""
        return any(self.number_str.startswith(p) for p in TEST_PREFIXES)

    def bin_lookup(self) -> dict:
        """Get metadata about the card using binlist.net."""
        try:
            response = requests.get(f"https://lookup.binlist.net/{self.number_str[:6]}")
            if response.status_code == 200:
                return response.json()
            return {}
        except requests.RequestException as e:
            logger.warning(f"BIN lookup failed: {e}")
            return {}

    def report(self, deep_check: bool = False):
        """Print full report for card"""
        print(f"\nCard Number: {self.masked()}")
        print(f"Type: {self.get_type()}")

        if not self.is_format_valid():
            logger.error("Invalid card format.")
            return

        if self.is_valid():
            print("Valid: ✅")
        else:
            print("Valid: ❌")
            return

        if self.is_test_card():
            print("Note: 🚧 Known test card")
        elif self.is_likely_test_card():
            print("Warning: ⚠️  Suspicious/test prefix")

        if deep_check:
            print("\n🔍 BIN Info:")
            bin_data = self.bin_lookup()
            if bin_data:
                print(f"  Scheme:   {bin_data.get('scheme', 'N/A')}")
                print(f"  Type:     {bin_data.get('type', 'N/A')}")
                print(f"  Brand:    {bin_data.get('brand', 'N/A')}")
                print(f"  Country:  {bin_data.get('country', {}).get('name', 'N/A')}")
                print(f"  Bank:     {bin_data.get('bank', {}).get('name', 'N/A')}")
            else:
                print("  No data found.")

def main():
    try:
        card_number, deep_check = handle_args()
        card = CreditCard(card_number)
        card.report(deep_check)
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return

if __name__ == "__main__":
    main()
