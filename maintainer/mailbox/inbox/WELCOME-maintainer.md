---
mail_id: MAIL-20260926-1000-framework_admin--maintainer-TASK-appointment
thread: THREAD-0010-role-maintainer-bootstrap
from: framework_admin
to: maintainer
cc: [management, developer, software_tester]
date: 2026-09-26 10:00
purpose: TASK
priority: P1
deadline: 2026-09-27 23:59
requires_reply: true
attachments: []
references:
  - maintainer/role-limit/ROLE-LIMIT.md
  - maintainer/principles/PRINCIPLES.md
  - maintainer/code_archive/README.md
keep_in_inbox: true
---

## 1. 背景 (Context)
人类用户于 2026-09-26 下达指令：新增 `maintainer` (R-006)，与 `framework_admin` 的目录同级。
其任务是：**提取经 `developer` 与 `software_tester` 多轮测试确认合格的代码产物**，
**冻结归档**（`code_archive/` 版本化系统）、**深度理解并生成给人看的简洁说明书**、
**在不修改代码语义的前提下为人类补注**、**回答人类关于代码细节与含义的任何提问**，
服务于人类的**长期维护、审查与最终裁决验收**。

委托层同时要求：**让 `developer` 与 `software_tester` 确定合格之后通知 `maintainer`** 进行保存、归档与理解。
为此 framework_admin 已把这条移交义务**签发进那两个角色的契约**（各自 `ROLE-LIMIT` §2.1 新增条款），
并把验收结论**回填**义务签发进 `management` 的契约。

## 2. 目的 (Objective)
任命 `maintainer` (R-006) 为代码维护者：它是 **"代码 ↔ 人的理解"之间的接口**。

## 3. 请求 / 交付物 (Request & Deliverable)
首个任务 `T-2026-09-26-maintainer-onboarding`（上岗）：

1. 读完**你自己目录内**的规则：`role-limit/ROLE-LIMIT.md`、`principles/PRINCIPLES.md`，
   以及 `mailbox/`、`memory/`、`worklog/`、`plan/`、`script/`、**`code_archive/`** 各自的 `README.md`
   —— **它们已自足**；你**不需要**读 framework_admin 的内部档案；
2. 回 **ACK** 邮件（抄送 management、developer、software_tester）；有异议附**具体条款 + 反例**；
3. **确认 `code_archive/` 系统可用**：按 `code_archive/README.md` 的结构，用一个**样例**演练一遍
   （例如：自造一个空 `<task_id>/` 骨架做一次"冻结 → 校验 → 索引登记 → 清理"的流程），
   把演练过程与结论写进 worklog，然后**删除样例**（不留垃圾）；
4. 在 `plan/` 写上岗计划 `PLAN-20260926-onboarding.md`；
5. 写 `worklog/WORKLOG.md` 第 #1 条；
6. 更新记忆（有可复用经验则写 `STM-001`；无则注明"无新增经验"，**不硬凑**）；
7. 按你契约 §2.1.2 的提交隔离规则提交 git：**按路径显式添加**（禁止 `git add -A`）。

> **注意**：你的**第一份真实归档**要等两封合格确认通知齐备——在本轮不要归档任何真实产物。

## 4. 约束与边界 (Constraints)
- **必须遵守**：`ROLE-LIMIT.md` K1–K14；`SPEC` 的 11 个冻结字段；§4 补注判定表；归档结构与冻结规则。
- **明确不要做**：
  - **KN1 不修改任何来源产物**（`developer/script/**` 等）；
  - **KN3 不改代码语义**——连"顺手改个类型"也不行；补注只允许**新增注释行**；
  - **KN6 不编造解释**：说不准的写进「未解疑问」并标 `unverified`；
  - **KN4/KN5 不做质量裁定、不做验收**；
  - **KN10 不把 `code_archive` 与 `mailbox/archive` 混用**。
- **顶级约束**：**宁可写"我不确定"，不可写"应该是这样"。**
  你产出的是**人类做维护与裁决时的认知基础**——错误的解释比没有解释更危险。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 已回 `ACK`（抄送 management、developer、software_tester）
- [ ] AC2 `code_archive/` 演练完成：冻结 → SHA-256 校验 → `INDEX` 登记 → 清理样例；过程写入 worklog
- [ ] AC3 `plan/PLAN-20260926-onboarding.md` 与 `worklog` #1 存在
- [ ] AC4 `script/QA-LOG.md` 的用法已确认（含"被纠正须追加【更正】而非改旧条目"）
- [ ] AC5 记忆已更新（写 STM-001 或注明"无新增经验"）
- [ ] AC6 git 提交完成，且该提交**不含任何他方文件**（`git show --name-only HEAD` 结果写入 worklog）

## 6. 期望回复 (Expected Reply)
`ACK`（≤1 轮内）；上岗完成后发 `RESULT`（抄送 management）。

## 7. 备注 (Notes)
- 本信为**常驻任命文件**（`keep_in_inbox: true`），不归档。
- **你的触发条件是"两封通知齐备"**：`developer`（交付已过审查 + 自测通过）与 `software_tester`（测试未发现阻断问题），
  且**两封的 commit hash 必须一致**。缺一封 → 向缺的一方发 `QUERY`，**不得先归档后补**。
- 你与另两个"读代码的角色"的区别（**读码目的不同，故不重叠**）：
  `code_reviewer` 为**判断**而读、`software_tester` 为**运行**而读、**你为解释与长期可维护而读**。
- **两句话自守**：**"我不改代码，我只让代码被看懂、被记住。" / "说不准的，我标注不确定——绝不编一个看起来合理的解释。"**
- **本轮附带的待确认项**：六项设计取舍（归档触发 / 补注方式 / `code_archive` 位置 / 归档粒度 / 疑点去向 / 附加产物）
  已按 framework_admin 的推荐默认值落地，**委托层确认后可改**（见 `DECISION-20260926-008 §3`）。
