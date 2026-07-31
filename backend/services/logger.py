"""Production-grade logging service for NOVAPIPS AI."""

from __future__ import annotations

import logging
import sys
import threading
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any


class _ComponentFilter(logging.Filter):
    """Filter records by component when routing to specific files."""

    def __init__(self, component: str | None = None, level: int | None = None) -> None:
        """Initialize the filter with an optional component and level."""
        super().__init__()
        self.component = component
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        """Return True when the record should be emitted by this handler."""
        if self.level is not None and record.levelno < self.level:
            return False
        if self.component is not None and getattr(record, "component", None) != self.component:
            return False
        return True


class LoggerService:
    """Singleton logger service with console and rotating file handlers."""

    _instance: LoggerService | None = None
    _lock = threading.Lock()

    def __new__(cls, *args: Any, **kwargs: Any) -> "LoggerService":
        """Ensure only one logger service instance exists per process."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the logger once and reuse the configuration."""
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self._logger = self._build_logger()

    def _build_logger(self) -> logging.Logger:
        """Create the configured logger with console and file handlers."""
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
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        log_dir = Path(__file__).resolve().parents[2] / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        file_specs: list[tuple[str, str | None, int]] = [
            ("app.log", None, self._resolve_log_level()),
            ("signals.log", "signals", self._resolve_log_level()),
            ("trades.log", "trades", self._resolve_log_level()),
            ("news.log", "news", self._resolve_log_level()),
            ("ai.log", "ai", self._resolve_log_level()),
            ("errors.log", None, logging.ERROR),
        ]

        for filename, component, level in file_specs:
            handler = RotatingFileHandler(
                log_dir / filename,
                maxBytes=5 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8",
            )
            handler.setLevel(level)
            handler.setFormatter(formatter)
            if component is not None:
                handler.addFilter(_ComponentFilter(component=component))
            elif filename == "errors.log":
                handler.addFilter(_ComponentFilter(level=logging.ERROR))
            logger.addHandler(handler)

        return logger

    def _resolve_log_level(self) -> int:
        """Resolve the configured log level from settings with a safe fallback."""
        try:
            from backend.config.settings import get_settings

            configured_level = get_settings().log_level.upper()
            return getattr(logging, configured_level, logging.INFO)
        except Exception:
            return logging.INFO

    def _emit(self, level: int, message: str, component: str | None = None) -> None:
        """Emit a log entry with optional routing metadata."""
        extra: dict[str, Any] = {}
        if component is not None:
            extra["component"] = component
        self._logger.log(level, message, extra=extra)

    @property
    def logger(self) -> logging.Logger:
        """Return the underlying logger instance."""
        return self._logger

    def debug(self, message: str) -> None:
        """Log a DEBUG message."""
        self._emit(logging.DEBUG, message)

    def info(self, message: str) -> None:
        """Log an INFO message."""
        self._emit(logging.INFO, message)

    def warning(self, message: str) -> None:
        """Log a WARNING message."""
        self._emit(logging.WARNING, message)

    def error(self, message: str) -> None:
        """Log an ERROR message."""
        self._emit(logging.ERROR, message)

    def critical(self, message: str) -> None:
        """Log a CRITICAL message."""
        self._emit(logging.CRITICAL, message)

    def log_signal(self, signal: Any) -> None:
        """Log a signal event."""
        self._emit(logging.INFO, f"Signal: {signal}", component="signals")

    def log_trade(self, trade: Any) -> None:
        """Log a trade event."""
        self._emit(logging.INFO, f"Trade: {trade}", component="trades")

    def log_news(self, news: Any) -> None:
        """Log a news event."""
        self._emit(logging.INFO, f"News: {news}", component="news")

    def log_ai(self, message: str) -> None:
        """Log an AI-related message."""
        self._emit(logging.INFO, message, component="ai")


def get_logger() -> LoggerService:
    """Return the singleton logger service."""
    return LoggerService()
