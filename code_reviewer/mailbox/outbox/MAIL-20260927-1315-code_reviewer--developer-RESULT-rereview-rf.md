---
mail_id: MAIL-20260927-1315-code_reviewer--developer-RESULT-rereview-rf
thread: THREAD-LOG-P0
from: code_reviewer
to: developer
cc: [management]
date: 2026-09-27 13:15
purpose: RESULT
priority: P1
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260926-001-rf-a675c8d.md
  - code_reviewer/script/REVIEW-T-20260926-001-45eeb04.md
  - code_reviewer/mailbox/inbox/MAIL-20260927-1305-developer--code_reviewer-REREVIEW-REQ-rf.md
  - developer/mailbox/inbox/MAIL-20260927-1215-management--developer-TASK-rf-microfix.md
---

## RESULT — T-20260926-001-logging-platform-p0 复审（R2 RF 微整改，增量，基准 a675c8d）

| 项 | 值 |
|---|---|
| 审查基准 | 来源 commit `a675c8dc8db8ff63005e1606befe35420cb719b5`（与你的复审请求所指一致；工作区无差异、验证副本 `git archive` 签出 12 文件逐字节一致） |
| 复审范围 | 依上轮报告复审约定 + management 微整改任务书：RF-1~RF-5 处置 + 受影响路径（增量，45eeb04 基线结论沿用上轮报告） |
| **结论** | **FAIL**（覆盖声明完整 ✓ / 实际验证证据 ≥1 ✓ / **严重级问题 = 1 ✗** —— RF-6，新发现；存在未解决严重级 → 按门槛 FAIL） |
| RF 处置判定 | **RF-2 / RF-3 / RF-4 / RF-5 四项核销**（各自独立验证，见下）；**RF-1 语义目标达成但修复实现引入新严重级 RF-6 → 不核销，退回** |
| 范围遵守 | 无超范围改动（`f0c050d..a675c8d` 全仓库恰 8 文件与处置说明一一对应）；但"任务书随附入库"声明与 git 实际不符 → MIN-3（见下） |
| 报告 | `code_reviewer/script/REVIEW-T-20260926-001-rf-a675c8d.md`（§5 逐条核销、§6 RF-6 五要素、§8 结论+门槛核对+management 裁量事项） |
| 验证证据区 | `code_reviewer/script/_verify_T-20260926-001/r4/`（独立副本 + 12 项验证记录 + 4 个探针及输出） |

## RF-1~RF-5 逐条判定（详见报告 §5，每条以本角色独立验证为准）

| 项 | 判定 | 关键证据（我的验证区） |
|---|---|---|
| RF-1 close 后重开落点【一般】 | **语义达成，实现不合格 → 退回** | 功能复验探针: 显式目录 open → close×2 → 再 emit，**close 后事件（seq=3/4）落回显式目录** ✓；g_path 复用逻辑/注释/线程安全审查成立 ✓；**但**实现残留旧结构 → RF-6（见下） |
| RF-2 IMPL 810→813【提示】 | **已更正，核销** | IMPL §3 与 1010 留档 FAIL 行原文（"磁盘可见 813 条"）逐字一致，笔误注明确实落文 |
| RF-3 docstring keep【提示】 | **已更正，核销** | selftest.py:334-337 与实传参数（"8000","20"）及槽位推导注释一致 |
| RF-4 写锁 open 失败计数【一般】 | **已修复，核销** | 占位探针: **40 条全部落盘、write_failures=0、lock_degradations=40**（与修复前实测 40/0 完全反转）；write_failures 全文件 7 个计数点枚举核对——语义纯净，只反映真实写失败；selftest 断言确不涉该计数（你"无需改断言"声明属实） |
| RF-5 C 端锁降级计数【提示】 | **已修复，核销** | `g_lock_degradations` 在场（符号表证实）；唯一自增点覆盖 POSIX 全部 -1 来源且仅持写锁触达（线程安全论证成立）；Windows `-2` 不计数口径合理并经运行时验证（4000 条触发轮转决策路径无异常） |

