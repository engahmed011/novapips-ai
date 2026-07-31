"""Tests for the backend configuration layer."""

from __future__ import annotations

import importlib
import sys

import pytest


@pytest.fixture(autouse=True)
def clear_config_modules() -> None:
    """Ensure config modules are re-imported for each test."""
    for module_name in list(sys.modules):
        if module_name.startswith("backend.config"):
            sys.modules.pop(module_name, None)


def test_settings_loads_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings should load required values from the environment."""
    env_values = {
        "APP_NAME": "NOVAPIPS AI",
        "APP_VERSION": "1.0.0",
        "ENVIRONMENT": "production",
        "LOG_LEVEL": "INFO",
        "TELEGRAM_BOT_TOKEN": "telegram-token",
        "TELEGRAM_PUBLIC_CHAT_ID": "public-chat-id",
        "TELEGRAM_VIP_CHAT_ID": "vip-chat-id",
        "OANDA_API_KEY": "oanda-key",
        "OANDA_ACCOUNT_ID": "account-id",
        "FIREBASE_PROJECT_ID": "firebase-project",
        "FIREBASE_CLIENT_EMAIL": "firebase@example.com",
        "FIREBASE_PRIVATE_KEY": "private-key",
        "OPENAI_API_KEY": "openai-key",
    }

    for key, value in env_values.items():
        monkeypatch.setenv(key, value)

    settings_module = importlib.import_module("backend.config.settings")
    settings = settings_module.get_settings()

    assert settings.app_name == "NOVAPIPS AI"
    assert settings.environment == "production"
    assert settings.log_level == "INFO"
    assert settings.telegram_bot_token == "telegram-token"
    assert settings.oanda_api_key == "oanda-key"


def test_settings_rejects_invalid_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unsupported environments should be rejected during validation."""
    env_values = {
        "APP_NAME": "NOVAPIPS AI",
        "APP_VERSION": "1.0.0",
        "ENVIRONMENT": "invalid-env",
        "LOG_LEVEL": "INFO",
        "TELEGRAM_BOT_TOKEN": "telegram-token",
        "TELEGRAM_PUBLIC_CHAT_ID": "public-chat-id",
        "TELEGRAM_VIP_CHAT_ID": "vip-chat-id",
        "OANDA_API_KEY": "oanda-key",
        "OANDA_ACCOUNT_ID": "account-id",
        "FIREBASE_PROJECT_ID": "firebase-project",
        "FIREBASE_CLIENT_EMAIL": "firebase@example.com",
        "FIREBASE_PRIVATE_KEY": "private-key",
        "OPENAI_API_KEY": "openai-key",
    }

    for key, value in env_values.items():
        monkeypatch.setenv(key, value)

    settings_module = importlib.import_module("backend.config.settings")

    with pytest.raises(RuntimeError, match="Invalid configuration"):
        settings_module.get_settings()
