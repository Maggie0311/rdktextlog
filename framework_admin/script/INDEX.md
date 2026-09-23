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
| 9 | 角色骨架规格（20 项建角色清单） | `framework_admin/script/role-skeleton-spec.md` | 规范产物 | v1.0 | 2026-02-14 | **已验证 1 次**（2026-09-23 手工创建 R-002 时逐项核对，未发现缺项） | 架构方 |
| 10 | R-002 角色契约与七目录实例（31 文件） | `management/role-limit/ROLE-LIMIT.md`、`management/principles/PRINCIPLES.md`、`management/memory/` 等 | 契约 + 实例 | v1.0 | 2026-09-23 | 自审通过（待真实项目验证） | management、全体 |
| 11 | 角色层级与权限声明（同级关系 / 分工轴 / 建角色权） | `_framework/01-ROLE-REGISTRY.md` 增补节 | 规范 | v1.0+ | 2026-09-23 | 自审通过 | 全体角色 |
| 12 | 裁定记录：R-002 采纳 + 正交性检查 + 缺口 G4 | `_framework/decisions/DECISION-20260923-002-management-role-adopted.md` | 裁决 | v1.0 | 2026-09-23 | — | 全体角色、人类用户 |

> **诚实声明（2026-09-23 修订）**：第 1–8 项仍为"未验证"（设计期产出，依据 LTM-006 封顶 0.85）；
> 第 9 项已获 1 次真实创建验证；第 10–12 项为本轮新增，尚待真实项目闭环验证。
> **G2 未闭合**：本轮 31 个文件全部手工创建，验证了规格可用，但同时验证了"手工执行耗时且完全依赖清单核对"。

## 待补产物（规划中）

| 产物 | 用途 | 触发条件 |
|---|---|---|
| `build_role_skeleton.ps1` | 一键生成新角色七目录 + 全部占位文件 | **单轮创建 ≥2 个角色时**（2026-09-23 由"创建第 2 个角色时"改；理由见 WORKLOG #21：单个角色无法暴露脚本的可变部分） |
| `audit_violations.ps1` | 扫描 V1–V6 违规 | 有 ≥2 个角色时 |
| `memory_index_gen.ps1` | 由记忆条目自动重建 MEMORY-INDEX | 记忆条目 ≥15 时 |
