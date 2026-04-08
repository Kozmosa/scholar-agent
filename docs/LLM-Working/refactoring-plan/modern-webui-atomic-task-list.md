---
aliases:
  - Modern WebUI Atomic Task List
  - WebUI 原子任务列表
tags:
  - scholar-agent
  - webui
  - dashboard
  - implementation-plan
  - atomic-tasks
source_repo: scholar-agent
created_at: 2026-04-07
---

# Modern WebUI 构建原子任务列表

> [!abstract]
> 本文档将 next release 的 Modern WebUI Dashboard 拆解为可单会话完成的原子任务。基于 [[LLM-Working/refactoring-plan/dashboard-baseline-spec]] 和 [[LLM-Working/refactoring-plan/architecture-baseline-plan]] 定义的范围。

## 前置条件

- Backend API 契约已定义（task read model、workspace/session/container summary、artifact preview）
- Frontend 技术栈已选定

## Phase 1: 项目初始化与基础设施

### 1.1 Frontend 项目初始化
- 任务：创建 frontend 项目骨架
- 输入：技术栈决策（React/Vue/Svelte + 构建工具）
- 输出：可运行的基础项目，包含路由框架、目录结构、基础配置
- 验证：`npm run dev` 或等效命令能启动开发服务器

### 1.2 Backend-Frontend 契约对齐
- 任务：确认 API endpoint 与 read model 契约
- 输入：task-read-model-contract、artifact-preview-contract、workspace-session-container-summary-contract
- 输出：OpenAPI/Swagger spec 或等效契约文档
- 验证：契约文档与后端实际实现一致

### 1.3 API Client 基础层
- 任务：实现 frontend API client 基础封装
- 输入：契约文档
- 输出：带类型标注的 API client，支持错误处理
- 验证：能成功调用后端 health endpoint

## Phase 2: 首页核心区块

### 2.1 系统健康状态条
- 任务：实现顶部系统健康状态组件
- 输入：health API endpoint
- 输出：HealthStatusBar 组件，展示 API状态、SSH可用性、环境状态
- 验证：组件能实时反映后端健康状态

### 2.2 当前运行任务 Timeline
- 任务：实现 RunningTaskTimeline 组件
- 输入：running task API + checkpoint/milestone 数据
- 输出：Timeline 组件，高亮当前checkpoint、区分完成/失败节点
- 验证：能展示任务的阶段进度和最近事件

### 2.3 最近完成任务列表
- 任务：实现 RecentFinishedTasks 组件
- 输入：recent tasks API
- 输出：列表组件，展示 mode、终态、结束时间、结果摘要入口
- 验证：点击能跳转到任务详情

### 2.4 最近 Artifacts 区块
- 任务：实现 RecentArtifacts 组件
- 输入：recent artifacts API
- 输出：Artifact 入口组件，点击触发 modal preview
- 验证：能正确区分 table/report/figure 类型

### 2.5 Workspace 资源快照
- 任务：实现 ResourceSnapshot 组件
- 输入：resource snapshot API
- 输出：GPU/CPU/Memory/Disk 快照展示
- 验证：数据能实时反映当前资源状态

### 2.6 首页组合布局
- 任务：组合所有首页区块为完整首页
- 输入：各区块组件
- 输出：DashboardHomePage 组件
- 验证：首页信息架构符合 dashboard-baseline-spec

## Phase 3: 任务详情页

### 3.1 Task Summary 区块
- 任务：实现 TaskSummary 组件
- 输入：task read model identity + lifecycle + input_summary
- 输出：展示 task_id、mode、时间、状态、输入摘要
- 验证：信息完整、布局清晰

### 3.2 Timeline/Checkpoints 详情
- 任务：实现 TaskTimeline 组件（详情页版本）
- 输入：progress_summary milestones
- 输出：完整时间线，带节点状态视觉区分
- 验证：当前节点高亮、历史节点可点击

### 3.3 Artifact Preview Modal
- 任务：实现 ArtifactPreviewModal 组件
- 输入：artifact preview contract
- 输出：Modal 组件，支持 CSV/MD table、Markdown report、SVG/PNG figure 渲染
- 验证：三种类型都能正确预览

### 3.4 Workspace/Session Context 区块
- 任务：实现 ExecutionContext 组件
- 输入：workspace/session/container summary
- 输出：展示 workspace 标识、session 状态、container 健康摘要
- 验证：状态信息与后端一致

### 3.5 Termination/Error Summary 区块
- 任务：实现 TerminationSummary 组件
- 输入：result_summary termination_reason + error_summary
- 输出：展示完成/失败/取消/阻塞原因
- 验证：终态任务能清晰展示结束原因

### 3.6 任务详情页组合
- 任务：组合所有详情区块为完整任务详情页
- 输入：各详情区块组件
- 输出：TaskDetailPage 组件
- 验证：页面能回答 5 个关键问题（是什么、在哪、经历过什么、产出什么、为什么结束）

## Phase 4: 交互与导航

### 4.1 任务列表导航
- 任务：实现 TaskListNavigation 组件
- 输入：task list API
- 输出：可筛选、可排序的任务列表视图
- 验证：支持按 mode、status、时间筛选

### 4.2 路由与状态管理
- 任务：实现前端路由和全局状态管理
- 输入：页面组件结构
- 输出：路由配置、状态 store（running task polling、health polling）
- 验证：页面切换流畅、状态同步正确

### 4.3 基础错误处理与加载状态
- 任务：实现统一的错误处理和加载状态 UI
- 输入：API error schema
- 输出：ErrorBoundary、LoadingSpinner、Toast 通知
- 验证：API 失败时用户能收到明确反馈

## Phase 5: 集成与验证

### 5.1 Backend-Frontend 集成测试
- 任务：端到端验证 dashboard 与后端集成
- 输入：完整 dashboard + backend API
- 输出：集成测试报告
- 验证：首页和详情页数据都能正确加载

### 5.2 响应式布局适配
- 任务：确保 dashboard 在常见屏幕尺寸可用
- 输入：各组件
- 输出：响应式布局调整
- 验证：在桌面和宽屏下布局合理

### 5.3 基础性能优化
- 任务：优化首页加载和 polling 性能
- 输入：当前实现
- 输出：合理的 polling interval、懒加载策略
- 验证：首页刷新不阻塞交互

## Deferred（本期不实现）

- Token Usage Overview（仅当 telemetry 能稳定提供时纳入）
- Artifact Graph 可视化
- 多用户协作视图
- 全局运营分析 dashboard
- 图形化任务编排器
- 长期知识图谱浏览器
- PDF 复杂文档 viewer
- 交互式图表分析器

## 建议执行顺序

```
Phase 1 (基础设施) → Phase 2 (首页区块) → Phase 3 (详情页) → Phase 4 (交互导航) → Phase 5 (集成验证)
```

建议 Phase 2 和 Phase 3 可并行推进，各自区块组件独立开发。

## 关联笔记

- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]
- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]
- [[LLM-Working/refactoring-plan/task-read-model-contract]]
- [[LLM-Working/refactoring-plan/artifact-preview-contract]]
- [[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]