"""Shared dataclasses for strategy engine context and results."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True, frozen=True)
class StrategySignal:
    """Canonical representation of a strategy signal payload."""

    name: str
    direction: str
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class StrategyResult:
    """Canonical result emitted by a strategy execution."""

    strategy_name: str
    timestamp: datetime
    signal: StrategySignal | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class StrategyContext:
    """Canonical execution context passed into strategies."""

    symbol: str
    timeframe: str
    timestamp: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
