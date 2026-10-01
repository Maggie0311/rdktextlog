# USAGE — rmlog 使用手册（RoboMaster 电控版）

> 读者: 电控队员（会 C/Python，不要求 Linux 专家）· 版本: 002（T-20260928-004 重构为用户优先结构）
> 一句话: **上电后 rmlog 自动把错误按"错误码 + 级别 + 双时间戳"写进板上的日志文件；比赛时你什么都不用做，赛后用一条命令把问题定位出来。**
> 平台目标: RDK X5（Ubuntu 22.04 aarch64）。本 T-20260930-005 v2 候选仅在开发机验证；
> X5 板端 selftest、编译、systemd 安装和运行仍待按本手册复测，不能用第一版历史报告替代。
> 命令是使用示例，不表示当前 v2 commit 已在板端实跑；版本证据见 `IMPL-T-20260930-005-logging-v2.md`。

---

## 1. 快速上手：3 分钟记出第一条日志

### 1.1 Python 程序（2 行起步）

把组件目录 `rmlog/` 放在你的代码能 import 到的位置（比如同目录），然后：

```python
import rmlog
rmlog.event("E-INIT-000", "ctrl", "上电启动完成")
```

这就写出了第一条日志——默认落在板上的 `/userdata/rmlog/rmlog.log`（root 运行即写，无需建目录）。
再进一步，给事件带上 k=v 属性（见 §2.3）：

```python
rmlog.event("E-COMM-001", "spi", "SPI 传输超时", attrs={"dev": "/dev/spidev0.0", "retry": 3})
```

**日志文件位置想换地方**（开发机上演示必读：`/userdata` 是板端分区，Windows/Linux 开发机上没有，
不换目录直接跑会在创建默认目录这一步报错）：

```python
from rmlog.writer import Writer, set_default_writer
set_default_writer(Writer(log_dir="./mylog"))   # 进程内所有 rmlog.event(...) 改写 ./mylog/rmlog.log
import rmlog                                    # 放在 set_default_writer 之后
rmlog.event("E-INIT-000", "ctrl", "开发机演示")
```

### 1.2 C 程序（3 行起步）

```c
#include "rmlog.h"
RMLOG_I("ctrl", RMLOG_CODE_INIT_000, "上电自检完成 state=%d", 1);
RMLOG_E("spi",  RMLOG_CODE_COMM_001, "SPI 传输超时 dev=%s", "/dev/spidev0.0");
```

首次调用宏会自动初始化，默认同样写 `/userdata/rmlog/rmlog.log`。编译（板端 gcc，错误码常量
在生成头文件 `rmlog_errors.h` 里，`-I` 指到组件目录即可）：

```bash
gcc -std=c99 -Wall -Wextra -I rmlog -o myprog myprog.c rmlog/rmlog.c -lpthread
```

想要可跑的最小完整示例：组件自带 `rmlog/example.c`（四级别各记一条），编译运行：

```bash
gcc -std=c99 -Wall -Wextra -I rmlog -o example rmlog/example.c rmlog/rmlog.c -lpthread
./example ~/rmlog/demo        # 参数 = 演示日志目录；板上省略参数走默认目录
```

### 1.3 看一眼你刚记的日志（读端工具）

读端工具 `rmlog_read.py` 与 `rmlog/` 同目录分发。三个子命令 `parse / tail / filter`：

```bash
python3 rmlog_read.py tail  /userdata/rmlog/rmlog.log -n 20        # 最后 20 条
python3 rmlog_read.py filter /userdata/rmlog/rmlog.log --level ERROR   # 所有错误及以上
```

输出一行一条，格式是 `时间 [级别] 错误码 模块: 消息 k=v...`，例如：

```
2026-09-28T21:50:29.794 [ERROR] E-COMM-001 spi: SPI 传输超时 dev=/dev/spidev0.0 retry=3
```

### 1.4 日志长什么样（行格式 v1）

用 `python3 rmlog_read.py parse <文件>` 可以看到每行的原始字段。原始行由 `|` 分成 8 段：

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

- 消息里的 `|`、换行会被转义成 `\x7c`、`\x0a`，**不会破坏一行一条事件**；
- 崩溃/断电留下的半行会被读端**丢弃并计数**（stderr 提示"丢弃残行 N 条"），不污染解析。

