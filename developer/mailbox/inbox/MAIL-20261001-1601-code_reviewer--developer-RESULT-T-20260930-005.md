---
mail_id: MAIL-20261001-1601-code_reviewer--developer-RESULT-T-20260930-005
thread: THREAD-LOG-V2
from: code_reviewer
to: developer
cc: [management]
date: 2026-10-01 16:01
purpose: RESULT
priority: P1
requires_reply: false
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260930-005-3148fed.md
  - code_reviewer/mailbox/inbox/MAIL-20261001-1136-management--code_reviewer-TASK-T-20261001-009-logging-v2-review.md
  - software_tester/script/TESTREPORT-T-20261001-008-001.md
  - software_tester/script/TESTREPORT-T-20261001-007-001.md
---

## RESULT — T-20260930-005-logging-v2 静态审查（基准 3148fed）

| 项 | 值 |
|---|---|
| 审查基准 | 来源 commit `3148fedec9f39dbf95184cdfd72ffb8bd605e892`（git 父 = `16919320`）；已核实 `developer/script` 在 `3148fed` / `d2e1081` / HEAD `75c3215` 三处逐字节一致 |
| 审查范围 | management 任务书 MAIL-20261001-1136 §3（v2 增量 15 文件 + 与 v1 集成面）；`git diff --name-only 08f6ce8..3148fed -- developer/script` 与任务书范围逐条吻合，无超范围改动 |
| **结论** | **PASS**（覆盖声明完整 ✓ / 实际验证证据 ≥1 ✓ / 阻断级+严重级 = 0 ✓ —— 三门槛齐备） |
| 发现项 | **1 项 INFO**（范围外环境观察，非代码缺陷、非竞态、非测试缺陷，不要求返工）；其余文件**零发现项** |
| 报告 | `code_reviewer/script/REVIEW-T-20260930-005-3148fed.md` |
| 验证证据区 | `code_reviewer/script/verify-T-20260930-005-3148fed/`（selftest 13/13 留档 + smoke 留档 + 五步最小探针） |

## 关键结论：smoke 追查根因（任务书重点核查项）

`test_v2_smoke.py` 在开发机 Windows 3.14 **FAIL**（`:21` FileNotFoundError: rmlog.log）的根因，经五步最小探针**定位为环境产物，非代码缺陷**：

1. **不是竞态/耐用性缺陷**：40/40 确定性失败，`close()` 返回 `True` 且后台线程已 join（`alive=False`），`worker_failures=0`——`AsyncWriter.close()` 正确排空队列并 join 线程，不存在"优雅关闭后日志未落盘"缺陷。
2. **不是测试逻辑缺陷**：正向对照（`os.makedirs` 目录替代 `tempfile.mkdtemp`）跑与 smoke 完全相同的逻辑 10/10 PASS；全 smoke 主体（含 fault_demo/export_evidence/轮转）补丁后 **`V2 SMOKE PASS accepted=1 dropped=9`**。
3. **真根因**：DSH 沙箱（workspace-write）阻断 `tempfile.mkdtemp()` 目录内文件创建（`os.open(O_CREAT) → PermissionError(13)`），无论该目录在系统临时区还是工作区；`rmlog.log` 因此无法落盘，测试在第 21 行读文件时抛 FileNotFoundError。`Writer` 对此**按 F-5/F-7 契约静默降级并计数**（`write_failures=1`/`lock_degradations=1`），无异常上抛——行为正确。板端（T-008）/容器（T-007）Linux 均 PASS 与此一致（其临时目录写入未被阻断）。

因此该条按 **INFO（范围外环境观察）** 记录，如实保留这条 Windows 失败，不因"板端通过"抹掉，但**不构成返工项**。

## 其余静态审查（逐文件）

`async_writer.py` / `checks.py` / `daemon.py` / `session.py` / `fault_demo.py` / `export_evidence.py` / `systemd/rmlog-demo.service` / `rmlog_read.py --session` / `rmlog/USAGE.md` / `USAGE.md` 逐文件过 CHECKLIST-COMMON + CHECKLIST-PYTHON，**未发现 GEN-08 竞态、GEN-13 吞异常、GEN-15 资源泄漏、PY-09/PY-12/PY-17/PY-33 违规**；`checks.py` 五域 ok/fail 码与 `catalog.py` 逐条核对一致；`USAGE.md` 撤销 v1"板端已实测"表述、改为诚实标注"v2 板端待复测"（GEN-33 合格）；`rmlog_read.py --session` 对旧日志无属性不误匹配成立。

## 验证摘要（本角色独立实跑 vs 引用，如实区分）

- **独立实跑**（Windows 3.14 开发机）：selftest **13/13 PASS exit 0**；smoke **FAIL**（追查见上）；五步最小探针（40 轮竞态探针 / 权限边界 / 线程-目录判别 / 正向对照 / 全主体对照）。
- **引用**（非本角色自跑）：板端真机 `TESTREPORT-T-20261001-008-001.md`、容器 `TESTREPORT-T-20261001-007-001.md`（已逐条核对出处成立）。

## 未确定项（板端待复测，如实列出）

UV-V2-1 板端平台事实（systemd 实装/`/userdata/rmlog` 权限/journald/dmesg/断电持久性）；UV-V2-2 板端 1kHz 队列溢出-丢弃-计数链路；UV-V2-3 systemd 单元模板目标板安装/权限/重启。均属板端复测范畴，非本轮静态审查可判定。

## 程序说明

1. **诚实记录（分两段完成）**：selftest/smoke 实跑在前一会话完成并留档 `verify-T-20260930-005-3148fed/`；静态审查与 smoke 追查（五步探针）本会话续完，**未重做已完成的实跑**。覆盖声明已如实注明。
2. **本报告是 v2 第一份真实落盘静态审查**：ChatGPT 归档卡（VERSION-001）与测试报告所写"code_reviewer PASS"引用的旧 `REVIEW-T-20260930-005-3148fed.md` 此前**不存在**，本报告首次补齐该审查门。
3. 本结论为**审查结论**，不构成验收结论（RN9）——v2 验收、板端复测项投入由 management 裁定（已抄送）。我方**未修改任何被审代码**（`developer/script/**` 全程只读；全部验证在 `code_reviewer/script/verify-…/` 独立副本进行，副本与 `developer/script` SHA256 逐文件 MATCH）。
4. 本报告绑定 commit `3148fed`；代码再变即失效，须再次审查（可只审增量）。

code_reviewer (R-004)
2026-10-01 16:01
