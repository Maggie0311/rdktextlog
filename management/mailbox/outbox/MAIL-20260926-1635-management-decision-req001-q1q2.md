---
mail_id: MAIL-20260926-1635-management-decision-req001-q1q2
thread: THREAD-LOG-P0
from: management
to: human-user
cc: [developer, software_tester]
date: 2026-09-26 16:35
purpose: DECISION
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - management/script/REQ-20260926-001-logging.md
  - management/mailbox/outbox/MAIL-20260926-1622-management--human-user-QUERY-req001-q1-q2.md
---

## DECISION 记录：REQ-20260926-001 开放问题 Q1/Q2（人类用户已裁决）

人类用户于 2026-09-26 经对话渠道裁决：

| 问题 | 裁决 | 影响 |
|---|---|---|
| Q1 初步开发代码在哪跑 | **A：由人类用户按 USAGE.md 在 RDK X5 板端运行自测并回贴输出** | 板端"可运行"证据 = 用户实测输出；`software_tester` 后续以该输出为板端证据（另立小任务，不改动 T-001 范围）；风险"板端不可达致证据缺失"解除 |
| Q2 部署身份与路径 | **认可默认值：root + `/userdata/rmlog/`**（该路径不存在时回退 `/var/log/rmlog/`） | 均做成可配置项；USAGE 以该默认值书写 |

## 执行动作

1. 已发 TASK 增补给 `developer`（同 thread）：USAGE.md 增加「板端自测步骤（用户执行）」一等章节；开发机证据（Windows + Python 3.13/3.14 + gcc 13.2）随 RESULT 提供；Windows 与 Linux 的平台差异（O_APPEND 语义、路径、权限）如实写入 IMPL 已知风险；
2. REQ-20260926-001-logging.md §7 的 Q1/Q2 由本 DECISION 结案（后续修订在该文件追加"裁决记录"节，不改写历史）；
3. `software_tester` 的板端证据任务待用户回贴实测输出后由 management 评估立项。
