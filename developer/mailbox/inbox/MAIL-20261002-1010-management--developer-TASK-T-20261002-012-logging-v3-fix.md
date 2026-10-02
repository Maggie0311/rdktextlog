---
mail_id: MAIL-20261002-1010-management--developer-TASK-T-20261002-012-logging-v3-fix
thread: THREAD-LOG-V3
from: management
to: developer
cc: [code_reviewer]
date: 2026-10-02 10:10
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

logging-v3（feature/logging-v3 @ 8ce5162，外部 ChatGPT 开发）经本框架 code_reviewer 独立审查：**CONDITIONAL**（0 阻断/严重，4 一般 F-01~F-04 + 2 提示 F-05/F-06）。本任务修复这 6 项。

## 2. 范围（冻结，只修这 6 项及直接关联）

（详细位置/现象/依据见审查报告，此处给修复要求）
| 项 | 级别 | 修复要求 |
|---|---|---|
| F-01 | 一般 | 黑匣子快照文件加保留上限（数量/总容量二选一并说明），错误风暴下磁盘不无限累积 |
| F-02 | 一般 | 心跳看门狗与 systemd WatchdogSec 接线：daemon 周期 sd_notify WATCHDOG=1 + service 模板设 WatchdogSec；若涉及板端实装部分，做到"代码接线 + 文档标注待板端验证"即可 |
| F-03 | 一般 | DmesgMonitor.stop() 能真正终止阻塞的 dmesg --follow（terminate/kill 子进程，避免线程泄漏） |
| F-04 | 一般 | crash 钩子写遗言后**不抑制 core dump**（signal-safe 写遗言 → 恢复默认处理器 + re-raise，让系统正常 dump core，呼应 REQ P0#2"留 coredump"） |
| F-05 | 提示 | `shared/rmlog_schema.h` 头注释更正（不再误写 rmlog_errors.h） |
| F-06 | 提示 | CommStats 阈值"连续失败数"与 REQ"错误率"措辞对齐——改实现为错误率，或保留连续失败并在 IMPL/注释如实说明"连续失败是错误率的简化代理"，二选一并记录 |

## 3. 约束

- 基座：feature/logging-v3 @ 8ce5162，**`git checkout feature/logging-v3` 后在其上改**；只动上述 6 项，不扩围；
- **不破坏 v1/v2 兼容**（24 错误码、Writer.event/rmlog.event/AsyncWriter.emit 不变）；黑匣子/崩溃/监控的对外行为除上述修复外不变；
- 修复后全量验证：`python -m rmlog.selftest`（13 项）+ `python tests/test_v2_smoke.py` + `python tests/test_v3_smoke.py` + C 侧 gcc `-std=c99 -Wall -Wextra`，全部退出码 0，留档。

## 4. 流程

修复 → 新 commit（含 task_id）→ **先发复审请求给 code_reviewer**（`code_reviewer/mailbox/inbox/MAIL-20261002-HHMM-developer--code_reviewer-REVIEW-REQ-v3-fix.md`，新 hash + 6 项逐条处置 + 验证留档路径，副本自留 outbox）→ 不发 RESULT（板端测/验收后另走）。

## 5. 纪律

只写 developer/** 与投递信件；git 提交先 status + diff --cached 核对、按路径显式 add、禁 -A/.；不触碰 logging-v3-*.bundle、code_reviewer 旧 verify 目录、management 未提交改动。
