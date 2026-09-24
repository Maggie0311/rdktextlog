# outbox/ — 已发出邮件（冻结副本）

本目录中的邮件在发出即冻结，**不得修改**。需要更正时：发一封新信，purpose 用 `NOTIFY`，并在 `references` 中列原信 `mail_id`。

本角色发出的信有四类，都必须留副本：
1. `RESULT` — **审查结论**（主送 developer，抄送 management）：结论 + 发现项摘要 + 报告路径；
2. `ISSUE` — 标准缺陷、边界冲突、无法收敛的争议；
3. `QUERY` — 索取必要信息（AC / 设计意图 / 复现环境 / 构建方式）；
4. `NOTIFY` — 标准变更通告（`developer` 依赖 `standard/`，变更须通知）。

当前已发：无（本角色尚未开工）。
