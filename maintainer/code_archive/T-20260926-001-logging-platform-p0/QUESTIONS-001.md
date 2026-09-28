# QUESTIONS-001 — 读这份代码前应当先弄懂的关键问题清单

> **归档版本 001 · 来源 commit `164d4c7`**。这 10 个问题不是测验——是"读码前先自查"的清单：每个问题都对应代码里一处**如果不先弄懂就会读错**的地方。答案指引给出落点（行号=归档带注版），但建议先自己想 30 秒再看。

1. **为什么"一条完整行必须放在一次 write() 里"？拆成两次 write 写同一行会怎样？**
   指引：CODE-STYLE §4.2；writer.py:227（_write_once）；format.py 模块头"多进程行完整性"。这是行完整性的根基——O_APPEND 只保证"单次 write 的数据连续追加不交错"，两次 write 之间可能插入他进程的行。

2. **O_APPEND 到底保证了什么、没保证什么？Windows 上为什么就不一样？**
   指引：writer.py 模块头"平台差异"（49-59 行）；rmlog.c 平台适配层（70-108）。Linux=内核级原子追加，所以写路径零锁；Windows CRT 的 `_O_APPEND` 是"写前 seek 到末尾"，跨进程不原子，所以 Windows 每写都要拿字节锁。

3. **为什么写路径不需要跨进程锁，而轮转（rename 链）必须锁？**
   指引：writer.py 模块头推理链 c（33-39 行）；`_rotate_if_needed`（writer.py:407）。一次 write 是单条原语；rename 链是"删最老→逐段后移→改主名"的复合操作，"replace 掉对方还没 shift 的副本"是唯一能凭空抹掉已落盘数据的竞争。

4. **旧轮转协议（R0）到底怎么丢数据的？"fd 搁浅在旧 inode 上"是什么意思？**
   指引：rmlog.c 轮转协议 v2 注释块（372-392 行）；IMPL §2.1 开头；REVIEW-…-f3331b0 的 F-1。常驻 fd 绑的是 inode 而不是路径；A 进程把文件 rename 进副本链后，B 的 fd 还在旧 inode 上写，那段数据随后随旧文件被当"最老副本"淘汰。

5. **"每写即开即关"多花 2 次系统调用，换来了什么？为什么 1kHz 场景可以接受？**
   指引：writer.py 模块头推理链 a/b；IMPL §4.5（性能取舍）。fd 的生命周期缩短为一条事件，"搁浅 fd"在结构上不存在；每次 open/write/close 是 µs 级，1kHz 下开销可忽略——这是 F-1 修复明码标价的代价。

6. **本进程的字节计数 `_bytes`/`g_own_bytes` 在多进程同写时必然偏小，为什么这个"失真"是安全的？**
   指引：writer.py:163-166 注释与 `_rotate_step`（444）；rmlog.c `g_own_bytes` 声明注释（rmlog.c:159-165 区）。偏小只会**偏早**触发轮转裁决，而偏早会被轮转锁内的 stat（真实大小）挡下并校准——失真方向不会导致丢数据。

7. **`.rmlog.ROTLOCK` 是什么？为什么它"不写数据、永不进副本链"，且双端必须同名？**
   指引：writer.py:81-84；rmlog.c:118-121；USAGE §6 部署约束。它是 flock/字节锁的锁体文件；进副本链或被写数据都会破坏锁语义；双端同名是 C/Python 写入方混用同一目录时互斥成立的前提（advisory 锁，互斥前提=所有写入方都经本组件）。

8. **`_POSIX_C_SOURCE` 特性宏是什么？为什么它必须出现在任何 #include 之前，且只包在 `#if !defined(_WIN32)` 里？**
   指引：rmlog.c:47-58 与 maintainer 补注；IMPL §8.1。glibc 的每个标准头先拉 `<features.h>`，按已定义特性宏决定暴露哪些声明；`-std=c99` 下不预定义则 clock_gettime/localtime_r/fdatasync 被隐藏（板端硬错误实测）。晚于任何头定义就晚了。MinGW 没有 features.h，定义它反而可能干扰 MSVCRT 头。

9. **C 端 close 之后再调 `RMLOG_*` 宏，是无操作吗？事件会落到哪里？**
   指引：rmlog.h:55-69 生命周期注释；`rmlog__open_locked`（rmlog.c:219，RF-1 语义：g_path 已有值直接复用）。不是无操作——emit 会按需重开**继续记录**，落点=最近一次成功打开的目录。想真正停记就别在 close 后再调宏。这是取证场景的刻意取舍（F-8 选"改注释"而非"收紧行为"）。

10. **`write_failures` 与 `lock_degradations` 两个计数器为什么必须分开？混了会发生什么？**
    指引：writer.py:175-181（计数器注释）；`_win_write_line` 降级路径 maintainer 补注；RF-4（REVIEW-…-45eeb04 §6）。锁文件 open 失败时事件本身能写成功（裸写落盘）——若计入 write_failures，健康检查会为"40 条全部写成功"报 40 次失败，健康口径失真。锁失败≠写失败。

---

**附加两问（关于验证体系，读 selftest 前自问）**：

11. **AC4 的"双端一致"为什么要把时间戳固定注入，而不是让两端各自取当前时间？**
    指引：encode_cases.py 模块头；selftest.py:278 用例 docstring。要验证的是"编码规则一致"（转义表/字段序/格式化），不是"时钟一致"——固定输入把判定边界收干净。

12. **为什么句柄泄漏（RF-6）在数据正确性用例全绿的情况下测不出来？必须用什么形态的用例才能抓住它？**
    指引：tests/probe_fdleak_rf6.c 文件头；selftest.py:580 用例 docstring。两个 fd 同指一文件且 O_APPEND 语义不变，数据层看不出差别——资源不变量必须由"句柄数增量"这类专项探针覆盖，且要双组隔离变量（泄漏路径 vs 对照快路径）。
