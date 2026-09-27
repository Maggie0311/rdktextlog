# -*- coding: utf-8 -*-
"""rmlog.writer — 事件写入端: 多进程安全追加、可控 flush、按大小轮转。

任务: T-20260926-001-logging-platform-p0（REQ §4 P0-c/P0-d）。
R1 返工: 修复审查报告 F-1/F-5/F-7 ——
  F-1 旧协议"常驻 fd + close→rename 链→reopen"跨进程零协调, 多进程×轮转组合下
      一个进程可整个搁浅在旧 inode 上, 该文件随后被当"最老副本"淘汰 ——
      其全部已确认写成功的事件静默消失（reviewer probe_1e/1g 实证）;
  F-5 旧协议轮转 reopen 失败不计数且永久停记（C 端）/ os.open 未包 try 会向业务
      抛异常（Python 端）;
  F-7 Windows 锁失败降级无任何可观测计数, 与注释"由计数器审计"不符。

---------------------------------------------------------------------------
轮转协议 v2（R1, F-1 修复核心）—— "每写即开即关 + 轮转跨进程互斥"
---------------------------------------------------------------------------
不变量（修复后承诺, selftest test_ac5_concurrent_rotation 逐 worker 对账）:
  1. 任何 event() 返回 True 的事件, 其完整行必然能在轮转链
     （rmlog.log + .1 ... .keep）的某一文件中读到;
  2. 链之外的磁盘位置永不承载本组件写入的数据（不存在被遗忘的孤儿 inode）;
  3. 每行一次 write 不拆分 —— 无半行交错（AC5 原有承诺继续成立）。

机制与推理链（每步为什么成立）:
  a. **写入 = 按路径 open(O_APPEND) → 一次 write 整行 → close**, 没有任何常驻
     fd。旧协议的全部问题都源于"fd 绑在 inode 上而 inode 的名字会被人改走";
     每写按路径重开, fd 的生命周期只有一条事件那么长, 从根上不存在"搁浅在
     旧 inode 上的 fd"。
  b. **写入目标必然是"开 fd 那一刻路径所指的文件"**。该文件此后只会沿
     path → .1 → .2 → ... → .keep 被 rename（POSIX rename 原子且内容随行）,
     链上每一环都是先被挪走（shift）、再被后来者 replace —— 即一条已落盘的行
     至少要再经历 keep 次完整轮转（每轮至少 max_bytes 新数据）才会到 .keep
     被淘汰。这正是单进程下的保留语义 —— 不是静默销毁, 是正常的容量治理。
  c. **轮转 = rename 链, 必须跨进程互斥**。两个进程同时做链操作时,
     "replace .1" 可能覆盖掉对方还没来得及 shift 的 .1 内容 —— 这是唯一能
     凭空抹掉已落盘数据的竞争。因此链操作全程持目录锁 .rmlog.ROTLOCK:
       - Linux/POSIX（X5 目标平台）: fcntl.flock(LOCK_EX)（advisory 锁,
         互斥前提 = 同目录所有写入方都经本组件 —— 比赛部署形态成立）;
         flock 随 fd 关闭自动释放, 无需显式 UNLOCK 也兜底安全;
       - Windows（开发机自测平台）: 复用跨进程写锁（msvcrt.locking 锁
         ROTLOCK 字节 0）—— 写与轮转共用同一把锁, rename 链对并发写原子。
  d. **锁内 stat 确认 + 计数校准**: 拿到轮转锁后先 stat 当前文件真实大小,
     仍 > max_bytes 才真正轮转; 否则放弃并把本地计数校准为真实大小 ——
     防止"他进程刚轮转过、我方计数陈旧"导致的过早轮转（过早轮转不丢数据,
     但会把新文件提前挤进副本链, 让保留期失真）。
  e. **写失败静默降级**: 按路径 open 失败 / write 失败都只累加计数
     （write_failures）并返回 False —— 每条事件都是一次全新的尝试, 天然满足
     F-5 的"可重试"要求, 不存在"一次失败永久停记"的状态机。

平台差异（诚实标注）:
- Linux（X5 目标环境）: 写路径零锁 —— open(2) 的 O_APPEND 是内核级原子追加,
  多进程各写完整行互不交错; 每条事件 3 次系统调用（open/write/close）, 比旧
  协议的常驻 fd 多 2 次, 1kHz 场景开销仍可忽略（µs 级）, 换来的是多进程×轮转
  的数据不灭失（F-1 修复的代价, IMPL §4 有记录）; ERROR/FATAL 在 close 前
  fdatasync（AC6）。
- Windows（本轮开发自测环境）: CRT 的 _O_APPEND 是"写前 seek 到末尾", 跨进程
  不原子 —— 每条事件在写锁内完成"open → write → close", 用锁补齐原子性;
  该代码仅 os.name == "nt" 生效。
  **Windows 自测结果不得表述为 Linux 已验证**（TASK 增补第 3 条）; Linux 侧
  行为是按上述推理链对 POSIX 语义的**推演结论**（unverified）, 板端实测由
  用户按 USAGE §3 回贴。
"""

