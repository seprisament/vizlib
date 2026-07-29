"""Tiny CSV loader — plain Python, no pandas."""

import csv


def load_csv(path="data/happiness_wealth.csv"):
    """Read a wealth/happiness CSV into simple parallel lists.

    Expects a header row with (at least) ``wealth`` and ``happiness``
    columns. Returns a dict of two ``float`` lists so the result can be
    passed straight into the plotting functions::

        data = load_csv()
        scatter_trend(data["wealth"], data["happiness"])

    Args:
        path: Path to the CSV file to read.

    Returns:
        dict with keys ``"wealth"`` and ``"happiness"``, each a list of floats.
    """
    wealth, happiness = [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            wealth.append(float(row["wealth"]))
            happiness.append(float(row["happiness"]))
    return {"wealth": wealth, "happiness": happiness}
