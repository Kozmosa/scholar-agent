# Repository Guidelines

## Instruction Priority

Agents working in this repository must treat [`PROJECT_BASIS.md`](PROJECT_BASIS.md) as a required long-lived constraints document.

- Follow `PROJECT_BASIS.md` for project goals, directory boundaries, documentation placement, coding standards, command entrypoints, and maintenance rules.
- If this file and `PROJECT_BASIS.md` overlap, apply the stricter rule.
- If a task-specific user instruction conflicts with `PROJECT_BASIS.md`, follow the user instruction for that task and keep other `PROJECT_BASIS.md` rules intact.

## Project Structure & Module Organization

This repository has two active concerns:

- `docs/`: source-of-truth Obsidian-style notes. Key areas are `docs/framework/`, `docs/projects/`, and `docs/summary/`.
- `src/ainrf/`: Python runtime scaffold for the AINRF CLI and future service code.
- `tests/`: CLI smoke tests for the Python package.
- `scripts/`: local build helpers for the notes site.
- `site/` and `.cache/html-notes/`: generated output; do not edit them directly.

Reference repositories live under `ref-repos/` and are treated as read-only research inputs.

## LLM Working Log

- `docs/LLM-Working/` is versioned working memory for plans, checklists, smoke notes, and agent-side implementation records.
- Daily work logs must live under `docs/LLM-Working/worklog/` using one file per day named `YYYY-MM-DD.md`.
- Before or during a work session, if today's file does not exist yet, create it first and keep appending to that same file for the rest of the day.
- Every key action must append one new log entry on the same day: file-edit batch, development/implementation batch, validation command run, and commit action all count.
- Each log entry must record at least the time, action type, and a concise summary. Commit entries must also record the commit hash and subject once available.
- Treat the worklog as append-only session history. Do not silently rewrite earlier entries unless you are correcting an objective factual mistake.

## Build, Test, and Development Commands

- `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build`: convert Obsidian notes and build the MkDocs site.
- `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py serve`: run the local docs preview server.
- `UV_CACHE_DIR=/tmp/uv-cache uv run ainrf --help`: inspect the CLI scaffold.
- `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`: run the current Python test suite.
- `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`: run lint checks.
- `UV_CACHE_DIR=/tmp/uv-cache uv run ruff format --check src tests`: verify formatting.

## Coding Style & Naming Conventions

Use 4-space indentation and keep Python compatible with `>=3.13`. All Python code in `src/ainrf/`, `tests/`, and `scripts/` must include strict type annotations. Treat missing annotations as defects, not optional cleanup. Use `snake_case` for files, functions, and variables; use `PascalCase` for classes.

For notes, keep file slugs in English and content in Chinese. Use Obsidian wikilinks like `[[framework/v1-rfc]]`, YAML frontmatter, and Mermaid fences when needed.

Formatting and linting are enforced with `ruff`; static type checking must pass with `ty`; pre-commit hooks are defined in `.pre-commit-config.yaml`.

## Testing Guidelines

Tests use `pytest`. Place new tests under `tests/` and name files `test_*.py`. Match function names to behavior, for example `test_serve_stub_runs`. Add or update smoke tests for every new CLI surface, parser behavior, or build-script contract you change.

Before submitting changes to Python code, run both runtime and static checks:

- `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
- `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`

## Commit & Pull Request Guidelines

Follow the existing commit style: short, imperative, and scoped when useful, e.g. `docs: revise framework...` or `chore: update gitignore`. Keep commits focused.

Pull requests should include:

- a brief summary of what changed,
- the commands you ran to validate it,
- screenshots only for docs/site rendering changes,
- links to related issues or design notes when applicable.

## Security & Configuration Tips

Do not commit secrets, SSH keys, or generated artifacts. Keep runtime state under `.ainrf/` out of version control. Prefer `uv run` over manual venv management so local execution matches the project lockfile.
