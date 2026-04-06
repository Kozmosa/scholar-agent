---
aliases:
  - Task Read Model Contract
  - Task Read Model 契约
tags:
  - scholar-agent
  - contract
  - task
  - read-model
  - implementation-plan
source_repo: scholar-agent
source_path: /Users/kozmosa/code/scholar-agent
last_local_commit: workspace aggregate
---
# Task Read Model 契约

> [!abstract]
> 本文档定义 next release 中 dashboard 所消费的 `task` 读模型契约。目标不是重写内部状态模型，而是固定前端真正需要看到的字段、字段分层、缺省规则和明确延期项，从而避免前端直接依赖当前 `ainrf` 的未来态字段或临时内部实现细节。

## 契约结论

- `task` 是 dashboard 的一级对象，所有首页列表、详情页、timeline、termination summary 都围绕它组织。
- read model 必须服务于展示和控制，而不是暴露全部内部状态细节。
- next release 的 task read model 应分成 5 个区块：identity、lifecycle、input summary、progress summary、result summary。
- 如果某些内部字段当前没有稳定数据源，不应为了契约完整性而伪造；应显式标为 optional 或 deferred。

## 顶层结构

task read model 至少应包含：

```json
{
  "identity": {},
  "lifecycle": {},
  "input_summary": {},
  "progress_summary": {},
  "result_summary": {}
}
```

## 1. identity

用于回答“这个 task 是什么”。

最低字段：

- `task_id`
- `mode`
- `created_at`
- `updated_at`

约束：

- `task_id` 是前后端主键，必须稳定。
- `mode` 在 next release 只允许对应 bounded discovery / bounded reproduction 两类模式。
- 时间字段至少要支持列表排序和详情展示。

## 2. lifecycle

用于回答“这个 task 现在处于什么状态”。

最低字段：

- `status`
- `stage`
- `termination_reason`
- `active_gate`

约束：

- `status` 用于高层状态显示，例如 running / completed / failed / cancelled / blocked。
- `stage` 用于更细粒度展示当前所处阶段。
- `termination_reason` 在非终态任务中可为空，在终态任务中应尽量明确。
- `active_gate` 只作为当前待处理 gate 的摘要，不暴露全部 gate 内部实现细节。

## 3. input_summary

用于回答“这个 task 是围绕什么输入启动的”。

最低字段：

- `title`
- `brief`
- `seed_inputs`
- `target_inputs`

约束：

- `title` 是面向 dashboard 的人类可读标题，不要求等于内部 task name。
- `brief` 是 1-2 句短摘要，用于列表和详情页摘要。
- `seed_inputs` / `target_inputs` 用于概括 topic、seed paper、target paper、target result 等输入，不要求直接暴露所有原始 request payload。

## 4. progress_summary

用于回答“这个 task 做到哪一步了”。

最低字段：

- `current_checkpoint`
- `milestones`
- `recent_events`
- `artifact_counts`

约束：

- `current_checkpoint` 用于首页和详情页高亮当前进度位置。
- `milestones` 应服务 timeline 展示，不要求暴露所有原始 event。
- `recent_events` 是最近若干条可读事件摘要，而不是完整日志流。
- `artifact_counts` 用于任务摘要，不要求前端先理解全部 artifact graph。

## 5. result_summary

用于回答“这个 task 产出了什么，为什么结束”。

最低字段：

- `result_brief`
- `termination_reason`
- `recent_artifacts`
- `error_summary`

约束：

- `result_brief` 是对当前结果的简洁总结。
- `recent_artifacts` 只提供最适合预览的结果工件入口。
- `error_summary` 在失败、阻塞、取消时必须可见；在正常完成时可为空。

## 列表页最小字段集

首页任务列表至少需要：

- `task_id`
- `mode`
- `title`
- `status`
- `stage`
- `updated_at`
- `termination_reason`

说明：

- 列表页不应依赖完整详情模型。
- 只要能支持排序、状态标签和点击进入详情即可。

## 详情页最小字段集

任务详情页至少需要：

- identity 全量
- lifecycle 全量
- input_summary 全量
- progress_summary 全量
- result_summary 全量

## 必须避免的错误

- 让前端直接消费原始内部状态文件结构。
- 把尚未稳定的 runtime 字段写成 required。
- 为了“字段齐全”而发明没有真实来源的数据。
- 把 artifact graph 细节塞进 task summary。

## Deferred

- 全局 task analytics 字段。
- 完整预算趋势字段。
- 精细 token telemetry 字段。
- experiment runtime streaming 字段。

## 对后续文档的回写要求

- architecture baseline 应以本文作为 task 相关 frontend / backend contract 的最小基线。
- 后续 dashboard 设计稿应引用本文，而不是自行定义 task card shape。

## 关联笔记

- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]
- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]
- [[LLM-Working/refactoring-plan/mode-baseline-spec]]
