---
name: webui-collapsible-sidebar-design
description: Approved design for adding a collapsible left sidebar with Terminal as the active section and placeholder tabs for future WebUI areas.
type: project
---

# WebUI 可收起侧边栏设计

日期：2026-04-14

## 背景

当前前端只有一个极简壳层：`frontend/src/components/common/Layout.tsx` 负责顶部 header、主内容区和 footer，`frontend/src/App.tsx` 只有一个 `/` 路由，直接渲染当前的 terminal shell dashboard。

现在需要把这个单页壳层演进成更接近工作台的结构：左侧提供可收起的全局导航，至少暴露 `Terminal`、`Workspaces`、`Containers`、`Settings` 四个入口。其中只有 `Terminal` 需要真实可用，其余页面先以明确的占位状态存在，为后续扩展预留路由和导航骨架。

## 目标

本次实现一个桌面端稳定可用的 app shell：

1. 左侧增加可收起 sidebar。
2. 收起后保留仅图标窄栏，不隐藏导航能力。
3. `Terminal` tab 展示现有 terminal shell 内容。
4. `Workspaces`、`Containers`、`Settings` 提供统一占位页。
5. 保持当前 Tailwind/Vite 样式链路与 terminal 页面功能正常。
6. 实现完成后启动后端 ttyd 和前端，供人工完整验收。

## 非目标

- 不在本次实现中填充 Workspaces / Containers / Settings 的真实业务逻辑。
- 不做移动端 drawer 或复杂响应式导航模式。
- 不重写 terminal 页面中的健康检查和 terminal bench 数据流。
- 不引入新的状态管理库。

## 方案选择

### 方案 A（采用）：直接把 sidebar 整合进现有 Layout

在现有 `Layout` 上演进为 app shell，统一承载：
- 左侧 sidebar
- 顶部品牌区 / 全局说明
- 右侧路由内容区域

**优点：**
- 改动集中，贴合当前代码规模
- 未来新增 tab 时继续沿用同一外壳
- 不需要额外套多层 shell 组件

**缺点：**
- `Layout` 会比现在承担更多 UI 结构责任

### 方案 B：新增一层 AppShell 组件，保留当前 Layout

不采用。当前前端体量太小，这会增加不必要嵌套和文件数。

### 方案 C：只在 Dashboard 页面局部加侧栏

不采用。这样会把全局导航错误地塞进单页内部，后续新增页面时还要再拆一轮。

## 具体设计

### 1. 路由结构

`frontend/src/App.tsx` 从单路由扩成多路由结构：
- `/` 重定向或直接映射到 `/terminal`
- `/terminal`：真实 terminal 页面
- `/workspaces`：占位页
- `/containers`：占位页
- `/settings`：占位页

这样后续每个 tab 都有稳定 path，不需要再改导航语义。

### 2. Layout / Shell 结构

`frontend/src/components/common/Layout.tsx` 改造成桌面端双栏结构：
- 左栏：sidebar
- 右栏：主内容区（顶部说明 + 路由内容 + footer）

Sidebar 需要包含：
- 品牌区（展开时显示产品名与简短说明）
- 收起/展开按钮
- 4 个导航项
- 当前路由高亮态

收起后：
- 宽度缩小为 icon rail
- 隐藏文字，仅保留图标
- 仍保留 hover/active 可见反馈
- 仍可点击切换路由

### 3. 页面划分

#### Terminal 页面

复用当前 `DashboardPage` 的核心内容，作为 `Terminal` 页入口，不改已有 health query 与 terminal bench 逻辑。

可以按需要微调标题或排版以适应新的 shell，但不改变功能边界。

#### Placeholder 页面

新增一个统一占位页组件或简单占位页面，用于：
- Workspaces
- Containers
- Settings

占位页需要明确展示：
- 当前模块名
- “coming soon / placeholder” 类状态
- 一句简短说明，表明该区域未来会承载什么类型能力

这样可以在不引入未来逻辑的情况下，让导航结构完整可用。

### 4. 状态管理

Sidebar 的收起状态只在前端当前会话内维护，使用局部 React state 即可。

本次不做：
- localStorage 持久化
- URL 参数同步
- 全局 context 抽象

原因：当前需求只要求“可以收起”，不要求跨刷新记忆用户偏好。

### 5. 视觉与交互规则

- 当前激活 tab 需要有明显高亮（背景、边框或文字强调）
- Sidebar 展开/收起按钮位置固定且清晰
- `Terminal` 默认作为首个主入口
- 占位 tab 视觉上与 `Terminal` 一致，只是内容区显示 placeholder
- 保持当前整体浅色背景、白色卡片和紫色 accent 语言，不额外引入另一套视觉体系

## 错误处理与边界

- 如果切换到占位页，不应触发现有 terminal API 请求。
- Sidebar 收起不应影响路由切换能力。
- 新增结构不得破坏现有 `TerminalBenchCard` 的嵌入和显示空间。
- 若 ttyd 或后端未启动，`Terminal` 页应继续沿用当前已有的状态提示，而不是新增一套并行错误语义。

## 测试与验证计划

1. 增加/更新前端页面与路由后，执行 `npm run lint`。
2. 执行 `npm run build`。
3. 启动前端，在浏览器验证：
   - sidebar 默认可见
   - 可收起为仅图标窄栏
   - `Terminal` 内容正常显示
   - `Workspaces` / `Containers` / `Settings` 可切换到各自占位页
4. 启动后端 ttyd 与前端，一并留给用户做人工完整验收。

## 影响文件范围

预计会涉及：
- `frontend/src/App.tsx`
- `frontend/src/components/common/Layout.tsx`
- `frontend/src/pages/DashboardPage.tsx`（或重命名为更贴近 Terminal 的页面）
- 新增 1~2 个占位页 / 导航相关组件文件

总体原则：保持文件职责清晰，避免为了 4 个 tab 过早引入复杂抽象。
