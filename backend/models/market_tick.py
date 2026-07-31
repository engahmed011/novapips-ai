"""Market tick model representing the latest bid/ask quote."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class MarketTick:
    """Represents the latest quote snapshot from a market provider."""

    symbol: str
    bid: float
    ask: float
    spread: float
    provider: str
    timestamp: datetime

    def __post_init__(self) -> None:
        """Validate quote values and ensure the spread is consistent."""
        if not self.symbol.strip():
            raise ValueError("symbol cannot be empty")
        if not self.provider.strip():
            raise ValueError("provider cannot be empty")
        if self.bid <= 0 or self.ask <= 0:
            raise ValueError("bid and ask must be positive")
        if self.ask < self.bid:
            raise ValueError("ask must be >= bid")
        if self.spread < 0:
            raise ValueError("spread cannot be negative")
        if abs(self.spread - (self.ask - self.bid)) > 1e-9:
            raise ValueError("spread must equal ask - bid")
        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        object.__setattr__(self, "symbol", self.symbol.strip().upper())
        object.__setattr__(self, "provider", self.provider.strip())

    def mid_price(self) -> float:
        """Return the midpoint between bid and ask."""
        return (self.bid + self.ask) / 2.0

    def __repr__(self) -> str:
        """Provide a concise, readable representation of the market tick."""
        return (
            f"MarketTick(symbol={self.symbol!r}, bid={self.bid}, ask={self.ask}, "
            f"spread={self.spread}, provider={self.provider!r}, timestamp={self.timestamp!r})"
        )
