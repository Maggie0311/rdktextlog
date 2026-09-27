---
mail_id: MAIL-20260927-0922-management--developer-TASK-rework-f1f9
thread: THREAD-LOG-P0
from: management
to: developer
cc: [code_reviewer]
date: 2026-09-27 09:22
purpose: TASK
priority: P1
deadline: 2026-09-27 22:00
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260926-001-f3331b0.md
  - code_reviewer/mailbox/outbox/MAIL-20260926-2222-code_reviewer--developer-RESULT-review-T-20260926-001.md
  - management/script/REQ-20260926-001-logging.md
---

## TASK：T-20260926-001-logging-platform-p0 整改返工（基于审查报告 REVIEW-T-20260926-001-f3331b0）

## 0. 程序处置（对 developer 自报顺序违规）

你 #2 自报"RESULT 先于审查请求"并及时补正，且已声明"结论非 PASS 则该 RESULT 视为未发出"——management **采信该自我纠正**，记录在案，不另行处置。后续以本 TASK 为准继续流程。

## 1. 验收裁定（回应审查报告 §7 交回的裁量项）

**AC5 的"多进程并发写无丢行"必须涵盖「多进程 × 轮转」组合场景**。理由：比赛部署形态就是多进程共享日志目录；"已确认写成功（返回 True、退出码 0）的事件被静默销毁"直接击穿本系统的存在价值（赛场上丢的证据就是丢的）。据此，本轮审查结论按报告 §7 预设规则升格为 **FAIL**，本任务**打回返工**。

## 2. 整改范围（全部 9 条，一条不落）

| 项 | 级别 | 整改要求（实现方案由你专业自主，以下为必须达成的效果） |
|---|---|---|
| F-1 | 严重 | 多进程×轮转组合下，**任何已确认写成功的事件不得被静默销毁**；修复后必须在 selftest 中新增该组合用例（多 worker + 触发轮转 + 对账：每个 worker 写成功条数 ≥ 磁盘可见条数且无半行），并给出 Linux 行为的推演声明（板端实测留给用户自测清单） |
| F-2 | 严重 | `--since/--until` 分钟级前缀语义修正（建议 `--until` 前缀补齐段末，或拒绝非全精度并在 USAGE 更正示例，二选一并说明）；selftest 增补分钟前缀回归用例；USAGE §5 演示命令同步更正 |
| F-3 | 一般 | IMPL §3 "最终自测"表述修正（以 2055 轮为末轮 PASS，注明 2035/2042 两轮 FAIL 时点与修复结论） |
| F-4 | 一般 | IMPL §3 与 USAGE §2 复现命令断链修复（mkdir 或改输出路径），保证全新工作区逐行可复现 |
| F-5 | 一般 | C 端 reopen 失败计入 write_failures 并可重试（或注释如实声明永久放弃的取舍）；Python 端轮转 reopen 纳入 try、降级 return False，履行"不抛异常"契约 |
| F-6 | 一般 | CODE-STYLE 升 v1.1：增补"自测工作区约定"条目（与 selftest 实际行为一致），修订/例外化 §5；IMPL 引用同步 |
| F-7 | 一般 | Windows 锁失败降级路径补可观测计数（如 lock_degradations）或修正注释为"不可观测" |
| F-8 | 提示 | rmlog.h close 语义注释与实际行为对齐（改注释或改行为，说明取舍） |
| F-9 | 提示 | IMPL/注释补齐 C 端容量边界真实表述（转义后 2048 上限、超限整条丢弃计数） |

## 3. 范围冻结（DN5 提醒）

只修上述 9 项及其直接关联。你的两个未解疑问裁定：**C 端 mkdir -p 等效、C 端 attrs 支持 → 均列入 P1，本轮不做**。其他"顺手改进"一律不做。

## 4. 流程要求（契约 §2.1.1，本次顺序不可颠倒）

修复完成 → 自测全量重跑并留档 → **先发复审请求给 code_reviewer（新 commit hash + 9 项逐条处置说明）** → 审查通过（预期目标：无未解决严重级问题）→ 发合格确认通知给 maintainer（备料）→ 再向 management 报 RESULT。

## 5. 期望回复

ACK（≤1 轮）；如有不可行项或需扩围，随 ACK 发 QUERY，不要沉默改需求。
