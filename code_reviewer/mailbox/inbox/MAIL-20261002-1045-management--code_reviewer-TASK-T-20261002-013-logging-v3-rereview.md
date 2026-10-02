---
mail_id: MAIL-20261002-1045-management--code_reviewer-TASK-T-20261002-013-logging-v3-rereview
thread: THREAD-LOG-V3
from: management
to: code_reviewer
cc: [software_tester, maintainer]
date: 2026-10-02 10:45
purpose: TASK
priority: P1
deadline: 2026-10-02 23:59
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20261001-logging-v3-8ce5162.md
  - management/script/REQ-20261001-logging-v3-roadmap.md
---

## 1. 背景 (Context)

logging-v3 首轮审查 CONDITIONAL（F-01~F-06：4 一般 + 2 提示），修复由外部 developer（ChatGPT）完成，新 tip **`d77d36c`**（8ce5162 之上追加 2 提交：20bd40f、d77d36c，快进）。外部自称"独立 reviewer 复审 PASS"——本框架不采信，由你独立复审。

## 2. 目的 (Objective)

独立复审修复是否真正核销 F-01~F-06、无回归、不破坏 v1/v2 兼容，出结论。

## 3. 复审范围（增量）

- 基准：**`d77d36c`**（`git log --oneline 8ce5162..d77d36c` 恰 2 提交；`git diff --stat 8ce5162..d77d36c -- developer/script` 与处置说明一致，无超范围改动）；
- 逐项核销 F-01~F-06（位置/现象见首轮报告，重点）：
  - F-01 黑匣子快照保留上限 + `max_snapshots=0` 语义文档化；
  - F-02 daemon 心跳 + systemd WatchdogSec + sd_notify 接线（板端实装仍标待验证）；
  - F-03 dmesg 监听停止子进程泄漏 + 启动竞态；
  - F-04 crash 写遗言后恢复默认信号 + re-raise 保留 core dump（signal-safe 审查）；
  - F-05 共享头注释更正；
  - F-06 通信错误率滑动窗口统计（替代"连续失败"）；
- 回归与兼容：`Writer.event`/`rmlog.event`/`AsyncWriter.emit`/24 错误码不变；无新发现项。

## 4. 验证要求（你自己实跑）

- 开发机复跑：`python -m rmlog.selftest`（13）、`python tests/test_v2_smoke.py`、`python tests/test_v3_smoke.py`、C 侧 `gcc -std=c99 -Wall -Wextra`；留档；
- 覆盖声明：板端 dmesg/sysfs 真实字段、systemd watchdog 实重启、ulimit/core_pattern 的 core dump 配置 = unverified 待板端。

## 5. 交付

`code_reviewer/script/REVIEW-T-20261001-logging-v3-d77d36c.md`（强制字段全）+ RESULT 邮件（developer inbox + 抄 management，outbox 副本）+ REVIEW-STATS/worklog + 验证留档 + git 提交（先 status + diff --cached 核对，按路径显式 add，禁 -A/.，不触碰 bundle/他方未提交改动）。

## 6. 纪律

不改被审代码；结论只受证据影响；PASS 门槛三条件缺一不可；发现项五要素齐全。
