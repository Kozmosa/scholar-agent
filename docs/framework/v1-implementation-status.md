---
aliases:
  - AINRF V1 实现概要
  - V1 Implementation Status
tags:
  - research-agent
  - framework-design
  - v1-spec
  - implementation-status
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# AINRF V1 实现概要

> [!abstract]
> 对齐 [[framework/v1-roadmap]] 与 [[framework/v1-rfc]] 的阶段定义，逐阶段（P0-P9 + WebUI W0-W5）标注已实现 / 未实现状态，并列出与设计文档的差异。

## 总览

| 阶段 | 名称 | 状态 | 实现提交 | 测试数 | 关键差异 |
|------|------|------|----------|--------|----------|
| P0 | Project Scaffold | **已完成** | `98118f0` | 11 | 无重大差异 |
| P1 | SSH Executor | **已完成** | `ab728fc` | 11 | 无重大差异 |
| P2 | MinerU Client | **已完成** | `1a109b6` `d9ea76f` | 13 | API 对接了 batch v4 接口，与 roadmap 预期一致 |
| P3 | Artifact Model & State | **已完成** | `7975cfa` | 18 | 缺少 `AgentAdapter` 工件类型 |
| P4 | FastAPI Service & Auth | **已完成** | `f319d2f` | 22 | API 路径未加 `/v1/` 前缀 |
| P5 | Human Gate & Webhook | **已完成** | `4842652` | ~30 | 无重大差异 |
| P6 | SSE Streaming | **已完成** | `bce40d2` | 5 | 无重大差异 |
| P7 | Agent Adapter & Engine | **部分完成** | `31c1df1` | 8 | 仅 fallback 模式，未真实调用 CC SDK |
| P8 | Mode 2 Deep Repro | **未实现** | — | 0 | 完全未实现 |
| P9 | Mode 1 Research Discovery | **未实现** | — | 0 | 完全未实现 |
| WebUI W0-W3 | 工作台前端 | **W0-W3 已完成** | `31c1df1` `7bb33b2` `08c5bfb` | 23 | W4/W5 未实现 |

**代码统计：** `src/ainrf/` 包含 54 个 Python 文件；测试 111 个用例（17 个测试文件）。

---

## P0: Project Scaffold — 已完成

**roadmap 要求：**
- `src/ainrf/` 包结构、`__init__.py`、`__main__.py`、`cli.py` ✅
- `pyproject.toml` 更新：ainrf 入口点、基础依赖 ✅
- CLI 入口：typer，支持 `--help`、`--version`、`serve`、`run` ✅
- structlog + JSON 日志 ✅
- pre-commit hooks（ruff lint + format）✅
- 基础 pytest 配置 ✅

**差异：** 无重大差异。CLI 框架选择了 typer（roadmap 建议）。后续阶段新增了 `webui` 子命令（超出 P0 scope 但合理）。

**关键文件：**
- `src/ainrf/cli.py` — CLI 入口，含 `serve`、`run`、`webui` 三个子命令
- `src/ainrf/__init__.py` — 版本号
- `src/ainrf/logging.py` — structlog 配置

---

## P1: SSH Executor & Container Bootstrap — 已完成

**roadmap 要求 vs 实现：**

| 交付物 | 状态 | 说明 |
|--------|------|------|
| `SSHExecutor` 类（连接池、复用、自动重连）| ✅ | 基于 asyncssh，指数退避重连 |
| `run_command(cmd, timeout, cwd)` → `CommandResult` | ✅ | 含 env 参数扩展 |
| `upload(local, remote)` / `download(remote, local)` | ✅ | SFTP + rsync fallback（>100MB） |
| Claude Code 自动检测与安装 | ✅ | `ensure_claude_code()` |
| `~/.ssh/config` 和 `AINRF_CONTAINER_*` 环境变量 | ✅ | `ContainerConfig.from_env()` |
| 健康检查 `ping()` | ✅ | GPU、CUDA、磁盘、CC 版本 |
| 仅 Ubuntu/Debian + bash | ✅ | `_ensure_supported_container()` |

**差异：** 无重大差异。实现完整覆盖了 roadmap 要求。

