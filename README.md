# vizlib

> A lightweight Python library for building clear, expressive data visualizations.

`vizlib` is a small, composable plotting toolkit that helps you go from a
DataFrame (or plain Python lists) to a polished chart in a couple of lines —
with sensible defaults, a consistent API, and full control when you need it.

---

## Features

- **Simple, consistent API** — every chart type follows the same `vizlib.<chart>(data, ...)` pattern.
- **Sensible defaults** — good-looking plots out of the box, no theme wrangling required.
- **Composable** — layer, facet, and annotate charts without fighting the library.
- **Works with what you have** — accepts pandas DataFrames, NumPy arrays, or plain lists/dicts.
- **Export anywhere** — save to PNG, SVG, or PDF, or show interactively.

## Installation

```bash
pip install vizlib
```

Or install the latest development version straight from source:

```bash
git clone https://github.com/seprisament/vizlib.git
cd vizlib
pip install -e .
```

### Requirements

- Python 3.9+
- `numpy`
- `pandas` (optional, for DataFrame support)

## Quick start

```python
import vizlib

data = {
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "sales": [120, 145, 132, 178],
}

chart = vizlib.bar(data, x="month", y="sales", title="Monthly Sales")
chart.show()
```

Save it to a file instead of displaying it:

```python
chart.save("sales.png", dpi=200)
```

## Examples

### Line chart

```python
import vizlib

chart = vizlib.line(
    df,
    x="date",
    y="temperature",
    color="city",
    title="Daily Temperature by City",
)
chart.show()
```

### Scatter plot

```python
chart = vizlib.scatter(
    df,
    x="height",
    y="weight",
    size="age",
    title="Height vs. Weight",
)
chart.show()
```

### Histogram

```python
chart = vizlib.histogram(df, x="score", bins=20)
chart.show()
```

## API overview

| Function | Description |
| --- | --- |
| `vizlib.line(data, x, y, ...)` | Line chart |
| `vizlib.bar(data, x, y, ...)` | Bar chart |
| `vizlib.scatter(data, x, y, ...)` | Scatter plot |
| `vizlib.histogram(data, x, bins, ...)` | Histogram |
| `vizlib.pie(data, values, labels, ...)` | Pie chart |

Every chart object supports:

- `.show()` — render the chart interactively
- `.save(path, ...)` — export to PNG, SVG, or PDF
- `.title(text)`, `.xlabel(text)`, `.ylabel(text)` — set labels fluently

## Development

Set up a local environment and run the tests:

```bash
git clone https://github.com/seprisament/vizlib.git
cd vizlib
pip install -e ".[dev]"
pytest
```

## Contributing

Contributions are welcome! Please open an issue to discuss significant
changes before submitting a pull request. For smaller fixes, feel free to
open a PR directly.

1. Fork the repository
2. Create a feature branch (`git checkout -b my-feature`)
3. Commit your changes
4. Push the branch and open a pull request

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.
