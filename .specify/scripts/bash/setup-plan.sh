#!/usr/bin/env bash

set -e

JSON_MODE=false
for arg in "$@"; do
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --help|-h)
            echo "Usage: $0 [--json]"
            exit 0
            ;;
        *)
            ;;
    esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
FEATURE_SPEC="$REPO_ROOT/specs/001-sbom-web-scanner/spec.md"
IMPL_PLAN="$REPO_ROOT/specs/001-sbom-web-scanner/plan.md"
SPECS_DIR="$REPO_ROOT/specs/001-sbom-web-scanner"
BRANCH="001-sbom-web-scanner"

mkdir -p "$SPECS_DIR"

TEMPLATE="$REPO_ROOT/.specify/templates/plan-template.md"
if [ -f "$TEMPLATE" ]; then
    cp "$TEMPLATE" "$IMPL_PLAN"
else
    touch "$IMPL_PLAN"
fi

if $JSON_MODE; then
    printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","SPECS_DIR":"%s","BRANCH":"%s"}\n' \
        "$FEATURE_SPEC" "$IMPL_PLAN" "$SPECS_DIR" "$BRANCH"
else
    echo "FEATURE_SPEC: $FEATURE_SPEC"
    echo "IMPL_PLAN: $IMPL_PLAN"
    echo "SPECS_DIR: $SPECS_DIR"
    echo "BRANCH: $BRANCH"
fi

