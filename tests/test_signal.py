"""Tests for the Signal model."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from backend.models import Signal


def test_signal_valid_creation_and_risk_reward() -> None:
    """A signal should be created with normalized values and computed risk-reward."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    signal = Signal(
        symbol="eurusd",
        direction="BUY",
        entry=1.1000,
        stop_loss=1.0900,
        take_profit=1.1300,
        confidence=0.82,
        nova_score=0.91,
        timeframe="1h",
        created_at=timestamp,
    )

    assert signal.symbol == "EURUSD"
    assert signal.direction == "buy"
    assert signal.timeframe == "1H"
    assert signal.risk_reward() == pytest.approx(3.0)
    assert "Signal(" in repr(signal)


def test_signal_risk_reward_returns_infinity_when_levels_match() -> None:
    """A zero-risk setup should return infinity."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    signal = Signal(symbol="xauusd", direction="sell", entry=1900.0, stop_loss=1900.0, take_profit=1950.0, confidence=0.5, nova_score=0.6, timeframe="4h", created_at=timestamp)

    assert signal.risk_reward() == float("inf")


@pytest.mark.parametrize(
    ("symbol", "direction", "entry", "stop_loss", "take_profit", "confidence", "nova_score", "timeframe"),
    [
        ("", "buy", 1.0, 0.9, 1.1, 0.5, 0.5, "1h"),
        ("eurusd", "", 1.0, 0.9, 1.1, 0.5, 0.5, "1h"),
        ("eurusd", "buy", 0.0, 0.9, 1.1, 0.5, 0.5, "1h"),
        ("eurusd", "buy", 1.0, 0.0, 1.1, 0.5, 0.5, "1h"),
        ("eurusd", "buy", 1.0, 0.9, 0.0, 0.5, 0.5, "1h"),
        ("eurusd", "buy", 1.0, 0.9, 1.1, 1.5, 0.5, "1h"),
        ("eurusd", "buy", 1.0, 0.9, 1.1, 0.5, -0.1, "1h"),
        ("eurusd", "buy", 1.0, 0.9, 1.1, 0.5, 0.5, ""),
    ],
)
def test_signal_invalid_values_raise_value_error(symbol: str, direction: str, entry: float, stop_loss: float, take_profit: float, confidence: float, nova_score: float, timeframe: str) -> None:
    """The constructor should reject invalid signal values."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        Signal(symbol=symbol, direction=direction, entry=entry, stop_loss=stop_loss, take_profit=take_profit, confidence=confidence, nova_score=nova_score, timeframe=timeframe, created_at=timestamp)


def test_signal_rejects_naive_timestamp() -> None:
    """Timezone-naive timestamps should be rejected."""
    timestamp = datetime(2024, 1, 1, 12, 0)
    with pytest.raises(ValueError, match="timezone-aware"):
        Signal(symbol="eurusd", direction="buy", entry=1.1, stop_loss=1.0, take_profit=1.2, confidence=0.5, nova_score=0.5, timeframe="1h", created_at=timestamp)
