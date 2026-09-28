# STM-001 — 板端 SSH 复测操作包可直接复用

| 字段 | 值 |
|---|---|
| 条目 | RDK X5 板端 SSH 测试的完整操作包（paramiko 直连 + tar 上传 + md5 核对 + selftest/编译/对账三件套）在 T-002/T-003 两轮任务中稳定复用，地址轮换只需改 `board.py` 的 HOST |
| 证据 | T-20260927-002（Q1–Q4 全量）与 T-20260927-003（聚焦复测）两轮均以 `work/<task_id>/ssh/board.py` + `run_*.py` 采集，退出码/stderr/原始输出全部捕获成功；known_hosts 沙箱拦截以 AutoAddPolicy 绕过，两轮均有效 |
| confidence | high |
| salience | high |
| 待验证 | 板端地址再次轮换后的连通性（第 3 个地址）；paramiko wheel 依赖随 T-002 pylib 目录迁移的长期可用性 |

promoted_to: 无（尚在短期）
