"""TradingView data provider architecture stub."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.core.providers.base_provider import BaseDataProvider, Candle


class TradingViewProvider(BaseDataProvider):
    """Architecture stub for a TradingView-backed market data provider."""

    name: str = "tradingview"

    def connect(self) -> None:
        """Establish a connection to the TradingView provider."""

    def disconnect(self) -> None:
        """Close the connection to the TradingView provider."""

    def get_current_price(self, symbol: str) -> float:
        """Return the current price for the requested symbol."""
        return 0.0

    def get_candles(self, symbol: str, timeframe: str, limit: int = 100) -> list[Candle]:
        """Return a list of OHLCV candles for the requested symbol."""
        return []

    def get_spread(self, symbol: str) -> float:
        """Return the current spread for the requested symbol."""
        return 0.0

    def is_market_open(self) -> bool:
        """Return whether the market is open for the provider."""
        return True

    def get_server_time(self) -> datetime:
        """Return the provider server time as a UTC datetime."""
        return datetime.now(timezone.utc)

    def health_check(self) -> bool:
        """Return whether the provider is ready for use."""
        return True