---

## 2. 日常使用：怎么打、怎么查

### 2.1 级别怎么选

**默认不用选**——每个错误码在 `ERR-CATALOG.md` 里都绑定了默认级别，你只管按码记录。
默认级别的含义：

| 级别 | 语义 | 你需要做什么 |
|---|---|---|
| INFO | 里程碑事件（如"初始化完成"） | 什么都不用做，用于划定时间线 |
| WARN | 降级可继续（如"电压接近下限"） | 场上不处理，赛后复盘 |
| ERROR | 功能受损需处理（如"SPI 传输超时"） | 赛后必查；场上按码表建议动作处置 |
| FATAL | 禁止带病上场（如"状态机未定义状态"） | 立即停机排查 |

只有当某次调用想临时升降级时才显式传：Python `rmlog.event(..., level="WARN")`；
C 端用对应级别宏 `RMLOG_W(...)`。**不要**靠改级别来"隐藏"某类错误——要修码表的语义就改码表（§6 Q5）。

### 2.2 错误码怎么打、怎么查

- **打**：直接用码字符串（Python），或生成头文件里的 `RMLOG_CODE_*` 常量（C）。码必须长得像
  `E-<域>-<三位序号>`，五域：`INIT` 初始化 / `COMM` 通信 / `HW` 硬件 / `FSM` 状态机 / `SYS` 系统资源。
  接入期想先跑起来，可以临时用表里没有的同格式码——读端不拒绝，但**正式代码请回归码表**。
- **查**：打开 `ERR-CATALOG.md`（或 `python3 -m rmlog.gen_code --doc` 重新生成最新版），
  每个码都有中文含义与**建议动作**，例如 `E-COMM-004 通信中断 → 触发安全态，检查连接器`。
- **按码过滤**：读端 `--code` 支持前缀通配，`*` 要写在一整段里：

  ```bash
  python3 rmlog_read.py filter rmlog.log --code E-COMM-*      # 通信域全部
  python3 rmlog_read.py filter rmlog.log --code E-INIT-001    # 单个码
  ```

### 2.3 模块名与 k=v 属性的使用时机

- **模块名**：你们子系统的短名（`ctrl` / `comm` / `spi` / `pwr` / `vision` …），全队统一一张小表即可。
  定位时按模块过滤没有专门参数——把模块名约定好，靠错误码域 + 消息文本即可定位。
- **k=v 属性**：**会变化、需要事后统计比对的参数**才做成属性（Python `attrs={...}`），
  如 `dev=/dev/spidev0.0`、`retry=3`、`v=22500`。读端会把属性解析出来回显，便于肉眼比对与脚本统计。
  固定不变的人话上下文直接写进消息文本就好，不必属性化。
- C 端宏暂不支持属性参数（P1 扩展项），需要 k=v 时直接写进消息文本（如 `"dev=%s"`）。

### 2.4 日志文件在哪、占多少盘

- 默认目录 **`/userdata/rmlog/`**（板上持久分区；`/userdata` 不存在时组件自动回退 `/var/log/rmlog/`，
  构造时连回退目录都建不出来会直接报错——不会静默丢日志）。
- 单文件上限默认 **2 MB**，超过自动轮转：`rmlog.log → rmlog.log.1 → … → rmlog.log.5`，最旧删除；
  保留策略由创建 Writer 时的 `max_bytes`（字节）与 `keep`（份数）决定，**同一目录的所有写入方
  必须用相同配置**（否则保留期按更小的那个算）。日志目录里还有一个 `.rmlog.ROTLOCK`
  轮转互斥锁文件，属正常现象，不要删。
- 磁盘占用上限 ≈ `max_bytes × (keep + 1)`，默认约 12 MB——不用担心把卡写满。
- 日志目录也可显式指定：Python `Writer(log_dir=...)` / C `rmlog_open(dir)`（见 §1.1、§7）。

### 2.5 rmlog_read 最常用的三条命令

