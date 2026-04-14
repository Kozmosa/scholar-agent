---
name: webui-ttyd-proxy-auth-design
description: Approved design for opening real ttyd sessions in the WebUI iframe through a backend-controlled open-plus-proxy flow with single-viewer state.
type: project
---

# WebUI ttyd 代理认证设计

日期：2026-04-14

## 背景

当前真实链路已经可以走通到后端 `POST /terminal/session`：
- 前端可以调用真实 API
- `X-API-Key` 已可用于创建真实 terminal session
- 后端也确实会启动 ttyd 进程

但 iframe 仍然打不开真实终端，根因已经明确有两层：

1. 后端当前返回的是裸 ttyd 地址（例如 `http://127.0.0.1:7681`），而 ttyd 自己仍启用了认证墙。浏览器 iframe 访问该地址时，会直接遇到 ttyd 的认证而不是进入终端页面。
2. 当前 ttyd 启动方式把原始 API key 作为 `--credential` 传入 ttyd 进程参数，这会把敏感凭证暴露给本机进程参数面，属于当前链路中的安全问题。

因此，这次修复不能再继续采用“open 路由校验后直接 307 跳转到裸 ttyd”的思路；该思路无法完成认证接力，也不能消除 API key 出现在 ttyd argv 中的问题。

## 目标

本次修改要在“最小可用优先”的前提下，让 WebUI 的 Terminal iframe 可以稳定打开真实 ttyd，并满足以下要求：

1. `POST /terminal/session` 返回的是浏览器可直接消费的后端入口，而不是裸 ttyd 地址。
2. 浏览器只访问 AINRF 后端提供的受控 terminal 路径，不直接访问裸 ttyd 地址。
3. ttyd 不再通过接收原始 API key 的 `--credential` 参数来完成浏览器认证。
4. 后端通过一次性 open token 放行浏览器进入 terminal 代理层。
5. 进入后续代理链路后，后端使用单 viewer 的短时会话状态维持 iframe 的 HTTP / WebSocket 访问。
6. 本次只支持单 terminal session、单浏览器 viewer 的最小可用链路。

## 非目标

- 不把当前 terminal 能力扩展为多 session terminal 平台。
- 不支持多个标签页或多个浏览器同时附着到同一个 ttyd session。
- 不引入数据库、Redis 或长期 session store。
- 不重做现有全局 API key 体系。
- 不重写前端 Terminal UI。
- 不构建通用反向代理框架，只实现 ttyd 所需的最小 HTTP / WebSocket 代理路径。

## 方案选择

### 方案 A（采用）：后端 open + 受控 proxy + ttyd 信任代理认证

实现方式：
- 创建 terminal session 时，后端启动 ttyd，并生成一次性 `browser_open_token`
- 返回给前端的 `terminal_url` 不再是裸 ttyd 地址，而是后端入口：
  - `/terminal/session/{session_id}/open?token=...`
- 浏览器首次访问 open 路由时，后端校验 token 与 session 状态
- 校验通过后，后端创建单 viewer 的短时会话标记，并通过 cookie 或等价浏览器态把 viewer 身份绑定到后续请求
- 浏览器后续访问全部进入 `/terminal/session/{session_id}/proxy/...`
- 后端代理 ttyd 的 HTTP 与 WebSocket，并向 ttyd 注入其信任的认证头

**优点：**
- 可以真正穿透 iframe，而不是停留在跳转层
- 浏览器不需要直接处理 ttyd 的 Basic Auth
- 不再把 API key 传入 ttyd 进程参数
- 与“单 viewer、最小可用”目标高度一致

**缺点：**
- 需要补 ttyd 的最小代理层，复杂度高于单纯 redirect

### 方案 B：open 成功后继续重定向到裸 ttyd

不采用。虽然实现最轻，但无法完成认证接力：浏览器仍会直接面对 ttyd 的登录墙，且无法解决 ttyd argv 中带原始 API key 的问题。

### 方案 C：继续让浏览器直接访问 ttyd，但改成短时 ttyd 凭证

不采用。即便凭证变短时，也仍然需要把 ttyd 凭证交给浏览器，且 iframe / WebSocket 场景下仍然脆弱，不符合这次最小可用与边界收口目标。

## 具体设计

### 1. Terminal session 扩展字段

在 `TerminalSessionRecord` 上补最小所需的浏览器访问状态：
- `browser_open_token`：首次进入用的一次性 token
- `browser_open_expires_at`：open token 过期时间
- `browser_open_consumed_at`：首次消费时间，用于判定单次消费
- `viewer_session_token`：后续 proxy 访问使用的短时 viewer 标识
- `viewer_session_expires_at`：viewer 会话过期时间
- 保留现有 `terminal_url` 字段，但其语义固定为“浏览器可直接访问的后端入口 URL”

这些状态继续保存在当前单 terminal session 的内存态中，不引入额外存储。

### 2. ttyd 启动方式调整

`start_ttyd_session` 不再接收和传递原始 API key 型 `--credential` 参数。

新的 ttyd 启动方式需要满足：
- ttyd 认证改为信任上游代理认证头，而不是由浏览器自己输入 ttyd 凭证
- ttyd 启动参数中不再出现原始 API key
- 仍保留 host / port / shell command / working directory 的当前生命周期语义

`ttyd.py` 仍然只负责“ttyd 进程如何启动”和“ttyd 实际上游地址如何计算”，不承担浏览器 open token 或 viewer session 校验职责。

### 3. Session 创建流程