**关键文件：**
- `src/ainrf/execution/ssh.py` — SSHExecutor (514 行)
- `src/ainrf/execution/models.py` — ContainerConfig, CommandResult, ContainerHealth
- `src/ainrf/execution/errors.py` — 错误类型层次

---

## P2: MinerU Client — 已完成

**roadmap 要求 vs 实现：**

| 交付物 | 状态 | 说明 |
|--------|------|------|
| `MinerUClient` 类 | ✅ | 实现 `PaperParser` Protocol |
| PDF 提交 → task_id | ✅ | 支持本地上传和远程 URL 两条路径 |
| 轮询与结果获取 → `ParseResult` | ✅ | 轮询 batch v4 接口，解析 zip 归档 |
| 结构验证（标题/摘要/section） | ✅ | `_validate_markdown()` |
| 错误处理（限流/损坏/超时）| ✅ | 完整 `ParseFailureType` 枚举 |
| 本地缓存（SHA256） | ✅ | `ParseCache` 独立模块 |
| `PaperParser` 抽象接口 | ✅ | Protocol 定义 |

**差异：**
- roadmap 写的是 `submit_pdf(pdf_path) → task_id`，实际实现为 `parse_pdf(request) → ParseResult | ParseFailure`，API 更高层——一次调用完成提交+轮询+解析。符合设计意图但接口粒度不同。
- 对接了 MinerU batch v4 API（而非简单的单文件 API），实现更完整。

**关键文件：**
- `src/ainrf/parsing/mineru.py` — MinerUClient (725 行)
- `src/ainrf/parsing/cache.py` — ParseCache
- `src/ainrf/parsing/contracts.py` — PaperParser Protocol
- `src/ainrf/parsing/models.py` — ParseRequest/ParseResult/ParseFailure

---

## P3: Artifact Model & State Store — 已完成

**roadmap 要求 vs 实现：**

| 交付物 | 状态 | 说明 |
|--------|------|------|
| 全部一等工件 Pydantic v2 models | ⚠️ 部分 | 缺少 `AgentAdapter` 工件类型 |
| 状态机（合法转换表） | ✅ | `transitions.py` 声明式转换表 |
| `StateStore` 接口 + JSON 实现 | ✅ | Protocol + `JsonStateStore` |
| Checkpoint/Resume | ✅ | `checkpoint_task()` / `resume_task()` |
| 工件关系索引 | ✅ | `artifact-links.json` 索引文件 |
| atomic write + 文件锁 | ✅ | `fcntl.flock` + 临时文件 rename |
| `schema_version` 字段 | ✅ | 每个 `ArtifactModel` 有 `schema_version=1` |

**差异：**
- **缺少 `AgentAdapter` 工件类型**：roadmap P3 列出的一等工件包含 `AgentAdapter`，但 `ArtifactType` 枚举中没有。这是因为 `AgentAdapter` 在实际实现中作为代码抽象（ABC）而非持久化工件存在——设计合理，但与 roadmap 文字有出入。
- 已实现 9 个工件类型：PaperCard, ReproductionTask, ExperimentRun, EvidenceRecord, Claim, ExplorationGraph, QualityAssessment, WorkspaceManifest, HumanGate。

**关键文件：**
- `src/ainrf/artifacts/models.py` — 全部工件 Pydantic models (246 行)
- `src/ainrf/artifacts/transitions.py` — 状态转换表
- `src/ainrf/state/store.py` — JsonStateStore (330 行)
- `src/ainrf/state/models.py` — TaskRecord, TaskCheckpoint, ArtifactQuery

---

## P4: FastAPI Service & Auth — 已完成

**roadmap 要求 vs 实现：**

