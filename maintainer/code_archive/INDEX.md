# code_archive/INDEX — 代码产物归档总索引

> 规则：每归档一个版本，在此追加一行。**只追加**。
> 状态取值：`已归档` / `验收通过` / `验收驳回` / `已废弃（见墓碑）`

| # | task_id | 版本 | 被测 commit | 归档日期 | **验收许可 mail_id** | **developer 通知 mail_id** | **tester 通知 mail_id** | 配套文档 | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | T-20260926-001-logging-platform-p0（含 R4 修复轮 T-20260927-003-logging-c-linux-build，同归档单元） | 001 | `164d4c7`（R4 终版；链 R0=f3331b0→R1=45eeb04→R2=a675c8d→R3=2d83644→R4=164d4c7） | 2026-09-28 | `ACCEPT-20260927-logging-p0.md` v2（accepted，验收报告形态非邮件，2026-09-28） | `MAIL-20260928-2000-developer--maintainer-HANDOFF-T-20260927-003-linuxbuild`（取代覆盖 2d83644 的 MAIL-20260927-1505） | `MAIL-20260928-1958-software_tester--maintainer-HANDOFF-T-20260927-003` | SPEC/WALKTHROUGH/QUESTIONS/DIFF/GLOSSARY ✅ 全齐 | 补注 +130/-0 行（KN3 校验通过）；双指纹见 VERSION-001；状态=accepted·冻结 |
| 2 | T-20260926-001-logging-platform-p0（task=T-20260928-004-usage-rewrite，增量归档） | 002 | `08f6ce8`（= 164d4c7 + 纯文档重构，恰 2 文档文件，代码零变更） | 2026-09-29 | `MAIL-20260929-2000-management--maintainer-DECISION-v002-archive`（accepted + 增量归档口径 B 强化变体） | `MAIL-20260929-1955-developer--maintainer-HANDOFF-T-20260928-004` | `code_reviewer/script/REVIEW-T-20260928-004-08f6ce8.md`（PASS 零发现项；tester 无新增报告，板端结论引 TESTREPORT-003-001 仍归 001 链——DECISION §2.1 口径） | 增量件：VERSION-002/DIFF-002/v002-code 2 文件带注副本；SPEC/WALKTHROUGH/QUESTIONS 不重发（SPEC-001 头部 v2 注记）；GLOSSARY +1 | 补注 +13/-0 行（USAGE+9/IMPL+4，KN3 校验通过）；双指纹见 VERSION-002；状态=accepted·冻结（001 件零触碰，SPEC-001 头注为 DECISION §2.3 允许项） |

**说明**：
- **三份要件缺一不得归档**：`management` 的 `accepted` 结论（归档许可）+ `developer` 与 `software_tester` 的合格确认通知；
- 三者的 **commit hash 必须一致**；
- "配套文档"列填 `SPEC/WALKTHROUGH/QUESTIONS/DIFF/GLOSSARY` 的齐备情况（✅/缺项）；
- 每一行都应有对应的 `<task_id>/VERSION-<NNN>.md`；
- 被 `management` 驳回或被否决的版本**不进本表**，进 `_tombstones/`。
