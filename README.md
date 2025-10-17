# gsd-estimate

A lightweight toolkit for computing geometric statistics from CSV data.

## Features

- `GSDStatistics` dataclass that encapsulates geometric mean, geometric
  standard deviation (GSD) and geometric coefficient of variation (GCV)
  for a set of samples.
- File loading helpers that validate numeric columns before performing
  calculations.
- Command line interface for quick one-off analysis.

## Usage

1. Install the project in editable mode:

   ```bash
   pip install -e .[dev]
   ```

2. Run the CLI against a CSV file:

   ```bash
   gsd-estimate data.csv --column value
   ```

3. Use the Python API:

   ```python
   from gsd_estimate import compute_gsd

   stats = compute_gsd([1.0, 2.0, 4.0])
   print(stats.geometric_mean)
   ```

## Development

Tests are powered by `pytest`:

```bash
pytest
```
