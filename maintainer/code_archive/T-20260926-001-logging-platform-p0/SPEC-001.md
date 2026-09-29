# SPEC-001 — rmlog 文本日志平台（T-20260926-001-logging-platform-p0）· 说明书

<!-- v2 增补（2026-09-29，maintainer）：本 SPEC 代码面结论对版本 002（来源 08f6ce8）继续有效——该版为纯文档重构（代码零变更）；文档面以 v002/code/ 为准，见同目录 VERSION-002.md 与 DIFF-002.md。 -->

> **归档版本 001 · 来源 commit `164d4c7`**（被审查/被板端复测/被验收的同一份；验收状态 accepted）
> 本文代码位置引用规则：`file:line` 均指**归档带注版**（`code/` 目录下文件）；带注版相对来源 commit 仅新增注释行（+130/-0，见 VERSION-001 §6）。
> **同一代码位置在来源 commit 中的行号 = 带注版行号 − 该文件头部新增行数**（各文件新增行数见 VERSION-001 §4/§6）；审查与测试一律以来源 commit 为准，**归档件不是审查/测试对象**。

---

## 1. 一句话定位

**rmlog 是一套给 RoboMaster 电控用的"场上黑匣子"文本日志平台**：赛场上，C 或 Python 程序用一行代码（`RMLOG_E("spi", E-COMM-001, "SPI 超时")` / `rmlog.event(...)`）把错误按"错误码 + 级别 + 双时间戳"自动追加进磁盘上的一个文本文件，多进程并发写不会丢行、文件超大会自动轮转保留最近几份、崩溃前最后一条 ERROR/FATAL 保证已落盘；场下，用 `rmlog_read.py` 一条命令（filter/tail/parse）就能按级别、错误码、时间窗定位问题——替代"依赖 Keil 在线断点调试"的传统工作方式。错误码表 C/Python 双端同源（单一 Python 表生成两端常量与文档）。

## 2. 结构总览（文件清单 + 职责）

| 文件 | 职责 | 语言 | 一句话读法 |
|---|---|---|---|
| `rmlog/__init__.py` | 包入口：转发公开 API、提供 `encode_line` 显式参数包装（AC4 对照用） | Python | 只看 `encode_line` 的 docstring 即可 |
| `rmlog/catalog.py` | **错误码表唯一数据源**（五域 24 码，每码绑定级别/含义/建议动作） | Python | 纯数据 + 3 个查表函数 |
| `rmlog/format.py` | **行格式 v1 唯一权威定义**：编码（事件→行）与解析（行→事件）、转义表、双时间戳 | Python | 看模块头 + `_ESCAPES` + `parse_line` 三道闸 |
| `rmlog/writer.py` | 写入端：多进程安全追加、可控 flush、按大小轮转（**轮转协议 v2**） | Python | 看模块头"轮转协议 v2"推理链 a~e |
| `rmlog/worker.py` | 多进程并发压测工作进程（selftest 专用，非业务 API） | Python | 看模块头即可 |
| `rmlog/gen_code.py` | 生成器：catalog → `rmlog_errors.h`（C 头）+ `ERR-CATALOG.md`（文档） | Python | 单一来源机制的工具落点 |
| `rmlog/selftest.py` | 自测入口：13 用例覆盖 AC2–AC6 + F-1/F-2/RF-6 回归闸 | Python | 看文件尾 `tests` 列表（maintainer 补注列了每用例守什么） |
| `rmlog/encode_cases.py` | AC4 双端一致性用例集（7 个固定输入用例 + 二进制传输编解码） | Python | 看模块头声明的一致性范围 |
| `rmlog/rmlog.h` | C 接口对外唯一头文件：`RMLOG_I/W/E/F` 宏族 + 生命周期 | C | 业务接入只看这一个文件 |
| `rmlog/rmlog.c` | C 实现：线程安全写入、轮转协议 v2、平台适配层（Win32/POSIX） | C | 739 行，看文件头变更史 + maintainer 补注的读码路径 |
| `rmlog/rmlog_errors.h` | **生成物（勿手改）**：C 端错误码常量/级别常量/静态码表 | C (generated) | 不读也行，查宏名时用 |
| `rmlog/example.c` | C 最小使用示例（四级事件各一条），USAGE §2/IMPL §3 命令编译对象 | C | 40 行，5 分钟读完 |
| `rmlog/_ac4_probe.c` | AC4 C 探针（selftest 运行时生成后再编译；此文件为留档静态审查副本） | C | 只在研究 AC4 验证方法时读 |
| `rmlog_read.py` | 读端工具：parse / tail / filter（比赛日一条命令定位） | Python | 看 `cmd_filter` + `_normalize_wall_prefix`（F-2） |
| `USAGE.md` | 场下使用方法（AC7）：快速体验/板端自测/行格式图解/5 分钟定位演示/部署样例 | 文档 | 电控队员第一读本 |
| `ERR-CATALOG.md` | 错误码表人读投影（生成物）：场下拿到码→查含义与建议动作 | 文档(生成) | 当字典查 |
| `README.md` | developer 产物区说明（随交付归档的副本） | 文档 | 了解交付方式用 |
| `CODE-STYLE.md` | developer 风格契约 v1.1（解释代码"为什么这样写"的规范依据） | 文档 | 读码前扫 §3/§4 |
| `IMPL-T-20260926-001-….md` | 实现说明：关键决策/轮转协议 v2 推理链/自测时间线/已知风险/T-003 缺陷追记 | 文档 | **读 writer.py 与 rmlog.c 前必读 §2.1 与 §8** |
| `INDEX.md` | developer 交付单元登记表（随交付归档的副本，R0–R3 行） | 文档 | 溯源用 |
| `tests/probe_fdleak_rf6.c` | RF-6 句柄泄漏回归探针（selftest 第 10 用例编译执行） | C | 看文件头 maintainer 补注 |

