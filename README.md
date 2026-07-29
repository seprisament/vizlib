# happiness_wealth

> A tiny, locally-installable Python library for visualizing the relationship between wealth and happiness.

Three plain functions, one matplotlib dependency, no pandas/numpy. Plots a
scatter of wealth vs. happiness with a hand-fitted trend line, a line chart
showing the classic diminishing-returns curve, and a histogram of happiness
split by wealth group.

## Install

```bash
pip install -e .
```

**matplotlib is the only runtime dependency.**

## Generate the data

A standard-library-only script generates a realistic, reproducible dataset
(positive-but-noisy correlation with a diminishing-returns shape) and writes
it to `data/happiness_wealth.csv`:

```bash
python generate_data.py
```

The amount of data (`N`) and the random `SEED` are constants at the top of
`generate_data.py` — edit them, or call `generate(n=..., seed=...)` directly.

## End-to-end example

```python
import happiness_wealth as hw

# 1. Load the generated CSV into plain lists (dict with "wealth"/"happiness").
data = hw.load_csv("data/happiness_wealth.csv")

# 2. Scatter of wealth vs. happiness with a fitted trend line.
fig1 = hw.scatter_trend(data["wealth"], data["happiness"],
                        title="Wealth vs. Happiness",
                        save_path="scatter.png")

# 3. The diminishing-returns curve (runs with no data at all).
fig2 = hw.diminishing_returns(save_path="diminishing.png")

# 4. Histogram of happiness, split into low/middle/high wealth groups.
fig3 = hw.happiness_histogram(data["wealth"], data["happiness"],
                              save_path="histogram.png")

# Show them interactively instead of / in addition to saving:
import matplotlib.pyplot as plt
plt.show()
```

## API

| Function | Description |
| --- | --- |
| `load_csv(path="data/happiness_wealth.csv")` | Read the CSV into `{"wealth": [...], "happiness": [...]}`. |
| `scatter_trend(wealth, happiness, title=..., save_path=None)` | Scatter plot with a plain least-squares trend line. |
| `diminishing_returns(wealth=None, model=None, title=..., save_path=None)` | Line chart of happiness rising then flattening. |
| `happiness_histogram(wealth, happiness, edges=None, bins=10, ...)` | Overlaid happiness histogram, split by wealth group (tertiles by default). |

Every plotting function returns the matplotlib `Figure`, and writes a PNG
when given `save_path`.

## File tree

```
.
├── happiness_wealth/
│   ├── __init__.py      # exposes load_csv + the three plotting functions
│   ├── loader.py        # load_csv
│   └── plots.py         # the three visualization functions
├── data/
│   └── happiness_wealth.csv   # sample generated dataset
├── generate_data.py     # standard-library data generator
├── pyproject.toml
└── README.md
```

## License

MIT
