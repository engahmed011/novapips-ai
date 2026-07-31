"""Application configuration settings for NOVAPIPS AI.

This module centralizes environment-based configuration for the backend.
It uses pydantic-settings to load values from environment variables and
supports validation for required fields and supported enum-like values.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Final, Any

from pydantic import Field, ValidationError, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

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


ROOT_DIR: Final[Path] = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Validated application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        validate_assignment=True,
    )

    app_name: str = Field(..., alias=APP_NAME_ENV_VAR)
    app_version: str = Field(..., alias=APP_VERSION_ENV_VAR)
    environment: str = Field(default="development", alias=ENVIRONMENT_ENV_VAR)
    log_level: str = Field(default="INFO", alias=LOG_LEVEL_ENV_VAR)

    telegram_bot_token: str = Field(..., alias=TELEGRAM_BOT_TOKEN_ENV_VAR)
    telegram_public_chat_id: str = Field(..., alias=TELEGRAM_PUBLIC_CHAT_ID_ENV_VAR)
    telegram_vip_chat_id: str = Field(..., alias=TELEGRAM_VIP_CHAT_ID_ENV_VAR)

    oanda_api_key: str = Field(..., alias=OANDA_API_KEY_ENV_VAR)
    oanda_account_id: str = Field(..., alias=OANDA_ACCOUNT_ID_ENV_VAR)

    firebase_project_id: str = Field(..., alias=FIREBASE_PROJECT_ID_ENV_VAR)
    firebase_client_email: str = Field(..., alias=FIREBASE_CLIENT_EMAIL_ENV_VAR)
    firebase_private_key: str = Field(..., alias=FIREBASE_PRIVATE_KEY_ENV_VAR)

    openai_api_key: str = Field(..., alias=OPENAI_API_KEY_ENV_VAR)

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        """Ensure the runtime environment is supported."""
        normalized_value = value.strip().lower()
        if normalized_value not in VALID_ENVIRONMENTS:
            raise ValueError(
                f"environment must be one of {VALID_ENVIRONMENTS}, got {value!r}"
            )
        return normalized_value

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Ensure the log level is one of the supported values."""
        normalized_value = value.strip().upper()
        if normalized_value not in VALID_LOG_LEVELS:
            raise ValueError(f"log_level must be one of {VALID_LOG_LEVELS}, got {value!r}")
        return normalized_value

    @field_validator("app_name", "app_version")
    @classmethod
    def validate_non_empty_strings(cls, value: str, info: ValidationInfo) -> str:
        """Ensure required string values are not blank."""
        if not value or not value.strip():
            raise ValueError(f"{info.field_name} cannot be empty")
        return value.strip()

    @field_validator(
        "telegram_bot_token",
        "telegram_public_chat_id",
        "telegram_vip_chat_id",
        "oanda_api_key",
        "oanda_account_id",
        "firebase_project_id",
        "firebase_client_email",
        "firebase_private_key",
        "openai_api_key",
    )
    @classmethod
    def validate_required_secret_fields(cls, value: str, info: ValidationInfo) -> str:
        """Ensure required secrets and identifiers are not blank."""
        if not value or not value.strip():
            raise ValueError(f"{info.field_name} cannot be empty")
        return value.strip()

    def is_development(self) -> bool:
        """Return whether the current environment is development."""
        return self.environment == "development"

    def is_production(self) -> bool:
        """Return whether the current environment is production."""
        return self.environment == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance.

    The settings are loaded once per process and reused thereafter.
    """
    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(f"Invalid configuration: {exc}") from exc


def __getattr__(name: str) -> Any:
    """Provide lazy access to the singleton settings instance."""
    if name == "settings":
        return get_settings()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
