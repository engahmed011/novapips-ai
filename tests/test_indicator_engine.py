"""Tests for the indicator engine architecture."""

from __future__ import annotations

from datetime import datetime, timezone

from backend.models import Candle
from backend.services.indicators.base_indicator import BaseIndicator
from backend.services.indicators.indicator_engine import IndicatorEngine
from backend.services.indicators.types import IndicatorResult


class StubIndicator(BaseIndicator):
    """Test double for validating engine behavior."""

    NAME = "stub"

    def __init__(self) -> None:
        super().__init__(name=self.NAME)

    def calculate(self, candles: list[Candle], **params: object) -> IndicatorResult:
        """Return a deterministic result for tests."""
        self.validate(candles)
        period = int(params.get("period", 1))
        return self._build_result(candles, {"stub": float(period)}, period=period)

    def required_periods(self) -> int:
        """Return the minimum candles required."""
        return 1


def _make_candles() -> list[Candle]:
    """Create a minimal candle history for tests."""
    now = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return [
        Candle(
            symbol="EURUSD",
            timeframe="M1",
            open=100.0,
            high=101.0,
            low=99.0,
            close=100.5,
            volume=10.0,
            timestamp=now,
        )
    ]


def test_engine_registers_indicator_classes_and_executes_with_params() -> None:
    """The engine should register classes and pass execution parameters through."""
    engine = IndicatorEngine()
    engine.register(StubIndicator)

    result = engine.execute("stub", _make_candles(), period=5)

    assert result.indicator_name == "stub"
    assert result.values["stub"] == 5.0


def test_engine_calculate_all_returns_results_by_name() -> None:
    """The engine should execute every registered indicator and return a mapping."""
    engine = IndicatorEngine()
    engine.register(StubIndicator)

    results = engine.calculate_all(_make_candles(), period=7)

    assert list(results.keys()) == ["stub"]
    assert results["stub"].values["stub"] == 7.0
