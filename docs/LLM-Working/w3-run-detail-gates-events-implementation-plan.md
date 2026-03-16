---
aliases:
  - W3 Run Detail Gates Events Implementation Plan
  - W3 Run Detail 与 Gate 时间线规划
tags:
  - ainrf
  - webui
  - gradio
  - implementation-plan
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# W3 Run Detail, Gates & Event Timeline 实施规划

> [!abstract]
> 基于 [[framework/webui-v1-rfc]]、[[framework/webui-v1-roadmap]] 与已落地的 W2 Project / Run 表单工作台，W3 收敛为“真实 Run Detail + gate 审批 + event timeline”。目标是在不修改 FastAPI 契约的前提下，把 WebUI 从任务提交台升级为任务观察与审批台。

## 规划结论

- W3 只消费现有真实 API：`GET /tasks/{id}`、`POST /tasks/{id}/approve`、`POST /tasks/{id}/reject`、`GET /tasks/{id}/events`。
- Run Detail 以真实 `TaskDetailResponse` 为准，不新增 WebUI 自有 task schema。
- 事件视图优先消费 SSE 历史回放；如果事件流不可用，则保留 detail 展示并退回手动 refresh 的 polling fallback。
- W3 不实现 W4 的 mode mock，也不做 artifact drill-down。

## 现状与约束

- W2 已有本地 Project / run registry，但 Run Detail 仍只有 last-known binding 摘要。
- FastAPI 已经具备 gate approve/reject 和 task-scoped SSE `/tasks/{id}/events`，无需额外后端路由。
- Gradio 更适合明确的刷新驱动交互，而不是复杂前端状态机；W3 应优先落稳定回调与可恢复刷新。

## 建议模块设计

### 目录

- `src/ainrf/webui/client.py`
- `src/ainrf/webui/models.py`
- `src/ainrf/webui/app.py`
- `src/ainrf/webui/store.py`
- `tests/test_webui_client.py`
- `tests/test_webui_app.py`

### 核心接口

- `AinrfApiClient.approve_task(...)`
- `AinrfApiClient.reject_task(...)`
- `AinrfApiClient.list_task_events(...)`
- `refresh_selected_run(...)`
- `approve_run_and_render(...)`
- `reject_run_and_render(...)`

## 实现顺序

### Slice 1：client 与 session 能力

- 扩展 API client 支持 approve / reject / SSE event replay。
- 为 WebUI session 增加 selected run detail、timeline、event mode 与 refresh error。

### Slice 2：Run Detail 数据加载

- 选中 run 后加载真实 `TaskDetailResponse`。
- 把 detail 同步回本地 run registry，保持 W2 binding 状态新鲜。
- 在 Run Detail 渲染预算、artifact summary、active gate 和 timeline。

### Slice 3：gate 审批与刷新

- 在 Run Detail 加 approve / reject 按钮与 reject feedback。
- 审批后刷新 task detail、timeline 和 project run 列表。
- 在 SSE 不可用时显示 fallback 文案，但不破坏页面结构。

### Slice 4：测试与文档收口

- 补 client 的 approve/reject/event tests。
- 补 app helper 的 refresh / approve / reject tests。
- 更新 roadmap 回链与当日 worklog。

## 验收与验证

- 选中本地 run 后，WebUI 能展示真实 task detail。
- waiting gate 时，UI 可以触发 approve / reject。
- terminal run 可以稳定展示历史 timeline。
- event replay 失败时，Run Detail 仍保留 detail 展示并进入 manual refresh fallback。
- 最终执行：
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`

## 关联笔记

- [[framework/webui-v1-rfc]]
- [[framework/webui-v1-roadmap]]
- [[LLM-Working/w2-project-run-forms-implementation-plan]]
