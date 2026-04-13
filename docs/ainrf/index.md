---
aliases:
  - AINRF 使用文档
  - AINRF Usage Guide
tags:
  - ainrf
  - cli
  - docs
  - obsidian-note
source_repo: scholar-agent
source_path: docs/ainrf/index.md
last_local_commit: workspace aggregate
---
# AINRF 使用文档

> [!abstract]
> 本页只记录当前仓库里已经存在、可直接看到的命令入口与使用方式，不展开历史 RFC、未落地能力或未来运行时设想。

## AINRF 是什么

AINRF 是 `scholar-agent` 仓库里当前可见的命令入口与运行时壳层，主要覆盖两类表面：

- 文档站点的本地预览与构建入口。
- `uv run ainrf serve` 对应的 API 服务入口，以及初始化、容器配置等 CLI 子命令。

当前如果把它拆成“前后端”来理解，较准确的说法是：

- 当前“frontend”更接近文档站点预览。
- 当前“backend”更接近 `uv run ainrf serve` 启动的 API 服务。

这里不把历史设计文档中的更大目标、RFC 术语或运行时愿景表述成已经完成的现实能力。

## 快速开始

建议先确认本地命令入口是否可见：

```bash
uv run ainrf --version
uv run ainrf --help
```

如果你的目标是阅读与预览仓库知识库，优先使用文档站点命令；如果你的目标是查看当前 AINRF 服务入口，再使用 `serve` 与相关帮助命令。

## 启动文档预览

本仓库已经提供脚本化入口：

```bash
scripts/serve.sh
```

它对应的实际执行命令是：

```bash
uv run python scripts/build_html_notes.py serve
```

这个入口更适合在本地连续查看 `docs/` 下的笔记内容与站点效果。就当前仓库现实而言，这一层更接近文档站点预览，而不是独立产品化前端。

## 构建文档站点

构建静态站点时可直接使用脚本：

```bash
scripts/build.sh
```

它对应的实际执行命令是：

```bash
uv run python scripts/build_html_notes.py build
```

这一流程会把 `docs/` 中的笔记转换为站点构建输入，再生成最终静态输出。生成目录属于构建产物，应继续只改源文档，不直接改生成结果。

## 启动 AINRF 服务

当前 `ainrf` 的服务入口是：

```bash
uv run ainrf serve
```

如果只想先看参数与说明，可用：

```bash
uv run ainrf serve --help
```

从现有代码看，`serve` 对应的是 API server 入口，因此这里更接近当前仓库的后端服务面，而不是完整研究系统的全部运行时能力。

## 首次初始化

当前首次初始化入口是：

```bash
uv run ainrf onboard
```

它用于准备服务运行所需的本地状态与配置。若后续 `serve` 提示缺少必要配置，应先回到这个初始化入口，而不是假设仓库已经具备自动完成所有运行时准备的能力。

## 其他命令入口

除初始化与服务启动外，当前还能直接看到的命令入口包括：

```bash
uv run ainrf container add
uv run ainrf container add --help
```

这组命令用于写入容器配置项。就当前可见表面来说，它是一个配置型入口，不应被解读为已经提供完整容器编排、任务调度或多节点运行能力。

## 常用开发与验证命令

如果你在仓库内做日常开发或文档更新，当前常见检查命令包括：

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

它们分别用于测试、静态检查与格式检查。对于仅修改文档的工作，这些命令是否执行可以按变更范围决定，但它们仍是当前仓库最直接的验证入口。

## 说明与边界

- 本页只描述当前代码与脚本已经暴露出来的命令表面。
- `scripts/serve.sh` 与 `uv run python scripts/build_html_notes.py serve` 主要服务于文档站点预览。
- `scripts/build.sh` 与 `uv run python scripts/build_html_notes.py build` 主要服务于文档站点构建。
- `uv run ainrf serve` 是当前更接近后端 API 服务的入口。
- `uv run ainrf onboard` 与 `uv run ainrf container add` 是当前已经存在的初始化/配置型 CLI 入口。
- 不应把历史 RFC、路线图或更大运行时 ambition 直接表述为当前已经交付的命令能力。

## 关联笔记

- [[framework/index]]
- [[framework/ai-native-research-framework]]
- [[index]]
