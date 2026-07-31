"""Trade model representing an executed trading position."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(slots=True, frozen=True)
class Trade:
    """Represents a completed or open trade position."""

    symbol: str
    direction: str
    entry: float
    exit: float | None
    profit_loss: float | None
    opened_at: datetime
    closed_at: datetime | None
    status: Literal["open", "closed", "pending"]

    def __post_init__(self) -> None:
        """Validate trade state and normalize simple values."""
        if not self.symbol.strip():
            raise ValueError("symbol cannot be empty")
        if not self.direction.strip():
            raise ValueError("direction cannot be empty")
        if self.entry <= 0:
            raise ValueError("entry must be positive")
        if self.exit is not None and self.exit <= 0:
            raise ValueError("exit must be positive when provided")
        if self.profit_loss is not None and not isinstance(self.profit_loss, (int, float)):
            raise ValueError("profit_loss must be numeric when provided")
        if self.opened_at.tzinfo is None:
            raise ValueError("opened_at must be timezone-aware")
        if self.closed_at is not None and self.closed_at.tzinfo is None:
            raise ValueError("closed_at must be timezone-aware when provided")
        if self.closed_at is not None and self.closed_at < self.opened_at:
            raise ValueError("closed_at cannot be before opened_at")
        if self.status not in {"open", "closed", "pending"}:
            raise ValueError("status must be open, closed, or pending")
        object.__setattr__(self, "symbol", self.symbol.strip().upper())
        object.__setattr__(self, "direction", self.direction.strip().lower())

    def duration(self) -> float | None:
        """Return the trade duration in seconds when the trade is closed."""
        if self.closed_at is None:
            return None
        return (self.closed_at - self.opened_at).total_seconds()

    def is_winner(self) -> bool | None:
        """Return True for winning trades, False for losing trades, and None for open trades."""
        if self.profit_loss is None:
            return None
        return self.profit_loss > 0

    def __repr__(self) -> str:
        """Provide a concise, readable representation of the trade."""
        return (
            f"Trade(symbol={self.symbol!r}, direction={self.direction!r}, entry={self.entry}, "
            f"exit={self.exit}, profit_loss={self.profit_loss}, opened_at={self.opened_at!r}, "
            f"closed_at={self.closed_at!r}, status={self.status!r})"
        )
