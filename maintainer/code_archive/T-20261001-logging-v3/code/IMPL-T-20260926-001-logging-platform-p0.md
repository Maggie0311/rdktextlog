# IMPL — T-20260926-001-logging-platform-p0 实现说明

| 字段 | 值 |
|---|---|
| task_id | T-20260926-001-logging-platform-p0 |
| 主责 | developer (R-003)（本会话上岗执行；前次中断的同任务产物已核验后并入） |
| 交付日期 | 2026-09-26（R0 首交付）；2026-09-27（R1 整改返工）；2026-09-27（R2 复审微整改 RF-1~RF-5）；2026-09-27（R3 终轮微修复 RF-6 + MIN-1/2/3）；2026-09-27（R4 构建可移植性修复，task_id T-20260927-003，见 §8；commit 见 §7 / INDEX） |
| 需求依据 | `management/script/REQ-20260926-001-logging.md`（§4 P0-a~f、§6 AC1–AC8、§7.1 裁决） |
| 任务书 | R0: inbox MAIL-…1620 + MAIL-…1640；R1: inbox MAIL-20260927-0922（F-1~F-9 整改书）；R2: inbox MAIL-20260927-1215（RF-1~RF-5 微整改书，范围冻结 5 项）；R3: inbox MAIL-20260927-1336（RF-6 + MIN-1/2/3 终轮微修复书，范围冻结 4 项） |
| 关联审查 | `code_reviewer/script/REVIEW-T-20260926-001-f3331b0.md`（结论 CONDITIONAL，F-1~F-9 逐条整改见 §1.1）；`code_reviewer/script/REVIEW-T-20260926-001-rf-a675c8d.md`（R3 复审 FAIL：RF-6 严重级 + MIN-1/2/3，逐条处置见 §1.3） |

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
| `rmlog/selftest.py` | 自测入口（R3 起 13 用例：AC2–AC6 + F-1 组合对账 + F-2 前缀回归 + RF-6 句柄守恒 + 附加） | AC1 |
| `rmlog_read.py` | 读端工具：parse/tail/filter；R1 增时间前缀归一（F-2） | AC5 |
| `USAGE.md` | 场下使用方法；R1 修正 §2 复现命令（F-4）与 §5 时间窗示例语义（F-2） | AC7 |
| `tests/selftest-*.log` | 自测原始输出留档（含修复过程各轮，R3 末轮 13/13 PASS） | AC1 |
| `tests/probe_fdleak_rf6.c` | RF-6 句柄泄漏回归探针（R3 新增，selftest 用例编译运行；POSIX/Windows 双口径，前后对照留档 `tests/probe_fdleak_rf6_before_after.log`） | RF-6 |
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

### 1.2 R2 微整改处置索引（RF-1~RF-5，逐条对应复审报告 REVIEW-…-45eeb04 §6/§8）

| 发现项 | 级别 | 处置摘要（详细位置与行号见复审请求信 MAIL-20260927-1305 的 RF 逐条节） |
|---|---|---|
| RF-1 C 端 close 后重开落点与注释失实（显式目录形态） | 一般 | **选"让行为与注释一致"**（二选一的前者）：`rmlog__open_locked` 在 `g_path` 已有值时跳过目录裁决直接复用（rmlog.c，与 Python 端 Writer 构造期裁决一次的语义对齐）；close 后 emit 重开落点 = 本进程最近一次成功打开的目录，显式目录形态成立（reviewer probe_c2 场景已由本角色复验探针证实修复）。取舍理由见 §4.1。rmlog.h 注释同步限定重开落点语义 |
| RF-2 IMPL §3 的 810 vs 留档 813 | 提示 | **已更正**：§3 数字改按留档原始记录 813/1200，并注明该处曾为转写笔误（GEN-33 证据诚实） |
| RF-3 selftest docstring keep=10 残留 | 提示 | **已更正**：test_ac5_concurrent_rotation docstring 改为 keep=20 并注明残留来源（1010 轮参数误校准修复后注释未同步） |
| RF-4 Windows 写锁 open 失败误计 write_failures | 一般 | **已修**：`_win_write_line` 锁文件 open 失败改计 `lock_degradations`（与 locking/解锁失败同口径），`write_failures` 只反映真实写失败；`__init__` 计数器注释同步收紧。selftest 12 用例断言未直接涉该计数语义，无需改断言（健康口径见 §2 第 7 条） |
| RF-5 C 端 rotlock 获取失败无计数 | 提示 | **已修**：rmlog.c 增 `g_lock_degradations`（对齐 Python `lock_degradations` 风格），`rmlog__rotate_locked` 取锁失败路径计数；仅在持写锁的 emit 路径自增，线程安全；Windows 平台的 -2 约定值（无跨进程锁）不计入，避免伪降级 |

