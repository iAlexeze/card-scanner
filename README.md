
# 💳 cardscan

**Automated Credit Card Checker** — a lightweight command-line tool to validate credit card numbers and detect card types using [Luhn's Algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm).

---

## 🚀 Features

* ✅ Validates credit card numbers using Luhn’s algorithm
* 🔒 Masks all digits except the last 4
* 🏷️ Detects card type (VISA, MasterCard, AMEX, or INVALID)
* 📦 Installable via [PEP 621](https://peps.python.org/pep-0621/) `pyproject.toml`
* 🧪 Usable as a standalone CLI or as a Python module

---

## 📦 Installation

### Option 1: Install via `pip` (Recommended for End Users)

```bash
pip install .
```

Then run:

```bash
cardscan -n 4111111111111111
```

### Option 2: Install with [Poetry](https://python-poetry.org/)

```bash
poetry install
poetry run cardscan -n 4111111111111111
```

---

## 🖥️ Usage

```bash
cardscan -n <CARD_NUMBER>
```

Or using an environment variable:

```bash
export CARD_NUMBER=378282246310005
cardscan
```

### 🧾 Example

```bash
$ cardscan -n 378282246310005
Card Number: ***********0005
Type: AMEX
Valid: ✅
Note: 🚧 Known test card
```

```bash
$ cardscan -n 1234567890123456
Card Number: *************4815
Type: INVALID
Valid: ❌
```

---
### 🔍 Deep Check Example

To perform a deeper check with BIN lookup and fraud checks, use the `--deep-check` option:

```bash
$ cardscan -n 4111111111111111 --deep-check
Card Number: ************1111
Type: VISA
Valid: ✅

🔍 BIN Info:
  Scheme:   Visa
  Type:     Credit
  Brand:    Visa
  Country:  United States
  Bank:     Bank of America
```
---

## 🧠 How It Works

1. **Validation**: Uses the Luhn algorithm to check card number validity.
2. **Detection**: Matches known prefixes and lengths to determine the card type:

   * `VISA`: Starts with `4`, length 13 or 16
   * `MASTERCARD`: Starts with `51-55`, length 16
   * `AMEX`: Starts with `34` or `37`, length 15
   * Otherwise: `INVALID`
3. **Masking**: Hides all digits except the last four for display.

---

## 📁 Project Structure

```.
├── cardscan
│   ├── credit.py        # Main logic and CLI entry
│   └── __init__.py
├── pyproject.toml       # Build config
└── README.md
```

---

## 🛠️ Development

### Run from Source

```bash
python cardscan/credit.py -n 4111111111111111
```

### Run `main.py` (if needed)

```bash
python main.py
```

### Run with Poetry

```bash
poetry run cardscan -n 4111111111111111
```

---

## 📄 License

MIT License © 2025 [Alex Eze](mailto:ialexeze@gmail.com)

<div align="center">
  <img src="./cardscan/qr.png" alt="Alex QR Code" width="200"/>
</div>

---
