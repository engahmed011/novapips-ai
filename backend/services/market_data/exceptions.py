"""Custom exceptions for the market data service layer."""

from __future__ import annotations


class MarketDataError(Exception):
    """Base exception for all market data service errors."""


class MarketDataNotAvailableError(MarketDataError):
    """Raised when market data cannot be served without a provider."""


class InvalidSymbolError(MarketDataError):
    """Raised when a symbol is missing or malformed."""


class UnsupportedTimeframeError(MarketDataError):
    """Raised when a timeframe is not supported by the service contract."""


class CacheError(MarketDataError):
    """Raised when the cache cannot complete an operation."""
