# QUESTIONS-001 — T-20260930-005-logging-v2

1. 队列容量为何必须是正整数？（`rmlog/async_writer.py`；tester 的 boundary 结果）
2. `accepted` 与 `dropped` 的计数分别在哪个生命周期更新？（`async_writer.py`）
3. `flush` 如何知道后台任务已完成？（`async_writer.py` 的 `unfinished_tasks`）
4. session 如何从启动/停止事件贯穿到导出筛选？（`session.py`、`daemon.py`、`export_evidence.py`）
5. 为什么导出必须枚举主文件和 `.1...` 副本？（`export_evidence.py`）
6. manifest 如何区分 MISSING、OK 与 UNAVAILABLE？（`export_evidence.py`）
7. 五域注入证明了什么，又没有证明什么？（`checks.py`、`fault_demo.py`；真实硬件仍 unverified）
8. daemon 收到 TERM 时，怎样保证停止事件与 flush 顺序？（`daemon.py`）
9. systemd 模板的 Restart 语义是否已在 X5 实机验证？（`systemd/rmlog-demo.service`；答案：unverified）
10. Python v2 与 C 端 LOGV1 的边界是什么？（`format.py`、`rmlog.c`、`rmlog.h`）
11. 轮转锁与队列容量分别保护哪个不变量？（`writer.py`、`async_writer.py`）
12. `13/13 PASS` 是否等于 X5、断电、硬实时均已通过？（tester/ACCEPT；答案：不是）
