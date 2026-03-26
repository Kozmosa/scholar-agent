---
aliases:
  - AI-Native Research Framework 索引
tags:
  - research-agent
  - framework-design
  - obsidian-note
  - index
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# AI-Native Research Framework 索引

> [!abstract]
> 这一组笔记把现有参考项目抽象成我们自己的 AI-Native Research Framework——一个有界自治研究系统，支持两种核心操作模式：调研发现（Mode 1）和深度复现（Mode 2）。V1 在隔离容器上自主运行，人在纳入和计划阶段定义合同边界。

## 阅读方式

- 先读 [[framework/ai-native-research-framework]]，确认框架定位、设计原则和边界。
- 再读 [[framework/artifact-graph-architecture]]，理解工件图谱、分层结构和 adapter 设计。
- 如果要了解容器执行环境和工作区约定，读 [[framework/container-workspace-protocol]]。
- 如果要落近期版本，接着读 [[framework/v1-dual-mode-research-engine]]。
- 如果要看实现规格（API、组件、状态机），读 [[framework/v1-rfc]]。
- 如果要看分阶段实现计划和里程碑，读 [[framework/v1-roadmap]]。
- 如果要看 agent 能力基座与角色分工，读 [[framework/agent-capability-base]]、[[framework/vsa-rfc]] 和 [[framework/pia-rfc]]。
- 如果要看基于 Gradio 的项目工作台设计，读 [[framework/webui-v1-rfc]] 和 [[framework/webui-v1-roadmap]]。
- 如果要追溯设计来源，最后读 [[framework/reference-mapping]] 和各项目研究报告。

## 内容索引

- [[framework/ai-native-research-framework]]
- [[framework/artifact-graph-architecture]]
- [[framework/container-workspace-protocol]]
- [[framework/v1-dual-mode-research-engine]]
- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[framework/agent-capability-base]]
- [[framework/vsa-rfc]]
- [[framework/pia-rfc]]
- [[framework/webui-v1-rfc]]
- [[framework/webui-v1-roadmap]]
- [[framework/reference-mapping]]

## 能力入口

- 框架愿景与系统边界：[[framework/ai-native-research-framework]]
- 工件模型、状态转换和宿主适配：[[framework/artifact-graph-architecture]]
- 容器工作区结构、同步协议与资源跟踪：[[framework/container-workspace-protocol]]
- 双模式 V1 的工作流、人工关卡与终止合同：[[framework/v1-dual-mode-research-engine]]
- V1 实现规格（API、组件、状态机）：[[framework/v1-rfc]]
- V1 分阶段实现路线图：[[framework/v1-roadmap]]
- Agent 能力基座总纲与三层角色分工：[[framework/agent-capability-base]]
- 容器内研究员预设 VSA：[[framework/vsa-rfc]]
- 面向用户的 PI 角色 PIA：[[framework/pia-rfc]]
- WebUI-v1 的项目工作台规格与路线图：[[framework/webui-v1-rfc]]、[[framework/webui-v1-roadmap]]
- 参考项目如何被吸收到框架中：[[framework/reference-mapping]]

## 使用说明

- 这组笔记是"自有框架蓝图"，不是对某一个开源仓库的复述；涉及参考项目的判断，均来自本仓库已有研究报告与静态证据。
- 现阶段默认研究对象是 AI/ML research，不试图抽象到所有学术门类；写作模块只保留下游接口，不在 V1 文档里展开。

## 关联笔记

- [[index]]
- [[summary/academic-research-agents-overview]]
- [[projects/ai-research-skills]]
- [[projects/auto-claude-code-research-in-sleep]]
