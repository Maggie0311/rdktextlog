---
mail_id: MAIL-20260926-1130-framework_admin--system-RESULT-maintainer-design-confirmed
thread: THREAD-0010-role-maintainer-bootstrap
from: framework_admin
to: system (人类用户)
cc: [management, developer, code_reviewer, software_tester, maintainer]
date: 2026-09-26 11:30
purpose: RESULT
priority: P1
deadline: -
requires_reply: true
attachments: []
references:
  - _framework/decisions/DECISION-20260926-009-maintainer-design-confirmed.md
  - maintainer/role-limit/ROLE-LIMIT.md
---

## 1. 背景 (Context)
你就 `maintainer` 的六项设计取舍做了确认。你的选择中有 **3 项与我的默认值不同**，我已逐处改到位。

## 2. 目的 (Objective)
回报六项已执行完毕；并请你确认**一处我需要你拍板的边界**（§4）。

## 3. 你的选择与执行结果

| # | 项 | 你的选择 | 我的处理 |
|---|---|---|---|
| 1 | 归档触发 | **必须先经 management 验收通过** | 改为**三份要件**：`management` 的 `accepted`（**许可**）+ 两封确认通知（**备料**）；三者 commit hash 必须一致；`rejected` → 不归档、进墓碑 |
| 2 | 补注方式 | **直接在原文件里只增注释行** | 改为**就地补注**：归档代码文件上直接加注释、**不另存副本**；新增**双指纹**要求；`original/`+`annotated/` 双目录 → 单一 `code/` |
| 3 | 归档位置 | `maintainer/code_archive/` | 不变 |
| 4 | 归档粒度 | 全留历史 + 大文件不入库 | 不变 |
| 5 | 疑点去向 | 发 ISSUE 给 developer 抄 management | 不变 |
| 6 | 附加产物 | **四类全要** | 四类均改为**每版本必产出**（术语表为项目级、跨版本累积） |

**改动落点（全部同步，非只改一处）**：
`maintainer` 契约（触发依赖 / 权力轴 / K1 / 权限矩阵 / KN2 / KN11 / §3 输入 / §5 / DoD）、
`code_archive/README.md` 与 `INDEX.md`、`script/README.md`+`INDEX.md`+**新增 `GLOSSARY.md`**、
**三方契约**（`management` §2.1.4「归档许可」、`developer` §2.1.5「归档备料」、`software_tester` §2.1.4「归档备料」）、
4 条记忆（LTM-001/002/003/009，**各附修订记录**）、任命信 **r2**（旧版已归档）。

## 4. 有一处冲突需要你拍板（**这是本信的要点**）

你选择了「**直接在原文件里**只增注释行」。但你的**另一条硬要求**是「**不得修改 `developer` 的源代码**」，
而 `developer` 的契约规定其 `script/**` 由 developer **独占写入**。两条要求在这里相抵。

**我的处理**：把"原文件"判定为「**归档下来的那份代码文件**」——
即注释加在 `code_archive/<task_id>/code/` 上、**不另存副本**；**`developer` 目录里的源文件仍然一字不动**。
这样你要的"人类打开的就是带注释的那份"成立，同时不打破"来源只读"。

**如果你要的是「连 developer 目录里的源代码也带注」**，请说一声——那需要你**明确授权**，因为：
① 它打破"来源只读"与"每块区域一个写入者"两条不变量；
② 带注后，代码与**既有审查报告 / 测试报告所对应的 commit** 不再一致，三方证据链要重新对齐；
③ 我会另出裁决，并把变更**签发**给 `developer` / `code_reviewer` / `software_tester` 三方。

> 我没有替你选其中一条执行，也没有停摆：**按改动面最小、可逆的方式先落地，并把冲突显式入档待你确认。**

## 5. 一个副作用，你应该提前知道

**归档触发改为"验收前置"之后，说明书要等你（或 management）验收通过之后才会产生。**
也就是说：**验收前你手上只有审查报告与测试报告，没有 `maintainer` 的说明书**。
如果这与你"**便于人类最终裁决并验收**"的初衷有冲突（拿着说明书去裁决 vs 裁决后才有说明书），
可以改成：**验收前先出"预览版说明书"（标注未验收）**，验收后出正式版。要的话我加这一条。

## 6. 验收 (Acceptance)
- [x] 六项取舍全部落地（3 项变更 + 3 项确认）
- [x] 三方契约 + 归档系统 + 记忆 + 任命信全部同步
- [x] 冲突已入档并显式请示（`DECISION-20260926-009 §4`）
- [x] `AUDIT-LOG` R11；`script/INDEX` 第 31 项；worklog #62–#64
- [x] 通告已投递五方 inbox
- [x] 按 §7.2 显式路径提交 git

## 7. 期望回复 (Expected Reply)
只需回两点：
1. §4 的边界：**仅限归档副本**（我的处理）／**连 developer 目录也要带注**（需授权）；
2. §5：**是否要"验收前预览版说明书"**（要／不要）。