### 1.3 R3 终轮微修复处置索引（RF-6 + MIN-1/2/3，逐条对应复审报告 REVIEW-…-rf-a675c8d §6/§8）

| 发现项 | 级别 | 处置摘要 |
|---|---|---|
| RF-6 `rmlog__open_locked` 双重 open + 句柄泄漏（rmlog.c:162-175 区域，1000 轮 emit→close 实测 +1000，1:1） | 严重 | **已修（结构归位：裁决与打开分离）**：三个裁决分支只裁决/复用 `g_path`，文件 `open` 保留为函数尾部唯一一次——首个 fd 被覆盖泄漏的结构性根源消除。返回值语义逐分支与修复前等价：① 各分支 open 失败 ⇒ 修复后尾部同路径同 flags 的 open 同样失败 ⇒ 返回 -1（等价，打开失败不回滚 g_path 的行为也未变）；② 各分支 open 成功 ⇒ 修复后打开同一同 flags 路径成功 ⇒ 返回 0（等价）。调用路径全走查：emit 按需重开（`rmlog__emit_locked` 打开分支，RF-6 主要触发面）、`rmlog_open(NULL)` 缺省裁决路径、INIT_ONCE 初始化路径（仅初始化写锁，与本函数无耦合，未变）——均不复现泄漏。**回归闸**：selftest 新增第 13 用例 `test_c_fdleak_reopen`（600 轮 emit→close 句柄守恒断言，探针 `tests/probe_fdleak_rf6.c` 留档进 tests/）+ 前后对照数据 `tests/probe_fdleak_rf6_before_after.log`（修复前 1000 轮 +1000 / 500 轮 +500 / 快路径 +0，泄漏复现；修复后 1000 轮 +0 / 500 轮 +0 / 快路径 +0，且 reopen 组落盘自检同时断言 RF-1 语义保持） |
| MIN-1 IMPL:52 / INDEX:11 邮件引用占位符"MAIL-…-HHMM/<HHMM>"未填实（实际 1305） | 一般 | **已更正**：IMPL §1.2 处置索引表头占位符改为 MAIL-20260927-1305；INDEX #3 行同步（见 §1.3 登记）；worklog #4 的同名占位符一并更正（worklog 只可追加，以新条目 #5 更正，不改动历史条目） |
| MIN-2 IMPL §7 / INDEX:11 未登记 R2 交付 commit a675c8d | 提示 | **已补登记**：INDEX #3 行 commit 栏补 `a675c8d（R2）`；IMPL §7 补 R2 交付 commit 与本轮 R3 交付顺序说明 |
| MIN-3 复审请求信"任务书随附入库"声明与 git 实际不符（1215 任务书未随 a675c8d 入库） | 一般 | **按管理侧裁定双向更正**：① 1215 任务书原件按"收件方应提交"原则随本轮提交入库（`developer/mailbox/inbox/MAIL-20260927-1215-…TASK-rf-microfix.md`，属流程更正非扩围——任务书MAIL-20260927-1336 已明示）；② 1305 请求信已发出即冻结，不再改动，其"随附入库说明"与 git 实际的出入以本轮提交事实与 worklog #5 更正说明为准（in-box 只可追加、发出信冻结，故采用新条目更正而非改历史信） |

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
   （selftest 主动检查）。R1 增 `lock_degradations`（锁降级可观测，F-7）；R2 收紧口径（RF-4）：
   Windows 写锁文件 open 失败计入 `lock_degradations`，`write_failures` 只反映真实写失败。
   C 端对等计数 `g_lock_degradations`（RF-5，轮转锁获取失败）。

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
| 20260927-1235-rf | **PASS 12/12** | **R2 微整改末轮 PASS**（RF-1/RF-3/RF-4/RF-5 代码与注释修正后全量重跑，28.2s，退出码 0；RF-2 为文档修正）|
| 20260927-1352-rf6 | **PASS 13/13** | **R3 终轮微修复末轮 PASS**（RF-6 修复 + selftest 新增第 13 用例 test_c_fdleak_reopen——600 轮 emit→close 句柄守恒探针，44.3s，退出码 0；句柄前后对照数据见 `tests/probe_fdleak_rf6_before_after.log`：修复前 1000 轮 +1000/500 轮 +500/快路径 +0，修复后全部 +0。用例数 12→13，新增用例为本轮范围）|

