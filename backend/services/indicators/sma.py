"""SMA indicator skeleton."""

from __future__ import annotations

from typing import Any

from backend.models import Candle

from .base_indicator import BaseIndicator
from .types import IndicatorResult


class SMAIndicator(BaseIndicator):
    """Skeleton SMA indicator with no business logic implementation."""

    NAME = "sma"

    def __init__(self) -> None:
        super().__init__(name=self.NAME)

    def calculate(self, candles: list[Candle], **params: Any) -> IndicatorResult:
        """Calculate the SMA result."""
        self.validate(candles)
        raise NotImplementedError("SMA calculation is not implemented in this architecture stub.")

    def required_periods(self) -> int:
        """Return the minimum period count required for SMA."""
        return 1
