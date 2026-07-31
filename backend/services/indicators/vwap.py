"""VWAP indicator skeleton."""

from __future__ import annotations

from typing import Any

from backend.models import Candle

from .base_indicator import BaseIndicator
from .types import IndicatorResult


class VWAPIndicator(BaseIndicator):
    """Skeleton VWAP indicator with no business logic implementation."""

    NAME = "vwap"

    def __init__(self) -> None:
        super().__init__(name=self.NAME)

    def calculate(self, candles: list[Candle], **params: Any) -> IndicatorResult:
        """Calculate the VWAP result."""
        self.validate(candles)
        raise NotImplementedError("VWAP calculation is not implemented in this architecture stub.")

    def required_periods(self) -> int:
        """Return the minimum period count required for VWAP."""
        return 1
