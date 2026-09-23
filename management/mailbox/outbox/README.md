# outbox/ — 已发出邮件（冻结副本）

本目录中的邮件在发出即冻结，**不得修改**。需要更正时：发一封新信，purpose 用 `NOTIFY` 或 `DECISION`，
并在 `references` 中列出原信 mail_id。

本角色发出的信有三类，都必须留副本：
1. `TASK` — 任务指派（必须含唯一 `task_id` 与可验收 AC）；
2. `QUERY` — 进度问询与催办；
3. `RESULT / ISSUE` — 向人类用户的汇报与请示、向 framework_admin 的建角色请求。

当前已发：无（本角色尚未开工）。
