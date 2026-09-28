# -*- coding: utf-8 -*-
# （maintainer 补注：整个错误码体系的"唯一数据源"。读码前只需记住三件事：
# ① C 端 rmlog_errors.h 与 ERR-CATALOG.md 都由本表生成（python3 -m rmlog.gen_code / --doc），手改生成物 = 破坏同源；
# ② 码结构 E-<域>-<3位序号>，五域见下方 DOMAINS，每码绑定 默认级别/中文含义/建议动作 三个字段；
# ③ 码首 E 是码族标记（Event/Error code），INFO 级里程碑也以 E 开头（如 E-INIT-000"初始化完成"是正常事件不是错误）。）
"""rmlog.catalog — 错误码表单一来源（C/Python 双端同源的根）。

任务: T-20260926-001-logging-platform-p0（REQ §4 P0-a）。

关键设计:
- 本文件是错误码的**唯一**数据源。C 端头文件 `rmlog_errors.h` 由
  `python3 -m rmlog.gen_code` 从本表生成（见 gen_code.py），
  禁止在任何一端手改错误码 —— 防止双端漂移（REQ P0-a 硬约束）。
- 错误码结构 `E-<域>-<3位序号>`，域取值: INIT/COMM/HW/FSM/SYS
  （用户四类错误 + 系统资源类，REQ §4 P0-a）。
- 每码绑定: 默认级别（INFO/WARN/ERROR/FATAL）/ 中文含义 / 建议动作。
  码首的 `E` 是码族标记（Event/Error code），即使默认级别为 INFO 也以 E 开头，
  保持编号格式统一（如 E-INIT-000 表示"初始化完成"这类正常里程碑事件）。
- 本模块保持零依赖（不 import rmlog 其他模块），保证它可作为纯数据被
  gen_code 与文档生成器独立引用，避免循环依赖。

平台差异: 无 —— 纯数据模块，双端行为一致。
"""

# 错误码表版本：表结构或语义变更时递增，并同步更新 ERR-CATALOG.md
CATALOG_VERSION = "1.0"

# 五域定义（顺序即展示顺序）。value 为中文域说明，供文档与生成头文件注释复用。
DOMAINS = {
    "INIT": "初始化域：组件启动、配置加载、自检等初始化阶段事件",
    "COMM": "通信域：SPI/CAN/串口/网络等链路的传输超时、校验失败、中断",
    "HW":   "硬件域：电源电压、温度、传感器等物理量越限或异常",
    "FSM":  "状态机域：比赛/控制状态机的跃迁合法性、超时、未定义状态",
    "SYS":  "系统资源域：内存、存储、CPU 节拍、日志设施自身的资源类事件",
}

