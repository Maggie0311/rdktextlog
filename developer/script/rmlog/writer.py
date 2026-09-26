# -*- coding: utf-8 -*-
"""rmlog.writer — 事件写入端: 多进程安全追加、可控 flush、按大小轮转。

任务: T-20260926-001-logging-platform-p0（REQ §4 P0-c/P0-d）。

可靠性设计（对应 REQ P0-d "崩溃/断电取证"）:
- **O_APPEND + 一次 write 一条完整行**：文件以 os.O_APPEND 打开，内核把每次
  write 追加到当前末尾；多个进程各写完整行时，写入互相独立、不产生交错半行。
  本组件**绝不**把一行拆成多次 write —— 这是行完整性的根基（AC5）。
- **flush 策略可配置**（对应"写入路径短且可控 flush"）:
    - FATAL/ERROR 级事件**必须** flush（关键证据先落盘再返回 —— AC6 的根基:
      业务进程随后硬崩溃/断电时，最后一条错误事件已在页缓存→磁盘的提交路径上，
      配合 OS 周期回写可被取证；绝对零丢失需 fsync，见下）;
    - 其余级别默认缓冲（性能路径短），可通过 flush_levels 放宽/收紧;
    - 传 fsync=True 可对关键事件强制 fsync（每条一次系统调用，约 1-10ms 级,
      1kHz 场景不可承受，故 P0 默认关闭、接口预留）。
- **按大小轮转保留 N 份**：超过 max_bytes 即轮转 rmlog.log -> rmlog.log.1 -> ...；
  最老的直接删除。轮转在"写入后"检查 —— 宁可当前文件短暂超限，也不在写入前
  引入 stat 与两次 rename 的复杂路径；超限量级为单条行长度，比赛取证可接受。
- **写失败静默降级**：日志组件自身故障不允许打断业务（CODE-STYLE §4.1），
  写失败仅累加 write_failures 计数器，由自测/健康检查读取。

多进程行为: 每个进程独立 Writer 实例，只依赖 O_APPEND 语义互斥，无进程间锁 ——
锁意味着共享状态与更长的临界区，而 O_APPEND 已给出行级原子性。
同进程多线程由 threading.Lock 保护 seq 计数与轮转 rename（线程安全要求, REQ P0-c）。

平台差异（诚实标注）:
- Linux（X5 目标环境）: open(2) 的 O_APPEND 为内核级原子追加 —— 单次 write
  天然行原子, 多进程零额外开销, 上述结论成立;
- Windows（本轮开发自测环境）: CRT 的 _O_APPEND 是"每次写前 seek 到末尾",
  seek+write 跨进程**不原子**, 并发追加会互相覆盖丢行。为让同一份代码在
  开发机也能等效演示多进程安全, Windows 路径在写入前对本文件字节 0 加
  排程锁（msvcrt.locking, 纯标准库）串行化各进程的 append; 这段代码仅
  os.name == "nt" 生效, Linux 板端为零开销的纯 O_APPEND 路径。
  **Windows 自测结果不得表述为 Linux 已验证**（TASK 增补第 3 条）。
"""

import os
import threading
import time

# Windows 开发机专用的字节锁（Linux 上恒为 None, 走纯 O_APPEND 路径）
if os.name == "nt":
    import msvcrt
else:
    msvcrt = None

from . import format as fmt

# 日志文件与轮转副本的默认命名（与 USAGE.md 部署章节保持一致）
DEFAULT_FILENAME = "rmlog.log"
DEFAULT_DIR = "/userdata/rmlog"      # REQ §7 Q2 裁决: root + /userdata/rmlog
FALLBACK_DIR = "/var/log/rmlog"      # /userdata 不存在时的回退路径（Q2）

# O_BINARY 仅 Windows 需要（禁止 CRT 文本模式改写 \n）; Linux 上不存在该标志,
# 用 getattr 取 0 兜底 —— 这是"同一份代码双端可跑"的必要适配点
_O_BINARY = getattr(os, "O_BINARY", 0)


