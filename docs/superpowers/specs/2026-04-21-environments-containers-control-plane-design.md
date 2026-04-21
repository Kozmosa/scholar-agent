# Environments / Containers 控制面闭环设计

日期：2026-04-21

## 背景

当前仓库的活跃实现主线已经从历史 `P0-P9` 路线图转向 dashboard-first / WebUI 控制面增量交付。最近一批提交已经完成以下能力收口：

- terminal 真链路创建与 session 打开流程
- ttyd proxy auth 与 session identity 校验
- code-server 受管嵌入
- WebUI 多 tab 导航
- Containers 页设计说明

同时，执行环境相关后端骨架已经开始落地：

- `src/ainrf/environments/` 已有域模型与服务层
- `tests/test_api_environments.py` 已锁定 `/environments` 的最小 API 契约
- 当前 API app 仅挂载 `health`、`terminal`、`code` 路由，说明 environments 仍处于待接线状态

因此，下一阶段应优先把 environments / containers 这一条线做成闭环，而不是切回更大的 task runtime 主线。

## 目标

本阶段要完成一个单用户、本地状态驱动的 environments 控制面闭环：

1. 用户可以创建、查看、编辑、删除 environment。
2. Containers 页从 placeholder 升级为真实 environment 管理页。
3. environment 可以产出并展示最近一次探测结果。
4. Terminal / Workspace 可以绑定到某个 environment。
5. 项目级可以对用户级 environment 做引用或最小覆盖。

## 非目标

本阶段不做以下内容：

- 不切回 `/run`、task engine、human gate、mode orchestration 主线。
- 不引入数据库或多用户权限模型。
- 不做自动持续探测，只做手动触发与最近结果展示。
- 不把 environments 扩展成完整 infra inventory / fleet management 系统。

## 方案选择

### 方案 A（采用）：先闭合 environments 控制面，再把它作为 terminal / workspace 的配置源

做法：

- 先把 `src/ainrf/environments/` 接入正式 API
- 再把 Containers 页实现为 environments 管理入口
- 然后让 Terminal / Workspace 消费 environment 选择结果
- 最后补项目级引用/覆盖

**优点：**
- 与当前未完成代码和红灯测试连续
- 可以尽快形成用户可见闭环
- 避免 terminal / workspace 各自维护一套隐式目标配置

**缺点：**
- 需要先补 environments API 和前端表单层，短期内工作偏控制面而非执行面

### 方案 B：先把 environment selector 接进 Terminal / Workspace，再回补 Containers 管理页

不采用。这样用户可见收益会更快，但底层 environment 管理面会暂时不完整，且容易把配置来源做散。

### 方案 C：中断当前控制面节奏，切回 task runtime 主线

不采用。虽然长期仍然要回到 runtime / orchestration，但与当前最近提交和工作区中的未完成改动不连续，切换成本更高。

## 范围与边界

本阶段把 environment 定义成当前控制面的核心资源层，位于已有 `terminal` / `code` 之下、UI 之上。它承担 SSH 目标、默认工作目录、运行时偏好与能力探测状态，不承担任务编排和自治执行。

需要明确的边界：

- Containers 是 environment 的管理页，而不是独立的另一套模型。
- Terminal / Workspace 使用 environment 作为上游配置源。
- project-level reference / override 只解决“某项目默认用哪个 environment、覆盖少量字段”的问题，不扩展成复杂继承体系。

## API 设计

在 `src/ainrf/api/app.py` 新增 `environments` 路由组，并与现有 `health` / `terminal` / `code` 一样同时挂裸路径和 `/v1` 前缀。

第一批 API 保持最小闭环：

1. `GET /environments`
   - 返回 environment 列表
   - 满足现有空列表契约

2. `POST /environments`
   - 创建 environment
   - 返回保存后的完整记录
   - `latest_detection` 初始为 `null`

3. `GET /environments/{id}`
   - 返回单个 environment 详情
   - 支持详情页或编辑页初始化

4. `PATCH /environments/{id}`
   - 更新基础字段
   - 服务层继续复用别名唯一性等约束

5. `DELETE /environments/{id}`
   - 删除 environment
   - 若仍被项目引用，则按现有服务层保护拒绝删除

6. `POST /environments/{id}/detect`
   - 触发一次手动探测
   - 返回最新 detection 结果
   - 第一版允许同步执行，后续如有必要再任务化

## 数据模型设计

保持三层模型：

### 1. Environment record

保存环境主记录，字段包括：

- `id`
- `alias`
- `display_name`
- `description`
- `tags`
- `host`
- `port`
- `user`
- `auth_kind`
- `identity_file`
- `proxy_jump`
- `proxy_command`
- `ssh_options`
- `default_workdir`
- `preferred_python`
- `preferred_env_manager`
- `preferred_runtime_notes`

### 2. Detection record

保存最近一次探测快照，用于 UI 展示与后续 terminal / workspace 绑定决策。第一版只保留最近一次结果，不做历史列表。可包含：

- 探测时间
- 探测是否成功
- python / uv / git / docker / nvidia-smi 等能力是否可用
- 错误摘要（若失败）

### 3. Project reference / override

保存项目与 environment 的引用关系，以及少量项目级覆盖字段。第一版作为后端内部模型存在，待 terminal / workspace 绑定时再公开最小接口。

### 返回模型原则

