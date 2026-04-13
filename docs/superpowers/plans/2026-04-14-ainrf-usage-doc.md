# AINRF Usage Docs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `docs/ainrf/index.md` as a single-page Chinese usage guide that documents the current, real AINRF command surface and the repo’s actual preview/service startup commands.

**Architecture:** Keep the change documentation-only. Create one new note under `docs/ainrf/` with YAML frontmatter and Obsidian-compatible structure, and do not invent unimplemented frontend/backend capabilities. Validate the page by building the docs site so the new note fits the existing MkDocs/Obsidian pipeline.

**Tech Stack:** Markdown, Obsidian wikilinks, MkDocs, Python build script, uv

---

## File Structure / Target Surface Map

### New file
- Create: `docs/ainrf/index.md` — single-page AINRF usage document covering positioning, quick start, preview commands, service startup commands, and boundaries

### Existing files to reference during implementation
- Read: `src/ainrf/cli.py` — current CLI command surface (`--version`, `serve`, `onboard`, `container add`)
- Read: `src/ainrf/server.py` — confirms `serve` is the API server entry
- Read: `CLAUDE.md` — repo-level command and documentation rules
- Read: `PROJECT_BASIS.md` — long-lived command/documentation constraints

### Validation target
- Run: `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` — confirms the new note is compatible with the docs build pipeline

### Worklog target
- Modify: `docs/LLM-Working/worklog/2026-04-14.md` — append one completed-slice changelog entry after implementation and validation finish

---

### Task 1: Create the single-page AINRF usage note

**Files:**
- Create: `docs/ainrf/index.md`
- Read while implementing: `src/ainrf/cli.py`, `src/ainrf/server.py`, `CLAUDE.md`, `PROJECT_BASIS.md`

- [ ] **Step 1: Create the note with required frontmatter and title**

Create `docs/ainrf/index.md` with this opening structure:

```markdown
---
aliases:
  - AINRF 使用说明
  - AINRF Commands
tags:
  - ainrf
  - runtime
  - docs
  - obsidian-note
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# AINRF 使用文档
```

- [ ] **Step 2: Write the positioning and quick-start section**

Add this content after the title:

```markdown
> [!abstract]
> 本文档只记录当前仓库里已经存在、可以直接使用或已经明确暴露出来的 AINRF 命令入口，不把未来规划中的能力写成已实现功能。

## AINRF 是什么

- `ainrf` 是当前仓库中的运行时 CLI / API 服务入口。
- 当前仓库更准确的形态是：一套正在收敛中的 daemon/runtime shell，加上文档站点预览入口。
- 因此，本文档只解释当前真实可用的命令面，不扩写历史蓝图或未来产品设想。

## 快速开始

先确认 CLI 可以被调用：

```bash
uv run ainrf --version
uv run ainrf --help
```

说明：

- `uv run ainrf --version`：查看当前安装的 `ainrf` 版本。
- `uv run ainrf --help`：查看当前 CLI 暴露的命令入口。
```

- [ ] **Step 3: Write the preview and runtime command sections**

Append these sections exactly:

```markdown
## 启动文档预览

如果你想预览 `docs/` 下的知识库站点，可以使用：

```bash
scripts/serve.sh
```

或者直接运行底层命令：

```bash
uv run python scripts/build_html_notes.py serve
```

这也是当前仓库里最接近“前端预览”的入口，因为它会启动 MkDocs 站点预览服务，而不是启动一个独立的产品前端应用。

## 构建文档站点

如果你只想生成静态站点构建结果，可以运行：

```bash
scripts/build.sh
```

或者：

```bash
uv run python scripts/build_html_notes.py build
```

## 启动 AINRF 服务

AINRF 当前的服务入口是：

```bash
uv run ainrf serve
```

如果需要显式指定监听地址、端口或状态目录，可以先查看帮助：

```bash
uv run ainrf serve --help
```

根据当前 CLI 表面，`serve` 是 AINRF API 服务的启动命令；它不是历史文档里那种完整研究平台的同义词，而是当前保留下来的运行时服务入口。

## 首次初始化

如果当前目录还没有 AINRF 运行时配置，可以先执行：

```bash
uv run ainrf onboard
```

该命令用于初始化当前工作目录下的 AINRF 配置。
```

