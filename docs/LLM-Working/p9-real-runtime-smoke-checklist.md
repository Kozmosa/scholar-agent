# P9 Real Runtime Smoke Checklist

## Purpose

Run and diagnose the real container smoke test for `ClaudeCodeAdapter` with stable failure categories.

## Required Environment

- `AINRF_CONTAINER_HOST` (required)
- `AINRF_CONTAINER_PORT` (optional, default `22`)
- `AINRF_CONTAINER_USER` (optional)
- `AINRF_CONTAINER_SSH_KEY_PATH` (optional)
- `AINRF_CONTAINER_PROJECT_DIR` (optional)

Remote container requirements:

- Claude Code CLI available (or installable)
- Python available
- `ANTHROPIC_API_KEY` configured in remote environment
- Project directory writable

## Run Command

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest \
  tests/test_claude_code_adapter.py::test_claude_code_adapter_e2e_smoke_with_real_runtime -q
```

## Failure Classification

Preflight classifies failures into:

- `ssh_unreachable`
- `claude_unavailable`
- `anthropic_api_key_missing`
- `project_dir_not_writable`

Warnings (non-blocking unless preflight fails):

- `gpu_unavailable`
- `cuda_unavailable`
- `disk_probe_failed`

## Current Local Result

- If `AINRF_CONTAINER_HOST` is not set, pytest reports `s` (skipped).
- This is expected and keeps CI/local deterministic without remote secrets.
