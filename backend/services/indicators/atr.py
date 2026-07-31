"""ATR indicator skeleton."""

from __future__ import annotations

from typing import Any

from backend.models import Candle

from .base_indicator import BaseIndicator
from .types import IndicatorResult


class ATRIndicator(BaseIndicator):
    """Skeleton ATR indicator with no business logic implementation."""

    NAME = "atr"

    def __init__(self) -> None:
        super().__init__(name=self.NAME)

    def calculate(self, candles: list[Candle], **params: Any) -> IndicatorResult:
        """Calculate the ATR result."""
        self.validate(candles)
        raise NotImplementedError("ATR calculation is not implemented in this architecture stub.")

    def required_periods(self) -> int:
        """Return the minimum period count required for ATR."""
        return 2
