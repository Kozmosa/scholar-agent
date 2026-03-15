---
aliases:
  - P3 Artifact State Store Implementation Plan
  - P3 工件模型与状态存储规划
tags:
  - ainrf
  - state-store
  - artifacts
  - implementation-plan
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: d9ea76f
---
# P3 Artifact Model & State Store 实施规划

> [!abstract]
> 基于 [[framework/v1-rfc]]、[[framework/v1-roadmap]]、[[framework/artifact-graph-architecture]] 与当前仓库已经落地的 `execution` / `parsing` 模块边界，本规划将 P3 收敛为“Pydantic 工件模型 + 本地 JSON read model + 任务 checkpoint/resume”。目标是在不提前实现 FastAPI 或 TaskEngine 的前提下，先交付一套可序列化、可查询、可恢复的核心状态层。

## 规划结论

- P3 的新领域模型直接使用 Pydantic v2，而不是延续现有 dataclass 风格；这样 P4 的 request/response models 可以直接复用，不需要再做一层迁移。
- `StateStore` 采用本地 read model 定位：满足 `save/load/query/checkpoint/resume` 与离线测试，但不把本地 JSON 定义为研究产物的长期 source of truth。
- 模块边界拆为 `src/ainrf/artifacts/` 和 `src/ainrf/state/` 两层，避免把状态机、任务 checkpoint 与 JSON 文件 I/O 混在一个包里。
- P3 不新增 CLI 命令，也不接入真实执行编排；所有对外契约先以 Python 模块 API 形式暴露。
- `AgentAdapter` 在 P3 继续视为后续 P7 的接口，而不是可落库 artifact；`ResearchProject` 也延后到真正需要 project aggregate 的阶段再引入。

## 现状与约束

- 已有代码风格：当前 `src/ainrf/execution/` 与 `src/ainrf/parsing/` 均按“models / errors / implementation”拆分，P3 应复用这种子包组织，而不是堆到顶层单文件。
- 已有质量基线：本地已通过 `pytest`、`ruff check`、`ty check`，说明可以按增量功能切片推进，不需要先做基线修复。
- 长期约束：`PROJECT_BASIS.md` 要求所有关键编辑、验证和提交动作都落到 `docs/LLM-Working/worklog/YYYY-MM-DD.md`；P3 实施必须把这部分作为正式流程，而不是会话内约定。
- 当前工作树存在与 P3 无关的文档改动；实施时需要路径级隔离提交，不得回滚他人未提交内容。

## 范围界定

### In Scope

- 一等工件的 Pydantic v2 models：`PaperCard`、`ReproductionTask`、`ExperimentRun`、`EvidenceRecord`、`Claim`、`ExplorationGraph`、`QualityAssessment`、`WorkspaceManifest`、`HumanGate`
- 以声明式转换表实现的工件状态机和 `InvalidTransitionError`
- `StateStore` protocol 与 JSON 实现：artifact save/load/query、task checkpoint/resume、resumable task scan
- `.ainrf/tasks/`、`.ainrf/artifacts/`、`.ainrf/indexes/` 的本地目录布局
- 关系索引和基于引用关系的查询能力
- 离线测试与 round-trip 验证

### Out of Scope

- FastAPI、OpenAPI、SSE、webhook 和任何 P4/P5/P6 服务能力
- TaskEngine 的实际调度与自动恢复执行；P3 只负责恢复状态，不负责任务重跑
- 容器侧 git repo 的真实 artifact 落库；该 source of truth 在 P7/P8 再接入
- 新 CLI 表面和用户级命令

## 建议模块设计

### 目录

- `src/ainrf/artifacts/__init__.py`
- `src/ainrf/artifacts/errors.py`
- `src/ainrf/artifacts/models.py`
- `src/ainrf/artifacts/transitions.py`
- `src/ainrf/state/__init__.py`
- `src/ainrf/state/errors.py`
- `src/ainrf/state/models.py`
- `src/ainrf/state/store.py`
- `tests/test_artifacts_models.py`
- `tests/test_state_store.py`

### 核心接口

- `ainrf.artifacts`
  - 导出全部 artifact models、状态枚举、`InvalidTransitionError`
  - 每个有生命周期的 artifact 提供统一 `transition_to(next_status)` 入口
- `ainrf.state`
  - `StateStore` protocol
  - `JsonStateStore`
  - `save_artifact()` / `load_artifact()` / `query_artifacts()`
  - `checkpoint_task()` / `load_task()` / `resume_task()` / `list_resumable_tasks()`

## 实现顺序

### Slice 1：模型与状态机

- 先定义 artifact 公共基类、关系引用类型和状态枚举。
- 把文档中已稳定的状态转移写成转换表，而不是散落在 if-else 中。
- 先补状态机与模型单测，确认非法迁移和字段校验都可预测。

### Slice 2：Artifact JSON Store

- 实现 `.ainrf/artifacts/<kind>/<id>.json` 的 snapshot 持久化。
- 用 `fcntl.flock` + 临时文件 rename 保证单文件原子写。
- 加关系索引文件，支持按 `related_to` 查询下游 artifact。

### Slice 3：Task Checkpoint / Resume

- 对齐 RFC 的任务 JSON 结构，实现 task-level read model。
- `resume_task()` 只负责恢复和校验，不负责调度。
- 补未完成任务扫描和 checkpoint round-trip 测试。

### Slice 4：文档收口

- 新增 `Impl` 笔记，记录最终接口、关键取舍、验证命令和 deferred 项。
- 在实现规划文档中补实现结果 backlink，保持 `docs/LLM-Working/` 的阶段索引闭环。

## 验收与验证

- `PaperCard(captured)` 只能转到 `structured`
- `HumanGate(waiting)` 能转到 `approved` / `rejected`
- 保存 artifact 后重新加载，字段和值一致
- `query_artifacts(related_to=...)` 能返回关系链上的下游对象
- `checkpoint_task()` 后 `resume_task()` 能恢复到 checkpoint 时刻
- 最终执行：
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`

## 原子提交建议

- `docs: add p3 artifact state store implementation plan`
- `feat: add artifact models and lifecycle transitions`
- `feat: add json artifact state store`
- `feat: add task checkpoint and resume state store`
- `docs: add p3 artifact state store impl note`

## 关联笔记

- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[framework/artifact-graph-architecture]]
- [[framework/container-workspace-protocol]]
- [[LLM-Working/p2-mineru-implementation-plan]]
- [[LLM-Working/p3-artifact-state-store-impl]]
