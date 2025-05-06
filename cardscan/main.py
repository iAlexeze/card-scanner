import argparse
import os
import sys
import logging
from cardscan import CreditCard

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
