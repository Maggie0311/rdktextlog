/*
 * （maintainer 补注，T-20261001-logging-v3 归档 001，来源 commit d77d36c）
 * 导读：本文件是生成物（勿手改），由 `python3 -m rmlog.gen_code` 从 catalog.py 单一来源渲染，
 * 供 Linux 与 STM32/RT-Thread 下位机共用同一份错误码表（P2 共用统一头文件）。
 * 与 rmlog/rmlog_errors.h 同源，仅 banner 头名与 include guard 宏不同。
 */
/*
 * rmlog_schema.h — 错误码表（C 端）。由 python3 -m rmlog.gen_code 自动生成。
 *
 * 错误码单一来源: rmlog/catalog.py（Python 包内嵌表, 含级别/含义/建议动作）。
 * !! 本文件是生成物, 禁止手改 !!  改错误码请改 catalog.py 后重新生成:
 *     python3 -m rmlog.gen_code
 * 任何对表内容的双端不一致都属缺陷（REQ P0-a: C/Python 双端同源）。
 *
 * 任务: T-20260926-001-logging-platform-p0
 */
#ifndef RMLOG_SCHEMA_H
#define RMLOG_SCHEMA_H

#ifdef __cplusplus
extern "C" {
#endif

/* 表版本: rmlog.catalog.CATALOG_VERSION = 1.0 */
/* bit 码布局: domain(8) | level(4) | number(12), 24-bit uint32_t */

/* ---- 级别常量（顺序与 Python 端 format.LEVELS 一致） ---- */
#define RMLOG_LVL_INFO 1
#define RMLOG_LVL_WARN 2
#define RMLOG_LVL_ERROR 3
#define RMLOG_LVL_FATAL 4

/* ---- 每码常量: RMLOG_CODE_<域>_<序号> 与 RMLOG_LVL_<域>_<序号> ---- */
#define RMLOG_CODE_INIT_000 "E-INIT-000"
#define RMLOG_LVL_INIT_000 RMLOG_LVL_INFO
#define RMLOG_BIT_INIT_000 0x211000u
#define RMLOG_CODE_INIT_001 "E-INIT-001"
#define RMLOG_LVL_INIT_001 RMLOG_LVL_ERROR
#define RMLOG_BIT_INIT_001 0x213001u
#define RMLOG_CODE_INIT_002 "E-INIT-002"
#define RMLOG_LVL_INIT_002 RMLOG_LVL_FATAL
#define RMLOG_BIT_INIT_002 0x214002u
#define RMLOG_CODE_INIT_003 "E-INIT-003"
#define RMLOG_LVL_INIT_003 RMLOG_LVL_WARN
#define RMLOG_BIT_INIT_003 0x212003u
#define RMLOG_CODE_INIT_004 "E-INIT-004"
#define RMLOG_LVL_INIT_004 RMLOG_LVL_ERROR
#define RMLOG_BIT_INIT_004 0x213004u
#define RMLOG_CODE_COMM_001 "E-COMM-001"
#define RMLOG_LVL_COMM_001 RMLOG_LVL_ERROR
#define RMLOG_BIT_COMM_001 0x223001u
#define RMLOG_CODE_COMM_002 "E-COMM-002"
#define RMLOG_LVL_COMM_002 RMLOG_LVL_ERROR
#define RMLOG_BIT_COMM_002 0x223002u
#define RMLOG_CODE_COMM_003 "E-COMM-003"
#define RMLOG_LVL_COMM_003 RMLOG_LVL_WARN
#define RMLOG_BIT_COMM_003 0x222003u
#define RMLOG_CODE_COMM_004 "E-COMM-004"
#define RMLOG_LVL_COMM_004 RMLOG_LVL_ERROR
#define RMLOG_BIT_COMM_004 0x223004u
#define RMLOG_CODE_COMM_005 "E-COMM-005"
#define RMLOG_LVL_COMM_005 RMLOG_LVL_WARN
#define RMLOG_BIT_COMM_005 0x222005u
#define RMLOG_CODE_HW_001 "E-HW-001"
#define RMLOG_LVL_HW_001 RMLOG_LVL_ERROR
#define RMLOG_BIT_HW_001 0x233001u
#define RMLOG_CODE_HW_002 "E-HW-002"
#define RMLOG_LVL_HW_002 RMLOG_LVL_ERROR
#define RMLOG_BIT_HW_002 0x233002u
#define RMLOG_CODE_HW_003 "E-HW-003"
#define RMLOG_LVL_HW_003 RMLOG_LVL_WARN
#define RMLOG_BIT_HW_003 0x232003u
#define RMLOG_CODE_HW_004 "E-HW-004"
#define RMLOG_LVL_HW_004 RMLOG_LVL_FATAL
#define RMLOG_BIT_HW_004 0x234004u
#define RMLOG_CODE_HW_005 "E-HW-005"
#define RMLOG_LVL_HW_005 RMLOG_LVL_WARN
#define RMLOG_BIT_HW_005 0x232005u
#define RMLOG_CODE_FSM_001 "E-FSM-001"
#define RMLOG_LVL_FSM_001 RMLOG_LVL_ERROR
#define RMLOG_BIT_FSM_001 0x243001u
#define RMLOG_CODE_FSM_002 "E-FSM-002"
#define RMLOG_LVL_FSM_002 RMLOG_LVL_WARN
#define RMLOG_BIT_FSM_002 0x242002u
#define RMLOG_CODE_FSM_003 "E-FSM-003"
#define RMLOG_LVL_FSM_003 RMLOG_LVL_ERROR
#define RMLOG_BIT_FSM_003 0x243003u
#define RMLOG_CODE_FSM_004 "E-FSM-004"
#define RMLOG_LVL_FSM_004 RMLOG_LVL_FATAL
#define RMLOG_BIT_FSM_004 0x244004u
#define RMLOG_CODE_SYS_001 "E-SYS-001"
#define RMLOG_LVL_SYS_001 RMLOG_LVL_ERROR
#define RMLOG_BIT_SYS_001 0x253001u
#define RMLOG_CODE_SYS_002 "E-SYS-002"
#define RMLOG_LVL_SYS_002 RMLOG_LVL_ERROR
#define RMLOG_BIT_SYS_002 0x253002u
#define RMLOG_CODE_SYS_003 "E-SYS-003"
#define RMLOG_LVL_SYS_003 RMLOG_LVL_WARN
#define RMLOG_BIT_SYS_003 0x252003u
#define RMLOG_CODE_SYS_004 "E-SYS-004"
#define RMLOG_LVL_SYS_004 RMLOG_LVL_WARN
#define RMLOG_BIT_SYS_004 0x252004u
#define RMLOG_CODE_SYS_005 "E-SYS-005"
#define RMLOG_LVL_SYS_005 RMLOG_LVL_INFO
#define RMLOG_BIT_SYS_005 0x251005u

/* ---- 错误码表（与 catalog.py ERRORS 一一对应, 顺序一致） ---- */
typedef struct {
    const char *code;      /* 错误码字符串, 如 "E-INIT-001" */
    int         level;     /* 默认级别（RMLOG_LVL_INFO..FATAL） */
    const char *meaning;   /* 中文含义 */
    const char *action;    /* 建议动作 */
} rmlog_err_entry_t;

static const rmlog_err_entry_t rmlog_error_table[] = {
    { "E-INIT-000", RMLOG_LVL_INIT_000, "组件初始化完成（rmlog 自身或业务组件启动就绪）", "无需处理；用于确认上电后组件存活时序" },
    { "E-INIT-001", RMLOG_LVL_INIT_001, "组件初始化失败（打开设备/加载配置/创建线程失败）", "场下查看该行 k=v 属性中的组件名与 errno，先查设备树/路径/权限" },
    { "E-INIT-002", RMLOG_LVL_INIT_002, "关键组件初始化失败，系统无法进入比赛模式（如控制主循环外设缺失）", "立即停机排查；比赛场上禁止带病上场，先修复再上电" },
    { "E-INIT-003", RMLOG_LVL_INIT_003, "组件初始化降级（非关键组件失败，功能受限但可继续运行）", "记录现象继续比赛；赛后复盘该组件，避免降级常态化" },
    { "E-INIT-004", RMLOG_LVL_INIT_004, "配置参数非法或读取失败（配置文件缺失/类型不符/数值越界）", "核对最近改动的配置项与单位（rad/deg、ms/s 常见混淆）" },
    { "E-COMM-001", RMLOG_LVL_COMM_001, "SPI 传输超时（从机未在时限内应答）", "检查从机供电/复位/接线；统计发生频率，连续出现即按链路故障处理" },
    { "E-COMM-002", RMLOG_LVL_COMM_002, "SPI/CAN 传输校验失败（CRC 或帧头不符，数据不可信）", "丢弃该帧并重传；频发时查线缆屏蔽与共地" },
    { "E-COMM-003", RMLOG_LVL_COMM_003, "通信链路抖动（短时丢包/重传率上升，未达到中断阈值）", "场上无需处理，观察是否升级为 E-COMM-004；赛后查电磁环境" },
    { "E-COMM-004", RMLOG_LVL_COMM_004, "通信中断（连续多次失败，链路判定丢失）", "触发安全态（停止输出），检查两端连接器是否松脱" },
    { "E-COMM-005", RMLOG_LVL_COMM_005, "通信数据越界（协议字段超出物理合理范围，疑似错位或固件不匹配）", "核对两端协议版本与字节序；单次出现可忽略，连续出现按版本不匹配排查" },
    { "E-HW-001", RMLOG_LVL_HW_001, "电源电压越限（电池电压低于比赛安全阈值）", "立即安排换电池；同时回看 E-HW-005 出现时间，评估耗电异常" },
    { "E-HW-002", RMLOG_LVL_HW_002, "温度越限（BPU/CPU/电调温度超过阈值）", "降负载或停机散热；检查散热接触与风道是否被遮挡" },
    { "E-HW-003", RMLOG_LVL_HW_003, "传感器数据异常（IMU/编码器输出突变、冻结或 NaN）", "标记该传感器数据不可信；检查插接件与标定" },
    { "E-HW-004", RMLOG_LVL_HW_004, "硬件自检失败（上电自检未通过，禁止进入比赛模式）", "停机，按 k=v 属性中自检项逐项排查后再上电" },
    { "E-HW-005", RMLOG_LVL_HW_005, "电压接近下限（预警带，提示电量即将不足）", "规划换电池时机（回库/间歇），不必立即停机" },
    { "E-FSM-001", RMLOG_LVL_FSM_001, "状态机非法跃迁（当前状态收到了不允许的事件）", "记录事件与状态组合，场上继续运行；赛后对照状态图定位逻辑漏洞" },
    { "E-FSM-002", RMLOG_LVL_FSM_002, "状态机事件丢失（当前状态无法处理该事件，已丢弃）", "通常可忽略；频发说明事件产生与状态设计不匹配，赛后梳理" },
    { "E-FSM-003", RMLOG_LVL_FSM_003, "状态机超时未流转（在当前状态停留超过预期时限）", "检查该状态的等待条件（传感器/通信）是否被上游错误阻塞" },
    { "E-FSM-004", RMLOG_LVL_FSM_004, "状态机进入未定义状态（查表失败，已切入安全态）", "立即停机复位；这是严重逻辑缺陷，赛后必须复现修复" },
    { "E-SYS-001", RMLOG_LVL_SYS_001, "内存不足（分配失败或内存水位越限）", "记录发生时段与组件；场下配合 journalctl 查 OOM 记录（USAGE §7）" },
    { "E-SYS-002", RMLOG_LVL_SYS_002, "日志落盘失败（磁盘满/IO 错误，取证能力受损）", "检查存储剩余空间与 SD 卡健康；期间日志可能缺失，证据链降级" },
    { "E-SYS-003", RMLOG_LVL_SYS_003, "实时节拍超期（如 1kHz 节拍线程错过 deadline）", "记录超期时长；频发时检查是否有高负载任务抢占（配合 dmesg）" },
    { "E-SYS-004", RMLOG_LVL_SYS_004, "存储水位告警（日志分区用量超阈值，即将依赖轮转清理）", "赛后及时导出并清理旧日志；确认轮转份数设置是否够用" },
    { "E-SYS-005", RMLOG_LVL_SYS_005, "系统里程碑事件（启动完成/优雅停机/配置切换等）", "无需处理；用于划定时间线（这是第几次上电、何时停机）" },
};

/* 表长: 与 catalog.ERRORS 条数一致, 供遍历与双端一致性自测 */
#define RMLOG_ERROR_TABLE_LEN 24

/* 五域白名单（顺序与 catalog.DOMAINS 一致） */
static const char *const rmlog_domains[] = {
    "INIT",
    "COMM",
    "HW",
    "FSM",
    "SYS",
};
#define RMLOG_DOMAIN_COUNT 5

#ifdef __cplusplus
}
#endif

#endif /* RMLOG_SCHEMA_H */
