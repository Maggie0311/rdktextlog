# REPORT-TEMPLATE — 审查报告骨架（字段冻结 v1.0）

> 复制本骨架生成 `code_reviewer/script/REVIEW-<task_id>-<commit7>.md`。**所有字段必填**，"无"也是一种填写。

```markdown
# REVIEW-<task_id>-<commit7>

| 字段 | 值 |
|---|---|
| 审查 ID | REVIEW-<task_id>-<commit7> |
| 关联 task_id | T-YYYYMMDD-NNN-<slug> |
| 审查请求来源 | developer（邮件 MAIL-...）|
| 被审 commit | <full hash>（短 hash: <7位>）|
| 审查时间 | YYYY-MM-DD HH:MM |
| 审查人 | code_reviewer (R-004) |
| 结论 | PASS / CONDITIONAL / FAIL |

## 1. 被审对象
- 文件清单（含行数）：
- 与上一轮相比的变更范围（复审时必填）：

## 2. 覆盖声明
| 文件 / 模块 | 覆盖方式 | 说明 |
|---|---|---|
| ... | 全查 / 抽样(比例,依据) / **不查(原因)** | |

- **未覆盖部分及原因**：（必填；无则写"无"）
- 本次执行的实际验证动作及证据：（编译命令 / 运行命令 / 最小复现 / 逐分支推演，**至少一项**）

## 3. 应用标准清单
- 通用清单：CHECKLIST-COMMON v1.0（GEN-01 ~ GEN-nn）
- 语言清单：CHECKLIST-C / CHECKLIST-PYTHON v1.0
- **用户自定义标准**：<列出本次实际应用的 USER-*.md 编号与标题；无则写"无">
- 项目契约：<AC 编号 / CODE-STYLE.md 条款>

## 4. 发现项
> 每条必须含**五要素**：位置 / 现象 / 复现路径或推演链 / 依据条款 / 级别 + 建议。缺一即无效。

### F-01 [级别] 一句话标题
- **位置**：<file:line>（同一根因的重复位置全部列出）
- **现象**：
- **复现路径 / 推演链**：
- **依据条款**：<GEN-xx / C-xx / PY-xx / USER-xxx / CODE-STYLE §x / AC-n>
- **级别**：BLOCKER / MAJOR / MINOR / NIT / INFO
- **建议**：（方向性描述，不提供实现代码）

## 5. 未确定项（unverified）
| 项 | 缺什么信息 | 已尝试的获取方式 |
|---|---|---|

## 6. 结论与理由
- 结论：PASS / CONDITIONAL / FAIL
- 门槛核对：覆盖声明 [完整/不完整]、验证证据 [有/无]、阻断级问题 [n 个]
- **验收权声明**：本结论不构成验收；验收由 management 裁定（架构 §4.1）。

## 7. 声明
- 本次审查**未修改任何被审代码**。
- 本报告对应的 commit hash 如发生变化，本报告即行失效。
```

## 使用规则

1. 字段不得删减；不适用的字段写"无"并说明原因。
2. 发现项编号 `F-01`、`F-02`… 在整个任务线程内**连续编号**，便于 developer 逐条回应与复审。
3. developer 的整改回应用 `R-01`、`R-02`… 对应编号；复审报告须**逐条**回应每个 `F-xx`（已修复 / 未修复 / 申诉）。
