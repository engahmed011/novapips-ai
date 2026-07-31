"""Financial candle model used across the trading platform."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Candle:
    """Represents a single OHLCV candle for a financial instrument."""

    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: datetime

    def __post_init__(self) -> None:
        """Validate the candle values for consistency and positivity."""
        if not self.symbol.strip():
            raise ValueError("symbol cannot be empty")
        if not self.timeframe.strip():
            raise ValueError("timeframe cannot be empty")
        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        if self.open <= 0 or self.high <= 0 or self.low <= 0 or self.close <= 0:
            raise ValueError("price values must be positive")
        if self.low > self.high:
            raise ValueError("low cannot exceed high")
        if self.high < max(self.open, self.close):
            raise ValueError("high must be >= open and close")
        if self.low > min(self.open, self.close):
            raise ValueError("low must be <= open and close")
        if self.volume < 0:
            raise ValueError("volume cannot be negative")
        object.__setattr__(self, "symbol", self.symbol.strip().upper())
        object.__setattr__(self, "timeframe", self.timeframe.strip().upper())

    def is_bullish(self) -> bool:
        """Return True when the candle closes above its open price."""
        return self.close > self.open

    def is_bearish(self) -> bool:
        """Return True when the candle closes below its open price."""
        return self.close < self.open

    def body_size(self) -> float:
        """Return the absolute candle body size."""
        return abs(self.close - self.open)

    def upper_wick(self) -> float:
        """Return the upper wick size."""
        return self.high - max(self.open, self.close)

    def lower_wick(self) -> float:
        """Return the lower wick size."""
        return min(self.open, self.close) - self.low

    def range(self) -> float:
        """Return the total price range of the candle."""
        return self.high - self.low

    def __repr__(self) -> str:
        """Provide a concise, readable representation of the candle."""
        return (
            f"Candle(symbol={self.symbol!r}, timeframe={self.timeframe!r}, "
            f"open={self.open}, high={self.high}, low={self.low}, "
            f"close={self.close}, volume={self.volume}, timestamp={self.timestamp!r})"
        )
