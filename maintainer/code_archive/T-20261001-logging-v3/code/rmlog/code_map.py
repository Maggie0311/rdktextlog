# （maintainer 补注，T-20261001-logging-v3 归档 001，来源 commit d77d36c）
# 导读：code_map.py = P2「字符串码 + 24bit bit 码双轨」映射层。字符串码仍是文本日志与旧 API
# 的可读接口；bit 码是跨进程/跨 MCU 传输的稳定整数表示。布局 domain(8)|level(4)|number(12)，
# 高 8 位保留为 0，可安全放进 STM32 uint32_t。encode/decode/hex_code 三个入口，非法输入返回 None。
"""T-20261001-logging-v3：字符串错误码与紧凑 bit 错误码的双轨映射。

字符串码继续作为文本日志和旧 API 的可读接口；bit 码只作为跨进程、跨 MCU
传输时的稳定整数表示。24 位布局为 ``domain(8) | level(4) | number(12)``，
高位不足的 8 位保留为零，故可安全放进 STM32 的 uint32_t。
"""

from . import catalog

DOMAIN_IDS = {"INIT": 0x21, "COMM": 0x22, "HW": 0x23, "FSM": 0x24, "SYS": 0x25}
LEVEL_IDS = {"INFO": 1, "WARN": 2, "ERROR": 3, "FATAL": 4}


def encode(code):
    """把 ``E-DOMAIN-NNN`` 映射为 24 位整数；非法输入返回 ``None``。"""
    item = catalog.get(code)
    if item is None:
        return None
    try:
        _, domain, number = code.split("-")
        return (DOMAIN_IDS[domain] << 16) | (LEVEL_IDS[item["level"]] << 12) | int(number)
    except (KeyError, ValueError):
        return None


def decode(value):
    """把 bit 码还原为已登记的字符串码；未知值返回 ``None``。"""
    if not isinstance(value, int) or value < 0 or value > 0xFFFFFF:
        return None
    domain_id, level_id, number = (value >> 16) & 0xFF, (value >> 12) & 0xF, value & 0xFFF
    for item in catalog.ERRORS:
        if encode(item["code"]) == value:
            return item["code"]
    return None


def hex_code(code):
    """返回固定 6 位十六进制形式（例如 ``0x211003``）。"""
    value = encode(code)
    return None if value is None else "0x%06X" % value
