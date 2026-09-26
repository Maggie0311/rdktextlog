---
mail_id: MAIL-20260926-2222-code_reviewer--developer-RESULT-review-T-20260926-001
thread: THREAD-LOG-P0
from: code_reviewer
to: developer
cc: [management]
date: 2026-09-26 22:22
purpose: RESULT
priority: P1
requires_reply: true
attachments:
  - code_reviewer/script/REVIEW-T-20260926-001-f3331b0.md
references:
  - MAIL-20260926-2035-developer--code_reviewer-REVIEW-REQ-T-20260926-001-logging-platform-p0
  - management/script/REQ-20260926-001-logging.md §6
  - developer/script/IMPL-T-20260926-001-logging-platform-p0.md
---

## 审查结论 — T-20260926-001-logging-platform-p0 · commit `f3331b0`

**结论: CONDITIONAL**（依 ROLE-LIMIT §4 门槛：覆盖声明完整 ✓、≥1 项实际验证证据 ✓、阻断/严重级问题为 0 ✗——实有严重级 2 条，故 PASS 不成立；未达 FAIL 的判定理由见报告 §7，其中 F-1 的验收影响需 management 裁量）。

完整报告: `code_reviewer/script/REVIEW-T-20260926-001-f3331b0.md`（含全部发现项五要素/未确定项/门槛核对/复审约定）。

### 发现项摘要（9 条，完整版见报告 §5）

| # | 级别 | 位置 | 一句话现象 |
|---|---|---|---|
| F-1 | **严重** | `rmlog/writer.py:217-244`、`rmlog/rmlog.c:283-308` | 多进程并发+轮转组合下，已确认写成功的事件被静默销毁（本角色独立复现 2 次：双 worker 各 300 条+max_bytes=1200，一侧 worker 全灭；不轮转对照 600/600 完好；Linux 行为 unverified 待板端） |
| F-2 | **严重** | `rmlog_read.py:151-153` | `filter --until` 接受分钟级前缀（USAGE §5 演示用法）却漏掉该分钟全部事件——实测 `--until 2026-09-26T12:01` 只返回 12:00 的行 |
| F-3 | 一般 | `IMPL-…md` §3 | "最终自测"标注为 2020 轮，但提交内留档其后还有 2035/2042 两轮 FAIL，末轮 PASS 实为 2055 |
| F-4 | 一般 | `IMPL-…md` §3、`USAGE.md` §2 | 复现命令按序执行失败：selftest 结束清掉 `tests/_work`，随后的 gcc 链接报 "No such file or directory"（实测） |
| F-5 | 一般 | `rmlog.c:302-306`、`writer.py:243` | 轮转后重开失败路径：C 端不计数且注释与"永久放弃"的实际行为矛盾；Python 端 os.open 未包 try，违反 `event()`"不抛异常"契约 |
| F-6 | 一般 | `CODE-STYLE.md` vs `IMPL` §1 | IMPL/请求信称 CODE-STYLE v1.1，文件实为 v1.0；§5 临时文件条款与 selftest 缺省工作区（`tests/_work`）字面冲突 |
| F-7 | 一般 | `writer.py:162-163,174-182` | 锁失败降级注释称"由计数器审计"，实际锁失败不产生任何计数 |
| F-8 | 提示 | `rmlog.h:60` | "rmlog_close 之后宏调用变为无操作"与实际（emit 会重新打开继续记录）相反 |
| F-9 | 提示 | `rmlog.c:76-78` vs `:199-201` | 转义膨胀可使 ≤1024B 消息整条丢弃，IMPL"截断记录"表述对该路径不成立 |

### 对 developer 自报 4 个高风险区的回应

1. writer.py 字节锁路径——锁/解锁顺序、降级、与轮转先后**已逐行核验，锁本身实现正确**；发现相邻问题 F-7；轮转的多进程行为发现 F-1（高风险区选得准，问题恰好在其边缘）。
2. rmlog.c 部分写入补偿（4 分支算术核验正确）与 Win32/POSIX 轮转分支——补偿逻辑正确；发现重开失败路径 F-5。
3. format.py 转义与 encode_cases 一致性范围——**声明（无属性形态）与用例真实覆盖一致**，未发现问题。
4. USAGE/IMPL"未验证写成已验证"——**未发现**此类表述；相邻证据链准确性问题见 F-3/F-4/F-6。

### 实际验证动作（证据留档 `code_reviewer/script/_verify_T-20260926-001/r2/`）

- **独立复跑全量自测 10/10 PASS（退出码 0）**——在从 `developer/script/` 复制出的副本上运行，未触碰原件；
- C 示例实跑（4 行 LOGV1 输出与 IMPL §3 一致）；gcc `-Wall -Wextra` 零警告；
- 工作区与 commit `f3331b0` 一致性抽查逐字节通过；
- 专项探针系列（F-1 对照实验×4、F-2 边界、F-4 命令复现），脚本与输出全部留档。

### 需要各方动作

- **developer**：针对 F-1/F-2 提出修复方案并按新 commit 提请复审（只审增量）；F-3~F-7 随下次提交处理；对任一发现项有异议可发 ISSUE 附证据，本角色 ≤1 轮裁定。
- **management**：F-1 属"多进程×轮转"组合场景（不在 AC5 字面演示配置内），其是否影响本轮验收投入请贵方裁定（报告 §7 已注明：若判定 AC5 必须涵盖该组合，结论应升格为 FAIL）；板端自测（Q1=A）时建议增测该组合（命令同报告 U-1）。

### 声明

本角色未修改任何被审代码（全部验证在本角色自有验证区内的副本上进行）；审查结论≠验收结论，验收权归 management。

— code_reviewer (R-004)
