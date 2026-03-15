# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

scholar-agent is an Obsidian-style knowledge base containing research notes on 8 academic research agent projects, plus a self-designed AI-Native Research Framework. Notes are written in Chinese with English file slugs. The repo also generates a static HTML site from these notes using MkDocs.

## Build & Serve Commands

```bash
# Build static site (converts Obsidian syntax, then runs mkdocs build)
scripts/build.sh

# Start local preview server
scripts/serve.sh

# Or run directly via uv
uv run python scripts/build_html_notes.py build
uv run python scripts/build_html_notes.py serve
```

Dependencies are managed by `uv` (see `pyproject.toml`). No separate install step needed — `uv run` handles the venv automatically.

## Architecture

### Build Pipeline

`scripts/build_html_notes.py` is the core build script. It:

1. Reads all `.md` files from `docs/` (the source of truth)
2. Converts Obsidian-only syntax to MkDocs-compatible Markdown:
   - `[[wikilinks]]` → standard `[label](relative-path.md)` links
   - Obsidian callouts (`> [!type]`) → MkDocs admonitions (`!!! type`)
   - Validates all internal links and fails on unresolved wikilinks
3. Computes backlinks and appends a "反向链接" section to each note
4. Writes processed files to `.cache/html-notes/docs/` (the `docs_dir` in `mkdocs.yml`)
5. Runs `mkdocs build` or `mkdocs serve` against the generated output

Important: never edit files under `.cache/html-notes/` or `site/` — they are generated. Edit only files under `docs/`.

### Directory Layout

- `docs/` — Source Obsidian notes (the only files you should edit)
  - `docs/index.md` — Top-level research index
  - `docs/projects/` — Per-project research reports (one per reference repo)
  - `docs/framework/` — AI-Native Research Framework design notes
  - `docs/summary/` — Cross-project comparison and capability matrix
- `ref-repos/` — Cloned reference repositories (read-only research subjects, gitignored)
- `.codex-skill-staging/` — Codex skill definitions (build-obsidian-mkdocs-site, write-obsidian-project-docs)
- `scripts/` — Build tooling
- `mkdocs.yml` — MkDocs config (Material theme, Mermaid, zh language)

### Note Conventions

- Frontmatter: YAML with `aliases`, `tags`, `source_repo`, `source_path`
- Internal links: use `[[note-name]]` or `[[note-name|label]]` syntax (Obsidian wikilinks)
- Callouts: use Obsidian `> [!type]` syntax, not MkDocs admonitions directly
- Diagrams: use Mermaid fenced code blocks (vendored JS at `docs/assets/javascripts/vendor/`)
- File naming: English slugs, content in Chinese
