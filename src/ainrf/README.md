# AINRF Runtime README

本文档描述 `src/ainrf` 运行时模块的职责、启动方式、环境变量和联调路径。

## 1. 目录定位

`src/ainrf` 是项目的 Python 运行时实现，包含以下核心能力：

- CLI 入口（`ainrf` 命令）
- FastAPI 服务（任务创建、审批、事件流）
- Worker 调度引擎（论文解析、计划生成、步骤执行）
- Agent 适配层（当前默认 `ClaudeCodeAdapter`）
- WebUI（Gradio）
- 状态存储（JSON 文件 + JSONL 事件）

主要入口文件：

- `src/ainrf/cli.py`: CLI 命令定义
- `src/ainrf/server.py`: API 服务启动与 daemon 启动
- `src/ainrf/engine/engine.py`: 调度核心 `TaskEngine`
- `src/ainrf/api/app.py`: FastAPI 应用装配
- `src/ainrf/webui/app.py`: WebUI 交互层

## 2. 功能全景

当前实现支持以下主流程：

- `deep_reproduction`（Mode 2）: 论文复现实验流程
- `research_discovery`（Mode 1）: 文献发现与探索图谱流程

关键配套能力：

- Human Gate（intake / plan approval）
- Webhook 通知 + Secret 独立存储
- SSE 事件流（任务/工件/gate）
- 预算消耗跟踪（GPU/API/Wall Clock）
- 工件持久化（PaperCard、ExplorationGraph、Claim 等）

## 3. 运行前准备

### 3.1 Python 与依赖

项目通过 `uv` 管理依赖，推荐直接使用：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf --help
```

### 3.2 API Key 配置（启动 API 必需）

API 中间件读取 `AINRF_API_KEY_HASHES`（SHA-256 哈希值，支持逗号分隔多个 key）。

生成哈希示例：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "from ainrf.api.config import hash_api_key; print(hash_api_key('your-api-key'))"
```

设置环境变量：

```bash
export AINRF_API_KEY_HASHES=<hash1>,<hash2>
```

首次启动时，如果既没有设置 `AINRF_API_KEY_HASHES`，也没有 `.ainrf/config.json` 中的
`api_key_hashes`，`ainrf serve` 会自动进入交互式引导，要求输入 API key 并把其哈希
写入 `.ainrf/config.json`。

### 3.3 MinerU 配置（Worker 解析 PDF 必需）

`MinerUClient` 从以下环境变量读取配置：

- `AINRF_MINERU_BASE_URL`
- `AINRF_MINERU_API_KEY`
- 可选：
- `AINRF_MINERU_TIMEOUT_SECONDS`
- `AINRF_MINERU_POLL_INTERVAL_SECONDS`
- `AINRF_MINERU_MAX_RETRIES`
- `AINRF_MINERU_CACHE_DIR`
- `AINRF_MINERU_MODEL_VERSION`
- `AINRF_MINERU_LANGUAGE`
- `AINRF_MINERU_ENABLE_FORMULA`
- `AINRF_MINERU_ENABLE_TABLE`
- `AINRF_MINERU_IS_OCR`

### 3.4 容器连接配置（Agent 执行与 e2e smoke）

`ContainerConfig.from_env()` 读取：

- `AINRF_CONTAINER_HOST`（必需）
- `AINRF_CONTAINER_PORT`（默认 `22`）
- `AINRF_CONTAINER_USER`（默认 `root`）
- `AINRF_CONTAINER_SSH_KEY_PATH`
- `AINRF_CONTAINER_PASSWORD`（可选，密码认证）
- `AINRF_CONTAINER_CONNECT_TIMEOUT`（默认 `30`）
- `AINRF_CONTAINER_COMMAND_TIMEOUT`（默认 `3600`）
- `AINRF_CONTAINER_PROJECT_DIR`（默认 `/workspace/projects`）

### 3.5 交互式添加 Container（新）

