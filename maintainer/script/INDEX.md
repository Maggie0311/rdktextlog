# script/INDEX — maintainer 产物登记表

> 规则：登记**交付单元**，**不逐文件登记**。
> **代码归档不在此表登记**——它的索引是 `../code_archive/INDEX.md`。

| # | 交付单元 | 路径 | 类型 | 关联 task_id | 版本 | 创建日期 | 消费者 |
|---|---|---|---|---|---|---|---|
| 1 | T-20260930-005-logging-v2 归档交付 | `../code_archive/T-20260930-005-logging-v2/` | VERSION/SPEC/WALKTHROUGH/QUESTIONS/DIFF | T-20260930-005-logging-v2 | 001 | 2026-10-01 | management / 维护者 |

**待产出（上岗后）**：

| 产物 | 用途 | 触发条件 |
|---|---|---|
| `QA-LOG.md` | 答疑记录（含依据与被纠正情况） | 上岗首个交付物之一，见 `mailbox/inbox/WELCOME-maintainer.md` |
| `GLOSSARY.md` | 项目级术语表 | 首次归档时建立，此后随版本增补 |
| 首份归档（`../code_archive/<task_id>/`） | `code/`（带注代码）+ 版本卡（双指纹）+ `SPEC` + `WALKTHROUGH` + `QUESTIONS` + `DIFF` | **三份要件齐备**时（`management` `accepted` 许可 + 两封合格确认通知） |
