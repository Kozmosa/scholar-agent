---
aliases:
  - P2 MinerU Smoke Checklist
  - P2 论文解析联调清单
tags:
  - ainrf
  - orchestrator
  - mineru
  - smoke-test
source_repo: scholar-agent
source_path: /home/xuyang/code/scholar-agent
last_local_commit: workspace aggregate
---
# P2 MinerU 手工 Smoke 清单

> [!abstract]
> 用于在真实 MinerU Cloud API 上验证 [[framework/v1-roadmap]] 的 P2 默认实现。目标是确认当前 `MinerUClient` 已按官方 batch 契约工作：申请上传 URL、上传 PDF、轮询 batch 结果、下载 `full_zip_url` 压缩包，并从其中提取 `full.md` 与 `content_list.json`。

## 官方契约对齐点

- 认证头：`Authorization: Bearer <token>`
- 本地 PDF 上传入口：`POST /api/v4/file-urls/batch`
- 远端 URL 解析入口：`POST /api/v4/extract/task/batch`
- 结果轮询入口：`GET /api/v4/extract-results/batch/{batch_id}`
- 终态结果字段：`data.extract_result.state == done`
- 成功产物字段：`data.extract_result.full_zip_url`

## 前置条件

- 已配置环境变量：
  - `AINRF_MINERU_BASE_URL`
  - `AINRF_MINERU_API_KEY`
- 可用测试 PDF：
  - 一份结构良好的论文 PDF
  - 一份故意损坏或截断的 PDF
- 本地安装依赖已完成：`UV_CACHE_DIR=/tmp/uv-cache uv sync --dev`

## 建议执行方式

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run python - <<'PY'
from __future__ import annotations

import asyncio
from pathlib import Path

from ainrf.parsing import MinerUClient, MinerUConfig, ParseRequest


async def main() -> None:
    client = MinerUClient(MinerUConfig.from_env())
    result = await client.parse_pdf(ParseRequest(pdf_path=Path("TMP_PDF_PATH")))
    print(type(result).__name__)
    print(result)


asyncio.run(main())
PY
```

把 `TMP_PDF_PATH` 替换成真实文件路径。

## 检查项

- 正常 PDF 首次解析
  - 返回 `ParseResult`
  - `provider_task_id` 为真实 `batch_id`
  - `markdown` 非空，且包含标题和至少 3 个 section
  - `warnings` 为空或只包含可接受的弱警告
- 首次请求链路
  - 观察日志或抓包，确认顺序为：
    - `POST /api/v4/file-urls/batch`
    - `PUT <presigned-upload-url>`
    - `GET /api/v4/extract-results/batch/{batch_id}` 轮询
    - `GET <full_zip_url>`
- 压缩包内容
  - 确认 `full_zip_url` 可下载
  - 压缩包内存在 `full.md`
  - 若存在 `content_list.json` 或 `_content_list.json`，客户端能提取图像/表格条目
- 缓存命中
  - 对同一 PDF 再跑一次
  - 返回 `ParseResult(cache_hit=True)`
  - 不再触发新的远端 batch 创建
- 损坏 PDF
  - 返回 `ParseFailure`
  - `failure_type` 应为 `provider_rejected`、`invalid_response` 或供应商明确失败态之一
  - 不应抛未处理异常
- 限流或超时
  - 人为降低账号限额或在弱网环境运行
  - 确认客户端会重试
  - 重试耗尽后返回 `rate_limit_exhausted` 或 `timeout`

## 排障提示

- `401` 或 `403`
  - 优先检查 `AINRF_MINERU_API_KEY` 是否有效，认证头是否为 `Bearer`
- `POST /api/v4/file-urls/batch` 成功但 `PUT` 失败
  - 通常是预签名 URL 过期、网络代理污染或请求头不兼容
- 轮询长期不结束
  - 检查 `batch_id` 是否正确，以及服务端状态是否卡在非终态
- `full_zip_url` 下载成功但解压失败
  - 说明返回内容不是标准 zip；记录原始响应头和 body 大小，便于回查供应商异常
- `missing_abstract` / `insufficient_sections`
  - 先判断是真实论文结构问题，还是 MinerU 输出质量退化

## 关联笔记

- [[framework/v1-roadmap]]
- [[framework/v1-rfc]]
- [[LLM-Working/p2-mineru-implementation-plan]]
