---
aliases:
  - Artifact Preview Contract
  - Artifact Preview 契约
tags:
  - scholar-agent
  - contract
  - artifact
  - preview
  - implementation-plan
source_repo: scholar-agent
source_path: /Users/kozmosa/code/scholar-agent
last_local_commit: workspace aggregate
---
# Artifact Preview 契约

> [!abstract]
> 本文档定义 next release 中 dashboard 对 artifact preview 的最小契约。目标是固定前端能预览哪些工件、需要哪些元信息、哪些内容必须延期，从而保证 artifact preview 成为 next release 的真实价值点，而不是继续依赖文件系统手工查看或膨胀成大型内容平台。

## 契约结论

- next release 的 artifact preview 只覆盖 tables、reports、figures 三类核心结果。
- preview 契约的重点是“可快速浏览结果”，不是“完整编辑或分析”。
- preview 所需元信息必须稳定、简短、可由 task 详情页直接消费。

## 支持类型

### 1. tables

- 支持格式：CSV / Markdown。
- 用途：快速查看复现表格、对比结果、汇总表。

### 2. reports

- 支持格式：Markdown。
- 用途：快速查看结果报告、摘要和任务输出说明。

### 3. figures

- 支持格式：SVG / PNG。
- 用途：快速查看结果图和导出图形。

## 每个 preview item 的最小元信息

最低字段：

- `artifact_id`
- `artifact_type`
- `display_title`
- `preview_format`
- `preview_ref`

约束：

- `artifact_id` 用于唯一识别。
- `artifact_type` 必须能区分 table / report / figure。
- `display_title` 用于 UI 列表和 modal 标题。
- `preview_format` 必须能直接映射到渲染组件。
- `preview_ref` 是内容引用，不要求直接暴露底层存储实现细节。

## 首页最近 Artifacts 最小字段集

- `artifact_id`
- `artifact_type`
- `display_title`
- `preview_format`

说明：

- 首页 recent artifacts 只做轻入口，不做复杂元数据面板。

## 任务详情页 Artifact Preview 最小字段集

- `artifact_id`
- `artifact_type`
- `display_title`
- `preview_format`
- `preview_ref`
- `created_at`

## Preview 非目标

- 不做 notebook viewer。
- 不做 artifact editor。
- 不做 artifact graph browser。
- 不做全局搜索平台。

## 必须避免的错误

- 为了 preview 引入复杂内容管理平台。
- 让前端直接猜文件类型和渲染方式。
- 把 preview 契约和底层文件系统结构硬绑定。

## Deferred

- PDF 复杂文档 viewer。
- 交互式图表分析器。
- 跨任务 artifact 搜索。
- artifact graph navigation。

## 对后续文档的回写要求

- architecture baseline 与正式 architecture 文档应引用本文作为 preview contract。
- dashboard 设计稿应以本文的三类支持格式为准，不自行扩大范围。

## 关联笔记

- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]
- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]
