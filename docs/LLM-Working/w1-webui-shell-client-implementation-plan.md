---
aliases:
  - W1 WebUI Shell Client Implementation Plan
  - W1 WebUI 壳层与客户端规划
tags:
  - ainrf
  - webui
  - gradio
  - implementation-plan
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# W1 WebUI App Shell & API Client 实施规划

> [!abstract]
> 基于 [[framework/webui-v1-rfc]]、[[framework/webui-v1-roadmap]] 与当前已落地的 FastAPI/CLI 契约，W1 收敛为“可启动的 Gradio 壳层 + 会话级 API 连接面 + 三页空壳工作台 + typed API client”。目标是为 W2/W3 固定入口、状态模型和错误处理边界，而不提前实现 Project 持久化、Run 创建或 SSE 交互。

## 规划结论

- W1 新增 `ainrf webui` 命令，但不负责自动拉起 `ainrf serve`；WebUI 只连接外部已运行的 API 服务。
- API 地址和 API key 通过 WebUI 顶部 connect panel 输入，信息仅保留在当前 Gradio 会话内存中，不写入 `.ainrf/config.json`。
- 页面结构直接落三页：`Project List`、`Project Detail`、`Run Detail`。后两页在 W1 只提供稳定 empty state，不引入 demo data。
- API client 只覆盖 W1 所需的读接口：`/health`、`/tasks`、`/tasks/{id}`；approve/reject/events 留给 W3。
- WebUI 继续遵循“Project 只是 UI 组织层”的 RFC 约束，不在 W1 引入 project 本地持久化。

## 现状与约束

- CLI 当前只有 `serve` / `run` 两个命令，`tests/test_cli.py` 已覆盖帮助信息、daemon 启动和 worker 入口；W1 必须同步扩展 CLI smoke。
- `/health` 与 `/openapi.json` 当前是公开端点，`/tasks*` 受 `X-API-Key` 保护；因此连接流应先探测 `/health`，再用 `/tasks` 校验鉴权。
- 现有 `TaskCreateRequest` / `TaskDetailResponse` 不包含 `project_slug`，说明 W1 不能假设后端已有 project 归属字段。
- `.ainrf/` 现有用途已覆盖 `tasks/`、`artifacts/`、`events/`、`runtime/`；W1 不应擅自复用 `config.json` 保存 UI 会话信息。
- 现有依赖未包含 Gradio；W1 需要在 `pyproject.toml` 中补充并通过全量测试、lint 与 `ty check`。

## 建议模块设计

### 目录

- `src/ainrf/webui/__init__.py`
- `src/ainrf/webui/app.py`
- `src/ainrf/webui/client.py`
- `src/ainrf/webui/models.py`
- `tests/test_webui_client.py`
- `tests/test_webui_app.py`

### 核心接口

- `create_webui(config: WebUiConfig) -> gr.Blocks`
- `launch_webui(config: WebUiConfig) -> None`
- `AinrfApiClient.get_health()`
- `AinrfApiClient.list_tasks(...)`
- `AinrfApiClient.get_task(task_id)`

## 实现顺序

### Slice 1：依赖、CLI 与 view model

- 在 `pyproject.toml` 补 `gradio`。
- 扩展 `ainrf` CLI，新增 `webui` 子命令和对应 help。
- 定义 `WebUiConfig`、`ConnectionSession`、`TaskStageSummary` 等内部状态类型。

### Slice 2：API client

- 封装 `httpx` 调用和错误映射。
- 用现有 `ainrf.api.schemas` 解析 `/health`、`/tasks`、`/tasks/{id}` 返回。
- 把鉴权错误、连接错误和协议错误收敛成独立异常类型。

### Slice 3：Gradio 壳层

- 构建顶部联系面板与三页 tab。
- 连接成功后在 `Project List` 渲染健康状态和任务 stage 聚合。
- 对 `Project Detail` / `Run Detail` 提供稳定的 empty state。

### Slice 4：测试与文档收口

- 新增 WebUI client / app 测试。
- 更新 CLI 测试。
- 在 `[[framework/webui-v1-roadmap]]` 的 W1 段落补实施规划回链。

## 验收与验证

- `ainrf --help` 和 `ainrf webui --help` 能展示新命令和参数。
- `ainrf webui` 能把 host、port、API base URL 传入 Gradio 启动函数。
- WebUI connect panel 对 `/health` 的 `200` 和 `503` 都能识别为服务可达。
- API key 无效时，UI 显示鉴权失败状态，不崩溃。
- `Project List` 能基于真实 `/tasks` 结果渲染 stage 聚合。
- `Project Detail` / `Run Detail` 在无 project/run 上下文时渲染稳定占位内容。
- 最终执行：
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`

## 关联笔记

- [[framework/webui-v1-rfc]]
- [[framework/webui-v1-roadmap]]
- [[framework/v1-rfc]]
