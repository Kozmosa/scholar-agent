# AINRF Usage Documentation Design

## Context

用户希望在 `docs/` 下新增 `ainrf/` 目录，并补充一份结构化的 AINRF 用法文档。该文档应只描述仓库中当前真实可用、已声明的命令入口，不把未来规划能力伪装成已可使用功能。

仓库当前同时包含两类与“启动”相关的入口：

- 文档站点预览入口：`scripts/serve.sh` 或 `uv run python scripts/build_html_notes.py serve`
- AINRF CLI / API 服务入口：`uv run ainrf serve`

因此，文档需要把用户口中的“启动前端、启动后端”等说法，映射到本仓库当前实际存在的启动方式，并明确边界，避免误导读者。

## Goal

在 `docs/ainrf/index.md` 新增一篇单页入口文档，面向希望快速上手当前仓库 AINRF 命令面的读者，提供：

- AINRF 当前定位的简要说明
- 当前可用 CLI 命令的快速开始
- 文档预览服务的启动方式
- AINRF API 服务的启动方式
- 常用开发与验证命令
- 当前“前端 / 后端 / 运行入口”在本仓库中的对应关系与边界说明

## Non-goals

本次不包括：

- 虚构尚未实现的前端应用、后端服务或任务调度能力
- 为未来蓝图补写详尽产品说明
- 拆分多篇 AINRF 文档
- 修改 `.cache/html-notes/`、`site/` 或其他生成产物
- 修改 AINRF 运行时代码或命令行为

## Proposed documentation shape

### File location

新增目录与文件：

- `docs/ainrf/`
- `docs/ainrf/index.md`

该文件作为 `docs/ainrf/` 下唯一入口页，保持单页结构，方便从知识库和站点中直接阅读。

### Document structure

建议按以下顺序组织内容：

1. **AINRF 是什么**
   - 用简短中文说明 AINRF 在当前仓库中的定位
   - 强调本文档聚焦“当前可用命令面”

2. **快速开始**
   - `uv run ainrf --version`
   - `uv run ainrf --help`
   - 用于确认安装和查看命令入口

3. **启动文档预览**
   - `scripts/serve.sh`
   - `uv run python scripts/build_html_notes.py serve`
   - 解释这是当前仓库最接近“前端预览”的入口，因为它提供 MkDocs 站点界面

4. **启动 AINRF 服务**
   - `uv run ainrf serve`
   - 如有必要，补充 host/port/daemon 相关参数的最小说明
   - 说明该命令用于启动 AINRF API 服务

5. **运行与其他命令入口**
   - `uv run ainrf onboard`
   - `uv run ainrf run`
   - 对 `run` 采取谨慎表述：若当前仓库未提供完整实现，则只说明它是已声明入口，不夸大能力

6. **常用开发与验证命令**
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run ruff format --check .`
   - 可补充 build 命令，帮助读者区分“运行文档站点”和“启动 AINRF 服务”

7. **说明与边界**
   - `docs/` 是长期文档源
   - `.cache/html-notes/` 与 `site/` 是生成产物，不手工修改
   - 当前“前端”更准确是文档站点预览；当前“后端”更准确是 `ainrf serve` 暴露的 API 服务

## Approach options considered

### Option A: single-page quickstart plus command guide (recommended)

把所有内容写进 `docs/ainrf/index.md` 一页中，兼顾入门路径和命令参考。

- 优点：最符合用户要求；结构简单；当前信息量适中；不容易因为拆页导致空洞
- 缺点：后续若 AINRF 文档面变大，可能需要再拆分

### Option B: multi-page split by topic

拆成 `index.md`、`cli.md`、`serve.md` 等多页。

- 优点：长期可扩展性更强
- 缺点：对当前仓库是过度设计；用户已明确希望单页入口

### Option C: pure command reference page

只列命令，不写上下文说明。

- 优点：查询速度快
- 缺点：无法解释“前端 / 后端”在当前仓库中的真实对应关系，容易让首次阅读者误解

推荐采用 **Option A**。

## Content boundaries and wording rules

文档写作时应遵守以下边界：

- 只写代码、README、CLI 表面中当前真实存在的入口
- 用“当前可用”“当前仓库中对应为”“目前可通过”这类表述，避免承诺未来能力
- 如果某个命令存在但能力仍偏 scaffold，应直说“当前为命令入口 / scaffold 表面”
- 不使用“前端应用已经实现”“后端完整可用平台”这类超出事实的描述

## Validation

完成后需要至少做以下验证：

1. 文档文件位于 `docs/ainrf/index.md`
2. 文档使用现有仓库约定：YAML frontmatter、中文正文、英文 slug 路径
3. 文中命令与当前代码 / CLAUDE.md / PROJECT_BASIS.md 一致
4. 如进行站点验证，应优先使用仓库标准命令，确认不会引入明显构建问题

## Success criteria

完成后，读者应能通过 `docs/ainrf/index.md` 明确知道：

- 当前 AINRF 有哪些可用命令入口
- 如何查看 CLI 帮助与版本
- 如何启动文档站点预览
- 如何启动 AINRF API 服务
- 当前仓库里“前端 / 后端”的实际含义是什么
- 哪些内容是当前可用，哪些只是保守说明而非功能承诺
