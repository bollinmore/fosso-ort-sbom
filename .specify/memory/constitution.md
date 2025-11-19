<!--
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- List of modified principles: N/A (Initial Creation)
- Added sections: Core Principles, Development Workflow, Governance
- Removed sections: N/A
- Templates requiring updates:
  - ⚠ .specify/templates/plan-template.md (file not yet created)
  - ⚠ .specify/templates/spec-template.md (file not yet created)
  - ⚠ .specify/templates/tasks-template.md (file not yet created)
- Follow-up TODOs:
  - TODO(TEMPLATES): Create SpecKit templates aligned with this constitution.
-->
# fosso-ort-sbom Constitution

## Core Principles

### I. Code Quality & Maintainability
All production code MUST be simple, readable, and maintainable. Complex logic MUST be clearly
structured and documented so that any contributor can understand, modify, and safely extend it.
Dead code, duplicated logic, and ad-hoc patterns MUST be actively removed or refactored.

Rationale: A clear and coherent codebase is essential for long-term sustainability of SBOM
generation workflows and for minimizing regression risk as tooling and compliance requirements
evolve.

### II. Testing Discipline & Coverage
All new features, bug fixes, and configuration changes that affect behavior MUST be covered by
automated tests (unit, integration, or end-to-end as appropriate). The test suite MUST be kept
green in the default branch, and any failing tests MUST be treated as release-blocking defects.

Tests MUST verify:
- Correct SBOM generation for representative project types and dependency graphs.
- Error handling for invalid inputs, external tool failures, and configuration issues.
- Integration boundaries with Fossology, OSS-Review-Toolkit, and other external systems.

Rationale: Reliable SBOM generation depends on trustworthy automation. Strong tests are the primary
defense against regressions in security, licensing, and dependency reporting.

### III. User Experience Consistency
Command-line interfaces, configuration formats, and outputs (including SBOM artifacts, logs, and
status messages) MUST be consistent, predictable, and discoverable. Breaking changes to user-facing
behavior MUST follow semantic versioning rules and include clear migration guidance.

User-facing behavior MUST:
- Use consistent terminology and option naming across commands and configuration.
- Provide meaningful error messages and actionable guidance for recovery.
- Preserve stable defaults that are safe and sensible for typical use cases.

Rationale: Consistent user experience reduces operator error, shortens onboarding time, and
increases trust in the generated SBOMs and related reports.

### IV. Performance & Resource Efficiency
SBOM generation workflows MUST be designed to run efficiently on typical CI/CD infrastructure and
developer machines. Changes that may impact performance or resource usage MUST be evaluated and, if
material, tested against representative repositories.

Performance requirements include:
- Avoiding unnecessary scans, duplicate work, or redundant network calls.
- Streaming or incremental processing where feasible to limit peak memory usage.
- Clear documentation of any configuration options that significantly affect runtime or resources.

Rationale: Efficient SBOM generation is necessary to keep CI pipelines fast, reduce infrastructure
costs, and ensure the tool remains usable for large codebases.

## Development Workflow

The project MUST follow a branch-based workflow (e.g., GitFlow or trunk-based with feature
branches) where all work lands via pull requests. Each pull request MUST:
- Be linked to a clear change description or issue.
- Include tests or an explicit justification for any exceptions.
- Receive at least one approval from a contributor other than the author.

Changes that affect user-facing behavior, performance characteristics, or integration points MUST
be called out explicitly in the pull request description and reviewed with these principles in
mind.

## Governance

This Constitution defines the non-negotiable standards for the fosso-ort-sbom project. All
contributors, reviewers, and maintainers are responsible for enforcing it.

Amendments:
- Any change to these principles MUST be proposed via a pull request that clearly describes the
  motivation, impact, and migration considerations.
- Backward-incompatible changes to principles or governance MUST be treated as MAJOR changes.
- Additions or substantial expansions of principles or sections MUST be treated as MINOR changes.
- Clarifications, typo fixes, and non-semantic wording updates MUST be treated as PATCH changes.

Versioning:
- The Constitution version MUST follow semantic versioning (MAJOR.MINOR.PATCH).
- Each ratified amendment MUST update the Constitution version and the "Last Amended" date.
- The Sync Impact Report at the top of this document MUST be updated with each amendment.

Compliance:
- Code reviews MUST explicitly consider alignment with Core Principles, Development Workflow, and
  Governance sections.
- Pull requests that violate MUST-level requirements MUST NOT be merged until they are brought into
  compliance or the Constitution is formally amended.

**Version**: 1.0.0 | **Ratified**: 2025-11-19 | **Last Amended**: 2025-11-19

