# C 端探针汇总（r3, 2026-09-27, code_reviewer 独立执行）

## probe_c_r3（无显式 open, 仅宏 + close 幂等 + F-8 行为初探）
- gcc -std=c99 -Wall -Wextra: 0 告警（rmlog.c 部分）; 探针自身 1 处告警（rmlog_flush 未在 rmlog.h 声明 —— 与 IMPL "P0 预留"声明一致）
- 运行退出码 0; rmlog_path() 在 close 后返回 NULL ✓
- 本机默认目录裁决两级均不可建（会话沙箱拒 D:\ 根写入）→ 事件按 F-5 语义静默计数丢弃（无日志文件产生）—— 该形态下"失败不崩溃"成立

## probe_c2_r3（显式 rmlog_open("probe_c_dir") + close 后续记 + 3200 长事件）
- 落盘: probe_c_dir/rmlog.log = 3211 行; 按码对账: E-SYS-005=3200(0..3199 无缺号), E-FSM-004=8(seq 4,6,507,1008,1509,2010,2511,3012), E-INIT-000=1, E-HW-005=1, E-COMM-001=1
- **缺失: seq 5（close 后那条 RMLOG_I "after close emit continues"）** ——
  emit 重开路径 rmlog__open_locked() 重新做缺省目录裁决（/userdata → /var/log）,
  本机两级均不可建 → open 失败 → 计数丢弃。**F-8 新注释"close 后 emit 按需重开继续记录"
  对显式目录调用方不成立**（缺省目录可用时则会静默落到缺省目录而非显式目录）。
  → 复审发现 RF-1（一般/MINOR）的实证
- 轮转分支: 该轮探针消息填充 bug 未触发轮转（探针自身问题, 与被审代码无关）

## probe_c3_r3（修正填充: 4000 长事件 ≈2.76MB + 每 500 条 FATAL, 共 4008 条）
- gcc 零告警; 运行退出码 0
- 对账: 4008/4008 行全部落盘, seq 1..4008 连续无缺号, 8 条 FATAL（AC6 fdatasync/_commit 组合）全部在场
- **Windows C 端轮转未触发**（rmlog.log 单文件 2.82MB > max 2MB）: rmlog__rotate_chain_locked 的
  rename(g_path, .1) 因本进程 fd 打开该文件而失败（MinGW rename 对打开中文件 EACCES）,
  保守跳过、数据零丢失 —— 与 IMPL §4.1 "C 端 Windows 是开发机编译自测平台, 不是部署目标;
  跨进程组合演示由 Python 端覆盖"的声明一致; C 端 flock 轮转路径的实测属 U-1（板端）

## 结论
- C 端主路径（写入/计数/幂等 close/AC6 同步/数据保全）与声明一致;
- RF-1 实证成立; C 端 Linux flock 轮转 + 多进程行为保持 unverified（U-1）。