R1 迭代说明（诚实记录；RF-2 更正：本段旧文的"810"系转写笔误，留档原始记录为
**813**/1200，以留档为准）：20260927-1010 轮的 F-1 FAIL 经临时诊断脚本定位 —— 磁盘可见
813/1200 行**全部是链容量淘汰**（1200 行 ≈ 15 次轮转 > keep=10 的 11 个槽位），对账
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

> **构建命令可移植说明（T-20260927-003 同步）**：`rmlog.c` 已源码内按平台定义
> `_POSIX_C_SOURCE 200809L`（非 Windows，位于任何 `#include` 之前），故上述 `-std=c99`
> 在 Windows（MinGW）与板端 Linux（glibc）**均原样可编译**（此前 `-std=c99` 在 glibc
> 下隐藏 POSIX 声明导致编译失败，见 §8 追记）。板端 C 链接因 POSIX 分支用到 pthread，
> 命令末尾追加 `-lpthread`（`gcc -std=c99 -Wall -Wextra -o example example.c rmlog.c -lpthread`）；
> selftest 内 AC4/RF6 两 C 探针已在非 Windows 下自动追加 `-lpthread`（selftest.py）。

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
  **R2（RF-1）**：复审实证该承诺对"显式目录"形态失实 —— 重开路径原实现固定重做缺省目录
  裁决，显式目录调用方 close 后事件会静默改投缺省目录（probe_c2 实测）。处置选"让行为与
  注释一致"（而非收窄注释）：`rmlog__open_locked` 在 `g_path` 已有值时直接按既有路径重开、
  不再重做裁决，目录裁决一次就固定，与 Python 端 Writer 构造期裁决一次的语义对齐。
  取舍理由：① 语义诚实且修复面小（一个函数内的分支前置）；② 显式目录是 rmlog.h 自己
  记载的合法用法，取证连续性场景（close→重开→事件仍在原目录）价值高于"回到缺省目录"；
  ③ 未采用"加终态标志收紧行为"，因那会改变 close 的既有承诺面（幂等重开），超出 RF-1
  范围（DN5）；④ 与 INIT_ONCE/线程锁的交互无回归 —— once 只初始化锁，重开全程持同一把
  写锁，g_path 的读写均在锁内（reviewer F-5 核销时已核对该组合，本轮分支前置不引入新交互）。
  **R3（RF-6）追记**：R2 的上述实现残留了"分支内 open + 尾部再 open"的旧结构（RF-6 句柄
  泄漏，R3 复审 §6 实证 1000 轮 +1000），已按复审建议归位为"裁决与打开分离"（函数尾部
  唯一 open）；本节描述的 RF-1 语义（重开落点=最近一次成功打开的目录）经修复后探针复验
  保持不变（前后对照数据见 §1.3 RF-6 行与 `tests/probe_fdleak_rf6_before_after.log`）。

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
  不触碰，并在此 NOTIFY：**management 名下有未提交改动（memory/PROJECT-BOARD/worklog、
  from_human 原件及 outbox 新邮件），请其自行提交**。
