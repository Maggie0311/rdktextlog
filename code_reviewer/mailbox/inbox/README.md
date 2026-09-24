# inbox/ — 来信（开工必读）

规则：
1. 每次开工前**必须**先读完 inbox 中的未处理信件，再动任何文件。
2. 处理完的信移入 `../archive/YYYY-MM/`。
3. **例外**：带 `keep_in_inbox: true` 的常驻文件（任命信）不归档（协议 v1.1 §2.1）。
4. inbox 中不得滞留除常驻文件外的任何信件。

当前常驻：
- `WELCOME-code_reviewer.md` — R-004 任命信（授权依据、使命来源与首个任务）

本角色预期的高频来信类型：
- `TASK`（来自 developer / management）— **审查请求**，必须含 `task_id`、**commit hash**、AC、`IMPL` 与 `CODE-STYLE` 路径；
- `ISSUE`（来自 developer）— **申诉**，须附证据；本角色 ≤1 轮内以证据裁定；
- `QUERY`（来自 management）— 澄清；≤2 轮内回；
- `DECISION`（来自 framework_admin）— 仲裁结论，必须执行。
