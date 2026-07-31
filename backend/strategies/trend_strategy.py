"""Skeleton strategy for trend-following concepts."""

from __future__ import annotations

from typing import Any

from .base_strategy import BaseStrategy
from .types import StrategyContext, StrategyResult


class TrendStrategy(BaseStrategy):
    """Architecture-only scaffold for a trend strategy."""

    NAME = "trend"

    def calculate(self, context: StrategyContext, **params: Any) -> StrategyResult:
        """Calculate a strategy result."""
        self.validate(context)
        raise NotImplementedError("Trend strategy calculation is not implemented.")
