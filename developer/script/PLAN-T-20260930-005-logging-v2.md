# T-20260930-005 第二版差距分析与实施计划（开发摘要）

## 基线与约束

- 第一版基线：`developer/script/`，LOGV1 行格式、五域错误码、C/Python 编码器、轮转写入器、读端和 13 项回归均已存在；旧归档与人类原件只读。
- 当前工作树存在大量既有未提交改动。此计划先于业务代码修改提交；待 framework_admin 明确基线/提交隔离后再编码。
- 当前可确认的历史事实仅用于差距分析；新版测试必须绑定新版 commit，不能把历史板端结果冒充新版实测。

## 第一版与 AC 差距

| AC | 第一版已有 | 主要缺口 | 第二版拟补齐 |
|---|---|---|---|
| AC1 | LOGV1、错误码目录、Python/C 双端实现、基础 Linux 复用说明 | 缺少集中式 v1→v2 差距矩阵、官方地瓜/Linux/systemd 证据索引及模块边界 | 在实现说明和使用手册中逐项引用官方资料，明确系统层复用、平台包装、业务接入责任 |
| AC2 | INIT/COMM/HW/FSM/SYS 共 24 码；基础写入与自测 | 自动检测/注入路径不完整，业务接口容易被误解为“库能自动识别硬件” | 增加可运行 fault demo/检测适配接口：初始化失败、通信中断、硬件阈值、FSM 超时、系统错误；明确 SPI/CAN/传感器/状态机由业务回调提供事实 |
| AC3 | 手动启动、轮转、ERROR/FATAL flush、systemd 使用示例 | 缺少可安装服务模板、异常退出/重启记录、会话 ID、风暴抑制/容量边界/日志自身健康出口的一体化实现 | 增加安装单元/启动包装器、session/run 标识、systemd Restart/StartLimit 说明；限速/摘要/丢弃计数；日志失败生成可观察 SYS 事件并保留健康快照 |
| AC4 | C/Python 接入，LOGV1 兼容，文件写入 | 无明确 1kHz 非阻塞接入边界、队列溢出可测计数，现有同步写入不适合控制线程 | 新增异步非实时 writer/有界队列 API；控制线程只做定长入队，定义满队列 drop 级别/计数；保留 `event()` 旧接口；不宣称硬实时，提供测量脚本 |
| AC5 | 按级别/错误码/时间过滤，tail/parse；已有 journald/dmesg 说明 | 无 session 过滤、一键导出业务+systemd+journal+dmesg+版本，缺失命令/权限时可能不完整 | 扩展读端 session 过滤与导出命令；每个证据源记录状态、缺失原因和权限；业务日志始终先导出，不伪造成功 |
| AC6 | 历史 13 项回归 | 新路径未覆盖异常退出、FSM timeout、COMM interruption、容量/风暴/队列、导出降级；缺少新版 commit 绑定报告 | 保留并重跑 13 项，新增故障注入与导出降级测试；所有输出写入 `developer/script/tests/`，注明 Windows/Linux 当前环境，板端/断电列待验 |
| AC7 | 有基础 USAGE | 缺少面向 MCU 成员的阶段化迁移、升级/回退/比赛日演练脚本 | 重写/增补手册与可执行 demo，按 catalog→同步 API→异步队列→systemd→导出定位分阶段说明 |
| AC8 | 历史已审查流程 | 新版尚未独立审查，且必须同一 commit 汇聚开发/测试证据 | 每轮先 code_reviewer；通过后 HANDOFF maintainer，再 RESULT management；所有证据固定候选 commit |

## 模块化实施顺序

1. **兼容基座**：复制/扩展现有 `rmlog`，保留 LOGV1、错误码和 `event()`/C 宏；新增 v2 版本元数据、session/run 字段以兼容方式编码（默认不破坏旧解析）。
2. **业务故障适配层**：提供 `checks.py`/fault demo，定义检测接口协议（返回事实→映射 catalog→记录），内置五类注入演示；不读取不存在的真实 SPI/电机协议。
3. **异步接入层**：有界队列、后台落盘线程、drop/overflow/worker-failure 健康计数；同步旧接口继续可用；C 端给出非实时线程接入示例和 1kHz 边界文档。
4. **会话与无人值守运行**：session manager、启动/退出/异常标记、systemd service/install/uninstall 脚本；systemd/journald 负责进程生命周期和系统日志，rmlog 负责业务语义。
5. **查询与导出**：扩展 `rmlog_read.py` 的 session/code/level/time 过滤；新增 export 脚本，逐项执行 journalctl/dmesg/uname/version，记录命令缺失/权限不足，保证业务日志导出不被可选项阻塞。
6. **测试与文档**：13 项旧回归 + 新故障注入、风暴、队列、异常退出、导出降级；实现说明列事实/推断/待验；手册给出部署、回退、比赛日、场下定位流程。

## 风险与边界

- 未取得 X5 板端环境前，Linux/systemd/journald/PREEMPT-RT 行为按文档和本机可复现实验分别标注；不宣称硬实时或断电零丢失。
- systemd、journalctl、dmesg、coredump 等可选能力按探测结果报告；任何命令失败都不能覆盖业务日志或伪造完整导出。
- 真实 SPI/CAN/电机/状态机逻辑不在输入源码中，故只交付适配接口和注入演示；真实接线验证列待验。
