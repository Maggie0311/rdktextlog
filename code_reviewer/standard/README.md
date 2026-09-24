# standard/ — 代码审查标准区

> 所有者: `code_reviewer` (R-004) · 审查依据的**唯一权威来源** · 被 `developer` 用作自查依据

## 1. 目录结构

| 文件 / 目录 | 内容 | 写入者 |
|---|---|---|
| `REVIEW-STANDARD.md` | 审查流程、结论定义与时效（**总纲**） | code_reviewer |
| `CHECKLIST-COMMON.md` | 语言无关的通用检查清单（GEN-xx） | code_reviewer |
| `CHECKLIST-C.md` | C 语言专项清单（C-xx） | code_reviewer |
| `CHECKLIST-PYTHON.md` | Python 专项清单（PY-xx） | code_reviewer |
| `SEVERITY.md` | 严重级别定义、判定门槛与返工门槛 | code_reviewer |
| `REPORT-TEMPLATE.md` | 审查报告骨架（字段冻结） | code_reviewer |
| `VERSION-LOG.md` | 标准变更流水（只追加） | code_reviewer |
| **`user/`** | **★ 人类用户自定义标准接口** | **人类用户**（code_reviewer 只读） |

## 2. 优先级（冲突时以序号小者为准）

| 优先级 | 来源 | 说明 |
|---|---|---|
| **1（最高）** | `standard/user/USER-*.md` | **人类用户直接写入的检查要求**。code_reviewer **不得删改**，只能发 ISSUE 建议 |
| 2 | 项目契约：`developer/script/` 相关 AC、`developer/script/CODE-STYLE.md` | 由 management / developer 制定 |
| 3 | 本目录的 `CHECKLIST-*.md` 与 `SEVERITY.md` | code_reviewer 专业判断 |
| 4 | `_framework/` 根规范中的强制约定 | 例如提交隔离、注释语言 |

> 用户标准若与项目契约冲突，**以用户标准为准**，同时由 code_reviewer 发 ISSUE 给 framework_admin 记入 DECISION。

## 3. 使用方式（强制）

1. 每次审查**必须**完整过一遍 `CHECKLIST-COMMON.md` + 对应语言清单；
2. 每次审查**必须**扫描 `user/` 下全部 `USER-*.md` 并在报告中列出**本次实际应用的用户标准清单**（无则写"无"）；
3. 报告中的每条发现项**必须**引用本条标准的编号（如 `GEN-09`、`C-06`）或用户标准编号；
4. `SEVERITY.md` 的门槛**不得突破**：没有条款依据的问题不得高于 NIT，没有复现场景的问题不得高于 MINOR。

## 4. 变更规则

- 任何清单条目的增删改：记入 `VERSION-LOG.md`（只追加）+ 更新本目录文件版本 + 发 `NOTIFY` 给 `developer` 与 `management`。
- `standard/` 一经被 `developer` 用作自查依据即成为**契约**，变更须给兼容期（`05-CONVENTIONS §3`）。
- `user/` **不受本规则约束**：用户可随时增删自己的标准，立即生效，无需通知（这是接口的设计目的）。