- commit hash 与产物以 INDEX.md 登记为准（审查/验收以该 hash 为基准）：
  R0=f3331b0；R1=45eeb04；**R2=a675c8d**（MIN-2 补登记：R2 交付权威 hash，亦为 R3 复审
  基准）；R3=本轮提交（hash 以 git log 为准，与本轮复审请求信同值）。
- 交付顺序（契约 §2.1.1，R1/R2/R3 三轮均按序执行）：修复 → 自测全量重跑留档 →
  **先发复审请求**（新 commit hash + 逐条处置）→ 审查通过 →
  合格确认通知 maintainer（备料）→ 再向 management 报 RESULT。
- MIN-3 流程更正（R3）：R2 复审请求信 MAIL-20260927-1305 的"任务书随附入库"声明与 git
  实际不符（a675c8d 未含 1215 任务书原件，该文件当时仍未跟踪）。已发出信件冻结不改；
  按管理侧裁定：1215 任务书原件按"收件方应提交"原则随 R3 提交入库（属流程更正非扩围），
  声明出入以本节与 worklog #5 更正条目为准。
- R4（T-20260927-003 linux-build-fix）：交付 commit 以 git log 为准，与 R4 复审请求信同值、
  由 INDEX #5 行登记（commit 栏 = R4 hash）。本轮为缺陷修复（非改验收）：先发复审请求 →
  审查通过 → 待 software_tester 板端复测通过 → 再走 maintainer 备料 / RESULT（顺序同 §7 交付顺序约定）。

## 8. T-20260927-003 缺陷追记（R4 linux-build-fix，板端实测缺陷）

> 触发：software_tester 板端 SSH 实测（T-20260927-002，TESTREPORT-…-001 §4/§6）发现
> `rmlog.c` 在目标平台（aarch64 glibc gcc 11.2.0）以文档化参数 `-std=c99 -Wall -Wextra`
> **无法编译**（Q4 硬错误），导致板端 selftest 11/13（AC4/RF-6 两 C 探针编译失败）。
> management 裁定开 T-20260927-003 修复（ACCEPT-20260927 §3 条件 1）。范围冻结 5 项，DN5。

### 8.1 根因（板端实测坐实，非推演）

严格 `-std=c99`（gcc 定义 `__STRICT_ANSI__`）下 glibc 的 `<features.h>` 隐藏 POSIX 声明，
本文件 POSIX 分支用到的 `clock_gettime`/`CLOCK_MONOTONIC`/`localtime_r`/`fdatasync` 因此
"未声明/未定义"（硬错误 + 隐式声明警告）。开发机 MinGW 走 `_WIN32` 分支、不触及这些符号，
故 gcc 13.2.0"零警告"掩盖了目标平台缺陷。另有 3× `-Wformat-truncation`：`rmlog__rotate_chain_locked`
用与 `g_path`（512B）等长的缓冲拼副本路径 `"%s.%d"`/`"%s.1"`，gcc 无法证明不截断（最坏
511+1+11=523 字节 > 512）。

### 8.2 修复（逐项，与任务书 §3 一一对应）

