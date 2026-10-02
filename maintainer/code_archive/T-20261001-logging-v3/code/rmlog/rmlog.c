/*
 * rmlog.c — RoboMaster 文本日志平台 C 实现。
 *
 * 任务: T-20260926-001-logging-platform-p0（REQ §4 P0-c/P0-d）。
 * R1 返工: 修复审查报告 F-1/F-5/F-9 ——
 *   F-1 旧轮转协议（常驻 fd + close→rename 链→reopen）跨进程零协调, 多进程×轮转
 *       组合下一个进程可整个搁浅在旧 inode 上、随后被当"最老副本"淘汰 ——
 *       已确认写成功的事件静默消失。R1 采用**轮转协议 v2**（见 rmlog__rotate_locked
 *       与 rmlog__reopen_current_locked 上方的大段注释）: 每写对准当前路径 + flock
 *       跨进程轮转互斥 + 锁内 stat 确认;
 *   F-5 轮转 reopen 失败改"计数 + 逐条重试", 不再永久静默停记;
 *   F-9 容量边界如实表述（转义膨胀可致整条丢弃计数, 见 RMLOG_LINE_MAX 注释）。
 * R2 微整改: 复审报告 RF-1/RF-5 ——
 *   RF-1 rmlog__open_locked 复用既有 g_path（close 后按需重开不再重做缺省
 *       目录裁决, 显式目录形态下事件继续落原目录, 与 rmlog.h 注释一致）;
 *   RF-5 轮转锁获取失败计入 g_lock_degradations（对齐 Python 端可观测口径,
 *       全程持写锁, 计数线程安全）。
 * R3 终轮微修复: 复审报告 RF-6 ——
 *   RF-6 rmlog__open_locked 结构归位（裁决与打开分离）: R2 实现各分支内
 *       open 一次、函数尾部又无条件第二次 open, 首个 fd 未 close 即被覆盖,
 *       每次"按需重开"泄漏 1 个文件句柄（1000 轮 emit→close 实测 +1000, 1:1）。
 *       修复后全函数 open 恰好一次（尾部）, 返回值语义逐分支不变;
 *       回归探针 tests/probe_fdleak_rf6.c（selftest RF6 用例守护）。
 * R4 构建可移植性修复（T-20260927-003-logging-c-linux-build, 板端实测缺陷）:
 *   严格 -std=c99 下 glibc 隐藏 POSIX 声明, 使本文件在 aarch64 gcc 11.2.0
 *   无法编译（CLOCK_MONOTONIC 未声明 + localtime_r/clock_gettime/fdatasync
 *   隐式声明 + 3× -Wformat-truncation）。修复 = 下方"特性测试宏"块（在**任何
 *   #include 之前**按平台定义 _POSIX_C_SOURCE）+ rmlog__rotate_chain_locked
 *   的副本路径缓冲加余量; 详细根因/取舍/验证边界见 IMPL §8（T-003 追记）。
 *
 * 设计决策（与 Python 端 writer.py/format.py 对齐，理由见对应文件头）:
 * - O_APPEND + 一次 write() 写一条完整行（含换行）—— 多进程行完整性根基（AC5）;
 * - 每条事件立即 write（进内核页缓存）; ERROR/FATAL 写后立即 fdatasync
 *   （关键证据先落盘再返回, AC6）; INFO/WARN 由 rmlog_close/rmlog_flush
 *   统一 fsync 落盘（P0 取舍: 硬崩溃时 INFO/WARN 可能滞留页缓存, IMPL 记录）;
 * - 日志故障不拖垮业务: 打开/写入失败静默丢弃并计数, 下一条事件重新尝试
 *   （无"一次失败永久停记"状态 —— F-5 语义）;
 * - 行编码与 Python format.py 同构: 同一转义表、同一字段序、同一时间戳格式（AC4）。
 *
 * 平台差异:
 * - 目标环境 Linux/X5: pthread / fdatasync / clock_gettime / flock 原生可用;
 * - 开发机 MinGW: 无 pthread, 用 Win32 Critical Section + INIT_ONCE 等效实现;
 *   fdatasync 用 _commit 等效; 跨进程轮转锁仅 POSIX 有（Windows 上 C 端不参与
 *   多进程轮转演示, 双进程轮转组合用例由 Python 端覆盖, 见 selftest）。两侧行
 *   字节流完全一致（selftest AC4 验证）。
 */
