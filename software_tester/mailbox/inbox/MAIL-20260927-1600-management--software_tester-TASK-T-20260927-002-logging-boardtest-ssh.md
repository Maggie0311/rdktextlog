---
mail_id: MAIL-20260927-1600-management--software_tester-TASK-T-20260927-002-logging-boardtest-ssh
thread: THREAD-LOG-P0
from: management
to: software_tester
cc: [developer, code_reviewer]
date: 2026-09-27 16:00
purpose: TASK
priority: P1
deadline: 2026-09-27 23:59
requires_reply: true
attachments: []
references:
  - management/script/REQ-20260926-001-logging.md
  - management/script/ACCEPT-20260927-logging-p0.md
  - management/mailbox/outbox/MAIL-20260927-1525-management-decision-req001-q1-amend-b.md
  - code_reviewer/script/REVIEW-T-20260926-001-rf6-2d83644.md
---

## 1. 背景 (Context)

T-20260926-001（rmlog 文本日志平台 P0）已 accepted（有条件）。板端"可运行"证据经 Q1 裁决修订（A→B）改由你 **SSH 直连 RDK X5 实测**。被测对象 = developer 交付终版 commit **`2d83644`**（其产物位于 `developer/script/`；代码已过四轮审查，终审 PASS）。

## 2. 目的 (Objective)

在真实 RDK X5 板端回答 4 个问题（§3），并出 `TESTPLAN` + `TESTREPORT`，作为验收条件 AC1/AC8 板端证据与审查链 unverified 项的实测结论。

## 3. 要回答的问题（测试清单）

| 编号 | 问题 | 对应验收/审查项 |
|---|---|---|
| Q1 | 板端执行 `python3 -m rmlog.selftest` 是否 13/13 全 PASS？ | AC1 板端可运行 |
| Q2 | 平台核查：板端 python3 版本、`/userdata` 分区是否存在、journald 是否持久化（`/var/log/journal` + Storage）、rsyslog 形态、systemd-coredump/coredumpctl 是否可用、`dmesg --time-format iso` 时间戳格式 | AC8 |
| Q3 | **Linux 多进程×轮转组合**是否不出现静默销毁（多 worker + 触发轮转 + 逐 worker 对账）——把审查链 UV-1 的"推演"落成实测 | UV-1（首轮 F-1 的 Linux 行为） |
| Q4 | 板端 gcc/clang 编译 `rmlog.c`（`-std=c99 -Wall -Wextra`）是否零警告？ | UV-3 |

## 4. 连接信息与约束

- **目标**：`2409:893d:5175:915b:7e04:818a:e96a:69ef`（IPv6，**优先用 IPv6**——板子 IPv4 `192.168.128.10` 与本机 IPv4 `172.20.10.3` 不同网段）；端口 22；用户 `root`；密码 `root`（出厂默认）。
- 已预验证：TCP 22 可达、SSH banner 正常（BatchMode 下返回 `Permission denied (publickey,password)`）。
- **本机环境事实**（你以此适配，HOW 自主）：Windows；`ssh.exe` 位于 `C:\Windows\System32\OpenSSH\ssh.exe`；`~/.ssh/known_hosts` 写入被沙箱拦截 → 用 `-o UserKnownHostsFile=<你的工作区路径> -o StrictHostKeyChecking=no` 或 paramiko 的 AutoAddPolicy；`paramiko` 未安装、`plink` 未安装、`pip 26.2.1` 可用（可 `pip install --target <工作区> paramiko`，PyPI 可达性需你确认，不可达则如实报告）。
- **安全边界（硬约束）**：只在板端自建工作目录内活动（建议 `/root/rmlog_test/` 或 `/userdata/rmlog_test/`）；**不修改系统配置、不 apt 安装系统级包、不触碰工作目录之外任何文件**；被测代码只允许用 **commit 2d83644 的副本**（git archive 或 scp 拷贝，不得修改 developer 源码原件）。
- **纪律（你的契约）**：TN3/TN4 禁止伪造/选择性呈现证据；环境每项标注"已验证/假设"；结论只描述"在什么条件下观察到什么"；适配仅限非语义适配且逐条声明。

## 5. 交付物（全部落 `software_tester/script/`）

1. `TESTPLAN-T-20260927-002.md`（回答什么问题/方法/环境/输入/预期/判定标准）；
2. `TESTREPORT-T-20260927-002-001.md`（你的契约 §4 冻结字段：被测对象 commit/环境/适配声明/步骤/原始输出/结果/覆盖声明/unverified 归因/复现性/声明未改源码）；
3. 更新 `ENVIRONMENTS.md`（板端环境每项标注已验证/假设）；
4. 板端原始输出留档（工作区）；
5. git 提交（先 `git status`，按路径显式添加你自己的文件，commit 含 task_id；禁止 `git add -A/.`；他方未提交改动不触碰）；
6. 按你的契约 §2.1.5：**未发现阻断级问题时**向 `maintainer` 发合格确认通知（HANDOFF，含 task_id/commit hash 2d83644/通过角度/报告路径/未覆盖项）；再向 `management` 报 RESULT（抄 developer）。

## 6. 期望回复

ACK ≤1 轮；受阻（认证失败/环境不可得/需改程序才能测）发 QUERY 并如实报告，禁止编造。
