---
aliases:
  - Workspace Session Container Summary Contract
  - Workspace / Session / Container 摘要契约
tags:
  - scholar-agent
  - contract
  - workspace
  - session
  - container
  - implementation-plan
source_repo: scholar-agent
source_path: /Users/kozmosa/code/scholar-agent
last_local_commit: workspace aggregate
---
# Workspace / Session / Container 摘要契约

> [!abstract]
> 本文档定义 next release 中 dashboard 对 workspace、session、container 的最小摘要契约。目标是让前端能够展示“任务在哪个执行上下文里运行、当前是否可连接、资源是否健康”，而不把这一层扩展成独立的 infra orchestrator 或云平台模型。

## 契约结论

- workspace、session、container 都是 task 的二级对象，不应在 next release 中演化为独立产品中心。
- dashboard 只需要它们的 summary contract，而不是完整编排模型。
- 这层的职责是可见、可诊断、可关联，不是调度和自动恢复平台。

## 顶层结构

```json
{
  "workspace": {},
  "session": {},
  "container": {},
  "resource_snapshot": {}
}
```

## 1. workspace summary

最低字段：

- `workspace_id`
- `workspace_label`
- `project_dir`

约束：

- 前端只需要知道 task 对应哪个 workspace，以及该 workspace 的人类可读标识。
- 不要求 next release 暴露完整文件树或复杂目录索引。

## 2. session summary

最低字段：

- `session_status`
- `connected`
- `recoverable`

约束：

- `session_status` 主要用于“当前是否有可用执行上下文”。
- `connected` 只表示当前是否可连，不要求表达完整会话历史。
- `recoverable` 用于帮助判断 task 是否还能继续。

## 3. container summary

最低字段：

- `container_label`
- `ssh_available`
- `environment_status`

约束：

- `container_label` 用于人类可读识别。
- `ssh_available` 是 next release 的关键健康信号之一。
- `environment_status` 用于回答“当前环境是否可用于继续任务”。

## 4. resource_snapshot

最低字段：

- `gpu`
- `cpu`
- `memory`
- `disk`

约束：

- 这是 snapshot，不是复杂时序分析。
- next release 只要求展示当前快照，不要求长期趋势图。

## 首页最小展示要求

- 当前 workspace 标识。
- 当前 session 是否可用。
- container / SSH 是否可用。
- GPU / CPU / memory / disk 快照。

## 详情页最小展示要求

- workspace label / project_dir。
- session 状态。
- container 健康摘要。
- resource snapshot。

## 必须避免的错误

- 把 workspace 设计成独立大模块，脱离 task 导航。
- 把 session 设计成复杂多会话编排模型。
- 把 container 扩展成生命周期管理平台。
- 为资源区块引入过重的 telemetry 平台。

## Deferred

- 多 container fleet 视图。
- 多 workspace 对比分析。
- 长期资源趋势图。
- 自动调度与自动恢复平台。

## 关联笔记

- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]
- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]
