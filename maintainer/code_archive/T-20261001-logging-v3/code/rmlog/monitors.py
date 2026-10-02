# （maintainer 补注，T-20261001-logging-v3 归档 001，来源 commit d77d36c）
# 导读：monitors.py = P1 三条自动捕获线的宿主类：
#   CommStats          通信错误率滑动窗口统计（E-COMM-004=连续中断 / E-COMM-003=分散失败或突发）
#   HeartbeatWatchdog  主循环喂狗超时→E-FSM-003（systemd WatchdogSec 由服务文件兜底重启）
#   DmesgMonitor       真实 dmesg --follow 监听内核日志，可疑行转 E-COMM-002/E-HW-003；source 可注入
"""T-20261001-logging-v3 P1：可注入数据源的自动捕获监控器。"""

import re
import subprocess
import threading
import time
from collections import deque


class CommStats:
    """通信成功/失败统计器，超过窗口阈值自动发出 COMM 码。"""

    def __init__(self, runtime, name, window=20, fail_threshold=3,
                 rate_window=20, error_rate_threshold=0.5):
        self.runtime, self.name = runtime, name
        self.window, self.fail_threshold = window, fail_threshold
        self.rate_window, self.error_rate_threshold = rate_window, error_rate_threshold
        if window <= 0 or fail_threshold <= 0 or rate_window <= 0:
            raise ValueError("communication thresholds must be positive")
        self.total = self.failed = self.consecutive_failures = 0
        self._outcomes = deque(maxlen=rate_window)

    def success(self):
        self.total += 1
        self.consecutive_failures = 0
        self._outcomes.append(0)
        self.runtime.sample("comm", name=self.name, ok=1, total=self.total,
                            failed=self.failed, consecutive=0)

    def failure(self, detail="transport failure"):
        self.total += 1
        self.failed += 1
        self.consecutive_failures += 1
        self._outcomes.append(1)
        self.runtime.sample("comm", name=self.name, ok=0, total=self.total,
                            failed=self.failed, consecutive=self.consecutive_failures)
        rate = float(sum(self._outcomes)) / len(self._outcomes)
        interrupted = self.consecutive_failures >= self.window
        rate_warning = (len(self._outcomes) >= self.rate_window and
                        rate >= self.error_rate_threshold)
        burst_warning = self.consecutive_failures >= self.fail_threshold
        if interrupted or rate_warning or burst_warning:
            # E-COMM-004 只表示连续 window 次失败的明确链路中断；分散失败
            # 和短时突发一律保留为抖动告警，便于场下区分链路断开与噪声。
            code = "E-COMM-004" if interrupted else "E-COMM-003"
            return self.runtime.emit(code, self.name, detail,
                                     attrs={"failed": self.failed, "total": self.total,
                                            "consecutive": self.consecutive_failures,
                                            "error_rate": "%.3f" % rate})
        return True


class HeartbeatWatchdog:
    """监视主循环喂狗；超时产生 FSM-003，systemd 由服务文件负责兜底重启。"""

    def __init__(self, runtime, name="main", timeout=1.0, interval=0.1):
        self.runtime, self.name, self.timeout, self.interval = runtime, name, timeout, interval
        self._stop = threading.Event()
        self._thread = None
        self.runtime.ensure_heartbeat(name)

    def start(self):
        self._thread = threading.Thread(target=self._run, name="rmlog-watchdog", daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(max(self.interval * 2, 0.2))

    def _run(self):
        reported = False
        while not self._stop.wait(self.interval):
            age = self.runtime.health_attrs().get("heartbeat_%s" % self.name)
            if age is not None and age > int(self.timeout * 1000) and not reported:
                self.runtime.emit("E-FSM-003", self.name, "heartbeat timeout",
                                  attrs={"age_ms": age})
                reported = True
            elif age is not None and age <= int(self.timeout * 1000):
                reported = False


class DmesgMonitor:
    """将可疑内核行转为业务码；source 可注入迭代器，测试不依赖 dmesg。"""

    PATTERN = re.compile(r"(spi|can|i2c|overheat|thermal|voltage|error|fail)", re.I)

    def __init__(self, runtime, source=None):
        self.runtime, self.source = runtime, source
        self._stop = threading.Event()
        self._proc = None
        self._proc_lock = threading.Lock()

    @staticmethod
    def _terminate_process(proc):
        """终止并等待 dmesg 子进程，重复调用安全。"""
        try:
            proc.terminate()
            proc.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
                proc.wait()
            except OSError:
                pass
        except (OSError, ValueError):
            pass

    def run(self):
        """阻塞监听直到 source 耗尽或 stop；真实板端使用 dmesg --follow。"""
        source = self.source
        proc = None
        if source is None:
            proc = subprocess.Popen(["dmesg", "--follow", "--time-format", "iso"],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, errors="replace")
            # （maintainer 补注：启动竞态闭合——锁内登记 _proc 并读取 stop 标志；若启动期间已被 stop，则立即终止子进程返回，无泄漏。）
            with self._proc_lock:
                self._proc = proc
                stop_during_start = self._stop.is_set()
            if stop_during_start:
                self._terminate_process(proc)
                return
            source = proc.stdout
        try:
            for line in source:
                if self._stop.is_set():
                    break
                line = line.rstrip()
                if self.PATTERN.search(line):
                    code = "E-COMM-002" if re.search(r"spi|can|i2c", line, re.I) else "E-HW-003"
                    self.runtime.emit(code, "kernel", line[:240])
        finally:
            if proc:
                self._terminate_process(proc)
                with self._proc_lock:
                    if self._proc is proc:
                        self._proc = None

    def stop(self):
        self._stop.set()
        with self._proc_lock:
            proc = self._proc
        if proc is not None:
            self._terminate_process(proc)
