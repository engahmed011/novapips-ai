"""Abstract interfaces for backend data providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Candle:
    """Canonical OHLCV candle structure used across providers."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class BaseDataProvider(ABC):
    """Abstract contract for all market-data providers."""

    name: str = "provider"

    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to the provider."""

    @abstractmethod
    def disconnect(self) -> None:
        """Close the connection to the provider."""

    @abstractmethod
    def get_current_price(self, symbol: str) -> float:
        """Return the current price for the provided symbol."""

    @abstractmethod
    def get_candles(self, symbol: str, timeframe: str, limit: int = 100) -> list[Candle]:
        """Return a list of OHLCV candles for the requested symbol and timeframe."""

    @abstractmethod
    def get_spread(self, symbol: str) -> float:
        """Return the current spread for the provided symbol."""

    @abstractmethod
    def is_market_open(self) -> bool:
        """Return whether the underlying market is currently open."""

    @abstractmethod
    def get_server_time(self) -> datetime:
        """Return the provider server time as a UTC datetime."""

    @abstractmethod
    def health_check(self) -> bool:
        """Return whether the provider is healthy and ready for use."""
