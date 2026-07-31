"""Skeleton strategy for breakout concepts."""

from __future__ import annotations

from typing import Any

from .base_strategy import BaseStrategy
from .types import StrategyContext, StrategyResult


class BreakoutStrategy(BaseStrategy):
    """Architecture-only scaffold for a breakout strategy."""

    NAME = "breakout"

    def calculate(self, context: StrategyContext, **params: Any) -> StrategyResult:
        """Calculate a strategy result."""
        self.validate(context)
        raise NotImplementedError("Breakout strategy calculation is not implemented.")
