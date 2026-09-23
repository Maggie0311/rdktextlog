# _framework/ — 框架根规范目录

> 本目录**只读于所有业务角色**，仅 framework_admin 可写。

| 文件 | 内容 |
|---|---|
| `00-ARCHITECTURE.md` | 总架构：目录结构、工作循环、违规判定 |
| `01-ROLE-REGISTRY.md` | 角色注册表与新增角色检查清单 |
| `02-MAILBOX-PROTOCOL.md` | 邮箱通信协议与消息语义契约 |
| `03-MEMORY-MODEL.md` | 仿动物记忆模型与置信/晋升/遗忘规则 |
| `04-ROLE-CONTRACT-TEMPLATE.md` | 新角色契约模板（填空即用） |
| `05-CONVENTIONS.md` | 命名、时间、不可变性、引用等通用约定 |
| `decisions/` | 仲裁结论、审计日志 |
| `templates/` | 邮件/记忆/计划/日志的可复制模板 |

阅读顺序建议：00 -> 01 -> 02 -> 03 -> 04 -> 05。
