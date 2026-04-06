---
aliases:
  - Mode Baseline Spec
  - Mode 1 / Mode 2 Baseline 规格
tags:
  - scholar-agent
  - mode-spec
  - dashboard
  - requirements
  - implementation-plan
source_repo: scholar-agent
source_path: /Users/kozmosa/code/scholar-agent
last_local_commit: workspace aggregate
---
# Mode 1 / Mode 2 Baseline 规格

> [!abstract]
> 本文档用于把 `scholar-agent` 当前文档中偏未来态的 Mode 1 / Mode 2 定义，收敛成 next release 可执行、可观察、可交付的 baseline 规格。目标不是保留完整“自动科研”承诺，而是固定两类任务模式在下一版中的最小输入、最小流程、最小输出、终止边界和非目标，从而为 manifesto、dashboard 和 architecture 提供统一约束。

## 规格结论

- 当前 `[[framework/v1-dual-mode-research-engine]]` 中的 Mode 1 / Mode 2 仍可保留为蓝图层文档，但不能直接作为 next release 的 requirement。
- next release 只承诺两种 bounded baseline：Mode 1 为 `bounded discovery baseline`，Mode 2 为 `bounded reproduction baseline`。
- 两种模式都应优先消费 `[[projects/auto-claude-code-research-in-sleep]]` 所代表的 skill + prompt 组织方式，但只吸收其 research pipeline baseline，不继承其“过夜全自动科研”叙事。
- baseline 的交付目标不是完整论文、不保证稳定达到 SOTA 复现，也不要求开放式长期自治；交付目标是可启动、可观察、可终止、可归档、可在 dashboard 中稳定展示。

## 为什么必须重写 Baseline

- 当前 framework 主线文档描述的是产品蓝图、长期方向和未来态系统，不适合直接约束 next release。
- 如果直接沿用旧定义，项目会再次落入“Mode 太大、UI 太大、runtime 太大、需求彼此牵连”的 scope explosion。
- baseline 规格的职责，是把 next release 先定义成“可用的研究 dashboard”，而不是“完整研究自动化系统”。

## 统一约束

### 统一目标

- 任务必须能在 dashboard 中被启动、跟踪、回看和归档。
- 任务过程中必须形成结构化 milestone / checkpoint，而不是只留下自由文本日志。
- 失败、阻塞和提前终止都必须成为正式结果，而不是未定义异常。

### 统一边界

- 单用户优先。
- task-centric operator dashboard 优先。
- 任务类别收缩优先于学科泛化。
- evidence-grounded workflow 优先于宏大叙事。

### 统一非目标

- 不承诺跨领域通用研究。
- 不承诺开放式长期无人监督研究。
- 不承诺投稿级写作或论文工厂输出。
- 不承诺稳定完成完整高精度论文复现。

## Mode 1：Bounded Discovery Baseline

### 定位

- Mode 1 在 next release 中不再定义为“文献探索与复现的完整自治系统”，而定义为“有边界的 discovery task baseline”。
- 它主要服务于：给定 topic description 和 seed PDF 后，发起一次可跟踪的研究探索任务，并把阶段进度、发现和工件沉淀到 dashboard 中。

### 典型触发方式

- prompt 形态可参考：`/research-pipeline start discovering <topic description>, with <seed pdf file path> for reference.`
- 这里的 prompt 只是启动入口，不是最终业务语义；系统内部必须把该请求翻译成 task、workspace、artifacts 和 checkpoints。

### 输入基线

- topic description：用户用自然语言给出的研究方向或问题框定。
- seed PDF：至少一份参考论文或综述。
- optional hints：可选的 focus / ignore directions。
- bounded contract：至少包含执行边界，如时间、深度或人工中止条件中的一部分。

### 最小流程

1. 创建 discovery task。
2. 绑定 workspace / session / container 上下文。
3. 使用种子论文和 topic description 启动一次 research pipeline baseline。
4. 生成 milestone / checkpoint timeline。
5. 产出中间和最终 artifacts。
6. 在达到边界、失败、用户取消或自然结束后归档。

### 最小可观察要求

- 当前阶段可见。
- milestone / checkpoint timeline 可见。
- 最近产出 artifacts 可见。
- 最近完成 discovery task 可回看。
- 对用户来说，系统状态不能退化为“只知道任务还在跑”。

### 最小输出

- 结构化任务记录。
- 一组可浏览的工件，至少可包含：notes、tables、reports、figures 中的一部分。
- 明确的终止结果：completed / failed / cancelled / blocked 之一。
- 一份 discovery outcome 摘要，用于说明这次探索到底得到了什么。

### 对参考项目的吸收方式

- 吸收 `[[projects/auto-claude-code-research-in-sleep]]` 中的 `/idea-discovery`、`/research-pipeline`、novelty check 和 reviewer loop 意识。
- 不吸收其“从方向一路串到 paper-writing”的整体承诺。
- 不把外部 reviewer、多模型协作、通知集成等外围能力写成 baseline requirement。

### 明确不承诺

