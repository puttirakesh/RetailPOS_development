"""Simple logging for RetailPOS (stdlib only — no structlog)."""

from __future__ import annotations

import logging
import sys
from typing import Any

from app.core.config import settings


def setup_logging() -> None:
    """Configure plain text logging for the application."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
        level=log_level,
        force=True,
    )


def get_logger(name: str | None = None) -> Any:
    """Return a standard library logger."""
    return logging.getLogger(name or "retailpos")