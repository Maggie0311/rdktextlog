# mailbox/ — management 的邮箱

| 子目录 | 用途 |
|---|---|
| `inbox/` | 别人发给我的信。**开工必读**，处理完移入 `archive/YYYY-MM/` |
| `outbox/` | 我发出的信（冻结副本，不可改） |
| `archive/YYYY-MM/` | 已关闭的信，只读 |
| `drafts/` | 未定稿草稿 |

命名与正文格式见 `_framework/02-MAILBOX-PROTOCOL.md`。
本角色的特殊地位：**派活一律走本目录的 outbox**，未落邮箱的"口头进度"与"口头派活"在本框架中**不存在**（PRINCIPLES P5 / MN6）。
铁律：**inbox 不得滞留未处理的信**。
