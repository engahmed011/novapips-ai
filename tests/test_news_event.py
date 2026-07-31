"""Tests for the NewsEvent model."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from backend.models import NewsEvent


def test_news_event_valid_creation_and_high_impact_flag() -> None:
    """A news event should normalize currency and expose impact helpers."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    event = NewsEvent(title="NFP", currency="usd", impact="High", time=timestamp, description="Employment data released")

    assert event.currency == "USD"
    assert event.impact == "high"
    assert event.is_high_impact() is True
    assert "NewsEvent(" in repr(event)


def test_news_event_non_high_impact_is_false() -> None:
    """Medium-impact events should not be flagged as high impact."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    event = NewsEvent(title="CPI", currency="eur", impact="medium", time=timestamp, description="Inflation reading")

    assert event.is_high_impact() is False


@pytest.mark.parametrize(
    ("title", "currency", "impact", "description"),
    [
        ("", "usd", "high", "Employment data released"),
        ("NFP", "", "high", "Employment data released"),
        ("NFP", "usd", "", "Employment data released"),
        ("NFP", "usd", "urgent", "Employment data released"),
        ("NFP", "usd", "high", ""),
    ],
)
def test_news_event_invalid_values_raise_value_error(title: str, currency: str, impact: str, description: str) -> None:
    """The constructor should reject invalid news event values."""
    timestamp = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        NewsEvent(title=title, currency=currency, impact=impact, time=timestamp, description=description)


def test_news_event_rejects_naive_time() -> None:
    """Timezone-naive timestamps should be rejected."""
    timestamp = datetime(2024, 1, 1, 12, 0)
    with pytest.raises(ValueError, match="timezone-aware"):
        NewsEvent(title="NFP", currency="usd", impact="high", time=timestamp, description="Employment data released")
