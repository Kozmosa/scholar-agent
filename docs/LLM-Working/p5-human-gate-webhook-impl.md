---
aliases:
  - P5 Human Gate Webhook Impl
  - P5 人工关卡与 Webhook 实现记录
tags:
  - ainrf
  - gates
  - webhook
  - impl
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# P5 Human Gate & Webhook 实现记录

> [!abstract]
> 本笔记记录 P5 在当前仓库中的最终落地结果：新增 `ainrf.gates` 领域服务，把 P4 的 task-scoped 审批占位接口升级为真实 gate lifecycle，并补齐 signed webhook、yolo bypass、timeout reminder 与 `active_gate` 详情输出。实现仍保持在控制面与本地 state 层，不提前实现 P6 SSE 或 P7 planner。

## 实现结论

- 新增 `src/ainrf/gates/`：承载 gate manager、payload schema、runtime secret registry 与 webhook dispatcher。
- `POST /tasks` 现在会立即创建 `intake` gate：
  - 默认进入 `gate_waiting`
  - `yolo=true` 时自动批准 gate，并把任务推进到 `planning`
- `POST /tasks/{id}/approve` / `reject` 不再返回 `501`，而是解析当前 waiting gate 并执行真实状态迁移。
- `GET /tasks/{id}` 新增 `active_gate`，返回当前 waiting gate 的摘要、payload 和 deadline。
- `webhook_secret` 不再写入 `.ainrf/tasks/*.json`；P5 通过进程内 registry 保留 runtime secret，只用来签署 webhook。
- app lifespan 会周期性扫描超时 gate，并对逾期 gate 发送一次 `gate.reminder` webhook。

## 代码结构

### `ainrf.gates`

- `models.py`
  - `IntakeGatePayload`
  - `PlanApprovalGatePayload`
  - `GateWebhookEvent`
  - `GateWebhookPayload`
- `manager.py`
  - `HumanGateManager`
  - `WebhookSecretRegistry`
  - `WebhookDispatcher`
- `errors.py`
  - `GateConflictError`
  - `GateNotFoundError`
  - `GateResolutionError`

### `ainrf.api`

- `app.py`
  - 注册 `gate_manager`
  - 在 lifespan 中启动 gate reminder sweep
- `routes/tasks.py`
  - `POST /tasks`
  - `POST /tasks/{id}/approve`
  - `POST /tasks/{id}/reject`
  - `GET /tasks/{id}` 的 `active_gate`
- `schemas.py`
  - `ActiveGateResponse`
  - 扩展 `GateRecordResponse` / `TaskDetailResponse`

### `ainrf.artifacts` / `ainrf.state`

- `HumanGate`
  - 增加 `payload`、`deadline_at`、`resolved_at`、`reminder_sent_at`
- `GateRecord`
  - 增加 `resolved_at`
- `JsonStateStore.save_task()`
  - 在持久化前移除 `config.webhook_secret`

## 关键实现决策

- 审批接口保持 task-scoped
  - P4 和 RFC 都已经围绕 `/tasks/{id}/approve|reject` 落地，P5 没有再引入 `/gates/*`，避免破坏现有兼容面。
- 只把 `intake` gate 接成公开端到端流程
  - 这是当前仓库在没有 planner / TaskEngine 的前提下能真实驱动的最小闭环；`plan_approval` 的状态机和审批语义已经实现，但真实触发留给 P7。
- `webhook_secret` 只保留在 runtime 内存
  - 这修复了 P4 当前“整个请求体落盘”的安全偏差，也保持实现简单；进程重启后无法继续为旧任务发送签名 webhook，是当前阶段接受的 tradeoff。
- 提醒 webhook 只发送一次
  - `reminder_sent_at` 作为 gate artifact 字段写回，既避免重复提醒，也让 reminder 状态可审计。
- 缺失 runtime secret 时 reminder 只记 warning，不阻塞任务状态
  - 这样重启后的历史 waiting task 仍可被轮询和审批，不会因为 webhook secret 丢失而让状态机失效。

## 自动化验证

- 定向验证
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_tasks.py tests/test_state_store.py tests/test_artifacts_models.py`
- 全量验证
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`
- 当前结果
  - `pytest tests/`：71 passed
  - `ruff check src tests`：passed
  - `ty check`：passed

## Deferred 项

- `plan_approval` 的真实计划 payload 生成与触发，保留到 P7 planner / TaskEngine。
- `GET /tasks/{id}/events` 的 gate SSE 事件流，保留到 P6。
- webhook secret 的跨进程持久化与恢复，目前不做；P5 只保证当前进程生命周期内的 signed webhook。
- `/gates/*` 资源视图与待审批专用列表，不在当前阶段引入，继续使用 `GET /tasks?status=gate_waiting`。

## 建议原子提交切片

- `docs: plan p5 human gate webhook implementation`
- `feat: add gate models and state sanitization`
- `feat: add intake gate workflow and signed webhooks`
- `feat: add gate approval and timeout reminders`
- `docs: add p5 human gate webhook impl note`

## 关联笔记

- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[LLM-Working/p5-human-gate-webhook-implementation-plan]]
- [[LLM-Working/p4-fastapi-service-auth-impl]]
