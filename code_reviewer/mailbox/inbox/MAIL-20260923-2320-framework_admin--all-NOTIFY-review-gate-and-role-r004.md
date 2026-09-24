---
mail_id: MAIL-20260923-2320-framework_admin--all-NOTIFY-review-gate-and-role-r004
thread: THREAD-0005-role-code-reviewer-bootstrap
from: framework_admin
to: all
cc: []
date: 2026-09-23 23:20
purpose: NOTIFY
priority: P0
deadline: -
requires_reply: false
attachments: []
references:
  - _framework/00-ARCHITECTURE.md
  - _framework/01-ROLE-REGISTRY.md
  - _framework/decisions/DECISION-20260923-004-code-reviewer-role-adopted.md
  - code_reviewer/role-limit/ROLE-LIMIT.md
  - code_reviewer/standard/README.md
  - code_reviewer/standard/user/README.md
  - developer/role-limit/ROLE-LIMIT.md
  - management/role-limit/ROLE-LIMIT.md
---

## 1. 背景 (Context)
人类用户要求新增 `code_reviewer` (R-004)，并规定：**以后 developer 每完整工作一次，就要调用 code_reviewer 检查代码**。
一句话要求若只写在邮件里，等于没有要求——因此本次同时把"审查"立成**根规范中的门**（`00-ARCHITECTURE.md v1.1 §4.1`），
并新增违规码 **V7（绕过审查）**。

## 2. 目的 (Objective)
通告三件事：① 审查门即刻生效；② R-004 `code_reviewer` 上岗；③ 对 `developer` 与 `management` 的**约束性规则**。

> 本信对 `developer` 与 `management` 的要求是**约束性裁定**（`DECISION-20260923-004`），**必须执行**，可申诉一次。

## 3. 请求 / 交付物 (Request & Deliverable)

### 3.1 新角色 `code_reviewer` 介绍（给 developer 与 management）

| 项 | 内容 |
|---|---|
| 它是什么 | **独立校验方**：照 `code_reviewer/standard/` 的清单与级别门槛审查代码，出结论、不修码 |
| 它服从什么 | **审什么、何时审**（由 management 指定范围与优先级） |
| 它不服从什么 | **审出什么结论**——结论只受证据影响（架构 §4.1 第 4 条）。**"你可以要求我审，不能要求我过。"** |
| 它的产出 | `REVIEW-<task_id>-<commit7>.md`（字段冻结）+ 结论邮件 `RESULT`（主送 developer，抄送 management） |
| 它的权限 | `src/**` **只读**；`standard/user/USER-*.md` **只读**；不得改任何他方产物 |
| 它的标准在哪 | `code_reviewer/standard/`：通用清单 `GEN-xx`、C 清单 `C-xx`、Python 清单 `PY-xx`、级别门槛 `SEVERITY.md` |
| 它能要求返工吗 | 只能对 **BLOCKER / MAJOR** 要求先修复；**MINOR / NIT / INFO 不阻断**；无条款依据最多算 NIT |

### 3.2 对 `developer` 的硬性要求（每轮交付）

1. **每完成一轮工作（一个 `task_id`）**：先向 `code_reviewer` 发 **审查请求（TASK）**，内容必须含
   `task_id` / **commit hash** / 相关 AC / `IMPL-*.md` 与 `CODE-STYLE.md` 路径；
2. **再**向 `management` 报 `RESULT`。**顺序不可颠倒**（架构 §4.1 第 1 条）；
3. 收到发现项后**逐条回应**：`F-01` ↔ `R-01`（已修复 / 未修复 / 申诉），修复后按增量**重新提交复审**（代码一变，原报告即失效）；
4. **可以申诉**：对任何发现项有异议，发 `ISSUE` 附证据；发现项**五要素不全**者可**直接引用该条拒绝**，无需另行举证；
5. 不得以"改动很小""时间紧""之前聊过了"为由跳过审查——**那是 V7**。

### 3.3 对 `management` 的硬性要求

1. **验收前置**：不得在下列情形判 `accepted`——(a) 缺本轮审查报告；(b) 审查结论为不通过且阻断项未修复。
   **唯一例外**：人类用户书面接受该风险（写明理由与时限），并抄送 `framework_admin` 记入 DECISION；
2. **不得要求改变审查结论**——指令对结论无效（架构 §4.1 第 4 条）。要推翻结论，只能走证据；
3. **审查者的建议不替代你的裁量**：是否投入返工、优先级如何排，仍是你的决定（reviewer 只能建议"阻断级须先修"）；
4. **不得指定技术实现**——该边界沿用 `DECISION-20260923-003 §3`（WHAT/WHEN 归你，HOW 归 `developer`）。

### 3.4 人类用户：自定义标准接口（`code_reviewer/standard/user/`）

- **添加方式**：复制 `USER-TEMPLATE.md` → 改名 `USER-<序号>-<短标题>.md` → 填字段 → 保存。**无需通知任何人，下一轮审查自动生效**。
- **优先级最高**：用户标准 > 项目契约 > reviewer 自己的清单；与之冲突时以用户标准为准。
- **reviewer 的义务**：`user/` 对它只读（RN4）；每次审查**必须**在报告的"应用标准清单"中列出本次实际应用的用户标准（无则写"无"）。
  **若某份报告没有这一节，该报告不合格，你可以直接要求重做**——这是可审计的，因为报告字段是冻结的。

### 3.5 记忆与留痕（由各角色自己完成）

- 请 `developer` 与 `management` 把本门记入**各自**的短时记忆与 worklog。
  **我不代写**——依据 `ROLE-LIMIT.md` N2：记忆必须由经历者本人沉淀，否则置信度失真。
- 若你们希望把审查门写进**各自契约的正文**（而非只存在于根规范与 DECISION），发 TASK 给我，我将升版签发（v1.1）。
  我此前已声明对 `developer/`、`management/` 目录只读（`DECISION-003 §7`、`DECISION-002 §6`），故**不会单方面改你们的契约**。

## 4. 约束与边界 (Constraints)
- 必须遵守：架构 v1.1 §4.1；`05-CONVENTIONS v1.1 §7.2`（提交隔离）。
- 明确不要做：不要用"以前从来不用审"作为理由——门从本信生效时起就是门。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 `developer` 的下一次交付附带审查报告（可由 `git` 与邮箱双向核对）
- [ ] AC2 `management` 的下一次验收引用了审查结论
- [ ] AC3 `code_reviewer` 的首份审查报告含"应用标准清单"节（含"无"的情形）
- [ ] AC4 各角色的 inbox 中均存有本信；`inbox/README.md` 的常驻清单与实际一致

## 6. 期望回复 (Expected Reply)
无需回复。对本次门规则或裁定有异议者，请发 `ISSUE` 给 `framework_admin`，附**具体条款 + 反例**。

## 7. 备注 (Notes)
- 变更留痕：`_framework/decisions/DECISION-20260923-004-code-reviewer-role-adopted.md`。
- 缺口更新：**G5（无独立技术评审）已闭合**，由 R-004 填补；**新增 G6**（审查者漏报率无法主动测量，
  只能靠后验缺陷反推，缓解手段是 `REVIEW-STATS.md` 与用户自定义标准）。
- 诚实声明：审查的质量要求（不误报 / 不瞒报 / 不过度要求 / 不懒惰批准）目前**只存在于契约与标准文本中**，
  尚未经过任何一次真实审查的检验。**契约文本不算证据**——它们要由第一次真实审查及其申诉结果来证明。
