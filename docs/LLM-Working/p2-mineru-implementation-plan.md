---
aliases:
  - P2 MinerU Implementation Plan
  - P2 论文解析客户端规划
tags:
  - ainrf
  - orchestrator
  - paper-ingestion
  - mineru
  - implementation-plan
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: e89118b
---
# P2 MinerU Client 实施规划

> [!abstract]
> 基于 [[framework/v1-rfc]] 与 [[framework/v1-roadmap]]，并结合当前仓库已经落地的 CLI、日志与 `execution` 模块骨架，收敛 P2 的实现边界、模块划分、测试策略与分批交付顺序。目标不是直接做任务编排，而是在 orchestrator 侧先交付一个可独立测试、可缓存、可扩展的 PDF 解析客户端。

## 规划结论

- P2 仍保持独立阶段，不依赖 P3 的工件模型和 P4 的 API 服务先落地。
- 代码位置建议新增 `src/ainrf/parsing/`，与现有 `src/ainrf/execution/` 平行，避免把解析逻辑塞进 CLI 或未来 API 层。
- 对外先定义 `PaperParser` 抽象接口，再以 `MinerUClient` 作为默认实现交付，这样后续替换本地 fallback 时不需要重写上层调用点。
- 本地缓存应放入 `.ainrf/cache/mineru/`，符合仓库“运行时状态不入库”的约定，也避免污染 `docs/`、`site/` 或 `.cache/html-notes/`。
- P2 默认不新增用户级 CLI 表面。当前阶段优先保证 Python 模块契约、缓存正确性和错误分类；如果过早暴露 CLI，会增加测试面而不提升核心能力。

## 现状与约束

- 已有基础骨架：`pyproject.toml` 已声明 `httpx`、`pydantic`、`typer`、`fastapi` 等依赖；`src/ainrf/cli.py` 和 `tests/test_cli.py` 已完成 P0 级 CLI 骨架。
- 已有模块组织模式：`src/ainrf/execution/` 已采用 `models.py`、`errors.py`、`ssh.py` 的拆分方式，P2 应复用这类结构，而不是新写成单文件脚本。
- 已有测试习惯：当前测试以离线 `pytest` 单元测试为主，`tests/test_execution_ssh.py` 已证明仓库倾向通过 fake object / monkeypatch 验证外部依赖边界。
- 长期约束要求：`src/ainrf/` 与 `tests/` 中 Python 代码必须有完整类型标注，并通过 `ruff`、`pytest`、`ty check`。
- 从现有仓库证据推断，P2 不应直接写入 `PaperCard`、`EvidenceRecord` 等工件，因为这些模型尚未在代码中落地；当前阶段只需要把“解析成功/失败”收敛成稳定的解析结果契约。

## P2 范围界定

### In Scope

- `PaperParser` 抽象接口，约束“输入 PDF，输出结构化解析结果或失败结果”。
- `MinerUClient` 的提交、轮询、结果拉取三段式调用编排。
- 解析结果的数据模型，包括 Markdown、图表、元数据、原始任务标识和缓存命中信息。
- 基于 PDF 内容 SHA256 的本地缓存。
- 超时、限流、远端失败、结构不完整等错误分类。
- 基础结构校验，例如标题、摘要、正文 section 数量等最低可用条件。
- 离线测试与契约测试，不要求真实 MinerU 网络调用进入默认测试。

### Out of Scope

- `PaperCard` / `EvidenceRecord` / `StateStore` 的持久化写入。
- 将解析结果上传到容器 `papers/seed/` 或 `papers/explored/` 的集成逻辑；这一步应在 P7/P8 编排接入时对接 `SSHExecutor`。
- FastAPI 端点、SSE、webhook、任务状态查询。
- 复杂质量评分体系；P2 只做最小结构验证，不做“解析质量分数”产品化。
- 真实云端 smoke 作为默认 CI 门槛；外部 API 集成应放入手工清单或受控环境测试。

## 建议模块设计

### 目录

- `src/ainrf/parsing/__init__.py`
- `src/ainrf/parsing/models.py`
- `src/ainrf/parsing/errors.py`
- `src/ainrf/parsing/contracts.py`
- `src/ainrf/parsing/cache.py`
- `src/ainrf/parsing/mineru.py`
- `tests/test_parsing_mineru.py`
- `tests/test_parsing_cache.py`

### 核心类型

- `ParseRequest`：统一 PDF 路径输入、可选源 URL、可选论文角色等上下文。
- `ParseMetadata`：标题、作者、摘要、原始文件名、来源信息。
- `ParseFigure`：图编号、标题、资源定位信息。
- `ParseResult`：成功结果，包含 `markdown`、`metadata`、`figures`、`provider_task_id`、`cache_hit`。
- `ParseFailure`：失败结果，包含 `failure_type`、`message`、`retryable`、`provider_task_id`。
- `PaperParser`：定义 `parse_pdf(...) -> ParseResult | ParseFailure` 的统一协议。

### 配置入口