/* ---- 特性测试宏（必须在**任何**标准头之前定义） ----
 * 严格 -std=c99（gcc 定义 __STRICT_ANSI__）下, glibc 的 <features.h> 会隐藏
 * POSIX 声明 —— 本文件 POSIX 分支用到的 clock_gettime/CLOCK_MONOTONIC/
 * localtime_r/fdatasync 因此在 aarch64 gcc 11.2.0 上"未声明/未定义", 编译失败
 * （T-20260927-003 板端实测硬错误; 开发机 MinGW 走 _WIN32 分支不触及, 故
 * 曾"零警告"掩盖）。_POSIX_C_SOURCE=200809L 是 POSIX.1-2008 全套声明的最小
 * 开关, 覆盖上述全部符号（tester 边界表征已证 -D_POSIX_C_SOURCE=200809L 硬
 * 错误清零）, 且**不改文档命令**——文档化的 -std=c99 因此原样可编译。
 * Windows/MinGW 无 <features.h>, 该宏无意义; 仅在非 _WIN32 下定义以保持清晰。 */
#if !defined(_WIN32)
#  define _POSIX_C_SOURCE 200809L
#endif

#include "rmlog.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>
#include <sys/types.h>

/* ---- 平台适配层: 锁原语 + fd 级同步 + open 标志 + 跨进程轮转锁 ---- */
#if defined(_WIN32)
#  ifndef _WIN32_WINNT
#    define _WIN32_WINNT 0x0600   /* INIT_ONCE 需要 Vista+; MinGW-w64 默认已满足 */
#  endif
#  include <windows.h>
#  include <io.h>
#  include <direct.h>            /* _mkdir/ mkdir 声明（MinGW） */
#  include <fcntl.h>             /* O_APPEND/O_CREAT/O_WRONLY/O_BINARY（MinGW 定义于此） */
#  include <sys/stat.h>
#  define RMLOG_LOCK_T           CRITICAL_SECTION
#  define RMLOG_LOCK_INIT(l)     InitializeCriticalSection(&(l))
#  define RMLOG_LOCK(l)          EnterCriticalSection(&(l))
#  define RMLOG_UNLOCK(l)        LeaveCriticalSection(&(l))
#  define RMLOG_LOCK_DESTROY(l)  DeleteCriticalSection(&(l))
#  define RMLOG_FDATASYNC(fd)    _commit(fd)   /* MSVCRT: fd 级数据同步落盘 */
#  define RMLOG_OPEN_FLAGS       (O_APPEND | O_CREAT | O_WRONLY | O_BINARY)
#  define RMLOG_OPEN_MODE        (_S_IREAD | _S_IWRITE)
#else
#  include <pthread.h>
#  include <unistd.h>
#  include <fcntl.h>
#  include <sys/file.h>          /* flock: 跨进程轮转锁（F-1 修复） */
#  include <time.h>
#  include <sys/stat.h>
#  include <sys/time.h>
#  define RMLOG_LOCK_T           pthread_mutex_t
#  define RMLOG_LOCK_INIT(l)     pthread_mutex_init(&(l), NULL)
#  define RMLOG_LOCK(l)          pthread_mutex_lock(&(l))
#  define RMLOG_UNLOCK(l)        pthread_mutex_unlock(&(l))
#  define RMLOG_LOCK_DESTROY(l)  pthread_mutex_destroy(&(l))
/* fdatasync 是 Linux 特性; 其他 POSIX 工具链回退 fsync（多刷一次元数据, 换可移植性） */
#  if defined(__linux__)
#    define RMLOG_FDATASYNC(fd)  fdatasync(fd)
#  else
#    define RMLOG_FDATASYNC(fd)  fsync(fd)
#  endif
#  define RMLOG_OPEN_FLAGS       (O_APPEND | O_CREAT | O_WRONLY)
#  define RMLOG_OPEN_MODE        0644
#endif

/* ---- 默认目录裁决（与 Python writer.py 完全一致; REQ §7.1 Q2 裁决值） ---- */
#define RMLOG_DEFAULT_DIR   "/userdata/rmlog"
#define RMLOG_FALLBACK_DIR  "/var/log/rmlog"

/* ---- 单文件上限与保留份数（P0 默认值, 与 Python 端 Writer 默认一致） ---- */
#define RMLOG_MAX_BYTES     (2 * 1024 * 1024)
#define RMLOG_KEEP          5

/* 跨进程轮转锁文件名（F-1 修复, 与 Python writer._ROTLOCK_NAME 协议约定一致）:
 * 与日志同目录的隐藏文件, 只作 flock 锁体, 不写入数据、不进副本链。
 * 同一目录混用 C/Python 写入方时, 两端经同一个锁文件互斥轮转。 */
#define RMLOG_ROTLOCK_NAME  ".rmlog.ROTLOCK"

/* 拼接路径用的缓冲（与 g_path 一致; 副本名 = 主名 + ".N"） */
#define RMLOG_PATH_CAP      512

