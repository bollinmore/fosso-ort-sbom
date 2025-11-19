"""Core data structures shared across the orchestration layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Dict, List, Optional


class ScanStatus(str, Enum):
    """State machine for scans triggered through the orchestration layer."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobState(str, Enum):
    """States tracked for internal integration jobs."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Project:
    """Represents a project submitted for SBOM generation."""

    id: str
    name: str
    path: str
    manifests: List[str] = field(default_factory=list)


@dataclass
class SBOMArtifact:
    """Metadata about a generated SBOM artifact."""

    scan_id: str
    format: str
    location: str
    components: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class IntegrationJob:
    """Tracks Fossology/ORT orchestration job lifecycle."""

    id: str
    scan_id: str
    state: JobState = JobState.QUEUED
    message: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Scan:
    """High-level summary of a scan request."""

    id: str
    project: Project
    status: ScanStatus = ScanStatus.QUEUED
    summary: Dict[str, int] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    artifacts: List[SBOMArtifact] = field(default_factory=list)
    job_id: Optional[str] = None
