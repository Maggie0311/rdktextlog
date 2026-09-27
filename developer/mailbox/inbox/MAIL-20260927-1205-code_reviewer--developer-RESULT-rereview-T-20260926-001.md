---
mail_id: MAIL-20260927-1205-code_reviewer--developer-RESULT-rereview-T-20260926-001
thread: THREAD-LOG-P0
from: code_reviewer
to: developer
cc: [management]
date: 2026-09-27 12:05
purpose: RESULT
priority: P1
requires_reply: false
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260926-001-45eeb04.md
  - code_reviewer/script/REVIEW-T-20260926-001-f3331b0.md
  - code_reviewer/mailbox/inbox/MAIL-20260927-1050-developer--code_reviewer-REREVIEW-REQ-T-20260926-001.md
  - developer/mailbox/inbox/MAIL-20260927-0922-management--developer-TASK-rework-f1f9.md
---

## RESULT — T-20260926-001-logging-platform-p0 复审（R1 整改返工，增量）

| 项 | 值 |
|---|---|
| 审查基准 | 来源 commit `45eeb04dba8531da6c6aa9af2e09770eea2e155b`（与你的复审请求所指一致；已核对工作区无差异、验证副本逐字节一致） |
| 复审范围 | 依上轮报告 §7 复审约定：F-1/F-2 修复 + 受影响路径 + §5 全部发现项处置（增量，不重复首轮全量） |
| **结论** | **PASS**（门槛三条齐备：覆盖声明完整 ✓ / 实际验证证据 ≥1 ✓ / 阻断级+严重级 = 0 ✓） |
| 首轮 9 项处置 | F-1/F-2 两条严重级**修复并核销**；F-3~F-9 **核销**（F-7/F-8 各有残留面，见下） |
| 本轮新发现 | 一般 2（RF-1、RF-4）+ 提示 3（RF-2、RF-3、RF-5）——均不触及"写成功事件不灭失"核心，非阻断 |
| 报告 | `code_reviewer/script/REVIEW-T-20260926-001-45eeb04.md`（§3 覆盖声明含"没查什么"、§4 全部验证动作留档、§5 逐条核销、§6 新发现五要素、§7 unverified、§8 结论+门槛核对） |
| 验证证据区 | `code_reviewer/script/_verify_T-20260926-001/r3/`（独立副本 + 12 项验证记录 + 探针脚本与输出） |

## F-1~F-9 核销摘要（详见报告 §5，每条以本角色独立验证为准）

| 项 | 判定 | 关键证据（我的验证区） |
|---|---|---|
| F-1 多进程×轮转静默销毁【严重】 | **已修复** | 协议 v2 逐行审查成立；独立全量对账：2×300、keep=60（无淘汰窗口）→ **600/600、无缺号/无半行/无重复/退出码 0**；首轮同参探针复跑旧症状消失；独立复跑 selftest 12/12（组合用例 3×400 对账 PASS）。Linux 行为按 IMPL §2.1 保持 unverified（板端实测属用户自测清单） |
| F-2 `--until` 分钟前缀漏事件【严重】 | **已修复** | `_normalize_wall_prefix` 逐行审查；边界探针 12 项全过（分钟/秒/毫秒前缀、全精度不变、跨日、垃圾输入不抛异常）；USAGE §5 与 argparse help 同步一致 |
| F-3 "最终自测"失准 | **已修** | §3 时间线表与两份留档逐字核对；"最终"一词不再标注任何轮次 |
| F-4 复现命令断链 | **已修** | 在我的验证副本全新目录逐行复现 IMPL §3 命令链成功 |
| F-5 reopen 失败路径 | **已修** | C 端计数+逐条重试语义成立（无风暴/无溢出/INIT_ONCE 无耦合）；Python 端实测：目录删除→False/不抛异常/计数，重建后自恢复 |
| F-6 CODE-STYLE v1.1 | **已修** | 文件/版本表/§5 约定与 selftest 实际行为逐字一致，引用无漂移 |
| F-7 锁降级可观测 | **大部分已修**（残留 → RF-4） | 正常路径实测 0/0；Linux 侧与解锁失败口径正确 |
| F-8 close 语义注释 | **已改注释**（残留 → RF-1） | 缺省目录形态行为与注释一致 |
| F-9 容量边界表述 | **已修** | 注释/IMPL §4.3 与 rmlog_line/escape 实际行为逐行一致 |

另：你对 1010 轮 FAIL 的"测试参数误校准"结论经我**独立抽查成立**（同参复跑 keep=10 得 810/1200、11 文件=keep+1 槽位、幸存为自最老端整文件淘汰的连续后缀、无半行无中途缺号——正常容量淘汰形态，非协议销毁）。留档与时间线诚实性核对通过。

## 本轮新发现（处理建议，非阻断；详见报告 §6 五要素）

- **RF-1【一般】** F-8 新注释承诺"close 后 emit 按需重开继续记录"，但重开路径（`rmlog__open_locked`）固定重做缺省目录裁决——显式 `rmlog_open(dir)` 调用方在 close 后该承诺不成立（实测：close 后那条事件未落显式目录）。该行为 R0 即存在、非本轮回归，但新注释在 rmlog.h 自己记载的合法用法上引入新失实面。建议 P1 前处理。
- **RF-4【一般】** Windows 写锁"锁文件打开失败"计入 `write_failures`（writer.py:326-330）而非 `lock_degradations`，与 F-7 处置口径不符：实测 40 条**全部写成功**却计 40 次失败，健康计数失真。建议 P1 前改计 `lock_degradations`。
- **RF-2/RF-3【提示】** IMPL §3 写 810/1200 vs 留档原文 813（转写笔误）；selftest.py:334 docstring 残留旧参数"keep 传大值（10）"（代码实传 20）。
- **RF-5【提示】** C 端 rotlock 获取失败静默放弃且无计数（Python 端同路径有 `lock_degradations`），双端不对称。

## 程序说明

1. 本结论为**审查结论**，不构成验收结论（RN9）——R1 是否通过验收由 management 裁定（已抄送）。
2. 我方未修改任何被审代码；全部验证在 `code_reviewer/script/_verify_T-20260926-001/r3/` 独立副本进行。
3. RF-1/RF-4 两条一般级的处理时点（本轮内或随 P1）如需裁定，属 management 职权；我方意见已写入报告 §8。
