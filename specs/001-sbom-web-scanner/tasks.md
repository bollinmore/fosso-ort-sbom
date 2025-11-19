# Tasks: Web SBOM Scanner

**Input**: Design documents from `/specs/001-sbom-web-scanner/`  
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Phase 1: Setup (Project Initialization)

- [ ] T001 Create base project structure under src/ and tests/ as described in specs/001-sbom-web-scanner/plan.md
- [ ] T002 Configure project tooling to run official Fossology and ORT Docker images from the internal environment (for example, docker-compose file in repo root)

## Phase 2: Foundational (Shared Prerequisites)

- [ ] T003 Define core orchestration module layout in src/orchestration/ and src/adapters/ based on specs/001-sbom-web-scanner/plan.md
- [ ] T004 Document configuration options and environment variables needed to connect to Fossology and ORT in specs/001-sbom-web-scanner/quickstart.md

## Phase 2.5: Tests for User Story 1 (Web-based SBOM scan via Fossology UI)

- [ ] T015 [P] [US1] Add integration test for a successful scan via Fossology UI in tests/integration/test_scan_success.py
- [ ] T016 [P] [US1] Add integration test for manifest parsing failures and warning behavior in tests/integration/test_scan_manifest_warning.py
- [ ] T017 [P] [US1] Add unit tests for scan job state transitions (queued, running, completed, failed) in tests/unit/test_jobs.py
- [ ] T018 [P] [US1] Add unit tests for SBOM artifact storage and retrieval metadata in tests/unit/test_sbom_storage.py
- [ ] T019 [P] [US1] Add unit tests for Fossology and ORT adapter request construction and parameter handling in tests/unit/test_adapters.py

## Phase 3: User Story 1 – Web-based SBOM scan via Fossology UI (P1)

- [ ] T005 [P] [US1] Represent Project, Scan, SBOM Artifact, and Integration Job entities in src/orchestration/models.py based on specs/001-sbom-web-scanner/data-model.md
- [ ] T006 [US1] Implement orchestration logic in src/orchestration/scans.py to start a scan when a project is submitted through Fossology
- [ ] T007 [US1] Implement adapter functions in src/adapters/fossology_client.py to interact with the Fossology web interface or APIs as needed for initiating scans
- [ ] T008 [US1] Implement adapter functions in src/adapters/ort_client.py to trigger ORT analysis for the same project inputs used by Fossology
- [ ] T009 [P] [US1] Implement job state tracking in src/orchestration/jobs.py for queued, running, completed, and failed scans
- [ ] T010 [US1] Ensure SBOM artifacts in SPDX and CycloneDX formats are stored in a location aligned with organizational policies, with paths or identifiers recorded in src/sbom/storage.py
- [ ] T011 [US1] Implement internal orchestration API endpoints in src/cli or a small backend module that correspond to contracts in specs/001-sbom-web-scanner/contracts/openapi.yaml
- [ ] T012 [US1] Update user-facing status and error descriptions in Fossology-related configuration or docs so operators understand scan progress and integration failures

## Final Phase: Polish & Cross-Cutting Concerns

- [ ] T013 Review requirements in specs/001-sbom-web-scanner/spec.md against implementation files to ensure SBOM coverage and integration behaviors are fully represented
- [ ] T014 Add or refine logging and basic metrics hooks in src/orchestration/logging.py to support monitoring of scan outcomes and durations
