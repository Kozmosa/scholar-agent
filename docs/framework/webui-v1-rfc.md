---
aliases:
  - AINRF WebUI V1 RFC
  - WebUI-v1 实现规格
tags:
  - research-agent
  - framework-design
  - webui
  - gradio
  - rfc
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# AINRF WebUI-v1 RFC：基于 Gradio 的项目工作台

> [!abstract]
> WebUI-v1 为 AINRF 提供一个 API-first 的项目工作台：以 `Project` 组织工作空间，以 `Run` 驱动单次任务，在已有 FastAPI、Human Gate 和 SSE 事件流之上提供可视化配置、审批与观察面。由于 P8/P9 尚未落地真实执行链路，Mode 1 / Mode 2 在 v1 中以可交互 mock 形式呈现。

## Problem Statement & Positioning

当前仓库已经具备 P4-P6 的服务骨架：任务创建、审批接口、状态持久化、事件流和健康检查都已存在，但仍缺少一个面向人类操作者的统一工作台。直接使用 API 或未来 CLI 客户端有三个缺口：

- 配置面分散：容器、预算、论文输入、webhook、审批状态分散在 task payload 和多个读接口中。
- 项目视角缺失：后端当前只有 task，没有一个把同一研究主题下多次运行组织起来的工作空间视图。
- P8/P9 体验无法前置：深度复现与文献探索还未实现，导致前端无法先行固化交互流程。

因此 WebUI-v1 的定位不是“新的核心编排层”，而是“已有 orchestrator 的可视化控制台”。

## Scope & Non-Goals

### In Scope

- 基于 Gradio 的独立 WebUI 入口，优先复用现有 FastAPI 契约。
- `Project List`、`Project Detail`、`Run Detail` 三个核心页面。
- 覆盖 P1-P7 的关键配置项，并拆分为 Project 默认配置与 Run 一次性参数。
- Mode 1 / Mode 2 的可交互 mock 流程：可发起、可观察阶段推进、可查看占位工件、可走审批入口。
- 事件流与 gate 审批的可视化。

### Non-Goals

- WebUI-v1 不引入后端一等 `Project` 资源；`Project` 仅是 UI 组织层。
- WebUI-v1 不补做 P8/P9 的真实 agent 执行、实验编排或论文解析逻辑。
- WebUI-v1 不替代 API；它是 API client，不是第二套业务后端。
- WebUI-v1 不在 v1 中追求复杂多用户权限、细粒度 RBAC 或协作编辑。

## Core Product Model

### Project

`Project` 是 WebUI 内部视图模型，不是后端持久化对象。它表示“一组围绕同一研究主题的 runs/task 集合”，并持有默认配置：

- `project_name` / `project_slug`
- `description`
- 默认容器连接信息
- 默认预算上限
- 默认 webhook 与 yolo 策略
- 默认 mode 参数模板
- 历史 runs 摘要与最近活动状态

推论：WebUI 需要自己的轻量 Project 配置存储或本地配置文件，但不要求 FastAPI 新增 `/projects/*` 资源。

### Run

`Run` 对应一次具体的 task 提交。WebUI 的 run 创建表单最终映射到现有 `POST /tasks` body，并额外记录其所属 `project_slug` 供 UI 聚合。

## Architecture

### Runtime shape

WebUI-v1 采用 `Gradio + API client`：

- Gradio 负责页面布局、表单状态、交互回调和 mock 视图。
- API client 负责调用 `POST /tasks`、`GET /tasks`、`GET /tasks/{id}`、`POST /tasks/{id}/approve`、`POST /tasks/{id}/reject`、`GET /tasks/{id}/events`、`GET /health`。
- 对尚未落地的 P7-P9 能力，WebUI 通过 mock adapter 生成占位阶段、假 artifacts 和示例事件，不伪装成真实执行结果。

### Layer boundary

- FastAPI 仍是 source of truth：真实任务状态、gate 状态、artifact 摘要、SSE 事件都以现有后端为准。
- WebUI 的 `Project` 只管理视图编排与默认值，不写回核心领域模型。
- 若未来需要升级为一等 Project 资源，WebUI-v1 的 Project 字段命名应尽量贴近潜在后端 schema，减少迁移成本。

## Information Architecture

### Project List

- 展示全部 projects、最近运行状态、待审批数量、容器健康摘要。
- 支持创建新 project、进入项目详情、查看最近失败或等待中的 run。

### Project Detail

- 展示 project 默认配置。
- 展示该 project 下的 runs 列表及状态筛选。
- 提供 “New Mode 1 Run” 与 “New Mode 2 Run” 两个入口。
- 汇总待审批 gate、最近事件和最近 artifacts。

### Run Detail

