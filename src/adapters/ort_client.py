"""Adapter for triggering OSS Review Toolkit analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from src.orchestration.models import Project


def analyze_project(project: Project) -> Tuple[List[Dict[str, str]], List[str]]:
    """Return third-party dependencies discovered via manifest parsing."""
    base_path = Path(project.path)
    if not base_path.exists():
        raise FileNotFoundError(f"Project path {project.path} not found")

    components: List[Dict[str, str]] = []
    warnings: List[str] = []

    for manifest in project.manifests:
        manifest_path = base_path / manifest
        if not manifest_path.exists():
            warnings.append(f"Manifest {manifest} not found")
            continue

        for idx, raw_line in enumerate(manifest_path.read_text().splitlines(), start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                warnings.append(f"Manifest {manifest} line {idx} missing version delimiter")
                continue
            name, version = [part.strip() for part in line.split(":", 1)]
            components.append(
                {
                    "name": name,
                    "version": version,
                    "manifest": manifest,
                    "type": "third-party",
                }
            )

    return components, warnings
