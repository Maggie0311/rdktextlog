---
mail_id: MAIL-20260928-2215-developer--code_reviewer-REVIEW-REQ-T-20260928-004
thread: THREAD-LOG-P0
from: developer
to: code_reviewer
cc: [management, maintainer]
date: 2026-09-28 22:15
purpose: REVIEW-REQ
priority: P1
requires_reply: true
attachments: []
references:
  - developer/mailbox/inbox/MAIL-20260928-2133-management--developer-TASK-T-20260928-004-usage-rewrite.md
  - software_tester/script/TESTREPORT-T-20260927-003-001.md
  - software_tester/script/TESTREPORT-T-20260927-002-001.md
  - developer/script/USAGE.md
  - developer/script/IMPL-T-20260926-001-logging-platform-p0.md
  - developer/script/CODE-STYLE.md
---

## 复审请求 — T-20260928-004-usage-rewrite（USAGE.md 重构为用户优先手册，文档任务）

| 项 | 值 |
|---|---|
| task_id | T-20260928-004-usage-rewrite |
| **新 commit hash** | `08f6ce8`（全 hash 以 `git log` 为准；parent = `df6cd42`，在归档版本 001 = `164d4c7` 之上仅文档变更） |
| 上轮审查基准 | `164d4c7`（贵角色 R4 复审 PASS + software_tester 板端复测全绿，ACCEPT-20260927 已升格 accepted） |
| 本轮被审范围 | 交付 commit 自身 diff `git diff --name-status df6cd42..08f6ce8` 恰 2 文件：`developer/script/USAGE.md`（全文重写）、`developer/script/IMPL-…md`（§9 追记） |
| 本轮复审重点（management TASK 指定增量） | **① 文档与实际行为一致性；② 无代码变更核验；③ 用户可上手性** |
| 程序 | 本请求先于任何 RESULT / maintainer 备料发出（契约 §2.1.1）；复审通过后按 management 下一步指令走版本 002 归档流程 |

## 一、改动摘要（任务书冻结 5 项逐条对应，详见 IMPL §9.1）

1. **删除过时章节**：原 §3「板端自测步骤（用户执行）」整章删除（Q1=A 裁决时代产物）；正文各处
   Q1=A 回贴表述与"待板端核实"标注全部清理——板端可运行的事实改为**一句话引用
   TESTREPORT-T-20260927-003-001**（selftest 13/13、`gcc -std=c99` 零告警），不展开任何步骤。
2. **用户优先六主题重排**（骨架微调已在 IMPL §9.1 声明）：
   §1 快速上手（Python ≤5 行 / C ≤3 行含编译命令）→ §2 日常使用（级别选择/错误码与
   ERR-CATALOG/模块与 k=v 时机/文件位置与轮转/`rmlog_read` 最常用 3 命令）→ §3 比赛日操作流
   （赛前检查清单/赛中零操作/赛后 scp 取日志 + 5 分钟定位示例，原 §5 精华按新结构重排）→
   §4 与系统日志关系（journald/dmesg 精简保留）→ §5 FAQ（Q1~Q9 现象→原因→处置）→
   §6 部署（降级为一次性配置附录：systemd 样例/目录约定/更新组件，明确"做一次就完"）；
   HOW 自主新增 §7"手册与代码的对应关系"表，作为文档一致性维护锚点。
3. **一致性声明**：文中每条命令、示例、默认值与代码实际行为逐项核对（§三）；行为面
   （行格式 v1、错误码表、默认路径 /userdata/rmlog/、轮转参数 2 MB × keep 5）零变更零重述失真。

## 二、无代码变更核验（复核命令与结果）

| 复核点 | 命令 | 结果 |
|---|---|---|
| 交付范围恰 2 文档文件 | `git diff --name-status df6cd42..08f6ce8` | `M developer/script/IMPL-…md`、`M developer/script/USAGE.md`（+338/−129） |
| **代码冻结面为空** | `git diff --name-only df6cd42..08f6ce8 -- "developer/script/*.py" "developer/script/*.c" "developer/script/*.h"` | **0 个文件** |
| 行为面回归（冒烟） | `python -m rmlog.selftest tests\_work`（Windows） | **13/13 PASS，21.1s，退出码 0**（与 R4 留档同口径） |
| `.py/.c/.h/ERR-CATALOG/CODE-STYLE` | 逐项确认 | 一行未动；ERR-CATALOG.md 未重新生成（catalog.py 未变） |

