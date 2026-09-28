---
mail_id: MAIL-20260927-1336-management--developer-TASK-rf6-fix
thread: THREAD-LOG-P0
from: management
to: developer
cc: [code_reviewer]
date: 2026-09-27 13:36
purpose: TASK
priority: P1
deadline: 2026-09-27 16:00
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260926-001-rf-a675c8d.md
  - developer/mailbox/inbox/MAIL-20260927-1215-management--developer-TASK-rf-microfix.md
---

## TASK：T-20260926-001-logging-platform-p0 终轮微修复（RF-6 + MIN-1/2/3）

复审 FAIL（RF-6 严重：句柄泄漏）。RF-2/3/4/5 已核销。终轮范围冻结如下 4 项，**不得有任何其他改动（DN5）**：

| 项 | 级别 | 要求 |
|---|---|---|
| RF-6 | 严重 | `rmlog.c` `rmlog__open_locked`（162-175 区域）：删除函数尾部残留的无条件第二次 open（首个 fd 被覆盖泄漏，1000 轮 close→重开 +1000 句柄）。修复后必须**新增自测断言**：emit→close 循环 N 轮（≥500）句柄数不随轮次增长（selftest 新用例或探针留档，给出前后对照数据） |
| MIN-1 | 一般 | IMPL 登记残留（按报告 §6 位置更正） |
| MIN-2 | 一般 | INDEX 登记残留（同上） |
| MIN-3 | 一般 | 请求信"任务书随附入库"声明与 git 实际不符 → 修正声明；1215 任务书原件是否入库由本轮提交一并处理（按收件方应提交原则补入，属流程更正不是扩围） |

## 流程（不变）

修复 → 全量 selftest 重跑留档 → 新 commit → **先发复审请求**（新 hash + 4 项处置）→ 审查通过 → **向 maintainer 发合格确认通知（备料）** → 向 management 报 RESULT。本轮通过后即进入验收，不再有下一轮改动（除非复审发现新的严重级问题）。

## 备注

RF-6 修复注意：确认首个 open 的返回值分支逻辑（成功/失败）与函数返回值语义不变；C 端 `-Wall -Wextra` 零警告复验。若有不可行项 → QUERY。
