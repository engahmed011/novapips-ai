"""Production-grade logging utilities for NOVAPIPS AI."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Final
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:  # pragma: no cover - optional dependency
    Fore = Style = None  # type: ignore[assignment]
    colorama_init = None


class ColoredFormatter(logging.Formatter):
    """Apply ANSI colors to console logs when color support is available."""

    COLORS: Final[dict[str, str]] = {
        "DEBUG": Fore.CYAN if Fore is not None else "",
        "INFO": Fore.GREEN if Fore is not None else "",
        "WARNING": Fore.YELLOW if Fore is not None else "",
        "ERROR": Fore.RED if Fore is not None else "",
        "CRITICAL": Fore.RED + Style.BRIGHT if Fore is not None else "",
    }

    def format(self, record: logging.LogRecord) -> str:
        """Return a colorized message for console output."""
        if colorama_init is not None:
            colorama_init(autoreset=True)
        message = super().format(record)
        color = self.COLORS.get(record.levelname, "")
        if color:
            return f"{color}{message}{Style.RESET_ALL}" if Style is not None else message
        return message


class NovaPipsLogger:
    """Singleton logger configured for console and file output."""

    _instance: NovaPipsLogger | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "NovaPipsLogger":
        """Ensure a single logger instance is created per process."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the logger once and reuse the configuration."""
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self._logger = self._build_logger()

    @classmethod
    def get_instance(cls) -> "NovaPipsLogger":
        """Return the singleton logger instance."""
        return cls()

    def _build_logger(self) -> logging.Logger:
        """Create a named logger with console and file handlers."""
        logger = logging.getLogger("novapips.ai")
        logger.setLevel(self._resolve_log_level())
        logger.propagate = False
        logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self._resolve_log_level())
        console_handler.setFormatter(ColoredFormatter(formatter._fmt, formatter.datefmt))
        logger.addHandler(console_handler)

        log_dir = Path(__file__).resolve().parents[2] / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        rotating_file = RotatingFileHandler(
            log_dir / "novapips-ai.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        rotating_file.setLevel(self._resolve_log_level())
        rotating_file.setFormatter(formatter)
        logger.addHandler(rotating_file)

        daily_file = TimedRotatingFileHandler(
            log_dir / "novapips-ai.daily.log",
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8",
        )
        daily_file.setLevel(self._resolve_log_level())
        daily_file.setFormatter(formatter)
        logger.addHandler(daily_file)

        return logger

    def _resolve_log_level(self) -> int:
        """Read the configured log level from settings with a safe fallback."""
        try:
            from backend.config.settings import get_settings

            configured_level = get_settings().log_level.upper()
            return getattr(logging, configured_level, logging.INFO)
        except Exception:
            return logging.INFO

    @property
    def logger(self) -> logging.Logger:
        """Expose the configured logger instance."""
        return self._logger

    def log_signal(self, message: str, *, level: int = logging.INFO, **context: Any) -> None:
        """Log a signal event with optional structured context."""
        self._log_event("SIGNAL", message, level, context)

    def log_news(self, message: str, *, level: int = logging.INFO, **context: Any) -> None:
        """Log a news event with optional structured context."""
        self._log_event("NEWS", message, level, context)

    def log_trade(self, message: str, *, level: int = logging.INFO, **context: Any) -> None:
        """Log a trade event with optional structured context."""
        self._log_event("TRADE", message, level, context)

    def log_ai(self, message: str, *, level: int = logging.INFO, **context: Any) -> None:
        """Log an AI-related event with optional structured context."""
        self._log_event("AI", message, level, context)

    def _log_event(self, prefix: str, message: str, level: int, context: dict[str, Any]) -> None:
        """Emit a structured log message to all configured handlers."""
        details = " | ".join(f"{key}={value}" for key, value in sorted(context.items()))
        payload = f"{prefix} | {message}"
        if details:
            payload = f"{payload} | {details}"
        self.logger.log(level, payload)


def get_logger() -> logging.Logger:
    """Return the configured singleton logger instance."""
    return NovaPipsLogger.get_instance().logger
