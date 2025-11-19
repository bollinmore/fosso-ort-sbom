"""Adapter for interacting with the Fossology deployment.

This adapter does not call a live Fossology instance; instead it emulates the
data that Fossology would produce so the orchestration layer can be developed
and tested in isolation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from src.orchestration.models import Project


def trigger_scan(project: Project) -> Dict[str, List[Dict[str, str]]]:
    """Return discovered first-party components for the requested project."""
    project_path = Path(project.path)
    if not project_path.exists():
        raise FileNotFoundError(f"Project path {project.path} not found")

    components: List[Dict[str, str]] = []
    for file_path in sorted(project_path.rglob("*")):
        if file_path.is_file():
            rel = file_path.relative_to(project_path)
            components.append(
                {"name": rel.stem or rel.name, "path": str(rel), "type": "first-party"}
            )

    return {"components": components}