| 交付物 | 状态 | 说明 |
|--------|------|------|
| FastAPI 应用骨架 `ainrf.api` | ✅ | `app.py`, `routes/`, `middleware/`, `schemas/` |
| API Key 认证中间件 | ✅ | SHA-256 哈希存储，`X-API-Key` header |
| `POST /tasks` | ✅ | 含 intake gate 自动触发 |
| `GET /tasks/{id}` | ✅ | 含工件摘要、活跃 gate 信息 |
| `POST /tasks/{id}/cancel` | ✅ | 优雅取消 + gate 取消 |
| `GET /tasks/{id}/artifacts` | ✅ | 全类型工件查询 |
| `GET /health` | ✅ | 含容器连通性信息 |
| Daemon 模式 `--daemon` | ✅ | `run_server_daemon()` |
| OpenAPI schema 自动生成 | ✅ | FastAPI 内置 |
| `GET /tasks` 列表（含过滤） | ✅ | `?status=` 参数过滤 |

**差异：**
- ⚠️ **API 路径未加 `/v1/` 版本前缀**：[[framework/v1-rfc]] 建议"版本化 API（`/v1/`）"，但实际端点直接挂在根路径（如 `/tasks` 而非 `/v1/tasks`）。
- ⚠️ **`TaskMode` 枚举命名差异**：RFC 定义为 `research_discovery | deep_reproduction`，实现为 `literature_exploration | deep_reproduction`。RFC 中有备注"代码实现需后续补迁移"。
- 多 key 管理：✅ 支持（逗号分隔的 hash 列表）。

**关键文件：**
- `src/ainrf/api/app.py` — create_app() + lifespan
- `src/ainrf/api/routes/tasks.py` — 全部任务端点 (467 行)
- `src/ainrf/api/schemas.py` — request/response models (233 行)
- `src/ainrf/api/middleware.py` — API Key 中间件
- `src/ainrf/api/config.py` — ApiConfig + 环境变量
- `src/ainrf/server.py` — daemon 启动逻辑

---

## P5: Human Gate & Webhook — 已完成

**roadmap 要求 vs 实现：**

| 交付物 | 状态 | 说明 |
|--------|------|------|
| `HumanGateManager` 类 | ✅ | 450 行完整实现 |
| intake + plan_approval 两种关卡 | ✅ | `GateType` 枚举，另有 `runtime_review` 预留 |
| Webhook POST（HMAC-SHA256 签名） | ✅ | `WebhookDispatcher` + 重试 |
| `POST /tasks/{id}/approve` | ✅ | |
| `POST /tasks/{id}/reject` | ✅ | 含 feedback |
| `GET /tasks?status=gate_waiting` | ✅ | 列表过滤 |
| Yolo 模式旁路 | ✅ | 自动批准 + 跳过 webhook |
| 超时处理（提醒 webhook） | ✅ | `sweep_overdue_gates()` 后台任务 |
| 连续 reject 3 次自动 failed | ✅ | `_consecutive_plan_rejections()` |
| Webhook secret 不写入 checkpoint | ✅ | `WebhookSecretStore` 独立存储 |

**差异：** 无重大差异。实现完整度高。

**关键文件：**
- `src/ainrf/gates/manager.py` — HumanGateManager + WebhookDispatcher
- `src/ainrf/gates/models.py` — GateWebhookPayload, IntakeGatePayload, PlanApprovalGatePayload
- `src/ainrf/runtime/secrets.py` — WebhookSecretStore

---

## P6: SSE Streaming — 已完成

**roadmap 要求 vs 实现：**

| 交付物 | 状态 | 说明 |
|--------|------|------|
| `GET /tasks/{id}/events` SSE 端点 | ✅ | `text/event-stream` |
| 事件类型 (task.*, artifact.*, gate.*, log.*) | ⚠️ 部分 | `log.*` 事件尚未在代码中被发射 |
| JSONL 持久化 | ✅ | `JsonlTaskEventStore` |
| 断线重连 `Last-Event-ID` | ✅ | `after_id` 参数 |
| 事件过滤 `?types=` | ✅ | `TaskEventCategory` 过滤 |
| Keepalive 心跳 | ✅ | 可配置间隔 |
| 终态后关闭连接 | ✅ | 检测 terminal stages |

