# AINRF Onboard Design

## Context

AINRF 当前已经具备最小运行时能力，包括 `ainrf serve`、API key 保护、container profile 持久化，以及 terminal-bench MVP 所需的 `./.ainrf/config.json` 读取路径。但首次使用时，配置初始化仍然分散在局部逻辑中：`serve` 只在缺失 API key hash 时触发最小 bootstrap，且默认关注的是 `state_root/config.json` 的单一字段，而不是完整的首次使用体验。

下一步需要把“第一次在某个项目目录运行 AINRF”这件事定义成显式、可复用、可测试的 onboarding 能力：如果当前目录下没有 AINRF 配置，就进入交互式初始化流程，在当前目录的 `./.ainrf/` 中生成一套本地优先、可立即使用的配置。

## Goal

为 AINRF 增加显式的 `ainrf onboard` 命令，并让 `ainrf serve` 在默认场景下自动触发该流程，使用户第一次在某目录启动 AINRF 时可以交互式创建 `./.ainrf/config.json`，必要时再继续补充默认 container profile。

## Non-goals

本次设计不包括：

- 新的配置文件格式或迁移系统
- 非交互式 onboarding
- 多环境 / 多工作区配置继承机制
- 自动探测远端主机或自动生成 SSH 配置
- onboarding 期间启动 terminal session 或其他运行时资源
- 对旧版 orchestrator / task engine 路径的恢复

## User-facing behavior

### New command surface

新增：

- `ainrf onboard`

该命令负责在目标 state root 下初始化 AINRF 配置。

### Default startup behavior

当用户运行：

- `ainrf serve`

CLI 应先解析目标 state root：

- 若用户显式传入 `--state-root`，使用显式路径
- 否则默认使用当前工作目录下的 `./.ainrf`

随后检查该目录下的 `config.json`：

- 若存在，继续正常启动 `serve`
- 若不存在，输出提示并自动进入 `ainrf onboard`
- onboard 成功后，继续执行当前这次 `serve`

### Existing config behavior

当用户显式运行 `ainrf onboard` 且目标位置已经存在 `config.json` 时：

- CLI 必须提示用户是否覆盖现有配置
- 选择“否”时，退出且不修改已有文件
- 选择“是”时，重新生成配置

覆盖只影响 onboarding 写入的配置文件，不额外删除其他 runtime 文件。

### Non-interactive shells

如果缺少配置且当前环境无法交互输入：

- 不应卡住等待输入
- 应快速失败并输出明确提示，告诉用户运行交互式 `ainrf onboard` 或显式准备配置

## State root and file layout

### Default location

默认 state root 固定为：

- `Path.cwd() / ".ainrf"`

这条规则适用于：

- `ainrf onboard`
- `ainrf serve`
- 其他未来需要“当前目录工作区配置”的命令

### Generated files

本次 onboarding 默认创建：

- `./.ainrf/`
- `./.ainrf/config.json`

不要求在 onboard 阶段额外预创建 runtime pid/log 文件；这些仍由实际运行时按需创建。

## Onboarding flow

### Phase A: local-first base config

首次 onboarding 的默认目标是“先让当前目录可本地启动”，因此基础阶段只要求：

1. 告知用户将初始化当前目录下的 `./.ainrf/`
2. 交互式询问 API key
3. 隐藏输入并要求二次确认
4. 计算 hash 后写入 `api_key_hashes`
5. 生成最小 `config.json`

最小配置示例：

```json
{
  "api_key_hashes": ["<sha256>"]
}
```

### Phase B: optional container profile

基础配置写完后，再追加一个显式问题：

- “是否现在配置默认 container profile？”

如果用户选择否：

- onboarding 直接结束

如果用户选择是：

- 进入与现有 `container add` 一致的交互风格
- 收集：
  - profile name
  - SSH command
  - remote project directory
  - optional password
