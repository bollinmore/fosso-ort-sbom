"""Entry point for CLI helpers that drive the orchestration layer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.orchestration import scans
from src.orchestration.jobs import JobRegistry
from src.orchestration.models import Project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run SBOM scan orchestration.")
    parser.add_argument("--project-id", required=True, help="Identifier for the project")
    parser.add_argument("--name", required=True, help="Human readable project name")
    parser.add_argument("--path", required=True, help="Path to the project to scan")
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        help="Relative path to a manifest file (may be repeated)",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    project_path = Path(args.path)
    project = Project(
        id=args.project_id,
        name=args.name,
        path=str(project_path),
        manifests=list(args.manifest),
    )
    registry = JobRegistry()
    scan = scans.start_scan(project, registry)
    output = {
        "scan_id": scan.id,
        "status": scan.status.value,
        "artifacts": [artifact.location for artifact in scan.artifacts],
        "warnings": scan.warnings,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":  # pragma: no cover
    main()