**差异：**
- ⚠️ **`log.*` 事件未发射**：定义了 `TaskEventCategory.LOG`，但 TaskEngine 和 GateManager 中没有代码发射 `log.info` / `log.warning` / `log.error` 事件。这是一个功能缺口——日志事件只在 RFC 中描述但未实现。
- ⚠️ **`experiment.*` 事件未发射**：roadmap 提到 `experiment.started` / `experiment.completed`，这些属于 P8 集成范畴，P6 本身不需要实现。

**关键文件：**
- `src/ainrf/events/store.py` — JsonlTaskEventStore（append-only JSONL）
- `src/ainrf/events/service.py` — TaskEventService
- `src/ainrf/events/models.py` — TaskEvent, TaskEventCategory
- `src/ainrf/api/routes/tasks.py:416-466` — SSE streaming 端点

---

## P7: Agent Adapter & Task Engine — 部分完成

**roadmap 要求 vs 实现：**

| 交付物 | 状态 | 说明 |
|--------|------|------|
| `AgentAdapter` 抽象基类 | ✅ | `bootstrap()`, `health_check()`, `plan_reproduction()`, `execute_step()` |
| `ClaudeCodeAdapter` 实现 | ⚠️ **Fallback 模式** | **未真实调用 `claude_code_sdk`**，使用远程 Python 脚本返回硬编码 fallback 响应 |
| `TaskEngine` 编排器 | ⚠️ **部分** | 仅实现 `deep_reproduction` 模式的 planning + executing 流程 |
| 原子任务粒度执行 | ✅ | `AtomicTaskSpec` → `TaskExecutionResult` |
| Checkpoint/Resume | ✅ | 每步持久化 + `run_once()` 从 pending_queue 恢复 |
| Budget 监控 | ✅ | `_budget_exhausted()` 三维度检查 |
| SSE 事件发射 | ✅ | task.started/progress/completed/failed |
| PDF 下载与 MinerU 解析 | ✅ | `_ingest_task()` 中实现 |

**关键差异：**

1. **ClaudeCodeAdapter 为 fallback 模式**：这是最大的差异。`claude_code.py:14-67` 定义了一个 `_REMOTE_RUNNER_SOURCE` Python 脚本，上传到容器后执行。该脚本的 `_fallback_response()` 返回硬编码响应——无论有没有 `claude_code_sdk`，都走 fallback 路径（`claude_code.py:59`: `result = _fallback_response(request)`）。这意味着当前 P7 **不能真正执行研究任务**。
2. **AgentAdapter 接口与 RFC 不一致**：
   - RFC 定义：`execute_task(task_spec, container, context) → TaskResult`
   - 实际实现：`plan_reproduction(container, prompt, context) → TaskPlanResult` + `execute_step(container, step, context) → TaskExecutionResult`
   - 实现拆分为两个方法（plan + execute），比 RFC 更细粒度，但接口签名不同。
   - RFC 定义的 `ingest_paper()`, `plan_reproduction()`, `implement_from_paper()`, `run_experiment()`, `analyze_deviation()` 五个方法未实现为独立接口。
3. **仅支持 Mode 2**：`engine.py:56-57` 明确写了 `mode_not_implemented` 对 Mode 1 直接 fail。
4. **`run` 子命令可用但无真实效果**：`ainrf run --once` 可以拉取 task 并执行 planning→executing 流程，但因 Adapter 为 fallback，产出均为占位数据。

**关键文件：**
- `src/ainrf/agents/base.py` — AgentAdapter ABC
- `src/ainrf/agents/claude_code.py` — ClaudeCodeAdapter + fallback runner (231 行)
- `src/ainrf/engine/engine.py` — TaskEngine (490 行)
- `src/ainrf/engine/models.py` — AtomicTaskSpec, TaskPlanResult, TaskExecutionResult

---

## P8: Mode 2 Deep Reproduction Pipeline — 未实现

**roadmap 要求：** 端到端深度复现——论文解析 → PaperCard → 复现计划 → 从零实现 → 实验执行 → 偏差分析 → QualityAssessment。

**当前状态：** 完全未实现。P7 的 TaskEngine 有 `_advance_planning_task()` 和 `_advance_executing_task()` 骨架，但 ClaudeCodeAdapter 为 fallback 模式，无法执行真实研究动作。

