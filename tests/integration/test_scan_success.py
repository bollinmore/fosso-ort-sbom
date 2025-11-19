"""Integration tests for scan orchestration logic."""

import json
from pathlib import Path

from src.orchestration import scans
from src.orchestration.jobs import JobRegistry
from src.orchestration.models import Project, ScanStatus, JobState


def _create_project(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "main.py").write_text("print('hello')\n")
    manifest = project_dir / "deps.txt"
    manifest.write_text("libA:1.0.0\nlibB:2.1.0\n")
    return project_dir, ["deps.txt"]


def test_scan_success(monkeypatch, tmp_path):
    project_dir, manifests = _create_project(tmp_path)
    project = Project(
        id="proj-1",
        name="Sample Project",
        path=str(project_dir),
        manifests=manifests,
    )
    registry = JobRegistry()
    sbom_dir = tmp_path / "sboms"
    monkeypatch.setenv("SBOM_OUTPUT_DIR", str(sbom_dir))

    scan = scans.start_scan(project, registry)

    assert scan.status == ScanStatus.COMPLETED
    assert scan.summary["first_party_components"] >= 1
    assert scan.summary["third_party_components"] == 2
    assert len(scan.artifacts) == 2
    for artifact in scan.artifacts:
        path = Path(artifact.location)
        assert path.exists()
        payload = json.loads(path.read_text())
        assert payload["scan_id"] == scan.id

    job = registry.get(scan.job_id)
    assert job is not None
    assert job.state == JobState.COMPLETED
