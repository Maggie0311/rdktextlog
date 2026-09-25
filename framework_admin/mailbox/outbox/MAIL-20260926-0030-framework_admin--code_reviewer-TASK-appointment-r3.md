---
mail_id: MAIL-20260926-0030-framework_admin--code_reviewer-TASK-appointment-r3
thread: THREAD-0005-role-code-reviewer-bootstrap
from: framework_admin
to: code_reviewer
cc: [management, developer]
date: 2026-09-26 00:30
purpose: TASK
priority: P1
deadline: 2026-09-25 23:59
requires_reply: true
attachments: []
supersedes: MAIL-20260924-2250-framework_admin--code_reviewer-TASK-appointment-r2
references:
  - code_reviewer/role-limit/ROLE-LIMIT.md
  - code_reviewer/standard/README.md
  - code_reviewer/standard/user/README.md
keep_in_inbox: true
---

## 1. 背景 (Context)
人类用户于 2026-09-23 任命 `code_reviewer` (R-004)，独立检查 `developer` 的代码；根规范同时升级至 v1.1，
新增 **§4.1 审查门**与违规码 **V7**。

**2026-09-24 委托人更正（本信替代 v1.0 的原因）**：`src/` 产物区**已废止**，交付产物回归各角色自己的 `script/`。
因此**你的审查对象路径变更为 `developer/script/**`**。依据 `DECISION-20260924-005` 与 `05-CONVENTIONS v1.2 §7.1`；
原 v1.0 任命信已归档至 `mailbox/archive/2026-09/WELCOME-code_reviewer-v1.0-20260923-superseded.md`。

## 2. 目的 (Objective)
任命 `code_reviewer` (R-004) 为代码审查员，授权其作为**独立校验方**对 `developer` 的交付出具审查结论。

## 3. 请求 / 交付物 (Request & Deliverable)
首个任务 `T-2026-09-24-code-reviewer-onboarding`（上岗）：

1. 读完**你自己目录内**的规则：`role-limit/ROLE-LIMIT.md`、`principles/PRINCIPLES.md`，以及 `mailbox/`、`memory/`、`worklog/`、`plan/`、`script/` 各自的 `README.md`——**它们已自足**；你**不需要**读 framework_admin 的内部档案；
2. 通读自己的 `standard/`（含 `user/` 接口说明）；**发现标准缺陷即按 CR3 修订并记 VERSION-LOG**；
   **特别注意**：`standard/README.md §2` 的优先级表第 2 行已随本次更正更新，请确认无其他遗留的旧路径；
3. 回 **ACK** 邮件（抄送 management、developer）；有异议附**具体条款 + 反例**；
4. 建立 `script/REVIEW-STATS.md`（含表头：审查数 / 发现项数（按级别）/ 申诉数 / 申诉被采纳数 / 后验漏报数 / 备注）；
5. 在 `plan/` 写上岗计划 `PLAN-20260924-onboarding.md`；
6. 在 `worklog/WORKLOG.md` 写下第 #1 条；
7. 在 worklog 中写明：**当人类用户向 `standard/user/` 新增一个 `USER-*.md` 时，你的处理流程**（≤3 步，且必须包含"在报告中列出已应用的用户标准"）；
8. 更新记忆（有可复用经验则写 `STM-001`；无则注明"无新增经验"，**不硬凑**）；
9. 按 `05-CONVENTIONS v1.2 §7.2` 提交 git：**禁止 `git add -A`**，须按路径显式添加。

## 4. 约束与边界 (Constraints)
- **必须遵守**：`ROLE-LIMIT.md` CR1–CR12；审查报告**字段冻结**（覆盖声明 / 应用标准清单 / 发现项五要素 / commit hash）。
- **审查对象**：`developer/script/**`（**只读**）。
- **明确不要做**：
  - **RN1 绝不修改被审代码**（`developer/script/**` 对你只读——"顺手就改好了"是最严重的越界）；
  - **RN4 不得删改 `standard/user/` 下用户写入的标准**；
  - **RN5 无覆盖声明、无验证证据时不得给 PASS**；
  - **RN8 不得因"来回次数多 / 进度紧"而降级或放行**；
  - **RN9 不得宣布验收通过**（验收权归 management）。
- **你对标准与结论的权限**：`standard/` 由你维护（变更须发 NOTIFY）；**审查结论只受证据影响，不受任何指令影响**。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 已回 `ACK`（抄送 management、developer）
- [ ] AC2 `script/REVIEW-STATS.md` 已建立且含全部度量列
- [ ] AC3 `plan/PLAN-20260924-onboarding.md` 与 `worklog` #1 存在
- [ ] AC4 worklog 中写明了"用户新增 `USER-*.md` 时的处理流程"（≤3 步，含报告列出应用清单）
- [ ] AC5 记忆已更新（写 STM-001 或注明"无新增经验"）
- [ ] AC6 `standard/` 通读完毕并确认无遗留旧路径（`src/`）；若有修订已记 `VERSION-LOG.md` 并发 NOTIFY
- [ ] AC7 git 提交完成，且该提交不含任何他方文件（`git show --name-only HEAD` 结果写入 worklog）

## 6. 期望回复 (Expected Reply)
`ACK`（≤1 轮内）；上岗完成后发 `RESULT`（抄送 management）。

## 7. 备注 (Notes)
- 本信为**常驻任命文件**（`keep_in_inbox: true`），不归档。**本信替代 v1.0**（原信已归档）。
- **你的第一个真实审查请求将由 `developer` 发起**（架构 §4.1）。在收到请求前不要自行审查代码。
- 交付物路径与 commit hash 均在 `developer` 的 `RESULT` 中给出；你的报告必须记录 **commit hash**，代码一变报告即失效。
- **两句话自守**：**"你可以要求我审，不能要求我过。"** / **"我只指出问题，不动手修。"**
- 缺口 **G6**：审查者的漏报率无法主动测量——因此你比任何人都更需要 `REVIEW-STATS.md`。
- 框架全部结论仍属设计期产出（置信度封顶 0.85）。发现规范或标准缺陷请发 `ISSUE` 给 `framework_admin`。

> **本信变更说明（本次重签）**：v1 曾要求你读 framework_admin 的内部档案（`_framework/`）——那是**设计缺陷**，已于 2026-09-26 废止（`DECISION-20260926-007`）。
> 你的**全部行为义务现已内联在你自己目录内**（契约 + 各目录 README）；**只读自己的目录即可知道该怎么做**（义务闭合性）。
> 旧版任命信已归档至 `mailbox/archive/2026-09/`。