- `AINRF_MINERU_BASE_URL`
- `AINRF_MINERU_API_KEY`
- `AINRF_MINERU_TIMEOUT_SECONDS`
- `AINRF_MINERU_POLL_INTERVAL_SECONDS`
- `AINRF_MINERU_MAX_RETRIES`
- `AINRF_MINERU_CACHE_DIR`

> [!note]
> 这里沿用 P1 的环境变量约定风格，即为外部系统能力定义独立前缀，而不是把配置散落到 CLI 参数中。

## 实现顺序

### Slice 1：契约与缓存骨架

- 先落 `models.py`、`errors.py`、`contracts.py`、`cache.py`。
- 完成 SHA256 计算、缓存 key 组织、原子写入和缓存读取。
- 先写离线测试，确认重复 PDF 会命中缓存，且缓存损坏时能 fail-fast 或重建。

### Slice 2：HTTP 传输与轮询

- 用 `httpx.AsyncClient` 封装提交、查询、拉取结果。
- 把 transport 异常、HTTP 非 2xx、限流、超时统一映射到明确错误类型。
- 只在 `MinerUClient` 内部处理重试，不把重试策略泄漏到调用方。

### Slice 3：结构验证与结果归一化

- 对远端返回的 Markdown 做最低结构检查。
- 把 provider 原始响应归一化成仓库内部类型，避免上层直接依赖第三方 JSON 字段名。
- 对结构不足但仍有正文的结果，返回成功结果并附带 warning，而不是一律抛错。

### Slice 4：手工集成入口

- 增补一份 `docs/LLM-Working` 的真实 API smoke 清单，类似当前 P1 的 SSH smoke 文档。
- 在该清单中约束手工验证输入、缓存复用、坏 PDF、限流和超时观察项。
- 不在这一阶段引入正式 CLI；如确实需要手工触发，可优先通过后续临时脚本或测试夹具执行。

## 测试与验收

### 自动化测试

- `tests/test_parsing_cache.py`
  - 相同 PDF 两次解析只触发一次远端调用。
  - 缓存文件损坏时返回明确错误或自动重建，不出现静默脏读。
- `tests/test_parsing_mineru.py`
  - 提交成功并轮询完成后，返回 `ParseResult`。
  - 损坏 PDF 或 provider 明确失败时，返回 `ParseFailure`。
  - 429 / 限流场景按配置重试，超过上限后返回可识别失败。
  - Markdown 缺标题、缺摘要或 section 数不足时，触发结构验证逻辑。
  - 网络超时和不可达错误被映射成明确异常或失败对象，而不是裸 `httpx` 异常外漏。

### 阶段验收标准

- 新模块通过 `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`。
- 新模块通过 `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`。
- 新模块通过 `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`。
- 在不接入 P3/P4 的前提下，调用方已可通过一个统一入口拿到成功或失败的解析结果。
- 缓存目录、敏感配置和运行时文件均位于 `.ainrf/` 或环境变量中，不引入新的版本控制污染。

## 关键决策与理由

- 先抽象 `PaperParser` 再写 `MinerUClient`
  - roadmap 已明确本地 fallback 是潜在缓解策略；如果直接把上层绑定到 MinerU JSON 协议，后续替换成本会偏高。
- 失败结果对象化，而不是全部抛异常
  - RFC 明确“失败模式也是正式状态”。在 P3 之前先把这个原则落成 `ParseFailure`，后续接工件模型会更顺。
- 缓存放 `.ainrf/cache/mineru/`
  - 这与仓库已有 `.gitignore` 和运行态目录约定一致，也便于后续任务级状态与解析缓存放在同一根目录下管理。
- 暂不提供正式 CLI
  - 当前 CLI 仍处在骨架阶段；如果为 P2 暴露不稳定命令，会引入额外用户契约和 smoke test 负担，但对核心模块沉淀帮助有限。

## 未决问题

- MinerU Cloud API 的官方 endpoint、认证头、异步任务状态字段和结果 schema 尚未在仓库中固定记录；开始编码前需要补一份 provider 契约摘要。
- RFC 允许输入 PDF 路径或 URL，但当前仓库尚无统一下载器。P2 是否同时支持 URL，建议在拿到 API 契约后再决定是否拆成 P2a/P2b。
- 图表资源是只保留 provider 返回的引用信息，还是顺手下载到本地缓存，目前没有明确长期约束；建议 P2 先只保留元数据和远端定位。
- 结构验证阈值需要谨慎设定。过严会把可用结果误判为失败，过松则会把低质量输出带给后续流程。

## 下一步 backlog

- 补齐 MinerU provider 契约说明，确认请求/响应格式与认证方式。
- 新建 `src/ainrf/parsing/` 模块骨架与对应测试文件。
- 先实现缓存和结果模型，再接入 `httpx.AsyncClient`。
- 补一份 P2 手工 smoke 清单，作为真实 API 联调入口。

## 关联笔记

- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[framework/artifact-graph-architecture]]
- [[framework/container-workspace-protocol]]
- [[framework/v1-dual-mode-research-engine]]
- [[LLM-Working/p1-ssh-executor-smoke-checklist]]
