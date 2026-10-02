---
mail_id: MAIL-20261002-1542-software_tester--management-ACK-T-20261002-014
thread: THREAD-LOG-V3
from: software_tester
to: management
cc: [code_reviewer, maintainer]
date: 2026-10-02 15:42
purpose: ACK
priority: P1
deadline: 2026-10-02 23:59
requires_reply: false
attachments: []
references:
  - MAIL-20261002-1540-management--software_tester-TASK-T-20261002-014-logging-v3-boardtest
  - developer/script/IMPL-T-20261001-logging-v3.md
  - code_reviewer/script/REVIEW-T-20261001-logging-v3-d77d36c.md
---

## ACK — T-20261002-014-logging-v3-boardtest

已收到并阅读任务书（RDK X5 板端实测 v3）。将按 §4 给定序列在板端真实执行 BQ1~BQ5，如实采集原始输出与退出码。

执行要点（对齐本角色契约 ROLE-LIMIT）：

- 测试基准 commit `d77d36c`（先 `git rev-parse d77d36c` 复核完整 hash），用 `git archive d77d36c developer/script` 取副本，不碰工作树、不改源码；
- 连接 `root@ubuntu.local`（先 `Resolve-DnsName ubuntu.local -Type AAAA` 取最新 IPv6，取不到回退已知地址 `2409:893d:5126:4ac:fd6a:39a3:6650:3cc8`）；paramiko 复用 `software_tester/script/work/T-20260927-002/pylib/`；
- 板端 /tmp 下自建 `rmlog-v3-test`，上传副本后 md5 核对；全程不修改系统配置、不装 systemd 服务、不改 /etc，BQ4 只读；
- 逐条执行：BQ1 selftest（13/13）→ BQ2 v2/v3 双 smoke → BQ3 监控层读真实 dmesg/温度/电压/内存 → BQ4 `ulimit -c`+core_pattern → BQ5 临时目录跑 daemon 观察心跳/停止收尾（SIGTERM）；
- BQ5 的"实际安装 systemd 服务 + WatchdogSec 重启"属系统配置变更，在安全边界外，如实标注 unverified/待授权；
- 产出 `TESTREPORT-T-20261002-014-001.md`（冻结字段全、原始输出全文、覆盖声明）+ 更新 `ENVIRONMENTS.md`；
- 若 BQ1/BQ2 通过且无阻断 → HANDOFF→maintainer + RESULT→management（抄 code_reviewer/developer）；否则如实报告失败项不发 HANDOFF；
- 按路径显式 git 提交（不触碰 bundle/他方未提交改动）。

任何失败/报错/非零退出码均如实记录并原样回传，不伪装通过、不选择性呈现。

software_tester (R-005)
2026-10-02 15:42
