"""Abstract base class for all technical indicators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from backend.models import Candle

from .exceptions import IndicatorError, InvalidIndicatorInputError, NotEnoughCandlesError
from .types import IndicatorResult


class BaseIndicator(ABC):
    """Abstract contract for all indicators in the engine."""

    NAME: str = "indicator"

    def __init__(self, name: str | None = None) -> None:
        """Initialize the indicator with an optional override name."""
        self.name = name or self.__class__.NAME

    @abstractmethod
    def calculate(self, candles: list[Candle], **params: Any) -> IndicatorResult:
        """Calculate the indicator result for the provided candle history."""

    def validate(self, candles: list[Candle]) -> None:
        """Validate that the candle history is suitable for this indicator."""
        if not isinstance(candles, list):
            raise InvalidIndicatorInputError("Candles must be provided as a list.")
        if not candles:
            raise NotEnoughCandlesError("At least one candle is required.")
        if any(not isinstance(candle, Candle) for candle in candles):
            raise InvalidIndicatorInputError("Every candle must be an instance of Candle.")

    def required_periods(self) -> int:
        """Return the minimum number of candles required by the indicator."""
        return 1

    def _build_result(
        self,
        candles: list[Candle],
        values: dict[str, float] | None = None,
        **metadata: Any,
    ) -> IndicatorResult:
        """Create a standardized result object from calculated values."""
        if not candles:
            raise IndicatorError("Cannot build an indicator result without candles.")
        latest = candles[-1]
        return IndicatorResult(
            indicator_name=self.name,
            symbol=latest.symbol,
            timeframe=latest.timeframe,
            timestamp=latest.timestamp,
            values=values or {},
            metadata=dict(metadata),
        )
