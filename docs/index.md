---
aliases:
  - 学术研究 Agent 调研与框架索引
tags:
  - research-agent
  - obsidian-note
  - index
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# 学术研究 Agent 调研索引

> [!abstract]
> 这是一组面向 Obsidian 知识库的本地笔记，现已分成两条主线：一条是对 8 个参考项目的静态调研，另一条是基于这些项目抽象出的 [[framework/index|AI-Native Research Framework]]。正文以中文为主，文件名使用英文 slug，结论基于本地仓库静态信息与设计推演，不包含联网补充调研或完整运行验证。

## 阅读方式

- 如果目标是构建自己的研究系统，先读 [[framework/index]]。
- 如果目标是先看外部项目版图，再读 [[summary/academic-research-agents-overview]]。
- 按项目类型回看单仓库报告，确认每个方案的工作流、集成面和局限。
- 如果目标是“增强现有 agent”，优先看 [[projects/ai-research-skills]]、[[projects/argusbot]]、[[projects/claude-scholar]]、[[projects/everything-claude-code]]。
- 如果目标是“直接做研究/写论文”，优先看 [[projects/auto-claude-code-research-in-sleep]]、[[projects/claude-code-deep-research]]、[[projects/academic-research-skills]]、[[projects/awesome-claudecode-paper-proofreading]]。

## 框架主线

| 笔记 | 作用 | 先读理由 |
| --- | --- | --- |
| [[framework/index]] | 框架导航页 | 先建立自有框架的阅读顺序 |
| [[framework/ai-native-research-framework]] | 愿景与系统边界 | 明确为什么它不是另一条固定 pipeline |
| [[framework/artifact-graph-architecture]] | 工件图谱与分层架构 | 把平台层、能力层、编排层、产物层拆开 |
| [[framework/v1-dual-mode-research-engine]] | 双模式 V1 规格 | 明确两种操作模式、人工关卡和终止合同 |
| [[framework/reference-mapping]] | 参考项目到框架映射 | 追溯设计依据，避免蓝图脱离证据层 |

## 项目清单

| 项目 | 定位 | 先读理由 |
| --- | --- | --- |
| [[projects/ai-research-skills]] | AI 研究工程技能库 | 覆盖面最广，适合作为能力底座 |
| [[projects/auto-claude-code-research-in-sleep]] | 过夜自治科研流水线 | 强调跨模型协作、实验执行与自动 review |
| [[projects/claude-code-deep-research]] | 深度研究与引文验证框架 | 聚焦问题澄清、研究执行和 citation-backed 报告 |
| [[projects/academic-research-skills]] | 从研究到发表的学术全流程管线 | 最强调 integrity、review 和定稿流程 |
| [[projects/argusbot]] | Codex 监督式 autoloop 控制层 | 解决长任务续跑、reviewer gating 和远程控制 |
| [[projects/awesome-claudecode-paper-proofreading]] | LaTeX 论文校对 prompt 工作流 | 极窄但实用，适合投稿前精修 |
| [[projects/claude-scholar]] | 学术研究与开发一体化个人配置 | 研究、开发、Zotero MCP 和多 CLI 支持兼顾 |
| [[projects/everything-claude-code]] | 通用 agent harness 基线 | 用作研究仓库的基础设施对照组 |

## 能力入口

- 自有框架设计：[[framework/index]]
- 研究工程技能底座：[[projects/ai-research-skills]]
- 自治研究流水线：[[projects/auto-claude-code-research-in-sleep]]
- 深度研究与报告生成：[[projects/claude-code-deep-research]]
- 学术写作、审稿与 integrity：[[projects/academic-research-skills]]
- Codex 监督式 autoloop 与远程控制：[[projects/argusbot]]
- 论文终稿校对：[[projects/awesome-claudecode-paper-proofreading]]
- 个人研究工作台：[[projects/claude-scholar]]
- 通用 harness 与运维能力：[[projects/everything-claude-code]]

## 调研边界

- 证据来源：各仓库 `README`、`CLAUDE.md`/`AGENTS.md`、目录结构、示例产出、许可证文件、本地 `git log -1`。
- 不做事项：联网核对 stars/issues/releases、不执行重量级安装、不验证完整长链路自动化。
- 比较方式：定性能力矩阵与场景建议，不给总分排名。

## 关联笔记

- [[framework/index]]
- [[summary/academic-research-agents-overview]]
- [[projects/ai-research-skills]]
- [[projects/argusbot]]
- [[projects/claude-scholar]]
- [[projects/academic-research-skills]]
