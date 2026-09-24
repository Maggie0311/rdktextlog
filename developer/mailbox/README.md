# mailbox/ — developer 的邮箱

| 子目录 | 用途 |
|---|---|
| `inbox/` | 别人发给我的信。**开工必读**，处理完移入 `archive/YYYY-MM/` |
| `outbox/` | 我发出的信（冻结副本，不可改） |
| `archive/YYYY-MM/` | 已关闭的信，只读 |
| `drafts/` | 未定稿草稿 |

命名与正文格式见 `_framework/02-MAILBOX-PROTOCOL.md`（v1.1）。

铁律：**inbox 不得滞留未处理的信**（常驻信例外见协议 §2.1）。
本角色收到 `TASK` 后**必须先回 ACK**（≤1 轮），再开工；交付后发 `RESULT`；受阻发 `ISSUE`。
