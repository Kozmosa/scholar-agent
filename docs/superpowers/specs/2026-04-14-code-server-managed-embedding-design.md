# Code-Server Managed Embedding Design

## Context

用户希望为当前项目引入 `code-server`，把它作为 WebUI 中的受管文件浏览入口，方便用户在浏览器内查看当前 workspace / 实验结果目录。第一阶段的重点不是把 Web IDE 做成独立产品，而是先把 `code-server` 的启停和暴露方式设计干净。

仓库当前 runtime 边界很明确：`src/ainrf/` 只保留最小化运行时能力，包括 API daemon 启停、container profile、SSH 健康探测和 terminal session MVP。`ainrf serve` 已经是当前 API runtime 的统一入口，daemon 模式会在 `.ainrf/runtime/` 下维护 pid/log 文件。现有 README 也明确说明当前 runtime 不包含 WebUI 能力，因此这次设计需要在不破坏“最小运行时”边界的前提下，为文件浏览能力增加一个受控、可降级的附属面。

同时，用户已明确以下约束：

- `code-server` 生命周期必须和 `ainrf serve` daemon 相同
- 前端不直接访问 `code-server` 端口，而是通过 AINRF 后端统一暴露的 `/code/` 路径进入
- `code-server` 打开的目录应绑定当前有效 container / workspace 配置中的 `project_dir`
- `code-server` 启动失败时，API daemon 继续运行，文件浏览能力降级为 unavailable

## Goal

在不引入复杂控制面的前提下，为 AINRF runtime 增加一个受管的 `code-server` 附属能力，使 WebUI 可以通过 iframe 嵌入 `/code/` 来浏览当前 daemon 实例绑定的 `project_dir`。

该设计需要保证：

- `ainrf serve` 启动时自动尝试拉起 `code-server`
- daemon 退出时自动终止其创建的 `code-server`
- API 统一暴露 `code-server` 入口，不泄漏内部端口给前端
- 失败时只影响 `/code/` 能力，不阻断 API 主体启动
- 第一版边界清晰、职责单一，避免过早扩展成多实例 IDE 平台

## Non-goals

本次不包括：

- 多实例 `code-server`
- 运行时动态切换目录
- 独立的 `ainrf code start/stop/restart` CLI
- 可配置的复杂 `code-server` 参数透传
- 把 `code-server` 状态建模为完整资源系统
- 在第一版中实现完整 WebUI 产品面，只定义最薄的 iframe 嵌入与状态展示

## Approach options considered

### Option A: AINRF daemon 托管 `code-server` 子进程 + 后端反向代理 `/code/`（recommended）

`ainrf serve` 在启动 API 的同时，创建一个只监听 `127.0.0.1` 的 `code-server` 子进程，并由 runtime 内部的 supervisor 负责探活、状态记录和退出清理。FastAPI 统一把 `/code/` 代理到这个本地实例，前端 iframe 只认 `/code/`。

- 优点：生命周期最干净；端口与鉴权边界统一；前端无需感知真实端口；未来容易扩展状态接口
- 缺点：需要在 runtime 中实现受管子进程和支持 websocket 的代理

### Option B: AINRF 只启动/停止 `code-server`，前端直接访问真实端口

- 优点：实现更省事
- 缺点：暴露内部端口；前端需理解地址与鉴权；不符合“统一后端入口”的目标

### Option C: 外部 supervisor（systemd / supervisor）托管 `code-server`，AINRF 只桥接

- 优点：守护机制成熟
- 缺点：生命周期不再真正绑定 daemon；部署复杂；超出当前最小 runtime 边界

推荐采用 **Option A**。

## Proposed architecture

### 1. Runtime child-service supervisor

新增一个聚焦单一职责的 runtime 模块，例如 `src/ainrf/code_server.py`，负责：

- 解析并冻结本次 daemon 实例的 `workspace_dir`
- 生成 `code-server` 启动命令与本地监听地址
- 启动子进程并进行 ready 探活
- 维护内存态状态：`starting | ready | unavailable`
- 停止进程并执行有限等待后的强制清理

这个 supervisor 不负责 API 路由、不负责前端，也不负责复杂配置模型。它的唯一职责是：管理“本 daemon 拥有的那个 `code-server` 实例”。

### 2. FastAPI integration layer

在现有 API 装配层新增两类能力：

- `GET /v1/code/status`：暴露当前 `code-server` 状态
- `/code/` 及其子路径：把请求代理到本地受管 `code-server`

这里的 API 层只消费 supervisor 暴露的状态和目标地址，不参与子进程管理逻辑。这样 runtime 生命周期和 HTTP 暴露面保持解耦。

### 3. Workspace resolution layer

`workspace_dir` 不引入新的配置中心，直接复用现有 runtime config / container profile 解析链路，从当前有效 profile 中读取 `project_dir`。如果无法解析到明确目录，supervisor 直接标记 unavailable，而不是回退到模糊默认目录。

