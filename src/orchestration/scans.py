"""High-level orchestration entry points for starting and monitoring scans."""

from __future__ import annotations

from typing import List
from uuid import uuid4

from src.adapters import fossology_client, ort_client
from src.orchestration.models import (
    Project,
    SBOMArtifact,
    Scan,
    ScanStatus,
    JobState,
)
from src.orchestration import jobs as jobs_registry
from src.orchestration import logging as orchestration_logging
from src.sbom import storage


def start_scan(project: Project, registry: jobs_registry.JobRegistry) -> Scan:
    """Execute a full scan workflow for the given project."""
    scan = Scan(id=uuid4().hex, project=project, status=ScanStatus.QUEUED)
    job = registry.register(scan.id)
    orchestration_logging.log_job_event(job.id, JobState.QUEUED.value, "Scan registered")
    scan.job_id = job.id

    try:
        registry.update(job.id, JobState.RUNNING, "Collecting first-party components")
        orchestration_logging.log_job_event(job.id, JobState.RUNNING.value, "Collecting first-party components")
        fossology_result = fossology_client.trigger_scan(project)

        registry.update(job.id, JobState.RUNNING, "Collecting third-party dependencies")
        orchestration_logging.log_job_event(job.id, JobState.RUNNING.value, "Collecting third-party dependencies")
        third_party_components, warnings = ort_client.analyze_project(project)

        combined_components = list(fossology_result["components"])
        combined_components.extend(third_party_components)

        scan.summary = {
            "first_party_components": len(fossology_result["components"]),
            "third_party_components": len(third_party_components),
            "total_components": len(combined_components),
        }
        scan.warnings.extend(warnings)

        registry.update(job.id, JobState.RUNNING, "Persisting SBOM artifacts")
        orchestration_logging.log_job_event(job.id, JobState.RUNNING.value, "Persisting SBOM artifacts")
        artifacts = _write_sboms(scan, combined_components)
        scan.artifacts = artifacts
        scan.status = ScanStatus.COMPLETED
        registry.update(job.id, JobState.COMPLETED, "Scan completed")
        orchestration_logging.log_job_event(job.id, JobState.COMPLETED.value, "Scan completed")
    except Exception as exc:  # pragma: no cover - defensive
        scan.status = ScanStatus.FAILED
        scan.warnings.append(str(exc))
        registry.update(job.id, JobState.FAILED, str(exc))
        orchestration_logging.log_error("Scan failed", job_id=job.id, error=str(exc))
        raise

    return scan


def rerun_scan(scan: Scan, registry: jobs_registry.JobRegistry) -> Scan:
    """Trigger a new scan using the same project metadata."""
    return start_scan(scan.project, registry)


def _write_sboms(scan: Scan, components: List[dict]) -> List[SBOMArtifact]:
    artifacts: List[SBOMArtifact] = []
    for fmt in ("spdx", "cyclonedx"):
        artifact = storage.store_sbom(scan, fmt, components)
        artifacts.append(artifact)
    return artifacts
