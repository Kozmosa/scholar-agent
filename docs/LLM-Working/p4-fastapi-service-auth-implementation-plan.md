---
aliases:
  - P4 FastAPI Service Auth Implementation Plan
  - P4 FastAPI 服务与认证规划
tags:
  - ainrf
  - api
  - fastapi
  - auth
  - implementation-plan
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: 7975cfa
---
# P4 FastAPI Service & Auth 实施规划

> [!abstract]
> 基于 [[framework/v1-rfc]]、[[framework/v1-roadmap]] 与当前仓库已经落地的 `execution`、`parsing`、`artifacts`、`state` 模块，本规划将 P4 收敛为“state-backed FastAPI 服务骨架 + API Key 认证 + OpenAPI + CLI daemon 启动”。目标是在不提前实现 TaskEngine、Human Gate 真逻辑和 SSE publisher 的前提下，先交付可运行、可测试、可扩展的对外 API 层。

## 规划结论

- P4 按 RFC 的任务路由骨架落地，而不是只做 roadmap 最小端点；`approve` / `reject` / `events` 先挂占位路由，为 P5/P6 保留兼容接口。
- 认证采用 API Key 哈希校验，统一读取 `X-API-Key`，只接受 SHA-256 哈希配置，不在本地配置文件持久化明文 key。
- `ainrf serve` 从 stub 升级为真实服务入口；`--daemon` 在 P4 必须是真后台化而不是保留占位。
- 任务 API 直接复用 P3 的 `TaskRecord` / `JsonStateStore` 作为 read model，避免再造一套平行持久化层。
- P4 完成后同步新增 `[[LLM-Working/p4-fastapi-service-auth-impl]]`，记录最终接口、验证结果和 deferred 项。

## 现状与约束

- 已有依赖：`pyproject.toml` 已声明 `fastapi`、`uvicorn`、`httpx`、`pydantic`，不需要再补基础服务依赖。
- 已有状态层：`src/ainrf/state/` 已提供 task checkpoint / load / resume，但还缺少面向 API 的 `save_task` 与任务列表查询接口。
- 已有执行器：`src/ainrf/execution/` 已能提供 `SSHExecutor.ping()`，因此 `GET /health` 可以实现“服务健康 + 可选容器探测”。
- 当前 CLI 仍是 P0 stub，`tests/test_cli.py` 也只覆盖帮助信息和 stub 输出；P4 必须同步把 CLI 验收升级到真实 server 启动和 daemon 行为。
- 长期约束要求新增 Python 代码具备严格类型标注，并通过 `pytest`、`ruff check`、`ty check`；同时需要向 `docs/LLM-Working/worklog/2026-03-16.md` 追加完成批次记录。

## 范围界定

### In Scope

- `src/ainrf/api/` 模块骨架：应用工厂、配置解析、认证中间件、路由、schema
- API Key 认证：`X-API-Key` header、SHA-256 哈希比对、多 key 支持
- 任务相关路由：`POST /tasks`、`GET /tasks`、`GET /tasks/{id}`、`POST /tasks/{id}/cancel`、`GET /tasks/{id}/artifacts`
- RFC 兼容占位路由：`POST /tasks/{id}/approve`、`POST /tasks/{id}/reject`、`GET /tasks/{id}/events`
- `GET /health`：服务健康，且在配置容器时附加可选 SSH 健康探测
- `ainrf serve` 前台与 daemon 模式
- OpenAPI schema 自动生成与 request/response 示例

### Out of Scope

- TaskEngine 真正调度、自动恢复执行、任务队列
- Human Gate 生命周期管理和 webhook 发送
- SSE 事件发布与事件持久化
- `/gates/*` 资源形状；P4/P5 统一按 RFC 的 task-scoped 审批端点
- `/v1` 版本前缀；当前阶段保留根路径

## 建议模块设计

### 目录

- `src/ainrf/api/__init__.py`
- `src/ainrf/api/app.py`
- `src/ainrf/api/config.py`
- `src/ainrf/api/dependencies.py`
- `src/ainrf/api/middleware.py`
- `src/ainrf/api/routes/health.py`
- `src/ainrf/api/routes/tasks.py`
- `src/ainrf/api/schemas.py`
- `tests/test_api_auth.py`
- `tests/test_api_tasks.py`
- `tests/test_api_health.py`

### 核心接口

- `create_app(config: ApiConfig | None = None) -> FastAPI`
- `ApiConfig.from_env(...)`
- `ApiStateStore` 继续复用 `JsonStateStore`
- `run_server(host, port, state_root, api_config)`
- `run_server_daemon(host, port, pid_file, log_file, state_root, api_config)`

## 实现顺序

### Slice 1：文档与服务骨架

- 新增 P4 规划笔记并在 roadmap 中补链接。
- 建立 `src/ainrf/api/` 包、应用工厂和健康检查骨架。
- 先让 `/health` 与 `/openapi.json` 可访问，再把 auth middleware 接入其余路由。

### Slice 2：认证与任务 schema

- 实现 API Key 哈希配置解析和中间件。
- 补 RFC 提交体 schema、任务摘要/详情 schema、错误返回 shape。
- 增加 `JsonStateStore.save_task()` 和 `list_tasks()`。

### Slice 3：任务端点

- 落地 `POST /tasks`、`GET /tasks`、`GET /tasks/{id}`、`POST /tasks/{id}/cancel`、`GET /tasks/{id}/artifacts`。
- 把 `approve` / `reject` / `events` 作为兼容占位路由挂上，统一返回 `501`。
- 为 OpenAPI 补示例和状态码说明。

### Slice 4：CLI daemon 与文档收口

- 把 `ainrf serve` 切到 uvicorn 真实启动。
- 实现 pid/log 文件写入、重复启动保护、健康探测轮询。
- 新增 `Impl` 笔记和当日 worklog 记录。

## 验收与验证

- 无 API Key 访问受保护端点返回 `401`
- 错误 API Key 返回 `401`
- 正确 API Key + `POST /tasks` 创建成功并写入 `.ainrf/tasks/`
- `GET /tasks?status=` 能按任务状态过滤
- `GET /tasks/{id}/artifacts` 能返回关联工件列表
- `POST /tasks/{id}/cancel` 能更新非终态任务并拒绝取消终态任务
- `GET /health` 在无容器配置时返回 `status=ok`；有容器配置时可返回容器健康详情或降级状态
- `ainrf serve --daemon` 能拉起后台进程并通过 `/health` 探测成功
- 最终执行：
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`

## 建议原子提交

- `docs: plan p4 fastapi service implementation`
- `feat: add fastapi app skeleton and api-key auth`
- `feat: add task creation and query api`
- `feat: add task artifact and cancel endpoints`
- `feat: add daemon serve mode and api stubs`
- `docs: add p4 fastapi service auth impl note`

## 关联笔记

- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[LLM-Working/p3-artifact-state-store-implementation-plan]]
- [[LLM-Working/p3-artifact-state-store-impl]]
- [[LLM-Working/p4-fastapi-service-auth-impl]]