/* 轮转副本路径缓冲容量 = g_path 容量 + 副本序号后缀余量。
 * 副本路径 = g_path(≤RMLOG_PATH_CAP-1 有效字符) + "." + 十进制序号(int 最坏
 * 11 字符含符号)。旧实现用与 g_path 等长的 512 缓冲, 理论上可能截断, 触发
 * gcc -Wformat-truncation（板端 gcc 11.2 实测 ×3）; +16 余量后最坏输出
 * 511+1+11=523 字节也放得下（< 528）, gcc 可证明不截断 —— 从根上消除告警,
 * 而非 -Wno 压制（T-20260927-003）。 */
#define RMLOG_ROTATE_PATH_CAP  (RMLOG_PATH_CAP + 16)

/* 单条行缓冲上限。
 * 容量边界真实表述（F-9 修正）: vsnprintf 把超长消息截断到 RMLOG_LINE_MAX-1 后
 * 仍记录（证据降级好过无证据, 截断计入 g_write_failures）; 但**转义可能膨胀** ——
 * `|`/换行/控制字符各 1 字节膨胀为 4 字节的 \xNN —— 转义后 mod+msg 总长超
 * 2*RMLOG_LINE_MAX-1 的整条事件被**丢弃并计数**（rmlog_line 返回 -1）,
 * 绝不产出坏行。即: "≤1023 字节的消息"不保证可记录, 依赖其中需转义字符的占比。 */
#define RMLOG_LINE_MAX      1024

/* ---- 全局状态（单文件单进程一份; 线程安全靠写锁） ---- */
static RMLOG_LOCK_T g_lock;
static int          g_fd = -1;            /* 日志 fd; <0 表示未打开（重试打开的依据） */
static char         g_path[RMLOG_PATH_CAP]; /* 当前日志文件路径（轮转/诊断用） */
static long         g_seq;                /* 进程内事件序号（跨轮转持续递增） */
static long long    g_own_bytes;          /* 本进程写入计数（轮转触发的廉价预判）:
                                           * 多进程同写时必然偏小（不含他进程字节）
                                           * → 只会偏早触发, 偏早被锁内 stat 确认挡下
                                           * （见 rmlog__rotate_locked）—— 失真方向安全 */
static int          g_open_failed;        /* 打开失败标志: emit 路径逐条重试的依据 */
static int          g_write_failures;     /* 静默降级计数（对齐 Python write_failures） */
static int          g_lock_degradations;  /* 轮转锁获取失败计数（RF-5, 对齐 Python lock_degradations） */
static int          g_ever_opened;        /* seq 只在首次打开时清零 —— 轮转/重开不重置,
                                           * 保证进程内事件全序（与 Python 端一致） */

/* flush 接口在本文件底部实现（rmlog.h 未声明 —— P0 预留, 见文件尾注释） */
int rmlog_flush(void);

/* 轮转链操作（本文件下方实现; 需在持轮转锁后调用） */
static void rmlog__rotate_chain_locked(void);

/* ---- 工具: 目录可用性探测/创建（与 Python Writer._resolve_dir 行为逐字对齐） ----
 * 为什么逐级探测而不是一次建多层: /userdata 是否存在是板端事实（AC8 未核实项）,
 * 探测能把真实落点暴露给 USAGE 指导用户确认。 */
static int rmlog__dir_usable(const char *dir)
{
#if defined(_WIN32)
    DWORD attr = GetFileAttributesA(dir);
    if (attr != INVALID_FILE_ATTRIBUTES && (attr & FILE_ATTRIBUTE_DIRECTORY)) {
        return 1;
    }
    return CreateDirectoryA(dir, NULL) ? 1 : 0;
#else
    struct stat st;
    if (stat(dir, &st) == 0 && S_ISDIR(st.st_mode)) {
        return 1;
    }
    return mkdir(dir, 0755) == 0 ? 1 : 0;
#endif
}

/* ---- 打开日志文件（持锁调用; 语义与 Python os.open(O_APPEND|O_CREAT|O_WRONLY) 一致） ----
 * 目录裁决**只发生一次**（RF-1, 复审报告 F-8 残留面处置）: g_path 已有值
 * （本进程此前以 rmlog_open(dir) 显式指定目录, 或已完成过缺省裁决）时直接
 * 按既有路径重开, 不再重新裁决 —— 否则 close 后再 emit 的"按需重开"会把
 * 事件静默落到缺省目录, rmlog.h 承诺的"重开继续记录"对显式目录形态失实
 * （reviewer probe_c2 实证）。g_path 为空才做缺省裁决, 与 Python 端 Writer
 * 构造期裁决一次的行为对齐。轮转/emit 期的按路径重开走
 * rmlog__reopen_current_locked（同样只复用 g_path, 从不重新裁决）。
 * R3（RF-6）: 裁决与打开分离 —— 本函数内 open 恰好一次（函数尾部）,
 * 各裁决分支不再 open; R2 曾分支内 open + 尾部再 open, 首个 fd 未 close
 * 即被覆盖, 每次按需重开泄漏 1 个句柄（回归探针 probe_fdleak_rf6 守护）。 */