```bash
# ① 赛后第一时间：这个时段所有错误及以上（量最大的一眼）
python3 rmlog_read.py filter rmlog.log --level ERROR

# ② 锁定可疑域：通信域到底有没有超时（--code 支持前缀通配）
python3 rmlog_read.py filter rmlog.log --code E-COMM-*

# ③ 宕机/掉电前最后发生了什么
python3 rmlog_read.py tail rmlog.log -n 50
```

补充两个顺手命令：

```bash
python3 rmlog_read.py parse rmlog.log            # 逐行全字段解析（检查格式/残行标注）
python3 rmlog_read.py tail rmlog.log -n 20 --follow   # 板上实时跟踪新日志（类 tail -f，Ctrl+C 退出）
```

时间窗过滤 `--since/--until` 支持毫秒全精度，也支持"分钟级前缀"（前缀按日历段语义解释：
`--until 14:38` = 含 14:38 这一整分钟）：

```bash
python3 rmlog_read.py filter rmlog.log --level ERROR --since 2026-09-26T14:32 --until 2026-09-26T14:38
```

> 注意：`rmlog_read.py` 的文件参数**不支持通配符展开**。轮转副本请逐个文件读
> （`rmlog.log`、`rmlog.log.1`、`rmlog.log.2` …），通配符会被当成字面文件名而"文件不存在"。

---

## 3. 比赛日操作流

### 3.1 赛前检查清单（3 分钟）

```bash
# ① 磁盘够不够（日志上限 ~12MB，正常永远够；担心的是整卡）
df -h /userdata

# ② 组件自启确认（按 §7 部署了 systemd 服务的队伍；没部署则跳过，赛前手动起程序）
systemctl is-active rmlog-demo        # 期望 active；inactive 则 sudo systemctl start rmlog-demo

# ③ 时间同步确认（时间戳要能跟系统日志对时间线，RTC 不准的板子务必确认 NTP 已对上）
timedatectl                           # 看 "System clock synchronized: yes"
```

三样都绿，比赛期间你不需要再碰板子。

### 3.2 赛中：零操作

程序跑起来之后**什么都不用做**——写入、轮转、错误落盘全自动。ERROR/FATAL 每条即写即落盘
（fdatasync），断电最多丢最近几条 INFO/WARN，关键证据不会丢。

### 3.3 赛后取日志 + 5 分钟定位

**场景**：决赛 3:40，操作手报"云台失控"，你赛后拿到板子（板子在本地网络，IP 换成实际值）。

```bash
# 第 1 分钟: 拷出全部日志（含轮转副本）
scp <用户名>@<板子IP>:/userdata/rmlog/rmlog.log* .

# 第 2 分钟: 先看所有错误及以上，量最大
python3 rmlog_read.py filter rmlog.log --level ERROR

# 第 3 分钟: 用比赛时间窗收窄
python3 rmlog_read.py filter rmlog.log --level ERROR --since 2026-09-26T14:32 --until 2026-09-26T14:38

# 第 4 分钟: 锁定可疑域（云台失控 → 通信/状态机）
python3 rmlog_read.py filter rmlog.log --code E-COMM-* --since 2026-09-26T14:32
python3 rmlog_read.py filter rmlog.log --code E-FSM-*  --since 2026-09-26T14:32

# 第 5 分钟: 对时间线交叉系统日志（谁先谁后、系统层面有没有同时出事，见 §4）
journalctl --since "2026-09-26 14:32" --until "2026-09-26 14:38" -p err
sudo dmesg --time-format iso | grep -iE "spi|error" | head -50
```

**判读要点**：rmlog 的墙上时间戳与 journalctl/dmesg 的 ISO 时间同源可比对；
命中的错误码拿去 `ERR-CATALOG.md` 查建议动作（`E-COMM-004 通信中断 → 检查两端连接器`）。

---

## 4. 与系统日志的关系（journald / dmesg）

**分工**：系统组件的账 journald/dmesg 记，比赛业务语义的账（错误码/建议动作/双时间戳）rmlog 记；
两边用**墙上时间戳**对齐时间线。journald 持久化、rsyslog 状态和 dmesg 时间格式需在目标板端复测；
`dmesg --time-format iso` 输出 ISO 时间（与 rmlog 墙上时间同格式可比）。

