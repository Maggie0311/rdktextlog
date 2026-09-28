/* （maintainer 补注：C 端对外唯一头文件。业务侧只需认识两样 —— 宏族 RMLOG_I/W/E/F(mod, code, fmt, ...)
 * （一行记一条事件，级别由宏决定）与 rmlog_open/rmlog_close 生命周期；RMLOG_CODE_* 常量来自 include 的
 * 生成物 rmlog_errors.h。一个易踩的语义点（见下方生命周期注释块）：close 后再调宏不是无操作，
 * emit 会按需重开继续记录，重开落点=最近一次成功打开的目录 —— 想真正停记就不要在 close 后再调宏。） */
/*
 * rmlog.h — RoboMaster 文本日志平台 C 接口（对外唯一头文件）。
 *
 * 任务: T-20260926-001-logging-platform-p0（REQ §4 P0-c）。
 *
 * 能力: 宏族 RMLOG_I/W/E/F(mod, code, fmt, ...) 一行记录一条事件;
 *       线程安全; 格式化失败不崩溃; 行格式与 Python 端 rmlog.format 同构（AC4）;
 *       错误码常量与 Python 端 catalog.py 同源（本头文件 include 生成物）。
 *
 * 典型用法（业务代码）:
 *     #include "rmlog.h"
 *     RMLOG_I("ctrl", RMLOG_CODE_INIT_000, "控制线程就绪 freq=%dHz", freq);
 *     RMLOG_E("spi",  RMLOG_CODE_COMM_001, "SPI 传输超时 dev=%s", dev);
 *     RMLOG_F("fsm",  RMLOG_CODE_FSM_004,  "状态机进入未定义状态 state=%d", st);
 *
 * 线程安全: 内部 pthread_once 初始化 + 每线程格式化缓冲 + 全局写锁,
 * 多线程并发调用安全; 多进程安全由 O_APPEND 一次 write 一行保证（见 rmlog.c）。
 *
 * 平台差异: 目标环境 Linux/X5（fdatasync/fsync/pthread）; 开发机 MinGW 自测时
 * _WIN32 分支等效实现 —— 两侧行字节流完全一致（自测 AC4 验证）。
 */
#ifndef RMLOG_H
#define RMLOG_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* 错误码常量与级别常量: 生成物（勿手改）, 单一来源 catalog.py */
#include "rmlog_errors.h"

/* ---- 级别常量别名（rmlog_errors.h 已定义 RMLOG_LVL_*; 此处提供语义别名,
 *      让宏族实现与 Python format.LEVELS 顺序对齐的意图显式化） ---- */
#define RMLOG_INFO  RMLOG_LVL_INFO
#define RMLOG_WARN  RMLOG_LVL_WARN
#define RMLOG_ERROR RMLOG_LVL_ERROR
#define RMLOG_FATAL RMLOG_LVL_FATAL

/* ---- 宏族: 业务一行记录。level 由错误码查表得默认级别（见 rmlog.c）。
 *      mod  : 模块名字符串字面量（如 "ctrl"）;
 *      code : 错误码字符串（建议用 RMLOG_CODE_* 常量, 也允许任意同格式码）;
 *      fmt/... : 消息 printf 风格格式串与参数。
 *      宏内部把 fmt/code/mod 包成字符串交给实现函数, 避免在调用点展开复杂逻辑,
 *      也保证 -Wall 下无副作用表达式问题。 */
#define RMLOG_I(mod, code, ...) rmlog_emit(RMLOG_LVL_INFO,  (mod), (code), __VA_ARGS__)
#define RMLOG_W(mod, code, ...) rmlog_emit(RMLOG_LVL_WARN,  (mod), (code), __VA_ARGS__)
#define RMLOG_E(mod, code, ...) rmlog_emit(RMLOG_LVL_ERROR, (mod), (code), __VA_ARGS__)
#define RMLOG_F(mod, code, ...) rmlog_emit(RMLOG_LVL_FATAL, (mod), (code), __VA_ARGS__)

/* 高级: 显式指定级别（覆盖码表默认级别）—— 对齐 Python writer.event(level=...) */
int rmlog_emit(int level, const char *mod, const char *code, const char *fmt, ...);

/* ---- 生命周期 ----
 * rmlog_open: 打开/初始化日志。dir 为 NULL 时用默认裁决:
 *   RMLOG_DEFAULT_DIR 存在 -> 用之; 否则 RMLOG_FALLBACK_DIR（与 Python 端一致）。
 * 返回 0 成功; 非 0 失败（业务可据此决定降级策略; 之后仍可调用 RMLOG_*,
 * 会重试初始化一次, 仍失败则静默丢弃 —— 日志故障不拖垮业务）。
 * rmlog_close: 进程退出前调用（把缓冲中的 INFO/WARN 落盘后关闭句柄）。
 * 注意: close 后再次调用 RMLOG_* 宏**并非无操作** —— emit 会按需重新打开
 * 日志文件继续记录（幂等重开的语义, 与 "打开失败重试" 共用同一路径）;
 * 重开落点 = 本进程最近一次成功打开的目录（RF-1: 以 rmlog_open(dir) 显式
 * 指定目录打开过的, close 后重开仍落该目录, 不改投缺省目录; 从未成功
 * 打开过则按缺省裁决重试）。若业务期望 "close 即停记", 请保证 close 后
 * 不再调用宏。 */
int  rmlog_open(const char *dir);
void rmlog_close(void);

/* 取当前日志文件完整路径（诊断用; 未初始化返回 NULL）。 */
const char *rmlog_path(void);

/* 双端一致性自测接口（AC4 用; 业务勿用）:
 * 按给定输入渲染一行（不带换行）, 与 Python rmlog.encode_line 输出逐字节对照。
 * seq/mono_ms 由调用方给定以消除双端取时间差异。返回写入 buf 的字节数。 */
int rmlog_line(long seq, const char *wall_ts, long mono_ms,
               const char *level, const char *code, const char *mod,
               const char *msg, char *buf, size_t buflen);

/* 转义函数暴露（自测 AC4 对照用; 业务勿用）: 返回写入 buf 的字节数。 */
int rmlog_escape(const char *src, char *buf, size_t buflen);

#ifdef __cplusplus
}
#endif

#endif /* RMLOG_H */
