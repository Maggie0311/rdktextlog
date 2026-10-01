# SPEC-001 — T-20260930-005-logging-v2（来源 `3148fed`）

## 1. 一句话定位

这是一套面向开发机的业务日志 v2：用有界异步队列、会话标识、五域事实注入、轮转导出和持续 daemon，把事件可靠写出并可按 session 查询。

## 2. 结构总览

| 区域 | 职责 |
|---|---|
| `rmlog/async_writer.py` | 有界入队、后台落盘、flush/close |
| `rmlog/writer.py`、`format.py` | 事件编码、追加、轮转与解析 |
| `rmlog/session.py`、`checks.py`、`fault_demo.py` | 会话与五域业务事实适配/演示 |
| `rmlog/daemon.py`、`systemd/rmlog-demo.service` | 持续运行入口与服务模板 |
| `export_evidence.py`、`rmlog_read.py` | 主/轮转日志导出与查询 |
| `tests/test_v2_smoke.py`、`rmlog/selftest.py` | v2 smoke 与既有 13 项回归 |
| `rmlog/*.c`、`rmlog/*.h` | C 端协议与探针配套 |

## 3. 各模块功能（事实）

- `AsyncWriter`（`rmlog/async_writer.py:20`）：控制线程入队，后台 worker 写入；队列满返回拒绝，`flush` 等待 task completion。
- `Writer`（`rmlog/writer.py:180`）：编码后追加，轮转锁内按实际大小裁决；`event` 在 `rmlog/writer.py:500`。
- 五域适配（`rmlog/checks.py:1`、`fault_demo.py:20`）：记录业务提供的 INIT/COMM/HW/FSM/SYS 事实，不自动诊断硬件。
- 导出（`export_evidence.py:70`）：枚举主文件及连续 `.1...`，生成 manifest；查询（`rmlog_read.py:35`）按行解析并过滤。
- daemon（`rmlog/daemon.py:20`）：启动/停止会话事件并响应 SIGTERM。

## 4. 关键流程

1. `session.py` 生成会话标识；调用方经 `AsyncWriter.emit` 入队。
2. 后台 worker 调 `writer.event`，`format.encode` 形成一条完整行后落盘。
3. 超限时 `writer` 获取 ROTLOCK，锁内检查真实大小并执行副本链轮转。
4. `export_evidence.py` 跨主文件与轮转副本导出；`rmlog_read.py filter --session` 查询。
5. daemon 收到 TERM 后 flush/close 并记录停止事件。

## 5. 数据流与关键状态

队列持有待处理事件；`unfinished_tasks` 代表尚未完成的落盘任务；writer 维护 seq、成功/丢弃/失败计数和当前文件大小估计；session 字符串贯穿事件与导出筛选。事实：容量为正整数，队列满时事件被显式 drop。

## 6. 依赖与外部接口

仅使用 Python 标准库；Linux 路径依赖文件、fcntl、signal 和可选 journal/dmesg 命令。C 端依赖 POSIX/Windows 对应系统 API。systemd 模板要求 `/opt/rdk_x5_software/developer/script` 和 Python 入口存在。

## 7. 构建与运行方式

在 `developer/script`（来源副本同于本版 `code/`）执行 `python3 -m rmlog.selftest`（13/13 PASS）和 `python3 tests/test_v2_smoke.py`（PASS）。daemon 可用 `python3 -m rmlog.daemon <dir>` 启动并以 SIGTERM 结束。上述命令与结果由 HANDOFF、review 与 tester 报告共同记录。

## 8. 术语表

见 `maintainer/script/GLOSSARY.md`；本版增补：bounded queue（有界队列）、session（跨文件事件会话标识）、manifest（逐来源导出清单）。

## 9. 已知关注点（只转述，不作质量裁定）

review PASS 报告称本版无新发现项；tester 报告明确未覆盖 X5 aarch64、板端 systemd 安装/重启、断电持久性、1 kHz 硬实时及真实 SPI/CAN/传感器接入。management ACCEPT 为“accepted（开发机范围）”。

## 10. 未解疑问（unverified）

- `unverified`：目标板 systemd 权限、失败重启与 aarch64 编译/运行结果，本归档没有目标板证据。
- `unverified`：真实硬件/通信故障是否能提供与演示适配器同形态的业务事实。
- `unverified`：断电持久性、长跑容量和硬实时延迟边界。

## 11. 事实层与推断层

本文带“事实”或引用报告的内容均可由来源代码/报告定位；“推断”仅指第 1 节对整体用途的概括，不能替代验收或质量结论。本文不宣称发布、整车交付或硬实时保证。
