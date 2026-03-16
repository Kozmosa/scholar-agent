---
aliases:
  - P5 Human Gate Webhook Implementation Plan
  - P5 人工关卡与 Webhook 规划
tags:
  - ainrf
  - gates
  - webhook
  - implementation-plan
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# P5 Human Gate & Webhook 实施规划

> [!abstract]
> 基于 [[framework/v1-rfc]]、[[framework/v1-roadmap]] 与当前仓库已经落地的 `api`、`artifacts`、`state` 模块，本规划将 P5 收敛为“task-scoped Human Gate 生命周期 + signed webhook + yolo bypass + timeout reminder”。目标是在不提前实现 P6 SSE 和 P7 TaskEngine 的前提下，先把 P4 留下的审批占位路由、`HumanGate` artifact 与 `TaskRecord.gates` 串成真实可测试的控制面。

## 规划结论

- P5 以 RFC 和现有 P4 路由为准，正式审批契约继续使用 task-scoped 的 `POST /tasks/{id}/approve` 与 `POST /tasks/{id}/reject`，不新增 `/gates/*` 公开端点。
- 公开端到端只接通 `intake` gate：`POST /tasks` 创建任务后立即创建纳入关卡；`plan_approval` 的模型、审批语义和 webhook 合同在 P5 一次定型，但真实触发留给 P7 planner 接入。
- `webhook_secret` 必须从 task checkpoint 中剔除，改为进程内 runtime registry 保存；这既修复 P4 当前“整个请求体持久化”对 RFC 安全约束的偏离，也避免把 secret 落入 `.ainrf/tasks/*.json`。
- `HumanGate` artifact 升级为 gate detail 的 source of truth，`TaskRecord.gates` 只保留 append-only 摘要账本；同一任务任一时刻只允许一个 waiting gate。
- P5 完成后同步新增 `[[LLM-Working/p5-human-gate-webhook-impl]]`，记录最终接口、验证结果和 deferred 项。

## 现状与约束

- 已有 API 兼容面：P4 已把 `approve` / `reject` / `events` 路由挂到 `/tasks/{id}/*`，测试和实现都已经围绕该形状建立，P5 不应再切换到 `/gates/*`。
- 已有状态基础：P3 已经具备 `HumanGate` artifact、`TaskRecord.gates` 和 `TaskStage.GATE_WAITING`，因此 P5 的核心工作是把这些离散状态接成生命周期，而不是重做持久化层。
- 现有安全缺口：`POST /tasks` 当前直接把 `TaskCreateRequest` 整体持久化进 `TaskRecord.config`，会把 `webhook_secret` 写入 checkpoint；P5 必须顺手修正。
- 当前还没有 TaskEngine / planner，所以不能伪造真实 `plan_approval` payload；P5 只交付该 gate 的领域模型与审批语义，不强行制造假计划。
- 长期约束仍要求新增 Python 代码具备严格类型标注，并通过 `pytest`、`ruff check`、`ty check`；同时要向 `docs/LLM-Working/worklog/2026-03-16.md` 追加完成批次记录。

## 范围界定

### In Scope

- `src/ainrf/gates/`：gate manager、payload schema、runtime secret registry、webhook dispatcher
- `HumanGate` / `GateRecord` / `TaskRecord.config` 的 P5 所需扩展
- `POST /tasks` 的 intake gate 创建、yolo auto-approve 和 waiting webhook
- `POST /tasks/{id}/approve` / `reject` 的真实 gate resolution
- Gate timeout reminder sweep 和 `gate.reminder` webhook
- `GET /tasks/{id}` 的 `active_gate` 详情
- 对应的单元测试、API 测试与 `Impl` 文档

### Out of Scope

- P6 SSE 事件流和 `/tasks/{id}/events` 真逻辑
- P7 planner / TaskEngine 产生的真实 `plan_approval` payload
- `/gates/*` 列表或审批路由
- gate 之外的任务调度、自动恢复执行和队列语义

## 建议模块设计

### 目录

- `src/ainrf/gates/__init__.py`
- `src/ainrf/gates/errors.py`
- `src/ainrf/gates/models.py`
- `src/ainrf/gates/manager.py`
- `src/ainrf/api/routes/tasks.py`
- `tests/test_api_tasks.py`
- `tests/test_artifacts_models.py`
- `tests/test_state_store.py`

### 核心接口

- `HumanGateManager.trigger_gate(...)`
- `HumanGateManager.resolve_current_gate(...)`
- `HumanGateManager.get_active_gate(task_id)`
- `HumanGateManager.sweep_overdue_gates()`
- `WebhookSecretRegistry.set/get/drop(...)`
- `WebhookDispatcher.send(url, secret, payload)`

## 实现顺序

### Slice 1：文档与领域模型

- 新增 P5 规划笔记并在 roadmap 的 P5 段落补实现入口。
- 扩展 `HumanGate` 与 `GateRecord`，补 payload、deadline、resolved_at、reminder_sent_at 等字段。
- 在 `save_task()` 路径收敛 config sanitize，先堵住 `webhook_secret` 落盘问题。

### Slice 2：Gate 服务层

- 新增 `ainrf.gates` 包，落地 manager、payload schema、secret registry 与 webhook dispatcher。
- 把“单 waiting gate 约束”“按 gate type 的状态迁移”“plan reject 连续三次 fail-fast”都集中在 manager，而不是散落在路由里。

### Slice 3：API 接线

- 改造 `POST /tasks`，创建 intake gate，并根据 `yolo` 决定进入 `gate_waiting` 还是直接转入 `planning`。
- 把 `approve` / `reject` 从 `501` 升级为真实 resolution 路由。
- 在 `GET /tasks/{id}` 暴露 `active_gate` 详情，方便轮询端发现待审批上下文。

### Slice 4：提醒与文档收口

- 在 app lifespan 中挂 gate reminder sweep，超时 gate 只提醒一次。
- 新增 `Impl` 笔记和当日 worklog 记录。

## 验收与验证

- `POST /tasks` 非 yolo 时创建 waiting `intake` gate，并发送 signed webhook
- `POST /tasks` 持久化的 task JSON 中不包含 `webhook_secret`
- `POST /tasks` yolo 时自动批准 intake gate，不发送 webhook，任务进入 `planning`
- `POST /tasks/{id}/approve` 能推进 intake gate 到 `planning`、推进 plan gate 到 `executing`
- `POST /tasks/{id}/reject` 能让 intake gate 终止任务，并让 plan gate 回到 `planning`；连续 3 次 plan reject 后任务进入 `failed`
- `sweep_overdue_gates()` 对超时 waiting gate 只发送一次 reminder
- 最终执行：
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`

## 建议原子提交

- `docs: plan p5 human gate webhook implementation`
- `feat: add gate models and state sanitization`
- `feat: add intake gate workflow and signed webhooks`
- `feat: add gate approval and timeout reminders`
- `docs: add p5 human gate webhook impl note`

## 关联笔记

- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[framework/ai-native-research-framework]]
- [[framework/v1-dual-mode-research-engine]]
- [[LLM-Working/p4-fastapi-service-auth-implementation-plan]]
- [[LLM-Working/p5-human-gate-webhook-impl]]