- 写入：
  - `container_profiles`
  - `default_container_profile`

带 container 的配置示例：

```json
{
  "api_key_hashes": ["<sha256>"],
  "default_container_profile": "default",
  "container_profiles": {
    "default": {
      "host": "gpu-server-01",
      "port": 22,
      "user": "researcher",
      "ssh_key_path": "~/.ssh/id_ed25519",
      "project_dir": "/workspace/projects",
      "ssh_password": null
    }
  }
}
```

## Architecture and boundaries

### Separate onboarding from config loading

onboarding 不应继续隐藏在 `ApiConfig.from_env()` 这种配置读取路径里。配置加载应保持“读取并校验”的职责；交互式创建配置应由 CLI 层显式触发。

推荐边界：

- `src/ainrf/cli.py`
  - 命令表面
  - 首次启动时的 onboarding 入口
- 新的 onboarding helper 模块
  - 负责提示、收集输入、写入配置
- `src/ainrf/api/config.py`
  - 保持读取已有配置并构造 `ApiConfig`
- 现有 container 解析辅助
  - 尽量复用，不重复实现 SSH command 解析逻辑

### Reuse over duplication

container profile 的交互字段和 SSH command 解析应复用现有 `container add` 已有行为，而不是再设计一套近似但不一致的规则。

### Serve orchestration boundary

`serve` 需要知道“如果缺配置，就先 onboard”，但不应自己内联完整交互实现。更合适的结构是：

- `serve` 调用一个“ensure initialized”入口
- 该入口决定是否需要 onboard
- 若需要，则转入 onboarding helper
- 成功后返回，再继续 `run_server()` / `run_server_daemon()`

## Error handling

### User cancellation

如果用户在 API key 输入或覆盖确认阶段取消：

- 不写半成品配置
- 直接退出，并给出可定位的提示

### Invalid container input

如果用户选择配置 container，但 SSH command 或必填字段无效：

- 在 CLI 层立即报错并重新提示该字段，或终止本次 onboarding
- 不写不完整 container profile
- 基础配置阶段已经成功的 `api_key_hashes` 可以保留

### Partial-write policy

本次流程采用“阶段化成功”策略：

- Phase A 成功后，最小配置可以落盘
- Phase B 是可选增强
- 如果 Phase B 失败，不回滚已经成功生成的最小本地配置

这样可以保证“至少本地可启动”这个最小目标已完成。

## Testing requirements

### CLI onboarding tests

需要覆盖：

- 当前目录缺少 `.ainrf/config.json` 时，`serve` 自动触发 onboard
- `onboard` 在成功输入 API key 后写入最小配置
- 用户选择继续配置 container 时，配置文件包含默认 profile
- 已存在配置时，`onboard` 会提示是否覆盖
- 选择不覆盖时，不修改已有配置
- 非交互环境下缺配置时，给出明确失败信息

### Config compatibility tests

需要确认：

- onboard 生成的 `config.json` 能被 `ApiConfig.from_env()` 正常读取
- container profile 结构与现有 `container add` 兼容
- 默认 state root 发现规则与显式 `--state-root` 不冲突

### Regression tests

需要保留并更新现有 `serve` / config 相关测试，确保：

- 已有配置目录仍可直接启动
- 显式环境变量 `AINRF_API_KEY_HASHES` 仍然优先于本地配置
- 不会破坏 terminal-bench MVP 现有 runtime 路径

## Success criteria

该设计完成后，应满足：

- 用户第一次在任意项目目录运行 `ainrf serve` 时，若缺少 `./.ainrf/config.json`，会被引导完成初始化
- 初始化默认以本地可用为目标，不强制首次配置 container
- 用户可以通过 `ainrf onboard` 显式重新执行初始化流程
- 生成的配置仍与现有 `ApiConfig` 和 container profile 读取逻辑兼容
- 所有配置默认落在执行命令时当前目录下的 `./.ainrf/`
