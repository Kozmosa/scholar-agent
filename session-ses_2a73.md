# Scholar agent docs update plan in Chinese

**Session ID:** ses_2a734ba42ffeGdN3JOiu8kF1cf
**Created:** 4/4/2026, 10:00:09 PM
**Updated:** 4/6/2026, 7:34:30 PM

---

## User

please refer to the new repo-for-reference `Awesome-AI-Scientist`, update docs for scholar agent framework properly, using chinese. refine my statement in better english expressions and talk with me in simplified chinese in following conversations. you are allowed to start no more than 24 subagents simutaneously, you may not start less than 16 subagents unless you are sure that it is not necessary. now start to explore and plan.

---

## Assistant (Plan · gpt-5.4 · 209.5s)

_Thinking:_

**Planning subagents' progress**

I’m considering starting 16 subagents in plan mode. This seems like a good approach to manage the task effectively. I wonder if I should think about how often to check in for progress updates. Maybe setting a regular schedule would help keep things on track. Alright, I’ll aim to gather those updates after the initial setup to see how everything is progressing as planned. Let’s keep this organized!

先做只读探索：并行查看项目约束、现有 framework 文档位置，以及 `ref-repos/Awesome-AI-Scientist` 里和“AI Scientist / framework / docs”相关的材料，然后整理一个可执行的更新计划。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/PROJECT_BASIS.md",
  "limit": 300,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/PROJECT_BASIS.md</path>
<type>file</type>
<content>1: # Scholar Agent Project Basis
2: 
3: > 用途：记录本仓库长期有效、跨会话应持续遵守的工程约束。临时方案、一次性实验和未落地设计不直接写入本文件。
4: 
5: ## 项目目标与当前边界
6: 
7: - 项目名称：`scholar-agent`
8: - 当前主要目标：沉淀面向学术研究 Agent 的调研笔记与框架设计，同时维护一个可扩展的 `ainrf`。
9: 
10: ## 约束优先级
11: 
12: - 更高优先级的局部约束文件，尤其是仓库根目录的 `AGENTS.md`，在用户当次指令和目录内更近的局部约束上优先级更高。
13: - 本文件声明的长期工程约定必须遵守，当本文档与工程出现冲突，显式提示用户处理。
14: 
15: ## LLM 协作与文档目录约定
16: 
17: - 本仓库现有长期文档主目录是 `docs/`；新增需要长期维护、会被纳入知识库与站点构建的 Markdown 内容，默认放入 `docs/` 下合适子目录。
18: - `docs/framework/` 用于框架设计、RFC、路线图和体系化方法论。
19: - `docs/projects/` 用于外部项目调研与对照分析。
20: - `docs/summary/` 用于跨项目综述、矩阵和汇总结论。
21: - 文档文件名使用英文 slug，正文以中文为主，优先使用 Obsidian 双链格式，例如 `[[framework/v1-rfc]]`。
22: - 会话日志、实现复盘或 agent 中间产物，存放于`docs/LLM-Working/` 当中。
23: - 每日工作日志固定存放于 `docs/LLM-Working/worklog/`，按天创建 `YYYY-MM-DD.md` 文件，并在同一日内持续追加。
24: - 工作日志默认按“每个已完成的修改计划 / 工作批次追加一条 changelog”记账，不把同一批次里的 edit、validation、commit 强拆成多条流水账。
25: - 每条 changelog 至少包含时间、批次或计划名、实际改动摘要与验证结论；若该批次产生 commit，在同一条末尾补充 commit hash 与 commit 首行。
26: - changelog 应总结“这一批完成了什么、影响了哪些部分、验证结果如何”，不要简单复述 commit message 或原子提交标题。
27: - 示例：`2026-03-16 10:40 changelog：完成 P3 worklog 规则调整，统一仓库级约束并同步修订 P3 规划说明；执行 docs build 成功；关联提交：abcd123 docs: revise worklog policy`
28: 
29: ## 工程编码风格与规范
30: 
31: ### 语言与工具
32: 
33: - 主要语言：`Python 3.13` 与 `Markdown`
34: - 运行时与构建：`uv run` 驱动的 Python CLI 与脚本执行，文档侧由 `scripts/build_html_notes.py` 构建 MkDocs 站点
35: - 包管理：`uv`
36: - 主要框架或库：`Typer`、`structlog`、`PyYAML`、`MkDocs`、`mkdocs-material`、`mkdocs-mermaid2-plugin`、`pytest`、`ruff`
37: 
38: ### 编译器 / 类型系统约束
39: 
40: - Python 版本要求固定为 `>=3.13`。
41: - `src/ainrf/`、`tests/` 和 `scripts/` 中的 Python 代码必须包含严格类型标注；缺失类型标注视为缺陷。
42: - 静态类型检查以 `ty check` 为准，提交前必须通过。
43: - 代码风格和基础质量由 `ruff check`、`ruff format` 和 `pytest` 共同约束。
44: - 当前项目不以口头约定替代落地配置；能进入长期约束的检查项，应当有对应命令或配置文件支撑。
45: 
46: ### 代码风格
47: 
48: - Python 模块使用标准 import 模块体系与 `snake_case` 命名；类名使用 `PascalCase`。
49: - 统一使用 4 空格缩进，字符串风格与格式化结果以 `ruff format` 为准。
50: - 优先保持实现简洁，避免为尚未验证的运行时能力过早抽象。
51: - 修改既有文件时优先遵循文件原有风格，再考虑局部重构。
52: - 非必要不添加注释；只有在复杂、非显而易见逻辑处补充简洁说明。
53: - 笔记类文档要求 YAML frontmatter、Obsidian wikilink 和可被站点构建脚本稳定处理的 Markdown 结构。
54: 
55: ### 错误处理与边界
56: 
57: - 对不可能状态与关键解析失败应快速失败，不静默吞错。
58: - 对外部输入、文件路径、frontmatter、wikilink 解析结果等边界值，在入口处完成校验与收敛。
59: - CLI 或脚本层输出应提供可定位问题的错误信息，避免只给出模糊失败描述。
60: - 生成目录 `site/` 与 `.cache/html-notes/` 视为构建产物，不直接手工编辑。
61: 
62: ## 架构解耦要求
63: 
64: - 文档构建逻辑、CLI 入口、日志配置和未来研究运行时能力应继续保持职责分离。
65: - `src/ainrf/` 负责可安装 Python 包与 CLI/服务运行时代码，避免把仓库级脚本逻辑直接堆入命令入口。
66: - `scripts/` 负责本地构建与辅助流程；若脚本演化为可复用运行时能力，应回收进入 `src/ainrf/`。
67: - `docs/` 负责长期知识资产；不要把仅用于一次调试的中间日志混入知识库主目录。
68: - 未来扩展 `ainrf` 时，优先把核心研究逻辑设计为可脱离具体宿主 CLI 复用的模块，再在 Typer 命令层做装配。
69: 
70: ## 目录约定
71: 
72: - `docs/`：Obsidian 风格知识库与站点源文档。
73: - `src/ainrf/`：AINRF Python 包、CLI 入口、日志与未来运行时代码。
74: - `tests/`：CLI smoke tests 与后续 Python 测试。
75: - `scripts/`：本地构建与预览辅助脚本。
76: - `site/`、`.cache/html-notes/`：生成产物，仅由构建流程维护。
77: - `ref-repos/`：参考仓库，只读研究输入，不在此目录内直接做业务开发。
78: 
79: ## 技术栈与官方参考链接
80: 
81: - Python
82:   - reference: `https://docs.python.org/3/`
83: - uv
84:   - reference: `https://docs.astral.sh/uv/`
85: - Typer
86:   - reference: `https://typer.tiangolo.com/`
87: - MkDocs
88:   - reference: `https://www.mkdocs.org/`
89: - MkDocs Material
90:   - reference: `https://squidfunk.github.io/mkdocs-material/`
91: - Ruff
92:   - reference: `https://docs.astral.sh/ruff/`
93: - pytest
94:   - reference: `https://docs.pytest.org/`
95: 
96: ## 开发与验证命令
97: 
98: - 安装依赖：`UV_CACHE_DIR=/tmp/uv-cache uv sync --dev`
99: - 本地开发：`UV_CACHE_DIR=/tmp/uv-cache uv run ainrf --help`
100: - 生产构建：`UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build`
101: - 测试：`UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
102: - 预览：`UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py serve`
103: - 其他关键命令：
104:   - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
105:   - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`
106:   - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff format --check src tests`
107: 
108: ## 本地调试与环境约定
109: 
110: - 本地标准入口优先使用 `uv run`，避免手工维护与锁文件不一致的虚拟环境。
111: - 本仓库不在标准文档中记录开发机私有绝对路径、账号信息或密钥路径。
112: - 本地辅助脚本如 `scripts/build.sh`、`scripts/serve.sh` 纳入版本控制。
113: - 日志输出当前以标准输出为主；CLI 运行时日志统一经 `structlog` 配置，后续服务化时应继续沿用统一日志入口。
114: - 排障优先级：
115:   - 先检查 `uv` 环境、依赖安装与 Python 版本是否满足 `>=3.13`
116:   - 再检查文档源文件 frontmatter、wikilink 与构建脚本输入是否一致
117:   - 最后检查 CLI 行为、日志配置和测试覆盖是否与当前 scaffold 状态匹配
118: 
119: ## Git 提交信息约定
120: 
121: - commit 首行使用 Conventional Commits，使用英文简要描述主要变更。
122: - 建议格式：`feat: ...` / `fix: ...` / `refactor: ...` / `docs: ...` / `chore: ...`。
123: - commit message 正文使用团队统一语言，说明本次修改细节、影响范围与必要背景。
124: - 正文使用 Markdown 无序列表分点描述，优先说明“为什么改”和“改了什么”。
125: - 需要换行时，使用多个 `-m` 参数或等效方式提交，不在字符串中写字面量 `\n`。
126: 
127: ## 变更维护原则
128: 
129: - 修改长期工程约定时，优先更新本文件。
130: - 新增长期有效的知识结构、构建规则或运行时约束时，应同步更新相关 `docs/` 文档，并在必要时从本文件补充索引。
131: - 新增 CLI 表面、解析行为或构建脚本契约时，必须同步补充或更新 `tests/` 中的 smoke tests。
132: - `LLM-Working`目录也需要纳入版本管理
133: - 对仓库进行实际修改、开发、验证或提交时，应同步追加当日 `docs/LLM-Working/worklog/YYYY-MM-DD.md`，不得把工作记录只留在会话上下文中。

(End of file - total 133 lines)
</content>
```

**Tool: glob**

**Input:**
```json
{
  "path": "/Users/kozmosa/code/scholar-agent",
  "pattern": "docs/framework/**/*.md"
}
```

**Output:**
```
/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md
/Users/kozmosa/code/scholar-agent/docs/framework/index.md
/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md
/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md
/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md
/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md
/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md
/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md
```

**Tool: glob**

**Input:**
```json
{
  "path": "/Users/kozmosa/code/scholar-agent/ref-repos",
  "pattern": "**/Awesome-AI-Scientist/**"
}
```

**Output:**
```
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/AGENTS.md
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/index
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/opencode
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/img/Wechat.jpg
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/img/WeChat Group.jpg
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/img/WeChat Group QR Code.jpg
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/img/WeChat Group
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/CONTRIBUTING.md
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/LICENSE
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/README.md
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/config
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/logs/HEAD
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/logs/refs/heads/main
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/refs/heads/main
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/HEAD
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/logs/refs/remotes/origin/HEAD
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/refs/remotes/origin/HEAD
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/packed-refs
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/objects/pack/pack-8c9de3fce424635cda12f7660c5cb027c9dac229.rev
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/objects/pack/pack-8c9de3fce424635cda12f7660c5cb027c9dac229.idx
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/objects/pack/pack-8c9de3fce424635cda12f7660c5cb027c9dac229.pack
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/push-to-checkout.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/update.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/pre-push.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/pre-applypatch.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/pre-merge-commit.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/post-update.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/prepare-commit-msg.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/pre-receive.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/fsmonitor-watchman.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/applypatch-msg.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/pre-commit.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/sendemail-validate.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/pre-rebase.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/hooks/commit-msg.sample
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/description
/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/.git/info/exclude
```

**Tool: task**

**Input:**
```json
{
  "command": "explore framework docs",
  "description": "scan framework docs",
  "prompt": "只读探索仓库中 scholar agent framework 相关文档。重点查找 docs/framework/ 下的核心文档、索引文档、总览文档、与 agent workflow / architecture / principles / planning / execution / repo structure 相关的内容。不要修改任何文件。返回：1) 关键文件路径列表；2) 每个文件一句话作用；3) 明显缺口或可改进点。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a7341151ffe15MiJnaU2OKsuR (for resuming to continue this task if needed)

<task_result>
以下是对仓库中 scholar agent framework 相关文档的只读探索结果，重点覆盖 `docs/framework/` 下核心文档、索引/总览文档，以及与 agent workflow / architecture / principles / planning / execution / repo structure 相关内容。

## 1) 关键文件路径列表

按建议阅读顺序与重要性整理：

1. `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
2. `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
3. `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
4. `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
5. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
6. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
7. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
8. `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`

补充的上位索引/总览文档：

9. `/Users/kozmosa/code/scholar-agent/docs/index.md`
10. `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`

约束背景文档（帮助理解仓库边界与文档定位）：

11. `/Users/kozmosa/code/scholar-agent/PROJECT_BASIS.md`

---

## 2) 每个文件一句话作用

### 核心 framework 文档

- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`  
  framework 总索引页，明确阅读顺序，并把愿景、架构、执行环境、V1 规格、路线图和参考映射串成一条主线。

- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`  
  这是框架总纲，定义系统定位、设计原则、双模式目标、人工关卡和“有界自治”的核心边界。

- `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`  
  这是核心架构文档，定义一等工件、分层边界、状态转换和“repo 优先”的研究数据平面。

- `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`  
  这是执行/仓库结构协议文档，规定容器接入假设、每项目 repo 目录布局、同步机制和资源追踪方式。

- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`  
  这是 V1 产品/工作流规格文档，详细说明 Mode 1 与 Mode 2 的输入输出、主工作流、细化流程、关卡和 done 定义。

- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`  
  这是实现级 RFC，把蓝图落到 REST 服务、三层架构、API、状态机、TaskEngine、GateManager、SSH Executor、Adapter 等具体组件设计上。

- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`  
  这是阶段化实施计划，按 P0-P9 定义交付物、测试标准、依赖关系和风险，最贴近 planning/execution 视角。

- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`  
  这是设计来源映射文档，解释外部参考项目分别贡献了哪些平台、控制、能力、编排和质量思路。

### 补充索引/总览

- `/Users/kozmosa/code/scholar-agent/docs/index.md`  
  仓库级文档入口页，把“参考项目调研”和“自有 framework 主线”并列组织，是理解文档全景的总导航。

- `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`  
  这是外部项目总览报告，提供框架抽象的证据层背景，帮助理解为什么需要自己定义 scholar agent framework。

### 约束背景

- `/Users/kozmosa/code/scholar-agent/PROJECT_BASIS.md`  
  这是仓库长期约束文档，说明 `docs/framework/` 的定位、目录边界、文档规范与项目当前目标。

---

## 3) 关键内容归类总结

### A. 核心文档 / 索引文档 / 总览文档
最关键的入口与总览是：

- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`

其中：
- `docs/framework/index.md` 是 framework 内部索引；
- `docs/index.md` 是整个 docs 的总入口；
- `docs/summary/academic-research-agents-overview.md` 是框架上游调研的总览背景。

### B. principles / architecture
最核心的是：

- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`

覆盖的关键点包括：
- 宿主无关
- repo 优先
- 工件优先于流程
- 有界自治
- 失败可记账
- 分层视图
- 工件图谱与状态机
- adapter 边界

### C. workflow / planning / execution
最相关的是：

- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`

三者关系大致是：
- `v1-dual-mode-research-engine.md`：定义工作流和业务目标
- `v1-rfc.md`：定义实现结构和运行机制
- `v1-roadmap.md`：定义分阶段落地路径和验收标准

### D. repo structure / execution environment
最相关的是：

- `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`

它是目前最明确描述项目级 repo 结构、同步策略和资源追踪的数据平面文档。

### E. 设计来源 / rationale
最相关的是：

- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
- `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`

这两篇共同回答“为什么这样设计”。

---

## 4) 明显缺口或可改进点

以下是从文档体系角度看，比较明显的缺口和优化方向。

### 1. 缺少一篇真正“面向实现者/新读者”的超短总览
现有文档很完整，但偏“体系化设计说明”，新读者需要在 `index -> blueprint -> architecture -> v1 spec -> rfc -> roadmap` 之间切换。  
可改进点：
- 增加一篇类似 `framework/overview.md` 或 “one-page architecture” 的速读文档；
- 用一页回答：系统是什么、怎么跑、有哪些核心对象、当前 V1 到哪里、代码入口在哪里。

### 2. repo structure 在“框架执行 repo”与“当前仓库源码结构”之间有一点混淆
`container-workspace-protocol.md` 讲的是未来研究项目在容器中的 per-project repo 结构；  
但用户如果想知道“当前这个 scholar-agent 仓库代码结构怎么映射到 framework”，还要再结合 `PROJECT_BASIS.md` 和 `docs/index.md` 理解。  
可改进点：
- 增加一篇“framework docs 与当前代码仓结构的映射”文档；
- 明确区分：
  1) 当前设计仓库结构；
  2) 未来 orchestrator/runtime 代码结构；
  3) 未来容器内 research project repo 结构。

### 3. workflow 文档强，但 execution contract 还比较分散
工作流定义在 `v1-dual-mode-research-engine.md`，实现机制在 `v1-rfc.md`，执行环境在 `container-workspace-protocol.md`，阶段化交付在 `v1-roadmap.md`；逻辑上合理，但查阅时较分散。  
可改进点：
- 增加“execution architecture guide”或“runtime walkthrough”；
- 用一篇文档串起：Task 提交 -> 论文解析 -> 计划审批 -> 原子任务执行 -> artifact 落库 -> 事件流 -> 报告归档。

### 4. 缺少统一术语表
文档里有很多关键术语：`PaperCard`、`ReproductionTask`、`ExplorationGraph`、`HumanGate`、`TaskEngine`、`StateStore`、`AgentAdapter`、`bounded autonomy` 等。  
虽然各文档里都解释了，但还没有一个统一 glossary。  
可改进点：
- 增加术语表文档，降低跨文档跳转成本；
- 尤其适合后续把设计移交给实现者或外部协作者。

### 5. RFC 很详细，但“当前已实现 vs 设计中”的状态边界不够集中
`v1-roadmap.md` 有阶段计划，`v1-rfc.md` 有完整实现设计，但如果读者想快速知道“哪些只是目标、哪些已经在仓库中有骨架”，需要自己拼接信息。  
可改进点：
- 增加一页“implementation status / design status”；
- 用表格列出每个组件：状态、代码位置、测试状态、下一步。

### 6. 缺少专门的 agent workflow 决策图
虽然 `v1-dual-mode-research-engine.md` 有 Mermaid 工作流图，`v1-rfc.md` 也有状态机图，但还缺一张“跨文档统一决策图”：
- 什么时候进入 HumanGate
- 什么时候 checkpoint
- 什么时候 budget/termination 生效
- 什么时候复现失败视为正式产出  
可改进点：
- 增加一张 end-to-end decision graph，连接业务工作流与实现状态机。

### 7. 缺少“代码入口映射到文档”的导航页
从文档里能看出未来应该有 `TaskEngine`、`StateStore`、`AgentAdapter`、`SSH Executor`、`MinerU Client` 等模块，但如果现在有人想从源码视角进入，还缺少“源码模块到设计文档”的双向索引。  
可改进点：
- 增加“source map”文档；
- 例如：`src/ainrf/...` 哪些模块对应 `v1-rfc` 哪一节。

### 8. 安全/权限假设写得较轻，适合补一篇 operational constraints
`container-workspace-protocol.md` 假设容器有 root、GPU、SSH 直连且框架不额外处理安全问题，这对设计初期合理，但运营落地时会是高风险区。  
可改进点：
- 增加一篇“deployment/security assumptions”；
- 明确哪些属于可信环境假设，哪些属于未来 V2/V运营层责任。

---

## 简短结论

如果只挑最值得先读的 6 篇：

1. `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
2. `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
3. `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
4. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
5. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
6. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`

这 6 篇基本就覆盖了：
- 为什么做这个 framework
- 核心原则是什么
- 关键对象与架构如何组织
- agent workflow 怎么跑
- execution 层如何实现
- planning 如何分阶段落地

如果你愿意，我下一步可以继续把这批文档整理成一个“按主题聚合”的精简阅读地图，比如分成：
- 原则层
- 架构层
- 工作流层
- 执行层
- 路线图层
- 证据来源层
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore reference repo overview",
  "description": "scan ref repo",
  "prompt": "只读探索 ref-repos 中名为 Awesome-AI-Scientist 的参考仓库。找出 README、docs、paper、architecture、workflow、agent design、experiment pipeline、planning loop 等最相关材料。不要修改任何文件。返回：1) 关键路径；2) 可借鉴的结构与表达方式；3) 不宜直接迁移的部分。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a7341140ffenIedv4IOaDgZWR (for resuming to continue this task if needed)

<task_result>
以下基于对 `ref-repos/Awesome-AI-Scientist` 的只读探索；我没有修改任何文件。

## 1) 关键路径

这个参考仓库本质上不是“实现型代码仓库”，而是“策展型知识库”。最相关材料几乎都集中在 `README.md`，另外有两份辅助规范文件。

### 核心文件
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/README.md`
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/CONTRIBUTING.md`
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/AGENTS.md`

### README 中最值得看的结构段落
#### 总体结构 / 信息架构
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/README.md`  
  - `# ⚙️ Core Components`
  - `## Research Automation Stack`
  - `## Emerging Capabilities`

这是全仓最接近“architecture / capability map”的部分。它不是系统架构图，而是“科研自动化分层框架”。

#### 工作流分解 / 科研生命周期拆分
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/README.md`
  - `# 📚 1. Knowledge Acquisition`
  - `# 💡 2. Idea Generation`
  - `# 🔬 3. Verification and Falsification`
  - `# ⚖️ 4. Review System`
  - `# 📈 5. Evolution`

这五大阶段就是它的主工作流表达方式。若你在找 workflow / pipeline / agent loop 的材料，这部分最有借鉴价值。

#### planning loop / 自我改进 / agentic cycle
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/README.md`
  - `#### 5.1.1. Dynamic Planning`
  - `#### 5.1.2. Autonomous Learning`

这两节最接近你提到的：
- planning loop
- iterative improvement
- agent self-reflection / self-correction
- closed-loop scientific discovery

#### experiment pipeline / verification / falsification
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/README.md`
  - `# 🔬 3. Verification and Falsification`
  - `### 3.1. Methods`
  - `### 3.2. Evaluation`

如果你关心“实验执行—验证—复现—反证”的流水线表达，这部分最相关。

#### agent design / multi-agent / end-to-end AI scientist
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/README.md`
  - `## Emerging Capabilities`
  - `#### 1.2.1. Literature Search and Curation`
  - `### 2.1. Methods`
  - `#### 5.1.1. Dynamic Planning`
  - `#### 5.1.2. Autonomous Learning`
  - `# 📜 Survey`
  - `# 🏆 Benchmarks`

其中反复出现的代表性条目包括：
- The AI Scientist
- Agent Laboratory
- Towards an AI Co-Scientist
- CycleResearcher
- AIGS
- AI Scientist-v2
- Agentrxiv
- AlphaEvolve
- ScienceAgentBench
- MLAgentBench
- PaperBench

### 补充说明
我没有在这个仓库里找到独立的：
- `docs/`
- `paper/` 或 `papers/`
- `architecture/`
- `workflow/`
- 专门的 agent 设计文档目录

也就是说，这个仓库的“文档”主要就是一份超长 `README.md`，不是多文档体系。

---

## 2) 可借鉴的结构与表达方式

### A. 用“科研生命周期”而不是“技术模块”来组织材料
这个仓库最强的地方，是把 AI Scientist 相关内容按研究流程拆成：

1. Knowledge Acquisition
2. Idea Generation
3. Verification and Falsification
4. Review System
5. Evolution

这比按“模型/工具/论文类型”分组更适合做你的框架文档，因为它天然对应：
- 输入知识
- 生成想法
- 做实验/验证
- 评审与筛选
- 动态规划与持续学习

如果你要构建自己的 scholar-agent 文档体系，这种“阶段式主线”非常适合做顶层目录。

### B. 用“分层表格”做一页式 architecture 概览
`README.md` 里的 `Research Automation Stack` 表格值得借鉴。它的优点是四列结构清晰：
- Layer
- Key Papers Category Alignment
- Example Technologies / Concepts
- Description

这种表达很适合迁移成你自己的：
- 系统层
- 职责
- 典型能力
- 对应模块 / 命令 / agent
- 边界说明

也就是说，可借鉴的是“表格式能力地图”，不是其具体内容。

### C. 用“Emerging Capabilities”承接 roadmap / frontier
`## Emerging Capabilities` 这一节表达得很轻量，但很适合作为：
- 当前已支持
- 正在探索
- 尚不稳定
- 未来方向

这种写法适合你的项目里用来区分：
- 已实现能力
- 实验性能力
- 研究性方向

### D. 把“planning loop / autonomous learning”单独抬成一级议题
它没有把 planning 只埋在方法细节里，而是在 `Evolution` 下单独拆成：
- Dynamic Planning
- Autonomous Learning

这很值得借鉴。因为对 agent 系统而言，很多人会把 planning、reflection、self-improvement 混进实现细节，结果顶层设计不清楚。这个仓库的好处是明确告诉读者：

“研究自动化不仅是做任务，还包括如何动态改计划、如何持续学习。”

如果你写自己的 agent design 文档，可参考这种结构，把以下内容单列：
- planning
- critique/review
- memory/knowledge update
- loop termination / stopping criteria

### E. 把“benchmark”从“methods”中剥离
它专门有 `# 🏆 Benchmarks`。这点很重要，因为很多项目会把 benchmark 混在论文列表里，导致：
- 方法、数据、评估边界模糊
- 难以快速定位验证依据

如果你的项目以后要形成研究代理评估体系，这种表达方式很好：
- 方法文档描述“怎么做”
- benchmark 文档描述“怎么评”
- survey 文档描述“领域全貌”

### F. “条目级标准模板”适合作为知识库录入规范
`CONTRIBUTING.md` 对 paper entry 的模板写得很直接：
- Paper
- Badge
- Code
- Review
- Project

这对“知识库类仓库”很有用。你若要在自己仓库里维护参考文献/项目索引，也可以借鉴其录入字段一致性，而不是自由文本式记录。

### G. “策展型 README”适合做入口，不适合做全部真相
它非常适合当门户页：
- 一眼看领域结构
- 快速跳转到主题
- 找代表性 paper / benchmark / project

如果你的项目要兼顾外部可读性，这种 README-first 风格值得借鉴为入口页。

---

## 3) 不宜直接迁移的部分

### A. 不宜直接迁移其“单 README 承载一切”的组织方式
这个仓库几乎把所有内容塞进一个 README。对“论文/资源清单”是可行的，但对你这种需要：
- 设计原则
- 运行时架构
- CLI/模块边界
- agent loop
- validation strategy
- implementation notes

的项目来说，不宜照搬。

原因：
- 长文难维护
- 设计、实现、参考资料混杂
- 后续难追踪版本演进
- 很难承接你的 Obsidian/docs 体系

你更适合把它的“顶层分类法”迁移到多文档结构，而不是把 README 变成百科全书。

### B. 不宜直接迁移其“资源策展视角”
这个仓库的本体是“资源清单 + 论文索引”，不是一个可运行系统的设计文档。  
所以其中很多内容适合当：
- literature landscape
- capability taxonomy
- benchmark map

但不适合直接当：
- 系统 architecture spec
- agent protocol spec
- experiment orchestration design
- implementation contract

换句话说，它更像“研究地图”，不是“工程蓝图”。

### C. 不宜直接迁移其大量营销/宣传式表达
例如 README 开头的语气较强：
- “Empowering Scientific Discovery”
- “your compass”
- “rapidly evolving world”
- 带较多 emoji 和宣传性措辞

如果你的仓库目标是严谨的 framework / RFC / implementation docs，这类文风不宜直接迁移。  
更适合借鉴的是其分类框架，不是其宣传口吻。

### D. 不宜直接迁移其对外部服务的强绑定表达
README 多次把内容导向其外部站点与服务，例如：
- AI-Researcher.net
- DeepReviewer
- CycleResearcher

这对他们的生态展示合理，但若直接迁移到你的项目，会产生问题：
- 文档中立性下降
- 参考与自有能力边界变模糊
- 容易把“第三方能力”写成“本项目能力”

你更需要保持：
- 文献综述
- 自身实现
- 外部参考
三者分离。

### E. 不宜直接迁移其“论文列表即架构说明”的写法
例如 “Dynamic Planning / Autonomous Learning” 下主要仍是论文条目，而不是：
- loop state
- planner inputs/outputs
- retry policy
- review gate
- experiment artifact lifecycle
- success/failure criteria

对你的项目而言，这些工程级抽象才是关键。  
所以能迁移的是“主题命名”，不能直接迁移其“仅列论文不抽象机制”的内容组织。

### F. 不宜直接迁移其格式细节中的不一致性
只读探索时可以看出 README 中存在一些不够稳的地方，例如：
- 有些标题大小写不统一
- 某些项目名称拼写可疑，如 `AI-Scientis`
- 同名条目跨区重复出现，如 `The AI Scientist`、`Towards an ai co-scientist`、`Cycleresearcher`
- 有些 badge/链接风格不完全一致
- 一些占位/模板痕迹还在，如 README 顶部 badge 中 `[YOUR_USERNAME]/[YOUR_REPO_NAME]`

因此不建议直接复制其具体格式模板到你的正式文档体系里。

### G. 不宜直接迁移其 community / event / social 区块
`Community`、`Upcoming Events`、`Discussion Forums` 对策展仓库有用，但对你的项目核心设计帮助有限。  
尤其是：
- 过期快
- 维护成本高
- 与系统设计无强关系

若迁移，应作为外围资源页，而不是核心文档主线。

---

## 简短结论

如果只看“对 scholar-agent 最有借鉴价值的部分”，我会这样总结：

### 最值得借鉴
1. 用“科研生命周期”做顶层结构
2. 用“Research Automation Stack”做一页式能力架构图
3. 单列 `Dynamic Planning` / `Autonomous Learning`
4. 把 `Survey` 和 `Benchmarks` 独立出来
5. 用统一条目模板维护参考资料

### 最不该照搬
1. 单 README 承载所有内容
2. 资源清单式写法替代系统设计
3. 宣传/生态导流式文风
4. 将论文分类直接当成工程架构
5. 格式和命名上的现存不一致

如果你愿意，我下一步可以继续基于这个参考仓库，帮你把“可借鉴结构”转写成一版更适合你当前项目 `docs/framework/` 的目录草案。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore docs navigation",
  "description": "find docs index",
  "prompt": "只读探索 docs 目录中的导航结构，特别是 framework、projects、summary 之间的链接关系，以及是否存在总索引、MOC、landing page。不要修改任何文件。返回：1) 导航入口文件；2) framework 文档如何被发现；3) 文档组织问题。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a73410b6ffegWrzI2JVZ5STYe (for resuming to continue this task if needed)

<task_result>
以下是对 `docs/` 目录导航结构的只读探索结果。未修改任何文件。

## 1) 导航入口文件

我看到当前文档导航主要依赖少数几个 `index`/`overview` 型页面，而不是显式命名为 `MOC.md` 或 `landing.md` 的文件。

### 一级入口 / landing page
1. `/Users/kozmosa/code/scholar-agent/docs/index.md`
   - 这是整个 `docs/` 的总入口。
   - 明确把内容分成两条主线：
     - `framework/`：自有框架蓝图
     - `summary/` + `projects/`：外部项目调研
   - 它本质上就是全站 landing page + 总索引 + 顶层 MOC。

### framework 子入口
2. `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
   - 这是 `framework/` 子目录的导航页。
   - 提供明确阅读顺序、内容索引、能力入口。
   - 它是 framework 的 MOC。

### research/summary 子入口
3. `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
   - 这是调研侧的汇总入口。
   - 从外部项目对比、能力矩阵、决策图把读者导向各 `projects/*`，并且再反向导向 `framework/index`。
   - 它更像 summary/overview hub，而不是全站总索引。

### 辅助入口
4. `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
   - 不是导航首页，但承担了“从调研到框架”的桥接入口。
   - 它把 `projects/` 的结论映射回 `framework/` 设计，是非常关键的跨区导航节点。

### 是否存在总索引 / MOC / landing page
- 有总索引：`/Users/kozmosa/code/scholar-agent/docs/index.md`
- 有 framework MOC：`/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
- 有 summary hub：`/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
- 没看到显式命名为 `MOC.md`、`landing.md` 的文件
- 但从功能上讲：
  - `docs/index.md` = 全站 landing + 总索引
  - `docs/framework/index.md` = framework MOC
  - `docs/summary/academic-research-agents-overview.md` = 调研总览 hub

---

## 2) framework 文档如何被发现

`framework` 文档的“被发现路径”比较清楚，主要有 4 条。

### 路径 A：从总入口直接进入
入口文件：
- `/Users/kozmosa/code/scholar-agent/docs/index.md`

机制：
- 在“阅读方式”里直接写明：
  - 构建自己的研究系统，先读 `[[framework/index]]`
- 在“框架主线”表格中列出整个 framework 文档序列：
  - `framework/index`
  - `framework/ai-native-research-framework`
  - `framework/artifact-graph-architecture`
  - `framework/v1-dual-mode-research-engine`
  - `framework/v1-rfc`
  - `framework/v1-roadmap`
  - `framework/reference-mapping`

结论：
- 这是 framework 最主要、最清晰的发现入口。

### 路径 B：从 summary 总览页跳转进入 framework
入口文件：
- `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`

机制：
- 开头摘要就写明：
  - 如果目标从“选仓库”转向“做自己的研究系统”，继续阅读 `[[framework/index]]`
- 还明确说明：
  - 这份报告承担“证据层”
  - 自有系统蓝图已拆到 `[[framework/index]]`

结论：
- summary 承担了“先调研，再进入框架”的转场职责。
- 这条路径是从 `summary -> framework` 的主桥。

### 路径 C：framework 内部靠 `framework/index.md` 顺序阅读
入口文件：
- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`

机制：
- 提供顺序化阅读路线：
  1. `ai-native-research-framework`
  2. `artifact-graph-architecture`
  3. `container-workspace-protocol`
  4. `v1-dual-mode-research-engine`
  5. `v1-rfc`
  6. `v1-roadmap`
  7. `reference-mapping`

结论：
- framework 内部发现依赖单一 index 页完成。
- 比较像线性蓝图阅读，不像网状知识库浏览。

### 路径 D：通过 cross-link 从 projects/summary 反向发现
关键文件：
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- 多个 `projects/*.md`

机制：
- `reference-mapping.md` 把具体项目映射到框架层决策，连接 `projects/*` 与 `framework/*`
- 部分项目页在关联笔记中链接 `[[framework/reference-mapping]]`
  - 例如：
    - `/Users/kozmosa/code/scholar-agent/docs/projects/argusbot.md`
    - `/Users/kozmosa/code/scholar-agent/docs/projects/evoscientist.md`
    - `/Users/kozmosa/code/scholar-agent/docs/projects/autoresearch.md`
- `ai-native-research-framework.md` 末尾又链接回 summary：
  - `[[summary/academic-research-agents-overview]]`

结论：
- framework 的被发现不只是“自顶向下”，也有“调研页 -> 映射页 -> 框架页”的反向路径。
- 但这条路径不如 `docs/index.md` 和 `framework/index.md` 那么统一。

---

## 3) 文档组织问题

下面是我看到的几个主要组织问题。

### 问题 1：总入口存在，但 projects 缺少独立 index/MOC
现状：
- 有：
  - `/Users/kozmosa/code/scholar-agent/docs/index.md`
  - `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
  - `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
- 没有看到：
  - `/Users/kozmosa/code/scholar-agent/docs/projects/index.md`

影响：
- `projects/` 的发现高度依赖：
  - `docs/index.md` 的项目清单
  - `summary/academic-research-agents-overview.md` 的矩阵和决策图
- 如果用户直接进入 `projects/` 目录，缺一个明确的子入口页。

判断：
- `framework` 有明确子导航，`projects` 没有，信息架构不对称。

---

### 问题 2：summary 与 index 的入口职能有一定重叠
现状：
- `docs/index.md` 已经在做：
  - 总入口
  - 两条主线说明
  - 项目清单
  - framework 主线入口
- `summary/academic-research-agents-overview.md` 也在做：
  - 项目总览
  - 能力矩阵
  - 决策图
  - 到 `framework/index` 的导流

影响：
- 用户可能不容易马上区分：
  - `index.md` 是“站点入口”
  - `summary/...overview.md` 是“调研结论页”
- 二者都像“总览页”，但角色边界没有被命名得非常明确。

判断：
- 结构上是合理的，但语义层次略模糊。
- 一个更清晰的做法通常是：
  - `index.md` 负责站点导航
  - `summary/...overview.md` 负责研究结论
- 当前已经部分这样做，但仍有重叠。

---

### 问题 3：framework 的发现很强，但更多依赖线性阅读
现状：
- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md` 提供非常明确的阅读顺序
- framework 文档之间也有很多互链
- 但它的组织方式偏“说明书/蓝图手册”，而不是多入口知识图谱

影响：
- 对首次阅读者很友好
- 对按问题跳读的人稍弱：
  - 想找“状态机”
  - 想找“容器协议”
  - 想找“人工关卡”
  - 想找“RFC vs 路线图差异”
  这些没有独立主题入口页，只能依赖 index 顺读或文内链接

判断：
- 不是坏事，但偏手册化，MOC 层次还可以更细。

---

### 问题 4：跨区桥接主要集中在少数文件，桥梁点偏少
关键桥梁主要是：
- `/Users/kozmosa/code/scholar-agent/docs/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`

影响：
- `framework`、`projects`、`summary` 三者之间的关系总体是清楚的：
  - `projects` = 单仓研究
  - `summary` = 汇总结论/证据层
  - `framework` = 自有抽象/蓝图层
- 但真正承担“层间跳转”的节点比较少，集中在 overview/reference-mapping/index 上

判断：
- 导航结构不是分散式网状，而是“中心枢纽式”。
- 一旦读者没从这些核心页进入，侧向发现能力会下降。

---

### 问题 5：项目页之间互链较多，但没有统一分类页承接
现状：
- 各 `projects/*.md` 在“关联笔记”里彼此互链很多
- 例如会互相指向：
  - `claude-scholar`
  - `argusbot`
  - `academic-research-skills`
  - `everything-claude-code`
- 但没有看到一个专门的 `projects/index.md` 按类别组织：
  - 技能库
  - 流水线
  - 控制层
  - 工作台
  - harness

影响：
- 当前分类知识存在，但主要散落在：
  - `summary/academic-research-agents-overview.md` 的矩阵与建议里
- 分类结果没有沉淀成一个稳定的 `projects` 子导航页

判断：
- 这会让 `projects` 的浏览体验更像“通过总结页反查单篇”，而不是“在 projects 区内部导航”。

---

### 问题 6：存在“站点导航”和“Obsidian 关联笔记”双重导航，但层次不总一致
现状：
- 文档末尾大量使用“关联笔记”
- 顶部/正文又有“阅读方式”“内容索引”“能力入口”
- 这是两套导航机制：
  1. 显式结构化导航
  2. 关联笔记式网状导航

影响：
- 优点：Obsidian 风格很自然
- 缺点：不同文件的导航语义不完全统一
  - 有的偏阅读顺序
  - 有的偏相关主题
  - 有的偏来源追溯

判断：
- 当前并不混乱，但信息架构风格不完全一致。

---

## 总结判断

### 当前导航关系，可概括为：
- `docs/index.md`
  - 全站总入口
  - 将读者分流到：
    - `framework/index.md`
    - `summary/academic-research-agents-overview.md`
    - 以及若干 `projects/*.md`
- `summary/academic-research-agents-overview.md`
  - 负责项目层面的总览、矩阵、决策
  - 再把“要做自有系统”的读者导向 `framework/index.md`
- `framework/index.md`
  - 负责 framework 内部顺序导航
- `framework/reference-mapping.md`
  - 负责 `projects -> framework` 的概念桥接

### 简短结论
1. 导航入口文件
   - `/Users/kozmosa/code/scholar-agent/docs/index.md`
   - `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
   - `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
   - `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`（桥接入口）

2. framework 文档如何被发现
   - 主要通过 `docs/index.md` 直接进入
   - 其次通过 `summary/academic-research-agents-overview.md` 从“调研结论”导流进入
   - 在 framework 内部再由 `framework/index.md` 线性组织
   - 少量通过 `reference-mapping.md` 和部分项目页反向发现

3. 文档组织问题
   - 缺少 `projects/index.md`
   - `index` 与 `summary overview` 的总览职能略有重叠
   - framework 导航强，但偏线性手册，问题导向入口较少
   - 三个区之间的桥接点集中在少数核心页面
   - 项目分类已存在于 summary 中，但未沉淀为 projects 子导航
   - 结构化导航和关联笔记两套机制并存，语义风格略不统一

如果你愿意，我下一步可以继续做一个“只读版导航图”，把 `index -> summary -> projects` 和 `index -> framework` 的链接关系画成树状/图状摘要。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore terminology",
  "description": "collect terminology",
  "prompt": "只读搜索 scholar agent framework 文档中使用的核心术语，比如 framework, agent, workflow, planning, execution, context, memory, repository, notes, validation, constraints。不要修改任何文件。返回：1) 术语清单；2) 不一致命名；3) 建议统一的中文表达。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a73410afffebgcsliFRXbl1s1 (for resuming to continue this task if needed)

<task_result>
以下是对 `docs/framework/` 中 scholar agent framework 文档的只读术语梳理。未修改任何文件。

核心来源文件：
- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`

## 1) 术语清单

下面按你给的目标词和文档中实际扩展出的近义词一起整理。

### A. framework
文档中的实际用法：
- framework
- AI-Native Research Framework
- AINRF
- 框架
- 研究系统
- 研究引擎
- 有界自治研究系统
- 有界自治研究引擎

语义观察：
- 在愿景层更常写“框架/研究系统”
- 在 V1 和 RFC 实现层更常写“研究引擎”
- `AINRF` 常作为缩写品牌名

建议将三层语义分开：
- 品牌名：AINRF
- 总体概念：框架
- 运行时实例/服务：研究引擎

### B. agent
实际用法：
- agent
- Agent
- research-agent
- Agent Adapter
- AgentAdapter
- Claude Code + Opus 等 agent
- 宿主
- 宿主适配
- adapter / Adapter

语义观察：
- “agent”有时指 Claude Code 这类执行主体
- 有时又和“宿主”混用
- 另有“AgentAdapter”作为正式接口名

建议区分：
- agent：智能体/执行代理
- 宿主：Claude Code / Codex / OpenCode 这类承载环境
- AgentAdapter：智能体适配器

### C. workflow
实际用法：
- workflow
- 工作流
- 流程
- pipeline
- stage
- 阶段
- 工作流控制器
- 基础流程
- 主工作流

语义观察：
- “工作流”是主表达
- “流程”常作泛称
- “pipeline”只在少数愿景描述中出现
- “stage/阶段”在 RFC 里专指任务状态阶段，不完全等于工作流

建议区分：
- workflow -> 工作流
- process/flow -> 流程
- stage -> 阶段

### D. planning
实际用法：
- planning
- 计划
- 规划
- 探索计划
- 复现计划
- 计划关卡
- 计划审批
- plan_approval
- 制定计划
- 计划修订

语义观察：
- 文档总体上“计划”比“规划”更稳定
- RFC 中 `planning` 是正式任务阶段名
- `plan_approval` 是正式关卡类型名

建议统一：
- planning -> 计划阶段
- plan_approval -> 计划审批关卡
- plan -> 计划
- planning docs 不用“规划”除非强调 roadmap 层

### E. execution
实际用法：
- execution
- 执行
- 执行层
- 执行平面
- Execution Layer
- Executor / SSH Executor
- 执行环境
- 原子任务执行

语义观察：
- “执行层”偏系统分层
- “执行平面”偏架构视角
- “执行环境”偏容器/基础设施
- `execution` 在路线图里又是代码模块名

建议区分：
- execution layer -> 执行层
- execution plane -> 执行平面
- execution environment -> 执行环境
- executor -> 执行器

### F. context
实际用法：
- context
- 上下文
- domain_context
- 领域上下文
- 会话上下文
- 隐式上下文
- 研究上下文

语义观察：
- “上下文”整体稳定
- `domain_context` 是明确的用户输入字段
- “会话上下文”与“隐式上下文”用于批判只靠会话记忆的做法

建议统一：
- context -> 上下文
- domain_context -> 领域上下文
- session context -> 会话上下文

### G. memory
实际用法：
- memory
- 记忆
- 会话记忆
- 持久记忆

语义观察：
- 在 framework 自身正文中出现不多，更多出现在 `reference-mapping.md`
- 常用于对比：不要只存在会话记忆里

建议统一：
- memory -> 记忆
- session memory -> 会话记忆
- persistent memory -> 持久记忆

### H. repository
实际用法：
- repository
- repo
- git repo
- per-project git repo
- 仓库
- 代码仓库
- source_repo
- Repo 优先

语义观察：
- “repo”远多于“repository”
- “仓库”有时泛指项目仓库，有时特指 git repo
- “Repo 优先”是核心设计原则之一

建议统一：
- repo / repository -> 仓库
- git repo -> Git 仓库
- per-project git repo -> 每项目 Git 仓库
- repo-first -> 仓库优先

### I. notes
实际用法：
- notes
- note
- 笔记
- system-note
- obsidian-note
- Markdown
- 知识库
- 关联笔记

语义观察：
- 文档里“笔记”“Markdown”“知识库”三者并存
- “笔记”强调文档形态
- “知识库”强调整体集合
- “Markdown”强调载体格式，不是同义词

建议统一：
- notes -> 笔记
- note repository / knowledge base -> 知识库
- Markdown note -> Markdown 笔记 / Obsidian 笔记

### J. validation
实际用法：
- validation
- 验证
- 校验
- 可测试标准
- formal verification
- health check / 健康检查
- 结构验证

语义观察：
- “验证”和“校验”都有
- “校验”更偏输入/参数/签名/结构检查
- “验证”更偏测试、正确性、结果确认
- “可测试标准”在 roadmap 中是重要术语

建议统一：
- validation -> 验证
- validation of input/schema/signature -> 校验
- acceptance criteria -> 可测试标准

### K. constraints
实际用法：
- constraints
- 约束
- 边界
- 合同边界
- 终止合同
- 预算上限
- 深度上限
- 时间上限
- 工具约束
- 默认实现约束

语义观察：
- 文档里最核心的表达其实不是单独“约束”，而是“有界自治”
- “边界”“合同”“约束”分别落在不同层
- “终止合同”是非常关键的专有表达

建议统一：
- constraints -> 约束
- boundary -> 边界
- contract boundary -> 合同边界
- termination contract -> 终止合同

---

## 2) 不一致命名

以下是不太统一、后续容易造成概念漂移的点。

### 2.1 “框架 / 研究系统 / 研究引擎”混用
表现：
- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md` 更常写“框架”“研究系统”
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md` 和 `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md` 更常写“研究引擎”

问题：
- 容易让人不清楚是在说总体方法论，还是具体运行时实现。

建议：
- “框架”表示总设计
- “研究引擎”表示 V1 运行时系统
- “研究系统”可少用，或作为总称但不要与“引擎”交替出现在同一层

### 2.2 “agent / 宿主 / Claude Code”边界偶尔不清
表现：
- 有时写“agent 自主执行”
- 有时写“宿主差异通过 adapter 吸收”
- 有时 Claude Code 既像 agent 又像 host harness

问题：
- “宿主”与“agent”不是一个层级，混写会让适配边界不清楚。

建议：
- 宿主：Claude Code / Codex / OpenCode
- agent：在宿主上运行的智能执行体
- adapter：把宿主能力映射到统一研究动作

### 2.3 “工作流 / 流程 / pipeline / stage”交替使用
表现：
- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md` 中有 “research pipeline”
- 其他文档大量用“工作流”“流程”
- RFC 里 `stage` 是状态机阶段，但中文也写“阶段”

问题：
- “工作流”和“阶段”容易被混为一体。

建议：
- workflow = 工作流
- flow/process = 流程
- stage = 阶段
- pipeline 仅在引用外部概念时保留

### 2.4 “计划 / 规划”不统一
表现：
- 大部分地方用“计划”
- 少量地方用“实施规划”“路线图”“规划见…”

问题：
- 语义不算严重冲突，但在系统状态 `planning` 对应中文时最好固定。

建议：
- 系统内术语统一为“计划”
- roadmap 继续叫“路线图”
- implementation plan 叫“实施计划”，少用“实施规划”

### 2.5 “执行层 / 执行平面 / 执行环境 / execution 模块”多层混写
表现：
- RFC 用 `Execution Layer`
- framework 总览里用“执行平面”
- 协议文档里用“执行环境”
- roadmap 又出现代码模块名 `execution`

问题：
- 一个英文词根对应多个架构层面，读者容易混淆。

建议：
- 执行层：架构分层
- 执行平面：系统部署/运行平面
- 执行环境：容器环境
- execution 模块：代码模块，首次出现时显式写“`execution` 模块”

### 2.6 “repo 优先 / 仓库 / Git repo / code repo”不统一
表现：
- `repo 优先`
- `git repo`
- `per-project git repo`
- `代码仓库`
- `source_repo`

问题：
- 有的偏原则，有的偏实现，有的偏 frontmatter 字段。

建议：
- 原则：仓库优先
- 实体：Git 仓库
- 字段：保留 `source_repo`
- 中文正文少直接写 “repo”，除非在术语或代码片段里

### 2.7 “笔记 / 知识库 / Markdown / note”有层次混杂
表现：
- “笔记负责解释、导航和设计”
- “Obsidian 风格文档”
- “Markdown”
- frontmatter 中有 `system-note`、`obsidian-note`

问题：
- “笔记”和“Markdown”不是同一层；“知识库”是集合层。

建议：
- 笔记：单篇文档
- 知识库：文档集合
- Markdown：格式
- Obsidian 笔记：具体风格

### 2.8 “验证 / 校验”未区分技术语义
表现：
- API 参数叫“校验”
- 结构检查也叫“验证”
- roadmap 用“可测试标准”
- 参考映射里还有 `formal verification`

问题：
- 容易在实现文档中混乱。

建议：
- 校验：输入、签名、schema、参数、结构
- 验证：行为、结果、能力、假设
- formal verification：形式化验证

### 2.9 “约束 / 边界 / 合同 / 终止合同”并列但未形成层次
表现：
- “合同边界”
- “终止合同”
- “预算上限/深度上限”
- “工具约束”
- “默认实现约束”

问题：
- 概念上存在层级，但表达还没完全固化。

建议：
- 总称：约束
- 人机授权层：合同边界
- 停机规则层：终止合同
- 资源约束：预算上限/深度上限/时间上限
- 技术实现层：实现约束

---

## 3) 建议统一的中文表达

下面给一个可直接落地的统一术语表。

| 英文/现用词 | 建议统一中文 | 备注 |
|---|---|---|
| AI-Native Research Framework | AI 原生研究框架 | 标题全称可保留英文名 |
| AINRF | AINRF | 缩写不翻译 |
| framework | 框架 | 总体设计层 |
| research system | 研究系统 | 仅在总称场景使用 |
| research engine | 研究引擎 | 运行时/V1 实现层 |
| agent | 智能体 | 正文建议如此；代码名保留 Agent |
| host / host harness | 宿主 / 宿主壳层 | 若要更自然，可只写“宿主” |
| adapter | 适配器 | |
| AgentAdapter | 智能体适配器 | 类名保留原文，正文可译 |
| workflow | 工作流 | 主术语 |
| process / flow | 流程 | 泛称 |
| pipeline | 流水线 | 仅在引用外部概念时使用 |
| stage | 阶段 | 专指状态机阶段 |
| planning | 计划阶段 | RFC 状态名建议固定 |
| plan | 计划 | |
| plan_approval | 计划审批关卡 | 或“计划审批” |
| exploration plan | 探索计划 | |
| reproduction plan | 复现计划 | |
| execution | 执行 | 泛称 |
| Execution Layer | 执行层 | 架构层 |
| execution plane | 执行平面 | 部署/架构视角 |
| execution environment | 执行环境 | 容器环境 |
| executor | 执行器 | 如 SSH 执行器 |
| context | 上下文 | |
| domain_context | 领域上下文 | API 字段中文说明固定 |
| session context | 会话上下文 | |
| memory | 记忆 | |
| session memory | 会话记忆 | |
| persistent memory | 持久记忆 | |
| repo / repository | 仓库 | 正文统一 |
| git repo | Git 仓库 | 实体层 |
| per-project git repo | 每项目 Git 仓库 | |
| repo-first | 仓库优先 | 比“Repo 优先”更一致 |
| notes | 笔记 | 单篇/泛称 |
| knowledge base | 知识库 | 集合层 |
| Markdown note | Markdown 笔记 | 格式+对象 |
| validation | 验证 | 总称偏行为/结果 |
| check / schema validation | 校验 | 输入/结构/签名 |
| acceptance criteria | 可测试标准 | roadmap 已稳定使用 |
| constraints | 约束 | 总称 |
| boundary | 边界 | |
| contract boundary | 合同边界 | 核心概念 |
| termination contract | 终止合同 | 强烈建议保留 |
| budget limit | 预算上限 | |
| depth limit | 深度上限 | |
| time limit | 时间上限 | |

---

## 简短结论

整体上，这组 framework 文档的主术语已经相当稳定，真正需要统一的重点只有三类：

1. “框架 / 研究系统 / 研究引擎”的层级区分  
2. “agent / 宿主 / adapter”的角色区分  
3. “工作流 / 阶段”“验证 / 校验”“约束 / 合同边界 / 终止合同”的概念边界

如果你愿意，我下一步可以继续只读整理成一份更短的“术语规范草案”，输出为可直接贴进文档风格指南的版本。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore architecture docs",
  "description": "find architecture docs",
  "prompt": "只读探索仓库中关于架构、运行时、CLI、agent scaffold 的文档与代码入口，帮助判断 framework 文档需要覆盖哪些实际系统边界。不要修改任何文件。返回：1) 关键文档/代码入口；2) 当前系统实际能力；3) 文档可能失真或过时之处。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a73410a9ffeg82zLw2FH2z08v (for resuming to continue this task if needed)

<task_result>
下面按“当前仓库真实落地”为准，帮助你判断 framework 文档应该覆盖哪些系统边界。

## 1) 关键文档/代码入口

### 约束与总览文档
1. `/Users/kozmosa/code/scholar-agent/PROJECT_BASIS.md`
   - 项目长期边界说明。
   - 明确当前仓库一半是 `docs/` 知识库，一半是 `src/ainrf/` 运行时 scaffold。

2. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
   - 当前最接近“目标系统形态”的规格文档。
   - 但它描述的是目标 V1，不等于已经实现的系统。

3. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
   - 最适合判断“哪些能力是已实现基础设施，哪些仍在后续阶段”。

4. `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
   - 蓝图级系统边界：宿主无关、repo 优先、bounded autonomy。

5. `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
   - 工件边界定义最重要，尤其是 PaperCard / ReproductionTask / ExperimentRun / HumanGate / WorkspaceManifest 等。

6. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
   - 两种模式的目标工作流定义。
   - 但当前代码只落了“任务壳 + gate/API/state”，没有落地 mode workflow。

7. `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
   - 定义容器工作区、per-project repo、同步协议。
   - 这是“设计中的执行数据平面”，与当前仓库实际实现差异很大。

### CLI / 服务入口
8. `/Users/kozmosa/code/scholar-agent/src/ainrf/__main__.py`
   - Python 模块入口，直接进 CLI。

9. `/Users/kozmosa/code/scholar-agent/src/ainrf/cli.py`
   - 当前真实 CLI 入口。
   - 已有：
     - `ainrf --version`
     - `ainrf serve`
     - `ainrf run`（仍是 stub）

10. `/Users/kozmosa/code/scholar-agent/src/ainrf/server.py`
   - 服务启动与 daemon 化入口。
   - `run_server()` 启动 FastAPI + uvicorn
   - `run_server_daemon()` 负责后台进程、pid/log 文件、健康探测

### API / runtime 主入口
11. `/Users/kozmosa/code/scholar-agent/src/ainrf/api/app.py`
   - 当前运行时主装配点。
   - 装配了：
     - `JsonStateStore`
     - `JsonlTaskEventStore`
     - `TaskEventService`
     - `HumanGateManager`
     - API key middleware
     - `/health`、`/tasks` 路由

12. `/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py`
   - 当前“任务系统”最核心入口。
   - 真实暴露了：
     - `POST /tasks`
     - `GET /tasks`
     - `GET /tasks/{id}`
     - `POST /tasks/{id}/cancel`
     - `GET /tasks/{id}/artifacts`
     - `POST /tasks/{id}/approve`
     - `POST /tasks/{id}/reject`
     - `GET /tasks/{id}/events`

13. `/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/health.py`
   - 健康检查入口。
   - 支持“仅 API 健康”或“附加 SSH 容器探测”。

14. `/Users/kozmosa/code/scholar-agent/src/ainrf/api/config.py`
   - 当前服务配置边界非常关键：
     - API key hash
     - state root
     - optional container config
     - gate timeout / SSE 参数
   - 说明系统当前主要是“本地状态目录 + API 服务”。

### 状态、工件、事件、gate 核心模块
15. `/Users/kozmosa/code/scholar-agent/src/ainrf/state/store.py`
   - 当前真实持久化边界。
   - 所有任务和工件写到本地 `.ainrf/` JSON 文件，不是容器内 per-project repo。

16. `/Users/kozmosa/code/scholar-agent/src/ainrf/state/models.py`
   - 当前任务状态机真实字段定义：
     - `TaskStage`
     - `TaskMode`
     - `TaskRecord`
     - `TaskCheckpoint`

17. `/Users/kozmosa/code/scholar-agent/src/ainrf/artifacts/models.py`
   - 当前已落地的工件 schema。
   - 是 framework 文档与真实代码对齐时最重要的代码依据之一。

18. `/Users/kozmosa/code/scholar-agent/src/ainrf/gates/manager.py`
   - 当前人工关卡系统真实边界。
   - 包含：
     - waiting/approve/reject/cancel
     - yolo auto-approve
     - webhook dispatch
     - overdue reminder
     - runtime secret registry

19. `/Users/kozmosa/code/scholar-agent/src/ainrf/events/models.py`
20. `/Users/kozmosa/code/scholar-agent/src/ainrf/events/store.py`
21. `/Users/kozmosa/code/scholar-agent/src/ainrf/events/service.py`
   - 当前 SSE/event sourcing 的真实边界。
   - 事件已落本地 JSONL，SSE 从这里回放/跟随。

### 执行层 / 解析层入口
22. `/Users/kozmosa/code/scholar-agent/src/ainrf/execution/ssh.py`
   - 当前已实现的 SSH 执行器，能力其实不弱。
   - 但它尚未被 task runtime 编排接起来。

23. `/Users/kozmosa/code/scholar-agent/src/ainrf/execution/models.py`
   - `ContainerConfig`、`CommandResult`、`ContainerHealth` 的真实契约。

24. `/Users/kozmosa/code/scholar-agent/src/ainrf/parsing/mineru.py`
   - 当前 MinerU client 已有完整 provider 交互逻辑与缓存。
   - 但还没有接入 `/tasks` 的实际执行链。

25. `/Users/kozmosa/code/scholar-agent/src/ainrf/parsing/contracts.py`
   - `PaperParser` 协议说明解析层抽象是存在的。

### 测试作为“实际能力证据”
26. `/Users/kozmosa/code/scholar-agent/tests/test_cli.py`
27. `/Users/kozmosa/code/scholar-agent/tests/test_api_tasks.py`
28. `/Users/kozmosa/code/scholar-agent/tests/test_api_events.py`
29. `/Users/kozmosa/code/scholar-agent/tests/test_api_health.py`
30. `/Users/kozmosa/code/scholar-agent/tests/test_server.py`
31. `/Users/kozmosa/code/scholar-agent/tests/test_execution_ssh.py`
32. `/Users/kozmosa/code/scholar-agent/tests/test_parsing_mineru.py`

这些测试基本能证明：当前真实系统是“API + 本地状态 + gate + SSE + SSH/MinerU 独立模块”，不是完整 research engine。

---

## 2) 当前系统实际能力

我把“已实现能力”按实际系统边界收敛为 4 层。

### A. 当前真正可运行的产品形态：本地 API 服务 + CLI 外壳
真实已落地的是一个小型 orchestrator control plane，而不是完整 research runtime。

#### 已有能力
- CLI 可启动服务：
  - `/Users/kozmosa/code/scholar-agent/src/ainrf/cli.py`
  - `/Users/kozmosa/code/scholar-agent/src/ainrf/server.py`
- 支持 daemon 模式，写 pid/log 到 `.ainrf/runtime/`
- 可通过 `python -m ainrf` 进入

#### 当前边界
- `ainrf run` 还是明确 stub
- CLI 不是 REST client，也没有 task submit/watch 的完整用户流
- 当前“可用产品”本质上是 API 服务器，不是 end-to-end 研究 agent

### B. 当前真实 control plane：任务记录 + 人工关卡 + 事件流
这是仓库里最完整的一块。

#### 1) 任务创建与查询
`/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py`

已支持：
- 创建 task
- 查询 task 列表/详情
- 查询关联 artifacts
- cancel task
- approve/reject 当前 gate
- 订阅 task event stream

#### 2) 任务状态模型
`/Users/kozmosa/code/scholar-agent/src/ainrf/state/models.py`

当前真实阶段：
- `submitted`
- `ingesting`
- `planning`
- `gate_waiting`
- `executing`
- `completed`
- `failed`
- `cancelled`

但要注意：
- 这些状态值虽然定义了，真实 API 流程只实际走到了少数阶段
- 目前 `POST /tasks` 创建后，主要进入：
  - `gate_waiting`，或
  - yolo 时直接 `planning`

也就是说：状态机“词汇表”比实际执行链更完整。

#### 3) 人工关卡系统
`/Users/kozmosa/code/scholar-agent/src/ainrf/gates/manager.py`

已实现的真实行为：
- intake gate 创建
- waiting/approved/rejected/cancelled 生命周期
- yolo 自动审批
- webhook 发送
- 超时 reminder sweep
- secret 只保留在 runtime registry，不落盘

这意味着 framework 文档必须覆盖的真实边界至少包括：
- task-scoped human gate
- webhook 通知与签名
- runtime-only secret
- gate timeout / reminder 机制
- reject 后的阶段回退/失败策略

#### 4) SSE/事件流
- `/Users/kozmosa/code/scholar-agent/src/ainrf/events/store.py`
- `/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py`

已实现：
- append-only JSONL 事件存储
- SSE 历史回放
- `Last-Event-ID` 断点恢复
- `?types=` 类别过滤
- keepalive
- terminal task 自动结束流

当前真实事件类别：
- `task`
- `artifact`
- `gate`
- `experiment`
- `log`

但真实已被发出的主要是：
- task stage change / terminal
- artifact create/update
- gate waiting/resolved/reminder

`experiment` / `log` 类别目前更像预留，不是实际执行系统输出。

### C. 当前真实持久化边界：本地 `.ainrf/` 文件状态，而不是容器 repo
这是 framework 文档很容易写失真的地方。

#### 真实实现
`/Users/kozmosa/code/scholar-agent/src/ainrf/state/store.py`

当前数据落地在本地 state root：
- `.ainrf/tasks/*.json`
- `.ainrf/events/*.jsonl`
- `.ainrf/artifacts/...`
- `.ainrf/indexes/artifact-links.json`

特点：
- JSON 文件持久化
- 原子写入
- 文件锁
- artifact relation index
- 任务 resume/list resumable

#### 实际意义
当前系统的 source of truth 在 orchestrator 本地 state 目录，而不是：
- 容器内项目 repo
- 数据库
- 远程对象存储

所以 framework 文档如果要描述“实际系统边界”，必须把以下两个层分开：
1. 当前已落地的 control-plane state store：`.ainrf/`
2. 未来设计中的 execution data plane：容器 per-project repo

### D. 当前已实现但尚未接入任务主链的能力：SSH 执行器与 MinerU 解析器
这两块不是空文档，代码和测试都很实。

#### 1) SSH 执行器
- `/Users/kozmosa/code/scholar-agent/src/ainrf/execution/ssh.py`
- `/Users/kozmosa/code/scholar-agent/tests/test_execution_ssh.py`

已具备：
- asyncssh 连接
- 自动重连
- 远程命令执行
- cwd/env 注入
- 超时终止
- SFTP 上传下载
- 大文件 rsync 优先
- Claude Code 检查/安装
- container ping/health probe

但当前只在 `/health` 中真正用到了 `SSHExecutor.ping()`。
还没有：
- 从 task 执行链里调用 `run_command`
- 真正执行 atomic task
- 真正创建/维护 container workspace

#### 2) MinerU 解析器
- `/Users/kozmosa/code/scholar-agent/src/ainrf/parsing/mineru.py`
- `/Users/kozmosa/code/scholar-agent/tests/test_parsing_mineru.py`

已具备：
- provider 提交与轮询
- 本地文件上传 / remote URL 提交
- 结果下载与 archive 解包
- Markdown 结构校验
- 缓存
- 失败分类

但当前并未接入：
- `POST /tasks`
- task stage `ingesting`
- PaperCard 自动生成

### E. 当前工件层真实能力
`/Users/kozmosa/code/scholar-agent/src/ainrf/artifacts/models.py`

当前真实已定义工件：
- `PaperCard`
- `ReproductionTask`
- `ExperimentRun`
- `EvidenceRecord`
- `Claim`
- `ExplorationGraph`
- `QualityAssessment`
- `WorkspaceManifest`
- `HumanGate`

已实现工件状态转换的主要是 lifecycle artifacts。

但当前“真实在运行中被创建和操作”的主要只有：
- `HumanGate`
- 少量测试中手工构造的 `PaperCard`

也就是说：
- schema 已先行
- runtime 编排尚未让大多数 artifact 真正活起来

---

## 3) 文档可能失真或过时之处

下面是我认为最需要警惕的失真点，按严重程度排序。

### 1. 文档把“目标系统”写成了“当前系统”
最核心失真。

#### 文档倾向
`/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
和
`/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`

描述的是：
- 完整 TaskEngine
- Mode 1 / Mode 2 工作流
- ingest -> planning -> executing
- agent 驱动实验、生成工件、归档报告

#### 代码现实
当前没有：
- TaskEngine
- AgentAdapter 抽象实现
- ClaudeCodeAdapter
- 实际 task queue / sequential executor
- Mode 1/Mode 2 workflow runner
- budget enforcement
- PaperCard 自动生成链
- ExperimentRun 执行链
- ExplorationGraph/QualityAssessment 生成链

所以 framework 文档如果要覆盖“实际系统边界”，必须明确分层：
- 已实现 control plane
- 已实现但未接线的 infra modules
- 尚未实现 orchestration/runtime

否则读者会误以为现在已是一个可执行的 research engine。

---

### 2. RFC 中的三层架构，当前只真正落了 API 层 + 一小部分 Core
#### 文档说
- API Layer
- Orchestrator Core（TaskEngine + StateStore + GateManager）
- Execution Layer（SSH Executor + Agent Adapter）

#### 实际上
当前落地程度更准确地说是：
- API Layer：已落地
- Core：
  - `StateStore`：已落地
  - `GateManager`：已落地
  - `TaskEventService`：已落地
  - `TaskEngine`：未落地
- Execution Layer：
  - `SSHExecutor`：已落地为独立模块
  - `AgentAdapter`：未落地
  - Claude Code runtime integration：未落地

所以架构文档需要把“已实现核心”缩写成：
- API control plane
- local JSON state/event store
- human gate subsystem
- pluggable but not yet orchestrated execution/parsing adapters

---

### 3. “REST 服务是 V1 正确形态”基本成立，但 CLI 仍非常薄
#### 现实
- `serve` 已是真实入口
- `run` 仍是 stub
- 没有 CLI 客户端化能力，如 submit/watch/approve/list

所以如果 framework 文档讲“CLI 是 REST client”，目前会偏超前。
当前更准确表述应是：
- CLI 目前主要是服务进程入口和未来运行入口占位
- 不是完整交互面

---

### 4. 任务状态机文档比真实执行链完整很多
RFC 写了完整：
- `submitted -> ingesting -> planning -> gate_waiting -> executing -> completed/failed`

但当前 API 真实路径里：
- `POST /tasks` 直接创建本地任务记录
- 然后触发 intake gate
- 非 yolo 进入 `gate_waiting`
- yolo 进入 `planning`

没有真实 ingesting/executing 逻辑。
因此 framework 文档应该区分：
- 状态机 vocabulary
- 当前已连接的 transitions
- 未来预留 transitions

---

### 5. SSE 事件命名与文档示例已有偏差
#### 文档示例倾向
- `task.gate_waiting`
- `task.artifact_created`
- `task.progress`
- `task.log`

#### 当前代码真实发出的事件
在 `/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py`
和
`/Users/kozmosa/code/scholar-agent/src/ainrf/gates/manager.py`

主要是：
- `task.stage_changed`
- `task.completed`
- `task.failed`
- `task.cancelled`
- `artifact.created`
- `artifact.updated`
- `gate.waiting`
- `gate.resolved`
- `gate.reminder`

这说明事件模型文档需要按代码校正，否则客户端会按错事件名实现。

---

### 6. P6 路线图中的事件类型描述部分已部分过时
`/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`

P6 写的是：
- `gate.pending`
- `artifact.created`
- `log.info` / `log.warning` / `log.error`
- `experiment.started` / `experiment.completed`

但当前实现中：
- 没有 `gate.pending`，而是 `gate.waiting`
- 没有 `log.*` 真实事件生产
- 没有 experiment runtime 事件生产

所以 roadmap 若被当成“当前 contract”，会误导实现者。

---

### 7. 工件文档中有些对象在代码里未落地或已降级
#### 典型例子
`/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
提到：
- `ResearchProject`
- `AgentAdapter` 作为一等工件

但当前代码里：
- 没有 `ResearchProject` model
- `AgentAdapter` 不是 artifact model，只是 roadmap/RFC 中的未来抽象
- 当前 artifact union 不包含它们

因此 framework 文档需要把：
- “理论一等对象”
- “当前代码中已落地可持久化 artifact”
分开写。

---

### 8. “repo 优先 / per-project git repo 是 source of truth”与当前实现不一致
这是另一个关键失真。

#### 文档说
- 容器上的 per-project git repo 是 source of truth
- workspace / experiments / reports / artifacts 都在容器项目目录中

#### 当前实现说
- `JsonStateStore` 把任务和工件写到本地 `.ainrf/`
- `JsonlTaskEventStore` 把事件写到本地 `.ainrf/events`
- 没有 project repo 初始化逻辑
- 没有 workspace manifest 自动维护链
- 没有 git sync/push integration

更准确的文档边界应是：
- 当前 source of truth：orchestrator local state root
- 未来 execution data plane：container project repo
- 两者如何映射，尚未实现

---

### 9. “计划关卡”在设计上存在，在产品流里并未自动触发
当前 gate manager 确实支持：
- `GateType.INTAKE`
- `GateType.PLAN_APPROVAL`

也支持 plan approval 被 reject 多次后 fail。

但当前 API 自动触发的只有 intake gate：
- `POST /tasks` 里只创建 intake gate

没有真实“生成计划 -> 触发 plan_approval gate”的 runtime。
因此：
- 文档不应写成“系统已经有两道真实可跑的关卡流”
- 更准确是：当前 runtime 只接通了 intake gate；plan gate 机制已具备底层支持，但未接入编排主链

---

### 10. Budget 在 schema 中存在，但没有真实 enforcement
当前请求 schema中有 budget：
- `/Users/kozmosa/code/scholar-agent/src/ainrf/api/schemas.py`

TaskRecord 中也有：
- `budget_limit`
- `budget_used`

但当前系统没有：
- budget 消耗累计逻辑
- 阈值判停
- budget 触发 terminal event

所以关于“预算边界自治”的 framework 文档应标注为设计目标，而非当前能力。

---

### 11. Health endpoint 的真实边界比文档更保守
当前 `/health` 实际行为：
- 未配置容器时，只返回 API ok
- 配置容器时，调用 SSH ping，可能返回 degraded/503

这意味着当前 health 不是“整个 research engine 健康”，而只是：
- API 服务健康
- 可选的 container SSH/Claude/env 探测

framework 文档若将其表述为“编排器整体健康”会过宽。

---

## 结论：framework 文档现在最应该覆盖的“实际系统边界”

如果你的目标是让 framework 文档贴近仓库现实，我建议至少明确这 6 个边界层：

1. **Control plane 已落地**
   - FastAPI service
   - API key auth
   - task CRUD-like endpoints
   - health endpoint
   - daemon serve

2. **State boundary 已落地**
   - local `.ainrf/` JSON/JSONL state
   - tasks / artifacts / events / indexes
   - webhook_secret 不落盘

3. **Human gate boundary 已落地**
   - intake gate fully wired
   - plan gate partially supported at model/manager level
   - webhook + reminder + yolo

4. **Observability boundary 已落地**
   - append-only event log
   - SSE replay/follow
   - Last-Event-ID + category filter

5. **Infra adapters 已落地但未接编排**
   - SSHExecutor
   - MinerUClient
   - container health probe

6. **Research runtime/orchestration 未落地**
   - TaskEngine
   - AgentAdapter / ClaudeCodeAdapter
   - Mode 1 / Mode 2 workflow
   - actual parsing -> planning -> execution pipeline
   - budget enforcement
   - per-project repo data plane

如果你愿意，我下一步可以基于以上发现，进一步给你整理一版“framework 文档应如何改写为：已实现 / 部分实现 / 未来设计”三栏对照表。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore worklog constraints",
  "description": "check worklog rules",
  "prompt": "只读检查 docs/LLM-Working/ 与工作日志约束，确认后续真正执行文档更新时需要记录哪些内容。不要修改任何文件。返回：1) 今日 worklog 是否已存在；2) 记录格式要求；3) 与本次 docs 更新相关的注意事项。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a73410a2ffe18fNpev2kVDZaC (for resuming to continue this task if needed)

<task_result>
已做只读检查，未修改任何文件。

1) 今日 worklog 是否已存在

不存在。

按今天日期 `2026-04-04`，应对应的文件路径是：

- `/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md`

当前在 `docs/LLM-Working/worklog/` 下只看到：

- `/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-03-15.md`
- `/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-03-16.md`

所以后续一旦开始“真正执行”文档更新，按仓库规则应先创建今天的 worklog 文件，再在同一天内持续追加。

2) 记录格式要求

综合 `/Users/kozmosa/code/scholar-agent/AGENTS.md` 与 `/Users/kozmosa/code/scholar-agent/PROJECT_BASIS.md`，worklog 约束如下：

- 位置固定在：
  - `/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/`
- 文件名固定为：
  - `YYYY-MM-DD.md`
- 同一天只用一个文件，持续追加，不要分散到多个文件。
- 记账粒度是：
  - “每个已完成的修改计划 / 工作批次一条”
  - 不是每个原子动作一条
  - 不要把 edit、validation、commit 拆成流水账
- 每条 changelog 至少要包含：
  - 时间
  - 批次名 / 计划名
  - 实际改动摘要
  - 验证结论
- 如果该批次产生 commit，还要在同一条末尾补充：
  - commit hash
  - commit 首行 / subject
- 内容要求：
  - 总结“这一批完成了什么、影响了哪些部分、验证结果如何”
  - 不要只复述 commit message
  - 不要把 worklog 写成提交标题或原子切片标签的简单转录
- 历史维护方式：
  - append-only
  - 不要静默重写旧记录，除非是纠正客观事实错误

可参考的推荐格式类似：

- `2026-04-04 14:30 docs-planning：完成 xxx 文档更新，调整了 yyy，并补充 zzz 链接；执行 <验证命令> 成功。`
- 若有提交：
  - `2026-04-04 14:30 docs-planning：完成 xxx 文档更新，调整了 yyy，并补充 zzz 链接；执行 <验证命令> 成功；关联提交：abcd123 docs: ...`

3) 与本次 docs 更新相关的注意事项

结合仓库长期约束，后续真正做 docs 更新时，建议特别注意：

- 本次你现在这一步是只读检查，不属于实际修改。
  - 因此当前不需要补写 worklog。
  - 但一旦开始真实文档编辑、验证或提交，就应同步记录到今日文件：
    - `/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md`

- 如果今天的 worklog 文件不存在，开始实际工作时应先创建它。
  - 这是 `AGENTS.md` 明确要求的。

- 文档放置位置要分清：
  - 长期知识库内容放在 `docs/` 下合适子目录
  - 会话日志、实现复盘、计划、checklist、agent 中间产物放在：
    - `/Users/kozmosa/code/scholar-agent/docs/LLM-Working/`

- 文档书写规范要保持：
  - 文件名用英文 slug
  - 正文以中文为主
  - 优先使用 Obsidian wikilink，例如 `[[framework/v1-rfc]]`
  - 笔记类文档要求有 YAML frontmatter，并保持能被站点构建稳定处理的 Markdown 结构

- 不要直接编辑生成产物：
  - `/Users/kozmosa/code/scholar-agent/site/`
  - `/Users/kozmosa/code/scholar-agent/.cache/html-notes/`

- 若本次 docs 更新属于一个完整工作批次，worklog 中应把以下信息合并成一条总结：
  - 更新了哪些文档
  - 改动目的/影响范围
  - 做了什么验证
  - 验证是否通过

- 若本次 docs 更新伴随验证，优先记录实际执行的验证结果。
  - 文档相关常见验证命令依据仓库约定通常是：
    - `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build`
  - 如果这次只是改 `LLM-Working` 内部工作文档，也仍建议在 worklog 里写明是否做了检索/构建/链接回扫等验证。

- 如果此次更新涉及 `LLM-Working` 下的计划文档或实现文档，已有惯例是：
  - 在相关规划文档、实现文档、roadmap 之间补回链
  - 并在 worklog 中记录这批文档闭环和验证情况

如果你愿意，我下一步可以继续只读帮你整理一份“适用于今天 docs 更新的 worklog 模板”，直接按本仓库风格给出可复制文本。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore existing english quality",
  "description": "review english phrasing",
  "prompt": "只读查看 scholar agent framework 文档中现有英文标题、英文短语、双语表达、术语命名，评估是否需要改成更自然的英文表达。不要修改任何文件。返回：1) 英文表达问题类型；2) 代表性例子路径；3) 总体改写建议。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a734109dffdil1quPNSyGzA9G (for resuming to continue this task if needed)

<task_result>
下面是对 `scholar agent framework` 文档中现有英文标题、英文短语、双语表达、术语命名的只读评估。未修改任何文件。

## 1) 英文表达问题类型

### A. 中式直译或“概念对、英语不够自然”
这类表达技术上能懂，但不太像英文母语技术文档会自然写出的说法。

常见表现：
- `bounded-autonomous research evidence engine`
- `repo 优先 / Repo 优先`
- `citation discipline`
- `review gate`
- `human-on-the-loop`
- `paper intake`

判断：
- 多数不是“错误英文”，而是“能懂但不够 idiomatic”。
- 适合改成更常见的产品/架构英语，如 `repository-first`, `citation rigor`, `review checkpoint`, `human-in-the-loop`, `paper ingestion`。

---

### B. 术语风格不统一：同一概念混用不同英文层级
同一个概念在不同文档里，有时是产品名风格，有时是工程实现名风格，有时是口语缩写。

常见表现：
- `Mode 2 Deep Repro` 与 `Deep Reproduction`
- `Lit Exploration` 与 `Literature Exploration`
- `Human Gate` / `GateManager` / `gate_waiting`
- `daemon` / `service` / `orchestrator`
- `source of truth` / `Source of truth`

判断：
- 对内部草案无伤大雅，但对框架文档会削弱术语体系感。
- 尤其标题、路线图、RFC、图示节点里的术语建议统一为一套正式命名。

---

### C. 缩写过猛，像内部便签，不像正式框架文档
在 roadmap / 图表 /阶段标题里，存在为省空间而压缩的英文。

常见表现：
- `Deep Repro`
- `Lit Exploration`
- `per-project`
- `per-table`

判断：
- `per-project`、`per-table` 在正文中可以接受；
- 但 `Deep Repro`、`Lit Exploration` 更像内部 shorthand，不适合作为长期对外文档标题或主标签。

---

### D. 双语混排时，英文 register 不一致
有些句子主体是中文，但嵌入的英文有的偏正式、有的偏口语、有的偏内部黑话。

常见表现：
- `API-first`
- `yolo mode`
- `nightly loop`
- `daemon bus`
- `resume continuity`

判断：
- 如果目标是“设计文档 + RFC”，嵌入英文最好分两类：
  1. 标准行业术语：保留英文
  2. 项目内自造词/口语词：改成更规范的说法，或第一次出现时附中文解释

---

### E. 标题层级中英文结构不完全协调
有些标题是“英文主标题 + 中文副标题”，有些是“中文主标题 + 英文术语点缀”，风格未完全收敛。

常见表现：
- `# AINRF V1 RFC：有界自治研究引擎实现规格`
- `# AINRF V1 Roadmap：实现路线图`
- `# AI-Native Research Framework：有界自治研究系统蓝图`
- `# 容器工作区协议`

判断：
- 单篇看没问题，但整组 framework 文档放在一起时，命名系统略显混搭。
- 建议选一种长期策略：
  - 要么“英文主标题 + 中文说明”
  - 要么“中文主标题 + 英文别名”
  - 不要混用太多模式。

---

### F. 个别表达接近“自造英文”
这类最值得优先改，因为读者会停顿一下。

代表：
- `human-on-the-loop`
- `bounded-autonomous research evidence engine`
- `citation discipline`（语义可猜，但搭配不自然）
- `resume continuity`

判断：
- 这些不算完全错误，但明显不像成熟英文产品文档里的稳定表达。

---

## 2) 代表性例子路径

下面列代表性文件与典型问题点。

### 1. `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
代表问题：
- `research pipeline`
- `repo 优先`
- `bounded-autonomous research evidence engine`
- `nightly loop`
- `review`

评估：
- 这是核心愿景文档，英文术语最值得统一。
- `bounded-autonomous research evidence engine` 概念上很强，但英文不够自然，建议重写。

---

### 2. `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
代表问题：
- `citation discipline`
- `integrity`
- `review gate`
- `human-on-the-loop`
- `daemon bus`
- `resume continuity`

评估：
- 这一篇最明显地出现“半术语、半口语、半内部 shorthand”的英文。
- 适合做一轮术语清洗，统一成更像分析报告的英语。

---

### 3. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
代表问题：
- `Mode 2 Deep Repro`
- `Mode 1 Lit Exploration`
- `FastAPI Service & Auth`
- `Human Gate & Webhook`
- `Agent Adapter & Engine`

评估：
- roadmap 标题需要短，但也要正式。
- `Deep Repro`、`Lit Exploration` 太像白板 shorthand，建议改为完整形式。

---

### 4. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
代表问题：
- `API-first`
- `yolo mode`
- `task.gate_waiting`
- `per-table`
- `source of truth`

评估：
- RFC 主体整体英文相对最稳。
- 问题主要不是语法，而是 register：正式 RFC 中夹入 `yolo mode` 这种口语词，会显得不够稳重。
- 若保留，也建议明确标为内部 flag 名，而不是叙述性术语。

---

### 5. `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
代表问题：
- `Source of truth`
- `source of truth`
- `Repo 优先的数据平面`
- `per-project git repo`

评估：
- 英文基本可懂，但大小写、术语风格和中文标题内嵌英文的协调度还可再提升。

---

### 6. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
代表问题：
- `Paper intake`
- `per-table`
- `baseline`
- `full-suite`

评估：
- 这里的问题较轻。
- `Paper intake` 更自然的工程说法通常是 `paper ingestion`。
- `baseline`、`full-suite`、`per-table` 在 ML / systems 语境中都可接受。

---

### 7. `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
代表问题：
- 标题别名是 `AI-Native Research Framework 索引`
- 整篇中“中文主体 + 英文框架名”的风格是统一的，但与其他文档中更重英文标题的写法不完全一致。

评估：
- 不是措辞错误，属于命名体系一致性问题。

---

## 3) 总体改写建议

### 总体结论
需要改，但不是“大面积英文有错”，而是“框架文档已进入较成熟阶段，现有英文表达值得做一轮术语规范化和自然化”。  
优先级属于：中高。

核心原因：
1. 文档已经不只是个人笔记，而是在承担 framework / RFC / roadmap 的长期命名职责；
2. 现有英文多数“可理解”，但有不少地方带有中文思维直译、内部 shorthand、口语 flag 名外溢的问题；
3. 若后续要对外展示、做站点导航、或沉淀成 API / 架构词表，越早统一越省成本。

---

### 建议一：建立一份小型术语表，先统一再改文案
建议先固定下面几类词的标准写法：

#### 推荐统一方向
- `repo-first` 或 `repository-first`
  - 不建议继续混用“repo 优先”
- `human-in-the-loop`
  - 不建议 `human-on-the-loop`
- `paper ingestion`
  - 不建议 `paper intake`
- `Deep Reproduction`
  - 不建议标题里用 `Deep Repro`
- `Literature Exploration`
  - 不建议标题里用 `Lit Exploration`
- `source of truth`
  - 统一小写，除非句首
- `citation rigor` 或 `citation-grounded synthesis`
  - 比 `citation discipline` 更自然
- `review checkpoint` / `approval checkpoint`
  - 比 `review gate` 更自然，除非你明确要把 `Gate` 作为框架一级术语
- `resumability` / `resume support`
  - 比 `resume continuity` 更自然

---

### 建议二：区分“产品术语”和“实现字段名”
例如：
- 可以保留实现字段/事件名：
  - `gate_waiting`
  - `task.gate_waiting`
  - `yolo`
- 但叙述性正文中建议写成更自然的英文：
  - `waiting for approval`
  - `approval-pending state`
  - `automatic approval mode`

也就是说：
- 代码名保持原样
- 说明文档使用自然语言解释  
这样最稳。

---

### 建议三：标题不要过度缩写
尤其是：
- `Deep Repro`
- `Lit Exploration`

更适合只出现在图示框、小表格窄列、临时计划里；  
不适合作为长期主标题、路线图阶段名、站点导航名。

---

### 建议四：对“自造大词”降一点抽象度
比如：
- `bounded-autonomous research evidence engine`

这个短语虽然有辨识度，但过于密、过于“概念堆叠”。  
更自然的方向通常是：
- `a bounded-autonomy research system`
- `a research execution system with bounded autonomy`
- `an evidence-driven research system`

也就是：
- 少一点 slogan 式压缩
- 多一点稳定、易复用、易传播的表述

---

### 建议五：为双语文档选定一种标题策略
建议二选一：

#### 方案 A：英文主标题 + 中文副标题
例如保持这种风格：
- `AI-Native Research Framework: Blueprint for a Bounded-Autonomy Research System`

优点：
- 对外展示更统一
- 便于以后站点英文导航/分享

#### 方案 B：中文主标题 + 英文 alias
例如：
- 标题用中文
- frontmatter alias 固定英文正式名

优点：
- 更符合“正文中文为主”的仓库现状

目前仓库是两种模式并存，建议收敛成一种。

---

### 建议六：哪些词可以保留，不必强行改
以下词在当前语境里基本自然，可保留：
- `FastAPI`
- `Artifact Model`
- `State Store`
- `Agent Adapter`
- `Task Engine`
- `SSE Streaming`
- `baseline`
- `full-suite`
- `API-first`
- `per-table`
- `per-project`

其中 `API-first`、`per-table`、`per-project` 虽不算最口语自然，但在技术文档里可接受。

---

## 简短结论

如果只给一句总评：

这组 framework 文档的英文总体“可读、可懂、概念清楚”，但存在一批“技术上没错、语感上不够自然”的表达，尤其集中在愿景表述、映射分析、路线图缩写和双语混排术语上。最值得优先处理的是：`human-on-the-loop`、`bounded-autonomous research evidence engine`、`citation discipline`、`Deep Repro`、`Lit Exploration`、`paper intake` 这类表达。

如果你愿意，我下一步可以继续只读整理一份“建议替换表（原词 -> 更自然英文）”，按文件分组列出，不修改任何文件。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore ai scientist workflow",
  "description": "study workflows",
  "prompt": "只读探索 Awesome-AI-Scientist 参考仓库里与研究工作流、idea generation、experiment loop、review loop、paper/report production 相关内容。不要修改任何文件。返回：1) 工作流步骤；2) 可迁移到 scholar agent framework 的抽象层；3) 风险点。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a7341080ffdVZJjwkU1dwOGaT (for resuming to continue this task if needed)

<task_result>
以下是对 Awesome-AI-Scientist 参考仓库的只读探索结论。先说明边界：

- 这个参考仓库本身不是可运行系统，而是一个“AI Scientist 生态资源清单/知识库”，核心内容集中在 README 的分类法与项目索引。
- 因此我能提炼出的“工作流”主要是它所隐含的研究自动化阶段模型，而不是某个仓库里的具体 agent 执行图。
- 我没有修改任何文件。

参考文件：
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/README.md`
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/AGENTS.md`
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/CONTRIBUTING.md`

## 1) 工作流步骤

基于 README 的顶层结构与“Research Automation Stack”，这个仓库隐含的研究工作流可以抽象为：

### A. Knowledge Acquisition / Knowledge Building
对应 README 中：
- `# 📚 1. Knowledge Acquisition`
- `#### 1.2.1. Literature Search and Curation`
- `#### 1.2.2. Knowledge Retrieval and Summarization`

可归纳为：
1. 文献搜索与收集  
   - 检索相关论文、项目、数据源、基准。
2. 知识整理与筛选  
   - 去重、分类、聚合、按主题组织。
3. 检索增强与总结  
   - 对文献进行摘要、对比、结构化提取。
4. 建立问题空间  
   - 识别研究空白、已有方法边界、值得推进的方向。

这是整个研究循环的输入层。

### B. Idea Generation
对应 README 中：
- `# 💡 2. Idea Generation`
- `### 2.1. Methods`
- `### 2.2. Evaluation`

可归纳为：
5. 假设/idea 生成  
   - 从知识库中提出研究问题、假设、方法组合、创新点。
6. novelty/diversity 约束下的候选扩展  
   - 不是只生成一个点子，而是生成多个候选并比较新颖性、可行性、多样性。
7. idea 评审与筛选  
   - 使用人工/模型/基准对 idea 进行可行性、创新性、价值判断。

这是“从知识到 proposal”的阶段。

### C. Verification / Experiment Loop
对应 README 中：
- `# 🔬 3. Verification and Falsification`
- `### 3.1. Methods`
- `### 3.2. Evaluation`

可归纳为：
8. 实验设计  
   - 将 idea 落成任务、方法、数据、代码、实验设置。
9. 执行验证或证伪  
   - 跑实验、复现实验、调用仿真/代码环境、收集结果。
10. 结果分析  
   - 比较基线、定位失败模式、判断是否支持原假设。
11. 迭代修正  
   - 基于结果回到 idea、计划、实现层继续修正。

这里最重要的不是“一次跑通”，而是 falsification + iteration。

### D. Review Loop
对应 README 中：
- `# ⚖️ 4. Review System`
- `### 4.1. Methods`
- `### 4.2. Evaluation Benchmarks`

可归纳为：
12. 生成内部评审/同行评审意见  
   - 对论文草稿、实验设计、论证链、引用充分性、表达清晰度进行审查。
13. 基于 review 发现问题  
   - 找逻辑漏洞、证据不足、实验不充分、引用缺失、表述不严谨。
14. 驱动新一轮修改  
   - review 不只是输出评论，而是反向推动 idea、experiment、writing 的再迭代。

这在该仓库中是被明确当作一个独立核心层的，而非附属步骤。

### E. Paper / Report Production
README 没有单独列顶级章节，但在“Research Automation Stack”里明确有：
- `Paper Writing`
- Featured Projects 中有 `AutoSurvey`, `PaperRobot`, `CycleResearcher`

可归纳为：
15. 研究结果结构化表达  
   - 生成摘要、方法、实验、图表、引用。
16. 报告/论文初稿生成  
   - 形成论文、survey、report、project summary。
17. 格式与论证完善  
   - 检查引用、结构、表达、一致性。
18. 与 review loop 联动  
   - 被评审后继续修改，直至输出可提交版本。

### F. Evolution / Closed-loop Research
对应 README 中：
- `# 📈 5. Evolution`
- `#### 5.1.1. Dynamic Planning`
- `#### 5.1.2. Autonomous Learning`

可归纳为：
19. 动态规划  
   - 研究过程中根据新结果动态改写计划，而不是固定流水线。
20. 自反馈/自学习  
   - 用历史失败、评审意见、实验结果来更新下一轮策略。
21. 开放式持续研究  
   - 从单次任务，转向持续迭代的研究代理系统。

一句话总结这个仓库隐含的总流程：

知识获取 -> idea generation -> experiment/verification -> review -> paper/report production -> 基于反馈继续演化

---

## 2) 可迁移到 scholar agent framework 的抽象层

对 scholar-agent 来说，最值得迁移的不是具体论文列表，而是它背后的“阶段分层 + 循环关系”。

### 抽象层 1：Research Lifecycle State Machine
可将整个框架设计成显式状态机：

- knowledge_building
- idea_generation
- experiment_design
- experiment_execution
- result_analysis
- review
- writing
- revision
- archive/publish

价值：
- 比“一个大而全 agent”更清晰
- 每个状态可以配置不同工具、输入、输出
- 更适合追踪 worklog、artifact lineage、可恢复执行

### 抽象层 2：Artifact-Centered Architecture
把研究过程中的产物当作一等公民，而不是把流程只建模成 prompt 链。

建议 artifact 类型：
- literature_set
- structured_notes
- problem_statement
- idea_card
- experiment_plan
- run_record
- result_summary
- review_report
- paper_draft
- revision_patch

价值：
- 方便版本化、可追溯、可评审
- 便于把 docs/knowledge 与 runtime 结合
- 很契合你们仓库当前“文档知识库 + Python runtime scaffold”的双轨结构

### 抽象层 3：Loop as First-Class Primitive
该参考仓库非常强调这些 loop：

- idea loop
- experiment loop
- review loop
- autonomous learning loop

对 scholar-agent 建议显式建模：
- propose -> critique -> refine
- design -> run -> analyze -> revise
- draft -> review -> rebut/refine -> redraft

价值：
- 研究不是线性流水线
- “循环的终止条件”可单独控制，如预算、质量阈值、novelty 阈值、review score 阈值

### 抽象层 4：Evaluator Layer
README 多处有 `Evaluation` / `Evaluation Benchmarks`，说明“生成能力”和“评估能力”要分层。

可迁移为统一 evaluator 接口：
- novelty evaluator
- feasibility evaluator
- experimental rigor evaluator
- writing quality evaluator
- review quality evaluator
- risk/safety evaluator

价值：
- 让生成模块和评估模块解耦
- 便于替换 judge：rule-based / LLM-based / benchmark-based / human-in-the-loop

### 抽象层 5：Planner vs Worker Separation
从 “Dynamic Planning / Autonomous Learning / Multi-agent team” 这些分类可以推出来：

- planner：决定下一步做什么
- worker：执行检索、总结、编码、实验、写作
- reviewer：独立提出批评
- curator/editor：整合产物

这比单 agent 更适合 scholar-agent framework：
- framework 层只定义 role contract
- runtime 层决定是单 agent 串行，还是 multi-agent 并行

### 抽象层 6：Knowledge Substrate
这个仓库把 Knowledge Acquisition 放在最前面，说明研究系统需要稳定知识底座。

可迁移为：
- paper registry
- note store
- citation graph / concept graph
- evidence store
- benchmark registry

对 scholar-agent 的意义：
- 不是每轮都从零检索
- 可沉淀跨任务知识
- 很适合和 `docs/` 中长期研究笔记结合

### 抽象层 7：Output Modes 区分
参考仓库实际覆盖了多种输出目标：
- hypothesis
- experiment result
- survey
- peer review
- report/paper

因此 scholar-agent framework 不应只面向“写论文”，而应支持不同目标模式：
- exploration mode
- replication mode
- hypothesis mode
- benchmark mode
- survey/report mode
- paper submission prep mode

### 抽象层 8：Benchmark-Aware Runtime
README 单列了 benchmarks，说明研究 agent 不应只靠主观 demo。

可迁移为：
- benchmark adapter
- task environment adapter
- scoring harness
- reproducibility record

价值：
- 把 framework 从“会生成文本”推向“可验证研究系统”

---

## 3) 风险点

### 风险 1：这是资源索引，不是经过统一实现验证的系统设计
最重要的风险是来源本身：
- Awesome-AI-Scientist 是 curated list，不是单一方法论或单一代码库
- 它把很多论文/项目放在一起，但这些方法之间的前提、目标、评估标准并不统一

含义：
- 不能把 README 的章节结构直接当作已经验证过的最佳系统架构
- 更适合作为 taxonomy 输入，而不是 blueprint

### 风险 2：分类法强，但执行契约弱
该仓库对阶段划分很强：
- knowledge
- idea
- verification
- review
- evolution

但没有提供：
- 每阶段标准输入/输出 schema
- 阶段切换条件
- 失败恢复机制
- 预算管理
- 质量门槛

如果直接迁移到 scholar-agent，容易得到“概念完整但工程不可运行”的框架。

### 风险 3：idea generation 容易高估，implementation capability 容易低估
README 本身就列出：
- `AI Scientists Fail Without Strong Implementation Capability`
这反映出一个核心现实：

风险表现：
- 点子很多，但实验做不出来
- proposal 看起来新颖，实际上无法验证
- 代码/环境/数据处理能力不够时，系统会停在“想法堆积”

对 scholar-agent 的启示：
- framework 不能只优化 ideation
- 必须把 implementation、execution、tool reliability 作为一等能力

### 风险 4：review loop 容易变成自我强化幻觉
该仓库高度重视 AI review / automated review，但这里有明显风险：

- reviewer 和 author 共享相同模型偏差
- review 可能奖励“写得像论文”而不是“研究真的成立”
- 内部自评容易出现虚假一致性

因此：
- review loop 不能替代外部证据
- 最好引入独立 judge、规则检查、基准任务、人工抽检

### 风险 5：evaluation 指标不统一
README 在各阶段都放了 evaluation，但不同任务本质不同：
- idea generation：novelty/diversity/usefulness
- experiment：reproducibility/correctness/performance
- review：helpfulness/actionability/fairness
- writing：clarity/faithfulness/citation quality

风险在于：
- 用一个统一分数覆盖所有阶段会失真
- LLM-as-judge 的分数很可能不稳定

对 scholar-agent：
- 必须阶段化评估
- 不要做单一“research quality score”幻觉指标

### 风险 6：闭环系统容易在错误目标上越跑越远
README 的 `Evolution / Dynamic Planning / Autonomous Learning` 很诱人，但自动闭环有典型风险：

- 早期错误假设被持续强化
- 检索偏差导致整个研究方向偏航
- 局部 reward 优化压过真实科学价值
- 为了“能产出”而牺牲 rigor

所以 scholar-agent 中最好加入：
- restart / branch / rollback 机制
- 关键阶段人工门控
- 证据不足时停止而不是硬写结论

### 风险 7：论文/报告生成容易先于证据成熟
这个生态很强调 AutoSurvey、Paper Writing、Review generation，一大风险是：

- 写作能力发展快于实验真实性
- 很容易先生成一篇“像样的文稿”，再回填证据
- 最终导致看起来完整、实则脆弱的研究产物

对 framework 的要求：
- 写作模块只能消费已验证 artifact
- 结论必须绑定 evidence provenance
- 引用、图表、实验数字需要可追踪来源

### 风险 8：多代理协作带来责任扩散
参考资源里有大量 multi-agent/team 风格方法。风险是：
- 谁对最终结论负责不清楚
- agent 间信息传递失真
- review agent 和 generation agent 串谋式偏置
- trace 太复杂，难以 debug

所以 scholar-agent 若走 multi-agent：
- 每个 role 的输入/输出必须结构化
- 每步保留 rationale 和 artifact trace
- 支持单 agent baseline，便于比较

### 风险 9：领域泛化风险
该仓库混合了：
- NLP
- 生物医药
- 化学
- 算法发现
- 代码研究
- peer review/support systems

风险：
- 不同学科的实验 loop 完全不同
- “通用研究 agent framework”如果过于统一，可能只在文本密集领域有效

建议：
- scholar-agent framework 做“领域无关核心层 + 领域适配层”
- 不要假设所有科学研究都可按同一实验接口运行

---

## 建议给 scholar-agent 的最小迁移结论

如果只提炼一个最实用版本，我建议迁移这 5 个核心抽象：

1. 阶段化生命周期  
   - knowledge -> idea -> experiment -> review -> writing

2. artifact 驱动  
   - 每阶段只读前一阶段产物，输出结构化新产物

3. loop 原语  
   - propose/critique/refine 与 design/run/analyze/revise

4. evaluator 分层  
   - novelty、feasibility、rigor、writing、risk 分开评估

5. 可追溯性  
   - 每个结论必须能回溯到文献、实验记录、review 意见

---

如果你愿意，我下一步可以继续做两种只读输出之一：

1. 把以上内容整理成一份更“框架设计向”的 scholar-agent 抽象模块清单；  
2. 从这个参考仓库里进一步筛出最相关的代表性项目/论文矩阵，按“idea loop / experiment loop / review loop / writing loop”四列做对照。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore agent roles",
  "description": "study roles",
  "prompt": "只读探索 Awesome-AI-Scientist 中的 agent role、module boundary、orchestration 或类似职责划分。不要修改任何文件。返回：1) 角色/模块划分；2) scholar agent framework 可借鉴的职责描述；3) 不适配本仓库的地方。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a734107affeBPWKXP6p1WCBBr (for resuming to continue this task if needed)

<task_result>
下面是对 Awesome-AI-Scientist 的只读探索结果。此次判断主要基于其知识库型 README 分类结构，而不是某个可运行框架的源码分层；也就是说，它更像“研究自动化能力地图/分类法”，不是一个实现了明确 agent runtime 的 orchestration 仓库。

参考文件：
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/README.md`
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/CONTRIBUTING.md`

## 1) 角色/模块划分

### A. 顶层不是“代码模块”，而是“研究生命周期模块”
它在 README 中把 AI Scientist 生态按研究流程拆成几个核心阶段：

1. Knowledge Acquisition
   - 文献搜索与整理
   - 知识检索与总结
   - 对应“知识构建/知识获取”职责

2. Idea Generation
   - 研究问题提出
   - 假设生成
   - 新方向探索
   - 对应“研究构思”职责

3. Verification and Falsification
   - 实验执行、代码实现、仿真、复现实验、证伪
   - 对应“验证/实现”职责

4. Review System
   - reviewer assignment、review generation、screening、meta-review/批评
   - 对应“评审/批判”职责

5. Evolution
   - Dynamic Planning
   - Autonomous Learning
   - 对应“闭环迭代/策略更新”职责

### B. README 中还有一个更粗粒度的“Research Automation Stack”
这个表格给出了一种更像系统设计的边界划分：

- Knowledge Building
- Idea Generation
- Experimentation
- Paper Writing
- Paper Review

这套划分的特点是：
- 把“实验”与“写作/评审”单独看待
- 强调每层都是一个独立能力域
- 适合做 scholar agent 的 capability map

### C. “Emerging Capabilities” 提供了 orchestration 视角
它没有写具体调度器，但提出了三类上层能力：

- End-to-End Research Agents
- Human-AI Collaboration Patterns
- AI for Reproducibility & Validation

可理解为三种系统组织方式：
1. 端到端自主代理
2. 人机协作工作流
3. 面向可复现与校验的保障层

### D. 与 agent role 最接近的隐含职责
仓库里并没有定义统一 agent role schema，但从所列项目/论文可抽象出这些常见角色：

- 检索员 / 文献搜集 agent
- 摘要员 / 知识综合 agent
- 假设生成 agent
- 实验执行 / 代码实现 agent
- 证伪 / 验证 agent
- 审稿 / 批评 agent
- 规划 / 迭代 agent
- 协作团队 agent（multi-agent research team）

### E. 它的“module boundary”本质是 taxonomy boundary
因为这是 curated list，不是软件仓库，所以边界不是 Python package boundary，而是：
- 按研究阶段分区
- 按方法 vs evaluation 分层
- 按 capability vs benchmark 分离

这个结构对你们尤其有价值，因为它天然适合映射到 scholar agent framework 的职责边界。

---

## 2) scholar agent framework 可借鉴的职责描述

下面是我认为可直接借鉴、并适合转成 framework 中 role/module contract 的部分。

### A. Research lifecycle-based module boundary
可借鉴描述：
- Scholar agent 不应先按“工具”划分，而应先按“研究生命周期职责”划分。
- 每个模块负责一个清晰的研究产出物与决策边界。

建议映射为：

1. Knowledge Module
   - 输入：研究主题、问题、关键词、已有论文集合
   - 输出：候选文献池、结构化笔记、证据摘要、主题图谱
   - 职责：搜集、筛选、归纳，不做最终研究主张

2. Ideation Module
   - 输入：知识摘要、空白点、限制条件
   - 输出：研究问题、假设、候选方案、 novelty rationale
   - 职责：提出可验证想法，不负责落实实现

3. Verification Module
   - 输入：假设、实验方案、代码/数据接口
   - 输出：实验结果、复现记录、失败证据、对假设的支持/反驳
   - 职责：把“想法”转成“证据”

4. Review/Critique Module
   - 输入：草案、实验记录、结论
   - 输出：缺陷清单、反例、可信度判断、改进建议
   - 职责：充当内部 reviewer，而不是生成宣传性总结

5. Evolution/Planning Module
   - 输入：前几轮结果与失败原因
   - 输出：下一轮计划、优先级、终止条件、资源分配
   - 职责：决定继续什么、放弃什么、改什么

### B. “方法层”和“评测层”分离
Awesome-AI-Scientist 在多个部分都区分：
- Methods
- Evaluation / Benchmarks

可借鉴描述：
- 任何 scholar agent 模块都应分成“执行逻辑”和“评估逻辑”两层。
- 例如 Idea Generation 不能只会生成 idea，还要有 novelty/usefulness/feasibility 的评测面。
- Verification 不能只跑实验，还要有 reproducibility 和 failure analysis。

这对 framework 很关键，因为否则 agent 很容易只会“生成”，不会“判定”。

### C. Review 不应只是末尾步骤，而应成为横切职责
该仓库把 Review System 独立成一级模块，这一点非常值得借鉴。

可借鉴描述：
- review/critique 不是 paper 写完后的附属动作，而是贯穿知识整理、idea 提出、实验结论、写作草稿的横切能力。
- 在 scholar agent 中，可把 Reviewer 设计成：
  - pre-idea critic
  - experiment critic
  - draft critic
  - claim-evidence checker

这比单纯“planner + executor”更贴近学术工作。

### D. Evolution 模块是 orchestration 的高级层
它将 Evolution 拆成：
- Dynamic Planning
- Autonomous Learning

可借鉴描述：
- orchestration 不应仅是顺序调度，而应包含：
  1. 计划更新
  2. 基于反馈修正策略
  3. 多轮闭环
  4. 失败后的路线重规划

对于 scholar agent framework，可定义：
- Planner：拆阶段目标与依赖
- Supervisor：检查是否达到阶段退出条件
- Learner/Memory：沉淀失败模式、有效检索路径、可复用实验模板

### E. End-to-End Research Agents 只是上层组合，不应压平子职责
README 把端到端 agent 视为 emerging capability，而不是唯一结构。

可借鉴描述：
- 端到端 agent 应建立在显式子职责之上，而不是一个大而全 agent。
- 更好的做法是：
  - 用 lifecycle modules 形成边界
  - 再通过 orchestrator 组合成 end-to-end flow
- 这能减少 prompt 巨石化和上下文污染。

### F. 可以借鉴的最小角色集
如果 scholar agent framework 要做最小可行角色集，我建议从该仓库的分类抽象为：

- Research Librarian：文献检索/筛选/摘要
- Research Designer：问题定义/假设生成
- Research Engineer：代码、实验、复现、数据处理
- Research Critic：证据校验、漏洞检查、评审意见
- Research Orchestrator：阶段编排、优先级、停止条件
- Research Memory：沉淀知识对象、失败经验、项目上下文

---

## 3) 不适配本仓库的地方

结合你当前仓库是 scholar-agent 的 notes + Python scaffold，我认为以下几点不适配，或者只能部分借鉴。

### A. 它不是可运行框架，缺少真实 runtime boundary
不适配点：
- Awesome-AI-Scientist 基本是 curated taxonomy，不是 agent runtime。
- 没有实际的：
  - role interface
  - message protocol
  - state machine
  - orchestration engine
  - tool contract

所以它适合启发“职责分类”，不适合直接指导代码模块结构。

### B. 它把“Paper Writing”作为一级能力，但你们当前仓库未必需要这么早固化
不适配点：
- 对 scholar-agent framework 而言，早期更核心的是：
  - retrieval
  - synthesis
  - planning
  - validation
- “论文写作”若过早变成一级模块，容易让系统偏向产文稿，而不是产可靠研究过程。

更适合本仓库的做法：
- 先把 writing 当作 downstream presentation layer
- 等上游证据链稳定后再强化

### C. 它的 taxonomy 偏宽泛，缺少“本仓库边界内的工程约束”
不适配点：
- 该仓库覆盖化学、生物、通用科研、review、benchmark、community 等非常广。
- 你们仓库当前更像“学术研究 agent 方法论与框架抽象”，不一定要纳入领域实验自动化。

所以不应直接照搬：
- CoScientist 这类实验室自动化能力
- Embodied / wet-lab / domain-specific execution 模块

### D. “Autonomous Learning” 在你们仓库中要慎用
不适配点：
- README 的 Evolution 包含 autonomous learning、自我修正、自主学习等概念。
- 对 scholar agent framework，如果没有严格 memory governance、evaluation harness、回滚机制，自主学习会放大错误沉积。

更适合本仓库的版本：
- 先做 supervised evolution：
  - 记录失败
  - 记录有效策略
  - 人工确认后沉淀
- 而不是让 agent 自主改写核心策略

### E. 它没有显式区分“研究知识库”和“项目执行上下文”
不适配点：
- 你们仓库已经同时有 docs 和 Python scaffold。
- scholar agent framework 需要明确分离：
  1. 长期知识库
  2. 当前任务工作记忆
  3. 执行日志 / worklog
  4. 可复用技能/模板
- Awesome-AI-Scientist 并未处理这些运行态边界。

### F. Multi-agent team 相关内容多数是论文索引，不是可直接落地的协作协议
不适配点：
- 虽然 README 收录了 multi-agent、hierarchical、collaborative research 等方向，
- 但没有提供可复用的协作机制细节，例如：
  - 角色切换条件
  - agent 间冲突仲裁
  - artifact ownership
  - 审批门禁
  - 终止条件

因此不能直接把“multi-agent”当成现成架构，只能把它当设计信号。

---

## 结论

如果一句话总结：

- Awesome-AI-Scientist 更适合作为 scholar agent framework 的“职责地图”和“能力 taxonomy”来源；
- 不适合作为“源码模块设计”或“orchestration 实现蓝图”直接照搬。

我建议你们优先吸收它的三点：

1. 按研究生命周期定义模块边界  
2. 把 review/critique 作为独立且横切的职责  
3. 把 evolution/planning 视为闭环调度层，而不是单次 planner

如果你愿意，我下一步可以继续把这份探索直接整理成一版“适配本仓库的 scholar agent role schema 草案”，输出成更接近你们 framework 文档的结构。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore doc gaps",
  "description": "find missing topics",
  "prompt": "只读从用户目标出发，判断 scholar agent framework 文档若要“properly”更新，最可能缺失哪些主题：目标定义、设计原则、生命周期、状态管理、知识沉淀、与 Obsidian docs 的关系、CLI/runtime 边界、验证与维护。不要修改任何文件。返回：1) 缺口列表；2) 每项缺口的优先级；3) 建议文档落点。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a7341076ffeIowMh6Rd0Qw3vE (for resuming to continue this task if needed)

<task_result>
下面是基于现有 framework 文档的只读判断：不是说这些主题“完全没有”，而是从“若要 properly 更新、让新读者/实现者能闭环理解 scholar agent framework”这个标准看，当前最可能仍然缺失或不够成体系的主题。

我主要对照了这些文档：
- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
- 以及实现侧参考：
  - `/Users/kozmosa/code/scholar-agent/src/ainrf/cli.py`
  - `/Users/kozmosa/code/scholar-agent/src/ainrf/server.py`
  - `/Users/kozmosa/code/scholar-agent/src/ainrf/state/store.py`

---

## 1) 缺口列表

### 1. 缺一个“面向用户目标”的总定义页
现状：
- `ai-native-research-framework.md` 已有愿景、定位、设计原则。
- `v1-dual-mode-research-engine.md` 已有 V1 目标。
- 但这些目标更偏“系统蓝图/模式目标”，还不够像一个“从用户任务出发的总说明”。

最可能缺什么：
- 目标用户是谁，分别要解决什么问题。
- scholar agent framework 的核心产出是什么，不是什么。
- “为什么这个仓库既有 docs，又有 ainrf runtime scaffold”这一总叙述。
- “properly 更新 framework 文档时，哪些内容是框架层、哪些是实现层、哪些是研究输入层”的总判断标准。

为什么算缺口：
- 现在读者能看到“系统想做什么”，但不容易快速回答“这个框架最终帮谁完成什么、输出什么、成功标准是什么”。
- 这会导致后续文档都偏 design-heavy，而缺少一个 product-definition / problem-definition 的总入口。

优先级：P0

建议文档落点：
- 优先补到 `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- 如果想单独成页，更适合新建一个总纲页并在 `/Users/kozmosa/code/scholar-agent/docs/framework/index.md` 置顶链接；但你这次要求不改文件，所以这里只给落点建议。


### 2. 设计原则有，但缺“原则到决策”的映射
现状：
- `ai-native-research-framework.md` 已有宿主无关、repo 优先、工件优先、有界自治、失败可记账。
- `reference-mapping.md` 也解释了一部分来源。

最可能缺什么：
- 每条原则对应哪些具体架构决策。
- 原则之间冲突时如何取舍。
- 哪些常见设计不采用，以及原因。
- “原则如何约束今后文档更新和代码演化”。

为什么算缺口：
- 目前原则更像宣言，不够像可执行的 decision rubric。
- 如果后续有人更新 RFC、runtime、docs，缺少清晰的“原则→约束→例外”链路。

优先级：P1

建议文档落点：
- 优先扩展 `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- 可在 `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md` 增补“原则来源与反例”部分


### 3. 生命周期是分散描述的，缺“端到端生命周期总图”
现状：
- `v1-dual-mode-research-engine.md` 讲了 Mode 1 / Mode 2 工作流。
- `artifact-graph-architecture.md` 讲了工件状态转换。
- `v1-rfc.md` 讲了 task lifecycle、checkpoint、gate、SSE。

最可能缺什么：
- 一个统一的 lifecycle：从用户提出任务，到 intake、planning、execution、review/archive、knowledge handoff、maintenance 的总链路。
- 区分 task lifecycle、artifact lifecycle、project lifecycle。
- 文档生命周期：哪些内容是设计、哪些是运行时状态、哪些是沉淀后的长期知识。

为什么算缺口：
- 现有文档分别从 workflow、artifact、API 三个视角写，但没有一页把“系统整体生命周期”串起来。
- 这会让状态管理、知识沉淀、维护边界看起来像碎片问题。

优先级：P0

建议文档落点：
- 最适合单独补在 `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
- 若想做更高层统一，也可在 `/Users/kozmosa/code/scholar-agent/docs/framework/index.md` 增加“生命周期导航”段落


### 4. 状态管理有实现规格，但缺“source of truth 分层说明”
现状：
- `artifact-graph-architecture.md` 已强调 repo 优先、工件状态、Obsidian 不是执行状态数据库。
- `v1-rfc.md` 已讲 orchestrator checkpoint 与 container git repo 是两个独立持久化通道。
- `src/ainrf/state/store.py` 也体现了 `.ainrf` JSON state store。

最可能缺什么：
- 明确三层状态分别是什么：
  1. orchestrator runtime state
  2. container project repo artifacts
  3. Obsidian/docs knowledge layer
- 每层谁是 source of truth，谁只是索引/镜像/摘要。
- 状态迁移与同步边界：何时从 runtime state 升格为 project artifact；何时从 project artifact 升格为 docs knowledge。
- 崩溃恢复、审计、知识回写之间的关系。

为什么算缺口：
- 这其实是当前最容易让人混淆的地方。
- 文档里已有局部说明，但没有一页专门把“状态系统设计”说透。

优先级：P0

建议文档落点：
- 最适合补在 `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
- 其次在 `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md` 增补一个 “State ownership / source-of-truth matrix” 小节


### 5. 知识沉淀讲了“repo 优先”，但缺“沉淀策略与升级路径”
现状：
- `artifact-graph-architecture.md` 说了 Obsidian 文档是知识层，不是执行状态数据库。
- `container-workspace-protocol.md` 说了项目 repo 中有哪些 artifacts / reports。
- 仓库级 `PROJECT_BASIS.md` 说了 `docs/`、`docs/LLM-Working/` 的用途。

最可能缺什么：
- 哪些运行产物应该留在项目 repo，哪些应该总结进 `docs/framework` / `docs/projects` / `docs/summary`。
- 知识升级路径：raw run → artifact/report → synthesis note → framework principle / RFC update。
- 何时形成长期知识，何时只保留为执行痕迹。
- 如何避免“所有东西都留在运行 repo 或 worklog 里，最后 framework 文档失真”。

为什么算缺口：
- 这部分正好连接你关心的“知识沉淀”和“与 Obsidian docs 的关系”。
- 当前 repo 优先讲清了“不要把 docs 当数据库”，但没有讲清“那 docs 到底该承载什么”。

优先级：P0

建议文档落点：
- 优先补在 `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- 并在 `/Users/kozmosa/code/scholar-agent/docs/framework/index.md` 增加“知识资产分层/阅读与回写关系”导航
- 如需更操作化，也可在 `/Users/kozmosa/code/scholar-agent/docs/index.md` 补仓库级知识分层说明


### 6. 与 Obsidian docs 的关系写得不够系统
现状：
- `artifact-graph-architecture.md` 有一句关键话：Obsidian 风格文档是人可读索引和知识层，而不是执行状态数据库。
- `PROJECT_BASIS.md` 规定了 docs 的目录职责。

最可能缺什么：
- framework 与 Obsidian docs 的正式关系定义：
  - docs 是设计层还是知识层，还是两者兼有？
  - docs/framework 与 container repo artifacts 的关系是什么？
  - docs/projects 与 docs/summary 如何反哺 framework？
- 从 runtime 到 docs 的“摘录/归纳/上升抽象”规则。
- Obsidian 作为浏览/导航/知识网络工具，而非 workflow engine 的角色定义。

为什么算缺口：
- 这部分目前存在于多处零碎表述，但不是一个明确章节。
- 对这个仓库尤其关键，因为仓库本身就是“研究笔记 + runtime scaffold”的混合体。

优先级：P0

建议文档落点：
- 最适合补在 `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
- 同时在 `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md` 增加“与 docs/Obsidian 的关系”小节


### 7. CLI / runtime 边界在 RFC 里有方向，但缺“当前仓库实际边界说明”
现状：
- `v1-rfc.md` 明确说 REST 服务是 V1 正确形态，CLI 可以作为客户端。
- 但当前实现里 `/Users/kozmosa/code/scholar-agent/src/ainrf/cli.py` 仍是 scaffold，`run` 还是 stub，`serve` 才是主要入口。
- 也就是说，设计目标与当前仓库现实之间存在一个需要解释的落差。

最可能缺什么：
- “当前已经实现到哪里，哪些只是 RFC 目标”。
- CLI 在本仓库里现在承担什么：开发入口、daemon 管理、API server 启动、未来 client。
- runtime 与 docs 的边界：文档定义语义，runtime 实现执行；哪些内容更新 docs 即可，哪些必须同步实现/测试。
- `src/ainrf` 与 `docs/framework` 的 contract。

为什么算缺口：
- 对外部读者和未来维护者来说，最容易误判的是：框架是不是已经是完整系统了。
- 需要一段明确的 current-state / intended-state 边界说明。

优先级：P0

建议文档落点：
- 优先补在 `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
- 同时在 `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md` 补一个“设计态 vs 已实现态”矩阵
- 也可在 `/Users/kozmosa/code/scholar-agent/docs/framework/index.md` 增加“阅读时请区分 blueprint / scaffold / implemented surfaces”


### 8. 验证与维护有仓库级规则，但 framework 级验证标准不足
现状：
- `PROJECT_BASIS.md` 已规定 pytest / ty / ruff 等。
- `v1-roadmap.md` 各阶段有交付物和可测试标准。
- 但 framework 文档层面，对“设计是否被 properly 维护”缺少统一的验证框架。

最可能缺什么：
- framework 级验证：
  - 语义一致性检查
  - 文档-代码映射检查
  - 关键边界是否被测试覆盖
  - 哪些变更必须同步更新哪些文档
- maintenance policy：
  - RFC 何时更新
  - roadmap 何时回写
  - index 何时调整导航
  - 实现偏离设计时如何记录 deviation
- 文档维护 owner / cadence / trigger。

为什么算缺口：
- 现在“怎么验证代码”比“怎么验证 framework 文档仍然准确”更清楚。
- 如果要 properly 更新 framework，这部分必须补，否则文档容易继续漂移。

优先级：P1

建议文档落点：
- 最适合补在 `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
- 其次在 `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
- 仓库级补充可落到 `/Users/kozmosa/code/scholar-agent/PROJECT_BASIS.md`，但这属于更高层工程治理


---

## 2) 每项缺口的优先级

| 缺口主题 | 优先级 | 理由 |
|---|---|---|
| 面向用户目标的总定义页 | P0 | 没有这个，其他文档都难形成统一入口 |
| 生命周期总图 | P0 | 现在工作流、状态机、RFC 分散，缺总链路 |
| source of truth 分层的状态管理说明 | P0 | 这是框架、runtime、docs 最容易混淆的核心边界 |
| 知识沉淀策略与升级路径 | P0 | 直接关系到 framework 文档是否会持续失真 |
| 与 Obsidian docs 的正式关系 | P0 | 当前仓库的“文档+runtime”双重性质要求必须讲清 |
| CLI/runtime 当前边界与目标边界 | P0 | 设计态与已实现态存在落差，需要显式标注 |
| 设计原则到具体决策的映射 | P1 | 已有原则，但执行约束不够强 |
| framework 级验证与维护机制 | P1 | 有工程规则，但缺 framework 文档治理规则 |

我会把最优先的实际补文顺序排成：

1. 用户目标总定义  
2. 生命周期总图  
3. 状态/SoT 分层  
4. 知识沉淀与 Obsidian 关系  
5. CLI/runtime 边界  
6. 验证与维护  
7. 原则到决策映射

---

## 3) 建议文档落点

### 最推荐的落点分布

#### A. `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
适合补：
- 面向用户目标的总定义
- 框架核心问题与非目标
- 设计原则到决策的映射
- 知识沉淀总策略
- 与 Obsidian/docs 的高层关系

原因：
- 这是当前最接近“框架宪法”的文档。


#### B. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
适合补：
- 端到端生命周期总图
- task / project / artifact 三类 lifecycle 的串联
- 从 intake 到 archive / handoff 的完整阶段定义

原因：
- 这里已经承接“V1 如何运转”，最适合加入 lifecycle 视角。


#### C. `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
适合补：
- source of truth 分层矩阵
- runtime state / project repo / docs knowledge 三层边界
- 状态升级与沉淀路径

原因：
- 它本来就是“工件、状态、图谱”的主文档。


#### D. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
适合补：
- CLI/runtime 边界
- 当前实现态 vs 目标设计态
- framework 级验证与维护
- 文档-实现 contract

原因：
- 这里最适合说明“怎么落地、落地到哪一步、如何验证没漂移”。


#### E. `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
适合补：
- 对读者的导航说明
- blueprint / scaffold / implemented surfaces 区分
- 与 Obsidian docs 的阅读路径和分层导航

原因：
- 它是最适合放“怎么读、去哪看”的地方，不该承载太多细节，但应该把结构说清。


#### F. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
适合补：
- 设计态 vs 已实现态矩阵
- 每阶段验证标准与需要同步更新的文档
- maintenance trigger

原因：
- 路线图天然适合承载演进与维护约束。


---

## 一个更凝练的结论

如果只看你列的 8 个主题，当前文档覆盖度大致是：

- 目标定义：有，但不够“用户目标导向”
- 设计原则：有，但缺决策映射
- 生命周期：有局部流程，缺统一总图
- 状态管理：有实现规格，缺 SoT 分层总述
- 知识沉淀：原则上提到 repo 优先，但缺沉淀策略
- 与 Obsidian docs 的关系：有一句核心判断，但缺系统说明
- CLI/runtime 边界：有 RFC 倾向，缺当前仓库现实边界说明
- 验证与维护：有工程验证，缺 framework 级治理与维护规则

如果你愿意，我下一步可以继续做一版“最小补文提纲”，直接按上述 6 个落点给出每页应增加的章节标题和 1-2 句摘要，仍然只读、不改文件。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore chinese doc style",
  "description": "check Chinese style",
  "prompt": "只读抽样检查 docs/ 下已有中文写作风格、frontmatter、wikilink 习惯、标题风格。不要修改任何文件。返回：1) 推荐沿用的中文文风；2) 结构模板；3) 需要避免的风格不一致。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a7341071ffexQ6C8RWI7uzRdU (for resuming to continue this task if needed)

<task_result>
下面是对 `docs/` 下现有文档做的只读抽样结论。抽样主要参考了这些文件：

- `/Users/kozmosa/code/scholar-agent/docs/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
- `/Users/kozmosa/code/scholar-agent/docs/projects/claude-scholar.md`
- `/Users/kozmosa/code/scholar-agent/docs/projects/academic-research-skills.md`
- `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`

未修改任何文件。

## 1) 推荐沿用的中文文风

### 总体风格
建议沿用当前仓库已经比较稳定的这类写法：

- 中文为主，英文术语点到为止，不强行全译
- 偏“分析型笔记”而不是“宣传型文案”
- 先下判断，再给依据
- 句子不追求文学性，追求信息密度和可比较性
- 明确边界、适用场景、优劣势，不写空泛结论

### 具体特征
1. 标题风格很稳定  
   常见模式是：

- `主题名：中文定位`
- 如：`Claude Scholar：学术研究与开发一体化个人配置系统`
- 如：`AINRF V1 RFC：有界自治研究引擎实现规格`

这类标题的好处是：
- 前半段负责对象识别
- 后半段负责结论定位
- 读者扫一眼就知道“这篇在说什么”

2. 开头常用一个高度压缩的摘要块  
   习惯是：

- 顶部 `# 标题`
- 紧跟 `> [!abstract]`
- 用 1 段话说明“这篇的核心判断是什么、边界是什么、为什么值得读”

这部分文风通常是：
- 不绕
- 直接给结论
- 带一点“不是 X，而是 Y”的界定句式

例如常见表达模式：
- “不是……，而是……”
- “最突出的不是……，而是……”
- “它的作用不是……，而是……”

这很值得沿用，因为很符合该仓库的“研究摘要卡片”气质。

3. 正文偏结构化判断
常见写法不是长段散文，而是：

- 小节标题
- 小节下 3–6 条 bullet
- 每条 bullet 讲一个判断点

例如常见节名：
- `## 项目定位`
- `## 仓库构成`
- `## 核心工作流`
- `## 研究生命周期覆盖`
- `## 集成与依赖面`
- `## 证据与样例`
- `## 优势`
- `## 局限与风险`
- `## 适用场景`
- `## 关联笔记`

这说明仓库写作更偏“可扫描、可比对、可复用”。

4. 语气偏克制
推荐保持：

- 不使用夸张词
- 不写“革命性”“颠覆式”这类宣传腔
- 不做无证据绝对化判断
- 经常出现限定语，例如：
  - “从静态证据看”
  - “更像……而不是……”
  - “最适合贡献……”
  - “不一定天然适合……”
  - “V1 不做……”
  - “Out of scope for V1”

这是很统一的仓库气质：结论鲜明，但不过度断言。

### 可直接模仿的文风公式
你后续写文档时，可以直接套这类表达：

- “这篇笔记回答一个实际问题：……”
- “它不是……，而是……”
- “一个直接结论是：……”
- “最适合贡献……，但不适合直接复制……”
- “相比……，它更强调……”
- “从现有参考项目抽象看，……”
- “适合……，不适合……”

---

## 2) 结构模板

下面给一个最贴近现有仓库风格的模板。

### A. 通用笔记模板
适合 framework / project / summary 三类文档。

```md
---
aliases:
  - 中文别名或英文正式名
tags:
  - research-agent
  - <分类标签>
  - <主题标签>
source_repo: <仓库名或 scholar-agent>
source_path: <绝对路径或来源路径>
last_local_commit: <commit 或 workspace aggregate>
---

# 标题：一句中文定位

> [!abstract]
> 用 1 段话先给出核心判断：它是什么，不是什么，解决什么问题，边界在哪里。

## 背景 / 定位
- 这篇笔记要回答什么问题。
- 对象的基本定位。
- 与相邻方案相比，它更强调什么。

## 核心内容 / 结构
- 拆 3–5 条核心机制、模块、主张或组成部分。
- 如果有必要，可补一张 Mermaid 图。

## 证据 / 依据
- 说明判断来自哪里。
- 列出 README、目录结构、样例产物、提交记录、协议等证据来源。

## 优势
- 用 bullet 列出 3–5 条。

## 局限与风险
- 用 bullet 列出 3–5 条。
- 尽量写“为什么是局限”，而不是只写标签。

## 适用场景 / 结论
- 谁适合用。
- 什么目标下优先读这篇。
- 不适合什么场景。

## 关联笔记
- [[index]]
- [[framework/index]]
- [[summary/xxx]]
- [[projects/xxx]]
```

### B. 项目调研模板
这个模板和 `projects/*.md` 的风格最接近。

```md
---
aliases:
  - 项目正式名
tags:
  - research-agent
  - repo-study
  - <项目类别标签>
source_repo: <外部仓库名>
source_path: <ref-repos/...>
last_local_commit: <hash + 日期 + subject>
---

# 项目名：中文定位

> [!abstract]
> 先给一句总判断：它更像什么，不像什么，最突出的差异点是什么。

## 项目定位
- README 如何定义它
- 它在本仓库比较系中的位置
- 相比其他项目最明显的取向差异

## 仓库构成
- 顶层目录
- 关键模块
- 命令 / agents / skills / hooks / plugins 等运行面

## 核心工作流
```mermaid
...
```

## 研究生命周期覆盖
- 前期
- 中期
- 后期

## 集成与依赖面
- 支持哪些宿主/工具
- 依赖什么外部系统
- 是否偏个人/团队/平台

## 证据与样例
- README
- 目录
- 样例产物
- LICENSE
- 最近提交

## 优势
- ...

## 局限与风险
- ...

## 适用场景
- ...

## 关联笔记
- [[index]]
- [[summary/...]]
- [[projects/...]]
```

### C. framework 文档模板
适合抽象设计、RFC、roadmap。

```md
---
aliases:
  - 英文名
  - 中文别名
tags:
  - research-agent
  - framework-design
  - <spec/rfc/index/roadmap>
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---

# 名称：中文规格定位

> [!abstract]
> 说明这篇在整个框架中的职责：定义愿景、规格、边界、实现路径中的哪一层。

## 问题定义 / 设计目标
- 当前缺口是什么
- 为什么需要这篇文档

## 核心主张 / 设计原则
- 原则 1
- 原则 2
- 原则 3

## 架构 / 模型 / 接口
- 分层视图
- Mermaid 图
- 关键对象或端点表格

## 边界与非目标
- In scope
- Out of scope

## 关键取舍
- 为什么选 A 不选 B
- 与参考方案的区别

## 关联笔记
- [[framework/index]]
- [[framework/...]]
- [[summary/...]]
```

### frontmatter 习惯
从抽样看，推荐延续以下固定字段顺序：

```yaml
---
aliases:
  - ...
tags:
  - ...
source_repo: ...
source_path: ...
last_local_commit: ...
---
```

特点是：
- 比较稳定
- 元信息简洁
- 对构建和索引友好

### wikilink 习惯
现有习惯也很明确：

1. 内链优先用 Obsidian wikilink
- `[[framework/index]]`
- `[[projects/claude-scholar]]`

2. 需要指定显示文本时用管道
- `[[framework/index|AI-Native Research Framework]]`

3. “关联笔记”段落一般只放内部 wikilink 列表

4. 指向外部参考仓库文件时，用普通 Markdown 链接相对路径
- `[claude-scholar/README.zh-CN.md](../../ref-repos/claude-scholar/README.zh-CN.md)`

这个边界很清楚，建议继续保持：
- 仓库内部知识网络：wikilink
- 外部证据文件：Markdown 链接

---

## 3) 需要避免的风格不一致

### 需要避免 1：中英混杂失控
当前文档会保留必要英文术语，但整体仍是中文主导。应避免：

- 一段里连续堆英文概念，中文只剩连接词
- 同一概念一会儿中文、一会儿英文、没有主称呼
- 标题全英文、正文又突然切回纯中文且不解释

更好的做法是：
- 首次出现保留英文术语
- 后面以中文概念为主，必要时括号保留英文

例如：
- 可写“监督式控制层（control layer）”
- 不建议全篇来回切换 “control plane / 控制面 / orchestration layer / 编排层” 而无收敛

### 需要避免 2：标题风格漂移
当前一级标题高度统一，尽量不要出现这些不一致：

- 只写一个很虚的中文标题，没有对象名
- 写成口号式标题
- 同类文档里有的“对象名：定位”，有的突然变成“关于……的一些想法”

建议继续用：
- `对象名：中文定位`
- `主题名：本文核心结论`

### 需要避免 3：摘要区缺失或过长
现有文档多数都有 `> [!abstract]`，而且作用很明确。应避免：

- 没有摘要，直接正文开讲
- 摘要写成三四段，失去“速览”功能
- 摘要只重复标题，不给判断

推荐摘要长度：
- 1 段
- 2–4 句
- 回答“它是什么 / 不是什么 / 核心价值 / 阅读边界”

### 需要避免 4：章节粒度忽粗忽细
当前项目调研文档常见章节很稳定。如果有的文档非常细，有的文档只有两节，会显得不齐。尤其要避免：

- 一篇全是长段落，没有 bullet
- 一篇只有 bullet，没有总判断
- 同类项目文档缺少“优势 / 局限 / 适用场景”这些对照段

如果是 `projects/`，建议尽量保留：
- 项目定位
- 仓库构成
- 核心工作流
- 优势
- 局限与风险
- 适用场景
- 关联笔记

### 需要避免 5：wikilink 与普通链接混用无规则
应避免：

- 内部文档有时用 `[[...]]`，有时又写成相对路径 Markdown 链接
- 关联笔记里混进裸文件路径
- 同一个对象有时写 `[[framework/index]]`，有时写 `[[docs/framework/index.md]]`

建议统一：
- 内部笔记一律 `[[...]]`
- 外部证据一律 `[text](relative/path)`
- 不把 `.md` 后缀写进 wikilink

### 需要避免 6：frontmatter 字段不齐或顺序飘
当前 frontmatter 很有规律。应避免：

- 有的文档缺 `aliases`
- 有的文档缺 `tags`
- 有的文档不用 `source_repo/source_path/last_local_commit`
- 键名大小写不统一

尤其如果是长期知识笔记，最好不要随意改成另一套元数据结构。

### 需要避免 7：结论写成宣传语或绝对判断
当前仓库风格是“判断明确，但带证据和边界”。应避免：

- “这是最强方案”
- “完美解决了……”
- “显然优于所有其他项目”
- “彻底改变研究流程”

更贴近现有风格的写法是：
- “更适合……”
- “最突出的是……”
- “在本目录中最接近……”
- “从静态证据看……”
- “不一定天然适合……”

### 需要避免 8：中文标点细节不统一
抽样里能看到少量引号样式不完全统一，比如有些地方用了中文引号，有些地方出现了弯引号或直引号。后续最好避免：

- 同一篇里混用 `“”`、`""`、`”`
- 冒号有时中文 `：`，有时英文 `:`
- 中文句子里频繁使用英文标点

建议正文统一偏中文排版：
- 中文标题用中文冒号 `：`
- 中文句子优先用 `“”`
- 表格和代码块内再保留英文样式

---

## 最后给一个简短结论

如果你要和现有 `docs/` 风格保持一致，最稳的策略是：

1. 标题用“对象名：中文定位”
2. 必带 YAML frontmatter
3. 开头必有 `> [!abstract]`
4. 正文用“判断性小节 + bullet”推进
5. 内部链接用 `[[wikilink]]`
6. 外部证据用普通 Markdown 链接
7. 语气克制，强调边界、适用场景、局限
8. 避免宣传腔、避免结构散文化、避免元数据格式漂移

如果你愿意，我下一步可以基于这个抽样结果，再给你整理一份“可直接复制的 docs 中文写作骨架（含 frontmatter 样板 + 常用小节名）”。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore references in framework",
  "description": "check crosslinks",
  "prompt": "只读探索 docs/framework/ 文档之间以及与 docs/summary/、docs/projects/ 的交叉引用。不要修改任何文件。返回：1) 现有交叉链接图概述；2) 孤立文档；3) 更新时应优先修补的链接。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a734106effdqb8yW08VcmvkcR (for resuming to continue this task if needed)

<task_result>
以下是对 `docs/framework/` 与 `docs/summary/`、`docs/projects/` 之间现有交叉引用的只读梳理结果。未修改任何文件。

## 1) 现有交叉链接图概述

### 总体结构
当前链接结构是“中心索引 + 总结页 + 映射页”三层骨架：

1. `docs/framework/index.md` 是 framework 区的主入口
2. `docs/summary/academic-research-agents-overview.md` 是 summary -> framework/projects 的总枢纽
3. `docs/framework/reference-mapping.md` 是 framework -> projects 的最强桥接页

可以概括为：

- framework 内部互链较密，尤其是：
  - `index`
  - `ai-native-research-framework`
  - `artifact-graph-architecture`
  - `v1-dual-mode-research-engine`
  - `v1-rfc`
  - `v1-roadmap`
- framework 对外连接主要集中在少数“桥接页”上，而不是平均分布在每篇文档中
- projects 区大多数文档更依赖 summary 页做分发，只有少数项目页直接回链到 framework

### 实际图谱概述

#### A. framework 内部主干
最核心的 framework 主干链是：

- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`

其中：

- `index.md` 明确给出阅读顺序，是最强导航页
- `v1-rfc.md` 与 `v1-roadmap.md` 承担“实现规格/实施计划”角色，更多面向内部深化
- `container-workspace-protocol.md` 更像基础设施附页，主要被架构/规格页引用

#### B. framework -> summary 的主要连接
主要是这几条：

- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`

反向上：

- `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
  -> `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`

结论：summary 与 framework 是双向连通的，但双向连接仍主要集中在 `framework/index`、`framework/reference-mapping` 和 summary 总览页。

#### C. framework -> projects 的主要连接
framework 直接连到 projects 的页面并不平均，集中在：

- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
  - `projects/ai-research-skills`
  - `projects/auto-claude-code-research-in-sleep`
- `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
  - `projects/everything-claude-code`
  - `projects/ai-research-skills`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
  - `projects/auto-claude-code-research-in-sleep`
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
  - `projects/everything-claude-code`
  - `projects/ai-research-skills`
  - `projects/claude-code-deep-research`
  - `projects/auto-claude-code-research-in-sleep`
  - `projects/academic-research-skills`
  - `projects/argusbot`
  - `projects/claude-scholar`
  - `projects/evoscientist`
  - `projects/autoresearch`

其中 `reference-mapping.md` 是最完整的 framework -> projects 聚合页。

#### D. projects -> framework 的回链情况
直接回链到 framework 的项目页较少，主要是：

- `/Users/kozmosa/code/scholar-agent/docs/projects/argusbot.md`
  -> `framework/reference-mapping`
- `/Users/kozmosa/code/scholar-agent/docs/projects/autoresearch.md`
  -> `framework/reference-mapping`
- `/Users/kozmosa/code/scholar-agent/docs/projects/evoscientist.md`
  -> `framework/reference-mapping`

其他多数项目页没有直接指向 framework 的具体设计页，只是指向：

- `[[summary/academic-research-agents-overview]]`
- 若干 peer project 页面
- `[[index]]`

这意味着：
- framework -> projects 很强
- projects -> framework 明显偏弱
- 当前是“框架吸收外部项目”的结构，不是“项目页帮助读者回到框架设计”的结构

---

## 2) 孤立文档

### 完全孤立文档
在你要求检查的范围内，没有“完全孤立”的文档。  
也就是：`docs/framework/`、`docs/summary/`、`docs/projects/` 中本次读到的页面，都至少通过 `index` 或 `summary` 间接接入网络。

### 相对孤立 / 连接薄弱的文档
如果按“跨目录桥接弱”来算，以下文档最接近“相对孤立”：

#### framework 中对 summary/projects 连接薄弱
1. `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
   - 只和 framework 内部页面互链
   - 没有直连 summary/projects

2. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
   - 内部链接很强
   - 几乎不直接连 summary/projects

3. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
   - 是最偏“实施计划”的内部文档
   - 对外桥接最弱，基本只在 framework 内循环

#### projects 中缺少 framework 回链的页面
这些项目页虽然被 summary 或 reference-mapping 覆盖，但自身几乎不把读者带回 framework：

- `/Users/kozmosa/code/scholar-agent/docs/projects/academic-research-skills.md`
- `/Users/kozmosa/code/scholar-agent/docs/projects/ai-research-skills.md`
- `/Users/kozmosa/code/scholar-agent/docs/projects/auto-claude-code-research-in-sleep.md`
- `/Users/kozmosa/code/scholar-agent/docs/projects/claude-code-deep-research.md`
- `/Users/kozmosa/code/scholar-agent/docs/projects/claude-scholar.md`
- `/Users/kozmosa/code/scholar-agent/docs/projects/everything-claude-code.md`
- `/Users/kozmosa/code/scholar-agent/docs/projects/awesome-claudecode-paper-proofreading.md`

这些页并不“断网”，但它们对 framework 的回流弱，读者在项目页里不容易被送回对应框架概念。

---

## 3) 更新时应优先修补的链接

我按“修一条能提升整网可导航性”的优先级给出建议。

### 第一优先级：补 projects -> framework 的回链
最值得优先修的不是 framework 内部，而是项目页回不到 framework 的问题。

建议在下列项目页的“关联笔记”里补对应 framework 页面：

1. `/Users/kozmosa/code/scholar-agent/docs/projects/ai-research-skills.md`
   - 应补：
     - `[[framework/reference-mapping]]`
     - 可选 `[[framework/artifact-graph-architecture]]`
   - 原因：它已被 framework 多次当作“能力层参考”，但项目页自己没有把读者送回该框架解释页

2. `/Users/kozmosa/code/scholar-agent/docs/projects/auto-claude-code-research-in-sleep.md`
   - 应补：
     - `[[framework/reference-mapping]]`
     - 可选 `[[framework/v1-dual-mode-research-engine]]`
   - 原因：它是 Mode 1/编排设计的重要来源，但回链不足

3. `/Users/kozmosa/code/scholar-agent/docs/projects/claude-code-deep-research.md`
   - 应补：
     - `[[framework/reference-mapping]]`
   - 原因：在 reference-mapping 里承担“阅读与综合参考”，但项目页未回链

4. `/Users/kozmosa/code/scholar-agent/docs/projects/claude-scholar.md`
   - 应补：
     - `[[framework/reference-mapping]]`
   - 原因：framework 明确把它当“工作台参考”，但项目页未反向建立关系

5. `/Users/kozmosa/code/scholar-agent/docs/projects/academic-research-skills.md`
   - 应补：
     - `[[framework/reference-mapping]]`
   - 原因：质量门参考已在框架中占重要位置，但项目页没有回指

6. `/Users/kozmosa/code/scholar-agent/docs/projects/everything-claude-code.md`
   - 应补：
     - `[[framework/reference-mapping]]`
     - 可选 `[[framework/artifact-graph-architecture]]`
   - 原因：它在框架里是“平台底盘参考”，适合双向闭环

### 第二优先级：补 framework 深层页 -> summary/projects 的桥
这类修补能降低“读到实现细节后与调研来源脱节”的问题。

1. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
   - 建议增加：
     - `[[summary/academic-research-agents-overview]]`
     - 或至少 `[[framework/reference-mapping]]` 的显式上下文说明
   - 原因：它现在几乎只在 framework 内部循环，读者不易回到“为什么这样设计”

2. `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
   - 建议增加：
     - `[[framework/reference-mapping]]` 已有，但可以更明确地在“动机/取舍”处加到 `summary` 或相关项目
   - 原因：RFC 很长，内部自洽强，但与调研来源的桥较隐

3. `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
   - 建议增加：
     - `[[framework/reference-mapping]]`
     - 或某个与执行/工作台/运行面更直接相关的项目页，如 `[[projects/claude-scholar]]` / `[[projects/evoscientist]]`
   - 原因：当前完全像内部附录，读者很难看出它与哪些调研对象有关

### 第三优先级：增强 summary 与 framework 深层页的双向导航
`summary/academic-research-agents-overview.md` 目前只强链到：

- `framework/index`
- `framework/reference-mapping`

如果未来继续扩写，优先考虑补到：

- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`

原因：
- `index` 是入口
- 但真正承接“从调研到框架”的正文，分别是“蓝图页”和“V1 模式页”

---

## 简短结论

### 结论一：现网不是散的，而是“中心化”
当前图谱不缺连接，缺的是“分布均衡”：
- 入口集中在 `framework/index`
- 对外映射集中在 `framework/reference-mapping`
- 总览分发集中在 `summary/academic-research-agents-overview`

### 结论二：没有完全孤立页，但有很多“单向挂靠页”
最明显的问题不是死链或孤页，而是：
- 很多 project 页只被 framework 引用
- 但 project 页自己不回链 framework
- 导致读者从项目调研难以自然回到框架设计

### 结论三：修补优先级应先补“回流链路”
优先补：
- `projects/* -> framework/reference-mapping`
其次补：
- `v1-roadmap` / `v1-rfc` / `container-workspace-protocol` -> summary/projects

如果你愿意，我下一步可以继续给你输出一版“可执行的补链清单”，按文件逐条列出建议新增哪些 wikilink。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore README and top docs",
  "description": "review entry docs",
  "prompt": "只读检查仓库顶层 README、docs 首页、summary 文档中如何介绍 scholar agent 或 framework。不要修改任何文件。返回：1) 当前对外叙述；2) 与 framework 文档是否一致；3) 需要统一的叙事。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a7341069ffdcwJQ9U1MLp97IE (for resuming to continue this task if needed)

<task_result>
已做只读检查，未修改任何文件。

检查范围：
- 顶层 README：未找到 `/Users/kozmosa/code/scholar-agent/README*`
- Docs 首页：`/Users/kozmosa/code/scholar-agent/docs/index.md`
- Framework 首页：`/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
- Summary 文档：`/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
- 另外对照了框架主文档：`/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- 以及长期约束：`/Users/kozmosa/code/scholar-agent/PROJECT_BASIS.md`

## 1) 当前对外叙述

### A. 顶层 README
当前仓库顶层没有 README，因此“对外叙述”在仓库入口层面是缺位的。

### B. docs 首页现在怎么讲
文件：`/Users/kozmosa/code/scholar-agent/docs/index.md`

当前叙述重点是：

- 这是一个“面向 Obsidian 知识库的本地笔记”
- 内容分成两条主线：
  1. 对 10 个参考项目的静态调研
  2. 基于这些项目抽象出的 `AI-Native Research Framework`
- 强调：
  - 正文中文、文件名英文 slug
  - 结论基于本地静态证据和设计推演
  - 不包含联网补充调研或完整运行验证

也就是说，docs 首页把仓库首先定义成：
“学术研究 Agent 调研知识库 + 自有 framework 蓝图入口”。

### C. framework 首页现在怎么讲
文件：`/Users/kozmosa/code/scholar-agent/docs/framework/index.md`

当前叙述重点是：

- 这是“我们自己的 AI-Native Research Framework”
- 它是一个“有界自治研究系统”
- 支持两种模式：
  - Mode 1：文献探索与复现
  - Mode 2：深度复现
- V1 运行在隔离容器上
- 人只在“纳入”和“计划”两个阶段定义合同边界

也就是说，framework 首页把 framework 定义为：
“不是普通笔记，而是一个明确有系统边界、执行环境、模式设计和人工关卡的研究系统蓝图”。

### D. summary 文档现在怎么讲
文件：`/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`

当前叙述重点是：

- 这是基于 10 个本地仓库静态调研形成的“能力地图”
- 目的不是选冠军，而是区分不同项目类型：
  - 技能库
  - 流水线
  - 控制层
  - 工作台
  - 统一运行面
  - 终稿质检协议
- 明确说：
  - 这页承担“证据层”角色
  - 自有系统蓝图已经拆到 `framework/index`
  - 因为没有现成仓库能同时覆盖平台底盘、能力包、复现账本、实验追踪、人工关卡，所以需要单独抽象自己的框架

也就是说，summary 页把自己定义为：
“外部项目调研与比较的证据层”，并把 framework 定位为由此推导出的自有系统蓝图。

---

## 2) 与 framework 文档是否一致

结论：大方向一致，但叙事层级还不完全统一。

### 一致的地方

#### 1. 都承认仓库有“两层”
- 一层是外部项目调研/证据层
- 一层是自有 framework/蓝图层

这点在以下文件中是一致的：
- `/Users/kozmosa/code/scholar-agent/docs/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`

#### 2. 都认为 framework 不是对单个开源仓库的复述
framework 页明确说这是“自有框架蓝图”；
summary 页也说 framework 是从多仓库调研中单独抽象出来的。

#### 3. 都把 framework 的核心价值指向“自建研究系统”
summary 页说如果目标已从“选仓库”转向“做自己的研究系统”，应继续读 framework；
docs 首页也把 framework 作为“构建自己的研究系统”的优先入口。

### 不完全一致的地方

#### 1. 仓库整体身份的表述深度不一致
- `docs/index.md` 更像在介绍“一个调研笔记知识库”
- `framework/index.md` 和 `ai-native-research-framework.md` 已经在介绍“一个明确可实现的有界自治研究系统蓝图”
- `PROJECT_BASIS.md` 又进一步指出仓库当前目标是：
  - 沉淀学术研究 Agent 调研笔记与框架设计
  - 同时维护一个可扩展的 `ainrf`

这说明仓库真实身份其实已经是三层结构：
1. 调研知识库
2. framework 设计库
3. `ainrf` 运行时实现 scaffold

但 docs 首页目前主要强调了前两层，对第三层几乎没外显。

#### 2. “framework” 的命名存在轻微摇摆
- docs 和 framework 文档主称呼是 `AI-Native Research Framework`
- roadmap / RFC 等实现文档大量使用 `AINRF`
- `PROJECT_BASIS.md` 又说“维护一个可扩展的 ainrf”

这并不冲突，但对外叙事还没收敛成一句清楚的话：
到底是
- “Scholar Agent 仓库，其中自有框架名为 AI-Native Research Framework，运行时包名为 ainrf”
还是
- “Scholar Agent 其实就是 AINRF 项目”

目前文本更接近前者，但仓库入口还没明确写死。

#### 3. docs 首页对 framework 的能力定义比较弱
docs 首页只说它是“基于参考项目抽象出的 framework”，
但 framework 主文档已经明确到：
- 宿主无关
- repo 优先
- 工件图谱驱动
- bounded autonomy
- 两种 mode
- 容器执行
- 人工关卡

因此首页对 framework 的介绍仍偏“来源描述”，不够“产品/系统定义”。

---

## 3) 需要统一的叙事

我建议统一成下面这条主叙事：

### 推荐统一叙事
`scholar-agent` 是一个面向学术研究 Agent 的仓库，包含三部分：
1. 对外部 academic research agent 项目的静态调研与能力地图；
2. 基于这些证据抽象出的自有框架 `AI-Native Research Framework (AINRF)`；
3. 该框架的 Python 运行时与 CLI 实现 `ainrf`。

其中：
- `summary` 负责“证据层/比较层”
- `framework` 负责“系统蓝图层”
- `src/ainrf` 负责“实现层”

### 用一句更稳的对外表述
可以收敛成：

“Scholar Agent 是一个面向学术研究 Agent 的研究与实现仓库：先通过多项目静态调研建立能力地图，再抽象出自有的 AI-Native Research Framework（AINRF），并逐步落地为 `ainrf` 运行时。”

### 这样统一后的好处

#### 1. 解决首页过于“笔记仓库化”的问题
现在首页首先像知识库，统一后能更清楚表明这是“研究 + 设计 + 实现”的仓库。

#### 2. 解决 framework 与 ainrf 的关系不清
明确：
- Framework 是概念/蓝图名
- AINRF 是缩写
- `ainrf` 是代码包/CLI 名

#### 3. 让 summary 与 framework 分工更稳定
- summary 不再像 manifesto
- framework 不再像单纯读书笔记
- 仓库整体叙事变成从证据到系统再到实现的连续链条

---

## 简明结论

### 1. 当前对外叙述
- 仓库入口没有 README，顶层对外叙述缺失。
- docs 首页把仓库讲成“学术研究 Agent 调研知识库 + framework 导航”。
- summary 把自己讲成“外部项目能力地图/证据层”。
- framework 把自己讲成“有界自治研究系统蓝图”。

### 2. 是否与 framework 一致
- 大方向一致。
- 但首页更像“笔记仓库”，framework 页更像“系统蓝图”，`PROJECT_BASIS.md` 还额外揭示了 `ainrf` 实现层，三者没有完全收敛成一套统一入口叙事。

### 3. 需要统一的叙事
建议统一为：
- Scholar Agent = 调研证据层 + framework 蓝图层 + ainrf 实现层
- AI-Native Research Framework (AINRF) = 自有框架名
- `ainrf` = 该框架的运行时/CLI 包名

如果你愿意，我下一步可以继续只读地帮你把这三处文档抽成一份“统一文案差异清单”，逐段指出哪些句子偏“知识库叙事”、哪些句子偏“系统叙事”。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore note conventions",
  "description": "inspect note metadata",
  "prompt": "只读检查 docs/framework/ 文档的 YAML frontmatter、标签、命名、slug、创建/更新时间等元数据约定。不要修改任何文件。返回：1) 现有元数据模式；2) 不一致点；3) 后续更新时建议遵循的最小规范。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a7341063ffec1yGLE4ztbKf26 (for resuming to continue this task if needed)

<task_result>
以下是对 `docs/framework/` 的只读检查结果。未修改任何文件。

检查范围：
- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`

---

## 1) 现有元数据模式

### A. YAML frontmatter 基本结构
`docs/framework/` 下 8 篇文档的 frontmatter 结构高度一致，当前实际模式是：

```yaml
---
aliases:
  - ...
tags:
  - ...
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
```

也就是当前共同字段基本固定为 5 个：

- `aliases`
- `tags`
- `source_repo`
- `source_path`
- `last_local_commit`

### B. 字段使用习惯

#### 1. `aliases`
- 始终存在
- 类型始终为 YAML 列表
- 通常 1 个别名，少数 2 个别名
- 别名语言不完全统一：
  - 英文：如 `AI-Native Research Framework`
  - 中文：如 `容器工作区协议`
  - 中英混合：如 `AINRF V1 RFC`、`V1 实现规格`

#### 2. `tags`
- 始终存在
- 类型始终为 YAML 列表
- 标签模式表现为：
  - 一个稳定公共主标签：`research-agent`
  - 一个稳定分类标签：`framework-design`
  - 再加 1~2 个文档类型/主题标签，例如：
    - `system-note`
    - `architecture`
    - `infrastructure`
    - `summary`
    - `v1-spec`
    - `rfc`
    - `roadmap`
    - `obsidian-note`
    - `index`

#### 3. `source_repo`
- 8 篇文档全部是：
  - `source_repo: scholar-agent`

#### 4. `source_path`
- 8 篇文档全部是：
  - `source_path: /home/xuyang/code/scholar-agent`

这说明当前约定里，`source_path` 记录的是仓库根路径，而不是单篇文档路径。

#### 5. `last_local_commit`
- 8 篇文档全部是：
  - `last_local_commit: workspace aggregate`

即当前 framework 文档并未记录具体 commit hash，而是统一使用聚合型占位值。

---

### C. 文件命名 / slug 实际模式

虽然 frontmatter 里没有显式 `slug` 字段，但文件名本身已经承担了 slug 角色。现有模式较一致：

- 全部为英文小写
- 使用 kebab-case
- 无空格、无中文、无下划线
- 对版本类文档使用 `v1-` 前缀

现有文件名如下：

- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`

### D. 标题与命名关系
H1 与文件名整体上是对应的，但不是机械一一同名，而是“slug 对应主题，H1 可更自然表达”的模式，例如：

- `ai-native-research-framework.md`
  - `# AI-Native Research Framework：有界自治研究系统蓝图`
- `v1-rfc.md`
  - `# AINRF V1 RFC：有界自治研究引擎实现规格`
- `reference-mapping.md`
  - `# 参考项目到框架映射`

可见当前更像是：
- 文件名负责稳定引用与链接
- H1 负责面向阅读的正式标题
- `aliases` 负责补充检索入口

### E. 创建/更新时间字段现状
在 `docs/framework/` 中未发现以下显式时间类元数据字段：

- `created`
- `updated`
- `date`
- `created_at`
- `updated_at`

也未发现显式：

- `slug`
- `title`

即当前 framework 文档的标题由 H1 表达，而不是 frontmatter 中的 `title` 字段。

---

## 2) 不一致点

这里分成“目录内不一致”和“与合理约定/当前环境相比的不一致”。

### A. 目录内整体一致性其实较高
严格说，`docs/framework/` 内部 frontmatter 结构本身非常整齐，几乎没有“这篇有那篇没有”的明显结构性混乱。

但仍有一些可视为不一致或潜在不稳定点：

---

### B. `aliases` 的命名语言与风格不统一
例子：

- 英文：
  - `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
    - `AI-Native Research Framework`
  - `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
    - `Research Artifact Graph`
- 中文：
  - `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
    - `容器工作区协议`
  - `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
    - `参考项目到框架映射`
- 中英混合：
  - `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
    - `AINRF V1 RFC`
    - `V1 实现规格`

这不一定是错误，但说明当前没有统一规定：
- alias 是否优先英文
- 是否必须包含中文别名
- 是否需要中英双别名

---

### C. `tags` 的“文档类型语义”不完全统一
公共标签稳定，但最后一层标签口径不完全一致：

- `system-note`
- `architecture`
- `infrastructure`
- `summary`
- `obsidian-note`
- `index`
- `v1-spec`
- `rfc`
- `roadmap`

问题不在“有差异”，而在“分类维度混用”：
- 有的是内容类型：`architecture` / `summary`
- 有的是文档角色：`index`
- 有的是媒介/工具属性：`obsidian-note`
- 有的是阶段/版本属性：`v1-spec`
- 有的是文档体裁：`rfc` / `roadmap`

这表示标签体系还没有严格分层。

---

### D. `source_path` 与当前实际环境不一致
所有 framework 文档都写的是：

```yaml
source_path: /home/xuyang/code/scholar-agent
```

但当前实际仓库路径是：

- `/Users/kozmosa/code/scholar-agent`

所以这批文档里的 `source_path` 是历史机器路径，不是当前环境路径。

这带来两个问题：

1. 如果 `source_path` 被视为“当前本地真实路径”，那它已经失真。
2. 如果它只是“原始作者工作路径”，那字段名 `source_path` 容易让人误解为当前有效路径。

这是本次检查里最明确的元数据不一致点。

---

### E. `last_local_commit` 全部为占位值，缺少精确性
`docs/framework/` 下所有文件统一是：

```yaml
last_local_commit: workspace aggregate
```

这在目录内是一致的，但如果把它当成“提交追踪元数据”，信息量很弱，且与仓库中其他文档的用法并不完全一致。

例如仓库其他 `docs/` 文档里存在更具体的写法，如：
- `last_local_commit: d9ea76f`
- `last_local_commit: 7975cfa`
- 或带 hash + subject 的更完整形式

因此，`docs/framework/` 当前写法更像“占位说明”，不是稳定可解析元数据。

---

### F. 缺少显式 `slug`
现在 slug 实际依赖文件名，这在 Obsidian/MkDocs 语境下通常可行，但从“元数据约定”角度看，有一个事实：

- 你要求检查 `slug` 元数据时，`docs/framework/` 实际没有 `slug` 字段

所以现状应表述为：
- “slug 约定存在，但它是隐式的文件名约定，不是显式 frontmatter 字段。”

---

### G. 缺少创建/更新时间元数据
如果你希望文档元数据涵盖“创建/更新时间等”，那么 `docs/framework/` 当前是空缺状态：
- 没有 `created`
- 没有 `updated`

这不是“个别文档不一致”，而是“整个目录尚未采用这类字段”。

---

### H. `index.md` 的标签口径与其他正文页略有不同
`/Users/kozmosa/code/scholar-agent/docs/framework/index.md` 使用：

- `obsidian-note`
- `index`

而其他框架正文页更偏：
- `architecture`
- `summary`
- `system-note`
- `v1-spec`

这本身合理，但如果未来要统一标签体系，需要明确：
- `index` 是页面角色标签
- `obsidian-note` 是否应作为全局标签，还是无必要

---

## 3) 后续更新时建议遵循的最小规范

下面给的是“最小规范”，尽量不引入过多字段，优先保持你现在已有风格，只补齐最必要的约束。

---

### 最小规范建议

#### 1. frontmatter 最少保留这些字段
建议 `docs/framework/` 后续每篇都至少包含：

```yaml
---
aliases:
  - ...
tags:
  - research-agent
  - framework-design
source_repo: scholar-agent
source_path: /Users/kozmosa/code/scholar-agent
last_local_commit: <commit-hash-or-aggregate>
---
```

说明：
- `aliases` 必填，至少 1 个
- `tags` 必填，至少包含两个基础标签：
  - `research-agent`
  - `framework-design`
- `source_repo` 固定填 `scholar-agent`
- `source_path` 若保留，应统一为仓库根绝对路径，且与当前有效环境一致
- `last_local_commit` 应有明确规则：
  - 要么统一允许 `workspace aggregate`
  - 要么统一改为具体 hash
  - 不建议混用且无说明

---

#### 2. slug 以文件名为准，不必强制新增 frontmatter 字段
最小规范下，建议直接规定：

- slug = Markdown 文件名（不含 `.md`）
- 必须使用英文小写 kebab-case
- 版本文档可用 `v1-...` 前缀
- 不要求再额外新增 `slug:` 字段

这样最符合你当前仓库现状，也最少改动。

---

#### 3. H1 与 slug 保持“主题对应”，不要求完全同名
建议规则：

- 每篇正文只有一个 H1
- H1 应与文件名表达同一主题
- 可比 slug 更完整、更自然，可中英混合或中文为主
- `aliases` 用来补充检索，不必与 H1 完全一致

这与当前目录现状兼容。

---

#### 4. 标签最小分层建议
为了避免继续发散，建议每篇最多按“三层”思路打标签：

- 固定域标签：
  - `research-agent`
- 固定目录标签：
  - `framework-design`
- 可选文档类型标签，最多 1~2 个：
  - `architecture`
  - `summary`
  - `index`
  - `rfc`
  - `roadmap`
  - `v1-spec`
  - `infrastructure`

最小原则：
- 不再随意新增同义类型标签
- `obsidian-note` 这种“工具属性标签”可以考虑不再新增，除非全库都要统一使用

---

#### 5. `aliases` 建议采用更稳的最低口径
建议最小规则：

- 每篇至少 1 个 alias
- 优先给“读者最可能搜索的标题形式”
- 对关键文档可补一个中英别名，但不是强制

例如：
- 英文主名 + 中文说明名
- 或中文主名 + 英文简称

但要避免没有标准地混杂过多变体。

---

#### 6. 创建/更新时间：如果要加，就统一加；如果暂时不加，就明确“不维护”
当前目录没有任何 `created/updated` 字段，所以最小规范有两个可选方向：

**方案 A：继续不加**
- 直接规定：framework 文档不维护 `created` / `updated` frontmatter，时间以 git 历史为准

**方案 B：从现在开始统一加**
- 每篇新增：
  - `created: YYYY-MM-DD`
  - `updated: YYYY-MM-DD`

如果你想保持最小成本，我更建议方案 A，因为它最符合现状；但要在规范里明确“时间以 git 为准”，否则会持续有人期待 frontmatter 时间。

---

#### 7. `source_path` 建议收敛为两选一
这是最值得马上统一的点。

**建议二选一：**

- 要么保留 `source_path`，但必须始终写当前仓库根路径，并随环境迁移更新
- 要么删除这类本机绝对路径字段的使用约定，避免机器相关路径污染元数据

从长期可移植性看，后者更稳；但如果你只想定义“最小规范且兼容现状”，那就至少要求：
- `source_path` 必须反映当前有效仓库根路径
- 不允许保留已失效的历史机器路径

---

#### 8. `last_local_commit` 建议明确语义
最小规范建议写成以下之一：

- 精确模式：`last_local_commit: <short-hash>`
- 聚合模式：`last_local_commit: workspace aggregate`

但同一目录最好统一一种，不要部分精确、部分占位，又没有说明。

---

## 总结

### 现状一句话总结
`docs/framework/` 的 frontmatter 结构其实已经比较整齐，当前真正的问题不是“缺字段乱写”，而是：
- `source_path` 已与当前环境不符
- `last_local_commit` 偏占位化
- `slug` / 创建时间 / 更新时间目前都是隐式或缺失状态
- 标签和 alias 口径还没有被明确规范化

### 我建议优先处理的 3 个规范点
如果只定最小规范，优先明确这三件事：

1. `slug` 以文件名为准，统一英文 kebab-case  
2. `tags` 至少固定 `research-agent` + `framework-design`，其余只加 1~2 个类型标签  
3. `source_path` 和 `last_local_commit` 明确语义并统一写法

如果你愿意，我下一步可以继续只读地帮你把这 8 篇文档整理成一张“元数据审计表”，逐文件列出：
- 文件名
- aliases
- tags
- H1
- 是否缺少 created/updated
- 是否存在潜在命名/标签问题
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "explore research framing",
  "description": "study framing language",
  "prompt": "只读从 Awesome-AI-Scientist 中提炼适合用于 scholar agent framework 文档的 framing language，例如 system goals, design principles, loop, artifacts, evaluation, knowledge capture。不要修改任何文件。返回：1) 可借鉴表达；2) 更适合 scholar agent 的改写方向；3) 3-5 个可作为章节名的短语。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a734105fffd2VtAgc0mAYlOj6 (for resuming to continue this task if needed)

<task_result>
下面是基于只读检索，对 `Awesome-AI-Scientist` 中适合迁移到 `scholar-agent framework` 文档的话语框架做的提炼。此次未修改任何文件。

主要参考来源：
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/README.md`
- `/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist/AGENTS.md`
- 对照约束：`/Users/kozmosa/code/scholar-agent/PROJECT_BASIS.md`

先给一个总判断：  
`Awesome-AI-Scientist` 更像“研究自动化生态/版图”的编目型 framing，而 `scholar-agent` 更适合采用“面向研究工作流的知识型 agent framework” framing。也就是说，可借鉴其分层、阶段、评估、协作、验证这些表达骨架，但需要从“全自动科研”收敛到“研究支持、知识沉淀、可验证流程、人与 agent 协同”。

---

## 1) 可借鉴表达

我按你点名的几个维度来提炼。

### A. System goals

`Awesome-AI-Scientist` 中可借鉴的表达骨架：

- “AI-powered research automation”
- “assist researchers throughout the entire research lifecycle”
- “structured overview of the AI researcher ecosystem”
- “empower researchers and accelerate breakthroughs”
- “automate multiple stages of the research cycle”
- “human-AI collaboration patterns”
- “AI for reproducibility & validation”

这些表达的优点：
- 目标对象清楚：researchers / scientific discovery
- 作用方式清楚：assist / automate / validate / collaborate
- 范围组织清楚：lifecycle / stack / stages

适合迁移成 scholar-agent 的核心语气：
- 不是单点工具，而是“覆盖研究生命周期若干关键环节的支持系统”
- 不是纯聊天，而是“围绕知识、假设、验证、产出组织工作流”

---

### B. Design principles

从 `AGENTS.md` 可抽出的原则性表达很值得借鉴，虽然它本来是仓库协作规范，但很适合转成 framework 原则：

- “optimize for factual accuracy”
- “link quality”
- “formatting consistency”
- “minimal diffs”
- “Preserve the current information architecture”
- “Prefer minimal, local edits over broad cleanup passes”
- “Do not silently remove content because it looks imperfect; verify first”
- “flag ambiguity instead of guessing”
- “never add unverified claims”
- “keep the diff tight and avoid unrelated reformatting”

这些话非常适合 scholar-agent 文档里的设计原则层，只要稍作泛化即可。  
它们体现的是：

- 事实优先，不臆断
- 局部增量，不大拆大改
- 保留信息结构
- 遇到歧义先显式标注
- 先验证，再陈述

这套气质其实很契合学术型 agent。

---

### C. Loop

`README.md` 里的 loop 不是显式“agent loop”写法，但它给了一个很好的研究阶段循环骨架：

- Knowledge Building / Knowledge Acquisition
- Idea Generation
- Verification and Falsification
- Review System
- Evolution
- Evaluation

再加上 `AGENTS.md` 的 workflow：

- read context
- find the appropriate section
- check whether it already exists
- match local pattern
- verify links
- review output
- keep changes tight

可抽象成 scholar-agent 的 loop 语言：

- ingest context
- synthesize knowledge
- generate hypotheses or plans
- verify / falsify / reproduce
- review and refine
- capture outputs into reusable knowledge

它的好处是：
- 有研究味，不只是 generic task loop
- 自带“验证-复盘-沉淀”闭环
- 兼容 scholar-agent 目前以文档和知识框架为主的仓库定位

---

### D. Artifacts

`Awesome-AI-Scientist` 不是 artifact-first 文档，但实际隐含了很多产物类型：

- structured overview
- papers / code / reviews
- benchmarks
- survey
- project list
- evaluation results
- report generation
- knowledge graph / leaderboards
- literature retrieval and summarization outputs

可借鉴的 artifact framing：

- knowledge artifacts
- review artifacts
- evaluation artifacts
- research outputs
- structured summaries
- evidence-linked records

对于 scholar-agent，特别适合强调：
- 每一步都应产出“可追溯、可复用、可链接”的文档资产
- 产物不是一次性中间态，而是知识库的一部分

---

### E. Evaluation

这是 `Awesome-AI-Scientist` 很强的一点，因为其目录结构天然强调 evaluation：

- Evaluation
- Evaluation Benchmarks
- rigorous assessment
- reproducibility
- validation
- benchmarking
- human evaluation
- faithfulness
- novelty and diversity
- uncertainty in evaluations

这些表达说明它对“研究 agent 的好坏如何判定”有天然意识。  
可借鉴的评价维度语言包括：

- retrieval quality
- faithfulness
- novelty
- diversity
- reproducibility
- rigor
- benchmarked performance
- human review / review-backed judgment
- uncertainty-aware evaluation

---

### F. Knowledge capture

这部分在 `README.md` 里主要通过“知识获取 / 检索 / 总结 / synthesis / knowledge graph / leaderboards”体现，在 `AGENTS.md` 中则通过“保留结构、避免重复、分类放置、验证链接”体现。

可借鉴表达：

- Knowledge Acquisition
- Knowledge Retrieval and Summarization
- Knowledge Building
- synthesizing existing work
- knowledge graph construction
- structured overview
- canonical source / official source
- check duplicates by title and URL
- place the item in the most specific matching subsection

这些词很适合迁移成 scholar-agent 的 knowledge capture 语言，尤其是：
- 从原始文献到结构化条目
- 从一次回答到长期知识资产
- 从碎片信息到带来源的 synthesis

---

## 2) 更适合 scholar agent 的改写方向

下面我按主题给出“原 framing 倾向 -> 更适合 scholar-agent 的改写方向”。

---

### A. System goals

#### 可借鉴原表达
- “AI-powered research automation”
- “assist researchers throughout the entire research lifecycle”
- “empower researchers and accelerate breakthroughs”

#### 更适合 scholar-agent 的改写方向
不要把目标写成“fully automated scientific discovery”，而是写成：

- “support knowledge-intensive scholarly workflows”
- “help researchers build, test, and refine structured understanding”
- “augment research thinking with traceable evidence and reusable artifacts”
- “accelerate scholarly sensemaking, not replace scholarly judgment”

更贴合你们仓库现状的中文方向可以是：

- 面向学术研究工作流的知识型 agent 框架
- 支持研究者完成资料收集、结构化理解、问题形成、验证记录与成果沉淀
- 以可追溯证据和可复用文档资产为核心，而非追求端到端自动科研

---

### B. Design principles

#### 可借鉴原表达
- factual accuracy
- verify first
- flag ambiguity instead of guessing
- preserve information architecture
- minimal diffs

#### 更适合 scholar-agent 的改写方向
把仓库编辑原则，升级成 agent 设计原则：

1. Evidence before assertion  
   先证据，后结论；不把流畅表述当作可靠结论。

2. Traceability by default  
   默认保留来源、上下文和推导痕迹。

3. Incremental knowledge building  
   优先增量沉淀，不追求一次性重写世界模型。

4. Ambiguity should be surfaced, not hidden  
   遇到歧义要显式暴露，必要时保留 competing interpretations。

5. Outputs should fit the knowledge base  
   产物应能进入长期知识结构，而不是只服务单轮会话。

这比单纯说“accuracy/consistency”更像 framework，而不是内容仓库规范。

---

### C. Loop

#### 可借鉴原表达
- Knowledge Acquisition
- Idea Generation
- Verification and Falsification
- Review System
- Evolution

#### 更适合 scholar-agent 的改写方向
建议不要直接复刻“科研自动化五段论”，而改成更适合 scholar-agent 的闭环：

1. Frame the research task  
2. Gather and structure evidence  
3. Synthesize and identify gaps  
4. Propose next questions / claims / plans  
5. Verify, review, or challenge  
6. Capture reusable knowledge artifacts

中文可写成：

- 任务界定
- 证据收集
- 知识综合
- 问题与假设形成
- 验证与审阅
- 知识沉淀与复用

这样兼容文档型、综述型、规划型、实验前期研究，不会过度承诺自动实验能力。

---

### D. Artifacts

#### 可借鉴原表达
- reviews
- benchmarks
- survey
- report generation
- knowledge graph
- structured overview

#### 更适合 scholar-agent 的改写方向
scholar-agent 的 artifact 不应主要写成“paper/report/code”三件套，而应更偏知识库友好：

- source-backed notes
- structured literature summaries
- comparison matrices
- research question frames
- verification logs
- decision records
- reusable synthesis documents

中文可表述为：

- 带来源的研究笔记
- 结构化文献摘要
- 对比矩阵与证据表
- 问题框定与假设卡片
- 验证记录与评审意见
- 可复用的综合性文档资产

这会更贴合 `docs/framework/`, `docs/projects/`, `docs/summary/` 的长期边界。

---

### E. Evaluation

#### 可借鉴原表达
- evaluation
- benchmarks
- rigorous assessment
- reproducibility
- novelty and diversity
- human evaluation
- uncertainty in evaluations

#### 更适合 scholar-agent 的改写方向
对 scholar-agent，评估要从“科研成果是否新颖”转成“知识工作流是否可靠有效”：

建议评估维度写成：

- retrieval quality: 找到的是否相关、充分、可追溯
- synthesis faithfulness: 综合是否忠于来源
- structural usefulness: 产物是否便于后续复用
- gap identification quality: 是否能正确发现未知与争议
- verification discipline: 是否区分事实、推断、假设
- human collaboration quality: 是否降低研究者认知负担
- longitudinal knowledge value: 产物是否能沉淀为长期知识资产

这比“novelty benchmark”更适合当前 scholar-agent。

---

### F. Knowledge capture

#### 可借鉴原表达
- Knowledge Building
- Knowledge Retrieval and Summarization
- synthesizing existing work
- knowledge graph construction
- structured overview

#### 更适合 scholar-agent 的改写方向
建议把 knowledge capture 提升为 framework 的一等公民，而不是附属功能：

- every meaningful loop should leave a reusable artifact
- notes should preserve source, claim, context, and open questions
- synthesis should connect documents, not merely compress them
- knowledge capture should support future retrieval, comparison, and review

中文更适合的说法：

- 每个有效工作回合都应留下可复用知识产物
- 沉淀的不只是摘要，还包括来源、主张、证据、分歧与未决问题
- 知识捕获的目标不是压缩文本，而是支持未来检索、比较、复核与扩展
- 会话输出应尽量转化为长期知识库中的结构化资产

这部分和你们 `PROJECT_BASIS.md` 中“长期知识资产”“docs/ 结构化归档”的方向非常一致。

---

## 3) 3-5 个可作为章节名的短语

下面给 5 个短语，偏 framework 文档风格，且较短：

1. System Goals
2. Design Principles
3. Research Loop
4. Knowledge Artifacts
5. Evaluation and Capture

如果你想更贴近 scholar-agent 的语气，我更推荐这一组：

1. Scholar Agent Goals
2. Operating Principles
3. Research Work Loop
4. Reusable Artifacts
5. Knowledge Capture

如果想更中文化、适合你们文档正文标题，可用：

1. 系统目标
2. 设计原则
3. 研究闭环
4. 产物模型
5. 知识沉淀

---

## 附：一句话总结建议

如果要把 `Awesome-AI-Scientist` 的 framing 借来给 `scholar-agent`，最值得借的不是“全自动科研”的口号，而是这条主线：

“围绕研究生命周期组织 agent 能力，以知识获取、问题形成、验证审阅、评估与长期沉淀为核心，产出可追溯、可复用的学术工作流资产。”

如果你愿意，我下一步可以继续只读帮你把这些内容整理成一版更像 `docs/framework/` 章节提纲的中文框架草案。
</task_result>
```

---

## Assistant (Plan · gpt-5.4 · 39.6s)

先给你一句更自然的英文改写，后续我会继续用简体中文和你交流。

Refined English:
`Please use the newly added reference repository, Awesome-AI-Scientist, to properly update the Scholar Agent framework documentation in Chinese. Also, please polish my requests into more natural English, and use Simplified Chinese when talking with me from now on. You may launch up to 24 subagents in parallel, and should not use fewer than 16 unless you are confident that fewer are sufficient. For now, start with exploration and planning only.`

**探索结论**
我已经按只读方式完成了一轮并行探索，覆盖了现有 `docs/framework/`、`docs/index.md`、`docs/summary/`、`src/ainrf/` 的实际边界，以及参考仓库 `ref-repos/Awesome-AI-Scientist` 的可借鉴结构。

当前判断比较明确：

1. `Awesome-AI-Scientist` 适合作为“能力分类法”和“研究生命周期 framing”的参考，不适合直接当成工程实现蓝图照搬。
2. 你现有的 `framework` 文档体系已经有主干，但还缺几块对“properly update”非常关键的内容：
   - 面向读者的统一总叙事
   - 生命周期总图
   - source of truth 分层说明
   - 知识沉淀策略
   - `docs/` 与 `src/ainrf/` 的关系
   - 当前实现态 vs 设计态的明确边界
3. 当前仓库整体叙事其实已经是三层，但文档入口还没有完全统一：
   - 调研证据层：`docs/projects/` + `docs/summary/`
   - 框架蓝图层：`docs/framework/`
   - 运行时实现层：`src/ainrf/`

**参考仓库最值得借的东西**
从 `Awesome-AI-Scientist` 看，最值得迁移到 Scholar Agent framework 的不是论文列表，而是这几个结构：

1. 用研究生命周期组织顶层叙事
   - Knowledge Acquisition
   - Idea Generation
   - Verification and Falsification
   - Review
   - Evolution

2. 把评估和验证单独抬出来
   - 不只讲“能做什么”
   - 还讲“如何判断做得是否可靠”

3. 把 review / critique 当成横切能力
   - 不是末尾附属步骤
   - 而是贯穿知识整理、计划、验证、写作的质量约束层

4. 把动态规划和持续演化作为闭环层
   - 很适合你现在的 scholar-agent 方向
   - 但需要比参考仓库更克制，不要写成“全自动科学家”口号

**不建议直接照搬的部分**
1. 单个超长 `README` 承载全部内容
2. 资源策展式写法替代系统设计
3. 宣传化英文和过强的自动科研叙事
4. 把论文分类直接当成 runtime 架构

**建议的文档更新方向**
如果下一阶段进入执行，我建议把这次更新定义成“框架文档重构与校正”，不是零散润色。最合适的更新目标是：

1. 统一总叙事
2. 借鉴 `Awesome-AI-Scientist` 的生命周期结构
3. 明确当前仓库真实边界
4. 补齐缺失章节
5. 修正部分英文术语表达
6. 补强 cross-link 和导航

**建议的具体落点**
优先修改这些文档：

1. `docs/framework/index.md`
   - 强化入口定位
   - 明确三层结构：证据层 / 蓝图层 / 实现层
   - 增加“如何阅读”与“当前实现状态”提示

2. `docs/framework/ai-native-research-framework.md`
   - 作为总纲页重写一部分 framing
   - 吸收 `Awesome-AI-Scientist` 的 lifecycle 语言
   - 增加系统目标、设计原则、知识沉淀、与 Obsidian/docs 的关系

3. `docs/framework/artifact-graph-architecture.md`
   - 明确三层 source of truth：
     - `.ainrf/` runtime state
     - future project repo artifacts
     - `docs/` long-lived knowledge
   - 解释状态升级路径和知识沉淀路径

4. `docs/framework/v1-dual-mode-research-engine.md`
   - 加一张更统一的端到端生命周期图
   - 把任务闭环和研究闭环分开

5. `docs/framework/v1-rfc.md`
   - 明确“当前已实现什么 / 还没实现什么”
   - 避免让读者误以为 Mode 1 / Mode 2 已经完整跑通

6. `docs/framework/v1-roadmap.md`
   - 校正和当前代码实现不一致的术语与事件名
   - 加一个“设计态 vs 已实现态”矩阵

7. `docs/framework/reference-mapping.md`
   - 用更自然的英文术语
   - 强化从参考项目到 Scholar Agent 决策的映射逻辑

**我建议新增或补出的章节**
不一定都新建文件，更建议尽量落到现有页面里，保持最小变更。

建议补这些内容：

1. 系统目标
2. 研究闭环
3. 运行时与知识库边界
4. 知识沉淀策略
5. 当前实现状态
6. 术语规范
7. 设计原则到决策的映射

**英文表达需要顺手优化的重点**
探索里看到一些表达可以统一得更自然。后续执行时我建议顺手修掉这些高优先级项：

1. `human-on-the-loop` -> `human-in-the-loop`
2. `paper intake` -> `paper ingestion`
3. `Deep Repro` -> `Deep Reproduction`
4. `Lit Exploration` -> `Literature Exploration`
5. `citation discipline` -> `citation rigor` 或更上下文相关的表达
6. `bounded-autonomous research evidence engine` -> 更自然、少口号化的表述

**执行计划**
如果你确认进入下一步，我建议按下面顺序真正动手：

1. 创建今天的 worklog
   - `docs/LLM-Working/worklog/2026-04-04.md`

2. 先改入口和总纲
   - `docs/framework/index.md`
   - `docs/framework/ai-native-research-framework.md`

3. 再改边界最容易失真的两篇
   - `docs/framework/artifact-graph-architecture.md`
   - `docs/framework/v1-rfc.md`

4. 再改工作流和路线图
   - `docs/framework/v1-dual-mode-research-engine.md`
   - `docs/framework/v1-roadmap.md`

5. 最后统一映射页与链接
   - `docs/framework/reference-mapping.md`
   - 必要时补部分 `projects/*` 的回链

6. 做文档验证
   - 至少跑一次文档构建
   - 检查主要 wikilink/导航是否闭环

**两个关键判断**
我现在比较倾向这两个编辑原则：

1. 不新开很多文档，优先在现有 framework 主干里补齐关键章节
2. 不把参考仓库写成“功能来源”，而是写成“结构启发”和“研究生命周期参照”

**需要你确认的一个问题**
为了避免我下一步在执行阶段做错方向，我只问一个关键问题：

你更希望这次更新偏向哪一种？

1. `保守整合`
   - 尽量保留现有文档结构
   - 主要补章节、校正叙事、统一术语、修链接

2. `中度重构`
   - 在保留主干文档的前提下，明显重写 `index`、总纲、RFC 的结构和叙事顺序
   - 让整个 framework 更像一套成型方法论文档

我目前推荐 `中度重构`。

---

## User

2. the project is now stuck at a bottleneck, there are mass of repositories aimed to (or claimed that they will) implement completely autonomous researches in all field, which we judged not possible currently. however, we should indeedly consider the future roadmap and plan of this repo causually. we may start a well-structured comprehensive docs refactoring and requirements(expectations) re-alignment for this project. that would not be finished in this conversation, so we have to exchange decisions and suggestions for that goal, write a comprehensive plan and roadmap so that we can push it forward step by step. we follow the communicating contract mentioned above in the whole session, so refine my statement first, restatement then, and finally start to do the solving work. now start to interview me.

---

## Assistant (Plan · gpt-5.4 · 39.4s)

_Thinking:_

**Preparing for the interview**

I need to refine my statement in English first, then translate it into Chinese before starting the interview. Since I’m in read-only mode, I could ask multiple questions using the question tool. I’m wondering if we even need any subagents since the user says they’re ready for the interview now. It seems like no further exploration is needed yet, so I’ll focus on asking structured questions.

Refined English:
`2. The project is currently stuck at a bottleneck. There are now many repositories aiming to implement, or at least claiming they will eventually enable, fully autonomous research across all fields. We currently judge that goal to be unrealistic. Even so, we should seriously and pragmatically think through this repository’s future roadmap and planning. I think we should begin a well-structured, comprehensive refactoring of the documentation, along with a realignment of the project’s requirements and expectations. This will not be finished in a single conversation, so we need to exchange decisions and suggestions toward that goal, and produce a comprehensive plan and roadmap that we can push forward step by step. We will follow the communication contract mentioned above throughout the whole session. Please first refine my statement, then restate it, and finally begin the actual problem-solving work. Start by interviewing me.`

**重述**
你的意思我理解为：

这个项目现在卡在一个关键瓶颈上。外部有很多仓库在做，或者声称未来会做“跨所有领域的完全自主研究”，但我们目前的判断是，这在现阶段并不现实。  
因此，这个仓库接下来不应该继续被“全自动科研”叙事牵着走，而是需要更冷静地重新定义目标、边界、路线图和预期管理。一个合适的起点，是发起一轮结构化、系统性的文档重构，以及项目需求/预期的重新对齐。  
这件事不可能在这一轮对话里完成，所以我们需要把它作为一个多轮推进的工作：持续交换判断、做决策、沉淀方案，最终形成一份可以分阶段执行的综合计划与路线图。

**当前工作方式**
现在处于只读规划阶段，我不会修改任何文件。  
我先通过访谈把你的核心判断、优先级、边界和预期钉牢，再据此整理一版“长期推进计划 + 文档重构路线图”。

**访谈目标**
这轮访谈我想先确认 6 件事：

1. 这个项目现在真正想成为什么
2. 你明确不想让它成为什么
3. 当前最卡住的瓶颈到底是哪几类
4. 文档重构要服务哪些决策，而不只是“写得更漂亮”
5. 未来 roadmap 要多激进，还是多保守
6. 这次需求/预期重对齐，最终要影响哪些层：
   - 对外叙事
   - framework 设计
   - implementation roadmap
   - repo structure
   - evaluation standard

**第一组问题：项目定位**
请你尽量按编号回答，短答也可以。

1. 你现在对 `scholar-agent` 的最核心定义是什么？
   - 例如更偏“研究框架”
   - “方法论仓库”
   - “研究工作流操作系统”
   - “知识型 agent 框架”
   - “未来 runtime 的设计仓库”
   - 或别的定义

2. 你希望这个项目在未来 6-12 个月最现实的主目标是什么？
   - 是先把 framework 讲清楚
   - 先把 runtime 边界讲清楚
   - 先做一个可信的最小可用系统
   - 先形成高质量研究/设计文档资产
   - 还是别的

3. 你认为这个项目当前最危险的误导性叙事是什么？
   - 例如“全自主科研”
   - “通用跨学科自动研究员”
   - “很快能端到端跑完整 research loop”
   - “现在已经接近产品化”
   - 或其他

**第二组问题：瓶颈判断**
4. 你说“项目卡在瓶颈”，这个瓶颈在你看来最主要是哪几项？
   - 愿景太大，边界太虚
   - 文档叙事和真实实现脱节
   - 需求不断漂移
   - 外部参考太多，难以抽象
   - 还没有统一评估标准
   - runtime 路线不清
   - repo 内三层内容混在一起
   - 其他

5. 如果这次只解决一个根本问题，你最想先解决哪一个？

**第三组问题：文档重构目标**
6. 你说“well-structured comprehensive docs refactoring”，在你心里它至少应该产出哪些东西？
   - 一套新的 framework 主线文档
   - 一套 requirements / expectations 文档
   - 一份 project positioning / manifesto
   - 一份 phased roadmap
   - 一份 glossary / terminology policy
   - 一份 implementation status 文档
   - 一份 architecture decision log
   - 你认为必须有的其他产物

7. 这次重构，你更希望它偏向哪种风格？
   - 更学术/研究设计文档
   - 更产品/系统规格文档
   - 更工程 roadmap 文档
   - 三者结合，但有主次

**第四组问题：预期重对齐**
8. 你希望这次“requirements(expectations) re-alignment”主要对齐谁的预期？
   - 你自己对项目的预期
   - 未来协作者/agent 的预期
   - 读者/外部访问者的预期
   - 未来实现者的预期
   - 这几类都要

9. 哪些明确应该被降级、降温、或者暂时移出主叙事？
   - 全自动科研
   - 全领域通用性
   - 无需人工 gate
   - 短期内做完整 runtime
   - 多 agent fully autonomous loop
   - 其他

10. 哪些反而应该被升格为主叙事？
   - bounded autonomy
   - evidence-grounded workflow
   - knowledge capture
   - human-in-the-loop research system
   - framework first, runtime later
   - domain-adaptable rather than domain-universal
   - 其他

**第五组问题：路线图哲学**
11. 你更倾向哪种 roadmap 哲学？
   - 先叙事重构，再设计收敛，再实现
   - 先明确 requirements，再倒推文档结构
   - 先做现状审计，再做目标蓝图，再做 gap roadmap
   - 你自己的顺序

12. 你希望 roadmap 更像：
   - 3 个阶段的大框架
   - 6-10 个里程碑的执行计划
   - 双层结构：长期方向 + 短期批次
   - 三层结构：vision / architecture / implementation
   - 其他

**建议回答方式**
你可以直接按下面这种格式回我：

```text
1. ...
2. ...
3. ...
...
12. ...
```

如果你愿意，我在你回答后会立即做三件事：

1. 提炼你的核心立场与约束
2. 归纳这次多轮工作的主问题树
3. 产出第一版“文档重构 + 需求/预期重对齐”的总计划框架

---

## User

1.Agent-driven Researching Copilot/Dashboard. 2. we have no such excess time for this project. pushing the project as a ready-for-use product and keeping refining the nature of the project in continuous development is the only possible way. 3. general ai-driven full-autonomous 24x7 researcher agent.(the combination of these too-big promises is toxic, however, we do not decline 24x7 subagent/agent as a specific role in helping research work, for example.) 4. all you mentioned 5.roadmap to next release ready-for-use version. 6.new version for framework docs, manifesto with clear versioning system(possibly semantic versioning, or simpler, v1.20260401, v2.20260403...), phased roadmap from current to next release, architechture design documentation with clear versioning system(share the versioning system with manifesto, but possibly not sync version with it from now and then), architechture decision log(versioning the same way, freeze after every release, and start a new empty log doc after releasing). 7.engineering>product/system>academic. 8.myself. 9. generality across many fields. 10. evidence-grounded workflow, robustness as a system(stability and really ready-for-use, a simple but helpful tool, not a fancy toy). 11.first. 12.decompose into several atomic tasks that can be finished one in one session.

---

## Assistant (Plan · gpt-5.4 · 53.9s)

_Thinking:_

**Refining the interview approach**

I need to focus on a respectful plan for the interview. First, I should refine my statements and maybe restate what they answered. Then, I can continue with the interview using more focused questions. It seems like it’s important to provide a synthesis of what we've discussed first before moving on to the next round of questions. It looks like I won’t need any tools for this — that should be sufficient!

Refined English:
`1. The project should be positioned as an agent-driven research copilot/dashboard. 2. We do not have excess time to develop this project slowly in isolation. The only realistic path is to keep pushing it toward a genuinely ready-to-use product while continuously refining its nature through ongoing development. 3. The most misleading narrative is the idea of a general AI-driven, fully autonomous, 24/7 researcher that can operate across all fields. That combination of oversized promises is toxic. That said, we do not reject 24/7 subagents or agents as specific supporting roles within a research workflow. 4. All of the bottlenecks you listed are real. 5. The immediate priority is a roadmap toward the next release that is genuinely ready for use. 6. We need a new version of the framework docs, a manifesto with a clear versioning system, a phased roadmap from the current state to the next release, architecture design documentation with explicit versioning, and an architecture decision log. The manifesto and architecture docs should share the same versioning scheme, though they do not need to stay perfectly synchronized forever. The decision log should be frozen after each release, and a new empty log should begin for the next cycle. 7. The priority order should be engineering first, then product/system, then academic framing. 8. The primary audience for this realignment is myself. 9. What should be de-emphasized is broad generality across many fields. 10. What should be elevated is an evidence-grounded workflow and robustness as a system: stability, real readiness for use, and a simple but helpful tool rather than a fancy toy. 11. The right order is to refactor the narrative first, then converge the design, and then implement. 12. The work should be decomposed into atomic tasks that can each be completed within a single session.`

**重述**
你的立场已经很清楚了，我先收敛成一版可执行表述：

`scholar-agent` 不应继续被定义成“跨所有领域、全天候、完全自主的通用研究员”。这类叙事当前既不现实，也会持续污染判断。  
你更希望把它定义为一个 `Agent-driven Researching Copilot/Dashboard`：它可以包含持续运行的 agent 或 subagent 角色，但这些角色应服务于研究工作流中的具体职责，而不是包装成一个“全能自动科学家”。  
由于没有额外时间做长期空转式设计，这个项目必须走“边开发边收敛定位”的路线：持续把它往真正可用、可发布、可依赖的产品推进，同时同步重构文档、收敛需求、修正预期。  
因此，接下来最关键的不是泛泛讨论愿景，而是围绕“下一版 ready-for-use release”做一轮系统性的文档重构与 requirements/expectations re-alignment，并把它拆成一批单会话可完成的原子任务。  
在优先级上，工程真实性高于产品包装，产品/系统叙事高于学术叙事；在价值取向上，应弱化跨领域通用性承诺，强化 evidence-grounded workflow、system robustness、稳定性、可用性，以及“简单但真正有帮助”的工具定位。  
为支撑这个方向，需要逐步建立一套带版本的文档体系：framework docs、manifesto、phased roadmap、architecture docs、architecture decision log，并以 release 为节奏冻结和续写。

**已确认的核心约束**
我先把已经确定的约束钉住，后面计划会以这些为准：

1. 项目定位
   - `Agent-driven Researching Copilot/Dashboard`

2. 路线原则
   - 必须朝“ready-for-use”推进
   - 不能先空转做很久纯设计
   - 文档重构和产品推进要并行

3. 明确反对的主叙事
   - 通用跨领域
   - 完全自主
   - 24x7 全能研究员
   - 大而空的 AI scientist 承诺

4. 允许保留的能力形式
   - 24x7 agent/subagent 作为特定角色
   - 但必须嵌入有边界的研究工作流

5. 最高优先级
   - 通向下一次可用 release 的 roadmap

6. 文档体系目标产物
   - 新版 framework docs
   - manifesto
   - phased roadmap
   - architecture design docs
   - architecture decision log

7. 价值排序
   - engineering > product/system > academic

8. 主要对齐对象
   - 你自己

9. 应强化的关键词
   - evidence-grounded workflow
   - robustness
   - stability
   - ready-for-use
   - simple but helpful

10. 工作拆解原则
   - 原子任务
   - 单会话可完成

**我现在的初步判断**
基于你的回答，这次长期工作的真实目标，不是“重写文档”本身，而是做三件事：

1. 重新定义这个项目到底是什么
2. 重新定义下一版 release 需要满足什么才算“可用”
3. 用文档体系把这个定义固定下来，避免项目继续被错误叙事牵着走

所以后续计划很可能要分成三条并行主线：

1. 定位与叙事线
   - manifesto
   - expectations realignment
   - non-goals

2. 设计与决策线
   - framework docs
   - architecture docs
   - architecture decision log

3. 交付与版本线
   - next-release roadmap
   - release criteria
   - session-sized atomic tasks

**第二轮访谈**
这轮我会更聚焦，直接为“总计划框架”补关键决策。仍然请你按编号简答。

**A. 产品定义**
1. 你说 `Research Copilot/Dashboard`，这里你更强调哪一个？
   - `Copilot`：以协助当前研究任务为主
   - `Dashboard`：以集中管理、观察、追踪研究流程为主
   - 两者并重，但有主次

2. “ready-for-use” 在你心里最低限度意味着什么？
   - 你可以直接说一组最小标准，比如：
   - 能稳定启动
   - 能完成某类典型任务
   - 有清晰的人机边界
   - 有可追踪输出
   - 有基本容错
   - 文档足够让你自己未来继续推进
   - 你最看重哪些

3. 下一次 release，你最希望用户实际能用它做什么？
   - 只选 1-3 个最重要的具体能力
   - 不要抽象愿景，尽量写成实际动作

**B. 非目标与边界**
4. 你希望下一版明确写进 `Non-Goals` 的内容有哪些？
   - 我建议至少会包括：
   - 全领域通用研究
   - 完全自主端到端研究
   - 无人工门控
   - 长周期无人监督探索
   - 你确认哪些必须写死

5. 你接受“领域聚焦”吗？
   - 例如先把目标限定为：
   - 文献理解与研究整理
   - 复现导向研究支持
   - 代码/论文相关研究工作流
   - 计算机科学邻域
   - 或你不想按学科限制，而想按任务类型限制

6. 你更想按什么来收缩范围？
   - 按领域收缩
   - 按任务类型收缩
   - 按工作流阶段收缩
   - 三者结合

**C. 下一版 release 的核心能力**
7. 如果下一版只能保住 3 个核心能力，你最想保哪 3 个？
   - 例如：
   - 任务 intake + planning + tracking
   - 文献/项目证据整理
   - 人工 gate 审批流
   - 研究工作台/dashboard
   - 工件/记录留痕
   - 运行稳定性
   - 可恢复与可观察性
   - agent 协作接口
   - 请你自己选

8. 哪些现有东西你觉得必须进入“下一版必须可用”清单？
   - 文档
   - CLI
   - API
   - dashboard/UI
   - task tracking
   - gate system
   - event stream
   - workspace management
   - parser integration
   - execution integration

9. 哪些东西你愿意明确延后？
   - 这样我后面才能把 roadmap 做得真的能落地

**D. 文档体系设计**
10. `manifesto` 在你心里更像什么？
   - 项目定位声明
   - 版本化产品哲学
   - requirements 与 expectations 的最高层文档
   - 对 framework/architecture/roadmap 的总入口
   - 你希望它承担哪些职责

11. `framework docs` 和 `architecture docs` 你希望怎么区分？
   - 我的理解可能是：
   - framework：做什么、为什么、边界是什么
   - architecture：系统如何组织与落地
   - 你是否认同，还是有别的划分

12. `architecture decision log` 你希望记录什么级别的决策？
   - 只记重大架构决策
   - 还是连重要产品边界决策也记
   - 是否要包含 rejected alternatives

**E. 版本与发布节奏**
13. 你偏好哪种版本风格？
   - 语义版本：`v0.1.0`
   - 日期版本：`v2026.04.04`
   - 混合版本：`v0.1-20260404`
   - 你前面提的 `v1.20260401` 这种也可以
   - 你更偏哪种，为什么

14. 你希望“文档版本”和“产品/release 版本”的关系是什么？
   - 强绑定
   - 弱绑定
   - manifesto/framework/architecture 共用大版本，但可各自演进小版本
   - 你希望怎么管理

15. “freeze after every release” 你是希望冻结哪些文档？
   - decision log
   - manifesto snapshot
   - architecture snapshot
   - roadmap snapshot
   - 全部或部分

**F. 计划执行方式**
16. 你说 atomic tasks 一次一会话完成。你更喜欢这些任务被组织成什么形式？
   - 按文档文件拆
   - 按决策主题拆
   - 按 release milestone 拆
   - 按 repo area 拆
   - 或混合方式

17. 你后续更希望我每轮产出什么？
   - 一版决策建议
   - 一版可执行任务清单
   - 一版文档结构草案
   - 一版 wording/refinement
   - 每轮都要包含哪些固定输出

18. 在这整个长期会话里，你更希望我保持哪种风格？
   - 更强主导，直接给收敛方案
   - 更强协商，先给 options 再让你选
   - 前期协商，后期强执行
   - 你偏好哪种

你回复这 18 个问题后，我下一步会做这三件事，仍然保持只读规划：

1. 输出一版“项目重新定位声明”
2. 输出一版“文档体系与版本体系草案”
3. 输出一版“从现在到 next ready-for-use release”的分层计划框架

---

## User

1.Dashboard; 2.can finish typical/simple/well-defined tasks independently and do not corrupt too frequentl; 3.Mode1/Mode2 described in current docs; 4. all you mentioned except 无人工门控 and 长周期无人监督探索; 5.accept; 6.task categories; 7.dashboard, stability, observable; 8.new modern webui dashboard(eg. using react or something else), task tracking, workspace management, container/session ssh integration, experiments results visualization(reproduced table and plots, show in webui); 9. anything except i mentioned should be implemented in next release. 10.requirements 与 expectations 的最高层文档; 11. framework are more abstract, focused on functions, philosophy of the project and how this project can be useful etc. architecture doc is strictly and closely bind with the project implementation itself, which is much more concrete about engineering design and tradeoff(though there may not be any code in architecture documentation). 12. first; 13.mixed version(eg. v1-20260401) currently, we can move to semantic versioning system when this project has stepped out rapid-changing stage. 14. weak binding; 15. log and snapshot. make them archived. 16. recommend a way. 17. suggestions and your understanding of the project and my requirements currently. 18. more collaborating. you should always take my decision and requirements seriously, but feel free to ask questions and provide suggestions. and more important, if you find that my thoughts are not well-constrained for engineering, too vague for designing, or conflicting with myself, point out my errors immediately.

---

## Assistant (Plan · gpt-5.4 · 55.6s)

Refined English:
`1. Dashboard. 2. A ready-to-use release should be able to complete typical, simple, and well-defined tasks independently, and it should not fail or corrupt things too frequently. 3. The next release should support Mode 1 and Mode 2 as currently described in the docs. 4. The Non-Goals should include everything you listed except “no human gate” and “long-running unsupervised exploration.” 5. I accept narrowing the scope. 6. We should narrow it by task categories. 7. The three core priorities are the dashboard, stability, and observability. 8. The next release must include a new modern web UI dashboard, task tracking, workspace management, container/session SSH integration, and experiment result visualization, including reproduced tables and plots shown in the web UI. 9. Everything I did not explicitly mention can be deferred beyond the next release. 10. The manifesto should be the highest-level document for requirements and expectations. 11. The framework docs should stay more abstract, focusing on the project’s functions, philosophy, and usefulness. The architecture docs should be tightly bound to implementation, with concrete engineering design and tradeoff discussion, even if they do not contain code. 12. The architecture decision log should record only major decisions. 13. For now, I prefer a hybrid versioning scheme such as v1-20260401. We can move to semantic versioning later, once the project is past this rapid-change stage. 14. Documentation versions and product/release versions should be only weakly coupled. 15. We should freeze and archive the decision log and release snapshots after each release. 16. Please recommend an execution structure. 17. In each round, I want your suggestions and your current understanding of the project and my requirements. 18. I prefer a collaborative style. You should take my decisions and requirements seriously, but feel free to ask questions and make suggestions. More importantly, if you find that my thinking is not well constrained for engineering, too vague for design, or internally inconsistent, point it out immediately.`

**重述**
你的方向现在已经比前一轮更清晰了：

这个项目下一阶段应优先被收敛为一个 `Dashboard` 型、agent-driven 的研究协作系统，而不是一个“大一统自动研究员”。  
“下一版可用”的最低标准不是宏大能力，而是能稳定完成典型、简单、边界明确的任务；系统可以独立工作，但不能频繁失效、状态损坏、或者不可观察。  
下一版的核心范围也更具体了：你要的是一个现代 Web UI dashboard，加上 task tracking、workspace management、container/session SSH integration，以及实验结果可视化。  
范围收缩方式上，你接受缩范围，但不按学科收，而是按任务类别收。  
文档体系上，`manifesto` 是最高层 requirements/expectations 文档；`framework docs` 负责抽象层的功能、哲学、用途与边界；`architecture docs` 负责与实际实现强绑定的工程设计与权衡；`decision log` 只记录重大决策，并在每次 release 后冻结归档。  
版本管理暂时采用混合风格，例如 `v1-20260401`；文档和产品版本弱绑定。  
你希望我在整个过程中保持协作式风格，但如果你的想法在工程上不收敛、设计上太虚、或前后冲突，我必须立即指出。

**先指出一个需要立刻收敛的工程冲突**
这里有一个很重要的潜在冲突，我先直接指出来：

你同时要求了：
1. 下一版要 `ready-for-use`
2. 下一版要支持当前文档中的 `Mode1/Mode2`
3. 下一版必须包含：
   - 新 Web UI dashboard
   - task tracking
   - workspace management
   - SSH integration
   - experiment result visualization

这组要求如果不进一步压缩，很容易再次变成“下一版目标过宽”，然后重演现在的瓶颈。

原因很直接：
- `Mode1/Mode2 as currently described in docs` 现在的描述本身就偏大、偏未来态
- 而你要的 UI、tracking、workspace、SSH、visualization 已经足够构成一个完整 release
- 如果 Mode1/Mode2 还按现在文档里的完整语义来实现，下一版很可能仍然不现实

所以我建议你下一步必须接受一个更严格的工程化表述：

- 下一版不是“完整实现当前文档中全部 Mode1/Mode2 语义”
- 而是“给出下一版可用的、缩减后的 Mode1/Mode2 定义与成功标准”

这个点如果不先定死，后面的 roadmap 会继续虚胖。

**我对项目的当前理解**
我现在对项目的理解，可以收敛成下面这版：

1. 项目定位
   - 一个 agent-driven research dashboard
   - 面向研究工作流中的具体任务
   - 不是通用全自动研究员

2. 下一版 release 的产品目标
   - 成为你自己可以实际拿来用的研究协作面板
   - 支持明确边界内的 Mode1/Mode2 任务类别
   - 强调稳定、可观察、可追踪，而不是夸张智能

3. 下一版 release 的工程核心
   - dashboard
   - task lifecycle visibility
   - workspace/session/container visibility and control
   - experiment result presentation
   - SSH-backed execution/session integration

4. 文档重构的真实作用
   - 不是“润色”
   - 而是把错误叙事移除，把 next release 的工程边界冻结下来

5. 文档体系的层级关系
   - `manifesto`: requirements / expectations / non-goals / release philosophy
   - `framework docs`: 项目抽象边界、功能哲学、使用价值
   - `architecture docs`: 面向当前实现的工程设计
   - `decision log`: 重大架构决策归档
   - `roadmap`: 拆成单会话原子任务的推进计划

**我给你的建议**
你让我推荐第 16 条怎么组织 atomic tasks，我的建议是：

**推荐组织方式：按“决策主题 -> 文档产物 -> 实施里程碑”三层拆解**
不要按文件直接拆，也不要只按里程碑拆。最稳的是三层混合：

1. 第一层：决策主题
   - 项目定位
   - next release scope
   - Mode1/Mode2 缩减定义
   - UI/dashboard scope
   - observability scope
   - workspace/session model
   - release criteria
   - 文档版本策略

2. 第二层：文档产物
   - manifesto
   - framework docs
   - architecture docs
   - decision log
   - roadmap

3. 第三层：单会话原子任务
   - 每次只完成一个可冻结的小决策或一个小文档切片
   - 例如：
     - 定义 next release 的 Non-Goals
     - 定义 Mode1 的缩减版任务范围
     - 定义 dashboard 首屏信息架构
     - 定义 workspace/session/container 三者关系
     - 定义 release-ready 的最低验收标准

为什么我推荐这个方式：
- 只按文件拆，容易又回到“写文档”而不是“做决策”
- 只按 milestone 拆，容易每个 session 太大
- 先按决策主题拆，才能保证每轮都有真正收敛

**我建议的总计划骨架**
这不是最终版，只是第一版框架。

**Phase 0: Reality Alignment**
目标：冻结错误叙事，定义 next release 的真实边界

1. 明确项目定位声明
2. 明确 Non-Goals
3. 明确 next release 的 ready-for-use 标准
4. 重新定义缩减版 Mode1/Mode2
5. 明确下一版只按任务类别收缩范围

**Phase 1: Documentation Refactoring Baseline**
目标：建立新版文档体系骨架

1. manifesto 结构草案
2. framework docs 的新版目录与职责边界
3. architecture docs 的新版目录与职责边界
4. decision log 规则
5. versioning and snapshot policy

**Phase 2: Release-Oriented Product Framing**
目标：把文档收敛为服务下一次 release 的工具

1. next release scope
2. dashboard requirements
3. observability requirements
4. workspace/session/container requirements
5. experiment result visualization requirements
6. deferred features list

**Phase 3: Architecture Convergence**
目标：把产品需求落成工程结构

1. runtime boundary
2. web UI boundary
3. task tracking model
4. workspace model
5. SSH/session/container model
6. result artifact and visualization model

**Phase 4: Atomic Delivery Roadmap**
目标：把长期规划拆成单会话可执行任务

1. 文档任务
2. architecture 任务
3. implementation prep 任务
4. release criteria 任务
5. archive/freeze 机制任务

**我建议你接受的两个强约束**
为了让这件事真的能推进，我建议现在就接受这两个约束：

1. 当前 docs 里的 `Mode1/Mode2` 不能原样继承进 next release
   - 必须缩减重定义

2. next release 的“must-have”需要区分三层
   - 真正必须可用
   - 最好有
   - 明确延期

否则 roadmap 还是会再次膨胀。

**下一轮我需要你回答的关键问题**
这轮我不再铺 18 个问题，只问最关键的 6 个。回答它们之后，我就能给出第一版“综合计划与路线图骨架”。

1. 你是否同意我刚才指出的冲突判断？
   - 即：`Mode1/Mode2 as currently documented` 对 next release 来说过大，必须缩减重定义
   - 请直接答：同意 / 不同意

2. 如果同意，请你分别用一句话定义 next release 的缩减版：
   - `Mode1 = ?`
   - `Mode2 = ?`

3. 对你来说，next release 的 primary user 只有你自己，还是也要假设“未来少量协作者可用”？
   - 这会影响文档和 UI 的复杂度

4. `dashboard` 首屏你最想第一眼看到的 5 类信息是什么？
   - 我建议你尽量像产品需求一样回答

5. 你说“实验结果可视化”，在下一版里你最关心展示什么？
   - 表格复现结果
   - 指标曲线
   - 图片/图表
   - run metadata
   - baseline comparison
   - failure reasons
   - 你选最重要的

6. 你是否接受这样的范围冻结方式：
   - next release 只面向“典型、简单、定义明确”的研究支持任务
   - 不承诺跨领域通用性
   - 不承诺开放式长期自主研究
   - 但保留持续 agent/session 作为局部能力

你回复这 6 个问题后，我下一步会输出：

1. 第一版项目重新定位声明
2. 第一版 manifesto 目录草案
3. 第一版 next-release roadmap 骨架
4. 第一版 atomic task decomposition 方法

---

## User

1.accept; 2.use `auto-claude-code-research-in-sleep` skill+prompt to implement mode1/mode2 baseline(eg. simply prompt claude code:`/research-pipeline start discovering <topic decription>, with <seed pdf file path> for reference.` for mode1); 3.single user for now; 4. milestone/checkpoint timeline of current running task, recent finished tasks, recent artifacts(tables, figures and reports, click to peek in modality dialog), resources(gpu/cpu/mem/disk usage of workspaces) using now, token usage overview(rpm, rph, rpd, tpm, tph, tpd); 5. artifacts preview(csv/markdown for tables, markdown for reports, svg/png for figures); 6. accept.

---

## Assistant (Plan · gpt-5.4 · 156.2s)

我先补一轮只读深挖：直接读取几篇最关键的现有 framework 文档和 `auto-claude-code-research-in-sleep` 相关材料，把你刚确认的方向和当前文本、参考技能之间对齐，然后给出第一版重定位声明、文档体系草案和路线图骨架。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/framework/index.md",
  "limit": 260,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/framework/index.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - AI-Native Research Framework 索引
4: tags:
5:   - research-agent
6:   - framework-design
7:   - obsidian-note
8:   - index
9: source_repo: scholar-agent
10: source_path: /home/xuyang/code/scholar-agent
11: last_local_commit: workspace aggregate
12: ---
13: # AI-Native Research Framework 索引
14: 
15: > [!abstract]
16: > 这一组笔记把现有参考项目抽象成我们自己的 AI-Native Research Framework——一个有界自治研究系统，支持两种核心操作模式：文献探索与复现（Mode 1）和深度复现（Mode 2）。V1 在隔离容器上自主运行，人在纳入和计划阶段定义合同边界。
17: 
18: ## 阅读方式
19: 
20: - 先读 [[framework/ai-native-research-framework]]，确认框架定位、设计原则和边界。
21: - 再读 [[framework/artifact-graph-architecture]]，理解工件图谱、分层结构和 adapter 设计。
22: - 如果要了解容器执行环境和工作区约定，读 [[framework/container-workspace-protocol]]。
23: - 如果要落近期版本，接着读 [[framework/v1-dual-mode-research-engine]]。
24: - 如果要看实现规格（API、组件、状态机），读 [[framework/v1-rfc]]。
25: - 如果要看分阶段实现计划和里程碑，读 [[framework/v1-roadmap]]。
26: - 如果要追溯设计来源，最后读 [[framework/reference-mapping]] 和各项目研究报告。
27: 
28: ## 内容索引
29: 
30: - [[framework/ai-native-research-framework]]
31: - [[framework/artifact-graph-architecture]]
32: - [[framework/container-workspace-protocol]]
33: - [[framework/v1-dual-mode-research-engine]]
34: - [[framework/v1-rfc]]
35: - [[framework/v1-roadmap]]
36: - [[framework/reference-mapping]]
37: 
38: ## 能力入口
39: 
40: - 框架愿景与系统边界：[[framework/ai-native-research-framework]]
41: - 工件模型、状态转换和宿主适配：[[framework/artifact-graph-architecture]]
42: - 容器工作区结构、同步协议与资源跟踪：[[framework/container-workspace-protocol]]
43: - 双模式 V1 的工作流、人工关卡与终止合同：[[framework/v1-dual-mode-research-engine]]
44: - V1 实现规格（API、组件、状态机）：[[framework/v1-rfc]]
45: - V1 分阶段实现路线图：[[framework/v1-roadmap]]
46: - 参考项目如何被吸收到框架中：[[framework/reference-mapping]]
47: 
48: ## 使用说明
49: 
50: - 这组笔记是"自有框架蓝图"，不是对某一个开源仓库的复述；涉及参考项目的判断，均来自本仓库已有研究报告与静态证据。
51: - 现阶段默认研究对象是 AI/ML research，不试图抽象到所有学术门类；写作模块只保留下游接口，不在 V1 文档里展开。
52: 
53: ## 关联笔记
54: 
55: - [[index]]
56: - [[summary/academic-research-agents-overview]]
57: - [[projects/ai-research-skills]]
58: - [[projects/auto-claude-code-research-in-sleep]]

(End of file - total 58 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md",
  "limit": 320,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - AI-Native Research Framework
4: tags:
5:   - research-agent
6:   - framework-design
7:   - system-note
8: source_repo: scholar-agent
9: source_path: /home/xuyang/code/scholar-agent
10: last_local_commit: workspace aggregate
11: ---
12: # AI-Native Research Framework：有界自治研究系统蓝图
13: 
14: > [!abstract]
15: > 这不是另一条固定 research pipeline，而是一个宿主无关、repo 优先、工件图谱驱动的研究系统。它要解决的问题是：如何让 Claude Code + Opus 等 agent 不只是"会读论文"或"会写报告"，而是能围绕论文、代码、实验和结论形成一个可审计、可复用、有界自治的研究操作系统。系统支持两种核心操作模式——文献探索与复现、深度复现——并在隔离容器中自主执行研究任务。
16: 
17: ## 框架定位
18: 
19: - 目标用户既包括要为研究工作流搭平台的团队，也包括直接使用 Claude Code + Opus 进行日常研究的实践者。
20: - 设计重心不是单次回答质量，而是研究资产如何沉淀、状态如何转换、人在关键节点如何定义合同边界。
21: - V1 的主要宿主是 Claude Code + Opus；核心工件模型保持宿主无关，宿主差异通过 adapter 吸收。
22: - 从现有参考项目抽象看，`everything-claude-code` 解决的是底盘，`ArgusBot` 解决的是监督式控制层，`AI-Research-SKILLs` 解决的是能力颗粒度，`ARIS` 和 `academic-research-skills` 解决的是长链路编排，`claude-scholar` 解决的是长期工作台；本框架试图把这些层统一成一个可组合系统。
23: 
24: ## 双模式概览
25: 
26: - **Mode 1 — 文献探索与复现**：给定一篇或数篇种子论文（综述或顶会），系统在隔离容器中自主探索、复现、跟踪相关文献，按深度上限/预算/递减收益自动终止，产出文献复现报告、idea 验证报告、核心发现和下一步建议。
27: - **Mode 2 — 深度复现**：给定一篇没有开源代码的论文，系统从零实现论文方法，按实验设置高精度复现文中表格，产出可运行代码、实验结果、偏差分析和对论文含金量、可复现性、方法科学性的结构化评估。
28: 
29: ## 设计原则
30: 
31: - 宿主无关：核心工件模型与状态机独立于 Claude/Codex/OpenCode，宿主差异通过 adapter 吸收。
32: - Repo 优先：代码、配置、实验日志、复现记录和研究产物都优先落在可版本化目录中，而不是只存在会话记忆里。每个研究项目在容器上是独立的 git repo。
33: - 工件优先于流程：流程只是工件之间的状态转换，不把线性 stage 当成唯一真相。
34: - 有界自治：系统在人类预设的合同边界内自主运行——包括递归深度上限、预算上限、时间上限和 agent 自评递减收益检测。不是开放式自治，也不是逐步审批；是在明确合同内自由行动，合同外必须停下。
35: - 失败可记账：复现失败、实验失败、证据冲突都不是异常分支，而是正式研究资产。
36: 
37: ## 系统边界
38: 
39: - In scope：论文阅读、结构化证据抽取、方法级复现、从零实现论文方法（无开源代码场景）、实验追踪与高精度表格复现、偏差归因、结果归档、文献递归探索与自动终止、论文含金量与可复现性的结构化评估、下游写作接口。
40: - Out of scope for V1：自动把论文写到可投稿质量、自动完成 rebuttal 与投稿合规、容器生命周期管理（外部负责）、数据集自动获取（用户提供或手动下载）。
41: - 一个关键推论是：V1 不应该被定义为"paper writing agent"，而应该被定义为"bounded-autonomous research evidence engine"。
42: 
43: ## 分层视图
44: 
45: ```mermaid
46: flowchart TD
47:     A[Host Harness<br/>Claude Code / Codex / OpenCode] --> B[Adapter Layer]
48:     B --> C[Core Research Runtime]
49:     C --> D[Artifact Graph]
50:     C --> E[Workflow Controllers]
51:     E --> F[Literature Exploration]
52:     E --> G[Reproduction & Implementation]
53:     E --> H[Experiment Tracking]
54:     D --> I[Container Workspace<br/>SSH · GPU · Isolated]
55:     I --> J[Per-Project Git Repo]
56: ```
57: 
58: ## 核心主张
59: 
60: - 平台层负责接入宿主能力、权限模型、长任务执行和可观测性。
61: - 核心运行时负责统一任务语义，例如"读一篇论文""启动一次复现""从零实现一个方法""归档一次实验"。
62: - 工件图谱层负责维持研究状态，不让系统退化为一堆互不相干的 Markdown 与脚本。
63: - 工作流控制器负责把一等工件串起来，但它本身不能成为新的单点耦合源。
64: - 执行平面运行在隔离容器上（SSH 接入、GPU 资源、完全 root 权限），框架定义工作区约定但不管理容器生命周期。
65: 
66: ## 人工关卡
67: 
68: 系统保留两个显式关卡，其余环节在预设合同内自治：
69: 
70: - **纳入关卡**：人决定哪些论文作为种子进入系统（Mode 1）或作为目标论文进入深度复现（Mode 2）。
71: - **计划关卡**：人审批复现计划——包括复现范围（仅核心方法 vs 完整实验套件）、资源预算（GPU 时间、API 费用、总时长）、递归深度上限和终止条件。
72: 
73: 预算和归档不再是阻塞式关卡，而是"合同与验证"模式：人在计划阶段预授权资源边界，agent 在边界内自主执行；结果（包括失败）全量归档，人事后审阅而非执行中逐一审批。
74: 
75: ## 不是要复制什么
76: 
77: - 不复制 `ARIS` 的无约束自治默认——系统可以过夜运行，但在合同之内，不是空白支票。吸收其 nightly loop、实验执行链和跨模型 review 思路，但附加终止合同。
78: - 不复制 `academic-research-skills` 的完整投稿工厂，因为这会过早把系统重心拉向写作。
79: - 不复制 `AI-Research-SKILLs` 的纯技能市场形态，因为那会让工件状态和流程责任继续外溢到宿主。
80: 
81: ## 关联笔记
82: 
83: - [[framework/index]]
84: - [[framework/artifact-graph-architecture]]
85: - [[framework/v1-dual-mode-research-engine]]
86: - [[framework/container-workspace-protocol]]
87: - [[framework/reference-mapping]]
88: - [[summary/academic-research-agents-overview]]

(End of file - total 88 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md",
  "limit": 360,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - 双模式研究引擎 V1
4:   - 半自动研究副驾 V1
5: tags:
6:   - research-agent
7:   - framework-design
8:   - v1-spec
9: source_repo: scholar-agent
10: source_path: /home/xuyang/code/scholar-agent
11: last_local_commit: workspace aggregate
12: ---
13: # V1：双模式有界自治研究引擎
14: 
15: > [!abstract]
16: > V1 支持两种核心操作模式：文献探索与复现（Mode 1）和深度复现（Mode 2）。系统在人类预设的合同边界内自主运行——人在纳入和计划阶段定义边界，agent 在边界内自治执行、全量归档。执行环境是隔离容器（SSH、GPU、root），每个研究项目是独立 git repo。
17: 
18: ## V1 目标
19: 
20: **工件升级（两种模式共享）：**
21: 
22: - 把论文阅读从自由文本总结升级为结构化 `PaperCard`。
23: - 把复现从"一次性跑脚本"升级为可跟踪的 `ReproductionTask`（区分 `reproduce-from-source` 与 `implement-from-paper`）。
24: - 把实验从零散命令历史升级为正式 `ExperimentRun` 账本。
25: - 为后续写作模块留下标准化输入，而不是直接在 V1 里追求投稿级成稿。
26: 
27: **Mode 1 专属目标：**
28: 
29: - 从种子论文出发，自主递归探索相关文献，构建 `ExplorationGraph`。
30: - 对高价值论文进行选择性复现，产出复现报告和核心发现。
31: - 按深度上限、预算上限和递减收益自动终止探索。
32: - 输出下一步探索方向建议和 idea 验证报告。
33: 
34: **Mode 2 专属目标：**
35: 
36: - 对没有开源代码的论文，从零实现论文提出的方法。
37: - 按论文实验设置高精度复现指定表格和结果。
38: - 产出对论文含金量、可复现性和方法科学性的结构化评估 `QualityAssessment`。
39: - 用户可设定预算和范围——仅核心方法或完整实验套件。
40: 
41: ## 输入与输出
42: 
43: ### Mode 1 — 文献探索与复现
44: 
45: **输入：**
46: 
47: - 种子论文：用户提供的 PDF 文件，经 MinerU API 解析为 Markdown。
48: - 领域上下文：用户对研究方向的简要说明，帮助 agent 判断论文相关性。
49: - 终止合同：递归深度上限（如 3 跳）、总预算上限（GPU 小时、API 费用、总时长）。
50: - 可选：用户标注的重点关注方向或需要忽略的子领域。
51: 
52: **输出：**
53: 
54: - `ExplorationGraph`：完整的探索前沿状态，包含所有已访问、排队和剪枝的 PaperCard。
55: - 文献复现报告：对已复现论文的结果记录与偏差分析。
56: - 核心发现（core findings）：从探索中提炼的关键洞察。
57: - 下一步探索方向建议：agent 对未来研究的具体建议。
58: - idea 验证报告：对初步想法的可行性评估。
59: 
60: ### Mode 2 — 深度复现
61: 
62: **输入：**
63: 
64: - 目标论文：用户提供的 PDF 文件，经 MinerU API 解析为 Markdown。
65: - 范围指令：`core-only`（仅实现核心方法和关键实验）或 `full-suite`（完整实验套件）。
66: - 目标表格/结果：用户指定需要复现的具体表格或实验。
67: - 预算上限：GPU 小时、API 费用、总时长。
68: 
69: **输出：**
70: 
71: - 可运行的实现代码（`src/` 目录，含 README 和依赖说明）。
72: - 实验结果：per-table 的定量对比（论文报告值 vs 复现值）。
73: - 偏差分析：对每个显著偏差的根因诊断。
74: - `QualityAssessment`：对论文的结构化评估——
75:   - 含金量：方法是否有实质技术贡献，还是增量改进。
76:   - 可复现性：按论文描述能否重现声称的结果，偏差多大。
77:   - 方法科学性：实验设计是否严谨，消融是否充分，比较基线是否合理。
78: 
79: ## 主工作流
80: 
81: ### Mode 1 工作流
82: 
83: ```mermaid
84: flowchart TD
85:     A[用户提供种子论文 PDF] --> B[MinerU 解析为 Markdown]
86:     B --> C[生成 PaperCard]
87:     C --> D[HumanGate: 纳入确认]
88:     D --> E[制定探索计划]
89:     E --> F[HumanGate: 计划审批<br/>深度/预算/范围]
90:     F --> G[自治探索循环]
91:     G --> G1[提取参考文献并排优先级]
92:     G1 --> G2[解析下一篇论文]
93:     G2 --> G3[生成 PaperCard]
94:     G3 --> G4{值得复现?}
95:     G4 -->|Yes| G5[创建 ReproductionTask]
96:     G5 --> G6[执行 ExperimentRun]
97:     G6 --> G7[记录 EvidenceRecord]
98:     G4 -->|No| G8[标记为已探索/剪枝]
99:     G7 --> G9[更新 ExplorationGraph]
100:     G8 --> G9
101:     G9 --> G10{终止检查}
102:     G10 -->|深度/预算/递减收益| H[生成探索报告]
103:     G10 -->|继续| G1
104: ```
105: 
106: ### Mode 2 工作流
107: 
108: ```mermaid
109: flowchart TD
110:     A[用户提供目标论文 PDF] --> B[MinerU 解析为 Markdown]
111:     B --> C[生成 PaperCard]
112:     C --> D[HumanGate: 纳入确认]
113:     D --> E[制定复现计划<br/>范围/目标表格/预算]
114:     E --> F[HumanGate: 计划审批]
115:     F --> G[从零实现核心方法]
116:     G --> H[运行 baseline 实验]
117:     H --> I{baseline 结果}
118:     I -->|接近论文| J[按论文设置复现完整表格]
119:     I -->|显著偏差| K[偏差诊断与修复迭代]
120:     K --> H
121:     J --> L[per-table 结果对比]
122:     L --> M[偏差分析 & EvidenceRecord]
123:     M --> N[生成 QualityAssessment]
124: ```
125: 
126: ## 工作流细化
127: 
128: ### Mode 1 细化
129: 
130: - **Paper intake**：通过 MinerU 将种子论文 PDF 解析为 Markdown，抽取问题、方法、依赖、主要 claim、参考文献列表。
131: - **探索排优先级**：根据引用频次、与种子论文的方法相关性、发表时间和 venue 排序参考文献。用户提供的领域上下文用于相关性判断。
132: - **选择性复现**：不是每篇论文都复现。Agent 根据以下标准决定是否发起 ReproductionTask：方法是否与种子论文的核心方法相关、是否有足够的实验描述支持复现、复现预期成本是否在剩余预算内。
133: - **终止决策**：三个维度的 OR 逻辑——递归深度达到上限、预算（GPU 时间/API 费用/总时长）耗尽、agent 自评后续探索的边际价值低于阈值（连续 N 篇论文无新发现）。
134: 
135: ### Mode 2 细化
136: 
137: - **Paper intake**：通过 MinerU 解析目标论文，重点抽取方法描述（模型架构、损失函数、训练细节）、实验设置（数据集、超参数、评估指标）和目标表格。
138: - **实现策略**：使用标准 ML 库（PyTorch、HuggingFace Transformers 等）从零实现论文方法。优先实现核心模块（模型架构、关键 loss），再搭建训练和评估 pipeline。
139: - **实验复现**：先跑通 baseline（小规模数据、短 epoch）确认代码正确性，再按论文完整设置运行。对 `full-suite` 范围，逐表复现论文结果。
140: - **偏差处理**：偏差分为可接受偏差（随机种子、硬件差异导致的小波动）和需要诊断的偏差（>5% 相对偏差）。对显著偏差进行根因分析并记录为 `EvidenceRecord`。
141: - **质量评估**：基于复现结果和全过程证据，生成 `QualityAssessment`。即使复现失败，结构化的失败分析本身也是有价值的输出。
142: 
143: ## 人工关卡
144: 
145: V1 保留两个显式关卡：
146: 
147: | 关卡 | 适用模式 | 内容 |
148: | --- | --- | --- |
149: | 纳入关卡 | Mode 1 & 2 | 人决定哪些论文进入系统：种子论文（Mode 1）或目标论文（Mode 2）。 |
150: | 计划关卡 | Mode 1 & 2 | 人审批复现/探索计划——包括范围（Mode 2：core-only vs full-suite）、资源预算、递归深度上限（Mode 1）和终止条件。 |
151: 
152: 预算和归档不再是阻塞式关卡。预算在计划阶段预授权，agent 在边界内自主执行；结果（成功和失败）全量归档，人事后审阅。
153: 
154: ## V1 Done 定义
155: 
156: **Mode 1：**
157: 
158: - 用户提供种子论文后，系统能自主完成文献递归探索并在深度/预算/递减收益条件下稳定终止。
159: - 产出结构化的 `ExplorationGraph`、复现报告和下一步建议。
160: - 探索过程中的失败（解析失败、复现失败、环境问题）被记录为正式工件状态。
161: 
162: **Mode 2：**
163: 
164: - 用户提供无开源代码的论文后，系统能从零实现论文方法并尝试高精度复现目标表格。
165: - 产出可运行代码、per-table 结果对比、偏差分析和 `QualityAssessment`。
166: - 复现失败（方法描述不足、结果不可重现）本身是有价值的正式输出。
167: 
168: **通用：**
169: 
170: - 不同宿主接入时，核心对象和状态定义保持一致，不重写业务语义。
171: - 文档层能明确说明 V1 如何向未来的写作系统和更强自动化系统交接。
172: 
173: ## 明确不做
174: 
175: - 不做投稿级论文写作、review 和 rebuttal。
176: - 不管理容器生命周期（创建、启动、停止、销毁由外部负责）。
177: - 不自动获取数据集（用户提供或在计划阶段明确数据来源）。
178: - 不保证复现一定成功——结构化的失败分析本身是正式产出，不是系统故障。
179: 
180: ## 关联笔记
181: 
182: - [[framework/index]]
183: - [[framework/ai-native-research-framework]]
184: - [[framework/artifact-graph-architecture]]
185: - [[framework/container-workspace-protocol]]
186: - [[framework/reference-mapping]]
187: - [[projects/auto-claude-code-research-in-sleep]]

(End of file - total 187 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md",
  "limit": 360,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - AINRF V1 RFC
4:   - V1 实现规格
5: tags:
6:   - research-agent
7:   - framework-design
8:   - v1-spec
9:   - rfc
10: source_repo: scholar-agent
11: source_path: /home/xuyang/code/scholar-agent
12: last_local_commit: workspace aggregate
13: ---
14: # AINRF V1 RFC：有界自治研究引擎实现规格
15: 
16: > [!abstract]
17: > 定位：把框架设计文档的"做什么"翻译成"怎么做"。[[framework/ai-native-research-framework]] 定义了愿景与原则，[[framework/artifact-graph-architecture]] 定义了工件模型，[[framework/v1-dual-mode-research-engine]] 定义了双模式工作流与终止合同，[[framework/container-workspace-protocol]] 定义了容器执行环境。本 RFC 在此基础上给出可部署的服务架构、API 设计、组件规格和实现路径——从蓝图到可运行系统的最后一公里。
18: 
19: ## Problem Statement & Motivation
20: 
21: ### 缺口
22: 
23: 框架文档已经定义了完整的工件模型（PaperCard、ReproductionTask、ExperimentRun 等）、双模式工作流（文献探索与深度复现）、人工关卡（纳入 + 计划）和容器工作区协议。但这些设计停留在"做什么"层面，缺少以下关键实现决策：
24: 
25: - 系统以什么形态运行？CLI 工具、daemon 服务还是 serverless 函数？
26: - 外部系统（CI/CD、webhook、未来 UI）如何与研究引擎交互？
27: - 任务状态如何持久化？orchestrator 崩溃后如何恢复？
28: - Claude Code 如何被调用？直接 subprocess 还是 SDK？
29: - 人工关卡如何从"设计概念"变成"可调用的 API"？
30: 
31: ### 为什么是 REST 服务而非 CLI
32: 
33: | 维度 | CLI 方案 | REST 服务方案 |
34: |------|---------|-------------|
35: | 部署位置 | 必须在容器本地或有 SSH 的机器上 | 任意位置，只需网络可达 |
36: | Webhook 集成 | 需要额外轮询脚本 | 原生支持，关卡触发直接 POST |
37: | 实时进度 | 只能 tail 日志 | SSE 推送 + 轮询端点 |
38: | 未来 UI | 需要包装层 | 天然 API-first |
39: | 多任务管理 | 多终端窗口 | 统一任务队列 |
40: | 可观测性 | 散落在日志文件中 | 结构化事件流 |
41: 
42: 结论：REST 服务是 V1 的正确形态。它不排斥 CLI——CLI 可以作为 REST 客户端存在，但核心是 API-first。
43: 
44: ## System Architecture Overview
45: 
46: ### 三层架构
47: 
48: 系统分为三层，职责严格隔离：
49: 
50: - **API Layer（FastAPI）**：接收外部请求、认证、参数校验、SSE 推送。不包含任何研究语义。
51: - **Orchestrator Core（TaskEngine + StateStore + GateManager）**：任务生命周期管理、状态持久化、关卡协调、checkpoint/resume。这是系统的大脑。
52: - **Execution Layer（SSH Executor + Agent Adapter）**：通过 SSH 连接容器，调用 Claude Code SDK 执行原子研究任务。不保存研究状态，只负责"在容器上执行并返回结果"。
53: 
54: ### 架构总览
55: 
56: ```mermaid
57: flowchart TD
58:     Client["Client<br/>(CLI / Webhook / Future UI)"]
59:     subgraph API["API Layer — FastAPI"]
60:         Auth[Auth Middleware]
61:         Router[Route Handlers]
62:         SSE[SSE Publisher]
63:     end
64:     subgraph Core["Orchestrator Core"]
65:         TE[TaskEngine<br/>状态机 + 调度]
66:         SS[StateStore<br/>JSON checkpoint]
67:         GM[GateManager<br/>关卡 + webhook]
68:         MC[MinerU Client<br/>PDF 解析]
69:     end
70:     subgraph Exec["Execution Layer"]
71:         SSHX[SSH Executor<br/>连接池 + 文件传输]
72:         AA[Agent Adapter<br/>抽象接口]
73:         CCA[ClaudeCodeAdapter<br/>claude_code_sdk]
74:     end
75:     Container["Container<br/>SSH · GPU · Per-Project Git Repo"]
76: 
77:     Client --> Auth --> Router
78:     Router --> TE
79:     TE --> SS
80:     TE --> GM
81:     TE --> MC
82:     TE --> AA
83:     AA --> CCA
84:     CCA --> SSHX
85:     SSHX --> Container
86:     TE --> SSE
87:     SSE --> Client
88:     GM -->|webhook| Client
89: ```
90: 
91: ### 部署模型
92: 
93: - Orchestrator 运行在任意有网络访问的机器上（本地开发机、云 VM、CI runner）。
94: - 容器通过 SSH 接入，orchestrator 不需要与容器在同一网络。
95: - V1 采用 1:1 映射：一个 orchestrator 实例管理一个容器。数据模型预留 `container_id` 字段，为未来 1:N 做准备。
96: - V1 任务顺序执行。TaskEngine 内部使用队列，但同一时刻只有一个任务在执行。并发调度留给 V2。
97: 
98: ## API Design
99: 
100: ### Authentication
101: 
102: V1 使用 API Key 认证，简单可靠：
103: 
104: - 客户端在请求头中携带 `X-API-Key: <key>`。
105: - 服务端存储 key 的 SHA-256 哈希值，不存明文。
106: - 认证失败返回 `401 Unauthorized`，不泄露 key 是否存在。
107: - 扩展路径：V2 可引入 JWT bearer token 或 OAuth2，API Layer 的 auth middleware 设计为可插拔。
108: 
109: > [!tip]
110: > V1 建议通过 reverse proxy（如 Caddy/Nginx）终止 TLS，FastAPI 本身不处理 HTTPS。这样 API key 在传输层有加密保护。
111: 
112: ### Endpoints
113: 
114: | Endpoint | Method | 用途 | 认证 |
115: |---|---|---|---|
116: | `/tasks` | `POST` | 提交研究任务 | 需要 |
117: | `/tasks` | `GET` | 列出任务（支持 `?status=` 过滤） | 需要 |
118: | `/tasks/{id}` | `GET` | 获取任务详情（含当前阶段、工件列表、预算消耗） | 需要 |
119: | `/tasks/{id}/approve` | `POST` | 审批通过人工关卡 | 需要 |
120: | `/tasks/{id}/reject` | `POST` | 拒绝并附带反馈（触发计划修订） | 需要 |
121: | `/tasks/{id}/cancel` | `POST` | 取消正在执行的任务（优雅终止） | 需要 |
122: | `/tasks/{id}/events` | `GET` | SSE 事件流（实时进度） | 需要 |
123: | `/health` | `GET` | 健康检查（含容器连通性） | 不需要 |
124: 
125: ### Task Submission Schema
126: 
127: 任务提交使用 JSON POST body。以下是完整 schema：
128: 
129: ```json
130: {
131:   "mode": "literature_exploration | deep_reproduction",
132:   "papers": [
133:     {
134:       "title": "Attention Is All You Need",
135:       "pdf_url": "https://arxiv.org/pdf/1706.03762",
136:       "pdf_path": "/local/path/to/paper.pdf",
137:       "role": "seed | target"
138:     }
139:   ],
140:   "config": {
141:     "mode_1": {
142:       "domain_context": "Transformer 架构在长序列建模中的效率优化",
143:       "max_depth": 3,
144:       "focus_directions": ["linear attention", "sparse attention"],
145:       "ignore_directions": ["vision transformer"]
146:     },
147:     "mode_2": {
148:       "scope": "core-only | full-suite",
149:       "target_tables": ["Table 1", "Table 3"],
150:       "baseline_first": true
151:     }
152:   },
153:   "container": {
154:     "host": "gpu-server-01",
155:     "port": 22,
156:     "user": "researcher",
157:     "ssh_key_path": "/path/to/id_rsa",
158:     "project_dir": "/workspace/projects/attention-study"
159:   },
160:   "budget": {
161:     "gpu_hours": 24,
162:     "api_cost_usd": 50,
163:     "wall_clock_hours": 48
164:   },
165:   "yolo": false,
166:   "webhook_url": "https://example.com/hooks/ainrf",
167:   "webhook_secret": "hmac-shared-secret"
168: }
169: ```
170: 
171: 字段说明：
172: 
173: - `mode`：必填。`literature_exploration` 对应 Mode 1，`deep_reproduction` 对应 Mode 2。
174: - `papers`：必填。至少一篇。`pdf_url` 和 `pdf_path` 二选一，系统优先使用本地路径。`role` 在 Mode 1 中为 `seed`，Mode 2 中为 `target`。
175: - `config.mode_1`：Mode 1 专属配置。`domain_context` 帮助 agent 判断论文相关性；`max_depth` 控制递归探索深度；`focus_directions` 和 `ignore_directions` 引导探索方向。
176: - `config.mode_2`：Mode 2 专属配置。`scope` 决定复现范围；`target_tables` 指定需要复现的表格；`baseline_first` 控制是否先跑小规模验证。
177: - `container`：必填。SSH 连接信息和项目目录。目录结构遵循 [[framework/container-workspace-protocol]] 定义的约定。
178: - `budget`：必填。三个维度的预算上限，任一维度触顶即终止。
179: - `yolo`：可选，默认 `false`。设为 `true` 时跳过所有人工关卡，自动审批通过。适用于信任度高的重复性任务。
180: - `webhook_url` / `webhook_secret`：可选。配置后，关卡等待和任务完成时发送 webhook 通知。
181: 
182: ### SSE Event Types
183: 
184: 客户端通过 `GET /tasks/{id}/events` 建立 SSE 连接，接收实时事件。每个事件包含 `event` 类型和 JSON `data`。
185: 
186: #### task.stage_changed
187: 
188: 任务阶段转换时触发。
189: 
190: ```json
191: {
192:   "event": "task.stage_changed",
193:   "data": {
194:     "task_id": "t-20260315-001",
195:     "previous_stage": "ingesting",
196:     "current_stage": "planning",
197:     "timestamp": "2026-03-15T10:30:00Z",
198:     "message": "论文解析完成，开始制定探索计划"
199:   }
200: }
201: ```
202: 
203: #### task.progress
204: 
205: 执行过程中的进度更新，粒度为原子任务级别。
206: 
207: ```json
208: {
209:   "event": "task.progress",
210:   "data": {
211:     "task_id": "t-20260315-001",
212:     "stage": "executing",
213:     "step": "explore_paper",
214:     "step_index": 5,
215:     "total_steps": 12,
216:     "detail": "正在解析第 5 篇论文: Linear Transformers Are Secretly Fast",
217:     "budget_consumed": {
218:       "gpu_hours": 2.3,
219:       "api_cost_usd": 8.5,
220:       "wall_clock_hours": 3.1
221:     },
222:     "timestamp": "2026-03-15T13:10:00Z"
223:   }
224: }
225: ```
226: 
227: #### task.gate_waiting
228: 
229: 人工关卡触发，等待审批。同时通过 webhook 发送通知。
230: 
231: ```json
232: {
233:   "event": "task.gate_waiting",
234:   "data": {
235:     "task_id": "t-20260315-001",
236:     "gate_type": "plan_approval",
237:     "gate_id": "g-20260315-001",
238:     "summary": "探索计划：从 3 篇种子论文出发，最大深度 3 跳，预算 24 GPU 小时",
239:     "plan_detail": {
240:       "seed_papers": 3,
241:       "max_depth": 3,
242:       "estimated_papers": 15,
243:       "estimated_gpu_hours": 18
244:     },
245:     "approve_url": "/tasks/t-20260315-001/approve",
246:     "reject_url": "/tasks/t-20260315-001/reject",
247:     "timestamp": "2026-03-15T10:35:00Z"
248:   }
249: }
250: ```
251: 
252: #### task.artifact_created
253: 
254: 新工件产生时触发。工件类型对应 [[framework/artifact-graph-architecture]] 中定义的一等对象。
255: 
256: ```json
257: {
258:   "event": "task.artifact_created",
259:   "data": {
260:     "task_id": "t-20260315-001",
261:     "artifact_type": "PaperCard",
262:     "artifact_id": "pc-attention-is-all-you-need",
263:     "artifact_path": "artifacts/paper-cards/attention-is-all-you-need.json",
264:     "summary": "PaperCard: Attention Is All You Need — structured reading complete",
265:     "timestamp": "2026-03-15T11:00:00Z"
266:   }
267: }
268: ```
269: 
270: #### task.log
271: 
272: 执行过程中的日志消息，用于调试和可观测性。
273: 
274: ```json
275: {
276:   "event": "task.log",
277:   "data": {
278:     "task_id": "t-20260315-001",
279:     "level": "info",
280:     "source": "claude_code_adapter",
281:     "message": "CC session completed: implemented core attention module (src/attention.py)",
282:     "timestamp": "2026-03-15T14:20:00Z"
283:   }
284: }
285: ```
286: 
287: #### task.completed / task.failed / task.cancelled
288: 
289: 任务终态事件。
290: 
291: ```json
292: {
293:   "event": "task.completed",
294:   "data": {
295:     "task_id": "t-20260315-001",
296:     "mode": "literature_exploration",
297:     "duration_hours": 8.2,
298:     "budget_consumed": {
299:       "gpu_hours": 6.5,
300:       "api_cost_usd": 12.3,
301:       "wall_clock_hours": 8.2
302:     },
303:     "artifacts_summary": {
304:       "paper_cards": 12,
305:       "reproduction_tasks": 3,
306:       "experiment_runs": 3,
307:       "evidence_records": 18,
308:       "exploration_graph": true
309:     },
310:     "termination_reason": "diminishing_returns",
311:     "report_path": "reports/exploration/exploration-report.md",
312:     "timestamp": "2026-03-15T18:30:00Z"
313:   }
314: }
315: ```
316: 
317: ## Core Components
318: 
319: ### Task Engine
320: 
321: TaskEngine 是 orchestrator 的核心，负责驱动任务通过生命周期状态机。
322: 
323: #### 状态机
324: 
325: ```mermaid
326: stateDiagram-v2
327:     [*] --> submitted: POST /tasks
328:     submitted --> ingesting: 开始解析论文
329:     ingesting --> planning: 论文解析完成
330:     planning --> gate_waiting: 需要人工审批
331:     gate_waiting --> planning: reject（附带反馈）
332:     gate_waiting --> executing: approve
333:     planning --> executing: yolo mode 自动通过
334:     executing --> gate_waiting: 运行中触发关卡
335:     executing --> completed: 所有步骤完成
336:     executing --> failed: 不可恢复错误
337:     submitted --> cancelled: 用户取消
338:     ingesting --> cancelled: 用户取消
339:     planning --> cancelled: 用户取消
340:     gate_waiting --> cancelled: 用户取消
341:     executing --> cancelled: 用户取消
342:     executing --> failed: 预算耗尽
343: ```
344: 
345: #### 阶段说明
346: 
347: - **submitted**：任务已接收，等待调度。V1 顺序执行，如果有任务正在运行，新任务排队。
348: - **ingesting**：调用 MinerU Cloud API 解析 PDF 为 Markdown，生成初始 PaperCard。这一步在 orchestrator 侧完成，不需要容器。
349: - **planning**：根据 mode 和 config 生成执行计划。Mode 1 生成探索计划（深度、方向、预算分配）；Mode 2 生成复现计划（实现步骤、实验矩阵、里程碑）。
350: - **gate_waiting**：等待人工审批。触发 webhook 通知，SSE 推送 `task.gate_waiting` 事件。yolo mode 下此阶段被跳过。
351: - **executing**：在容器上通过 Agent Adapter 逐步执行原子任务。每个原子任务完成后更新 checkpoint。
352: - **completed**：所有步骤完成或终止条件满足（深度/预算/递减收益）。归档最终报告。
353: - **failed**：不可恢复错误（SSH 连接永久失败、容器不可用、关键依赖缺失）。已完成的工件保留。
354: - **cancelled**：用户主动取消。优雅终止当前原子任务，归档已有成果。
355: 
356: #### 任务粒度：原子任务
357: 
358: TaskEngine 不会把整个 Mode 1 或 Mode 2 工作流作为一次 Claude Code 调用。而是将工作流拆解为细粒度的原子任务，每个原子任务对应一次 CC SDK 调用：
359: 
360: **Mode 1 原子任务示例：**

(Showing lines 1-360 of 724. Use offset=361 to continue.)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md",
  "limit": 320,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - AINRF V1 Roadmap
4:   - V1 实现路线图
5: tags:
6:   - research-agent
7:   - framework-design
8:   - v1-spec
9:   - roadmap
10: source_repo: scholar-agent
11: source_path: /home/xuyang/code/scholar-agent
12: last_local_commit: workspace aggregate
13: ---
14: # AINRF V1 Roadmap：实现路线图
15: 
16: > [!abstract]
17: > 分阶段实现计划，每阶段有明确交付物和可测试标准。总体原则：infrastructure first → Mode 2（更可控）→ Mode 1（更开放）。基础设施阶段（P0-P6）可大量并行；Mode 2（P8）整合全部基础设施；Mode 1（P9）在 Mode 2 之上叠加探索能力。
18: 
19: ## Overview
20: 
21: > [!tip]
22: > 下图展示各阶段的时序关系。P0-P3 无依赖可并行启动；P4 依赖 P3 的工件模型；P5/P6 依赖 P4 的 API 骨架；P7 整合执行器与 API；P8/P9 是两种模式的端到端集成。
23: 
24: ```mermaid
25: gantt
26:     title AINRF V1 实现路线图
27:     dateFormat  YYYY-MM-DD
28:     axisFormat  %m-%d
29: 
30:     section 基础设施
31:     P0 Project Scaffold        :p0, 2026-03-16, 2d
32:     P1 SSH Executor            :p1, 2026-03-16, 5d
33:     P2 MinerU Client           :p2, 2026-03-16, 4d
34:     P3 Artifact Model & State  :p3, 2026-03-16, 5d
35: 
36:     section 服务层
37:     P4 FastAPI Service & Auth  :p4, after p3, 4d
38:     P5 Human Gate & Webhook    :p5, after p4, 4d
39:     P6 SSE Streaming           :p6, after p4, 3d
40: 
41:     section 编排层
42:     P7 Agent Adapter & Engine  :p7, after p1 p4, 5d
43: 
44:     section 模式集成
45:     P8 Mode 2 Deep Repro       :p8, after p7 p2 p5 p6, 7d
46:     P9 Mode 1 Lit Exploration  :p9, after p8, 7d
47: ```
48: 
49: ## P0: Project Scaffold
50: 
51: > [!info]
52: > 最小骨架，确保后续所有阶段有统一的包结构和入口点。
53: 
54: **交付物：**
55: 
56: - `src/ainrf/` 包结构：`__init__.py`、`__main__.py`、`cli.py`
57: - `pyproject.toml` 更新：添加 `ainrf` 入口点、基础依赖声明（pydantic、fastapi、uvicorn、asyncssh、httpx）
58: - CLI 入口：基于 `click` 或 `typer`，支持 `ainrf --help`、`ainrf serve`、`ainrf run` 子命令骨架
59: - 基础日志配置：structlog + JSON 格式，统一全项目日志规范
60: - CI 骨架：pre-commit hooks（ruff lint + format）、基础 pytest 配置
61: 
62: **可测试标准：**
63: 
64: - `uv run ainrf --help` 正常输出帮助信息
65: - `uv run ainrf --version` 输出版本号
66: - `uv run pytest tests/` 通过（即使只有一个 placeholder test）
67: - `ruff check src/ainrf/` 零错误
68: 
69: **依赖：** 无——这是所有阶段的起点。
70: 
71: **风险：** 低。唯一需要决策的是 CLI 框架选择（typer vs click），建议用 typer 以减少样板代码。
72: 
73: ## P1: SSH Executor & Container Bootstrap
74: 
75: > [!info]
76: > 框架的执行平面运行在隔离容器上（详见 [[framework/container-workspace-protocol]]）。本阶段交付从宿主到容器的完整连接与命令执行能力。
77: 
78: > [!note]
79: > 当前实现默认项：
80: > - 仅支持 `Ubuntu/Debian + bash`
81: > - 仅实现 `asyncssh` 路径，不做 `paramiko` fallback
82: > - 环境变量入口使用 `AINRF_CONTAINER_*`
83: > - 默认验收是离线 `pytest` 契约测试 + 真实容器手工 smoke，不把外部容器接入默认测试
84: 
85: **交付物：**
86: 
87: - `SSHExecutor` 类：管理 SSH 连接池、支持连接复用和自动重连
88: - 命令执行接口：`run_command(cmd, timeout, cwd)` → `CommandResult(exit_code, stdout, stderr)`
89: - 文件传输接口：`upload(local, remote)` / `download(remote, local)`，基于 SFTP
90: - Claude Code 自动检测与安装：连接后检测容器上是否已安装 CC CLI，未安装则自动执行安装脚本
91: - 连接配置：从 `~/.ssh/config` 或环境变量读取，支持密钥认证和跳板机
92: - 健康检查：`ping()` 方法验证连接可用性、GPU 可见性、磁盘空间
93: 
94: **可测试标准：**
95: 
96: - 连接到测试容器 → 执行 `echo hello` → 返回 `hello`
97: - 检测容器上无 CC → 自动安装 → 验证 `claude --version` 可用
98: - 上传本地文件到容器 → 下载回来 → 内容一致
99: - 连接断开后自动重连 → 再次执行命令成功
100: - 健康检查返回 GPU 型号、CUDA 版本、可用磁盘空间
101: 
102: **依赖：** P0（需要包结构）
103: 
104: **风险：**
105: 
106: | 风险 | 影响 | 缓解策略 |
107: | --- | --- | --- |
108: | SSH 库选择：paramiko vs asyncssh | asyncssh 原生 async 但生态较小；paramiko 成熟但同步 | 选 asyncssh，框架整体基于 asyncio；paramiko 作为 fallback |
109: | 容器网络不稳定导致连接中断 | 长时间任务执行失败 | 指数退避重连 + 命令级幂等设计 + nohup 包装长任务 |
110: | CC 安装脚本在不同 OS 上行为不一致 | 自动安装失败 | 预定义支持的 OS 列表，不支持的抛明确错误 |
111: 
112: ## P2: MinerU Client
113: 
114: > [!info]
115: > MinerU Cloud API 是论文 PDF → Markdown 的唯一入口。本阶段交付独立的 API 客户端，不依赖其他模块。
116: 
117: > [!note]
118: > 结合当前仓库已落地的 CLI 与 `execution` 模块骨架，P2 的具体实施规划见 [[LLM-Working/p2-mineru-implementation-plan]]。
119: 
120: **交付物：**
121: 
122: - `MinerUClient` 类：封装 MinerU Cloud API 的完整调用流程
123: - PDF 提交接口：`submit_pdf(pdf_path) → task_id`
124: - 轮询与结果获取：`poll_result(task_id) → ParseResult(markdown, figures, metadata)`
125: - 结构验证：检查返回的 Markdown 是否包含标题、摘要、正文等必要结构
126: - 错误处理：API 限流重试、解析失败分类（PDF 损坏 / 结构无法提取 / API 超时）
127: - 本地缓存：相同 PDF（按 SHA256）不重复提交
128: 
129: **可测试标准：**
130: 
131: - 提交一份已知结构良好的 PDF → 获取 Markdown → 包含标题、摘要、至少 3 个 section
132: - 提交一份损坏的 PDF → 返回明确的 `ParseFailure` 而非未处理异常
133: - 重复提交同一 PDF → 命中本地缓存，不发起 API 调用
134: - API 限流场景 → 自动重试 → 最终成功或返回 `RateLimitExhausted`
135: 
136: **依赖：** 无——完全独立模块，可与 P0/P1/P3 并行开发。
137: 
138: **风险：**
139: 
140: | 风险 | 影响 | 缓解策略 |
141: | --- | --- | --- |
142: | MinerU API 不可用或变更 | 论文解析完全阻塞 | 定义 `PaperParser` 抽象接口，MinerU 作为默认实现；预留本地 fallback（如 marker） |
143: | 复杂 PDF（双栏、大量公式）解析质量差 | PaperCard 信息不完整 | 解析后自动质量评分，低于阈值标记为 `partial_parse`，不阻塞流程 |
144: | API 费用超预期 | 预算消耗过快 | 客户端内置调用计数和费用估算，接近预算时告警 |
145: 
146: ## P3: Artifact Model & State Store
147: 
148: > [!info]
149: > 工件模型是整个框架的核心数据结构（详见 [[framework/artifact-graph-architecture]]）。本阶段把设计文档中的一等工件转化为可运行的 Pydantic models 和状态机。
150: >
151: > 结合当前仓库已落地的 `execution` / `parsing` 模块边界与本地状态约束，P3 的具体实施规划见 [[LLM-Working/p3-artifact-state-store-implementation-plan]]。
152: 
153: **交付物：**
154: 
155: - 全部一等工件的 Pydantic v2 models：`PaperCard`、`ReproductionTask`、`ExperimentRun`、`EvidenceRecord`、`Claim`、`ExplorationGraph`、`QualityAssessment`、`WorkspaceManifest`、`HumanGate`、`AgentAdapter`
156: - 状态机实现：每个有生命周期的工件（PaperCard、ReproductionTask、ExperimentRun、HumanGate）定义合法状态转换，非法转换抛 `InvalidTransitionError`
157: - `StateStore` 接口与 JSON 实现：`save(artifact)`、`load(artifact_type, id)`、`query(artifact_type, filters)`
158: - Checkpoint/Resume：`checkpoint()` 序列化全部活跃工件到 JSON 文件；`resume(checkpoint_path)` 恢复状态
159: - 工件关系索引：维护工件间的引用关系（如 PaperCard → ReproductionTask → ExperimentRun）
160: 
161: **可测试标准：**
162: 
163: - 创建 `PaperCard(status="captured")` → 转换到 `structured` → 成功
164: - 尝试 `PaperCard(status="captured")` → 直接转换到 `completed` → 抛 `InvalidTransitionError`
165: - `save()` 一组工件 → 关闭进程 → `load()` 恢复 → 所有字段一致
166: - `checkpoint()` → 修改工件状态 → `resume()` → 状态回到 checkpoint 时刻
167: - 创建 PaperCard → 关联 ReproductionTask → 查询 PaperCard 的下游工件 → 返回该 ReproductionTask
168: 
169: **依赖：** 无——纯数据模型，可与 P0/P1/P2 并行开发。
170: 
171: **风险：**
172: 
173: | 风险 | 影响 | 缓解策略 |
174: | --- | --- | --- |
175: | 工件 schema 在后续阶段频繁变更 | 已持久化的 JSON 与新 schema 不兼容 | 每个工件带 `schema_version` 字段 + 编写迁移函数 |
176: | JSON 文件在并发写入时损坏 | 状态丢失 | 写入使用 atomic write（先写临时文件再 rename）+ 文件锁 |
177: | 状态机复杂度随工件增多而膨胀 | 维护困难 | 用声明式状态转换表而非 if-else，状态图可自动生成文档 |
178: 
179: ## P4: FastAPI Service & Auth
180: 
181: > [!info]
182: > FastAPI 服务是框架的对外接口层（详见 [[framework/v1-rfc]]）。本阶段交付 API 骨架、认证和所有端点的 request/response models。
183: >
184: > 结合当前仓库已落地的 `execution`、`artifacts`、`state` 模块边界与本地 daemon 约束，P4 的具体实施规划见 [[LLM-Working/p4-fastapi-service-auth-implementation-plan]]。
185: 
186: **交付物：**
187: 
188: - FastAPI 应用骨架：`ainrf.api` 模块，含 `app.py`、`routes/`、`middleware/`、`schemas/`
189: - 认证中间件：API Key 认证，从 header `X-API-Key` 读取，支持多 key 管理
190: - 核心端点（request/response models 完整，业务逻辑可为 stub）：
191:   - `POST /tasks` — 创建研究任务（Mode 1 或 Mode 2）
192:   - `GET /tasks/{id}` — 查询任务状态与工件摘要
193:   - `POST /tasks/{id}/cancel` — 取消运行中的任务
194:   - `GET /tasks/{id}/artifacts` — 获取任务关联的所有工件
195:   - `GET /health` — 服务健康检查
196: - Daemon 启动模式：`ainrf serve --port 8000 --daemon` 后台运行
197: - OpenAPI schema 自动生成，包含完整的类型定义和示例
198: 
199: **可测试标准：**
200: 
201: - 无 API Key 请求任意端点 → 401 Unauthorized
202: - 无效 API Key → 401
203: - 有效 Key + `POST /tasks` 合法 body → 201 Created + 返回 task_id
204: - 有效 Key + `GET /tasks/{id}` → 200 + 任务状态 JSON
205: - `GET /health` → 200 + `{"status": "ok"}`
206: - `GET /openapi.json` → 完整 OpenAPI schema，所有端点和 model 均有定义
207: - `ainrf serve --daemon` → 进程后台运行 → `curl /health` 成功
208: 
209: **依赖：** P3（API 的 request/response models 基于工件 Pydantic models）
210: 
211: **风险：**
212: 
213: | 风险 | 影响 | 缓解策略 |
214: | --- | --- | --- |
215: | API 设计在集成阶段需要大幅调整 | 前端/客户端代码返工 | 先定义 OpenAPI spec，用 spec-first 方式开发；版本化 API（`/v1/`） |
216: | Daemon 模式下日志丢失 | 问题难以排查 | 日志写文件 + 支持 `--log-file` 参数；structlog JSON 格式 |
217: 
218: ## P5: Human Gate & Webhook
219: 
220: > [!info]
221: > 人工关卡是有界自治的核心机制（详见 [[framework/ai-native-research-framework]] 和 [[framework/v1-dual-mode-research-engine]]）。V1 保留两个显式关卡：纳入关卡和计划关卡。
222: >
223: > 结合当前仓库已落地的 P4 task-scoped 路由、`HumanGate` artifact 与本地 state read model，P5 的具体实施规划见 [[LLM-Working/p5-human-gate-webhook-implementation-plan]]。
224: 
225: **交付物：**
226: 
227: - `HumanGateManager` 类：管理关卡的创建、等待、审批/拒绝生命周期
228: - 关卡类型：`intake`（纳入关卡）和 `plan_approval`（计划关卡），各有专属的 payload schema
229: - Webhook 发送：关卡触发时向配置的 URL 发送 POST 请求，包含关卡详情和审批链接
230: - 审批端点：
231:   - `POST /tasks/{id}/approve` — 审批当前 waiting gate
232:   - `POST /tasks/{id}/reject` — 拒绝当前 waiting gate，并可附带反馈
233:   - `GET /tasks?status=gate_waiting` — 列出所有待审批任务
234: - Yolo 模式旁路：配置 `yolo: true` 时自动批准所有关卡，用于测试和信任场景
235: - 超时处理：关卡超过配置时间未审批 → 自动暂停任务 + 发送提醒 webhook
236: **可测试标准：**
237: 
238: - 任务到达纳入关卡 → webhook POST 发出 → 包含 gate_id 和 payload
239: - `POST /tasks/{id}/approve` → 当前 waiting gate 变为 `approved` → 任务继续执行
240: - `POST /tasks/{id}/reject` → 当前 waiting gate 变为 `rejected` → 任务按 gate 语义回退或终止
241: - Yolo 模式开启 → 关卡创建后立即自动批准 → 不发送 webhook → 任务无阻塞
242: - 关卡超时 → 任务暂停 → 提醒 webhook 发出 → 人工审批后恢复
243: 
244: **依赖：** P3（HumanGate 工件模型）、P4（API 端点挂载）
245: 
246: **风险：**
247: 
248: | 风险 | 影响 | 缓解策略 |
249: | --- | --- | --- |
250: | Webhook 目标不可达 | 人无法收到审批通知 | 重试 3 次 + 指数退避；支持多 webhook URL；失败后记录到日志供轮询发现 |
251: | Yolo 模式误用于生产 | 跳过关键审批 | 启动时 yolo 模式打印醒目警告；API 响应中标注 `auto_approved: true` |
252: 
253: ## P6: SSE Streaming
254: 
255: > [!info]
256: > Server-Sent Events 提供任务执行的实时可观测性。客户端（CLI、Web UI、webhook consumer）通过 SSE 订阅任务事件流。
257: >
258: > 结合当前仓库已落地的 P4 task-scoped 路由、P5 Human Gate 生命周期与本地 JSON state 约束，P6 的具体实施规划见 [[LLM-Working/p6-sse-streaming-implementation-plan]]。
259: 
260: **交付物：**
261: 
262: - SSE 端点：`GET /tasks/{id}/events`，返回 `text/event-stream`
263: - 事件类型定义：
264:   - `task.started` / `task.completed` / `task.failed` / `task.cancelled`
265:   - `artifact.created` / `artifact.updated` — 工件生命周期事件
266:   - `gate.pending` / `gate.resolved` — 人工关卡事件
267:   - `experiment.started` / `experiment.completed` — 实验执行事件
268:   - `log.info` / `log.warning` / `log.error` — 结构化日志事件
269: - 事件持久化：所有事件写入 append-only 的 JSON Lines 文件
270: - 断线重连：客户端通过 `Last-Event-ID` header 从断点恢复
271: - 事件过滤：`?types=artifact,gate` 参数只订阅指定类型
272: **可测试标准：**
273: 
274: - 连接 `GET /tasks/{id}/events` → 触发任务 → 收到 `task.started` 事件
275: - 工件状态变更 → SSE 推送 `artifact.updated` 事件 → 包含工件 ID 和新状态
276: - 断开连接 → 重连并携带 `Last-Event-ID` → 从断点继续接收，不丢失事件
277: - `?types=gate` 过滤 → 只收到 `gate.*` 事件，不收到 `artifact.*` 事件
278: - 任务完成后连接 → 收到完整历史事件回放 + `task.completed` 终止事件
279: 
280: **依赖：** P4（SSE 端点挂载在 FastAPI 服务上）
281: 
282: **风险：**
283: 
284: | 风险 | 影响 | 缓解策略 |
285: | --- | --- | --- |
286: | 长连接占用服务器资源 | 并发任务多时连接数爆炸 | 设置最大连接数 + 空闲超时断开 + 客户端自动重连 |
287: | 事件积压导致内存增长 | 服务 OOM | 事件持久化到文件而非内存队列；SSE 从文件读取 |
288: 
289: ## P7: Agent Adapter & Task Engine
290: 
291: > [!info]
292: > Adapter 是宿主无关设计的关键抽象（详见 [[framework/artifact-graph-architecture]]）。TaskEngine 是编排核心，驱动工件状态机并通过 Adapter 在容器上执行原子研究动作。
293: 
294: **交付物：**
295: 
296: - `AgentAdapter` 抽象基类：定义宿主无关的研究动作接口
297:   - `ingest_paper(pdf_path) → PaperCard`
298:   - `plan_reproduction(paper_card) → ReproductionTask`
299:   - `implement_from_paper(task) → CodeArtifact`
300:   - `run_experiment(config) → ExperimentRun`
301:   - `analyze_deviation(expected, actual) → EvidenceRecord`
302: - `ClaudeCodeAdapter` 实现：基于 `claude_code_sdk`，通过 SSH 在容器上调用 CC 执行研究动作
303:   - 每个动作映射为一次 CC 会话，带有结构化 system prompt 和工具约束
304:   - 结果解析：从 CC 输出中提取结构化工件数据
305: - `TaskEngine` 编排器：
306:   - 接收任务请求 → 初始化工件 → 按工作流驱动状态转换
307:   - 在每个状态转换点检查人工关卡、预算边界、终止条件
308:   - 发射 SSE 事件 → 持久化状态 → 处理失败与重试
309:   - 支持 checkpoint/resume：任意时刻可暂停，重启后从最近 checkpoint 恢复
310: **可测试标准：**
311: 
312: - 提交任务 → TaskEngine 创建 PaperCard → 状态从 `captured` 转到 `structured` → SSE 事件发出
313: - TaskEngine 到达 HumanGate → 暂停 → approve → 继续执行下一步
314: - 通过 ClaudeCodeAdapter 在容器上执行 `echo "test"` → 返回结果 → 解析成功
315: - TaskEngine 执行中 kill 进程 → 重启 → `resume()` → 从最近 checkpoint 继续
316: - 预算耗尽 → TaskEngine 自动终止 → 记录终止原因 → 发射 `task.cancelled` 事件
317: 
318: **依赖：** P1（SSH 执行器）、P3（工件模型）、P4（API 集成）
319: 
320: **风险：**

(Showing lines 1-320 of 476. Use offset=321 to continue.)
</content>
```

**Tool: grep**

**Input:**
```json
{
  "include": "*.md",
  "path": "/Users/kozmosa/code/scholar-agent",
  "pattern": "auto-claude-code-research-in-sleep|/research-pipeline|research-pipeline start discovering|Mode 1|Mode 2"
}
```

**Output:**
```
Found 76 matches
/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md:
  Line 17: > 分阶段实现计划，每阶段有明确交付物和可测试标准。总体原则：infrastructure first → Mode 2（更可控）→ Mode 1（更开放）。基础设施阶段（P0-P6）可大量并行；Mode 2（P8）整合全部基础设施；Mode 1（P9）在 Mode 2 之上叠加探索能力。
  Line 45:     P8 Mode 2 Deep Repro       :p8, after p7 p2 p5 p6, 7d
  Line 46:     P9 Mode 1 Lit Exploration  :p9, after p8, 7d
  Line 191:   - `POST /tasks` — 创建研究任务（Mode 1 或 Mode 2）
  Line 328: ## P8: Mode 2 — Deep Reproduction Pipeline
  Line 331: > Mode 2 是更可控的模式——给定单篇论文，从零实现并高精度复现。本阶段整合 P1-P7 全部基础设施，交付端到端的深度复现能力。详见 [[framework/v1-dual-mode-research-engine]] 中 Mode 2 工作流定义。
  Line 365: ## P9: Mode 1 — Literature Exploration Pipeline
  Line 368: > Mode 1 是更开放的模式——从种子论文出发递归探索文献网络。本阶段在 Mode 2 复现能力之上叠加探索、排序和终止控制。详见 [[framework/v1-dual-mode-research-engine]] 中 Mode 1 工作流定义。
  Line 375: - 选择性复现：对高价值论文触发 ReproductionTask（复用 P8 的 Mode 2 能力）
  Line 417:     P8[P8: Mode 2 Deep Repro]
  Line 418:     P9[P9: Mode 1 Lit Exploration]

/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md:
  Line 26: - 如果要找“过夜自治研究流水线”，优先看 [[projects/auto-claude-code-research-in-sleep]]。
  Line 72: | [[projects/auto-claude-code-research-in-sleep]] | 自治流水线 | 强 | 强 | 强 | 强 | 强 | 以 Claude + 外部 reviewer 为主 | 想把研究循环过夜跑起来的人 |
  Line 94:     H -->|是, 且重自治| I[[projects/auto-claude-code-research-in-sleep]]
  Line 113: - [[projects/auto-claude-code-research-in-sleep]]、[[projects/claude-code-deep-research]]、[[projects/academic-research-skills]] 更像可执行的研究流程。
  Line 126: - [[projects/auto-claude-code-research-in-sleep]] 最强调自治回路、跨模型 reviewer 和实验执行。
  Line 136: - 想直接搭“研究会自己跑一晚”的系统：选 [[projects/auto-claude-code-research-in-sleep]]。
  Line 158: - [[projects/auto-claude-code-research-in-sleep]]

/Users/kozmosa/code/scholar-agent/docs/projects/claude-code-deep-research.md:
  Line 85: - [[projects/auto-claude-code-research-in-sleep]]

/Users/kozmosa/code/scholar-agent/docs/projects/awesome-claudecode-paper-proofreading.md:
  Line 84: - [[projects/auto-claude-code-research-in-sleep]]

/Users/kozmosa/code/scholar-agent/docs/projects/autoresearch.md:
  Line 100: - [[projects/auto-claude-code-research-in-sleep]]

/Users/kozmosa/code/scholar-agent/docs/projects/auto-claude-code-research-in-sleep.md:
  Line 21: - README 定义了 3 条主工作流：`/idea-discovery`、`/auto-review-loop`、`/paper-writing`，并可组合成 `/research-pipeline`。

/Users/kozmosa/code/scholar-agent/docs/projects/argusbot.md:
  Line 92: - [[projects/auto-claude-code-research-in-sleep]]

/Users/kozmosa/code/scholar-agent/docs/index.md:
  Line 23: - 如果目标是“直接做研究/写论文”，优先看 [[projects/auto-claude-code-research-in-sleep]]、[[projects/claude-code-deep-research]]、[[projects/academic-research-skills]]、[[projects/awesome-claudecode-paper-proofreading]]。
  Line 42: | [[projects/auto-claude-code-research-in-sleep]] | 过夜自治科研流水线 | 强调跨模型协作、实验执行与自动 review |
  Line 56: - 自治研究流水线：[[projects/auto-claude-code-research-in-sleep]]

/Users/kozmosa/code/scholar-agent/docs/projects/academic-research-skills.md:
  Line 88: - [[projects/auto-claude-code-research-in-sleep]]

/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md:
  Line 22: - `ARIS` 最适合贡献长链路编排、实验执行和跨模型审查。其 nightly loop 和探索循环直接启发了 Mode 1 的递归探索，区别在于我们附加了终止合同（深度/预算/递减收益）而非开放式自治。
  Line 27: - `autoresearch` 最适合贡献"固定预算实验原语 + 单标量评估 + git-native 追踪"思路，作为 Mode 1 递归探索中最轻量的实验执行参考。
  Line 36: | [[projects/auto-claude-code-research-in-sleep]] | 编排与执行参考 | nightly loop、run-experiment、探索循环、终止模式、外部 reviewer、研究闭环意识 | 无约束自治默认值；框架用终止合同替代 |
  Line 48: - 编排层优先借鉴 [[projects/auto-claude-code-research-in-sleep]] 的执行链条和探索循环，用终止合同（深度/预算/递减收益）替代其无约束自治默认。还可借鉴 [[projects/autoresearch]] 的固定预算 + 单标量评估 + git-native 追踪模式，作为实验执行原语的最轻量参考。

/Users/kozmosa/code/scholar-agent/docs/framework/index.md:
  Line 16: > 这一组笔记把现有参考项目抽象成我们自己的 AI-Native Research Framework——一个有界自治研究系统，支持两种核心操作模式：文献探索与复现（Mode 1）和深度复现（Mode 2）。V1 在隔离容器上自主运行，人在纳入和计划阶段定义合同边界。
  Line 58: - [[projects/auto-claude-code-research-in-sleep]]

/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md:
  Line 173: - `mode`：必填。`literature_exploration` 对应 Mode 1，`deep_reproduction` 对应 Mode 2。
  Line 174: - `papers`：必填。至少一篇。`pdf_url` 和 `pdf_path` 二选一，系统优先使用本地路径。`role` 在 Mode 1 中为 `seed`，Mode 2 中为 `target`。
  Line 175: - `config.mode_1`：Mode 1 专属配置。`domain_context` 帮助 agent 判断论文相关性；`max_depth` 控制递归探索深度；`focus_directions` 和 `ignore_directions` 引导探索方向。
  Line 176: - `config.mode_2`：Mode 2 专属配置。`scope` 决定复现范围；`target_tables` 指定需要复现的表格；`baseline_first` 控制是否先跑小规模验证。
  Line 349: - **planning**：根据 mode 和 config 生成执行计划。Mode 1 生成探索计划（深度、方向、预算分配）；Mode 2 生成复现计划（实现步骤、实验矩阵、里程碑）。
  Line 358: TaskEngine 不会把整个 Mode 1 或 Mode 2 工作流作为一次 Claude Code 调用。而是将工作流拆解为细粒度的原子任务，每个原子任务对应一次 CC SDK 调用：
  Line 360: **Mode 1 原子任务示例：**
  Line 370: **Mode 2 原子任务示例：**
  Line 592:   "summary": "Mode 1 探索计划：3 篇种子论文，最大深度 3，预算 24 GPU 小时",
  Line 714: - **增量探索**：Mode 1 任务完成后，基于已有 ExplorationGraph 继续探索，而非从头开始。

/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md:
  Line 16: > V1 支持两种核心操作模式：文献探索与复现（Mode 1）和深度复现（Mode 2）。系统在人类预设的合同边界内自主运行——人在纳入和计划阶段定义边界，agent 在边界内自治执行、全量归档。执行环境是隔离容器（SSH、GPU、root），每个研究项目是独立 git repo。
  Line 27: **Mode 1 专属目标：**
  Line 34: **Mode 2 专属目标：**
  Line 43: ### Mode 1 — 文献探索与复现
  Line 60: ### Mode 2 — 深度复现
  Line 81: ### Mode 1 工作流
  Line 106: ### Mode 2 工作流
  Line 128: ### Mode 1 细化
  Line 135: ### Mode 2 细化
  Line 149: | 纳入关卡 | Mode 1 & 2 | 人决定哪些论文进入系统：种子论文（Mode 1）或目标论文（Mode 2）。 |
  Line 150: | 计划关卡 | Mode 1 & 2 | 人审批复现/探索计划——包括范围（Mode 2：core-only vs full-suite）、资源预算、递归深度上限（Mode 1）和终止条件。 |
  Line 156: **Mode 1：**
  Line 162: **Mode 2：**
  Line 187: - [[projects/auto-claude-code-research-in-sleep]]

/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md:
  Line 15: > 如果没有统一工件模型，研究系统就会退化成"几个 skill + 一堆输出文件"。这份笔记定义框架中的一等对象、层间边界和状态转换，确保无论是 Mode 1 的文献递归探索还是 Mode 2 的从零深度复现，所有研究状态都在同一张图里。
  Line 21: - `ReproductionTask`：对某篇论文或某个方法发起的复现任务，包含目标、入口、依赖、成功标准和停止条件。区分两种策略：`reproduce-from-source`（有开源代码，复现已有实现）和 `implement-from-paper`（无开源代码，从论文描述从零实现，Mode 2 主路径）。
  Line 25: - `ExplorationGraph`：Mode 1 专属工件，跟踪文献探索的前沿状态——哪些 PaperCard 已访问、哪些排队中、哪些触发了复现、哪些被剪枝、当前递归深度和预算消耗。没有它，递归探索在工件模型中没有显式表示。
  Line 26: - `QualityAssessment`：Mode 2 专属工件，将多个 Claim 汇聚为对目标论文的结构化评估——含金量（方法是否有实质贡献）、可复现性（结果是否可重现）、方法科学性（实验设计是否严谨）。比泛化的 `Claim` 更结构化，适合作为最终可交付评估报告。
  Line 53: ### Mode 1 — 文献探索与复现
  Line 73: ### Mode 2 — 深度复现
  Line 109: - Mode 2 实现失败（论文方法描述不充分，无法从零实现）应记录为 `ReproductionTask: blocked`，附带具体卡点说明。
  Line 110: - Mode 1 深度/预算耗尽（探索未收敛即触顶）应在 `ExplorationGraph` 中标注终止原因和当前前沿状态。

/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md:
  Line 26: - **Mode 1 — 文献探索与复现**：给定一篇或数篇种子论文（综述或顶会），系统在隔离容器中自主探索、复现、跟踪相关文献，按深度上限/预算/递减收益自动终止，产出文献复现报告、idea 验证报告、核心发现和下一步建议。
  Line 27: - **Mode 2 — 深度复现**：给定一篇没有开源代码的论文，系统从零实现论文方法，按实验设置高精度复现文中表格，产出可运行代码、实验结果、偏差分析和对论文含金量、可复现性、方法科学性的结构化评估。
  Line 70: - **纳入关卡**：人决定哪些论文作为种子进入系统（Mode 1）或作为目标论文进入深度复现（Mode 2）。

/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md:
  Line 33: │   └── explored/        # Mode 1 递归探索中发现并解析的论文
  Line 34: ├── src/                 # 实现代码（Mode 2 从零实现；Mode 1 复现脚本）
  Line 44: │   ├── quality/         # 论文质量评估报告（Mode 2）
  Line 45: │   └── exploration/     # 探索报告与下一步建议（Mode 1）
  Line 50: │   └── exploration-graph.json  # ExplorationGraph 状态（Mode 1）
  Line 59: - 对于 Mode 1 递归探索中引用链上的论文，agent 按需调用 MinerU 解析并存入 `papers/explored/`。
  Line 71:   - Mode 1 每轮探索迭代结束时
  Line 72:   - Mode 2 每个主要实现里程碑后
```

**Tool: glob**

**Input:**
```json
{
  "path": "/Users/kozmosa/code/scholar-agent/ref-repos",
  "pattern": "**/auto-claude-code-research-in-sleep/**"
}
```

**Output:**
```
No files found
```

**Tool: task**

**Input:**
```json
{
  "command": "explore mode baseline from reference",
  "description": "derive mode baseline",
  "prompt": "只读探索 ref-repos 中 auto-claude-code-research-in-sleep 相关仓库/文档，以及本仓库 docs 中对它的引用。目标：帮助把下一版 Mode1/Mode2 重定义为可执行 baseline。不要修改任何文件。返回：1) 参考仓库提供了哪些实际可借鉴的 skill/prompt/workflow；2) 哪些最适合作为 Mode1 baseline；3) 哪些最适合作为 Mode2 baseline；4) 需要避免的过度承诺。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a6f393e2ffeCYd8NwnAHTysPf (for resuming to continue this task if needed)

<task_result>
先说结论：当前工作区里并没有实际可读的 `Auto-claude-code-research-in-sleep` 参考仓库内容；`/Users/kozmosa/code/scholar-agent/ref-repos` 下目前只有 `Awesome-AI-Scientist/`。所以这次只能基于本仓库中已有的二手研究笔记，做“静态转译”，不能声称我已核验该参考仓库的 README/skills 实现细节。

我实际读取并依据的文件是：

- `/Users/kozmosa/code/scholar-agent/docs/projects/auto-claude-code-research-in-sleep.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
- `/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md`
- `/Users/kozmosa/code/scholar-agent/docs/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`

另外，笔记里引用了但本地不存在的目标路径是：

- `/Users/kozmosa/code/scholar-agent/ref-repos/Auto-claude-code-research-in-sleep/README_CN.md`
- `/Users/kozmosa/code/scholar-agent/ref-repos/Auto-claude-code-research-in-sleep/skills`
- `/Users/kozmosa/code/scholar-agent/ref-repos/Auto-claude-code-research-in-sleep/mcp-servers`

下面按你的 4 个目标给出判断。

---

## 1) 参考仓库提供了哪些实际可借鉴的 skill / prompt / workflow

基于现有笔记，可明确提炼出的可借鉴元素主要有 3 类。

### A. 可借鉴 workflow

这是证据最强的一部分。

从 `/Users/kozmosa/code/scholar-agent/docs/projects/auto-claude-code-research-in-sleep.md` 可提炼出该项目的主工作流：

- `/idea-discovery`
- `/auto-review-loop`
- `/paper-writing`
- 并可组合成 `/research-pipeline`

以及更具体的研究链条：

1. 研究方向输入
2. idea discovery
3. 文献检索与 novelty check
4. 实验设计与运行
5. auto review loop
6. 外部模型批判式审查
7. 改实验 / 改论证
8. paper writing
9. LaTeX / PDF 产出
10. 可选通知与知识库集成

这里最值得借鉴的不是“全套论文工厂”，而是这几个 workflow 原语：

- idea discovery 作为前期发散入口
- novelty check 作为早期去重/降幻觉关卡
- run-experiment / monitor-experiment / analyze-results 作为中期执行闭环
- auto-review-loop 作为每轮产出后的批判性回看
- 失败也作为正式输出，而非 silently retry

### B. 可借鉴 skill 颗粒度

虽然本地没有 `skills/` 目录本体，但 docs 已经总结了其 skill 覆盖面，说明它不是单 prompt，而是一组研究阶段化技能。

已被明确提到的 skill/能力块包括：

- literature survey
- idea discovery
- novelty check
- research planning
- run-experiment
- monitor-experiment
- analyze-results
- paper-plan
- paper-write
- paper-compile
- auto-paper-improvement-loop
- Feishu/Lark 通知
- Zotero / Obsidian / 本地 PDF / 远程服务器集成

对你现在“把下一版 Mode1/Mode2 重定义为可执行 baseline”的目标来说，最有价值的不是全量保留，而是把这些能力压缩成更小的 baseline skill 集：

- 检索与读文献
- novelty / related-work sanity check
- 制定实验或复现计划
- 执行单轮实验
- 监控与汇总结果
- reviewer 式批判反馈
- 根据反馈决定继续 / 终止

### C. 可借鉴 prompt / role 设计

虽然没拿到原 prompt 文本，但 docs 已明确其角色分工：

- Claude Code 负责执行
- 外部 LLM（Codex/GPT-5.4）负责更慢但更严谨的 reviewer
- 强调跨模型协作，而不是单模型自审

这能转译成非常实用的 prompt 结构，而不是照搬宿主实现：

1. Executor prompt
   - 负责检索、编码、运行、记录、汇总
   - 目标是推进状态，而不是最终宣称成功

2. Reviewer prompt
   - 专门找漏洞、遗漏变量、证据不足、实验缺口、论证过度
   - 默认不负责“帮忙写更好看”，而是负责“挑错和设 gate”

3. Termination / continuation contract
   - 每轮必须回答：是否值得继续，依据是什么，下一轮增益在哪里
   - 用 budget/depth/收益递减替代无限循环

这其实是比 skill 名字更值得吸收的部分。

---

## 2) 哪些最适合作为 Mode1 baseline

如果目标是“下一版 Mode1 重定义为可执行 baseline”，我建议只吸收 ARIS 中最轻、最稳、最少依赖的部分，不要把“过夜自治论文工厂”整体搬进来。

### 我认为最适合 Mode1 baseline 的元素

#### a) `idea discovery -> literature scan -> novelty check -> recursive exploration`
这是最自然的 Mode1 核心。

依据：
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md` 明确写了：
  - ARIS 最适合贡献 nightly loop、run-experiment、探索循环、终止模式、外部 reviewer、研究闭环意识
  - 其 nightly loop 和探索循环直接启发了 Mode 1 的递归探索
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md` 已把 Mode 1 定义为：
  - 用户给种子论文
  - 系统自主完成文献递归探索
  - 在深度/预算/递减收益条件下终止
  - 产出 `ExplorationGraph`、复现报告、下一步建议

所以 Mode1 baseline 最应该固化为：

- 输入：seed paper / topic / question
- 执行：
  - 读种子论文
  - 扩展相关工作
  - novelty/relatedness 筛查
  - 为候选论文生成可复现性与价值摘要
  - 选出下一层探索对象
- 终止：
  - 达到深度上限
  - 达到 budget 上限
  - 连续 N 轮收益递减
- 输出：
  - `ExplorationGraph`
  - 每篇论文的结构化卡片
  - 候选复现清单 / 下一步建议
  - 失败原因记录

#### b) reviewer-gated exploration，而不是自由探索
Mode1 非常适合引入“轻 reviewer”，但 reviewer 不应阻塞每一步。

建议 baseline 做成：

- executor 生成本轮探索候选
- reviewer 只做三件事：
  - 质疑证据是否够
  - 质疑 novelty 判断是否过强
  - 质疑下一跳是否值得
- 再由 orchestrator 决定是否继续

这比“agent 自己一路扩展直到停不下来”稳得多。

#### c) 失败工件化
Mode1 baseline 很需要这一点。

可直接吸收的思想：

- 解析失败
- PDF 不可读
- 代码仓库不可用
- 复现条件不明
- 相关性不足

都应该成为正式状态，而不是被吞掉。

这和 `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md` 中“失败被记录为正式工件状态”完全一致。

### 不建议放进 Mode1 baseline 的内容

- paper-writing
- LaTeX/PDF 终稿
- Feishu/Obsidian/Zotero 集成
- 远程 GPU 编排
- 多模型/MCP 重度依赖

Mode1 baseline 应该优先证明“探索可控地跑完”，不是“整条研究流水线都接上”。

---

## 3) 哪些最适合作为 Mode2 baseline

Mode2 的目标是“从无代码论文到实现与高精度复现”，所以相较 Mode1，更该借 ARIS 的执行闭环，而不是前期探索闭环。

### 我认为最适合 Mode2 baseline 的元素

#### a) `research plan -> run-experiment -> monitor-experiment -> analyze-results`
这是最像 Mode2 最小闭环的部分。

从 `/Users/kozmosa/code/scholar-agent/docs/projects/auto-claude-code-research-in-sleep.md` 看，ARIS 对“真实驱动 GPU / 远程实验”的意识很强，这正是 Mode2 所需，但 baseline 要做瘦身版：

Mode2 baseline 可执行流程建议：

1. 输入目标论文 + 目标表格/指标
2. 生成 implementation plan
3. 生成 reproduction plan
4. 实现最小可运行版本
5. 运行 core experiment
6. 汇总结果与论文 target 对比
7. reviewer 分析偏差原因
8. 决定：
   - 再跑一轮修正
   - 或宣布当前不可复现并给出结构化原因

这里最关键的是“per-table / per-metric 对比”和“偏差分析”，这与现有 V1 文档很契合。

#### b) 外部 reviewer 作为偏差分析器
Mode2 比 Mode1 更需要 reviewer，因为实现偏差、超参偏差、数据预处理偏差、评估协议偏差都很常见。

最适合吸收的 reviewer 职责：

- 检查实现与论文方法是否一致
- 检查实验设置是否缺失关键细节
- 检查当前结果差距更像：
  - 实现错误
  - 数据处理偏差
  - 训练预算不足
  - 论文信息不充分
- 给出“下一轮最值得尝试的 1-2 个变更”

这会把 reviewer 从“抽象批评者”变成“复现诊断器”。

#### c) “失败复现也是正式产出”
这点对 Mode2 几乎必须保留。

`/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md` 已明确：

- 复现失败本身是有价值的正式输出
- 不保证复现一定成功

Mode2 baseline 最好明确产出：

- 可运行代码
- 环境与依赖记录
- target table 映射
- result diff
- error budget / mismatch hypothesis
- `QualityAssessment`
- unreproducible verdict with evidence

#### d) 有界自治，而不是 nightly free-run
虽然 ARIS 的亮点是“while you sleep”，但你们框架已经很明确要替换成“合同内自治”。

这点在 `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md` 里已经写得很清楚：
- 用终止合同替代其无约束自治默认

所以 Mode2 baseline 最该吸收的是：
- 多轮迭代意识
- 每轮 reviewer 诊断
- 实验执行闭环

而不该吸收的是：
- 默认无限试
- 默认全套 full-suite
- 默认自动写成论文

---

## 4) 需要避免的过度承诺

这是我觉得最重要的一部分。因为 ARIS 在叙事上很强，但你们要定义的是“可执行 baseline”，所以必须防止把 showcase 叙事写成产品承诺。

### A. 避免承诺“过夜就能自动做完研究”
应改成：

- 系统能在合同边界内自主推进研究任务
- 能产出结构化探索/复现结果
- 能在失败时给出正式分析

不要承诺：

- 一晚跑完完整研究闭环
- 自动从方向到论文稳定成稿
- 无人监督即可产出可靠科研结论

### B. 避免承诺“跨模型 reviewer 必然提升质量”
当前证据只支持“这是一个设计思路”，不支持“稳定显著提升”。

更稳妥的表述应是：

- 外部 reviewer 有助于降低单模型自审盲点
- 但其收益受模型质量、提示词、上下文完整性影响

不要承诺：

- reviewer 一定能发现关键问题
- 双模型一定优于单模型
- reviewer 就等同于严谨科学审稿

### C. 避免承诺“Mode2 能高精度复现论文结果”
你们自己的 V1 文档已经写得很对：

- 不保证复现一定成功
- 失败分析是正式输出

所以要避免把 baseline 写成：

- 自动高精度复现 SOTA
- 从无代码论文稳定还原结果表
- 结果偏差可自动收敛到论文水平

更合理的是：

- 尝试实现并逼近目标结果
- 在预算内完成若干轮诊断与修正
- 给出结构化偏差归因

### D. 避免承诺“完整研究流水线 baseline”
baseline 的关键是“能跑通、可界定、可验证”，不是“功能多”。

因此不要把这些也塞进 baseline 承诺：

- 投稿级写作
- rebuttal / revision 工厂
- 远程 GPU 管理
- 多工具生态深度集成
- 全自动数据获取
- 全自动论文定稿

### E. 避免承诺“静态仓库信号 = 真实运行成功率”
`/Users/kozmosa/code/scholar-agent/docs/summary/academic-research-agents-overview.md` 已经明确提醒：
- 静态仓库信号强，不等于真实运行成功率强
- 长链路质量受模型、权限、远程环境、数据条件影响

这句话应该直接内化进你们的 baseline 叙述。

---

## 最后给一个可直接落地的 baseline 建议

### Mode1 baseline
定义成“有界文献探索与候选复现筛选器”最稳：

- 输入：seed paper / topic
- 核心步骤：
  - read
  - expand citations / related work
  - novelty check
  - candidate ranking
  - lightweight reviewer critique
  - bounded recursion
- 输出：
  - `ExplorationGraph`
  - paper cards
  - candidate reproduction list
  - failure states
- 不包含：
  - paper writing
  - heavy experiment orchestration
  - external integrations as requirement

### Mode2 baseline
定义成“有界实现与复现诊断器”最稳：

- 输入：paper + target table/metric + data source contract
- 核心步骤：
  - implementation plan
  - minimal implementation
  - core experiment run
  - result comparison
  - reviewer-based discrepancy diagnosis
  - bounded retry
- 输出：
  - runnable code
  - result table diff
  - discrepancy analysis
  - `QualityAssessment`
  - unreproducible report if needed
- 不包含：
  - 投稿级论文自动生成
  - 无限实验搜索
  - 默认远程 infra 自动化

---

如果你愿意，我下一步可以继续做一件更具体的事：基于这些结论，直接给出一版“Mode1/Mode2 baseline 规范草案”，按“输入/状态机/终止合同/最小 skill 集/必需输出”五栏整理。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "plan dashboard requirements",
  "description": "derive dashboard scope",
  "prompt": "只读分析用户刚刚给出的 dashboard 需求，并结合当前 ainrf 实现边界，整理 next release dashboard 的信息架构 baseline。不要修改任何文件。返回：1) 首屏信息区块建议；2) 哪些已有后端能力可支撑；3) 哪些是必须新设计但范围可控的；4) 会导致 scope explosion 的点。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a6f393d8ffe4jb52oO2Uwwgex (for resuming to continue this task if needed)

<task_result>
下面给的是一个“只读、按当前 ainrf 实现边界收敛”的 next release dashboard baseline。结论先说：

当前 ainrf 还不适合做“全量研究运行监控大屏”，但已经足够支撑一个“单机、本地、面向 operator 的任务控制台”：
- 看任务列表
- 看单任务详情
- 看待审批 gate
- 看任务事件流
- 看基础健康状态
- 做 approve / reject / cancel

也就是说，next release 的 dashboard baseline 应该定义成“控制面 dashboard”，而不是“完整研究过程 dashboard”。

---

## 前提边界

结合仓库现状，有两个非常关键的边界：

1. 设计文档里明确写了 V1 不做 Web UI，Web UI 在 future work 里  
   `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`

2. 但当前代码已经落了 dashboard 最关键的后端基础件：
   - FastAPI service
   - task list/detail/artifacts
   - human gate 审批流
   - SSE 事件流  
   主要实现位于：
   - `/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py`
   - `/Users/kozmosa/code/scholar-agent/src/ainrf/gates/manager.py`
   - `/Users/kozmosa/code/scholar-agent/src/ainrf/events/service.py`
   - `/Users/kozmosa/code/scholar-agent/src/ainrf/events/store.py`

所以 next release 可以做 dashboard，但必须定位成：
- 不发明新运行时
- 不假装已有 experiment/runtime telemetry
- 只消费现有 control-plane API 和事件

---

# 1) 首屏信息区块建议

我建议首屏不是“大盘”，而是“操作型首页”，按优先级分成 5 个区块。

## A. System Status / Service Health 顶部状态条
目标：用户一进来先知道系统是不是可用。

建议展示：
- API 服务状态：ok / degraded
- state root 路径
- container 是否已配置
- container SSH 是否可用
- Claude 是否可用
- project_dir 是否可写
- GPU / CUDA / 磁盘剩余
- 最近一次健康检查时间

为什么要放首屏顶部：
- 当前 ainrf 更像本地 orchestrator/control-plane，不是 SaaS
- 如果 container 连不上，后面所有任务信息都缺乏执行意义

这块非常贴合已有 `/health` 能力。

---

## B. Pending Actions / 待处理事项
目标：把“必须人处理的东西”放在最显眼的位置。

建议展示：
- 当前等待审批的任务数
- 每个 waiting gate 的：
  - task_id
  - gate_type
  - summary
  - deadline_at
  - 是否已 reminder
- 快捷操作：
  - approve
  - reject
  - 打开任务详情

为什么这块优先级很高：
- 现阶段 ainrf 最成熟、最明确的控制面能力其实就是 human gate
- dashboard 第一价值不是“展示”，而是“缩短审批闭环”

这块会比“预算图表”更符合现在的实现成熟度。

---

## C. Task Snapshot / 任务概览列表
目标：让用户快速浏览系统里有哪些任务、处于什么阶段。

建议列表字段：
- task_id
- mode
- status
- current_stage
- created_at / updated_at
- termination_reason
- active_gate 标记
- artifact 总数
- 简单预算字段：
  - budget_limit
  - budget_used

建议支持的基础筛选：
- status
- mode
- 是否有 active gate

为什么这是首屏核心：
- 当前后端已经天然围绕 TaskRecord 建模
- dashboard 的主导航对象应该是 task，而不是 artifact 或 graph

注意：
- 首屏这里只放“列表 + 轻摘要”
- 不要首屏直接做复杂 artifact graph

---

## D. Selected Task Summary / 选中任务摘要面板
目标：用户点击一个任务后，不切页也能看关键上下文。

建议展示：
- 基本信息
  - task_id
  - mode
  - status / current_stage
  - termination_reason
- 配置摘要
  - papers 标题
  - yolo
  - container.host / project_dir
- gate 摘要
  - 当前 active gate
  - 历史 gates
- artifact summary
  - 各 artifact_type 数量
- 预算摘要
  - budget_limit vs budget_used

为什么适合 next release：
- 这些信息都已经在 task detail API 中可拼装
- 可以做出“像 dashboard”的信息密度，但几乎不需要新后端协议

---

## E. Live Event Feed / 实时事件流
目标：给 dashboard 一个“正在发生”的感觉，但不承诺超出现有粒度。

建议展示：
- 单任务实时事件 feed
- 支持事件类别过滤：
  - task
  - gate
  - artifact
- 事件卡片内容：
  - timestamp
  - event 名
  - payload 摘要
- 自动保持连接 / 断开后从 Last-Event-ID 恢复

为什么这块可行：
- SSE 已经是真实实现，不是 stub
- 这是当前最接近“dashboard 实时性”的能力

但要注意：
- 现在的事件主要是 task/gate/artifact 状态变化
- 不是运行日志，不是 step-by-step experiment telemetry

---

# 2) 哪些已有后端能力可支撑

下面按“可直接支撑 dashboard”的角度来列。

## 2.1 任务列表与任务详情
已有能力：
- `GET /tasks`
- `GET /tasks/{id}`

可支撑：
- task 首页列表
- task 详情摘要
- 状态筛选
- 当前阶段展示
- termination reason 展示
- budget limit / used 展示
- artifact summary 展示
- gate 历史展示

主要代码：
- `/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py`
- `/Users/kozmosa/code/scholar-agent/src/ainrf/api/schemas.py`

---

## 2.2 Artifact 摘要与清单
已有能力：
- `GET /tasks/{id}/artifacts`

可支撑：
- 单任务 artifact list
- artifact type 分组
- 点击查看 payload
- 作为“详情抽屉”或“侧边栏”展示

限制：
- 现在更适合列表和 JSON payload 浏览
- 还不适合做高级 graph exploration

---

## 2.3 Human Gate 审批流
已有能力：
- 任务创建时会生成 intake gate
- 支持 active gate 查询
- 支持 approve / reject / cancel
- 有 deadline / reminder / resolved / feedback
- 有 gate webhook 机制，但 dashboard 本身不必依赖 webhook

可支撑：
- 待审批区块
- 任务详情里的 gate timeline
- 快捷审批按钮
- “超时提醒/已提醒”状态展示

主要代码：
- `/Users/kozmosa/code/scholar-agent/src/ainrf/gates/manager.py`
- `/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py`

---

## 2.4 SSE 实时事件流
已有能力：
- `GET /tasks/{id}/events`
- 支持历史回放
- 支持 `Last-Event-ID`
- 支持 `types` 分类过滤
- 终态任务自动关闭连接
- 非终态任务 keepalive + 轮询跟随

可支撑：
- 单任务 live feed
- timeline 面板
- 断线重连
- 最近事件侧栏

主要代码：
- `/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py`
- `/Users/kozmosa/code/scholar-agent/src/ainrf/events/store.py`
- `/Users/kozmosa/code/scholar-agent/src/ainrf/events/models.py`
- `/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p6-sse-streaming-impl.md`

---

## 2.5 基础健康检查
已有能力：
- `GET /health`

可支撑：
- 顶部状态条
- container readiness
- SSH/Claude/GPU/disk 基础诊断
- degraded 提示

主要代码：
- `/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/health.py`

---

## 2.6 本地状态持久化
已有能力：
- 任务 JSON 存储
- artifact JSON 存储
- relation index
- event JSONL 存储

可支撑：
- dashboard 重载后恢复历史数据
- 非数据库环境下的本地控制台
- 基于 task_id 的页面深链

主要代码：
- `/Users/kozmosa/code/scholar-agent/src/ainrf/state/store.py`
- `/Users/kozmosa/code/scholar-agent/src/ainrf/events/store.py`

---

# 3) 哪些是必须新设计但范围可控的

这里说的“必须新设计”，不是要做大后端重构，而是 dashboard 要成型，前后端之间仍有几个最小增量需要补。

## 3.1 Dashboard 的主导航模型
必须新设计：
- 首页以“task”为中心，而不是 artifact、paper、experiment
- 从 task list -> selected task -> event feed 的信息流关系
- 首屏是否支持 split view

为什么必须：
- 现在 API 有数据，但还没有 dashboard 的页面级 IA
- 这属于前端/产品层设计，不会碰核心后端边界

建议 baseline：
- 左侧 task list
- 右侧 selected task summary + event feed
- 顶部 health + pending actions

这个设计非常收敛。

---

## 3.2 事件展示语义层
必须新设计：
- 如何把原始 SSE event 名和 payload 转成用户看得懂的 UI 文案
- 例如：
  - `task.stage_changed` -> “任务阶段从 planning 变为 gate_waiting”
  - `gate.waiting` -> “等待人工审批”
  - `artifact.created` -> “新建 human_gate 工件”

为什么必须：
- 当前事件是后端事件，不是直接可读的产品文案
- 但这完全可以做在前端 mapping 层，不必改后端

范围可控点：
- 先只支持当前真实存在的 event 类型
- 未识别事件就 fallback 为 raw JSON 展示

---

## 3.3 首屏聚合视图的数据编排
必须新设计：
- `/health`、`/tasks`、`/tasks/{id}`、`/tasks/{id}/events` 的调用顺序
- 默认选中哪个任务
- 首屏 polling / SSE 订阅策略

为什么必须：
- 现有 API 足够，但还没定义 dashboard 的“数据装配方式”

范围可控建议：
- 首屏只实时订阅“当前选中任务”的 SSE
- 任务列表用定时 refresh，而不是为每个 task 建 SSE
- pending actions 也通过 task detail 或 list 衍生，不做全局 event broker

---

## 3.4 Pending gate 的显式聚合方式
这是一个小的“新设计但可控”点。

当前后端没有单独的“GET /gates?status=waiting”聚合端点，但可以通过：
- `GET /tasks`
- 逐个 `GET /tasks/{id}` 或通过列表摘要扩展
来拼出 pending actions。

如果想让 dashboard 更顺手，下一步可控增量是：
- 增加一个轻量聚合只读端点，例如 pending gate summary

但即使不加，也能先用已有能力拼出来。

所以它属于：
- 不是必须马上新增后端
- 但如果做 dashboard，可能是最值得加的一个小聚合接口

---

## 3.5 预算展示口径
必须新设计：
- budget_used 目前更像“预留字段”，dashboard 如何表达这个不确定性
- 哪些预算数字能展示为真实值，哪些只能展示为“已预留结构、暂无实时消耗源”

建议：
- next release 只展示 budget limit / used 原始数值
- 明确文案写成“budget snapshot”
- 不做 burn-down chart / 预测耗尽时间

这是范围可控的关键。

---

# 4) 会导致 scope explosion 的点

这部分最重要。很多 dashboard 一旦不收边界，很快就会把 ainrf 拖进“先补运行时、再补前端、再补可视化”的失控状态。

## 4.1 实验级实时监控
会爆 scope 的原因：
- 当前并没有真正落地的 P7/P8 engine runtime telemetry
- `experiment.*` 和 `log.*` 在事件模型里有 category 预留，但并没有真实稳定事件源
- 若强做，会逼着后端先实现 execution tracing、step log、stdout 流、失败分类

结论：
- next release 不要承诺“实验过程直播”
- 只做 task/gate/artifact 事件流

---

## 4.2 Artifact graph 可视化
会爆 scope 的原因：
- 虽然 state store 已有 relation index，但没有专门 graph query API
- 图可视化一旦开始做，就会牵涉：
  - 节点类型设计
  - 边类型语义
  - graph layout
  - 过滤/搜索
  - 点击 drill-down
- 很容易从“简单视图”变成知识图谱产品

结论：
- next release 只做 artifact summary + flat list
- 最多加“related artifacts count”
- 不做交互式 graph canvas

---

## 4.3 跨任务分析与全局研究运营指标
例如：
- 所有项目 budget 使用排行
- 所有论文复现成功率
- 失败原因聚类
- artifact 全局搜索
- 多任务热度图

会爆 scope 的原因：
- 当前 API 是 task-scoped + local state store
- 没有 analytics schema、没有索引层、没有稳定的聚合口径
- 一做就会逼出数据库、查询语言、缓存和 migration 问题

结论：
- next release 不做 global analytics dashboard
- 首页只做“当前任务控制台 + 简单任务列表”

---

## 4.4 多容器 / 多节点 / 多用户协作视图
会爆 scope 的原因：
- RFC 明确 V1 不做 1:N 容器调度
- 当前 health 更偏“单配置 container”
- auth 也只是 API key，不是多角色权限系统

结论：
- next release 不要设计成 team dashboard
- 不做 operator presence、role-based controls、multi-runner fleet view

---

## 4.5 可编辑计划、可视化编排、拖拽式工作流
会爆 scope 的原因：
- 当前 ainrf 还是 API-first scaffold，不是 workflow builder
- 计划层和 execution layer 尚未形成完整闭环
- 一旦引入编辑器，就会倒逼 task schema、validation、diff、审批重提交流程

结论：
- dashboard 只做“观察 + 控制”
- 不做“图形化编排”

---

## 4.6 预算预测、成本归因、耗尽预警模型
会爆 scope 的原因：
- 虽然 schema 里有 `budget_limit` / `budget_used`
- 但当前没有稳定来源去实时更新：
  - GPU 实际消耗
  - API 实际成本
  - 预测剩余时间
- 做图表会制造“看起来很精确，实际上没数据”的错觉

结论：
- next release 只做静态 budget snapshot
- 不做预测分析

---

# 收敛后的 baseline 建议

如果要把 next release dashboard 定义成一句话，我建议是：

**一个基于现有 FastAPI + SSE 的 task-centric operator dashboard，优先解决任务可见性、人工审批、基础健康诊断和单任务事件跟踪，不扩展到实验遥测、跨任务分析和图谱可视化。**

---

# 可直接落地的 baseline IA

可以收敛成下面这个版本：

## 首页
1. 顶部健康条
2. 待审批区
3. 任务列表
4. 选中任务摘要
5. 选中任务实时事件流

## 任务详情页/抽屉
1. 基本信息
2. gate timeline
3. artifact summary
4. artifact list
5. raw config / raw payload

## 支持操作
- approve
- reject
- cancel
- 打开 SSE 实时流
- 查看健康状态

---

# 最终回答摘要

## 1) 首屏信息区块建议
- 顶部 System Health 状态条
- Pending Actions / 待审批 gate 列表
- Task Snapshot / 任务概览列表
- Selected Task Summary / 选中任务摘要
- Live Event Feed / 单任务实时事件流

## 2) 哪些已有后端能力可支撑
- `/health` 支撑健康状态条
- `/tasks`、`/tasks/{id}` 支撑任务列表与详情摘要
- `/tasks/{id}/artifacts` 支撑 artifact 列表与摘要
- `/tasks/{id}/approve|reject|cancel` 支撑控制操作
- `/tasks/{id}/events` 的 SSE 支撑实时事件流
- 本地 state store + event store 支撑 dashboard 重载后的历史回放

## 3) 哪些是必须新设计但范围可控的
- dashboard 页面级 IA：task-centric 导航
- 事件到 UI 文案的映射层
- 首屏聚合的数据装配策略
- pending gate 的聚合展示方式
- budget 展示口径的保守定义

## 4) 会导致 scope explosion 的点
- 实验级实时监控与日志直播
- artifact graph 可视化
- 跨任务全局分析与搜索
- 多容器 / 多用户协作面板
- 图形化计划编辑与编排
- 预算预测与成本分析

如果你愿意，我下一步可以继续基于这个 baseline，进一步给出一个“next release dashboard 页面线框 + API 映射表”。
</task_result>
```

**Tool: task**

**Input:**
```json
{
  "command": "plan versioned docs system",
  "description": "design doc system",
  "prompt": "只读基于当前 docs/framework/ 结构与用户要求，规划一个带版本的 manifesto/framework/architecture/decision-log/roadmap 文档体系。不要修改任何文件。返回：1) 推荐的目录结构和命名策略；2) 版本号策略如何落地；3) release freeze/archive 机制；4) 适合按单会话推进的原子任务拆法。",
  "subagent_type": "explore",
  "task_id": ""
}
```

**Output:**
```
task_id: ses_2a6f393cfffevA6Y85duzN1IQt (for resuming to continue this task if needed)

<task_result>
下面是一个只读、基于当前 `docs/framework/` 现状的版本化文档体系规划方案。我会尽量贴合你仓库已经存在的内容和命名习惯，而不是另起一套完全陌生的结构。

当前已存在的框架文档位于：

- `/Users/kozmosa/code/scholar-agent/docs/framework/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-dual-mode-research-engine.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`

从这些内容看，当前实际上已经有了：
- manifesto 倾向：`ai-native-research-framework.md`
- architecture 倾向：`artifact-graph-architecture.md`、`container-workspace-protocol.md`
- versioned spec：`v1-dual-mode-research-engine.md`、`v1-rfc.md`、`v1-roadmap.md`
- reference / rationale：`reference-mapping.md`

你现在要补的是把它们收束成一个“长期可维护、可冻结、可归档、可多版本并存”的体系。

---

## 1) 推荐的目录结构和命名策略

## 1.1 设计原则

建议遵循 4 条原则：

1. 稳定层与版本层分离  
   - 不随版本频繁变化的理念类文档放在顶层稳定区
   - 会随版本演进的 architecture / roadmap / decision-log 放到版本目录里

2. “当前入口”与“历史归档”分离  
   - 当前主线文档应有固定入口
   - 老版本应冻结后归档，但仍可浏览与双链引用

3. 文档类型比阶段名更重要  
   - manifesto / architecture / decision-log / roadmap 这些是“文档职责”
   - v1 / v2 是“版本视图”
   - 最好两者都能从目录中看出来

4. 文件名保持英文 slug，正文中文  
   - 与仓库既有约定一致
   - 也利于 Obsidian / MkDocs 稳定链接

---

## 1.2 推荐目录结构

我建议把 `/Users/kozmosa/code/scholar-agent/docs/framework/` 演进为下面这种结构：

```text
/Users/kozmosa/code/scholar-agent/docs/framework/
  index.md
  manifesto/
    index.md
    core.md
    glossary.md
    principles.md
  architecture/
    index.md
    cross-version.md
    artifact-graph.md
    container-workspace.md
  decisions/
    index.md
    adr-0001-framework-scope.md
    adr-0002-bounded-autonomy.md
    adr-0003-repo-first-state.md
  roadmap/
    index.md
    cross-version.md
  releases/
    index.md
    v1/
      index.md
      manifesto.md
      architecture.md
      decision-log.md
      roadmap.md
      rfc.md
      release-freeze.md
      changelog.md
    v2/
      index.md
      manifesto.md
      architecture.md
      decision-log.md
      roadmap.md
      rfc.md
  archive/
    index.md
    v0-pre-release/
    v1/
```

---

## 1.3 这套结构如何映射当前已有文档

### 稳定层
适合长期稳定、跨版本复用的内容：

- `/Users/kozmosa/code/scholar-agent/docs/framework/manifesto/core.md`
  - 可由当前 `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md` 提炼而来
  - 内容聚焦：愿景、边界、原则、非目标

- `/Users/kozmosa/code/scholar-agent/docs/framework/architecture/artifact-graph.md`
  - 对应当前 `/Users/kozmosa/code/scholar-agent/docs/framework/artifact-graph-architecture.md`

- `/Users/kozmosa/code/scholar-agent/docs/framework/architecture/container-workspace.md`
  - 对应当前 `/Users/kozmosa/code/scholar-agent/docs/framework/container-workspace-protocol.md`

- `/Users/kozmosa/code/scholar-agent/docs/framework/decisions/*.md`
  - 可将当前 `reference-mapping.md` 里“关键取舍”拆成正式 ADR/decision 文档

### 版本层
适合明确和 release 绑定的内容：

- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/manifesto.md`
  - “V1 对核心 manifesto 的裁剪版/落地版”
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/architecture.md`
  - “V1 的实现架构”
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/rfc.md`
  - 对应当前 `/Users/kozmosa/code/scholar-agent/docs/framework/v1-rfc.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/roadmap.md`
  - 对应当前 `/Users/kozmosa/code/scholar-agent/docs/framework/v1-roadmap.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/decision-log.md`
  - 汇总 V1 相关 ADR 链接和 release 内决策

---

## 1.4 命名策略

建议统一采用“双层命名”：

### 目录命名
- 文档类型目录：`manifesto/`、`architecture/`、`decisions/`、`roadmap/`、`releases/`、`archive/`
- 版本目录：`v1/`、`v2/`、`v1.1/` 不推荐；目录层最好只放主版本

### 文件命名
稳定层：
- `core.md`
- `principles.md`
- `glossary.md`
- `cross-version.md`
- `index.md`

版本层：
- `manifesto.md`
- `architecture.md`
- `decision-log.md`
- `roadmap.md`
- `rfc.md`
- `release-freeze.md`
- `changelog.md`

### ADR 命名
推荐：
- `adr-0001-framework-scope.md`
- `adr-0002-bounded-autonomy.md`
- `adr-0003-repo-first-state.md`

不要用：
- `decision1.md`
- `some-thoughts.md`
- `new-architecture-final-v2.md`

原因很简单：后者随着时间必然失控。

---

## 1.5 为什么不建议继续把所有内容平铺在 `docs/framework/`

当前平铺结构适合早期探索，但到你要做“版本治理”时会遇到几个问题：

1. `v1-rfc.md` 和 `artifact-graph-architecture.md` 的层级不一致  
   一个是版本文件，一个是跨版本文件，却都在同一层

2. `reference-mapping.md` 兼具研究映射和架构理由  
   容易和 decision-log 混淆

3. 后续加 `v2-*` 时会迅速平铺爆炸  
   例如：
   - `v2-rfc.md`
   - `v2-roadmap.md`
   - `v2-architecture.md`
   - `v2-decision-log.md`
   - `v2-manifesto.md`
   顶层可读性会很差

所以建议尽早转成“类型目录 + release 目录”的组合结构。

---

## 2) 版本号策略如何落地

## 2.1 建议采用“框架主版本 + 文档状态”的双轨策略

不要只靠文件名里的 `v1`。建议文档同时具备：

1. 框架版本
2. 文档状态

例如 frontmatter 可以有：

```yaml
framework_version: v1
doc_type: roadmap
doc_status: draft
release_status: active
supersedes: null
superseded_by: null
freeze_date: null
```

---

## 2.2 版本号层级建议

建议使用三层语义，但只在“release 管理”里完整使用：

- 主版本：`v1`, `v2`
- 次版本：`v1.1`, `v1.2`
- 修订版：仅用于 changelog 或 release note，不建议进入目录层

落地建议：

### 目录层只放主版本
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/`
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v2/`

### 次版本放 frontmatter 和 changelog
例如 `releases/v1/roadmap.md` 的 frontmatter：

```yaml
framework_version: v1
release_line: v1.x
current_minor: v1.2
doc_status: active
```

这样避免目录变成：
- `v1.0/`
- `v1.1/`
- `v1.2/`
- `v1.2.1/`
过度碎片化。

---

## 2.3 哪些文档跟主版本走，哪些文档跨版本维护

### 跟主版本走
这些文档应该放到 `releases/v1/` 下：
- `manifesto.md`
- `architecture.md`
- `decision-log.md`
- `roadmap.md`
- `rfc.md`
- `release-freeze.md`
- `changelog.md`

原因：它们描述的是“这一版到底承诺什么”。

### 跨版本维护
这些文档应保持稳定层：
- 核心理念
- 长期术语表
- 共用架构原则
- 跨版本决策索引

原因：否则每个版本都复制一遍，维护成本会极高。

---

## 2.4 版本演进规则建议

建议定义 3 条规则：

### 规则 A：主版本升级条件
只有在以下情况之一发生时，才升主版本：
- 核心对象模型重写
- 系统边界发生根本变化
- 人工关卡 / 自治合同发生原则性变化
- 兼容性承诺被打破

例子：
- 从“bounded-autonomous research evidence engine”变成“full research platform”可视为主版本升级

### 规则 B：次版本升级条件
以下内容升 `v1.1` / `v1.2`：
- 增加新能力但不推翻 v1 核心
- 扩展流程节点
- 新增非破坏性架构模块
- roadmap 里新增阶段，但仍服务于 v1 目标

### 规则 C：补丁修订不升目录版本
以下只更新 changelog 或文档修订号：
- 错别字
- 例子修正
- 表达澄清
- 小范围术语统一

---

## 2.5 版本状态机

建议每个 release 目录都遵循相同状态：

- `draft`
- `candidate`
- `frozen`
- `archived`

定义如下：

### draft
持续编辑中，结构不稳定

### candidate
准备冻结，允许小范围修订，不再增大范围

### frozen
该版本正文不再承载新增需求，只允许勘误

### archived
被新版本替代，只保留索引、链接和历史说明

这套状态比单纯“v1/v2”更有治理意义。

---

## 3) release freeze/archive 机制

## 3.1 freeze 的目标

freeze 不是“以后不许碰”，而是：

1. 锁定某一版本的承诺边界
2. 防止 roadmap / architecture / manifesto 相互漂移
3. 让后续讨论能基于固定基线进行

你的仓库现在最需要的其实就是这个，因为当前 `v1-rfc.md` 和 `v1-roadmap.md` 已经很具体，适合收敛成 release bundle。

---

## 3.2 推荐的 freeze 单元

建议按“release bundle”冻结，而不是单文件冻结。  
即以下文件一起 freeze：

- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/index.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/manifesto.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/architecture.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/decision-log.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/roadmap.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/rfc.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/release-freeze.md`
- `/Users/kozmosa/code/scholar-agent/docs/framework/releases/v1/changelog.md`

---

## 3.3 freeze 判定标准

一个版本可以进入 freeze，建议至少满足：

1. manifesto 已明确
   - 目标、边界、非目标稳定

2. architecture 已明确
   - 核心组件、边界、职责稳定

3. decision-log 已补齐关键取舍
   - 为什么选 REST、为什么保留双关卡、为什么 repo-first 等

4. roadmap 已映射到 release scope
   - 哪些在本版内，哪些明确不做

5. RFC 已可作为实现参考
   - API / 状态机 / 对象模型至少稳定到可执行

---

## 3.4 freeze 后允许什么改动

建议 freeze 后只允许两类改动：

### A. 勘误型
- 拼写
- 链接
- 图示错误
- 不改变语义的表达修正

### B. 补充型注记
- “已知限制”
- “后续版本迁移说明”
- 指向新版本的 superseded notice

不允许：
- 新增本版 scope
- 改动关键术语定义
- 改动承诺边界
- 改写 roadmap 使其看起来“本来就如此”

换句话说，freeze 后要保住历史真相。

---

## 3.5 archive 机制

建议 archive 分两层：

### 软归档
版本已冻结，但仍是当前主参考  
状态：`frozen`

例如刚冻结的 `v1`

### 硬归档
版本已被后继版本替代  
状态：`archived`

例如当 `v2` 成为主线后，`v1` 进入 archive

---

## 3.6 archive 的落地方式

推荐不是“移动全部文件到 archive 后原地消失”，而是：

### 方案 A：保留 release 原位 + archive 建索引
优先推荐。

- `releases/v1/` 仍保留
- `archive/index.md` 建立归档导航
- `releases/v1/index.md` 标明 `release_status: archived`

好处：
- 不破坏旧 wikilink
- MkDocs / Obsidian 路径更稳定
- 不需要全库批量改链接

### 方案 B：物理迁移到 archive/v1/
不太推荐，除非你很确定还没形成大量链接依赖。

---

## 3.7 release-freeze.md 应记录什么

每个版本应有一份 `release-freeze.md`，记录：

- freeze 日期
- freeze 范围
- 版本目标
- 关键不变项
- 明确 deferred items
- 与上一版 / 下一版关系

建议字段示意：

```yaml
framework_version: v1
release_status: frozen
freeze_date: 2026-04-04
successor_version: null
```

正文建议包含：
- 本版使命
- 本版冻结范围
- 不纳入本版的事项
- 后续迭代入口
- 相关 ADR 列表

---

## 4) 适合按单会话推进的原子任务拆法

你要求的是“单会话可推进”的拆法，所以每个任务都应该满足：

- 输入边界清楚
- 输出是一个具体文档或一个具体整理动作
- 不依赖大规模迁移
- 一次会话内可评审完成

下面给出推荐拆法，按从低风险到高风险排列。

---

## 4.1 Phase A：先定义体系，不碰内容重写

### A1. 盘点当前框架文档角色
目标：
- 给现有 8 个文档标注类型：manifesto / architecture / roadmap / decision / reference / index

产出：
- 一份映射清单

完成标准：
- 每个现有文件只有一个主角色，必要时有次角色

---

### A2. 定义目标信息架构
目标：
- 产出“未来目录树 + 每类文档职责说明”

产出：
- 一份目录树草案
- 每类文档的 3-5 条职责定义

完成标准：
- 能解释为什么 `reference-mapping` 不等于 `decision-log`

---

### A3. 定义命名规范
目标：
- 固化目录、文件、版本、ADR 命名方式

产出：
- 一份 naming policy

完成标准：
- 能指导后续新建文档，不再临时命名

---

### A4. 定义 frontmatter 元数据规范
目标：
- 统一版本、状态、替代关系、冻结状态字段

产出：
- frontmatter schema 草案

完成标准：
- manifesto / roadmap / decision-log / release-freeze 都能套用

---

## 4.2 Phase B：建立版本治理规则

### B1. 定义 release line 规则
目标：
- 说清 `v1`、`v1.x`、`v2` 怎么区分

产出：
- 版本策略说明文档

完成标准：
- 能判断一个变化是 minor 还是 major

---

### B2. 定义文档状态机
目标：
- 明确 `draft / candidate / frozen / archived`

产出：
- 文档生命周期规则

完成标准：
- 每种状态允许和禁止的变更都明确

---

### B3. 定义 freeze checklist
目标：
- 形成“什么情况下可以冻结”的清单

产出：
- freeze checklist

完成标准：
- 任何人都可按清单判断 v1 是否准备 freeze

---

### B4. 定义 archive policy
目标：
- 解决老版本是否迁移、如何保留链接、如何标记 superseded

产出：
- archive policy

完成标准：
- 不破坏旧链接的策略被明确选定

---

## 4.3 Phase C：把现有内容映射进新体系

### C1. 提炼 stable manifesto
目标：
- 从当前 `/Users/kozmosa/code/scholar-agent/docs/framework/ai-native-research-framework.md`
  中区分“跨版本不变”与“V1 特有”

产出：
- stable manifesto 提纲
- v1 manifesto 提纲

完成标准：
- 愿景与实现细节分离

---

### C2. 提炼 stable architecture vs v1 architecture
目标：
- 把工件图谱 / 容器协议中的稳定原则和 V1 特化实现拆开

产出：
- cross-version architecture 提纲
- v1 architecture 提纲

完成标准：
- 能回答“哪些架构在 V2 也成立，哪些只是 V1 实现路径”

---

### C3. 把 reference-mapping 转成 decision sources
目标：
- 从当前 `/Users/kozmosa/code/scholar-agent/docs/framework/reference-mapping.md`
  中抽出正式决策项

产出：
- ADR 候选列表，例如：
  - bounded autonomy
  - repo-first
  - artifact graph over skills market
  - REST-first API

完成标准：
- 至少得到一组可编号的 ADR 标题

---

### C4. 重建 v1 bundle 目录提纲
目标：
- 定义 `releases/v1/` 下各文件职责

产出：
- `v1/index / manifesto / architecture / decision-log / roadmap / rfc / release-freeze / changelog` 的提纲

完成标准：
- 不再让 `v1-rfc.md` 与 `v1-roadmap.md` 成为孤立文件

---

## 4.4 Phase D：面向执行的最小原子任务

如果你要按“一次会话一个明确成果”的方式推进，我建议用下面这个粒度：

1. 会话 1：现状分类  
   - 输出“当前 framework 文档角色地图”

2. 会话 2：目录树与命名策略  
   - 输出“推荐结构与命名规则”

3. 会话 3：frontmatter 规范  
   - 输出“版本/状态元数据 schema”

4. 会话 4：版本号与 release line 规则  
   - 输出“major/minor/fix 的判断规则”

5. 会话 5：freeze/archive 机制  
   - 输出“freeze checklist + archive policy”

6. 会话 6：stable manifesto 提纲  
   - 从现有 manifesto 抽稳定层

7. 会话 7：stable architecture 提纲  
   - 从现有 architecture 文档抽稳定层

8. 会话 8：ADR 候选清单  
   - 从 reference-mapping 和现有 RFC 提炼 निर्णय项

9. 会话 9：v1 release bundle 提纲  
   - 定义 v1 版本包结构

10. 会话 10：索引与链接迁移方案  
   - 只规划，不改文件；产出 wikilink 重定向策略

---

## 4.5 我最推荐的“最小闭环”任务包

如果你想先用最少 4 个会话拿到一个可执行方案，建议顺序是：

### 包 1：信息架构
- 当前文档分类
- 目标目录树
- 命名规范

### 包 2：治理规则
- 版本号策略
- 文档状态机
- freeze/archive policy

### 包 3：内容映射
- stable manifesto 提纲
- stable architecture 提纲
- ADR 候选表

### 包 4：v1 release bundle
- v1 文件清单
- 每个文件职责
- freeze checklist

这样做的好处是：在你真正改文档之前，体系已经闭环。

---

## 最后给一个简化结论

如果只保留最核心建议，我建议你这样落地：

### 推荐结构
- 稳定层：`manifesto/`、`architecture/`、`decisions/`、`roadmap/`
- 版本层：`releases/v1/`、`releases/v2/`
- 历史导航：`archive/`

### 推荐命名
- 稳定层用职责名：`core.md`、`cross-version.md`
- 版本层用固定套件名：`manifesto.md`、`architecture.md`、`decision-log.md`、`roadmap.md`、`rfc.md`

### 版本策略
- 目录只分主版本：`v1/`, `v2/`
- 次版本放 frontmatter 和 changelog：`v1.1`, `v1.2`
- 每篇文档都带 `framework_version`、`doc_status`、`release_status`

### freeze/archive
- 按 release bundle 整体冻结
- freeze 后只允许勘误和注记
- archived 版本最好原位保留，仅用状态和 archive 索引标记，不建议大迁移

### 原子任务
- 先做信息架构
- 再做版本治理
- 再做内容映射
- 最后做 v1 release bundle 设计

如果你愿意，我下一步可以继续只读帮你做一版“基于当前 8 个 framework 文档的逐文件映射表”，把每个现有文件精确归类到 manifesto / architecture / decision-log / roadmap / release bundle 中。
</task_result>
```

---

## Assistant (Plan · gpt-5.4 · 61.6s)

**当前结论**
方向现在已经足够清晰，可以进入“长期计划设计”阶段了。  
我先给你这轮的三项产出：

1. 我对项目与需求的当前理解
2. 第一版项目重定位声明
3. 第一版综合计划与路线图骨架

同时，我会直接指出一个需要马上冻结的关键收敛点。

**我对项目与需求的当前理解**
现在我理解的 `scholar-agent` 是：

1. 产品定位
   - 单用户优先的 `Agent-driven Research Dashboard`
   - 不是通用全自动研究员
   - 不是跨领域通用研究平台
   - 不是论文工厂

2. 下一版 release 的最低目标
   - 能独立完成典型、简单、定义明确的任务
   - 不频繁损坏状态或失控
   - 对用户是“可用的工具”，不是“概念样机”

3. 下一版必须优先体现的价值
   - dashboard
   - stability
   - observability

4. 下一版必须覆盖的功能面
   - 现代 Web UI dashboard
   - task tracking
   - workspace management
   - container/session SSH integration
   - artifact/result preview in UI

5. 范围收缩方式
   - 按任务类别收缩，不按学科大词扩张
   - 接受单用户、单机控制面优先
   - 接受有界自治，不拒绝 24x7 agent/subagent 作为局部能力

6. 文档治理目标
   - 用版本化文档体系冻结边界
   - manifesto 作为 requirements/expectations 最高层文档
   - framework 保持抽象层
   - architecture 与实现强绑定
   - decision log 只记录重大决策，并按 release 冻结归档

**我现在要直接指出的工程收敛点**
你已经接受了一个非常关键的判断：  
`Mode1/Mode2` 不能继续沿用当前 docs 里的完整承诺语义，必须重定义成 next-release baseline。

这一点必须被写进后续计划的最前面。  
否则项目还是会被“现有文档中的超前定义”拖回旧瓶颈。

你已经给了一个很有用的 baseline 方向：

- Mode1/Mode2 baseline 可以借 `auto-claude-code-research-in-sleep` 的 skill + prompt 体系来定义
- 但它们在 next release 中应被理解为“可执行 baseline 模式”，不是“完整研究闭环”

这意味着，下一步文档重构的第一目标，不是写更多，而是先降承诺、再重定义。

**第一版项目重定位声明**
下面这版，是我建议你后续作为 manifesto 核心开场的方向。

`scholar-agent` is not a general fully autonomous researcher. It is an agent-driven research dashboard for bounded, evidence-grounded scholarly workflows.

中文收敛版：

`scholar-agent` 不是一个面向所有领域、全天候、完全自主的通用研究员。  
它应被重新定位为一个面向单用户研究工作的、agent-driven 的研究 dashboard：围绕任务跟踪、工作区管理、证据产物、可观察执行过程和有界自治，帮助用户把典型、简单、定义明确的研究支持任务稳定地跑起来。  
在这个定位下，24x7 agent/subagent 不是项目的总体承诺，而是工作流中的局部能力；Mode1/Mode2 也不是“完整自动科研”的同义词，而是两类可收敛、可交付、可观察的任务模式 baseline。  
项目的优先级应明确为：工程真实性先于宏大叙事，系统稳定性先于能力堆叠，ready-for-use 先于理论完备。

**我建议冻结的 next-release 产品定义**
我建议把下一版产品定义成一句非常硬的表述：

下一版是一个单用户 research operator dashboard，而不是完整研究自动化平台。

这句话的重要性在于，它天然限制了范围：

1. 首先是控制面，不是全功能平台
2. 首先是任务可见性和执行边界，不是全链路自动智能
3. 首先证明“可用、稳定、可观察”，再讨论更强自治

**第一版 next-release baseline 定义**
基于你刚才的回答，我建议把 baseline 收敛成这样：

1. Mode1 baseline
   - 基于种子论文或主题描述发起 bounded discovery
   - 借鉴 `auto-claude-code-research-in-sleep` 的 research-pipeline 思路
   - 目标不是完整自主研究，而是：
     - 启动一个有边界的探索任务
     - 记录 milestone/checkpoint
     - 沉淀 artifacts
     - 让用户在 dashboard 中看到进度、资源和结果

2. Mode2 baseline
   - 基于目标论文或明确任务发起 bounded reproduction-oriented execution
   - 目标不是保证高精度 full reproduction，而是：
     - 跑通 baseline task
     - 留下结构化结果与 artifacts
     - 可在 dashboard 里观察、预览和回顾

换句话说：

- Mode1 是 bounded discovery baseline
- Mode2 是 bounded reproduction baseline

而不是当前文档里那种更重、更广的承诺版本。

**第一版 dashboard 收敛定义**
结合只读分析，我建议下一版 dashboard 的 baseline 不要定义成“大屏”，而定义成：

task-centric operator dashboard

最合理的首屏结构是：

1. 顶部健康状态
   - API / container / SSH / Claude / GPU / disk

2. 当前任务时间线
   - 你要的 milestone/checkpoint timeline
   - 这是首屏主角，不是附属模块

3. 最近完成任务
   - 轻列表

4. 最近 artifacts
   - tables / figures / reports
   - 点击预览 modal

5. 当前资源占用
   - gpu / cpu / mem / disk
   - 先做 workspace 级 snapshot，不做复杂预测

6. token usage overview
   - rpm / rph / rpd / tpm / tph / tpd
   - 但这里我先提醒一个风险：
   - 如果当前系统没有稳定 token telemetry 源，就不能把它定义成 next-release hard requirement
   - 只能写成“若运行时可稳定提供，则纳入首屏；否则延期”

这里我要明确指出一个工程约束：  
你提出的 token usage overview 很合理，但以当前代码状态看，它很可能不是 next release 里最便宜、最稳的功能。  
如果后面你坚持把它列为 must-have，我会建议同步下调别的项目，否则 scope 会再次膨胀。

**第一版文档体系草案**
我建议未来文档体系按下面四层组织：

1. 顶层定位层
   - manifesto
   - 最高层 requirements / expectations / non-goals

2. 抽象框架层
   - framework docs
   - 解释项目功能、哲学、使用价值、边界与模式

3. 实现架构层
   - architecture docs
   - 紧贴当前 release 和工程设计
   - 解释组件、接口、约束、tradeoff

4. 发布治理层
   - roadmap
   - decision log
   - release snapshot / freeze / archive

我比较推荐的版本化方式是：

- 版本风格：`v1-20260404`
- 文档与产品版本弱绑定
- release 后冻结并归档：
  - decision log
  - release snapshot
  - architecture snapshot
  - manifesto snapshot（如果该版承诺已冻结）

**第一版长期计划骨架**
下面这版是当前最适合你的“多轮推进总计划”。

**Phase A: Repositioning**
目标：先把项目从错误叙事里拉出来

1. 定义新的项目定位
2. 写死 next-release 非目标
3. 重定义 Mode1/Mode2 baseline
4. 写死 ready-for-use 最低标准
5. 写死单用户优先、任务类别收缩、bounded autonomy

这个阶段的产物应包括：
- positioning statement
- non-goals list
- baseline mode definitions
- release-ready criteria draft

**Phase B: Documentation System Refactoring**
目标：建立可以长期推进的版本化文档体系

1. manifesto 结构
2. framework 结构
3. architecture 结构
4. decision log 规则
5. versioning / snapshot / archive 规则

这个阶段的产物应包括：
- docs information architecture
- naming/versioning policy
- document lifecycle policy
- freeze/archive policy

**Phase C: Next Release Scope Freezing**
目标：把“想做什么”压缩成“下一版必须可用什么”

1. dashboard baseline
2. task tracking baseline
3. workspace/session/container baseline
4. artifact preview baseline
5. observability baseline
6. deferred items list

这个阶段的产物应包括：
- release scope
- must-have / should-have / deferred matrix
- dashboard information architecture
- mode/task category scope

**Phase D: Architecture Convergence**
目标：把产品边界转换成实现边界

1. task model
2. workspace model
3. session/container/SSH model
4. artifact model for preview and visualization
5. telemetry/observability model
6. backend/frontend contract

这个阶段的产物应包括：
- implementation-facing architecture draft
- key tradeoff notes
- major ADR candidates

**Phase E: Atomic Session Roadmap**
目标：拆成单会话可完成任务

1. 每次会话只解决一个硬问题
2. 每次会话只产出一个可冻结的文档切片或决策
3. 每次会话都更新 roadmap / decision context

这个阶段的产物应包括：
- session-sized task list
- ordering and dependencies
- per-task done criteria

**我推荐的 atomic task 组织方式**
你让我推荐第 16 条，我现在给出明确建议：

推荐按“决策主题”为主轴拆，再映射到具体文档。

也就是：

1. 先按决策主题拆
   - 项目定位
   - non-goals
   - ready-for-use 标准
   - Mode1 baseline
   - Mode2 baseline
   - dashboard 首页 IA
   - artifact preview 规范
   - workspace/session/container 关系
   - observability 口径
   - 版本治理
   - release freeze 规则

2. 再把每个主题落到文档
   - manifesto / framework / architecture / roadmap / decision log

为什么推荐这样：
- 只按文件拆，容易变成“写文档”而不是“解决问题”
- 只按 milestone 拆，单次会话常常太大
- 决策主题拆法最能保证每轮都在收敛项目本身

**我建议的首批 10 个原子任务**
这是我认为最适合作为后续几轮会话起点的任务序列。

1. 定义项目新定位与一句话声明
2. 定义 next-release ready-for-use 标准
3. 定义 Non-Goals
4. 定义缩减版 Mode1 baseline
5. 定义缩减版 Mode2 baseline
6. 定义 dashboard 首屏信息架构
7. 定义 artifact preview 范围与格式
8. 定义 workspace / session / container 三者关系
9. 定义版本体系与 release freeze 规则
10. 定义 next-release must-have / deferred matrix

这 10 个主题，每一个都可以在单次会话内完成一轮收敛。

**这轮我对你的两个建议**
1. 不要再把“Mode1/Mode2 现有描述”直接当作下一版 requirement
   - 它们应该被视为旧蓝图，需要重写成 baseline spec

2. 先不要把 token telemetry 直接列成 must-have
   - 先列为“候选要求”
   - 等我们做 observability 决策时再冻结
   - 否则会很可能拖慢整个 release

**下一步我建议怎么继续**
下一轮我们最合适做的是以下四件事中的一件或两件：

1. 直接开始定义 `manifesto` 的目录与章节职责
2. 直接开始写“项目重定位声明 + Non-Goals + ready-for-use 标准”的规划稿
3. 直接开始重定义 `Mode1/Mode2 baseline`
4. 直接开始定义 dashboard 首屏 IA 和 must-have/deferred matrix

我建议下一轮优先做：

1. `项目重定位声明 + Non-Goals + ready-for-use 标准`
2. `Mode1/Mode2 baseline`

因为这两步会决定后面所有文档和 roadmap 的边界。

如果你愿意，我下一条就进入这两个主题，先给你一版：
- `Manifesto` 核心章节草案
- `Mode1/Mode2 baseline spec` 规划稿  
仍然保持只读，不改文件。

---

## User

start writing and refining

---

## Assistant (Build · gpt-5.4 · 17.5s)

_Thinking:_

**Preparing to create a work log**

I need to start by editing and creating a work log since the user wants to write and refine a multi-step process. First things first, I should check if today’s work log exists. If not, I may not need to worry about it yet. It would help to read the project documentation before diving into substantial work. I’m also considering where to store planning documents for the long-term, possibly under docs/LLM-Working. I think it’s clear I need to build a comprehensive plan step by step.

**Drafting a roadmap and manifesto**

I need to think about producing an initial draft of the manifesto or roadmap, perhaps under LLM-Working or the framework. Since this work isn't complete in our current chat, I should be ready to exchange decisions, suggestions, and develop a comprehensive plan. It might make the most sense to create a versioned planning document in docs/LLM-Working and draft the manifesto in the framework. First, I'll inspect the current directory structure to see how docs/LLM-Working is organized.

先落地这次长期工作的骨架：创建今日 worklog，并起草一组可持续迭代的规划文档，优先把“项目重定位、文档体系、next release 路线图”写成可继续协作的基线。

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "创建今日 worklog 并记录本次规划批次",
      "priority": "high",
      "status": "in_progress"
    },
    {
      "content": "梳理 LLM-Working 现有规划文档结构与命名习惯",
      "priority": "medium",
      "status": "pending"
    },
    {
      "content": "起草项目重定位与 manifesto 基线文档",
      "priority": "high",
      "status": "pending"
    },
    {
      "content": "起草 next-release 路线图与原子任务拆解文档",
      "priority": "high",
      "status": "pending"
    },
    {
      "content": "必要时补 framework 入口说明以链接新规划文档",
      "priority": "medium",
      "status": "pending"
    },
    {
      "content": "更新 worklog 记录本轮完成内容与验证结果",
      "priority": "high",
      "status": "pending"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "创建今日 worklog 并记录本次规划批次",
    "priority": "high",
    "status": "in_progress"
  },
  {
    "content": "梳理 LLM-Working 现有规划文档结构与命名习惯",
    "priority": "medium",
    "status": "pending"
  },
  {
    "content": "起草项目重定位与 manifesto 基线文档",
    "priority": "high",
    "status": "pending"
  },
  {
    "content": "起草 next-release 路线图与原子任务拆解文档",
    "priority": "high",
    "status": "pending"
  },
  {
    "content": "必要时补 framework 入口说明以链接新规划文档",
    "priority": "medium",
    "status": "pending"
  },
  {
    "content": "更新 worklog 记录本轮完成内容与验证结果",
    "priority": "high",
    "status": "pending"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 9.5s)

先看 `docs/LLM-Working/` 现有结构和近两天工作日志风格，再开始写新文档，尽量沿用仓库已有模式。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/LLM-Working",
  "limit": 200,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/LLM-Working</path>
<type>directory</type>
<entries>
p1-ssh-executor-smoke-checklist.md
p2-mineru-implementation-plan.md
p2-mineru-smoke-checklist.md
p3-artifact-state-store-impl.md
p3-artifact-state-store-implementation-plan.md
p4-fastapi-service-auth-impl.md
p4-fastapi-service-auth-implementation-plan.md
p5-human-gate-webhook-impl.md
p5-human-gate-webhook-implementation-plan.md
p6-sse-streaming-impl.md
p6-sse-streaming-implementation-plan.md
worklog/

(12 entries)
</entries>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-03-16.md",
  "limit": 220,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-03-16.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - 2026-03-16 工作日志
4: tags:
5:   - llm-working
6:   - worklog
7:   - daily-log
8: source_repo: scholar-agent
9: source_path: /home/xuyang/code/scholar-agent
10: last_local_commit: d9ea76f
11: ---
12: # 2026-03-16 工作日志
13: 
14: ## 日志记录
15: 
16: - 2026-03-16 00:05 `planning`：核对 `[[framework/v1-rfc]]`、`[[framework/v1-roadmap]]`、`PROJECT_BASIS.md`、当前 `src/ainrf/` 模块结构和测试基线，收敛 P3 的默认技术路线为 “Pydantic v2 + 本地 read model StateStore”。
17: - 2026-03-16 00:12 `docs-planning`：新增 `docs/LLM-Working/p3-artifact-state-store-implementation-plan.md` 并在 roadmap 的 P3 段落补实现入口，固定后续代码切片与 `Impl` 文档索引。
18: - 2026-03-16 00:24 `implementation`：新增 `src/ainrf/artifacts/` 包与 `tests/test_artifacts_models.py`，落地一等工件 Pydantic models、生命周期枚举、声明式状态机与 `InvalidTransitionError`。
19: - 2026-03-16 00:35 `implementation`：新增 `src/ainrf/state/` 包与 `tests/test_state_store.py`，实现 `.ainrf/` 本地 JSON read model、artifact 关系索引、task checkpoint/resume 与 resumable task scan。
20: - 2026-03-16 00:39 `validation`：执行 `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_artifacts_models.py tests/test_state_store.py`、`UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src/ainrf/artifacts src/ainrf/state tests/test_artifacts_models.py tests/test_state_store.py`、`UV_CACHE_DIR=/tmp/uv-cache uv run ty check src/ainrf/artifacts src/ainrf/state tests/test_artifacts_models.py tests/test_state_store.py`，确认 P3 新增模块的定向测试、lint 与类型检查通过。
21: - 2026-03-16 00:43 `validation`：执行 `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`、`UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`、`UV_CACHE_DIR=/tmp/uv-cache uv run ty check`，确认 P3 与现有 P0-P2 代码集成后全量检查通过。
22: - 2026-03-16 00:46 `docs-impl`：新增 `docs/LLM-Working/p3-artifact-state-store-impl.md`，记录 P3 最终接口、目录布局、验证结果、deferred 项与建议原子提交切片，并在规划文档中补实现结果 backlink。
23: - 2026-03-16 00:55 `commit-prep`：整理当前未提交文档，准备以单个 `docs` 提交纳入 `PROJECT_BASIS.md`、仓库约束更新、两篇项目调研补充、框架索引修订与 P3 规划/实现文档。
24: - 2026-03-16 01:02 `commit-prep`：整理剩余 P3 代码改动，准备以单个 `feat` 提交纳入 `ainrf.artifacts`、`ainrf.state` 与对应测试。
25: - 2026-03-16 11:05 `changelog`：完成 worklog 规则调整，统一把仓库级约束改成“每个已完成的修改计划 / 工作批次追加一条 changelog”，并同步修订 P3 规划文档中的旧约束描述；`rg` 回扫确认旧规则只残留在历史 worklog 示例中，按“future only”约定不回写；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。
26: - 2026-03-16 10:18 `docs-planning`：新增 `docs/LLM-Working/p4-fastapi-service-auth-implementation-plan.md`，并在 `[[framework/v1-roadmap]]` 的 P4 段落补实现入口，固定 P4 的 API 路由范围、daemon 目标与后续 `Impl` 文档命名。
27: - 2026-03-16 10:32 `implementation`：新增 `src/ainrf/api/` 与 `src/ainrf/server.py`，把 `ainrf serve` 从 stub 升级为真实 FastAPI/uvicorn 服务入口，落地 API Key 认证、任务创建/列表/详情/取消/artifact 查询、RFC 兼容的 approve/reject/events 占位路由，以及“服务健康 + 可选容器探测”的 `/health`；同步扩展 `JsonStateStore` 支持 `save_task()` 与任务列表查询。
28: - 2026-03-16 10:44 `validation`：新增 `tests/test_api_auth.py`、`tests/test_api_tasks.py`、`tests/test_api_health.py`、`tests/test_server.py` 并更新 `tests/test_cli.py`、`tests/test_state_store.py`，覆盖服务鉴权、任务路由、健康检查、daemon 进程管理和状态层新接口；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`、`UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`、`UV_CACHE_DIR=/tmp/uv-cache uv run ty check` 全部通过，其中 `pytest tests/` 为 63 passed。
29: - 2026-03-16 10:48 `docs-impl`：新增 `docs/LLM-Working/p4-fastapi-service-auth-impl.md`，记录 P4 最终接口、目录结构、关键取舍、验证结果与 deferred 项，并把 daemon 在当前 sandbox 下无法做真实 socket smoke 的限制显式写入实现文档。
30: - 2026-03-16 11:32 `docs-planning`：新增 `docs/LLM-Working/p5-human-gate-webhook-implementation-plan.md`，并同步修订 `[[framework/v1-roadmap]]` 的 P5 段落，使其与 RFC 和当前 P4 task-scoped 审批接口保持一致，明确 `intake` / `plan_approval` 命名、待审批发现方式和 `Impl` 文档入口。
31: - 2026-03-16 11:48 `implementation`：新增 `src/ainrf/gates/` 包，把 P4 的 approve/reject 占位路由升级为真实 gate lifecycle；扩展 `HumanGate` / `GateRecord` 字段、为 `JsonStateStore.save_task()` 增加 `webhook_secret` sanitize，并在 `POST /tasks` 接入 intake gate、yolo auto-approve、signed webhook 和 reminder sweep。
32: - 2026-03-16 11:56 `validation`：重写 `tests/test_api_tasks.py` 并更新 `tests/test_state_store.py`、`tests/test_artifacts_models.py`，覆盖 intake gate 创建、active gate 查询、审批/拒绝流、连续 plan reject fail-fast、yolo bypass 和 reminder 单次发送；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/test_api_tasks.py tests/test_state_store.py tests/test_artifacts_models.py`、`UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`、`UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`、`UV_CACHE_DIR=/tmp/uv-cache uv run ty check` 全部通过，其中 `pytest tests/` 为 71 passed。
33: - 2026-03-16 12:02 `docs-impl`：使用 `write-obsidian-project-docs` 的单项目笔记约定新增 `docs/LLM-Working/p5-human-gate-webhook-impl.md`，记录 P5 的最终接口、关键取舍、验证结果与 deferred 项，并与规划笔记及 roadmap 建立闭环链接。
34: - 2026-03-16 14:47 `changelog`：完成 P6 SSE Streaming 落地，新增 `ainrf.events` 作为 task-scoped JSONL 事件层，把 `POST /tasks`、`approve/reject`、`cancel` 与 gate reminder sweep 接到 `artifact.*` / `gate.*` / `task.*` 事件发射，并将 `/tasks/{id}/events` 从 `501` 升级为支持历史回放、`Last-Event-ID`、`?types=` 过滤和非终态轮询跟随的 SSE 端点；同步新增 P6 planning/impl 笔记、更新 roadmap 回链，并补充 `tests/test_api_events.py` 与 `tests/test_events_store.py` 及现有 task API 事件断言；执行 `.venv/bin/python -m pytest tests -q`、`.venv/bin/python -m ruff check src tests`、`.venv/bin/python -m ty check` 全部通过。

(End of file - total 34 lines)
</content>
```

**Tool: glob**

**Input:**
```json
{
  "path": "/Users/kozmosa/code/scholar-agent/docs/LLM-Working",
  "pattern": "**/*.md"
}
```

**Output:**
```
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-03-16.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p6-sse-streaming-impl.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p6-sse-streaming-implementation-plan.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p5-human-gate-webhook-implementation-plan.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p5-human-gate-webhook-impl.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p3-artifact-state-store-implementation-plan.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p4-fastapi-service-auth-implementation-plan.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p4-fastapi-service-auth-impl.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p2-mineru-smoke-checklist.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p3-artifact-state-store-impl.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-03-15.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p2-mineru-implementation-plan.md
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p1-ssh-executor-smoke-checklist.md
```

---

## Assistant (Build · gpt-5.4 · 9.4s)

_Thinking:_

**Creating and Inspecting Files**

I need to create some files and make sure to inspect the implementation plan style. I think it might help to look at one of the planning files to see how it's structured. By reading through that file, I might get some inspiration or clarity on how to proceed. It's all about getting the format right so that everything aligns with what I'm trying to accomplish! Let's get started!

我已经确认 `LLM-Working` 里已有“implementation-plan / impl / worklog”三类文档习惯。下一步直接按这个体系新增两份规划文档：一份做项目重定位与版本化文档体系基线，一份做 next-release 路线图与原子任务拆解。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p4-fastapi-service-auth-implementation-plan.md",
  "limit": 260,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p4-fastapi-service-auth-implementation-plan.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - P4 FastAPI Service Auth Implementation Plan
4:   - P4 FastAPI 服务与认证规划
5: tags:
6:   - ainrf
7:   - api
8:   - fastapi
9:   - auth
10:   - implementation-plan
11: source_repo: scholar-agent
12: source_path: /home/xuyang/code/scholar-agent
13: last_local_commit: 7975cfa
14: ---
15: # P4 FastAPI Service & Auth 实施规划
16: 
17: > [!abstract]
18: > 基于 [[framework/v1-rfc]]、[[framework/v1-roadmap]] 与当前仓库已经落地的 `execution`、`parsing`、`artifacts`、`state` 模块，本规划将 P4 收敛为“state-backed FastAPI 服务骨架 + API Key 认证 + OpenAPI + CLI daemon 启动”。目标是在不提前实现 TaskEngine、Human Gate 真逻辑和 SSE publisher 的前提下，先交付可运行、可测试、可扩展的对外 API 层。
19: 
20: ## 规划结论
21: 
22: - P4 按 RFC 的任务路由骨架落地，而不是只做 roadmap 最小端点；`approve` / `reject` / `events` 先挂占位路由，为 P5/P6 保留兼容接口。
23: - 认证采用 API Key 哈希校验，统一读取 `X-API-Key`，只接受 SHA-256 哈希配置，不在本地配置文件持久化明文 key。
24: - `ainrf serve` 从 stub 升级为真实服务入口；`--daemon` 在 P4 必须是真后台化而不是保留占位。
25: - 任务 API 直接复用 P3 的 `TaskRecord` / `JsonStateStore` 作为 read model，避免再造一套平行持久化层。
26: - P4 完成后同步新增 `[[LLM-Working/p4-fastapi-service-auth-impl]]`，记录最终接口、验证结果和 deferred 项。
27: 
28: ## 现状与约束
29: 
30: - 已有依赖：`pyproject.toml` 已声明 `fastapi`、`uvicorn`、`httpx`、`pydantic`，不需要再补基础服务依赖。
31: - 已有状态层：`src/ainrf/state/` 已提供 task checkpoint / load / resume，但还缺少面向 API 的 `save_task` 与任务列表查询接口。
32: - 已有执行器：`src/ainrf/execution/` 已能提供 `SSHExecutor.ping()`，因此 `GET /health` 可以实现“服务健康 + 可选容器探测”。
33: - 当前 CLI 仍是 P0 stub，`tests/test_cli.py` 也只覆盖帮助信息和 stub 输出；P4 必须同步把 CLI 验收升级到真实 server 启动和 daemon 行为。
34: - 长期约束要求新增 Python 代码具备严格类型标注，并通过 `pytest`、`ruff check`、`ty check`；同时需要向 `docs/LLM-Working/worklog/2026-03-16.md` 追加完成批次记录。
35: 
36: ## 范围界定
37: 
38: ### In Scope
39: 
40: - `src/ainrf/api/` 模块骨架：应用工厂、配置解析、认证中间件、路由、schema
41: - API Key 认证：`X-API-Key` header、SHA-256 哈希比对、多 key 支持
42: - 任务相关路由：`POST /tasks`、`GET /tasks`、`GET /tasks/{id}`、`POST /tasks/{id}/cancel`、`GET /tasks/{id}/artifacts`
43: - RFC 兼容占位路由：`POST /tasks/{id}/approve`、`POST /tasks/{id}/reject`、`GET /tasks/{id}/events`
44: - `GET /health`：服务健康，且在配置容器时附加可选 SSH 健康探测
45: - `ainrf serve` 前台与 daemon 模式
46: - OpenAPI schema 自动生成与 request/response 示例
47: 
48: ### Out of Scope
49: 
50: - TaskEngine 真正调度、自动恢复执行、任务队列
51: - Human Gate 生命周期管理和 webhook 发送
52: - SSE 事件发布与事件持久化
53: - `/gates/*` 资源形状；P4/P5 统一按 RFC 的 task-scoped 审批端点
54: - `/v1` 版本前缀；当前阶段保留根路径
55: 
56: ## 建议模块设计
57: 
58: ### 目录
59: 
60: - `src/ainrf/api/__init__.py`
61: - `src/ainrf/api/app.py`
62: - `src/ainrf/api/config.py`
63: - `src/ainrf/api/dependencies.py`
64: - `src/ainrf/api/middleware.py`
65: - `src/ainrf/api/routes/health.py`
66: - `src/ainrf/api/routes/tasks.py`
67: - `src/ainrf/api/schemas.py`
68: - `tests/test_api_auth.py`
69: - `tests/test_api_tasks.py`
70: - `tests/test_api_health.py`
71: 
72: ### 核心接口
73: 
74: - `create_app(config: ApiConfig | None = None) -> FastAPI`
75: - `ApiConfig.from_env(...)`
76: - `ApiStateStore` 继续复用 `JsonStateStore`
77: - `run_server(host, port, state_root, api_config)`
78: - `run_server_daemon(host, port, pid_file, log_file, state_root, api_config)`
79: 
80: ## 实现顺序
81: 
82: ### Slice 1：文档与服务骨架
83: 
84: - 新增 P4 规划笔记并在 roadmap 中补链接。
85: - 建立 `src/ainrf/api/` 包、应用工厂和健康检查骨架。
86: - 先让 `/health` 与 `/openapi.json` 可访问，再把 auth middleware 接入其余路由。
87: 
88: ### Slice 2：认证与任务 schema
89: 
90: - 实现 API Key 哈希配置解析和中间件。
91: - 补 RFC 提交体 schema、任务摘要/详情 schema、错误返回 shape。
92: - 增加 `JsonStateStore.save_task()` 和 `list_tasks()`。
93: 
94: ### Slice 3：任务端点
95: 
96: - 落地 `POST /tasks`、`GET /tasks`、`GET /tasks/{id}`、`POST /tasks/{id}/cancel`、`GET /tasks/{id}/artifacts`。
97: - 把 `approve` / `reject` / `events` 作为兼容占位路由挂上，统一返回 `501`。
98: - 为 OpenAPI 补示例和状态码说明。
99: 
100: ### Slice 4：CLI daemon 与文档收口
101: 
102: - 把 `ainrf serve` 切到 uvicorn 真实启动。
103: - 实现 pid/log 文件写入、重复启动保护、健康探测轮询。
104: - 新增 `Impl` 笔记和当日 worklog 记录。
105: 
106: ## 验收与验证
107: 
108: - 无 API Key 访问受保护端点返回 `401`
109: - 错误 API Key 返回 `401`
110: - 正确 API Key + `POST /tasks` 创建成功并写入 `.ainrf/tasks/`
111: - `GET /tasks?status=` 能按任务状态过滤
112: - `GET /tasks/{id}/artifacts` 能返回关联工件列表
113: - `POST /tasks/{id}/cancel` 能更新非终态任务并拒绝取消终态任务
114: - `GET /health` 在无容器配置时返回 `status=ok`；有容器配置时可返回容器健康详情或降级状态
115: - `ainrf serve --daemon` 能拉起后台进程并通过 `/health` 探测成功
116: - 最终执行：
117:   - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
118:   - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
119:   - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`
120: 
121: ## 建议原子提交
122: 
123: - `docs: plan p4 fastapi service implementation`
124: - `feat: add fastapi app skeleton and api-key auth`
125: - `feat: add task creation and query api`
126: - `feat: add task artifact and cancel endpoints`
127: - `feat: add daemon serve mode and api stubs`
128: - `docs: add p4 fastapi service auth impl note`
129: 
130: ## 关联笔记
131: 
132: - [[framework/v1-rfc]]
133: - [[framework/v1-roadmap]]
134: - [[LLM-Working/p3-artifact-state-store-implementation-plan]]
135: - [[LLM-Working/p3-artifact-state-store-impl]]
136: - [[LLM-Working/p4-fastapi-service-auth-impl]]

(End of file - total 136 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p6-sse-streaming-implementation-plan.md",
  "limit": 260,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/LLM-Working/p6-sse-streaming-implementation-plan.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - P6 SSE Streaming Implementation Plan
4:   - P6 SSE 流式事件规划
5: tags:
6:   - ainrf
7:   - events
8:   - sse
9:   - implementation-plan
10: source_repo: scholar-agent
11: source_path: /home/xuyang/code/scholar-agent
12: last_local_commit: workspace aggregate
13: ---
14: # P6 SSE Streaming 实施规划
15: 
16: > [!abstract]
17: > 基于 [[framework/v1-rfc]]、[[framework/v1-roadmap]] 与当前仓库已经落地的 `api`、`gates`、`state` 模块，本规划将 P6 收敛为“task-scoped 事件持久化 + SSE 历史回放/跟随 + 现有控制面状态变化接线”。目标是在不提前实现 P7 TaskEngine、实验流和 agent 日志流的前提下，先把 P4/P5 已经存在的任务、关卡和 artifact 变化转换成可回放、可过滤、可断点恢复的事件流。
18: 
19: ## 规划结论
20: 
21: - P6 新增独立的 `ainrf.events` 运行时模块，承载事件模型、JSONL 持久化和查询逻辑，而不是把事件文件读写直接塞进 FastAPI 路由。
22: - SSE 继续沿用 P4 留下的 task-scoped 形状：`GET /tasks/{id}/events`，不引入 `/events/*` 或 WebSocket 新接口。
23: - 事件命名采用“RFC 的 task 阶段语义 + 当前仓库 gate 命名习惯”的折中方案：保留 `task.stage_changed`，并将 roadmap 中的 `gate.pending` 收敛为现有代码已经使用的 `gate.waiting`。
24: - 为遵守“避免过早抽象”的仓库约束，P6 默认采用“append-only JSONL + SSE 轮询跟随”的简单实现，不引入 broker、内存 fan-out 或额外第三方 SSE 依赖。
25: - P6 完成后同步新增 `[[LLM-Working/p6-sse-streaming-impl]]`，记录最终接口、验证结果、deferred 项与文档回链。
26: 
27: ## 现状与约束
28: 
29: - 当前 API 兼容面已经固定：`/tasks/{id}/events` 在 P4 挂载、P5 保持占位，因此 P6 只需要接管现有路由，不应改动 URL 形状。
30: - 当前仓库已真实发生的状态变化集中在 `POST /tasks`、`approve/reject`、`cancel` 和 gate reminder sweep；不存在 TaskEngine、experiment lifecycle 或 agent log stream，因此这些事件不能靠伪造补齐。
31: - `HumanGateManager` 已经集中管理 gate 生命周期，适合作为 gate-related 事件的统一发射点；取消任务仍由 tasks 路由本地处理，因此 task cancel 事件在路由中发射。
32: - 长期约束要求新增 Python 代码具备严格类型标注，并通过 `pytest`、`ruff check`、`ty check`；同时执行实际修改时要同步追加 `docs/LLM-Working/worklog/2026-03-16.md`。
33: 
34: ## 范围界定
35: 
36: ### In Scope
37: 
38: - `ainrf.events` 包：事件模型、JSONL 事件存储、事件服务
39: - `GET /tasks/{id}/events` 的真实 SSE 回放/跟随实现
40: - `Last-Event-ID` 断点恢复、`?types=` 过滤、keepalive 保活
41: - 对现有 task/gate/artifact 状态变化的事件发射接线
42: - 覆盖事件存储、SSE 回放、过滤、断点恢复与 live follow 的测试
43: - `Impl` 笔记、roadmap 回链和当日 worklog
44: 
45: ### Out of Scope
46: 
47: - P7 TaskEngine 的进度事件、执行日志和真正的 `task.started`
48: - P8/P9 的 `experiment.*` 事件实际发射
49: - WebSocket、外部消息队列或内存 pub/sub fan-out
50: - 对 P6 之前旧任务反推补写历史事件
51: 
52: ## 建议模块设计
53: 
54: ### 目录
55: 
56: - `src/ainrf/events/__init__.py`
57: - `src/ainrf/events/models.py`
58: - `src/ainrf/events/store.py`
59: - `src/ainrf/events/service.py`
60: - `src/ainrf/api/routes/tasks.py`
61: - `src/ainrf/gates/manager.py`
62: - `tests/test_events_store.py`
63: - `tests/test_api_events.py`
64: 
65: ### 核心接口
66: 
67: - `TaskEvent`
68: - `TaskEventCategory`
69: - `JsonlTaskEventStore.append_event(...)`
70: - `JsonlTaskEventStore.list_events(...)`
71: - `TaskEventService.publish(...)`
72: - `GET /tasks/{id}/events?types=task,gate`
73: 
74: ## 实现顺序
75: 
76: ### Slice 1：事件层
77: 
78: - 新增事件模型与 `.ainrf/events/{task_id}.jsonl` 持久化。
79: - 把事件服务注入 FastAPI app state，供路由和 gate manager 共享。
80: 
81: ### Slice 2：控制面事件发射
82: 
83: - 在 `HumanGateManager` 接入 trigger/resolve/reminder 事件。
84: - 在 `POST /tasks/{id}/cancel` 接入 gate cancel 与 task cancel 事件。
85: 
86: ### Slice 3：SSE 路由
87: 
88: - 把 `/tasks/{id}/events` 从 `501` 升级为真实 `text/event-stream`。
89: - 落地历史回放、轮询跟随、keepalive、终态自动关闭和 `Last-Event-ID`。
90: 
91: ### Slice 4：测试与文档收口
92: 
93: - 补事件存储和 SSE API 测试。
94: - 新增 `Impl` 笔记、roadmap 回链和当日 worklog 记录。
95: 
96: ## 验收与验证
97: 
98: - `POST /tasks` 创建 waiting intake gate 后，事件日志包含 `artifact.created`、`gate.waiting`、`task.stage_changed`
99: - yolo 模式下创建任务时，事件日志包含 `artifact.created`、`gate.resolved`、`task.stage_changed`
100: - `POST /tasks/{id}/cancel` 能发出 gate cancel 相关事件和 `task.cancelled`
101: - `GET /tasks/{id}/events` 对终态任务能完整回放历史事件并自动结束连接
102: - `Last-Event-ID` 只回放断点之后的事件，`?types=gate` 只返回 `gate.*`
103: - 非终态任务在连接建立后新增事件时，SSE 能在轮询窗口内推送到客户端
104: - 最终执行：
105:   - `UV_CACHE_DIR=/tmp/uv-cache uv run pytest tests/`
106:   - `UV_CACHE_DIR=/tmp/uv-cache uv run ruff check src tests`
107:   - `UV_CACHE_DIR=/tmp/uv-cache uv run ty check`
108: 
109: ## 关联笔记
110: 
111: - [[framework/v1-rfc]]
112: - [[framework/v1-roadmap]]
113: - [[LLM-Working/p5-human-gate-webhook-implementation-plan]]
114: - [[LLM-Working/p5-human-gate-webhook-impl]]
115: - [[LLM-Working/p6-sse-streaming-impl]]

(End of file - total 115 lines)
</content>
```

---

## Assistant (Build · gpt-5.4 · 79.9s)

开始写文档。我会先新增两份 `LLM-Working` 规划文档和今天的 worklog，再视需要补 framework 入口的跳转说明。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md\n+---\n+aliases:\n+  - 2026-04-04 工作日志\n+tags:\n+  - llm-working\n+  - worklog\n+  - daily-log\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# 2026-04-04 工作日志\n+\n+## 日志记录\n+\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/project-realignment-manifesto-plan.md\n+---\n+aliases:\n+  - Project Realignment Manifesto Plan\n+  - 项目重定位与 manifesto 规划\n+tags:\n+  - scholar-agent\n+  - manifesto\n+  - requirements\n+  - expectations\n+  - implementation-plan\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# 项目重定位与 Manifesto 规划\n+\n+> [!abstract]\n+> 本规划用于把 `scholar-agent` 从“泛化的全自动科研叙事”收敛为“单用户优先、agent-driven、evidence-grounded 的 research dashboard”。目标不是一次性写完所有新文档，而是先固定新的项目定位、文档职责边界、版本治理规则，以及 next release 需要遵守的 requirements / expectations 基线。\n+\n+## 规划结论\n+\n+- 项目定位从“有界自治研究系统”进一步收敛为“单用户优先的 agent-driven research dashboard”，强调 dashboard、稳定性和可观察性，而不是跨领域通用自动研究员。\n+- `manifesto` 应成为 requirements / expectations 的最高层文档，优先负责项目定位、适用边界、Non-Goals、ready-for-use 标准和 release 哲学。\n+- `framework` 文档保持抽象层职责：解释项目功能、哲学、边界、为什么有用，以及 Mode 1 / Mode 2 的基线含义；不再直接把未来态实现承诺写成当前版本要求。\n+- `architecture` 文档与实际实现强绑定，专门记录 next release 的工程边界、组件关系、接口契约和关键 tradeoff。\n+- 版本管理采用混合风格，例如 `v1-20260404`；当前阶段文档版本与产品 release 版本弱绑定，每次 release 后归档 snapshot 与 decision log。\n+\n+## 项目重新定位\n+\n+### 一句话定位\n+\n+- `scholar-agent` 不是一个跨所有领域、全天候、完全自主的通用研究员，而是一个面向单用户研究工作的、agent-driven 的 research dashboard。\n+\n+### 面向用户的定义\n+\n+- 核心用户是当前维护者本人，而不是团队协作或公共 SaaS 用户。\n+- 系统的首要价值是把典型、简单、定义明确的研究支持任务稳定地跑起来，并把进度、关卡、工件和资源使用情况放到统一 dashboard 中可见。\n+- 24x7 agent / subagent 可以作为具体工作流中的局部能力存在，但不再作为项目总叙事或总承诺。\n+\n+### 当前必须弱化的叙事\n+\n+- 跨所有领域的通用研究自动化。\n+- “general AI-driven fully autonomous 24x7 researcher” 式承诺。\n+- 用完整论文工厂、开放式自治探索或全自动写作来定义项目成功。\n+\n+### 当前必须强化的叙事\n+\n+- evidence-grounded workflow。\n+- robustness as a system。\n+- stability and ready-for-use。\n+- a simple but genuinely helpful tool rather than a fancy toy。\n+\n+## Next Release 的最低判断标准\n+\n+### Ready-for-use 的最低定义\n+\n+- 能独立完成典型、简单、定义明确的任务。\n+- 失败和状态损坏不能过于频繁。\n+- 用户能从 dashboard 直接看到当前任务进度、最近完成任务、最近工件和基础资源状态。\n+- 系统输出要以可追溯工件为中心，而不是只留在一次会话或日志里。\n+\n+### 单用户优先\n+\n+- next release 默认按单用户、本地或单机控制面设计，不提前引入多用户协作和多租户权限模型。\n+- dashboard 首先服务 operator，而不是服务审美化展示或团队运营分析。\n+\n+## Mode 1 / Mode 2 Baseline 重定义\n+\n+### 为什么必须重定义\n+\n+- 当前 `[[framework/v1-dual-mode-research-engine]]` 中的 Mode 1 / Mode 2 描述更接近蓝图和未来态承诺，不适合作为 next release 的直接 requirement。\n+- next release 必须把两种模式降到可交付 baseline，否则 roadmap 会再次失控。\n+\n+### Mode 1 Baseline\n+\n+- 建议定义为“bounded discovery baseline”，即围绕种子论文或主题描述启动一次有边界的探索任务。\n+- 默认参考 `[[projects/auto-claude-code-research-in-sleep]]` 的 skill / prompt 组织方式，但在本项目中只吸收其 research pipeline baseline，不继承“过夜全自动科研”叙事。\n+- 最小可交付重点是：任务可启动、里程碑可观察、工件可沉淀、探索边界可终止。\n+\n+### Mode 2 Baseline\n+\n+- 建议定义为“bounded reproduction baseline”，即围绕目标论文、目标表格或明确任务发起一次可观察的实现 / 复现任务。\n+- 最小可交付重点是：任务过程可跟踪、结果工件可预览、失败可归档，而不是承诺稳定达到完整高精度复现。\n+\n+## 文档体系建议\n+\n+### 文档职责分层\n+\n+- `manifesto`：最高层 requirements / expectations / Non-Goals / release philosophy。\n+- `framework`：抽象层功能、哲学、用途、模式解释和边界说明。\n+- `architecture`：与实现紧密绑定的工程设计和 tradeoff。\n+- `decision-log`：重大决策记录，按 release 冻结归档。\n+- `roadmap`：面向下一次 release 的原子任务与推进节奏。\n+\n+### 建议引入的版本化产物\n+\n+- `manifesto` snapshot。\n+- `architecture` snapshot。\n+- `decision-log` archive。\n+- `release-freeze` 或等价的 release snapshot 文档。\n+\n+## 推荐的 Manifesto 章节结构\n+\n+### 1. Positioning\n+\n+- 项目是什么。\n+- 项目不是什么。\n+- 为什么当前要收缩定位。\n+\n+### 2. Requirements and Expectations\n+\n+- 当前主要用户。\n+- next release 的 ready-for-use 标准。\n+- 允许的局部自治与不允许的整体叙事。\n+\n+### 3. Product Priorities\n+\n+- engineering > product/system > academic。\n+- dashboard、stability、observability 作为 next release 核心。\n+\n+### 4. Non-Goals\n+\n+- 跨领域通用研究。\n+- 全自动端到端研究。\n+- 论文工厂式写作主叙事。\n+- 其余明确延期项目。\n+\n+### 5. Release Philosophy\n+\n+- 通过持续开发收敛项目本质，而不是长期空转设计。\n+- 每次 release 后冻结 snapshot 和 decision log。\n+- 采用单会话可完成的原子任务推进。\n+\n+## 版本策略建议\n+\n+### 当前阶段\n+\n+- 版本风格采用混合命名：`v1-YYYYMMDD`。\n+- 在项目离开快速变化阶段前，不引入严格语义化版本作为主要命名方式。\n+\n+### 文档与产品版本关系\n+\n+- 弱绑定。\n+- `manifesto` / `framework` / `architecture` 可以共享同一套版本规则，但不要求每次完全同步升版。\n+\n+### Release 后的治理\n+\n+- 冻结并归档 decision log。\n+- 冻结并归档该 release 的 manifesto / architecture snapshot。\n+- 新周期从新的空白 decision log 文档开始。\n+\n+## 建议的单会话原子任务序列\n+\n+1. 固定项目新定位与一句话声明。\n+2. 固定 next release 的 ready-for-use 标准。\n+3. 固定 Non-Goals。\n+4. 重写 Mode 1 baseline。\n+5. 重写 Mode 2 baseline。\n+6. 固定 dashboard 首屏信息架构。\n+7. 固定 artifact preview 和资源展示边界。\n+8. 固定 workspace / session / container 关系。\n+9. 固定版本与 freeze/archive 规则。\n+10. 把上述决策映射回新版 manifesto / framework / architecture / roadmap。\n+\n+## 本规划对应的后续文档\n+\n+- 需要新增或重写 manifesto 主文档。\n+- 需要新增 next release roadmap 文档，专门承载 must-have / deferred / atomic tasks。\n+- 需要后续补一份 architecture baseline 文档，把 dashboard、task tracking、workspace management、SSH integration 和 artifact preview 的实现边界讲清。\n+\n+## 关联笔记\n+\n+- [[framework/index]]\n+- [[framework/ai-native-research-framework]]\n+- [[framework/v1-dual-mode-research-engine]]\n+- [[framework/v1-rfc]]\n+- [[framework/v1-roadmap]]\n+- [[projects/auto-claude-code-research-in-sleep]]\n+\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md\n+---\n+aliases:\n+  - Next Release Realignment Roadmap\n+  - 下一版重对齐路线图\n+tags:\n+  - scholar-agent\n+  - roadmap\n+  - dashboard\n+  - release-planning\n+  - implementation-plan\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# 下一版重对齐路线图\n+\n+> [!abstract]\n+> 本路线图用于把 `scholar-agent` 从当前瓶颈状态推进到“单用户优先、ready-for-use 的 research dashboard next release”。路线图不试图在一轮内完成全部文档或代码，而是按可在单会话完成的原子任务拆解，并将下一版的 must-have 范围压缩到 dashboard、stability、observability、workspace/session/container integration 和 artifact preview 这些真正可交付的内容上。\n+\n+## 路线图结论\n+\n+- next release 应被定义为一个 task-centric operator dashboard，而不是完整研究自动化平台。\n+- 当前文档中的 Mode 1 / Mode 2 需要重写为 bounded baseline，而不是原样继承未来态承诺。\n+- 下一版的核心优先级固定为：dashboard、stability、observability。\n+- 任何未被明确列入 must-have 的能力，都应默认进入 deferred 列表，防止 scope 再次膨胀。\n+\n+## Next Release Must-Have\n+\n+### 产品面\n+\n+- 新的现代 Web UI dashboard。\n+- task tracking。\n+- workspace management。\n+- container / session SSH integration。\n+- experiment result visualization 与 artifacts preview。\n+\n+### 体验面\n+\n+- 当前运行任务的 milestone / checkpoint timeline。\n+- 最近完成任务列表。\n+- 最近工件预览入口（tables / figures / reports）。\n+- 资源快照（GPU / CPU / memory / disk）。\n+- 单任务过程可观察，而不是只能看原始日志文件。\n+\n+### 稳定性面\n+\n+- 能稳定完成典型、简单、定义明确的任务。\n+- 失败时不频繁损坏状态。\n+- 关卡、取消、任务详情和工件查询要有一致行为。\n+\n+## Deferred by Default\n+\n+- 跨领域通用研究能力。\n+- 多用户、多租户和团队协作视图。\n+- 交互式 artifact graph 可视化。\n+- 开放式长期无人监督研究。\n+- 投稿级论文写作与 paper factory 工作流。\n+- 任何未被明确列入 must-have 的外围集成。\n+\n+## Dashboard Baseline\n+\n+### 推荐首页信息架构\n+\n+1. 顶部系统健康状态条。\n+2. 当前运行任务的 milestone / checkpoint timeline。\n+3. 最近完成任务列表。\n+4. 最近工件区：点击后用 modal preview。\n+5. 资源快照：GPU / CPU / memory / disk。\n+6. token usage overview（仅当运行时能稳定提供 telemetry 时纳入，否则延期）。\n+\n+### Artifact Preview Baseline\n+\n+- tables：优先支持 CSV / Markdown 预览。\n+- reports：优先支持 Markdown 预览。\n+- figures：优先支持 SVG / PNG 预览。\n+\n+### 范围约束\n+\n+- dashboard 以 task 为主对象，不先做全局研究运营大盘。\n+- 先做单任务时间线、摘要和 preview，不做复杂图谱探索器。\n+\n+## Mode Baseline 重写目标\n+\n+### Mode 1\n+\n+- 目标：bounded discovery baseline。\n+- 典型触发方式：围绕 topic description 和 seed PDF 发起一次有边界的探索任务。\n+- 最小承诺：任务可启动、进度可见、工件可沉淀、边界可终止。\n+\n+### Mode 2\n+\n+- 目标：bounded reproduction baseline。\n+- 典型触发方式：围绕目标论文与目标结果发起一次实现 / 复现任务。\n+- 最小承诺：任务过程可跟踪、工件可预览、失败可归档。\n+\n+## 推进阶段\n+\n+### Phase A：叙事与需求对齐\n+\n+- 写死项目新定位。\n+- 写死 ready-for-use 标准。\n+- 写死 Non-Goals。\n+- 重写 Mode 1 / Mode 2 baseline 定义。\n+\n+### Phase B：文档体系收敛\n+\n+- 起草 manifesto。\n+- 起草 architecture baseline。\n+- 起草 release decision-log 规则。\n+- 固定版本与 snapshot / archive 机制。\n+\n+### Phase C：产品范围冻结\n+\n+- 固定 dashboard 首屏信息架构。\n+- 固定 task tracking / workspace / SSH / preview 的 must-have。\n+- 列出 deferred 项目。\n+\n+### Phase D：实现边界收敛\n+\n+- 固定 backend / frontend contract。\n+- 固定 workspace / session / container 关系。\n+- 固定 artifacts preview 数据形态。\n+- 固定 observability 口径。\n+\n+### Phase E：原子任务执行\n+\n+- 将上述内容拆成单会话任务。\n+- 每次会话解决一个硬边界问题，并更新 roadmap 与 decision context。\n+\n+## 推荐的原子任务拆解方法\n+\n+### 原则\n+\n+- 按“决策主题”拆，而不是按文件平均拆。\n+- 每次只完成一个可冻结的判断或一个文档切片。\n+- 完成后立即把结论回写到对应规划文档中。\n+\n+### 第一批原子任务\n+\n+1. 项目新定位声明。\n+2. ready-for-use 最低标准。\n+3. Non-Goals 清单。\n+4. Mode 1 baseline 定义。\n+5. Mode 2 baseline 定义。\n+6. dashboard 首屏 IA。\n+7. artifact preview 范围。\n+8. workspace / session / container 关系。\n+9. 版本与 release freeze 机制。\n+10. must-have / deferred matrix。\n+\n+## 当前最需要警惕的风险\n+\n+### 1. Scope Explosion\n+\n+- 同时要求 dashboard、全量 Mode 1/2、复杂 telemetry 和未来态 runtime，会重复当前瓶颈。\n+\n+### 2. 旧文档语义挟持新版本\n+\n+- 如果不先重写 Mode baseline，现有 framework 文档会继续把 next release 拉回过大承诺。\n+\n+### 3. 把“设计愿景”误写成“当前 requirement”\n+\n+- 这会直接破坏工程收敛。\n+\n+## 当前建议的推进顺序\n+\n+1. 先写 manifesto 基线。\n+2. 再写 mode baseline。\n+3. 再写 dashboard baseline。\n+4. 再写 architecture baseline。\n+5. 最后把实现任务拆成原子会话清单。\n+\n+## 关联笔记\n+\n+- [[LLM-Working/project-realignment-manifesto-plan]]\n+- [[framework/index]]\n+- [[framework/v1-dual-mode-research-engine]]\n+- [[framework/v1-rfc]]\n+- [[framework/v1-roadmap]]\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A docs/LLM-Working/worklog/2026-04-04.md
A docs/LLM-Working/project-realignment-manifesto-plan.md
A docs/LLM-Working/next-release-realignment-roadmap.md
```

---

## Assistant (Build · gpt-5.4 · 10.7s)

规划文档基线已经写出来了。下一步我补一处轻量入口链接，让 framework 主线能发现这些新规划，而不大改现有结构。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/framework/index.md\n@@\n ## 使用说明\n \n - 这组笔记是\"自有框架蓝图\"，不是对某一个开源仓库的复述；涉及参考项目的判断，均来自本仓库已有研究报告与静态证据。\n - 现阶段默认研究对象是 AI/ML research，不试图抽象到所有学术门类；写作模块只保留下游接口，不在 V1 文档里展开。\n+\n+## 当前规划入口\n+\n+- 如果当前目标是对项目做重定位、requirements / expectations 重对齐，先读 [[LLM-Working/project-realignment-manifesto-plan]]。\n+- 如果当前目标是规划 next release 的 scope、原子任务和 dashboard baseline，接着读 [[LLM-Working/next-release-realignment-roadmap]]。\n \n ## 关联笔记\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M docs/framework/index.md
```

---

## Assistant (Build · gpt-5.4 · 8.1s)

我还需要把今天 worklog 补完整，并跑一次文档构建，确认这批新增文档不会破坏站点构建。

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "创建今日 worklog 并记录本次规划批次",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "梳理 LLM-Working 现有规划文档结构与命名习惯",
      "priority": "medium",
      "status": "completed"
    },
    {
      "content": "起草项目重定位与 manifesto 基线文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "起草 next-release 路线图与原子任务拆解文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "必要时补 framework 入口说明以链接新规划文档",
      "priority": "medium",
      "status": "completed"
    },
    {
      "content": "更新 worklog 记录本轮完成内容与验证结果",
      "priority": "high",
      "status": "in_progress"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "创建今日 worklog 并记录本次规划批次",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "梳理 LLM-Working 现有规划文档结构与命名习惯",
    "priority": "medium",
    "status": "completed"
  },
  {
    "content": "起草项目重定位与 manifesto 基线文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "起草 next-release 路线图与原子任务拆解文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "必要时补 framework 入口说明以链接新规划文档",
    "priority": "medium",
    "status": "completed"
  },
  {
    "content": "更新 worklog 记录本轮完成内容与验证结果",
    "priority": "high",
    "status": "in_progress"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 8.0s)

先跑文档构建验证；如果通过，我再把验证结果写进今天的 worklog。

**Tool: bash**

**Input:**
```json
{
  "command": "UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build",
  "description": "Builds the HTML notes site",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```

[31m │  ⚠  Warning from the Material for MkDocs team[0m
[31m │[0m
[31m │[0m  MkDocs 2.0, the underlying framework of Material for MkDocs,
[31m │[0m  will introduce backward-incompatible changes, including:
[31m │[0m
[31m │  × [0mAll plugins will stop working – the plugin system has been removed
[31m │  × [0mAll theme overrides will break – the theming system has been rewritten
[31m │  × [0mNo migration path exists – existing projects cannot be upgraded
[31m │  × [0mClosed contribution model – community members can't report bugs
[31m │  × [0mCurrently unlicensed – unsuitable for production use
[31m │[0m
[31m │[0m  Our full analysis:
[31m │[0m
[31m │[0m  [4mhttps://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/[0m
[0m
INFO    -  MERMAID2  - Initialization arguments: {}
INFO    -  MERMAID2  - Using specified javascript library: assets/javascripts/vendor/mermaid-10.4.0.min.js
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /Users/kozmosa/code/scholar-agent/site
INFO    -  MERMAID2  - Found superfences config: {'custom_fences': [{'name': 'mermaid', 'class': 'mermaid', 'format': functools.partial(<function fence_mermaid at 0x101a08220>, custom=True)}]}
INFO    -  MERMAID2  - Found 'fence_mermaid_custom' function: activate custom loader for superfences
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI-Native Research Framework：有界自治研究系统蓝图': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '工件图谱架构：AI-Native Research Framework 的核心模型': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'V1：双模式有界自治研究引擎': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 RFC：有界自治研究引擎实现规格': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 Roadmap：实现路线图': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Academic Research Skills：从研究到发表的学术全流程管线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI Research SKILLs：AI 研究工程技能库': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'ArgusBot：面向 Codex 的监督式 Autoloop 控制层': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Auto-claude-code-research-in-sleep：过夜自治科研流水线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'autoresearch：自治 ML 实验迭代框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Awesome Claude Code Paper Proofreading：LaTeX 论文校对 prompt 工作流': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Code Deep Research：多阶段深度研究框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Scholar：学术研究与开发一体化个人配置系统': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Everything Claude Code：通用 Agent Harness 基线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'EvoScientist：多渠道统一控制面的自进化 AI 科学家工作台': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '学术研究 Agent 汇总研究报告': found 2 diagrams, adding scripts
INFO    -  Documentation built in 0.72 seconds

```

---

## Assistant (Build · gpt-5.4 · 10.7s)

构建通过了。我现在把这批实际改动和验证结果补进今日 worklog，形成这轮长期规划的第一条正式记录。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md\n@@\n # 2026-04-04 工作日志\n \n ## 日志记录\n \n+- 2026-04-04 15:20 `docs-planning`：完成 scholar-agent 项目重定位与 next release 重对齐的首轮规划基线，新增 `[[LLM-Working/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/next-release-realignment-roadmap]]`，把项目主叙事收敛为“单用户优先的 agent-driven research dashboard”，固定 manifesto / framework / architecture / decision-log / roadmap 的职责边界、Mode 1 / Mode 2 baseline 重写方向，以及以单会话原子任务推进的路线图；同时在 `[[framework/index]]` 增加当前规划入口，便于后续从 framework 主线进入这组长期规划文档；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M docs/LLM-Working/worklog/2026-04-04.md
```

---

## Assistant (Build · gpt-5.4 · 8.9s)

我已经完成文档起草和验证，接下来整理结果给你，并指出下一轮最应该继续收敛的两个主题。

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "创建今日 worklog 并记录本次规划批次",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "梳理 LLM-Working 现有规划文档结构与命名习惯",
      "priority": "medium",
      "status": "completed"
    },
    {
      "content": "起草项目重定位与 manifesto 基线文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "起草 next-release 路线图与原子任务拆解文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "必要时补 framework 入口说明以链接新规划文档",
      "priority": "medium",
      "status": "completed"
    },
    {
      "content": "更新 worklog 记录本轮完成内容与验证结果",
      "priority": "high",
      "status": "completed"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "创建今日 worklog 并记录本次规划批次",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "梳理 LLM-Working 现有规划文档结构与命名习惯",
    "priority": "medium",
    "status": "completed"
  },
  {
    "content": "起草项目重定位与 manifesto 基线文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "起草 next-release 路线图与原子任务拆解文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "必要时补 framework 入口说明以链接新规划文档",
    "priority": "medium",
    "status": "completed"
  },
  {
    "content": "更新 worklog 记录本轮完成内容与验证结果",
    "priority": "high",
    "status": "completed"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 30.2s)

这轮已经开始正式落地，并把长期推进的第一批骨架文档写出来了。

**本轮新增/修改**
新增了这 3 个文件：

1. `docs/LLM-Working/project-realignment-manifesto-plan.md`
2. `docs/LLM-Working/next-release-realignment-roadmap.md`
3. `docs/LLM-Working/worklog/2026-04-04.md`

修改了这 1 个文件：

4. `docs/framework/index.md`

**这轮实际写了什么**
**1. 项目重定位与 manifesto 规划**
`docs/LLM-Working/project-realignment-manifesto-plan.md`

这份文档现在固定了几个关键方向：

1. 新定位
   - `scholar-agent` 不是通用全自动研究员
   - 而是“单用户优先的 agent-driven research dashboard”

2. 叙事降温
   - 弱化跨领域通用自动科研
   - 弱化论文工厂式目标
   - 强化 evidence-grounded workflow、robustness、stability、ready-for-use

3. 文档职责边界
   - `manifesto`：requirements / expectations / non-goals / release philosophy
   - `framework`：抽象功能、哲学、用途、模式边界
   - `architecture`：紧贴实现的工程设计与 tradeoff
   - `decision-log`：重大决策，按 release 冻结归档
   - `roadmap`：面向下一版的原子任务推进计划

4. Mode baseline 重写方向
   - Mode 1 收敛为 `bounded discovery baseline`
   - Mode 2 收敛为 `bounded reproduction baseline`

5. 版本治理方向
   - 暂时采用混合风格版本号，例如 `v1-20260404`
   - release 后冻结并归档 snapshot 与 decision log

**2. 下一版重对齐路线图**
`docs/LLM-Working/next-release-realignment-roadmap.md`

这份文档现在固定了：

1. next release 的 must-have 范围
   - 新现代 Web UI dashboard
   - task tracking
   - workspace management
   - container/session SSH integration
   - experiment result visualization / artifact preview

2. next release 的 deferred 范围
   - 跨领域通用性
   - 多用户/多租户
   - artifact graph 可视化
   - 开放式长期无人监督研究
   - 投稿级 paper factory
   - 任何未明确纳入 must-have 的外围能力

3. dashboard baseline
   - 当前运行任务的 milestone/checkpoint timeline
   - 最近完成任务
   - 最近 artifacts
   - 资源快照
   - token telemetry 先保留为条件性需求，不直接写死为 must-have

4. 原子任务拆法
   - 按决策主题拆，不按文件平均拆
   - 第一批已经列出了 10 个原子任务主题

**3. framework 入口补了规划跳转**
`docs/framework/index.md`

我加了一个非常轻量的新段落 `当前规划入口`，让现有 framework 主线可以直接跳到这两份新规划文档。这样后续你从 framework 阅读链就能自然进入这轮长期重构。

**4. worklog 已按仓库规则补齐**
`docs/LLM-Working/worklog/2026-04-04.md`

已经写入这轮规划工作的正式记录，并附上文档构建验证结果。

**验证**
我执行了：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build
```

结果：通过。

**我现在的判断**
这轮最重要的成果，不是“多了两篇文档”，而是你项目的长期推进已经有了第一组被写下来的硬边界：

1. 项目从“AI scientist 叙事”收敛到“research dashboard”
2. next release 从“大而全能力”收敛到一组必须可用的控制面能力
3. 文档体系开始从平铺式 framework，转向“manifesto / roadmap / architecture / decision-log”分层思路
4. 你后续每轮会话已经可以围绕原子决策推进，而不是继续泛泛讨论

**我必须继续提醒你的一个风险**
目前仍有一个没有彻底解决的工程风险：

你说 next release 要支持 “Mode1/Mode2 described in current docs”，但我们现在只是把它们的“重写方向”写出来了，还没有把 baseline 规范真正落成明确 requirement。

这意味着当前风险依然是：

- 如果后续不立即重写 Mode 1 / Mode 2 baseline
- 现有 `framework/v1-dual-mode-research-engine.md` 仍会继续把项目往过大承诺方向拉

所以我建议下一轮不要先写 architecture，不要先写 UI 细节，而是优先做这两件事：

1. 写 `Mode 1 / Mode 2 baseline spec`
2. 写 `ready-for-use / non-goals / must-have` 的更正式 manifesto 草稿

**我建议的下一轮顺序**
按最稳的工程收敛顺序，我建议下一轮直接继续：

1. 重写 `Mode 1 baseline`
2. 重写 `Mode 2 baseline`
3. 冻结 `Non-Goals`
4. 冻结 `ready-for-use` 标准
5. 再进入 dashboard IA 和 architecture baseline

**我建议你现在给我的下一条指令**
最自然的下一步是二选一：

1. `继续写 manifesto 草稿`
2. `继续写 Mode1/Mode2 baseline spec`

我推荐先做 `Mode1/Mode2 baseline spec`。  
因为这会直接决定后面 dashboard、architecture、roadmap 的真正边界。

---

## User

continue do 2

---

## Assistant (Build · gpt-5.4 · 12.9s)

_Thinking:_

**Creating a planning doc**

I'm thinking about making a new planning document in the LLM-Working folder and crosslinking it with the two existing ones. That should help keep everything organized. Once I have that set up, I'll also build and update the work log to reflect any changes or progress. Let's get started on this! It's exciting to see things coming together.

我现在继续把 `Mode1/Mode2 baseline spec` 真正写出来，作为后续 manifesto、dashboard 和 architecture 收敛的硬边界。写完后我会补回链并重新做一次文档构建验证。

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "起草 Mode1/Mode2 baseline spec 文档",
      "priority": "high",
      "status": "in_progress"
    },
    {
      "content": "把 baseline spec 回链到现有规划文档",
      "priority": "medium",
      "status": "pending"
    },
    {
      "content": "更新今日 worklog 记录本轮 baseline 收敛",
      "priority": "high",
      "status": "pending"
    },
    {
      "content": "执行文档构建验证 baseline 文档改动",
      "priority": "high",
      "status": "pending"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "起草 Mode1/Mode2 baseline spec 文档",
    "priority": "high",
    "status": "in_progress"
  },
  {
    "content": "把 baseline spec 回链到现有规划文档",
    "priority": "medium",
    "status": "pending"
  },
  {
    "content": "更新今日 worklog 记录本轮 baseline 收敛",
    "priority": "high",
    "status": "pending"
  },
  {
    "content": "执行文档构建验证 baseline 文档改动",
    "priority": "high",
    "status": "pending"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 8.0s)

先读取刚写的两份规划文档，确保新 spec 和它们完全对齐，然后直接落文。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/LLM-Working/project-realignment-manifesto-plan.md",
  "limit": 320,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/LLM-Working/project-realignment-manifesto-plan.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - Project Realignment Manifesto Plan
4:   - 项目重定位与 manifesto 规划
5: tags:
6:   - scholar-agent
7:   - manifesto
8:   - requirements
9:   - expectations
10:   - implementation-plan
11: source_repo: scholar-agent
12: source_path: /Users/kozmosa/code/scholar-agent
13: last_local_commit: workspace aggregate
14: ---
15: # 项目重定位与 Manifesto 规划
16: 
17: > [!abstract]
18: > 本规划用于把 `scholar-agent` 从“泛化的全自动科研叙事”收敛为“单用户优先、agent-driven、evidence-grounded 的 research dashboard”。目标不是一次性写完所有新文档，而是先固定新的项目定位、文档职责边界、版本治理规则，以及 next release 需要遵守的 requirements / expectations 基线。
19: 
20: ## 规划结论
21: 
22: - 项目定位从“有界自治研究系统”进一步收敛为“单用户优先的 agent-driven research dashboard”，强调 dashboard、稳定性和可观察性，而不是跨领域通用自动研究员。
23: - `manifesto` 应成为 requirements / expectations 的最高层文档，优先负责项目定位、适用边界、Non-Goals、ready-for-use 标准和 release 哲学。
24: - `framework` 文档保持抽象层职责：解释项目功能、哲学、边界、为什么有用，以及 Mode 1 / Mode 2 的基线含义；不再直接把未来态实现承诺写成当前版本要求。
25: - `architecture` 文档与实际实现强绑定，专门记录 next release 的工程边界、组件关系、接口契约和关键 tradeoff。
26: - 版本管理采用混合风格，例如 `v1-20260404`；当前阶段文档版本与产品 release 版本弱绑定，每次 release 后归档 snapshot 与 decision log。
27: 
28: ## 项目重新定位
29: 
30: ### 一句话定位
31: 
32: - `scholar-agent` 不是一个跨所有领域、全天候、完全自主的通用研究员，而是一个面向单用户研究工作的、agent-driven 的 research dashboard。
33: 
34: ### 面向用户的定义
35: 
36: - 核心用户是当前维护者本人，而不是团队协作或公共 SaaS 用户。
37: - 系统的首要价值是把典型、简单、定义明确的研究支持任务稳定地跑起来，并把进度、关卡、工件和资源使用情况放到统一 dashboard 中可见。
38: - 24x7 agent / subagent 可以作为具体工作流中的局部能力存在，但不再作为项目总叙事或总承诺。
39: 
40: ### 当前必须弱化的叙事
41: 
42: - 跨所有领域的通用研究自动化。
43: - “general AI-driven fully autonomous 24x7 researcher” 式承诺。
44: - 用完整论文工厂、开放式自治探索或全自动写作来定义项目成功。
45: 
46: ### 当前必须强化的叙事
47: 
48: - evidence-grounded workflow。
49: - robustness as a system。
50: - stability and ready-for-use。
51: - a simple but genuinely helpful tool rather than a fancy toy。
52: 
53: ## Next Release 的最低判断标准
54: 
55: ### Ready-for-use 的最低定义
56: 
57: - 能独立完成典型、简单、定义明确的任务。
58: - 失败和状态损坏不能过于频繁。
59: - 用户能从 dashboard 直接看到当前任务进度、最近完成任务、最近工件和基础资源状态。
60: - 系统输出要以可追溯工件为中心，而不是只留在一次会话或日志里。
61: 
62: ### 单用户优先
63: 
64: - next release 默认按单用户、本地或单机控制面设计，不提前引入多用户协作和多租户权限模型。
65: - dashboard 首先服务 operator，而不是服务审美化展示或团队运营分析。
66: 
67: ## Mode 1 / Mode 2 Baseline 重定义
68: 
69: ### 为什么必须重定义
70: 
71: - 当前 `[[framework/v1-dual-mode-research-engine]]` 中的 Mode 1 / Mode 2 描述更接近蓝图和未来态承诺，不适合作为 next release 的直接 requirement。
72: - next release 必须把两种模式降到可交付 baseline，否则 roadmap 会再次失控。
73: 
74: ### Mode 1 Baseline
75: 
76: - 建议定义为“bounded discovery baseline”，即围绕种子论文或主题描述启动一次有边界的探索任务。
77: - 默认参考 `[[projects/auto-claude-code-research-in-sleep]]` 的 skill / prompt 组织方式，但在本项目中只吸收其 research pipeline baseline，不继承“过夜全自动科研”叙事。
78: - 最小可交付重点是：任务可启动、里程碑可观察、工件可沉淀、探索边界可终止。
79: 
80: ### Mode 2 Baseline
81: 
82: - 建议定义为“bounded reproduction baseline”，即围绕目标论文、目标表格或明确任务发起一次可观察的实现 / 复现任务。
83: - 最小可交付重点是：任务过程可跟踪、结果工件可预览、失败可归档，而不是承诺稳定达到完整高精度复现。
84: 
85: ## 文档体系建议
86: 
87: ### 文档职责分层
88: 
89: - `manifesto`：最高层 requirements / expectations / Non-Goals / release philosophy。
90: - `framework`：抽象层功能、哲学、用途、模式解释和边界说明。
91: - `architecture`：与实现紧密绑定的工程设计和 tradeoff。
92: - `decision-log`：重大决策记录，按 release 冻结归档。
93: - `roadmap`：面向下一次 release 的原子任务与推进节奏。
94: 
95: ### 建议引入的版本化产物
96: 
97: - `manifesto` snapshot。
98: - `architecture` snapshot。
99: - `decision-log` archive。
100: - `release-freeze` 或等价的 release snapshot 文档。
101: 
102: ## 推荐的 Manifesto 章节结构
103: 
104: ### 1. Positioning
105: 
106: - 项目是什么。
107: - 项目不是什么。
108: - 为什么当前要收缩定位。
109: 
110: ### 2. Requirements and Expectations
111: 
112: - 当前主要用户。
113: - next release 的 ready-for-use 标准。
114: - 允许的局部自治与不允许的整体叙事。
115: 
116: ### 3. Product Priorities
117: 
118: - engineering > product/system > academic。
119: - dashboard、stability、observability 作为 next release 核心。
120: 
121: ### 4. Non-Goals
122: 
123: - 跨领域通用研究。
124: - 全自动端到端研究。
125: - 论文工厂式写作主叙事。
126: - 其余明确延期项目。
127: 
128: ### 5. Release Philosophy
129: 
130: - 通过持续开发收敛项目本质，而不是长期空转设计。
131: - 每次 release 后冻结 snapshot 和 decision log。
132: - 采用单会话可完成的原子任务推进。
133: 
134: ## 版本策略建议
135: 
136: ### 当前阶段
137: 
138: - 版本风格采用混合命名：`v1-YYYYMMDD`。
139: - 在项目离开快速变化阶段前，不引入严格语义化版本作为主要命名方式。
140: 
141: ### 文档与产品版本关系
142: 
143: - 弱绑定。
144: - `manifesto` / `framework` / `architecture` 可以共享同一套版本规则，但不要求每次完全同步升版。
145: 
146: ### Release 后的治理
147: 
148: - 冻结并归档 decision log。
149: - 冻结并归档该 release 的 manifesto / architecture snapshot。
150: - 新周期从新的空白 decision log 文档开始。
151: 
152: ## 建议的单会话原子任务序列
153: 
154: 1. 固定项目新定位与一句话声明。
155: 2. 固定 next release 的 ready-for-use 标准。
156: 3. 固定 Non-Goals。
157: 4. 重写 Mode 1 baseline。
158: 5. 重写 Mode 2 baseline。
159: 6. 固定 dashboard 首屏信息架构。
160: 7. 固定 artifact preview 和资源展示边界。
161: 8. 固定 workspace / session / container 关系。
162: 9. 固定版本与 freeze/archive 规则。
163: 10. 把上述决策映射回新版 manifesto / framework / architecture / roadmap。
164: 
165: ## 本规划对应的后续文档
166: 
167: - 需要新增或重写 manifesto 主文档。
168: - 需要新增 next release roadmap 文档，专门承载 must-have / deferred / atomic tasks。
169: - 需要后续补一份 architecture baseline 文档，把 dashboard、task tracking、workspace management、SSH integration 和 artifact preview 的实现边界讲清。
170: 
171: ## 关联笔记
172: 
173: - [[framework/index]]
174: - [[framework/ai-native-research-framework]]
175: - [[framework/v1-dual-mode-research-engine]]
176: - [[framework/v1-rfc]]
177: - [[framework/v1-roadmap]]
178: - [[projects/auto-claude-code-research-in-sleep]]

(End of file - total 178 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md",
  "limit": 320,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - Next Release Realignment Roadmap
4:   - 下一版重对齐路线图
5: tags:
6:   - scholar-agent
7:   - roadmap
8:   - dashboard
9:   - release-planning
10:   - implementation-plan
11: source_repo: scholar-agent
12: source_path: /Users/kozmosa/code/scholar-agent
13: last_local_commit: workspace aggregate
14: ---
15: # 下一版重对齐路线图
16: 
17: > [!abstract]
18: > 本路线图用于把 `scholar-agent` 从当前瓶颈状态推进到“单用户优先、ready-for-use 的 research dashboard next release”。路线图不试图在一轮内完成全部文档或代码，而是按可在单会话完成的原子任务拆解，并将下一版的 must-have 范围压缩到 dashboard、stability、observability、workspace/session/container integration 和 artifact preview 这些真正可交付的内容上。
19: 
20: ## 路线图结论
21: 
22: - next release 应被定义为一个 task-centric operator dashboard，而不是完整研究自动化平台。
23: - 当前文档中的 Mode 1 / Mode 2 需要重写为 bounded baseline，而不是原样继承未来态承诺。
24: - 下一版的核心优先级固定为：dashboard、stability、observability。
25: - 任何未被明确列入 must-have 的能力，都应默认进入 deferred 列表，防止 scope 再次膨胀。
26: 
27: ## Next Release Must-Have
28: 
29: ### 产品面
30: 
31: - 新的现代 Web UI dashboard。
32: - task tracking。
33: - workspace management。
34: - container / session SSH integration。
35: - experiment result visualization 与 artifacts preview。
36: 
37: ### 体验面
38: 
39: - 当前运行任务的 milestone / checkpoint timeline。
40: - 最近完成任务列表。
41: - 最近工件预览入口（tables / figures / reports）。
42: - 资源快照（GPU / CPU / memory / disk）。
43: - 单任务过程可观察，而不是只能看原始日志文件。
44: 
45: ### 稳定性面
46: 
47: - 能稳定完成典型、简单、定义明确的任务。
48: - 失败时不频繁损坏状态。
49: - 关卡、取消、任务详情和工件查询要有一致行为。
50: 
51: ## Deferred by Default
52: 
53: - 跨领域通用研究能力。
54: - 多用户、多租户和团队协作视图。
55: - 交互式 artifact graph 可视化。
56: - 开放式长期无人监督研究。
57: - 投稿级论文写作与 paper factory 工作流。
58: - 任何未被明确列入 must-have 的外围集成。
59: 
60: ## Dashboard Baseline
61: 
62: ### 推荐首页信息架构
63: 
64: 1. 顶部系统健康状态条。
65: 2. 当前运行任务的 milestone / checkpoint timeline。
66: 3. 最近完成任务列表。
67: 4. 最近工件区：点击后用 modal preview。
68: 5. 资源快照：GPU / CPU / memory / disk。
69: 6. token usage overview（仅当运行时能稳定提供 telemetry 时纳入，否则延期）。
70: 
71: ### Artifact Preview Baseline
72: 
73: - tables：优先支持 CSV / Markdown 预览。
74: - reports：优先支持 Markdown 预览。
75: - figures：优先支持 SVG / PNG 预览。
76: 
77: ### 范围约束
78: 
79: - dashboard 以 task 为主对象，不先做全局研究运营大盘。
80: - 先做单任务时间线、摘要和 preview，不做复杂图谱探索器。
81: 
82: ## Mode Baseline 重写目标
83: 
84: ### Mode 1
85: 
86: - 目标：bounded discovery baseline。
87: - 典型触发方式：围绕 topic description 和 seed PDF 发起一次有边界的探索任务。
88: - 最小承诺：任务可启动、进度可见、工件可沉淀、边界可终止。
89: 
90: ### Mode 2
91: 
92: - 目标：bounded reproduction baseline。
93: - 典型触发方式：围绕目标论文与目标结果发起一次实现 / 复现任务。
94: - 最小承诺：任务过程可跟踪、工件可预览、失败可归档。
95: 
96: ## 推进阶段
97: 
98: ### Phase A：叙事与需求对齐
99: 
100: - 写死项目新定位。
101: - 写死 ready-for-use 标准。
102: - 写死 Non-Goals。
103: - 重写 Mode 1 / Mode 2 baseline 定义。
104: 
105: ### Phase B：文档体系收敛
106: 
107: - 起草 manifesto。
108: - 起草 architecture baseline。
109: - 起草 release decision-log 规则。
110: - 固定版本与 snapshot / archive 机制。
111: 
112: ### Phase C：产品范围冻结
113: 
114: - 固定 dashboard 首屏信息架构。
115: - 固定 task tracking / workspace / SSH / preview 的 must-have。
116: - 列出 deferred 项目。
117: 
118: ### Phase D：实现边界收敛
119: 
120: - 固定 backend / frontend contract。
121: - 固定 workspace / session / container 关系。
122: - 固定 artifacts preview 数据形态。
123: - 固定 observability 口径。
124: 
125: ### Phase E：原子任务执行
126: 
127: - 将上述内容拆成单会话任务。
128: - 每次会话解决一个硬边界问题，并更新 roadmap 与 decision context。
129: 
130: ## 推荐的原子任务拆解方法
131: 
132: ### 原则
133: 
134: - 按“决策主题”拆，而不是按文件平均拆。
135: - 每次只完成一个可冻结的判断或一个文档切片。
136: - 完成后立即把结论回写到对应规划文档中。
137: 
138: ### 第一批原子任务
139: 
140: 1. 项目新定位声明。
141: 2. ready-for-use 最低标准。
142: 3. Non-Goals 清单。
143: 4. Mode 1 baseline 定义。
144: 5. Mode 2 baseline 定义。
145: 6. dashboard 首屏 IA。
146: 7. artifact preview 范围。
147: 8. workspace / session / container 关系。
148: 9. 版本与 release freeze 机制。
149: 10. must-have / deferred matrix。
150: 
151: ## 当前最需要警惕的风险
152: 
153: ### 1. Scope Explosion
154: 
155: - 同时要求 dashboard、全量 Mode 1/2、复杂 telemetry 和未来态 runtime，会重复当前瓶颈。
156: 
157: ### 2. 旧文档语义挟持新版本
158: 
159: - 如果不先重写 Mode baseline，现有 framework 文档会继续把 next release 拉回过大承诺。
160: 
161: ### 3. 把“设计愿景”误写成“当前 requirement”
162: 
163: - 这会直接破坏工程收敛。
164: 
165: ## 当前建议的推进顺序
166: 
167: 1. 先写 manifesto 基线。
168: 2. 再写 mode baseline。
169: 3. 再写 dashboard baseline。
170: 4. 再写 architecture baseline。
171: 5. 最后把实现任务拆成原子会话清单。
172: 
173: ## 关联笔记
174: 
175: - [[LLM-Working/project-realignment-manifesto-plan]]
176: - [[framework/index]]
177: - [[framework/v1-dual-mode-research-engine]]
178: - [[framework/v1-rfc]]
179: - [[framework/v1-roadmap]]

(End of file - total 179 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/projects/auto-claude-code-research-in-sleep.md",
  "limit": 240,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/projects/auto-claude-code-research-in-sleep.md</path>
<type>file</type>
<content>1: ---
2: aliases:
3:   - Auto-claude-code-research-in-sleep
4:   - ARIS
5: tags:
6:   - research-agent
7:   - repo-study
8:   - autonomous-research
9: source_repo: Auto-claude-code-research-in-sleep
10: source_path: /home/xuyang/code/scholar-agent/ref-repos/Auto-claude-code-research-in-sleep
11: last_local_commit: c4016ec 2026-03-14 docs: warn users to set gpt-5.4 in Codex config
12: ---
13: # Auto-claude-code-research-in-sleep：过夜自治科研流水线
14: 
15: > [!abstract]
16: > 这个项目最鲜明的标签不是“技能库”，而是“把研究循环交给模型过夜跑”。它用 Claude Code 负责执行，用外部 LLM 通过 Codex MCP 承担批判式 reviewer 角色，强调跨模型协作而不是单模型自我博弈。
17: 
18: ## 项目定位
19: 
20: - 仓库主张是“Let Claude Code do research while you sleep”，重点是研究自治和长链路串联。
21: - README 定义了 3 条主工作流：`/idea-discovery`、`/auto-review-loop`、`/paper-writing`，并可组合成 `/research-pipeline`。
22: - 设计哲学是“speed × rigor”：Claude Code 执行快，Codex/GPT-5.4 负责更慢但更严谨的审查。
23: 
24: ## 仓库构成
25: 
26: - 本地 `skills/` 下有 21 个技能目录，覆盖找 idea、文献调研、novelty check、实验执行、论文写作、review loop、Feishu 通知等。
27: - 存在 `mcp-servers/minimax-chat/`，说明它并不完全绑定 OpenAI 组合，也考虑替代模型接入。
28: - `docs/` 和 `assets/` 中放了流程图、评分曲线、通知截图等展示材料，强调实际运行体验。
29: 
30: ## 核心工作流
31: 
32: ```mermaid
33: flowchart LR
34:     A[研究方向输入] --> B[/idea-discovery]
35:     B --> C[文献检索与 novelty check]
36:     C --> D[实验设计与运行]
37:     D --> E[/auto-review-loop]
38:     E --> F[外部模型批判式审查]
39:     F --> G[迭代改实验与改论证]
40:     G --> H[/paper-writing]
41:     H --> I[LaTeX/PDF 产出]
42:     I --> J[可选 Feishu/Obsidian/Zotero 集成]
43: ```
44: 
45: ## 研究生命周期覆盖
46: 
47: - 前期覆盖较强：文献调研、idea discovery、novelty check 和研究计划都已经产品化。
48: - 中期覆盖实验执行：`run-experiment`、`monitor-experiment`、`analyze-results` 说明它希望真实驱动 GPU/远程实验，而不只是写报告。
49: - 后期覆盖写作与审阅：`paper-plan`、`paper-write`、`paper-compile`、`auto-paper-improvement-loop` 连接成论文成稿回路。
50: - 在“从方向到论文”的完整性上，它是本目录里最强调自治迭代的项目之一。
51: 
52: ## 集成与依赖面
53: 
54: - 安装方式是把 `skills/*` 复制到 `~/.claude/skills/`，说明其主要宿主仍是 Claude Code。
55: - 高价值能力依赖 Codex MCP，README 还专门提醒模型配置来自 `~/.codex/config.toml`。
56: - 可选集成面很多：Zotero、Obsidian、本地 PDF、Feishu/Lark、远程服务器、多模型组合，这让能力更强，也显著推高初始配置复杂度。
57: 
58: ## 证据与样例
59: 
60: - 工作流、功能亮点、远程服务器和集成项见 [Auto-claude-code-research-in-sleep/README_CN.md](../../ref-repos/Auto-claude-code-research-in-sleep/README_CN.md)。
61: - 技能清单见 [Auto-claude-code-research-in-sleep/skills](../../ref-repos/Auto-claude-code-research-in-sleep/skills)。
62: - 替代模型和 MCP 方向可从 [Auto-claude-code-research-in-sleep/mcp-servers](../../ref-repos/Auto-claude-code-research-in-sleep/mcp-servers) 观察。
63: - 本地最近提交为 `c4016ec`，日期 `2026-03-14`。
64: 
65: ## 优势
66: 
67: - 工作流完整，能把“找方向、做实验、写论文、反复 review”串成一条自动链路。
68: - 跨模型 reviewer 设计有明确理论立场，避免单模型自审的盲点。
69: - 对实验、通知、远程执行这些现实科研摩擦点有直接设计，而不是只停留在写作层。
70: 
71: ## 局限与风险
72: 
73: - 外部依赖多，包含 Claude、Codex、可选 MCP、可选远程 GPU，部署门槛明显高于 prompt 型项目。
74: - 质量叙事高度依赖 README 中展示的 run story，本地仓库本身仍以技能文档和操作说明为主。
75: - 长链路自治适合熟手，不适合把每一步都需要强控制的人。
76: 
77: ## 适用场景
78: 
79: - 有明确研究方向，希望把 nightly loop、交叉模型审查和实验执行串起来。
80: - 需要“研究助手 + reviewer”双角色分工，而不是单一模型全包。
81: - 对 Feishu、Zotero、Obsidian 一类研究配套工具有真实接入需求。
82: 
83: ## 关联笔记
84: 
85: - [[index]]
86: - [[summary/academic-research-agents-overview]]
87: - [[projects/argusbot]]
88: - [[projects/claude-code-deep-research]]
89: - [[projects/academic-research-skills]]
90: - [[projects/claude-scholar]]

(End of file - total 90 lines)
</content>
```

---

## Assistant (Build · gpt-5.4 · 70.5s)

_Thinking:_

**Updating documentation spec**

I need to write a new document for the baseline specification, perhaps under LLM-Working or the framework. The user mentioned to keep going with step 2: building the mode baseline spec, so I think LLM-Working makes sense to start with. I should also consider updating any relevant links, possibly for framework/index or plans. It looks like I'll be using apply_patch for this task. Let's get this organized!

我会把 baseline spec 先写成一份独立规划文档，避免直接污染现有未来态 framework 文档。这样我们先冻结 next-release 的硬边界，后续再决定怎么回写到 `framework/` 主线。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/mode-baseline-spec.md\n+---\n+aliases:\n+  - Mode Baseline Spec\n+  - Mode 1 / Mode 2 Baseline 规格\n+tags:\n+  - scholar-agent\n+  - mode-spec\n+  - dashboard\n+  - requirements\n+  - implementation-plan\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# Mode 1 / Mode 2 Baseline 规格\n+\n+> [!abstract]\n+> 本文档用于把 `scholar-agent` 当前文档中偏未来态的 Mode 1 / Mode 2 定义，收敛成 next release 可执行、可观察、可交付的 baseline 规格。目标不是保留完整“自动科研”承诺，而是固定两类任务模式在下一版中的最小输入、最小流程、最小输出、终止边界和非目标，从而为 manifesto、dashboard 和 architecture 提供统一约束。\n+\n+## 规格结论\n+\n+- 当前 `[[framework/v1-dual-mode-research-engine]]` 中的 Mode 1 / Mode 2 仍可保留为蓝图层文档，但不能直接作为 next release 的 requirement。\n+- next release 只承诺两种 bounded baseline：Mode 1 为 `bounded discovery baseline`，Mode 2 为 `bounded reproduction baseline`。\n+- 两种模式都应优先消费 `[[projects/auto-claude-code-research-in-sleep]]` 所代表的 skill + prompt 组织方式，但只吸收其 research pipeline baseline，不继承其“过夜全自动科研”叙事。\n+- baseline 的交付目标不是完整论文、不保证稳定达到 SOTA 复现，也不要求开放式长期自治；交付目标是可启动、可观察、可终止、可归档、可在 dashboard 中稳定展示。\n+\n+## 为什么必须重写 Baseline\n+\n+- 当前 framework 主线文档描述的是产品蓝图、长期方向和未来态系统，不适合直接约束 next release。\n+- 如果直接沿用旧定义，项目会再次落入“Mode 太大、UI 太大、runtime 太大、需求彼此牵连”的 scope explosion。\n+- baseline 规格的职责，是把 next release 先定义成“可用的研究 dashboard”，而不是“完整研究自动化系统”。\n+\n+## 统一约束\n+\n+### 统一目标\n+\n+- 任务必须能在 dashboard 中被启动、跟踪、回看和归档。\n+- 任务过程中必须形成结构化 milestone / checkpoint，而不是只留下自由文本日志。\n+- 失败、阻塞和提前终止都必须成为正式结果，而不是未定义异常。\n+\n+### 统一边界\n+\n+- 单用户优先。\n+- task-centric operator dashboard 优先。\n+- 任务类别收缩优先于学科泛化。\n+- evidence-grounded workflow 优先于宏大叙事。\n+\n+### 统一非目标\n+\n+- 不承诺跨领域通用研究。\n+- 不承诺开放式长期无人监督研究。\n+- 不承诺投稿级写作或论文工厂输出。\n+- 不承诺稳定完成完整高精度论文复现。\n+\n+## Mode 1：Bounded Discovery Baseline\n+\n+### 定位\n+\n+- Mode 1 在 next release 中不再定义为“文献探索与复现的完整自治系统”，而定义为“有边界的 discovery task baseline”。\n+- 它主要服务于：给定 topic description 和 seed PDF 后，发起一次可跟踪的研究探索任务，并把阶段进度、发现和工件沉淀到 dashboard 中。\n+\n+### 典型触发方式\n+\n+- prompt 形态可参考：`/research-pipeline start discovering <topic description>, with <seed pdf file path> for reference.`\n+- 这里的 prompt 只是启动入口，不是最终业务语义；系统内部必须把该请求翻译成 task、workspace、artifacts 和 checkpoints。\n+\n+### 输入基线\n+\n+- topic description：用户用自然语言给出的研究方向或问题框定。\n+- seed PDF：至少一份参考论文或综述。\n+- optional hints：可选的 focus / ignore directions。\n+- bounded contract：至少包含执行边界，如时间、深度或人工中止条件中的一部分。\n+\n+### 最小流程\n+\n+1. 创建 discovery task。\n+2. 绑定 workspace / session / container 上下文。\n+3. 使用种子论文和 topic description 启动一次 research pipeline baseline。\n+4. 生成 milestone / checkpoint timeline。\n+5. 产出中间和最终 artifacts。\n+6. 在达到边界、失败、用户取消或自然结束后归档。\n+\n+### 最小可观察要求\n+\n+- 当前阶段可见。\n+- milestone / checkpoint timeline 可见。\n+- 最近产出 artifacts 可见。\n+- 最近完成 discovery task 可回看。\n+- 对用户来说，系统状态不能退化为“只知道任务还在跑”。\n+\n+### 最小输出\n+\n+- 结构化任务记录。\n+- 一组可浏览的工件，至少可包含：notes、tables、reports、figures 中的一部分。\n+- 明确的终止结果：completed / failed / cancelled / blocked 之一。\n+- 一份 discovery outcome 摘要，用于说明这次探索到底得到了什么。\n+\n+### 对参考项目的吸收方式\n+\n+- 吸收 `[[projects/auto-claude-code-research-in-sleep]]` 中的 `/idea-discovery`、`/research-pipeline`、novelty check 和 reviewer loop 意识。\n+- 不吸收其“从方向一路串到 paper-writing”的整体承诺。\n+- 不把外部 reviewer、多模型协作、通知集成等外围能力写成 baseline requirement。\n+\n+### 明确不承诺\n+\n+- 不承诺自动递归跑完整文献图谱。\n+- 不承诺稳定给出高质量 idea 验证。\n+- 不承诺自动完成高价值论文筛选与复现闭环。\n+- 不承诺 next release 中完整实现当前 `ExplorationGraph` 的全部蓝图语义。\n+\n+### 成功标准\n+\n+- 用户能稳定发起一次 discovery task。\n+- 用户能在 dashboard 中看见这次 task 的时间线、近期工件和结果摘要。\n+- 任务结束后有明确归档状态和可回看的 artifacts。\n+- 失败不会频繁破坏状态或让任务进入不可理解的悬空状态。\n+\n+## Mode 2：Bounded Reproduction Baseline\n+\n+### 定位\n+\n+- Mode 2 在 next release 中不再定义为“从零高精度深度复现论文方法的完整系统”，而定义为“有边界的 reproduction task baseline”。\n+- 它主要服务于：围绕目标论文、目标表格或明确实验目标，发起一次可跟踪的实现 / 复现任务，并把结果工件以 dashboard 可预览的方式呈现出来。\n+\n+### 典型触发方式\n+\n+- 启动入口可以是目标论文 + 目标结果，也可以是面向 skill 的 reproduction prompt。\n+- 与 Mode 1 一样，prompt 只是入口；系统内部必须转换为 task、workspace、artifacts 和 checkpoints。\n+\n+### 输入基线\n+\n+- target paper：至少一篇目标论文。\n+- target result：至少一个明确的结果目标，例如目标表格、指标或复现范围。\n+- workspace / container context。\n+- bounded contract：至少有预算、时间、轮次或人工中止边界之一。\n+\n+### 最小流程\n+\n+1. 创建 reproduction task。\n+2. 绑定 workspace / session / container。\n+3. 启动 baseline implementation / reproduction 流程。\n+4. 记录 checkpoint 和中间工件。\n+5. 生成结果产物并归档。\n+6. 在完成、失败、取消或阻塞时结束任务。\n+\n+### 最小可观察要求\n+\n+- 当前任务阶段可见。\n+- 当前 checkpoint / milestone 可见。\n+- 结果工件可预览。\n+- 任务结束后可回看 artifacts、结果摘要和终止原因。\n+\n+### 最小输出\n+\n+- 结构化任务记录。\n+- 至少一类可预览结果工件：table / report / figure。\n+- reproduction outcome 摘要。\n+- 明确终止状态与原因。\n+\n+### 对参考项目的吸收方式\n+\n+- 吸收 `[[projects/auto-claude-code-research-in-sleep]]` 中的 `run-experiment`、`monitor-experiment`、`analyze-results` 和 reviewer loop 思路。\n+- 不继承其完整 paper-writing、通知、MCP、多模型组合等外围能力。\n+- 不把“深度复现 = 高精度还原论文所有结果”写成 next release 承诺。\n+\n+### 明确不承诺\n+\n+- 不承诺稳定达到完整高精度复现。\n+- 不承诺自动从零实现完整方法并跑完整实验套件。\n+- 不承诺自动完成偏差归因的完整科学评估。\n+- 不承诺 next release 中完整实现当前 `QualityAssessment` 蓝图语义。\n+\n+### 成功标准\n+\n+- 用户能稳定发起一次 reproduction task。\n+- 用户能在 dashboard 中看到任务进度、近期结果工件和结果摘要。\n+- 系统能把失败、阻塞和提前结束作为正式输出，而不是隐式吞掉。\n+- 结果工件能被预览，而不是只能从容器或磁盘手工翻找。\n+\n+## Dashboard 对两种 Mode 的共同要求\n+\n+### 必须可见的信息\n+\n+- 当前运行任务的 milestone / checkpoint timeline。\n+- recent finished tasks。\n+- recent artifacts。\n+- workspace resources snapshot：GPU / CPU / memory / disk。\n+\n+### 必须可预览的工件\n+\n+- tables：CSV / Markdown。\n+- reports：Markdown。\n+- figures：SVG / PNG。\n+\n+### 条件性需求\n+\n+- token usage overview 只在运行时能稳定提供 telemetry 时纳入 next release；否则延期，不可反向绑架 mode baseline。\n+\n+## 对 Architecture 的约束\n+\n+- 不能先为了追求完整 research runtime，而牺牲 dashboard、stability、observability 三项核心。\n+- 不能把 next release 定义成“先实现完整 TaskEngine，再顺便补 UI”。\n+- architecture 应优先服务于 task tracking、workspace management、SSH integration、artifact preview 和 checkpoint timeline。\n+\n+## 对后续文档的回写要求\n+\n+- manifesto 需要引用本文，作为 requirements / expectations 的模式约束。\n+- next release roadmap 需要引用本文，作为 must-have / deferred 划分依据。\n+- 后续 architecture baseline 需要显式说明：每个 mode 的 backend / frontend contract 如何满足这里的最小要求。\n+- `[[framework/v1-dual-mode-research-engine]]` 后续需要增加说明：当前文档是蓝图层，next release baseline 以本文为准。\n+\n+## 当前建议的后续原子任务\n+\n+1. 把本文的 Mode 1 / Mode 2 基线回写到 manifesto 规划。\n+2. 把本文的 dashboard 共同要求回写到 next release roadmap。\n+3. 起草 architecture baseline，明确 task、workspace、session、artifact preview 的实现边界。\n+4. 评估 token telemetry 是否应保留在 next release 候选需求中。\n+\n+## 关联笔记\n+\n+- [[LLM-Working/project-realignment-manifesto-plan]]\n+- [[LLM-Working/next-release-realignment-roadmap]]\n+- [[framework/v1-dual-mode-research-engine]]\n+- [[framework/v1-rfc]]\n+- [[projects/auto-claude-code-research-in-sleep]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/project-realignment-manifesto-plan.md\n@@\n ### Mode 1 Baseline\n \n - 建议定义为“bounded discovery baseline”，即围绕种子论文或主题描述启动一次有边界的探索任务。\n - 默认参考 `[[projects/auto-claude-code-research-in-sleep]]` 的 skill / prompt 组织方式，但在本项目中只吸收其 research pipeline baseline，不继承“过夜全自动科研”叙事。\n - 最小可交付重点是：任务可启动、里程碑可观察、工件可沉淀、探索边界可终止。\n+- 更具体的 baseline 约束以后续 `[[LLM-Working/mode-baseline-spec]]` 为准。\n@@\n ### Mode 2 Baseline\n \n - 建议定义为“bounded reproduction baseline”，即围绕目标论文、目标表格或明确任务发起一次可观察的实现 / 复现任务。\n - 最小可交付重点是：任务过程可跟踪、结果工件可预览、失败可归档，而不是承诺稳定达到完整高精度复现。\n+- 更具体的 baseline 约束以后续 `[[LLM-Working/mode-baseline-spec]]` 为准。\n@@\n - [[framework/v1-rfc]]\n - [[framework/v1-roadmap]]\n+- [[LLM-Working/mode-baseline-spec]]\n - [[projects/auto-claude-code-research-in-sleep]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md\n@@\n ### Mode 1\n \n - 目标：bounded discovery baseline。\n - 典型触发方式：围绕 topic description 和 seed PDF 发起一次有边界的探索任务。\n - 最小承诺：任务可启动、进度可见、工件可沉淀、边界可终止。\n+- 具体输入、最小输出和非目标约束以 `[[LLM-Working/mode-baseline-spec]]` 为准。\n@@\n ### Mode 2\n \n - 目标：bounded reproduction baseline。\n - 典型触发方式：围绕目标论文与目标结果发起一次实现 / 复现任务。\n - 最小承诺：任务过程可跟踪、工件可预览、失败可归档。\n+- 具体输入、最小输出和非目标约束以 `[[LLM-Working/mode-baseline-spec]]` 为准。\n@@\n - [[framework/index]]\n - [[framework/v1-dual-mode-research-engine]]\n - [[framework/v1-rfc]]\n - [[framework/v1-roadmap]]\n+- [[LLM-Working/mode-baseline-spec]]\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A docs/LLM-Working/mode-baseline-spec.md
M docs/LLM-Working/project-realignment-manifesto-plan.md
M docs/LLM-Working/next-release-realignment-roadmap.md
```

---

## Assistant (Build · gpt-5.4 · 7.7s)

baseline spec 已经写出来并回链到两份规划文档。下一步做构建验证，然后补今天的 worklog。

**Tool: bash**

**Input:**
```json
{
  "command": "UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build",
  "description": "Builds the HTML notes site",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```

[31m │  ⚠  Warning from the Material for MkDocs team[0m
[31m │[0m
[31m │[0m  MkDocs 2.0, the underlying framework of Material for MkDocs,
[31m │[0m  will introduce backward-incompatible changes, including:
[31m │[0m
[31m │  × [0mAll plugins will stop working – the plugin system has been removed
[31m │  × [0mAll theme overrides will break – the theming system has been rewritten
[31m │  × [0mNo migration path exists – existing projects cannot be upgraded
[31m │  × [0mClosed contribution model – community members can't report bugs
[31m │  × [0mCurrently unlicensed – unsuitable for production use
[31m │[0m
[31m │[0m  Our full analysis:
[31m │[0m
[31m │[0m  [4mhttps://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/[0m
[0m
INFO    -  MERMAID2  - Initialization arguments: {}
INFO    -  MERMAID2  - Using specified javascript library: assets/javascripts/vendor/mermaid-10.4.0.min.js
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /Users/kozmosa/code/scholar-agent/site
INFO    -  MERMAID2  - Found superfences config: {'custom_fences': [{'name': 'mermaid', 'class': 'mermaid', 'format': functools.partial(<function fence_mermaid at 0x104eac220>, custom=True)}]}
INFO    -  MERMAID2  - Found 'fence_mermaid_custom' function: activate custom loader for superfences
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI-Native Research Framework：有界自治研究系统蓝图': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '工件图谱架构：AI-Native Research Framework 的核心模型': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'V1：双模式有界自治研究引擎': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 RFC：有界自治研究引擎实现规格': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 Roadmap：实现路线图': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Academic Research Skills：从研究到发表的学术全流程管线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI Research SKILLs：AI 研究工程技能库': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'ArgusBot：面向 Codex 的监督式 Autoloop 控制层': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Auto-claude-code-research-in-sleep：过夜自治科研流水线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'autoresearch：自治 ML 实验迭代框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Awesome Claude Code Paper Proofreading：LaTeX 论文校对 prompt 工作流': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Code Deep Research：多阶段深度研究框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Scholar：学术研究与开发一体化个人配置系统': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Everything Claude Code：通用 Agent Harness 基线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'EvoScientist：多渠道统一控制面的自进化 AI 科学家工作台': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '学术研究 Agent 汇总研究报告': found 2 diagrams, adding scripts
INFO    -  Documentation built in 0.74 seconds

```

---

## Assistant (Build · gpt-5.4 · 15.0s)

构建通过。我现在补 worklog，并把 todo 收口。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md\n@@\n ## 日志记录\n \n - 2026-04-04 15:20 `docs-planning`：完成 scholar-agent 项目重定位与 next release 重对齐的首轮规划基线，新增 `[[LLM-Working/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/next-release-realignment-roadmap]]`，把项目主叙事收敛为“单用户优先的 agent-driven research dashboard”，固定 manifesto / framework / architecture / decision-log / roadmap 的职责边界、Mode 1 / Mode 2 baseline 重写方向，以及以单会话原子任务推进的路线图；同时在 `[[framework/index]]` 增加当前规划入口，便于后续从 framework 主线进入这组长期规划文档；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 15:35 `docs-planning`：完成 `[[LLM-Working/mode-baseline-spec]]`，把 next release 的 Mode 1 / Mode 2 从未来态蓝图收敛为 bounded discovery / bounded reproduction baseline，明确两种模式的最小输入、最小流程、最小输出、统一非目标、dashboard 共同要求，以及对后续 manifesto / roadmap / architecture 的回写约束；同步把该规格回链到 `[[LLM-Working/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M docs/LLM-Working/worklog/2026-04-04.md
```

---

## Assistant (Build · gpt-5.4 · 7.6s)

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "起草 Mode1/Mode2 baseline spec 文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "把 baseline spec 回链到现有规划文档",
      "priority": "medium",
      "status": "completed"
    },
    {
      "content": "更新今日 worklog 记录本轮 baseline 收敛",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "执行文档构建验证 baseline 文档改动",
      "priority": "high",
      "status": "completed"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "起草 Mode1/Mode2 baseline spec 文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "把 baseline spec 回链到现有规划文档",
    "priority": "medium",
    "status": "completed"
  },
  {
    "content": "更新今日 worklog 记录本轮 baseline 收敛",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "执行文档构建验证 baseline 文档改动",
    "priority": "high",
    "status": "completed"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 25.2s)

这轮已经继续把第 2 项真正落成文档了。

**新增**
1. `docs/LLM-Working/mode-baseline-spec.md`

**更新**
1. `docs/LLM-Working/project-realignment-manifesto-plan.md`
2. `docs/LLM-Working/next-release-realignment-roadmap.md`
3. `docs/LLM-Working/worklog/2026-04-04.md`

**这次具体完成了什么**
我把 `Mode 1 / Mode 2 baseline spec` 正式写出来了，并且不直接改写现有未来态 `framework` 文档，而是先在 `LLM-Working` 层冻结 next-release 的硬边界。这样做的好处是：

1. 不会直接污染现有蓝图层文档
2. 先把 next release 需要 obey 的 requirements 固定下来
3. 后面可以再有控制地回写到 manifesto / framework / architecture

**新文档的核心内容**
`docs/LLM-Working/mode-baseline-spec.md` 现在明确了：

**1. 为什么必须重写 baseline**
- 当前 `framework/v1-dual-mode-research-engine.md` 更像蓝图和未来态承诺
- 不适合作为 next release 的直接 requirement
- 否则项目会继续 scope explosion

**2. Mode 1 的 next-release 定义**
- 不是“完整文献探索与复现自治系统”
- 而是 `bounded discovery baseline`

它现在固定了：
- 定位
- 典型触发方式
- 最小输入
- 最小流程
- 最小可观察要求
- 最小输出
- 对 `auto-claude-code-research-in-sleep` 的吸收方式
- 明确不承诺什么
- 成功标准

**3. Mode 2 的 next-release 定义**
- 不是“完整从零高精度深度复现系统”
- 而是 `bounded reproduction baseline`

同样固定了：
- 最小输入
- 最小流程
- 最小输出
- 最小可观察要求
- 不承诺什么
- 成功标准

**4. dashboard 对两种 mode 的共同要求**
这里我也顺手把 mode 和 dashboard 绑定起来了，明确 next release 至少要支持：

- milestone / checkpoint timeline
- recent finished tasks
- recent artifacts
- workspace resources snapshot
- artifact preview:
  - tables: CSV / Markdown
  - reports: Markdown
  - figures: SVG / PNG

同时我把一个关键工程约束写死了：

- token usage overview 只有在运行时能稳定提供 telemetry 时才纳入
- 否则延期
- 不能反向绑架 mode baseline

这个约束我认为很重要，因为它在帮你防 scope 再膨胀。

**5. 对后续文档的回写要求**
我已经在文档里明确要求：

- manifesto 要引用这份 spec
- roadmap 要引用这份 spec
- architecture baseline 要按它来解释 backend/frontend contract
- 未来 `framework/v1-dual-mode-research-engine.md` 也应该显式说明：
  - 自己是蓝图层
  - next release baseline 以这份 spec 为准

**我对当前状态的判断**
现在你的长期规划已经有了 3 个连续层次：

1. `project-realignment-manifesto-plan.md`
   - 解决项目是什么

2. `next-release-realignment-roadmap.md`
   - 解决下一版要交付什么

3. `mode-baseline-spec.md`
   - 解决 Mode1 / Mode2 到底在 next release 中意味着什么

这三份文档现在已经形成了一个比较健康的收敛链条。  
这比之前只在对话里讲方向，已经前进了一大步。

**验证**
我又执行了一次文档构建：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build
```

结果：通过。

**我现在要直接指出的一个工程建议**
下一步不要急着写完整 manifesto 正文，也不要急着写完整 architecture。  
最合理的顺序现在应该是：

1. 先写 `dashboard baseline / IA`
2. 再写 `architecture baseline`

原因是：

- 你现在已经有项目定位
- 有 next release 范围
- 有 mode baseline
- 接下来最需要固定的是 UI/控制面到底展示什么、围绕什么对象工作

否则 architecture 很容易又写回“未来态 runtime 架构”，而不是 next-release dashboard architecture。

**我建议的下一步**
下一轮最适合继续做的是：

1. `dashboard baseline spec`
   - 首页区块
   - 主导航对象
   - task detail / artifact preview / timeline 的信息架构
   - must-have vs deferred

2. `architecture baseline plan`
   - task / workspace / session / container / artifact preview 的实现边界
   - frontend/backend contract
   - 不去碰未来态完整 TaskEngine 幻觉

我推荐先做 `dashboard baseline spec`。  
因为它会直接决定 architecture 该围绕什么收敛。

---

## User

continue

---

## Assistant (Build · gpt-5.4 · 17.2s)

_Thinking:_

**Moving forward with the dashboard**

I need to continue building the baseline specifications for the dashboard since I feel like we have enough context now. Maybe using todowrite could be complex, but it might work. I also think I need to get a progress update. Plus, creating a new LLM-Working document sounds like a good idea, and maybe I should link that framework too. Let's make sure we get this done!

继续把下一个硬边界落成文档：先写 `dashboard baseline spec`，把 next release 的 UI/控制面范围冻结下来，再决定后续 architecture 应该围绕什么组织。

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "起草 dashboard baseline spec 文档",
      "priority": "high",
      "status": "in_progress"
    },
    {
      "content": "将 dashboard spec 回链到现有规划文档",
      "priority": "medium",
      "status": "pending"
    },
    {
      "content": "更新今日 worklog 记录 dashboard 收敛",
      "priority": "high",
      "status": "pending"
    },
    {
      "content": "执行文档构建验证 dashboard 文档改动",
      "priority": "high",
      "status": "pending"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "起草 dashboard baseline spec 文档",
    "priority": "high",
    "status": "in_progress"
  },
  {
    "content": "将 dashboard spec 回链到现有规划文档",
    "priority": "medium",
    "status": "pending"
  },
  {
    "content": "更新今日 worklog 记录 dashboard 收敛",
    "priority": "high",
    "status": "pending"
  },
  {
    "content": "执行文档构建验证 dashboard 文档改动",
    "priority": "high",
    "status": "pending"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 58.6s)

我会直接写一份 `dashboard baseline spec`，内容会严格围绕你已经确认的首屏信息、artifact 预览、task-centric 控制面和 scope 限制，不提前展开成完整前端方案。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/dashboard-baseline-spec.md\n+---\n+aliases:\n+  - Dashboard Baseline Spec\n+  - Dashboard Baseline 规格\n+tags:\n+  - scholar-agent\n+  - dashboard\n+  - webui\n+  - requirements\n+  - implementation-plan\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# Dashboard Baseline 规格\n+\n+> [!abstract]\n+> 本文档用于把 next release 的 dashboard 从“一个模糊的现代 Web UI 想法”收敛成可实现的 baseline 规格。目标是定义 dashboard 的主对象、首页信息架构、任务详情结构、artifact preview 范围、可观察性边界和明确的 deferred 列表，让后续 architecture 文档围绕一个稳定控制面而不是围绕未来态研究平台展开。\n+\n+## 规格结论\n+\n+- next release 的 dashboard 应被定义为 `task-centric operator dashboard`，而不是“完整研究运营平台”或“研究大屏”。\n+- dashboard 首先服务单用户 operator：启动任务、看当前任务、回看最近任务、查看 artifacts、观察资源和系统健康，而不是做全局知识图谱、组织协作或战略分析。\n+- dashboard 的主对象必须是 `task`，而不是 paper、artifact graph 或全局项目空间。\n+- 任何无法由当前或短期可控实现支撑的 telemetry，都不能写成 next release 的硬 requirement。\n+\n+## 为什么必须先写 Dashboard Baseline\n+\n+- 当前关于 dashboard 的需求已经足够具体，但如果不先写成规格，后续 architecture 很容易继续围绕未来态 research runtime 发散。\n+- 项目当前的核心价值排序是 dashboard、stability、observability；因此 dashboard 不是“最后补 UI”，而是 next release 的主要交付面。\n+- dashboard 规格必须先于 frontend 选型、页面细化和 architecture baseline，否则 scope 会反向膨胀。\n+\n+## Dashboard 的定位\n+\n+### 一句话定义\n+\n+- dashboard 是一个单用户优先的 research operator control plane，用来观察、控制和回看 bounded discovery / bounded reproduction task。\n+\n+### 它要解决的问题\n+\n+- 让用户不再依赖散落的终端、日志文件和手工目录浏览来理解任务状态。\n+- 把任务进度、里程碑、工件、workspace 资源和系统健康放到统一界面中。\n+- 把“任务跑到哪了、产出了什么、出了什么问题、能不能继续”变成默认可见信息。\n+\n+### 它不负责解决的问题\n+\n+- 不负责成为完整研究工作台或团队协作门户。\n+- 不负责替代长期知识库或文献图谱浏览器。\n+- 不负责在 next release 中承载完整实验运营分析。\n+\n+## 主对象与导航原则\n+\n+### 主对象\n+\n+- task 是 dashboard 的一级对象。\n+- workspace、session、container、artifact 都是围绕 task 展开的二级对象。\n+\n+### 导航原则\n+\n+- 首页应先回答“现在正在发生什么”。\n+- 任务详情页应回答“这个 task 到底做到了哪一步，产出了什么，为什么结束”。\n+- artifact 预览应服务 task 回看，而不是独立发展成大型内容浏览器。\n+\n+## 首页 Baseline\n+\n+### 首屏必须有的区块\n+\n+1. 系统健康状态条。\n+2. 当前运行任务的 milestone / checkpoint timeline。\n+3. 最近完成任务。\n+4. 最近 artifacts。\n+5. workspace 资源快照。\n+6. token usage overview（仅当 telemetry 能稳定提供时启用）。\n+\n+### 1. 系统健康状态条\n+\n+应展示：\n+\n+- API 服务状态。\n+- container / session SSH 可用性。\n+- workspace 或容器是否已就绪。\n+- 基础资源健康：GPU / CPU / memory / disk 是否处于可用状态。\n+\n+说明：\n+\n+- 这一区块必须放在首屏顶端。\n+- 它首先回答“系统现在能不能正常工作”，而不是展示漂亮指标。\n+\n+### 2. 当前运行任务的 Timeline\n+\n+应展示：\n+\n+- 当前任务名称或摘要。\n+- 当前 mode。\n+- 当前阶段。\n+- 已完成 milestone / checkpoint。\n+- 当前所在 checkpoint。\n+- 最近日志性事件摘要。\n+\n+要求：\n+\n+- 这是首页主区块，不是附属模块。\n+- 对用户来说，dashboard 的核心价值之一就是“当前任务时间线一眼可见”。\n+\n+### 3. 最近完成任务\n+\n+应展示：\n+\n+- 最近若干个完成、失败、取消或阻塞的任务。\n+- 每个任务至少展示：mode、终态、结束时间、结果摘要入口。\n+\n+目的：\n+\n+- 帮助用户快速回看最近发生了什么。\n+- 支持从首页直接进入任务详情。\n+\n+### 4. 最近 Artifacts\n+\n+应展示：\n+\n+- 最近生成的 tables、figures、reports。\n+- 点击后直接用 modal preview，而不是强迫用户跳到文件系统。\n+\n+要求：\n+\n+- 这里展示的是“近期有价值工件”，不是全量 artifact index。\n+- 首屏只做轻量回看入口，不发展成复杂浏览器。\n+\n+### 5. Workspace 资源快照\n+\n+应展示：\n+\n+- GPU usage。\n+- CPU usage。\n+- memory usage。\n+- disk usage。\n+\n+说明：\n+\n+- 这里优先做 snapshot，而不是复杂趋势分析。\n+- next release 不应为了首页资源图表反向引入大型 telemetry 子系统。\n+\n+### 6. Token Usage Overview\n+\n+候选展示字段：\n+\n+- rpm\n+- rph\n+- rpd\n+- tpm\n+- tph\n+- tpd\n+\n+工程约束：\n+\n+- 只有当运行时能稳定提供这些数据时，才纳入 baseline。\n+- 如果当前实现无法稳定提供，则必须延期，而不是为了满足首页字段去硬造不可靠统计。\n+\n+## 任务详情页 Baseline\n+\n+### 任务详情页必须回答的 5 个问题\n+\n+1. 这个 task 是什么。\n+2. 它现在在哪个阶段。\n+3. 它经历了哪些 milestone / checkpoint。\n+4. 它产出了什么 artifacts。\n+5. 它为什么还在运行、已经完成、失败或被终止。\n+\n+### 建议区块\n+\n+1. Task Summary\n+2. Timeline / Checkpoints\n+3. Artifact Preview\n+4. Workspace / Session Context\n+5. Termination / Error Summary\n+\n+### Task Summary\n+\n+至少展示：\n+\n+- task id\n+- mode\n+- created at / updated at\n+- current stage\n+- current status\n+- brief input summary\n+\n+### Timeline / Checkpoints\n+\n+至少展示：\n+\n+- 时间排序的 milestone / checkpoint 节点\n+- 当前节点高亮\n+- 完成节点、失败节点、阻塞节点的视觉区分\n+\n+### Artifact Preview\n+\n+至少支持：\n+\n+- tables：CSV / Markdown\n+- reports：Markdown\n+- figures：SVG / PNG\n+\n+要求：\n+\n+- preview 是 next release 的硬价值点之一。\n+- 不能把 artifact 继续留在“只能去文件系统自己看”的状态。\n+\n+### Workspace / Session Context\n+\n+至少展示：\n+\n+- 当前 workspace 标识\n+- 当前 container / session 是否可用\n+- 当前资源 snapshot\n+\n+### Termination / Error Summary\n+\n+至少展示：\n+\n+- 完成原因\n+- 失败原因\n+- 取消原因\n+- 阻塞原因\n+\n+要求：\n+\n+- 不能把失败仅表示成一个红点或模糊状态。\n+- 必须让用户知道 task 为什么停下。\n+\n+## Artifact Preview Baseline\n+\n+### 支持格式\n+\n+- tables：CSV / Markdown\n+- reports：Markdown\n+- figures：SVG / PNG\n+\n+### Preview 目标\n+\n+- 用户能在 dashboard 中快速浏览结果工件。\n+- 不要求 next release 做复杂编辑器。\n+- 不要求做全局 artifact 搜索引擎。\n+\n+### Preview 非目标\n+\n+- 不做复杂 notebook viewer。\n+- 不做交互式图表工作台。\n+- 不做 artifact graph browser。\n+\n+## 可观察性 Baseline\n+\n+### 必须可见的维度\n+\n+- 当前任务阶段。\n+- milestone / checkpoint timeline。\n+- 最近 artifacts。\n+- 当前资源 snapshot。\n+- 系统健康状态。\n+\n+### 可以延期的维度\n+\n+- 精细 token telemetry。\n+- 完整 experiment runtime streaming。\n+- 全局任务 analytics。\n+- 历史趋势图和成本预测。\n+\n+## 明确 Deferred\n+\n+- artifact graph 可视化。\n+- 多用户协作视图。\n+- 全局运营分析 dashboard。\n+- 图形化任务编排器。\n+- 长期知识图谱浏览器。\n+- 为了 UI 炫技而引入的大量非必要图表。\n+\n+## 对 Architecture 的约束\n+\n+- architecture 必须围绕 task-centric control plane 组织，而不是围绕未来态完整 research platform 组织。\n+- frontend / backend contract 优先服务首页区块、任务详情页、artifact preview 和资源快照。\n+- 任何需要复杂后端重构才能勉强支撑的 UI 诉求，都应优先被降级或延期。\n+\n+## 对后续文档的回写要求\n+\n+- `[[LLM-Working/next-release-realignment-roadmap]]` 需要以本文为 dashboard 范围基线。\n+- `[[LLM-Working/mode-baseline-spec]]` 中对 dashboard 的共同要求，应以本文为更具体解释。\n+- 后续 architecture baseline 应解释：这些 UI 区块如何映射到 task、workspace、session、artifact 和 telemetry 结构。\n+\n+## 当前建议的后续原子任务\n+\n+1. 起草 architecture baseline。\n+2. 固定 task / workspace / session / container 关系。\n+3. 固定 artifact preview 的数据路径与展示契约。\n+4. 决定 token telemetry 是否留在 next release 候选范围内。\n+\n+## 关联笔记\n+\n+- [[LLM-Working/project-realignment-manifesto-plan]]\n+- [[LLM-Working/next-release-realignment-roadmap]]\n+- [[LLM-Working/mode-baseline-spec]]\n+- [[framework/v1-rfc]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md\n@@\n ### Dashboard Baseline\n+\n+- dashboard 规格以后续 `[[LLM-Working/dashboard-baseline-spec]]` 为准。\n \n ### 推荐首页信息架构\n@@\n - [[framework/index]]\n - [[framework/v1-dual-mode-research-engine]]\n - [[framework/v1-rfc]]\n - [[framework/v1-roadmap]]\n - [[LLM-Working/mode-baseline-spec]]\n+- [[LLM-Working/dashboard-baseline-spec]]\n*** End Patch"
}
```

**Error:**
```
apply_patch verification failed: Error: Failed to find expected lines in /Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md:
### Dashboard Baseline

### 推荐首页信息架构
```

---

## Assistant (Build · gpt-5.4 · 8.9s)

补丁有一处上下文没对上。我先读一下那段原文，按实际内容重新打一个最小补丁。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md",
  "limit": 80,
  "offset": 56
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md</path>
<type>file</type>
<content>56: - 开放式长期无人监督研究。
57: - 投稿级论文写作与 paper factory 工作流。
58: - 任何未被明确列入 must-have 的外围集成。
59: 
60: ## Dashboard Baseline
61: 
62: ### 推荐首页信息架构
63: 
64: 1. 顶部系统健康状态条。
65: 2. 当前运行任务的 milestone / checkpoint timeline。
66: 3. 最近完成任务列表。
67: 4. 最近工件区：点击后用 modal preview。
68: 5. 资源快照：GPU / CPU / memory / disk。
69: 6. token usage overview（仅当运行时能稳定提供 telemetry 时纳入，否则延期）。
70: 
71: ### Artifact Preview Baseline
72: 
73: - tables：优先支持 CSV / Markdown 预览。
74: - reports：优先支持 Markdown 预览。
75: - figures：优先支持 SVG / PNG 预览。
76: 
77: ### 范围约束
78: 
79: - dashboard 以 task 为主对象，不先做全局研究运营大盘。
80: - 先做单任务时间线、摘要和 preview，不做复杂图谱探索器。
81: 
82: ## Mode Baseline 重写目标
83: 
84: ### Mode 1
85: 
86: - 目标：bounded discovery baseline。
87: - 典型触发方式：围绕 topic description 和 seed PDF 发起一次有边界的探索任务。
88: - 最小承诺：任务可启动、进度可见、工件可沉淀、边界可终止。
89: - 具体输入、最小输出和非目标约束以 `[[LLM-Working/mode-baseline-spec]]` 为准。
90: 
91: ### Mode 2
92: 
93: - 目标：bounded reproduction baseline。
94: - 典型触发方式：围绕目标论文与目标结果发起一次实现 / 复现任务。
95: - 最小承诺：任务过程可跟踪、工件可预览、失败可归档。
96: - 具体输入、最小输出和非目标约束以 `[[LLM-Working/mode-baseline-spec]]` 为准。
97: 
98: ## 推进阶段
99: 
100: ### Phase A：叙事与需求对齐
101: 
102: - 写死项目新定位。
103: - 写死 ready-for-use 标准。
104: - 写死 Non-Goals。
105: - 重写 Mode 1 / Mode 2 baseline 定义。
106: 
107: ### Phase B：文档体系收敛
108: 
109: - 起草 manifesto。
110: - 起草 architecture baseline。
111: - 起草 release decision-log 规则。
112: - 固定版本与 snapshot / archive 机制。
113: 
114: ### Phase C：产品范围冻结
115: 
116: - 固定 dashboard 首屏信息架构。
117: - 固定 task tracking / workspace / SSH / preview 的 must-have。
118: - 列出 deferred 项目。
119: 
120: ### Phase D：实现边界收敛
121: 
122: - 固定 backend / frontend contract。
123: - 固定 workspace / session / container 关系。
124: - 固定 artifacts preview 数据形态。
125: - 固定 observability 口径。
126: 
127: ### Phase E：原子任务执行
128: 
129: - 将上述内容拆成单会话任务。
130: - 每次会话解决一个硬边界问题，并更新 roadmap 与 decision context。
131: 
132: ## 推荐的原子任务拆解方法
133: 
134: ### 原则
135: 

(Showing lines 56-135 of 182. Use offset=136 to continue.)
</content>
```

---

## Assistant (Build · gpt-5.4 · 49.5s)

我会重新应用一个更小的补丁：只添加 dashboard spec 文档和对 roadmap 的引用，不碰别的段落。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/dashboard-baseline-spec.md\n+---\n+aliases:\n+  - Dashboard Baseline Spec\n+  - Dashboard Baseline 规格\n+tags:\n+  - scholar-agent\n+  - dashboard\n+  - webui\n+  - requirements\n+  - implementation-plan\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# Dashboard Baseline 规格\n+\n+> [!abstract]\n+> 本文档用于把 next release 的 dashboard 从“一个模糊的现代 Web UI 想法”收敛成可实现的 baseline 规格。目标是定义 dashboard 的主对象、首页信息架构、任务详情结构、artifact preview 范围、可观察性边界和明确的 deferred 列表，让后续 architecture 文档围绕一个稳定控制面而不是围绕未来态研究平台展开。\n+\n+## 规格结论\n+\n+- next release 的 dashboard 应被定义为 `task-centric operator dashboard`，而不是“完整研究运营平台”或“研究大屏”。\n+- dashboard 首先服务单用户 operator：启动任务、看当前任务、回看最近任务、查看 artifacts、观察资源和系统健康，而不是做全局知识图谱、组织协作或战略分析。\n+- dashboard 的主对象必须是 `task`，而不是 paper、artifact graph 或全局项目空间。\n+- 任何无法由当前或短期可控实现支撑的 telemetry，都不能写成 next release 的硬 requirement。\n+\n+## 为什么必须先写 Dashboard Baseline\n+\n+- 当前关于 dashboard 的需求已经足够具体，但如果不先写成规格，后续 architecture 很容易继续围绕未来态 research runtime 发散。\n+- 项目当前的核心价值排序是 dashboard、stability、observability；因此 dashboard 不是“最后补 UI”，而是 next release 的主要交付面。\n+- dashboard 规格必须先于 frontend 选型、页面细化和 architecture baseline，否则 scope 会反向膨胀。\n+\n+## Dashboard 的定位\n+\n+### 一句话定义\n+\n+- dashboard 是一个单用户优先的 research operator control plane，用来观察、控制和回看 bounded discovery / bounded reproduction task。\n+\n+### 它要解决的问题\n+\n+- 让用户不再依赖散落的终端、日志文件和手工目录浏览来理解任务状态。\n+- 把任务进度、里程碑、工件、workspace 资源和系统健康放到统一界面中。\n+- 把“任务跑到哪了、产出了什么、出了什么问题、能不能继续”变成默认可见信息。\n+\n+### 它不负责解决的问题\n+\n+- 不负责成为完整研究工作台或团队协作门户。\n+- 不负责替代长期知识库或文献图谱浏览器。\n+- 不负责在 next release 中承载完整实验运营分析。\n+\n+## 主对象与导航原则\n+\n+### 主对象\n+\n+- task 是 dashboard 的一级对象。\n+- workspace、session、container、artifact 都是围绕 task 展开的二级对象。\n+\n+### 导航原则\n+\n+- 首页应先回答“现在正在发生什么”。\n+- 任务详情页应回答“这个 task 到底做到了哪一步，产出了什么，为什么结束”。\n+- artifact 预览应服务 task 回看，而不是独立发展成大型内容浏览器。\n+\n+## 首页 Baseline\n+\n+### 首屏必须有的区块\n+\n+1. 系统健康状态条。\n+2. 当前运行任务的 milestone / checkpoint timeline。\n+3. 最近完成任务。\n+4. 最近 artifacts。\n+5. workspace 资源快照。\n+6. token usage overview（仅当 telemetry 能稳定提供时启用）。\n+\n+### 1. 系统健康状态条\n+\n+应展示：\n+\n+- API 服务状态。\n+- container / session SSH 可用性。\n+- workspace 或容器是否已就绪。\n+- 基础资源健康：GPU / CPU / memory / disk 是否处于可用状态。\n+\n+### 2. 当前运行任务的 Timeline\n+\n+应展示：\n+\n+- 当前任务名称或摘要。\n+- 当前 mode。\n+- 当前阶段。\n+- 已完成 milestone / checkpoint。\n+- 当前所在 checkpoint。\n+- 最近日志性事件摘要。\n+\n+### 3. 最近完成任务\n+\n+应展示：\n+\n+- 最近若干个完成、失败、取消或阻塞的任务。\n+- 每个任务至少展示：mode、终态、结束时间、结果摘要入口。\n+\n+### 4. 最近 Artifacts\n+\n+应展示：\n+\n+- 最近生成的 tables、figures、reports。\n+- 点击后直接用 modal preview，而不是强迫用户跳到文件系统。\n+\n+### 5. Workspace 资源快照\n+\n+应展示：\n+\n+- GPU usage。\n+- CPU usage。\n+- memory usage。\n+- disk usage。\n+\n+### 6. Token Usage Overview\n+\n+候选展示字段：\n+\n+- rpm\n+- rph\n+- rpd\n+- tpm\n+- tph\n+- tpd\n+\n+工程约束：\n+\n+- 只有当运行时能稳定提供这些数据时，才纳入 baseline。\n+- 如果当前实现无法稳定提供，则必须延期，而不是为了满足首页字段去硬造不可靠统计。\n+\n+## 任务详情页 Baseline\n+\n+### 任务详情页必须回答的 5 个问题\n+\n+1. 这个 task 是什么。\n+2. 它现在在哪个阶段。\n+3. 它经历了哪些 milestone / checkpoint。\n+4. 它产出了什么 artifacts。\n+5. 它为什么还在运行、已经完成、失败或被终止。\n+\n+### 建议区块\n+\n+1. Task Summary\n+2. Timeline / Checkpoints\n+3. Artifact Preview\n+4. Workspace / Session Context\n+5. Termination / Error Summary\n+\n+### Task Summary\n+\n+至少展示：\n+\n+- task id\n+- mode\n+- created at / updated at\n+- current stage\n+- current status\n+- brief input summary\n+\n+### Timeline / Checkpoints\n+\n+至少展示：\n+\n+- 时间排序的 milestone / checkpoint 节点\n+- 当前节点高亮\n+- 完成节点、失败节点、阻塞节点的视觉区分\n+\n+### Artifact Preview\n+\n+至少支持：\n+\n+- tables：CSV / Markdown\n+- reports：Markdown\n+- figures：SVG / PNG\n+\n+### Workspace / Session Context\n+\n+至少展示：\n+\n+- 当前 workspace 标识\n+- 当前 container / session 是否可用\n+- 当前资源 snapshot\n+\n+### Termination / Error Summary\n+\n+至少展示：\n+\n+- 完成原因\n+- 失败原因\n+- 取消原因\n+- 阻塞原因\n+\n+## Artifact Preview Baseline\n+\n+### 支持格式\n+\n+- tables：CSV / Markdown\n+- reports：Markdown\n+- figures：SVG / PNG\n+\n+### Preview 非目标\n+\n+- 不做复杂 notebook viewer。\n+- 不做交互式图表工作台。\n+- 不做 artifact graph browser。\n+\n+## 可观察性 Baseline\n+\n+### 必须可见的维度\n+\n+- 当前任务阶段。\n+- milestone / checkpoint timeline。\n+- 最近 artifacts。\n+- 当前资源 snapshot。\n+- 系统健康状态。\n+\n+### 可以延期的维度\n+\n+- 精细 token telemetry。\n+- 完整 experiment runtime streaming。\n+- 全局任务 analytics。\n+- 历史趋势图和成本预测。\n+\n+## 明确 Deferred\n+\n+- artifact graph 可视化。\n+- 多用户协作视图。\n+- 全局运营分析 dashboard。\n+- 图形化任务编排器。\n+- 长期知识图谱浏览器。\n+- 为了 UI 炫技而引入的大量非必要图表。\n+\n+## 对 Architecture 的约束\n+\n+- architecture 必须围绕 task-centric control plane 组织，而不是围绕未来态完整 research platform 组织。\n+- frontend / backend contract 优先服务首页区块、任务详情页、artifact preview 和资源快照。\n+- 任何需要复杂后端重构才能勉强支撑的 UI 诉求，都应优先被降级或延期。\n+\n+## 对后续文档的回写要求\n+\n+- `[[LLM-Working/next-release-realignment-roadmap]]` 需要以本文为 dashboard 范围基线。\n+- `[[LLM-Working/mode-baseline-spec]]` 中对 dashboard 的共同要求，应以本文为更具体解释。\n+- 后续 architecture baseline 应解释：这些 UI 区块如何映射到 task、workspace、session、artifact 和 telemetry 结构。\n+\n+## 当前建议的后续原子任务\n+\n+1. 起草 architecture baseline。\n+2. 固定 task / workspace / session / container 关系。\n+3. 固定 artifact preview 的数据路径与展示契约。\n+4. 决定 token telemetry 是否留在 next release 候选范围内。\n+\n+## 关联笔记\n+\n+- [[LLM-Working/project-realignment-manifesto-plan]]\n+- [[LLM-Working/next-release-realignment-roadmap]]\n+- [[LLM-Working/mode-baseline-spec]]\n+- [[framework/v1-rfc]]\n+\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md\n@@\n ## Dashboard Baseline\n+\n+- dashboard 规格以后续 `[[LLM-Working/dashboard-baseline-spec]]` 为准。\n \n ### 推荐首页信息架构\n@@\n - [[framework/v1-dual-mode-research-engine]]\n - [[framework/v1-rfc]]\n - [[framework/v1-roadmap]]\n - [[LLM-Working/mode-baseline-spec]]\n+- [[LLM-Working/dashboard-baseline-spec]]\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A docs/LLM-Working/dashboard-baseline-spec.md
M docs/LLM-Working/next-release-realignment-roadmap.md
```

---

## Assistant (Build · gpt-5.4 · 8.6s)

dashboard baseline spec 已经写好并挂回路线图。下一步做构建验证，并补 worklog。

**Tool: bash**

**Input:**
```json
{
  "command": "UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build",
  "description": "Builds the HTML notes site",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```

[31m │  ⚠  Warning from the Material for MkDocs team[0m
[31m │[0m
[31m │[0m  MkDocs 2.0, the underlying framework of Material for MkDocs,
[31m │[0m  will introduce backward-incompatible changes, including:
[31m │[0m
[31m │  × [0mAll plugins will stop working – the plugin system has been removed
[31m │  × [0mAll theme overrides will break – the theming system has been rewritten
[31m │  × [0mNo migration path exists – existing projects cannot be upgraded
[31m │  × [0mClosed contribution model – community members can't report bugs
[31m │  × [0mCurrently unlicensed – unsuitable for production use
[31m │[0m
[31m │[0m  Our full analysis:
[31m │[0m
[31m │[0m  [4mhttps://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/[0m
[0m
INFO    -  MERMAID2  - Initialization arguments: {}
INFO    -  MERMAID2  - Using specified javascript library: assets/javascripts/vendor/mermaid-10.4.0.min.js
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /Users/kozmosa/code/scholar-agent/site
INFO    -  MERMAID2  - Found superfences config: {'custom_fences': [{'name': 'mermaid', 'class': 'mermaid', 'format': functools.partial(<function fence_mermaid at 0x1037e0220>, custom=True)}]}
INFO    -  MERMAID2  - Found 'fence_mermaid_custom' function: activate custom loader for superfences
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI-Native Research Framework：有界自治研究系统蓝图': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '工件图谱架构：AI-Native Research Framework 的核心模型': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'V1：双模式有界自治研究引擎': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 RFC：有界自治研究引擎实现规格': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 Roadmap：实现路线图': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Academic Research Skills：从研究到发表的学术全流程管线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI Research SKILLs：AI 研究工程技能库': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'ArgusBot：面向 Codex 的监督式 Autoloop 控制层': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Auto-claude-code-research-in-sleep：过夜自治科研流水线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'autoresearch：自治 ML 实验迭代框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Awesome Claude Code Paper Proofreading：LaTeX 论文校对 prompt 工作流': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Code Deep Research：多阶段深度研究框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Scholar：学术研究与开发一体化个人配置系统': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Everything Claude Code：通用 Agent Harness 基线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'EvoScientist：多渠道统一控制面的自进化 AI 科学家工作台': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '学术研究 Agent 汇总研究报告': found 2 diagrams, adding scripts
INFO    -  Documentation built in 0.74 seconds

```

---

## Assistant (Build · gpt-5.4 · 17.1s)

验证通过。我把这轮 dashboard 收敛补进 worklog，并收口 todo。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md\n@@\n - 2026-04-04 15:20 `docs-planning`：完成 scholar-agent 项目重定位与 next release 重对齐的首轮规划基线，新增 `[[LLM-Working/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/next-release-realignment-roadmap]]`，把项目主叙事收敛为“单用户优先的 agent-driven research dashboard”，固定 manifesto / framework / architecture / decision-log / roadmap 的职责边界、Mode 1 / Mode 2 baseline 重写方向，以及以单会话原子任务推进的路线图；同时在 `[[framework/index]]` 增加当前规划入口，便于后续从 framework 主线进入这组长期规划文档；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n - 2026-04-04 15:35 `docs-planning`：完成 `[[LLM-Working/mode-baseline-spec]]`，把 next release 的 Mode 1 / Mode 2 从未来态蓝图收敛为 bounded discovery / bounded reproduction baseline，明确两种模式的最小输入、最小流程、最小输出、统一非目标、dashboard 共同要求，以及对后续 manifesto / roadmap / architecture 的回写约束；同步把该规格回链到 `[[LLM-Working/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 15:48 `docs-planning`：完成 `[[LLM-Working/dashboard-baseline-spec]]`，把 next release 的 dashboard 固定为单用户优先、task-centric 的 operator control plane，明确首页区块、任务详情页结构、artifact preview 格式、可观察性边界和 deferred 清单，并要求后续 architecture 围绕 task / workspace / session / artifact preview 组织，而不是继续围绕未来态完整 research platform 发散；同步把该规格回链到 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M docs/LLM-Working/worklog/2026-04-04.md
```

---

## Assistant (Build · gpt-5.4 · 6.4s)

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "起草 dashboard baseline spec 文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "将 dashboard spec 回链到现有规划文档",
      "priority": "medium",
      "status": "completed"
    },
    {
      "content": "更新今日 worklog 记录 dashboard 收敛",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "执行文档构建验证 dashboard 文档改动",
      "priority": "high",
      "status": "completed"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "起草 dashboard baseline spec 文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "将 dashboard spec 回链到现有规划文档",
    "priority": "medium",
    "status": "completed"
  },
  {
    "content": "更新今日 worklog 记录 dashboard 收敛",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "执行文档构建验证 dashboard 文档改动",
    "priority": "high",
    "status": "completed"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 28.5s)

继续推进完成了，这次把 `dashboard baseline` 也正式写出来了。

**新增**
1. `docs/LLM-Working/dashboard-baseline-spec.md`

**更新**
1. `docs/LLM-Working/next-release-realignment-roadmap.md`
2. `docs/LLM-Working/worklog/2026-04-04.md`

**这次写了什么**
`dashboard-baseline-spec.md` 现在把 next release 的 dashboard 从一个“想法”收敛成了一个明确的控制面规格。

它固定了这些关键点：

**1. dashboard 的定位**
- 不是“完整研究运营平台”
- 不是“研究大屏”
- 而是 `task-centric operator dashboard`

也就是：
- 单用户优先
- 面向 bounded discovery / bounded reproduction task
- 主要职责是观察、控制、回看

**2. dashboard 的一级对象**
我明确写死了：

- `task` 是 dashboard 的一级对象
- `workspace`、`session`、`container`、`artifact` 都是围绕 task 展开的二级对象

这个点很重要，因为它会直接限制后面的 architecture，不让它重新滑向“全局 paper / graph / project center”。

**3. 首页 baseline**
我把你前面确认过的首页诉求冻结成了规格：

首页必须有：

1. 系统健康状态条
2. 当前运行任务的 milestone / checkpoint timeline
3. 最近完成任务
4. 最近 artifacts
5. workspace 资源快照
6. token usage overview
   - 但这里只有在 telemetry 稳定时才纳入
   - 否则延期

这里我继续保持了一个工程约束：
token telemetry 仍然不是硬 requirement，避免它反向拖慢整个 next release。

**4. 任务详情页 baseline**
我把任务详情页也写成了结构化要求，要求它必须回答这 5 个问题：

1. 这个 task 是什么
2. 现在在哪个阶段
3. 经历了哪些 milestone / checkpoint
4. 产出了什么 artifacts
5. 为什么还在运行、完成、失败或终止

并建议区块为：

- Task Summary
- Timeline / Checkpoints
- Artifact Preview
- Workspace / Session Context
- Termination / Error Summary

**5. artifact preview baseline**
我把可预览格式冻结为：

- tables：CSV / Markdown
- reports：Markdown
- figures：SVG / PNG

同时明确不做：

- notebook viewer
- 交互式图表工作台
- artifact graph browser

这个边界现在很清楚了。

**6. 可观察性边界**
我把 next release 的 observability 也压缩成了两个层次：

必须可见：
- 当前任务阶段
- checkpoint timeline
- 最近 artifacts
- 当前资源 snapshot
- 系统健康状态

可以延期：
- 精细 token telemetry
- 完整 experiment runtime streaming
- 全局 analytics
- 趋势图和成本预测

**7. 明确 deferred**
我把这些直接写进了 deferred：

- artifact graph 可视化
- 多用户协作视图
- 全局运营分析 dashboard
- 图形化任务编排器
- 长期知识图谱浏览器
- 为 UI 炫技而引入的大量非必要图表

这对后面控制 scope 很关键。

**8. 对 architecture 的约束**
这是这份文档最重要的价值之一。

我已经明确写了：

- architecture 必须围绕 `task-centric control plane` 组织
- 不能继续围绕未来态完整 research platform 组织
- frontend/backend contract 优先服务：
  - 首页区块
  - 任务详情页
  - artifact preview
  - 资源快照

也就是说，这份 spec 已经开始“反向约束”后面的 architecture 了。

**验证**
我执行了：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build
```

结果：通过。

**当前状态**
现在你的长期规划已经形成了 4 个稳定的收敛层：

1. `project-realignment-manifesto-plan.md`
   - 项目重新定位

2. `next-release-realignment-roadmap.md`
   - 下一版范围与推进顺序

3. `mode-baseline-spec.md`
   - Mode 1 / Mode 2 的 next-release 硬边界

4. `dashboard-baseline-spec.md`
   - dashboard 的 next-release 硬边界

这套结构已经足够支撑下一步去写真正的 `architecture baseline` 了。

**我现在对下一步的建议**
下一步最合理的就是继续写：

1. `architecture-baseline-plan`
   - 固定 task / workspace / session / container / artifact preview / resource snapshot 的实现边界
   - 固定 frontend/backend contract
   - 解释哪些直接复用当前 `ainrf`，哪些需要补新能力

这是现在最顺的下一步，因为：

- manifesto 的定位已经有了
- roadmap 的范围已经有了
- mode baseline 已经有了
- dashboard baseline 也已经有了
- architecture 现在终于有清晰的约束源，不会继续漂

如果你同意，我下一步就继续直接写 `architecture-baseline-plan`。

---

## User

continue

---

## Assistant (Build · gpt-5.4 · 10.1s)

_Thinking:_

**Building the architecture plan**

I need to continue working on the architecture baseline plan. Before making any edits, it’s likely worth writing some commentary first. I might not need to read more because I can use existing documents. I think I should write a new document and perhaps link it to the roadmap or manifesto. An index for the framework could be useful, but maybe not. Updating the worklog is also on my list.

继续落地下一层：我会新增一份 `architecture baseline` 规划文档，把前面已经冻结的项目定位、mode baseline 和 dashboard baseline 变成实现边界与前后端契约。

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "起草 architecture baseline 规划文档",
      "priority": "high",
      "status": "in_progress"
    },
    {
      "content": "把 architecture baseline 回链到现有规划文档",
      "priority": "medium",
      "status": "pending"
    },
    {
      "content": "更新今日 worklog 记录 architecture 收敛",
      "priority": "high",
      "status": "pending"
    },
    {
      "content": "执行文档构建验证 architecture 文档改动",
      "priority": "high",
      "status": "pending"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "起草 architecture baseline 规划文档",
    "priority": "high",
    "status": "in_progress"
  },
  {
    "content": "把 architecture baseline 回链到现有规划文档",
    "priority": "medium",
    "status": "pending"
  },
  {
    "content": "更新今日 worklog 记录 architecture 收敛",
    "priority": "high",
    "status": "pending"
  },
  {
    "content": "执行文档构建验证 architecture 文档改动",
    "priority": "high",
    "status": "pending"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 56.4s)

先直接写文档，不再做额外探索。这一版 architecture baseline 会尽量贴当前 `ainrf` 实现现实，避免重新写回未来态 RFC。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/architecture-baseline-plan.md\n+---\n+aliases:\n+  - Architecture Baseline Plan\n+  - Architecture Baseline 规划\n+tags:\n+  - scholar-agent\n+  - architecture\n+  - implementation-plan\n+  - dashboard\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# Architecture Baseline 规划\n+\n+> [!abstract]\n+> 本文档用于把 `scholar-agent` 的 next release 架构从“未来态研究引擎蓝图”收敛为“围绕单用户 research dashboard 的可实现控制面架构”。目标不是重写现有 `[[framework/v1-rfc]]`，而是基于当前已经落地的 `ainrf` 控制面能力，固定 next release 的核心对象、模块边界、前后端契约、must-have 数据面和明确延期项，从而给后续真正的 architecture 文档和实现切片提供稳定基线。\n+\n+## 规划结论\n+\n+- next release 的架构必须围绕 `task-centric operator control plane` 组织，而不是围绕未来态完整 research runtime 组织。\n+- 当前 `ainrf` 已有的 API、state、gates、events、SSH health 基础，应被视为 next release 的真实起点，而不是被新架构推倒重来。\n+- architecture 的核心对象应收敛为：task、workspace、session、container、artifact preview、resource snapshot。\n+- 任何需要完整 TaskEngine、完整 experiment runtime、全局 analytics 或多用户权限系统才能成立的设计，都必须延期。\n+\n+## 与现有文档的关系\n+\n+### 与 Framework 的关系\n+\n+- `[[framework/ai-native-research-framework]]` 负责解释项目为什么存在、为什么有用、边界在哪里。\n+- `[[framework/v1-dual-mode-research-engine]]` 保留蓝图层意义，但不直接约束 next release。\n+- 本文档只负责 next release 的实现边界，不负责长期愿景扩展。\n+\n+### 与 RFC 的关系\n+\n+- `[[framework/v1-rfc]]` 仍然是未来态和实现蓝图的重要来源。\n+- 但 next release 不直接照搬 RFC 的完整三层研究引擎叙事。\n+- 本文档优先以“当前已有实现 + next release 必交付功能”为准，必要时显式压缩 RFC 范围。\n+\n+### 与 Baseline Specs 的关系\n+\n+- `[[LLM-Working/mode-baseline-spec]]` 定义 Mode 1 / Mode 2 的 next release 边界。\n+- `[[LLM-Working/dashboard-baseline-spec]]` 定义 dashboard 的 next release 边界。\n+- 本文档把这两个 baseline 转换成实现结构与模块责任。\n+\n+## 架构目标\n+\n+### 必须实现的目标\n+\n+- 支撑一个单用户优先的 task-centric dashboard。\n+- 支撑 Mode 1 / Mode 2 baseline 的任务创建、状态推进、结果回看与归档。\n+- 支撑 workspace / session / container 上下文的可见性。\n+- 支撑 artifact preview 与资源快照。\n+- 支撑系统健康、任务 timeline 和 recent artifacts 的统一呈现。\n+\n+### 不应试图在 next release 解决的目标\n+\n+- 完整 research runtime 自动化。\n+- 完整 ExperimentRun orchestration。\n+- 开放式多轮自治研究。\n+- 全局知识图谱和 artifact graph 浏览。\n+- 多用户和团队协作。\n+\n+## 核心对象模型\n+\n+### 1. Task\n+\n+- task 是一级对象，也是前后端 contract 的中心。\n+- 所有首页列表、详情页、timeline、termination summary 都围绕 task 组织。\n+\n+next release 中 task 至少应包含：\n+\n+- 基本标识：id、mode、created_at、updated_at。\n+- 生命周期：status、stage、termination_reason。\n+- 输入摘要：topic / seed paper / target paper / target result 的轻摘要。\n+- 运行摘要：current checkpoint、active gate、artifact summary。\n+\n+### 2. Workspace\n+\n+- workspace 是 task 的执行和产物归属上下文，不是独立产品对象。\n+- 在 next release 中，workspace 的主要职责是：让 dashboard 能展示“这个 task 在哪个工作区里运行、消耗了哪些资源、产出了哪些工件”。\n+\n+### 3. Session\n+\n+- session 是当前 task 与 container / execution context 的连接状态抽象。\n+- 在 next release 中，session 不应被设计成复杂的多会话编排系统。\n+- 它只需要支撑：当前是否可连接、是否可恢复、是否可观察。\n+\n+### 4. Container\n+\n+- container 是资源与执行环境来源，不是 next release 的编排中心。\n+- next release 只要求 container 对 dashboard 可见、可诊断、可通过 SSH 建立上下文。\n+- container lifecycle management 继续保持 out of scope。\n+\n+### 5. Artifact Preview\n+\n+- artifact 在 next release 中不是图谱浏览对象，而是 task 结果的可预览载体。\n+- preview contract 只覆盖 tables / reports / figures 三类核心结果。\n+\n+### 6. Resource Snapshot\n+\n+- 资源信息不是完整可观测平台，而是 workspace / container 的轻量 snapshot。\n+- next release 中只要求对 dashboard 可见，不要求复杂时间序列分析。\n+\n+## 模块边界\n+\n+### A. Control Plane Backend\n+\n+负责：\n+\n+- task list / task detail / task lifecycle summary。\n+- gate actions。\n+- event timeline。\n+- artifact summary 与 preview metadata。\n+- workspace / session / container 基础状态。\n+- health 和 resource snapshot。\n+\n+不负责：\n+\n+- 完整研究算法编排。\n+- 高级自治策略。\n+- 全局分析平台。\n+\n+### B. Dashboard Frontend\n+\n+负责：\n+\n+- 首页区块组织。\n+- task 详情页。\n+- artifact preview modal。\n+- timeline 与 recent lists 的呈现。\n+- 轻量交互：选择 task、查看详情、预览工件、查看健康状态。\n+\n+不负责：\n+\n+- 图形化任务编排。\n+- 图谱探索器。\n+- 内容编辑器。\n+\n+### C. Execution Context Integration\n+\n+负责：\n+\n+- 当前 workspace / session / container 是否可用。\n+- 资源 snapshot。\n+- 与 task 的关联展示。\n+\n+不负责：\n+\n+- next release 中不引入新的大规模 infra orchestrator。\n+- 不把 SSH integration 变成多节点调度系统。\n+\n+## 当前实现现实与架构策略\n+\n+### 已有基础\n+\n+- FastAPI service。\n+- task 路由与 task read model。\n+- human gate lifecycle。\n+- SSE 事件流。\n+- 本地 state / artifacts / events 持久化。\n+- SSH health / container config 基础。\n+\n+### 架构策略\n+\n+- 优先复用现有控制面基础，而不是发明一套与当前 `ainrf` 脱节的新模型。\n+- architecture 文档必须承认 next release 是“control plane first”，而不是“runtime-first”。\n+- 所有新增设计都应尽量作为现有 task、state、events、health 能力的扩展，而不是并行体系。\n+\n+## Frontend / Backend Contract Baseline\n+\n+### 首页至少需要的后端数据面\n+\n+1. system health summary\n+2. running task summary\n+3. running task timeline / checkpoints\n+4. recent finished tasks\n+5. recent artifacts\n+6. workspace resource snapshot\n+\n+### 任务详情页至少需要的后端数据面\n+\n+1. task summary\n+2. timeline / event summary\n+3. artifact list + preview metadata\n+4. workspace / session / container summary\n+5. termination / error summary\n+\n+### Preview Contract\n+\n+next release 中后端对 preview 至少需要能区分：\n+\n+- table artifact\n+- report artifact\n+- figure artifact\n+\n+并提供：\n+\n+- artifact type\n+- display title\n+- preview format\n+- preview source path or equivalent payload reference\n+\n+## 推荐的架构切片顺序\n+\n+### Slice 1：Task-Centric Read Model\n+\n+- 固定首页和详情页真正消费哪些 task 字段。\n+- 避免 UI 直接依赖未来态 artifact graph 或完整 runtime schema。\n+\n+### Slice 2：Workspace / Session / Container Summary\n+\n+- 定义 dashboard 需要看到的最小 execution context。\n+- 不把 execution context 设计成独立编排系统。\n+\n+### Slice 3：Artifact Preview Contract\n+\n+- 为 tables / reports / figures 定义统一 preview 元信息。\n+- 优先服务 modal preview，而不是大而全内容中心。\n+\n+### Slice 4：Observability Contract\n+\n+- 固定 milestone / checkpoint / event summary 如何被前端消费。\n+- 把精细 telemetry 作为候选项，而不是硬依赖。\n+\n+## 当前最需要警惕的架构风险\n+\n+### 1. 被旧 RFC 拖回完整研究引擎叙事\n+\n+- 如果 architecture 继续按完整 TaskEngine、完整 execution loop、完整 experiment runtime 展开，next release 会重新失控。\n+\n+### 2. 过早为前端引入复杂 telemetry 体系\n+\n+- 如果为了 token usage、资源趋势和全局分析去重构大量后端，next release 的 ready-for-use 目标会被拖慢。\n+\n+### 3. 把 workspace / session / container 过度平台化\n+\n+- 当前需求是“可见、可诊断、可关联”，不是“云原生任务平台”。\n+\n+## 明确 Deferred\n+\n+- 完整 TaskEngine 重构。\n+- experiment runtime streaming 全量协议。\n+- 全局 analytics / trends / forecasting。\n+- 多用户权限模型。\n+- artifact graph explorer。\n+- 可视化 workflow builder。\n+\n+## 对后续文档的回写要求\n+\n+- manifesto 需要把本文视为 next release 的实现边界补充。\n+- roadmap 需要把本文中的架构切片映射成原子任务。\n+- 后续正式 architecture 文档应以本文为提纲，而不是重新发明结构。\n+\n+## 当前建议的后续原子任务\n+\n+1. 固定 task read model 给 dashboard 的字段清单。\n+2. 固定 workspace / session / container summary shape。\n+3. 固定 artifact preview metadata shape。\n+4. 决定 token telemetry 是否延期。\n+5. 起草正式 architecture 文档目录。\n+\n+## 关联笔记\n+\n+- [[LLM-Working/project-realignment-manifesto-plan]]\n+- [[LLM-Working/next-release-realignment-roadmap]]\n+- [[LLM-Working/mode-baseline-spec]]\n+- [[LLM-Working/dashboard-baseline-spec]]\n+- [[framework/v1-rfc]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md\n@@\n ### Phase D：实现边界收敛\n \n - 固定 backend / frontend contract。\n - 固定 workspace / session / container 关系。\n - 固定 artifacts preview 数据形态。\n - 固定 observability 口径。\n+- 以 `[[LLM-Working/architecture-baseline-plan]]` 作为当前实现边界基线。\n@@\n - [[framework/v1-rfc]]\n - [[framework/v1-roadmap]]\n - [[LLM-Working/mode-baseline-spec]]\n - [[LLM-Working/dashboard-baseline-spec]]\n+- [[LLM-Working/architecture-baseline-plan]]\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A docs/LLM-Working/architecture-baseline-plan.md
M docs/LLM-Working/next-release-realignment-roadmap.md
```

---

## Assistant (Build · gpt-5.4 · 7.5s)

architecture baseline 已经写出来并挂到路线图。现在做构建验证，再补 worklog。

**Tool: bash**

**Input:**
```json
{
  "command": "UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build",
  "description": "Builds the HTML notes site",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```

[31m │  ⚠  Warning from the Material for MkDocs team[0m
[31m │[0m
[31m │[0m  MkDocs 2.0, the underlying framework of Material for MkDocs,
[31m │[0m  will introduce backward-incompatible changes, including:
[31m │[0m
[31m │  × [0mAll plugins will stop working – the plugin system has been removed
[31m │  × [0mAll theme overrides will break – the theming system has been rewritten
[31m │  × [0mNo migration path exists – existing projects cannot be upgraded
[31m │  × [0mClosed contribution model – community members can't report bugs
[31m │  × [0mCurrently unlicensed – unsuitable for production use
[31m │[0m
[31m │[0m  Our full analysis:
[31m │[0m
[31m │[0m  [4mhttps://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/[0m
[0m
INFO    -  MERMAID2  - Initialization arguments: {}
INFO    -  MERMAID2  - Using specified javascript library: assets/javascripts/vendor/mermaid-10.4.0.min.js
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /Users/kozmosa/code/scholar-agent/site
INFO    -  MERMAID2  - Found superfences config: {'custom_fences': [{'name': 'mermaid', 'class': 'mermaid', 'format': functools.partial(<function fence_mermaid at 0x102ed8220>, custom=True)}]}
INFO    -  MERMAID2  - Found 'fence_mermaid_custom' function: activate custom loader for superfences
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI-Native Research Framework：有界自治研究系统蓝图': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '工件图谱架构：AI-Native Research Framework 的核心模型': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'V1：双模式有界自治研究引擎': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 RFC：有界自治研究引擎实现规格': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 Roadmap：实现路线图': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Academic Research Skills：从研究到发表的学术全流程管线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI Research SKILLs：AI 研究工程技能库': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'ArgusBot：面向 Codex 的监督式 Autoloop 控制层': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Auto-claude-code-research-in-sleep：过夜自治科研流水线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'autoresearch：自治 ML 实验迭代框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Awesome Claude Code Paper Proofreading：LaTeX 论文校对 prompt 工作流': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Code Deep Research：多阶段深度研究框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Scholar：学术研究与开发一体化个人配置系统': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Everything Claude Code：通用 Agent Harness 基线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'EvoScientist：多渠道统一控制面的自进化 AI 科学家工作台': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '学术研究 Agent 汇总研究报告': found 2 diagrams, adding scripts
INFO    -  Documentation built in 0.71 seconds

```

---

## Assistant (Build · gpt-5.4 · 14.9s)

验证通过。我补一条 worklog，并收口 todo。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md\n@@\n - 2026-04-04 15:35 `docs-planning`：完成 `[[LLM-Working/mode-baseline-spec]]`，把 next release 的 Mode 1 / Mode 2 从未来态蓝图收敛为 bounded discovery / bounded reproduction baseline，明确两种模式的最小输入、最小流程、最小输出、统一非目标、dashboard 共同要求，以及对后续 manifesto / roadmap / architecture 的回写约束；同步把该规格回链到 `[[LLM-Working/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n - 2026-04-04 15:48 `docs-planning`：完成 `[[LLM-Working/dashboard-baseline-spec]]`，把 next release 的 dashboard 固定为单用户优先、task-centric 的 operator control plane，明确首页区块、任务详情页结构、artifact preview 格式、可观察性边界和 deferred 清单，并要求后续 architecture 围绕 task / workspace / session / artifact preview 组织，而不是继续围绕未来态完整 research platform 发散；同步把该规格回链到 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 16:00 `docs-planning`：完成 `[[LLM-Working/architecture-baseline-plan]]`，把 next release 的实现边界收敛为围绕单用户 research dashboard 的 control plane 架构，固定 task、workspace、session、container、artifact preview、resource snapshot 等核心对象与模块责任，明确当前 `ainrf` 既有 API / state / gates / events / SSH health 是真实起点，并将完整 TaskEngine、全局 analytics、多用户权限和 artifact graph explorer 继续保留为 deferred；同步把该基线回链到 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M docs/LLM-Working/worklog/2026-04-04.md
```

---

## Assistant (Build · gpt-5.4 · 7.6s)

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "起草 architecture baseline 规划文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "把 architecture baseline 回链到现有规划文档",
      "priority": "medium",
      "status": "completed"
    },
    {
      "content": "更新今日 worklog 记录 architecture 收敛",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "执行文档构建验证 architecture 文档改动",
      "priority": "high",
      "status": "completed"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "起草 architecture baseline 规划文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "把 architecture baseline 回链到现有规划文档",
    "priority": "medium",
    "status": "completed"
  },
  {
    "content": "更新今日 worklog 记录 architecture 收敛",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "执行文档构建验证 architecture 文档改动",
    "priority": "high",
    "status": "completed"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 27.1s)

继续完成了，这次把 `architecture baseline` 也正式落成文档了。

**新增**
1. `docs/LLM-Working/architecture-baseline-plan.md`

**更新**
1. `docs/LLM-Working/next-release-realignment-roadmap.md`
2. `docs/LLM-Working/worklog/2026-04-04.md`

**这次具体完成了什么**
`architecture-baseline-plan.md` 现在把 next release 的实现边界固定下来了，而且是明确贴着当前 `ainrf` 现实来写的，不是重新抄一遍未来态 RFC。

它主要做了这几件事：

**1. 固定 next release 的架构中心**
我明确写死了：

- next release 的架构必须围绕 `task-centric operator control plane`
- 不是围绕未来态完整 research runtime
- 不是围绕全功能 research platform

这个点非常关键，因为它直接把后续工程方向从“再设计一个大系统”拉回了“把当前控制面做成可用产品”。

**2. 固定核心对象**
我把 next release 的核心对象收敛成：

- task
- workspace
- session
- container
- artifact preview
- resource snapshot

这已经和前面两轮的 mode baseline、dashboard baseline 对上了。

**3. 明确与已有文档的关系**
文档里现在已经明确区分：

- `framework/*`
  - 继续负责蓝图和抽象层

- `v1-rfc`
  - 仍然有参考价值
  - 但 next release 不直接照搬它的完整研究引擎叙事

- 这份 architecture baseline
  - 只负责 next release 的现实实现边界

这一步其实很重要，因为它开始把“蓝图”和“当前实现要求”系统性分开了。

**4. 明确架构策略：复用现有 ainrf**
我在文档里写死了一个工程现实：

当前 `ainrf` 已有：
- FastAPI service
- task 路由与 read model
- human gate lifecycle
- SSE 事件流
- 本地 state / artifacts / events
- SSH health / container config 基础

所以 next release 的架构策略应该是：

- 以现有控制面为真实起点
- 扩展它
- 不推倒重来
- 不先去造完整 TaskEngine 幻觉

这点我认为对你现在最重要，因为它直接抑制“重新架构一遍”的冲动。

**5. 固定 frontend / backend contract 的最低要求**
我把 architecture 至少要服务的数据面也先写下来了。

首页最少需要：
- system health summary
- running task summary
- running task timeline / checkpoints
- recent finished tasks
- recent artifacts
- workspace resource snapshot

任务详情页最少需要：
- task summary
- timeline / event summary
- artifact list + preview metadata
- workspace / session / container summary
- termination / error summary

preview contract 也写了最小 shape：
- artifact type
- display title
- preview format
- preview source path 或等价引用

这意味着后面如果写正式 architecture 或开始写前端契约，就已经不是从零开始。

**6. 明确了 deferred 的工程边界**
我把这些继续明确留在 deferred：

- 完整 TaskEngine 重构
- experiment runtime streaming 全量协议
- 全局 analytics / trends / forecasting
- 多用户权限模型
- artifact graph explorer
- 可视化 workflow builder

这和前面 dashboard baseline 的 deferred 是一致的，没有漂。

**验证**
我再次执行了：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build
```

结果：通过。

**当前整体进展**
到现在为止，这一轮长期规划已经形成了 5 个连续文档层：

1. `project-realignment-manifesto-plan.md`
   - 项目重定位

2. `next-release-realignment-roadmap.md`
   - 下一版范围与推进顺序

3. `mode-baseline-spec.md`
   - Mode baseline

4. `dashboard-baseline-spec.md`
   - Dashboard baseline

5. `architecture-baseline-plan.md`
   - 实现边界 baseline

这已经不只是“想法整理”，而是一条逐层收敛的规划链了。

**我现在的工程判断**
下一步已经不适合继续无限扩展 planning 文档了。  
现在最自然的方向有两个：

**方向 A：开始写正式 manifesto 草稿**
把前面这些 planning 文档开始汇总成真正的版本化主文档。

适合现在做的原因：
- 项目定位已经比较清楚
- 需求与预期边界已经成型

**方向 B：开始写更接近实现的 contract 文档**
例如继续写：

1. task read model field contract
2. workspace / session / container summary contract
3. artifact preview metadata contract

这会更贴近后面真正实现 dashboard。

**我推荐的下一步**
我建议现在优先走 **方向 B**，先写 contract 级文档，而不是立刻写 manifesto 正文。

原因：
- manifesto 现在写也能写
- 但 contract 级文档会更直接地推动 next release
- 而且你之前已经明确：`engineering > product/system > academic`

所以我推荐下一轮继续写：

1. `task-read-model-contract`
2. `workspace-session-container-summary-contract`
3. `artifact-preview-contract`

如果你愿意，我下一步就继续直接写第一个：  
`task-read-model-contract`。

---

## User

continue write contracts

---

## Assistant (Build · gpt-5.4 · 9.7s)

我继续往实现边界推进，先写第一批 contract 文档：`task read model`、`workspace/session/container summary`、`artifact preview`。写完后我会把它们挂回现有规划链，并做一次构建验证。

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "起草 task read model contract 文档",
      "priority": "high",
      "status": "in_progress"
    },
    {
      "content": "起草 workspace/session/container summary contract 文档",
      "priority": "high",
      "status": "pending"
    },
    {
      "content": "起草 artifact preview contract 文档",
      "priority": "high",
      "status": "pending"
    },
    {
      "content": "把 contract 文档回链到现有规划文档",
      "priority": "medium",
      "status": "pending"
    },
    {
      "content": "更新今日 worklog 记录 contract 收敛",
      "priority": "high",
      "status": "pending"
    },
    {
      "content": "执行文档构建验证 contract 文档改动",
      "priority": "high",
      "status": "pending"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "起草 task read model contract 文档",
    "priority": "high",
    "status": "in_progress"
  },
  {
    "content": "起草 workspace/session/container summary contract 文档",
    "priority": "high",
    "status": "pending"
  },
  {
    "content": "起草 artifact preview contract 文档",
    "priority": "high",
    "status": "pending"
  },
  {
    "content": "把 contract 文档回链到现有规划文档",
    "priority": "medium",
    "status": "pending"
  },
  {
    "content": "更新今日 worklog 记录 contract 收敛",
    "priority": "high",
    "status": "pending"
  },
  {
    "content": "执行文档构建验证 contract 文档改动",
    "priority": "high",
    "status": "pending"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 79.2s)

直接落文，不再做额外探索。这批 contract 会尽量短、硬、可用于后续 architecture 和实现切片。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/task-read-model-contract.md\n+---\n+aliases:\n+  - Task Read Model Contract\n+  - Task Read Model 契约\n+tags:\n+  - scholar-agent\n+  - contract\n+  - task\n+  - read-model\n+  - implementation-plan\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# Task Read Model 契约\n+\n+> [!abstract]\n+> 本文档定义 next release 中 dashboard 所消费的 `task` 读模型契约。目标不是重写内部状态模型，而是固定前端真正需要看到的字段、字段分层、缺省规则和明确延期项，从而避免前端直接依赖当前 `ainrf` 的未来态字段或临时内部实现细节。\n+\n+## 契约结论\n+\n+- `task` 是 dashboard 的一级对象，所有首页列表、详情页、timeline、termination summary 都围绕它组织。\n+- read model 必须服务于展示和控制，而不是暴露全部内部状态细节。\n+- next release 的 task read model 应分成 5 个区块：identity、lifecycle、input summary、progress summary、result summary。\n+- 如果某些内部字段当前没有稳定数据源，不应为了契约完整性而伪造；应显式标为 optional 或 deferred。\n+\n+## 顶层结构\n+\n+task read model 至少应包含：\n+\n+```json\n+{\n+  \"identity\": {},\n+  \"lifecycle\": {},\n+  \"input_summary\": {},\n+  \"progress_summary\": {},\n+  \"result_summary\": {}\n+}\n+```\n+\n+## 1. identity\n+\n+用于回答“这个 task 是什么”。\n+\n+最低字段：\n+\n+- `task_id`\n+- `mode`\n+- `created_at`\n+- `updated_at`\n+\n+约束：\n+\n+- `task_id` 是前后端主键，必须稳定。\n+- `mode` 在 next release 只允许对应 bounded discovery / bounded reproduction 两类模式。\n+- 时间字段至少要支持列表排序和详情展示。\n+\n+## 2. lifecycle\n+\n+用于回答“这个 task 现在处于什么状态”。\n+\n+最低字段：\n+\n+- `status`\n+- `stage`\n+- `termination_reason`\n+- `active_gate`\n+\n+约束：\n+\n+- `status` 用于高层状态显示，例如 running / completed / failed / cancelled / blocked。\n+- `stage` 用于更细粒度展示当前所处阶段。\n+- `termination_reason` 在非终态任务中可为空，在终态任务中应尽量明确。\n+- `active_gate` 只作为当前待处理 gate 的摘要，不暴露全部 gate 内部实现细节。\n+\n+## 3. input_summary\n+\n+用于回答“这个 task 是围绕什么输入启动的”。\n+\n+最低字段：\n+\n+- `title`\n+- `brief`\n+- `seed_inputs`\n+- `target_inputs`\n+\n+约束：\n+\n+- `title` 是面向 dashboard 的人类可读标题，不要求等于内部 task name。\n+- `brief` 是 1-2 句短摘要，用于列表和详情页摘要。\n+- `seed_inputs` / `target_inputs` 用于概括 topic、seed paper、target paper、target result 等输入，不要求直接暴露所有原始 request payload。\n+\n+## 4. progress_summary\n+\n+用于回答“这个 task 做到哪一步了”。\n+\n+最低字段：\n+\n+- `current_checkpoint`\n+- `milestones`\n+- `recent_events`\n+- `artifact_counts`\n+\n+约束：\n+\n+- `current_checkpoint` 用于首页和详情页高亮当前进度位置。\n+- `milestones` 应服务 timeline 展示，不要求暴露所有原始 event。\n+- `recent_events` 是最近若干条可读事件摘要，而不是完整日志流。\n+- `artifact_counts` 用于任务摘要，不要求前端先理解全部 artifact graph。\n+\n+## 5. result_summary\n+\n+用于回答“这个 task 产出了什么，为什么结束”。\n+\n+最低字段：\n+\n+- `result_brief`\n+- `termination_reason`\n+- `recent_artifacts`\n+- `error_summary`\n+\n+约束：\n+\n+- `result_brief` 是对当前结果的简洁总结。\n+- `recent_artifacts` 只提供最适合预览的结果工件入口。\n+- `error_summary` 在失败、阻塞、取消时必须可见；在正常完成时可为空。\n+\n+## 列表页最小字段集\n+\n+首页任务列表至少需要：\n+\n+- `task_id`\n+- `mode`\n+- `title`\n+- `status`\n+- `stage`\n+- `updated_at`\n+- `termination_reason`\n+\n+说明：\n+\n+- 列表页不应依赖完整详情模型。\n+- 只要能支持排序、状态标签和点击进入详情即可。\n+\n+## 详情页最小字段集\n+\n+任务详情页至少需要：\n+\n+- identity 全量\n+- lifecycle 全量\n+- input_summary 全量\n+- progress_summary 全量\n+- result_summary 全量\n+\n+## 必须避免的错误\n+\n+- 让前端直接消费原始内部状态文件结构。\n+- 把尚未稳定的 runtime 字段写成 required。\n+- 为了“字段齐全”而发明没有真实来源的数据。\n+- 把 artifact graph 细节塞进 task summary。\n+\n+## Deferred\n+\n+- 全局 task analytics 字段。\n+- 完整预算趋势字段。\n+- 精细 token telemetry 字段。\n+- experiment runtime streaming 字段。\n+\n+## 对后续文档的回写要求\n+\n+- architecture baseline 应以本文作为 task 相关 frontend / backend contract 的最小基线。\n+- 后续 dashboard 设计稿应引用本文，而不是自行定义 task card shape。\n+\n+## 关联笔记\n+\n+- [[LLM-Working/architecture-baseline-plan]]\n+- [[LLM-Working/dashboard-baseline-spec]]\n+- [[LLM-Working/mode-baseline-spec]]\n+\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/workspace-session-container-summary-contract.md\n+---\n+aliases:\n+  - Workspace Session Container Summary Contract\n+  - Workspace / Session / Container 摘要契约\n+tags:\n+  - scholar-agent\n+  - contract\n+  - workspace\n+  - session\n+  - container\n+  - implementation-plan\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# Workspace / Session / Container 摘要契约\n+\n+> [!abstract]\n+> 本文档定义 next release 中 dashboard 对 workspace、session、container 的最小摘要契约。目标是让前端能够展示“任务在哪个执行上下文里运行、当前是否可连接、资源是否健康”，而不把这一层扩展成独立的 infra orchestrator 或云平台模型。\n+\n+## 契约结论\n+\n+- workspace、session、container 都是 task 的二级对象，不应在 next release 中演化为独立产品中心。\n+- dashboard 只需要它们的 summary contract，而不是完整编排模型。\n+- 这层的职责是可见、可诊断、可关联，不是调度和自动恢复平台。\n+\n+## 顶层结构\n+\n+```json\n+{\n+  \"workspace\": {},\n+  \"session\": {},\n+  \"container\": {},\n+  \"resource_snapshot\": {}\n+}\n+```\n+\n+## 1. workspace summary\n+\n+最低字段：\n+\n+- `workspace_id`\n+- `workspace_label`\n+- `project_dir`\n+\n+约束：\n+\n+- 前端只需要知道 task 对应哪个 workspace，以及该 workspace 的人类可读标识。\n+- 不要求 next release 暴露完整文件树或复杂目录索引。\n+\n+## 2. session summary\n+\n+最低字段：\n+\n+- `session_status`\n+- `connected`\n+- `recoverable`\n+\n+约束：\n+\n+- `session_status` 主要用于“当前是否有可用执行上下文”。\n+- `connected` 只表示当前是否可连，不要求表达完整会话历史。\n+- `recoverable` 用于帮助判断 task 是否还能继续。\n+\n+## 3. container summary\n+\n+最低字段：\n+\n+- `container_label`\n+- `ssh_available`\n+- `environment_status`\n+\n+约束：\n+\n+- `container_label` 用于人类可读识别。\n+- `ssh_available` 是 next release 的关键健康信号之一。\n+- `environment_status` 用于回答“当前环境是否可用于继续任务”。\n+\n+## 4. resource_snapshot\n+\n+最低字段：\n+\n+- `gpu`\n+- `cpu`\n+- `memory`\n+- `disk`\n+\n+约束：\n+\n+- 这是 snapshot，不是复杂时序分析。\n+- next release 只要求展示当前快照，不要求长期趋势图。\n+\n+## 首页最小展示要求\n+\n+- 当前 workspace 标识。\n+- 当前 session 是否可用。\n+- container / SSH 是否可用。\n+- GPU / CPU / memory / disk 快照。\n+\n+## 详情页最小展示要求\n+\n+- workspace label / project_dir。\n+- session 状态。\n+- container 健康摘要。\n+- resource snapshot。\n+\n+## 必须避免的错误\n+\n+- 把 workspace 设计成独立大模块，脱离 task 导航。\n+- 把 session 设计成复杂多会话编排模型。\n+- 把 container 扩展成生命周期管理平台。\n+- 为资源区块引入过重的 telemetry 平台。\n+\n+## Deferred\n+\n+- 多 container fleet 视图。\n+- 多 workspace 对比分析。\n+- 长期资源趋势图。\n+- 自动调度与自动恢复平台。\n+\n+## 关联笔记\n+\n+- [[LLM-Working/architecture-baseline-plan]]\n+- [[LLM-Working/dashboard-baseline-spec]]\n+\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/artifact-preview-contract.md\n+---\n+aliases:\n+  - Artifact Preview Contract\n+  - Artifact Preview 契约\n+tags:\n+  - scholar-agent\n+  - contract\n+  - artifact\n+  - preview\n+  - implementation-plan\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# Artifact Preview 契约\n+\n+> [!abstract]\n+> 本文档定义 next release 中 dashboard 对 artifact preview 的最小契约。目标是固定前端能预览哪些工件、需要哪些元信息、哪些内容必须延期，从而保证 artifact preview 成为 next release 的真实价值点，而不是继续依赖文件系统手工查看或膨胀成大型内容平台。\n+\n+## 契约结论\n+\n+- next release 的 artifact preview 只覆盖 tables、reports、figures 三类核心结果。\n+- preview 契约的重点是“可快速浏览结果”，不是“完整编辑或分析”。\n+- preview 所需元信息必须稳定、简短、可由 task 详情页直接消费。\n+\n+## 支持类型\n+\n+### 1. tables\n+\n+- 支持格式：CSV / Markdown。\n+- 用途：快速查看复现表格、对比结果、汇总表。\n+\n+### 2. reports\n+\n+- 支持格式：Markdown。\n+- 用途：快速查看结果报告、摘要和任务输出说明。\n+\n+### 3. figures\n+\n+- 支持格式：SVG / PNG。\n+- 用途：快速查看结果图和导出图形。\n+\n+## 每个 preview item 的最小元信息\n+\n+最低字段：\n+\n+- `artifact_id`\n+- `artifact_type`\n+- `display_title`\n+- `preview_format`\n+- `preview_ref`\n+\n+约束：\n+\n+- `artifact_id` 用于唯一识别。\n+- `artifact_type` 必须能区分 table / report / figure。\n+- `display_title` 用于 UI 列表和 modal 标题。\n+- `preview_format` 必须能直接映射到渲染组件。\n+- `preview_ref` 是内容引用，不要求直接暴露底层存储实现细节。\n+\n+## 首页最近 Artifacts 最小字段集\n+\n+- `artifact_id`\n+- `artifact_type`\n+- `display_title`\n+- `preview_format`\n+\n+说明：\n+\n+- 首页 recent artifacts 只做轻入口，不做复杂元数据面板。\n+\n+## 任务详情页 Artifact Preview 最小字段集\n+\n+- `artifact_id`\n+- `artifact_type`\n+- `display_title`\n+- `preview_format`\n+- `preview_ref`\n+- `created_at`\n+\n+## Preview 非目标\n+\n+- 不做 notebook viewer。\n+- 不做 artifact editor。\n+- 不做 artifact graph browser。\n+- 不做全局搜索平台。\n+\n+## 必须避免的错误\n+\n+- 为了 preview 引入复杂内容管理平台。\n+- 让前端直接猜文件类型和渲染方式。\n+- 把 preview 契约和底层文件系统结构硬绑定。\n+\n+## Deferred\n+\n+- PDF 复杂文档 viewer。\n+- 交互式图表分析器。\n+- 跨任务 artifact 搜索。\n+- artifact graph navigation。\n+\n+## 对后续文档的回写要求\n+\n+- architecture baseline 与正式 architecture 文档应引用本文作为 preview contract。\n+- dashboard 设计稿应以本文的三类支持格式为准，不自行扩大范围。\n+\n+## 关联笔记\n+\n+- [[LLM-Working/dashboard-baseline-spec]]\n+- [[LLM-Working/architecture-baseline-plan]]\n+\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/architecture-baseline-plan.md\n@@\n ## 当前建议的后续原子任务\n \n 1. 固定 task read model 给 dashboard 的字段清单。\n 2. 固定 workspace / session / container summary shape。\n 3. 固定 artifact preview metadata shape。\n 4. 决定 token telemetry 是否延期。\n 5. 起草正式 architecture 文档目录。\n+\n+## 当前契约入口\n+\n+- task 读模型以 `[[LLM-Working/task-read-model-contract]]` 为准。\n+- workspace / session / container 摘要以 `[[LLM-Working/workspace-session-container-summary-contract]]` 为准。\n+- artifact preview 以 `[[LLM-Working/artifact-preview-contract]]` 为准。\n@@\n - [[LLM-Working/project-realignment-manifesto-plan]]\n - [[LLM-Working/next-release-realignment-roadmap]]\n - [[LLM-Working/mode-baseline-spec]]\n - [[LLM-Working/dashboard-baseline-spec]]\n+- [[LLM-Working/task-read-model-contract]]\n+- [[LLM-Working/workspace-session-container-summary-contract]]\n+- [[LLM-Working/artifact-preview-contract]]\n - [[framework/v1-rfc]]\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A docs/LLM-Working/task-read-model-contract.md
A docs/LLM-Working/workspace-session-container-summary-contract.md
A docs/LLM-Working/artifact-preview-contract.md
M docs/LLM-Working/architecture-baseline-plan.md
```

---

## Assistant (Build · gpt-5.4 · 11.0s)

第一批 contract 文档已经写完并挂回 architecture baseline。下一步跑构建验证，然后补 worklog。

**Tool: bash**

**Input:**
```json
{
  "command": "UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build",
  "description": "Builds the HTML notes site",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```

[31m │  ⚠  Warning from the Material for MkDocs team[0m
[31m │[0m
[31m │[0m  MkDocs 2.0, the underlying framework of Material for MkDocs,
[31m │[0m  will introduce backward-incompatible changes, including:
[31m │[0m
[31m │  × [0mAll plugins will stop working – the plugin system has been removed
[31m │  × [0mAll theme overrides will break – the theming system has been rewritten
[31m │  × [0mNo migration path exists – existing projects cannot be upgraded
[31m │  × [0mClosed contribution model – community members can't report bugs
[31m │  × [0mCurrently unlicensed – unsuitable for production use
[31m │[0m
[31m │[0m  Our full analysis:
[31m │[0m
[31m │[0m  [4mhttps://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/[0m
[0m
INFO    -  MERMAID2  - Initialization arguments: {}
INFO    -  MERMAID2  - Using specified javascript library: assets/javascripts/vendor/mermaid-10.4.0.min.js
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /Users/kozmosa/code/scholar-agent/site
INFO    -  MERMAID2  - Found superfences config: {'custom_fences': [{'name': 'mermaid', 'class': 'mermaid', 'format': functools.partial(<function fence_mermaid at 0x101a18220>, custom=True)}]}
INFO    -  MERMAID2  - Found 'fence_mermaid_custom' function: activate custom loader for superfences
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI-Native Research Framework：有界自治研究系统蓝图': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '工件图谱架构：AI-Native Research Framework 的核心模型': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'V1：双模式有界自治研究引擎': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 RFC：有界自治研究引擎实现规格': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 Roadmap：实现路线图': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Academic Research Skills：从研究到发表的学术全流程管线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI Research SKILLs：AI 研究工程技能库': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'ArgusBot：面向 Codex 的监督式 Autoloop 控制层': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Auto-claude-code-research-in-sleep：过夜自治科研流水线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'autoresearch：自治 ML 实验迭代框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Awesome Claude Code Paper Proofreading：LaTeX 论文校对 prompt 工作流': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Code Deep Research：多阶段深度研究框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Scholar：学术研究与开发一体化个人配置系统': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Everything Claude Code：通用 Agent Harness 基线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'EvoScientist：多渠道统一控制面的自进化 AI 科学家工作台': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '学术研究 Agent 汇总研究报告': found 2 diagrams, adding scripts
INFO    -  Documentation built in 0.77 seconds

```

---

## Assistant (Build · gpt-5.4 · 17.1s)

验证通过。我补充 worklog，并收口当前 todo。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md\n@@\n - 2026-04-04 15:48 `docs-planning`：完成 `[[LLM-Working/dashboard-baseline-spec]]`，把 next release 的 dashboard 固定为单用户优先、task-centric 的 operator control plane，明确首页区块、任务详情页结构、artifact preview 格式、可观察性边界和 deferred 清单，并要求后续 architecture 围绕 task / workspace / session / artifact preview 组织，而不是继续围绕未来态完整 research platform 发散；同步把该规格回链到 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n - 2026-04-04 16:00 `docs-planning`：完成 `[[LLM-Working/architecture-baseline-plan]]`，把 next release 的实现边界收敛为围绕单用户 research dashboard 的 control plane 架构，固定 task、workspace、session、container、artifact preview、resource snapshot 等核心对象与模块责任，明确当前 `ainrf` 既有 API / state / gates / events / SSH health 是真实起点，并将完整 TaskEngine、全局 analytics、多用户权限和 artifact graph explorer 继续保留为 deferred；同步把该基线回链到 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 16:12 `docs-planning`：完成第一批实现契约文档：`[[LLM-Working/task-read-model-contract]]`、`[[LLM-Working/workspace-session-container-summary-contract]]`、`[[LLM-Working/artifact-preview-contract]]`，分别固定 dashboard 所消费的 task 读模型分层、workspace/session/container 的摘要契约，以及 tables / reports / figures 三类工件的 preview metadata；同时在 `[[LLM-Working/architecture-baseline-plan]]` 中补“当前契约入口”，形成从项目重定位、mode baseline、dashboard baseline、architecture baseline 到具体 contract 的完整规划链；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M docs/LLM-Working/worklog/2026-04-04.md
```

---

## Assistant (Build · gpt-5.4 · 9.1s)

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "起草 task read model contract 文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "起草 workspace/session/container summary contract 文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "起草 artifact preview contract 文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "把 contract 文档回链到现有规划文档",
      "priority": "medium",
      "status": "completed"
    },
    {
      "content": "更新今日 worklog 记录 contract 收敛",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "执行文档构建验证 contract 文档改动",
      "priority": "high",
      "status": "completed"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "起草 task read model contract 文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "起草 workspace/session/container summary contract 文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "起草 artifact preview contract 文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "把 contract 文档回链到现有规划文档",
    "priority": "medium",
    "status": "completed"
  },
  {
    "content": "更新今日 worklog 记录 contract 收敛",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "执行文档构建验证 contract 文档改动",
    "priority": "high",
    "status": "completed"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 26.8s)

继续完成了，这次已经开始进入你要的“contracts”层，而不是继续停留在高层规划。

**新增**
1. `docs/LLM-Working/task-read-model-contract.md`
2. `docs/LLM-Working/workspace-session-container-summary-contract.md`
3. `docs/LLM-Working/artifact-preview-contract.md`

**更新**
1. `docs/LLM-Working/architecture-baseline-plan.md`
2. `docs/LLM-Working/worklog/2026-04-04.md`

**这次具体写了什么**
**1. Task Read Model Contract**
`docs/LLM-Working/task-read-model-contract.md`

这份文档现在把 dashboard 消费的 `task` 读模型固定下来了。

它把 task read model 收敛成 5 个区块：

1. `identity`
2. `lifecycle`
3. `input_summary`
4. `progress_summary`
5. `result_summary`

并且明确了：

- 首页列表最小字段集需要什么
- 详情页最小字段集需要什么
- 哪些字段不能伪造
- 哪些应该 deferred

这个 contract 的价值在于：  
后面前端或 API 聚合层不需要再自己发明 task card shape 了。

**2. Workspace / Session / Container Summary Contract**
`docs/LLM-Working/workspace-session-container-summary-contract.md`

这份文档把 execution context 也压缩成了 dashboard 真正需要的最小摘要模型。

固定了这 4 组内容：

1. `workspace`
2. `session`
3. `container`
4. `resource_snapshot`

也明确了：

- 这层是 task 的二级对象
- 目标是可见、可诊断、可关联
- 不是把这套东西膨胀成 infra orchestrator

这个边界很重要，因为它会避免后面为了“展示 workspace/session/container”而滑向平台化过度设计。

**3. Artifact Preview Contract**
`docs/LLM-Working/artifact-preview-contract.md`

这份文档把 artifact preview 真正冻结下来了。

支持类型明确为：

- tables：CSV / Markdown
- reports：Markdown
- figures：SVG / PNG

每个 preview item 的最小元信息固定为：

- `artifact_id`
- `artifact_type`
- `display_title`
- `preview_format`
- `preview_ref`

同时明确不做：

- notebook viewer
- artifact editor
- graph browser
- 全局搜索平台

这一步很关键，因为 artifact preview 是你 next release 明确要求的硬价值点之一。

**4. Architecture Baseline 已挂接 contracts**
我在 `architecture-baseline-plan.md` 里新增了一个 `当前契约入口` 段落，明确写了：

- task 读模型以 `task-read-model-contract` 为准
- workspace/session/container 摘要以对应 contract 为准
- artifact preview 以对应 contract 为准

所以现在不是只有 planning 文档，而是已经开始形成一条真正能指导后续实现的 contract 链条了。

**验证**
我执行了：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build
```

结果：通过。

**当前我对项目状态的判断**
现在你这轮长期重构已经形成了一个比较完整的文档梯度：

1. `project-realignment-manifesto-plan`
   - 项目重新定位

2. `next-release-realignment-roadmap`
   - next release 范围与推进顺序

3. `mode-baseline-spec`
   - mode 边界

4. `dashboard-baseline-spec`
   - dashboard 边界

5. `architecture-baseline-plan`
   - 实现边界

6. contracts
   - `task-read-model-contract`
   - `workspace-session-container-summary-contract`
   - `artifact-preview-contract`

这已经不再只是“规划感很强”，而是开始进入“可以直接喂给后续 architecture / API / frontend 设计”的层次了。

**我现在要直接指出的一点**
你让继续写 contracts，这是对的。  
但到这个节点，继续无限写更多 contract，收益会开始下降。

因为现在最欠缺的已经不是“还缺几个 contract 文件”，而是：

- 这些 contract 如何映射到当前 `ainrf` 已有 API 和 state
- 哪些字段今天就有数据
- 哪些字段需要新增聚合接口或 read model 扩展

换句话说，下一步最自然的方向应该从“纯文档 contracts”转向：

**面向当前实现的 gap mapping**

也就是：

1. 现有 `ainrf` 已经能提供什么
2. 为满足这些 contracts 还缺什么
3. 哪些应该进 next release implementation slices

**我推荐的下一步**
最合理的下一轮，不是继续发散写更多 contract，而是写一份：

`contracts-to-current-ainrf-gap-plan`

这份文档应该做三件事：

1. 把现有 API / state / events / health 映射到当前 contracts
2. 标出缺口
3. 给出最小实现切片顺序

这一步会非常接近工程推进，而不会重新掉回大而空的规划。

如果你同意，我下一步就继续写这份 gap plan。

---

## User

move these doc files into a new sub-dir which contains all the documents that belongs to this refactoring plan

---

## Assistant (Build · gpt-5.4 · 15.4s)

_Thinking:_

**Considering patch application process**

I need to apply a patch for manual edits. I can use bash commands like `mkdir` to create directories after verifying the parent directory exists. Maybe I’ll consider moving files with `apply_patch`, as it supports moving within the update file. It seems I might need to create a subdirectory called `docs/LLM-Working/refactoring-plan`, but I should ask about the naming first. After that, I may need to update links in relevant files and inspect their directory structure.

我会把这批重构规划文档收拢到 `docs/LLM-Working/` 下的新子目录，并同步修正现有 wikilink，保持整个规划链可导航。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/docs/LLM-Working",
  "limit": 200,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/docs/LLM-Working</path>
<type>directory</type>
<entries>
architecture-baseline-plan.md
artifact-preview-contract.md
dashboard-baseline-spec.md
mode-baseline-spec.md
next-release-realignment-roadmap.md
p1-ssh-executor-smoke-checklist.md
p2-mineru-implementation-plan.md
p2-mineru-smoke-checklist.md
p3-artifact-state-store-impl.md
p3-artifact-state-store-implementation-plan.md
p4-fastapi-service-auth-impl.md
p4-fastapi-service-auth-implementation-plan.md
p5-human-gate-webhook-impl.md
p5-human-gate-webhook-implementation-plan.md
p6-sse-streaming-impl.md
p6-sse-streaming-implementation-plan.md
project-realignment-manifesto-plan.md
task-read-model-contract.md
worklog/
workspace-session-container-summary-contract.md

(20 entries)
</entries>
```

**Tool: grep**

**Input:**
```json
{
  "include": "*.md",
  "path": "/Users/kozmosa/code/scholar-agent/docs",
  "pattern": "project-realignment-manifesto-plan|next-release-realignment-roadmap|mode-baseline-spec|dashboard-baseline-spec|architecture-baseline-plan|task-read-model-contract|workspace-session-container-summary-contract|artifact-preview-contract"
}
```

**Output:**
```
Found 44 matches
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md:
  Line 16: - 2026-04-04 15:20 `docs-planning`：完成 scholar-agent 项目重定位与 next release 重对齐的首轮规划基线，新增 `[[LLM-Working/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/next-release-realignment-roadmap]]`，把项目主叙事收敛为“单用户优先的 agent-driven research dashboard”，固定 manifesto / framework / architecture / decision-log / roadmap 的职责边界、Mode 1 / Mode 2 baseline 重写方向，以及以单会话原子任务推进的路线图；同时在 `[[framework/index]]` 增加当前规划入口，便于后续从 framework 主线进入这组长期规划文档；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。
  Line 17: - 2026-04-04 15:35 `docs-planning`：完成 `[[LLM-Working/mode-baseline-spec]]`，把 next release 的 Mode 1 / Mode 2 从未来态蓝图收敛为 bounded discovery / bounded reproduction baseline，明确两种模式的最小输入、最小流程、最小输出、统一非目标、dashboard 共同要求，以及对后续 manifesto / roadmap / architecture 的回写约束；同步把该规格回链到 `[[LLM-Working/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。
  Line 18: - 2026-04-04 15:48 `docs-planning`：完成 `[[LLM-Working/dashboard-baseline-spec]]`，把 next release 的 dashboard 固定为单用户优先、task-centric 的 operator control plane，明确首页区块、任务详情页结构、artifact preview 格式、可观察性边界和 deferred 清单，并要求后续 architecture 围绕 task / workspace / session / artifact preview 组织，而不是继续围绕未来态完整 research platform 发散；同步把该规格回链到 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。
  Line 19: - 2026-04-04 16:00 `docs-planning`：完成 `[[LLM-Working/architecture-baseline-plan]]`，把 next release 的实现边界收敛为围绕单用户 research dashboard 的 control plane 架构，固定 task、workspace、session、container、artifact preview、resource snapshot 等核心对象与模块责任，明确当前 `ainrf` 既有 API / state / gates / events / SSH health 是真实起点，并将完整 TaskEngine、全局 analytics、多用户权限和 artifact graph explorer 继续保留为 deferred；同步把该基线回链到 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。
  Line 20: - 2026-04-04 16:12 `docs-planning`：完成第一批实现契约文档：`[[LLM-Working/task-read-model-contract]]`、`[[LLM-Working/workspace-session-container-summary-contract]]`、`[[LLM-Working/artifact-preview-contract]]`，分别固定 dashboard 所消费的 task 读模型分层、workspace/session/container 的摘要契约，以及 tables / reports / figures 三类工件的 preview metadata；同时在 `[[LLM-Working/architecture-baseline-plan]]` 中补“当前契约入口”，形成从项目重定位、mode baseline、dashboard baseline、architecture baseline 到具体 contract 的完整规划链；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/artifact-preview-contract.md:
  Line 108: - [[LLM-Working/dashboard-baseline-spec]]
  Line 109: - [[LLM-Working/architecture-baseline-plan]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/architecture-baseline-plan.md:
  Line 42: - `[[LLM-Working/mode-baseline-spec]]` 定义 Mode 1 / Mode 2 的 next release 边界。
  Line 43: - `[[LLM-Working/dashboard-baseline-spec]]` 定义 dashboard 的 next release 边界。
  Line 265: - task 读模型以 `[[LLM-Working/task-read-model-contract]]` 为准。
  Line 266: - workspace / session / container 摘要以 `[[LLM-Working/workspace-session-container-summary-contract]]` 为准。
  Line 267: - artifact preview 以 `[[LLM-Working/artifact-preview-contract]]` 为准。
  Line 271: - [[LLM-Working/project-realignment-manifesto-plan]]
  Line 272: - [[LLM-Working/next-release-realignment-roadmap]]
  Line 273: - [[LLM-Working/mode-baseline-spec]]
  Line 274: - [[LLM-Working/dashboard-baseline-spec]]
  Line 275: - [[LLM-Working/task-read-model-contract]]
  Line 276: - [[LLM-Working/workspace-session-container-summary-contract]]
  Line 277: - [[LLM-Working/artifact-preview-contract]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/workspace-session-container-summary-contract.md:
  Line 123: - [[LLM-Working/architecture-baseline-plan]]
  Line 124: - [[LLM-Working/dashboard-baseline-spec]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/task-read-model-contract.md:
  Line 176: - [[LLM-Working/architecture-baseline-plan]]
  Line 177: - [[LLM-Working/dashboard-baseline-spec]]
  Line 178: - [[LLM-Working/mode-baseline-spec]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md:
  Line 62: - dashboard 规格以后续 `[[LLM-Working/dashboard-baseline-spec]]` 为准。
  Line 91: - 具体输入、最小输出和非目标约束以 `[[LLM-Working/mode-baseline-spec]]` 为准。
  Line 98: - 具体输入、最小输出和非目标约束以 `[[LLM-Working/mode-baseline-spec]]` 为准。
  Line 128: - 以 `[[LLM-Working/architecture-baseline-plan]]` 作为当前实现边界基线。
  Line 180: - [[LLM-Working/project-realignment-manifesto-plan]]
  Line 185: - [[LLM-Working/mode-baseline-spec]]
  Line 186: - [[LLM-Working/dashboard-baseline-spec]]
  Line 187: - [[LLM-Working/architecture-baseline-plan]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/dashboard-baseline-spec.md:
  Line 244: - `[[LLM-Working/next-release-realignment-roadmap]]` 需要以本文为 dashboard 范围基线。
  Line 245: - `[[LLM-Working/mode-baseline-spec]]` 中对 dashboard 的共同要求，应以本文为更具体解释。
  Line 257: - [[LLM-Working/project-realignment-manifesto-plan]]
  Line 258: - [[LLM-Working/next-release-realignment-roadmap]]
  Line 259: - [[LLM-Working/mode-baseline-spec]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/project-realignment-manifesto-plan.md:
  Line 79: - 更具体的 baseline 约束以后续 `[[LLM-Working/mode-baseline-spec]]` 为准。
  Line 85: - 更具体的 baseline 约束以后续 `[[LLM-Working/mode-baseline-spec]]` 为准。
  Line 180: - [[LLM-Working/mode-baseline-spec]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/mode-baseline-spec.md:
  Line 221: - [[LLM-Working/project-realignment-manifesto-plan]]
  Line 222: - [[LLM-Working/next-release-realignment-roadmap]]

/Users/kozmosa/code/scholar-agent/docs/framework/index.md:
  Line 55: - 如果当前目标是对项目做重定位、requirements / expectations 重对齐，先读 [[LLM-Working/project-realignment-manifesto-plan]]。
  Line 56: - 如果当前目标是规划 next release 的 scope、原子任务和 dashboard baseline，接着读 [[LLM-Working/next-release-realignment-roadmap]]。
```

---

## Assistant (Build · gpt-5.4 · 98.5s)

_Thinking:_

**Planning file management**

I'm figuring out which subdirectory to move files into, like maybe docs/LLM-Working/refactoring-plan/ or project-realignment/. I'll need to use apply_patch for any file edits, and bash for making directories after confirming the parent exists. It sounds like apply_patch can help with moving files and updating links too, but I should probably create a subdirectory first. I might end up using apply_patch for multiple updates, but simpler options might be using bash commands. Still, I'll stick with apply_patch since that's recommended for manual edits.

**Organizing subdirectory files**

The user asked for a new subdirectory to hold all documents related to the refactoring plan, specifically at docs/LLM-Working/refactoring-plan/. I think I might need to update any references in the worklog path and ensure the links still work. I'll need to move eight specific files listed from a grep search, but I’m also considering whether to include future documents or add an index file in the subdirectory. Creating the directory and moving these files seems essential, and adding an index could help navigation, but maybe it's not necessary unless the user requests it.

**Updating directory structure**

I’m considering including an index with links because it might be really useful, even if it’s minimal. Having an index as an entry point for the new directory could help navigation. I also need to update the links to reflect the new subdirectory path. I wonder if I can use Obsidian wikilinks with the full path while also making them shorter using a relative path—especially since all existing links use the format `[[LLM-Working/...]]`.

我准备把这 8 份规划/contract 文档收拢到 `docs/LLM-Working/refactoring-plan/`，并顺手加一个 `index.md` 作为这组长期重构文档的入口。然后统一修正所有现有 wikilink。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/index.md\n+---\n+aliases:\n+  - Refactoring Plan Index\n+  - 重构规划索引\n+tags:\n+  - scholar-agent\n+  - refactoring-plan\n+  - index\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# 重构规划索引\n+\n+> [!abstract]\n+> 这一组文档用于推进 scholar-agent 的项目重定位、next release 范围冻结、dashboard/control-plane 架构收敛，以及与实现直接相关的 contract 设计。它们共同服务于当前这轮“文档重构 + requirements / expectations 重对齐”工作，而不是已有 P1-P6 的实现规划。\n+\n+## 阅读顺序\n+\n+- 先读 [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]，确认项目重定位与 manifesto 方向。\n+- 再读 [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]，确认 next release 的范围和推进阶段。\n+- 接着读 [[LLM-Working/refactoring-plan/mode-baseline-spec]] 与 [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]，确认模式与 dashboard 的产品边界。\n+- 再读 [[LLM-Working/refactoring-plan/architecture-baseline-plan]]，确认实现边界。\n+- 最后读 3 份 contract，确认后续实现需要遵守的最小前后端契约。\n+\n+## 文档索引\n+\n+- [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]\n+- [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]\n+- [[LLM-Working/refactoring-plan/mode-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]\n+- [[LLM-Working/refactoring-plan/task-read-model-contract]]\n+- [[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]\n+- [[LLM-Working/refactoring-plan/artifact-preview-contract]]\n+\n+## 关联笔记\n+\n+- [[framework/index]]\n+- [[LLM-Working/worklog/2026-04-04]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/project-realignment-manifesto-plan.md\n*** Move to: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/project-realignment-manifesto-plan.md\n@@\n-- 更具体的 baseline 约束以后续 `[[LLM-Working/mode-baseline-spec]]` 为准。\n+- 更具体的 baseline 约束以后续 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。\n@@\n-- 更具体的 baseline 约束以后续 `[[LLM-Working/mode-baseline-spec]]` 为准。\n+- 更具体的 baseline 约束以后续 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。\n@@\n-- [[LLM-Working/mode-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/mode-baseline-spec]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/next-release-realignment-roadmap.md\n*** Move to: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/next-release-realignment-roadmap.md\n@@\n-- dashboard 规格以后续 `[[LLM-Working/dashboard-baseline-spec]]` 为准。\n+- dashboard 规格以后续 `[[LLM-Working/refactoring-plan/dashboard-baseline-spec]]` 为准。\n@@\n-- 具体输入、最小输出和非目标约束以 `[[LLM-Working/mode-baseline-spec]]` 为准。\n+- 具体输入、最小输出和非目标约束以 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。\n@@\n-- 具体输入、最小输出和非目标约束以 `[[LLM-Working/mode-baseline-spec]]` 为准。\n+- 具体输入、最小输出和非目标约束以 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。\n@@\n-- 以 `[[LLM-Working/architecture-baseline-plan]]` 作为当前实现边界基线。\n+- 以 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]` 作为当前实现边界基线。\n@@\n-- [[LLM-Working/project-realignment-manifesto-plan]]\n+- [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]\n@@\n-- [[LLM-Working/mode-baseline-spec]]\n-- [[LLM-Working/dashboard-baseline-spec]]\n-- [[LLM-Working/architecture-baseline-plan]]\n+- [[LLM-Working/refactoring-plan/mode-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/mode-baseline-spec.md\n*** Move to: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/mode-baseline-spec.md\n@@\n-- manifesto 需要引用本文，作为 requirements / expectations 的模式约束。\n-- next release roadmap 需要引用本文，作为 must-have / deferred 划分依据。\n+- manifesto 需要引用本文，作为 requirements / expectations 的模式约束。\n+- next release roadmap 需要引用本文，作为 must-have / deferred 划分依据。\n@@\n-- [[LLM-Working/project-realignment-manifesto-plan]]\n-- [[LLM-Working/next-release-realignment-roadmap]]\n+- [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]\n+- [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/dashboard-baseline-spec.md\n*** Move to: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/dashboard-baseline-spec.md\n@@\n-- `[[LLM-Working/next-release-realignment-roadmap]]` 需要以本文为 dashboard 范围基线。\n-- `[[LLM-Working/mode-baseline-spec]]` 中对 dashboard 的共同要求，应以本文为更具体解释。\n+- `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]` 需要以本文为 dashboard 范围基线。\n+- `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 中对 dashboard 的共同要求，应以本文为更具体解释。\n@@\n-- [[LLM-Working/project-realignment-manifesto-plan]]\n-- [[LLM-Working/next-release-realignment-roadmap]]\n-- [[LLM-Working/mode-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]\n+- [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]\n+- [[LLM-Working/refactoring-plan/mode-baseline-spec]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/architecture-baseline-plan.md\n*** Move to: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/architecture-baseline-plan.md\n@@\n-- `[[LLM-Working/mode-baseline-spec]]` 定义 Mode 1 / Mode 2 的 next release 边界。\n-- `[[LLM-Working/dashboard-baseline-spec]]` 定义 dashboard 的 next release 边界。\n+- `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 定义 Mode 1 / Mode 2 的 next release 边界。\n+- `[[LLM-Working/refactoring-plan/dashboard-baseline-spec]]` 定义 dashboard 的 next release 边界。\n@@\n-- task 读模型以 `[[LLM-Working/task-read-model-contract]]` 为准。\n-- workspace / session / container 摘要以 `[[LLM-Working/workspace-session-container-summary-contract]]` 为准。\n-- artifact preview 以 `[[LLM-Working/artifact-preview-contract]]` 为准。\n+- task 读模型以 `[[LLM-Working/refactoring-plan/task-read-model-contract]]` 为准。\n+- workspace / session / container 摘要以 `[[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]` 为准。\n+- artifact preview 以 `[[LLM-Working/refactoring-plan/artifact-preview-contract]]` 为准。\n@@\n-- [[LLM-Working/project-realignment-manifesto-plan]]\n-- [[LLM-Working/next-release-realignment-roadmap]]\n-- [[LLM-Working/mode-baseline-spec]]\n-- [[LLM-Working/dashboard-baseline-spec]]\n-- [[LLM-Working/task-read-model-contract]]\n-- [[LLM-Working/workspace-session-container-summary-contract]]\n-- [[LLM-Working/artifact-preview-contract]]\n+- [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]\n+- [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]\n+- [[LLM-Working/refactoring-plan/mode-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/task-read-model-contract]]\n+- [[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]\n+- [[LLM-Working/refactoring-plan/artifact-preview-contract]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/task-read-model-contract.md\n*** Move to: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/task-read-model-contract.md\n@@\n-- [[LLM-Working/architecture-baseline-plan]]\n-- [[LLM-Working/dashboard-baseline-spec]]\n-- [[LLM-Working/mode-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]\n+- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/mode-baseline-spec]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/workspace-session-container-summary-contract.md\n*** Move to: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/workspace-session-container-summary-contract.md\n@@\n-- [[LLM-Working/architecture-baseline-plan]]\n-- [[LLM-Working/dashboard-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]\n+- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/artifact-preview-contract.md\n*** Move to: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/artifact-preview-contract.md\n@@\n-- [[LLM-Working/dashboard-baseline-spec]]\n-- [[LLM-Working/architecture-baseline-plan]]\n+- [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/framework/index.md\n@@\n-- 如果当前目标是对项目做重定位、requirements / expectations 重对齐，先读 [[LLM-Working/project-realignment-manifesto-plan]]。\n-- 如果当前目标是规划 next release 的 scope、原子任务和 dashboard baseline，接着读 [[LLM-Working/next-release-realignment-roadmap]]。\n+- 如果当前目标是对项目做重定位、requirements / expectations 重对齐，先读 [[LLM-Working/refactoring-plan/index]]。\n+- 如果当前目标是继续推进 next release 的 scope、contracts 和 dashboard / architecture baseline，也从 [[LLM-Working/refactoring-plan/index]] 进入。\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md\n@@\n-- 2026-04-04 15:20 `docs-planning`：完成 scholar-agent 项目重定位与 next release 重对齐的首轮规划基线，新增 `[[LLM-Working/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/next-release-realignment-roadmap]]`，把项目主叙事收敛为“单用户优先的 agent-driven research dashboard”，固定 manifesto / framework / architecture / decision-log / roadmap 的职责边界、Mode 1 / Mode 2 baseline 重写方向，以及以单会话原子任务推进的路线图；同时在 `[[framework/index]]` 增加当前规划入口，便于后续从 framework 主线进入这组长期规划文档；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n-- 2026-04-04 15:35 `docs-planning`：完成 `[[LLM-Working/mode-baseline-spec]]`，把 next release 的 Mode 1 / Mode 2 从未来态蓝图收敛为 bounded discovery / bounded reproduction baseline，明确两种模式的最小输入、最小流程、最小输出、统一非目标、dashboard 共同要求，以及对后续 manifesto / roadmap / architecture 的回写约束；同步把该规格回链到 `[[LLM-Working/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n-- 2026-04-04 15:48 `docs-planning`：完成 `[[LLM-Working/dashboard-baseline-spec]]`，把 next release 的 dashboard 固定为单用户优先、task-centric 的 operator control plane，明确首页区块、任务详情页结构、artifact preview 格式、可观察性边界和 deferred 清单，并要求后续 architecture 围绕 task / workspace / session / artifact preview 组织，而不是继续围绕未来态完整 research platform 发散；同步把该规格回链到 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n-- 2026-04-04 16:00 `docs-planning`：完成 `[[LLM-Working/architecture-baseline-plan]]`，把 next release 的实现边界收敛为围绕单用户 research dashboard 的 control plane 架构，固定 task、workspace、session、container、artifact preview、resource snapshot 等核心对象与模块责任，明确当前 `ainrf` 既有 API / state / gates / events / SSH health 是真实起点，并将完整 TaskEngine、全局 analytics、多用户权限和 artifact graph explorer 继续保留为 deferred；同步把该基线回链到 `[[LLM-Working/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n-- 2026-04-04 16:12 `docs-planning`：完成第一批实现契约文档：`[[LLM-Working/task-read-model-contract]]`、`[[LLM-Working/workspace-session-container-summary-contract]]`、`[[LLM-Working/artifact-preview-contract]]`，分别固定 dashboard 所消费的 task 读模型分层、workspace/session/container 的摘要契约，以及 tables / reports / figures 三类工件的 preview metadata；同时在 `[[LLM-Working/architecture-baseline-plan]]` 中补“当前契约入口”，形成从项目重定位、mode baseline、dashboard baseline、architecture baseline 到具体 contract 的完整规划链；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 15:20 `docs-planning`：完成 scholar-agent 项目重定位与 next release 重对齐的首轮规划基线，新增 `[[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]`，把项目主叙事收敛为“单用户优先的 agent-driven research dashboard”，固定 manifesto / framework / architecture / decision-log / roadmap 的职责边界、Mode 1 / Mode 2 baseline 重写方向，以及以单会话原子任务推进的路线图；同时在 `[[framework/index]]` 增加当前规划入口，便于后续从 framework 主线进入这组长期规划文档；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 15:35 `docs-planning`：完成 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]`，把 next release 的 Mode 1 / Mode 2 从未来态蓝图收敛为 bounded discovery / bounded reproduction baseline，明确两种模式的最小输入、最小流程、最小输出、统一非目标、dashboard 共同要求，以及对后续 manifesto / roadmap / architecture 的回写约束；同步把该规格回链到 `[[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 15:48 `docs-planning`：完成 `[[LLM-Working/refactoring-plan/dashboard-baseline-spec]]`，把 next release 的 dashboard 固定为单用户优先、task-centric 的 operator control plane，明确首页区块、任务详情页结构、artifact preview 格式、可观察性边界和 deferred 清单，并要求后续 architecture 围绕 task / workspace / session / artifact preview 组织，而不是继续围绕未来态完整 research platform 发散；同步把该规格回链到 `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 16:00 `docs-planning`：完成 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]`，把 next release 的实现边界收敛为围绕单用户 research dashboard 的 control plane 架构，固定 task、workspace、session、container、artifact preview、resource snapshot 等核心对象与模块责任，明确当前 `ainrf` 既有 API / state / gates / events / SSH health 是真实起点，并将完整 TaskEngine、全局 analytics、多用户权限和 artifact graph explorer 继续保留为 deferred；同步把该基线回链到 `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 16:12 `docs-planning`：完成第一批实现契约文档：`[[LLM-Working/refactoring-plan/task-read-model-contract]]`、`[[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]`、`[[LLM-Working/refactoring-plan/artifact-preview-contract]]`，分别固定 dashboard 所消费的 task 读模型分层、workspace/session/container 的摘要契约，以及 tables / reports / figures 三类工件的 preview metadata；同时在 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]` 中补“当前契约入口”，形成从项目重定位、mode baseline、dashboard baseline、architecture baseline 到具体 contract 的完整规划链；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A docs/LLM-Working/refactoring-plan/index.md
M docs/LLM-Working/refactoring-plan/project-realignment-manifesto-plan.md
M docs/LLM-Working/refactoring-plan/next-release-realignment-roadmap.md
M docs/LLM-Working/refactoring-plan/mode-baseline-spec.md
M docs/LLM-Working/refactoring-plan/dashboard-baseline-spec.md
M docs/LLM-Working/refactoring-plan/architecture-baseline-plan.md
M docs/LLM-Working/refactoring-plan/task-read-model-contract.md
M docs/LLM-Working/refactoring-plan/workspace-session-container-summary-contract.md
M docs/LLM-Working/refactoring-plan/artifact-preview-contract.md
M docs/framework/index.md
M docs/LLM-Working/worklog/2026-04-04.md
```

---

## Assistant (Build · gpt-5.4 · 12.6s)

文档已经移动并修正了主要链接。下一步我会跑一次全量内容搜索确认旧路径没有残留，再做构建验证。

**Tool: grep**

**Input:**
```json
{
  "include": "*.md",
  "path": "/Users/kozmosa/code/scholar-agent/docs",
  "pattern": "\\[\\[LLM-Working/(project-realignment-manifesto-plan|next-release-realignment-roadmap|mode-baseline-spec|dashboard-baseline-spec|architecture-baseline-plan|task-read-model-contract|workspace-session-container-summary-contract|artifact-preview-contract)\\]\\]"
}
```

**Output:**
```
No files found
```

**Tool: grep**

**Input:**
```json
{
  "include": "*.md",
  "path": "/Users/kozmosa/code/scholar-agent/docs",
  "pattern": "LLM-Working/refactoring-plan/(project-realignment-manifesto-plan|next-release-realignment-roadmap|mode-baseline-spec|dashboard-baseline-spec|architecture-baseline-plan|task-read-model-contract|workspace-session-container-summary-contract|artifact-preview-contract)"
}
```

**Output:**
```
Found 54 matches
/Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md:
  Line 16: - 2026-04-04 15:20 `docs-planning`：完成 scholar-agent 项目重定位与 next release 重对齐的首轮规划基线，新增 `[[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]`，把项目主叙事收敛为“单用户优先的 agent-driven research dashboard”，固定 manifesto / framework / architecture / decision-log / roadmap 的职责边界、Mode 1 / Mode 2 baseline 重写方向，以及以单会话原子任务推进的路线图；同时在 `[[framework/index]]` 增加当前规划入口，便于后续从 framework 主线进入这组长期规划文档；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。
  Line 17: - 2026-04-04 15:35 `docs-planning`：完成 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]`，把 next release 的 Mode 1 / Mode 2 从未来态蓝图收敛为 bounded discovery / bounded reproduction baseline，明确两种模式的最小输入、最小流程、最小输出、统一非目标、dashboard 共同要求，以及对后续 manifesto / roadmap / architecture 的回写约束；同步把该规格回链到 `[[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]` 与 `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。
  Line 18: - 2026-04-04 15:48 `docs-planning`：完成 `[[LLM-Working/refactoring-plan/dashboard-baseline-spec]]`，把 next release 的 dashboard 固定为单用户优先、task-centric 的 operator control plane，明确首页区块、任务详情页结构、artifact preview 格式、可观察性边界和 deferred 清单，并要求后续 architecture 围绕 task / workspace / session / artifact preview 组织，而不是继续围绕未来态完整 research platform 发散；同步把该规格回链到 `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。
  Line 19: - 2026-04-04 16:00 `docs-planning`：完成 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]`，把 next release 的实现边界收敛为围绕单用户 research dashboard 的 control plane 架构，固定 task、workspace、session、container、artifact preview、resource snapshot 等核心对象与模块责任，明确当前 `ainrf` 既有 API / state / gates / events / SSH health 是真实起点，并将完整 TaskEngine、全局 analytics、多用户权限和 artifact graph explorer 继续保留为 deferred；同步把该基线回链到 `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。
  Line 20: - 2026-04-04 16:12 `docs-planning`：完成第一批实现契约文档：`[[LLM-Working/refactoring-plan/task-read-model-contract]]`、`[[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]`、`[[LLM-Working/refactoring-plan/artifact-preview-contract]]`，分别固定 dashboard 所消费的 task 读模型分层、workspace/session/container 的摘要契约，以及 tables / reports / figures 三类工件的 preview metadata；同时在 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]` 中补“当前契约入口”，形成从项目重定位、mode baseline、dashboard baseline、architecture baseline 到具体 contract 的完整规划链；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/artifact-preview-contract.md:
  Line 108: - [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]
  Line 109: - [[LLM-Working/refactoring-plan/architecture-baseline-plan]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/workspace-session-container-summary-contract.md:
  Line 123: - [[LLM-Working/refactoring-plan/architecture-baseline-plan]]
  Line 124: - [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/architecture-baseline-plan.md:
  Line 42: - `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 定义 Mode 1 / Mode 2 的 next release 边界。
  Line 43: - `[[LLM-Working/refactoring-plan/dashboard-baseline-spec]]` 定义 dashboard 的 next release 边界。
  Line 265: - task 读模型以 `[[LLM-Working/refactoring-plan/task-read-model-contract]]` 为准。
  Line 266: - workspace / session / container 摘要以 `[[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]` 为准。
  Line 267: - artifact preview 以 `[[LLM-Working/refactoring-plan/artifact-preview-contract]]` 为准。
  Line 271: - [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]
  Line 272: - [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]
  Line 273: - [[LLM-Working/refactoring-plan/mode-baseline-spec]]
  Line 274: - [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]
  Line 275: - [[LLM-Working/refactoring-plan/task-read-model-contract]]
  Line 276: - [[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]
  Line 277: - [[LLM-Working/refactoring-plan/artifact-preview-contract]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/task-read-model-contract.md:
  Line 176: - [[LLM-Working/refactoring-plan/architecture-baseline-plan]]
  Line 177: - [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]
  Line 178: - [[LLM-Working/refactoring-plan/mode-baseline-spec]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/dashboard-baseline-spec.md:
  Line 244: - `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]` 需要以本文为 dashboard 范围基线。
  Line 245: - `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 中对 dashboard 的共同要求，应以本文为更具体解释。
  Line 257: - [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]
  Line 258: - [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]
  Line 259: - [[LLM-Working/refactoring-plan/mode-baseline-spec]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/next-release-realignment-roadmap.md:
  Line 62: - dashboard 规格以后续 `[[LLM-Working/refactoring-plan/dashboard-baseline-spec]]` 为准。
  Line 91: - 具体输入、最小输出和非目标约束以 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。
  Line 98: - 具体输入、最小输出和非目标约束以 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。
  Line 128: - 以 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]` 作为当前实现边界基线。
  Line 180: - [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]
  Line 185: - [[LLM-Working/refactoring-plan/mode-baseline-spec]]
  Line 186: - [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]
  Line 187: - [[LLM-Working/refactoring-plan/architecture-baseline-plan]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/mode-baseline-spec.md:
  Line 221: - [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]
  Line 222: - [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/project-realignment-manifesto-plan.md:
  Line 79: - 更具体的 baseline 约束以后续 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。
  Line 85: - 更具体的 baseline 约束以后续 `[[LLM-Working/refactoring-plan/mode-baseline-spec]]` 为准。
  Line 180: - [[LLM-Working/refactoring-plan/mode-baseline-spec]]

/Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/index.md:
  Line 20: - 先读 [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]，确认项目重定位与 manifesto 方向。
  Line 21: - 再读 [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]，确认 next release 的范围和推进阶段。
  Line 22: - 接着读 [[LLM-Working/refactoring-plan/mode-baseline-spec]] 与 [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]，确认模式与 dashboard 的产品边界。
  Line 23: - 再读 [[LLM-Working/refactoring-plan/architecture-baseline-plan]]，确认实现边界。
  Line 28: - [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]
  Line 29: - [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]
  Line 30: - [[LLM-Working/refactoring-plan/mode-baseline-spec]]
  Line 31: - [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]
  Line 32: - [[LLM-Working/refactoring-plan/architecture-baseline-plan]]
  Line 33: - [[LLM-Working/refactoring-plan/task-read-model-contract]]
  Line 34: - [[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]
  Line 35: - [[LLM-Working/refactoring-plan/artifact-preview-contract]]
```

---

## Assistant (Build · gpt-5.4 · 8.1s)

旧路径引用已经清干净了。最后跑一次文档构建，并把这次目录整理追加到 worklog。

**Tool: bash**

**Input:**
```json
{
  "command": "UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build",
  "description": "Builds the HTML notes site",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```

[31m │  ⚠  Warning from the Material for MkDocs team[0m
[31m │[0m
[31m │[0m  MkDocs 2.0, the underlying framework of Material for MkDocs,
[31m │[0m  will introduce backward-incompatible changes, including:
[31m │[0m
[31m │  × [0mAll plugins will stop working – the plugin system has been removed
[31m │  × [0mAll theme overrides will break – the theming system has been rewritten
[31m │  × [0mNo migration path exists – existing projects cannot be upgraded
[31m │  × [0mClosed contribution model – community members can't report bugs
[31m │  × [0mCurrently unlicensed – unsuitable for production use
[31m │[0m
[31m │[0m  Our full analysis:
[31m │[0m
[31m │[0m  [4mhttps://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/[0m
[0m
INFO    -  MERMAID2  - Initialization arguments: {}
INFO    -  MERMAID2  - Using specified javascript library: assets/javascripts/vendor/mermaid-10.4.0.min.js
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /Users/kozmosa/code/scholar-agent/site
INFO    -  MERMAID2  - Found superfences config: {'custom_fences': [{'name': 'mermaid', 'class': 'mermaid', 'format': functools.partial(<function fence_mermaid at 0x105784220>, custom=True)}]}
INFO    -  MERMAID2  - Found 'fence_mermaid_custom' function: activate custom loader for superfences
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI-Native Research Framework：有界自治研究系统蓝图': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '工件图谱架构：AI-Native Research Framework 的核心模型': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'V1：双模式有界自治研究引擎': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 RFC：有界自治研究引擎实现规格': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 Roadmap：实现路线图': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Academic Research Skills：从研究到发表的学术全流程管线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI Research SKILLs：AI 研究工程技能库': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'ArgusBot：面向 Codex 的监督式 Autoloop 控制层': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Auto-claude-code-research-in-sleep：过夜自治科研流水线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'autoresearch：自治 ML 实验迭代框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Awesome Claude Code Paper Proofreading：LaTeX 论文校对 prompt 工作流': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Code Deep Research：多阶段深度研究框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Scholar：学术研究与开发一体化个人配置系统': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Everything Claude Code：通用 Agent Harness 基线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'EvoScientist：多渠道统一控制面的自进化 AI 科学家工作台': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '学术研究 Agent 汇总研究报告': found 2 diagrams, adding scripts
INFO    -  Documentation built in 0.78 seconds

```

---

## Assistant (Build · gpt-5.4 · 16.9s)

构建通过。我补一条 worklog，说明这次把重构规划文档集中到新子目录并新增索引入口。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md\n@@\n - 2026-04-04 16:00 `docs-planning`：完成 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]`，把 next release 的实现边界收敛为围绕单用户 research dashboard 的 control plane 架构，固定 task、workspace、session、container、artifact preview、resource snapshot 等核心对象与模块责任，明确当前 `ainrf` 既有 API / state / gates / events / SSH health 是真实起点，并将完整 TaskEngine、全局 analytics、多用户权限和 artifact graph explorer 继续保留为 deferred；同步把该基线回链到 `[[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]`；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n - 2026-04-04 16:12 `docs-planning`：完成第一批实现契约文档：`[[LLM-Working/refactoring-plan/task-read-model-contract]]`、`[[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]`、`[[LLM-Working/refactoring-plan/artifact-preview-contract]]`，分别固定 dashboard 所消费的 task 读模型分层、workspace/session/container 的摘要契约，以及 tables / reports / figures 三类工件的 preview metadata；同时在 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]` 中补“当前契约入口”，形成从项目重定位、mode baseline、dashboard baseline、architecture baseline 到具体 contract 的完整规划链；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 16:26 `docs-refactor`：将本轮长期重构相关的 8 份规划与 contract 文档统一迁入 `docs/LLM-Working/refactoring-plan/`，新增 `[[LLM-Working/refactoring-plan/index]]` 作为这一组文档的集中入口，并同步修正 `framework/index`、worklog 和各规划文档之间的 wikilink，避免 `LLM-Working/` 根目录继续混放实现规划与长期重构规划；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M docs/LLM-Working/worklog/2026-04-04.md
```

---

## Assistant (Build · gpt-5.4 · 16.7s)

已经完成整理，这批文档现在被收拢到一个新的子目录里了。

**新目录**
`docs/LLM-Working/refactoring-plan/`

**移动进去的文件**
1. `project-realignment-manifesto-plan.md`
2. `next-release-realignment-roadmap.md`
3. `mode-baseline-spec.md`
4. `dashboard-baseline-spec.md`
5. `architecture-baseline-plan.md`
6. `task-read-model-contract.md`
7. `workspace-session-container-summary-contract.md`
8. `artifact-preview-contract.md`

**新增**
1. `docs/LLM-Working/refactoring-plan/index.md`

这个 `index.md` 现在作为这组长期重构/重对齐文档的统一入口。

**同步做了这些修正**
1. 更新了这些文档之间的所有主要 wikilink
2. 更新了 `docs/framework/index.md`
   - 现在直接指向 `[[LLM-Working/refactoring-plan/index]]`
3. 更新了 `docs/LLM-Working/worklog/2026-04-04.md`
   - 把旧路径全部改成新路径
   - 并追加了一条“文档迁移到新子目录”的记录

**验证**
我做了两步验证：

1. 搜索旧 wikilink 路径
   - 没有残留旧形式的 `[[LLM-Working/<旧文件名>]]`

2. 重新构建文档
```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build
```

结果：通过。

**当前结果**
现在 `docs/LLM-Working/` 被分成了更清晰的两类内容：

1. 原有实现规划/实现记录
   - `p1` 到 `p6` 相关文档
   - `worklog/`

2. 这轮长期重构规划
   - `refactoring-plan/`

这个整理方向是对的，后面继续推进 manifesto、architecture、gap plan 等内容，也都应该优先放进这个子目录里。

**建议的下一步**
既然这组文档已经被集中起来，下一步最自然的是继续在这个目录里新增：

1. `contracts-to-current-ainrf-gap-plan.md`

这样后续工作就会变成：

- 从规划与 contract
- 进入 gap mapping
- 再进入 implementation slices

如果你要，我下一步就继续写这份 gap plan。

---

## User

continue write

---

## Assistant (Build · gpt-5.4 · 13.2s)

_Thinking:_

**Continuing the gap plan**

I need to write more on the gap plan. It's likely important to send out commentary before I dive into the substantial work. I think updating my to-do list will help keep me organized as I move forward. So, I'll make sure to address these actions soon and ensure everything is on track. It's all about staying focused and ensuring I get this done effectively!

我继续在 `refactoring-plan/` 下往工程推进，新增一份 `contracts-to-current-ainrf-gap-plan`，把现有 `ainrf` 能力和刚冻结的 contracts 对齐，标出 next release 的真实缺口与实现切片。

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "起草 contracts-to-current-ainrf gap plan 文档",
      "priority": "high",
      "status": "in_progress"
    },
    {
      "content": "将 gap plan 回链到现有 refactoring-plan 文档",
      "priority": "medium",
      "status": "pending"
    },
    {
      "content": "更新 refactoring-plan 索引纳入 gap plan",
      "priority": "medium",
      "status": "pending"
    },
    {
      "content": "更新今日 worklog 记录 gap mapping",
      "priority": "high",
      "status": "pending"
    },
    {
      "content": "执行文档构建验证 gap plan 改动",
      "priority": "high",
      "status": "pending"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "起草 contracts-to-current-ainrf gap plan 文档",
    "priority": "high",
    "status": "in_progress"
  },
  {
    "content": "将 gap plan 回链到现有 refactoring-plan 文档",
    "priority": "medium",
    "status": "pending"
  },
  {
    "content": "更新 refactoring-plan 索引纳入 gap plan",
    "priority": "medium",
    "status": "pending"
  },
  {
    "content": "更新今日 worklog 记录 gap mapping",
    "priority": "high",
    "status": "pending"
  },
  {
    "content": "执行文档构建验证 gap plan 改动",
    "priority": "high",
    "status": "pending"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 10.3s)

先快速核对一下当前 `src/ainrf/` 目录，确保这份 gap plan 真正贴近现状，而不是只根据之前的印象来写。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/src/ainrf",
  "limit": 220,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/src/ainrf</path>
<type>directory</type>
<entries>
__init__.py
__main__.py
__pycache__/
api/
artifacts/
cli.py
events/
execution/
gates/
logging.py
parsing/
server.py
state/

(13 entries)
</entries>
```

**Tool: glob**

**Input:**
```json
{
  "path": "/Users/kozmosa/code/scholar-agent/src/ainrf",
  "pattern": "**/*.py"
}
```

**Output:**
```
/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py
/Users/kozmosa/code/scholar-agent/src/ainrf/events/store.py
/Users/kozmosa/code/scholar-agent/src/ainrf/gates/manager.py
/Users/kozmosa/code/scholar-agent/src/ainrf/events/__init__.py
/Users/kozmosa/code/scholar-agent/src/ainrf/events/service.py
/Users/kozmosa/code/scholar-agent/src/ainrf/api/dependencies.py
/Users/kozmosa/code/scholar-agent/src/ainrf/api/app.py
/Users/kozmosa/code/scholar-agent/src/ainrf/api/config.py
/Users/kozmosa/code/scholar-agent/src/ainrf/events/models.py
/Users/kozmosa/code/scholar-agent/src/ainrf/state/models.py
/Users/kozmosa/code/scholar-agent/src/ainrf/state/store.py
/Users/kozmosa/code/scholar-agent/src/ainrf/server.py
/Users/kozmosa/code/scholar-agent/src/ainrf/cli.py
/Users/kozmosa/code/scholar-agent/src/ainrf/artifacts/models.py
/Users/kozmosa/code/scholar-agent/src/ainrf/gates/errors.py
/Users/kozmosa/code/scholar-agent/src/ainrf/gates/__init__.py
/Users/kozmosa/code/scholar-agent/src/ainrf/gates/models.py
/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/__init__.py
/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/health.py
/Users/kozmosa/code/scholar-agent/src/ainrf/api/schemas.py
/Users/kozmosa/code/scholar-agent/src/ainrf/artifacts/__init__.py
/Users/kozmosa/code/scholar-agent/src/ainrf/api/middleware.py
/Users/kozmosa/code/scholar-agent/src/ainrf/api/__init__.py
/Users/kozmosa/code/scholar-agent/src/ainrf/parsing/errors.py
/Users/kozmosa/code/scholar-agent/src/ainrf/parsing/contracts.py
/Users/kozmosa/code/scholar-agent/src/ainrf/parsing/mineru.py
/Users/kozmosa/code/scholar-agent/src/ainrf/parsing/__init__.py
/Users/kozmosa/code/scholar-agent/src/ainrf/parsing/cache.py
/Users/kozmosa/code/scholar-agent/src/ainrf/parsing/models.py
/Users/kozmosa/code/scholar-agent/src/ainrf/state/errors.py
/Users/kozmosa/code/scholar-agent/src/ainrf/state/__init__.py
/Users/kozmosa/code/scholar-agent/src/ainrf/logging.py
/Users/kozmosa/code/scholar-agent/src/ainrf/execution/ssh.py
/Users/kozmosa/code/scholar-agent/src/ainrf/execution/errors.py
/Users/kozmosa/code/scholar-agent/src/ainrf/execution/__init__.py
/Users/kozmosa/code/scholar-agent/src/ainrf/execution/models.py
/Users/kozmosa/code/scholar-agent/src/ainrf/artifacts/transitions.py
/Users/kozmosa/code/scholar-agent/src/ainrf/__main__.py
/Users/kozmosa/code/scholar-agent/src/ainrf/__init__.py
/Users/kozmosa/code/scholar-agent/src/ainrf/artifacts/errors.py
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py",
  "limit": 260,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/tasks.py</path>
<type>file</type>
<content>1: from __future__ import annotations
2: 
3: import asyncio
4: from collections import Counter
5: from collections.abc import AsyncIterator
6: from datetime import UTC, datetime
7: import json
8: import logging
9: import time
10: from uuid import uuid4
11: 
12: from fastapi import APIRouter, HTTPException, Query, Request, Response, status
13: from starlette.responses import StreamingResponse
14: 
15: from ainrf.api.dependencies import get_api_config, get_event_service, get_gate_manager, get_state_store
16: from ainrf.api.schemas import (
17:     ActiveGateResponse,
18:     ArtifactItemResponse,
19:     ArtifactSummaryResponse,
20:     GateRecordResponse,
21:     TaskActionResponse,
22:     TaskArtifactsResponse,
23:     TaskCreateRequest,
24:     TaskCreateResponse,
25:     TaskDetailResponse,
26:     TaskListResponse,
27:     TaskRejectRequest,
28:     TaskSummaryResponse,
29: )
30: from ainrf.artifacts import ArtifactRecord, ArtifactType, GateType, HumanGate, HumanGateStatus
31: from ainrf.events import TaskEvent, TaskEventCategory, TaskEventService
32: from ainrf.gates import GateConflictError, GateNotFoundError, GateResolutionError, IntakeGatePayload
33: from ainrf.state import ArtifactQuery, JsonStateStore, TaskCheckpoint, TaskRecord, TaskStage
34: 
35: logger = logging.getLogger(__name__)
36: 
37: router = APIRouter(prefix="/tasks", tags=["tasks"])
38: 
39: _TERMINAL_STAGES = {TaskStage.COMPLETED, TaskStage.FAILED, TaskStage.CANCELLED}
40: 
41: 
42: def _utc_now() -> datetime:
43:     return datetime.now(UTC)
44: 
45: 
46: def _build_task_id() -> str:
47:     timestamp = _utc_now().strftime("%Y%m%d%H%M%S")
48:     return f"t-{timestamp}-{uuid4().hex[:8]}"
49: 
50: 
51: def _task_summary(task: TaskRecord) -> TaskSummaryResponse:
52:     return TaskSummaryResponse(
53:         task_id=task.task_id,
54:         mode=task.mode,
55:         status=task.status,
56:         created_at=task.created_at,
57:         updated_at=task.updated_at,
58:         current_stage=task.checkpoint.current_stage,
59:         termination_reason=task.termination_reason,
60:     )
61: 
62: 
63: def _artifact_summary(artifacts: list[ArtifactRecord]) -> ArtifactSummaryResponse:
64:     counts = Counter(artifact.artifact_type.value for artifact in artifacts)
65:     return ArtifactSummaryResponse(counts=dict(counts), total=sum(counts.values()))
66: 
67: 
68: def _artifact_item(artifact: ArtifactRecord) -> ArtifactItemResponse:
69:     raw_payload = artifact.model_dump(mode="json")
70:     status_value = raw_payload.get("status")
71:     return ArtifactItemResponse(
72:         artifact_id=artifact.artifact_id,
73:         artifact_type=artifact.artifact_type,
74:         source_task_id=artifact.source_task_id,
75:         summary=artifact.summary,
76:         status=status_value if isinstance(status_value, str) else None,
77:         payload=raw_payload,
78:     )
79: 
80: 
81: def _active_gate_response(active_gate: HumanGate | None) -> ActiveGateResponse | None:
82:     if active_gate is None:
83:         return None
84:     return ActiveGateResponse(
85:         gate_id=active_gate.artifact_id,
86:         gate_type=active_gate.gate_type,
87:         status=active_gate.status,
88:         summary=active_gate.summary,
89:         payload=active_gate.payload,
90:         deadline_at=active_gate.deadline_at,
91:         resolved_at=active_gate.resolved_at,
92:         reminder_sent_at=active_gate.reminder_sent_at,
93:         feedback=active_gate.feedback,
94:         auto_approved=active_gate.auto_approved,
95:     )
96: 
97: 
98: def _task_artifacts(store: JsonStateStore, task_id: str) -> list[ArtifactRecord]:
99:     artifacts: list[ArtifactRecord] = []
100:     for artifact_type in ArtifactType:
101:         artifacts.extend(store.query_artifacts(artifact_type, ArtifactQuery(source_task_id=task_id)))
102:     return artifacts
103: 
104: 
105: def _load_task_or_404(store: JsonStateStore, task_id: str) -> TaskRecord:
106:     task = store.load_task(task_id)
107:     if task is None:
108:         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
109:     return task
110: 
111: 
112: def _artifact_event_payload(artifact: ArtifactRecord) -> dict[str, object]:
113:     status_value = getattr(artifact, "status", None)
114:     return {
115:         "artifact_id": artifact.artifact_id,
116:         "artifact_type": artifact.artifact_type.value,
117:         "status": status_value.value if hasattr(status_value, "value") else status_value,
118:         "summary": artifact.summary,
119:     }
120: 
121: 
122: def _gate_event_payload(gate: HumanGate) -> dict[str, object]:
123:     return {
124:         "gate_id": gate.artifact_id,
125:         "gate_type": gate.gate_type.value,
126:         "status": gate.status.value,
127:         "summary": gate.summary,
128:         "payload": gate.payload,
129:         "deadline_at": gate.deadline_at.isoformat() if gate.deadline_at is not None else None,
130:         "resolved_at": gate.resolved_at.isoformat() if gate.resolved_at is not None else None,
131:         "reminder_sent_at": gate.reminder_sent_at.isoformat()
132:         if gate.reminder_sent_at is not None
133:         else None,
134:         "feedback": gate.feedback,
135:         "auto_approved": gate.auto_approved,
136:     }
137: 
138: 
139: def _publish_task_stage_events(
140:     *,
141:     event_service: TaskEventService,
142:     previous_stage: TaskStage,
143:     updated_task: TaskRecord,
144: ) -> None:
145:     event_service.publish(
146:         task_id=updated_task.task_id,
147:         category=TaskEventCategory.TASK,
148:         event="task.stage_changed",
149:         payload={
150:             "previous_stage": previous_stage.value,
151:             "current_stage": updated_task.status.value,
152:             "termination_reason": updated_task.termination_reason,
153:         },
154:     )
155:     terminal_event: str | None = None
156:     if updated_task.status is TaskStage.CANCELLED:
157:         terminal_event = "task.cancelled"
158:     elif updated_task.status is TaskStage.FAILED:
159:         terminal_event = "task.failed"
160:     elif updated_task.status is TaskStage.COMPLETED:
161:         terminal_event = "task.completed"
162:     if terminal_event is not None:
163:         event_service.publish(
164:             task_id=updated_task.task_id,
165:             category=TaskEventCategory.TASK,
166:             event=terminal_event,
167:             payload={
168:                 "current_stage": updated_task.status.value,
169:                 "termination_reason": updated_task.termination_reason,
170:             },
171:         )
172: 
173: 
174: def _parse_event_categories(raw_types: str | None) -> set[TaskEventCategory] | None:
175:     if raw_types is None or not raw_types.strip():
176:         return None
177:     categories: set[TaskEventCategory] = set()
178:     for value in raw_types.split(","):
179:         normalized = value.strip()
180:         if not normalized:
181:             continue
182:         try:
183:             categories.add(TaskEventCategory(normalized))
184:         except ValueError as exc:
185:             raise HTTPException(
186:                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
187:                 detail=f"Unsupported event type filter: {normalized}",
188:             ) from exc
189:     return categories or None
190: 
191: 
192: def _parse_last_event_id(raw_value: str | None) -> int | None:
193:     if raw_value is None:
194:         return None
195:     try:
196:         value = int(raw_value)
197:     except ValueError as exc:
198:         raise HTTPException(
199:             status_code=status.HTTP_400_BAD_REQUEST,
200:             detail="Last-Event-ID must be an integer",
201:         ) from exc
202:     if value < 0:
203:         raise HTTPException(
204:             status_code=status.HTTP_400_BAD_REQUEST,
205:             detail="Last-Event-ID must be non-negative",
206:         )
207:     return value
208: 
209: 
210: def _encode_sse(event: TaskEvent) -> str:
211:     return (
212:         f"id: {event.event_id}\n"
213:         f"event: {event.event}\n"
214:         f"data: {json.dumps(event.model_dump(mode='json'), ensure_ascii=False)}\n\n"
215:     )
216: 
217: 
218: @router.post("", response_model=TaskCreateResponse, status_code=status.HTTP_201_CREATED)
219: async def create_task(request: Request, payload: TaskCreateRequest) -> TaskCreateResponse:
220:     store = get_state_store(request)
221:     gate_manager = get_gate_manager(request)
222:     task_id = _build_task_id()
223:     now = _utc_now()
224:     task = TaskRecord(
225:         task_id=task_id,
226:         mode=payload.mode,
227:         status=TaskStage.SUBMITTED,
228:         created_at=now,
229:         updated_at=now,
230:         config=payload.model_dump(mode="json"),
231:         checkpoint=TaskCheckpoint(current_stage=TaskStage.SUBMITTED),
232:         budget_limit=payload.budget,
233:         budget_used=payload.budget.model_copy(
234:             update={"gpu_hours": 0.0, "api_cost_usd": 0.0, "wall_clock_hours": 0.0}
235:         ),
236:     )
237:     store.save_task(task)
238:     gate_manager.register_secret(task_id, payload.webhook_secret)
239: 
240:     intake_payload = IntakeGatePayload(
241:         mode=payload.mode.value,
242:         paper_titles=[paper.title for paper in payload.papers],
243:         paper_count=len(payload.papers),
244:         yolo=payload.yolo,
245:     )
246:     updated_task, gate = await gate_manager.trigger_gate(
247:         task=task,
248:         gate_type=GateType.INTAKE,
249:         summary=f"Review intake for {len(payload.papers)} paper(s)",
250:         payload=intake_payload.model_dump(mode="json"),
251:         yolo=payload.yolo,
252:     )
253:     if not payload.yolo:
254:         try:
255:             await gate_manager.send_waiting_webhook(task=updated_task, gate=gate)
256:         except Exception:
257:             logger.exception("Failed to deliver intake gate webhook", extra={"task_id": task_id})
258: 
259:     return TaskCreateResponse(task_id=task_id, status=updated_task.status)
260: 

(Showing lines 1-260 of 466. Use offset=261 to continue.)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/health.py",
  "limit": 220,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/src/ainrf/api/routes/health.py</path>
<type>file</type>
<content>1: from __future__ import annotations
2: 
3: from fastapi import APIRouter, Request, status
4: from fastapi.responses import JSONResponse
5: 
6: from ainrf.api.dependencies import get_api_config
7: from ainrf.api.schemas import ApiStatus, HealthResponse
8: from ainrf.execution import SSHExecutor
9: 
10: router = APIRouter()
11: 
12: 
13: @router.get("/health", response_model=HealthResponse)
14: async def health_check(request: Request) -> JSONResponse | HealthResponse:
15:     api_config = get_api_config(request)
16:     payload = api_config.as_public_health_payload()
17:     container_config = api_config.container_config
18:     if container_config is None:
19:         return HealthResponse(status=ApiStatus.OK, **payload)
20: 
21:     executor = SSHExecutor(container_config)
22:     health = await executor.ping()
23:     response = HealthResponse(
24:         status=ApiStatus.OK if health.ssh_ok else ApiStatus.DEGRADED,
25:         container_health={
26:             "ssh_ok": health.ssh_ok,
27:             "claude_ok": health.claude_ok,
28:             "anthropic_api_key_ok": health.anthropic_api_key_ok,
29:             "project_dir_writable": health.project_dir_writable,
30:             "claude_version": health.claude_version,
31:             "gpu_models": health.gpu_models,
32:             "cuda_version": health.cuda_version,
33:             "disk_free_bytes": health.disk_free_bytes,
34:             "warnings": health.warnings,
35:         },
36:         detail=None if health.ssh_ok else "Container connectivity degraded",
37:         **payload,
38:     )
39:     if health.ssh_ok:
40:         return response
41:     return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=response.model_dump(mode="json"))

(End of file - total 41 lines)
</content>
```

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/src/ainrf/api/schemas.py",
  "limit": 320,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/src/ainrf/api/schemas.py</path>
<type>file</type>
<content>1: from __future__ import annotations
2: 
3: from datetime import datetime
4: from enum import StrEnum
5: from typing import Any
6: 
7: from pydantic import BaseModel, ConfigDict, Field, model_validator
8: 
9: from ainrf.artifacts import ArtifactType, GateType, HumanGateStatus, ResourceUsage
10: from ainrf.state import TaskMode, TaskStage
11: 
12: 
13: class PaperRole(StrEnum):
14:     SEED = "seed"
15:     TARGET = "target"
16: 
17: 
18: class ModeTwoScope(StrEnum):
19:     CORE_ONLY = "core-only"
20:     FULL_SUITE = "full-suite"
21: 
22: 
23: class ApiStatus(StrEnum):
24:     OK = "ok"
25:     DEGRADED = "degraded"
26: 
27: 
28: class PaperInput(BaseModel):
29:     model_config = ConfigDict(extra="forbid")
30: 
31:     title: str
32:     pdf_url: str | None = None
33:     pdf_path: str | None = None
34:     role: PaperRole
35: 
36:     @model_validator(mode="after")
37:     def validate_pdf_source(self) -> PaperInput:
38:         if not self.pdf_url and not self.pdf_path:
39:             raise ValueError("Either pdf_url or pdf_path must be provided")
40:         return self
41: 
42: 
43: class ModeOneConfig(BaseModel):
44:     model_config = ConfigDict(extra="forbid")
45: 
46:     domain_context: str | None = None
47:     max_depth: int = 3
48:     focus_directions: list[str] = Field(default_factory=list)
49:     ignore_directions: list[str] = Field(default_factory=list)
50: 
51: 
52: class ModeTwoConfig(BaseModel):
53:     model_config = ConfigDict(extra="forbid")
54: 
55:     scope: ModeTwoScope = ModeTwoScope.CORE_ONLY
56:     target_tables: list[str] = Field(default_factory=list)
57:     baseline_first: bool = True
58: 
59: 
60: class TaskConfigInput(BaseModel):
61:     model_config = ConfigDict(extra="forbid")
62: 
63:     mode_1: ModeOneConfig | None = None
64:     mode_2: ModeTwoConfig | None = None
65: 
66: 
67: class ContainerInput(BaseModel):
68:     model_config = ConfigDict(extra="forbid")
69: 
70:     host: str
71:     port: int = 22
72:     user: str
73:     ssh_key_path: str | None = None
74:     project_dir: str
75: 
76: 
77: class TaskCreateRequest(BaseModel):
78:     model_config = ConfigDict(
79:         extra="forbid",
80:         json_schema_extra={
81:             "example": {
82:                 "mode": "deep_reproduction",
83:                 "papers": [
84:                     {
85:                         "title": "Attention Is All You Need",
86:                         "pdf_url": "https://arxiv.org/pdf/1706.03762",
87:                         "role": "target",
88:                     }
89:                 ],
90:                 "config": {
91:                     "mode_2": {
92:                         "scope": "core-only",
93:                         "target_tables": ["Table 1"],
94:                         "baseline_first": True,
95:                     }
96:                 },
97:                 "container": {
98:                     "host": "gpu-server-01",
99:                     "port": 22,
100:                     "user": "researcher",
101:                     "ssh_key_path": "/path/to/id_rsa",
102:                     "project_dir": "/workspace/projects/attention-study",
103:                 },
104:                 "budget": {
105:                     "gpu_hours": 24,
106:                     "api_cost_usd": 50,
107:                     "wall_clock_hours": 48,
108:                 },
109:                 "yolo": False,
110:                 "webhook_url": "https://example.com/hooks/ainrf",
111:                 "webhook_secret": "hmac-shared-secret",
112:             }
113:         },
114:     )
115: 
116:     mode: TaskMode
117:     papers: list[PaperInput] = Field(min_length=1)
118:     config: TaskConfigInput = Field(default_factory=TaskConfigInput)
119:     container: ContainerInput
120:     budget: ResourceUsage
121:     yolo: bool = False
122:     webhook_url: str | None = None
123:     webhook_secret: str | None = None
124: 
125: 
126: class GateRecordResponse(BaseModel):
127:     model_config = ConfigDict(extra="forbid")
128: 
129:     gate_id: str
130:     gate_type: GateType
131:     status: HumanGateStatus
132:     at: datetime
133:     resolved_at: datetime | None = None
134:     feedback: str | None = None
135: 
136: 
137: class ActiveGateResponse(BaseModel):
138:     model_config = ConfigDict(extra="forbid")
139: 
140:     gate_id: str
141:     gate_type: GateType
142:     status: HumanGateStatus
143:     summary: str
144:     payload: dict[str, Any] = Field(default_factory=dict)
145:     deadline_at: datetime | None = None
146:     resolved_at: datetime | None = None
147:     reminder_sent_at: datetime | None = None
148:     feedback: str | None = None
149:     auto_approved: bool = False
150: 
151: 
152: class ArtifactSummaryResponse(BaseModel):
153:     model_config = ConfigDict(extra="forbid")
154: 
155:     counts: dict[str, int] = Field(default_factory=dict)
156:     total: int = 0
157: 
158: 
159: class TaskSummaryResponse(BaseModel):
160:     model_config = ConfigDict(extra="forbid")
161: 
162:     task_id: str
163:     mode: TaskMode
164:     status: TaskStage
165:     created_at: datetime
166:     updated_at: datetime
167:     current_stage: TaskStage
168:     termination_reason: str | None = None
169: 
170: 
171: class TaskDetailResponse(TaskSummaryResponse):
172:     budget_limit: ResourceUsage
173:     budget_used: ResourceUsage
174:     gates: list[GateRecordResponse] = Field(default_factory=list)
175:     active_gate: ActiveGateResponse | None = None
176:     artifact_summary: ArtifactSummaryResponse
177:     config: dict[str, Any] = Field(default_factory=dict)
178: 
179: 
180: class TaskListResponse(BaseModel):
181:     model_config = ConfigDict(extra="forbid")
182: 
183:     items: list[TaskSummaryResponse]
184: 
185: 
186: class TaskCreateResponse(BaseModel):
187:     model_config = ConfigDict(extra="forbid")
188: 
189:     task_id: str
190:     status: TaskStage
191: 
192: 
193: class TaskActionResponse(BaseModel):
194:     model_config = ConfigDict(extra="forbid")
195: 
196:     task_id: str
197:     status: TaskStage
198:     detail: str
199: 
200: 
201: class TaskRejectRequest(BaseModel):
202:     model_config = ConfigDict(extra="forbid")
203: 
204:     feedback: str | None = None
205: 
206: 
207: class ArtifactItemResponse(BaseModel):
208:     model_config = ConfigDict(extra="forbid")
209: 
210:     artifact_id: str
211:     artifact_type: ArtifactType
212:     source_task_id: str | None = None
213:     summary: str | None = None
214:     status: str | None = None
215:     payload: dict[str, Any]
216: 
217: 
218: class TaskArtifactsResponse(BaseModel):
219:     model_config = ConfigDict(extra="forbid")
220: 
221:     task_id: str
222:     items: list[ArtifactItemResponse]
223: 
224: 
225: class HealthResponse(BaseModel):
226:     model_config = ConfigDict(extra="forbid")
227: 
228:     status: ApiStatus
229:     state_root: str
230:     container_configured: bool
231:     container_health: dict[str, Any] | None = None
232:     detail: str | None = None

(End of file - total 232 lines)
</content>
```

---

## Assistant (Build · gpt-5.4 · 58.6s)

我已经有足够上下文，开始直接写 gap plan，并把它挂到 refactoring-plan 索引和 architecture baseline 上。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan.md\n+---\n+aliases:\n+  - Contracts to Current AINRF Gap Plan\n+  - Contract 到当前 AINRF 的缺口规划\n+tags:\n+  - scholar-agent\n+  - gap-analysis\n+  - contract\n+  - implementation-plan\n+source_repo: scholar-agent\n+source_path: /Users/kozmosa/code/scholar-agent\n+last_local_commit: workspace aggregate\n+---\n+# Contract 到当前 AINRF 的缺口规划\n+\n+> [!abstract]\n+> 本文档用于把 `refactoring-plan/` 下已经冻结的 contracts，与当前 `src/ainrf/` 已有实现逐项对照，明确“哪些已经具备、哪些只具备一半、哪些仍然缺失”，并给出 next release 最小实现切片顺序。目标不是重新设计系统，而是把规划链真正转换成可执行的工程缺口图。\n+\n+## 结论\n+\n+- 当前 `ainrf` 已具备 next release control plane 的骨架：FastAPI、task API、health、gates、events、state store、SSH health 已经存在。\n+- 当前最主要的缺口不是“完全没有后端”，而是“contracts 需要的 read model shape、summary shape、preview metadata 和 dashboard-friendly 聚合层还没有正式形成”。\n+- 因此 next release 的最小实现重点不应是重写 runtime，而应是：扩展当前 read model 和 API 聚合，使其稳定支撑 dashboard。\n+\n+## 对照范围\n+\n+本次对照的 contracts 包括：\n+\n+- `[[LLM-Working/refactoring-plan/task-read-model-contract]]`\n+- `[[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]`\n+- `[[LLM-Working/refactoring-plan/artifact-preview-contract]]`\n+\n+本次对照的当前实现主要来自：\n+\n+- `src/ainrf/api/routes/tasks.py`\n+- `src/ainrf/api/routes/health.py`\n+- `src/ainrf/api/schemas.py`\n+- `src/ainrf/state/`\n+- `src/ainrf/events/`\n+- `src/ainrf/gates/`\n+\n+## 一、Task Read Model 合约对照\n+\n+### 当前已具备\n+\n+- `TaskSummaryResponse` 已提供：\n+  - `task_id`\n+  - `mode`\n+  - `status`\n+  - `created_at`\n+  - `updated_at`\n+  - `current_stage`\n+  - `termination_reason`\n+- `TaskDetailResponse` 已额外提供：\n+  - `budget_limit`\n+  - `budget_used`\n+  - `gates`\n+  - `active_gate`\n+  - `artifact_summary`\n+  - `config`\n+\n+### 当前只具备一半\n+\n+- `input_summary`\n+  - 当前只有原始 `config`，没有面向 dashboard 的 `title` / `brief` / `seed_inputs` / `target_inputs` 摘要层。\n+- `progress_summary`\n+  - 当前只有 `current_stage` 和事件流能力，没有正式的 `current_checkpoint`、`milestones`、`recent_events` 聚合字段。\n+- `result_summary`\n+  - 当前只有 `termination_reason` 和 artifact summary，没有 `result_brief`、`recent_artifacts`、`error_summary` 的专门摘要层。\n+\n+### 当前缺失\n+\n+- dashboard 友好的 task card shape。\n+- 首页任务列表与详情页之间明确分层的 read model。\n+- 轻量 summary 字段与原始 config/payload 之间的边界。\n+\n+### 工程判断\n+\n+- 这部分不需要推翻 `TaskRecord`。\n+- 更合理的做法是在现有 API schema 之上增加一层 dashboard-oriented summary shape，而不是让前端直接消费原始 `config`。\n+\n+## 二、Workspace / Session / Container Summary 合约对照\n+\n+### 当前已具备\n+\n+- `TaskCreateRequest.container` 已有：\n+  - `host`\n+  - `port`\n+  - `user`\n+  - `ssh_key_path`\n+  - `project_dir`\n+- `/health` 已能提供：\n+  - `container_configured`\n+  - `ssh_ok`\n+  - `claude_ok`\n+  - `anthropic_api_key_ok`\n+  - `project_dir_writable`\n+  - `gpu_models`\n+  - `cuda_version`\n+  - `disk_free_bytes`\n+\n+### 当前只具备一半\n+\n+- workspace summary\n+  - 当前有 `project_dir`，但没有专门的 `workspace_id` / `workspace_label` 抽象。\n+- session summary\n+  - 当前能从健康检查和 SSH 可达性间接推断 session 可用性，但没有正式的 `session_status` / `connected` / `recoverable` read model。\n+- resource snapshot\n+  - 当前只在 `/health` 里有部分 container health 字段，没有统一成 dashboard summary shape。\n+\n+### 当前缺失\n+\n+- 一个稳定的 task-scoped execution context summary。\n+- 能直接挂在 task detail 上的 workspace/session/container 摘要响应。\n+- 统一的 `resource_snapshot` 结构。\n+\n+### 工程判断\n+\n+- 这部分很适合先做“只读摘要层”，不需要先做真正的 workspace/session runtime 重构。\n+- next release 只需要 summary contract，不需要正式引入独立 infra domain model。\n+\n+## 三、Artifact Preview 合约对照\n+\n+### 当前已具备\n+\n+- `TaskArtifactsResponse` 已支持列出 task 关联 artifacts。\n+- `ArtifactItemResponse` 已有：\n+  - `artifact_id`\n+  - `artifact_type`\n+  - `source_task_id`\n+  - `summary`\n+  - `status`\n+  - `payload`\n+\n+### 当前只具备一半\n+\n+- 已有 artifact list，但没有 dashboard-friendly preview metadata。\n+- 当前 `payload` 是原始 JSON payload，不等于 preview contract 所需的：\n+  - `display_title`\n+  - `preview_format`\n+  - `preview_ref`\n+\n+### 当前缺失\n+\n+- 三类核心 artifact 的稳定 preview shape：\n+  - tables\n+  - reports\n+  - figures\n+- recent artifacts 轻量入口 shape。\n+- artifact list 和 artifact preview 之间的清晰分层。\n+\n+### 工程判断\n+\n+- 这里最关键的不是“支持所有 artifact”，而是先为结果导向的三类 artifact 增加 preview metadata。\n+- next release 应避免让前端直接解析原始 artifact payload 来猜预览方式。\n+\n+## 四、总体缺口总结\n+\n+### 已有骨架\n+\n+- task API 已有。\n+- health API 已有。\n+- event stream 已有。\n+- gate lifecycle 已有。\n+- artifact list 已有。\n+\n+### 真实缺口\n+\n+1. 缺 dashboard-oriented read model，而不是缺 task 概念。\n+2. 缺 execution context summary，而不是缺 SSH / container 基础。\n+3. 缺 preview metadata，而不是缺 artifact list。\n+\n+### 不应误判为短期目标的内容\n+\n+- 完整 experiment runtime。\n+- 全局 analytics。\n+- 多用户 / 多工作区平台化。\n+- 完整 token telemetry 系统。\n+\n+## 五、推荐实现切片\n+\n+### Slice 1：Task Summary Layer\n+\n+目标：\n+\n+- 在现有 `TaskSummaryResponse` / `TaskDetailResponse` 之上，为 dashboard 增加 summary-oriented 字段分层。\n+\n+最小交付：\n+\n+- `title`\n+- `brief`\n+- `current_checkpoint`\n+- `recent_events`\n+- `result_brief`\n+\n+### Slice 2：Execution Context Summary Layer\n+\n+目标：\n+\n+- 为 task detail 增加 workspace / session / container / resource snapshot 摘要。\n+\n+最小交付：\n+\n+- `workspace_label`\n+- `project_dir`\n+- `session_status`\n+- `ssh_available`\n+- `resource_snapshot`\n+\n+### Slice 3：Artifact Preview Metadata Layer\n+\n+目标：\n+\n+- 为三类核心 artifact 加上 dashboard 直接可用的 preview metadata。\n+\n+最小交付：\n+\n+- `display_title`\n+- `preview_format`\n+- `preview_ref`\n+\n+### Slice 4：Recent Artifacts / Recent Tasks 聚合层\n+\n+目标：\n+\n+- 为首页提供轻量聚合接口或可复用响应 shape。\n+\n+最小交付：\n+\n+- recent finished tasks\n+- recent artifacts\n+- running task summary\n+\n+## 六、当前最推荐的实施顺序\n+\n+1. 先做 task read model summary layer。\n+2. 再做 artifact preview metadata。\n+3. 再做 workspace / session / container summary。\n+4. 最后评估是否值得引入 token telemetry 候选字段。\n+\n+原因：\n+\n+- task 和 artifact preview 对 dashboard 首屏价值最高。\n+- workspace / session / container 适合在已有 health 基础上逐步补。\n+- token telemetry 仍然是最容易引发 scope 膨胀的部分。\n+\n+## 七、后续文档回写要求\n+\n+- roadmap 应把上述 4 个 slices 转成原子实施任务。\n+- architecture baseline 应把这些 gap 映射到具体模块边界。\n+- 如果后续开始改代码，`impl` 文档应按 slice 记录，而不是跳过 gap analysis 直接堆功能。\n+\n+## 关联笔记\n+\n+- [[LLM-Working/refactoring-plan/index]]\n+- [[LLM-Working/refactoring-plan/architecture-baseline-plan]]\n+- [[LLM-Working/refactoring-plan/task-read-model-contract]]\n+- [[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]\n+- [[LLM-Working/refactoring-plan/artifact-preview-contract]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/index.md\n@@\n - 再读 [[LLM-Working/refactoring-plan/architecture-baseline-plan]]，确认实现边界。\n+- 然后读 [[LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan]]，确认这些 contracts 与当前 `ainrf` 实现之间的真实缺口。\n - 最后读 3 份 contract，确认后续实现需要遵守的最小前后端契约。\n@@\n - [[LLM-Working/refactoring-plan/architecture-baseline-plan]]\n+- [[LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan]]\n - [[LLM-Working/refactoring-plan/task-read-model-contract]]\n - [[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]\n - [[LLM-Working/refactoring-plan/artifact-preview-contract]]\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/refactoring-plan/architecture-baseline-plan.md\n@@\n ## 对后续文档的回写要求\n \n - manifesto 需要把本文视为 next release 的实现边界补充。\n - roadmap 需要把本文中的架构切片映射成原子任务。\n - 后续正式 architecture 文档应以本文为提纲，而不是重新发明结构。\n+- contracts 与当前实现的落差以 `[[LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan]]` 为准。\n@@\n - [[LLM-Working/refactoring-plan/dashboard-baseline-spec]]\n+- [[LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan]]\n - [[LLM-Working/refactoring-plan/task-read-model-contract]]\n - [[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]\n - [[LLM-Working/refactoring-plan/artifact-preview-contract]]\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A docs/LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan.md
M docs/LLM-Working/refactoring-plan/index.md
M docs/LLM-Working/refactoring-plan/architecture-baseline-plan.md
```

---

## Assistant (Build · gpt-5.4 · 8.1s)

gap plan 已写好并挂进索引。下一步做构建验证，然后补 worklog。

**Tool: bash**

**Input:**
```json
{
  "command": "UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build",
  "description": "Builds the HTML notes site",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```

[31m │  ⚠  Warning from the Material for MkDocs team[0m
[31m │[0m
[31m │[0m  MkDocs 2.0, the underlying framework of Material for MkDocs,
[31m │[0m  will introduce backward-incompatible changes, including:
[31m │[0m
[31m │  × [0mAll plugins will stop working – the plugin system has been removed
[31m │  × [0mAll theme overrides will break – the theming system has been rewritten
[31m │  × [0mNo migration path exists – existing projects cannot be upgraded
[31m │  × [0mClosed contribution model – community members can't report bugs
[31m │  × [0mCurrently unlicensed – unsuitable for production use
[31m │[0m
[31m │[0m  Our full analysis:
[31m │[0m
[31m │[0m  [4mhttps://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/[0m
[0m
INFO    -  MERMAID2  - Initialization arguments: {}
INFO    -  MERMAID2  - Using specified javascript library: assets/javascripts/vendor/mermaid-10.4.0.min.js
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: /Users/kozmosa/code/scholar-agent/site
INFO    -  MERMAID2  - Found superfences config: {'custom_fences': [{'name': 'mermaid', 'class': 'mermaid', 'format': functools.partial(<function fence_mermaid at 0x105bb8220>, custom=True)}]}
INFO    -  MERMAID2  - Found 'fence_mermaid_custom' function: activate custom loader for superfences
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI-Native Research Framework：有界自治研究系统蓝图': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '工件图谱架构：AI-Native Research Framework 的核心模型': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'V1：双模式有界自治研究引擎': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 RFC：有界自治研究引擎实现规格': found 3 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AINRF V1 Roadmap：实现路线图': found 2 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Academic Research Skills：从研究到发表的学术全流程管线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'AI Research SKILLs：AI 研究工程技能库': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'ArgusBot：面向 Codex 的监督式 Autoloop 控制层': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Auto-claude-code-research-in-sleep：过夜自治科研流水线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'autoresearch：自治 ML 实验迭代框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Awesome Claude Code Paper Proofreading：LaTeX 论文校对 prompt 工作流': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Code Deep Research：多阶段深度研究框架': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Claude Scholar：学术研究与开发一体化个人配置系统': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'Everything Claude Code：通用 Agent Harness 基线': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page 'EvoScientist：多渠道统一控制面的自进化 AI 科学家工作台': found 1 diagrams, adding scripts
INFO    -  MERMAID2  - Custom loader activated
INFO    -  MERMAID2  - Page '学术研究 Agent 汇总研究报告': found 2 diagrams, adding scripts
INFO    -  Documentation built in 0.79 seconds

```

---

## Assistant (Build · gpt-5.4 · 17.7s)

构建通过。我补 worklog，并收口当前 todo。

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: /Users/kozmosa/code/scholar-agent/docs/LLM-Working/worklog/2026-04-04.md\n@@\n - 2026-04-04 16:12 `docs-planning`：完成第一批实现契约文档：`[[LLM-Working/refactoring-plan/task-read-model-contract]]`、`[[LLM-Working/refactoring-plan/workspace-session-container-summary-contract]]`、`[[LLM-Working/refactoring-plan/artifact-preview-contract]]`，分别固定 dashboard 所消费的 task 读模型分层、workspace/session/container 的摘要契约，以及 tables / reports / figures 三类工件的 preview metadata；同时在 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]` 中补“当前契约入口”，形成从项目重定位、mode baseline、dashboard baseline、architecture baseline 到具体 contract 的完整规划链；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n - 2026-04-04 16:26 `docs-refactor`：将本轮长期重构相关的 8 份规划与 contract 文档统一迁入 `docs/LLM-Working/refactoring-plan/`，新增 `[[LLM-Working/refactoring-plan/index]]` 作为这一组文档的集中入口，并同步修正 `framework/index`、worklog 和各规划文档之间的 wikilink，避免 `LLM-Working/` 根目录继续混放实现规划与长期重构规划；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n+- 2026-04-04 16:40 `docs-planning`：完成 `[[LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan]]`，将当前 `src/ainrf/` 已有的 API、state、gates、events、health 能力与 task read model、workspace/session/container summary、artifact preview 三份 contract 逐项对照，明确当前真实缺口是 dashboard-friendly 的 summary/read model/preview metadata 聚合层，而不是“完全没有后端”，并据此收敛出 4 个推荐实现切片；同步更新 `[[LLM-Working/refactoring-plan/index]]` 与 `[[LLM-Working/refactoring-plan/architecture-baseline-plan]]` 回链；执行 `UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build` 成功。\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M docs/LLM-Working/worklog/2026-04-04.md
```

---

## Assistant (Build · gpt-5.4 · 7.2s)

**Tool: todowrite**

**Input:**
```json
{
  "todos": [
    {
      "content": "起草 contracts-to-current-ainrf gap plan 文档",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "将 gap plan 回链到现有 refactoring-plan 文档",
      "priority": "medium",
      "status": "completed"
    },
    {
      "content": "更新 refactoring-plan 索引纳入 gap plan",
      "priority": "medium",
      "status": "completed"
    },
    {
      "content": "更新今日 worklog 记录 gap mapping",
      "priority": "high",
      "status": "completed"
    },
    {
      "content": "执行文档构建验证 gap plan 改动",
      "priority": "high",
      "status": "completed"
    }
  ]
}
```

**Output:**
```
[
  {
    "content": "起草 contracts-to-current-ainrf gap plan 文档",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "将 gap plan 回链到现有 refactoring-plan 文档",
    "priority": "medium",
    "status": "completed"
  },
  {
    "content": "更新 refactoring-plan 索引纳入 gap plan",
    "priority": "medium",
    "status": "completed"
  },
  {
    "content": "更新今日 worklog 记录 gap mapping",
    "priority": "high",
    "status": "completed"
  },
  {
    "content": "执行文档构建验证 gap plan 改动",
    "priority": "high",
    "status": "completed"
  }
]
```

---

## Assistant (Build · gpt-5.4 · 21.7s)

继续完成了，而且这一步已经明显从“规划文档”进入“工程推进文档”了。

**新增**
1. `docs/LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan.md`

**更新**
1. `docs/LLM-Working/refactoring-plan/index.md`
2. `docs/LLM-Working/refactoring-plan/architecture-baseline-plan.md`
3. `docs/LLM-Working/worklog/2026-04-04.md`

**这次具体写了什么**
我新增了一份 `contracts-to-current-ainrf-gap-plan`，它的作用不是再写一层抽象规划，而是把你前面已经冻结的 contracts，和当前 `src/ainrf/` 的真实实现逐项对照。

它现在回答了这几个关键问题：

**1. 当前 `ainrf` 到底已经有什么**
文档里明确点了当前已有能力：

- FastAPI service
- task API
- health API
- gates
- events
- state store
- SSH health / container config 基础

这一步很重要，因为它把工程判断从“好像什么都还没开始”拉回到“控制面骨架其实已经有了”。

**2. 真正的缺口是什么**
这份 gap plan 明确指出：

当前最主要的缺口不是：
- 没有后端
- 没有 task 概念
- 没有 artifact list
- 没有 SSH/container 基础

而是：

1. 缺 dashboard-friendly 的 task summary/read model
2. 缺 execution context summary
3. 缺 artifact preview metadata
4. 缺给首页用的轻量聚合层

这个判断我认为非常关键，因为它能防止后续工程走偏。

**3. 针对三份 contract 分别做了实现对照**
文档里分别对照了：

1. `task-read-model-contract`
2. `workspace-session-container-summary-contract`
3. `artifact-preview-contract`

每一类都拆成：

- 当前已具备
- 当前只具备一半
- 当前缺失
- 工程判断

这使得它已经不只是规划，而是很接近 implementation prep 了。

**4. 推荐了 4 个最小实现切片**
文档现在给出了一组很清晰的 next-step implementation slices：

1. `Task Summary Layer`
2. `Execution Context Summary Layer`
3. `Artifact Preview Metadata Layer`
4. `Recent Artifacts / Recent Tasks 聚合层`

并且给了推荐顺序：

1. 先做 task summary layer
2. 再做 artifact preview metadata
3. 再做 workspace / session / container summary
4. 最后再评估 token telemetry

这个顺序是合理的，我也认同它比继续发散规划更有效。

**我对当前工程状态的判断**
现在这条文档链已经从“愿景”一直走到了“切片化缺口分析”：

1. 项目重定位
2. release roadmap
3. mode baseline
4. dashboard baseline
5. architecture baseline
6. contracts
7. gap plan

这已经足够作为真正开始下一波实现工作的基础。

**验证**
我执行了：

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/build_html_notes.py build
```

结果：通过。

**现在最值得做的事**
此时我不建议继续无限写更多 planning 文档。  
现在最自然的方向已经变成：

**开始把 gap plan 转成真正的 implementation tasks**

最合理的下一步是从你 gap plan 里推荐的第一个切片开始：

1. `Task Summary Layer`

也就是：
- 设计和实现 dashboard-friendly 的 task summary/read model
- 不改 runtime 大方向
- 直接服务后续 dashboard

这一步会非常具体，也最符合你现在的优先级：`engineering > product/system > academic`

**我建议下一步**
如果继续推进，我建议直接进入实现准备甚至实现本身：

1. 先写一份很短的实施文档，或者
2. 直接开始改代码，落地 `Task Summary Layer`

我更推荐第 2 种：  
直接开始实现 `Task Summary Layer`，因为现在文档约束已经足够了。

如果你同意，我下一步就直接开始做这一层实现。

---

## User

pull and merge safely, and then commit and push latest changes

---

## Assistant (Build · gpt-5.4 · 13.1s)

_Thinking:_

**Following git safety protocols**

I need to prioritize git safety since the user asked about pulling and merging safely, and then committing and pushing the latest changes. I'll start by inspecting the git status, diff, and log using bash commands without extra code. It’s possible there could be conflicts during the pull, so checking the status first is essential. I’m focused on ensuring a smooth process for the user!

我先按安全流程检查当前 git 状态、差异和最近提交风格，再决定如何安全拉取、提交和推送。

**Tool: bash**

**Input:**
```json
{
  "command": "git status --short --branch",
  "description": "Shows working tree status",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
## master...origin/master [behind 30]
 M CLAUDE.md
 M docs/framework/index.md
 M uv.lock
?? docs/LLM-Working/refactoring-plan/
?? docs/LLM-Working/worklog/2026-04-04.md
?? select.md

```

**Tool: bash**

**Input:**
```json
{
  "command": "git diff --stat && git diff --cached --stat",
  "description": "Shows changed file summary",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
 CLAUDE.md               | 110 +++---
 docs/framework/index.md |   5 +
 uv.lock                 | 974 ++++++++++++++++++++++++------------------------
 3 files changed, 549 insertions(+), 540 deletions(-)

```

**Tool: bash**

**Input:**
```json
{
  "command": "git log -5 --oneline",
  "description": "Shows recent commit messages",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
bce40d2 feat: add task event streaming
d84c2dd docs: align worklog policy and roadmap notes
4842652 feat: add human gate workflow and webhook controls
f319d2f feat: add fastapi service and daemon api layer
7975cfa feat: add artifact models and json state store

```

---

## Assistant (Build · gpt-5.4 · 24.1s)

_Thinking:_

**Evaluating Git Rebase Options**

I'm considering the potential issues with rebasing when there are dirty files that could interfere. It seems that Git doesn't allow rebasing with unstaged changes, so I need to stash or address those. I could use `git stash push`, but I'm worried about affecting user changes. A safer option might be to create a temporary commit on my files and use `git pull --rebase --autostash`. However, I need to check if the local branch is tracking a remote one and ensure everything is in order before proceeding.

**Checking for Conflicts Before Stashing**

I’m thinking that stashing could touch user changes, but it might not be necessary to ask if I’m confident about restoring them safely. However, there's a risk of conflicts if the remote has modified the same files. Before I make any decisions, I should check if the remote changes impact the unrelated files by using `git fetch` and then doing a diff on specific files. Checking the remote status will help ensure everything stays safe.

我先获取远端最新状态，并检查远端这 30 个提交是否会碰到你当前未提交的文件。这样能决定是直接 `rebase`，还是先做最小范围的暂存/搁置。

**Tool: bash**

**Input:**
```json
{
  "command": "git fetch origin",
  "description": "Fetches latest remote commits",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
From github.com:Kozmosa/scholar-agent
   48dde94..2557ada  master     -> origin/master

```

**Tool: bash**

**Input:**
```json
{
  "command": "git diff --name-only HEAD..origin/master",
  "description": "Lists files changed on remote",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
.gitignore
PROJECT_BASIS.md
docs/LLM-Working/p7-agent-adapter-task-engine-impl.md
docs/LLM-Working/p9-real-runtime-smoke-checklist.md
docs/LLM-Working/w1-webui-shell-client-implementation-plan.md
docs/LLM-Working/w2-project-run-forms-implementation-plan.md
docs/LLM-Working/w3-run-detail-gates-events-implementation-plan.md
docs/LLM-Working/worklog/2026-03-16.md
docs/LLM-Working/worklog/2026-03-17.md
docs/LLM-Working/worklog/2026-03-26.md
docs/framework/agent-capability-base.md
docs/framework/ai-native-research-framework.md
docs/framework/artifact-graph-architecture.md
docs/framework/container-workspace-protocol.md
docs/framework/index.md
docs/framework/pia-rfc.md
docs/framework/reference-mapping.md
docs/framework/v1-dual-mode-research-engine.md
docs/framework/v1-implementation-status.md
docs/framework/v1-rfc.md
docs/framework/v1-roadmap.md
docs/framework/vsa-rfc.md
docs/framework/webui-v1-rfc.md
docs/framework/webui-v1-roadmap.md
paper-test/paper.md
pyproject.toml
src/ainrf/README.md
src/ainrf/agents/__init__.py
src/ainrf/agents/base.py
src/ainrf/agents/claude_code.py
src/ainrf/agents/skill_profiles.py
src/ainrf/api/app.py
src/ainrf/api/config.py
src/ainrf/api/middleware.py
src/ainrf/artifacts/models.py
src/ainrf/cli.py
src/ainrf/engine/__init__.py
src/ainrf/engine/engine.py
src/ainrf/engine/models.py
src/ainrf/execution/models.py
src/ainrf/execution/ssh.py
src/ainrf/gates/__init__.py
src/ainrf/gates/manager.py
src/ainrf/gates/models.py
src/ainrf/runtime/__init__.py
src/ainrf/runtime/secrets.py
src/ainrf/state/models.py
src/ainrf/webui/__init__.py
src/ainrf/webui/app.py
src/ainrf/webui/client.py
src/ainrf/webui/models.py
src/ainrf/webui/store.py
tests/test_api_auth.py
tests/test_api_tasks.py
tests/test_api_v1_routes.py
tests/test_claude_code_adapter.py
tests/test_cli.py
tests/test_execution_ssh.py
tests/test_performance_benchmarks.py
tests/test_state_store.py
tests/test_task_engine.py
tests/test_webui_app.py
tests/test_webui_client.py
tests/test_webui_store.py
uv.lock

```

**Tool: bash**

**Input:**
```json
{
  "command": "git diff --name-only -- docs/framework/index.md docs/LLM-Working/refactoring-plan docs/LLM-Working/worklog/2026-04-04.md",
  "description": "Lists my planned changed docs",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
docs/framework/index.md

```

---

## Assistant (Build · gpt-5.4 · 34.6s)

_Thinking:_

**Considering stash application**

I'm thinking about applying the user's stash, but I might need to address unrelated changes after rebasing. If there’s a conflict in the `uv.lock`, we’d have to pause and ask the user. They requested to commit and push the latest changes, so I might proceed with caution. I’ll apply our stash afterward and focus on committing only our files while ensuring I create a commit message, possibly something like `docs: add refactoring plan baseline`. I need to stage only our files and avoid unrelated user files. Let's see how it goes!

我发现当前工作区里有与你这次文档重构无关的本地改动，且远端也改了 `docs/framework/index.md` 和 `uv.lock`。我会先把“你的无关本地改动”和“这次重构文档改动”分开暂存，再 `pull --rebase`，最后只提交这次重构相关文件，尽量避免把无关改动卷进去。

**Tool: bash**

**Input:**
```json
{
  "command": "git stash push --include-untracked --message \"temp-user-local-before-rebase\" -- CLAUDE.md uv.lock select.md",
  "description": "Stashes unrelated local changes",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
Saved working directory and index state On master: temp-user-local-before-rebase

```

**Tool: bash**

**Input:**
```json
{
  "command": "git stash push --include-untracked --message \"temp-refactor-plan-before-rebase\" -- docs/framework/index.md docs/LLM-Working/refactoring-plan docs/LLM-Working/worklog/2026-04-04.md",
  "description": "Stashes refactor plan changes",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
error: could not write index

```

---

## Assistant (Build · gpt-5.4 · 7.8s)

第一步暂存成功，第二步因为 index 状态变化失败了。我先检查当前工作区和 stash 状态，再继续安全处理。

**Tool: bash**

**Input:**
```json
{
  "command": "git status --short --branch",
  "description": "Shows working tree status",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
## master...origin/master [behind 33]
 M docs/framework/index.md
?? docs/LLM-Working/refactoring-plan/
?? docs/LLM-Working/worklog/2026-04-04.md

```

**Tool: bash**

**Input:**
```json
{
  "command": "git stash list",
  "description": "Lists current git stashes",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
stash@{0}: On master: temp-user-local-before-rebase

```

---

## Assistant (Build · gpt-5.4 · 13.9s)

现在只剩这次重构相关改动在工作区，可以安全地整体 stash 后 rebase。接着我会拉取远端、恢复这批改动、解决可能冲突，再提交。

**Tool: bash**

**Input:**
```json
{
  "command": "git stash push --include-untracked --message \"temp-refactor-plan-before-rebase\" -- docs/framework/index.md docs/LLM-Working/refactoring-plan docs/LLM-Working/worklog/2026-04-04.md && git pull --rebase origin master",
  "description": "Stashes refactor docs then rebases",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
Saved working directory and index state On master: temp-refactor-plan-before-rebase
From github.com:Kozmosa/scholar-agent
 * branch            master     -> FETCH_HEAD
Updating bce40d2..2557ada
Fast-forward
 .gitignore                                         |   12 +-
 .gitmodules                                        |    6 +
 PROJECT_BASIS.md                                   |    1 +
 .../p7-agent-adapter-task-engine-impl.md           |   82 +
 .../LLM-Working/p9-real-runtime-smoke-checklist.md |   47 +
 .../w1-webui-shell-client-implementation-plan.md   |   97 +
 .../w2-project-run-forms-implementation-plan.md    |   97 +
 ...-run-detail-gates-events-implementation-plan.md |   92 +
 docs/LLM-Working/worklog/2026-03-16.md             |    8 +
 docs/LLM-Working/worklog/2026-03-17.md             |    9 +
 docs/LLM-Working/worklog/2026-03-26.md             |   23 +
 docs/framework/agent-capability-base.md            |  108 +
 docs/framework/ai-native-research-framework.md     |   10 +-
 docs/framework/artifact-graph-architecture.md      |   17 +-
 docs/framework/container-workspace-protocol.md     |    6 +-
 docs/framework/index.md                            |   13 +-
 docs/framework/pia-rfc.md                          |   92 +
 docs/framework/reference-mapping.md                |    6 +-
 docs/framework/v1-dual-mode-research-engine.md     |   67 +-
 docs/framework/v1-implementation-status.md         |  350 +++
 docs/framework/v1-rfc.md                           |   53 +-
 docs/framework/v1-roadmap.md                       |   34 +-
 docs/framework/vsa-rfc.md                          |  112 +
 docs/framework/webui-v1-rfc.md                     |  206 ++
 docs/framework/webui-v1-roadmap.md                 |  185 ++
 .../2026-04-06-ref-repos-submodules-design.md      |   94 +
 paper-test/paper.md                                |  780 +++++++
 pyproject.toml                                     |    2 +
 ref-repos/EvoMaster                                |    1 +
 ref-repos/MagiClaw                                 |    1 +
 src/ainrf/README.md                                |  258 +++
 src/ainrf/agents/__init__.py                       |   23 +
 src/ainrf/agents/base.py                           |   42 +
 src/ainrf/agents/claude_code.py                    | 1051 +++++++++
 src/ainrf/agents/skill_profiles.py                 |  198 ++
 src/ainrf/api/app.py                               |   10 +-
 src/ainrf/api/config.py                            |   51 +-
 src/ainrf/api/middleware.py                        |    9 +-
 src/ainrf/artifacts/models.py                      |    7 +
 src/ainrf/cli.py                                   |  264 ++-
 src/ainrf/engine/__init__.py                       |   10 +
 src/ainrf/engine/engine.py                         | 1371 ++++++++++++
 src/ainrf/engine/models.py                         |   52 +
 src/ainrf/execution/models.py                      |    3 +
 src/ainrf/execution/ssh.py                         |    5 +
 src/ainrf/gates/__init__.py                        |    3 +-
 src/ainrf/gates/manager.py                         |   24 +-
 src/ainrf/gates/models.py                          |    3 +
 src/ainrf/runtime/__init__.py                      |    5 +
 src/ainrf/runtime/secrets.py                       |   42 +
 src/ainrf/state/models.py                          |   12 +-
 src/ainrf/webui/__init__.py                        |   40 +
 src/ainrf/webui/app.py                             | 2262 ++++++++++++++++++++
 src/ainrf/webui/client.py                          |  203 ++
 src/ainrf/webui/models.py                          |  152 ++
 src/ainrf/webui/store.py                           |  183 ++
 test/IDEA_REPORT.md                                |  150 ++
 ...244\215\347\216\260\346\212\245\345\221\212.md" |  439 ++++
 test/collect_results.py                            |   97 +
 test/reproduction_results.json                     |  104 +
 tests/test_api_auth.py                             |   36 +
 tests/test_api_tasks.py                            |   16 +-
 tests/test_api_v1_routes.py                        |   51 +
 tests/test_claude_code_adapter.py                  |  598 ++++++
 tests/test_cli.py                                  |  199 +-
 tests/test_execution_ssh.py                        |   18 +
 tests/test_performance_benchmarks.py               |   68 +
 tests/test_state_store.py                          |    4 +-
 tests/test_task_engine.py                          |  816 +++++++
 tests/test_webui_app.py                            |  860 ++++++++
 tests/test_webui_client.py                         |  287 +++
 tests/test_webui_store.py                          |  127 ++
 uv.lock                                            |  733 +++++++
 73 files changed, 13365 insertions(+), 132 deletions(-)
 create mode 100644 .gitmodules
 create mode 100644 docs/LLM-Working/p7-agent-adapter-task-engine-impl.md
 create mode 100644 docs/LLM-Working/p9-real-runtime-smoke-checklist.md
 create mode 100644 docs/LLM-Working/w1-webui-shell-client-implementation-plan.md
 create mode 100644 docs/LLM-Working/w2-project-run-forms-implementation-plan.md
 create mode 100644 docs/LLM-Working/w3-run-detail-gates-events-implementation-plan.md
 create mode 100644 docs/LLM-Working/worklog/2026-03-17.md
 create mode 100644 docs/LLM-Working/worklog/2026-03-26.md
 create mode 100644 docs/framework/agent-capability-base.md
 create mode 100644 docs/framework/pia-rfc.md
 create mode 100644 docs/framework/v1-implementation-status.md
 create mode 100644 docs/framework/vsa-rfc.md
 create mode 100644 docs/framework/webui-v1-rfc.md
 create mode 100644 docs/framework/webui-v1-roadmap.md
 create mode 100644 docs/superpowers/specs/2026-04-06-ref-repos-submodules-design.md
 create mode 100755 paper-test/paper.md
 create mode 160000 ref-repos/EvoMaster
 create mode 160000 ref-repos/MagiClaw
 create mode 100644 src/ainrf/README.md
 create mode 100644 src/ainrf/agents/__init__.py
 create mode 100644 src/ainrf/agents/base.py
 create mode 100644 src/ainrf/agents/claude_code.py
 create mode 100644 src/ainrf/agents/skill_profiles.py
 create mode 100644 src/ainrf/engine/__init__.py
 create mode 100644 src/ainrf/engine/engine.py
 create mode 100644 src/ainrf/engine/models.py
 create mode 100644 src/ainrf/runtime/__init__.py
 create mode 100644 src/ainrf/runtime/secrets.py
 create mode 100644 src/ainrf/webui/__init__.py
 create mode 100644 src/ainrf/webui/app.py
 create mode 100644 src/ainrf/webui/client.py
 create mode 100644 src/ainrf/webui/models.py
 create mode 100644 src/ainrf/webui/store.py
 create mode 100644 test/IDEA_REPORT.md
 create mode 100644 "test/SAGDFN_\345\244\215\347\216\260\346\212\245\345\221\212.md"
 create mode 100644 test/collect_results.py
 create mode 100644 test/reproduction_results.json
 create mode 100644 tests/test_api_v1_routes.py
 create mode 100644 tests/test_claude_code_adapter.py
 create mode 100644 tests/test_performance_benchmarks.py
 create mode 100644 tests/test_task_engine.py
 create mode 100644 tests/test_webui_app.py
 create mode 100644 tests/test_webui_client.py
 create mode 100644 tests/test_webui_store.py

```

---

## Assistant (Build · gpt-5.4 · 8.3s)

rebase 已完成。现在我恢复这次重构文档 stash，检查是否与远端新的 `framework/index.md` 发生冲突，然后只提交这批重构文档。

**Tool: bash**

**Input:**
```json
{
  "command": "git stash list",
  "description": "Lists git stashes after rebase",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
stash@{0}: On master: temp-refactor-plan-before-rebase
stash@{1}: On master: temp-user-local-before-rebase

```

**Tool: bash**

**Input:**
```json
{
  "command": "git stash pop stash@{0}",
  "description": "Restores refactor plan stash",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
Auto-merging docs/framework/index.md
On branch master
Your branch is up to date with 'origin/master'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   docs/framework/index.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/LLM-Working/refactoring-plan/
	docs/LLM-Working/worklog/2026-04-04.md
	ref-repos/Awesome-AI-Scientist/

no changes added to commit (use "git add" and/or "git commit -a")
Dropped stash@{0} (3de89386a4afa365b13f4bf43b16df33243770fc)

```

---

## Assistant (Build · gpt-5.4 · 13.8s)

_Thinking:_

**Evaluating git status**

It looks like I need to check the untracked repository, Awesome-AI-Scientist, since it could have been added by the user. I should probably avoid committing it right away. I also need to inspect the status and look for any merge conflict markers. Checking the framework index might help clarify if there's a conflict. My plan involves committing only the documentation files while stashing any local changes and reviewing the remote index to ensure everything is merged properly.

恢复成功，没有冲突中断。现在工作区里还包含用户新加的 `ref-repos/Awesome-AI-Scientist/`，我不会把它一起提交；接下来只暂存这次重构相关文档并创建一个独立 docs 提交。

**Tool: bash**

**Input:**
```json
{
  "command": "git status --short",
  "description": "Shows current changed files",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
 M docs/framework/index.md
?? docs/LLM-Working/refactoring-plan/
?? docs/LLM-Working/worklog/2026-04-04.md
?? ref-repos/Awesome-AI-Scientist/

```

**Tool: bash**

**Input:**
```json
{
  "command": "git diff -- docs/framework/index.md docs/LLM-Working/refactoring-plan docs/LLM-Working/worklog/2026-04-04.md",
  "description": "Shows refactor docs diff",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
diff --git a/docs/framework/index.md b/docs/framework/index.md
index 84d02b6..aa1b0c0 100644
--- a/docs/framework/index.md
+++ b/docs/framework/index.md
@@ -61,6 +61,11 @@ last_local_commit: workspace aggregate
 - 这组笔记是"自有框架蓝图"，不是对某一个开源仓库的复述；涉及参考项目的判断，均来自本仓库已有研究报告与静态证据。
 - 现阶段默认研究对象是 AI/ML research，不试图抽象到所有学术门类；写作模块只保留下游接口，不在 V1 文档里展开。
 
+## 当前规划入口
+
+- 如果当前目标是对项目做重定位、requirements / expectations 重对齐，先读 [[LLM-Working/refactoring-plan/index]]。
+- 如果当前目标是继续推进 next release 的 scope、contracts 和 dashboard / architecture baseline，也从 [[LLM-Working/refactoring-plan/index]] 进入。
+
 ## 关联笔记
 
 - [[index]]

```

**Tool: bash**

**Input:**
```json
{
  "command": "git log -5 --oneline",
  "description": "Shows recent commit messages",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
2557ada chore: convert ref-repos to git submodules
2c5aa05 docs: add ref-repos submodules migration design
684194b chore: make ref-repos/ submodules in repo, modify .gitignore
48dde94 feat: split webui project and container panels
7b5643a feat: coerce mode1 skill outputs for engine consumption

```

---

## Assistant (Build · gpt-5.4 · 13.3s)

我已经确认提交范围。接下来只 `git add` 这次重构文档，提交后再推送到远端；用户的 `ref-repos/Awesome-AI-Scientist/` 保持不动。

**Tool: bash**

**Input:**
```json
{
  "command": "git add \"docs/framework/index.md\" \"docs/LLM-Working/refactoring-plan\" \"docs/LLM-Working/worklog/2026-04-04.md\" && git commit -m \"docs: add refactoring plan baseline\" && git push origin master",
  "description": "Commits refactor docs and pushes",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
[master c2378f2] docs: add refactoring plan baseline
 12 files changed, 1872 insertions(+)
 create mode 100644 docs/LLM-Working/refactoring-plan/architecture-baseline-plan.md
 create mode 100644 docs/LLM-Working/refactoring-plan/artifact-preview-contract.md
 create mode 100644 docs/LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan.md
 create mode 100644 docs/LLM-Working/refactoring-plan/dashboard-baseline-spec.md
 create mode 100644 docs/LLM-Working/refactoring-plan/index.md
 create mode 100644 docs/LLM-Working/refactoring-plan/mode-baseline-spec.md
 create mode 100644 docs/LLM-Working/refactoring-plan/next-release-realignment-roadmap.md
 create mode 100644 docs/LLM-Working/refactoring-plan/project-realignment-manifesto-plan.md
 create mode 100644 docs/LLM-Working/refactoring-plan/task-read-model-contract.md
 create mode 100644 docs/LLM-Working/refactoring-plan/workspace-session-container-summary-contract.md
 create mode 100644 docs/LLM-Working/worklog/2026-04-04.md
To github.com:Kozmosa/scholar-agent.git
   2557ada..c2378f2  master -> master

```

---

## Assistant (Build · gpt-5.4 · 6.7s)

提交和推送都完成了。我再检查一下工作区，确认只剩下未提交的用户改动，并把结果总结给你。

**Tool: bash**

**Input:**
```json
{
  "command": "git status --short --branch && git stash list",
  "description": "Shows final status and stashes",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
## master...origin/master
?? ref-repos/Awesome-AI-Scientist/
stash@{0}: On master: temp-user-local-before-rebase

```

---

## Assistant (Build · gpt-5.4 · 24.8s)

已经安全完成：

1. 拉取并合并远端最新改动
2. 保留并恢复这次重构规划文档改动
3. 提交并推送这批最新文档变更

**我实际做了什么**
**1. 安全处理本地无关改动**
我先检查了当前工作区，发现有与你这次文档重构无关的本地改动：

- `CLAUDE.md`
- `uv.lock`
- `select.md`

以及这次相关改动：

- `docs/framework/index.md`
- `docs/LLM-Working/refactoring-plan/`
- `docs/LLM-Working/worklog/2026-04-04.md`

我没有把无关改动一起卷入。  
先把无关本地改动单独 stash 了，避免 pull/rebase 污染它们。

**2. 安全拉取远端**
我执行了 `git fetch origin` 和后续 `git pull --rebase origin master`。  
远端确实有大量新提交，而且改动到了：

- `docs/framework/index.md`
- `uv.lock`
- 一批新的 framework/docs/webui/runtime 文件

因为我先把无关改动和这次重构文档改动分开处理了，所以 rebase 是安全完成的。

**3. 恢复这次重构规划文档**
rebase 后我恢复了这次重构相关的 stash。  
`docs/framework/index.md` 自动合并成功，没有留下冲突中断。

**4. 只提交这次相关文档**
我只提交了这次 refactoring plan 相关文件，没有把以下内容一起提交：

- `ref-repos/Awesome-AI-Scientist/`
- stash 里的本地无关改动

**提交信息**
```text
docs: add refactoring plan baseline
```

**提交哈希**
```text
c2378f2
```

**5. 已推送**
已经成功推送到 `origin/master`。

**当前工作区状态**
现在仓库状态是：

- 分支已与远端同步
- 仍有一个未跟踪目录：
  - `ref-repos/Awesome-AI-Scientist/`
- 仍保留一个 stash：
  - `stash@{0}: temp-user-local-before-rebase`

也就是说，我没有动你那批无关本地改动，也没有把 `Awesome-AI-Scientist` 一起提交进去。

**这次提交包含的主要内容**
提交进远端的是：

- `docs/LLM-Working/refactoring-plan/index.md`
- `docs/LLM-Working/refactoring-plan/project-realignment-manifesto-plan.md`
- `docs/LLM-Working/refactoring-plan/next-release-realignment-roadmap.md`
- `docs/LLM-Working/refactoring-plan/mode-baseline-spec.md`
- `docs/LLM-Working/refactoring-plan/dashboard-baseline-spec.md`
- `docs/LLM-Working/refactoring-plan/architecture-baseline-plan.md`
- `docs/LLM-Working/refactoring-plan/task-read-model-contract.md`
- `docs/LLM-Working/refactoring-plan/workspace-session-container-summary-contract.md`
- `docs/LLM-Working/refactoring-plan/artifact-preview-contract.md`
- `docs/LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan.md`
- `docs/LLM-Working/worklog/2026-04-04.md`
- `docs/framework/index.md`

**需要你知道的一个点**
我保留了这个 stash，没有自动恢复：

```text
stash@{0}: temp-user-local-before-rebase
```

里面是你原来无关的本地改动：
- `CLAUDE.md`
- `uv.lock`
- `select.md`

我没自动 pop，是为了避免把它们重新混进当前干净工作区。

如果你要，我下一步可以继续帮你：

1. 安全恢复这个 stash
2. 单独处理 `ref-repos/Awesome-AI-Scientist/` 的纳入方式
3. 继续基于刚刚推送的 refactoring plan 开始下一轮实现或文档收敛

---

## User

make awesome-ai-scientist a submodule

---

## Assistant (Build · gpt-5.4 · 13.1s)

_Thinking:_

**Considering submodule integration**

I need to determine if I should add a submodule from an existing untracked directory. First, I’ll check the .gitmodules file to see if any submodule structure is already there. It’s important to be cautious about this process. I might also want to confirm if the local path is pointing to the correct repo origin, but I can probably infer that. I should inspect the status and the remote URL in that directory, and I'll need to use bash for this.

我先检查 `ref-repos/Awesome-AI-Scientist/` 当前是不是一个本地 git 仓库、它的 remote 是什么，以及仓库当前的 submodule 配置，再把它安全纳入 `.gitmodules`。

**Tool: bash**

**Input:**
```json
{
  "command": "git status --short --branch",
  "description": "Shows repository status",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
## master...origin/master
?? ref-repos/Awesome-AI-Scientist/

```

**Tool: bash**

**Input:**
```json
{
  "command": "git config --file .gitmodules --get-regexp '^submodule\\..*\\.path$'",
  "description": "Lists configured submodule paths",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
submodule.ref-repos/EvoMaster.path ref-repos/EvoMaster
submodule.ref-repos/MagiClaw.path ref-repos/MagiClaw

```

**Tool: bash**

**Input:**
```json
{
  "command": "git rev-parse --is-inside-work-tree",
  "description": "Checks nested repo exists",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist"
}
```

**Output:**
```
true

```

**Tool: bash**

**Input:**
```json
{
  "command": "git remote -v",
  "description": "Shows nested repo remotes",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist"
}
```

**Output:**
```
origin	https://github.com/ResearAI/Awesome-AI-Scientist.git (fetch)
origin	https://github.com/ResearAI/Awesome-AI-Scientist.git (push)

```

---

## Assistant (Build · gpt-5.4 · 11.3s)

_Thinking:_

**Considering git submodules**

I need to add a submodule from an existing local repository. I’m thinking I probably have to remove an untracked directory from the index. To do this, I can use the command `git submodule add --force URL path` to possibly reuse the local git directory. Since the untracked path is a git repo, maybe I could safely move it? I’ll try `git submodule add -f https... ref-repos/Awesome-AI-Scientist` if the parent directory exists.

路径和 remote 都确认了：它已经是一个独立 git 仓库，remote 是 `https://github.com/ResearAI/Awesome-AI-Scientist.git`。我直接把这个现有目录注册成 submodule，然后检查 `.gitmodules` 和工作区状态。

**Tool: bash**

**Input:**
```json
{
  "command": "git submodule add -f https://github.com/ResearAI/Awesome-AI-Scientist.git ref-repos/Awesome-AI-Scientist",
  "description": "Adds Awesome-AI-Scientist as submodule",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
Adding existing repo at 'ref-repos/Awesome-AI-Scientist' to the index

```

---

## Assistant (Build · gpt-5.4 · 9.0s)

submodule 已加进索引。现在我检查 `.gitmodules`、submodule 状态和 git 状态，确认它被正确登记。

**Tool: read**

**Input:**
```json
{
  "filePath": "/Users/kozmosa/code/scholar-agent/.gitmodules",
  "limit": 200,
  "offset": 1
}
```

**Output:**
```
<path>/Users/kozmosa/code/scholar-agent/.gitmodules</path>
<type>file</type>
<content>1: [submodule "ref-repos/EvoMaster"]
2: 	path = ref-repos/EvoMaster
3: 	url = https://github.com/sjtu-sai-agents/EvoMaster.git
4: [submodule "ref-repos/MagiClaw"]
5: 	path = ref-repos/MagiClaw
6: 	url = https://github.com/sjtu-sai-agents/MagiClaw.git
7: [submodule "ref-repos/Awesome-AI-Scientist"]
8: 	path = ref-repos/Awesome-AI-Scientist
9: 	url = https://github.com/ResearAI/Awesome-AI-Scientist.git

(End of file - total 9 lines)
</content>
```

**Tool: bash**

**Input:**
```json
{
  "command": "git submodule status",
  "description": "Shows registered submodules",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
 2e904fe468d93bfeaacd26d51c62ccaea9067ace ref-repos/Awesome-AI-Scientist (heads/main)
-37283fc3be87935117eaf8f9bc7bd2944414a153 ref-repos/EvoMaster
-4b4cb28e7f3ff653b11ad03aafad70862e07e800 ref-repos/MagiClaw

```

**Tool: bash**

**Input:**
```json
{
  "command": "git status --short --branch",
  "description": "Shows working tree status",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
## master...origin/master
M  .gitmodules
Am ref-repos/Awesome-AI-Scientist

```

---

## Assistant (Build · gpt-5.4 · 13.6s)

`Awesome-AI-Scientist` 已经安全加成 submodule 了。

**已完成**
1. 检查了 `ref-repos/Awesome-AI-Scientist/` 当前是一个独立 git 仓库
2. 确认了它的 remote：
   - `https://github.com/ResearAI/Awesome-AI-Scientist.git`
3. 将现有目录注册为 submodule

执行的是：
```bash
git submodule add -f https://github.com/ResearAI/Awesome-AI-Scientist.git ref-repos/Awesome-AI-Scientist
```

**当前结果**
`.gitmodules` 现在已经包含：

```ini
[submodule "ref-repos/Awesome-AI-Scientist"]
	path = ref-repos/Awesome-AI-Scientist
	url = https://github.com/ResearAI/Awesome-AI-Scientist.git
```

`git submodule status` 里也已经出现：

```text
2e904fe468d93bfeaacd26d51c62ccaea9067ace ref-repos/Awesome-AI-Scientist (heads/main)
```

**当前工作区状态**
现在有未提交改动：

- `.gitmodules`
- `ref-repos/Awesome-AI-Scientist`

也就是 submodule 登记已经就位，但还没有 commit。

**一个需要提醒的点**
`git submodule status` 里你原来已有的两个 submodule：

- `ref-repos/EvoMaster`
- `ref-repos/MagiClaw`

前面带了 `-`，这通常表示当前工作树里它们还没有初始化/checkout 到工作目录状态。  
这不是这次 `Awesome-AI-Scientist` 的错误，只是当前仓库 submodule 整体状态的一个现象。

**下一步**
如果你要，我现在可以继续直接帮你：

1. 提交这次 submodule 变更
2. 推送到远端

我建议提交信息用：

```text
chore: add Awesome-AI-Scientist submodule
```

---

## User

commit and push, as you recommended.

---

## Assistant (Build · gpt-5.4 · 10.5s)

我先按提交安全流程检查这次 submodule 变更的状态，然后只提交 `.gitmodules` 和 `ref-repos/Awesome-AI-Scientist`，不碰其他内容。

**Tool: bash**

**Input:**
```json
{
  "command": "git status --short --branch",
  "description": "Shows working tree status",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
## master...origin/master
M  .gitmodules
Am ref-repos/Awesome-AI-Scientist

```

**Tool: bash**

**Input:**
```json
{
  "command": "git diff -- .gitmodules ref-repos/Awesome-AI-Scientist && git diff --cached -- .gitmodules ref-repos/Awesome-AI-Scientist",
  "description": "Shows submodule change diff",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
diff --git a/ref-repos/Awesome-AI-Scientist b/ref-repos/Awesome-AI-Scientist
--- a/ref-repos/Awesome-AI-Scientist
+++ b/ref-repos/Awesome-AI-Scientist
@@ -1 +1 @@
-Subproject commit 2e904fe468d93bfeaacd26d51c62ccaea9067ace
+Subproject commit 2e904fe468d93bfeaacd26d51c62ccaea9067ace-dirty
diff --git a/.gitmodules b/.gitmodules
index 53e3c9f..7c1991f 100644
--- a/.gitmodules
+++ b/.gitmodules
@@ -4,3 +4,6 @@
 [submodule "ref-repos/MagiClaw"]
 	path = ref-repos/MagiClaw
 	url = https://github.com/sjtu-sai-agents/MagiClaw.git
+[submodule "ref-repos/Awesome-AI-Scientist"]
+	path = ref-repos/Awesome-AI-Scientist
+	url = https://github.com/ResearAI/Awesome-AI-Scientist.git
diff --git a/ref-repos/Awesome-AI-Scientist b/ref-repos/Awesome-AI-Scientist
new file mode 160000
index 0000000..2e904fe
--- /dev/null
+++ b/ref-repos/Awesome-AI-Scientist
@@ -0,0 +1 @@
+Subproject commit 2e904fe468d93bfeaacd26d51c62ccaea9067ace

```

**Tool: bash**

**Input:**
```json
{
  "command": "git log -5 --oneline",
  "description": "Shows recent commit messages",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
c2378f2 docs: add refactoring plan baseline
2557ada chore: convert ref-repos to git submodules
2c5aa05 docs: add ref-repos submodules migration design
684194b chore: make ref-repos/ submodules in repo, modify .gitignore
48dde94 feat: split webui project and container panels

```

---

## Assistant (Build · gpt-5.4 · 11.8s)

_Thinking:_

**Inspecting submodule status**

I need to check if the submodule is dirty, which might be because there are untracked files. It's important to investigate the nested status before making any commits. I want to make sure that everything is in order so I don't accidentally mess things up. This involves a little more attention to detail, but getting the status right will help prevent complications down the line. Let's take a closer look!

我发现 submodule 工作树当前是 `dirty`，虽然索引里记录的是干净 commit。提交前我先检查 `ref-repos/Awesome-AI-Scientist` 里有没有未提交改动，避免把一个脏 submodule 状态留在主仓库工作区。

**Tool: bash**

**Input:**
```json
{
  "command": "git status --short",
  "description": "Shows nested repo status",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist"
}
```

**Output:**
```
 M img/WeChat.jpg
?? AGENTS.md

```

**Tool: bash**

**Input:**
```json
{
  "command": "git rev-parse HEAD",
  "description": "Shows nested repo HEAD commit",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist"
}
```

**Output:**
```
2e904fe468d93bfeaacd26d51c62ccaea9067ace

```

**Tool: bash**

**Input:**
```json
{
  "command": "git clean -nd",
  "description": "Previews untracked nested files",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist"
}
```

**Output:**
```
Would remove AGENTS.md

```

---

## Assistant (Build · gpt-5.4 · 15.3s)

_Thinking:_

**Considering git commit process**

I need to figure out how to handle the user's request to commit and push. There are local changes in a submodule that aren’t part of our scope. The submodule index points to a clean commit, but the working tree is dirty due to those local modifications. I can go ahead with committing the superproject, but I should note that the dirty worktree will stay local. I'll definitely include the necessary components in the commit and then push it. Let's proceed!

我检查到 `ref-repos/Awesome-AI-Scientist/` 里有本地未提交内容：

- 修改：`img/WeChat.jpg`
- 未跟踪：`AGENTS.md`

主仓库索引里记录的 submodule 指针仍然是干净 commit `2e904fe...`，所以我可以安全提交主仓库的 submodule 注册，不会把这些子仓库内的本地脏改动一起提交。接下来我只提交主仓库层面的 `.gitmodules` 和 submodule gitlink。

**Tool: bash**

**Input:**
```json
{
  "command": "git add .gitmodules ref-repos/Awesome-AI-Scientist && git commit -m \"chore: add Awesome-AI-Scientist submodule\" && git push origin master",
  "description": "Commits submodule registration and pushes",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
[master 02d8a1b] chore: add Awesome-AI-Scientist submodule
 2 files changed, 4 insertions(+)
 create mode 160000 ref-repos/Awesome-AI-Scientist
To github.com:Kozmosa/scholar-agent.git
   c2378f2..02d8a1b  master -> master

```

---

## Assistant (Build · gpt-5.4 · 8.9s)

提交和推送都完成了。我再检查一次最终状态，并把需要你知道的子仓库脏状态说明清楚。

**Tool: bash**

**Input:**
```json
{
  "command": "git status --short --branch",
  "description": "Shows final repository status",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
## master...origin/master
 m ref-repos/Awesome-AI-Scientist

```

**Tool: bash**

**Input:**
```json
{
  "command": "git submodule status",
  "description": "Shows final submodule status",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent"
}
```

**Output:**
```
 2e904fe468d93bfeaacd26d51c62ccaea9067ace ref-repos/Awesome-AI-Scientist (heads/main)
-37283fc3be87935117eaf8f9bc7bd2944414a153 ref-repos/EvoMaster
-4b4cb28e7f3ff653b11ad03aafad70862e07e800 ref-repos/MagiClaw

```

**Tool: bash**

**Input:**
```json
{
  "command": "git status --short",
  "description": "Shows nested repo final status",
  "timeout": 120000,
  "workdir": "/Users/kozmosa/code/scholar-agent/ref-repos/Awesome-AI-Scientist"
}
```

**Output:**
```
 M img/WeChat.jpg
?? AGENTS.md

```

---

## Assistant (Build · gpt-5.4 · 13.7s)

已经按建议完成提交并推送。

**提交信息**
```text
chore: add Awesome-AI-Scientist submodule
```

**提交哈希**
```text
02d8a1b
```

**已推送**
已推送到 `origin/master`。

**当前状态**
主仓库现在已经包含：
- `.gitmodules` 中新增的 `Awesome-AI-Scientist`
- `ref-repos/Awesome-AI-Scientist` 的 submodule gitlink

**需要你知道的一个重要点**
虽然主仓库提交是干净且正确的，但子仓库 `ref-repos/Awesome-AI-Scientist/` 自己当前仍然是脏的，本地状态为：

- 修改：`img/WeChat.jpg`
- 未跟踪：`AGENTS.md`

所以主仓库现在的 `git status` 显示：

```text
 m ref-repos/Awesome-AI-Scientist
```

这不是主仓库提交失败，而是因为 submodule 工作目录里还有本地改动。  
主仓库记录的 submodule 指针仍然是干净 commit：

```text
2e904fe468d93bfeaacd26d51c62ccaea9067ace
```

**另外两个已有 submodule**
`git submodule status` 里仍然显示：

- `ref-repos/EvoMaster`
- `ref-repos/MagiClaw`

前面带 `-`，表示它们当前没有初始化到工作目录状态。这和这次提交无关，我没有动它们。

**如果你要继续，我建议两种下一步**
1. 处理 `Awesome-AI-Scientist` 子仓库里的本地脏改动
   - 看看 `AGENTS.md` 和 `img/WeChat.jpg` 是否应该保留、忽略或还原

2. 回到主项目继续推进实现
   - 基于你已经推送的 `refactoring-plan`
   - 开始做 `Task Summary Layer` 的实际代码

如果你愿意，我下一步可以先帮你把 `Awesome-AI-Scientist` 子仓库清理到干净状态。

---

## User

you may ignore these dirty changes

---

## Assistant (Build · gpt-5.4 · 9.4s)

可以，我会忽略 `ref-repos/Awesome-AI-Scientist/` 里的脏改动，不把它们当成当前主仓库工作的阻塞项。

当前我会按这个约定处理：

- 主仓库层面：继续正常推进
- 子仓库 `Awesome-AI-Scientist` 内部：
  - `img/WeChat.jpg`
  - `AGENTS.md`
  这些本地脏改动先不处理、不还原、不提交

如果你愿意，我下一步就回到主项目，开始做前面已经规划好的第一个实现切片：

1. `Task Summary Layer` 实现  
或
2. 先把 gap plan 转成更细的 implementation task list

我推荐直接做 `Task Summary Layer`。

---

## User

---

## Assistant (Compaction · gpt-5.4 · 65.5s)

---
## Goal

将 `scholar-agent` 从“泛化的全自动科研叙事”重定位为一个**单用户优先、agent-driven、evidence-grounded 的 research dashboard / copilot**，并基于这个新定位，系统性重构文档、重对齐 requirements / expectations、制定 next release 的 roadmap 与实现边界。  
同时参考新的子模块仓库 `ref-repos/Awesome-AI-Scientist`，但不直接照搬其“全自动 AI scientist”叙事。

另一个并行目标是：把这一轮长期重构规划文档集中管理在一个单独的子目录里，并让后续工作能基于这些规划文档继续推进实现。

## Instructions

- 之后对用户**使用简体中文**交流。
- 先帮用户把表达润色成更自然的英文，再用中文继续讨论。
- 一次最多可启动 24 个 subagents；除非确信不需要，否则不应少于 16 个。此前已经遵守此约束做过多轮探索；本总结阶段无需再提问。
- 用户希望采用**协作式**推进方式，但如果其想法：
  - 工程上不收敛
  - 设计上过于模糊
  - 自相矛盾  
  必须直接指出。
- 用户明确要求项目优先级为：
  - **engineering > product/system > academic**
- 当前主要用户是**用户自己（single user for now）**。
- next release 的核心目标不是“大而全的自动科研”，而是：
  - **dashboard**
  - **stability**
  - **observability**
- 必须弱化/降级的叙事：
  - general AI-driven fully autonomous 24x7 researcher
  - 跨很多领域的通用性
  - 论文工厂式承诺
- 可以保留的能力形式：
  - 24x7 agent/subagent 作为**特定角色**
  - 但必须在**bounded** 工作流里
- next release 的 must-have，用户明确提出：
  - 新的现代 Web UI dashboard
  - task tracking
  - workspace management
  - container/session SSH integration
  - experiments results visualization / artifact preview（tables, reports, figures）
- 用户明确接受：
  - 范围按**任务类别**收缩
  - 非按学科泛化收缩
  - 单会话可完成的 atomic tasks 推进方式
- 版本策略偏好：
  - 当前采用混合版本号，如 `v1-20260401`
  - 文档与产品版本**弱绑定**
  - release 后冻结并归档 decision log / snapshots
- 沟通与执行风格：
  - 更偏合作，不是强行接管
  - 但应主动给出建议与风险判断

## Discoveries

1. **项目真实定位已收敛**
   - 用户明确把项目定位为 **Agent-driven Researching Copilot/Dashboard**，更偏 **Dashboard**
   - 不是跨所有领域的 fully autonomous researcher
   - next release 是一个**单用户 task-centric operator dashboard**，不是完整研究自动化平台

2. **ready-for-use 的最低定义已明确**
   - 能独立完成**典型 / 简单 / 定义明确**的任务
   - 不应频繁失败或损坏状态
   - 必须能让用户看到任务进度、最近任务、最近 artifacts、资源状态

3. **Mode 1 / Mode 2 不能沿用现有 framework 文档中的未来态定义**
   - 这是本轮非常关键的工程判断，用户已接受
   - 需要重写为 next release 的 baseline：
     - Mode 1 = bounded discovery baseline
     - Mode 2 = bounded reproduction baseline
   - 用户给的具体 baseline 灵感来自 `auto-claude-code-research-in-sleep` 风格 prompt，例如：
     - `/research-pipeline start discovering <topic description>, with <seed pdf file path> for reference.`

4. **Dashboard 信息需求已明确**
   - 用户最想在 dashboard 首页看到：
     - 当前运行任务的 milestone/checkpoint timeline
     - recent finished tasks
     - recent artifacts（tables, figures, reports，可点开 modal preview）
     - 资源使用：GPU / CPU / memory / disk
     - token usage overview（rpm/rph/rpd/tpm/tph/tpd）
   - 但经过工程收敛判断，token telemetry 不能硬写成 must-have，除非运行时能稳定提供；目前被保留为条件性需求/候选项

5. **参考仓库探索结论**
   - `Awesome-AI-Scientist` 适合作为：
     - 研究生命周期 framing
     - evaluation / validation / knowledge capture 语言参考
   - 不适合直接作为实现蓝图照搬
   - `auto-claude-code-research-in-sleep`（通过本仓库已有项目研究笔记间接观察）适合作为：
     - Mode baseline 的 workflow / skill / prompt 参考
   - 但不能继承其“过夜全自动科研”的叙事

6. **当前 ainrf 的真实起点已被明确**
   - 当前 `src/ainrf/` 已有：
     - FastAPI API
     - tasks routes
     - health route
     - state store
     - gates
     - events / SSE
     - SSH health / container config 基础
   - 真正缺的不是“后端不存在”，而是：
     - dashboard-friendly task summary layer
     - workspace/session/container summary
     - artifact preview metadata
     - recent tasks / recent artifacts 等聚合层

7. **Git / submodule 处理结果**
   - 已安全 pull/rebase 远端最新 master
   - 已提交并推送这轮重构文档：
     - commit: `c2378f2`
     - message: `docs: add refactoring plan baseline`
   - 已将 `ref-repos/Awesome-AI-Scientist` 注册为 git submodule：
     - commit: `02d8a1b`
     - message: `chore: add Awesome-AI-Scientist submodule`
   - 用户已明确说：`Awesome-AI-Scientist` 子仓库里的 dirty changes **可以忽略**
   - 当前主仓库工作区会显示 submodule dirty，但这是允许的，不应当成为阻塞项
   - 仍保留一个 stash：`temp-user-local-before-rebase`，里面是用户之前无关本地改动（如 `CLAUDE.md`, `uv.lock`, `select.md`），未恢复

## Accomplished

### 已完成

1. **大规模只读探索与规划**
   - 并行探索了现有 docs/framework、docs/index、docs/summary、src/ainrf 边界、文档风格、交叉链接、术语、元数据、Awesome-AI-Scientist 参考价值等
   - 得出了“先叙事重构，再设计收敛，再实现”的总策略

2. **形成了一整套重构规划文档链**
   这些文档最初建在 `docs/LLM-Working/` 根目录，随后被统一迁入 `docs/LLM-Working/refactoring-plan/`，并新增索引页。

   已完成的文档链包括：

   - 项目重定位 / manifesto 规划
   - next release roadmap
   - Mode baseline spec
   - Dashboard baseline spec
   - Architecture baseline plan
   - 三份 contract 文档
   - contracts 到当前 ainrf 的 gap plan
   - refactoring-plan 索引页

3. **文档结构整理**
   - 将这轮长期重构相关的文档集中到：
     - `docs/LLM-Working/refactoring-plan/`
   - 新增：
     - `docs/LLM-Working/refactoring-plan/index.md`
   - 更新：
     - `docs/framework/index.md`
       - 现在引导读者从 `[[LLM-Working/refactoring-plan/index]]` 进入这组长期规划文档
   - 所有主要 wikilink 已修正
   - 文档构建多次验证均通过

4. **worklog 记录**
   - 新增并持续更新：
     - `docs/LLM-Working/worklog/2026-04-04.md`
   - 已记录这轮所有关键 planning / refactor / contract / gap analysis / subdir migration 工作

5. **Git / push**
   - 已把重构规划文档 push 到远端
   - 已把 `Awesome-AI-Scientist` 作为 submodule push 到远端

### 正在进行 / 下一步最自然的工作

当前最自然的下一步不是继续无限写高层规划文档，而是**开始把 gap plan 转成实现切片**。  
之前已明确推荐的首个实现切片是：

1. **Task Summary Layer**
   - 实现 dashboard-friendly 的 task read model / summary layer
   - 不重写 runtime
   - 直接服务后续 dashboard

gap plan 里已经推荐了 4 个实现切片：
1. Task Summary Layer
2. Execution Context Summary Layer
3. Artifact Preview Metadata Layer
4. Recent Tasks / Recent Artifacts 聚合层

### 尚未完成

1. manifesto 正式正文尚未落地（目前是 plan，不是最终正式版）
2. framework 现有主文档尚未正式回写/重写为新叙事（目前只是通过新规划文档和 framework/index 入口做了桥接）
3. architecture 正式实现文档尚未从 baseline plan 变成最终版
4. 上述 4 个推荐 implementation slices 还没有开始改代码
5. token telemetry 是否纳入 next release 仍未最终冻结
6. stash `temp-user-local-before-rebase` 仍在，尚未处理（但与当前主任务无关）

## Relevant files / directories

### 1) 重构规划总目录（本轮最重要）
- `docs/LLM-Working/refactoring-plan/`

其中包含：

- `docs/LLM-Working/refactoring-plan/index.md`
  - 这组重构规划文档的统一入口

- `docs/LLM-Working/refactoring-plan/project-realignment-manifesto-plan.md`
  - 项目重定位、manifesto 职责边界、版本治理思路

- `docs/LLM-Working/refactoring-plan/next-release-realignment-roadmap.md`
  - next release 范围、must-have / deferred、阶段与原子任务方向

- `docs/LLM-Working/refactoring-plan/mode-baseline-spec.md`
  - Mode 1 / Mode 2 baseline 的 next-release 约束

- `docs/LLM-Working/refactoring-plan/dashboard-baseline-spec.md`
  - dashboard 首页、详情页、artifact preview、observability、deferred

- `docs/LLM-Working/refactoring-plan/architecture-baseline-plan.md`
  - next release 实现边界、核心对象、模块责任、frontend/backend baseline

- `docs/LLM-Working/refactoring-plan/task-read-model-contract.md`
  - dashboard 所消费的 task read model contract

- `docs/LLM-Working/refactoring-plan/workspace-session-container-summary-contract.md`
  - workspace / session / container / resource snapshot summary contract

- `docs/LLM-Working/refactoring-plan/artifact-preview-contract.md`
  - artifact preview contract（tables/reports/figures）

- `docs/LLM-Working/refactoring-plan/contracts-to-current-ainrf-gap-plan.md`
  - contracts 与当前 `src/ainrf/` 实现的缺口映射；给出推荐实现 slices

### 2) 工作日志
- `docs/LLM-Working/worklog/2026-04-04.md`
  - 记录本轮所有 planning / refactor / subdir migration / gap mapping 的完成批次

### 3) framework 入口
- `docs/framework/index.md`
  - 已更新“当前规划入口”，现在引导到：
    - `[[LLM-Working/refactoring-plan/index]]`

### 4) 已读/参考的 framework 文档（用于理解旧蓝图与未来态承诺）
- `docs/framework/ai-native-research-framework.md`
- `docs/framework/v1-dual-mode-research-engine.md`
- `docs/framework/v1-rfc.md`
- `docs/framework/v1-roadmap.md`
- `docs/framework/artifact-graph-architecture.md`
- `docs/framework/container-workspace-protocol.md`
- `docs/framework/reference-mapping.md`

这些文档还未正式回写为新叙事，但它们是理解旧蓝图的重要背景。

### 5) 已读/参考的项目调研文档
- `docs/projects/auto-claude-code-research-in-sleep.md`
  - 用于间接提炼 Mode baseline 的 workflow / skill / prompt 风格

### 6) 当前实现相关目录（gap plan 直接对照了这些）
- `src/ainrf/`
- 重点相关文件：
  - `src/ainrf/api/routes/tasks.py`
  - `src/ainrf/api/routes/health.py`
  - `src/ainrf/api/schemas.py`
  - `src/ainrf/state/`
  - `src/ainrf/events/`
  - `src/ainrf/gates/`
  - `src/ainrf/execution/`

### 7) 参考仓库 / submodule
- `ref-repos/Awesome-AI-Scientist/`
  - 现在已是 submodule
  - 当前子仓库内部仍有 dirty changes，但用户明确允许忽略
  - remote: `https://github.com/ResearAI/Awesome-AI-Scientist.git`

### 8) Git 状态相关补充
- 已推送的提交：
  - `c2378f2 docs: add refactoring plan baseline`
  - `02d8a1b chore: add Awesome-AI-Scientist submodule`
- 仍存在一个本地 stash（无关当前主任务）：
  - `stash@{0}: temp-user-local-before-rebase`

### 9) 其他重要背景文件
- `PROJECT_BASIS.md`
  - 用于约束整体项目方向与工作规则
- `docs/index.md`
- `docs/summary/academic-research-agents-overview.md`
  - 用于理解仓库对外叙事与调研层/框架层关系
---

---

