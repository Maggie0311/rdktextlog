# IMPL — T-20260926-001-logging-platform-p0 实现说明

| 字段 | 值 |
|---|---|
| task_id | T-20260926-001-logging-platform-p0 |
| 主责 | developer (R-003)（本会话上岗执行；前次中断的同任务产物已核验后并入） |
| 交付日期 | 2026-09-26（R0 首交付）；2026-09-27（R1 整改返工，commit 见 §7 / INDEX） |
| 需求依据 | `management/script/REQ-20260926-001-logging.md`（§4 P0-a~f、§6 AC1–AC8、§7.1 裁决） |
| 任务书 | R0: inbox MAIL-…1620 + MAIL-…1640；R1: inbox MAIL-20260927-0922（F-1~F-9 整改书） |
| 关联审查 | `code_reviewer/script/REVIEW-T-20260926-001-f3331b0.md`（结论 CONDITIONAL，F-1~F-9 逐条整改见 §1.1） |

## 1. 改动清单（交付物全集，均在 `developer/script/`）

| 路径 | 内容 | AC 关联 |
|---|---|---|
| `CODE-STYLE.md` | v1.1 风格契约（v1.0 基础上 §5 增补"自测工作区约定"，F-6） | 通用 |
| `rmlog/__init__.py` | 包入口 + `encode_line` 显式参数包装（AC4 对照用） | AC1 |
| `rmlog/catalog.py` | 错误码**单一数据源**（五域 24 码，含默认级别/含义/建议动作） | AC3 |
| `rmlog/format.py` | 行格式 v1 唯一权威定义（转义规则/双时间戳/解析三道闸） | AC2 |
| `rmlog/writer.py` | 写入端（O_APPEND 一次一行、条件 flush、轮转协议 v2、静默降级、进程级单例）；R1 重构轮转（F-1/F-5/F-7） | AC5/AC6 |
| `rmlog/worker.py` | 多进程并发压测工作进程（selftest 专用）；R1 增 keep 参数 | AC5 |
| `rmlog/gen_code.py` | 生成器：catalog → `rmlog_errors.h`（C 头）与 `ERR-CATALOG.md`（文档） | AC3 |
| `rmlog/rmlog_errors.h` | **生成物**（勿手改）：C 端码表/级别常量/静态表 | AC3/AC4 |
| `rmlog/rmlog.h` `rmlog/rmlog.c` | C 接口：RMLOG_I/W/E/F 宏族、线程安全、行编码与 Python 同构；R1 轮转协议 v2 + reopen 可重试（F-1/F-5）+ 容量注释（F-9） | AC4 |
| `rmlog/example.c` | C 最小示例（四级事件各一条） | AC1 |
| `rmlog/encode_cases.py` | AC4 用例集与二进制传输编解码（开发机自测专用） | AC4 |
| `rmlog/_ac4_probe.c` | AC4 C 探针（selftest 运行时生成，读二进制用例→渲染→写二进制输出） | AC4 |
| `rmlog/selftest.py` | 自测入口（R1 起 12 用例：AC2–AC6 + F-1 组合对账 + F-2 前缀回归 + 附加） | AC1 |
| `rmlog_read.py` | 读端工具：parse/tail/filter；R1 增时间前缀归一（F-2） | AC5 |
| `USAGE.md` | 场下使用方法；R1 修正 §2 复现命令（F-4）与 §5 时间窗示例语义（F-2） | AC7 |
| `tests/selftest-*.log` | 自测原始输出留档（含修复过程各轮，R1 末轮 12/12 PASS） | AC1 |
| `INDEX.md` | 交付单元登记 | 通用 |

### 1.1 R1 返工处置索引（F-1~F-9，逐条对应审查报告 §5）

| 发现项 | 级别 | 处置摘要（详细位置见 §2.1/复审请求信） |
|---|---|---|
| F-1 多进程×轮转数据销毁 | 严重 | **已修**：轮转协议 v2（每写即开即关 + flock/写锁跨进程轮转互斥 + 锁内 stat 确认），双端同协议；selftest 新增组合对账用例 |
| F-2 `--until` 分钟前缀漏事件 | 严重 | **已修**：读端时间前缀归一（前缀=日历段语义，全精度值不变），USAGE §5 同步，selftest 回归用例 |
| F-3 "最终自测"标注失准 | 一般 | **已修**：§3 重写自测时间线（末轮 PASS=R1 的 20260927 轮，2035/2042 两轮 FAIL 时点与结论如实注明） |
| F-4 复现命令断链 | 一般 | **已修**：§3 与 USAGE §2 命令补 `mkdir` 步骤 |
| F-5 reopen 失败不计数/抛异常 | 一般 | **已修**：C 端计数+逐条重试；Python 端全程不抛异常（每条事件独立尝试） |
| F-6 CODE-STYLE 版本漂移 | 一般 | **已修**：升 v1.1，§5 增补自测工作区约定（显式例外化 `_work`） |
| F-7 锁降级不可观测 | 一般 | **已修**：Writer 增 `lock_degradations` 计数 |
| F-8 rmlog.h close 语义失实 | 提示 | **已修**：头注释改为"close 后 emit 按需重开继续记录"（改注释不改行为） |
| F-9 C 端容量表述缺口 | 提示 | **已修**：rmlog.c 头注释与本文件 §4.3 补真实边界（转义后 2048 上限、超限整条丢弃计数） |

