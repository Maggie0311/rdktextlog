# VERSION-002 — T-20260930-005-logging-v2 · 版本记录卡（版本 002 · 增量归档 · KN3 纠正）

| 字段 | 值 |
|---|---|
| task_id | `T-20260930-005-logging-v2` |
| 归档版本号 | **002（增量版 · 纠正 v001 归档件 systemd 伪 `[Unit]` 缺陷）** |
| 来源 commit | **`3148fedec9f39dbf95184cdfd72ffb8bd605e892`**（短 `3148fed`） |
| 验收状态 | **accepted**（`ACCEPT-20261001-logging-v2.md` + DECISION `MAIL-20261001-1610`）；本版纠正许可 = DECISION `MAIL-20261001-1630` |
| 归档形态 | **增量归档**（不重抄全套）：仅 `v002/systemd/rmlog-demo.service` 1 个纠正文件带注副本 + 本卡 + DIFF-002；v001 全套归档件保持冻结（KN2/KN9），仅 VERSION-001 追加一行注记（DECISION §4 明示允许项） |
| 归档日期 | 2026-10-01 |
| 归档执行 | maintainer (R-006) |

---

## 1. 三份要件（齐备性核验；口径 = DECISION MAIL-20261001-1610 / MAIL-20261001-1630）

| # | 要件 | mail_id / 文件 | commit 口径 | 核验结论 |
|---|---|---|---|---|
| 1 | **management 验收许可（accepted）** | `management/script/ACCEPT-20261001-logging-v2.md` + DECISION `MAIL-20261001-1610-management--maintainer-DECISION-accept-v2-and-archive-fix` | 对齐基准 `3148fed` | ✅ accepted（板端实测通过）；本版纠正另由 DECISION `MAIL-20261001-1630` 裁定 |
| 2 | **静态审查（code_reviewer）** | `code_reviewer/script/REVIEW-T-20260930-005-3148fed.md`（第一份真实落盘审查，落盘 commit `b6c8aac`） | 被审 `3148fed` | ✅ PASS（零阻断/严重） |
| 3 | **测试（software_tester）** | 容器 `software_tester/script/TESTREPORT-T-20261001-007-001.md` + 板端真机 `software_tester/script/TESTREPORT-T-20261001-008-001.md` | 容器 `3148fed`；板端 `d2e1081`（与 `3148fed` 同源，见 VERSION-001 §1） | ✅ 容器 13/13 + 板端 X5 13/13 + 五域注入 5/5 |

一致性：三件证据均以 `3148fed` 对齐（同 VERSION-001 §1 核验）；developer 备料无落盘 HANDOFF（外部实例直接提交 `3148fed`，VERSION-001 §6 已如实记录，不伪造）。本版只纠正归档件自身缺陷、不改来源 `3148fed` 任何字节，故被审/被测内容不变，**无需重审/重测**。

## 2. 本版纠正内容与基准

- **纠正对象**：v001 归档件 `code/systemd/rmlog-demo.service` 第 17 行含 1 个伪 `[Unit]` 非注释节头（KN3 越界；来源 `3148fed` 无此问题——该文件来源仅 16 行，唯一 `[Unit]` 在首行）。
- **纠正基准**：来源 blob `git -c core.autocrlf=false cat-file blob 3148fed:developer/script/systemd/rmlog-demo.service`（LF，360 字节，16 行）。
- **纠正结果**：`v002/systemd/rmlog-demo.service` = 来源 blob 逐字节内容（LF，16 行）+ 仅 1 行注释（文件头导读，带 `（maintainer 补注（v002）：…）` 标记）；**删除伪 `[Unit]` 非注释行，恢复与来源一致**。

## 3. 补注前指纹（来源基准；仅本次 1 个纠正文件）

**来源 commit：`3148fed`（git blob 原始字节，LF）。**

| 文件 | SHA-256（补注前 = 3148fed blob） |
|---|---|
| `systemd/rmlog-demo.service` | `be564ad42dc4a02c8d686cfc3d584f1c40e337c518ade68d446b1b99723582af` |

## 4. 补注（唯一写操作，就地补注）

- **方式**：来源 blob 逐字节副本上**仅新增 1 行注释**（文件头导读），标记 `（maintainer 补注（v002）：…）`；未触碰来源 16 行任何内容（含节头、字符串、空行、缩进）；未新增任何非注释行（尤其无 `[Unit]` 节头）。
- **规模**：**新增 1 行、删除 0 行**。

## 5. 补注后指纹（v002 归档件实际内容）

| 文件 | SHA-256（补注后 = `v002/systemd/rmlog-demo.service`，LF） |
|---|---|
| `systemd/rmlog-demo.service` | `f0fb946cfc826f0f3ba3ef0f7f6a459b1e2c4aff39404640526937ba436ceb9b` |

## 6. diff 结论（KN3 合规；无伪节头）

- **方法**：`git diff --no-index -U0` 以补注前基准（来源 blob LF 副本）对照 `v002/systemd/rmlog-demo.service`，逐行核对。
- **结论**：**新增 1 行、删除 0 行**；唯一新增行以 `# （maintainer 补注（v002）：` 开头；**非注释新增行 = 0；无 `[Unit]` 伪节头**。**KN3 合规（只增注释行）；KN2 冻结生效**——本卡落笔起 `v002/systemd/rmlog-demo.service` 一字不改。

## 7. 与版本 001 的关系

- **本版 = 对 v001 归档件 `code/systemd/rmlog-demo.service` 的 KN3 越界（1 个伪 `[Unit]` 节头）的纠正**：删除该非注释行，恢复与来源 `3148fed` 一致。
- v001 归档件（32 文件带注 `code/` + SPEC-001/WALKTHROUGH-001/QUESTIONS-001/DIFF-001/VERSION-001）**继续冻结、零改动**（KN2/KN9）；唯一例外：按 DECISION `MAIL-20261001-1630` §4 在 VERSION-001 追加一行注记（"该版本 systemd 伪 `[Unit]` 缺陷已由 v002 纠正"），属明示允许的注记追加，**不改 `code/` 内容**。
- **阅读口径**：systemd 服务文件以 `v002/systemd/rmlog-demo.service`（纠正版）为准；其余 31 文件仍以 v001 `code/` 为准。
- 归档件不是审查/测试对象（冻结约定延续）：审查与测试以来源 commit `3148fed` 为准。

## 8. 状态

| 项 | 值 |
|---|---|
| 状态 | **accepted · 已归档（增量 · KN3 纠正） · 冻结** |
| 本版增量产物 | VERSION-002（本卡）/ DIFF-002 / `v002/systemd/rmlog-demo.service`（1 文件带注副本）/ INDEX #4 行 / VERSION-001 注记一行 |
| RESULT | `MAIL-20261001-1645-maintainer--management-RESULT-v002-fix-unit`（→ management，副本自留 outbox） |
| v001 触碰记录 | 仅 VERSION-001 追加一行注记（DECISION §4 明示允许）；`code/` 32 文件零改动（KN2/KN9） |
