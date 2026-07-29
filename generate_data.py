"""Generate a realistic wealth vs. happiness dataset.

Standard library only (``random``, ``math``, ``csv``). The data follows a
diminishing-returns shape — happiness climbs steeply at low wealth and
flattens as wealth grows — with a positive-but-noisy correlation. The
randomness is seeded so the output is reproducible.

Run it directly to (re)write ``data/happiness_wealth.csv``::

    python generate_data.py
"""

import csv
import math
import os
import random

N = 200          # number of people to generate (configurable)
SEED = 42        # seed for reproducibility
OUT_PATH = "data/happiness_wealth.csv"


def generate(n=N, seed=SEED):
    """Return ``n`` (wealth, happiness) rows following diminishing returns."""
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        # Skew wealth toward lower incomes (most people earn less).
        wealth = round(rng.expovariate(1 / 40000) + 5000)
        # Saturating "true" happiness, then add noise and clamp to 0..10.
        base = 10 * (1 - math.exp(-wealth / 25000))
        happiness = base + rng.gauss(0, 1.1)
        happiness = round(max(0.0, min(10.0, happiness)), 2)
        rows.append((wealth, happiness))
    return rows


def write_csv(rows, path=OUT_PATH):
    """Write rows to ``path`` with a ``wealth,happiness`` header."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["wealth", "happiness"])
        writer.writerows(rows)


if __name__ == "__main__":
    write_csv(generate())
    print(f"Wrote {N} rows to {OUT_PATH}")
