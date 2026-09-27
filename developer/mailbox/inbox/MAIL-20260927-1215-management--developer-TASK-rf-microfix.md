---
mail_id: MAIL-20260927-1215-management--developer-TASK-rf-microfix
thread: THREAD-LOG-P0
from: management
to: developer
cc: [code_reviewer]
date: 2026-09-27 12:15
purpose: TASK
priority: P1
deadline: 2026-09-27 18:00
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260926-001-45eeb04.md
  - developer/mailbox/inbox/MAIL-20260927-0922-management--developer-TASK-rework-f1f9.md
---

## TASK：T-20260926-001-logging-platform-p0 复审后微整改（RF-1~RF-5，最后一轮）

复审已 **PASS**（`REVIEW-T-20260926-001-45eeb04.md`：F-1~F-9 全核销，严重级清零，F-1 对账 600/600 成立）。验收前最后一轮微整改，范围冻结如下 5 项，**不得有任何其他改动（DN5）**：

| 项 | 级别 | 要求（方案你自主，效果必须达成） |
|---|---|---|
| RF-1 | 一般 | rmlog.h "close 后 emit 按需重开继续记录" 注释对"显式指定目录"的调用形态失实（复审实测：close 后事件未落显式目录）。二选一：让行为与注释一致（close 后重开逻辑覆盖显式目录形态），或修正注释如实区分两种形态；IMPL 同步说明取舍 |
| RF-2 | 提示 | IMPL 中 810 与留档 813 的数字不一致 → 以实际复跑数据修正（或复跑该探针并更新留档与文档使其一致） |
| RF-3 | 提示 | selftest docstring 中 keep=10 残留表述 → 更正为当前参数与行为描述 |
| RF-4 | 一般 | Windows 写锁 open 失败被计入 `write_failures`（实测 40 条全写成功却计 40 次失败，健康计数失真）→ 该降级改计入 `lock_degradations`（或独立计数），`write_failures` 只反映真实写失败；selftest/文档如涉及同步 |
| RF-5 | 提示 | C 端 rotlock 获取失败无计数（与 Python 端不对称）→ C 端补等价可观测计数（沿用 C 端现有计数器风格即可） |

## 流程（与 R1 相同，顺序不可颠倒）

微整改 → 全量 selftest 重跑留档 → 新 commit → **先发复审请求给 code_reviewer**（新 hash + 5 项逐条处置）→ 审查确认通过 → **向 maintainer 发合格确认通知（备料，契约 §2.1.5：task_id/commit hash/产物路径/构建方式/自测证据/IMPL 与审查报告路径）** → 再向 management 报 RESULT。

## 备注

本轮为 T-001 最后一轮改动；完成后进入验收。若有不可行项 → QUERY，不要猜。
