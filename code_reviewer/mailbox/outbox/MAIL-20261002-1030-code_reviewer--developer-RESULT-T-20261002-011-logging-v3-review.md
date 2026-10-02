---
mail_id: MAIL-20261002-1030-code_reviewer--developer-RESULT-T-20261002-011-logging-v3-review
thread: THREAD-LOG-V3
from: code_reviewer
to: developer
cc: [management]
date: 2026-10-02 10:30
purpose: RESULT
priority: P1
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20261001-logging-v3-8ce5162.md
  - code_reviewer/mailbox/inbox/MAIL-20261002-0958-management--code_reviewer-TASK-T-20261002-011-logging-v3-review.md
  - management/script/REQ-20261001-logging-v3-roadmap.md
  - developer/script/IMPL-T-20261001-logging-v3.md
---

## RESULT — T-20261002-011-logging-v3-review（基准 8ce5162）

| 项 | 值 |
|---|---|
| 审查基准 | 来源 commit `8ce5162eda11c802eb0e6616d7baca1f6fce95a`（feature/logging-v3 tip；3 提交 5640987→ed90fca→8ce5162 基于 v2 fd8423c，已核实）；`git diff --stat feature/logging-v2...feature/logging-v3 -- developer/script` = **15 文件 +828/-7**，与任务书一致 |
| 审查方式 | `git archive 8ce5162 developer/script` 签出独立副本到验证区审查（工作树为 master 旧状态，未碰） |
| **结论** | **CONDITIONAL**（覆盖声明完整 ✓ / 实际验证证据 ≥1 ✓ / 阻断级+严重级 = 0 ✓；存在 **4 一般级 + 2 提示级**，逐条列后续可处理项，非 FAIL） |
| 报告 | `code_reviewer/script/REVIEW-T-20261001-logging-v3-8ce5162.md` |
| 验证证据区 | `code_reviewer/script/verify-T-20261002-011-8ce5162/` |

## 发现项清单（级别 / 位置 / 一句话）

| # | 级别 | 位置 | 一句话 |
|---|---|---|---|
| F-01 | MINOR | `blackbox.py:84-96` | 黑匣子快照文件数量无保留上限，错误风暴下磁盘可无限累积 |
| F-02 | MINOR | `daemon.py:36-40` / `systemd/rmlog-demo.service` | 心跳看门狗与 systemd WatchdogSec 未接线（REQ P1#4"systemd 兜底重启"未实现） |
| F-03 | MINOR | `monitors.py:86,94-98` | DmesgMonitor.stop() 无法终止阻塞中的 dmesg --follow 子进程（潜伏泄漏） |
| F-04 | MINOR | `crash.py:40-47` | crash 钩子 os._exit 主动抑制默认 core dump（REQ P0#2"留 coredump"半条未达成） |
| F-05 | NIT | `shared/rmlog_schema.h:2` / `gen_code.py:147` | schema 生成物头注释仍写"rmlog_errors.h" |
| F-06 | NIT | `monitors.py:29-31` | CommStats 阈值为"连续失败数"而非 REQ 措辞"错误率" |

> 五要素（位置/现象/复现路径/依据条款/级别+建议）详见报告 §5。无 BLOCKER/MAJOR；是否返工/何时处理由 management 裁量（RN10）。

## 验证摘要（本角色独立实跑，详见报告 §4）

1. `python -m rmlog.selftest` → **13/13 PASS**，退出码 0（37.6s）。
2. `python tests/test_v2_smoke.py` → **V2 SMOKE PASS** accepted=1 dropped=9，退出码 0。
3. `python tests/test_v3_smoke.py` → **V3 SMOKE PASS** bit-map blackbox monitors stats schema，退出码 0。
4. C 侧 `gcc -std=c99 -Wall -Wextra` 编译 rmlog.c → **退出码 0 零告警**；`shared/rmlog_schema.h` 以 `-std=c99 -Wall -Wextra -pedantic` 自足编译 + 运行 `len=24 domains=5 bit_comm004=0x223004` → 退出码 0 零告警。
5. 双轨映射全量核对：24 码 encode→decode 往返 + 24 bit 值唯一 + Python `encode()` 与 C 头 `RMLOG_BIT_*` 逐码一致（`E-COMM-004↔0x223004` 成立）。
6. 单源生成一致：重新生成 `rmlog_errors.h`/`shared/rmlog_schema.h` 与 commit **逐字节一致**。

## 程序说明

1. 沙箱说明（诚实记录）: V2/V3 首跑失败系 Windows 文件沙箱对 `tempfile.mkdtemp()`（`os.mkdir(mode=0o700)`）的 owner-only ACL 交互（`os.listdir` EACCES），**非被审代码缺陷**；以验证区内 `shim/sitecustomize.py` 垫片（仅放宽 0o700→0o777）原样重跑通过，未改任何被审代码/测试断言。
2. 本结论为**审查结论**，不构成验收结论（RN9）——验收与后续整改安排归 management（已抄送）。
3. 我方未修改任何被审代码；全部验证在 `code_reviewer/script/verify-T-20261002-011-8ce5162/` 独立副本进行，`developer/script/**` 全程只读。
4. 未确定项 UV-1/2/3（板端 dmesg/sysfs、systemd/core 策略、STM32 实测）待 software_tester 板端任务 / 下位机复验。
5. 本报告绑定 commit `8ce5162`；被审代码再变即失效，须再次审查（可只审增量）。

code_reviewer (R-004)
2026-10-02 10:30
