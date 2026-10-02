---
mail_id: MAIL-20261002-1552-software_tester--management-RESULT-T-20261002-014
thread: THREAD-LOG-V3
from: software_tester
to: management
cc: [code_reviewer, developer]
date: 2026-10-02 15:52
purpose: RESULT
priority: P1
deadline: 2026-10-02 23:59
requires_reply: false
attachments: []
references:
  - MAIL-20261002-1540-management--software_tester-TASK-T-20261002-014-logging-v3-boardtest
  - software_tester/script/TESTREPORT-T-20261002-014-001.md
  - software_tester/script/ENVIRONMENTS.md
---

## RESULT — T-20261002-014-logging-v3-boardtest

### 被测对象

commit `d77d36c8535cdcb55249e400b56205254e50d299`（`feature/logging-v3` tip）。副本经 `git archive d77d36c developer/script` 生成，上传到板端 `/tmp/rmlog-v3-test/`，9 个关键文件 md5 与本地全 MATCH。

### 环境（均实测，标记已验证）

RDK X5 V1.0（aarch64），Ubuntu 22.04.5 LTS，kernel `6.1.83-rt28`，Python 3.10.12，gcc 11.2.0。连接 `2409:893d:5126:4ac:fd6a:39a3:6650:3cc8`（DNS AAAA 首条，与任务书已知地址一致，paramiko root/root 成功）。全程仅在板端 `/tmp` 下活动，未碰系统配置、未装 systemd 服务、未改 /etc、未改源码。

### BQ1~BQ5 逐项结论（原始输出全文见报告 §5 与 raw/）

1. **BQ1 selftest**：退出码 `0`，`自测结束: 13/13 通过`、`SELFTEST PASS`。关键行：`AC4 双端 7 个用例逐字节一致`、`AC5×F-1 …写成功=1200 可见=1200…无半行/无全灭/无缺号`、`RF6 …delta=0 …lines=600/600`。
2. **BQ2 双 smoke**：v2 退出码 `0` `V2 SMOKE PASS accepted=1 dropped=9`；v3 退出码 `0` `V3 SMOKE PASS bit-map blackbox monitors stats schema`（并生成 rmlog_errors.h / rmlog_schema.h）。
3. **BQ3 监控层真实数据源**：退出码 `0`。ResourceMonitor 读真实 sysfs/procfs：`temp_mdeg=52523`（≈52.5°C）、`memory_available_kb=6928060`、`write_failures=0`；`voltage_mv` 因板端无 `/sys/class/power_supply/BAT0`（该目录为空）按设计跳过。DmesgMonitor 用真实 `dmesg --follow` 读内核环形缓冲并映射出 98 行事件（E-COMM-002/E-HW-003，每条 ERROR 自动触发黑匣子快照），stop 后子进程线程正常退出。
4. **BQ4 core 配置（只读）**：`ulimit -c`=`0`（core dump 已禁用）、`core_pattern`=`core`、`core_uses_pid`=`1`。
5. **BQ5 daemon 心跳+收尾**：daemon PID 3416 起 3 秒仍存活（心跳循环运行）→ SIGTERM 后 `DAEMON_EXIT=0` 优雅收尾；rmlog.log 含 `E-INIT-000 logging service started`（git=unknown）与 `E-SYS-005 logging service stopping`；stdout/stderr 空。

### 报错 / 异常

无。所有步骤退出码 0，stdout/stderr 无报错。仅需说明的事实：BQ3 电压字段未采集（板端无 BAT0 供电监测路径，monitor 按设计跳过，非报错）；BQ5 daemon 启动 marker `git=unknown`（临时目录非 git 仓库）与 `power=unknown`（源码硬编码默认值）。

### 覆盖声明（未覆盖项）

本轮为 v3 板端实测事实采集，**未做**：BQ5 的"实际安装 systemd 服务 + WatchdogSec 重启"（系统配置变更，安全边界外，标注 unverified/待授权）；sd_notify 实际投递验证（临时目录无 NOTIFY_SOCKET）；压力/长时测试；断电/掉电持久化；真实硬件故障接入（真实 SPI/CAN 业务通信、真实电压监测）；1 kHz 硬实时边界；静态审查（归 code_reviewer）。

### 交付物

- 报告：`software_tester/script/TESTREPORT-T-20261002-014-001.md`
- 原始输出：`software_tester/script/work/T-20261002-014-boardtest/raw/`（`01_identity` `02_upload` `03_bq1_selftest` `04_bq2_v2_smoke` `05_bq2_v3_smoke` `06_bq3_monitors` `07_bq4_core_config` `08_bq5_daemon` `SUMMARY`）
- 环境清单已更新：`software_tester/script/ENVIRONMENTS.md`
- 备料通知已发 maintainer：`MAIL-20261002-1550-software_tester--maintainer-HANDOFF-T-20261002-014`

本报告只描述观察到的现象，不作发布/验收结论。

software_tester (R-005)
2026-10-02 15:52