static int rmlog__open_locked(void)
{
    int fd;

    /* 目录裁决段: 只裁决/复用 g_path, 不打开文件（RF-6, R3 结构归位）。
     * 打开动作保留为函数尾部唯一一次 —— R2 曾在各分支内各 open 一次、
     * 尾部又无条件第二次 open, 首个 fd 未 close 即被覆盖, 每次"按需重开"
     * 泄漏 1 个文件句柄（1000 轮 emit→close 实测 +1000, 1:1）。
     * 语义与修复前逐分支等价:
     *   - g_path 为空 → 两级缺省裁决, 命中即拼路径; 两级皆败 → 返回 -1,
     *     g_path 保持为空, 下次 emit 再重试裁决;
     *   - g_path 已有值（显式目录或此前缺省裁决过）→ 跳过裁决直接落到底部
     *     按既有路径重开（RF-1 语义保留: close 后重开落点=最近一次成功
     *     打开的目录, 显式目录形态成立）。 */
    if (g_path[0] == '\0') {
        if (rmlog__dir_usable(RMLOG_DEFAULT_DIR)) {
            snprintf(g_path, sizeof(g_path), "%s/rmlog.log", RMLOG_DEFAULT_DIR);
        } else if (rmlog__dir_usable(RMLOG_FALLBACK_DIR)) {
            snprintf(g_path, sizeof(g_path), "%s/rmlog.log", RMLOG_FALLBACK_DIR);
        } else {
            return -1;   /* 两级缺省目录都不可建: g_path 保持为空, 下次 emit 再重试裁决 */
        }
    }
    /* 文件打开: 全函数唯一一次 open（O_APPEND 是多进程行完整性的根基:
     * 内核保证每次 write 追加到当前末尾）。g_path 已有值时（含显式目录）
     * 直接按既有路径重开。打开失败时不回滚 g_path —— 与修复前语义一致
     * （首 open 失败即整体失败返回 -1）, 下次 emit 按既有 g_path 重试打开。 */
    fd = open(g_path, RMLOG_OPEN_FLAGS, RMLOG_OPEN_MODE);
    if (fd < 0) {
        return -1;
    }
    g_fd = fd;
    if (!g_ever_opened) {
        g_seq = 0;                           /* 仅首次打开清零; 轮转/重开保持全序 */
        g_ever_opened = 1;
    }
    g_open_failed = 0;
    /* g_own_bytes 置 0 交由调用方（rmlog_open / emit 的打开分支）按需赋值 */
    return 0;
}

/* ---- 初始化: Linux 用 pthread_once, Win32 用 INIT_ONCE（均为"恰好一次"原语） ---- */
#if defined(_WIN32)
static INIT_ONCE g_once = INIT_ONCE_STATIC_INIT;
static BOOL CALLBACK rmlog__once_cb(PINIT_ONCE ctx, PVOID param, PVOID *pctx)
{
    (void)ctx; (void)param; (void)pctx;   /* 本初始化无负载参数 */
    RMLOG_LOCK_INIT(g_lock);
    return TRUE;
}
static void rmlog__init_once(void)
{
    InitOnceExecuteOnce(&g_once, rmlog__once_cb, NULL, NULL);
}
#else
static pthread_once_t g_once = PTHREAD_ONCE_INIT;
static void rmlog__once_cb(void)
{
    RMLOG_LOCK_INIT(g_lock);
}
static void rmlog__init_once(void)
{
    pthread_once(&g_once, rmlog__once_cb);
}
#endif

/* ---- 转义: 与 Python format._escape 同一映射表（AC4 双端一致的根基） ----
 * 顺序敏感: 反斜杠最先; 控制字符统一 \xNN; 溢出截断并返回 -2（调用方计数丢弃）。 */
int rmlog_escape(const char *src, char *buf, size_t buflen)
{
    size_t o = 0;
    const unsigned char *p = (const unsigned char *)src;

    if (!src || !buf || buflen == 0) {
        return -1;
    }
    while (*p) {
        char tmp[8];
        const char *rep;
        switch (*p) {
        case '\\': rep = "\\\\";  break;
        case '|':  rep = "\\x7c"; break;
        case '\r': rep = "\\x0d"; break;
        case '\n': rep = "\\x0a"; break;
        case '\t': rep = "\\x09"; break;
        default:
            if (*p < 0x20 || *p == 0x7F) {
                snprintf(tmp, sizeof(tmp), "\\x%02x", (unsigned)*p);
                rep = tmp;
            } else {
                tmp[0] = (char)*p; tmp[1] = '\0';
                rep = tmp;
            }
            break;
        }
        {
            size_t n = strlen(rep);
            if (o + n >= buflen) {
                buf[o] = '\0';
                return -2;               /* 溢出: 截断并报错, 绝不产出坏行 */
            }
            memcpy(buf + o, rep, n);
            o += n;
        }
        p++;
    }
    buf[o] = '\0';
    return (int)o;
}

