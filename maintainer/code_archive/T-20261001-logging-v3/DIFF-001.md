# DIFF-001 — T-20261001-logging-v3（v2 → v3 差异）

本版是 `T-20261001-logging-v3` 首次归档，其**上一版**为 `T-20260930-005-logging-v2`（来源 commit `3148fed`，见该 task 的 VERSION/DIFF）。`git diff --stat 3148fed d77d36c -- developer/script` = **16 文件、+963 / -9**。v3 在 v2 之上"加层"，不重写 v1/v2 地基，保留 v2 的 `Writer.event` / `rmlog.event` / `AsyncWriter.emit` / 24 个字符串错误码。

## 新增能力（相对 v2）

| 路线图 | 新增 | 文件 |
|---|---|---|
| P0 黑匣子环形缓冲 + 错误快照 | 内存滚动窗口 + ERROR/FATAL 自动 JSONL 快照，`max_snapshots` 保留上限 | `rmlog/blackbox.py`（新增） |
| P0 崩溃遗言 | 信号钩子写遗言 + 恢复 SIG_DFL 重抛保留 core | `rmlog/crash.py`（新增） |
| P1 通信错误率 + 心跳看门狗 + dmesg 监听 | `CommStats` 滑动窗口、`HeartbeatWatchdog`、`DmesgMonitor`（可注入） | `rmlog/monitors.py`（新增） |
| P1 资源越限监控 | 温度/电压/内存越限映射既有码 | `rmlog/resources.py`（新增） |
| P0/P1 低打点运行时 | `LogRuntime` 统一 heartbeat/sample/emit 入口 | `rmlog/auto.py`（新增） |
| P2 双轨错误码 | 字符串码 + 24bit bit 码映射 | `rmlog/code_map.py`（新增） |
| P2 公共头文件 | Linux/STM32 共用 `shared/rmlog_schema.h`（生成物） | `shared/rmlog_schema.h`（新增）；`rmlog/gen_code.py` 增 `write_schema` + `RMLOG_BIT_*` 宏 |
| P2 统计 CLI | 读端 `stats` 子命令按码/级别统计频次 | `rmlog_read.py`（修改，+23） |
| P1 systemd 接线 | `sd_notify` + 心跳 + `WatchdogSec=2` | `rmlog/daemon.py`（修改，+48/-?）、`systemd/rmlog-demo.service`（+1 行 `WatchdogSec=2`） |
| 回归烟测 | v3 smoke 覆盖双轨/黑匣子/监控/统计/schema | `tests/test_v3_smoke.py`（新增） |

## 修改（相对 v2，非新增）

| 文件 | 变更 |
|---|---|
| `rmlog/gen_code.py` | +21/-?：新增 `write_schema()`（banner `rmlog_errors.h`→`rmlog_schema.h`、`RMLOG_ERRORS_H`→`RMLOG_SCHEMA_H` 替换，F-05）；每码增 `RMLOG_BIT_*` 宏 |
| `rmlog/rmlog_errors.h` | +25：生成物重生成，每码增 `RMLOG_BIT_*` 宏（24bit 码） |
| `rmlog/daemon.py` | +48/-?：`sd_notify` + 心跳循环 + `HeartbeatWatchdog` 接线 |
| `systemd/rmlog-demo.service` | +1：`WatchdogSec=2` |
| `rmlog_read.py` | +23：`stats` 子命令 |
| `rmlog/__init__.py` | +5/-?：导出 `encode_code`/`decode_code`/`hex_code` |
| `README.md` | +6：v3 能力说明 |

## 保持不变（相对 v2，零变更，回归兼容）

`rmlog/writer.py`、`rmlog/async_writer.py`、`rmlog/session.py`、`rmlog/checks.py`、`rmlog/format.py`、`rmlog/catalog.py`、`rmlog/rmlog.c`、`rmlog/rmlog.h` 等——`git diff --name-status` 不在增量内，24 错误码与 `Writer.event`/`rmlog.event`/`AsyncWriter.emit` 接口冻结未动（review 已核）。

## 归档差异

- 来源：`d77d36c8535cdcb55249e400b56205254e50d299`，逐字节复制（`git cat-file blob` 逐文件，54 文件）。
- 带注副本：11 个 v3 相关文件新增 maintainer 注释（+57/-0，仅注释行），未改 developer 源码/字符串/语句/宏/格式（KN3）。
- 归档策略：`shared/rmlog_schema.h` 与历史 selftest 日志一并入档（均为 d77d36c tracked 内容）；`.gitignore` 声明的构建产物（`__pycache__/`、`tests/_work/`）不在 tracked 内、不入档。
- 旧归档：既有 `T-20260926-001-logging-platform-p0`（v001/v002）与 `T-20260930-005-logging-v2`（v001/v002）零修改。

## 事实边界

review PASS（`REVIEW-T-20261001-logging-v3-d77d36c.md`）、tester 板端 `TESTREPORT-T-20261002-014-001.md`（BQ1~BQ5 全通过）、management `ACCEPT-20261002-logging-v3.md`（accepted）均以 `d77d36c` 对齐。systemd 实装重启、sd_notify 投递、断电/压力、真实硬件、1 kHz 硬实时、板端 core 放开均保持 `unverified`。本文件不作质量或发布裁定。
