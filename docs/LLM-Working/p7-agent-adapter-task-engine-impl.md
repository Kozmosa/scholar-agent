---
aliases:
  - P7 Agent Adapter Task Engine Impl
  - P7 Agent Adapter 与 TaskEngine 实现记录
tags:
  - ainrf
  - engine
  - adapter
  - impl
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# P7 Agent Adapter & Task Engine 实现记录

> [!abstract]
> 本笔记记录 P7 在当前仓库中的落地结果：新增顺序执行的 `TaskEngine`、基于 `claude_code_sdk` 契约的 `ClaudeCodeAdapter`、文件化 runtime secret store，以及 `ainrf run` worker 入口。实现保持在 P7 基础设施层，打通 intake 之后的 ingest / planning / executing 控制流，但不提前实现 P8 的完整深度复现领域闭环。

## 实现结论

- 新增 `src/ainrf/engine/`：
  - `TaskEngine` 负责顺序扫描可运行任务
  - `EngineContext` 统一装配 state / events / gates / parser / adapter
  - `AtomicTaskSpec` / `TaskPlanResult` / `TaskExecutionResult` 作为 worker 与 adapter 合同
- 新增 `src/ainrf/agents/`：
  - `AgentAdapter` 抽象接口
  - `ClaudeCodeAdapter` 通过 SSH 上传 remote runner，并在容器侧调用 `claude_code_sdk`
- 新增 `src/ainrf/runtime/secrets.py`：
  - `WebhookSecretStore` 将 webhook secret 从纯内存升级为 `.ainrf/runtime/webhook-secrets/` 下的文件化 runtime state
- `ainrf run` 不再是 stub：
  - `--once` 支持单轮调度
  - `--poll-interval` 支持持续 worker 模式
- P7 接通的执行路径固定为 `deep_reproduction`
  - `literature_exploration` 在当前阶段明确标记为 `mode_not_implemented`

## 关键行为

- intake 审批通过后，task 继续保持现有 API 兼容语义，由 worker 在 `planning` 阶段接管：
  - 先执行 PDF ingestion
  - 生成 `PaperCard`
  - 再调用 planner 生成 `ReproductionTask` 与 `pending_queue`
  - 触发 `plan_approval` gate
- plan gate reject 会把最近一次 feedback 注入下一轮 planning 上下文。
- plan gate approve 后，worker 按 `pending_queue` 顺序执行原子步骤，并在每步后更新：
  - `completed_steps`
  - `budget_used`
  - `artifact_refs`
  - `task.progress` 事件
- 预算任一维度触顶后，当前步骤落盘完成，任务以 `completed + budget_exhausted` 终止。
- parse 失败会生成 `EvidenceRecord(type=parse_failure)`，任务进入 `failed`。

## 测试与验证

- 新增 `tests/test_task_engine.py`
  - 覆盖 ingestion → planning → gate_waiting
  - 覆盖 plan gate approval 后的执行推进
  - 覆盖 reject feedback 回注
  - 覆盖 mode 未实现和预算耗尽终止
- 新增 `tests/test_claude_code_adapter.py`
  - 覆盖 remote runner 上传
  - 覆盖 SDK 缺失时的安装路径
  - 覆盖 plan / execute 响应解析
- 更新 `tests/test_cli.py`
  - `ainrf run --once`
  - worker 无任务 / 有任务输出
- 最终验证：
  - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
  - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`

## Deferred 项

- `claude_code_sdk` 的真实 prompt/工具约束和容器内完整研究动作，继续留给 P8 细化。
- `ExperimentRun`、`QualityAssessment`、完整 Mode 2 复现闭环，仍属于 P8。
- `literature_exploration` 真正的 TaskEngine 路径，仍属于 P9。
- 真实容器 smoke 还未在默认测试里接通；当前自动化验证使用 fake parser / fake executor / fake adapter。

## 关联笔记

- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[LLM-Working/p6-sse-streaming-impl]]