/* ---- 双端一致性渲染接口（AC4 用）: 与 Python format.encode 字段序逐字对齐 ---- */
int rmlog_line(long seq, const char *wall_ts, long mono_ms,
               const char *level, const char *code, const char *mod,
               const char *msg, char *buf, size_t buflen)
{
    char e_mod[RMLOG_LINE_MAX];
    char e_msg[RMLOG_LINE_MAX];
    int  n;

    if (!wall_ts || !level || !code || !mod || !msg || !buf || buflen == 0) {
        return -1;
    }
    if (rmlog_escape(mod, e_mod, sizeof(e_mod)) < 0) {
        return -1;
    }
    if (rmlog_escape(msg, e_msg, sizeof(e_msg)) < 0) {
        return -1;
    }
    n = snprintf(buf, buflen, "LOGV1|%ld|%s|%ld|%s|%s|%s|%s",
                 seq, wall_ts, mono_ms, level, code, e_mod, e_msg);
    if (n < 0 || (size_t)n >= buflen) {
        return -1;
    }
    return n;
}

/* ---- 墙上时间戳: 与 Python wall_timestamp() 同格式（ISO8601 本地毫秒） ----
 * 平台差异: Win32 GetLocalTime / POSIX localtime_r+gettimeofday, 均取本地时区;
 * 板端时区与 NTP 约定属部署配置（USAGE §6）, 格式本身双端一致。 */
static void rmlog__wall_ts(char *buf, size_t cap)
{
#if defined(_WIN32)
    SYSTEMTIME st;
    GetLocalTime(&st);
    snprintf(buf, cap, "%04d-%02d-%02dT%02d:%02d:%02d.%03d",
             st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond,
             st.wMilliseconds);
#else
    struct tm tmv;
    struct timeval tv;
    gettimeofday(&tv, NULL);
    localtime_r(&tv.tv_sec, &tmv);
    snprintf(buf, cap, "%04d-%02d-%02dT%02d:%02d:%02d.%03d",
             tmv.tm_year + 1900, tmv.tm_mon + 1, tmv.tm_mday,
             tmv.tm_hour, tmv.tm_min, tmv.tm_sec, (int)(tv.tv_usec / 1000));
#endif
}

/* ---- 单调时间戳（毫秒）: Win32 QPC / POSIX CLOCK_MONOTONIC（防 NTP 倒流） ---- */
static long rmlog__mono_ms(void)
{
#if defined(_WIN32)
    static LARGE_INTEGER freq;
    static int freq_init = 0;
    LARGE_INTEGER now;
    if (!freq_init) {
        QueryPerformanceFrequency(&freq);
        freq_init = 1;
    }
    QueryPerformanceCounter(&now);
    return (long)(now.QuadPart * 1000 / freq.QuadPart);
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (long)(ts.tv_sec * 1000 + ts.tv_nsec / 1000000);
#endif
}

/* ---- 轮转协议 v2（R1 返工, 修复 F-1; C 端实现, 语义与 Python writer.py 对齐） ----
 *
 * 旧协议（R0）: 常驻 fd 持续追加 → 超限 close → rename 链 → reopen。
 * 缺陷: 对其他进程的 fd 与计数零感知 —— A 进程把 rmlog.log 改名进副本链后,
 * B 进程的 fd 仍绑在旧 inode 上写; B 后续轮转把这段新近数据连同旧 inode
 * 一起挪进副本链、再被"删最老副本"当作垃圾淘汰 —— B 已确认写成功的事件
 * 从磁盘上消失（reviewer probe_1e/1g 实证）。
 *
 * v2 的两条不变量（推理链详见 Python 端 writer.py 模块头, C 端逐条对应）:
 *   1. 写入目标 = 本进程 open 那一刻 g_path 所指的文件; 该文件此后只会沿
 *      path → .1 → ... → .keep 被 rename, 一条已落盘的行至少要再经历 keep 次
 *      完整轮转才会被淘汰 —— 保留语义与单进程一致, 不存在"整文件当垃圾删";
 *   2. rename 链全程持跨进程 flock（.rmlog.ROTLOCK, 与 Python 端同名锁文件）
 *      —— "replace 掉对方还没来得及 shift 的副本"这一唯一能凭空抹数据的
 *      竞争被锁排除; 锁内再做 stat 确认（真实大小仍超限才轮转）, 消除
 *      "他进程刚轮转过、我方计数陈旧"的过早轮转。
 *
 * 写路径配合: 每次 emit 前经 rmlog__reopen_current_locked 对准当前路径 ——
 * fd 若还绑在他进程已改名的旧 inode 上（上一轮轮转由他进程完成）, 会先
 * 关旧 fd、重开当前路径的新文件, 再写入。
 */
