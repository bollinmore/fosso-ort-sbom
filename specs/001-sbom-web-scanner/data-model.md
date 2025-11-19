# Data Model: Web SBOM Scanner

## Entities

### Project
- Represents a software project submitted for SBOM analysis.
- Key attributes:
  - Identifier (unique within the system)
  - Name or label provided by the user
  - Metadata about the upload or source location

### Scan
- Represents a single execution of analysis for a Project.
- Key attributes:
  - Identifier
  - Associated Project
  - Status (queued, running, completed, failed)
  - Start and end timestamps
  - Summary metrics (for example, number of components discovered)

### SBOM Artifact
- Represents a generated SBOM document for a Scan.
- Key attributes:
  - Identifier
  - Associated Scan
  - Format (SPDX or CycloneDX)
  - Location where the artifact is stored

### Integration Job
- Represents coordination steps between Fossology and ORT for a given Scan.
- Key attributes:
  - Identifier
  - Associated Scan
  - Status and any error messages

