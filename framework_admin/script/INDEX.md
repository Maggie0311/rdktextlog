# script/INDEX — framework_admin 产物登记表

> 规则：任何新增/重大变更的产物必须在此登记。重大变更另存 `-v2`，不覆盖。

| # | 产物 | 路径 | 类型 | 版本 | 创建日期 | 最近验证 | 消费者 |
|---|---|---|---|---|---|---|---|
| 1 | 总架构规范 | `_framework/00-ARCHITECTURE.md` | 规范 | v1.0 | 2026-02-14 | 未验证（待真实角色） | 全体角色 |
| 2 | 角色注册表 | `_framework/01-ROLE-REGISTRY.md` | 规范 | v1.0 | 2026-02-14 | 未验证 | 全体角色 |
| 3 | 邮箱通信协议 | `_framework/02-MAILBOX-PROTOCOL.md` | 规范 | v1.0 | 2026-02-14 | 未验证 | 全体角色 |
| 4 | 记忆模型与置信规则 | `_framework/03-MEMORY-MODEL.md` | 规范 | v1.0 | 2026-02-14 | 未验证 | 全体角色 |
| 5 | 角色契约模板 | `_framework/04-ROLE-CONTRACT-TEMPLATE.md` | 模板 | v1.0 | 2026-02-14 | 未验证 | 架构方 |
| 6 | 通用约定 | `_framework/05-CONVENTIONS.md` | 规范 | v1.0 | 2026-02-14 | 未验证 | 全体角色 |
| 7 | 邮件/记忆/计划/日志模板 ×5 | `_framework/templates/*.md` | 模板 | v1.0 | 2026-02-14 | 未验证 | 全体角色 |
| 8 | 本角色边界契约 | `framework_admin/role-limit/ROLE-LIMIT.md` | 契约 | v1.0 | 2026-02-14 | 自审通过 | framework_admin |
| 9 | 角色骨架规格（20 项建角色清单） | `framework_admin/script/role-skeleton-spec.md` | 规范产物 | v1.0 | 2026-02-14 | 未验证 | 架构方 |

> **诚实声明**：以上"最近验证"列全部为"未验证"，依据 LTM-006——框架初始发布只算 1 个证据源。
> 待第一个真实角色创建并完成一次任务后，回填验证状态。

## 待补产物（规划中）

| 产物 | 用途 | 触发条件 |
|---|---|---|
| `build_role_skeleton.ps1` | 一键生成新角色七目录 + 全部占位文件 | 创建第 2 个角色时 |
| `audit_violations.ps1` | 扫描 V1–V6 违规 | 有 ≥2 个角色时 |
| `memory_index_gen.ps1` | 由记忆条目自动重建 MEMORY-INDEX | 记忆条目 ≥15 时 |
