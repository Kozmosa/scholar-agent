---
aliases:
  - W2 Project Run Forms Implementation Plan
  - W2 Project 与 Run 表单规划
tags:
  - ainrf
  - webui
  - gradio
  - implementation-plan
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# W2 Project & Run Forms 实施规划

> [!abstract]
> 基于 [[framework/webui-v1-rfc]]、[[framework/webui-v1-roadmap]] 与已落地的 W1 WebUI 壳层，W2 收敛为“本地 Project 持久化 + Project 默认配置表单 + Project Detail 内联 Run 创建表单 + 本地 run registry”。目标是在不修改 FastAPI 契约的前提下，把 WebUI 从观察壳层升级为可配置、可提交任务的工作台。

## 规划结论

- Project 持久化采用本地 `state_root`，数据固定写入 `.ainrf/webui/` 下，不与 API 的 `.ainrf/config.json` 混用。
- Project 与 runs 的归属采用 registry-first：只记录通过 WebUI 创建的 runs，历史 tasks 不自动导入。
- Project 默认配置采用 full defaults：共享默认值加 Mode 1 / Mode 2 模板都可编辑。
- Run 创建在 Project Detail 内联完成，不做独立向导页。
- 论文输入在 W2 仅支持 `pdf_url` / `pdf_path` 文本，不做浏览器文件上传。

## 现状与约束

- 现有 `POST /tasks` 仍然只接受 `TaskCreateRequest`，没有 `project_slug` 字段，也没有文件上传接口。
- W1 已有 session 级 API 连接态和三页壳层，但没有本地 store，也没有 create-task client 方法。
- 仓库的 `default_state_root()` 已固定为 `.ainrf`，适合为 WebUI 新增子目录而不是引入平行存储根。
- `webhook_secret` 仍然只能作为一次性提交参数，不能进入本地 Project JSON 或 run registry。

## 建议模块设计

### 目录

- `src/ainrf/webui/store.py`
- `src/ainrf/webui/models.py`
- `src/ainrf/webui/app.py`
- `src/ainrf/webui/client.py`
- `tests/test_webui_store.py`
- `tests/test_webui_app.py`
- `tests/test_webui_client.py`

### 核心接口

- `JsonProjectStore`
- `ProjectRecord`
- `ProjectRunRecord`
- `save_project_from_form(...)`
- `submit_project_run(...)`
- `build_task_create_request(...)`

## 实现顺序

### Slice 1：本地 store 与 CLI

- 为 `ainrf webui` 新增 `--state-root`。
- 新增 Project/store 模型与 `.ainrf/webui/` 目录布局。
- 补 CLI 测试覆盖新参数。

### Slice 2：Project 编辑面

- 落地 Project create/edit 表单。
- 支持 slug 创建时输入、保存后固定。
- 在 Project List 显示本地 projects 与本地 run 计数。

### Slice 3：Run 创建面

- 扩展 API client 支持 `POST /tasks`。
- 在 Project Detail 落地 inline Run 表单。
- 提交成功后写入本地 run registry 并刷新列表。

### Slice 4：同步、测试与文档收口

- 连接 API 后，用 `/tasks` 回填本地 run binding 状态。
- 补 Project store、payload 映射与 Run 提交测试。
- 更新 roadmap 回链与当日 worklog。

## 验收与验证

- `ainrf webui --state-root ...` 能把路径传入 WebUI config。
- WebUI 可以本地创建、编辑、重新加载 Project。
- Mode 1 / Mode 2 表单都能映射到合法 `TaskCreateRequest`。
- Run 创建成功后，Project Detail run 列表能显示本地绑定记录与最新状态。
- `webhook_secret` 不写入本地 store。
- 最终执行：
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`

## 关联笔记

- [[framework/webui-v1-rfc]]
- [[framework/webui-v1-roadmap]]
- [[LLM-Working/w1-webui-shell-client-implementation-plan]]
