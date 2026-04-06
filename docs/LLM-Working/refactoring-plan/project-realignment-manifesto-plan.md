---
aliases:
  - Project Realignment Manifesto Plan
  - 项目重定位与 manifesto 规划
tags:
  - scholar-agent
  - manifesto
  - requirements
  - expectations
  - implementation-plan
source_repo: scholar-agent
source_path: /Users/kozmosa/code/scholar-agent
last_local_commit: workspace aggregate
---
# 项目重定位与 Manifesto 规划

> [!abstract]
> 本规划用于把 `scholar-agent` 从“泛化的全自动科研叙事”收敛为“单用户优先、agent-driven、evidence-grounded 的 research dashboard”。目标不是一次性写完所有新文档，而是先固定新的项目定位、文档职责边界、版本治理规则，以及 next release 需要遵守的 requirements / expectations 基线。

## 规划结论

- 项目定位从“有界自治研究系统”进一步收敛为“单用户优先的 agent-driven research dashboard”，强调 dashboard、稳定性和可观察性，而不是跨领域通用自动研究员。
- `manifesto` 应成为 requirements / expectations 的最高层文档，优先负责项目定位、适用边界、Non-Goals、ready-for-use 标准和 release 哲学。
- `framework` 文档保持抽象层职责：解释项目功能、哲学、边界、为什么有用，以及 Mode 1 / Mode 2 的基线含义；不再直接把未来态实现承诺写成当前版本要求。
- `architecture` 文档与实际实现强绑定，专门记录 next release 的工程边界、组件关系、接口契约和关键 tradeoff。
- 版本管理采用混合风格，例如 `v1-20260404`；当前阶段文档版本与产品 release 版本弱绑定，每次 release 后归档 snapshot 与 decision log。

## 项目重新定位

### 一句话定位

- `scholar-agent` 不是一个跨所有领域、全天候、完全自主的通用研究员，而是一个面向单用户研究工作的、agent-driven 的 research dashboard。

### 面向用户的定义

- 核心用户是当前维护者本人，而不是团队协作或公共 SaaS 用户。
- 系统的首要价值是把典型、简单、定义明确的研究支持任务稳定地跑起来，并把进度、关卡、工件和资源使用情况放到统一 dashboard 中可见。
- 24x7 agent / subagent 可以作为具体工作流中的局部能力存在，但不再作为项目总叙事或总承诺。

### 当前必须弱化的叙事

- 跨所有领域的通用研究自动化。
- “general AI-driven fully autonomous 24x7 researcher” 式承诺。
- 用完整论文工厂、开放式自治探索或全自动写作来定义项目成功。

### 当前必须强化的叙事

- evidence-grounded workflow。
- robustness as a system。
- stability and ready-for-use。
- a simple but genuinely helpful tool rather than a fancy toy。

## Next Release 的最低判断标准

### Ready-for-use 的最低定义

- 能独立完成典型、简单、定义明确的任务。
- 失败和状态损坏不能过于频繁。
- 用户能从 dashboard 直接看到当前任务进度、最近完成任务、最近工件和基础资源状态。
- 系统输出要以可追溯工件为中心，而不是只留在一次会话或日志里。

### 单用户优先

- next release 默认按单用户、本地或单机控制面设计，不提前引入多用户协作和多租户权限模型。
- dashboard 首先服务 operator，而不是服务审美化展示或团队运营分析。

## Mode 1 / Mode 2 Baseline 重定义

### 为什么必须重定义

- 当前 `[[framework/v1-dual-mode-research-engine]]` 中的 Mode 1 / Mode 2 描述更接近蓝图和未来态承诺，不适合作为 next release 的直接 requirement。
- next release 必须把两种模式降到可交付 baseline，否则 roadmap 会再次失控。

### Mode 1 Baseline

- 建议定义为“bounded discovery baseline”，即围绕种子论文或主题描述启动一次有边界的探索任务。
- 默认参考 `[[projects/auto-claude-code-research-in-sleep]]` 的 skill / prompt 组织方式，但在本项目中只吸收其 research pipeline baseline，不继承“过夜全自动科研”叙事。
- 最小可交付重点是：任务可启动、里程碑可观察、工件可沉淀、探索边界可终止。
- 更具体的 baseline 约束以后续 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。

### Mode 2 Baseline

- 建议定义为“bounded reproduction baseline”，即围绕目标论文、目标表格或明确任务发起一次可观察的实现 / 复现任务。
- 最小可交付重点是：任务过程可跟踪、结果工件可预览、失败可归档，而不是承诺稳定达到完整高精度复现。
- 更具体的 baseline 约束以后续 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。

## 文档体系建议

### 文档职责分层

- `manifesto`：最高层 requirements / expectations / Non-Goals / release philosophy。
- `framework`：抽象层功能、哲学、用途、模式解释和边界说明。
- `architecture`：与实现紧密绑定的工程设计和 tradeoff。
- `decision-log`：重大决策记录，按 release 冻结归档。
- `roadmap`：面向下一次 release 的原子任务与推进节奏。

### 建议引入的版本化产物

- `manifesto` snapshot。
- `architecture` snapshot。
- `decision-log` archive。
- `release-freeze` 或等价的 release snapshot 文档。

## 推荐的 Manifesto 章节结构

### 1. Positioning

- 项目是什么。
- 项目不是什么。
- 为什么当前要收缩定位。

### 2. Requirements and Expectations

- 当前主要用户。
- next release 的 ready-for-use 标准。
- 允许的局部自治与不允许的整体叙事。

### 3. Product Priorities

- engineering > product/system > academic。
- dashboard、stability、observability 作为 next release 核心。

### 4. Non-Goals

- 跨领域通用研究。
- 全自动端到端研究。
- 论文工厂式写作主叙事。
- 其余明确延期项目。

### 5. Release Philosophy

- 通过持续开发收敛项目本质，而不是长期空转设计。
- 每次 release 后冻结 snapshot 和 decision log。
- 采用单会话可完成的原子任务推进。

## 版本策略建议

### 当前阶段

- 版本风格采用混合命名：`v1-YYYYMMDD`。
- 在项目离开快速变化阶段前，不引入严格语义化版本作为主要命名方式。

### 文档与产品版本关系

- 弱绑定。
- `manifesto` / `framework` / `architecture` 可以共享同一套版本规则，但不要求每次完全同步升版。

### Release 后的治理

- 冻结并归档 decision log。
- 冻结并归档该 release 的 manifesto / architecture snapshot。
- 新周期从新的空白 decision log 文档开始。

## 建议的单会话原子任务序列

1. 固定项目新定位与一句话声明。
2. 固定 next release 的 ready-for-use 标准。
3. 固定 Non-Goals。
4. 重写 Mode 1 baseline。
5. 重写 Mode 2 baseline。
6. 固定 dashboard 首屏信息架构。
7. 固定 artifact preview 和资源展示边界。
8. 固定 workspace / session / container 关系。
9. 固定版本与 freeze/archive 规则。
10. 把上述决策映射回新版 manifesto / framework / architecture / roadmap。

## 本规划对应的后续文档

- 需要新增或重写 manifesto 主文档。
- 需要新增 next release roadmap 文档，专门承载 must-have / deferred / atomic tasks。
- 需要后续补一份 architecture baseline 文档，把 dashboard、task tracking、workspace management、SSH integration 和 artifact preview 的实现边界讲清。

## 关联笔记

- [[framework/index]]
- [[framework/ai-native-research-framework]]
- [[framework/v1-dual-mode-research-engine]]
- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[LLM-Working/refactoring-plan/mode-baseline-spec]]
- [[projects/auto-claude-code-research-in-sleep]]
