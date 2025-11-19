"""Utilities for persisting generated SBOM artifacts."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

from src.orchestration.models import SBOMArtifact, Scan


def get_output_dir() -> Path:
    """Return the directory where SBOM artifacts should be stored."""
    configured = os.environ.get("SBOM_OUTPUT_DIR", "sbom-artifacts")
    path = Path(configured)
    path.mkdir(parents=True, exist_ok=True)
    return path


def store_sbom(scan: Scan, fmt: str, components: List[Dict[str, str]]) -> SBOMArtifact:
    """Persist a minimal SBOM document and return its metadata."""
    fmt_normalized = fmt.lower()
    if fmt_normalized not in {"spdx", "cyclonedx"}:
        raise ValueError(f"Unsupported SBOM format {fmt}")

    output_dir = get_output_dir()
    filename = f"{scan.id}.{fmt_normalized}.json"
    file_path = output_dir / filename
    payload = {
        "scan_id": scan.id,
        "format": fmt_normalized,
        "project": {"id": scan.project.id, "name": scan.project.name},
        "components": components,
        "summary": scan.summary,
        "warnings": scan.warnings,
    }
    file_path.write_text(json.dumps(payload, indent=2))

    return SBOMArtifact(
        scan_id=scan.id,
        format=fmt_normalized,
        location=str(file_path),
        components=components,
    )
