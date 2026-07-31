"""Mock data provider for testing and local development."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from backend.core.providers.base_provider import BaseDataProvider, Candle


class MockProvider(BaseDataProvider):
    """In-memory provider that returns deterministic fake market data."""

    name: str = "mock"

    def connect(self) -> None:
        """Establish the mock provider connection."""

    def disconnect(self) -> None:
        """Disconnect the mock provider."""

    def get_current_price(self, symbol: str) -> float:
        """Return a fake price for the requested symbol."""
        return 3375.42

    def get_candles(self, symbol: str, timeframe: str, limit: int = 100) -> list[Candle]:
        """Return sample OHLCV candles for the requested symbol."""
        now = datetime.now(timezone.utc)
        candles: list[Candle] = []
        base_price = 3375.42
        for index in range(limit):
            timestamp = now - timedelta(minutes=(limit - index) * 5)
            candles.append(
                Candle(
                    timestamp=timestamp,
                    open=base_price,
                    high=base_price + 0.25,
                    low=base_price - 0.15,
                    close=base_price + 0.10,
                    volume=1250.0 + index,
                )
            )
        return candles

    def get_spread(self, symbol: str) -> float:
        """Return a fake spread for the requested symbol."""
        return 0.18

    def is_market_open(self) -> bool:
        """Return whether the mock provider reports the market as open."""
        return True

    def get_server_time(self) -> datetime:
        """Return the mock provider server time as a UTC datetime."""
        return datetime.now(timezone.utc)

    def health_check(self) -> bool:
        """Return whether the mock provider is healthy."""
        return True