## 3. 各模块功能（模块 → 输入 → 输出 → 关键函数）

> 行号 = 归档带注版。

### 3.1 catalog（错误码数据源）
- **输入**：无（内嵌表）。**输出**：码表项（code/level/meaning/action）。
- 关键函数：`DOMAINS` 五域定义（catalog.py:29）、`ERRORS` 24 码表体（catalog.py:42）、`get(code)`（catalog.py:127）、`codes_by_domain`（catalog.py:139）、`default_level(code)`（catalog.py:149）。
- 约束：零依赖（不 import 包内其他模块）；改码只能改这里再 `python3 -m rmlog.gen_code` 重新生成两端投影。

### 3.2 format（行格式 v1）
- **输入**：事件字段（seq、两时间戳、level、code、module、message、attrs）。**输出**：一行 `LOGV1|seq|wall|mono|LEVEL|CODE|module|message[|k=v…]`；反向：行→事件字典（不合法返回 None）。
- 关键定义/函数：`PREFIX="LOGV1"`（format.py:47）、`LEVELS`（format.py:50）、**转义表 `_ESCAPES`**（format.py:67）、`_escape`（format.py:78）、`_unescape`（format.py:100）、`wall_timestamp`（format.py:139）、`mono_timestamp`（format.py:158）、`encode`（format.py:167）、`parse_line`（format.py:201）、`level_rank`（format.py:242）。
- 解析三道闸（parse_line）：前缀闸（`LOGV1|` 开头）→ 字段数闸（≥8 段）→ 语义闸（seq 与 mono 为纯 ASCII 数字，`_ASCII_DIGITS` 正则防 Unicode 数字击穿）。

