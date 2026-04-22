#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

export UV_CACHE_DIR="${UV_CACHE_DIR:-/tmp/uv-cache}"

cd "${REPO_ROOT}"
exec uv run python scripts/run_webui.py "$@"