- 不承诺自动递归跑完整文献图谱。
- 不承诺稳定给出高质量 idea 验证。
- 不承诺自动完成高价值论文筛选与复现闭环。
- 不承诺 next release 中完整实现当前 `ExplorationGraph` 的全部蓝图语义。

### 成功标准

- 用户能稳定发起一次 discovery task。
- 用户能在 dashboard 中看见这次 task 的时间线、近期工件和结果摘要。
- 任务结束后有明确归档状态和可回看的 artifacts。
- 失败不会频繁破坏状态或让任务进入不可理解的悬空状态。

## Mode 2：Bounded Reproduction Baseline

### 定位

- Mode 2 在 next release 中不再定义为“从零高精度深度复现论文方法的完整系统”，而定义为“有边界的 reproduction task baseline”。
- 它主要服务于：围绕目标论文、目标表格或明确实验目标，发起一次可跟踪的实现 / 复现任务，并把结果工件以 dashboard 可预览的方式呈现出来。

### 典型触发方式

- 启动入口可以是目标论文 + 目标结果，也可以是面向 skill 的 reproduction prompt。
- 与 Mode 1 一样，prompt 只是入口；系统内部必须转换为 task、workspace、artifacts 和 checkpoints。

### 输入基线

- target paper：至少一篇目标论文。
- target result：至少一个明确的结果目标，例如目标表格、指标或复现范围。
- workspace / container context。
- bounded contract：至少有预算、时间、轮次或人工中止边界之一。

### 最小流程

1. 创建 reproduction task。
2. 绑定 workspace / session / container。
3. 启动 baseline implementation / reproduction 流程。
4. 记录 checkpoint 和中间工件。
5. 生成结果产物并归档。
6. 在完成、失败、取消或阻塞时结束任务。

### 最小可观察要求

- 当前任务阶段可见。
- 当前 checkpoint / milestone 可见。
- 结果工件可预览。
- 任务结束后可回看 artifacts、结果摘要和终止原因。

### 最小输出

- 结构化任务记录。
- 至少一类可预览结果工件：table / report / figure。
- reproduction outcome 摘要。
- 明确终止状态与原因。

### 对参考项目的吸收方式

- 吸收 `[[projects/auto-claude-code-research-in-sleep]]` 中的 `run-experiment`、`monitor-experiment`、`analyze-results` 和 reviewer loop 思路。
- 不继承其完整 paper-writing、通知、MCP、多模型组合等外围能力。
- 不把“深度复现 = 高精度还原论文所有结果”写成 next release 承诺。

### 明确不承诺

- 不承诺稳定达到完整高精度复现。
- 不承诺自动从零实现完整方法并跑完整实验套件。
- 不承诺自动完成偏差归因的完整科学评估。
- 不承诺 next release 中完整实现当前 `QualityAssessment` 蓝图语义。

### 成功标准

- 用户能稳定发起一次 reproduction task。
- 用户能在 dashboard 中看到任务进度、近期结果工件和结果摘要。
- 系统能把失败、阻塞和提前结束作为正式输出，而不是隐式吞掉。
- 结果工件能被预览，而不是只能从容器或磁盘手工翻找。

## Dashboard 对两种 Mode 的共同要求

### 必须可见的信息

- 当前运行任务的 milestone / checkpoint timeline。
- recent finished tasks。
- recent artifacts。
- workspace resources snapshot：GPU / CPU / memory / disk。

### 必须可预览的工件

- tables：CSV / Markdown。
- reports：Markdown。
- figures：SVG / PNG。

### 条件性需求

- token usage overview 只在运行时能稳定提供 telemetry 时纳入 next release；否则延期，不可反向绑架 mode baseline。

## 对 Architecture 的约束

- 不能先为了追求完整 research runtime，而牺牲 dashboard、stability、observability 三项核心。
- 不能把 next release 定义成“先实现完整 TaskEngine，再顺便补 UI”。
- architecture 应优先服务于 task tracking、workspace management、SSH integration、artifact preview 和 checkpoint timeline。

## 对后续文档的回写要求

- manifesto 需要引用本文，作为 requirements / expectations 的模式约束。
- next release roadmap 需要引用本文，作为 must-have / deferred 划分依据。
- 后续 architecture baseline 需要显式说明：每个 mode 的 backend / frontend contract 如何满足这里的最小要求。
- `[[framework/v1-dual-mode-research-engine]]` 后续需要增加说明：当前文档是蓝图层，next release baseline 以本文为准。

## 当前建议的后续原子任务

1. 把本文的 Mode 1 / Mode 2 基线回写到 manifesto 规划。
2. 把本文的 dashboard 共同要求回写到 next release roadmap。
3. 起草 architecture baseline，明确 task、workspace、session、artifact preview 的实现边界。
4. 评估 token telemetry 是否应保留在 next release 候选需求中。

## 关联笔记

- [[LLM-Working/refactoring-plan/project-realignment-manifesto-plan]]
- [[LLM-Working/refactoring-plan/next-release-realignment-roadmap]]
- [[framework/v1-dual-mode-research-engine]]
- [[framework/v1-rfc]]
- [[projects/auto-claude-code-research-in-sleep]]
