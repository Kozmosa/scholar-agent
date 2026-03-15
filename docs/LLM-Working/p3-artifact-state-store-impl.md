---
aliases:
  - P3 Artifact State Store Impl
  - P3 工件模型与状态存储实现记录
tags:
  - ainrf
  - state-store
  - artifacts
  - impl
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: d9ea76f
---
# P3 Artifact Model & State Store 实现记录

> [!abstract]
> 本笔记记录 P3 在当前仓库中的最终落地结果：新增 `ainrf.artifacts` 与 `ainrf.state` 两个子包，提供一等工件 Pydantic models、生命周期状态机、本地 JSON read model、关系索引和 task checkpoint/resume。实现保持在 Python 模块 API 层，不提前引入 P4 FastAPI 或 P7 TaskEngine。

## 实现结论

- 新增 `src/ainrf/artifacts/`：承载全部 P3 一等工件模型、状态枚举、声明式状态迁移和 `InvalidTransitionError`。
- 新增 `src/ainrf/state/`：承载本地 JSON `StateStore`、task read model、关系索引和 resumable task scan。
- 本地状态目录固定为：
  - `.ainrf/artifacts/<kind>/<artifact_id>.json`
  - `.ainrf/tasks/<task_id>.json`
  - `.ainrf/indexes/artifact-links.json`
- `StateStore` 使用 `fcntl.flock` + 临时文件 rename 做单文件原子写，满足 P3 的离线可靠性要求。
- P3 不新增 CLI 命令，也不把容器 repo 提前实现成 source of truth；当前 `.ainrf/` 仅作为 orchestrator read model。

## 代码结构

### `ainrf.artifacts`

- `models.py`
  - 公共字段：`artifact_id`、`artifact_type`、`schema_version`、时间戳、`source_task_id`、`related_artifacts`
  - 工件类型：`PaperCard`、`ReproductionTask`、`ExperimentRun`、`EvidenceRecord`、`Claim`、`ExplorationGraph`、`QualityAssessment`、`WorkspaceManifest`、`HumanGate`
- `transitions.py`
  - 声明式状态表，覆盖 `PaperCard`、`ReproductionTask`、`ExperimentRun`、`HumanGate`
- `errors.py`
  - `ArtifactError`
  - `InvalidTransitionError`

### `ainrf.state`

- `models.py`
  - `TaskRecord`、`TaskCheckpoint`、`AtomicTaskRecord`、`GateRecord`、`ArtifactQuery`
- `store.py`
  - `JsonStateStore`
  - `save_artifact()` / `load_artifact()` / `query_artifacts()`
  - `checkpoint_task()` / `load_task()` / `resume_task()` / `list_resumable_tasks()`
- `errors.py`
  - `StateStoreError`
  - `SerializationError`
  - `ResumeNotAllowedError`

## 关键实现决策

- 新模型直接采用 Pydantic v2
  - 当前仓库已有 `pydantic` 依赖，P4 还会继续消费这些类型；因此 P3 不再延续 dataclass 路线。
- `AgentAdapter` 继续保留为后续 P7 的接口
  - 虽然 roadmap 的 P3 清单把它列入一等工件，但 RFC 与工件图谱笔记都把它定义为宿主接口而非研究真相；本轮不将其持久化为 JSON artifact。
- `ResearchProject` 继续 deferred
  - 当前 P3 尚未进入容器 repo 初始化与 project aggregate 语义，引入它只会制造未消费字段。
- `ReproductionTask.active`、`ExperimentRun.pending`、`HumanGate.cancelled`
  - 这是为可执行状态机补入的最小中间状态，属于实现侧推导，不是额外产品能力。

## 自动化验证

- 定向验证
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_artifacts_models.py tests/test_state_store.py`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src/ainrf/artifacts src/ainrf/state tests/test_artifacts_models.py tests/test_state_store.py`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check src/ainrf/artifacts src/ainrf/state tests/test_artifacts_models.py tests/test_state_store.py`
- 全量验证
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`
- 当前结果
  - `pytest tests/`：45 passed
  - `ruff check src tests`：passed
  - `ty check`：passed

## Deferred 项

- 容器 repo 侧的真实 artifact source-of-truth 与 git 同步协议，保留到 P7/P8 接入。
- FastAPI request/response models、列表端点与任务调度恢复，保留到 P4/P7。
- `StateStore` 当前只支持 top-level 精确字段过滤和 `related_to` 查询，不做全文检索或嵌套 DSL。
- 目前没有把 P3 类型导出到顶层 `ainrf` 包；保持和现有 `execution` / `parsing` 并行的子包使用方式。

## 建议原子提交切片

- `docs: add p3 artifact state store implementation plan`
- `feat: add artifact models and lifecycle transitions`
- `feat: add state store and checkpoint models`
- `docs: add p3 artifact state store impl note`

## 关联笔记

- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[framework/artifact-graph-architecture]]
- [[framework/container-workspace-protocol]]
- [[LLM-Working/p3-artifact-state-store-implementation-plan]]