### 3.3 writer（写入端）
- **输入**：单条事件（code/module/message/level/attrs）。**输出**：按行追加到磁盘文件；返回 True/False（绝不抛异常）。
- 关键函数/状态：`Writer.__init__`（writer.py:136，max_bytes=2MiB、keep=5、flush_levels=ERROR/FATAL）、`_resolve_dir`（writer.py:185，/userdata→/var/log 两级裁决）、`_open_append`（writer.py:200）、`_write_once`（writer.py:227，一次写整行+部分写补写一次）、`event`（writer.py:247）、`_posix_write_line`（writer.py:298，**每写即开即关**）、`_win_write_line`（writer.py:329，写锁内整段+**字节锁降级路径**）、`_rotate_if_needed`（writer.py:407，flock 取锁）、`_rotate_step`（writer.py:444，**锁内 stat 确认**）、`_rotate_file`（writer.py:97，纯链操作）、进程级单例 `get_writer`/`set_default_writer`/模块级 `event`（writer.py:508/522/531）。
- 计数器（可观测出口）：`write_failures`（只计真实写失败）、`lock_degradations`（锁相关降级）、`last_error`。

### 3.4 rmlog C 接口（rmlog.h + rmlog.c）
- **输入**：`RMLOG_I/W/E/F(mod, code, fmt, ...)` 宏调用 / `rmlog_emit`。**输出**：与 Python 端同构的行（AC4 字节一致）。
- 关键函数：`rmlog_escape`（rmlog.c:287，与 Python `_ESCAPES` 同表）、`rmlog_line`（rmlog.c:330，同字段序渲染）、`rmlog__wall_ts`/`rmlog__mono_ms`（双端同格式时间戳）、`rmlog__open_locked`（rmlog.c:219，**裁决与打开分离**，RF-6 修复结构）、`rmlog__rotlock_acquire/release`（rmlog.c:423/467 区，POSIX flock / Windows 约定值 -2）、`rmlog__rotate_chain_locked`（rmlog.c:485，链操作，缓冲 528 可证安全）、`rmlog__rotate_locked`（rmlog.c:511，**锁内 stat 确认**）、`rmlog__reopen_current_locked`（rmlog.c:541，fd 对准当前路径）、`rmlog__emit_locked`（rmlog.c:574，写主路径）、`rmlog_emit`（rmlog.c:642）、`rmlog_open/close/flush/path`（rmlog.c:666/706/722/735）。
- 特性测试宏块（rmlog.c:56-58 区）：`#if !defined(_WIN32) #define _POSIX_C_SOURCE 200809L`——**必须在任何 #include 之前**（glibc `<features.h>` 按已定义特性宏决定暴露哪些声明；`-std=c99` 下不预定义则 clock_gettime/localtime_r/fdatasync 被隐藏 → 板端硬错误，T-002 实测、T-003 修复）。

### 3.5 gen_code（生成器）
- **输入**：catalog.ERRORS/DOMAINS。**输出**：`rmlog_errors.h`（宏常量+静态码表）与 `ERR-CATALOG.md`。
- 关键函数：`symbol_for`（gen_code.py:62，`E-INIT-001`→`INIT_001`）、`render_header`（gen_code.py:67）、`render_doc`（gen_code.py:140）、`main`（gen_code.py:190，`--doc` 分支）。

### 3.6 selftest（13 用例自测）
- **输入**：工作区路径（可选）。**输出**：逐用例 PASS/FAIL + `SELFTEST PASS`/`FAIL` + 退出码 0/1。
- 13 用例各自守什么（逐条见 selftest.py:13-28 maintainer 补注；注册表在 selftest.py:645 区 `tests` 列表）：AC2 往返（selftest.py:92）/AC2 残行+fuzz（selftest.py:110）/AC3 码表（selftest.py:134）/AC4 双端一致（selftest.py:278）/AC5 并发（selftest.py:300）/AC5 轮转（selftest.py:336）/AC5×F-1 组合（selftest.py:353）/AC5 读端过滤（selftest.py:433）/AC6 崩溃取证（selftest.py:460）/RF6 句柄守恒（selftest.py:580）/GEN 生成一致（selftest.py:491）/F2 前缀归一（selftest.py:505）/READ CLI 冒烟（selftest.py:564）。
- C 探针链接参数 `_CC_LINK_LIBS`（selftest.py:78）：非 Windows 追加 `-lpthread`（R4）。

