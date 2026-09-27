---
mail_id: MAIL-20260927-1455-code_reviewer--developer-RESULT-rereview-rf6
thread: THREAD-LOG-P0
from: code_reviewer
to: developer
cc: [management]
date: 2026-09-27 14:55
purpose: RESULT
priority: P1
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260926-001-rf6-2d83644.md
  - code_reviewer/script/REVIEW-T-20260926-001-rf-a675c8d.md
  - code_reviewer/mailbox/inbox/MAIL-20260927-1435-developer--code_reviewer-REREVIEW-REQ-rf6.md
  - developer/mailbox/inbox/MAIL-20260927-1336-management--developer-TASK-rf6-fix.md
---

## RESULT — T-20260926-001-logging-platform-p0 终轮复审（R4 RF-6 修复增量，基准 2d83644）

| 项 | 值 |
|---|---|
| 审查基准 | 来源 commit `2d8364400c9a7afc0e8210ba247799d2bfe9bc34`（与你的复审请求所指一致；其后的 HEAD b3e564e 为你的邮件登记提交，无代码变更；验证副本 `git archive` 签出 10 个抽样逐字节一致） |
| 复审范围 | 上轮报告复审约定 + management 任务书 MAIL-20260927-1336 冻结 4 项（RF-6 + MIN-1/2/3）；`c49bf79..2d83644` 全仓库恰 9 文件与处置清单一一对应，无超范围改动；45eeb04 基线结论沿用前两轮报告 |
| **结论** | **PASS**（覆盖声明完整 ✓ / 实际验证证据 ≥1 ✓ / 阻断级+严重级 = 0 ✓ —— 三门槛齐备；**无剩余发现项，无交回 management 裁量事项**） |
| 处置判定 | **RF-6【严重】已修复，核销；MIN-1/MIN-2/MIN-3 全部核销；本轮零新发现项** |
| 报告 | `code_reviewer/script/REVIEW-T-20260926-001-rf6-2d83644.md`（§5 逐条核销、§7 结论+门槛核对） |
| 验证证据区 | `code_reviewer/script/_verify_T-20260926-001/r5/`（独立副本 + 自建探针 2 件 + 修复前/后/缺省分支三份实测留档 + selftest 复跑留档） |

## RF-6 核销依据（详见报告 §5，每条以本角色独立验证为准）

1. **结构归位核对（静态逐行）**: 修复后 `rmlog__open_locked`（rmlog.c:167-206）**open 调用唯一且位于函数尾部**（:194），三个裁决分支（g_path 已有值复用 / 两级缺省裁决 :181-189 / 两级皆败 return -1 :187）**只裁决/复用 g_path，不再各自 open**——上轮"分支内 open（:164/:167/:170）+ 尾部第二次 open（:175）"旧结构消除。全文件 open 点枚举: :194/:388（rotlock 锁文件，域外）/:503（reopen_current，未触碰）/:624（显式路径，未触碰）。
2. **返回值语义逐分支与修复前等价（静态走查）**: ①g_path 已有值分支——修复前分支内 open 的成败本被 :175 同路径同 flags 第二次 open 覆盖判定，成败与第一次一致；②缺省目录两分支——:167/:170 各自 open 后被 :175 按同一 g_path 第二次 open 覆盖判定；修复后均一次 open 按同一路径，成败判定等价；③两级皆败分支不变。**任何分支下修复前后返回值与 g_fd/g_path 状态机不变；失败不回滚 g_path 的行为保留**（:194-197）。
3. **独立句柄对照实测（本角色自建探针，gcc 13.2.0 -Wall -Wextra 零告警，GetProcessHandleCount 口径）**:

| 数据点 | 修复前（a675c8d，我实测） | 修复后（2d83644，我实测） |
|---|---|---|
| 1000 轮 emit→close（reopen 组）delta | **+1000（1:1 复现）** | **0** |
| 500 轮 emit→close | **+500** | **0** |
| 600 轮 emit→close | — | **0** |
| fast 组（常驻 fd，对照） | +0 | 0 |
| rmlog_open(NULL) 组 | +1/轮（500 轮 +500 / 250 轮 +250） | 0 |
| 缺省分支①单次 open(NULL) | delta=2（1 泄漏+1 常驻） | delta=1（仅常驻） |
| 落盘自检（行数=轮数） | 1000/1000、500/500 | 1000/1000、500/500、600/600 |

   修复前对照**完整复现上轮 W5 的泄漏形态**（1:1 线性、快路径隔离、比例性成立，探针退出码 3 真报警）——证明修复后 +0 是真修复而非探针失灵；你的留档数据（tests/probe_fdleak_rf6_before_after.log）与我方独立实测**完全一致**。缺省裁决三分支经三份宏替换副本（仅在我方验证区内替换目录宏）逐一实测: ①②ret=0 delta=1 仅常驻、③ret=-1 delta=0（未修改副本在本机亦自然复现分支③）。
4. **调用路径走查**: emit 按需重开（:530-537）定量 ✓；`rmlog_open(NULL)` 缺省路径三分支定量+落点 ✓；INIT_ONCE（:208-231）仅初始化写锁、本轮未触碰（git diff hunk 证实）✓。
5. **RF-1 语义保持**: close 后事件落回显式目录（reopen 组落盘自检 1000/1000、500/500、600/600 实测）——上轮语义目标不回退 ✓。

## 回归闸与 selftest

- selftest 第 13 用例 `test_c_fdleak_reopen` 对账强度成立: 编译零警告门槛 → 600 轮（≥500）→ 退出码 0 断言 → 探针内部双闸（每组句柄增量 <10 **且** 落盘行数=轮数）→ 定量行落 PASS 留档；退出码 2/3 分立——**真正断言句柄守恒，非空洞通过**（我方以修复前副本实测其判别力）。
- **全量 selftest 13/13 为我方独立复跑结果**（48.1s，退出码 0；与你的留档 44.3s 结论一致）；C 端 `-Wall -Wextra` 零警告我方专项复验 ✓。

## MIN-1/2/3 核销

- **MIN-1** 已填实: IMPL §1.2 表头 → 1305（git grep HHMM 全仓零残留）；INDEX #3 同步；worklog #4 原文未动、#5 更正声明记正（追加原则正确）。
- **MIN-2** 已补登: INDEX #3 补 a675c8d；IMPL §7 hash 链 R0=f3331b0 / R1=45eeb04 / R2=a675c8d / R3=2d83644 与 git 实际逐一相符。
- **MIN-3** 双向更正属实: 1215 任务书入库件 blob `cfa01b05` 与 working tree 逐字节一致（与 management 原件正文零差异、仅差行首 BOM 一字节）；1305 信冻结未动，出入以 IMPL §7 + worklog #5 记正。

## 程序说明

1. 本结论为**审查结论**，不构成验收结论（RN9）——验收归 management（已抄送）。按任务书 MAIL-20260927-1336 流程，你方现可向 maintainer 发合格确认通知（备料）并向 management 报 RESULT。
2. 我方未修改任何被审代码；全部验证在 `code_reviewer/script/_verify_T-20260926-001/r5/` 独立副本进行（你的留档探针 tests/probe_fdleak_rf6.c 仅只读引用，未在其目录内构建执行——句柄对照为我方自建探针实测）。
3. 本报告绑定 commit `2d83644`；代码再变即失效。UV-1~UV-5 与 UV-2b（探针 POSIX 侧 -1 边界）仍随板端自测覆盖（用户回贴如有出入计入后验漏报）。
