# happiness_wealth

> A tiny Python project that models how extra wealth buys less and less
> happiness — and how that curve *kinked* between the 1980s and the 2010s.

One self-contained script generates a synthetic, reproducible dataset and
renders two charts:

- **Chart 1 — marginal-gain histogram** (`chart1_marginal_gain_hist.png`):
  the marginal happiness gained per equal-width wealth bracket, both eras
  combined. The bars shrink left to right — classic diminishing returns.
- **Chart 2 — era curves** (`chart2_era_curves.pdf`): happiness vs. wealth
  for each era, sharing one curve until a *kink* (~$115k) where the 2010s
  starts flattening much faster than the 1980s.

## Install

```bash
pip install -e .
```

Runtime dependencies: **matplotlib, numpy, pandas**.

## Run

The package is self-contained — it generates its own data, so there's no
separate data-generation step:

```bash
# via the installed console script
happiness-wealth

# or as a module
python -m happiness_wealth.plots
```

Each run writes three files to the current directory:

| Output | What it is |
| --- | --- |
| `wealth_happiness.csv` | The generated dataset (`year, era, wealth, happiness`). |
| `chart1_marginal_gain_hist.png` | Marginal-gain histogram (raster). |
| `chart2_era_curves.pdf` | Era curves with the divergence line (vector). |

A committed sample of the dataset lives at `data/wealth_happiness.csv`.

## Use as a library

The building blocks are importable so you can generate data or draw a single
chart yourself:

```python
import happiness_wealth as hw

df = hw.generate_dataset()          # pandas DataFrame: year, era, wealth, happiness
edges = hw.bracket_edges(df, n=5)   # equal-width wealth brackets

hw.apply_style()                    # shared matplotlib styling
hw.make_histogram(df, edges, path="hist.png")
hw.make_line_chart(df, path="curves.pdf")
```

## API

| Function | Description |
| --- | --- |
| `generate_dataset()` | Build the synthetic era-split DataFrame (`year, era, wealth, happiness`). |
| `happiness_curve(wealth, era)` | The piecewise wealth→happiness model (shared below the kink, era-specific above). |
| `bracket_edges(df, n=5)` | Equal-width wealth-bracket edges (tail trimmed at the 98th pct). |
| `marginal_gain_by_bracket(df, edges)` | Mean happiness gained by each successive wealth bracket. |
| `apply_style()` | Apply the shared, minimal matplotlib style. |
| `make_histogram(df, edges, path=...)` | Render the marginal-gain histogram (Chart 1). |
| `make_line_chart(df, path=...)` | Render the era curves with the divergence line (Chart 2). |
| `main()` | Generate the data, print a verification summary, and write all three outputs. |

## File tree

```
.
├── happiness_wealth/
│   ├── __init__.py      # exposes the dataset + charting functions
│   └── plots.py         # data model, charts, and CLI entry point
├── data/
│   └── wealth_happiness.csv   # committed sample dataset
├── pyproject.toml
└── README.md
```

## License

MIT