| # | 项 | 处置 | 落点 |
|---|---|---|---|
| 1 | 构建可移植性（硬错误） | **选"源码内定义特性测试宏"而非改 `-std=gnu99`**：在 `rmlog.c` 任何 `#include` 之前 `#if !defined(_WIN32) #define _POSIX_C_SOURCE 200809L`。理由：① POSIX.1-2008 是覆盖全部缺失符号的最小开关；② 保持严格 ISO C99 模式（比 gnu99 更早暴露非标准写法）；③ 文档命令 `-std=c99` 原样可编译，无需改文档命令、无需使用者加 `-D`；④ tester 边界表征已证 `-D_POSIX_C_SOURCE=200809L` 硬错误清零，此选择有板端证据背书 | `rmlog/rmlog.c`（文件头 + 特性宏块） |
| 2 | 3× `-Wformat-truncation` | **根上消除（非 `-Wno` 压制）**：副本路径缓冲 `RMLOG_ROTATE_PATH_CAP = RMLOG_PATH_CAP + 16`（528B），任何合法 `g_path`(≤511 字符) + `.N` 后缀的最坏输出 523B 也放得下，gcc 可证明不截断。**不涉及日志消息截断**——消息截断仍走 `vsnprintf` 进 `msg[RMLOG_LINE_MAX]` 并由 `g_write_failures` 计数（§4.3 能力原样保留），本修复只放大**轮转副本路径**缓冲（该路径本不应截断，旧实现是潜在的静默路径破坏） | `rmlog/rmlog.c`（`RMLOG_ROTATE_PATH_CAP` + `rmlog__rotate_chain_locked`） |
| 3 | selftest C 探针 | AC4 探针 `_ac4_probe.c` 仅用 ISO C，板端已证其无自身编译错误（Q1 原始输出仅 rmlog.c 报错），无需改源码；RF-6 探针 `tests/probe_fdleak_rf6.c` POSIX 分支的 dirent 函数板端亦无自身错误。**编译链接参数**：selftest 两用例在非 Windows 下追加 `-lpthread`（`selftest.py` 新增 `_CC_LINK_LIBS`），与 example.c 板端文档命令一致；`-std=c99` 不变 | `rmlog/selftest.py`、`tests/probe_fdleak_rf6.c`（文件头命令注释补板端形态） |
| 4 | 文档同步 | USAGE §2 与 IMPL §3 构建命令保持 `-std=c99`（现已真实可编译），并补"可移植说明"；IMPL 追记本节（根因/修复/验证边界）；INDEX 登记新 hash | `USAGE.md`、本文件 §3/§8、`INDEX.md` |
| 5 | Windows 不回退 | 开发机 gcc 13.2.0 `-Wall -Wextra` 复验零警告（`_WIN32` 分支不受影响，见 §8.3） | §8.3 |

### 8.3 验证边界（诚实声明，DN6/DN9）

- **本机（Windows 开发机）已验证**：全量 selftest 13/13 PASS（留档 `tests/selftest-20260927-2208-r4.log`，
  本轮新留档）；`gcc 13.2.0 -std=c99 -Wall -Wextra -c rmlog.c` **零警告、退出码 0**（`_WIN32` 分支路径，
  未回退）。
- **本机无法复现板端失败，也未声称"已板端验证"**：开发机**无 aarch64/glibc 工具链**，且经查
  **无 WSL / 无 docker**（`wsl --status` 未安装、`docker` 命令不存在），故无法在本机做 glibc 交叉加验。
  板端复测由 software_tester 执行（management 随后下发），**通过前本结论对"板端可编译/零警告"不作断言**。
- **静态论证 glibc 行为**（供复测对照，非实测结论）：`_POSIX_C_SOURCE=200809L` 使 glibc 定义
  `__USE_POSIX199309` 等，`clock_gettime`/`CLOCK_MONOTONIC`（POSIX.1b，≥199309L）、`localtime_r`
  （POSIX.1c/2001）、`fdatasync`（POSIX.1b）均被声明；该阈值下的声明集已被 tester 边界表征
  （`-D_POSIX_C_SOURCE=200809L` → 硬错误清零）坐实。3× format-truncation 在**所有**参数组合下均不消失
  （tester 实证），故必须靠 §8.2 项 2 的缓冲放大根除，不能靠 `-std=gnu99`/`-D` 顺带解决。
- **链接**：板端 Ubuntu 22.04 为 glibc 2.35（pthread 已并入 libc，`-lpthread` 为兼容空桩），
  selftest 探针链接追加 `-lpthread` 后在最坏旧 glibc（<2.34）下亦成立；此点未板端实测。

