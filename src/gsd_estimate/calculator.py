"""Utilities for computing geometric standard deviation statistics.

The geometric standard deviation (GSD) is often preferred over the
classical (arithmetic) standard deviation when the underlying data is
log-normally distributed.  This module contains a high level data class
that encapsulates the key statistics derived from a sample collection.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, sqrt
from statistics import StatisticsError
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class GSDStatistics:
    """Container for statistics derived from a log-normal sample.

    Attributes
    ----------
    geometric_mean:
        The exponential of the average log value.  Equivalent to the
        central tendency of the sample in log-space.
    geometric_standard_deviation:
        Multiplicative factor that describes the spread of the
        distribution.  Values larger than ``1`` indicate larger spread.
    geometric_coefficient_of_variation:
        Normalised measure of spread sometimes used by occupational
        hygienists.  Expressed as a percentage.
    sample_size:
        Total number of observations used to compute the statistics.
    """

    geometric_mean: float
    geometric_standard_deviation: float
    geometric_coefficient_of_variation: float
    sample_size: int

    @classmethod
    def from_samples(cls, samples: Sequence[float]) -> "GSDStatistics":
        """Create :class:`GSDStatistics` from a sequence of samples.

        Parameters
        ----------
        samples:
            Sequence of positive floating point values.  The samples are
            validated to ensure they are strictly positive since the
            geometric mean is undefined for non-positive numbers.

        Returns
        -------
        GSDStatistics
            A populated data class instance.

        Raises
        ------
        StatisticsError
            If fewer than two samples are provided or a non-positive
            value is encountered.
        """

        _validate_samples(samples)

        log_values = [math_log(value) for value in samples]
        log_mean = sum(log_values) / len(log_values)

        # The geometric mean is just exp of the average of log values.
        geometric_mean = exp(log_mean)

        # Compute the population standard deviation in log space.
        squared_diffs = [(value - log_mean) ** 2 for value in log_values]
        log_variance = sum(squared_diffs) / (len(log_values) - 1)
        geometric_standard_deviation = exp(sqrt(log_variance))

        # GCV expresses the spread as a percentage.  The formula is a
        # widely-used approximation that remains stable for small spreads.
        spread_term = max(0.0, geometric_standard_deviation**2 - 1.0)
        geometric_coefficient_of_variation = sqrt(spread_term) * 100

        return cls(
            geometric_mean=geometric_mean,
            geometric_standard_deviation=geometric_standard_deviation,
            geometric_coefficient_of_variation=geometric_coefficient_of_variation,
            sample_size=len(samples),
        )


def compute_gsd(samples: Iterable[float]) -> GSDStatistics:
    """Convenience wrapper around :meth:`GSDStatistics.from_samples`.

    Parameters
    ----------
    samples:
        Any iterable of sample values.  The values are materialised into
        a tuple to allow validation and reuse.
    """

    materialised = tuple(samples)
    return GSDStatistics.from_samples(materialised)


def _validate_samples(samples: Sequence[float]) -> None:
    """Validate input data prior to computing statistics.

    The helper raises :class:`StatisticsError` whenever the data does not
    satisfy the contract required by the geometric standard deviation.
    A separate function keeps the validation logic centralised and
    unit-testable.
    """

    if len(samples) < 2:
        raise StatisticsError("at least two samples are required to estimate spread")

    if any(value <= 0 for value in samples):
        raise StatisticsError("geometric statistics require strictly positive samples")


# The logarithm helper is defined at module level so that it can be easily
# patched during testing should the need arise (for example to simulate
# floating point errors).
def math_log(value: float) -> float:
    from math import log

    return log(value)
