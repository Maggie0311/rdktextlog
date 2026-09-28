# STM-001 — 归档前必须区分"EOL 表示差"与"内容差"，否则误判 QUERY

| 字段 | 值 |
|---|---|
| task_id | T-20260926-001-logging-platform-p0（归档 001，2026-09-28） |
| confidence | high |
| salience | low |
| 类别 | 归档流程 / 校验方法 |

**经验**：`git archive <commit>` 签出与工作区逐字节比对时，仓库 blob=LF 而工作区=CRLF（`core.autocrlf=true` 且无 .gitattributes）会让纯文本文件在"字节级"不一致，但内容完全相等；归档前核验应分两层：①字节比对（blob 原始字节为基准，用 `-c core.autocrlf=false` 签出）②对不一致者逐个定性（EOL 表示差 / 后续簿记提交 / 真实未提交改动）。本任务 4/32 差异全部为前两类，未误发 QUERY。

**可证伪性**：若某次归档前核验发现差异文件属于第三类（工作区真实未提交源码改动）而本方法仍归档，即证伪。

**复用条件**：任何"git archive 签出 vs 工作区"形态的归档/审计核验，跨项目成立。
