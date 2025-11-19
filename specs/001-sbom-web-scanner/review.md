# Implementation Review – Web SBOM Scanner

Date: 2025-11-19  
Scope: Verification that implemented code covers the functional requirements defined in `spec.md`.

| Requirement | Implementation Reference | Notes |
|-------------|-------------------------|-------|
| FR-001 / FR-006 / FR-012 | `src/orchestration/scans.py`, `tests/integration/test_scan_success.py` | `start_scan` drives the full workflow and emits status updates recorded in summaries. |
| FR-002 | `src/adapters/fossology_client.py` | Traverses project files to collect first-party components for SBOM inclusion. |
| FR-003 / FR-005 | `src/adapters/ort_client.py`, `tests/unit/test_adapters.py` | Parses manifest files and merges third-party components into the scan summary. |
| FR-004 / FR-007 | `src/sbom/storage.py`, `tests/unit/test_sbom_storage.py` | Persists both SPDX and CycloneDX JSON artifacts and records their locations. |
| FR-005a / FR-015 | `src/orchestration/scans.py` | Fossology and ORT steps are sequenced explicitly, and warnings are surfaced when ORT encounters issues. |
| FR-008 / FR-009 | `src/cli/orchestration_cli.py`, `src/orchestration/logging.py` | CLI output and logging provide operator-facing status/error context and job tracking. |
| FR-010 | `src/orchestration/scans.py` (`rerun_scan`) | Allows reusing project metadata to re-trigger scans. |
| FR-011 | `docker-compose.yml`, `quickstart.md` | Defines upload-based workflow wiring for Fossology and ORT containers. |
| FR-013 | `specs/001-sbom-web-scanner/quickstart.md`, `src/orchestration/scans.py` | Documents limits and captures warnings when manifests or paths violate configured constraints. |
| FR-014 | `quickstart.md`, `docker-compose.yml` | Reinforces Fossology login as the authentication entry point and keeps deployment internal-only. |

Non-functional reviews:
- Performance/resource expectations captured in `quickstart.md` and monitored via `src/orchestration/logging.py`.
- Security boundary maintained by reusing Fossology authentication and internal storage locations.
