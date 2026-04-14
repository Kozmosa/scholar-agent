---
name: webui-style-loading-fix-design
description: Approved design for restoring Tailwind style loading in the WebUI and verifying the fix before visual polish.
type: project
---

# WebUI 样式加载修复设计

日期：2026-04-14

## 背景

当前 WebUI 页面结构已经大量依赖 Tailwind utility class，例如 `frontend/src/pages/DashboardPage.tsx` 与多个公共组件都使用了 `className="..."` 的 Tailwind 原子类。

但当前前端入口只在 `frontend/src/index.css` 中使用了 Tailwind v4 风格的：

```css
@import "tailwindcss";
```

与此同时，`frontend/vite.config.ts` 仅注册了 React 插件，没有注册 Tailwind v4 官方要求的 `@tailwindcss/vite` 插件。实际构建日志已经出现 `@theme` / `@tailwind` unknown at rule 的证据，说明 Tailwind 指令没有被正确编译，导致页面样式表现接近“完全未加载”。

## 目标

本次仅解决样式加载链路故障，并在样式恢复后再进行 UI 细节检查。

成功标准：

1. WebUI 的 Tailwind utility class 被正确编译进前端构建产物。
2. 页面恢复基础布局、颜色、间距、边框和排版样式。
3. 修复方案是最小改动，不顺带重写现有 UI。
4. 修复后保留一次可复现的回归验证，避免以后再次出现“页面无样式但构建仍成功”的情况。

## 方案选择

### 方案 A（采用）：补上 Tailwind v4 的 Vite 官方插件

- 在前端依赖中增加 `@tailwindcss/vite`
- 在 `frontend/vite.config.ts` 中注册该插件
- 保留现有 React 插件、代理和 host/port 配置
- 增加最小回归验证，确认构建产物中确实包含 Tailwind 生成的 utility class 对应 CSS

**优点：**
- 与当前 `@import "tailwindcss";` 的用法一致
- 改动范围最小
- 符合 Tailwind v4 + Vite 的官方集成方式

**缺点：**
- 需要新增一个前端依赖

### 方案 B：改回传统 PostCSS / Tailwind 配置

不采用。原因是当前代码已经按 Tailwind v4 的 CSS import 方式组织，回退方案会扩大修改面，且不如官方 Vite 插件直接。

### 方案 C：去掉 Tailwind，改写为手写 CSS

不采用。原因是这会把“修复样式链路”膨胀成“重写 UI 样式体系”，明显超出本次范围。

## 具体设计

### 1. 依赖与构建链路

在 `frontend/package.json` 中补充 `@tailwindcss/vite` 依赖，并更新 lockfile。

在 `frontend/vite.config.ts` 中：
- 引入 `@tailwindcss/vite`
- 将其加入 `plugins` 数组
- 保留现有 `react()`、`server.proxy`、`server.host`、`server.port`、`preview.host`、`preview.port`

### 2. 回归验证

增加一个最小化前端回归测试或构建检查，验证目标不是“构建成功”，而是“Tailwind 样式真实生效”。

建议验证方式：
- 运行前端生产构建
- 读取生成后的 CSS 产物
- 断言其中包含当前页面实际使用到的 utility class 所生成的规则片段，例如 `px-4`、`text-gray-900`、`rounded-xl` 等对应的编译结果中的稳定片段

这样可以覆盖以下回归场景：
- 忘记配置 Tailwind Vite 插件
- Tailwind 编译链失效但构建未硬失败
- CSS 入口仍被打包，但 utility class 未被展开

### 3. UI 复查

在样式链路修复并通过回归验证后：
- 启动前端页面
- 人工检查主页面是否恢复基础视觉层级
- 再决定是否需要单独处理视觉细节问题

这一步只做检查，不预先承诺额外改动。

## 错误处理与边界

- 不修改现有页面结构和组件职责
- 不引入与本问题无关的样式重构
- 如果回归验证发现构建链路修复后仍有样式异常，再进入下一轮根因排查，而不是一次性叠加多个猜测性修复

## 测试与验证计划

1. 先创建失败的回归验证，证明当前配置下 Tailwind utility 没有正确落入构建产物
2. 引入 `@tailwindcss/vite` 并更新 Vite 配置
3. 重新运行回归验证，确认变绿
4. 启动 WebUI，在浏览器中验证页面样式恢复
5. 补充当日 worklog，记录本批次改动与验证结果

## 非目标

- 不在本次修改中重设计 Dashboard 布局
- 不在本次修改中替换组件库或样式方案
- 不在本次修改中处理所有视觉 polish 问题
