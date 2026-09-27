# USAGE — rmlog 场下使用方法（RoboMaster 电控版）

> 任务: T-20260926-001-logging-platform-p0 · 读者: 电控队员（不要求 Linux 专家）
> 一句话: **赛场上 rmlog 自动把错误按"错误码+级别+双时间戳"写进日志文件；场下你用一条命令把问题定位出来。**
> 平台说明: 目标平台 RDK X5（Ubuntu 22.04 aarch64，已启用 PREEMPT-RT 实时内核）；
> 本文所有板端命令以 Q1=A 裁决为准 —— **由你按 §3 在板端执行自测并把输出回贴**，
> §6/§7 涉及系统组件的部分标注了"待板端核实"，未经你实测前不作为已验证结论。

---

## 0. 它能回答你什么问题（对应告别 Keil 断点）

| 场上现象 | 场下一条命令 |
|---|---|
| "上电后初始化失败过几次？" | `python3 rmlog_read.py filter rmlog.log --code E-INIT-*` |
| "SPI 是什么时候开始超时的？" | `python3 rmlog_read.py filter rmlog.log --code E-COMM-* --since 2026-09-26T14:00` |
| "比赛那 6 分钟里所有错误" | `python3 rmlog_read.py filter rmlog.log --level ERROR --since ... --until ...` |
| "宕机前最后发生了什么？" | `python3 rmlog_read.py tail rmlog.log -n 50` |

## 1. 交付物清单（本目录）

| 文件/目录 | 作用 |
|---|---|
| `rmlog/` | Python 日志组件（写入端 + 自测；**纯标准库，零第三方依赖**） |
| `rmlog/rmlog.h / rmlog.c / rmlog_errors.h / example.c` | C 接口（给 X5 上的 C/C++ 电控程序链接） |
| `rmlog_read.py` | 读端工具（parse / tail / filter） |
| `ERR-CATALOG.md` | 错误码表（五域 24 码，由 catalog.py 自动生成） |
| `tests/selftest-*.log` | 开发机自测原始输出（R1 末轮 12/12 PASS） |

## 2. 快速体验（Windows 开发机，3 分钟，可选）

```bat
cd developer\script
python -m rmlog.selftest                 :: 期望最后一行 SELFTEST PASS
mkdir tests\_work                        :: 自测结束会清理 _work, 先建回目录再编译（R1 修正）
gcc -std=c99 -Wall -Wextra -I rmlog -o tests\_work\example.exe rmlog\example.c rmlog\rmlog.c
tests\_work\example.exe tests\_work\demo
type tests\_work\demo\rmlog.log          :: 看到 4 行 LOGV1|... 即成功
python rmlog_read.py filter tests\_work\demo\rmlog.log --level ERROR
```

## 3. 板端自测步骤（用户执行 —— 需要你回贴输出）

> 目标: 在 RDK X5 真机上验证"组件可运行"（AC1 板端证据）。全程约 10 分钟。

### 3.1 把组件拷到板子

WiFi 已配置的前提下，在 **Windows 电脑**上（PowerShell）：

```powershell
# IP 换成你板子的地址；用户名默认 ubuntu（镜像默认）
scp -r developer\script\rmlog  ubuntu@<板子IP>:~/rmlog
scp    developer\script\rmlog_read.py  ubuntu@<板子IP>:~/rmlog/
```

（没有 scp 条件时用 U 盘拷贝 `rmlog/` 整个目录与 `rmlog_read.py` 同样有效。）

### 3.2 环境探测（把这两条的输出一并回贴）

```bash
python3 --version                 # 期望 Python 3.10.x（Ubuntu 22.04 自带）；≥3.8 即可跑
ls -ld /userdata 2>/dev/null; df -h /userdata 2>/dev/null   # 确认持久分区是否存在
```

### 3.3 跑自测

```bash
cd ~/rmlog
python3 -m rmlog.selftest
echo "EXIT=$?"
```

**期望结果**: 12 行 `PASS`（AC2/AC3/AC4/AC5×3/AC6/GEN/F2/READ），最后两行
`自测结束: 12/12 通过` 与 `SELFTEST PASS`，`EXIT=0`。

### 3.4 需要回贴的内容

1. §3.2 两条探测命令的完整输出；
2. §3.3 自测的**完整 stdout**（从 `rmlog.selftest — 工作区:` 到 `SELFTEST PASS`）；
3. `EXIT=` 那一行的值。

### 3.5 常见失败排查