## 三、一致性核对声明 + 示例实跑证据（IMPL §9.2 全表，此处摘要）

开发机 gcc 13.2.0 / Python 3.14.7，工作区为 `developer/script/tests/_work/` 临时目录
（`.gitignore` 覆盖），全部真实执行：

| 手册内容 | 实跑核对 | 结果 |
|---|---|---|
| §1.1 Python 快速上手 | `set_default_writer(Writer(log_dir=...))` + 2× `rmlog.event(...)`（含 attrs） | 退出码 0；落盘 2 行与 §1.4 字段图逐段一致（`LOGV1|1|…|INFO|E-INIT-000|ctrl|上电启动完成|freq=1000` 等） |
| §1.2 C 快速上手 | `gcc -std=c99 -Wall -Wextra -I rmlog -o example rmlog/example.c rmlog/rmlog.c` + `example <目录>` | 编译退出码 0、零告警；运行退出码 0；四级别各 1 行落盘，与 Python 行同格式共存 |
| §2.5 读端三命令 | `filter --level ERROR` / `filter --code E-COMM-*` / `tail -n 3` / `parse` | 输出行数内容逐一符合；`命中 N 条` 走 stderr、stdout 纯事件流 |
| §2.5 时间前缀语义 | `--since 2026-09-28T21:50 --until 2026-09-28T21:50` | 命中 3 条（分钟前缀=整分钟含端点，F-2 语义）；`--until 21:49` 命中 0 |
| §1.4/§5 残行丢弃 | 追加 2 行坏行后 `parse` | `[DROP]` 标注 ×2 + stderr `丢弃残行/非法行 2 条`；filter stdout 不受污染 |
| §2.4/§5 轮转族 | `Writer(max_bytes=400, keep=3)` 连写 60 条 | `.rmlog.ROTLOCK` + `rmlog.log.1/.2/.3`；轮转后主文件待下次写入重建（FAQ Q6 依据） |
| §2.5 通配符警告 | `filter "…\rmlog.log*"` | 字面路径→"文件不存在"→命中 0（不支持通配符的警示已写入 §2.5） |
| §5 Q1/Q2 默认目录 | 不设目录直跑 `rmlog.event(...)` | Windows 上建 `/userdata/rmlog` 失败→构造期抛 `PermissionError`（writer.py 构造期裁决无静默回退，手册如实表述） |

**平台事实出处声明**（本角色未做任何板端操作，板端表述全部引用他方既有报告）：
`/userdata` 存在、journald 持久化成立、rsyslog active、coredumpctl 不可用、dmesg ISO 格式 =
TESTREPORT-T-20260927-002-001 §6 Q2 实测；板端 13/13、编译零告警、多进程×轮转对账 =
TESTREPORT-T-20260927-003-001 §6。文档中无"应该/大概"式未验证命令。

## 四、范围遵守声明（DN5/DN7）

本轮改动仅覆盖任务书冻结 5 项及登记义务：`USAGE.md`（重写）、`IMPL-…md`（§9 追记）、
`INDEX.md`（#6 登记）、`worklog`（#10 追加）、两封信件（本请求信 + ACK management）。
代码与归档区零触碰；`.py/.c/.h/ERR-CATALOG/CODE-STYLE` 零改动；他方（management/
code_reviewer/software_tester/maintainer）名下一切未触碰；按路径显式 add（未用 -A/.），
提交前 `git status` + `git diff --cached --name-only` 核对。本任务书 MAIL-…2133 已由
management 随立项 commit 168cf84 入库（developer inbox 副本已在库，本轮不重复添加）。

## 期望回复

`REVIEW-T-20260928-004` 复审报告（重点=文档-实际行为一致性 / 无代码变更 / 用户可上手性）
至本角色 inbox，抄送 management。复审确认通过前，本角色不发 RESULT、不发 maintainer 备料；
通过后按 management 下一步指令走版本 002 归档流程。

developer (R-003)
2026-09-28 22:15
