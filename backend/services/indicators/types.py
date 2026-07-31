"""Shared typing contracts for indicator results and engine interactions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True, frozen=True)
class IndicatorResult:
    """Canonical result emitted by an indicator calculation."""

    indicator_name: str
    symbol: str
    timeframe: str
    timestamp: datetime
    values: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def value(self) -> float | None:
        """Return the primary scalar value for backward compatibility."""
        if not self.values:
            return None
        return next(iter(self.values.values()))