可以通过 CLI 交互方式，从 SSH 命令直接生成可复用的容器配置：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf container add --state-root .ainrf
```

交互输入示例：

- profile 名称: `gpu-main`
- SSH 命令: `ssh -p 2222 researcher@gpu-server-01 -i ~/.ssh/id_ed25519`
- 远端项目目录: `/workspace/projects/attention-study`
- SSH 密码: `<可留空，留空表示 key-based auth>`

命令会把配置保存到 `.ainrf/config.json` 的 `container_profiles`，并默认设置为 `default_container_profile`。

## 4. 启动方式

### 4.1 启动 API 服务

前台模式：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf serve --host 127.0.0.1 --port 8000
```

daemon 模式：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf serve --daemon --host 127.0.0.1 --port 8000
```

首次无配置示例（会触发交互式 API key 初始化）：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf serve --host 127.0.0.1 --port 8000
```

### 4.2 启动 Worker

单次调度：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf run --once
```

持续调度：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf run --poll-interval 5
```

### 4.3 启动 WebUI

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf webui --host 127.0.0.1 --port 7860 --api-base-url http://127.0.0.1:8000
```

建议启动顺序：

1. 启动 API
2. 启动 Worker
3. 启动 WebUI

## 5. API 路由说明

目前同时支持旧路径与 `/v1` 兼容路径。

公共健康检查：

- `GET /health`
- `GET /v1/health`

需要 API Key 的主要路由：

- `GET /tasks`
- `POST /tasks`
- `GET /tasks/{task_id}`
- `GET /tasks/{task_id}/artifacts`
- `POST /tasks/{task_id}/approve`
- `POST /tasks/{task_id}/reject`
- `POST /tasks/{task_id}/cancel`
- `GET /tasks/{task_id}/events`（SSE）

对应 `/v1` 版本路径同样可用，例如 `/v1/tasks`。

## 6. 状态目录结构

默认状态根目录为 `.ainrf/`（可通过 `--state-root` 指定）。

典型结构：

```text
.ainrf/
  artifacts/
    paper-cards/
    exploration-graphs/
    claims/
    reproduction-tasks/
    experiment-runs/
    evidence/
    quality-assessments/
    human-gates/
  events/
    <task_id>.jsonl
  tasks/
    <task_id>.json
  indexes/
    artifact-links.json
  runtime/
    ainrf-api.pid
    ainrf-api.log
```

## 7. 调试与排障

### 7.1 常见问题

- API 启动报 `AINRF API key hashes are not configured`
- 原因：未设置 `AINRF_API_KEY_HASHES` 且 `.ainrf/config.json` 无哈希

- Worker 解析失败（MinerU）
- 原因：`AINRF_MINERU_BASE_URL` / `AINRF_MINERU_API_KEY` 未设置，或网络不可达

- Agent e2e smoke 被跳过
- 原因：未设置 `AINRF_CONTAINER_HOST`
- 说明：这是预期行为，测试通过 skip 保证本地无密钥环境可稳定执行

### 7.2 真实运行时 smoke

已提供专门清单：

- `docs/LLM-Working/p9-real-runtime-smoke-checklist.md`

该清单包含环境准备、运行命令、失败分类和当前行为说明。

## 8. 测试建议

快速回归（不依赖真实容器）：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_v1_routes.py tests/test_claude_code_adapter.py tests/test_webui_app.py -q -k 'not e2e_smoke_with_real_runtime and not create_webui_returns_blocks'
```

静态检查：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests
UV_CACHE_DIR=/tmp/uv-cache uv run ty check src tests
```

## 9. 对外说明

`src/ainrf` 目录主要服务运行时与研发验证，不是最终用户文档站点内容。
如果你在改动运行时行为，请同步更新：

- 对应测试（`tests/`）
- 实现状态文档（`docs/framework/v1-implementation-status.md`）
- 工作日志（`docs/LLM-Working/worklog/YYYY-MM-DD.md`）