| 现象 | 原因与处理 |
|---|---|
| `python3: command not found` | 板子烧的不是标准镜像或 PATH 异常；`which python3`、`ls /usr/bin/python*` 核实后反馈 |
| 自测里 AC5 concurrent / AC5×F-1 失败 | 先重跑一次（并发压测对 IO 负载敏感）；仍失败把完整输出回贴，属需修复缺陷 |
| `PermissionError` 写 `/userdata/rmlog` | 用户无该目录写权限；自测不受影响（selftest 用 `tests/_work`），部署时按 §6 用 root 或 `sudo chown` |
| scp 传输后报解码错误 | 用二进制方式传（scp 默认即是）；不要经 Windows 记事本中转任何 `.py` 文件（会引入 CRLF/编码问题） |
| 想指定自测工作区 | `python3 -m rmlog.selftest /tmp/rmlog_work`（参数 1 = 工作区路径） |

### 3.6 与实时内核的关系

自测**不依赖也不验证** PREEMPT-RT 特性（P0 日志组件不参与调度实时性）；
rt_patch 的作用是保证你们后续 1kHz 控制线程的确定性——日志只是在那之上如实记账。

## 4. 日志长什么样（行格式 v1）

```
LOGV1|3|2026-09-26T20:14:32.737|361673859|ERROR|E-COMM-001|spi|SPI 传输超时 dev=/dev/spidev0.0 retry=3
  │   │        │               │        │        │        │              │
  │   │        │               │        │        │        │              └ 消息（可含 k=v 细节）
  │   │        │               │        │        │        └ 模块名（哪个子系统）
  │   │        │               │        │        └ 错误码（五域，见 ERR-CATALOG.md）
  │   │        │               │        └ 级别: INFO < WARN < ERROR < FATAL
  │   │        │               └ 单调时间戳 ms（同一次开机内递增，防 NTP 跳变，算间隔用它）
  │   │        └ 墙上时间戳 ISO8601 毫秒（对表、与 journalctl/dmesg 对时间线用它）
  │   └ 进程内事件序号（#3 = 本进程第 3 条）
  └ 格式版本前缀（读端靠它识别并丢弃残行）
```

- **级别**: `INFO` 里程碑 / `WARN` 降级可继续 / `ERROR` 功能受损需处理 / `FATAL` 禁止带病上场；
- **错误码**: `E-<域>-<序号>`，五域 `INIT/COMM/HW/FSM/SYS` —— 每码的默认级别、中文含义、
  **建议动作**都在 `ERR-CATALOG.md`（例如 `E-COMM-004 通信中断 → 触发安全态，检查连接器`）；
- 消息里的 `|`、换行等会被转义成 `\x7c`、`\x0a`，**不会破坏一行一条事件**；
- 崩溃/断电留下的半行会被读端**丢弃并计数**（stderr 提示"丢弃残行 N 条"），不污染解析。

## 5. 场下定位演示（假想故障，5 分钟）

**场景**: 决赛 3:40，操作手报"云台失控"，你赛后拿到板子。

```bash
# 第 1 分钟: 装上板子拷出日志（板子在本地网络）
scp ubuntu@<板子IP>:/userdata/rmlog/rmlog.log* .

# 第 2 分钟: 先看"所有错误及以上"，量最大
python3 rmlog_read.py filter rmlog.log --level ERROR

# 第 3 分钟: 用比赛时间窗收窄（--since/--until 支持分钟级前缀; 前缀按日历语义
#   解释: --until 14:38 = 含 14:38 这一整分钟, 即 [14:38:00.000, 14:38:59.999]）
python3 rmlog_read.py filter rmlog.log --level ERROR --since 2026-09-26T14:32 --until 2026-09-26T14:38

# 第 4 分钟: 锁定可疑域（云台失控 → 通信/状态机）
python3 rmlog_read.py filter rmlog.log --code E-COMM-* --since 2026-09-26T14:32
python3 rmlog_read.py filter rmlog.log --code E-FSM-*  --since 2026-09-26T14:32

# 第 5 分钟: 对时间线交叉系统日志（谁先谁后、系统层面有没有同时出事）
journalctl --since "2026-09-26 14:32" --until "2026-09-26 14:38" -p err   # 待板端核实 §7
sudo dmesg --time-format iso | grep -iE "spi|error" | head -50
```

**判读要点**: rmlog 的墙上时间戳与 journalctl/dmesg 的 ISO 时间同源可比对；
`E-COMM-004（通信中断）` 的建议动作会直接写在 `ERR-CATALOG.md` 里。

## 6. 部署为常驻服务（P1 实测项；本节为样例）