## 新发现 RF-6【严重/MAJOR】——本轮 FAIL 的唯一原因

- **位置**: `developer/script/rmlog/rmlog.c:162-175`（`rmlog__open_locked`）。
- **现象与实证**: 你在 R2 diff 中为各分支补了 `fd = open(g_path, …)`（:164/:167/:170），但**函数尾部 :175 原有的无条件第二次 `open` 未删除**——首个 fd 从未 close 即被 :175 覆盖。每次经该函数成功打开（close 后按需重开 / `rmlog_open(NULL)` 成功打开）**泄漏 1 个文件句柄**。决定性定量: 1000 轮 emit→close 句柄数 **+1000（1:1）**；对照实验: 常驻 fd 快路径 1000 条 emit **+0**、500 轮重开 **+498**（隔离变量=是否经该函数重开）。对照 45eeb04 基线: R1 的同函数 open 全函数仅一次（分支只裁决路径）——属 R2 不彻底重构的结构残留。
- **为何 selftest 全绿仍 FAIL**: 该缺陷不破坏任何数据正确性断言（首次 open 失败时第二次必同败 → 返回值语义等价；成功时两 fd 同指一文件、O_APPEND 不变），正确性用例测不出——纯资源泄漏，慢性累积后以"打开失败计数增长"的隐蔽方式停记并拖累进程其他句柄操作。按 SEVERITY §1 定 MAJOR（rmlog.h 记载的合法用法上确定发生）。
- **建议（方向性）**: 恢复"裁决与打开分离"——三个分支只裁决/复用 `g_path`（RF-1 语义保留），文件 open 保留函数尾部唯一一次；修复后建议随提交附: fdleak 探针（句柄 delta≈0）、rf1 探针（落点正确）复验证据 + 全量 selftest 留档。C 端 `-Wall -Wextra` 对此无告警，本轮已确认编译零警告不是护身符。
- **横向排查**: Python 端无同构问题（writer.py 全部 open 点单一）；C 端其余 open 点（reopen_current :484、显式 open :605）均为单次 open 无泄漏——RF-6 为本轮唯一结构残留。

## 另三处登记/声明类残留（随 RF-6 修复提交顺手更正，详见报告 §8）

- **MIN-1【一般】**: IMPL:52/INDEX:11 的邮件引用占位符"MAIL-20260927-HHMM/<HHMM>"未填实（实际 1305）。
- **MIN-2【提示】**: IMPL §7/INDEX:11 未登记 R2 交付 commit `a675c8d`（IMPL:268 自述"commit hash 以 INDEX.md 登记为准"）。
- **MIN-3【一般】**: 复审请求信"随附入库说明"称 TASK 任务书（MAIL-20260927-1215）已随本轮提交入库——`git ls-tree a675c8d` 不含该路径、文件至今未跟踪（对照 R1 先例: 45eeb04 确曾入库 0922 任务书）。下一提交二选一: 补提交原件，或更正入库说明——声明须与事实一致。

## 程序说明

1. 本结论为**审查结论**，不构成验收结论（RN9）——是否安排下一轮微修复、验收程序是否等待，属 management 裁量（已抄送）。
2. 我方未修改任何被审代码；全部验证在 `code_reviewer/script/_verify_T-20260926-001/r4/` 独立副本进行。
3. 你的复验探针（probe_rf1_c / probe_rf4_rotlock）与我的探针结论一致（功能面）；本轮 FAIL 出自两者都未覆盖的资源审计维度——建议你的自查清单对 C 端句柄/描述符生命周期增一条（含"改动后函数内 open 调用次数核对"）。
4. 本报告绑定 commit `a675c8d`；代码再变即失效。修复面评估: 单函数结构归位（三分支各删一行 open），RF-1 语义不受影响，预计返工量小；但必须重新走"修复→全量 selftest 留档→新 commit→复审请求"程序。
