---
aliases:
  - P4 FastAPI Service Auth Impl
  - P4 FastAPI 服务与认证实现记录
tags:
  - ainrf
  - api
  - fastapi
  - auth
  - impl
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: 7975cfa
---
# P4 FastAPI Service & Auth 实现记录

> [!abstract]
> 本笔记记录 P4 在当前仓库中的最终落地结果：新增 `ainrf.api` 服务层、API Key 认证、state-backed 任务路由、可选容器健康检查，以及 `ainrf serve` 的真实前台/daemon 启动模式。实现保持在 API skeleton 层，不提前接入 TaskEngine、Human Gate 真逻辑或 SSE publisher。

## 实现结论

- 新增 `src/ainrf/api/`：承载应用工厂、服务配置、认证 middleware、任务与健康路由、HTTP schema。
- `JsonStateStore` 扩展了 `save_task()` 与 `list_tasks()`，P4 的任务 API 直接复用 P3 的 `.ainrf/tasks/*.json` read model。
- 对外路由按 RFC 任务资源形状落地：
  - `POST /tasks`
  - `GET /tasks`
  - `GET /tasks/{id}`
  - `POST /tasks/{id}/cancel`
  - `GET /tasks/{id}/artifacts`
  - `POST /tasks/{id}/approve`
  - `POST /tasks/{id}/reject`
  - `GET /tasks/{id}/events`
  - `GET /health`
- `approve` / `reject` / `events` 在 P4 只提供占位路由，统一返回 `501`，留给 P5/P6 接管。
- `ainrf serve` 从 stub 升级为真实服务入口；`--daemon` 现在会派生后台子进程，并把 pid/log 写到 `.ainrf/runtime/` 默认路径。

## 代码结构

### `ainrf.api`

- `config.py`
  - `ApiConfig`
  - `hash_api_key()`
  - 从 `AINRF_API_KEY_HASHES` 或 `.ainrf/config.json` 读取哈希配置
- `app.py`
  - `create_app()`
- `middleware.py`
  - task 路由统一的 `X-API-Key` 校验
- `routes/health.py`
  - 服务健康检查
  - 配置容器时复用 `SSHExecutor.ping()`
- `routes/tasks.py`
  - 任务创建、列表、详情、取消、artifact 查询
  - P5/P6 兼容占位端点
- `schemas.py`
  - RFC 提交体、响应体、健康检查 schema

### `ainrf.server`

- `run_server()`
  - 前台 uvicorn 启动
- `run_server_daemon()`
  - 后台子进程拉起
  - pid/log 文件写入
  - 重复启动保护
  - `/health` 就绪轮询

### `ainrf.state`

- `store.py`
  - 新增 `save_task()`
  - 新增 `list_tasks(status=...)`
  - `checkpoint_task()` 改为复用 `save_task()`

## 关键实现决策

- API Key 只以哈希形式校验
  - 服务端不持久化明文 key；测试和运行时都通过预计算 SHA-256 哈希进行验证。
- 健康检查采用“服务层必有、容器探测可选”的策略
  - 没有 `AINRF_CONTAINER_*` 时，`GET /health` 只报告 API 与 state root 可用。
  - 配置容器后，附带 `SSHExecutor.ping()` 结果；SSH 失败时返回 `503 degraded`。
- 任务路由直接复用 P3 state store
  - P4 不引入新的 repository/service abstraction，避免 API 层与 `.ainrf/` 状态写入分叉。
- CLI daemon 测试在本地 sandbox 中改为进程管理单测
  - 当前环境禁止真实监听本地端口，故 `tests/test_server.py` 用 monkeypatch 验证子进程、pid/log、失败清理逻辑；真实网络监听保留给手工 smoke。

## 自动化验证

- 定向验证
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_auth.py tests/test_api_tasks.py tests/test_api_health.py tests/test_cli.py tests/test_server.py tests/test_state_store.py`
- 全量验证
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`
- 当前结果
  - `pytest tests/`：63 passed
  - `ruff check src tests`：passed
  - `ty check`：passed

## Deferred 项

- TaskEngine、任务队列和自动恢复执行，保留到 P7。
- Human Gate 真正的审批状态流转和 webhook 发送，保留到 P5。
- SSE 事件流与事件持久化，保留到 P6。
- `/gates/*` 资源形状与 API 版本前缀，目前都不引入，避免过早扩张兼容面。
- daemon 的真实 socket 监听 smoke 目前未纳入默认测试，原因是当前 sandbox 禁止本地 bind。

## 建议原子提交切片

- `docs: plan p4 fastapi service implementation`
- `feat: add fastapi app skeleton and api-key auth`
- `feat: add task creation and query api`
- `feat: add task artifact and cancel endpoints`
- `feat: add daemon serve mode and api stubs`
- `docs: add p4 fastapi service auth impl note`

## 关联笔记

- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[LLM-Working/p4-fastapi-service-auth-implementation-plan]]
- [[LLM-Working/p3-artifact-state-store-impl]]
