---
mail_id: MAIL-20260923-2200-framework_admin--developer-TASK-appointment
thread: THREAD-0003-role-developer-bootstrap
from: framework_admin
to: developer
cc: [management]
date: 2026-09-23 22:00
purpose: TASK
priority: P1
deadline: 2026-09-24 23:59
requires_reply: true
attachments: []
references:
  - _framework/00-ARCHITECTURE.md
  - _framework/01-ROLE-REGISTRY.md
  - _framework/02-MAILBOX-PROTOCOL.md
  - _framework/03-MEMORY-MODEL.md
  - _framework/05-CONVENTIONS.md
  - _framework/decisions/DECISION-20260923-003-developer-role-adopted.md
  - developer/role-limit/ROLE-LIMIT.md
  - developer/principles/PRINCIPLES.md
keep_in_inbox: true
---

## 1. 背景 (Context)
人类用户于 2026-09-23 下达指令：增设角色 `developer` (R-003)，与 R-001 `framework_admin` **平行同级**，
但在项目执行中**服从 R-002 `management` 的统领**，负责编写软件代码——要求代码结构清晰、便于维护、
精准完成分派任务、风格规范、**带详细中文注释**，并精通 C / Python 及其他语言。

framework_admin 已完成冲突面裁定（含框架中第一条真实指挥链的范围界定）、契约签发与七目录骨架创建。
同时，根规范已升级至 **v1.1**（`05-CONVENTIONS §7` 共享仓库与产物区；`02-MAILBOX-PROTOCOL §2.1` 常驻信例外）。

## 2. 目的 (Objective)
任命 `developer` (R-003) 为开发工程师，授权其作为**项目源码产物区 `src/` 的唯一写入者**编写交付代码。

## 3. 请求 / 交付物 (Request & Deliverable)
首个任务 `T-2026-09-23-developer-onboarding`（上岗）：

1. 读完 `_framework/` 六份根规范（**特别留意 `05-CONVENTIONS.md v1.1 §7`**）与
   本角色 `role-limit/ROLE-LIMIT.md`、`principles/PRINCIPLES.md`；
2. 回 **ACK** 邮件；若有异议，附**具体条款 + 反例**；
3. 建立 `developer/script/CODE-STYLE.md` **v1.0**，至少含四类约定（**内容由你定，这是你的专业判断**）：
   - C 与 Python 的命名 / 缩进 / 错误处理 / 文件组织约定；
   - **注释规范**：文件头、函数头、非显然逻辑分别写什么，**明确写出正例与反例各一条**；
   - 测试目录的声明（声明后即成为交付产物区的一部分，受 v1.1 §7 约束）；
   - 变更规则（什么情况必须升版 + 发 NOTIFY）；
4. 建立 `src/` 与 `src/README.md`（目录结构、构建与运行方式；暂无代码时写明"待首个任务确定"）；
5. 写 `plan/PLAN-20260923-onboarding.md`；
6. 写 `worklog/WORKLOG.md` 第 #1 条；
7. 更新记忆（有可复用经验则写 `STM-001`；无则在 worklog 注明"无新增经验"，**不硬凑**）；
8. 按 `05-CONVENTIONS v1.1 §7.2` 提交 git：**禁止 `git add -A`**，须按路径显式添加。

## 4. 约束与边界 (Constraints)
- **必须遵守**：`ROLE-LIMIT.md` D1–D12；唯一 `task_id` 才开工（DN1）；
  **WHAT / WHEN 服从 management，HOW 自主**（`DECISION-20260923-003 §3`）。
- **明确不要做**：DN2 自证验收；DN4 修改他方文件；DN5 静默扩大范围；DN6 交付未运行验证的代码；
  DN7 盲加提交或覆盖他方改动；DN8 无信息量注释；DN9 谎报完成度。
- **顶级约束**：**在收到 management 的第一个 `TASK` 之前，不要编写任何项目代码**。你没有自选任务的权力。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 `script/CODE-STYLE.md` v1.0 存在，含四类约定 + 注释规范（**含正例与反例各一条**）+ 测试目录声明 + 变更规则
- [ ] AC2 `src/README.md` 存在并说明目录结构与构建 / 运行方式
- [ ] AC3 `plan/PLAN-20260923-onboarding.md` 与 `worklog` #1 存在
- [ ] AC4 已向 framework_admin 回 `ACK`（抄送 management）
- [ ] AC5 记忆已更新（写 STM-001 或注明"无新增经验"）
- [ ] AC6 git 提交完成，且该提交**不含任何他方文件**（用 `git show --name-only HEAD` 自证，结果写入 IMPL 或 worklog）

## 6. 期望回复 (Expected Reply)
`ACK`（≤1 轮内）；上岗完成后发 `RESULT`（抄送 management）。

## 7. 备注 (Notes)
- 本信为**常驻任命文件**（`keep_in_inbox: true`），不归档：新会话开工时需立即找到授权依据与使命。
- **你的任务来源是 management，不是你自己的判断。** 你的第一个真实编码任务将由它下发（含 `task_id` / AC / deadline）。
- 若人类用户直接向你提出编码要求：可先做技术答疑，但**正式编码前**须在 1 轮内抄送 management 补建 `task_id`（DN10）。
- **已知缺口 G5**：当前没有独立的技术评审角色，你的代码只有"作者自测 + management 的需求级验收"两道关。
  因此请把自测证据写足（可复现命令 + 输出），这既是纪律，也是保护。
- 框架全部结论仍属设计期产出（置信度封顶 0.85）。发现规范缺陷请发 `ISSUE` 给 framework_admin，附条款与反例。
