# Feature Specification: Web SBOM Scanner

**Feature Branch**: `001-sbom-web-scanner`  
**Created**: 2025-11-19  
**Status**: Draft  
**Input**: User description: "我想要設計一個網頁應用程式可以用來掃描指定的專案原始碼，然後產生 SBOM, 支援 SPDX 與 CycloneDX 格式。除了可以根據當前專案目錄的程式碼產生之外，還能夠掃描 package manager 描述檔案，找出相依的第三方軟體組件，並確保這些用到的第三方組件也要描述在 SBOM 中。"

---

## Clarifications

### Session 2025-11-19

- Q: How are users authenticated and authorized for the web SBOM scanner? → A: 使用Fossology內建的登入機制

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a developer or compliance engineer, I want a browser-based application
where I can select a project to scan, so that I can automatically generate a
complete Software Bill of Materials (SBOM) for that project in SPDX and
CycloneDX formats, including all third-party dependencies discovered from
both source code and package manager manifest files.

### Acceptance Scenarios
1. **Given** a user opens the web application and selects a project to scan,
   **When** they start a scan,
   **Then** the system analyzes the project source and relevant package
   manager manifest files and generates downloadable SBOM files in SPDX and
   CycloneDX formats.
2. **Given** a project that declares third-party dependencies in package
   manager manifest files,
   **When** the user runs a scan,
   **Then** the resulting SBOM includes entries for those third-party
   components in addition to components discovered directly from the project
   source.
3. **Given** the system cannot access or parse a relevant manifest file,
   **When** the scan completes,
   **Then** the user sees a clear warning describing which manifests were not
   processed and how this may affect the completeness of the SBOM.
4. **Given** Fossology completes its portion of a scan but OSS Review Toolkit
   encounters an error,
   **When** the scan completes,
   **Then** the user is informed that third-party dependency coverage is
   partial and is directed to retry once the ORT issue is resolved.

### Edge Cases
- Projects that contain no recognizable package manager manifests but do have
  source code.
- Projects with multiple manifest files for different ecosystems (for
  example, one for backend and one for frontend).
- Very large projects where scanning may take noticeable time or require
  progress feedback, including scans that may run for up to about one hour
  under normal operating conditions, with visible job states.
- Projects where manifest files declare dependencies that cannot be resolved
  or mapped to SBOM components.
- Users attempting to scan projects that are too large or exceed configured
  limits for a single scan, in which case the system MUST clearly explain
  that the configured maximum project size or scan time has been exceeded.

---

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The system MUST allow a user to initiate a scan for a specific
  project through a web-based interface.
- **FR-002**: The system MUST analyze the project source code in the selected
  location to identify first-party components for inclusion in the SBOM.
- **FR-003**: The system MUST detect and parse common package manager
  manifest files in the project (for example, files that declare third-party
  dependencies) and use them to identify third-party software components.
- **FR-004**: The system MUST generate SBOM outputs in both SPDX and
  CycloneDX formats for each completed scan.
- **FR-005**: The system MUST include in the SBOM both first-party components
  and all third-party components discovered from package manager manifests,
  so that the SBOM provides a holistic view of the project's software
  composition.
- **FR-005a**: The system MUST orchestrate Fossology and OSS Review Toolkit in
  a defined order so that Fossology handles upload-based scanning and license
  analysis while ORT processes the same project inputs to enumerate resolved
  third-party dependencies referenced in manifests.
- **FR-006**: The system MUST present a summary of scan results to the user,
  including counts of components discovered and any warnings about incomplete
  or partial analysis.
- **FR-007**: The system MUST allow users to download SBOM artifacts for a
  completed scan in at least SPDX and CycloneDX formats.
- **FR-008**: The system MUST provide clear error messages and guidance when
  a scan cannot be completed (for example, due to invalid project selection
  or missing permissions).
- **FR-009**: The system MUST log scan activity and outcomes (success,
  failure, warnings) so that users can audit what was scanned and when.
- **FR-010**: The system MUST allow users to re-run a scan for the same
  project to regenerate SBOMs after the project changes.
- **FR-011**: The system MUST support scanning projects that reside on or are
  accessible from the environment where the web application is deployed, with
  projects provided through an upload-based workflow in the underlying
  scanning backend rather than direct repository integration or arbitrary file
  system browsing.
- **FR-012**: The system SHOULD provide progress indication for scans that
  take longer than a short threshold (for example, multiple seconds) so users
  understand that work is ongoing.
- **FR-013**: The system MUST respect any configured limits on what projects
  can be scanned (for example, allowed locations or size limits) to avoid
  misuse, including enforcing organization-defined policies on which internal
  storage locations and uploaded project archives are eligible for scanning.
