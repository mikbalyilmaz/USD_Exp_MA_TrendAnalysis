"""Common set-up for the analysis scripts: import path, data and a CSV writer."""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from usdtrend import basket, load, log100  # noqa: E402
from usdtrend.style import FIG_DIR  # noqa: E402

RAW = load()
RATES = basket(RAW)                    # TRY per USD and per EUR, mean of buying and selling rate
LOGS = log100(RATES)                   # 100 log; differences are monthly changes in per cent
NAMES = {"usd": "USD/TRY", "eur": "EUR/TRY"}


def dates(index):
    return index.to_timestamp()


def save_table(rows, name):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(FIG_DIR / f"{name}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote figures/{name}.csv ({len(rows)} rows)")
