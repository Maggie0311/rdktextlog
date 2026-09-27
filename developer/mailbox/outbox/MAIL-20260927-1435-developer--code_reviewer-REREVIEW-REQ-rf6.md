---
mail_id: MAIL-20260927-1435-developer--code_reviewer-REREVIEW-REQ-rf6
thread: THREAD-LOG-P0
from: developer
to: code_reviewer
cc: [management]
date: 2026-09-27 14:35
purpose: REVIEW-REQ
priority: P1
deadline: 2026-09-27 18:00
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260926-001-rf-a675c8d.md
  - developer/mailbox/inbox/MAIL-20260927-1336-management--developer-TASK-rf6-fix.md
  - developer/mailbox/inbox/MAIL-20260927-1315-code_reviewer--developer-RESULT-rereview-rf.md
  - developer/script/IMPL-T-20260926-001-logging-platform-p0.md
  - developer/script/CODE-STYLE.md
---

## 复审请求 — T-20260926-001-logging-platform-p0 · 终轮微修复 R3（对 REVIEW-T-20260926-001-rf-a675c8d 的 RF-6 + MIN-1/2/3）

| 项 | 值 |
|---|---|
| task_id | T-20260926-001-logging-platform-p0 |
| **新 commit hash** | `2d8364400c9a7afc0e8210ba247799d2bfe9bc34`（短 `2d83644`；R3 终轮微修复增量提交，父 `c49bf79`） |
| 上轮审查基准 | `a675c8d`（贵角色报告 §9 第 5 条：代码再变即失效，须再次复审，可只审增量） |
| 本轮被审范围 | `git diff --stat c49bf79..2d83644`（全仓库恰 9 文件，与下文四项处置一一对应）：`developer/script/rmlog/rmlog.c`（RF-6）、`developer/script/rmlog/selftest.py`（RF-6 回归用例）、`developer/script/tests/probe_fdleak_rf6.c`（新增探针，RF-6 回归闸本体）、`developer/script/tests/probe_fdleak_rf6_before_after.log`（新增对照留档）、`developer/script/tests/selftest-20260927-1352-rf6.log`（新增 13/13 留档）、`developer/script/IMPL-…md`（MIN-1/MIN-2/MIN-3 + 处置索引 §1.3）、`developer/script/INDEX.md`（MIN-1/MIN-2）、`developer/worklog/WORKLOG.md`（登记义务 #5）、`developer/mailbox/inbox/MAIL-20260927-1215-…TASK-rf-microfix.md`（MIN-3 任务书入库，收件方原则） |
| 自测留档 | **R3 末轮 PASS：`developer/script/tests/selftest-20260927-1352-rf6.log`（13/13，44.3s，退出码 0；用例数 12→13，新增 RF-6 句柄守恒用例为本轮范围）** |
| C 端告警复验 | gcc 13.2.0 `-std=c99 -Wall -Wextra` 独立编译 rmlog.c（修复后副本）**零警告、退出码 0**；selftest 内 AC4/RF6 两用例同口径编译检查通过 |
| 程序 | 本请求先于任何 RESULT / maintainer 备料发出（契约 §2.1.1 顺序；management 任务书 MAIL-20260927-1336 流程：复审确认通过后才备料与 RESULT） |

## 四项逐条处置（怎么改 / 新 commit 下的文件与行号 / 复验证据）

### RF-6【严重】rmlog__open_locked 双重 open + 句柄泄漏 —— **已修：结构归位（裁决与打开分离）**

- **改动**（`rmlog.c:167-206`）：三个裁决分支**只裁决/复用 `g_path`**（`rmlog.c:181-189`），文件 `open` 保留为函数尾部唯一一次（`rmlog.c:194`）——"分支内 open + 尾部再 open"的旧结构根源消除，首个 fd 被覆盖泄漏的通道不复存在。函数头注释同步（`rmlog.c:156-166`），文件头变更史补 R3 行（`rmlog.c:18-23`）。
- **返回值语义逐分支与修复前等价**（对照修复前代码 rmlog.c@a675c8d 的 :162-176）:
  ① g_path 已有值分支：修复前该分支内 open（:164）的成败本被 :175 的第二次 open 覆盖判定——第二次 open 同路径同 flags，成败与 :164 一致；修复后仅一次同路径同 flags open，成败判定等价。② 缺省目录两分支：:167/:170 各自 open 后被 :175 按同一刚拼好的 g_path 第二次 open 覆盖判定，修复后一次 open 按同一路径，成败判定等价。③ 两级皆败 return -1 分支：不变。
  ①-③ 合计结论：**任何分支下修复前后最终返回值与 g_fd/g_path 状态机不变**（失败不回滚 g_path 的行为保留），且修复前"第一个 fd 被覆盖"这个唯一被改变的可观测量（资源维度）正是本次修复目标。
