"""Unit tests for Fossology/ORT adapters."""

from src.adapters import fossology_client, ort_client
from src.orchestration.models import Project


def test_fossology_adapter(tmp_path):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    (project_dir / "main.py").write_text("print('hi')\n")
    project = Project(id="p1", name="Proj", path=str(project_dir))

    result = fossology_client.trigger_scan(project)

    assert result["components"]
    assert result["components"][0]["type"] == "first-party"


def test_ort_adapter(tmp_path):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    manifest = project_dir / "deps.txt"
    manifest.write_text("libA:1.0.0\n")
    project = Project(id="p1", name="Proj", path=str(project_dir), manifests=["deps.txt"])

    components, warnings = ort_client.analyze_project(project)

    assert warnings == []
    assert components[0]["name"] == "libA"
