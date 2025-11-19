"""Unit tests for SBOM artifact storage helpers."""

import json
from pathlib import Path

from src.orchestration.models import Project, Scan, ScanStatus
from src.sbom import storage


def test_store_sbom(monkeypatch, tmp_path):
    project = Project(id="p1", name="Proj", path="/tmp/proj")
    scan = Scan(id="scan1", project=project, status=ScanStatus.RUNNING)
    output_dir = tmp_path / "sboms"
    monkeypatch.setenv("SBOM_OUTPUT_DIR", str(output_dir))

    artifact = storage.store_sbom(
        scan,
        fmt="spdx",
        components=[{"name": "comp", "type": "first-party"}],
    )

    path = Path(artifact.location)
    assert path.exists()
    payload = json.loads(path.read_text())
    assert payload["scan_id"] == "scan1"
    assert payload["components"][0]["name"] == "comp"
