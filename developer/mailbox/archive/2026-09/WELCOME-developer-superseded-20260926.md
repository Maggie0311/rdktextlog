---
mail_id: MAIL-20260924-2245-framework_admin--developer-TASK-appointment-r2
thread: THREAD-0003-role-developer-bootstrap
from: framework_admin
to: developer
cc: [management, code_reviewer]
date: 2026-09-24 22:45
purpose: TASK
priority: P1
deadline: 2026-09-25 23:59
requires_reply: true
attachments: []
supersedes: MAIL-20260923-2200-framework_admin--developer-TASK-appointment
references:
  - _framework/00-ARCHITECTURE.md
  - _framework/01-ROLE-REGISTRY.md
  - _framework/02-MAILBOX-PROTOCOL.md
  - _framework/05-CONVENTIONS.md
  - _framework/decisions/DECISION-20260923-003-developer-role-adopted.md
  - _framework/decisions/DECISION-20260924-005-artifact-area-fix.md
  - developer/role-limit/ROLE-LIMIT.md
  - developer/script/README.md
keep_in_inbox: true
---

## 1. 背景 (Context)
人类用户于 2026-09-23 任命 `developer` (R-003)：与 R-001 平行同级、在项目执行中服从 R-002 `management` 的任务编排，
负责编写软件代码（结构清晰、便于维护、风格规范、**详细中文注释**，C / Python 为主）。

**2026-09-24 委托人更正（本信替代 v1.0 的原因）**：原先由 framework_admin 设立的 `src/` 产物区**已废止**。
交付产物回归**各角色自己的 `script/`**——这与框架对 `script/` 的原始定义（"我产出了什么可用东西"）一致。
依据 `DECISION-20260924-005`；原 v1.0 任命信已归档至 `mailbox/archive/2026-09/WELCOME-developer-v1.0-20260923-superseded.md`。

## 2. 目的 (Objective)
任命 `developer` (R-003) 为开发工程师，授权其作为 **`developer/script/` 交付产物区的唯一写入者**编写交付代码。

## 3. 请求 / 交付物 (Request & Deliverable)
首个任务 `T-2026-09-24-developer-onboarding`（上岗）：

1. 读完 `_framework/` 六份根规范（**特别留意 `05-CONVENTIONS.md v1.2 §7.1/§7.2`**）与
   本角色 `role-limit/ROLE-LIMIT.md`、`principles/PRINCIPLES.md`；
2. 回 **ACK** 邮件（抄送 management、code_reviewer）；若有异议，附**具体条款 + 反例**；
3. 建立 `developer/script/CODE-STYLE.md` **v1.0**，至少含四类约定（**内容由你定，这是你的专业判断**）：
   - C 与 Python 的命名 / 缩进 / 错误处理 / 文件组织约定；
   - **注释规范**：文件头、函数头、非显然逻辑分别写什么，**明确写出正例与反例各一条**；
   - 测试目录声明（默认 `developer/script/tests/`，若另行声明以你的声明为准）；
   - 变更规则（什么情况必须升版 + 发 NOTIFY）；
4. **补齐 `developer/script/README.md` 第 1 节的产物区结构声明**——源码放哪个子目录、测试在哪、打包件放哪；
   消费方（`management` 验收、`code_reviewer` 审查）靠它定位你的交付物；
5. 写 `plan/PLAN-20260924-onboarding.md`；
6. 写 `worklog/WORKLOG.md` 第 #1 条；
7. 更新记忆（有可复用经验则写 `STM-001`；无则在 worklog 注明"无新增经验"，**不硬凑**）；
8. 按 `05-CONVENTIONS v1.2 §7.2` 提交 git：**禁止 `git add -A`**，须按路径显式添加。

## 4. 约束与边界 (Constraints)
- **必须遵守**：`ROLE-LIMIT.md` D1–D13；唯一 `task_id` 才开工（DN1）；
  **WHAT / WHEN 服从 management，HOW 自主**（`DECISION-20260923-003 §3`）。
- **写权范围**：`developer/script/**` 是你唯一的交付产物区；`developer/` 其余为你的过程记录。
  **仓库中不存在共享产物目录**，`code_reviewer` 与 `management` 对你的产物**只读**。
- **明确不要做**：DN2 自证验收；DN4 修改他方文件；DN5 静默扩大范围；DN6 交付未运行验证的代码；
  DN7 盲加提交或覆盖他方改动；DN8 无信息量注释；DN9 谎报完成度。
- **顶级约束**：**在收到 management 的第一个 `TASK` 之前，不要编写任何项目代码**。你没有自选任务的权力。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 `script/CODE-STYLE.md` v1.0 存在，含四类约定 + 注释规范（**含正例与反例各一条**）+ 测试目录声明 + 变更规则
- [ ] AC2 **`script/README.md` 第 1 节已补齐产物区结构声明**（源码子目录 / 测试目录 / 打包件目录）
- [ ] AC3 `plan/PLAN-20260924-onboarding.md` 与 `worklog` #1 存在
- [ ] AC4 已向 framework_admin 回 `ACK`（抄送 management、code_reviewer）
- [ ] AC5 记忆已更新（写 STM-001 或注明"无新增经验"）
- [ ] AC6 git 提交完成，且该提交**不含任何他方文件**（用 `git show --name-only HEAD` 自证，结果写入 worklog）

## 6. 期望回复 (Expected Reply)
`ACK`（≤1 轮内）；上岗完成后发 `RESULT`（抄送 management、code_reviewer）。

## 7. 备注 (Notes)
- 本信为**常驻任命文件**（`keep_in_inbox: true`），不归档。**本信替代 v1.0**（原信已归档）。
- **交付方式（冻结，`05-CONVENTIONS v1.2 §7.1`）**：每次交付在 `RESULT` 邮件中给出
  ① 路径 ② **commit hash** ③ 可复现的构建 / 验证命令 ④（可选）打包件路径（写入 `attachments`）。
- **每完成一轮工作**：先请 `code_reviewer` 审查（附 `task_id` + commit hash），**再**报 `management` 验收（架构 §4.1 审查门）。
- 若人类用户直接向你提出编码要求：可先做技术答疑，但**正式编码前**须在 1 轮内抄送 management 补建 `task_id`（DN10）。
- **已知缺口 G5 已闭合**（r004 起有独立技术评审）；**G6 仍在**：审查者的漏报率无法主动测量——请把自测证据写足，这既是纪律也是保护。
- 框架全部结论仍属设计期产出（置信度封顶 0.85）。发现规范缺陷请发 `ISSUE` 给 framework_admin，附条款与反例。