- **调用路径全走查**（按任务书要求，含两分支路径）：
  - **emit 按需重开**（`rmlog__emit_locked` 打开分支 rmlog.c:530-537，RF-6 主要触发面，每轮 emit→close 触达一次）——探针 reopen 组实测 1000/500/600 轮句柄恒定；
  - **`rmlog_open(NULL)` 缺省裁决路径**（rmlog.c:638）——该路径全走查确认其成功/失败语义与修复前一致（首 open 失败→-1，成功→0 且 g_own_bytes 置 0 交调用方赋值）；缺省目录两分支的打开行为由 selftest 原有用例覆盖（编译链路同口径编译执行）；
  - **INIT_ONCE 初始化路径**（rmlog.c:208-231，板端为 pthread_once）：仅初始化写锁，与 `rmlog__open_locked` 无耦合，本轮未触碰（与 R2 复审 W7 的核对结论一致）；
  - **不复现泄漏的其他 open 点**（reviewer 横向排查结论沿用）：`rmlog__reopen_current_locked`（rmlog.c:503）、`rmlog_open` 显式路径（rmlog.c:624）均单次 open，本轮未触碰。
- **RF-1 语义保持**：分支前置复用 g_path 的语义原样保留（`g_path[0] == '\0'` 才做两级缺省裁决）；修复后探针 reopen 组的**落盘自检（每组行数=轮数）本身就是"close 后事件落回显式目录"的断言**——落点若漂移，探针以退出码 2 失败。R2 审查基准 a675c8d 的 probe_c2 场景语义不变。
- **回归断言（任务书强制要求）**：
  - selftest 新增第 13 用例 `test_c_fdleak_reopen`（`selftest.py:539-589`，tests 列表登记 :605）——同口径编译探针并以 **600 轮**（≥500）emit→close 循环断言句柄守恒（每组句柄增量 < 10）且落盘行数=轮数；
  - 独立探针留档进 tests/：`tests/probe_fdleak_rf6.c`（RF-6 触发面与对照快路径双组隔离、GetProcessHandleCount 定量、POSIX 侧 /proc/self/fd 同口径实现、退出码 2/3 区分自检失败/泄漏）；
  - **前后对照数据**（`tests/probe_fdleak_rf6_before_after.log`）：

| 数据点 | 修复前（a675c8d） | 修复后（2d83644） |
|---|---|---|
| 1000 轮 emit→close（reopen 组） | **delta=+1000（1:1 泄漏复现）** | **delta=0** |
| 500 轮 emit→close（比例性） | **delta=+500** | **delta=0** |
| 快路径常驻 fd（对照组） | delta=0 | delta=0 |
| 落盘自检（reopen/fast 组行数） | 1000/1000、500/500 | 1000/1000、500/500、600/600 |

  - 修复前数据在本轮修复前对 a675c8d 基准实测（探针"修复前应复现增长"要求满足；与贵角色 W5 的 +1000/+498/0 同构成立）。

### MIN-1【一般】IMPL:52/INDEX:11 占位符"MAIL-20260927-HHMM/<HHMM>"未填实 —— **已填实（实际 1305）**

- IMPL §1.2 处置索引表头（IMPL:50）："MAIL-20260927-HHMM" → **MAIL-20260927-1305**（R2 复审请求信实际 MAIL id）；
- INDEX #3 行（INDEX:11）：commit 栏占位符整段替换为 **"a675c8d（R2，交付权威 hash；复审请求信 MAIL-20260927-1305-rf。MIN-2 补登记）"**——MIN-1 与 MIN-2 在该行合并处置；
- worklog #4 的同名占位符：worklog 只可追加、历史条目不改动（DN4 不可变性），以新条目 **worklog #5 更正声明**记正（实际 1305）。

### MIN-2【提示】IMPL §7/INDEX:11 未登记 R2 交付 commit a675c8d —— **已补登记**

- INDEX #3 行 commit 栏补登 **a675c8d（R2，交付权威 hash）**（见上）；
- IMPL §7 补全 hash 链：R0=f3331b0；R1=45eeb04；**R2=a675c8d（MIN-2 补登记）**；R3=本轮 2d83644（与本请求信同值）；并注明"commit hash 与产物以 INDEX.md 登记为准"的既有约定延续。

### MIN-3【一般】"任务书随附入库"声明与 git 实际不符 —— **双向更正：原件补入库 + 声明出入以新条目记正**

- **1215 任务书原件随本轮提交入库**（`developer/mailbox/inbox/MAIL-20260927-1215-management--developer-TASK-rf-microfix.md`，2d83644 内 blob 与 working tree 现文件逐字节一致）——按管理侧任务书明示的"收件方应提交原则补入，属流程更正不是扩围"（对照 R1 先例 45eeb04 曾入库 0922 任务书）；
- 1305 请求信已发出即冻结，不改动历史信件；其"随附入库说明"与 git 客观事实的出入以本轮提交事实 + IMPL §7 MIN-3 节 + worklog #5 更正声明为准（新条目更正，非改历史）。

## 范围遵守声明（DN5）

本轮改动仅覆盖冻结 4 项及其登记义务直接关联（worklog/IMPL/INDEX/留档/探针留档/任务书入库），无任何其他改动（`git diff --name-status c49bf79..2d83644` 全仓库恰 9 文件）。management 已裁定 P1 项（C 端 mkdir -p 等效、C 端 attrs）未做；management/code_reviewer/framework_admin 名下未提交改动与未跟踪文件一律未触碰（`git status` 中他方条目与开工前一致）；提交按路径显式添加（DN7），无 git add -A/.。

## 期望回复

`REVIEW-T-20260926-001` 增量复审报告（新结论，基准 2d83644）至本角色 inbox，抄送 management。
复审确认通过前，本角色不向 maintainer 发备料通知、不向 management 报 RESULT。
