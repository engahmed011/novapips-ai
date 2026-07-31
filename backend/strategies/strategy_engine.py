"""Thread-safe strategy engine for registering and executing strategies."""

from __future__ import annotations

import threading
from typing import Any

from .base_strategy import BaseStrategy
from .exceptions import InvalidStrategyError, StrategyError
from .types import StrategyContext, StrategyResult


class StrategyEngine:
    """Registry and executor for trading strategies."""

    def __init__(self) -> None:
        """Initialize the engine with an empty thread-safe registry."""
        self._lock = threading.RLock()
        self._strategies: dict[str, type[BaseStrategy]] = {}

    def register(self, strategy_cls: type[BaseStrategy]) -> None:
        """Register a strategy class in the engine."""
        if not isinstance(strategy_cls, type):
            raise InvalidStrategyError("Strategy must be a class.")
        if not issubclass(strategy_cls, BaseStrategy):
            raise InvalidStrategyError("Strategy must inherit from BaseStrategy.")

        name = getattr(strategy_cls, "NAME", None)
        if not isinstance(name, str) or not name.strip():
            raise InvalidStrategyError("Strategy class must define a non-empty NAME constant.")

        with self._lock:
            self._strategies[name.lower()] = strategy_cls

    def remove(self, name: str) -> None:
        """Remove a registered strategy by name."""
        with self._lock:
            self._strategies.pop(name.lower(), None)

    def execute(self, name: str, context: StrategyContext, **params: Any) -> StrategyResult:
        """Execute a single strategy for the provided context."""
        strategy_cls = self._get_strategy_class(name)
        if strategy_cls is None:
            raise StrategyError(f"Strategy '{name}' is not registered.")
        return self._execute_strategy(strategy_cls, context, **params)

    def execute_all(self, context: StrategyContext, **params: Any) -> dict[str, StrategyResult]:
        """Execute all registered strategies and return their results."""
        with self._lock:
            strategy_classes = list(self._strategies.items())

        results: dict[str, StrategyResult] = {}
        for strategy_name, strategy_cls in strategy_classes:
            results[strategy_name] = self._execute_strategy(strategy_cls, context, **params)
        return results

    def list(self) -> list[str]:
        """Return the registered strategy names."""
        with self._lock:
            return list(self._strategies.keys())

    def _get_strategy_class(self, name: str) -> type[BaseStrategy] | None:
        """Return a registered strategy class by name."""
        with self._lock:
            return self._strategies.get(name.lower())

    def _execute_strategy(
        self,
        strategy_cls: type[BaseStrategy],
        context: StrategyContext,
        **params: Any,
    ) -> StrategyResult:
        """Instantiate and execute a strategy without holding the registry lock."""
        strategy = strategy_cls()
        strategy.validate(context)
        if not strategy.enabled():
            raise StrategyError(f"Strategy '{strategy.name}' is disabled.")
        return strategy.calculate(context, **params)
