---
id: LTM-011
title: 答疑等于承诺：回答前必须读过那段代码，不能凭文件名或印象作答
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-26-create-maintainer-role]
first_seen: 2026-09-26
last_used: 2026-09-26
last_reviewed: 2026-09-26
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [qa, innate, honesty]
---

## 断言 (Claim)
回答任何关于代码细节与含义的提问前，必须**实际读过相关代码**并给出位置；若一时读不完，应明确说明需读码后回答并给出预计时限，而不是先答一个大概。

## 适用条件 (When it holds)
所有答疑场合。**不适用**于对已归档并已写入说明书的结论的复述（那些已有依据）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | 人类用户 2026-09-26 指令 | 成立 | 要求能回答用户关于代码细节与含义的任何提问，并服务于最终裁决与验收 |
| 2026-09-26 | ROLE-LIMIT §3 必须响应 | 成立 | ≤1 轮内给出有依据的回答，或明确延期 |
| 2026-09-26 | PRINCIPLES KP8 | 成立 | 凭印象作答是产生合理但错误答案的主要路径 |

## 反例 (Counter-evidence)
无。注意时效与准确性的取舍：宁可回我需要先读某文件再答复、下一轮内给出，也不要给一个未经阅读的即时答案。

## 应用方式 (How to apply)
接到提问 → 定位文件 → 读相关段落 → 给出含 `file:line` 的回答 → 记入 `script/QA-LOG.md`；读不完就明确延期。
