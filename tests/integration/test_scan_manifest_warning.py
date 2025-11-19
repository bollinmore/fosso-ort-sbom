"""Integration tests covering warning scenarios."""

from src.orchestration import scans
from src.orchestration.jobs import JobRegistry
from src.orchestration.models import Project, ScanStatus


def test_scan_with_missing_manifest(monkeypatch, tmp_path):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    project = Project(
        id="proj-missing-manifest",
        name="MissingManifest",
        path=str(project_dir),
        manifests=["does-not-exist.txt"],
    )
    registry = JobRegistry()
    monkeypatch.setenv("SBOM_OUTPUT_DIR", str(tmp_path / "sboms"))

    scan = scans.start_scan(project, registry)

    assert scan.status == ScanStatus.COMPLETED
    assert scan.warnings, "Expected warnings for missing manifest"
    assert any("not found" in warning for warning in scan.warnings)