- [ ] **Step 4: Write the remaining command and boundary sections**

Append these sections exactly:

```markdown
## 其他命令入口

当前 CLI 还暴露了容器配置相关入口，例如：

```bash
uv run ainrf container add
```

可以先通过帮助命令查看完整参数：

```bash
uv run ainrf container add --help
```

如果你只想查看当前命令面，最稳妥的入口仍然是：

```bash
uv run ainrf --help
```

## 常用开发与验证命令

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

这些命令分别用于：

- 运行测试
- 检查 lint 问题
- 检查代码格式是否符合仓库规范

## 说明与边界

- `docs/` 是长期维护的知识库源目录。
- `.cache/html-notes/` 和 `site/` 是生成产物，不应手工编辑。
- 当前仓库里更接近“前端”的是文档站点预览服务，而不是独立 Web App。
- 当前仓库里更接近“后端”的是 `uv run ainrf serve` 启动的 API 服务。
- 如果某个能力只在历史 RFC / roadmap 中出现，但没有体现在当前 CLI 或代码表面，就不应视为当前可用功能。

## 关联笔记

- [[framework/index]]
- [[framework/ai-native-research-framework]]
- [[index]]
```

- [ ] **Step 5: Review the note for wording discipline**

Check the finished file and make sure:

- it never claims there is an already-implemented standalone frontend
- it never claims there is a complete autonomous research backend
- every command shown exists in the current repo surface
- the prose stays in Chinese and the path stays under `docs/ainrf/`

- [ ] **Step 6: Commit**

```bash
git add docs/ainrf/index.md
git commit -m "docs: add ainrf usage guide"
```

---

### Task 2: Validate the new note against the docs pipeline

**Files:**
- Validate: `docs/ainrf/index.md`
- Run against: `scripts/build_html_notes.py`, `mkdocs.yml`

- [ ] **Step 1: Run the docs build**

Run:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build
```

Expected: the build completes successfully without unresolved wikilinks or Markdown conversion errors.

- [ ] **Step 2: If the build fails on wikilinks or frontmatter, make the minimal fix in `docs/ainrf/index.md`**

Use these adjustment rules only if needed:

```markdown
- Keep wikilinks in the form `[[framework/index]]` or `[[index]]`
- Keep YAML frontmatter valid
- Do not add unrelated documentation changes elsewhere
```

- [ ] **Step 3: Re-run the docs build and confirm success**

Run again:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build
```

Expected: PASS.

- [ ] **Step 4: Append the implementation changelog entry**

Append one line to `docs/LLM-Working/worklog/2026-04-14.md` in this shape:

```markdown
2026-04-14 HH:MM changelog：完成 AINRF 用法文档落地，新建 docs/ainrf/index.md，整理当前可用 CLI、文档预览与服务启动命令；验证：执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。
```

Replace `HH:MM` with the actual local time when the slice is done.

- [ ] **Step 5: Commit**

```bash
git add docs/ainrf/index.md docs/LLM-Working/worklog/2026-04-14.md
git commit -m "docs: validate ainrf usage page"
```

---

## Self-review

### Spec coverage
- Single-page doc under `docs/ainrf/index.md`: covered by Task 1
- Only current real commands, no speculative features: covered by Task 1 steps 2-5
- Include preview/startup/service/dev-validation commands: covered by Task 1 steps 2-4
- Validate with docs pipeline: covered by Task 2 steps 1-3
- Record completed slice in worklog: covered by Task 2 step 4

### Placeholder scan
- No `TBD`, `TODO`, or deferred implementation markers remain in the plan.
- All file paths and commands are explicit.

### Scope check
- The work is a single documentation slice, not multiple independent subsystems.
- No extra refactor or runtime code changes are included.
