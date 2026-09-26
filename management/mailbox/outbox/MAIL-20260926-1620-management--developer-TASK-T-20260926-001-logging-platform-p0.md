---
mail_id: MAIL-20260926-1620-management--developer-TASK-T-20260926-001-logging-platform-p0
thread: THREAD-LOG-P0
from: management
to: developer
cc: []
date: 2026-09-26 16:20
purpose: TASK
priority: P1
deadline: 2026-09-27 23:59
requires_reply: true
attachments: []
references:
  - management/script/REQ-20260926-001-logging.md
  - management/from_human/开发节奏规划.docx
---

## 1. 背景 (Context)

人类用户（RoboMaster 电控组）下达赛季需求：在 RDK X5（Ubuntu 22.04，8×A55，已打 PREEMPT-RT 实时内核补丁）上建设**文本日志系统**，用于比赛场景自动记录运行信息与错误，场下凭日志快速定位问题，替代依赖 Keil 在线调试的传统方式。完整需求拆解、平台日志设施盘点、分阶段思路与 AC 见需求拆解书：

- **`management/script/REQ-20260926-001-logging.md`（必读，本任务的 AC 与边界唯一来源）**
- 团队节奏一手依据：`management/from_human/开发节奏规划.docx`（只读；本任务对应其阶段一"实现基础的文本日志系统"）

## 2. 目的 (Objective)

按 REQ §4 阶段 P0 的 P0-a~f，交付**可运行的初步文本日志平台（rmlog，C/Python 双端）+ 场下使用方法（USAGE.md）**。

## 3. 请求 / 交付物 (Request & Deliverable)

**task_id：`T-20260926-001-logging-platform-p0`**（唯一主责：developer）

交付物（全部落 `developer/script/`，产物区结构见你目录的 README）：

1. `rmlog/` 组件（**Python3 标准库实现，零第三方依赖**）：事件写入 API（含时间戳/级别/错误码/模块/消息/k=v 属性）、单文件多进程安全追加、按大小轮转；
2. C 侧接口（`.h/.c`，供后续 X5 上的 C/C++ 电控程序链接）：宏族 `RMLOG_I/W/E/F(mod, code, fmt, ...)`，与 Python 端**同源错误码、同构行格式**；
3. `ERR-CATALOG.md` 错误码表：INIT/COMM/HW/FSM/SYS 五域（REQ §4 P0-a），每码含编号/默认级别/含义/建议动作；C 与 Python 常量**同源**（单一来源，防止两端漂移）；
4. `rmlog_read.py` 读端：parse / tail / filter（`--level` `--code` `--since` `--until`）；
5. 自测：`python3 -m rmlog.selftest` 覆盖 REQ **AC1–AC6** 全部可自测项（双端格式一致性对照、并发写、轮转、崩溃取证模拟、残行丢弃）；
6. `USAGE.md` 场下使用方法（REQ **AC7**：部署到 X5、systemd 自启样例、WiFi 提取、5 分钟定位示例、局限与 P1 展望）；
7. `IMPL-T-20260926-001-logging-platform-p0.md` 实现说明：改动清单 / 关键决策与理由 / 验证方式与输出 / 已知风险与未覆盖项（含 REQ **AC8** 平台核查项的标注——板端本轮可能不可达，不可核实项如实标注"未核实"，禁止假设填充）。

## 4. 约束与边界 (Constraints)

- **WHAT**：只做 P0 范围（REQ §4 P0-a~f + §6 AC1–AC8）。**不做**：systemd 实机安装、看门狗心跳、快照打包、与 SPI/节拍线程对接（属 P1，另行建任务）；不引入 TROS/ROS 依赖；不绑定 root 权限假设（部署路径与身份做成可配置，见 REQ §7 Q2）。
- **HOW**：实现方式（语言内部结构、锁策略、文件布局细节）由你专业自主；但**行格式 v1 与错误码分域须符合 REQ §4 P0-a/P0-b 的约定**（它们是跨端与读端工具的接口，属 WHAT）。
- 平台事实（已由 management 从官方手册核实）：RDK X5 系统为 **Ubuntu 22.04**；实时内核经 `/boot/boot.cmd` 切换 `Image-rt`（PREEMPT-RT patch-6.1.83-rt28，社区衍生分支，官方明示稳定性需自行评估）——因此"进程崩溃/断电后日志可取证"是硬需求而非锦上添花。
- 技术判断如有异议：按你的契约 D9/D12/§5 发 ISSUE 或 QUERY 给我，不要沉默执行也不要猜（DN12）。
- **顺序（契约强制）**：交付前先请 `code_reviewer` 审查 → 通过后向 `maintainer` 发合格确认通知（备料）→ 再向我报 RESULT。
- 部署目标环境（写进 USAGE 的假设前提）：板端 Python3 版本与持久分区路径需在 USAGE 中标注"待板端核实"或给出探测命令，**不得**写成已验证事实（AC8 的诚实要求同样约束文档）。

## 5. 验收标准 (Acceptance Criteria)

REQ §6 **AC1–AC8 全部适用**，逐条给"可复现命令 + 输出摘要"。其中 AC8 允许按两种形态交付（板端可达=核实记录；不可达=明确标注"未核实项清单"+ 给出用户可自行执行的探测命令清单）。

## 6. 期望回复 (Expected Reply)

1. **`ACK`（≤1 轮）**：确认接单；对 WHAT/AC 有异议或需求疑点，在 ACK 中附 QUERY，不要猜着写；
2. 交付时：`RESULT`（附 commit hash / 产物路径 / 自测输出摘要 / IMPL 与审查报告路径）。

## 7. 备注 (Notes)

- 本项目为该协作框架**首次真实交付**：审查门（code_reviewer）与 RESULT 顺序是框架级强制（你的契约 §2.1.1/§2.1.5），不是形式。
- 技术背景补充（management 已核实的一手资料，供你设计参考，不构成 HOW 指令）：
  - 官方手册入口：`https://developer.d-robotics.cc/rdk_x_doc/RDK?v=3.5.0&p=RDK+X5`
  - 实时内核章节：`https://developer.d-robotics.cc/rdk_x_doc/Advanced_development/linux_development/realtime_kernel`
  - 平台自带日志设施盘点与"直接用/包装用/自建"裁定：REQ §3（你的自建边界以该表为准——journald/dmesg/coredump 是系统层，rmlog 是业务层，两者通过时间戳关联，不重复造系统日志）。
