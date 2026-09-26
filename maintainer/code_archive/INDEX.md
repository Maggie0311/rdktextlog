# code_archive/INDEX — 代码产物归档总索引

> 规则：每归档一个版本，在此追加一行。**只追加**。
> 状态取值：`已归档` / `验收通过` / `验收驳回` / `已废弃（见墓碑）`

| # | task_id | 版本 | 被测 commit | 归档日期 | **验收许可 mail_id** | **developer 通知 mail_id** | **tester 通知 mail_id** | 配套文档 | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| — | （暂无） | — | — | — | — | — | — | — | — |

**说明**：
- **三份要件缺一不得归档**：`management` 的 `accepted` 结论（归档许可）+ `developer` 与 `software_tester` 的合格确认通知；
- 三者的 **commit hash 必须一致**；
- "配套文档"列填 `SPEC/WALKTHROUGH/QUESTIONS/DIFF/GLOSSARY` 的齐备情况（✅/缺项）；
- 每一行都应有对应的 `<task_id>/VERSION-<NNN>.md`；
- 被 `management` 驳回或被否决的版本**不进本表**，进 `_tombstones/`。
