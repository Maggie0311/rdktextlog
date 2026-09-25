# mailbox/ — developer 的邮箱

| 子目录 | 用途 |
|---|---|
| `inbox/` | 别人发给我的信。**开工必读**，处理完移入 `archive/YYYY-MM/` |
| `outbox/` | 我发出的信（冻结副本，不可改） |
| `archive/YYYY-MM/` | 已关闭的信，只读 |
| `drafts/` | 未定稿草稿 |

**命名与正文格式（本节即全部要求，无需查阅他处）**

- 文件名：`MAIL-<YYYYMMDD>-<HHMM>-<from>--<to>-<CAT>-<slug>.md`
- front matter 12 个必填字段：`mail_id` / `thread` / `from` / `to` / `cc` / `date` / `purpose` / `priority` / `deadline` / `requires_reply` / `attachments` / `references`
- 正文 7 段：1 背景 / 2 目的 / 3 请求与交付物 / 4 约束与边界 / 5 验收标准 / 6 期望回复 / 7 备注
- `purpose` 取值与**你的义务**：`TASK`→先回 ACK（≤1 轮）再 RESULT 或 ISSUE；`QUERY`→≤2 轮内作答；`RESULT`→≤1 轮内 ACK 或提 ISSUE；`ACK`→无需再回；`HANDOFF`→≤1 轮内 ACK 接手；`ISSUE`→≤1 轮内回应；`NOTIFY`→无需回（有异议则回）；`DECISION`→**必须执行**（可申诉一次）
- `priority`：P0 立即中断当前工作 / P1 本轮内 / P2 正常 / P3 有空再做
- 不可变性：**发出的信即冻结**；更正须发新信并在 `references` 中列原信 `mail_id`
- 铁律：inbox 不得滞留未处理的信（带 `keep_in_inbox: true` 的常驻件除外）

铁律：**inbox 不得滞留未处理的信**（常驻信例外见协议 §2.1）。
本角色收到 `TASK` 后**必须先回 ACK**（≤1 轮），再开工；交付后发 `RESULT`；受阻发 `ISSUE`。
