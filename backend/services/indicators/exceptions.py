"""Custom exceptions for the indicator engine."""

from __future__ import annotations


class IndicatorError(Exception):
    """Base exception raised by the indicator subsystem."""


class InvalidIndicatorInputError(IndicatorError):
    """Raised when the input data is invalid for an indicator."""


class NotEnoughCandlesError(IndicatorError):
    """Raised when insufficient candles are provided for calculation."""
