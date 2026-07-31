"""Manager for selecting and coordinating data providers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from backend.core.providers.base_provider import BaseDataProvider


@dataclass(slots=True)
class ProviderRegistration:
    """Registration metadata for a provider instance."""

    name: str
    provider: BaseDataProvider


class DataProviderManager:
    """Central registry for switching between data providers."""

    def __init__(
        self,
        providers: Mapping[str, BaseDataProvider] | None = None,
        active_provider: str | None = None,
    ) -> None:
        self._providers: dict[str, BaseDataProvider] = {}
        self._active_provider_name: str | None = None

        if providers:
            for name, provider in providers.items():
                self.register_provider(name, provider)

        if active_provider:
            self.set_active_provider(active_provider)
        elif self._providers:
            self._active_provider_name = next(iter(self._providers))

    def register_provider(self, name: str, provider: BaseDataProvider) -> None:
        """Register a provider instance under a stable name."""
        self._providers[name] = provider
        if self._active_provider_name is None:
            self._active_provider_name = name

    def set_active_provider(self, name: str) -> None:
        """Set the active provider by its registered name."""
        if name not in self._providers:
            raise KeyError(f"Provider {name!r} is not registered")
        self._active_provider_name = name

    def get_active_provider(self) -> BaseDataProvider:
        """Return the currently active provider instance."""
        if self._active_provider_name is None:
            raise RuntimeError("No active provider has been configured")
        return self._providers[self._active_provider_name]

    def get_provider(self, name: str) -> BaseDataProvider:
        """Return a registered provider by name."""
        if name not in self._providers:
            raise KeyError(f"Provider {name!r} is not registered")
        return self._providers[name]

    def list_providers(self) -> tuple[str, ...]:
        """Return the registered provider names in insertion order."""
        return tuple(self._providers.keys())
