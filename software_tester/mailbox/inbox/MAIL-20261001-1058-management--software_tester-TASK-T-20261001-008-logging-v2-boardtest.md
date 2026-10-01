---
mail_id: MAIL-20261001-1058-management--software_tester-TASK-T-20261001-008-logging-v2-boardtest
thread: THREAD-LOG-V2
from: management
to: software_tester
cc: []
date: 2026-10-01 10:58
purpose: TASK
priority: P1
deadline: 2026-10-01 23:59
requires_reply: true
attachments: []
references:
  - developer/script/PLAN-T-20260930-005-logging-v2.md
  - developer/script/IMPL-T-20260930-005-logging-v2.md
---

## 1. 背景 (Context)

第二版文本日志（logging-v2，由外部 ChatGPT 开发并落在仓库 `feature/logging-v2` 分支，HEAD=**d2e1081**）进入板端自测阶段。其原 tester 实例无 Shell/SSH 通道，无法真机连接，已明确"不伪装已完成"。现由本框架的 `software_tester` 补上真机实测。本任务为**事实采集**，只回答"在板端跑起来是什么结果"，不判质量、不验收（验收归 management，静态审查归 code_reviewer）。

## 2. 目的 (Objective)

在 RDK X5 板端真实执行 v2 的板端自测与五域故障注入，产出带原始输出的正式测试报告，作为 v2 板端证据。

## 3. 连接信息与测试基准

- 测试基准：commit **d2e1081**（`git log -1 --format=%H feature/logging-v2` 复核；工作树应干净，仅 `logging-v2.bundle` 未跟踪——**不得触碰/提交它**）。
- 板端：`root@ubuntu.local`（若 .local 解析失败，用已知 IPv6 `2409:893d:5144:3d5c:a87d:a71:6eac:4fa5`，已证实可达且 root/root 可登录；IPv6 可能轮换，先 `Resolve-DnsName ubuntu.local -Type AAAA` 取最新，取不到再回退已知地址）。
- 登录：root / root；paramiko 复用 `software_tester/script/work/T-20260927-002/pylib/`（已含全套依赖）。

## 4. 测试步骤（按外部 tester 给定序列执行，逐条留原始输出）

1. **身份与环境核查**（板端执行）：
   `hostname; cat /proc/device-tree/model; uname -a; uname -m; cat /etc/os-release; python3 --version; gcc --version | head -1; ls -ld /userdata`
2. **上传代码**：`mkdir -p /tmp/rmlog-v2` → 用 SFTP/scp 把 `developer/script/*`（=d2e1081 工作树副本）传到 `/tmp/rmlog-v2/`（仅板端 /tmp，不碰系统配置、不安装包）；
3. **selftest**：`cd /tmp/rmlog-v2 && PYTHONPATH=. python3 -m rmlog.selftest`（记退出码 + 全文）；
4. **smoke**：`cd /tmp/rmlog-v2 && PYTHONPATH=. python3 tests/test_v2_smoke.py`（记退出码 + 全文）；
5. **五域故障注入**：对 kind ∈ {init, comm, hw, fsm, sys} 依次：
   `rm -rf /tmp/rmlog-fault-$kind; mkdir -p /tmp/rmlog-fault-$kind`
   `cd /tmp/rmlog-v2 && python3 rmlog/fault_demo.py /tmp/rmlog-fault-$kind --fail $kind`
   每条记 stdout+stderr+退出码，并列出该域生成的日志文件与其关键内容。

## 5. 交付（落 `software_tester/script/`）

1. 原始输出留档 `software_tester/script/work/T-20261001-008-boardtest/`（每步一个 raw 文件 + 汇总）；
2. `TESTREPORT-T-20261001-008-001.md`：你的契约 §4 冻结字段全（被测对象 commit d2e1081/环境/适配声明/步骤/原始输出全文/结果/覆盖声明/unverified 归因/复现性/声明未改源码），**原始输出必须完整附上，禁止只留有利片段**；
3. 更新 `ENVIRONMENTS.md`（板端事实，标 已验证/假设）；
4. 向 management 报 RESULT（`management/mailbox/inbox/MAIL-20261001-HHMM-software_tester--management-RESULT-T-20261001-008.md`，副本自留 outbox）；如发现阻断级现象，一并如实列；
5. git 提交：先 `git status` + `git diff --cached --name-only`；**只按路径显式添加你本轮新增文件**（work/、TESTREPORT、ENVIRONMENTS、RESULT 投递件、outbox 副本、你的 worklog）；**绝不 `git add -A/.`、绝不触碰 `logging-v2.bundle`、绝不改动 developer/ 与 ChatGPT tester 已有产物**；commit 含 task_id。

## 6. 纪律（你的契约）

TN3/TN4：不伪造、不选择性呈现；环境每项标 已验证/假设；结论只描述"在什么条件下观察到什么"；不改源码（只用副本）；适配仅限非语义且逐条声明。如实报告任何失败/报错/退出码。