### 3.7 rmlog_read（读端）
- **输入**：日志文件 + 过滤条件。**输出**：人读事件流（stdout）+ 残行丢弃计数（stderr）。
- 关键函数：`iter_events`（rmlog_read.py:38，流式解析）、`cmd_parse`（rmlog_read.py:54）、`cmd_tail`（rmlog_read.py:72，--follow 轮询实现）、`_normalize_wall_prefix`（rmlog_read.py:136，**F-2 修复落点**：前缀按日历段归一）、`cmd_filter`（rmlog_read.py:206）、`build_parser`（rmlog_read.py:243）。

## 4. 关键流程（主要执行路径，按步骤标位置）

### 4.1 Python 写一条事件（Linux 主路径）
1. 业务调 `rmlog.event(code, module, message, ...)`（writer.py:531）→ `get_writer()` 单例（writer.py:508）。
2. `Writer.event`（writer.py:247）：level 未给则查 catalog 默认级别（查表失败静默回退 INFO）→ 持线程锁 `self._lock` → `self._seq += 1` → `fmt.encode(...)` 组行。
3. `_write_line`（writer.py:274）→ `_posix_write_line`（writer.py:298）：`open(O_APPEND|O_CREAT|O_WRONLY)`（writer.py:200）→ 一次 `os.write` 整行（writer.py:227）→ level∈{ERROR,FATAL} 时 `fdatasync`（writer.py:215）→ `close`。**全程无跨进程锁**（行完整性由 O_APPEND 单次 write 保证）。
4. 写成功后 `_bytes += len(data)`；超 max_bytes → `_rotate_if_needed`（writer.py:407）：开 `.rmlog.ROTLOCK` → `fcntl.flock(LOCK_EX)`（阻塞式）→ `_rotate_step`（writer.py:444）：**锁内 stat 真实大小**，仍超限才 `_rotate_file`（writer.py:97，删最老→逐段后移→主文件改名 .1），否则把本地计数校准为真实大小；flock 随 close 自动释放。
5. 任何失败：`write_failures`/`lock_degradations` 计数 + 返回 False，不抛异常；下一条事件是全新尝试。

### 4.2 Python 写一条事件（Windows 自测路径）
1~2 同上；3. `_win_write_line`（writer.py:329）：开 ROTLOCK 文件 → `msvcrt.locking` 锁字节 0（**写与轮转共用一把锁**）→ 锁内 open→write→(同步)→close；4. 仍在写锁内判断轮转（锁内不做 stat 确认的对应逻辑由 `_rotate_step` 复用）。
**降级路径**（writer.py:329-382 maintainer 补注）：锁文件 open 失败 / locking 取锁失败 / 解锁失败 → 全部计 `lock_degradations`（不计 `write_failures`，RF-4 口径），降级裸写（数据照常落盘，Windows 并发下可能丢行）；**降级时不轮转**（无锁保护的 rename 链正是丢数据竞争）。

### 4.3 C 端写一条事件（板端 Linux 主路径）
1. 业务调 `RMLOG_E("spi", RMLOG_CODE_COMM_001, "…", args)` → `rmlog_emit`（rmlog.c:642）：`rmlog__init_once`（pthread_once 初始化写锁）→ `vsnprintf` 格式化进 `msg[1024]`（超长截断并计 `g_write_failures`）→ 持全局写锁 → `rmlog__emit_locked`。
2. `rmlog__emit_locked`（rmlog.c:574）：fd 未开 → `rmlog__open_locked`（rmlog.c:219：**裁决段** g_path 为空才做 /userdata→/var/log 两级裁决；**打开段**函数尾部恰好一次 open——RF-6 结构归位）；fd 已开 → `rmlog__reopen_current_locked`（rmlog.c:541：fstat/stat 的 size+inode 对比，fd 绑在他进程已改名的旧 inode 上就关旧重开——协议 v2 写侧配合）。
3. `g_seq++` → `rmlog__wall_ts`/`rmlog__mono_ms` → `rmlog_line`（rmlog.c:330，转义+同字段序 snprintf）→ 追加 `\n` → 一次 `write`（部分写补写一次）。
4. ERROR/FATAL → `RMLOG_FDATASYNC`（rmlog.c:605 区；Linux=fdatasync，其他 POSIX 回退 fsync）——崩溃取证承诺（AC6）。
5. `g_own_bytes > RMLOG_MAX_BYTES` → `rmlog__rotate_locked`（rmlog.c:511）：`rmlog__rotlock_acquire`（rmlog.c:423，flock LOCK_EX；失败计 `g_lock_degradations` 放弃本轮）→ **锁内 stat 确认** → `rmlog__rotate_chain_locked`（rmlog.c:485，副本路径缓冲 `RMLOG_ROTATE_PATH_CAP=528`，最坏输出 524B ≤ 528B，gcc 可证不截断）→ 释放锁。

