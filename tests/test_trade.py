"""Tests for the Trade model."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from backend.models import Trade


def test_trade_valid_creation_for_open_and_closed_positions() -> None:
    """A trade should support open and closed states with helper methods."""
    opened_at = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    closed_at = datetime(2024, 1, 1, 11, 30, tzinfo=timezone.utc)
    closed_trade = Trade(symbol="eurusd", direction="buy", entry=1.1000, exit=1.1150, profit_loss=150.0, opened_at=opened_at, closed_at=closed_at, status="closed")
    open_trade = Trade(symbol="eurusd", direction="buy", entry=1.1000, exit=None, profit_loss=None, opened_at=opened_at, closed_at=None, status="open")

    assert closed_trade.is_winner() is True
    assert closed_trade.duration() == pytest.approx(5400.0)
    assert open_trade.is_winner() is None
    assert open_trade.duration() is None
    assert "Trade(" in repr(closed_trade)


@pytest.mark.parametrize(
    ("symbol", "direction", "entry", "exit", "profit_loss", "status"),
    [
        ("", "buy", 1.1, 1.2, 10.0, "open"),
        ("eurusd", "", 1.1, 1.2, 10.0, "open"),
        ("eurusd", "buy", 0.0, 1.2, 10.0, "open"),
        ("eurusd", "buy", 1.1, 0.0, 10.0, "open"),
        ("eurusd", "buy", 1.1, 1.2, "bad", "open"),
        ("eurusd", "buy", 1.1, 1.2, 10.0, "invalid"),
    ],
)
def test_trade_invalid_values_raise_value_error(symbol: str, direction: str, entry: float, exit: float | None, profit_loss: object, status: str) -> None:
    """The constructor should reject invalid trade state."""
    opened_at = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        Trade(symbol=symbol, direction=direction, entry=entry, exit=exit, profit_loss=profit_loss, opened_at=opened_at, closed_at=None, status=status)


def test_trade_rejects_naive_datetimes_and_ordering() -> None:
    """Trade timestamps should be timezone-aware and ordered."""
    opened_at = datetime(2024, 1, 1, 10, 0)
    with pytest.raises(ValueError, match="timezone-aware"):
        Trade(symbol="eurusd", direction="buy", entry=1.1, exit=1.2, profit_loss=10.0, opened_at=opened_at, closed_at=None, status="open")

    opened_at = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    closed_at = datetime(2024, 1, 1, 9, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError, match="closed_at"):
        Trade(symbol="eurusd", direction="buy", entry=1.1, exit=1.2, profit_loss=10.0, opened_at=opened_at, closed_at=closed_at, status="closed")