### 8.4 未覆盖项（诚实清单）

1. 板端 aarch64 gcc 11.2.0 复编译（含 `-std=c99 -Wall -Wextra` 零警告）——**待 software_tester 复测**；
2. 板端 AC4/RF-6 两 C 探针的编译+链接+执行全链路——同上，待板端 selftest 13/13 复跑；
3. clang 编译（板端无 clang，历史未覆盖项延续，UV 类）；
4. 其他非 glibc POSIX 工具链（如 musl）——不在目标平台范围，未验证。

## 9. T-20260928-004 追记（usage-rewrite：USAGE.md 重构为用户优先手册，版本 002）

> 触发：人类用户 2026-09-28 审查归档产物提出两条意见（经 management TASK
> MAIL-20260928-2133-management--developer-TASK-T-20260928-004-usage-rewrite 下达，范围冻结 5 项，DN5）：
> ① **USAGE.md 视角错位**——原文档按"开发者视角的部署+验证流程"组织，缺"用户如何快速上手"
> 的主线（怎么几行代码记出第一条日志、比赛日怎么操作、错误码怎么打怎么查）；
> ② **「板端自测步骤（用户执行）」章节过时**——该章节是 Q1=A 裁决时代（用户板端自测回贴）的产物；
> Q1 已修订为 B 且板端已由 software_tester 真机实测全绿（TESTREPORT-T-20260927-003-001：
> selftest 13/13、`gcc -std=c99 -Wall -Wextra` 编译零告警、多进程×轮转对账无回归），
> 继续保留会误导用户以为还要自己做板端自测。
> 归档版本 001 不可改，文档问题走本任务产出新版本（164d4c7 之上仅文档变更）。

### 9.1 改动清单（范围冻结 5 项逐条对应）

| # | 项 | 处置 | 落点 |
|---|---|---|---|
| 1 | 删除过时板端自测章节 | 原 §3「板端自测步骤（用户执行）」整章删除；正文各处引用同步清理——原 §2 的 Q1=A 回贴表述、§7 的"待板端核实"标注改为引用 TESTREPORT-T-20260927-003-001 实测结论（板端可运行一句话引用，不展开步骤）；原 §8 局限表中已由板端实测闭环的行删除，剩余有效信息并入 FAQ/§7 | `USAGE.md` |
| 2 | 重构为用户优先结构 | 六主题全覆盖（任务书骨架，微调说明：① 原主内容"部署"降级为 §6 一次性配置附录；② 原样例 Systemd 单元保留为 §6.2；③ 原 §5 场下定位演示精华为 §3.3 赛后 5 分钟定位（按新结构重排，命令实测语义不变）；④ 原 §4 行格式说明并入 §1.4 快速上手（用户先见格式再谈深入）；⑤ 新增 §7"手册与代码的对应关系"作为一致性维护锚点（HOW 自主项）：§2 日常使用（级别/错误码/模块/k=v/文件位置/rmlog_read 三命令）、§3 比赛日操作流（赛前清单/赛中零操作/赛后取日志）、§4 与系统日志关系（journald/dmesg 精简保留）、§5 FAQ（Q1~Q9 现象→原因→处置）、§6 部署（systemd/目录约定/更新组件，压缩为"做一次就完"） | `USAGE.md` |
| 3 | 一致性 | 文中每条命令、示例、默认值与代码实际行为逐项核对（见 §9.2 实跑记录）；标注过的平台事实均有他方报告出处：`/userdata` 存在、journald 持久化、rsyslog active、coredumpctl 不可用、dmesg ISO 格式 = TESTREPORT-T-20260927-002-001 §6 Q2；板端 13/13/零告警 = TESTREPORT-T-20260927-003-001 §6 | `USAGE.md` |
| 4 | IMPL 追记 | 本节 | 本文件 §9 |
| 5 | 不做（零代码变更） | `.py/.c/.h/ERR-CATALOG/CODE-STYLE` 一行未动；行格式、错误码、默认路径（/userdata/rmlog/）、轮转参数等行为面零变更；INDEX 登记与 worklog 追加属登记义务 | — |