#if !defined(_WIN32)

/* POSIX: 跨进程轮转锁（flock 独占; advisory 锁, 互斥前提 = 同目录所有写入方
 * 都经本组件/本协议 —— 比赛部署形态成立）。返回锁 fd, 失败返回 -1。
 * flock 随 close 自动释放, 正常路径仍显式 LOCK_UN（清晰优先, 双保险一致）。 */
static int rmlog__rotlock_acquire(void)
{
    char lock_path[RMLOG_PATH_CAP];
    int lfd;
    const char *slash;

    if (g_path[0] == '\0') {
        return -1;
    }
    /* 锁文件与日志同目录: 取 g_path 的目录部分拼锁名（g_path 末段是 rmlog.log） */
    slash = strrchr(g_path, '/');
    if (slash) {
        snprintf(lock_path, sizeof(lock_path), "%.*s/%s",
                 (int)(slash - g_path), g_path, RMLOG_ROTLOCK_NAME);
    } else {
        snprintf(lock_path, sizeof(lock_path), "%s", RMLOG_ROTLOCK_NAME);
    }
    lfd = open(lock_path, O_CREAT | O_RDWR, 0666);
    if (lfd < 0) {
        return -1;
    }
    if (flock(lfd, LOCK_EX) != 0) {
        close(lfd);
        return -1;
    }
    return lfd;
}

static void rmlog__rotlock_release(int lfd)
{
    if (lfd >= 0) {
        flock(lfd, LOCK_UN);     /* 显式解锁; 即便失败 close 也会释放 */
        close(lfd);
    }
}

#else

/* Windows（开发机 MinGW）: 无 flock —— C 端在 Windows 上退化为"进程内轮转"
 * （线程锁仍保证本进程安全）。理由: 双进程×轮转组合的演示用例跑在 Python 端
 * （selftest 可跨平台覆盖该组合）; C 端板端目标 Linux 有原生 flock, 协议完整。
 * 该取舍与两侧行字节流一致性（AC4）无关, 属部署行为差异, IMPL §4 已声明。
 * 返回 -2（约定值"无跨进程锁可用", 非 -1）: 调用方只对 -1 计
 * g_lock_degradations —— 平台本就无跨进程锁, 不算降级事件（RF-5 口径）。 */
static int rmlog__rotlock_acquire(void)
{
    return -2;                   /* 约定值: "无跨进程锁可用"（非错误） */
}

static void rmlog__rotlock_release(int lfd)
{
    (void)lfd;
}

#endif

/* 轮转链操作: rmlog.log -> .1 -> ... -> .keep, 最老删除。
 * 调用方必须已持跨进程轮转锁（或平台无跨进程锁, 见上）。逐段失败保守跳过:
 * 轮转是容量治理, 宁可超限也不冒险; 失败段下次轮转重试, 数据不丢。
 * 副本路径缓冲用 RMLOG_ROTATE_PATH_CAP（比 g_path 大 16）: 保证任何合法
 * g_path（≤511 字符）加 ".N" 序号后缀都不截断, gcc -Wformat-truncation 可
 * 证明不截断（根上消除告警, 非 -Wno 压制; 详见 RMLOG_ROTATE_PATH_CAP 注释）。 */
static void rmlog__rotate_chain_locked(void)
{
    char src[RMLOG_ROTATE_PATH_CAP], dst[RMLOG_ROTATE_PATH_CAP];
    int i;

    for (i = RMLOG_KEEP - 1; i >= 1; i--) {
        snprintf(src, sizeof(src), "%s.%d", g_path, i);
        snprintf(dst, sizeof(dst), "%s.%d", g_path, i + 1);
#if defined(_WIN32)
        remove(dst);
#endif
        rename(src, dst);
    }
    snprintf(dst, sizeof(dst), "%s.1", g_path);
#if defined(_WIN32)
    remove(dst);
#endif
    rename(g_path, dst);
}

/* 轮转决策入口（持写锁调用; 写入成功且 g_own_bytes 超限后执行）:
 * 取跨进程轮转锁 → 锁内 stat 确认 → 链操作 → 释放锁。
 * 拿锁失败: 放弃本轮轮转（数据留在原文件不丢, 下次写入再触发）;
 * 计入 g_lock_degradations 可观测（RF-5, 与 Python 端 lock_degradations
 * 同口径）—— 否则"容量治理暂停"没有任何外部信号。
 * 线程安全: 本函数只在持写锁的 emit 路径被调, 计数自增无竞争（RF-5）。 */
