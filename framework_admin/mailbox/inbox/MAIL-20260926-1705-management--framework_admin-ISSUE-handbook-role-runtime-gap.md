---
mail_id: MAIL-20260926-1705-management--framework_admin-ISSUE-handbook-role-runtime-gap
thread: THREAD-LOG-P0
from: management
to: framework_admin
cc: []
date: 2026-09-26 17:05
purpose: ISSUE
priority: P2
deadline: -
requires_reply: false
attachments: []
references:
  - HANDBOOK.md
  - management/worklog/WORKLOG.md
---

## ISSUE：手册未写明"角色由谁、以何种运行时机制实际执行"

### 现象（含自责部分）
2026-09-26 首个真实需求中，本角色完成拆解与派工信后即停下等待，项目实际停滞；用户质询"未见 subagent 调用"后确认：**各角色是 AI 工作者，须由接活的会话以 subagent 方式逐个上岗执行，邮箱仅是留痕/证据层**——本角色此前误把"发出 TASK 信"当作"任务已被执行"。主责在本角色的执行模型错误，worklog #3 已如实记录。

### 手册缺口（建议，非裁断）
HANDBOOK.md 与各 role-limit 均未写明角色的**运行时执行机制**（谁上岗、以什么方式上岗、产物如何回流邮箱）。设计期默认"角色即文件夹"，首次真实运行才暴露该歧义。

### 建议
1. HANDBOOK 增补一节："每个角色的实际工作由主持会话（当前为与用户对话的 management 所在会话）以子代理方式执行；子代理必须先读该角色 role-limit 与相关邮件；一切结果以落盘产物为准，主持会话只采信落盘证据"；
2. 明确验收口径：**子代理的对话转述不构成证据，只有落盘文件（代码/报告/邮件/提交）构成证据**。

本 ISSUE 仅供你裁定，本角色不代改手册。
