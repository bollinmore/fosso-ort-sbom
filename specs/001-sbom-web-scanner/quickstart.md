# Quickstart: Web SBOM Scanner (Fossology + OSS Review Toolkit)

1. Ensure the official Fossology and OSS Review Toolkit Docker images are available in the internal
   environment.
2. Deploy Fossology and verify that users can log in via the existing Fossology login mechanism.
3. Configure the orchestration layer so that project uploads handled through the Fossology web UI
   can also be analyzed by OSS Review Toolkit for dependency discovery.
4. Start a test project scan from the Fossology UI and confirm that SBOM artifacts in SPDX and
   CycloneDX formats are generated and accessible.

## Configuration

Set these environment variables (or docker-compose equivalents) before running scans:

| Component  | Variable                 | Description                                              |
|------------|--------------------------|----------------------------------------------------------|
| Fossology  | `FOSSOLOGY_DB_HOST`      | Hostname of the Fossology database container/service     |
| Fossology  | `FOSSOLOGY_DB_NAME`      | Database name (default `fossology`)                      |
| Fossology  | `FOSSOLOGY_DB_USER`      | Database user (e.g., `fossy`)                            |
| Fossology  | `FOSSOLOGY_DB_PASS`      | Database password                                        |
| ORT        | `ORT_DATA_DIR`           | Directory for ORT cache/results inside the container     |
| ORT        | `ORT_CONFIG_DIR` (opt)   | Optional directory for ORT configuration overrides       |
| Orchestration | `PROJECT_INPUT_DIR`   | Host path mounted into both Fossology and ORT containers |
| Orchestration | `SBOM_OUTPUT_DIR`     | Host or network path where SBOM artifacts are stored     |

Document any additional organization-specific variables (proxy, TLS, storage credentials) in this
quickstart so operators have a single reference.

## Status & Error Guidance

- **Queued** – scan registered and waiting for Fossology/ORT resources. No operator action required.
- **Running** – orchestration is collecting first-party components (Fossology) and third-party dependencies (ORT).
- **Completed** – SBOM artifacts were written to the configured `SBOM_OUTPUT_DIR`. Review warnings for any manifests that could not be parsed.
- **Failed** – orchestration could not complete. Review the job message in logs or CLI output; common causes are missing project directories, unreachable Docker containers, or malformed manifest files.
