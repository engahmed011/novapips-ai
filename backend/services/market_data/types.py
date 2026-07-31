"""Shared typing contracts and canonical data structures for market data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol


@dataclass(slots=True)
class PriceQuote:
    """Canonical representation of a current price snapshot."""

    symbol: str
    price: float
    currency: str = "USD"
    timestamp: datetime | None = None


@dataclass(slots=True)
class Candle:
    """Canonical OHLCV candle representation used by the service layer."""

    timestamp: datetime | None
    open: float
    high: float
    low: float
    close: float
    volume: float
    timeframe: str = "unknown"


@dataclass(slots=True)
class MarketStatus:
    """Canonical representation of market availability state."""

    is_open: bool
    status: str
    timestamp: datetime | None = None


class MarketDataProvider(Protocol):
    """Protocol for providers that can supply market data."""

    def get_current_price(self, symbol: str) -> Any:
        """Return a raw current price payload for the given symbol."""

    def get_candles(self, symbol: str, timeframe: str, limit: int = 100) -> list[Any]:
        """Return raw candle payloads for the given symbol and timeframe."""

    def get_market_status(self) -> Any:
        """Return a raw market status payload."""