### 9.2 示例实跑核对证据（Windows 开发机，2026-09-28 21:49~21:55，gcc 13.2.0 / Python 3.14.7）

工作区为 `developer/script/tests/_work/` 临时子目录（`.gitignore` 覆盖，实测后可重建），
全部命令真实执行，输出摘要如下（任务书 AC"示例已实跑核对"的依据）：

| 核对项 | 命令 | 结果 |
|---|---|---|
| Python 快速上手 §1.1 | `set_default_writer(Writer(log_dir=...))` + 2× `rmlog.event(...)`（含 attrs） | 退出码 0；落盘 2 行 `LOGV1|1|...|INFO|E-INIT-000|ctrl|上电启动完成|freq=1000`、`LOGV1|2|...|ERROR|E-COMM-001|spi|...|dev=/dev/spidev0.0|retry=3`——与 §1.4 字段图一致 |
| C 快速上手 §1.2 | `gcc -std=c99 -Wall -Wextra -I rmlog -o example rmlog/example.c rmlog/rmlog.c` + `example <目录>` | 编译退出码 0、零告警；运行退出码 0；四级别各 1 行落盘，与既有 Python 行同格式共存 |
| 读端三命令 §2.5 | `filter --level ERROR` / `filter --code E-COMM-*` / `tail -n 3` / `parse` | 输出行数与内容逐一符合（filter 3 条/2 条、tail 3 条）；`rmlog_read: 命中 N 条` 走 stderr、stdout 纯事件流（可安全重定向） |
| 时间前缀语义 §2.5 | `--since 2026-09-28T21:50 --until 2026-09-28T21:50` | 命中 3 条 = 该分钟全部 ERROR+（分钟前缀含整分钟，F-2 语义）；`--until 21:49` 命中 0 条 |
| 残行丢弃 §1.4/§5 | 追加 2 行坏行后 `parse` | `[DROP] L7/L8` 标注 + stderr `丢弃残行/非法行 2 条`；`filter` 的 stdout 保持 3 条纯事件 |
| 轮转文件族 §2.4/§5 | `Writer(max_bytes=400, keep=3)` 连写 60 条 | 目录含 `.rmlog.ROTLOCK` 与 `rmlog.log.1/.2/.3`；轮转后主文件待下次写入重建（Q6 依据）；副本逐个显式可读 |
| 通配符限制 §2.5 | `filter "...\rmlog.log*"` | 字面路径→"文件不存在"→命中 0（不支持通配符的警告写入 §2.5） |
| 默认目录行为 §5 Q1/Q2 | `rmlog.event(...)` 不设目录直跑 | Windows 上建 `/userdata/rmlog` 失败 → 构造期抛 `PermissionError`（writer.py 构造期裁决无静默回退；Q1③/Q2 依据） |
| 全量 selftest 冒烟（本轮回归证据） | `python -m rmlog.selftest tests\_work` | **13/13 PASS，21.1s，退出码 0**——文档任务不改代码行为的回归证据 |

### 9.3 验证边界与已知风险（诚实声明，DN6/DN9）

- **本轮为纯文档任务**：零代码变更（§9.1 项 5），selftest 冒烟仅为回归证据；示例实跑均在
  Windows 开发机完成，与代码开发自测同环境（不涉及板端声明——板端结论全部引用
  software_tester 既有报告并注明出处，本角色未做板端操作）。
- **诚实边界**：手册中"赛中零操作/断电丢 INFO 边界/多进程同一目录"等表述与 writer.py/rmlog.c
  注释承诺一致，属设计承诺的转述；断电恢复（UV-5）仍为历史未实测项，FAQ 未做超出承诺的断言。
- **遗留风险**：无阻塞项。P1 展望（C 端 attrs、mkdir 逐级创建、正式常驻服务）在 §5/§6 以
  "当前形态"表述，未承诺时间点，与 management 既有裁定一致。
