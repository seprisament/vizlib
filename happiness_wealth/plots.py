"""
Wealth -> Happiness: a shared curve that KINKS into sharp diminishing returns
=============================================================================

Charts:
  Chart 1 (histogram): marginal happiness gained per wealth bracket (5 wide,
      equal-width brackets, both eras combined). Soft-blue bars; the bracket where
      returns collapse is highlighted. Bars shrink left to right.
  Chart 2 (line chart): happiness vs wealth for each era, with one vertical line
      marking the kink where the 2010s starts flattening faster.

Run:  plots.py
Out:  wealth_happiness.csv, chart1_marginal_gain_hist.png, chart2_era_curves.pdf
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

RNG = np.random.default_rng(42)

# ---- Model constants (happiness on a 0-10 life-satisfaction scale) ----------
OBS_PER_YEAR = 200
ERAS = {"1980s": range(1980, 1990), "2010s": range(2010, 2020)}

FLOOR = 2.0              # happiness at (near) zero wealth
KINK = 115.0            # wealth ($1,000s) where the eras diverge
NOISE_SD = 0.35

# Shared regime BELOW the kink (identical for both eras).
K_LO, CAP_LO = 80.0, 7.8
H_KINK = FLOOR + (CAP_LO - FLOOR) * (1.0 - np.exp(-KINK / K_LO))

# Era-specific regime ABOVE the kink: (extra ceiling above H_KINK, saturation k).
ABOVE = {
    "1980s": (1.6, 90.0),    # keeps climbing gradually
    "2010s": (0.28, 10.0),   # flattens hard almost immediately
}

# Soft, minimal palette.
SOFT_BLUE = "#8FB8DE"
ACCENT = "#E8794A"       # (kept for reference; histogram now uses one color)
C_1980 = "#8189C6"       # soft indigo
C_2010 = "#E7A76A"       # soft amber
SOFT_RED = "#D98C82"     # soft red for the divergence line


# ----------------------------------------------------------------------------
# 1. DATASET
# ----------------------------------------------------------------------------
def happiness_curve(wealth: np.ndarray, era: np.ndarray) -> np.ndarray:
    """Piecewise curve: shared below KINK, era-specific above KINK (continuous)."""
    below = FLOOR + (CAP_LO - FLOOR) * (1.0 - np.exp(-wealth / K_LO))

    gap = np.where(era == "2010s", ABOVE["2010s"][0], ABOVE["1980s"][0])
    k_hi = np.where(era == "2010s", ABOVE["2010s"][1], ABOVE["1980s"][1])
    step = np.clip(wealth - KINK, 0, None)
    above = H_KINK + gap * (1.0 - np.exp(-step / k_hi))

    return np.where(wealth <= KINK, below, above)


def generate_dataset() -> pd.DataFrame:
    years = np.concatenate([np.repeat(list(r), OBS_PER_YEAR) for r in ERAS.values()])
    era = np.where(years >= 2010, "2010s", "1980s")
    n = years.size

    # Wealth ($1,000s): broad lognormal so every bracket is populated, low -> high.
    wealth = np.clip(RNG.lognormal(np.log(60), 0.75, size=n), 3, 600)

    happiness = happiness_curve(wealth, era) + RNG.normal(0, NOISE_SD, size=n)
    happiness = np.clip(happiness, 0.0, 10.0)

    return pd.DataFrame({
        "year": years,
        "era": era,
        "wealth": np.round(wealth, 1),
        "happiness": np.round(happiness, 2),
    })


# ----------------------------------------------------------------------------
# 2. MARGINAL-GAIN HELPERS
# ----------------------------------------------------------------------------
def bracket_edges(df: pd.DataFrame, n: int = 5) -> np.ndarray:
    """Equal-WIDTH wealth brackets from min to the 98th pct (tail trimmed)."""
    lo = df["wealth"].min() - 1e-6
    hi = np.percentile(df["wealth"], 98)
    return np.linspace(lo, hi, n + 1)


def marginal_gain_by_bracket(df: pd.DataFrame, edges: np.ndarray) -> np.ndarray:
    """Mean-happiness increase contributed by each successive wealth bracket."""
    d = df.copy()
    d["bin"] = pd.cut(d["wealth"], bins=edges, include_lowest=True, labels=False)
    means = d.groupby("bin")["happiness"].mean().reindex(range(len(edges) - 1))
    means = means.interpolate().bfill().ffill()
    prev = np.concatenate([[FLOOR], means.values[:-1]])
    return means.values - prev


# ----------------------------------------------------------------------------
# 3. VERIFICATION
# ----------------------------------------------------------------------------
def verify(df: pd.DataFrame) -> np.ndarray:
    print("Sample rows")
    print("-" * 52)
    print(df.sample(10, random_state=1).sort_index().to_string(index=False))

    edges = bracket_edges(df, n=5)
    centers = (edges[:-1] + edges[1:]) / 2

    agg = marginal_gain_by_bracket(df, edges)
    g80 = marginal_gain_by_bracket(df[df.era == "1980s"], edges)
    g10 = marginal_gain_by_bracket(df[df.era == "2010s"], edges)

    print("\nMarginal happiness gain per wealth bracket")
    print("-" * 52)
    print(f"{'bracket':>8}{'center$k':>10}{'1980s':>9}{'2010s':>9}{'combined':>10}")
    for i in range(len(agg)):
        print(f"{i + 1:>8}{centers[i]:>10.0f}{g80[i]:>9.3f}{g10[i]:>9.3f}{agg[i]:>10.3f}")

    above = centers > KINK
    print("\nPhenomenon (a) aggregate diminishing returns:")
    print(f"  gain bracket 1 = {agg[0]:.3f}  >>  gain bracket {len(agg)} = {agg[-1]:.3f}"
          f"  ({'PASS' if agg[0] > agg[-1] else 'FAIL'})")

    print("Eras start together below the kink:")
    print(f"  bracket-1 gain  1980s {g80[0]:.3f} vs 2010s {g10[0]:.3f}"
          f"  ({'PASS' if abs(g80[0] - g10[0]) < 0.25 else 'FAIL'})")

    print("Phenomenon (b) 2010s flattens sooner/harder above the kink:")
    print(f"  mean gain above ${KINK:.0f}k  1980s {g80[above].mean():.3f} "
          f"vs 2010s {g10[above].mean():.3f}"
          f"  ({'PASS' if g10[above].mean() < g80[above].mean() else 'FAIL'})")
    return edges


# ----------------------------------------------------------------------------
# Shared styling
# ----------------------------------------------------------------------------
def apply_style() -> None:
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#d9d9d9",
        "axes.linewidth": 1.0,
        "axes.grid": True,
        "grid.color": "#ececec",
        "grid.linewidth": 0.9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.family": "DejaVu Sans",
        "font.size": 12,
        "axes.titlesize": 17,
        "axes.titleweight": "bold",
        "axes.labelsize": 12.5,
        "xtick.color": "#555555",
        "ytick.color": "#555555",
        "axes.labelcolor": "#333333",
    })


# ----------------------------------------------------------------------------
# 4. CHART 1 - marginal-gain histogram (5 brackets, one color + accent)
# ----------------------------------------------------------------------------
def make_histogram(df: pd.DataFrame, edges: np.ndarray,
                   path: str = "chart1_marginal_gain_hist.png") -> None:
    gains = marginal_gain_by_bracket(df, edges)
    n = len(gains)
    x = np.arange(1, n + 1)

    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.bar(x, gains, color=SOFT_BLUE, edgecolor="white",
           linewidth=1.4, width=0.80, zorder=3)

    ax.set_title("Diminishing returns of wealth on happiness", loc="left", pad=14)

    # X-axis: label "Wealth", ticks show each bracket's dollar range.
    ax.set_xlabel("Wealth")
    ax.set_ylabel("Marginal happiness gained  (0\u201310 scale)")
    ax.set_xticks(x)
    ax.set_xticklabels([f"${edges[i]:.0f}\u2013{edges[i + 1]:.0f}k" for i in range(n)])
    ax.set_ylim(0, max(gains) * 1.18)
    ax.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    print(f"\nsaved {path}")


# ----------------------------------------------------------------------------
# 5. CHART 2 - era curves with a single kink line
# ----------------------------------------------------------------------------
def make_line_chart(df: pd.DataFrame,
                    path: str = "chart2_era_curves.pdf") -> None:
    q_edges = df["wealth"].quantile(np.linspace(0, 1, 26)).values
    centers = (q_edges[:-1] + q_edges[1:]) / 2

    def smooth(y, w=3):
        kern = np.ones(w) / w
        return np.convolve(np.pad(y, (w // 2, w // 2), mode="edge"), kern, mode="valid")

    fig, ax = plt.subplots(figsize=(10, 6.4))
    y_lo, y_hi = FLOOR - 0.3, 9.2

    for label, color in (("1980s", C_1980), ("2010s", C_2010)):
        sub = df[df.era == label].copy()
        sub["bin"] = pd.cut(sub["wealth"], bins=q_edges, include_lowest=True, labels=False)
        means = sub.groupby("bin")["happiness"].mean().reindex(
            range(len(centers))).interpolate().values
        ax.plot(centers, smooth(means), color=color, linewidth=3.2,
                solid_capstyle="round", label=label, zorder=3)

    # Single vertical line at the kink where the 2010s starts flattening faster.
    ax.axvline(KINK, color=SOFT_RED, linewidth=2.0, linestyle=(0, (4, 3)), zorder=2)
    ax.text(KINK + 4, y_hi - 0.15, f"Eras Diverge (~${KINK:.0f}k)",
            color=SOFT_RED, fontsize=10.5, ha="left", va="top", fontweight="bold")

    ax.set_title("Past ~$115k, extra wealth bought more happiness in the "
                 "1980s than the 2010s", loc="left", pad=14, fontsize=13.5)

    ax.set_xlabel("Wealth  ($1,000s)")
    ax.set_ylabel("Happiness  (0\u201310 scale)")
    ax.set_xlim(0, np.percentile(df["wealth"], 99))
    ax.set_ylim(y_lo, y_hi)

    leg = ax.legend(title="Era", frameon=False, loc="lower right",
                    fontsize=11.5, title_fontsize=12)
    leg._legend_box.align = "left"

    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")          # vector PDF
    print(f"saved {path}")


# ----------------------------------------------------------------------------
def main() -> None:
    df = generate_dataset()
    df.to_csv("wealth_happiness.csv", index=False)
    print(f"dataset: {len(df):,} rows, eras {list(ERAS)}  (kink at ${KINK:.0f}k)\n")

    edges = verify(df)

    apply_style()
    make_histogram(df, edges)
    make_line_chart(df)


if __name__ == "__main__":
    main()