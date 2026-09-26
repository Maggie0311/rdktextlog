# IMPL — T-20260926-001-logging-platform-p0 实现说明

| 字段 | 值 |
|---|---|
| task_id | T-20260926-001-logging-platform-p0 |
| 主责 | developer (R-003)（本会话上岗执行；前次中断的同任务产物已核验后并入） |
| 交付日期 | 2026-09-26 |
| 需求依据 | `management/script/REQ-20260926-001-logging.md`（§4 P0-a~f、§6 AC1–AC8、§7.1 裁决） |
| 任务书 | inbox MAIL-…1620（主）+ MAIL-…1640（增补：证据形态/板端自测章节） |

## 1. 改动清单（交付物全集，均在 `developer/script/`）

| 路径 | 内容 | AC 关联 |
|---|---|---|
| `CODE-STYLE.md` | v1.0 风格契约（含 rmlog 特化可靠性约定）；v1.1: 自测工作区约定 | 通用 |
| `rmlog/__init__.py` | 包入口 + `encode_line` 显式参数包装（AC4 对照用） | AC1 |
| `rmlog/catalog.py` | 错误码**单一数据源**（五域 24 码，含默认级别/含义/建议动作） | AC3 |
| `rmlog/format.py` | 行格式 v1 唯一权威定义（转义规则/双时间戳/解析三道闸） | AC2 |
| `rmlog/writer.py` | 写入端（O_APPEND 一次一行、条件 flush、按大小轮转、静默降级、进程级单例） | AC5/AC6 |
| `rmlog/worker.py` | 多进程并发压测工作进程（selftest 专用） | AC5 |
| `rmlog/gen_code.py` | 生成器：catalog → `rmlog_errors.h`（C 头）与 `ERR-CATALOG.md`（文档） | AC3 |
| `rmlog/rmlog_errors.h` | **生成物**（勿手改）：C 端码表/级别常量/静态表 | AC3/AC4 |
| `rmlog/rmlog.h` `rmlog/rmlog.c` | C 接口：RMLOG_I/W/E/F 宏族、线程安全、行编码与 Python 同构 | AC4 |
| `rmlog/example.c` | C 最小示例（四级事件各一条） | AC1 |
| `rmlog/encode_cases.py` | AC4 用例集与二进制传输编解码（开发机自测专用） | AC4 |
| `rmlog/_ac4_probe.c` | AC4 C 探针（selftest 运行时生成，读二进制用例→渲染→写二进制输出） | AC4 |
| `rmlog/selftest.py` | 自测入口（10 用例，覆盖 AC2–AC6 + 附加） | AC1 |
| `rmlog_read.py` | 读端工具：parse/tail/filter（--level/--code 前缀通配/--since/--until） | AC5 |
| `USAGE.md` | 场下使用方法（含「板端自测步骤（用户执行）」一等章节） | AC7 |
| `tests/selftest-*.log` | 自测原始输出留档（含修复过程各轮，最终轮 10/10 PASS） | AC1 |
| `INDEX.md` | 交付单元登记 | 通用 |

## 2. 关键决策与理由

1. **同源机制**（P0-a）：错误码唯一数据源 = `catalog.py` 内嵌表；C 头与错误码文档均为**生成物**
   （`python3 -m rmlog.gen_code` / `--doc`）。理由：任何"两处手写"都会漂移，生成链路让三份投影
   （Python 表 / C 头 / 文档）天然一致，selftest 对此有断言。
2. **行格式 v1 转义选编码替换而非引用转义**（P0-b）：`|`→`\x7c`、换行→`\x0a`、控制字符→`\xNN`。
   理由：解析端零状态机、C 端实现简单、肉眼可读；引用转义（`\\|`）要求扫描状态机，C 端易错。
3. **多进程行完整性**（P0-d）：一条完整行一次 `write()`。Linux 上 `open(2)` 的 O_APPEND 是
   内核级原子追加（目标平台 X5 的主路径，零额外开销）；**Windows CRT 的 `_O_APPEND` 是
   "写前 seek"，跨进程不原子** —— 为让开发机自测能等效演示，Windows 路径在写入前对文件
   字节 0 加 `msvcrt.locking` 锁串行化（纯标准库），Linux 路径不经过该分支（`os.name=="nt"` 恒假）。
   这是本轮自测发现的真缺陷（修复前 4×250 并发丢 89 行），已修复并复测通过。
4. **flush 策略**（P0-d）：ERROR/FATAL 每条写后立即 fdatasync（`fsync=True` 可升级强持久化，
   接口预留默认关）；INFO/WARN 依赖页缓存回写，`close()`/手动 `flush()` 兜底。理由：1kHz 场景
   每条 fsync（约 1–10ms）不可承受；"关键证据先落盘"与"非关键路径短"分开对待。
5. **C/Python 一致性验证方法**（AC4）：时间等输入由用例**固定注入**（消除双端各自取时间的差异），
   C 探针读二进制用例文件渲染后与 Python 端逐字节对照。一致性范围 = 行的无属性形态
   （C 宏族 P0 不含 attrs 参数；属性转义规则已由 AC2 Python 往返覆盖，C 端 attrs 属 P1 扩展）。
6. **默认目录裁决**（Q2）：`/userdata/rmlog`（存在或可建）→ 回退 `/var/log/rmlog`，双端行为逐字一致。
7. **写失败静默降级**：日志故障绝不打断比赛业务；`write_failures`/`last_error` 计数器是可观测出口
   （selftest 主动检查）。

## 3. 验证方式与原始输出摘要（开发机 Windows；板端证据见 §5）

环境：Windows 10 x64 · Python 3.13/3.14（本次 3.14.7 实跑）· gcc 13.2.0 (MinGW-w64) · git 2.53。