## 2. 关键决策与理由

1. **同源机制**（P0-a）：错误码唯一数据源 = `catalog.py` 内嵌表；C 头与错误码文档均为**生成物**
   （`python3 -m rmlog.gen_code` / `--doc`）。理由：任何"两处手写"都会漂移，生成链路让三份投影
   （Python 表 / C 头 / 文档）天然一致，selftest 对此有断言。
2. **行格式 v1 转义选编码替换而非引用转义**（P0-b）：`|`→`\x7c`、换行→`\x0a`、控制字符→`\xNN`。
   理由：解析端零状态机、C 端实现简单、肉眼可读；引用转义（`\\|`）要求扫描状态机，C 端易错。
3. **多进程行完整性**（P0-d）：一条完整行一次 `write()`。Linux 上 `open(2)` 的 O_APPEND 是
   内核级原子追加（目标平台 X5 的主路径）；**Windows CRT 的 `_O_APPEND` 是"写前 seek"，
   跨进程不原子** —— Windows 路径在写锁内完成"open→write→close"串行化（纯标准库），
   Linux 路径不经过该分支（`os.name=="nt"` 恒假）。
   这是 R0 自测发现的真缺陷（修复前 4×250 并发丢 89 行），已修复并复测通过。
4. **flush 策略**（P0-d）：ERROR/FATAL 每条写后立即 fdatasync（`fsync=True` 可升级强持久化，
   接口预留默认关）；INFO/WARN 依赖页缓存回写。理由：1kHz 场景每条 fsync（约 1–10ms）
   不可承受；"关键证据先落盘"与"非关键路径短"分开对待。
5. **C/Python 一致性验证方法**（AC4）：时间等输入由用例**固定注入**（消除双端各自取时间的差异），
   C 探针读二进制用例文件渲染后与 Python 端逐字节对照。一致性范围 = 行的无属性形态
   （C 宏族 P0 不含 attrs 参数；属性转义规则已由 AC2 Python 往返覆盖，C 端 attrs 属 P1 扩展）。
6. **默认目录裁决**（Q2）：`/userdata/rmlog`（存在或可建）→ 回退 `/var/log/rmlog`，双端行为逐字一致。
7. **写失败静默降级**：日志故障绝不打断比赛业务；`write_failures`/`last_error` 计数器是可观测出口
   （selftest 主动检查）。R1 增 `lock_degradations`（锁降级可观测，F-7）。

### 2.1 轮转协议 v2（R1 新增，F-1 修复方案；双端同协议）

**旧协议缺陷**（R0，reviewer 实证）：每进程常驻 fd 持续追加 → 超限 close → rename 链 →
reopen。对其他进程的 fd 与计数零感知：A 进程把 `rmlog.log` 改名进副本链后，B 进程的 fd
仍绑在旧 inode 上继续写；B 后续轮转把这段新近数据连同旧 inode 一起挪进副本链、再被
"删最老副本"当作垃圾淘汰 —— B 已确认写成功（event 返回 True）的事件从磁盘上完全消失
（probe_1e/1g 双次复现；同负载不轮转对照 600/600 完好）。

**v2 方案**（实现细节与逐行注释见 `writer.py` 模块头 / `rmlog.c` 轮转段）：

1. **每写即开即关（Python 端全部平台；根上消除搁浅 fd）**：每条事件按路径
   `open(O_APPEND) → 一次 write 整行 → close`，无常驻 fd。写入目标必然是"open 那一刻
   路径所指的文件"，它此后只会沿 `path → .1 → ... → .keep` 被 rename —— 一条已落盘的行
   至少要再经历 keep 次完整轮转（每轮至少 max_bytes 新数据）才会被淘汰，与单进程保留
   语义一致，不存在"整文件被当垃圾删"的通道。代价：每条事件多 2 次系统调用（µs 级），
   1kHz 场景可接受，换来组合场景的数据不灭失。
