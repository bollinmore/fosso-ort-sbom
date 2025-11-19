"""Job tracking utilities for long-running Fossology/ORT scans."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4

from .models import IntegrationJob, JobState


class JobRegistry:
    """Lightweight in-memory registry for tracking scan jobs."""

    def __init__(self) -> None:
        self._jobs: Dict[str, IntegrationJob] = {}

    def register(self, scan_id: str) -> IntegrationJob:
        job = IntegrationJob(id=uuid4().hex, scan_id=scan_id)
        self._jobs[job.id] = job
        return job

    def update(self, job_id: str, state: JobState, message: str = "") -> IntegrationJob:
        job = self._require_job(job_id)
        job.state = state
        job.message = message
        job.updated_at = datetime.utcnow()
        return job

    def get(self, job_id: str) -> Optional[IntegrationJob]:
        return self._jobs.get(job_id)

    def all(self):
        return list(self._jobs.values())

    def _require_job(self, job_id: str) -> IntegrationJob:
        job = self._jobs.get(job_id)
        if job is None:
            raise KeyError(f"Unknown job id {job_id}")
        return job
