---
aliases:
  - P6 SSE Streaming Implementation Plan
  - P6 SSE 流式事件规划
tags:
  - ainrf
  - events
  - sse
  - implementation-plan
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# P6 SSE Streaming 实施规划

> [!abstract]
> 基于 [[framework/v1-rfc]]、[[framework/v1-roadmap]] 与当前仓库已经落地的 `api`、`gates`、`state` 模块，本规划将 P6 收敛为“task-scoped 事件持久化 + SSE 历史回放/跟随 + 现有控制面状态变化接线”。目标是在不提前实现 P7 TaskEngine、实验流和 agent 日志流的前提下，先把 P4/P5 已经存在的任务、关卡和 artifact 变化转换成可回放、可过滤、可断点恢复的事件流。

## 规划结论

- P6 新增独立的 `ainrf.events` 运行时模块，承载事件模型、JSONL 持久化和查询逻辑，而不是把事件文件读写直接塞进 FastAPI 路由。
- SSE 继续沿用 P4 留下的 task-scoped 形状：`GET /tasks/{id}/events`，不引入 `/events/*` 或 WebSocket 新接口。
- 事件命名采用“RFC 的 task 阶段语义 + 当前仓库 gate 命名习惯”的折中方案：保留 `task.stage_changed`，并将 roadmap 中的 `gate.pending` 收敛为现有代码已经使用的 `gate.waiting`。
- 为遵守“避免过早抽象”的仓库约束，P6 默认采用“append-only JSONL + SSE 轮询跟随”的简单实现，不引入 broker、内存 fan-out 或额外第三方 SSE 依赖。
- P6 完成后同步新增 `[[LLM-Working/p6-sse-streaming-impl]]`，记录最终接口、验证结果、deferred 项与文档回链。

## 现状与约束

- 当前 API 兼容面已经固定：`/tasks/{id}/events` 在 P4 挂载、P5 保持占位，因此 P6 只需要接管现有路由，不应改动 URL 形状。
- 当前仓库已真实发生的状态变化集中在 `POST /tasks`、`approve/reject`、`cancel` 和 gate reminder sweep；不存在 TaskEngine、experiment lifecycle 或 agent log stream，因此这些事件不能靠伪造补齐。
- `HumanGateManager` 已经集中管理 gate 生命周期，适合作为 gate-related 事件的统一发射点；取消任务仍由 tasks 路由本地处理，因此 task cancel 事件在路由中发射。
- 长期约束要求新增 Python 代码具备严格类型标注，并通过 `pytest`、`ruff check`、`ty check`；同时执行实际修改时要同步追加 `docs/LLM-Working/worklog/2026-03-16.md`。

## 范围界定

### In Scope

- `ainrf.events` 包：事件模型、JSONL 事件存储、事件服务
- `GET /tasks/{id}/events` 的真实 SSE 回放/跟随实现
- `Last-Event-ID` 断点恢复、`?types=` 过滤、keepalive 保活
- 对现有 task/gate/artifact 状态变化的事件发射接线
- 覆盖事件存储、SSE 回放、过滤、断点恢复与 live follow 的测试
- `Impl` 笔记、roadmap 回链和当日 worklog

### Out of Scope

- P7 TaskEngine 的进度事件、执行日志和真正的 `task.started`
- P8/P9 的 `experiment.*` 事件实际发射
- WebSocket、外部消息队列或内存 pub/sub fan-out
- 对 P6 之前旧任务反推补写历史事件

## 建议模块设计

### 目录

- `src/ainrf/events/__init__.py`
- `src/ainrf/events/models.py`
- `src/ainrf/events/store.py`
- `src/ainrf/events/service.py`
- `src/ainrf/api/routes/tasks.py`
- `src/ainrf/gates/manager.py`
- `tests/test_events_store.py`
- `tests/test_api_events.py`

### 核心接口

- `TaskEvent`
- `TaskEventCategory`
- `JsonlTaskEventStore.append_event(...)`
- `JsonlTaskEventStore.list_events(...)`
- `TaskEventService.publish(...)`
- `GET /tasks/{id}/events?types=task,gate`

## 实现顺序

### Slice 1：事件层

- 新增事件模型与 `.ainrf/events/{task_id}.jsonl` 持久化。
- 把事件服务注入 FastAPI app state，供路由和 gate manager 共享。

### Slice 2：控制面事件发射

- 在 `HumanGateManager` 接入 trigger/resolve/reminder 事件。
- 在 `POST /tasks/{id}/cancel` 接入 gate cancel 与 task cancel 事件。

### Slice 3：SSE 路由

- 把 `/tasks/{id}/events` 从 `501` 升级为真实 `text/event-stream`。
- 落地历史回放、轮询跟随、keepalive、终态自动关闭和 `Last-Event-ID`。

### Slice 4：测试与文档收口

- 补事件存储和 SSE API 测试。
- 新增 `Impl` 笔记、roadmap 回链和当日 worklog 记录。

## 验收与验证

- `POST /tasks` 创建 waiting intake gate 后，事件日志包含 `artifact.created`、`gate.waiting`、`task.stage_changed`
- yolo 模式下创建任务时，事件日志包含 `artifact.created`、`gate.resolved`、`task.stage_changed`
- `POST /tasks/{id}/cancel` 能发出 gate cancel 相关事件和 `task.cancelled`
- `GET /tasks/{id}/events` 对终态任务能完整回放历史事件并自动结束连接
- `Last-Event-ID` 只回放断点之后的事件，`?types=gate` 只返回 `gate.*`
- 非终态任务在连接建立后新增事件时，SSE 能在轮询窗口内推送到客户端
- 最终执行：
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`

## 关联笔记

- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[LLM-Working/p5-human-gate-webhook-implementation-plan]]
- [[LLM-Working/p5-human-gate-webhook-impl]]
- [[LLM-Working/p6-sse-streaming-impl]]