### 4.4 场下定位（读端）
1. `python3 rmlog_read.py filter <log> --level ERROR --code E-INIT-* --since T14:32 --until T14:38`（rmlog_read.py:206）。
2. `iter_events`（rmlog_read.py:38）流式逐行 `parse_line` 三道闸（format.py:201），残行丢弃计数。
3. 条件 AND：级别（`level_rank` ≥ 给定级）+ 码前缀通配（`E-INIT-*`→`E-INIT-`）+ 时间窗（`_normalize_wall_prefix`（rmlog_read.py:136）把前缀按日历段补齐定宽后字典序比较；until=段末 59.999 / since=段始 00.000——F-2 修复）。
4. 命中行人读打印；stderr 报"丢弃残行 N 条"与"命中 N 条"。

## 5. 数据流与关键状态

- **一行日志**（行格式 v1，唯一权威定义 format.py 模块头）：`LOGV1|<seq>|<墙上时间戳 ISO8601 毫秒>|<单调时间戳 ms>|<LEVEL>|<CODE>|<MODULE>|<message>[|k=v...]`。转义：`\`→`\\`（最先）、`|`→`\x7c`、`\r`→`\x0d`、`\n`→`\x0a`、`\t`→`\x09`、其余 C0/DEL→`\xNN`。解析端逆向还原，残行三道闸丢弃。
- **双时间戳**：墙上时间（`time.time()`/`gettimeofday`，对表、与 journalctl/dmesg 对时间线）+ 单调时间（`time.monotonic()`/`CLOCK_MONOTONIC`，防 NTP 跳变，算事件间隔）。每行都带，缺一不可（CODE-STYLE §4.4）。
- **磁盘布局**：`<dir>/rmlog.log`（当前）+ `rmlog.log.1 … rmlog.log.<keep>`（副本链，最老淘汰）+ `.rmlog.ROTLOCK`（跨进程轮转锁文件，双端同名协议约定，不写数据、永不进副本链）。默认 `<dir>=/userdata/rmlog`，回退 `/var/log/rmlog`（双端一致，Q2 裁决）。
- **C 端全局状态**（单文件单进程一份，全部读写持 `g_lock` 写锁）：`g_fd`（<0=未开）、`g_path[512]`（当前落点，close 后保留——重开落点语义 RF-1）、`g_seq`（仅首次打开清零）、`g_own_bytes`（本进程字节计数，偏小只会偏早触发，被锁内 stat 挡下——失真方向安全）、`g_open_failed`、`g_write_failures`、`g_lock_degradations`、`g_ever_opened`。
- **Python 端实例状态**：`self._seq/_bytes/_lock`、`write_failures`/`lock_degradations`/`last_error`；进程级单例 `_default_writer`。
- **生命周期**：事件 → `encode` 组行 → 一次 write 进内核页缓存 →（ERROR/FATAL 才 fdatasync）→ 字节计数 → 超限轮转。INFO/WARN 依赖页缓存回写（断电窗口=最近几条非关键行，IMPL §4 声明）。

## 6. 依赖与外部接口

- **运行依赖**：Python 3 标准库（零第三方依赖——板端不可假设 pip/外网）；C99 + POSIX（pthread/flock/fdatasync/clock_gettime/localtime_r，由特性宏 `_POSIX_C_SOURCE 200809L` 在 glibc 下解锁）；Windows 自测分支用 msvcrt/CriticalSection/INIT_ONCE 等效实现。
- **外部接口（被依赖）**：业务 C 代码 include `rmlog.h` 用宏族；业务 Python `import rmlog` 用 `event()`；读端 CLI 供人/脚本使用；错误码常量 `RMLOG_CODE_*` 由生成头提供（跨端接口，禁手改）。
- **部署约束**（advisory 锁前提）：同一日志目录的所有写入方必须都经本组件（C/Python 双端同名锁文件 `.rmlog.ROTLOCK`）；混用相同 keep/max_bytes 配置；`rmlog__dir_usable` 仅单级建目录（深层目录部署方预建，P1 升级项）。
- **平台边界**：C 端 Windows 无跨进程轮转锁（约定值 -2，不计数），多进程×轮转组合语义完整形态在 Linux；fdatasync 为 Linux 特性，其他 POSIX 回退 fsync。

## 7. 构建与运行方式（已实际核实）

**Python 自测（全量 13 用例）**：
```
cd <产物目录>          # 归档对应 developer/script
python3 -m rmlog.selftest
# 期望末行 SELFTEST PASS、退出码 0（自测临时产物缺省落 script/tests/_work，跑完自清理）
```
**C 编译（文档命令原样，R4 后双端可编译）**：
```
gcc -std=c99 -Wall -Wextra -o example rmlog/example.c rmlog/rmlog.c -lpthread   # 板端/Linux
gcc -std=c99 -Wall -Wextra -o example.exe rmlog/example.c rmlog/rmlog.c          # Windows/MinGW（无 -lpthread）
./example <日志目录>    # 板端可省略参数走默认裁决 /userdata/rmlog
```

**核实证据（三级）**：
1. **maintainer 本机独立复验（2026-09-28，Windows 11 x64 · Python 3.14.7 · gcc 13.2.0 MinGW-w64）**：以 `git archive 164d4c7` 签出副本（非工作区）实跑 `python -m rmlog.selftest` → **13/13 PASS，退出码 0，用时 44.9s**；带注 `rmlog.c` 以 `gcc -std=c99 -Wall -Wextra -c` 编译 → **退出码 0、stderr 0 字节**。证据来源：maintainer 会话执行记录（本次归档任务内，输出留存于 maintainer 执行日志）。
2. **developer 留档**：`developer/script/tests/selftest-20260927-2208-r4.log`（R4 末轮 13/13 PASS，43.8s，退出码 0；IMPL §8.3）。
3. **板端实测（software_tester，aarch64 gcc 11.2.0 / Ubuntu 22.04）**：`software_tester/script/TESTREPORT-T-20260927-003-001.md` — R-Q1 selftest 13/13 全 PASS（退出码 0，含 AC4/RF6 两 C 探针 `-lpthread` 链接执行成功）、R-Q4 `gcc -std=c99 -Wall -Wextra -c rmlog.c` 退出码 0 且 stderr 0 字节、R-Q3 多进程×轮转对账无回归。

## 8. 术语表

见 `maintainer/script/GLOSSARY.md`（项目级、跨版本累积）。核心词：rmlog / 错误码五域（INIT/COMM/HW/FSM/SYS）/ 行格式 v1（LOGV1）/ 双时间戳 / 轮转协议 v2 / ROTLOCK / O_APPEND / 特性测试宏 / advisory 锁 / 残行三道闸 / write_failures 与 lock_degradations 的口径区分 / RF-6 / 可证安全（528 缓冲）。

## 9. 已知关注点（**事实摘录，标注来源，不自行判定**）

**已修复（历史发现项，修复经复审核销）**：
- F-1【严重】多进程×轮转数据静默销毁（旧协议 fd 搁浅旧 inode）——REVIEW-…-f3331b0.md §5；R1 轮转协议 v2 修复核销——REVIEW-…-45eeb04.md。
- F-2【严重】读端 `--until` 分钟前缀漏掉该分钟全部事件——REVIEW-…-f3331b0.md；R1 前缀归一修复核销。
- F-3~F-9（一般/提示级：自测表述失准、复现命令断链、reopen 失败不计数、CODE-STYLE 漂移、锁降级不可观测、close 语义注释失实、C 端容量表述缺口）——同报告，R1 核销。
- RF-1【一般】close 后重开落点对显式目录失实（probe_c2 实证）——REVIEW-…-45eeb04.md §6；R2 修复（g_path 复用）。
- RF-2/3/5【提示】810 vs 813 笔误 / docstring keep=10 残留 / C 端锁失败无计数——同报告；R2 核销。
- RF-4【一般】Windows 写锁 open 失败误计 write_failures（40 条全成功却计 40 失败）——REVIEW-…-45eeb04.md §6；R2 改道 lock_degradations。
- RF-6【严重】`rmlog__open_locked` 双重 open 句柄泄漏（1000 轮实测 +1000）——REVIEW-…-rf-a675c8d.md §6（该轮整体 FAIL 的原因）；R3 结构归位修复核销（三重口径+句柄前后对照 `tests/probe_fdleak_rf6_before_after.log`）——REVIEW-…-rf6-2d83644.md。
- T-003 缺陷【板端实测】严格 `-std=c99` 下 glibc 隐藏 POSIX 声明致 rmlog.c 在 aarch64 板端无法编译 + 3× `-Wformat-truncation`——TESTREPORT-T-20260927-002-001 Q4；R4 修复（特性宏 + 528 缓冲）核销——REVIEW-T-20260927-003-164d4c7.md §5，板端复测全绿。

**未返工/遗留（摘录）**：
- NIT-1【提示，不要求返工】`_POSIX_C_SOURCE` 未用 `#ifndef` 保护：若构建系统全局另传 `-D_POSIX_C_SOURCE=<其他值>` 会触发重定义告警；正常文档命令无此场景——REVIEW-T-20260927-003-164d4c7.md §7.1。
- 审查侧 unverified 承接：UV-1（协议 v2 Linux 实际行为）、UV-2（C 端 Linux flock 路径实测）、UV-3（工具链告警）、UV-4（板端环境形态）、UV-5（fdatasync 持久化边界）——REVIEW-…-rf-a675c8d.md §6。其中 UV-1/UV-3 的关键面已由 T-003 板端复测坐实（selftest 13/13、gcc 零告警）；**UV-5（断电/掉电破坏性实测）与 UV-2（flock 竞争轮转专测）仍未覆盖**——TESTREPORT-T-20260927-003-001 §7。
- tester 未覆盖项（TESTREPORT-T-20260927-003-001 §7 + HANDOFF §5）：Q2 全量平台核查未重复（沿用 T-002 采集，平台未变）；clang 编译（板端无 clang）；断电/掉电恢复（UV-5）；C 端 Linux flock 竞争轮转专测（UV-2，仅由 selftest RF6 用例间接覆盖）；大压力/长时稳定性。
- ACCEPT §3.2 遗留项（不阻断验收，已排程 P1）：AC4 一致性范围=无属性行（C 端 attrs 属 P1）；C 端 mkdir -p 等效、INFO-3 计数器读取出口属 P1；clang；UV-5/UV-2 板端项；**coredumpctl 板端不可用 → P1 崩溃取证需换方案**——management/script/ACCEPT-20260927-logging-p0.md §3.2。
- 平台表述纪律：Windows 自测结论不得表述为 Linux 已验证（IMPL §4；现板端实测已覆盖 selftest/编译/组合对账，但 fdatasync 持久化等破坏性场景仍无实测）。

