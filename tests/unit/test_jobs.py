"""Unit tests for job registry."""

from src.orchestration.jobs import JobRegistry
from src.orchestration.models import JobState


def test_register_and_update_job():
    registry = JobRegistry()
    job = registry.register("scan-123")
    assert job.scan_id == "scan-123"
    assert job.state == JobState.QUEUED

    registry.update(job.id, JobState.RUNNING, "Processing")
    updated = registry.get(job.id)
    assert updated.state == JobState.RUNNING
    assert updated.message == "Processing"

    registry.update(job.id, JobState.COMPLETED, "Done")
    assert registry.get(job.id).state == JobState.COMPLETED
