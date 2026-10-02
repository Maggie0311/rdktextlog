# rmlog v3 电控使用说明

这套日志用于比赛现场自动留证和赛后定位问题。文本日志说明“发生了什么、属于哪类问题”；黑匣子保存错误发生前的高频状态，便于和数值日志对照。

## 1. 前置准备

将以下内容复制到板端项目目录，例如 `/opt/rdk_x5_software/developer/script`：

```text
rmlog/
rmlog_read.py
export_evidence.py
systemd/rmlog-demo.service
shared/rmlog_schema.h
```

运行程序前设置路径并创建日志目录：

```bash
export PYTHONPATH=/opt/rdk_x5_software/developer/script:$PYTHONPATH
mkdir -p /userdata/rmlog
```

错误码只修改 `rmlog/catalog.py`，再生成 C/Python/STM32 共享头文件：

```bash
python3 -m rmlog.gen_code
```

不要手改 `rmlog_errors.h` 和 `shared/rmlog_schema.h`。

## 2. 在业务代码中接入

### 2.1 初始化一次日志运行时

在控制程序启动函数中写：

```python
from rmlog.session import Session
from rmlog.writer import Writer
from rmlog.async_writer import AsyncWriter
from rmlog.auto import LogRuntime

session = Session("match")
writer = AsyncWriter(Writer(log_dir="/userdata/rmlog"), session=session)
runtime = LogRuntime(
    writer,
    "/userdata/rmlog/blackbox",
    capacity=2000,
    session=session,
)
```

程序退出前写：

```python
writer.close()
```

### 2.2 记录初始化、模式切换和业务错误

在对应业务函数中调用 `runtime.emit()`：

```python
runtime.emit("E-INIT-000", "chassis", "底盘初始化完成")
runtime.emit(
    "E-COMM-001", "spi", "SPI 应答超时",
    attrs={"device": "/dev/spidev0.0", "retry": 2},
)
```

只使用现有错误码：`INIT`、`COMM`、`HW`、`FSM`、`SYS` 五个域共 24 个码。`ERROR/FATAL` 事件会自动触发黑匣子快照。

### 2.3 记录黑匣子高频数据

在底盘循环、IMU 更新、状态机更新处调用 `runtime.sample()`。它只写内存，不直接落盘：

```python
runtime.sample("chassis", vx=vx, vy=vy, wz=wz, mode=chassis_mode)
runtime.sample(
    "imu", yaw=yaw, pitch=pitch, roll=roll,
    gyro_x=gx, gyro_y=gy, gyro_z=gz, valid=int(imu_valid),
)
runtime.sample(
    "fsm", state=state_name,
    last_event=last_event, dwell_ms=state_dwell_ms,
)
```

建议同时记录心跳、通信计数、电压、温度和日志丢弃计数。错误发生后，最近窗口会写入 `/userdata/rmlog/blackbox/blackbox-*.jsonl`。

### 2.4 主循环心跳和状态机卡死

主循环每次迭代末尾喂狗：

```python
runtime.heartbeat("main", count=loop_count)
```

启动看门狗（超时记录 `E-FSM-003`）：

```python
from rmlog.monitors import HeartbeatWatchdog

watchdog = HeartbeatWatchdog(runtime, name="main", timeout=1.5)
watchdog.start()
```

退出时调用 `watchdog.stop()`。

### 2.5 通信失败和错误率

在 SPI/CAN/串口适配层创建统计器，每次收发后调用 `success()` 或 `failure()`：

```python
from rmlog.monitors import CommStats

comm = CommStats(
    runtime, "spi_chassis",
    window=20, fail_threshold=3,
    rate_window=20, error_rate_threshold=0.5,
)

if spi_ok:
    comm.success()
else:
    comm.failure("底盘 SPI 传输失败")
```

短时突发或分散失败通常记录 `E-COMM-003`；连续达到 `window` 次失败才记录 `E-COMM-004`。

### 2.6 温度、电压和内存监控

在启动阶段创建并启动：

```python
from rmlog.resources import ResourceMonitor

resources = ResourceMonitor(
    runtime, interval=1.0,
    temp_limit=85000,       # 毫摄氏度，85000 = 85°C
    voltage_min=14000,      # mV
    memory_min_kb=32768,
)
resources.start()
```

退出时调用 `resources.stop()`。越限会自动记录 `E-HW-001`、`E-HW-002` 或 `E-SYS-001`。

### 2.7 内核日志捕获

在后台线程启动：

```python
from rmlog.monitors import DmesgMonitor
import threading

dmesg_monitor = DmesgMonitor(runtime)
dmesg_thread = threading.Thread(target=dmesg_monitor.run, daemon=True)
dmesg_thread.start()
```

退出时停止并等待：

```python
dmesg_monitor.stop()
dmesg_thread.join(timeout=2.0)
```

测试时可传入字符串列表作为 `source`，不依赖真实 `dmesg`。

### 2.8 systemd 自启和崩溃遗言

自带服务入口已经接好启动 Marker、主循环心跳、watchdog 和崩溃遗言：

```bash
sudo cp systemd/rmlog-demo.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now rmlog-demo.service
```

查看服务：

```bash
systemctl status rmlog-demo.service
journalctl -u rmlog-demo.service --no-pager
```

崩溃遗言在 `/userdata/rmlog/crash/crash-<pid>.log`。是否生成 core 文件还取决于板端 `ulimit -c` 和 `kernel.core_pattern`。

## 3. 赛后查看和导出

```bash
cd /opt/rdk_x5_software/developer/script

# 最近 20 条、持续跟踪
python3 rmlog_read.py tail /userdata/rmlog/rmlog.log
python3 rmlog_read.py tail /userdata/rmlog/rmlog.log --follow

# 错误、错误域、会话和统计
python3 rmlog_read.py filter /userdata/rmlog/rmlog.log --level ERROR
python3 rmlog_read.py filter /userdata/rmlog/rmlog.log --code E-COMM-*
python3 rmlog_read.py filter /userdata/rmlog/rmlog.log --session <session_id>
python3 rmlog_read.py stats /userdata/rmlog/rmlog.log
```

一键导出业务日志、轮转副本、journal、dmesg、系统版本和清单：

```bash
python3 export_evidence.py \
  /userdata/rmlog/rmlog.log \
  /userdata/evidence/match-$(date +%Y%m%d-%H%M%S)
```

只导出某次启动/比赛：

```bash
python3 export_evidence.py \
  /userdata/rmlog/rmlog.log \
  /userdata/evidence/match-session \
  --session <session_id>
```

导出目录主要包含：

```text
business.log   # 业务日志及轮转副本
journal.txt    # systemd 日志
kernel.txt     # dmesg
version.txt    # uname -a
MANIFEST.txt   # 每项成功、缺失或权限不足原因
```

建议排查顺序：先看 `ERROR/FATAL` 和错误域，再看对应 `blackbox-*.jsonl`，最后按时间戳、session、错误码与数值日志对照。

## 4. 使用边界

- 异步队列满时会增加 `dropped` 计数；不承诺硬实时和零丢失。
- 日志库不会自动理解 SPI/CAN、状态机或电机协议，业务需要接入上面的统计、心跳和样本接口。
- 24 个字符串错误码、旧 API 和 bit 映射保持兼容。
- systemd、dmesg、sysfs、STM32 工具链和 core dump 的真实权限/行为仍需在 RDK X5 上实测。
