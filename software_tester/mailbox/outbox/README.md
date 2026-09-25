# outbox/ — 已发出邮件（冻结副本）

本目录中的邮件在发出即冻结，**不得修改**。需要更正时：发一封新信，purpose 用 `NOTIFY`，并在 `references` 中列原信 `mail_id`。

本角色发出的信有四类，都必须留副本：
1. `RESULT` — 运行结果（主送 management，抄 developer）：报告路径 + commit hash + 复现命令 + 原始输出路径；
2. `ISSUE` — 环境不可得 / 必须改程序才能测 / 疑似缺陷现象（附复现步骤）；
3. `QUERY` — 测试请求不可判定、需要澄清；
4. `NOTIFY` — `ENVIRONMENTS.md` 能力变化（新增手段 / 手段失效）。

当前已发：无（本角色尚未开工）。
