"""Facade service for market data access with caching and normalization."""

from __future__ import annotations

from threading import RLock
from typing import Any

from .cache import MarketDataCache
from .exceptions import (
    MarketDataNotAvailableError,
    UnsupportedTimeframeError,
)
from .normalizer import MarketDataNormalizer
from .types import Candle, MarketStatus, PriceQuote


class MarketDataService:
    """High-level service for retrieving normalized market data."""

    def __init__(
        self,
        provider: Any | None = None,
        cache: MarketDataCache | None = None,
        normalizer: MarketDataNormalizer | None = None,
    ) -> None:
        """Initialize the service with injectable dependencies."""
        self._provider = provider
        self._cache = cache or MarketDataCache()
        self._normalizer = normalizer or MarketDataNormalizer()
        self._lock = RLock()

    def get_current_price(self, symbol: str) -> PriceQuote:
        """Return the current normalized price for a symbol."""
        normalized_symbol = self._normalizer.normalize_symbol(symbol)
        with self._lock:
            cached = self._cache.get_current_price(normalized_symbol)
            if cached is not None:
                return cached
            if self._provider is None:
                raise MarketDataNotAvailableError("No provider configured.")
            raw_payload = self._provider.get_current_price(normalized_symbol)
            normalized = self._normalizer.normalize_price(normalized_symbol, raw_payload)
            self._cache.set_current_price(normalized_symbol, normalized)
            return normalized

    def get_candles(self, symbol: str, timeframe: str, limit: int = 100) -> list[Candle]:
        """Return normalized candles for the requested symbol and timeframe."""
        normalized_symbol = self._normalizer.normalize_symbol(symbol)
        normalized_timeframe = self._normalizer.normalize_timeframe(timeframe)
        if limit <= 0:
            raise ValueError("Limit must be positive.")

        with self._lock:
            cached = self._cache.get_candles(normalized_symbol, normalized_timeframe)
            if cached is not None:
                return list(cached)
            if self._provider is None:
                raise MarketDataNotAvailableError("No provider configured.")
            raw_payload = self._provider.get_candles(
                normalized_symbol,
                normalized_timeframe,
                limit=limit,
            )
            normalized = self._normalizer.normalize_candles(
                normalized_symbol,
                normalized_timeframe,
                raw_payload,
            )
            self._cache.set_candles(normalized_symbol, normalized_timeframe, normalized)
            return normalized

    def get_market_status(self) -> MarketStatus:
        """Return the current normalized market status."""
        with self._lock:
            cached = self._cache.get_market_status()
            if cached is not None:
                return cached
            if self._provider is None:
                raise MarketDataNotAvailableError("No provider configured.")
            raw_payload = self._provider.get_market_status()
            normalized = self._normalizer.normalize_market_status(raw_payload)
            self._cache.set_market_status(normalized)
            return normalized

    def refresh_cache(self) -> None:
        """Invalidate and refresh cached market data artifacts."""
        with self._lock:
            self._cache.clear()
