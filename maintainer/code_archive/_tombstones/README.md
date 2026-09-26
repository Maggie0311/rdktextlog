# _tombstones/ — 未采用与被否决版本的墓碑记录

> **只追加，不删除。** 一个版本被否决，不等于它的经验没有价值。

## 什么情况写墓碑

- 某版本被 `code_reviewer` 判为不通过、且未修复即被新版本取代；
- `software_tester` 报出阻断级问题后开发者重写，旧版本未归档为正式版本；
- 人类用户或 `management` 明确否决的版本；
- 因需求变更被放弃的实现路线。

## 墓碑记录格式

```markdown
# TOMBSTONE-<task_id>-<NNN>

| 字段 | 值 |
|---|---|
| 版本 | v<NNN> |
| commit | <hash> |
| 时间 | YYYY-MM-DD |
| 否决方 | code_reviewer / software_tester / management / 人类用户 |

## 为什么未采用（事实）
（引用当时的报告或邮件，给 mail_id / 文件路径）

## 当时的判断依据
（客观记录，不加评价）

## 是否已被后续版本取代
（是 → 指向取代它的版本；否 → 说明后来怎么处理的）
```

> **注意**：墓碑记录**只记录事实与依据**，不评价代码好坏（那是 `code_reviewer` 与 `software_tester` 的职责）。