import os
import threading

# Windows 开发机专用的字节锁（Linux 上恒为 None, 走纯 O_APPEND 路径）
if os.name == "nt":
    import msvcrt
else:
    msvcrt = None
# 轮转互斥锁（F-1 修复）: POSIX 用 fcntl.flock; Windows 无 fcntl, 复用写锁
if os.name != "nt":
    import fcntl

from . import format as fmt

# 日志文件与轮转副本的默认命名（与 USAGE.md 部署章节保持一致）
DEFAULT_FILENAME = "rmlog.log"
DEFAULT_DIR = "/userdata/rmlog"      # REQ §7 Q2 裁决: root + /userdata/rmlog
FALLBACK_DIR = "/var/log/rmlog"      # /userdata 不存在时的回退路径（Q2）

# 跨进程轮转锁文件名（F-1 修复）: 与日志同目录的隐藏文件, 两个平台都不写入
# 数据、永不进副本链。Linux 上是 flock 锁文件; Windows 上是 msvcrt.locking
# 锁体（锁其字节 0）。所有写入方经本组件 —— 锁文件名是双端（Py/C）协议约定。
_ROTLOCK_NAME = ".rmlog.ROTLOCK"

# O_BINARY 仅 Windows 需要（禁止 CRT 文本模式改写 \n）; Linux 上不存在该标志,
# 用 getattr 取 0 兜底 —— 这是"同一份代码双端可跑"的必要适配点
_O_BINARY = getattr(os, "O_BINARY", 0)


