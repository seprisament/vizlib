"""happiness_wealth — tiny matplotlib visualizations of wealth vs. happiness."""

from .loader import load_csv
from .plots import scatter_trend, diminishing_returns, happiness_histogram

__version__ = "0.2.0"
__all__ = [
    "load_csv",
    "scatter_trend",
    "diminishing_returns",
    "happiness_histogram",
]
