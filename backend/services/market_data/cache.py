"""Thread-safe cache abstractions for market data objects."""

from __future__ import annotations

import threading
from typing import Any

from .types import Candle, MarketStatus, PriceQuote


class MarketDataCache:
    """Thread-safe in-memory cache for market data artifacts."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._prices: dict[str, PriceQuote] = {}
        self._candles: dict[tuple[str, str], list[Candle]] = {}
        self._market_status: MarketStatus | None = None

    def get_current_price(self, symbol: str) -> PriceQuote | None:
        """Return a cached price quote for the given symbol if present."""
        with self._lock:
            return self._prices.get(symbol.upper())

    def set_current_price(self, symbol: str, price: PriceQuote) -> None:
        """Store a price quote in the cache."""
        with self._lock:
            self._prices[symbol.upper()] = price

    def get_candles(self, symbol: str, timeframe: str) -> list[Candle] | None:
        """Return cached candles for the given symbol and timeframe if present."""
        with self._lock:
            return self._candles.get((symbol.upper(), timeframe.lower()))

    def set_candles(self, symbol: str, timeframe: str, candles: list[Candle]) -> None:
        """Store candles in the cache."""
        with self._lock:
            self._candles[(symbol.upper(), timeframe.lower())] = list(candles)

    def get_market_status(self) -> MarketStatus | None:
        """Return the cached market status if present."""
        with self._lock:
            return self._market_status

    def set_market_status(self, status: MarketStatus) -> None:
        """Store a market status object in the cache."""
        with self._lock:
            self._market_status = status

    def clear(self) -> None:
        """Clear all cached market data artifacts."""
        with self._lock:
            self._prices.clear()
            self._candles.clear()
            self._market_status = None

    def snapshot(self) -> dict[str, Any]:
        """Return a shallow snapshot of current cache contents."""
        with self._lock:
            return {
                "prices": dict(self._prices),
                "candles": dict(self._candles),
                "market_status": self._market_status,
            }
