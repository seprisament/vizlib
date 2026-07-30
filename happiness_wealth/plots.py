"""Small visualizations of the wealth/happiness relationship.

Each is a single standalone function (no classes) that takes plain Python
lists, draws with matplotlib, optionally saves to disk, and returns the
Figure so callers can further tweak or display it.
"""

import math

import matplotlib.pyplot as plt


def _fit_line(xs, ys):
    """Ordinary least-squares fit in plain Python (no numpy).

    Returns ``(slope, intercept)`` for the best-fit line ``y = slope*x + b``.
    """
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    # slope = covariance(x, y) / variance(x)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    slope = num / den if den else 0.0
    intercept = mean_y - slope * mean_x
    return slope, intercept


def scatter_trend(wealth, happiness, title="Wealth vs. Happiness",
                  save_path=None):
    """Scatter plot of wealth vs. happiness with a fitted trend line.

    The trend line's slope and intercept are computed by hand with a plain
    least-squares fit — no numpy involved.

    Args:
        wealth: List of wealth/income values (x-axis).
        happiness: List of happiness scores (y-axis), same length as ``wealth``.
        title: Figure title.
        save_path: If given, the figure is written to this path.

    Returns:
        The matplotlib ``Figure``.
    """
    slope, intercept = _fit_line(wealth, happiness)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(wealth, happiness, s=25, alpha=0.6, color="#3b7dd8",
               edgecolor="white", linewidth=0.5, label="people")

    # Draw the fitted line across the observed wealth range.
    x0, x1 = min(wealth), max(wealth)
    ax.plot([x0, x1], [slope * x0 + intercept, slope * x1 + intercept],
            color="#d64545", linewidth=2,
            label=f"trend (slope={slope:.2e})")

    ax.set_xlabel("Wealth (annual income)")
    ax.set_ylabel("Happiness score")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.2)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig


def happiness_histogram(wealth, happiness, edges=None, bins=10,
                        labels=("low wealth", "middle wealth", "high wealth"),
                        title="Happiness Distribution by Wealth Group",
                        save_path=None):
    """Overlaid histogram of happiness, split into wealth groups.

    People are bucketed by wealth (low / middle / high by default) and a
    translucent happiness histogram is drawn for each group, so you can see
    how the distribution shifts as wealth rises.

    Args:
        wealth: List of wealth/income values.
        happiness: List of happiness scores, same length as ``wealth``.
        edges: Wealth cut points between groups. Defaults to the data's
            tertiles, giving three roughly equal-sized groups.
        bins: Number of histogram bins for the happiness axis.
        labels: Names for the groups (one more than ``edges``).
        title: Figure title.
        save_path: If given, the figure is written to this path.

    Returns:
        The matplotlib ``Figure``.
    """
    if edges is None:
        # Tertiles of wealth -> three roughly equal groups (plain Python).
        s = sorted(wealth)
        edges = [s[len(s) // 3], s[2 * len(s) // 3]]

    # Assign each person to a group index from their wealth.
    groups = [[] for _ in labels]
    for w, h in zip(wealth, happiness):
        idx = sum(1 for e in edges if w >= e)  # 0..len(edges)
        groups[idx].append(h)

    colors = ["#d64545", "#e0a13c", "#2e8b57"]
    fig, ax = plt.subplots(figsize=(8, 5))
    for scores, label, color in zip(groups, labels, colors):
        if scores:
            ax.hist(scores, bins=bins, range=(0, 10), alpha=0.55,
                    color=color, edgecolor="white",
                    label=f"{label} (n={len(scores)})")

    ax.set_xlabel("Happiness score")
    ax.set_ylabel("Number of people")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.2)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig


def diminishing_returns(wealth=None, model=None,
                        title="Diminishing Returns of Wealth on Happiness",
                        save_path=None):
    """Line chart showing happiness rising steeply, then flattening.

    Illustrates diminishing returns: each extra dollar buys less happiness
    than the last. By default it evaluates a saturating log-style model over
    an even sweep of wealth values, so it runs out of the box with no data.

    Args:
        wealth: Optional list of wealth values (x-axis). Defaults to an even
            sweep from 0 to 120,000.
        model: Optional ``f(wealth) -> happiness`` curve. Defaults to a
            saturating curve that flattens toward a happiness of ~10.
        title: Figure title.
        save_path: If given, the figure is written to this path.

    Returns:
        The matplotlib ``Figure``.
    """
    if wealth is None:
        # Even sweep of incomes from 0 to 120k.
        wealth = [i * 120000 / 200 for i in range(201)]
    if model is None:
        # Saturating curve: fast early gains, flattening tail.
        model = lambda w: 10 * (1 - math.exp(-w / 25000))

    xs = sorted(wealth)
    ys = [model(w) for w in xs]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, ys, color="#2e8b57", linewidth=2.5)
    ax.fill_between(xs, ys, color="#2e8b57", alpha=0.08)

    ax.set_xlabel("Wealth (annual income)")
    ax.set_ylabel("Happiness score")
    ax.set_title(title)
    ax.grid(True, alpha=0.2)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig
