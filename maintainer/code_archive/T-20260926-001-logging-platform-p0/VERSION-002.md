# VERSION-002 — T-20260926-001-logging-platform-p0 · 版本记录卡（版本 002 · 增量归档）

| 字段 | 值 |
|---|---|
| task_id | `T-20260928-004-usage-rewrite`（同归档单元 `T-20260926-001-logging-platform-p0` 的版本 002；USAGE.md 重构为用户优先手册） |
| 归档版本号 | **002（增量版）** |
| 来源 commit | **`08f6ce840d3bdbbeb2df2c20fcba0b4e54fe25a3`（短 `08f6ce8`）** — 即被复审（REVIEW-T-20260928-004-08f6ce8 PASS 零发现项）与被验收（DECISION MAIL-20260929-2000 accepted）的同一份 |
| 版本链 | R0=`f3331b0` → R1=`45eeb04` → R2=`a675c8d` → R3=`2d83644` → **R4=`164d4c7`（归档版本 001）** → **`08f6ce8`（本版 = 164d4c7 + 纯文档重构）**，无分叉 |
| 验收状态 | **accepted**（`MAIL-20260929-2000-management--maintainer-DECISION-v002-archive`，2026-09-29，验收 + 增量归档口径裁定：B 强化变体） |
| 归档形态 | **增量归档**（不重抄全套）：仅 `v002/` 增量件（2 个变更文件的带注副本 + 本卡 + DIFF-002）；版本 001 全套归档件**保持冻结不动**（KN2/KN9） |
| 归档日期 | 2026-09-29 |
| 归档执行 | maintainer (R-006) |

---

## 1. 三份要件（齐备性核验，逐份确认；口径 = DECISION §2.1）

| # | 要件 | mail_id / 文件 | commit 口径 | 核验结论 |
|---|---|---|---|---|
| 1 | **management 验收许可（accepted）+ 归档口径裁定** | `MAIL-20260929-2000-management--maintainer-DECISION-v002-archive` | **08f6ce8** | ✅ §1 验收 accepted（ACCEPT v3 已追记）；§2 裁定增量归档（B 强化变体），逐条执行于本轮 |
| 2 | **developer 合格确认通知（备料）** | `MAIL-20260929-1955-developer--maintainer-HANDOFF-T-20260928-004` | **08f6ce8** | ✅ 五要素齐（task_id/hash/产物路径/构建方式/自测证据）；"备料不是许可"声明在案（§7） |
| 3 | **复审结论（PASS）** | `code_reviewer/script/REVIEW-T-20260928-004-08f6ce8.md` | **08f6ce8** | ✅ 文档专项复审 **PASS、零发现项**（§7）；验证证据区 `code_reviewer/script/_verify_T-20260926-001/r7/` |

**要件形态说明（如实记录）**：本版第三要件按 DECISION §2.1 明示口径由 **reviewer 复审报告**承担（不再是 tester 通知）。software_tester 本任务**无新增报告**——纯文档、零代码行为变更，其 TESTREPORT-T-20260927-003-001 板端实测结论被本版手册引用并注明出处，仍归版本 001 链（developer HANDOFF §7 声明，reviewer 报告 §4/§6 同口径采信）。

**hash 一致性**：DECISION §3 要求的核对口径——**三件均指向 `08f6ce8`**，逐件核过，完全一致。

## 2. 归档基准核验（git 实证，2026-09-29 maintainer 自核）

- **来源字节**：`git -c core.autocrlf=false archive 08f6ce8`（blob 原始字节）签出 USAGE.md 与 IMPL-…p0.md，与工作区同名文件 **SHA-256 逐字节一致**（`5d1c0f0e…` / `6123faef…`，见 §3）；工作区对两文件 vs 08f6ce8 `git diff` 为空（与 REVIEW §1 基准核对 B4 同口径）。
- **变更面**：`git diff --name-status df6cd42..08f6ce8` 全仓库**恰 2 文件**（USAGE.md M、IMPL-…p0.md M，+338/−129）——与 developer HANDOFF §2、reviewer 报告 §1（B2）三方口径一致，本轮自核一致。
- **代码冻结面**：`git diff --name-only df6cd42..08f6ce8 -- *.py *.c *.h rmlog/*` = **0 文件**（REVIEW §1 B3 同口径）；行格式/错误码/默认路径/轮转参数等行为面零变更。
- **工作区他方改动**：本轮开工时未提交改动仅 management 的 PROJECT-BOARD.md 与 code_reviewer r7 未跟踪验证区（他方区域，本轮零触碰）。
- **行为面复验说明（诚实记录）**：本版**零代码变更**（代码文件与版本 001 来源 164d4c7 逐字节同源），maintainer 未重跑 selftest——依据：① 代码面无差异，版本 001 归档时的独立复验（VERSION-001 §9，13/13 PASS）继续有效；② 本轮 developer（13/13，21.1s）与 reviewer（两次复跑 13/13，r7 在库留档）证据在案。此为**不新增声明**，非跳过义务。

## 3. 补注前指纹（来源基准；**仅本次 2 个变更文件**，其余产物与版本 001 归档件相同）

**来源 commit：`08f6ce8`（git archive blob 原始字节）。**

| 文件 | SHA-256（补注前 = 08f6ce8 blob） |
|---|---|
| `USAGE.md` | `5d1c0f0e02769eef75675e50d8cbb2c4676d7912f3409147f46a6a1bc3f8d425` |
| `IMPL-T-20260926-001-logging-platform-p0.md` | `6123faef2e227daff197d6ca7b13eee8f9ca7c4f5c72e5d394fa4e6950d7aec1` |

## 4. 补注（唯一写操作，就地补注）

- **方式**：`v002/code/` 内逐字节副本上就地补注；Markdown 注释 `<!-- … -->` 单行；全部新增行携带 **`（maintainer 补注（v002）：…）`** 标记；未触碰 developer 原文任何一行（含原注释、标题、表格、代码块）。
- **USAGE.md（9 行）**：文件头"版本 002 导读"注释块 ×1 + 关键段落后说明行 ×8（卷首引言后 / §1 主线前 / §1.4 行格式图后 / §1.4 末尾 / §2 章前 / §3.3 判读要点后 / §4 末尾 / §5 FAQ 末尾 / §7 对应关系表后）。
- **IMPL（4 行）**：文件头"版本 002 导读"注释块 ×1 + §9 区说明行 ×3（§9 章首 / §9.2 表前 / §9.3 章首）。
- **规模**：共**新增 13 行、删除 0 行**（USAGE +9、IMPL +4）。
- **过程修正（诚实记录）**：首轮补注在每个注释块后追加了空行，权威校验发现 12 行空行属"非注释新增行"，与 ROLE-LIMIT §4 判定表"diff 只含以注释符号开头的新增行"不符——**已剔除并复验通过**（§6）；该修正本身即"只增注释行"规则的落地。

## 5. 补注后指纹（归档件实际内容）

| 文件 | SHA-256（补注后 = `v002/code/` 归档件） |
|---|---|
| `USAGE.md` | `500c45130bad4edff232362e3de7ef2b947872e5e0d5b0468985cb3f24d1cd0e` |
| `IMPL-T-20260926-001-logging-platform-p0.md` | `14c599773f8027710bf4fbb6ba4fd82c5a67802f122d483ce5340f5928fd97e7` |

## 6. diff 结论（KN3 合规）

- **方法**：`git diff --no-index -U0` 以补注前基准（git archive 签出副本）对照 `v002/code/` 归档件，逐行核对。
- **结论**：USAGE.md **新增 9 行、删除 0 行**；IMPL **新增 4 行、删除 0 行**；**全部新增行均以 `<!-- （maintainer 补注（v002）` 开头，非注释新增行 = 0**。**KN3 合规（只增注释行）；KN2 冻结生效**——本版本卡落笔之时起 `v002/code/` 两文件一字不改，任何变动只能作为新版本。
- 两文件均为纯 Markdown 文档（无可编译面），不适用 v001 的编译复验项。

## 7. 与版本 001 的关系

- **版本 002 = 版本 001（164d4c7）+ 纯文档重构**（恰 2 文档文件，+338/−129；代码零变更）。
- 版本 001 归档件（`code/` 21 文件带注版、SPEC-001、WALKTHROUGH-001、QUESTIONS-001、DIFF-001、VERSION-001）**继续有效、继续冻结**；本轮对其**零改动**（KN2/KN9；唯一例外见 §8 注记：SPEC-001 头部按 DECISION §2.3 加一行 v2 注记，属 DECISION 明示允许的追加，已标注"v2 增补"）。
- `v002/code/` 仅含本次 2 个变更文件的带注副本（增量件，DECISION §2 口径）；**阅读顺序建议**：文档面看 `v002/code/`，代码面与行号走读仍看 `code/` 与 SPEC-001——本版代码零变更，v001 带注版行号对全部代码文件继续有效；USAGE/IMPL 两文档以 `v002/code/` 为准。
- 归档件不是审查/测试对象（冻结约定延续）：复审与验收以来源 commit `08f6ce8` 为准。

## 8. 状态

| 项 | 值 |
|---|---|
| 状态 | **accepted · 已归档（增量） · 冻结** |
| 本版增量产物 | VERSION-002（本卡）/ DIFF-002 / `v002/code/`（2 文件带注副本）/ INDEX #2 行 / GLOSSARY 增补（+1 条）/ SPEC-001 头部 v2 注记一行（DECISION 允许项） |
| RESULT | `MAIL-20260929-20xx-maintainer--management-RESULT-archive-v002`（→ management，副本自留 outbox） |
| 版本 001 触碰记录 | **零触碰**（SPEC-001 头部一行 v2 注记为 DECISION §2.3 明示允许的追加，非改写，已在 worklog 与本卡 §7 记录） |
