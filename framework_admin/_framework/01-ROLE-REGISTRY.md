# 角色注册表 (Role Registry)

> 维护者: framework_admin · 任何角色变更必须先在此登记

## 命名规范

- 文件夹名：小写 + 下划线，例如 `framework_admin`、`data_curator`、`report_writer`。
- 角色代号：与文件夹名一致，邮件中用 `to: <role_code>`。
- 角色 ID：`R-001` 递增编号，永不复用。

## 注册表

| ID | 角色代号 | 中文名 | 职责一句话 | 状态 | 创建日期 | 契约文件 |
|---|---|---|---|---|---|---|
| R-001 | framework_admin | 架构管理员 | 设计角色分工、划定边界、维护根规范与仲裁 | active | 2026-02-14 | `framework_admin/role-limit/ROLE-LIMIT.md` |

> 后续角色：在下方追加行，并同步创建其七个标准目录与契约文件。

## 新增角色检查清单

- [ ] 在 `_framework/01-ROLE-REGISTRY.md` 登记一行（ID / 代号 / 中文名 / 一句话职责）
- [ ] 创建七个标准目录（含空目录的 README 占位）
- [ ] 写 `role-limit/ROLE-LIMIT.md`（含"只能做 / 绝不能做 / 交接口 / 升级路径"四段）
- [ ] 写 `principles/PRINCIPLES.md`（专业原则）
- [ ] 初始化 `memory/long-term/LTM-000-BOOTSTRAP.md` 与 `memory/short-term/STM-000-BOOTSTRAP.md`
- [ ] 初始化 `memory/index/MEMORY-INDEX.md`
- [ ] 初始化 `worklog/WORKLOG.md`
- [ ] 创建 `mailbox/inbox/WELCOME-<role>.md`（framework_admin 发出的任命信）
- [ ] 检查与其他角色的边界**无重叠、无真空**

## 边界正交性自检（framework_admin 必做）

对任意两个角色 A、B，检查是否存在动作 X 使得 X 同时落在 A 的"只能做"与 B 的"只能做"中。
若存在，必须指定**唯一主责方**，另一方降级为"仅可建议"。
