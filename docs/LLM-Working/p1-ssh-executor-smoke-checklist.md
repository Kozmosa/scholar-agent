---
aliases:
  - P1 SSH Executor Smoke Checklist
tags:
  - ainrf
  - execution-layer
  - smoke-test
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# P1 SSH Executor 手工 Smoke 清单

> [!abstract]
> 用于在真实容器上验证 [[framework/v1-roadmap]] 的 P1 默认实现。不替代 `pytest`，只覆盖离线测试无法证明的 SSH/容器联通性。

## 检查项

- 基础连通：连接目标容器并执行 `echo hello`，确认 stdout 返回正常。
- Claude Code 探测：执行 `claude --version`；若未安装，触发 bootstrap 并再次验证版本。
- 环境校验：确认远端 `ANTHROPIC_API_KEY` 已配置。
- 传输回环：上传一个本地小文件到容器，再下载回本地，确认内容一致。
- 健康检查：执行 `ping()`，确认返回 GPU 型号、CUDA 版本、磁盘可用空间和 `project_dir` 可写状态。
- 断连恢复：在首次成功执行后人为断开 SSH，再次执行命令，确认自动重连生效。

## 关联笔记

- [[framework/v1-roadmap]]
- [[framework/v1-rfc]]
- [[framework/container-workspace-protocol]]
