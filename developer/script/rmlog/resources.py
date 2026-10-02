"""T-20261001-logging-v3 P1：温度、电压、内存等资源越限监控。

默认读取 Linux sysfs/procfs；所有读取器均可注入，开发机自测不依赖 RDK X5 硬件。
"""

import os
import threading


class ResourceMonitor:
    """周期采样资源并把越限事实映射到既有 24 个错误码。"""

    def __init__(self, runtime, provider=None, interval=1.0, temp_limit=85000,
                 voltage_min=14000, memory_min_kb=32768):
        self.runtime, self.provider = runtime, provider or self._linux_values
        self.interval, self.temp_limit = interval, temp_limit
        self.voltage_min, self.memory_min_kb = voltage_min, memory_min_kb
        self._stop = threading.Event()
        self._thread = None

    @staticmethod
    def _read_int(path):
        try:
            with open(path, encoding="ascii") as fh:
                return int(fh.read().strip())
        except (OSError, ValueError):
            return None

    @classmethod
    def _linux_values(cls):
        values = {}
        temp = cls._read_int("/sys/class/thermal/thermal_zone0/temp")
        if temp is not None:
            values["temp_mdeg"] = temp
        voltage = cls._read_int("/sys/class/power_supply/BAT0/voltage_now")
        if voltage is not None:
            values["voltage_mv"] = voltage // 1000
        try:
            with open("/proc/meminfo", encoding="ascii") as fh:
                for line in fh:
                    if line.startswith("MemAvailable:"):
                        values["memory_available_kb"] = int(line.split()[1])
                        break
        except (OSError, ValueError, IndexError):
            pass
        return values

    def check_once(self):
        """执行一次采样并返回读取值；不支持的资源只被跳过。"""
        values = dict(self.provider() or {})
        self.runtime.sample("resources", **values)
        if values.get("temp_mdeg", 0) > self.temp_limit:
            self.runtime.emit("E-HW-002", "resource", "temperature limit exceeded",
                              attrs={"temp_mdeg": values["temp_mdeg"]})
        if values.get("voltage_mv", self.voltage_min + 1) < self.voltage_min:
            self.runtime.emit("E-HW-001", "resource", "voltage below limit",
                              attrs={"voltage_mv": values["voltage_mv"]})
        if values.get("memory_available_kb", self.memory_min_kb + 1) < self.memory_min_kb:
            self.runtime.emit("E-SYS-001", "resource", "memory waterline exceeded",
                              attrs={"available_kb": values["memory_available_kb"]})
        return values

    def start(self):
        self._thread = threading.Thread(target=self._run, name="rmlog-resources", daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(max(0.2, self.interval * 2))

    def _run(self):
        while not self._stop.wait(self.interval):
            self.check_once()
