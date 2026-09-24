---
id: STM-006
title: 校验/判断型角色的服从边界必须切在 PROCESS 与 VERDICT 之间（"可以要求我审，不能要求我过"），否则审查退化为盖章
layer: short-term
status: candidate
confidence: 0.35
evidence_count: 1
success_count: 0
failure_count: 0
source_tasks: [T-2026-09-23-create-code-reviewer-role]
first_seen: 2026-09-23
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.025
promoted_to: none
tags: [boundary, authority, independence]
---

## 观察 (Observation)
创建 R-004 `code_reviewer`（独立审查 `developer` 的代码）时，遇到一个 `STM-005` 未能直接覆盖的情形：
用户既要求它"受 management 统领"（审什么、何时审由 management 定），又要求它"不误报、不瞒报、不懒惰批准"。
后者若可由 management 一句话改变，则审查立刻退化为盖章——**"不懒惰批准"与"服从统领"直接冲突**。

解法不是折中，而是**换切分轴**：
- 产出**交付物**的角色（如 `developer`）：切在 **WHAT/WHEN（服从） vs HOW（自主）**；
- 产出**判断**的角色（如 `code_reviewer`）：切在 **PROCESS（服从） vs VERDICT（不服从）**。

写成一句可执行的话就是：**"你可以要求我审，不能要求我过。"**
并配一条机制：改变结论的唯一途径是**补充证据**（申诉成立则撤回并记入 `REVIEW-STATS`），而不是指令。

## 提炼 (Generalization)
当新角色的产出是"**判断/结论**"而非"**物件**"时，其独立性必须落在**结论生成环节**上：
把"流程"划给指挥方，"结论"留给角色自己，且明确规定"改变结论的唯一合法输入是证据"。
若只写"服从统领"或只写"独立判断"，两种失效必发生其一：要么被指挥成盖章机，要么以"独立"为由拒绝接活。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | T-2026-09-23-create-code-reviewer-role | 待验证 | 裁定见 `DECISION-20260923-004 §2.3`，并已写入根规范 `00-ARCHITECTURE §4.1` 第 4 条（结论独立于指令） |

## 待验证 (To Verify)
需在出现**第二个产出"判断"的角色**时验证（例如未来的"验收员""安全审查员"或"合规检查员"）。
若 PROCESS/VERDICT 这一刀仍能消解冲突 -> 可考虑晋升为长期记忆。

反面待验证：**独立性过强**导致协作失灵——例如审查者以"结论独立"为由拒绝接受 management 的范围限定与优先级安排。
届时需补充"独立性只覆盖结论、不覆盖范围与时效"的限定句。

晋升还差：`evidence_count` 需 ≥3 + ≥1 次独立确认。

## 应用方式 (How to apply)
创建任何产出"判断/结论"的角色时：
1. 把它的行为拆成**流程**（审什么、何时审、按什么交付）与**结论**（通过/不通过、级别、发现项）两段；
2. 流程段写"服从 X 角色"；结论段写"**只受证据影响**"，并援引根规范（本框架为 `00-ARCHITECTURE §4.1` 第 4 条）；
3. 显式写明**合法改变结论的唯一输入是证据**，并给出申诉/证据通道；
4. 用一句自守句固化。本角色用的是：**"你可以要求我审，不能要求我过。"**
