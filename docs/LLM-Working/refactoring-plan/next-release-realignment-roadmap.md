---
aliases:
  - Next Release Realignment Roadmap
  - 下一版重对齐路线图
tags:
  - scholar-agent
  - roadmap
  - dashboard
  - release-planning
  - implementation-plan
source_repo: scholar-agent
source_path: /Users/kozmosa/code/scholar-agent
last_local_commit: workspace aggregate
---
# 下一版重对齐路线图

> [!abstract]
> 本路线图用于把 `scholar-agent` 从当前瓶颈状态推进到“单用户优先、ready-for-use 的 research dashboard next release”。路线图不试图在一轮内完成全部文档或代码，而是按可在单会话完成的原子任务拆解，并将下一版的 must-have 范围压缩到 dashboard、stability、observability、workspace/session/container integration 和 artifact preview 这些真正可交付的内容上。

## 路线图结论

- next release 应被定义为一个 task-centric operator dashboard，而不是完整研究自动化平台。
- 当前文档中的 Mode 1 / Mode 2 需要重写为 bounded baseline，而不是原样继承未来态承诺。
- 下一版的核心优先级固定为：dashboard、stability、observability。
- 任何未被明确列入 must-have 的能力，都应默认进入 deferred 列表，防止 scope 再次膨胀。

## Next Release Must-Have

### 产品面

- 新的现代 Web UI dashboard。
- task tracking。
- workspace management。
- container / session SSH integration。
- experiment result visualization 与 artifacts preview。

### 体验面

- 当前运行任务的 milestone / checkpoint timeline。
- 最近完成任务列表。
- 最近工件预览入口（tables / figures / reports）。
- 资源快照（GPU / CPU / memory / disk）。
- 单任务过程可观察，而不是只能看原始日志文件。

### 稳定性面

- 能稳定完成典型、简单、定义明确的任务。
- 失败时不频繁损坏状态。
- 关卡、取消、任务详情和工件查询要有一致行为。

## Deferred by Default

- 跨领域通用研究能力。
- 多用户、多租户和团队协作视图。
- 交互式 artifact graph 可视化。
- 开放式长期无人监督研究。
- 投稿级论文写作与 paper factory 工作流。
- 任何未被明确列入 must-have 的外围集成。

## Dashboard Baseline

- dashboard 规格以后续 `[[LLM-Working/refactoring-plan/dashboard-baseline-spec]]` 为准。

### 推荐首页信息架构

1. 顶部系统健康状态条。
2. 当前运行任务的 milestone / checkpoint timeline。
3. 最近完成任务列表。
4. 最近工件区：点击后用 modal preview。
5. 资源快照：GPU / CPU / memory / disk。
6. token usage overview（仅当运行时能稳定提供 telemetry 时纳入，否则延期）。

### Artifact Preview Baseline

- tables：优先支持 CSV / Markdown 预览。
- reports：优先支持 Markdown 预览。
- figures：优先支持 SVG / PNG 预览。

### 范围约束

- dashboard 以 task 为主对象，不先做全局研究运营大盘。
- 先做单任务时间线、摘要和 preview，不做复杂图谱探索器。

## Mode Baseline 重写目标

### Mode 1

- 目标：bounded discovery baseline。
- 典型触发方式：围绕 topic description 和 seed PDF 发起一次有边界的探索任务。
- 最小承诺：任务可启动、进度可见、工件可沉淀、边界可终止。
- 具体输入、最小输出和非目标约束以 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。

### Mode 2

- 目标：bounded reproduction baseline。
- 典型触发方式：围绕目标论文与目标结果发起一次实现 / 复现任务。
- 最小承诺：任务过程可跟踪、工件可预览、失败可归档。
- 具体输入、最小输出和非目标约束以 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。

## 推进阶段

### Phase A：叙事与需求对齐

- 写死项目新定位。
- 写死 ready-for-use 标准。
- 写死 Non-Goals。
- 重写 Mode 1 / Mode 2 baseline 定义。

### Phase B：文档体系收敛

- 起草 manifesto。
- 起草 architecture baseline。
- 起草 release decision-log 规则。
- 固定版本与 snapshot / archive 机制。

### Phase C：产品范围冻结

- 固定 dashboard 首屏信息架构。
- 固定 task tracking / workspace / SSH / preview 的 must-have。
- 列出 deferred 项目。

### Phase D：实现边界收敛

- 固定 backend / frontend contract。
- 固定 workspace / session / container 关系。
- 固定 artifacts preview 数据形态。
- 固定 observability 口径。
- 以 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]` 作为当前实现边界基线。

### Phase E：原子任务执行

- 将上述内容拆成单会话任务。
- 每次会话解决一个硬边界问题，并更新 roadmap 与 decision context。

## 推荐的原子任务拆解方法

### 原则

- 按“决策主题”拆，而不是按文件平均拆。
- 每次只完成一个可冻结的判断或一个文档切片。
- 完成后立即把结论回写到对应规划文档中。

### 第一批原子任务

1. 项目新定位声明。
2. ready-for-use 最低标准。
3. Non-Goals 清单。
4. Mode 1 baseline 定义。
5. Mode 2 baseline 定义。
6. dashboard 首屏 IA。
7. artifact preview 范围。
8. workspace / session / container 关系。
9. 版本与 release freeze 机制。
10. must-have / deferred matrix。

## 当前最需要警惕的风险

### 1. Scope Explosion

- 同时要求 dashboard、全量 Mode 1/2、复杂 telemetry 和未来态 runtime，会重复当前瓶颈。

### 2. 旧文档语义挟持新版本

- 如果不先重写 Mode baseline，现有 framework 文档会继续把 next release 拉回过大承诺。

### 3. 把“设计愿景”误写成“当前 requirement”

- 这会直接破坏工程收敛。

## 当前建议的推进顺序

1. 先写 manifesto 基线。
2. 再写 mode baseline。
3. 再写 dashboard baseline。
4. 再写 architecture baseline。
5. 最后把实现任务拆成原子会话清单。

## 关联笔记

- [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]
- [[framework/index]]
- [[framework/v1-dual-mode-research-engine]]
- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[LLM-Working/refactoring-plan/mode-baseline-spec]]
- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]
- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]
