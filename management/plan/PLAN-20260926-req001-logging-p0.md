# PLAN-20260926-req001-logging-p0 — 需求 REQ-20260926-001 第一轮分派的编排计划

| 字段 | 值 |
|---|---|
| 计划 ID | PLAN-20260926-req001-logging-p0 |
| 角色 | management (R-002) |
| 关联邮件 | in: 人类用户 2026-09-26 对话渠道需求 + `from_human/开发节奏规划.docx`；out: TASK→developer（MAIL-20260926-1620）、QUERY→人类用户（Q1/Q2）、ACK→framework_admin |
| 创建时间 | 2026-09-26 16:22 |
| 状态 | executing |

> 诚实备注：任命信中的上岗计划 `PLAN-20260923-onboarding` 在 2026-09-23~25 期间未有真实编排动作可规划；
> 本文件是本角色**第一份真实编排计划**，同时覆盖上岗收尾动作。空转三日的事实如实记录于 worklog #1，不硬凑历史计划。

## 1. 目标（可验收判据）
把人类用户的"RDK X5 文本日志系统"需求拆解为可验收任务并完成第一轮分派：
REQ 拆解书落盘、TASK 落邮箱、台账更新、开放问题（跑通环境 Q1 / 部署身份 Q2）请示人类用户。

## 2. 约束（边界、上游、资源）
- 边界：MN2（不写码）、MN14（from_human 只读）、MN5（唯一主责）、MN10/P13（关键问题请示附选项+建议+影响）；
- 上游：`from_human/开发节奏规划.docx`（阶段一定位）、官方手册（平台事实）；
- 资源：developer/code_reviewer/software_tester/maintainer 均已上岗；板端本轮不可达（无远控信息）。

## 3. 记忆依据
LTM-002（唯一主责）、LTM-003（落邮箱）、LTM-005（范围与请示）、LTM-007（人类文件只读+登记+路径引用）、P1/P3/P9/P13。

## 4. 专业方法（为什么选这条路线）
- **先拆解后分派**（P1）：平台盘点（REQ §3）先行，避免把"Linux 自带日志能干嘛"的判断责任转嫁给 developer；
- **平台层直接用 + 业务层自建**的分层裁定：减少自建面，阶段一聚焦"错误码/双时间戳/可靠落盘/读端"这些 MCU 体验痛点；
- **P0 纯 Python 标准库 + 零依赖**：板端网络与 pip 不可假设可用，保证"拿到就能跑"；
- **双端同源错误码**：团队后续 X5 上是 C/C++ 电控程序 + Python 工具链混合，接口分叉是最大漂移风险；
- **测试暂不派发**：板端不可达且无远控信息，此刻派 software_tester 必然得到"环境不可得"——等 Q1 裁决（P6 不铺非关键任务）。

## 5. 步骤
| 步骤 | 输入 | 输出 | 负责人 | 预计 |
|---|---|---|---|---|
| 1 解析并登记人类文件 | docx 原件 | INTAKE-LOG #1 | management | 已完成 |
| 2 平台资料核实 | 官方手册两页 | REQ §3 事实行 | management | 已完成 |
| 3 拆解落盘 | 需求+规划+平台事实 | REQ-20260926-001-logging.md | management | 已完成 |
| 4 派发 TASK | REQ | developer inbox TASK 邮件 | management | 已完成 |
| 5 请示 Q1/Q2 | REQ §7 | QUERY 邮件 + 对话渠道提问 | management | 已完成 |
| 6 交付期跟进 | developer ACK/RESULT | 台账状态流转、（若 Q1=A/B）测试任务 | management | 09-27 |
| 7 验收 | 交付+审查报告 | ACCEPT 报告 | management | 09-27 后 |

## 6. 接口与依赖
task_id `T-20260926-001-logging-platform-p0`；AC 以 REQ §6 为准（冻结）；Q1 裁决决定是否新增 software_tester 任务（新 task_id，不改动 T-001 范围）。

## 7. 风险与回滚
| 风险 | 概率 | 影响 | 缓解 | 回滚 |
|---|---|---|---|---|
| 板端始终不可达，AC8 缺实机证据 | 中 | "可运行"降级为"开发机自测+板端待验证" | Q1 请示，用户书面选择即风险接受记录 | 用户选 C 即视为接受该缺口并记入验收报告 |
| developer 对 WHAT/AC 有异议 | 低 | 一轮往返 | ACK 中要求异议随回执提出 | 按 ISSUE 调整 AC（范围变更再请示用户） |
| 首次全链路协作断链（G10） | 中 | 环节掉链 | 台账逐环节核对邮件流 | 催办 ≤2 次后升级 framework_admin |

## 8. 验收（可勾选项）
- [ ] REQ 拆解书落盘且登记 INDEX
- [ ] TASK 落 developer inbox 且自己 outbox 留档
- [ ] PROJECT-BOARD 首行任务建立（assigned）
- [ ] Q1/Q2 已请示人类用户（邮件 + 对话）
- [ ] from_human 原件未动（MN14）

## 9. 收工检查
- [ ] 产物已登记 INDEX / [ ] worklog 已记 / [ ] mailbox 已闭环 / [ ] 记忆待第一轮真实调度完成后提炼 / [ ] git 已提交
