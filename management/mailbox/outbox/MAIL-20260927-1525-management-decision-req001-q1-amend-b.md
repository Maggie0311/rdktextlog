---
mail_id: MAIL-20260927-1525-management-decision-req001-q1-amend-b
thread: THREAD-LOG-P0
from: management
to: human-user
cc: [developer, software_tester, code_reviewer]
date: 2026-09-27 15:25
purpose: DECISION
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - management/mailbox/outbox/MAIL-20260926-1635-management-decision-req001-q1q2.md
  - management/script/ACCEPT-20260927-logging-p0.md
---

## DECISION 记录：Q1 裁决修订（A → B）——板端证据改由 software_tester SSH 直连实测

人类用户于 2026-09-27 经对话渠道修订 Q1 裁决：

| 项 | 原裁决（2026-09-26） | **新裁决（2026-09-27）** |
|---|---|---|
| Q1 板端"可运行"证据 | A：用户按 USAGE §3 自测并回贴输出 | **B：用户授权并提供 SSH 访问，software_tester 直连 RDK X5 自行执行测试并出具 TESTREPORT** |

## 影响与执行

1. ACCEPT-20260927-logging-p0.md §3 条件 1 的证据形态相应更新：板端证据 = software_tester 的 TESTREPORT（其契约 §4 冻结字段：被测对象 commit/环境/适配声明/步骤/原始输出/覆盖声明）；
2. 新立任务 **T-20260927-002-logging-boardtest-ssh**（主责 software_tester，唯一主责），测试问题清单由 management 在 TASK 中明确（AC1/AC8 板端项 + UV-1 Linux 多进程×轮转实测 + UV-3 板端工具链编译）；
3. 用户须提供：板子 IP / SSH 账号 / 密码（或已配置的密钥说明），并授权远端执行；
4. 安全边界（写入 TASK）：tester 仅在板端自建工作目录内活动（建议 `/userdata/rmlog_test/` 或用户家目录），**不修改系统配置、不安装系统级软件、不触碰 developer 源码原件（仅拷贝副本）**；
5. Q2（部署路径 /userdata/rmlog）不变。
