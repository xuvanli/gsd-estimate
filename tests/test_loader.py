import csv
from pathlib import Path

import pytest

from gsd_estimate.loader import ColumnNotFoundError, load_numeric_series


def write_csv(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream)
        if headers:
            writer.writerow(headers)
        writer.writerows(rows)


def test_load_numeric_series_named_column(tmp_path: Path):
    csv_path = tmp_path / "data.csv"
    write_csv(
        csv_path,
        ["value", "note"],
        [["1", "a"], ["2", "b"], ["4", "c"]],
    )

    series = load_numeric_series(csv_path, column="value")
    assert series == (1.0, 2.0, 4.0)


def test_load_numeric_series_missing_column(tmp_path: Path):
    csv_path = tmp_path / "data.csv"
    write_csv(csv_path, ["value"], [["1"], ["2"]])

    with pytest.raises(ColumnNotFoundError):
        load_numeric_series(csv_path, column="other")


def test_load_numeric_series_positive_constraint(tmp_path: Path):
    csv_path = tmp_path / "data.csv"
    write_csv(csv_path, ["value"], [["1"], ["-1"]])

    with pytest.raises(ValueError):
        load_numeric_series(csv_path, column="value")