2. **跨进程轮转互斥（rename 链对并发轮转原子）**：链操作全程持目录锁 `.rmlog.ROTLOCK`
   （与日志同目录，不写数据、不进副本链，双端同名 = 协议约定）：
   - Linux/X5（板端主路径）：`fcntl.flock(LOCK_EX)`（advisory 锁，互斥前提 = 同目录所有
     写入方都经本组件 —— 比赛部署形态成立；flock 随 close 自动释放）；
   - Windows（开发机）：复用跨进程写锁（`msvcrt.locking` 锁锁文件字节 0），写与轮转共用
     一把锁，rename 链对并发写原子；
   - C 端 Windows：无 flock，退化为"进程内轮转"（跨进程组合演示由 Python 端覆盖），
     属部署行为差异，见 §4.1。
3. **锁内 stat 确认（消除过早轮转）**：拿到轮转锁后按**真实文件大小**裁决（本进程自计
   字节不含他进程写入，必然偏小、只会偏早触发；真实大小仍 > max_bytes 才轮转，否则
   校准本地计数）——他进程刚轮转过时本进程不再触发轮转，保留期不失真。
4. **C 端写侧配合**：C 端保持常驻 fd（低开销主路径），每次 emit 前 fstat/stat 对比
   fd 所指文件与当前路径的 inode/size，不一致（被他进程轮转改走）即关旧 fd、重开当前
   路径 —— 落点永远对准当前文件；reopen 失败按 F-5 语义计数并可重试。

**修复后承诺**（selftest `test_ac5_concurrent_rotation` 逐 worker 对账）：
多进程×轮转组合下，任何 event() 返回 True 的事件，其完整行必然能在轮转链
（rmlog.log + .1 ... .keep）的某一文件中读到；链之外的磁盘位置永不承载本组件写入的数据；
每行一次 write 不拆分（无半行交错）。

**Linux 行为推演声明（unverified，诚实备案）**：上述机制在 Linux/X5 上的结论来自对
POSIX 语义的逐调用推演，**未经板端实测**。推演依据：
- `open(O_APPEND)`：内核级原子追加，单次 write 行原子（Linux `open(2)`/`write(2)` 语义）；
- 每写按路径 open：fd 只指向 open 那一刻 path 所指 inode；此后该文件仅被 rename
  （POSIX rename 对被打开文件同样生效，fd 与内容随 inode 走，这正是"行至少随链保留
  keep 轮"的依据），不存在 Windows 的"目标被占用即 rename 失败"问题；
- `flock(LOCK_EX)`：同目录各进程对同一锁文件互斥，链操作串行；flock 是 advisory 锁，
  若部署中存在不经本组件的写入方，互斥前提失效（已写入 §4.1 部署约束）；
- 板端实测由用户按 USAGE §3 自测清单执行（Q1=A 裁决），建议增测多进程×轮转组合
  （命令形态同 selftest 的 `python3 -m rmlog.worker <dir> 300 8000 20` ×2 并行）。
  在该实测回贴之前，本组合的 Linux 行为一律按 unverified 表述。

## 3. 验证方式与原始输出摘要（开发机 Windows；板端证据见 §5）

环境：Windows 10 x64 · Python 3.13/3.14（R1 实跑 3.14.7）· gcc 13.2.0 (MinGW-w64) · git 2.53。

**自测时间线（R1 重写 —— 修正审查报告 F-3 指出的表述失准；全部留档可查）**：

| 轮次（文件名时间戳） | 结果 | 说明 |
|---|---|---|
| 20260926-1958 | FAIL | Python SyntaxError（R0 修复迭代第 1 轮） |
| 20260926-2002 | FAIL | C 探针编译失败（R0 第 2 轮） |
| 20260926-2020-final | PASS 10/10 | R0 第 3 轮；**R0 交付时点它并非末轮**（F-3 指出的失准所在） |
| 20260926-2035 | **FAIL 9/10** | R0 第 4 轮（AC5 并发丢行 89/1000）；commit f3331b0（20:22）之后发现 |
| 20260926-2042 | **FAIL 9/10** | R0 第 5 轮（AC5 丢行 911/1000，迭代中） |
| 20260926-2055 | PASS 10/10 | **R0 真正的末轮 PASS**（修复=Windows 字节锁路径补齐；R0 的 IMPL 曾把 2020 轮误标"最终"，已按本轮修正） |
| 20260927-1010-r1 | **FAIL 10/12** | R1 第 1 轮：两个新用例 FAIL —— F-1 组合用例误报（参数 keep=10 过小，触发**正常保留淘汰**而非数据销毁，见下）+ F-2 用例期望值写反 |
| 20260927-1028-r1 | **PASS 12/12** | **R1 末轮 PASS**（修复=组合用例 keep 提至 20 保证轮转次数 < 链槽位；F-2 用例改为正确的日历语义断言）|

