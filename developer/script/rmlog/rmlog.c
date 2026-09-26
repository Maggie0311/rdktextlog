/*
 * rmlog.c — RoboMaster 文本日志平台 C 实现。
 *
 * 任务: T-20260926-001-logging-platform-p0（REQ §4 P0-c/P0-d）。
 *
 * 设计决策（与 Python 端 writer.py/format.py 对齐，理由见对应文件头）:
 * - O_APPEND + 一次 write() 写一条完整行（含换行）—— 多进程行完整性根基（AC5）;
 * - 每条事件立即 write（进内核页缓存）; ERROR/FATAL 写后立即 fdatasync
 *   （关键证据先落盘再返回, AC6）; INFO/WARN 由 rmlog_close/rmlog_flush
 *   统一 fsync 落盘（P0 取舍: 硬崩溃时 INFO/WARN 可能滞留页缓存, IMPL 记录）;
 * - 日志故障不拖垮业务: 打开失败后 emit 静默重试一次, 仍失败静默丢弃并计数;
 * - 行编码与 Python format.py 同构: 同一转义表、同一字段序、同一时间戳格式（AC4）。
 *
 * 平台差异:
 * - 目标环境 Linux/X5: pthread / fdatasync / clock_gettime 原生可用;
 * - 开发机 MinGW: 无 pthread, 用 Win32 Critical Section + INIT_ONCE 等效实现;
 *   fdatasync 用 _commit 等效。两侧行字节流完全一致（selftest AC4 验证）。
 */
#include "rmlog.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>
#include <sys/types.h>

/* ---- 平台适配层: 锁原语 + fd 级同步 + open 标志 ---- */
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

/* 单条行缓冲上限。超长消息: C 端 vsnprintf 截断后仍记录（证据降级好过无证据）,
 * 截断事实计入 g_write_failures 供健康检查审计。 */
#define RMLOG_LINE_MAX      1024

/* ---- 全局状态（单文件单进程一份; 线程安全靠写锁） ---- */
static RMLOG_LOCK_T g_lock;
static int          g_fd = -1;            /* 日志 fd; <0 表示未打开 */
static char         g_path[512];          /* 当前日志文件路径（诊断用） */
static long         g_seq;                /* 进程内事件序号（跨轮转持续递增） */
static int          g_bytes;              /* 当前文件字节数（写后累计, 免 stat） */
static int          g_open_failed;        /* 打开失败标志: emit 静默重试一次的依据 */
static int          g_write_failures;     /* 静默降级计数（对齐 Python write_failures） */
static int          g_ever_opened;        /* seq 只在首次打开时清零 —— 轮转/重开不重置,
                                              保证进程内事件全序（与 Python 端一致） */

/* flush 接口在本文件底部实现（rmlog.h 未声明 —— P0 预留, 见文件尾注释） */
int rmlog_flush(void);

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

/* ---- 打开日志文件（持锁调用; 语义与 Python os.open(O_APPEND|O_CREAT|O_WRONLY) 一致） ---- */
static int rmlog__open_locked(void)
{
    const char *dir;
    int fd;

    if (rmlog__dir_usable(RMLOG_DEFAULT_DIR)) {
        dir = RMLOG_DEFAULT_DIR;
    } else if (rmlog__dir_usable(RMLOG_FALLBACK_DIR)) {
        dir = RMLOG_FALLBACK_DIR;
    } else {
        return -1;
    }
    snprintf(g_path, sizeof(g_path), "%s/rmlog.log", dir);
    /* O_APPEND 是多进程行完整性的根基: 内核保证每次 write 追加到当前末尾 */
    fd = open(g_path, RMLOG_OPEN_FLAGS, RMLOG_OPEN_MODE);
    if (fd < 0) {
        return -1;
    }
    g_fd = fd;
    if (!g_ever_opened) {
        g_seq = 0;                           /* 仅首次打开清零; 轮转/重开保持全序 */
        g_ever_opened = 1;
    }
    g_bytes = (int)lseek(fd, 0, SEEK_END);   /* 追加模式: 现文件大小即起始偏移 */
    g_open_failed = 0;
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

/* ---- 轮转: rmlog.log -> .1 -> ... -> .keep, 最老删除（与 Python 语义一致） ----
 * 平台差异: Win32 rename 不许目标存在, 先 remove; POSIX rename 原子替换。
 * 失败保守放弃本轮轮转（下条日志继续追加, 数据不丢; 下次写入再触发）。 */
static void rmlog__rotate_locked(void)
{
    char src[512], dst[512];
    int i;

    close(g_fd);
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
    g_fd = open(g_path, RMLOG_OPEN_FLAGS, RMLOG_OPEN_MODE);
    if (g_fd < 0) {
        g_open_failed = 1;               /* 重开失败: emit 路径下次静默重试 */
        return;
    }
    g_bytes = 0;
}

/* ---- 写入路径（持锁）: 组行 -> O_APPEND 一次 write -> 条件同步 -> 轮转 ---- */
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
        if (g_open_failed) {
            return;                      /* 已失败过: 静默丢弃, 不反复撞盘 */
        }
        if (rmlog__open_locked() != 0) {
            g_open_failed = 1;
            g_write_failures++;
            return;
        }
    }
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
    g_bytes += (int)total + 1;
    if (level >= RMLOG_LVL_ERROR) {
        RMLOG_FDATASYNC(g_fd);           /* ERROR/FATAL 先落盘再返回（AC6） */
    }
    if (g_bytes > RMLOG_MAX_BYTES) {
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
            g_bytes = (int)lseek(g_fd, 0, SEEK_END);
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