static void rmlog__rotate_locked(void)
{
    struct stat st;
    int lfd;

    lfd = rmlog__rotlock_acquire();
    if (lfd == -1) {
        /* 锁不可得（锁文件 open 失败 / flock 失败）: 放弃本轮, 保守不冒险 */
        g_lock_degradations++;
        return;
    }
    /* 锁内 stat 确认（F-1 推理链 2）: 本进程 g_own_bytes 不含他进程写入,
     * 必然偏小 → 只会偏早触发; 用真实文件大小做最终裁决, 他进程刚轮转过
     * （现文件尚小）时放弃并把计数校准为真实值, 避免保留期失真。 */
    if (stat(g_path, &st) == 0 && st.st_size > (long long)RMLOG_MAX_BYTES) {
        rmlog__rotate_chain_locked();
        g_own_bytes = 0;         /* 主文件已改名走, 本进程后续写入重建新文件 */
    } else if (stat(g_path, &st) == 0) {
        g_own_bytes = (long long)st.st_size;   /* 校准: 消除陈旧偏大 */
    }
    rmlog__rotlock_release(lfd);
}

/* 让当前 fd 对准 g_path 当前所指的文件（每次 emit 前调用; 持写锁）。
 * 这是协议 v2 的写侧配合点: 旧协议的 fd 可能绑在他进程已改名的旧 inode 上
 * —— 那正是数据被"整文件淘汰"的通道。这里检测并纠正:
 *   - fd 有效且 fstat 的 size/inode 与 stat(g_path) 一致 → 直接复用（快路径）;
 *   - 否则关旧 fd、按路径重开 —— O_APPEND 落点回到当前文件。
 * inode 对比在 POSIX 上用 st_ino（同文件必同 inode）; Windows 无可靠 inode,
 * 用 size 一致的近似（C 端 Windows 路径不参与跨进程轮转演示, 见上）。 */
static int rmlog__reopen_current_locked(void)
{
    struct stat st_path, st_fd;

    if (g_fd >= 0) {
        if (stat(g_path, &st_path) == 0
            && fstat(g_fd, &st_fd) == 0
            && st_fd.st_size == st_path.st_size
#if !defined(_WIN32)
            && st_fd.st_ino == st_path.st_ino
#endif
        ) {
            return 0;            /* fd 仍指向当前文件: 复用 */
        }
        close(g_fd);
        g_fd = -1;
    }
    g_fd = open(g_path, RMLOG_OPEN_FLAGS, RMLOG_OPEN_MODE);
    if (g_fd < 0) {
        return -1;
    }
    g_own_bytes = 0;     /* 对准后的计数基线重置; 既有内容由轮转 stat 确认兜底 */
    if (!g_ever_opened) {
        g_seq = 0;
        g_ever_opened = 1;
    }
    return 0;
}

/* ---- 写入路径（持锁）: 对准当前文件 → 组行 → O_APPEND 一次 write → 条件同步 → 轮转 ---- */
static void rmlog__emit_locked(int level, const char *mod, const char *code,
                               const char *msg)
{
    char wall[40];
    char line[RMLOG_LINE_MAX * 2];
    char out[RMLOG_LINE_MAX * 2 + 1];
    int  n;
    size_t total;
    /* 数值级别 -> 级别字符串: 顺序与 Python format.LEVELS 语义一致 */
    const char *lvl = (level >= RMLOG_LVL_FATAL) ? "FATAL"
                    : (level >= RMLOG_LVL_ERROR) ? "ERROR"
                    : (level >= RMLOG_LVL_WARN)  ? "WARN"
                    : "INFO";

    if (g_fd < 0) {
        /* 未打开: 重试打开（F-5 修复语义 —— 每条事件都是一次全新尝试,
         * 打开失败计数后返回, 无"一次失败永久停记"状态）。 */
        if (rmlog__open_locked() != 0) {
            g_open_failed = 1;
            g_write_failures++;
            return;
        }
        g_own_bytes = 0;     /* 只计本进程后续写入; 既有内容由轮转 stat 确认兜底 */
    } else {
        /* fd 已开: 先对准当前路径（协议 v2 写侧配合, 见该函数上方注释）。
         * 对准失败按打开失败处理（计数, 本条放弃, 下条重试）。 */
        if (rmlog__reopen_current_locked() != 0) {
            g_open_failed = 1;
            g_write_failures++;
            return;
        }
    }
    g_open_failed = 0;
    g_seq++;
    rmlog__wall_ts(wall, sizeof(wall));
    n = rmlog_line(g_seq, wall, rmlog__mono_ms(), lvl, code, mod, msg,
                   line, sizeof(line));
    if (n < 0) {
        g_write_failures++;              /* 渲染失败: 计数丢弃, 不产出半行 */
        return;
    }
    total = (size_t)n;
    memcpy(out, line, total);
    out[total] = '\n';
    {
        ssize_t w = write(g_fd, out, total + 1);
        if (w < 0 || (size_t)w != total + 1) {
            /* 部分写入: 与 Python 端一致重试补写剩余部分; 仍失败则放弃 ——
             * 理论上 O_APPEND 常规 write 不会出现, 防御磁盘满等极端情况 */
            ssize_t w2 = (w > 0) ? write(g_fd, out + w, (size_t)(total + 1 - w))
                                 : write(g_fd, out, total + 1);
            if (w2 < 0 || (w > 0 && (size_t)w + (size_t)w2 != total + 1)
                       || (w <= 0 && (size_t)w2 != total + 1)) {
                g_write_failures++;
                return;
            }
        }
    }
    g_own_bytes += (long long)total + 1;
    if (level >= RMLOG_LVL_ERROR) {
        RMLOG_FDATASYNC(g_fd);           /* ERROR/FATAL 先落盘再返回（AC6） */
    }
    if (g_own_bytes > RMLOG_MAX_BYTES) {
        rmlog__rotate_locked();
    }
}