R1 迭代说明（诚实记录）：20260927-1010 轮的 F-1 FAIL 经临时诊断脚本定位 —— 磁盘可见
810/1200 行**全部是链容量淘汰**（1200 行 ≈ 15 次轮转 > keep=10 的 11 个槽位），对账
缺失区间恰为最早写入的整文件，属正常容量治理而非协议销毁；将 keep 提至 20（槽位 21 >
15 次轮转）后全量对账通过。该轮诊断脚本为临时件，未入库；结论经 1028 轮复跑证实。

**R1 末轮自测输出摘要（`tests/selftest-20260927-1028-r1.log`，12/12 PASS，退出码 0）**：

```
  PASS  AC2 roundtrip(转义/属性/双时间戳)
  PASS  AC2 残行三道闸 + 随机字节 fuzz(300 次, 解析不抛异常)
  PASS  AC3 五域 INIT/COMM/HW/FSM/SYS 共 24 码(字段完整/无重复)
  PASS  AC4 双端 7 个用例逐字节一致(含|/换行/控制字符/中文)
  PASS  AC5 多进程并发 4x250=1000 行无丢行/无交错
  PASS  AC5 轮转触发, 副本数 3 (2<=n<=keep=3), 最老已淘汰
  PASS  AC5×F-1 多进程×轮转 3x400 行逐 worker 对账: 写成功=1200 可见=1200, 副本文件 16 个, 无半行/无全灭/无缺号
  PASS  AC5 读端一条命令 --level ERROR --code E-INIT-* 命中 2/5
  PASS  AC6 硬崩溃(os._exit)后最后一条 ERROR/FATAL 事件可读
  PASS  GEN 生成头/文档与 catalog 单一来源一致
  PASS  F2 时间前缀归一: 前缀=日历段语义（until=段末/since=段始）, 窗口与全精度行为正确
  PASS  READ parse/tail CLI 冒烟
自测结束: 12/12 通过, 用时 28.1s
SELFTEST PASS          （退出码 0）
```

复现命令（R1 修正 F-4：先建 `tests\_work` 目录 —— 缺省自测结束会清理该目录，
保证全新工作区逐行可复现；Linux 板端将 `mkdir`/反斜杠换成对应形态）：

```
cd developer/script
python -m rmlog.selftest
mkdir tests\_work
gcc -std=c99 -Wall -Wextra -I rmlog -o tests\_work\example.exe rmlog\example.c rmlog\rmlog.c
tests\_work\example.exe tests\_work\demo3
```

C 示例真实运行输出（R0 时点留档，`tests/_work/demo3/rmlog.log`；时间戳/序号每次运行不同）：
```
LOGV1|1|2026-09-26T20:16:57.032|361818154|INFO|E-INIT-000|ctrl|上电自检完成, 进入待机 state=1
LOGV1|2|2026-09-26T20:16:57.032|361818155|WARN|E-HW-005|pwr|电池电压接近下限 v=22500mV
LOGV1|3|2026-09-26T20:16:57.032|361818155|ERROR|E-COMM-001|spi|SPI 传输超时 dev=/dev/spidev0.0 retry=3
LOGV1|4|2026-09-26T20:16:57.034|361818156|FATAL|E-FSM-004|fsm|状态机进入未定义状态 st=7
```
与 Python 端写同组事件输出**结构逐字段一致**（仅时间戳/序号本身不同）。

## 4. 已知风险与未覆盖项（诚实清单）

1. **平台差异（最重要）**：
   - Windows 自测结论**不得表述为 Linux 已验证**。多进程安全与轮转协调在两平台的
     实现路径不同（Linux=内核 O_APPEND 原子 + flock 轮转互斥；Windows=开发机专用的
     写锁串行化）；**多进程×轮转组合在 Linux 上的行为是协议推演（unverified）**，
     推演依据见 §2.1 末段，板端以 §5 用户实测为准（建议增测该组合）。
   - C 端 Windows 分支无跨进程轮转锁（无 flock），C 端多进程×轮转组合仅在
     Linux 板端语义完整；Windows 上该组合的演示由 Python 端用例覆盖（C 端
     Windows 是开发机编译自测平台，不是部署目标）。
   - 跨进程轮转互斥是 **advisory 锁**：前提是同一日志目录的所有写入方都经本组件
     （rmlog C/Python 双端约定同名锁文件 `.rmlog.ROTLOCK`）；若有第三方工具直接
     对 `rmlog.log` 写入并自行 rename，互斥前提不成立（部署约束，USAGE §6 注明）。
   - C 端 `rmlog__dir_usable` 仅单级创建；`/userdata` 若是多级深层路径需部署方
     预先建目录（USAGE §6 已注明；板端实际层级属未核实项 —— management 已裁定
     "mkdir -p 等效"列入 P1，本轮不做）。
   - `fdatasync` 为 Linux 特性，其他 POSIX 工具链回退 `fsync`（多刷元数据，语义不变）。
