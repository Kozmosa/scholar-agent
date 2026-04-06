---
aliases:
  - Dashboard Baseline Spec
  - Dashboard Baseline 规格
tags:
  - scholar-agent
  - dashboard
  - webui
  - requirements
  - implementation-plan
source_repo: scholar-agent
source_path: /Users/kozmosa/code/scholar-agent
last_local_commit: workspace aggregate
---
# Dashboard Baseline 规格

> [!abstract]
> 本文档用于把 next release 的 dashboard 从“一个模糊的现代 Web UI 想法”收敛成可实现的 baseline 规格。目标是定义 dashboard 的主对象、首页信息架构、任务详情结构、artifact preview 范围、可观察性边界和明确的 deferred 列表，让后续 architecture 文档围绕一个稳定控制面而不是围绕未来态研究平台展开。

## 规格结论

- next release 的 dashboard 应被定义为 `task-centric operator dashboard`，而不是“完整研究运营平台”或“研究大屏”。
- dashboard 首先服务单用户 operator：启动任务、看当前任务、回看最近任务、查看 artifacts、观察资源和系统健康，而不是做全局知识图谱、组织协作或战略分析。
- dashboard 的主对象必须是 `task`，而不是 paper、artifact graph 或全局项目空间。
- 任何无法由当前或短期可控实现支撑的 telemetry，都不能写成 next release 的硬 requirement。

## 为什么必须先写 Dashboard Baseline

- 当前关于 dashboard 的需求已经足够具体，但如果不先写成规格，后续 architecture 很容易继续围绕未来态 research runtime 发散。
- 项目当前的核心价值排序是 dashboard、stability、observability；因此 dashboard 不是“最后补 UI”，而是 next release 的主要交付面。
- dashboard 规格必须先于 frontend 选型、页面细化和 architecture baseline，否则 scope 会反向膨胀。

## Dashboard 的定位

### 一句话定义

- dashboard 是一个单用户优先的 research operator control plane，用来观察、控制和回看 bounded discovery / bounded reproduction task。

### 它要解决的问题

- 让用户不再依赖散落的终端、日志文件和手工目录浏览来理解任务状态。
- 把任务进度、里程碑、工件、workspace 资源和系统健康放到统一界面中。
- 把“任务跑到哪了、产出了什么、出了什么问题、能不能继续”变成默认可见信息。

### 它不负责解决的问题

- 不负责成为完整研究工作台或团队协作门户。
- 不负责替代长期知识库或文献图谱浏览器。
- 不负责在 next release 中承载完整实验运营分析。

## 主对象与导航原则

### 主对象

- task 是 dashboard 的一级对象。
- workspace、session、container、artifact 都是围绕 task 展开的二级对象。

### 导航原则

- 首页应先回答“现在正在发生什么”。
- 任务详情页应回答“这个 task 到底做到了哪一步，产出了什么，为什么结束”。
- artifact 预览应服务 task 回看，而不是独立发展成大型内容浏览器。

## 首页 Baseline

### 首屏必须有的区块

1. 系统健康状态条。
2. 当前运行任务的 milestone / checkpoint timeline。
3. 最近完成任务。
4. 最近 artifacts。
5. workspace 资源快照。
6. token usage overview（仅当 telemetry 能稳定提供时启用）。

### 1. 系统健康状态条

应展示：

- API 服务状态。
- container / session SSH 可用性。
- workspace 或容器是否已就绪。
- 基础资源健康：GPU / CPU / memory / disk 是否处于可用状态。

### 2. 当前运行任务的 Timeline

应展示：

- 当前任务名称或摘要。
- 当前 mode。
- 当前阶段。
- 已完成 milestone / checkpoint。
- 当前所在 checkpoint。
- 最近日志性事件摘要。

### 3. 最近完成任务

应展示：

- 最近若干个完成、失败、取消或阻塞的任务。
- 每个任务至少展示：mode、终态、结束时间、结果摘要入口。

### 4. 最近 Artifacts

应展示：

- 最近生成的 tables、figures、reports。
- 点击后直接用 modal preview，而不是强迫用户跳到文件系统。

### 5. Workspace 资源快照

应展示：

- GPU usage。
- CPU usage。
- memory usage。
- disk usage。

### 6. Token Usage Overview

候选展示字段：

- rpm
- rph
- rpd
- tpm
- tph
- tpd

工程约束：

- 只有当运行时能稳定提供这些数据时，才纳入 baseline。
- 如果当前实现无法稳定提供，则必须延期，而不是为了满足首页字段去硬造不可靠统计。

## 任务详情页 Baseline

### 任务详情页必须回答的 5 个问题

1. 这个 task 是什么。
2. 它现在在哪个阶段。
3. 它经历了哪些 milestone / checkpoint。
4. 它产出了什么 artifacts。
5. 它为什么还在运行、已经完成、失败或被终止。

### 建议区块

1. Task Summary
2. Timeline / Checkpoints
3. Artifact Preview
4. Workspace / Session Context
5. Termination / Error Summary

### Task Summary

至少展示：

- task id
- mode
- created at / updated at
- current stage
- current status
- brief input summary

### Timeline / Checkpoints

至少展示：

- 时间排序的 milestone / checkpoint 节点
- 当前节点高亮
- 完成节点、失败节点、阻塞节点的视觉区分

### Artifact Preview

至少支持：

- tables：CSV / Markdown
- reports：Markdown
- figures：SVG / PNG

### Workspace / Session Context

至少展示：

- 当前 workspace 标识
- 当前 container / session 是否可用
- 当前资源 snapshot

### Termination / Error Summary

至少展示：

- 完成原因
- 失败原因
- 取消原因
- 阻塞原因

## Artifact Preview Baseline

### 支持格式

- tables：CSV / Markdown
- reports：Markdown
- figures：SVG / PNG

### Preview 非目标

- 不做复杂 notebook viewer。
- 不做交互式图表工作台。
- 不做 artifact graph browser。

## 可观察性 Baseline

### 必须可见的维度

- 当前任务阶段。
- milestone / checkpoint timeline。
- 最近 artifacts。
- 当前资源 snapshot。
- 系统健康状态。

### 可以延期的维度

- 精细 token telemetry。
- 完整 experiment runtime streaming。
- 全局任务 analytics。
- 历史趋势图和成本预测。

## 明确 Deferred

- artifact graph 可视化。
- 多用户协作视图。
- 全局运营分析 dashboard。
- 图形化任务编排器。
- 长期知识图谱浏览器。
- 为了 UI 炫技而引入的大量非必要图表。

## 对 Architecture 的约束

- architecture 必须围绕 task-centric control plane 组织，而不是围绕未来态完整 research platform 组织。
- frontend / backend contract 优先服务首页区块、任务详情页、artifact preview 和资源快照。
- 任何需要复杂后端重构才能勉强支撑的 UI 诉求，都应优先被降级或延期。

## 对后续文档的回写要求

- `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]` 需要以本文为 dashboard 范围基线。
- `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 中对 dashboard 的共同要求，应以本文为更具体解释。
- 后续 architecture baseline 应解释：这些 UI 区块如何映射到 task、workspace、session、artifact 和 telemetry 结构。

## 当前建议的后续原子任务

1. 起草 architecture baseline。
2. 固定 task / workspace / session / container 关系。
3. 固定 artifact preview 的数据路径与展示契约。
4. 决定 token telemetry 是否留在 next release 候选范围内。

## 关联笔记

- [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]
- [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]
- [[LLM-Working/refactoring-plan/mode-baseline-spec]]
- [[framework/v1-rfc]]