class Writer:
    """单文件追加式日志写入器（一个实例对应一个日志文件）。

    典型用法（业务代码只碰这三个方法）::

        from rmlog.writer import Writer
        w = Writer()                      # 默认 /userdata/rmlog/rmlog.log
        w.event("E-INIT-000", "ctrl", "控制线程就绪")
        w.close()
    """

    def __init__(self, log_dir=None, max_bytes=2 * 1024 * 1024, keep=5,
                 flush_levels=("ERROR", "FATAL"), fsync=False):
        """初始化写入器并打开日志文件。

        参数:
            log_dir      日志目录; None 时走 DEFAULT_DIR，不存在自动回退 FALLBACK_DIR
                         （目录都建不出来时抛 OSError —— 这是构造期唯一允许的失败,
                         因为此时"降级继续"只会把故障藏得更深; 写入期失败才静默降级）
            max_bytes    单文件大小上限（字节），超过即轮转
            keep         保留份数: rmlog.log + keep 个 .1/.2/... 副本
            flush_levels flush 触发级别集合（默认 ERROR 及以上）
            fsync        True 时 flush 级事件额外 fsync（强持久化, 性能代价大, 默认关）
        """
        self.max_bytes = max_bytes
        self.keep = keep
        self.flush_levels = set(flush_levels)
        self.fsync = fsync
        self.log_dir = log_dir if log_dir is not None else self._resolve_dir()
        os.makedirs(self.log_dir, exist_ok=True)
        self.path = os.path.join(self.log_dir, DEFAULT_FILENAME)
        self.path = os.path.abspath(self.path)
        # 线程锁: 保护 seq 自增与轮转 rename 的原子性（多线程共用实例时）
        self._lock = threading.Lock()
        self._seq = 0            # 本进程事件序号（跨轮转持续递增, 不随文件重置）
        self._fd = os.open(self.path, os.O_APPEND | os.O_CREAT | os.O_WRONLY | _O_BINARY, 0o644)
        self._bytes = os.fstat(self._fd).st_size
        # 健康计数器: 写失败次数（静默降级的可观测出口, selftest 与健康检查用）
        self.write_failures = 0
        self.last_error = None

    @staticmethod
    def _resolve_dir():
        """默认目录裁决: /userdata/rmlog 存在或可创建则用它, 否则回退 /var/log/rmlog。

        为什么探测而不是直接 makedirs: /userdata 分区是否存在是板端事实（AC8
        未核实项）, 开发机与未知板上都可能出现"第一层就不存在"的情况;
        逐级探测比一次 makedirs 多层路径更能暴露真实落点, 便于 USAGE 指导用户确认。
        """
        if os.path.isdir(DEFAULT_DIR):
            return DEFAULT_DIR
        try:
            os.makedirs(DEFAULT_DIR, exist_ok=True)
            return DEFAULT_DIR
        except OSError:
            return FALLBACK_DIR

    def event(self, code, module, message, level=None, attrs=None):
        """写入一条事件（Python 侧写入 API, 对应 REQ P0-c）。

        参数:
            code    错误码（建议取自 catalog; 未知码允许 —— 扩展期临时代码先跑起来）
            module  模块名（如 "ctrl" "comm" "vision"）
            message 消息文本
            level   级别; None 时用 catalog 默认级别（未知码回退 INFO）。
                    业务显式传 level 可临时升降级, 不污染错误码表。
            attrs   k=v 属性字典, 如 {"baud": 115200, "err": "timeout"}

        返回: True=写入成功; False=写入失败（已静默降级, 不抛异常）。
        """
        if level is None:
            level = fmt.LEVELS[0]  # 先给兜底值, 防下面查表失败
            try:
                from . import catalog
                level = catalog.default_level(code) or level
            except Exception:
                # 目录模块加载失败也不允许影响写入路径 —— 兜底 INFO 继续写
                pass
        with self._lock:
            self._seq += 1
            line = fmt.encode(self._seq, fmt.wall_timestamp(), fmt.mono_timestamp(),
                              level, code, module, message, attrs)
            return self._write_line(line, level)

    def _flush_fd(self):
        """把已写数据推离本进程（fd 级 flush）。

        两档语义: fsync=False 时用 fdatasync（只刷数据, 不刷元数据, 更快 ——
        日志追加场景元数据无意义）; fsync=True 时全量 fsync（强持久化）。
        fdatasync 在部分平台缺失, 缺失时回退 fsync。
        """
        if self.fsync or not hasattr(os, "fdatasync"):
            os.fsync(self._fd)
        else:
            os.fdatasync(self._fd)

    def _write_line(self, line, level):
        """单条行的落盘路径（持线程锁调用）: 一次 write 写整行 + 条件 flush + 轮转。

        多进程互斥的两个平台路径:
        - Linux: 依赖 O_APPEND 内核原子性, 无任何额外系统调用（目标平台主路径）;
        - Windows: CRT append 不原子, 写前锁住文件字节 0（固定区域, 各进程
          同一把锁）把 append 串行化, 写完解锁。锁失败时降级为裸 O_APPEND
          写（可能丢行, 但不崩溃）—— 开发机极端场景, 由计数器审计。

        关键点:
        - 一次 os.write 写整行（含换行）—— 行完整性的根基, 不得拆分;
        - os.write 返回值若小于行长度说明部分写入（异常罕见）, 保守计为失败重试一次,
          仍失败则放弃 —— 避免半行留在文件里污染读端;
        - 写后立即更新 _bytes; 轮转放在解锁之后执行（rotate 会 close/reopen fd,
          在持文件锁期间做会让解锁落在错误的新 fd 上）。
        """
        data = (line + "\n").encode("utf-8")
        locked = False
        if msvcrt is not None:
            try:
                # 锁固定区域（字节 0）: 各进程锁同一字节才互斥;
                # locking 作用于"当前位置起", 必须先 seek 到 0
                os.lseek(self._fd, 0, os.SEEK_SET)
                msvcrt.locking(self._fd, msvcrt.LK_LOCK, 1)
                locked = True
            except OSError:
                locked = False      # 锁失败: 降级裸写, 不阻塞业务
        try:
            n = os.write(self._fd, data)
            if n < len(data):
                # 部分写入: 重试补写剩余部分; 再失败只能放弃（计数） ——
                # 理论上 O_APPEND 常规 write 不会出现, 防御磁盘满等极端情况
                n2 = os.write(self._fd, data[n:])
                if n + n2 < len(data):
                    raise OSError("partial write persists")
            self._bytes += len(data)
            ok = True
        except OSError as exc:
            # 静默降级: 日志组件故障不允许打断比赛业务（CODE-STYLE §4.1）;
            # 计数器留给健康检查/自测 —— 如果连计数都无法进行, 说明内存已不可靠
            self.write_failures += 1
            self.last_error = repr(exc)
            ok = False
        finally:
            if locked:
                try:
                    # 解锁同样按"当前位置起"寻址, 必须重新 seek 到字节 0
                    os.lseek(self._fd, 0, os.SEEK_SET)
                    msvcrt.locking(self._fd, msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass            # 解锁失败: 该进程后续写入降级, 不崩溃
        # 关键事件先落盘再返回（AC6）; flush 放锁外亦可 —— 每进程 flush 自己的 fd
        if ok and level in self.flush_levels:
            try:
                self._flush_fd()
            except OSError:
                pass
        if ok:
            self._rotate_if_needed()
        return ok

    def _rotate_if_needed(self):
        """超过 max_bytes 即轮转（持锁调用）。写后检查: 宁可短暂超限, 不引入写前 stat。"""
        if self._bytes <= self.max_bytes:
            return
        os.close(self._fd)
        # 链式重命名: .(keep-1) -> .keep ... .1 -> .2; 最老的一份直接删除。
        # Windows 上 os.replace 的目标若被其他进程占用会失败 —— 板端 Linux 无此问题,
        # 失败时保守放弃本轮轮转（下条日志继续追加, 下次再试）。
        oldest = "%s.%d" % (self.path, self.keep)
        if os.path.exists(oldest):
            try:
                os.remove(oldest)
            except OSError:
                pass
        for i in range(self.keep - 1, 0, -1):
            src = "%s.%d" % (self.path, i)
            dst = "%s.%d" % (self.path, i + 1)
            if os.path.exists(src):
                try:
                    os.replace(src, dst)
                except OSError:
                    pass
        try:
            os.replace(self.path, self.path + ".1")
        except OSError:
            pass  # 多进程同时轮转可能竞争 rename —— 失败者继续用原文件, 数据不丢
        self._fd = os.open(self.path, os.O_APPEND | os.O_CREAT | os.O_WRONLY | _O_BINARY, 0o644)
        self._bytes = 0

    def flush(self):
        """手动 flush（级别不在 flush_levels 又想立即落盘时用, 如关键节点前后）。"""
        try:
            self._flush_fd()
            return True
        except OSError:
            return False

    def close(self):
        """关闭文件句柄（进程退出前调用; 重复调用安全）。"""
        with self._lock:
            if self._fd is not None and self._fd >= 0:
                try:
                    os.close(self._fd)
                except OSError:
                    pass
                self._fd = -1


# ---------------- 进程级默认写入器（跨模块共享同一个文件句柄与 seq 空间） ----------------
# 为什么需要单例: 同进程多个模块各自 new Writer 会产生两套 seq 与两个句柄,
# 无谓增加 fd 占用且 seq 无法反映进程内事件全序。默认配置集中在这里,
# 业务可用 set_default_writer 换成自定义配置（如比赛机上改目录）。
_default_writer = None
_default_lock = threading.Lock()


def get_writer(**kwargs):
    """取进程级默认 Writer; 首次调用时按 kwargs 创建, 之后忽略 kwargs 返回既有实例。

    kwargs 仅在首次创建时生效 —— 这是刻意的: 中途改配置会造成"同一文件
    两种轮转参数"的隐晦行为, 需要换配置时显式 set_default_writer。
    """
    global _default_writer
    if _default_writer is None:
        with _default_lock:
            if _default_writer is None:
                _default_writer = Writer(**kwargs)
    return _default_writer


def set_default_writer(writer):
    """替换进程级默认 Writer（测试/特殊部署用; 原实例不自动 close —— 调用方自管）。"""
    global _default_writer
    with _default_lock:
        old = _default_writer
        _default_writer = writer
    return old


def event(code, module, message, level=None, attrs=None):
    """模块级便捷 API: 直接写进程级默认 Writer（对齐 REQ P0-c 的 rmlog.event(...)）。

    C 端宏族 RMLOG_I/W/E/F 与本函数一一对应, 双端产出同构行（AC4）。
    """
    return get_writer().event(code, module, message, level=level, attrs=attrs)
