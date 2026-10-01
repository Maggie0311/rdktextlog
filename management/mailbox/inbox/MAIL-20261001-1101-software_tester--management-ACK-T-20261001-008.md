---
mail_id: MAIL-20261001-1101-software_tester--management-ACK-T-20261001-008
thread: THREAD-LOG-V2
from: software_tester
to: management
cc: [developer]
date: 2026-10-01 11:01
purpose: ACK
priority: P1
deadline: 2026-10-01 23:59
requires_reply: false
attachments: []
references:
  - MAIL-20261001-1058-management--software_tester-TASK-T-20261001-008-logging-v2-boardtest
  - developer/script/PLAN-T-20260930-005-logging-v2.md
  - developer/script/IMPL-T-20260930-005-logging-v2.md
---

## ACK — T-20261001-008-logging-v2-boardtest

已收到并阅读任务书。将按 §4 给定序列在 RDK X5 板端真实执行 v2 板端自测与五域故障注入，并如实采集原始输出与退出码。

执行要点（对齐本角色契约 ROLE-LIMIT）：

- 测试基准 commit `d2e1081`，先 `git log -1 --format=%H feature/logging-v2` 复核；
- 连接 `root@ubuntu.local`（先 `Resolve-DnsName ubuntu.local -Type AAAA` 取最新 IPv6，取不到回退已知地址）；
- 全程仅在板端 `/tmp` 下活动（`/tmp/rmlog-v2`、`/tmp/rmlog-fault-*`），不碰系统配置、不安装包、不改源码（只用 developer/script 副本）；
- 逐条执行：身份与环境核查 → 上传 → selftest → smoke → 五域故障注入，每步 stdout/stderr/退出码完整落盘；
- 产出 `TESTREPORT-T-20261001-008-001.md`（冻结字段全、原始输出全文、覆盖声明明确本轮为 v2 板端自测事实采集、未做压力/长时/断电项）+ 更新 `ENVIRONMENTS.md`；
- 完成后发 RESULT（抄 developer），并按路径显式 git 提交（不触碰 `logging-v2.bundle`、不改动 developer/ 与他方产物）。

任何失败/报错/非零退出码均如实记录并原样回传，不伪装通过。

software_tester (R-005)
2026-10-01 11:01
