---
mail_id: MAIL-20260928-2133-management--developer-TASK-T-20260928-004-usage-rewrite
thread: THREAD-LOG-P0
from: management
to: developer
cc: [maintainer, code_reviewer]
date: 2026-09-28 21:33
purpose: TASK
priority: P1
deadline: 2026-09-29 12:00
requires_reply: true
attachments: []
references:
  - maintainer/code_archive/T-20260926-001-logging-platform-p0/SPEC-001.md
  - developer/script/USAGE.md
  - management/script/ACCEPT-20260927-logging-p0.md
---

## 1. 背景 (Context)

人类用户审查归档产物后提出两条意见（2026-09-28）：
1. **USAGE.md 视角错位**：现有文档按"开发者视角的部署+验证流程"组织，缺少"用户如何快速上手使用日志功能"的主线——用户要的是：怎么在几行代码里记出第一条日志、比赛日怎么操作、错误码怎么打怎么查；
2. **「板端自测步骤（用户执行）」章节已过时**：该章节是 Q1=A 裁决时代（用户板端自测回贴）的产物；Q1 已修订为 B 且 software_tester 真机实测全绿，继续保留会误导用户以为还要自己做板端自测。

架构管理员明确：**归档版本 001 不可改，文档问题走新任务产出新版本归档**（framework_admin 裁决）。

## 2. 目的 (Objective)

重构 `USAGE.md` 为**用户优先**的使用手册，删除过时的板端自测章节，产出新版本（164d4c7 之上仅文档变更）并归档为版本 002。

## 3. 范围（冻结）

1. **删除**：USAGE.md 中「板端自测步骤（用户执行）」章节及相关引用（IMPL 中对应描述同步注明已移除及缘由）；
2. **重构 USAGE.md 结构（用户优先，建议骨架，HOW 你自主）**：
   - **§1 快速上手**：3 分钟记出第一条日志——Python 端 5 行以内示例、C 端 3 行以内示例（含编译命令），直接可复制运行；
   - **§2 日常使用**：如何打日志（级别选择建议、错误码怎么选怎么查 ERR-CATALOG、模块命名建议、k=v 属性什么时候用）、日志文件在哪、怎么看（rmlog_read 常用三条命令）；
   - **§3 比赛日操作流**：赛前检查（磁盘空间/组件自启确认）、赛中（什么都不用做——自动记录）、赛后取日志（scp 命令）+ 快速定位示例（保留现有 §5 精华）；
   - **§4 与系统日志的关系**：精简保留 journald/dmesg 关联查法（这是比赛排障时真有用的）；
   - **§5 部署**（从"主内容"降级为"一次性配置"附录）：systemd 样例、目录约定——压缩篇幅，面向做一次就不用再管的人；
   - **§6 FAQ 与故障排查**：从历史问题提炼（如文件没生成/没权限/磁盘满/时间戳不对怎么排查）；
3. **一致性**：文档命令必须与实际行为一致（行格式、错误码、路径默认值 /userdata/rmlog/ 等），示例代码真实可跑；
4. **IMPL 追记**：本任务缘由（用户审查意见）、改动清单；
5. **不做**：任何代码行为变更（.py/.c/.h 一行不动）；ERR-CATALOG/IMPL 主体不动；不改行格式与错误码（AC 冻结面）。

## 4. 流程

修复 → 新 commit → **先发复审请求给 code_reviewer**（增量：文档与实际行为一致性 + 无代码变更核验）→ 通过后向 maintainer 发 HANDOFF（新版本备料）→ 向 management 报 RESULT。

## 5. 期望回复

ACK ≤1 轮；对骨架有异议或发现用户视角缺失的其他点，随 ACK 提出。