# 错误码表本体。字段:
#   code    错误码字符串（E-域-序号，序号域内从 000 起连续编号）
#   level   默认级别，取值 INFO/WARN/ERROR/FATAL（业务可临时升/降级，但不改表）
#   meaning 中文含义（一句话，写"发生了什么"）
#   action  建议动作（一句话，写"场上/场下该干什么"，面向电控队员而非系统管理员）
ERRORS = [
    # ---- INIT 初始化域 ----
    {"code": "E-INIT-000", "level": "INFO",
     "meaning": "组件初始化完成（rmlog 自身或业务组件启动就绪）",
     "action": "无需处理；用于确认上电后组件存活时序"},
    {"code": "E-INIT-001", "level": "ERROR",
     "meaning": "组件初始化失败（打开设备/加载配置/创建线程失败）",
     "action": "场下查看该行 k=v 属性中的组件名与 errno，先查设备树/路径/权限"},
    {"code": "E-INIT-002", "level": "FATAL",
     "meaning": "关键组件初始化失败，系统无法进入比赛模式（如控制主循环外设缺失）",
     "action": "立即停机排查；比赛场上禁止带病上场，先修复再上电"},
    {"code": "E-INIT-003", "level": "WARN",
     "meaning": "组件初始化降级（非关键组件失败，功能受限但可继续运行）",
     "action": "记录现象继续比赛；赛后复盘该组件，避免降级常态化"},
    {"code": "E-INIT-004", "level": "ERROR",
     "meaning": "配置参数非法或读取失败（配置文件缺失/类型不符/数值越界）",
     "action": "核对最近改动的配置项与单位（rad/deg、ms/s 常见混淆）"},

    # ---- COMM 通信域 ----
    {"code": "E-COMM-001", "level": "ERROR",
     "meaning": "SPI 传输超时（从机未在时限内应答）",
     "action": "检查从机供电/复位/接线；统计发生频率，连续出现即按链路故障处理"},
    {"code": "E-COMM-002", "level": "ERROR",
     "meaning": "SPI/CAN 传输校验失败（CRC 或帧头不符，数据不可信）",
     "action": "丢弃该帧并重传；频发时查线缆屏蔽与共地"},
    {"code": "E-COMM-003", "level": "WARN",
     "meaning": "通信链路抖动（短时丢包/重传率上升，未达到中断阈值）",
     "action": "场上无需处理，观察是否升级为 E-COMM-004；赛后查电磁环境"},
    {"code": "E-COMM-004", "level": "ERROR",
     "meaning": "通信中断（连续多次失败，链路判定丢失）",
     "action": "触发安全态（停止输出），检查两端连接器是否松脱"},
    {"code": "E-COMM-005", "level": "WARN",
     "meaning": "通信数据越界（协议字段超出物理合理范围，疑似错位或固件不匹配）",
     "action": "核对两端协议版本与字节序；单次出现可忽略，连续出现按版本不匹配排查"},

    # ---- HW 硬件域 ----
    {"code": "E-HW-001", "level": "ERROR",
     "meaning": "电源电压越限（电池电压低于比赛安全阈值）",
     "action": "立即安排换电池；同时回看 E-HW-005 出现时间，评估耗电异常"},
    {"code": "E-HW-002", "level": "ERROR",
     "meaning": "温度越限（BPU/CPU/电调温度超过阈值）",
     "action": "降负载或停机散热；检查散热接触与风道是否被遮挡"},
    {"code": "E-HW-003", "level": "WARN",
     "meaning": "传感器数据异常（IMU/编码器输出突变、冻结或 NaN）",
     "action": "标记该传感器数据不可信；检查插接件与标定"},
    {"code": "E-HW-004", "level": "FATAL",
     "meaning": "硬件自检失败（上电自检未通过，禁止进入比赛模式）",
     "action": "停机，按 k=v 属性中自检项逐项排查后再上电"},
    {"code": "E-HW-005", "level": "WARN",
     "meaning": "电压接近下限（预警带，提示电量即将不足）",
     "action": "规划换电池时机（回库/间歇），不必立即停机"},

    # ---- FSM 状态机域 ----
    {"code": "E-FSM-001", "level": "ERROR",
     "meaning": "状态机非法跃迁（当前状态收到了不允许的事件）",
     "action": "记录事件与状态组合，场上继续运行；赛后对照状态图定位逻辑漏洞"},
    {"code": "E-FSM-002", "level": "WARN",
     "meaning": "状态机事件丢失（当前状态无法处理该事件，已丢弃）",
     "action": "通常可忽略；频发说明事件产生与状态设计不匹配，赛后梳理"},
    {"code": "E-FSM-003", "level": "ERROR",
     "meaning": "状态机超时未流转（在当前状态停留超过预期时限）",
     "action": "检查该状态的等待条件（传感器/通信）是否被上游错误阻塞"},
    {"code": "E-FSM-004", "level": "FATAL",
     "meaning": "状态机进入未定义状态（查表失败，已切入安全态）",
     "action": "立即停机复位；这是严重逻辑缺陷，赛后必须复现修复"},

    # ---- SYS 系统资源域 ----
    {"code": "E-SYS-001", "level": "ERROR",
     "meaning": "内存不足（分配失败或内存水位越限）",
     "action": "记录发生时段与组件；场下配合 journalctl 查 OOM 记录（USAGE §7）"},
    {"code": "E-SYS-002", "level": "ERROR",
     "meaning": "日志落盘失败（磁盘满/IO 错误，取证能力受损）",
     "action": "检查存储剩余空间与 SD 卡健康；期间日志可能缺失，证据链降级"},
    {"code": "E-SYS-003", "level": "WARN",
     "meaning": "实时节拍超期（如 1kHz 节拍线程错过 deadline）",
     "action": "记录超期时长；频发时检查是否有高负载任务抢占（配合 dmesg）"},
    {"code": "E-SYS-004", "level": "WARN",
     "meaning": "存储水位告警（日志分区用量超阈值，即将依赖轮转清理）",
     "action": "赛后及时导出并清理旧日志；确认轮转份数设置是否够用"},
    {"code": "E-SYS-005", "level": "INFO",
     "meaning": "系统里程碑事件（启动完成/优雅停机/配置切换等）",
     "action": "无需处理；用于划定时间线（这是第几次上电、何时停机）"},
]


def get(code):
    """按码取表项；不存在返回 None。

    为什么返回副本引用即可：表项为只读约定（运行期不应修改），
    与 Python 习惯一致，不做防御性拷贝以保持零开销。
    """
    for item in ERRORS:
        if item["code"] == code:
            return dict(item)
    return None


def codes_by_domain(domain):
    """列出指定域的全部错误码（保持表内顺序）。

    domain 不合法时返回空列表而不是抛异常 —— 调用方（读端/文档）用它做
    存在性判断，空列表本身就是"该域无码"的有效回答。
    """
    prefix = "E-%s-" % domain
    return [item["code"] for item in ERRORS if item["code"].startswith(prefix)]


def default_level(code):
    """取某码的默认级别；未知码返回 None（调用方决定回退策略）。"""
    item = get(code)
    return item["level"] if item else None
