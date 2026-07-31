"""News event model for economic and market-moving announcements."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class NewsEvent:
    """Represents an economic or market news event."""

    title: str
    currency: str
    impact: str
    time: datetime
    description: str

    def __post_init__(self) -> None:
        """Validate the news event payload and normalize simple fields."""
        if not self.title.strip():
            raise ValueError("title cannot be empty")
        if not self.currency.strip():
            raise ValueError("currency cannot be empty")
        if not self.description.strip():
            raise ValueError("description cannot be empty")
        if not self.impact.strip():
            raise ValueError("impact cannot be empty")
        if self.time.tzinfo is None:
            raise ValueError("time must be timezone-aware")
        normalized_impact = self.impact.strip().lower()
        if normalized_impact not in {"low", "medium", "high"}:
            raise ValueError("impact must be low, medium, or high")
        object.__setattr__(self, "currency", self.currency.strip().upper())
        object.__setattr__(self, "impact", normalized_impact)

    def is_high_impact(self) -> bool:
        """Return True when the event is marked as high impact."""
        return self.impact == "high"

    def __repr__(self) -> str:
        """Provide a concise, readable representation of the news event."""
        return (
            f"NewsEvent(title={self.title!r}, currency={self.currency!r}, "
            f"impact={self.impact!r}, time={self.time!r}, description={self.description!r})"
        )
