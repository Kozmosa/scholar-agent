# AINRF Runtime README

本文档描述 `src/ainrf` 当前保留运行时的职责、启动方式、环境变量和联调路径。

## 1. 目录定位

> [!success]
> Cleanup gate passed：旧的 task/orchestrator/WebUI product center 已从当前 runtime 主路径移除；现阶段只保留 daemon/API health、container profile 和 SSH health probing 这组最小存活表面，作为后续 realignment 的起点。

`src/ainrf` 当前仅保留以下稳定能力：

- CLI 入口（`ainrf` 命令）
- FastAPI 服务（仅健康检查与 API key 中间件）
- 容器连接配置持久化（`ainrf container add`）
- SSH 容器健康探测与远端命令执行
- API daemon 启停支持

主要入口文件：

- `src/ainrf/cli.py`: CLI 命令定义
- `src/ainrf/server.py`: API 服务启动与 daemon 启动
- `src/ainrf/api/app.py`: FastAPI 应用装配
- `src/ainrf/api/routes/health.py`: 健康检查路由
- `src/ainrf/execution/ssh.py`: SSH 执行与健康探测

## 2. 当前支持的 CLI 表面

### 2.1 启动 API 服务

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

### 2.2 交互式添加 Container

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

## 3. 运行前准备

### 3.1 Python 与依赖

项目通过 `uv` 管理依赖，推荐直接使用：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf --help
```

### 3.2 首次运行 Onboarding

AINRF 默认使用当前工作目录下的 `./.ainrf/` 作为 state root；如果通过 `--state-root`
显式指定，则改用指定目录。

当目录内还不存在 `./.ainrf/config.json`，且也没有通过环境变量提供
`AINRF_API_KEY_HASHES` 时，第一次执行 `ainrf serve` 会自动进入交互式 onboarding。
如果希望显式执行同一流程，也可以直接运行：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run ainrf onboard
```

onboarding 至少会创建 `./.ainrf/config.json`。最小可用配置只需要包含
`api_key_hashes`；在同一交互流程里，用户也可以选择顺手写入一个默认的 container
profile，供后续容器连接配置复用。

### 3.3 API Key 配置（启动 API 必需）

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

### 3.3 容器连接配置

`ContainerConfig.from_env()` 读取：

- `AINRF_CONTAINER_HOST`（必需）
- `AINRF_CONTAINER_PORT`（默认 `22`）
- `AINRF_CONTAINER_USER`（默认 `root`）
- `AINRF_CONTAINER_SSH_KEY_PATH`
- `AINRF_CONTAINER_PASSWORD`（可选，密码认证）
- `AINRF_CONTAINER_CONNECT_TIMEOUT`（默认 `30`）
- `AINRF_CONTAINER_COMMAND_TIMEOUT`（默认 `3600`）
- `AINRF_CONTAINER_PROJECT_DIR`（默认 `/workspace/projects`）

如果未设置环境变量，也可以从 `.ainrf/config.json` 的默认容器 profile 读取。

## 4. API 路由说明

### 4.1 Terminal Bench MVP

Terminal Bench MVP 依赖本机可执行的 `ttyd` 二进制；联调前请先确认：

```bash
ttyd --version
```

当前 runtime API 只暴露以下最小表面：

- 公共健康检查路径：
  - `GET /health`
  - `GET /v1/health`
- Terminal Bench MVP 路径（均受 API key 中间件保护）：
  - `GET /terminal/session`
  - `POST /terminal/session`
  - `DELETE /terminal/session`
  - `GET /v1/terminal/session`
  - `POST /v1/terminal/session`
  - `DELETE /v1/terminal/session`

其中 terminal session API 只控制单个 ttyd-backed browser terminal session：

- `GET /terminal/session`：读取当前终端 session 状态
- `POST /terminal/session`：创建或刷新当前终端 session
- `DELETE /terminal/session`：关闭当前终端 session

`/v1/terminal/session` 提供相同语义的版本化镜像路径。

已移除的旧 task 路径不会再由应用注册；在提供有效 API key 后会返回 `404`。

## 5. 状态目录结构

默认状态根目录为 `.ainrf/`（可通过 `--state-root` 指定）。

当前实际使用的典型结构：

```text
.ainrf/
  config.json
  runtime/
    ainrf-api.pid
    ainrf-api.log
```

## 6. 调试与排障

### 6.1 常见问题

- API 启动报 `AINRF API key hashes are not configured`
- 原因：未设置 `AINRF_API_KEY_HASHES` 且 `.ainrf/config.json` 无哈希

- 容器健康检查显示 `degraded`
- 原因：SSH 不可达、Claude CLI 不可用、Anthropic key 缺失，或远端项目目录不可写

- daemon 启动失败
- 原因：端口不可用，或健康检查在超时窗口内未就绪

### 6.2 推荐验证

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_auth.py tests/test_api_health.py tests/test_api_v1_routes.py tests/test_cli.py tests/test_server.py tests/test_execution_ssh.py -q
python -m compileall src/ainrf
```

## 7. 对外说明

`src/ainrf` 目录当前主要服务于最小化运行时验证，不再包含任务编排、工件存储、事件流、解析流程或 WebUI 能力。
如果你继续收缩或调整运行时行为，请同步更新：

- 对应测试（`tests/`）
- 工作日志（`docs/LLM-Working/worklog/YYYY-MM-DD.md`）
