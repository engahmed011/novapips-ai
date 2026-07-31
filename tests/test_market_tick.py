"""Tests for the MarketTick model."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from backend.models import MarketTick


def test_market_tick_valid_creation_and_mid_price() -> None:
    """A market tick should be created and compute its midpoint."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    tick = MarketTick(symbol="gbpusd", bid=1.2500, ask=1.2505, spread=0.0005, provider="OANDA", timestamp=timestamp)

    assert tick.symbol == "GBPUSD"
    assert tick.mid_price() == pytest.approx(1.25025)
    assert "MarketTick(" in repr(tick)


@pytest.mark.parametrize(
    ("symbol", "bid", "ask", "spread", "provider"),
    [
        ("", 1.25, 1.2505, 0.0005, "OANDA"),
        ("gbpusd", 1.25, 1.2505, -0.0005, "OANDA"),
        ("gbpusd", 1.25, 1.24, 0.0005, "OANDA"),
        ("gbpusd", 0.0, 1.2505, 0.0005, "OANDA"),
        ("gbpusd", 1.25, 1.2505, 0.0005, ""),
    ],
)
def test_market_tick_invalid_values_raise_value_error(symbol: str, bid: float, ask: float, spread: float, provider: str) -> None:
    """The constructor should reject inconsistent quote values."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        MarketTick(symbol=symbol, bid=bid, ask=ask, spread=spread, provider=provider, timestamp=timestamp)


def test_market_tick_rejects_naive_timestamp() -> None:
    """Timezone-naive timestamps should be rejected."""
    timestamp = datetime(2024, 1, 1, 12, 0)
    with pytest.raises(ValueError, match="timezone-aware"):
        MarketTick(symbol="eurusd", bid=1.10, ask=1.1005, spread=0.0005, provider="OANDA", timestamp=timestamp)
