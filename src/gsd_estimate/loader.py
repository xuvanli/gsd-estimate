"""Data loading helpers for the :mod:`gsd_estimate` package."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Iterator, Sequence


class ColumnNotFoundError(RuntimeError):
    """Raised when a requested column is missing from an input file."""


def load_numeric_series(path: str | Path, *, column: str | int | None = None) -> Sequence[float]:
    """Load a sequence of positive numbers from a delimited text file.

    The loader is intentionally strict: all values must be parseable as
    floats and strictly greater than zero.  Violations surface
    immediately to keep downstream computations reliable.
    """

    path = Path(path)
    with path.open("r", newline="") as stream:
        reader = csv.DictReader(stream) if column is None or isinstance(column, str) else csv.reader(stream)

        if isinstance(reader, csv.DictReader):
            return tuple(_read_named_column(reader, column))

        return tuple(_read_positional_column(reader, int(column) if column is not None else 0))


def _read_named_column(reader: csv.DictReader, column: str | None) -> Iterator[float]:
    if column is None:
        # Default to the first column declared in the header.
        try:
            column = reader.fieldnames[0]  # type: ignore[index]
        except (TypeError, IndexError) as exc:  # pragma: no cover - handled via ValueError from csv
            raise ColumnNotFoundError("input file is missing a header row") from exc

    if column not in reader.fieldnames:
        raise ColumnNotFoundError(f"column '{column}' is not present in the file header")

    for row in reader:
        yield _parse_positive_float(row[column])


def _read_positional_column(reader: Iterable[Sequence[str]], column_index: int) -> Iterator[float]:
    for row in reader:
        try:
            value = row[column_index]
        except IndexError as exc:
            raise ColumnNotFoundError(f"column index {column_index} exceeds row width") from exc
        yield _parse_positive_float(value)


def _parse_positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise ValueError("geometric statistics require strictly positive samples")
    return parsed
