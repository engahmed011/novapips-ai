"""Abstract base class for all trading strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .exceptions import InvalidStrategyError, StrategyExecutionError
from .types import StrategyContext, StrategyResult


class BaseStrategy(ABC):
    """Abstract contract for strategies in the strategy engine."""

    NAME: str = "strategy"

    def __init__(self, name: str | None = None) -> None:
        """Initialize the strategy with an optional runtime name override."""
        if name is not None:
            self.name = name
        else:
            self.name = self.__class__.NAME

    @abstractmethod
    def calculate(self, context: StrategyContext, **params: Any) -> StrategyResult:
        """Calculate a strategy result for the provided context."""

    def validate(self, context: StrategyContext) -> None:
        """Validate the strategy context before execution."""
        if not isinstance(context, StrategyContext):
            raise InvalidStrategyError("Context must be an instance of StrategyContext.")
        if not context.symbol.strip():
            raise InvalidStrategyError("Context symbol must not be empty.")
        if not context.timeframe.strip():
            raise InvalidStrategyError("Context timeframe must not be empty.")

    def priority(self) -> int:
        """Return the execution priority of the strategy."""
        return 100

    def enabled(self) -> bool:
        """Return whether the strategy is enabled for execution."""
        return True

    def _build_result(self, context: StrategyContext, signal: StrategySignal | None = None, **metadata: Any) -> StrategyResult:
        """Create a standardized strategy result."""
        if not isinstance(context, StrategyContext):
            raise StrategyExecutionError("Cannot build a result from an invalid context.")
        return StrategyResult(
            strategy_name=self.name,
            timestamp=context.timestamp,
            signal=signal,
            metadata=dict(metadata),
        )