- 展示 task 当前阶段、预算、相关 artifacts、gate 记录和事件时间线。
- 提供 approve / reject 操作。
- 对 Mode 1 / Mode 2 展示专属的 mock 结果面板。
- 当真实 SSE 不可用时，允许降级到轮询，但界面结构保持一致。

## Config Layering

### Project defaults

Project 级别维护稳定、可复用的配置：

- P1：容器连接默认值，如 `host`、`port`、`user`、`ssh_key_path`、`project_dir`
- P4：API endpoint、API key 引用、服务健康检查地址
- P5：`webhook_url`、默认 `yolo`、审批提醒偏好
- 通用预算模板：`gpu_hours`、`api_cost_usd`、`wall_clock_hours`

### Run overrides

Run 级别维护一次性输入和覆盖项：

- P2：论文输入来源、标题、URL/路径、解析方式提示
- P6：事件展示过滤条件与默认订阅类别
- P7：mode 选择、启动参数、执行入口
- Mode 1：`domain_context`、`max_depth`、`focus_directions`、`ignore_directions`
- Mode 2：`scope`、`target_tables`、`baseline_first`

### Mapping rule

- WebUI 表单输出必须能无损映射到当前 `TaskCreateRequest`。
- 无法映射到现有 API 的字段，只能停留在 UI 本地状态或 mock adapter 中，不能偷偷扩展真实请求体。

## P1-P7 Coverage Matrix

| 阶段 | WebUI-v1 覆盖方式 |
| --- | --- |
| P1 SSH Executor | 通过 Project 默认容器配置暴露连接参数与健康状态 |
| P2 MinerU Client | 在 Run 创建时暴露论文输入与解析前置说明；解析结果页先以占位/后端返回为准 |
| P3 Artifact / State | 在 Run Detail 中展示 artifact 摘要、状态与 task 持久化结果 |
| P4 FastAPI / Auth | 提供 API 连接配置、认证输入、健康检查与任务创建入口 |
| P5 Human Gate / Webhook | 可视化 waiting gate、approve/reject 操作与 webhook 相关配置 |
| P6 SSE Streaming | 在 Run Detail 中展示实时事件流，支持过滤与回放 |
| P7 Agent Adapter / Engine | 提供 mode 启动入口与执行页骨架；真实任务推进未完成部分由 mock adapter 承担 |

## Mode Mock Strategy

### Mode 1

Mock 面板应模拟：

- intake -> planning -> exploration -> completed/paused 的阶段切换
- 候选论文列表、探索图谱摘要、占位发现卡片
- 对“建议复现某篇论文”的占位决策提示

### Mode 2

Mock 面板应模拟：

- intake -> planning -> implementing -> baseline -> full-run -> assessment 的阶段切换
- 目标表格、基线结果、偏差分析和质量评估卡片
- 失败分支的占位说明，使 UI 能提前固化异常态

### Guardrail

- 所有 mock 数据必须清晰标记为 `mock` 或 `placeholder`。
- 一旦 P8/P9 接入真实链路，优先替换数据源，不改页面信息架构。

## Public Interfaces

### Recommended entrypoint

- 建议新增 `ainrf webui` 作为 WebUI 启动入口。
- Gradio app 模块建议位于 `src/ainrf/webui/`。

### Internal view models

WebUI-v1 需要稳定的内部类型：

- `ProjectView`
- `ProjectDefaults`
- `RunListItem`
- `RunCreateFormState`
- `RunTimelineItem`
- `MockModeSession`

这些类型是 UI 内部契约，不等同于后端 Pydantic model，但字段命名应尽量与 `TaskCreateRequest` 和 `TaskDetailResponse` 对齐。

## Risks & Open Issues

| 风险 | 影响 | 缓解策略 |
| --- | --- | --- |
| 当前后端没有 project 资源 | 项目列表需要自管聚合 | 先将 Project 限定为 UI 组织层，避免误导为正式领域对象 |
| P8/P9 未实现 | 执行页只能展示占位能力 | 明确 mock 边界，并把真实/占位数据源隔离 |
| Gradio 组件状态复杂 | 页面间共享状态容易失控 | 先收敛为三页结构和明确 view model，不在 v1 引入过深自定义前端框架 |
| SSE 或后端不可用 | 运行详情页体验断裂 | 提供轮询降级和错误状态占位 |

## Relationship To Core V1 Docs

- `[[framework/v1-rfc]]` 继续定义 orchestrator 核心与 API-first 原则。
- `[[framework/webui-v1-rfc]]` 定义“如何把这些能力组织成可操作的工作台”。
- `[[framework/webui-v1-roadmap]]` 单独管理交付切片，不改写 P0-P9 的实现顺序。

## 关联笔记

- [[framework/index]]
- [[framework/v1-rfc]]
- [[framework/v1-roadmap]]
- [[framework/v1-dual-mode-research-engine]]
- [[framework/webui-v1-roadmap]]
