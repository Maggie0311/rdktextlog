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
| 13 | 根规范 v1.1：共享仓库与产物区（§7）+ 常驻信例外（§2.1） | `_framework/05-CONVENTIONS.md`、`_framework/02-MAILBOX-PROTOCOL.md` | 规范 | **v1.1** | 2026-09-23 | 自审通过（待首次真实提交验证 §7.2） | 全体角色 |
| 14 | R-003 角色契约与七目录实例（34 文件） | `developer/role-limit/ROLE-LIMIT.md`、`developer/principles/PRINCIPLES.md`、`developer/memory/` 等 | 契约 + 实例 | v1.0 | 2026-09-23 | 自审通过（待真实编码任务验证） | developer、全体 |
| 15 | 三层结构与指挥链声明（含首条指挥链 R-002 → R-003） | `_framework/01-ROLE-REGISTRY.md` 增补节 | 规范 | v1.0+ | 2026-09-23 | 自审通过 | 全体角色 |
| 16 | 裁定记录：R-003 采纳 + 指挥链范围（WHAT/WHEN）+ G5 + DECISION-002 §6 澄清 | `_framework/decisions/DECISION-20260923-003-developer-role-adopted.md` | 裁决 | v1.0 | 2026-09-23 | — | 全体角色、人类用户 |
| 17 | **根规范 v1.1：§4.1 审查门 + 违规码 V7** | `_framework/00-ARCHITECTURE.md` | 规范 | **v1.1** | 2026-09-23 | 自审通过（待首轮真实"开发→审查→验收"验证） | 全体角色 |
| 18 | R-004 角色契约与实例（46 文件，含 `standard/` 10 文件） | `code_reviewer/role-limit/ROLE-LIMIT.md`、`code_reviewer/principles/PRINCIPLES.md`、`code_reviewer/standard/` 等 | 契约 + 实例 + 标准 | v1.0 | 2026-09-23 | 自审通过（**标准质量待真实审查验证**） | code_reviewer、developer、全体 |
| 19 | 审查标准区与用户自定义标准接口 | `code_reviewer/standard/`（GEN / C / PY 清单、SEVERITY、REPORT-TEMPLATE、`user/`） | 标准 | v1.0 | 2026-09-23 | 自审通过（清单条目尚未被真实代码检验） | developer、人类用户 |
| 20 | 裁定记录：R-004 采纳 + 审查门 + 权力轴 + G6 | `_framework/decisions/DECISION-20260923-004-code-reviewer-role-adopted.md` | 裁决 | v1.0 | 2026-09-23 | — | 全体角色、人类用户 |
| 21 | **根规范 v1.2：废止 `src/`，交付产物回归各角色 `script/`** | `_framework/05-CONVENTIONS.md` | 规范 | **v1.2** | 2026-09-24 | 自审通过（全仓复扫无残留规定） | 全体角色 |
| 22 | 裁定记录：产物区修正 + 交付流转方式 + 残留风险 | `_framework/decisions/DECISION-20260924-005-artifact-area-fix.md` | 裁决 | v1.0 | 2026-09-24 | — | 全体角色、人类用户 |
| 23 | 根规范 v1.2：§2.1 角色自足原则（无公共工作空间） | `_framework/00-ARCHITECTURE.md` | 规范 | v1.2 | 2026-09-25 | 自审通过（全仓自足性核查：0 个多主区） | 全体角色 |
| 24 | **根规范 v1.3：§7 新增违规码 V8 伪造证据** | `_framework/00-ARCHITECTURE.md` | 规范 | **v1.3** | 2026-09-25 | 自审通过（尚无适用对象） | 全体角色 |
| 25 | R-005 角色契约与实例（37 文件） | `software_tester/role-limit/ROLE-LIMIT.md`、`principles/`、`script/ENVIRONMENTS.md` 等 | 契约 + 实例 | v1.0 | 2026-09-25 | 自审通过（**能力待实测**，见 G7） | software_tester、全体 |
| 26 | 裁定记录：R-005 采纳 + 两通道分离 + 适配判定表 + G7 | `_framework/decisions/DECISION-20260925-006-software-tester-role-adopted.md` | 裁决 | v1.0 | 2026-09-25 | — | 全体角色、人类用户 |
| 27 | **根规范 v1.4：§2.1.1 义务闭合性 + §2.1.2 `_framework` 定位** | `_framework/00-ARCHITECTURE.md` | 规范 | **v1.4** | 2026-09-26 | **已验证**（全仓复扫：非我目录内可执行引用清零） | 全体角色 |
| 28 | 裁定记录：`_framework` 私有化 + 义务内联化（方案丁）+ G8 闭合 | `_framework/decisions/DECISION-20260926-007-obligation-closure.md` | 裁决 | v1.0 | 2026-09-26 | 已验证 | 全体角色、人类用户 |
| 29 | R-006 角色契约与实例（39 文件，含 `code_archive` 空系统） | `maintainer/role-limit/ROLE-LIMIT.md`、`principles/`、`code_archive/README.md` 等 | 契约 + 实例 | v1.0 | 2026-09-26 | 自审通过（**归档与说明书有效性待真实验证**，见 G10/G11） | maintainer、人类用户、全体 |
| 30 | 裁定记录：R-006 采纳 + 归档触发 + 六项待确认 + 三处新增义务 | `_framework/decisions/DECISION-20260926-008-maintainer-role-adopted.md` | 裁决 | v1.0 | 2026-09-26 | — | 全体角色、人类用户 |

> **诚实声明（2026-09-23 二次修订）**：第 1–8 项仍为"未验证"（设计期产出，依据 LTM-006 封顶 0.85）；
> 第 9 项已获 2 次真实创建验证（R-002、R-003，均逐项核对无缺项）；第 10–16 项为本轮及上轮新增，尚待真实项目闭环验证。
> **G2 未闭合**：累计 63 个角色文件全部手工创建，规格可用性已被验证两次，但"手工执行耗时且完全依赖清单核对"这一点同样被验证两次。
>
> **契约≠证据（第二次适用）**：用户对 `developer` 的三项质量硬要求（结构清晰 / 风格规范 / 详细中文注释）
> 与对 `code_reviewer` 的四项质量硬要求（确实做到 / 不误报 / 不瞒报 / 不过度要求且不懒惰批准），
> **目前全部只存在于契约与标准文本中**，未经任何一行真实代码或一次真实审查的检验。
> 在首个完整链路（开发 → 审查 → 申诉/修复 → 复审 → 验收）跑通之前，它们一律按"未验证"对待（LTM-006）。
>
> **G2 未闭合（第三次记录）**：累计 107 个角色文件全部手工创建，规格已被验证三次，但"手工执行耗时且完全依赖清单核对"同样被验证三次。
> 触发条件"单轮创建 ≥2 个角色"至今未出现，故仍未写脚本——这是遵守先前决定的结果，不是遗忘。

## 待补产物（规划中）

| 产物 | 用途 | 触发条件 |
|---|---|---|
| `build_role_skeleton.ps1` | 一键生成新角色七目录 + 全部占位文件 | **单轮创建 ≥2 个角色时**（2026-09-23 由"创建第 2 个角色时"改；理由见 WORKLOG #21：单个角色无法暴露脚本的可变部分） |
| `audit_violations.ps1` | 扫描 V1–V6 违规 | 有 ≥2 个角色时 |
| `memory_index_gen.ps1` | 由记忆条目自动重建 MEMORY-INDEX | 记忆条目 ≥15 时 |
