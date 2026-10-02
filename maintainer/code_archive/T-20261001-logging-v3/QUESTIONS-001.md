# QUESTIONS-001 — T-20261001-logging-v3

读这份代码前，先弄懂下面这些问题（行号为来源 commit `d77d36c` 行号）。

1. 黑匣子为什么"正常不落盘、出错才落盘"？内存窗口的容量与快照文件保留上限分别由谁控制？（`blackbox.py` 的 `capacity` 与 `max_snapshots`；`max_snapshots=0` 语义是什么？）
2. `snapshot` 为什么用 `mkstemp` + `fsync` + `os.replace`，而不是直接 `open(final)` 写？（原子落名、崩溃不留半文件，`blackbox.py:105-115`）
3. 崩溃遗言 handler 为什么**不在**信号上下文里做格式化/分配？（`crash.py:35-36` 安装期预格式化；handler 只 `os.write`）
4. handler 写完遗言后为何要 `signal.signal(SIG_DFL)` + `os.kill` 重抛，而不是 `os._exit`？（保留内核 core dump；`crash.py:44-48`）
5. `CommStats` 怎么区分"链路真断"与"分散失败/短时突发"？`E-COMM-004` 与 `E-COMM-003` 各自的触发条件？（`monitors.py:37-45`）
6. `HeartbeatWatchdog`（应用层）与 systemd `WatchdogSec`（系统层）是同一件事吗？各兜底什么？（`monitors.py:53`、`daemon.py:59-61`、`systemd/rmlog-demo.service:7`）
7. `DmesgMonitor` 的 stop 与启动之间的竞态是怎么闭合的？（锁内登记 `_proc` + `stop_during_start`，`monitors.py:117-122`）
8. `ResourceMonitor` 读不到电压（RDK X5 无 `BAT0`）时会发生什么——报错还是跳过？（按设计跳过，`resources.py:35-37`；这是否等于"电压监控已覆盖"？答案：否，unverified）
9. 字符串错误码与 24bit bit 码是什么关系？`0x223004` 是怎么从 `E-COMM-004` 算出来的？（`code_map.py:10-21`）
10. `shared/rmlog_schema.h` 为什么是"生成物、勿手改"？改了 catalog.py 之后要做什么？（`gen_code.py:140-149`、文件头 banner）
11. daemon 的 `sd_notify` 在无 `NOTIFY_SOCKET` 时做了什么？这能证明 `READY=1`/`WATCHDOG=1` 已送达 systemd 吗？（静默返回 False；不能证明，`daemon.py:19-34`）
12. `LogRuntime.emit` 在写 ERROR/FATAL 后自动做了什么？失败时如何留痕？（`auto.py:56-66`）
13. `rmlog_read.py stats` 统计的是什么？它和 `filter` 各解决哪类场下问题？（`rmlog_read.py:239-254`、`:273`）
14. 板端 BQ1~BQ5 全通过，是否等于 systemd 实装重启 / 断电 / 真实硬件 / 1 kHz 硬实时 / core dump 已全部验证？（答案：不是，见 TESTREPORT §7 未做项与 SPEC §10）
