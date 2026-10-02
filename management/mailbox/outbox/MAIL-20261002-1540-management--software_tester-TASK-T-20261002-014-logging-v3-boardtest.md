---
mail_id: MAIL-20261002-1540-management--software_tester-TASK-T-20261002-014-logging-v3-boardtest
thread: THREAD-LOG-V3
from: management
to: software_tester
cc: [code_reviewer, maintainer]
date: 2026-10-02 15:40
purpose: TASK
priority: P1
deadline: 2026-10-02 23:59
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20261001-logging-v3-d77d36c.md
  - management/script/REQ-20261001-logging-v3-roadmap.md
  - developer/script/IMPL-T-20261001-logging-v3.md
---

## 1. 背景 (Context)

logging-v3（feature/logging-v3，commit **`d77d36c`**）已通过本框架 code_reviewer 复审（PASS，F-01~F-06 全核销）。现做**板端真机实测**，作为 v3 验收的板端证据。v3 新增黑匣子、崩溃遗言、监控层（dmesg/温度/电压/内存）、错误码双轨等。

## 2. 目的 (Objective)

在 RDK X5 板端实测 v3，回答以下问题并出 TESTREPORT。

## 3. 连接与基准

- 测试基准 commit **`d77d36c`**（`git archive d77d36c developer/script` 取副本，不改源码）；
- 板端：`root@ubuntu.local`，root/root；已知 IPv6 `2409:893d:5126:4ac:fd6a:39a3:6650:3cc8`（已预验证端口 22 开放、sshd 应答）；IPv6 可能轮换，先 `Resolve-DnsName ubuntu.local -Type AAAA` 取最新，取不到回退已知地址；
- paramiko 复用 `software_tester/script/work/T-20260927-002/pylib/`。

## 4. 测试清单（回答的问题）

| 编号 | 问题 | 判定 |
|---|---|---|
| BQ1 | 板端 `python3 -m rmlog.selftest` 是否 13/13 PASS？ | 退出码 0 |
| BQ2 | 板端 `test_v2_smoke.py` / `test_v3_smoke.py` 是否双 PASS？ | 退出码 0 |
| BQ3 | v3 监控层在板端读**真实** dmesg/sysfs 字段（温度/电压/内存）是否正常（非报错/非空）？ | 观察事实 |
| BQ4 | `ulimit -c` 与 `cat /proc/sys/kernel/core_pattern` 当前值，确认 core dump 配置现状 | 记录事实 |
| BQ5 | systemd watchdog：daemon 心跳 + sd_notify 代码路径在板端能否跑通（临时目录跑 daemon，观察心跳/停止收尾） | 观察事实；**"实际安装 systemd 服务 + WatchdogSec 重启"属系统配置变更，不在本次安全边界内，如实标注 unverified/待授权** |

## 5. 安全边界（硬约束）

仅板端 /tmp 自建工作目录内活动；**不修改系统配置、不安装 systemd 服务、不改 /etc 任何文件**；被测代码只用 d77d36c 副本；BQ4 只读不写。

## 6. 交付（落 `software_tester/script/`）

1. 原始输出留档 `software_tester/script/work/T-20261002-014-boardtest/raw/`；
2. `TESTREPORT-T-20261002-014-001.md`（冻结字段全：被测对象 d77d36c/环境/适配声明/步骤/原始输出全文/结果/覆盖声明/unverified 归因/复现性/未改源码声明）；覆盖声明写明"BQ5 的 systemd 实装重启未做（系统配置变更，安全边界外）"；
3. 更新 ENVIRONMENTS.md（板端事实）；
4. 若 BQ1/BQ2 通过且无阻断级问题 → 向 maintainer 发 HANDOFF（备料，含 commit d77d36c/通过角度/报告路径/未覆盖项）；再向 management 报 RESULT（抄 code_reviewer、developer，副本自留 outbox）；
5. git 提交：先 status + diff --cached --name-only，按路径显式 add 自己文件，禁 -A/.，不触碰 bundle/他方未提交改动，commit 含 task_id。

## 7. 纪律

TN3/TN4 不伪造/选择性呈现；环境每项标 已验证/假设；结论只描述"在什么条件下观察到什么"；不改源码；适配仅限非语义且逐条声明。
