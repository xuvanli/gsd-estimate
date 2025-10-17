"""Public package interface for :mod:`gsd_estimate`.

This package exposes convenience functions for computing the geometric
standard deviation (GSD) and related descriptive statistics from a
collection of strictly-positive samples.
"""

from .calculator import GSDStatistics, compute_gsd
from .loader import load_numeric_series

__all__ = ["GSDStatistics", "compute_gsd", "load_numeric_series"]
