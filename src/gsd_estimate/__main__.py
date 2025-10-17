"""Command line interface for computing geometric statistics."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .calculator import compute_gsd
from .loader import load_numeric_series


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute geometric statistics (mean, deviation) for a column of numeric data.",
    )
    parser.add_argument("path", type=Path, help="Path to a CSV file containing numeric samples.")
    parser.add_argument(
        "--column",
        help="Column name or zero-based index to read. Defaults to the first column.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        series = load_numeric_series(args.path, column=_parse_column(args.column))
        stats = compute_gsd(series)
    except Exception as exc:  # pragma: no cover - CLI level error reporting
        parser.error(str(exc))
        return 2

    print("Sample size:", stats.sample_size)
    print("Geometric mean:", f"{stats.geometric_mean:.5f}")
    print("Geometric SD:", f"{stats.geometric_standard_deviation:.5f}")
    print("Geometric CV (%):", f"{stats.geometric_coefficient_of_variation:.2f}")
    return 0


def _parse_column(raw: str | None) -> str | int | None:
    if raw is None:
        return None

    try:
        return int(raw)
    except ValueError:
        return raw


if __name__ == "__main__":
    sys.exit(main())