2. **断电窗口**：INFO/WARN 滞留页缓存，硬断电可能丢最近几条非关键行；ERROR/FATAL 已强制
   fdatasync。绝对零丢失需逐条 fsync（1kHz 不可承受），损失边界见 USAGE §8。
   R1 的 `flush()` 仅同步当前主文件 —— 副本链中数据的落盘依赖 OS 周期回写（与 R0 一致）。
3. **容量边界（R1 修正，F-9）**：C 端消息经 vsnprintf 截断到 1023 字节后仍记录（截断计数）；
   但**转义会膨胀**（`|`/换行/控制字符 1 字节 → 4 字节 `\xNN`），mod+msg 转义后总长超过
   行缓冲上限 2047 字节的事件**整条丢弃并计数**（不产坏行、不崩溃）—— 即"≤1023 字节
   的消息"不保证可记录，取决于其中需转义字符的占比。Python 端无硬限。
4. **单文件全局状态**（C 端）：一个进程一份日志上下文（单文件）；多文件需求属 P1。
5. **性能取舍（R1 新增）**：Python 端每条事件 3 次系统调用（open/write/close，无常驻 fd），
   比常驻 fd 路径多 2 次；1kHz 场景开销 µs 级可接受，1kHz 以上高频路径建议用 C 端
   （常驻 fd + 仅 emit 前对准检查）或 P2 的批量化优化（REQ §4 P2）。
6. **覆盖声明**：未测项 = 板端实机行为（python3 版本/`/userdata` 存在性/O_APPEND 板端原子性/
   多进程×轮转 Linux 实测/journald 持久化/rsyslog 形态/coredump 可用性/dmesg 时间戳格式）；
   `--follow` 的长时间跟踪、1kHz 高频写入压测、日志尺寸真实上限（数 GB 级）——均超出
   P0 范围或依赖板端。
7. **构建/运行遗留**：无（R1 后 C 端 `-Wall -Wextra` 零警告已复验；selftest 12/12 PASS）。

## 4.1 R1 后 `close()` 语义说明（F-8 关联）

- **Python 端**：轮转协议 v2 无常驻 fd，`Writer.close()` 保留为兼容接口（无操作）；
  ERROR/FATAL 逐条已落盘，INFO/WARN 依赖页缓存回写 —— 损失边界与 R0 声明一致。
- **C 端**：`rmlog_close` 落盘并关 fd 后，后续 RMLOG_* 宏会**按需重新打开继续记录**
  （幂等重开，与"打开失败重试"共用同一路径）—— rmlog.h 注释已按此真实行为修正
  （F-8 选"改注释"而非"加终态标志"：重开继续记录对取证场景更有利，行为无需收紧）。

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

## 6. 未解疑问（不阻塞验收，供管理侧决策；management 已裁定两项列入 P1）

1. `rmlog__dir_usable` 的单级创建限制是否需要升级为逐级创建（`mkdir -p` 等效）？
   现状已在 USAGE/本文注明；**management 已裁定：列入 P1，本轮不做**（R1 任务书 §3）。
2. C 端 attrs 支持（`RMLOG_I` 宏族带 k=v 参数）—— **management 已裁定：列入 P1，
   本轮不做**（R1 任务书 §3）。

## 7. 提交信息

- 提交隔离：按路径显式添加本轮文件（契约 §2.1.2）；发现他方（management）未提交改动，
  不触碰，并在此 NOTIFY：**management 名下有未提交改动（memory/PROJECT-BOARD/worklog 及
  from_human 原件），请其自行提交**。
- commit hash 与产物以 INDEX.md 登记为准（审查/验收以该 hash 为基准）。
- R1 交付顺序（契约 §2.1.1，本次已按序执行）：修复 → 自测全量重跑留档 →
  **先发复审请求**（新 commit hash + F-1~F-9 逐条处置）→ 审查通过 →
  合格确认通知 maintainer（备料）→ 再向 management 报 RESULT。
