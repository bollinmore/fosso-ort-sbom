# Research: Web SBOM Scanner (Fossology + OSS Review Toolkit)

## Implementation Language and Framework

- Decision: Use a backend-friendly language and framework that integrates well with Dockerized
  tools (for example, a language already common in the organization).
- Rationale: The orchestration layer primarily needs to invoke Dockerized Fossology and ORT, manage
  scan lifecycles, and handle SBOM artifacts. Any language with solid process orchestration and
  HTTP capabilities is suitable.
- Alternatives considered: Tight coupling to a specific web framework or language is not required
  at the research stage; the spec remains technology-agnostic.

## SBOM Storage and Retention

- Decision: Store generated SBOM artifacts in a location controlled by the organization, with
  retention and deletion policies defined by internal governance rather than hard-coding a fixed
  duration into this feature.
- Rationale: Different organizations may have varying compliance and retention requirements for
  SBOM data. Keeping retention policy configurable avoids premature constraints.
- Alternatives considered: Fixed retention windows (for example, 90 days) were considered but
  rejected for now due to varying compliance needs.

## Integration: Fossology and OSS Review Toolkit with Docker

- Decision: Use the official Fossology and ORT Docker images as the foundation, running them in the
  same internal environment and configuring ORT so that it can analyze the same project inputs used
  by Fossology.
- Rationale: Official images are maintained by the respective projects, reducing maintenance
  overhead and aligning with best practices for deployment.
- Alternatives considered: Custom-built images or installing tools directly on the host were
  considered but would increase operational complexity without clear benefit.

## Orchestration Pattern for Long-Running Scans

- Decision: Treat each scan as a long-running job with clear states (queued, running, completed,
  failed) and ensure that progress can be communicated back to users through the Fossology UI or
  related status views.
- Rationale: SBOM generation for large projects can take significant time; modeling scans as jobs
  with explicit states improves transparency and reliability.
- Alternatives considered: Synchronous request/response scanning was rejected because it does not
  handle long-running operations or failures as robustly.