- **日志目录**: 默认 `/userdata/rmlog/`（Q2 裁决值，root 运行）；该分区不存在时组件自动回退
  `/var/log/rmlog/`。代码路径也可显式指定（Python `Writer(log_dir=...)` / C `rmlog_open(dir)`）。
- **部署约束（R1 增补）**: 同一日志目录的**所有写入方必须都经 rmlog 组件**（C/Python 双端
  已约定同名轮转锁文件 `.rmlog.ROTLOCK`）—— 跨进程轮转互斥是 advisory 锁，若有第三方工具
  直接写 `rmlog.log` 或自行 rename，互斥前提不成立。多进程部署时各进程应使用**相同的
  max_bytes/keep 配置**。
- **systemd 单元样例**（保存为 `/etc/systemd/system/rmlog-demo.service`；P0 未在板端实测安装）:

```ini
[Unit]
Description=RoboMaster text logger demo
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/ubuntu/rmlog/demo_service.py
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload && sudo systemctl enable --now rmlog-demo
```

> P1 会交付正式的常驻服务与开机自启验证（REQ §4 P1），本节仅作为样例说明部署形态。

## 7. 与 X5 自带日志设施的配合（系统层"直接用"，业务层 rmlog）

| 你要看 | 命令 | 说明 |
|---|---|---|
| 上次开机的系统级错误 | `journalctl -b -1 -p err` | 服务崩溃/OOM/启动失败（journald 持久化待板端核实） |
| 本次开机内核报错 | `sudo dmesg --time-format iso | grep -iE "spi|can|i2c|oops"` | 总线/驱动级异常，MCU 时代没有的证据面 |
| 进程崩溃现场 | `coredumpctl list` | 需 systemd-coredump 已启用（待板端核实） |
| 文本系统日志 | `/var/log/syslog` | 若镜像带 rsyslog（待板端核实） |

**分工**: 系统组件的账 journald/dmesg 记，比赛业务语义的账（错误码/建议动作/双时间戳）rmlog 记，
两边用**墙上时间戳**对齐时间线——这就是 REQ §3"平台层直接用 + 业务层自建"的落地。

## 8. 本阶段（P0）局限与 P1 展望（诚实清单）

| 局限 | 影响 | P1 计划 |
|---|---|---|
| Windows 侧多进程写入用写锁串行化 | 仅影响开发机自测；Linux 板端为内核级 O_APPEND 原子追加 + flock 轮转互斥，写路径零锁 | 板端实测复验（§3）；多进程×轮转组合建议增测（IMPL §2.1） |
| Python 端每条事件 3 次系统调用（open/write/close） | 多进程×轮转数据不灭失的代价；1kHz 场景 µs 级可忽略 | 高频路径用 C 端（常驻 fd）；P2 批量化优化 |
| 多进程×轮转的 Linux 行为是协议推演（unverified） | 板端实测前不作为已验证结论（IMPL §2.1 推演声明） | 用户板端自测增测该组合 |
| INFO/WARN 依赖缓冲，硬断电窗口可能丢少量非关键行 | ERROR/FATAL 已强制 flush；预期损失边界=最近几条 INFO | 关键事件可开 `fsync=True`（接口已留） |
| C 端暂不支持 k=v 属性参数 | C 宏消息里可自带 `k=v` 文本 | P1 扩展宏族（management 已裁定列入 P1） |
| C 端 mkdir 仅单级创建 | 深层目录需部署方预建（§6） | P1 升级逐级创建（management 已裁定列入 P1） |
| systemd/快照包/自启动未实测 | §6 为样例 | P1 交付实测版 + 一键快照脚本 |
| 错误码表 24 码为初版 | 覆盖团队规划的高频场景 | 随业务接入扩充（改 catalog.py 重新生成，勿手改） |

## 9. FAQ

**Q: 为什么不直接用 print 或 logging？**
A: print 没有错误码/级别约定、多进程会串行半行、断电即丢；logging 面向进程内调试，
没有"场上黑匣子"的落盘保证与比赛语义的错误码表。rmlog 是这两者的比赛特化。

**Q: 单调时间戳和墙上时间戳为什么要都有？**
A: 墙上时间会被 NTP 校时"跳变"甚至倒流（比赛现场断网后回连很常见），算"两次事件间隔多少 ms"
必须用单调时间；而对表、和系统日志对时间线必须用墙上时间。双轨制让两种问题都不踩坑。

**Q: 怎么新增一个错误码？**
A: 只改 `rmlog/catalog.py` 的 `ERRORS` 表 → `python3 -m rmlog.gen_code`（重新生成 C 头）→
`python3 -m rmlog.gen_code --doc`（重新生成 ERR-CATALOG.md）。**永远不要手改生成的文件**。