`POST /terminal/session` 时：
1. 若当前已有活动 terminal session，先按现有单 session 语义清理旧 session，再创建新 session。
2. 启动 ttyd 进程。
3. 生成短时 `browser_open_token`。
4. 记录 open token 的过期时间。
5. 清空旧 viewer session 状态。
6. 返回浏览器可访问的后端 open URL：
   - `/terminal/session/{session_id}/open?token=...`

此时前端仍然只消费 `terminal_url` 字段，不需要感知 ttyd 的真实地址。

### 4. Browser open 入口

新增：
- `GET /terminal/session/{session_id}/open?token=...`

该入口负责：
- 校验 session 是否存在且为 running
- 校验 `browser_open_token` 是否匹配
- 校验 token 是否过期
- 校验 token 是否已消费
- 校验当前是否已有活动 viewer

校验成功后：
- 将 `browser_open_consumed_at` 写入 session 状态
- 生成 `viewer_session_token`
- 设置 `viewer_session_expires_at`
- 通过 `Set-Cookie` 把 viewer 身份绑定到浏览器
- 重定向到：
  - `/terminal/session/{session_id}/proxy/`

这里采用 cookie 而不是把 viewer token 持续放在 query string 中，是为了避免后续静态资源与 WebSocket 路径反复携带 URL token。

### 5. Proxy HTTP 路由

新增最小 HTTP 代理入口，例如：
- `GET /terminal/session/{session_id}/proxy/{path:path}`

职责：
- 校验 viewer session 是否存在且未过期
- 将 HTTP 请求转发到 ttyd 对应路径
- 向 ttyd 注入其信任的认证头
- 透传响应内容、状态码和必要响应头

该入口负责 ttyd 页面的 HTML、静态资源、脚本等普通 HTTP 请求。

### 6. Proxy WebSocket 路由

新增 ttyd 所需的 WebSocket 代理入口，例如：
- `WS /terminal/session/{session_id}/proxy/ws`
  或与 ttyd 当前真实 ws 路径做等价映射

职责：
- 校验同一 viewer session
- 建立浏览器到 ttyd 的双向 WebSocket 转发
- 在连接 ttyd 上游时注入 ttyd 信任的认证头

这是让 iframe 中的真实 terminal 可交互的关键路径；如果没有这一层，页面即使加载成功，终端也会停留在不可交互状态。

### 7. 前端行为

前端保持最小改动：
- `TerminalBenchCard` 继续使用后端返回的 `terminal_url`
- iframe 继续加载 `session.terminal_url`
- 不新增前端登录流程
- 不新增前端 ttyd 凭证拼接逻辑

如果后端遵守“`terminal_url` 永远是浏览器可消费入口”的契约，前端无需理解 open token 或 viewer session 的内部细节。

### 8. 删除与清理语义

`DELETE /terminal/session` 时：
- 停止 ttyd 进程
- 清理 `browser_open_token` 相关状态
- 清理 `viewer_session_token` 相关状态
- 返回 idle 状态 session

这样旧 iframe 即使还持有原页面，也会在下一次 proxy 请求或 ws 续连时失效。

## 错误处理与边界

### Open 阶段
- session 不存在：`404`
- session 非 running：`409`
- token 不匹配：`403`
- token 已消费：`409`
- token 过期：`410`
- 已存在活动 viewer：`409`

### Proxy 阶段
- viewer session 缺失或无效：`401` 或 `403`，实现时统一一种即可
- ttyd 上游不可达：`502`
- ttyd session 已停止：`409` 或 `502`，优先使用更能表达“当前会话状态不允许访问”的语义

### Single viewer 边界
本次明确只支持单 viewer：
- 同一 terminal session 只允许一个活动浏览器 viewer
- 不保证多标签并发
- 若用户需要重新打开，允许通过重新创建 session 获取新的 open token 和新的 viewer session

## 测试与验证计划

### 1. 路由与状态测试
需要覆盖：
1. `POST /terminal/session` 返回的 `terminal_url` 指向后端 open 路径，而不是裸 ttyd 地址。
2. open token 首次消费成功。
3. 重复消费同一个 open token 被拒绝。
4. 过期 open token 被拒绝。
5. 已有活动 viewer 时再次 open 被拒绝。
6. viewer session 缺失时 proxy 路由拒绝访问。
7. 删除 session 后旧 viewer session 失效。

### 2. ttyd 启动参数测试
需要覆盖：
1. ttyd 启动参数已切换到代理认证模式。
2. ttyd 启动参数中不再出现原始 API key。
3. ttyd 仍可正常创建与停止。

### 3. HTTP / WebSocket 代理验证
需要验证：
1. open 成功后 iframe 可以拿到 ttyd 页面。
2. ttyd 静态资源通过 proxy 正常加载。
3. WebSocket 握手成功并可双向通信。
4. terminal 不是只显示空页面，而是能看到真实 shell 内容。

### 4. 手工端到端验证
至少确认：
1. 在 WebUI 点击 **Start terminal**。
2. iframe 可以直接显示真实 ttyd 页面。
3. 终端可交互。
4. Stop 后旧 iframe 链路失效。
5. 旧 open URL 无法再次复用。

## 影响文件范围

预计会涉及：
- `src/ainrf/terminal/models.py`
- `src/ainrf/terminal/ttyd.py`
- `src/ainrf/api/routes/terminal.py`
- `src/ainrf/api/middleware.py`
- `tests/test_api_terminal.py`
- `tests/test_terminal_ttyd.py`
- 前端通常无需改动，除非需要补极小兼容逻辑；若保持 `terminal_url` 契约稳定，则 `frontend/src/components/terminal/TerminalBenchCard.tsx` 可不变

总体原则：只补最小可用的 ttyd open-plus-proxy 链路，不把当前单 session terminal 能力膨胀成完整会话平台。
