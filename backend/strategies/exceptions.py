"""Custom exceptions for the strategy engine."""

from __future__ import annotations


class StrategyError(Exception):
    """Base exception for strategy engine errors."""


class InvalidStrategyError(StrategyError):
    """Raised when a strategy definition is invalid."""


class StrategyExecutionError(StrategyError):
    """Raised when a strategy cannot be executed."""