**缺口清单：**
- [ ] ClaudeCodeAdapter 需要真实调用 claude_code_sdk
- [ ] 每个原子任务（analyze_method, plan_implementation, implement_module, run_baseline, diagnose_deviation, run_full_experiment, compare_tables, generate_quality_assessment）需要对应的 system prompt 和结果解析
- [ ] 容器上的 per-project 工作区初始化（遵循 [[framework/container-workspace-protocol]]）
- [ ] 实验结果与论文值的定量对比逻辑
- [ ] QualityAssessment 生成逻辑
- [ ] 实际的集成测试（需要真实容器 + API key）

---

## P9: Mode 1 Research Discovery Pipeline — 未实现

**roadmap 要求：** 从种子材料出发的递归调研发现——需求澄清 → 文献扩展 → 图谱更新 → idea 发现 → 终止控制 → 调研报告。

**当前状态：** 完全未实现。TaskEngine 对 Mode 1 直接返回 `mode_not_implemented` 错误。

**缺口清单：**
- [ ] ExplorationGraph 管理逻辑
- [ ] 需求澄清与问题画像的原子任务
- [ ] 参考文献提取与排序
- [ ] 方法脉络与知识图更新
- [ ] idea 发现与评估
- [ ] 三重终止控制器（深度/预算/递减收益）
- [ ] 调研发现报告生成
- [ ] Mode 1 专属 gate payload 和 webhook 内容

---

## WebUI 独立轨道

| 阶段 | 名称 | 状态 | 提交 |
|------|------|------|------|
| W0 | WebUI RFC & IA | ✅ | `31c1df1` |
| W1 | App Shell & API Client | ✅ | `31c1df1` |
| W2 | Project & Run Forms | ✅ | `7bb33b2` |
| W3 | Run Detail, Gates & Events | ✅ | `08c5bfb` |
| W4 | Mode Mock Panels | **未实现** | — |
| W5 | Validation & Docs | **未实现** | — |

**已实现能力：**
- Gradio App Shell + `ainrf webui` 启动入口
- API 连通性检测 + 健康状态展示
- AinrfApiClient typed 封装（create_task, get_task, list_tasks, approve, reject, cancel, list_events, health）
- Project List / Detail 两级视图
- Project 默认配置持久化（JsonProjectStore）
- Run 创建表单（Mode 1/Mode 2 切换，覆盖 container/budget 配置）
- Run Detail 页面（gate 状态、approve/reject 操作、artifact 摘要、事件时间线）
- SSE 优先 + 轮询降级的事件观察

**W4/W5 缺口：**
- [ ] Mode 1 / Mode 2 interactive mock 面板
- [ ] mock data adapter
- [ ] smoke test coverage
- [ ] 演示路径文档

---

## 跨阶段差异汇总

| 差异项 | 涉及阶段 | 详情 | 严重程度 |
|--------|----------|------|----------|
| Mode 1 枚举命名 | P4, RFC | RFC: `research_discovery`；代码: `literature_exploration` | 中 — 需要迁移 |
| API 路径无版本前缀 | P4 | RFC 建议 `/v1/`，实际为 `/tasks` | 低 — 可后续添加 |
| AgentAdapter 工件类型缺失 | P3 | roadmap 列出但未实现为持久化工件 | 低 — 设计合理 |
| CC SDK 未真实集成 | P7 | 仅 fallback 模式 | **高** — P8/P9 的前置 |
| AgentAdapter 接口签名 | P7, RFC | RFC 单方法 `execute_task()`；实现为 `plan_reproduction()` + `execute_step()` | 中 — 接口更细但不同 |
| log.* 事件未发射 | P6 | 定义了 category 但无代码发射 | 低 — 可后续补充 |
| prompt 字段缺失 | P4 | RFC task schema 有 `prompt` 对象；API schema 未包含 | 中 — Mode 1 依赖 |

---

## 验证方式

```bash
# 运行全部 111 个测试
uv run pytest

# 检查 CLI 入口
uv run ainrf --version
uv run ainrf --help

# 检查 lint
uv run ruff check src/ainrf/
uv run ruff format --check src/ainrf/
```
