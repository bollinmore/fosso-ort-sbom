#!/usr/bin/env bash

# Consolidated prerequisite checking script for SpecKit workflows.
#
# Usage: ./check-prerequisites.sh [OPTIONS]
#   --json          Output in JSON format
#   --paths-only    Only output path variables (no validation)

set -e

JSON_MODE=false
PATHS_ONLY=false
REQUIRE_TASKS=false
INCLUDE_TASKS=false

for arg in "$@"; do
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --paths-only)
            PATHS_ONLY=true
            ;;
        --require-tasks)
            REQUIRE_TASKS=true
            ;;
        --include-tasks)
            INCLUDE_TASKS=true
            ;;
        --help|-h)
            echo "Usage: $0 [--json] [--paths-only] [--require-tasks] [--include-tasks]"
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option '$arg'. Use --help for usage information." >&2
            exit 1
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

eval "$(get_feature_paths)"

# In this repository, we treat the existing feature directory as authoritative
if [[ ! -d "$FEATURE_DIR" ]]; then
    echo "ERROR: Feature directory not found: $FEATURE_DIR" >&2
    echo "Run /speckit.specify first to create the feature structure." >&2
    exit 1
fi

if [[ ! -f "$IMPL_PLAN" ]]; then
    echo "ERROR: plan.md not found in $FEATURE_DIR" >&2
    echo "Run /speckit.plan first to create the implementation plan." >&2
    exit 1
fi

if $REQUIRE_TASKS && [[ ! -f "$TASKS" ]]; then
    echo "ERROR: tasks.md not found in $FEATURE_DIR" >&2
    echo "Run /speckit.tasks first to generate the task list." >&2
    exit 1
fi

AVAILABLE_DOCS=()
[[ -f "$FEATURE_SPEC" ]] && AVAILABLE_DOCS+=("spec.md")
[[ -f "$IMPL_PLAN" ]] && AVAILABLE_DOCS+=("plan.md")
[[ -f "$RESEARCH" ]] && AVAILABLE_DOCS+=("research.md")
[[ -f "$DATA_MODEL" ]] && AVAILABLE_DOCS+=("data-model.md")
if [[ -d "$CONTRACTS_DIR" ]] && [[ -n "$(ls -A "$CONTRACTS_DIR" 2>/dev/null)" ]]; then
    AVAILABLE_DOCS+=("contracts/")
fi
[[ -f "$QUICKSTART" ]] && AVAILABLE_DOCS+=("quickstart.md")
if $INCLUDE_TASKS && [[ -f "$TASKS" ]]; then
    AVAILABLE_DOCS+=("tasks.md")
fi

if $PATHS_ONLY && ! $JSON_MODE; then
    echo "REPO_ROOT: $REPO_ROOT"
    echo "FEATURE_DIR: $FEATURE_DIR"
    echo "FEATURE_SPEC: $FEATURE_SPEC"
    echo "IMPL_PLAN: $IMPL_PLAN"
    exit 0
fi

if $JSON_MODE; then
    if [[ ${#AVAILABLE_DOCS[@]} -eq 0 ]]; then
        docs_json="[]"
    else
        docs_json=$(printf '"%s",' "${AVAILABLE_DOCS[@]}")
        docs_json="[${docs_json%,}]"
    fi
    printf '{"FEATURE_DIR":"%s","AVAILABLE_DOCS":%s}\n' "$FEATURE_DIR" "$docs_json"
else
    echo "FEATURE_DIR:$FEATURE_DIR"
    echo "AVAILABLE_DOCS:"
    for d in "${AVAILABLE_DOCS[@]}"; do
        echo "  - $d"
    done
fi