| 你要看 | 命令 | 说明 |
|---|---|---|
| 上次开机的系统级错误 | `journalctl -b -1 -p err` | 服务崩溃/OOM/启动失败 |
| 本次开机内核报错 | `sudo dmesg --time-format iso \| grep -iE "spi\|can\|i2c\|oops"` | 总线/驱动级异常 |
| 文本系统日志 | `/var/log/syslog` | rsyslog 在跑，可直接翻 |
| 某进程的全部输出 | `journalctl -u rmlog-demo` | 配合 §7 的 systemd 服务名 |

> 板端未启用 systemd-coredump（`coredumpctl` 不存在）——进程崩溃现场主要靠 `journalctl`
> 里的崩溃记录与 rmlog 的 FATAL 行交叉定位。

---

## 5. FAQ 与故障排查（现象 → 原因 → 处置）

**Q1 日志文件没生成？**
现象：`/userdata/rmlog/` 下没有 `rmlog.log`。
原因与处置：① 程序还没记过任何一条日志（文件在第一条写入时才创建）——先确认业务代码真的调到了
`rmlog.event(...)` / `RMLOG_*`，可用一条 INFO 试写；② `/userdata` 分区不存在，组件回退到了
`/var/log/rmlog/`——去那里找；③ 目录建不出来（权限/只读盘）——组件会在创建默认目录这一步直接报错
（Python 抛 `PermissionError`/`OSError`，C 端 `rmlog_open` 返回非 0），按报错修目录权限或显式指定目录。

**Q2 写日志报 Permission denied？**
现象：Python 抛 `PermissionError`，或 C 端 `rmlog_open` 失败。
原因与处置：日志目录的属主与运行身份不一致。默认部署形态是 **root 运行 + root 目录**；
用普通用户跑就把目录属主改一致：`sudo chown -R <运行用户> /userdata/rmlog`，
或干脆用 `Writer(log_dir=...)` / `rmlog_open(dir)` 指定一个该用户可写的目录。
开发机上没有 `/userdata`，别对着默认目录跑（§1.1 的自定义目录版）。

**Q3 磁盘满了 / 存储水位告警怎么办？**
现象：`E-SYS-002 日志落盘失败` / `E-SYS-004 存储水位告警` 出现在日志里。
原因与处置：rmlog 自身默认只占约 12 MB（2 MB × 6 份），满了说明整卡空间被别的数据吃了。
`df -h /userdata` 确认 → 删旧日志/旧录像腾空间 → 期间缺失的日志证据链已降级（E-SYS-002 的含义
就是"这段时间可能没记上"），无法补录。赛前按 §3.1 检查磁盘即可避免。

**Q4 时间戳不对/和系统日志对不上？**
现象：墙上时间戳明显不是当前时间，或跟 journalctl 对不齐。
原因与处置：板子 RTC 不准且未 NTP 对时。rmlog 的**墙上时间**来自系统时钟，系统不对它就不对；
**单调时间**只管算间隔（同一次开机内递增），跨开机比较没有意义。处置：
`timedatectl set-ntp true` 对时后重启程序；比对时间线一律用墙上时间（§4）。

**Q5 多个进程写同一个目录安全吗？**
现象：想多个进程共用一个日志目录。
原因与处置：**安全，前提是所有写入方都走 rmlog 组件**（C/Python 双端经同名锁文件
`.rmlog.ROTLOCK` 互斥轮转），并使用相同的 `max_bytes/keep` 配置。不要让 print 重定向、
第三方工具直接写 `rmlog.log` 或自行改名轮转——互斥前提就不成立了。每个进程的事件序号
（seq 段）独立递增，同进程内有序、跨进程不比较。

**Q6 日志文件只剩 `rmlog.log.1/.2/...`，主文件去哪了？**
现象：目录里没有 `rmlog.log` 本体。
原因与处置：正常。轮转是把当前文件改名进副本链，主文件在**下一条写入时**才重建；
写入频率低时可能长时间只有副本。读任意副本用 `rmlog_read.py` 逐个传路径（不支持通配符，§2.5）。

**Q7 怎么新增一个错误码？**
只改 `rmlog/catalog.py` 的 `ERRORS` 表 → `python3 -m rmlog.gen_code`（重新生成 C 头）→
`python3 -m rmlog.gen_code --doc`（重新生成 ERR-CATALOG.md）。**永远不要手改生成的文件**。

