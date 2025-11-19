
# Implementation Plan: Web SBOM Scanner

**Branch**: `001-sbom-web-scanner` | **Date**: 2025-11-19 | **Spec**: /Users/chenwensheng/Documents/Codes/bollinmore/fosso-ort-sbom/specs/001-sbom-web-scanner/spec.md
**Input**: Feature specification from `/specs/001-sbom-web-scanner/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

## Summary
Design and implement an internal, web-based SBOM scanning workflow that uses
the official Fossology and OSS Review Toolkit (ORT) Docker images. Users
interact through the Fossology web interface as the unified UI, and the
system automatically coordinates Fossology and ORT so that SBOMs in SPDX and
CycloneDX formats include both first-party code and third-party dependencies
discovered from package manager manifests.

## Technical Context
**Language/Version**: NEEDS CLARIFICATION  
**Primary Dependencies**: Fossology (official Docker image), OSS Review Toolkit (official Docker image)  
**Storage**: NEEDS CLARIFICATION (e.g., Fossology DB only vs additional storage for SBOM artifacts)  
**Testing**: NEEDS CLARIFICATION (e.g., preferred test framework for orchestration layer)  
**Target Platform**: Linux server in internal environment  
**Project Type**: web (Fossology UI + backend orchestration)  
**Performance Goals**: Complete typical scans within minutes; support long-running scans up to about one hour with progress feedback  
**Constraints**: Internal-only deployment; must not expose anonymous access; respect organization limits on project size and scan time  
**Scale/Scope**: Initial adoption within a single organization; multiple teams may run scans but multi-tenant SaaS is explicitly out of scope

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Analysis-First Compliance
- [x] Feature requirements include sufficient detail for comprehensive analysis
- [x] Context dependencies clearly identified (Fossology, ORT, Docker-based deployment)
- [x] No assumptions made without explicit justification beyond marked NEEDS CLARIFICATION items in Technical Context

### Security-First Compliance
- [x] Security implications assessed for feature scope (internal deployment, authenticated access via Fossology login)
- [x] Authentication/authorization requirements specified via Fossology’s existing login mechanism
- [ ] Data handling and privacy considerations documented for SBOM storage and logs (NEEDS CLARIFICATION for retention policy)

### Test-Driven Validation Compliance
- [x] Test strategy will be defined before implementation planning in Phase 0/1 artifacts
- [x] Test coverage targets implied by constitution (unit, integration around scan orchestration and SBOM completeness)
- [x] Integration test scenarios identified from user stories (end-to-end scan from upload to SBOM download)

### Convention Consistency Compliance
- [x] Existing project patterns will be followed (branch-based workflow, PR review, constitution principles)
- [ ] Coding standards and architectural decisions documented (to be refined in research.md and data-model.md)
- [x] Dependency management strategy aligns with project standards (official Docker images, minimal new tech)

### Performance Awareness Compliance
- [x] Performance requirements specified at a high level (scan completes within minutes for typical projects; up to one hour for large ones)
- [ ] Scalability considerations documented for data/user growth (to be detailed in research.md)
- [x] Resource usage implications to be assessed when defining orchestration and storage strategy

## Project Structure

### Documentation (this feature)
```
specs/001-sbom-web-scanner/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Web-oriented structure with orchestration focus
src/
├── orchestration/       # Logic coordinating Fossology and ORT
├── adapters/            # Integration with Fossology and ORT APIs/CLI
├── sbom/                # SBOM formatting, validation, export
└── cli/                 # Optional CLI helpers if needed

tests/
├── integration/
└── unit/
```

**Structure Decision**: Web-style backend orchestration centered around Fossology UI as the primary interface.

## Phase 0: Outline & Research

Planned outputs in `research.md`:
- Clarify implementation language and core frameworks for the orchestration layer.
- Decide where SBOM artifacts are stored and how long they are retained.
- Document best practices for integrating Fossology and ORT in Docker-based environments.
- Capture patterns for orchestrating long-running scans with progress and error reporting.

## Phase 1: Design & Contracts

Planned outputs:
- `data-model.md`: Entities for Project, Scan, SBOM Artifact, Integration Job, and their relationships.
- `contracts/`: High-level API or integration contracts describing how the orchestration layer interacts with Fossology and ORT (even if primarily via their UIs/CLIs), and any internal endpoints if needed.
- `quickstart.md`: Steps for running the Docker images together, wiring integration, and running a full scan from upload through SBOM download.

## Phase 2: Task Planning Approach

**Task Generation Strategy**:
- Derive tasks from contracts, data model, and quickstart:
  - Integration tasks for wiring Fossology and ORT.
  - Orchestration tasks for scan lifecycle and SBOM generation.
  - Testing tasks for end-to-end and edge-case flows.

**Ordering Strategy**:
- Design and contracts first.
- Integration scaffolding and orchestration flow next.
- Hardening (error handling, performance, observability) after core path works.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| Coordinating two external systems (Fossology + ORT) | Required to produce complete SBOMs from both code and manifest-based dependencies | Using only one tool would miss key dependency sources or require heavy custom logic |

## Progress Tracking

**Phase Status**:
- [x] Phase 0: Research outline defined (this plan)
- [ ] Phase 0: Research complete
- [ ] Phase 1: Design complete
- [ ] Phase 2: Task planning complete

**Gate Status**:
- [ ] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [ ] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

