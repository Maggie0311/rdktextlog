# 通用约定 (Conventions)

> 版本: v1.0 · 维护者: framework_admin · 所有角色适用

## 1. 命名

| 对象 | 规范 | 示例 |
|---|---|---|
| 角色目录 | snake_case 小写 | `data_curator` |
| 邮件 | `MAIL-YYYYMMDD-HHMM-<from>--<to>-<CAT>-<slug>.md` | `MAIL-20260214-1030-framework_admin--data_curator-TASK-x.md` |
| 长期记忆 | `LTM-<NNN>-<slug>.md` | `LTM-003-boundary-first.md` |
| 短期记忆 | `STM-<NNN>-<slug>.md` | `STM-007-first-task.md` |
| 计划 | `PLAN-<YYYYMMDD>-<slug>.md` | `PLAN-20260214-role-skeleton.md` |
| 脚本/产物 | `<slug>.<ext>` + 版本 | `build_index.ps1`, `report-v2.md` |
| 线程 | `THREAD-<NNNN>-<slug>` | `THREAD-0007-corpus-build` |

## 2. 时间

- 一切时间戳用本地时间 `YYYY-MM-DD HH:MM`。
- 日期字段（front matter）用 `YYYY-MM-DD`。
- 归档目录用 `YYYY-MM`。

## 3. 语言

- 正文中文；字段名、文件名、代码标识符英文。
- 断言/结论必须**可证伪**，禁止"效果较好"这类模糊表述。

## 4. 不可变性

| 文件类型 | 可变性 |
|---|---|
| `worklog/` | **只追加**，禁止改写历史条目；更正用新条目 + `[更正: #N]` |
| `mailbox/outbox/` | 发出即冻结；更正发新信并 `references` 原信 |
| `memory/long-term/` | 证据表只追加；结论可改但必须记版本行 |
| `memory/short-term/` | 可编辑（工作记忆），但证据表同样只追加 |
| `role-limit/` `principles/` | 仅 framework_admin 可改；角色可发 ISSUE 建议 |
| 他人目录 | **只读**。需要改动 -> 发 TASK 给对方 |

## 5. 引用

- 提到任何文件必须写**相对仓库根的路径**，且该文件必须真实存在。
- 引用他人结论必须写明来源 ID（如 `LTM-003 of data_curator`）。

## 6. 空目录占位

任何标准目录若暂无内容，必须有 `README.md` 说明用途，避免"看起来坏了"。