/* ---- 对外: 业务宏族最终走这里（rmlog.h 的 RMLOG_I/W/E/F 展开目标） ---- */
int rmlog_emit(int level, const char *mod, const char *code, const char *fmt, ...)
{
    char msg[RMLOG_LINE_MAX];
    va_list ap;
    int n;

    rmlog__init_once();
    va_start(ap, fmt);
    n = vsnprintf(msg, sizeof(msg), fmt, ap);
    va_end(ap);
    if (n < 0) {
        g_write_failures++;              /* 格式化失败: 计数, 绝不崩溃（REQ P0-c） */
        return -1;
    }
    if ((size_t)n >= sizeof(msg)) {
        g_write_failures++;              /* 超长截断: 记录降级证据并计数（见 RMLOG_LINE_MAX） */
    }
    RMLOG_LOCK(g_lock);
    rmlog__emit_locked(level, mod, code, msg);
    RMLOG_UNLOCK(g_lock);
    return 0;
}

/* ---- 生命周期 ---- */
int rmlog_open(const char *dir)
{
    rmlog__init_once();
    RMLOG_LOCK(g_lock);
    if (g_fd >= 0) {
        RMLOG_UNLOCK(g_lock);
        return 0;                        /* 幂等: 已打开直接成功 */
    }
    if (dir != NULL) {
        /* 与 Python 端 os.makedirs(exist_ok=True) 对齐: 目录不存在先创建
         * （单级创建 —— 与 mkdir 语义一致, 多级目录由部署方预先建好, USAGE 注明） */
        if (!rmlog__dir_usable(dir)) {
            RMLOG_UNLOCK(g_lock);
            return -1;
        }
        snprintf(g_path, sizeof(g_path), "%s/rmlog.log", dir);
        g_fd = open(g_path, RMLOG_OPEN_FLAGS, RMLOG_OPEN_MODE);
        if (g_fd >= 0) {
            if (!g_ever_opened) {
                g_seq = 0;
                g_ever_opened = 1;
            }
            g_own_bytes = 0;   /* 只计自己后续写入; 既有内容由轮转 stat 确认兜底 */
            g_open_failed = 0;
            RMLOG_UNLOCK(g_lock);
            return 0;
        }
        RMLOG_UNLOCK(g_lock);
        return -1;
    }
    if (rmlog__open_locked() != 0) {
        g_open_failed = 1;
        RMLOG_UNLOCK(g_lock);
        return -1;
    }
    g_own_bytes = 0;     /* 只计本进程后续写入; 既有内容由轮转 stat 确认兜底 */
    RMLOG_UNLOCK(g_lock);
    return 0;
}

void rmlog_close(void)
{
    rmlog__init_once();
    RMLOG_LOCK(g_lock);
    if (g_fd >= 0) {
        RMLOG_FDATASYNC(g_fd);           /* 退出前把缓冲的 INFO/WARN 也落盘 */
        close(g_fd);
        g_fd = -1;
        /* 注意: close 后 g_open_failed 不置位、g_path 保留 —— 与 rmlog.h 的
         * close 语义注释一致, 后续 emit 会按需重新打开**同一落点**继续记录
         * （重开复用 g_path, 显式目录形态同样成立 —— 见 rmlog__open_locked
         * 的 RF-1 注释）。 */
    }
    RMLOG_UNLOCK(g_lock);
}

int rmlog_flush(void)
{
    rmlog__init_once();
    RMLOG_LOCK(g_lock);
    if (g_fd < 0) {
        RMLOG_UNLOCK(g_lock);
        return -1;
    }
    RMLOG_FDATASYNC(g_fd);
    RMLOG_UNLOCK(g_lock);
    return 0;
}

const char *rmlog_path(void)
{
    /* 仅诊断用; 未加锁读 g_path —— 诊断通道不做强一致承诺（IMPL 已注明） */
    return (g_fd >= 0) ? g_path : NULL;
}
