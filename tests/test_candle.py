"""Tests for the Candle model."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from backend.models import Candle


def test_candle_valid_creation_and_helpers() -> None:
    """A candle should be created with normalized values and helper methods."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    candle = Candle(
        symbol="eurusd",
        timeframe="1h",
        open=1.1000,
        high=1.1200,
        low=1.0900,
        close=1.1150,
        volume=1200.5,
        timestamp=timestamp,
    )

    assert candle.symbol == "EURUSD"
    assert candle.timeframe == "1H"
    assert candle.is_bullish() is True
    assert candle.is_bearish() is False
    assert candle.body_size() == pytest.approx(0.0150)
    assert candle.upper_wick() == pytest.approx(0.0050)
    assert candle.lower_wick() == pytest.approx(0.0100)
    assert candle.range() == pytest.approx(0.0300)
    assert "Candle(" in repr(candle)


@pytest.mark.parametrize(
    ("symbol", "timeframe", "open", "high", "low", "close", "volume"),
    [
        ("", "1h", 1.0, 1.1, 1.0, 1.05, 10.0),
        ("eurusd", "", 1.0, 1.1, 1.0, 1.05, 10.0),
        ("eurusd", "1h", 0.0, 1.1, 1.0, 1.05, 10.0),
        ("eurusd", "1h", 1.0, 1.1, 1.2, 1.05, 10.0),
        ("eurusd", "1h", 1.0, 1.1, 1.15, 1.05, 10.0),
        ("eurusd", "1h", 1.0, 1.1, 1.0, 1.2, 10.0),
        ("eurusd", "1h", 1.0, 1.1, 1.0, 1.05, -1.0),
    ],
)
def test_candle_invalid_values_raise_value_error(symbol: str, timeframe: str, open: float, high: float, low: float, close: float, volume: float) -> None:
    """The constructor should reject invalid candle data."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        Candle(symbol=symbol, timeframe=timeframe, open=open, high=high, low=low, close=close, volume=volume, timestamp=timestamp)


def test_candle_rejects_naive_timestamp() -> None:
    """Timezone-naive timestamps should be rejected."""
    timestamp = datetime(2024, 1, 1, 12, 0)
    with pytest.raises(ValueError, match="timezone-aware"):
        Candle(symbol="eurusd", timeframe="1h", open=1.0, high=1.1, low=1.0, close=1.05, volume=10.0, timestamp=timestamp)


def test_candle_handles_doji_shape() -> None:
    """A candle with equal open and close should be neutral."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    candle = Candle(symbol="xauusd", timeframe="4h", open=1900.0, high=1910.0, low=1890.0, close=1900.0, volume=50.0, timestamp=timestamp)

    assert candle.is_bullish() is False
    assert candle.is_bearish() is False
    assert candle.body_size() == 0.0
    assert candle.upper_wick() == 10.0
    assert candle.lower_wick() == 10.0
