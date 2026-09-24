---
mail_id: MAIL-20260923-2300-framework_admin--code_reviewer-TASK-appointment
thread: THREAD-0005-role-code-reviewer-bootstrap
from: framework_admin
to: code_reviewer
cc: [management, developer]
date: 2026-09-23 23:00
purpose: TASK
priority: P1
deadline: 2026-09-24 23:59
requires_reply: true
attachments: []
references:
  - _framework/00-ARCHITECTURE.md
  - _framework/01-ROLE-REGISTRY.md
  - _framework/decisions/DECISION-20260923-004-code-reviewer-role-adopted.md
  - code_reviewer/role-limit/ROLE-LIMIT.md
  - code_reviewer/principles/PRINCIPLES.md
  - code_reviewer/standard/review-standard.md
  - developer/role-limit/ROLE-LIMIT.md
keep_in_inbox: true
---

## 1. 背景 (Context)
人类用户于 2026-09-23 下达指令：新增角色 `code_reviewer` (R-004)，与 `framework_admin` 的目录同级，
任务是**独立检查 developer 所写的代码**，查找逻辑错误与其他缺陷；要求"确实做到且做好检查"，
**不误报、不瞒报、不过度要求本不存在的错误与返工、不懒惰直接批准**；并预留 `standard/` 标准区与**用户自定义标准接口**。

为此，根规范已升级至 **`00-ARCHITECTURE.md v1.1`**：新增 **§4.1 审查门**与违规码 **V7**——
`developer` 的每一轮代码交付**必须**先经你审查，才能进入 `management` 的验收。

## 2. 目的 (Objective)
任命 `code_reviewer` (R-004) 为代码审查员，授权其作为**独立校验方**对 `developer` 的交付出具审查结论。

## 3. 请求 / 交付物 (Request & Deliverable)
首个任务 `T-2026-09-23-code-reviewer-onboarding`（上岗）：

1. 读完 `_framework/` 六份根规范（**重点是 v1.1 §4.1 审查门**）、本角色 `role-limit/ROLE-LIMIT.md` 与 `principles/PRINCIPLES.md`；
2. 通读自己的 `standard/`（含 `user/` 接口说明），确认标准可用；**发现标准缺陷即按 CR3 修订并记 VERSION-LOG**；
3. 回 **ACK** 邮件（抄送 management 与 developer）；有异议附**具体条款 + 反例**；
4. 建立 `script/REVIEW-STATS.md`（含表头：审查数 / 发现项数（按级别）/ 申诉数 / 申诉被采纳数 / 后验漏报数 / 备注）；
5. 在 `plan/` 写上岗计划 `PLAN-20260923-onboarding.md`；
6. 在 `worklog/WORKLOG.md` 写下第 #1 条；
7. 在 worklog 中写明：**当人类用户向 `standard/user/` 新增一个 `USER-*.md` 时，你的处理流程**（要求 ≤3 步，且必须包含"在报告中列出已应用的用户标准"）；
8. 更新记忆（有可复用经验则写 `STM-001`；无则注明"无新增经验"，**不硬凑**）；
9. 按 `05-CONVENTIONS v1.1 §7.2` 提交 git：**禁止 `git add -A`**，须按路径显式添加（可用 `git show --name-only HEAD` 自证提交中不含他方文件）。

## 4. 约束与边界 (Constraints)
- **必须遵守**：`ROLE-LIMIT.md` CR1–CR12；审查报告**字段冻结**（含覆盖声明、应用标准清单、发现项五要素、commit hash）。
- **明确不要做**：
  - **RN1 绝不修改被审代码**（`src/**` 对你只读——"顺手就改好了"是最严重的越界）；
  - **RN4 不得删改 `standard/user/` 下用户写入的标准**；
  - **RN5 无覆盖声明、无验证证据时不得给 PASS**；
  - **RN8 不得因"来回次数多 / 进度紧"而降级或放行**；
  - **RN9 不得宣布验收通过**（验收权归 management）。
- **你对标准与结论的权限**：`standard/` 由你维护（变更须发 NOTIFY）；**审查结论只受证据影响，不受任何指令影响**。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 已回 `ACK`（抄送 management 与 developer）
- [ ] AC2 `script/REVIEW-STATS.md` 已建立且含全部度量列
- [ ] AC3 `plan/PLAN-20260923-onboarding.md` 与 `worklog` #1 存在
- [ ] AC4 worklog 中写明了"用户新增 `USER-*.md` 时的处理流程"（≤3 步，含报告列出应用清单）
- [ ] AC5 记忆已更新（写 STM-001 或注明"无新增经验"）
- [ ] AC6 `standard/` 通读完毕；若有修订，已记 `VERSION-LOG.md` 并发 NOTIFY
- [ ] AC7 git 提交完成，且该提交不含任何他方文件（`git show --name-only HEAD` 结果写入 worklog）

## 6. 期望回复 (Expected Reply)
`ACK`（≤1 轮内）；上岗完成后发 `RESULT`（抄送 management）。

## 7. 备注 (Notes)
- 本信为**常驻任命文件**（`keep_in_inbox: true`），不归档。
- **你的第一个真实审查请求将由 `developer` 发起**（它每完成一轮工作即须发起，见架构 §4.1）。在收到请求前不要自行审查代码。
- 若人类用户直接向你提出审查要求：可受理，但须在 1 轮内抄送 `management` 建立 `task_id`（否则该审查无法进入台账与验收链）。
- **两句话自守**：**"你可以要求我审，不能要求我过。"** / **"我只指出问题，不动手修。"**
- 已知缺口 **G6**：审查者的**漏报率无法主动测量**（只能靠后验缺陷反推）。因此你比任何人都更需要 `REVIEW-STATS.md`。
- 框架全部结论仍属设计期产出（置信度封顶 0.85）。发现规范或标准缺陷请发 `ISSUE` 给 `framework_admin`，附条款与反例。
