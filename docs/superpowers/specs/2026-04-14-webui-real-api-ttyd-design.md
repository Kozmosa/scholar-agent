---
name: webui-real-api-ttyd-design
description: Approved design for switching the WebUI to real API mode by default and enabling ttyd end-to-end validation through explicit API key forwarding.
type: project
---

# WebUI 真实 API + ttyd 全链路设计

日期：2026-04-14

## 背景

当前 WebUI 在开发模式下默认启用 mock：`frontend/src/api/endpoints.ts` 使用 `import.meta.env.DEV` 直接决定 `Health` 与 `TerminalSession` 请求是否走 mock。结果是在 `npm run dev` 时，Terminal 页并没有调用真实后端，而是从 `frontend/src/api/mock.ts` 返回一个写死的 `terminal_url`（例如 `http://127.0.0.1:7681`）。

因此即便后端 API 实际已经启动，前端 iframe 仍然可能指向并不存在的 ttyd 地址，表现为 connection refused 或空白页。

同时，后端真实 API 还要求 `X-API-Key`。只把前端切回真实 `/api` 还不够，必须同时把 API key 带到请求头，否则真实请求会落到 401 Unauthorized。

## 目标

本次修改要让 WebUI 能在 dev 模式下默认验证真实后端链路：

1. `npm run dev` 默认走真实 `/api`。
2. mock 仍然保留，但只在显式环境变量开启时使用。
3. 前端真实请求统一自动带上 `X-API-Key`。
4. Terminal 页通过真实 `POST /terminal/session` 获取真实 ttyd URL。
5. 页面 iframe 使用后端返回的真实地址，完成 ttyd-webui 全链路验证。

## 非目标

- 不新增完整的设置页表单让用户在浏览器里输入 API key。
- 不修改后端 API 的鉴权模型。
- 不删除现有 mock 代码。
- 不重做 terminal session 后端逻辑。

## 方案选择

### 方案 A（采用）：默认真实 API，mock 仅由显式环境变量开启

实现方式：
- 将 `frontend/src/api/endpoints.ts` 的 mock 开关改为 `import.meta.env.VITE_USE_MOCK === 'true'`
- 将 `frontend/src/api/client.ts` 增加统一请求头注入逻辑，从显式前端环境变量中读取 API key 并写入 `X-API-Key`

**优点：**
- 最符合当前“要验证真实 ttyd 全链路”的目标
- dev 环境不再暗中回退到 mock
- 保留 mock 作为未来纯前端调试工具

**缺点：**
- 本地运行前需要明确提供前端环境变量中的 API key

### 方案 B：只让 Terminal / Health 特例走真实 API

不采用。这样会让同一个 WebUI 同时存在两套数据源策略，后续更难理解和维护。

### 方案 C：彻底删除 mock

不采用。mock 仍然有保留价值，只是当前默认行为不适合全链路验收。

## 具体设计

### 1. API 数据源开关

`frontend/src/api/endpoints.ts` 中：
- 将 `USE_MOCK` 的定义从 `import.meta.env.DEV` 改为显式布尔开关
- 推荐表达方式：

```ts
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true';
```

这样只有在前端启动时显式设置 `VITE_USE_MOCK=true` 才会启用 mock。

### 2. API key 注入

`frontend/src/api/client.ts` 中：
- 增加从前端环境变量读取 API key 的逻辑
- 当存在 key 时，统一向请求头加入：

```http
X-API-Key: <value>
```

推荐使用前端显式环境变量，例如：
- `VITE_AINRF_API_KEY`

这样改动集中在请求层，不需要在每个 endpoint 单独重复处理。

### 3. 运行方式

前端 dev server 启动时：
- 默认不设置 `VITE_USE_MOCK`，因此走真实 API
- 同时设置 `VITE_AINRF_API_KEY=<your-key>` 以便通过后端鉴权

后端按既有方式运行即可，只要该 key 与 onboarding 保存的 hash 对应。

### 4. Terminal 全链路数据流

修复后的真实链路应为：

1. WebUI 打开 Terminal 页
2. `GET /api/health` 走真实后端
3. 点击 Start terminal
4. `POST /api/terminal/session` 携带 `X-API-Key`
5. 后端创建真实 ttyd session
6. 后端返回真实 `terminal_url`
7. iframe 加载该真实 ttyd URL

### 5. 错误处理与边界

- 若未设置 `VITE_AINRF_API_KEY`，前端请求将会 401；本次不把它伪装成 mock 成功。
- 若 ttyd 进程未正常启动，Terminal 页应显示真实后端返回的 detail / 错误，而不是 mock 地址。
- 若用户显式设置 `VITE_USE_MOCK=true`，则继续沿用现有 mock 行为。

## 测试与验证计划

1. 修改后执行 `cd frontend && npm run lint`。
2. 执行 `cd frontend && npm run build`。
3. 使用真实前端环境变量启动 dev server：
   - 不设置 `VITE_USE_MOCK`
   - 设置 `VITE_AINRF_API_KEY`
4. 打开 Terminal 页并验证：
   - health 请求命中真实后端
   - Start terminal 调用真实 `POST /terminal/session`
   - iframe 不再固定跳转 mock 的 `127.0.0.1:7681`
   - ttyd 页面成功加载

## 影响文件范围

预计会涉及：
- `frontend/src/api/endpoints.ts`
- `frontend/src/api/client.ts`
- 可能补充一处运行说明或 worklog 记录

总体原则：只修改真实链路必需部分，不把本次验收问题扩展成新的配置系统工程。