## 10. 未解疑问（`unverified`——maintainer 读码后如实列出，禁止省略；不构成质量判定）

1. **UQ-1（unverified）Python 端 flock 阻塞无超时上界**：`_rotate_if_needed` 用阻塞式 `fcntl.flock(LOCK_EX)`（writer.py:430 区）。代码事实=取锁会阻塞到获得为止；推断=若某进程在轮转链操作中异常滞留（如磁盘 IO 停顿），其他进程的 event() 会阻塞在轮转段，最坏阻塞时长没有上界承诺。该阻塞是否在真实部署出现、时长量级如何，无实测数据。
2. **UQ-2（unverified）降级路径长期不轮转的增长边界**：Windows 降级（未持锁）不轮转（writer.py:357-358），Linux 端 flock 失败同样放弃本轮轮转（writer.py:421-424 区）。数据不丢（明确承诺），但推断=锁长期不可用时主文件会持续增长、保留期失真；持续多久的增长量级无实测。
3. **UQ-3（unverified）C 端 Windows fd 对准用 size 近似 inode**：`rmlog__reopen_current_locked` 在 Windows 分支仅比 size 不比 inode（rmlog.c:541-563 区，代码注释自认"无可靠 inode"）。事实=Windows 上 C 端不参与跨进程轮转（部署形态保证）；该近似在何种非标准部署下可能误判、后果如何，未验证。
4. **UQ-4（unverified）双端毫秒取整策略差异**：Python `wall_timestamp` 用 `int(round(...))`（Python3 银行家舍入，format.py:139-152），C 端 `tv.tv_usec / 1000` 整除截断（rmlog.c:346-348 区）。事实=两处取整策略不同；推断=仅影响"双端各自取时间"场景下微秒恰在 500 边界的同一事件毫秒可能差 1ms，AC4 对照用固定输入不受影响。是否需要统一、真实影响面，未验证。
5. **UQ-5（unverified）catalog 导入失败静默回退 INFO 无计数**：`Writer.event` 查默认级别失败时静默回退 INFO（writer.py:254-261），该降级不计入任何计数器、不写 last_error。事实=此路径不可观测；是否需要可观测出口属设计取舍，无裁定记录。
6. **UQ-6（unverified）`rmlog__rotate_locked` 的 stat 失败窗口**：stat 抛错（如文件恰被他进程 rename 的瞬间）时两个分支都不进入，`g_own_bytes` 不校准（rmlog.c:511-535 区）。事实=该窗口计数保持陈旧值；后续影响（会偏早触发下一次轮转裁决，再被锁内 stat 挡下？）是读码推断，未实测。
7. **UQ-7（unverified）fuzz 覆盖完备性**：AC2 fuzz 用固定种子 42 跑 300 次（selftest.py:110-132 区）。事实=单一种子的非穷尽采样；对"任意字节解析不抛异常"承诺的覆盖置信度无形式化依据（属测试设计取舍，非缺陷指控）。

## 11. 事实层与推断层的分离声明

- **【事实】**=代码确实这么写、或三方报告书面记载的内容：本文 §2/§3/§4/§5 的全部结构与流程描述（读自 `code/` 与来源 commit 164d4c7）；§7 的命令与三级核实证据（selftest 13/13 与编译零告警，本机独立复验 + developer/tester 留档）；§9 全部发现项与未覆盖项（逐条标注 reviewer/tester/management 报告来源）。
- **【推断】**=maintainer 基于代码与注释推断的设计意图或影响面，均已在文中显式标注"推断"或"unverified"：各设计动机（如"每写即开即关是为了根除 fd 搁浅"在模块头有作者自述者为事实，maintainer 转述的未尽影响为推断）；§10 UQ-1~UQ-7 全部为推断层，**均无实测数据支撑**。
- **本角色不对代码质量做任何判定**（KN4）：§9 仅转述三方报告结论；本文任何"为什么这样设计"若无作者注释或报告佐证，一律标注推断。
- 引用代码位置时同时给出：**来源 commit `164d4c7` + 归档版本 001**；两者内容差异仅限 130 行新增注释（VERSION-001 §6），审查/测试基准以来源 commit 为准。
