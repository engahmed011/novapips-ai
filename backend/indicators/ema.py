"""Exponential Moving Average (EMA) indicator implementation."""

from __future__ import annotations

from typing import Any

from backend.models import Candle
from backend.services.indicators.base_indicator import BaseIndicator
from backend.services.indicators.exceptions import (
    InvalidIndicatorInputError,
    NotEnoughCandlesError,
)
from backend.services.indicators.types import IndicatorResult


class EMAIndicator(BaseIndicator):
    """Pure-Python EMA indicator implementation for candle series."""

    NAME = "ema"

    def __init__(self, period: int = 20) -> None:
        """Initialize the EMA indicator with a positive period."""
        super().__init__(name=self.NAME)
        if not isinstance(period, int):
            raise InvalidIndicatorInputError("Period must be an integer.")
        if period <= 0:
            raise InvalidIndicatorInputError("Period must be greater than zero.")
        self._period = period

    @property
    def period(self) -> int:
        """Return the configured EMA period."""
        return self._period

    def calculate(self, candles: list[Candle], **params: Any) -> IndicatorResult:
        """Calculate the EMA for the provided candle history."""
        self.validate(candles)

        if len(candles) < self._period:
            raise NotEnoughCandlesError(
                f"At least {self._period} candles are required for EMA."
            )

        candles = sorted(candles, key=lambda candle: candle.timestamp)

        multiplier = 2.0 / (self._period + 1.0)
        initial_value = sum(candle.close for candle in candles[: self._period]) / float(self._period)
        ema_value = initial_value
        for candle in candles[self._period :]:
            ema_value = ((candle.close - ema_value) * multiplier) + ema_value

        return self._build_result(candles, values={"ema": ema_value}, period=self._period)

    def required_periods(self) -> int:
        """Return the minimum number of candles required for EMA."""
        return self._period