### 4. Frontend embedding layer

WebUI 只承担薄 UI：

- 拉取 `/v1/code/status`
- `ready` 时渲染 iframe 指向 `/code/`
- `starting` 时展示加载态
- `unavailable` 时展示明确错误信息

前端不关心真实监听端口，也不参与启动控制。

## Lifecycle semantics

### Startup

- `ainrf serve` 启动 API 时，同时初始化 `CodeServerSupervisor`
- supervisor 解析本次 daemon 的 `workspace_dir`
- 若目录可用，则尝试拉起本地 `code-server`
- `code-server` 只监听 `127.0.0.1:<managed-port>`
- supervisor 在有限超时窗口内探活

### Success path

- API 继续正常启动
- supervisor 状态为 `ready`
- `/v1/code/status` 返回 `ready`
- `/code/` 可代理访问

### Failure path

如果发生以下任一情况：

- 主机未安装 `code-server`
- `workspace_dir` 不存在或不可访问
- 端口冲突
- 启动超时
- 子进程异常退出

则：

- API 仍然正常启动
- supervisor 状态转为 `unavailable`
- 失败原因记录到 `detail`
- `/v1/code/status` 返回 `unavailable`
- `/code/` 返回明确错误页或 `503 Service Unavailable`

### Shutdown

- daemon 收到终止信号时，先执行应用生命周期内的 child-service cleanup
- supervisor 先发送正常终止信号
- 在短超时内未退出则执行强制 kill
- 如使用 runtime 下的 pid / metadata 文件，则一并清理

### Ownership rule

每个 daemon 实例只认自己启动的 `code-server` 子进程，不尝试接管历史孤儿进程，也不复用旧实例。若发现 stale pid / stale metadata，仅做清理后重新拉起新实例。

## HTTP surface design

### `GET /v1/code/status`

第一版返回极简只读结构即可，例如：

- `status`: `starting | ready | unavailable`
- `workspace_dir`: 当前绑定目录
- `detail`: 补充说明或失败原因
- `managed`: `true`

用途仅限于前端展示状态，不扩展为复杂控制 API。

### `/code/` reverse proxy

由 FastAPI 挂载统一代理入口，前端 iframe 固定指向 `/code/`。

该代理需要满足两个要求：

1. **稳定的前缀语义**
   - 前端永远只访问 `/code/`
   - 代理层负责前缀剥离 / 转发，或配合 `code-server` base path 能力保证静态资源与内部导航可工作

2. **支持 websocket / upgrade**
   - 不能只做简单 HTTP 文件代理
   - 必须覆盖 `code-server` 运行所需的 websocket / streaming 连接

第一版不新增 restart、switch-workspace 等控制接口。

## Configuration rules

第一版保持最小配置面：

- `workspace_dir`：来自当前有效 `project_dir`
- bind host：固定 `127.0.0.1`
- bind port：由 AINRF 选择内部 managed port
- 对前端暴露：仅 `/code/` 代理路径

暂不引入以下配置项：

- `enable_code_server`
- 用户自定义根目录
- 自定义任意启动参数透传
- 多 workspace 切换

如果未来确实要扩展，应在这套“受管附属能力”先稳定后再单独设计。

## State freezing rule

`workspace_dir` 应在 daemon 启动时解析并冻结，而不是在前端打开 iframe 时动态决定。

这样可以保证：

- 一个 daemon 实例对应一个确定的文件浏览根目录
- 状态接口语义稳定
- 避免 runtime 运行期间 profile 变化导致 `code-server` 指向漂移

## Validation plan

### Supervisor tests

- 成功启动时状态可转为 `ready`
- 启动失败时状态为 `unavailable` 且带 detail
- stop 能正确终止子进程
- stale pid / stale metadata 可清理

### API integration tests

- `/v1/code/status` 在 `ready` / `unavailable` 场景下返回正确结构
- `/code/` 在不可用场景下返回明确错误
- 代理前缀行为正确
- websocket / upgrade 路径能通过测试替身验证基本转发语义

### CLI / server smoke tests

- `ainrf serve` 启动时会尝试初始化 supervisor
- `code-server` 启动失败不阻断 API 主体启动
- daemon 退出时会触发 child cleanup

### Frontend verification

- `ready` 时 iframe 渲染 `/code/`
- `starting` 时显示加载态
- `unavailable` 时展示明确错误信息
- 状态切换不出现明显闪烁或空白挂死

## Success criteria

完成后，系统应满足：

- `ainrf serve` daemon 启动时自动托管一个 `code-server` 实例
- `code-server` 根目录绑定本次 daemon 启动时解析出的 `project_dir`
- 前端只通过 `/code/` 访问文件浏览能力
- `code-server` 异常不阻断 API 主服务
- daemon 退出时不会遗留被自己创建的 `code-server` 常驻进程
- 第一版边界仍然保持“最小 runtime + 附属文件浏览能力”，没有演化成复杂 IDE 子系统