- **FR-014**: The system MUST require users to authenticate via the existing
  login mechanism provided by the underlying scanning web interface before
  they can initiate scans or view and download SBOM artifacts, and MUST not
  permit anonymous access.
- **FR-015**: The system MUST surface integration warnings when Fossology and
  ORT produce divergent or partial results, explaining which tool encountered
  issues and how the SBOM output was affected.

### Success Criteria
- At least 90% of typical projects (defined as uploads up to 5 GB or 200k
  files) can be successfully scanned and produce SBOMs in both SPDX and
  CycloneDX formats without manual intervention, completing within five
  minutes of active processing time.
- For projects with known and supported package manager manifests, at least
  95% of declared third-party dependencies are represented as components in
  the generated SBOMs.
- Integration between Fossology and ORT is considered successful when both
  systems produce component inventories whose counts differ by no more than
  2% for overlapping scopes, or else the user is given explicit warnings
  describing any discrepancies.
- Users report that they understand the status of scans and how to download
  and interpret SBOM outputs, as measured by a high rate of successful
  completion of the primary user task in usability reviews.

### Non-Functional Requirements
- Performance: Long-running scans (up to one hour) MUST expose job state and
  progress updates at least every two minutes; typical scans MUST finish
  within five minutes of processing time as noted earlier.
- Resource Usage: The orchestration layer MUST document CPU, memory, and disk
  expectations for Fossology and ORT containers and provide guardrails to
  prevent exhausted resources from impacting other internal workloads.
- Security: SBOM artifacts and scan logs MUST reside in organization-managed
  storage with access governed by the same authentication mechanism used by
  Fossology, and sensitive metadata MUST not be exposed outside the internal
  network.

### Assumptions
- The primary users are developers, security engineers, or compliance
  stakeholders who already have access to the projects being scanned.
- Projects to be scanned are hosted in environments that the web application
  can access without needing to handle complex cross-organization access
  workflows.
- The initial release focuses on a prioritized set of package manager
  manifest formats based on common usage; additional ecosystems can be added
  in future iterations.
- Official Fossology and OSS Review Toolkit Docker images are available in
  the target environment, and the orchestrator can run them with the required
  permissions.
- The orchestration layer can rely on the existing Fossology authentication
  flow and internal network connectivity; no external multi-tenant exposure
  is required.
- SBOM artifacts are stored in organization-controlled storage with retention
  policies configured by administrators outside the scope of this feature.

### Dependencies
- Access to the project source code and manifest files is available from the
  environment where the web application runs.
- Organizational policies allow generating and storing SBOM artifacts for the
  scanned projects.
- Any downstream tooling or processes that will consume the generated SBOMs
  (for example, compliance reporting or security analysis) can already handle
  SPDX and CycloneDX formats.
- SBOM storage endpoints and retention settings are configured before scans
  begin, and the orchestration layer captures artifact identifiers and
  locations for auditability.

---

## Key Entities
- **Project**: A collection of source code and related files that the user
  selects for scanning. A project may contain one or more package manager
  manifest files.
- **Manifest File**: A file that describes third-party software dependencies
  for a project or a part of a project (for example, a dependency
  declaration file for a specific ecosystem).
- **Component**: A first-party or third-party software element that appears
  in the SBOM, including metadata such as name, version, and relationship to
  the project.
- **Scan**: A single execution of the analysis process for a project,
  producing SBOM artifacts and associated status, warnings, and logs.
- **SBOM Artifact**: A machine-readable document that describes the
  components and relationships in a project, generated in a specific format
  such as SPDX or CycloneDX.
- **Integration Warning**: Metadata produced when Fossology or ORT cannot
  complete part of the analysis, including cause, affected manifests or
  components, and required operator follow-up.

---

## Non-Goals
- Managing or enforcing license compliance decisions based on SBOM contents.
- Performing vulnerability analysis or risk scoring for components listed in
  the SBOM.
- Providing advanced user management, access control, or multi-tenant
  features beyond what is necessary for the initial deployment.
- Deep integration with specific development platforms or repository hosting
  services beyond what is minimally required to access projects for scanning.

---

## Risks & Open Questions
- Risk that very large projects or deeply nested dependency graphs may lead
  to long scan times or resource constraints.
- Risk that missing or non-standard manifest files could lead to incomplete
  SBOMs and user confusion.
- Risk that users may misinterpret the completeness of SBOMs without clear
  explanations of what was scanned and what was not.
- The initial deployment model assumes an internally hosted environment (for
  example, on-premises or a private cloud within a single organization),
  which reduces multi-tenant privacy concerns but requires alignment with
  internal security and access-control policies.
