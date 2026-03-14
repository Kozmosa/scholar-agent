---
aliases:
  - 学术研究 Agent 汇总研究报告
tags:
  - research-agent
  - repo-study
  - summary
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# 学术研究 Agent 汇总研究报告

> [!abstract]
> 本汇总报告基于 7 个本地仓库的静态调研，目标不是给出唯一冠军，而是建立一张“能力地图”：哪些仓库更像技能库，哪些更像流水线，哪些更像工作台，哪些只是终稿质检协议。

## 总览结论

- 如果要找“研究工程能力底座”，优先看 [[projects/ai-research-skills]]。
- 如果要找“过夜自治研究流水线”，优先看 [[projects/auto-claude-code-research-in-sleep]]。
- 如果要找“深度研究报告系统”，优先看 [[projects/claude-code-deep-research]]。
- 如果要找“研究到投稿的严肃管线”，优先看 [[projects/academic-research-skills]]。
- 如果要找“论文投稿前终稿质检”，优先看 [[projects/awesome-claudecode-paper-proofreading]]。
- 如果要找“长期个人研究工作台”，优先看 [[projects/claude-scholar]]。
- 如果要找“通用 harness 基线”，优先看 [[projects/everything-claude-code]]。

## 项目关系图

```mermaid
graph TD
    A[AI Research SKILLs<br/>技能库]
    B[ARIS<br/>自治科研流水线]
    C[Claude Code Deep Research<br/>深度研究报告]
    D[Academic Research Skills<br/>学术全流程]
    E[Paper Proofreading<br/>终稿质检]
    F[Claude Scholar<br/>个人工作台]
    G[Everything Claude Code<br/>通用 Harness]

    A --> B
    A --> F
    G --> F
    C --> D
    B --> D
    D --> E
    F --> D
    G --> A
```

## 能力矩阵

| 项目 | 主要形态 | 研究前期 | 实验/执行 | 写作/投稿 | 引文/质控 | 宿主范围 | 适合谁 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [[projects/ai-research-skills]] | 技能库 | 强 | 强 | 中 | 中 | 多宿主 | 想增强现有 agent 的团队 |
| [[projects/auto-claude-code-research-in-sleep]] | 自治流水线 | 强 | 强 | 强 | 强 | 以 Claude + 外部 reviewer 为主 | 想把研究循环过夜跑起来的人 |
| [[projects/claude-code-deep-research]] | 深度研究框架 | 强 | 中 | 弱 | 强 | Claude Code | 想快速得到 citation-backed 报告的人 |
| [[projects/academic-research-skills]] | 学术全流程管线 | 强 | 中 | 强 | 很强 | Claude Code | 追求严肃投稿流程的人 |
| [[projects/awesome-claudecode-paper-proofreading]] | Prompt 协议 | 弱 | 弱 | 中 | 很强 | Claude Code | 论文终稿质检需求 |
| [[projects/claude-scholar]] | 个人工作台 | 强 | 强 | 强 | 中 | Claude/Codex/OpenCode | 长期个人研究与开发用户 |
| [[projects/everything-claude-code]] | 通用 harness | 中 | 强 | 弱 | 强 | 多宿主 | 要先搭平台再接研究能力的团队 |

## 选型决策图

```mermaid
flowchart TD
    A[你的首要目标是什么?]
    A --> B{先搭能力底座?}
    B -->|是| C[[projects/ai-research-skills]]
    B -->|否| D{要不要通用 Harness?}
    D -->|要| E[[projects/everything-claude-code]]
    D -->|不要| F{目标是完整科研流水线?}
    F -->|是, 且重自治| G[[projects/auto-claude-code-research-in-sleep]]
    F -->|是, 且重严谨投稿| H[[projects/academic-research-skills]]
    F -->|否| I{只要深度研究报告?}
    I -->|是| J[[projects/claude-code-deep-research]]
    I -->|否| K{只想精修论文终稿?}
    K -->|是| L[[projects/awesome-claudecode-paper-proofreading]]
    K -->|否| M[[projects/claude-scholar]]
```

## 定性对比与建议

### 1. 技能库 vs 流水线

- [[projects/ai-research-skills]] 和 [[projects/everything-claude-code]] 更像平台层资产。
- [[projects/auto-claude-code-research-in-sleep]]、[[projects/claude-code-deep-research]]、[[projects/academic-research-skills]] 更像可执行的研究流程。
- [[projects/claude-scholar]] 介于两者之间，它不是平台 SDK，也不是固定流水线，而是长期工作台。

### 2. 研究严谨度

- [[projects/academic-research-skills]] 在 integrity、review、revision 和 final verification 上最重。
- [[projects/claude-code-deep-research]] 在 citation-backed synthesis 上最专注。
- [[projects/awesome-claudecode-paper-proofreading]] 在终稿层的人工可控质检上最干净。

### 3. 自治与执行

- [[projects/auto-claude-code-research-in-sleep]] 最强调自治回路、跨模型 reviewer 和实验执行。
- [[projects/claude-scholar]] 更适合研究者长期手动-半自动混合使用。
- [[projects/everything-claude-code]] 提供的是自治运行底座，而不是学术流程本身。

### 4. 推荐场景

- 想给现有 agent 补研究工程能力：选 [[projects/ai-research-skills]]。
- 想直接搭“研究会自己跑一晚”的系统：选 [[projects/auto-claude-code-research-in-sleep]]。
- 想快速产出高质量研究报告：选 [[projects/claude-code-deep-research]]。
- 想要最接近正式投稿工艺的管线：选 [[projects/academic-research-skills]]。
- 想做长期的个人研究/开发环境：选 [[projects/claude-scholar]]。
- 想在团队里统一 agent 基础设施：先看 [[projects/everything-claude-code]]，再补 [[projects/ai-research-skills]]。
- 想对现有论文做严格终稿检查：选 [[projects/awesome-claudecode-paper-proofreading]]。

## 关键空白带

- 没有任何一个仓库同时在“研究工程广度、实验自治、严肃投稿、通用 harness”四个维度都做到最强。
- 多数仓库依赖 Claude Code 或相关 agent 生态，真正完全宿主无关的只有技能资产层更接近。
- 静态仓库信号强，不等于真实运行成功率强；尤其是长链路项目，实际质量仍受模型、权限、远程环境和数据条件影响。

## 关联笔记

- [[index]]
- [[projects/ai-research-skills]]
- [[projects/auto-claude-code-research-in-sleep]]
- [[projects/claude-code-deep-research]]
- [[projects/academic-research-skills]]
- [[projects/awesome-claudecode-paper-proofreading]]
- [[projects/claude-scholar]]
- [[projects/everything-claude-code]]
