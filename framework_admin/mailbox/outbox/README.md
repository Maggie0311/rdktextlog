# outbox/ — 已发出邮件（冻结副本）

本目录中的邮件在发出即冻结，**不得修改**。需要更正时：发一封新信，purpose 用 `NOTIFY` 或 `DECISION`，
并在 `references` 中列出原信 mail_id。

当前已发：

| mail_id | 目的 | 收件人 | 说明 |
|---|---|---|---|
| MAIL-20260214-1200-framework_admin--all-NOTIFY-rfc-framework-v1 | NOTIFY | all | 框架 v1.0 生效通告（同时充当格式样例） |