**Q8 为什么不直接用 print 或 logging？**
print 没有错误码/级别约定、多进程会写串半行、断电即丢；logging 面向进程内调试，没有
"场上黑匣子"的落盘保证与比赛语义的错误码表。rmlog 是这两者的比赛特化：
ERROR/FATAL 即写即落盘、多进程一行不串、崩溃残行不污染解析。

**Q9 单调时间戳和墙上时间戳为什么要都有？**
墙上时间会被 NTP 校时"跳变"甚至倒流（比赛现场断网后回连很常见），算"两次事件间隔多少 ms"
必须用单调时间；而对表、和系统日志对时间线必须用墙上时间。双轨制让两种问题都不踩坑。

---

## 6. 部署（一次性配置附录：做一次就完）

本节是**给部署者的一次性配置**，做完之后日常使用回到 §2/§3，不需要再碰。

### 6.1 组件放哪

把 `rmlog/`（Python 组件 + C 接口）与 `rmlog_read.py` 拷到板上一个固定位置，建议：

```
/home/ubuntu/rmlog/          # rmlog/ 组件目录 + rmlog_read.py + 你的业务程序
/userdata/rmlog/             # 日志数据目录（组件默认落点，root 运行自动创建）
```

传输：`scp -r developer/script/rmlog ubuntu@<板子IP>:~/rmlog`（U 盘同样有效）。
不要经 Windows 记事本中转任何 `.py` 文件（会引入 CRLF/编码问题）。

### 6.2 开机自启（systemd 样例）

把你的主控程序包成服务，保存为 `/etc/systemd/system/rmlog-demo.service`
（`ExecStart` 换成你的程序；rmlog-demo 只是示例名）：

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

> `ExecStart` 必须指向持续运行的业务入口（不能指向写几条日志后正常退出的 fault demo）。
> 仓库模板 `systemd/rmlog-demo.service` 使用 `python3 -m rmlog.daemon` 作为持续运行示例；
> 它只写启动/停止事件，真实项目应在该入口接入业务循环。目标板上的安装、权限和重启行为仍待复测。

### 6.3 更新组件的方法

换新版本组件 = 停程序 → 覆盖 `rmlog/` 与 `rmlog_read.py` → 起程序：

```bash
sudo systemctl stop rmlog-demo       # 或手动停你的程序
# 覆盖 ~/rmlog 下的组件文件（scp/U 盘均可）
sudo systemctl start rmlog-demo
```

日志数据在 `/userdata/rmlog/`，与组件分离，更新组件**不动日志**。

### 6.4 部署约束（写给配置的人）

- 同一日志目录的**所有写入方必须都经 rmlog 组件**（§5 Q5）；
- C 端 `rmlog_open(dir)` 的目录**只创建单级**——深层目录请预先建好（`mkdir -p`）；
- 错误码表如需扩充，按 §5 Q7 从 `catalog.py` 重新生成，勿手改生成物。

---

## 7. 本手册与代码的对应关系（维护者参考）

| 手册内容 | 代码事实来源 |
|---|---|
| 行格式 v1 / 转义 / 残行判定 | `rmlog/format.py`（唯一权威定义，C 端同构） |
| 默认目录 / 轮转参数 / flush 语义 | `rmlog/writer.py`（`DEFAULT_DIR=/userdata/rmlog`，回退 `/var/log/rmlog`；2 MB × keep 5） |
| C 接口宏族 / 初始化语义 | `rmlog/rmlog.h`、`rmlog/rmlog.c` |
| 错误码表 / 默认级别 / 建议动作 | `rmlog/catalog.py` → `ERR-CATALOG.md`（生成物，勿手改） |
| 读端三命令 / 时间前缀语义 | `rmlog_read.py`（`--since/--until` 前缀=日历段语义） |
| 板端实测结论（selftest 13/13、编译零告警、多进程×轮转对账） | `software_tester/script/TESTREPORT-T-20260927-003-001.md` |
| 版本 002 手册改版缘由与示例实跑核对记录 | `IMPL-T-20260926-001-logging-platform-p0.md` §9 |
