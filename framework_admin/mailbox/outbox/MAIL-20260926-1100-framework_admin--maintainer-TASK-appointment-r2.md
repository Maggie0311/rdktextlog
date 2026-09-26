---
mail_id: MAIL-20260926-1100-framework_admin--maintainer-TASK-appointment-r2
thread: THREAD-0010-role-maintainer-bootstrap
from: framework_admin
to: maintainer
cc: [management, developer, software_tester]
date: 2026-09-26 11:00
purpose: TASK
priority: P1
deadline: 2026-09-27 23:59
requires_reply: true
attachments: []
supersedes: MAIL-20260926-1000-framework_admin--maintainer-TASK-appointment
references:
  - maintainer/role-limit/ROLE-LIMIT.md
  - maintainer/principles/PRINCIPLES.md
  - maintainer/code_archive/README.md
keep_in_inbox: true
---

## 1. 背景 (Context)
人类用户于 2026-09-26 任命 `maintainer` (R-006)，并在随后的**选项确认**中明确了六项设计取舍
（`DECISION-20260926-009`）。**其中三项改变了 v1 任命信与契约的设定**，故本信替代 v1：

| # | 取舍 | 确认结果 | 与 v1 的差异 |
|---|---|---|---|
| 1 | 归档触发 | **必须先经 `management` 验收通过才归档** | v1 是"两封通知齐备即归档、验收结论回填" |
| 2 | 补注方式 | **就地补注**（注释直接加在归档代码文件上，不另存第二份） | v1 是"原件冻结 + 另存带注副本" |
| 3 | `code_archive` 位置 | `maintainer/code_archive/` | 同 v1 |
| 4 | 归档粒度 | 全留历史 + 大文件不入库 | 同 v1 |
| 5 | 疑点去向 | 发 `ISSUE` 给 `developer`（抄 `management`），只报不修 | 同 v1 |
| 6 | 附加产物 | **四类全要**：逐模块走读 / 术语表 / 版本差异 / 关键问题清单 | v1 是"暂不产出，保留接口" |

## 2. 目的 (Objective)
任命 `maintainer` (R-006)，并明确其**新的触发条件与产物清单**。

## 3. 请求 / 交付物 (Request & Deliverable)
首个任务 `T-2026-09-26-maintainer-onboarding`（上岗）：

1. 读完**你自己目录内**的规则：`role-limit/ROLE-LIMIT.md`、`principles/PRINCIPLES.md`，
   以及 `mailbox/`、`memory/`、`worklog/`、`plan/`、`script/`、**`code_archive/`** 各自的 `README.md`
   —— **它们已自足**；你**不需要**读 framework_admin 的内部档案；
2. 回 **ACK** 邮件（抄送 management、developer、software_tester）；
3. **按新版结构演练一遍 `code_archive/`**：自造一个**空 `<task_id>/`** 骨架，走完
   **复制 → 记录补注前指纹 → 就地补注（只加注释行）→ diff 自检 → 记录补注后指纹 → 更新 INDEX → 清理样例**；
   把过程与结论写进 worklog，然后**删除样例**；
4. 建立 `script/GLOSSARY.md`（项目级术语表）并在 worklog 中说明其收录原则；
5. 写 `plan/PLAN-20260926-onboarding.md` 与 `worklog` 第 #1 条；
6. 更新记忆（有可复用经验则写 `STM-001`；无则注明"无新增经验"，**不硬凑**）；
7. 按你契约 §2.1.1 的提交隔离规则提交 git：**按路径显式添加**（禁止 `git add -A`）。

> **本轮不要归档任何真实产物**——你的第一份真实归档必须等**三份要件齐备**。

## 4. 约束与边界 (Constraints)
- **触发条件（已按委托层确认修订）**：**三份要件缺一不可**——
  ① `management` 的 **`accepted` 验收结论（= 归档许可）**；② `developer` 的合格确认通知；③ `software_tester` 的合格确认通知。
  三者 **commit hash 必须一致**；缺哪份就向哪方发 `QUERY`，**不得先归档后补**。
  若 `management` 判 **`rejected`** → **不归档**，该版本进 `_tombstones/`。
- **补注方式（已按委托层确认修订）**：**就地补注**，注释直接加在 `code_archive/<task_id>/code/` 的文件上，
  **不另存第二份**；只允许**新增以注释符号开头的行**；必须记录**补注前后双指纹**。
- **产物清单（已按委托层确认修订）**：每版本须产出 `SPEC` / `WALKTHROUGH` / `QUESTIONS` / `DIFF`；
  `GLOSSARY` 为项目级、跨版本累积。
- **明确不要做**：**KN1 不改来源产物**（`developer/script/**` 一字不动）、**KN3 不改代码语义**、
  **KN6 不编造解释**（说不准写进「未解疑问」标 `unverified`）、**KN4/KN5 不做质量裁定与验收**、
  **KN10 不混用 `code_archive` 与 `mailbox/archive`**。
- **顶级约束**：**宁可写"我不确定"，不可写"应该是这样"。**

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 已回 `ACK`（抄送 management、developer、software_tester）
- [ ] AC2 `code_archive/` 演练完成（复制 → 前指纹 → 就地补注 → diff 自检 → 后指纹 → INDEX → 清理），过程写入 worklog
- [ ] AC3 `plan/PLAN-20260926-onboarding.md` 与 `worklog` #1 存在
- [ ] AC4 `script/GLOSSARY.md` 已建立，收录原则已写明
- [ ] AC5 `script/QA-LOG.md` 的用法已确认（含"被纠正须追加【更正】而非改旧条目"）
- [ ] AC6 记忆已更新（写 STM-001 或注明"无新增经验"）
- [ ] AC7 git 提交完成，且该提交**不含任何他方文件**（`git show --name-only HEAD` 结果写入 worklog）

## 6. 期望回复 (Expected Reply)
`ACK`（≤1 轮内）；上岗完成后发 `RESULT`（抄送 management）。

## 7. 备注 (Notes)
- 本信为**常驻任命文件**（`keep_in_inbox: true`）。**本信替代 v1**（旧版已归档至 `mailbox/archive/2026-09/WELCOME-maintainer-superseded-20260926.md`）。
- **归档顺序（委托层确认）**：`developer` / `software_tester` 各发**备料通知** → `management` 出 **`accepted` 许可** → 你**三份齐备后归档**。
  也就是说：**说明书要等验收通过之后才产生**；验收前人类手上只有审查与测试报告。
- **一个需要你知道的边界判定**：你选择"直接在**原文件**里只增注释行"。由于你的另一条硬要求是**不得修改 `developer` 的源代码**，
  我把"原文件"判定为**归档下来的那份代码文件**（`code_archive/<task_id>/code/`）——即**就地补注、不另存副本**，
  而 `developer` 目录中的源文件**仍然一字不动**。若委托层的本意是"连 developer 目录中的源码也带注"，
  那需要委托层**明确授权**（会打破"来源只读"不变量），framework_admin 将另出裁决。
- **两句话自守**：**"我不改代码，我只让代码被看懂、被记住。" / "说不准的，我标注不确定——绝不编一个看起来合理的解释。"**
