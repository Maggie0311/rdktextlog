# T-20260930-005 第二版实现与差距说明

## 已实现（本候选版本）

- `Session` 通过 `Session.event`/`Session.wrap` 接入同步 `Writer`；`AsyncWriter(session=...)` 在入队前注入 `session` 与 `pid` 属性。`fault_demo.py` 已实际使用会话绑定路径。
- `rmlog_read.py filter --session ID` 对解析后的 `session` 属性做精确筛选；没有该属性的旧日志不会被误匹配。
- `export_evidence.py --session ID` 逐行解析业务日志后导出匹配行，manifest 报告筛选数量；journal、dmesg、uname 仍是可选证据，失败会逐项标记，不影响业务日志导出。
- `AsyncWriter` 是有界、非阻塞入队；队列满计 `dropped`，后台写失败分别计数。它不是硬实时实现。

## 事实边界与待验

本候选版本在当前开发机完成 Python 13 项旧回归、自测和 v2 smoke 的运行记录后才可声称“开发机通过”。旧板端日志、历史 Windows/Linux 记录不属于本版本证据，不能冒充新版板端事实。X5 板端 Python/systemd 安装、真实 SPI/CAN/传感器检测接入、断电持久性、硬实时延迟、异常重启链路仍待板端按 `USAGE.md` 复测。

`checks.py` 只映射业务传入的检测事实，不会探测硬件；五域 fault demo 是可运行注入演示。systemd 单元是模板，路径和权限需目标机确认。

## 验证口径

候选提交后运行：`python3 -m rmlog.selftest`（13 项）、`python3 developer/script/tests/test_v2_smoke.py`。结果、解释器、平台和 commit 必须记录在评审请求中；失败项不得用历史留档替代。