API 返回继续内嵌 `latest_detection` 字段，而不是要求前端单独二次查询 detection。这样能直接契合当前测试契约，也方便 Containers 首页直接展示状态。

## 前端设计

### Containers 首页

将当前 Containers tab 升级为真实 environment 控制面首页，但保持单页优先，不急着拆更多路由。

首页展示建议采用卡片 / 表格混合视图，至少包含：

- 名称
- alias
- host
- auth kind
- 默认工作目录
- 最近探测状态 badge
- 关键能力摘要
- 操作按钮：`Edit` / `Detect` / `Delete` / `Use`

页面顶部提供 `Add environment` 入口。

### 新建 / 编辑表单

新建和编辑共用一套表单，不做分步向导。字段基本对应当前测试 payload 与服务层模型：

- 基础信息：`alias`、`display_name`、`description`、`tags`
- SSH 信息：`host`、`port`、`user`、`auth_kind`、`identity_file`
- 跳板 / 高级选项：`proxy_jump`、`proxy_command`、`ssh_options`
- 运行偏好：`default_workdir`、`preferred_python`、`preferred_env_manager`、`preferred_runtime_notes`

### 探测交互

Detect 保持显式按钮触发，而不是自动探测。

原因：
- 自动探测会引入频率控制、失败噪音与状态抖动
- 当前阶段只需要“用户配置后手动验证一次”
- 这样更符合最小闭环目标

### 跨页面使用入口

#### Terminal 页

增加 environment selector：

- 默认使用当前项目绑定 environment，若无则回退到最近使用 environment
- 打开 terminal 时携带当前 environment 上下文

#### Workspace 页

同样显示当前 environment，并用它驱动 workspace / code-server 所使用的工作目录与目标上下文。

这样，Containers 不只是管理页，也成为 terminal / workspace 的上游配置源。

## 错误处理与边界

- environment alias 冲突时返回明确 4xx 错误。
- environment 被项目引用时，删除请求应被拒绝。
- Detect 失败时应返回明确错误摘要，并在 `latest_detection` 中反映失败状态，而不是静默吞掉。
- Terminal / Workspace 选择了无效 environment 时，应阻止打开并给出明确提示。
- 第一版不支持自动后台持续刷新探测状态。
- 第一版不要求复杂的多项目、多环境批量操作。

## 实施顺序

按五个 feat、两层闭环推进。

### 第一层闭环：先把 environments 自己做成立

1. `feat: add environments API`
   - 新增 environments router
   - 接 service 与 schema
   - 让现有 `tests/test_api_environments.py` 红灯转绿

2. `feat: implement Containers page CRUD`
   - 将 placeholder 页接为真实列表 + 创建/编辑/删除
   - 与 API 形成第一个用户可见闭环

3. `feat: add environment detection run/status`
   - 接通 Detect 按钮与 `latest_detection` 展示
   - 保持手动触发

### 第二层闭环：让 environments 成为其他页面的配置源

4. `feat: bind terminal and workspace to selected environment`
   - Terminal / Workspace 增加 environment selector
   - 打开 terminal / workspace 时带上当前 environment 上下文

5. `feat: add project-level environment references/overrides`
   - 增加最小项目级绑定关系
   - 解决“某项目默认用哪个 environment”的问题

## 测试与验证计划

### 后端

- 先让 `GET /environments` 和 `POST /environments` 契约测试转绿
- 再补 `GET` / `PATCH` / `DELETE` / `detect` 的 API 测试
- 保持现有 service 级约束测试覆盖别名唯一性、引用保护等边界

### 前端

- 组件级测试覆盖：列表渲染、表单提交、Detect 按钮、错误展示
- 验证 Containers 页可完成创建、编辑、删除和探测展示

### 集成

至少验证一条黄金路径：

1. 创建 environment
2. 触发 Detect
3. 在 Terminal 页选择该 environment
4. 成功打开 terminal

若 Workspace 绑定在同一批次完成，则补一条 workspace 打开路径验证。

### 回归

继续运行现有 terminal / code 相关测试，确保引入 environments 后不破坏已完成控制面能力。

## Rollout 原则

- 每个 feat 都应独立可提交，不把五个增量混成一个大补丁。
- 先保证 API 契约和 Containers 页，再做跨页绑定。
- 如果 terminal / workspace 绑定迫使后端大改，则允许先停在前三个 feat，优先交付完整的 environment 控制面。

## 影响文件范围

预计会涉及：

- `src/ainrf/api/app.py`
- `src/ainrf/api/routes/` 下新增 environments router
- `src/ainrf/api/schemas.py` 或对应 schema 模块
- `src/ainrf/environments/models.py`
- `src/ainrf/environments/service.py`
- `tests/test_api_environments.py`
- `frontend/src/pages/` 下 Containers 页面
- `frontend/src/api/` 下 environments endpoint 封装
- `frontend/src/components/` 下 environment 列表、表单、selector 组件
- Terminal / Workspace 页面对应集成点

## 总结

当前最合理的推进方式，是沿着最近已经成形的 WebUI 控制面主线，先把 environments / containers 这条线做成闭环，再让 terminal / workspace 复用它，而不是立即切回更大的 runtime 编排主线。

总体原则：以最小 API 与最小 UI 闭环优先，保持单用户、本地状态、显式操作、可测试、可逐步提交。
