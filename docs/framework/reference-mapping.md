---
aliases:
  - 参考项目到框架映射
tags:
  - research-agent
  - framework-design
  - summary
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# 参考项目到框架映射

> [!abstract]
> 这份映射笔记回答一个实际问题：现有调研项目里，哪些能力应该被吸收到 AI-Native Research Framework，哪些只适合作为启发而不适合直接复制。它的作用不是重新评分，而是把参考项目转换成架构决策。

## 总览结论

- `everything-claude-code` 主要贡献平台层思路，不应被误当成研究流程本身。
- `AI-Research-SKILLs` 证明“研究能力应该模块化”，但它把太多编排责任留给宿主，因此不能直接当框架主体。
- `Claude Code Deep Research` 最适合贡献阅读、综合和 citation discipline。
- `ARIS` 最适合贡献长链路编排、实验执行和跨模型审查，但其高自治叙事需要在 V1 中收敛。
- `academic-research-skills` 最适合贡献 integrity 和 review gate 思维，而不是整套投稿工厂。
- `ArgusBot` 最适合贡献监督回路、planner/reviewer 双关卡和可恢复控制面，而不是研究内容能力。
- `claude-scholar` 最适合贡献多宿主工作台和长期研究环境视角。

## 框架映射矩阵

| 项目 | 在框架中的角色 | 应吸收的部分 | 不直接复制的部分 |
| --- | --- | --- | --- |
| [[projects/everything-claude-code]] | 平台底盘参考 | hooks、rules、验证门、多宿主适配思路 | 把研究能力继续当通用 skill 附属品 |
| [[projects/ai-research-skills]] | 能力包参考 | 研究能力模块化、工具/框架级技能颗粒度 | 缺少统一工件状态与编排核心 |
| [[projects/claude-code-deep-research]] | 阅读与综合参考 | question refinement、citation-backed synthesis、标准化产物目录 | 只做到报告，不覆盖复现与实验追踪 |
| [[projects/auto-claude-code-research-in-sleep]] | 编排与执行参考 | nightly loop、run-experiment、外部 reviewer、研究闭环意识 | V1 不复制其高依赖、高自治默认值 |
| [[projects/academic-research-skills]] | 质量门参考 | integrity、review、revision、formal verification | V1 不做完整投稿与返修工厂 |
| [[projects/argusbot]] | 控制层参考 | reviewer/planner gating、daemon bus、resume continuity、operator control | 不复制 `--yolo` 默认和 Codex 专属假设 |
| [[projects/claude-scholar]] | 工作台参考 | 多 CLI、Zotero/MCP、长期个人研究环境 | 个人配置系统不等于平台核心模型 |

## 结构化借鉴

- 平台层优先借鉴 [[projects/everything-claude-code]] 和 [[projects/claude-scholar]] 的宿主兼容与长期治理观。
- 控制层优先借鉴 [[projects/argusbot]] 的监督回路、计划快照与可恢复运行面。
- 能力层优先借鉴 [[projects/ai-research-skills]] 的技能颗粒度，再用 [[projects/claude-code-deep-research]] 补阅读与证据纪律。
- 编排层优先借鉴 [[projects/auto-claude-code-research-in-sleep]] 的执行链条，但用关键人工关卡替代其默认强自治。
- 质量层优先借鉴 [[projects/academic-research-skills]] 的 integrity 观，而不是直接移植其重写作管线。

## 关键取舍

- 我们选“工件图谱系统”，而不是“技能市场”，因为后者无法给 `PaperCard`、`ReproductionTask`、`ExperimentRun` 一个统一状态语义。
- 我们选“半自动副驾”，而不是“一夜全自动”，因为现阶段更需要可信的研究账本，而不是最长的自治链。
- 我们选“repo 优先”，而不是“知识库优先”，因为平台团队真正需要的是可移交、可审计、可重跑的研究资产。

## 关联笔记

- [[framework/index]]
- [[framework/ai-native-research-framework]]
- [[framework/artifact-graph-architecture]]
- [[summary/academic-research-agents-overview]]
- [[projects/argusbot]]
- [[projects/academic-research-skills]]
