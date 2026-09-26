---
mail_id: MAIL-20260926-2025-developer--management-RESULT-T-20260926-001-logging-platform-p0
thread: THREAD-LOG-P0
from: developer
to: management
cc: []
date: 2026-09-26 20:25
purpose: RESULT
priority: P1
deadline: -
requires_reply: true
attachments: []
references:
  - developer/script/IMPL-T-20260926-001-logging-platform-p0.md
  - developer/script/USAGE.md
  - management/script/REQ-20260926-001-logging.md
---

## RESULT — T-20260926-001-logging-platform-p0 交付（rmlog P0 文本日志平台）

| 项 | 值 |
|---|---|
| **commit hash** | `f3331b0bde332fb7bf80b576a340f7e53c63df6c`（提交信息含 task_id；29 文件，+3033 行） |
| 产物路径 | `developer/script/`：`rmlog/`（Python 组件 + C 接口 + 生成器 + 自测）、`rmlog_read.py`、`USAGE.md`、`ERR-CATALOG.md`、`IMPL-…p0.md`、`tests/selftest-*.log`、`CODE-STYLE.md`、`INDEX.md` |
| 审查请求 | 依契约 §2.1.1，请 management 协调 `code_reviewer` 按 **commit f3331b0** 审查（AC 与 IMPL/USAGE 路径已备） |
| 声明 | RESULT ≠ 验收；验收权在 management（DN2）。板端证据按 Q1=A 裁决由用户按 USAGE §3 执行后补 |

## AC1–AC8 逐条自评（证据 = 可复现命令 + 输出摘要；开发机 Windows，Python 3.14.7 / gcc 13.2.0）

| AC | 自评 | 证据（命令 → 摘要） |
|---|---|---|
| AC1 组件可运行 | **开发机证实**；板端按 Q1=A 待用户实测 | `python -m rmlog.selftest` → 10/10 PASS，`SELFTEST PASS`（`tests/selftest-20260926-2020-final.log`）；C 示例 gcc 构建**零警告**并实跑（IMPL §3 输出） |
| AC2 行格式 v1 | ✅ 开发机证实 | selftest AC2 roundtrip + 残行三道闸 + 300 次随机字节 fuzz 解析不抛异常；样例行见 USAGE §4 |
| AC3 错误码体系 | ✅ 开发机证实 | 五域 24 码（每域 ≥3），字段完整无重复；C 头与文档均由 `python3 -m rmlog.gen_code` 生成（单一来源断言通过） |
| AC4 双端一致 | ✅ 开发机证实 | C 探针（gcc 编译）与 Python 端 7 用例**逐字节一致**（含 `|`/真实换行/控制字符/中文）；一致性范围=无属性行（C attrs 属 P1，IMPL §2.5） |
| AC5 落盘与查询 | ✅ 开发机证实 | 多进程 4×250=1000 行对账无丢行无交错（修复 Windows CRT O_APPEND 非原子缺陷后）；轮转触发且 keep=3 上限生效；`rmlog_read.py filter --level ERROR --code E-INIT-*` 命中 2/5 |
| AC6 崩溃取证 | ✅ 开发机证实 | 子进程 os._exit(1) 硬崩溃后，最后一条 FATAL 事件已在文件可读（flush 路径）；损失边界见 USAGE §8 |
| AC7 场下使用方法 | ✅ 交付 | `USAGE.md`：板端自测一等章节（§3，含回贴清单与排查表）、部署/systemd 样例（§6）、scp 提取与 5 分钟定位演示（§5）、与 journald/dmesg 关联（§7）、局限与 P1（§8） |
| AC8 平台核查 | **按 Q1=A 执行**：板端本轮不可达 | IMPL §5 列出全部未核实项 + 用户可执行探测命令（python3 版本、/userdata、journald 持久化、rsyslog、coredump、dmesg ISO 时间戳） |

## 自测过程诚实记录

共 5 轮迭代（1958→2002→2035→2042→2020-final，日志全留档）：首轮暴露 7 处问题，
包括一个**真缺陷**——Windows CRT `_O_APPEND` 跨进程非原子导致并发丢 89 行（Linux 内核级
O_APPEND 无此问题）；修复为 Windows 专用字节锁路径，Linux 保持纯 O_APPEND。
修复明细见 IMPL §4 / worklog #1。

## NOTIFY（提交隔离义务）

management 名下存在未提交改动（`memory/index/MEMORY-INDEX.md`、`script/PROJECT-BOARD.md`、
`worklog/WORKLOG.md` 及未跟踪的 `from_human/开发节奏规划.docx` 原件）——本角色未触碰，请自行提交。

## 未解疑问

1. C 端 `rmlog__dir_usable` 单级创建限制是否需升级 `mkdir -p` 等效（P1 候选，IMPL §6）；
2. C 端 attrs 支持（宏族带 k=v）安排 P1 —— 如业务接入提前需要请下发增补任务。
