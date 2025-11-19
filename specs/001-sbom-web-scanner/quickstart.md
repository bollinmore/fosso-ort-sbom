# Quickstart: Web SBOM Scanner (Fossology + OSS Review Toolkit)

1. Ensure the official Fossology and OSS Review Toolkit Docker images are available in the internal
   environment.
2. Deploy Fossology and verify that users can log in via the existing Fossology login mechanism.
3. Configure the orchestration layer so that project uploads handled through the Fossology web UI
   can also be analyzed by OSS Review Toolkit for dependency discovery.
4. Start a test project scan from the Fossology UI and confirm that SBOM artifacts in SPDX and
   CycloneDX formats are generated and accessible.

