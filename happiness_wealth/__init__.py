"""happiness_wealth — wealth vs. happiness curves that kink into diminishing returns.

Self-contained: :func:`main` generates a synthetic, era-split dataset and
renders both charts. The building blocks are exposed for reuse.
"""

from .plots import (
    generate_dataset,
    happiness_curve,
    bracket_edges,
    marginal_gain_by_bracket,
    apply_style,
    make_histogram,
    make_line_chart,
    main,
)

__version__ = "0.3.0"
__all__ = [
    "generate_dataset",
    "happiness_curve",
    "bracket_edges",
    "marginal_gain_by_bracket",
    "apply_style",
    "make_histogram",
    "make_line_chart",
    "main",
]