def _rotate_file(path, keep):
    """轮转链操作（无状态帮助函数, 调用方必须已持跨进程轮转锁）。

    rmlog.log -> .1 -> .2 -> ... -> .keep, 最老的一份直接删除。
    POSIX: rename 原子替换目标; Windows: os.replace 亦为原子覆盖 —— 在持有
    轮转锁的前提下, "replace 掉未 shift 的副本"这一丢数据竞争被排除。
    逐段失败保守跳过（失败段下次轮转重试）: 轮转是容量治理, 宁可超限也不冒险。
    """
    oldest = "%s.%d" % (path, keep)
    if os.path.exists(oldest):
        try:
            os.remove(oldest)
        except OSError:
            pass
    for i in range(keep - 1, 0, -1):
        src = "%s.%d" % (path, i)
        dst = "%s.%d" % (path, i + 1)
        if os.path.exists(src):
            try:
                os.replace(src, dst)
            except OSError:
                pass
    try:
        os.replace(path, path + ".1")
    except OSError:
        pass


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
        """初始化写入器。

        参数:
            log_dir      日志目录; None 时走 DEFAULT_DIR，不存在自动回退 FALLBACK_DIR
                         （目录都建不出来时抛 OSError —— 这是构造期唯一允许的失败,
                         因为此时"降级继续"只会把故障藏得更深; 写入期失败才静默降级）
            max_bytes    单文件大小上限（字节），超过即轮转; 不得小于单行长度
                         （ pathological 配置会让轮转退化为"每条一轮转", 虽不丢数据
                         但保留语义失真 —— selftest 与文档均不使用此类配置）
            keep         保留份数: rmlog.log + keep 个 .1/.2/... 副本;
                         同一目录的所有写入方应使用相同 keep（否则各方对"最老"
                         的理解不一致, 副本会按更小的 keep 提前淘汰）
            flush_levels flush 触发级别集合（默认 ERROR 及以上）
            fsync        True 时 flush 级事件额外用 fsync 替代 fdatasync（强持久化,
                         性能代价大, 默认关）
        """
        self.max_bytes = max_bytes
        self.keep = keep
        self.flush_levels = set(flush_levels)
        self.fsync = fsync
        self.log_dir = log_dir if log_dir is not None else self._resolve_dir()
        os.makedirs(self.log_dir, exist_ok=True)
        self.path = os.path.abspath(os.path.join(self.log_dir, DEFAULT_FILENAME))
        self._rotlock_path = os.path.join(self.log_dir, _ROTLOCK_NAME)
        # 线程锁: 保护 seq 自增、_bytes 与轮转决策（多线程共用实例时）。
        # 跨进程互斥不靠它 —— 见模块头"轮转协议 v2"。
        self._lock = threading.Lock()
        self._seq = 0            # 本进程事件序号（跨轮转持续递增, 不随文件重置）
        # _bytes 是"本进程视角的当前文件字节数"（轮转触发的廉价预判）:
        # 多进程同写时它必然偏小（不含他进程的字节）→ 只会造成"偏早触发",
        # 而偏早会被轮转锁内的 stat 确认挡下（见 _rotate_step）—— 失真方向安全。
        try:
            self._bytes = os.stat(self.path).st_size
        except OSError:
            self._bytes = 0
        # 健康计数器（可观测出口, selftest 与健康检查用）:
        self.write_failures = 0      # 写入/打开失败次数（静默降级, 每条事件重试）
        # 锁降级计数（F-7 修复）: 跨进程锁取锁失败而降级的次数。
        # Linux = 轮转锁失败（本轮轮转放弃, 数据不丢）; Windows = 写锁失败
        # （降级裸写, 可能丢行）。两者都曾被旧代码静默吞掉 —— 现在必须可见。
        self.lock_degradations = 0
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

    def _open_append(self):
        """按路径打开日志文件（O_APPEND|O_CREAT|O_WRONLY）, 返回 fd。

        失败时计数并返回 -1, 绝不抛异常（F-5: 打开失败按"本条事件写入失败"
        处理 —— 下一条事件是全新尝试, 无"永久停记"状态）。
        """
        try:
            return os.open(self.path,
                           os.O_APPEND | os.O_CREAT | os.O_WRONLY | _O_BINARY,
                           0o644)
        except OSError as exc:
            self.write_failures += 1
            self.last_error = repr(exc)
            return -1

    def _sync_fd(self, fd):
        """fd 级落盘: fsync=True 或平台缺 fdatasync 时用 fsync, 否则 fdatasync。

        只刷数据不刷元数据更快（日志追加场景元数据无意义）; 调用方吞 OSError
        —— flush 失败不影响"写入成功"判定（数据已进内核页缓存, flush 只是
        收紧断电窗口的手段）。
        """
        if self.fsync or not hasattr(os, "fdatasync"):
            os.fsync(fd)
        else:
            os.fdatasync(fd)

    def _write_once(self, fd, data):
        """在已打开的 fd 上一次 write 写整行; 部分写入重试补写一次。

        一次 os.write 写整行（含换行）是行完整性的根基, 不得拆分 —— 见 CODE-STYLE
        §4.2。返回 True/False; OSError 已计数转 False, 不上抛（不抛异常契约）。
        """
        try:
            n = os.write(fd, data)
            if n < len(data):
                # 部分写入: 重试补写剩余部分; 再失败只能放弃（计数）——
                # 理论上常规 write 不会出现, 防御磁盘满等极端情况
                n2 = os.write(fd, data[n:])
                if n + n2 < len(data):
                    raise OSError("partial write persists")
            return True
        except OSError as exc:
            self.write_failures += 1
            self.last_error = repr(exc)
            return False

    def event(self, code, module, message, level=None, attrs=None):
        """写入一条事件（Python 侧写入 API, 对应 REQ P0-c）。

        参数:
            code    错误码（建议取自 catalog; 未知码允许 —— 扩展期临时代码先跑起来）
            module  模块名（如 "ctrl" "comm" "vision"）
            message 消息文本
            level   级别; None 时用 catalog 默认级别（未知码回退 INFO）。
                    业务显式传 level 可临时升降级, 不污染错误码表。
            attrs   k=v 属性字典, 如 {"baud": 115200, "err": "timeout"}

        返回: True=写入成功; False=写入失败（已静默降级并计数, 不抛异常）。
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

    def _write_line(self, line, level):
        """单条行的落盘路径（持线程锁调用）: 写整行 → 条件落盘 → 轮转预判。

        平台分派:
        - Linux: 无锁 open→write→(ERROR/FATAL 同步)→close —— O_APPEND 原子性
          足以行级互斥; 轮转由 _rotate_if_needed 自取 flock（只有轮转需要
          跨进程互斥, 写不需要 —— 见模块头推理链 b/c）;
        - Windows: 整段（写+可能的轮转）在写锁内 —— CRT append 不原子,
          且 rename 链必须与并发写互斥（见 _win_write_line）。
        """
        data = (line + "\n").encode("utf-8")
        if msvcrt is None:
            # Linux: 字节累计与轮转由本层统一做（写完之后）
            ok = self._posix_write_line(data, level)
            if ok:
                self._bytes += len(data)
                self._rotate_if_needed()
            return ok
        # Windows: 写+轮转整段在 _win_write_line 的锁内完成（字节累计与轮转
        # 也必须在锁内, 否则计数与链操作会跨锁失步）—— 本层不再重复累计
        return self._win_write_line(data, level)

    def _posix_write_line(self, data, level):
        """Linux 主路径: open → 一次 write → (ERROR/FATAL) 同步 → close。

        全程不持跨进程锁。为什么这样是安全的（推理链见模块头）:
        - 行原子性由 O_APPEND 一次 write 保证（多进程互不交错）;
        - 本 fd 生命周期只有这一条事件, 不存在被轮转"改名甩下"的常驻 fd;
        - 写入目标 = open 那一刻 path 所指的文件, 它此后只沿副本链 rename,
          至少经历 keep 次完整轮转后才会被淘汰 —— 保留语义与单进程一致。
        fdatasync 在 close 之前做: 即使此刻他进程把文件 rename 进副本链,
        fd 仍指向同一 inode, 刷的就是本进程刚写的数据（AC6）。
        """
        fd = self._open_append()
        if fd < 0:
            return False
        try:
            ok = self._write_once(fd, data)
            if ok and level in self.flush_levels:
                try:
                    self._sync_fd(fd)
                except OSError:
                    pass            # flush 失败不影响成功判定（数据已在页缓存）
            return ok
        finally:
            try:
                os.close(fd)
            except OSError:
                pass

    def _win_write_line(self, data, level):
        """Windows 自测路径: 写锁内 open → write → (同步) → close → (轮转)。

        为什么写也要锁（与 Linux 不同）: CRT 的 append 是"写前 seek", 跨进程
        两个 seek+write 会互相覆盖; 锁住 ROTLOCK 字节 0 把各进程的整段写入
        串行化。轮转在同一把锁内做（写与轮转互斥, rename 链对并发写原子）。
        取锁失败降级裸写（可能丢行但不阻塞业务）—— F-7: 计入 lock_degradations。
        """
        lock_fd = -1
        locked = False
        try:
            lock_fd = os.open(self._rotlock_path,
                              os.O_CREAT | os.O_RDWR | _O_BINARY, 0o666)
        except OSError as exc:
            self.write_failures += 1
            self.last_error = repr(exc)
        if lock_fd >= 0:
            try:
                os.lseek(lock_fd, 0, os.SEEK_SET)
                msvcrt.locking(lock_fd, msvcrt.LK_LOCK, 1)
                locked = True
            except OSError:
                # 锁失败: 降级裸写。降级必须可观测（F-7）—— 该状态下跨进程
                # 互斥丧失, Windows 并发下可能丢行, selftest/健康检查审计此计数
                locked = False
                self.lock_degradations += 1
        try:
            ok = self._write_once_under_win(data, level)
            if ok:
                self._bytes += len(data)
                # 轮转仍在写锁内做 —— rename 链与所有持锁写互斥（推理链 c）;
                # 降级路径（未持锁）不轮转: 没有锁保护的链操作正是丢数据竞争,
                # 宁可推迟到下次拿锁成功的写入（数据不丢, 只是晚轮转）
                if locked and self._bytes > self.max_bytes:
                    self._rotate_step()
            return ok
        finally:
            if lock_fd >= 0:
                if locked:
                    try:
                        os.lseek(lock_fd, 0, os.SEEK_SET)
                        msvcrt.locking(lock_fd, msvcrt.LK_UNLCK, 1)
                    except OSError:
                        # 解锁失败: 互斥状态已不可信, 与取锁失败同级可观测（F-7）
                        self.lock_degradations += 1
                try:
                    os.close(lock_fd)
                except OSError:
                    pass

    def _write_once_under_win(self, data, level):
        """锁内的实际写入: open → write → (ERROR/FATAL 同步) → close。

        与 Linux 路径共用 _write_once 的行完整性逻辑; 差异只在"外面套着锁"。
        """
        fd = self._open_append()
        if fd < 0:
            return False
        try:
            ok = self._write_once(fd, data)
            if ok and level in self.flush_levels:
                try:
                    self._sync_fd(fd)
                except OSError:
                    pass
            return ok
        finally:
            try:
                os.close(fd)
            except OSError:
                pass

    def _rotate_if_needed(self):
        """Linux 轮转入口（持线程锁调用; 写入成功后执行）。写后检查: 宁可短暂
        超限, 不引入写前 stat。

        轮转是唯一需要跨进程互斥的操作, 写路径不锁（推理链 c）—— 链操作全程
        持 flock; 拿锁失败放弃本轮（计数 lock_degradations）, 数据不丢,
        下条事件写入后再次触发。
        （Windows 的轮转不经过本方法 —— 在 _win_write_line 的写锁内直接调
        _rotate_step, 因为那条路径的写锁就是轮转锁。）
        """
        if self._bytes <= self.max_bytes:
            return
        # ---- Linux: 为"链操作"这一小段取跨进程轮转锁 ----
        try:
            lock_fd = os.open(self._rotlock_path, os.O_CREAT | os.O_RDWR, 0o666)
        except OSError as exc:
            # 锁文件都开不出来（fd 耗尽/目录被移除）: 放弃本轮轮转, 可观测
            self.lock_degradations += 1
            self.last_error = repr(exc)
            return
        try:
            # 阻塞式 LOCK_EX: 轮转本身毫秒级, 竞争方只是顺序排队, 不丢事件;
            # flock 随下面 close 自动释放（异常路径也兜底安全）
            fcntl.flock(lock_fd, fcntl.LOCK_EX)
            self._rotate_step()
        except OSError as exc:
            # flock 失败（文件系统不支持等罕见情形）: 同样保守放弃, 可观测
            self.lock_degradations += 1
            self.last_error = repr(exc)
        finally:
            try:
                os.close(lock_fd)
            except OSError:
                pass

    def _rotate_step(self):
        """锁内的一步轮转: stat 确认 → 链操作 → 计数校准。

        调用方必须已持跨进程轮转锁（Linux=本类 _rotate_if_needed 的 flock;
        Windows=_win_write_line 的写锁）—— "replace 掉未 shift 副本"的丢数据
        竞争正是靠这把锁排除的。

        stat 确认（推理链 d）: 只有当前文件真实大小仍 > max_bytes 才轮转 ——
        本进程的 _bytes 是"只计自己"的陈旧近似, 他进程可能刚轮转并重开了
        小文件; 此时放弃并把 _bytes 校准为真实大小, 避免把新文件过早挤进
        副本链（过早轮转不丢数据, 但让 keep 的保留期失真）。
        """
        try:
            st_size = os.stat(self.path).st_size
        except OSError:
            # 当前文件不存在 = 刚被他进程轮转走（新文件要等下一次写入创建）:
            # 无可轮转之物, 计数归零即可 —— 不是错误, 不计数
            self._bytes = 0
            return
        if st_size > self.max_bytes:
            _rotate_file(self.path, self.keep)
            self._bytes = 0        # 轮转后 path 不存在, 下次写入由 open 重建
        else:
            self._bytes = st_size  # 校准: 消除"只计自己"的陈旧偏大

    def flush(self):
        """手动 flush 当前日志文件（级别不在 flush_levels 又想立即落盘时用）。

        临时开 fd 对当前文件做一次同步; 只覆盖 rmlog.log 本体 —— 副本链中的
        数据依赖 OS 周期回写（与旧协议一致, IMPL §4 已记录该边界）。
        """
        fd = self._open_append()
        if fd < 0:
            return False
        try:
            try:
                self._sync_fd(fd)
            except OSError:
                return False
            return True
        finally:
            try:
                os.close(fd)
            except OSError:
                pass

    def close(self):
        """兼容接口（进程退出前调用; 重复调用安全）。

        协议 v2 没有常驻 fd（每写即开即关）, 无句柄可关 —— 保留方法是为了
        不破坏 R0 的调用方代码与文档示例。ERROR/FATAL 已逐条落盘, INFO/WARN
        依赖页缓存回写（与 IMPL §4 声明的损失边界一致）。
        """
        return None


# ---------------- 进程级默认写入器（跨模块共享同一个 seq 空间与配置） ----------------
# 为什么需要单例: 同进程多个模块各自 new Writer 会产生两套 seq,
# seq 无法反映进程内事件全序。默认配置集中在这里,
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