**最终自测（全量通过，日志 `tests/selftest-20260926-2020-final.log`）**：

```
  PASS  AC2 roundtrip(转义/属性/双时间戳)
  PASS  AC2 残行三道闸 + 随机字节 fuzz(300 次, 解析不抛异常)
  PASS  AC3 五域 INIT/COMM/HW/FSM/SYS 共 24 码(字段完整/无重复)
  PASS  AC4 双端 7 个用例逐字节一致(含|/换行/控制字符/中文)
  PASS  AC5 多进程并发 4x250=1000 行无丢行/无交错
  PASS  AC5 轮转触发, 副本数 3 (2<=n<=keep=3), 最老已淘汰
  PASS  AC5 读端一条命令 --level ERROR --code E-INIT-* 命中 2/5
  PASS  AC6 硬崩溃(os._exit)后最后一条 ERROR/FATAL 事件可读
  PASS  GEN 生成头/文档与 catalog 单一来源一致
  PASS  READ parse/tail CLI 冒烟
自测结束: 10/10 通过, 用时 5.3s
SELFTEST PASS          （退出码 0）
```

复现命令：
```
cd developer/script
python -m rmlog.selftest
gcc -std=c99 -Wall -Wextra -I rmlog -o tests\_work\example.exe rmlog\example.c rmlog\rmlog.c
tests\_work\example.exe tests\_work\demo3
```

C 示例真实运行输出（`tests/_work/demo3/rmlog.log`）：
```
LOGV1|1|2026-09-26T20:16:57.032|361818154|INFO|E-INIT-000|ctrl|上电自检完成, 进入待机 state=1
LOGV1|2|2026-09-26T20:16:57.032|361818155|WARN|E-HW-005|pwr|电池电压接近下限 v=22500mV
LOGV1|3|2026-09-26T20:16:57.032|361818155|ERROR|E-COMM-001|spi|SPI 传输超时 dev=/dev/spidev0.0 retry=3
LOGV1|4|2026-09-26T20:16:57.034|361818156|FATAL|E-FSM-004|fsm|状态机进入未定义状态 st=7
```
与 Python 端写同组事件输出**结构逐字段一致**（仅时间戳/序号本身不同）。

## 4. 已知风险与未覆盖项（诚实清单）

1. **平台差异（最重要）**：
   - Windows 自测结论**不得表述为 Linux 已验证**。多进程安全在两平台的实现路径不同
     （Linux=内核 O_APPEND 原子；Windows=开发机专用的字节锁串行化）；板端以 §5 用户实测为准。
   - C 端 `rmlog__dir_usable` 仅单级创建；`/userdata` 若是多级深层路径需部署方预先建目录
     （USAGE §6 已注明；板端实际层级属未核实项）。
   - `fdatasync` 为 Linux 特性，其他 POSIX 工具链回退 `fsync`（多刷元数据，语义不变）。
2. **断电窗口**：INFO/WARN 滞留页缓存，硬断电可能丢最近几条非关键行；ERROR/FATAL 已强制
   fdatasync。绝对零丢失需逐条 fsync（1kHz 不可承受），损失边界见 USAGE §8。
3. **消息长度上限**：C 端单条 1024 字节（截断计数不崩溃）；Python 端无硬限。
4. **单文件全局状态**（C 端）：一个进程一份日志上下文（单文件）；多文件需求属 P1。
5. **覆盖声明**：未测项 = 板端实机行为（python3 版本/`/userdata` 存在性/O_APPEND 板端原子性/
   journald 持久化/rsyslog 形态/coredump 可用性/dmesg 时间戳格式）；`--follow` 的长时间跟踪、
   1kHz 高频写入压测、日志尺寸真实上限（数 GB 级）——均超出 P0 范围或依赖板端。
6. **构建/运行遗留**：无（开发机构建零警告零错误；`-Wall -Wextra` 下警告视为失败已入 selftest）。

## 5. 板端未核实项清单 + 用户探测命令（AC8，按 Q1=A 裁决执行）

| 未核实项 | 探测命令（在 X5 上执行，输出随 §3 板端自测一并回贴） |
|---|---|
| python3 版本 | `python3 --version` |
| /userdata 分区存在性 | `ls -ld /userdata 2>/dev/null; df -h /userdata 2>/dev/null` |
| journald 持久化 | `ls /var/log/journal 2>/dev/null && echo persistent || echo volatile` |
| rsyslog 形态 | `ls /var/log/syslog 2>/dev/null; systemctl is-active rsyslog 2>/dev/null` |
| coredump 可用性 | `coredumpctl list 2>&1 | head -5` |
| dmesg 时间戳格式 | `sudo dmesg --time-format iso | tail -3` |
| 板端自测结果 | `cd ~/rmlog && python3 -m rmlog.selftest; echo EXIT=$?`（USAGE §3 全流程） |

## 6. 未解疑问（不阻塞验收，供管理侧决策）

1. `rmlog__dir_usable` 的单级创建限制是否需要升级为逐级创建（`mkdir -p` 等效）？
   现状已在 USAGE/本文注明；若板端 `/userdata` 层级复杂则 P1 升级。
2. C 端 attrs 支持（`RMLOG_I` 宏族带 k=v 参数）安排在 P1 —— 若业务接入提前需要，请 management
   下发增补任务。

## 7. 提交信息

- 提交隔离：按路径显式添加本轮文件（契约 §2.1.2）；发现他方（management）未提交改动，
  不触碰，并在此 NOTIFY：**management 名下有未提交改动（memory/PROJECT-BOARD/worklog 及
  from_human 原件），请其自行提交**。
- commit hash 与产物以 INDEX.md 登记为准（审查/验收以该 hash 为基准）。
