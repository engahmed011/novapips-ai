"""Skeleton strategy for smart money concepts."""

from __future__ import annotations

from typing import Any

from .base_strategy import BaseStrategy
from .types import StrategyContext, StrategyResult


class SmartMoneyStrategy(BaseStrategy):
    """Architecture-only scaffold for a smart money strategy."""

    NAME = "smart_money"

    def calculate(self, context: StrategyContext, **params: Any) -> StrategyResult:
        """Calculate a strategy result."""
        self.validate(context)
        raise NotImplementedError("Smart money strategy calculation is not implemented.")
