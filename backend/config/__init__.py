"""Configuration package for the NOVAPIPS AI backend."""

from typing import Any

from backend.config.constants import (
    APP_NAME_ENV_VAR,
    APP_VERSION_ENV_VAR,
    ENVIRONMENT_ENV_VAR,
    FIREBASE_CLIENT_EMAIL_ENV_VAR,
    FIREBASE_PRIVATE_KEY_ENV_VAR,
    FIREBASE_PROJECT_ID_ENV_VAR,
    LOG_LEVEL_ENV_VAR,
    OANDA_ACCOUNT_ID_ENV_VAR,
    OANDA_API_KEY_ENV_VAR,
    OPENAI_API_KEY_ENV_VAR,
    TELEGRAM_BOT_TOKEN_ENV_VAR,
    TELEGRAM_PUBLIC_CHAT_ID_ENV_VAR,
    TELEGRAM_VIP_CHAT_ID_ENV_VAR,
    VALID_ENVIRONMENTS,
    VALID_LOG_LEVELS,
)
from backend.config.settings import Settings, get_settings

__all__ = [
    "APP_NAME_ENV_VAR",
    "APP_VERSION_ENV_VAR",
    "ENVIRONMENT_ENV_VAR",
    "FIREBASE_CLIENT_EMAIL_ENV_VAR",
    "FIREBASE_PRIVATE_KEY_ENV_VAR",
    "FIREBASE_PROJECT_ID_ENV_VAR",
    "LOG_LEVEL_ENV_VAR",
    "OANDA_ACCOUNT_ID_ENV_VAR",
    "OANDA_API_KEY_ENV_VAR",
    "OPENAI_API_KEY_ENV_VAR",
    "Settings",
    "TELEGRAM_BOT_TOKEN_ENV_VAR",
    "TELEGRAM_PUBLIC_CHAT_ID_ENV_VAR",
    "TELEGRAM_VIP_CHAT_ID_ENV_VAR",
    "VALID_ENVIRONMENTS",
    "VALID_LOG_LEVELS",
    "get_settings",
    "settings",
]


def __getattr__(name: str) -> Any:
    """Provide lazy access to the default settings object."""
    if name == "settings":
        from backend.config.settings import get_settings

        return get_settings()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
