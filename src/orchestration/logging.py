"""Logging helper for the orchestration layer."""

from __future__ import annotations

import logging
import os
from datetime import UTC, datetime
from typing import Any, Dict

LOG_LEVEL = os.environ.get("SBOM_LOG_LEVEL", "INFO").upper()

logger = logging.getLogger("sbom_orchestration")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(LOG_LEVEL)


def log_job_event(job_id: str, status: str, message: str, extra: Dict[str, Any] | None = None) -> None:
    """Emit a structured log entry for job lifecycle events."""
    payload = {
        "job_id": job_id,
        "status": status,
        "message": message,
        "ts": datetime.now(UTC).isoformat(),
    }
    if extra:
        payload.update(extra)
    logger.info("%s", payload)


def log_warning(message: str, **context: Any) -> None:
    logger.warning("%s | %s", message, context)


def log_error(message: str, **context: Any) -> None:
    logger.error("%s | %s", message, context)
