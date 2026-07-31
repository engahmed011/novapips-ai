"""Thread-safe indicator engine for registering and executing indicators."""

from __future__ import annotations

import threading
from typing import Any, TypeVar

from backend.models import Candle

from .base_indicator import BaseIndicator
from .exceptions import IndicatorError, InvalidIndicatorInputError
from .types import IndicatorResult

TIndicatorClass = TypeVar("TIndicatorClass", bound=type[BaseIndicator])


class IndicatorEngine:
    """Registry and executor for technical indicators."""

    def __init__(self) -> None:
        """Initialize an empty engine with a lock for thread safety."""
        self._lock = threading.RLock()
        self._indicator_classes: dict[str, type[BaseIndicator]] = {}

    def register(self, indicator_cls: type[BaseIndicator]) -> None:
        """Register an indicator class in the engine."""
        if not isinstance(indicator_cls, type):
            raise InvalidIndicatorInputError("Indicator must be a class.")
        if not issubclass(indicator_cls, BaseIndicator):
            raise InvalidIndicatorInputError("Indicator must inherit from BaseIndicator.")

        indicator_name = getattr(indicator_cls, "NAME", None)
        if indicator_name is None:
            indicator_name = getattr(indicator_cls, "name", None)
        if not isinstance(indicator_name, str) or not indicator_name.strip():
            raise InvalidIndicatorInputError("Indicator class must define a non-empty NAME constant.")

        with self._lock:
            self._indicator_classes[indicator_name.lower()] = indicator_cls

    def register_indicator(self, indicator_cls: type[BaseIndicator]) -> None:
        """Backward-compatible alias for register."""
        self.register(indicator_cls)

    def remove(self, name: str) -> None:
        """Remove an indicator from the engine by name."""
        with self._lock:
            self._indicator_classes.pop(name.lower(), None)

    def remove_indicator(self, name: str) -> None:
        """Backward-compatible alias for remove."""
        self.remove(name)

    def get_indicator_class(self, name: str) -> type[BaseIndicator] | None:
        """Return a registered indicator class by name if present."""
        with self._lock:
            return self._indicator_classes.get(name.lower())

    def execute(self, name: str, candles: list[Candle], **params: Any) -> IndicatorResult:
        """Execute a single indicator calculation for the provided candles."""
        indicator_cls = self.get_indicator_class(name)
        if indicator_cls is None:
            raise IndicatorError(f"Indicator '{name}' is not registered.")
        return self._execute_indicator(indicator_cls, candles, **params)

    def run_many(self, names: list[str], candles: list[Candle], **params: Any) -> list[IndicatorResult]:
        """Execute multiple indicators in sequence and return their results."""
        results: list[IndicatorResult] = []
        for name in names:
            results.append(self.execute(name, candles, **params))
        return results

    def calculate_all(self, candles: list[Candle], **params: Any) -> dict[str, IndicatorResult]:
        """Execute every registered indicator and return the mapping of results."""
        with self._lock:
            indicator_classes = list(self._indicator_classes.items())

        results: dict[str, IndicatorResult] = {}
        for name, indicator_cls in indicator_classes:
            results[name] = self._execute_indicator(indicator_cls, candles, **params)
        return results

    def _execute_indicator(
        self,
        indicator_cls: type[BaseIndicator],
        candles: list[Candle],
        **params: Any,
    ) -> IndicatorResult:
        """Validate and execute an indicator instance without holding the registry lock."""
        indicator = indicator_cls()
        indicator.validate(candles)
        if len(candles) < indicator.required_periods():
            raise IndicatorError("Not enough candles for the requested indicator.")
        return indicator.calculate(candles, **params)

    def list_indicators(self) -> list[str]:
        """Return the names of all registered indicators."""
        with self._lock:
            return list(self._indicator_classes.keys())
