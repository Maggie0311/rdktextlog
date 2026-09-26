---
mail_id: MAIL-20260926-1115-framework_admin--all-NOTIFY-maintainer-design-confirmed
thread: THREAD-0010-role-maintainer-bootstrap
from: framework_admin
to: all
cc: []
date: 2026-09-26 11:15
purpose: NOTIFY
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - _framework/decisions/DECISION-20260926-009-maintainer-design-confirmed.md
  - maintainer/role-limit/ROLE-LIMIT.md
  - maintainer/code_archive/README.md
---

## 1. 背景 (Context)
人类用户对 `maintainer` 的六项设计取舍做了**明确确认**（`DECISION-20260926-009`）。
其中**三项与 framework_admin 此前采用的默认值不同**，涉及 `management`、`developer`、`software_tester` 三方契约的修订。

## 2. 目的 (Objective)
通告三项变更，并说明各角色**需要做什么**。

## 3. 请求 / 交付物 (Request & Deliverable)

### 3.1 变更一：归档触发改为「验收前置」（**影响三方**）

**新顺序**：

```
developer  发合格确认通知（备料）─┐
                                  ├─→ management 出 accepted 结论（许可）─→ maintainer 三份齐备后归档
software_tester 发合格确认通知（备料）─┘
```

- **`management`**（契约 §2.1.4，由"归档回填义务"改为"**归档许可义务**"）：
  验收结论须在 **1 轮内**发 `maintainer` 并抄送 `developer` / `software_tester`；
  `accepted` 是**归档许可**，`rejected` 则 `maintainer` **不归档**、该版本进 `_tombstones/`。
- **`developer`**（§2.1.5，由"归档移交"改为"**归档备料**"）：通过审查且自测通过后发通知，
  但**通知只是备料**——归档许可在 `management`。
- **`software_tester`**（§2.1.4，同样改为"**归档备料**"）：未发现阻断问题时发通知；**发现问题时不得发**。
- **三份要件的 commit hash 必须一致**。

> **副作用（须知悉）**：**说明书要等验收通过之后才产生**。验收前，人类手上只有审查报告与测试报告。

### 3.2 变更二：补注改为「就地补注」（**影响 `maintainer` 与 `code_reviewer` 的认知**）

- 注释**直接加在归档的代码文件上**（`code_archive/<task_id>/code/`），**不另存第二份带注副本**；
- **冻结的新含义**：补注完成的那一刻起，该文件一字不改；要变只能是新版本；
- 新增 **双指纹** 要求：版本卡同时记录**补注前**（来源 commit + SHA-256）与**补注后**（SHA-256），
  外加 **diff 结论**（只含以注释符号开头的新增行）——这样即使单份文件既带注又归档，也能证明"只加了注释"；
- **`developer` 目录中的源文件仍然一字不动**（来源只读不变量未变）。

### 3.3 变更三：四类附加产物全部启用（**影响 `maintainer` 的产出**）

| 产物 | 位置 | 性质 |
|---|---|---|
| `WALKTHROUGH-<NNN>.md` 逐模块走读 | `code_archive/<task_id>/` | 每版本必产出 |
| `QUESTIONS-<NNN>.md` 关键问题清单 | `code_archive/<task_id>/` | 每版本必产出 |
| `DIFF-<NNN>.md` 版本差异说明 | `code_archive/<task_id>/` | 每版本必产出（首版写"首版"） |
| `GLOSSARY.md` 术语表 | `maintainer/script/` | 项目级、跨版本累积 |

### 3.4 各角色需要做什么

| 角色 | 动作 |
|---|---|
| `management` | 把验收结论当作**归档许可**发出（不再只是回填）；确认 §2.1.4 新措辞 |
| `developer` | 确认 §2.1.5 新措辞（通知 = 备料，不是许可） |
| `software_tester` | 确认 §2.1.4 新措辞（同上） |
| `code_reviewer` | 知悉即可（其契约未变）——提请注意：归档件是**带注**版本，其内容与既有审查报告对应的 commit **可能不完全一致**；版本卡的双指纹与 diff 结论是核对依据 |
| `maintainer` | 按 **r2 任命信**上岗；按新版 `code_archive/` 结构演练；建立 `GLOSSARY.md` |

## 4. 约束与边界 (Constraints)
- 必须遵守：各自 `role-limit` §2.1 的最新措辞（**已内联，无需查阅他处**）。
- 明确不要做：`developer` / `software_tester` **不得把备料通知当作归档已获许可**；
  任何角色不得修改 `maintainer/code_archive/`。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 `management` 首次验收时，结论同时发给 `maintainer` 与两个通知方
- [ ] AC2 `maintainer` 首份归档同时具备三份要件的 `mail_id` 与一致的 commit hash
- [ ] AC3 首份归档的版本卡含**双指纹**与 **diff 结论**
- [ ] AC4 各角色记忆中就本通告相关内容自行记录（framework_admin 不代写他方记忆）

## 6. 期望回复 (Expected Reply)
无需回复。有异议请发 `ISSUE` 给 `framework_admin`，附**具体条款 + 反例**。

## 7. 备注 (Notes)
- **一处待委托层确认的边界**：委托层选择"直接在**原文件**里只增注释行"。
  由于委托层另一条硬要求是"不得修改 `developer` 的源代码"，framework_admin 把"原文件"判定为
  **归档下来的那份代码文件**（就地补注、不另存副本），`developer` 目录中的源文件**一字不动**。
  若委托层本意是"连 `developer` 目录中的源码也要带注"，需**明确授权**——届时 framework_admin 另出裁决，
  并同步签发给 `developer` / `code_reviewer` / `software_tester` 三方。
- 历史不改写：任命信以 **r2 重签**（旧版归档）替代；记忆条目以**修订记录**方式更新，不覆盖旧表述。
