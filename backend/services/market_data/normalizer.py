"""Normalization utilities for converting provider payloads into canonical types."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from .exceptions import InvalidSymbolError, UnsupportedTimeframeError
from .types import Candle, MarketStatus, PriceQuote


class MarketDataNormalizer:
    """Normalize provider payloads into stable, typed domain objects."""

    def normalize_symbol(self, symbol: str) -> str:
        """Normalize and validate a market symbol."""
        normalized = symbol.strip().upper()
        if not normalized:
            raise InvalidSymbolError("Symbol must not be empty.")
        return normalized

    def normalize_timeframe(self, timeframe: str) -> str:
        """Normalize and validate a timeframe value."""
        normalized = timeframe.strip().lower()
        if not normalized:
            raise UnsupportedTimeframeError("Timeframe must not be empty.")
        return normalized

    def normalize_price(self, symbol: str, raw_value: Any) -> PriceQuote:
        """Convert a raw price payload into a canonical price quote."""
        normalized_symbol = self.normalize_symbol(symbol)
        if isinstance(raw_value, Mapping):
            price = raw_value.get("price")
            timestamp = raw_value.get("timestamp")
            currency = str(raw_value.get("currency", "USD")).upper()
        else:
            price = raw_value
            timestamp = None
            currency = "USD"

        price_value = float(price)
        if price_value <= 0:
            raise ValueError("Price must be positive.")

        return PriceQuote(
            symbol=normalized_symbol,
            price=price_value,
            currency=currency,
            timestamp=self._coerce_timestamp(timestamp),
        )

    def normalize_candles(
        self,
        symbol: str,
        timeframe: str,
        raw_items: Any,
    ) -> list[Candle]:
        """Convert raw candle payloads into a list of canonical candles."""
        normalized_symbol = self.normalize_symbol(symbol)
        normalized_timeframe = self.normalize_timeframe(timeframe)
        if raw_items is None:
            return []

        candles: list[Candle] = []
        for raw_item in raw_items:
            if not isinstance(raw_item, Mapping):
                raise TypeError("Each candle payload must be a mapping.")
            candles.append(
                Candle(
                    timestamp=self._coerce_timestamp(raw_item.get("timestamp")),
                    open=float(raw_item.get("open", 0.0)),
                    high=float(raw_item.get("high", 0.0)),
                    low=float(raw_item.get("low", 0.0)),
                    close=float(raw_item.get("close", 0.0)),
                    volume=float(raw_item.get("volume", 0.0)),
                    timeframe=normalized_timeframe,
                )
            )

        return candles

    def normalize_market_status(self, raw_value: Any) -> MarketStatus:
        """Convert a raw market status payload into a canonical status object."""
        if isinstance(raw_value, Mapping):
            is_open = bool(raw_value.get("is_open", False))
            status = str(raw_value.get("status", "unknown")).strip() or "unknown"
            timestamp = raw_value.get("timestamp")
        else:
            is_open = bool(raw_value)
            status = "unknown"
            timestamp = None

        return MarketStatus(
            is_open=is_open,
            status=status,
            timestamp=self._coerce_timestamp(timestamp),
        )

    def _coerce_timestamp(self, value: Any) -> datetime | None:
        """Best-effort conversion of various timestamp values to datetime."""
        if value is None or isinstance(value, datetime):
            return value
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(float(value), tz=timezone.utc)
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None
        return None
