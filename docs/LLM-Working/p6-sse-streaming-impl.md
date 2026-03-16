---
aliases:
  - P6 SSE Streaming Impl
  - P6 SSE 流式事件实现记录
tags:
  - ainrf
  - events
  - sse
  - impl
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# P6 SSE Streaming 实现记录

> [!abstract]
> 本笔记记录 P6 在当前仓库中的最终落地结果：新增 `ainrf.events`，把 P4/P5 已经存在的 task/gate/artifact 状态变化持久化为 task-scoped JSONL 事件，并把 `/tasks/{id}/events` 从占位路由升级为可回放、可过滤、可断点恢复的 SSE 端点。实现仍保持在控制面和本地 state 层，不提前实现 P7 TaskEngine 或实验流。

## 实现结论

- 新增 `src/ainrf/events/`：承载 `TaskEvent` 模型、事件类别枚举、JSONL 存储和事件服务。
- `GET /tasks/{id}/events` 现在返回真实 `text/event-stream`：
  - 支持历史回放
  - 支持 `Last-Event-ID`
  - 支持 `?types=` 分类过滤
  - 非终态任务支持轮询跟随和 keepalive
  - 终态任务在历史回放后自动关闭连接
- `HumanGateManager` 现在会发射：
  - `artifact.created` / `artifact.updated`
  - `gate.waiting` / `gate.resolved` / `gate.reminder`
  - `task.stage_changed`
  - 进入终态时补发 `task.failed` / `task.cancelled`
- `POST /tasks/{id}/cancel` 现在会补发被取消 gate 的 `artifact.updated`、`gate.resolved`，以及 `task.stage_changed` 和 `task.cancelled`

## 代码结构

### `ainrf.events`

- `models.py`
  - `TaskEventCategory`
  - `TaskEvent`
- `store.py`
  - `JsonlTaskEventStore`
- `service.py`
  - `TaskEventService`

### `ainrf.api`

- `app.py`
  - 注册事件存储与事件服务
- `dependencies.py`
  - 新增 `get_event_service`
- `routes/tasks.py`
  - 实现 `/tasks/{id}/events`
  - 在 `cancel` 路由发射 task/gate 取消相关事件

### `ainrf.gates`

- `manager.py`
  - 在 gate trigger / resolve / reminder 路径统一发射事件

## 关键实现决策

- 事件存储采用 task-scoped JSONL
  - 路径固定为 `.ainrf/events/{task_id}.jsonl`，与 RFC 的本地 append-only 事件日志设计一致，也避免为 P6 引入额外数据库或 broker。
- SSE 跟随采用“轮询文件”而不是内存 fan-out
  - 这与 roadmap 中“事件持久化到文件而非内存队列”的风险缓解一致，也更符合当前仓库“优先简单实现”的约束。
- 事件命名对齐当前仓库语义
  - gate 事件统一使用 `gate.waiting` / `gate.resolved` / `gate.reminder`，保持与 P5 的 webhook 事件和 `HumanGateStatus.WAITING` 一致。
- 旧任务不做历史补写
  - P6 只保证本阶段之后发生的状态变化会进入事件日志；已经存在但没有 `.jsonl` 的旧任务可以被订阅，但不会得到伪造历史。
- `Last-Event-ID` 非法值快速失败
  - 直接返回 `400`，避免把错误 header 静默降级成全量回放。

## 自动化验证

- 定向验证
  - `.venv/bin/python -m pytest tests/test_api_tasks.py tests/test_api_events.py tests/test_events_store.py -q`
- 全量验证
  - `.venv/bin/python -m pytest tests -q`
  - `.venv/bin/python -m ruff check src tests`
  - `.venv/bin/python -m ty check`
- 当前结果
  - `pytest tests`：passed
  - `ruff check src tests`：passed
  - `ty check`：passed

## Deferred 项

- `task.started`、`task.completed` 的真实运行期发射，留给 P7 TaskEngine 接入。
- `experiment.*` 和 `log.*` 的真实事件源，留给 P7/P8。
- 对历史 task 的事件补写与迁移，目前不做。
- 如果未来任务并发和 SSE 连接数显著增加，再评估是否把“文件轮询”升级为 broker 或内存 fan-out。

## 关联笔记

- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[LLM-Working/p6-sse-streaming-implementation-plan]]
- [[LLM-Working/p5-human-gate-webhook-impl]]
