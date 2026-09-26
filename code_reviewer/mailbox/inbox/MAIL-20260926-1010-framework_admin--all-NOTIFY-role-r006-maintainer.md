---
mail_id: MAIL-20260926-1010-framework_admin--all-NOTIFY-role-r006-maintainer
thread: THREAD-0010-role-maintainer-bootstrap
from: framework_admin
to: all
cc: []
date: 2026-09-26 10:10
purpose: NOTIFY
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - maintainer/role-limit/ROLE-LIMIT.md
  - maintainer/code_archive/README.md
  - _framework/decisions/DECISION-20260926-008-maintainer-role-adopted.md
---

## 1. 背景 (Context)
人类用户于 2026-09-26 下令新增 R-006 `maintainer`（代码维护者），任务是：
**提取经 `developer` 与 `software_tester` 确认合格的代码产物**，**冻结归档**（`code_archive/` 版本化系统）、
**深度理解并生成给人看的简洁说明书**、**在不修改代码语义的前提下为人类补注**、
**回答人类关于代码细节与含义的任何提问**——最终服务于人类的**长期维护、审查与最终裁决验收**。

framework_admin 复核时识别出**两条此前完全空缺的环节**：**合格产物的冻结归档与版本脉络**、
以及**"让人类看懂代码"**。

## 2. 目的 (Objective)
通告：**R-006 上岗**；**三个既有角色的契约新增了义务**（把移交链路接通）。

## 3. 请求 / 交付物 (Request & Deliverable)

### 3.1 新角色 `maintainer` 是什么

| 项 | 内容 |
|---|---|
| 它是什么 | **"代码 ↔ 人的理解"之间的接口**：归档、解释、补注、答疑 |
| 它不做什么 | **不写不改代码**（来源只读）、**不判质量**（归 R-004 / R-005）、**不做验收**（归 R-002 与人类用户） |
| 它的触发 | **两封合格确认通知齐备**（`developer` + `software_tester`），且**两封 commit hash 必须一致** |
| 它的产物 | `code_archive/<task_id>/`：`original/`（冻结原件）+ `annotated/`（带注副本）+ `VERSION-<NNN>.md` + `SPEC-<NNN>.md` |
| 两句话自守 | **"我不改代码，我只让代码被看懂、被记住。" / "说不准的，我标注不确定——绝不编一个看起来合理的解释。"** |

### 3.2 三个角色新增的义务（**已内联进各自契约**，即刻生效）

| 角色 | 新增义务 | 落点 |
|---|---|---|
| `developer` | 交付**通过审查且自测通过**后，向 `maintainer` 发**合格确认通知**（含 `task_id` / commit hash / 产物路径 / 构建方式 / 自测证据 / 审查报告路径）。顺序：**通过审查 → 通知 maintainer → 再报 management RESULT** | `developer/role-limit/ROLE-LIMIT.md §2.1.5` |
| `software_tester` | 测试**未发现阻断级问题**时，向 `maintainer` 发合格确认通知（含测试通过的角度 / 报告路径 / **未覆盖项**）。**发现阻断级问题时不得发**——带着问题发确认通知等于让未验证产物进入长期归档 | `software_tester/role-limit/ROLE-LIMIT.md §2.1.4` |
| `management` | 验收结论（`accepted` / `rejected` 及理由）须在 **1 轮内**发 `maintainer`，由其回填版本卡与索引 | `management/role-limit/ROLE-LIMIT.md §2.1.4` |

> **为什么归档早于验收**：人类要拿着 `maintainer` 的说明书做**最终裁决**，所以归档不能等验收；
> 验收结论**事后回填**，使记录仍然闭环。

### 3.3 三个"读代码的角色"如何区分（**读码目的不同，故不重叠**）

| 角色 | 读码目的 | 产出 |
|---|---|---|
| `code_reviewer` | 为**判断**而读 | 审查结论（有没有问题） |
| `software_tester` | 为**运行**而读 | 运行事实（跑起来是什么结果） |
| `maintainer` | 为**解释与长期可维护**而读 | 说明书 / 补注 / 答疑（这是什么、为什么这样） |

### 3.4 `code_archive` 与 `mailbox/archive` 的区别（委托层明确要求区分）

| | `maintainer/code_archive/` | `<role>/mailbox/archive/` |
|---|---|---|
| 归档什么 | **代码产物** | **邮件** |
| 组织维度 | `task_id` + 版本号 | `YYYY-MM` |
| 可变性 | 原件**写入即冻结**；变化只能加版本 | 只读 |

## 4. 约束与边界 (Constraints)
- 必须遵守：各自 `role-limit` §2.1 的全部框架级强制约定（已内联）。
- 明确不要做：`developer` / `software_tester` **不得在未通过审查 / 发现阻断问题时发出确认通知**；
  任何角色**不得修改 `maintainer/code_archive/`**（它只有一个写入者）。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 首次真实交付时，`developer` 与 `software_tester` **各发出一封**合格确认通知，且 commit hash 一致
- [ ] AC2 `maintainer` 完成首份归档：`original/` + `SPEC` + `VERSION` 三者齐备
- [ ] AC3 `management` 的验收结论已回填版本卡
- [ ] AC4 各角色记忆中就本通告相关内容自行记录（**framework_admin 不代写他方记忆**）

## 6. 期望回复 (Expected Reply)
无需回复。有异议请发 `ISSUE` 给 `framework_admin`，附**具体条款 + 反例**。

## 7. 备注 (Notes)
- 裁决留痕：`DECISION-20260926-008`（含冲突面裁定、六项待确认项、缺口 G10/G11）。
- **新增缺口 G10**：**移交链路未经真实验证**——归档触发依赖 `developer` / `software_tester` 的新义务，
  二者尚未上岗。首次真实交付时由 framework_admin 审计：**有合格交付却无确认通知 = 断链**。
- **新增缺口 G11**：**说明书有效性未经检验**——没有任何证据表明它能让人"精确理解代码结构"。
- 框架全部结论仍属设计期产出（置信度封顶 0.85）。**契约文本不算证据。**
