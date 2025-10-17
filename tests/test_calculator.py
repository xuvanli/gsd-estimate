from math import exp, isclose, log

import pytest

from statistics import StatisticsError

from gsd_estimate.calculator import GSDStatistics, compute_gsd


def test_compute_gsd_basic():
    samples = [1.0, 2.0, 4.0]
    stats = compute_gsd(samples)
    assert stats.sample_size == 3
    assert isclose(stats.geometric_mean, 2.0, rel_tol=1e-9)
    expected_gsd = exp(log(2))
    assert isclose(stats.geometric_standard_deviation, expected_gsd, rel_tol=1e-9)


def test_from_samples_requires_positive_values():
    with pytest.raises(StatisticsError):
        GSDStatistics.from_samples([1.0, 0.0])


def test_from_samples_requires_minimum_sample_size():
    with pytest.raises(StatisticsError):
        GSDStatistics.from_samples([1.0])
