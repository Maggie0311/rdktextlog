# -*- coding: utf-8 -*-
"""rmlog.gen_code — 错误码表 C 头文件生成器（单一来源 -> C 端，杜绝双端漂移）。

任务: T-20260926-001-logging-platform-p0（REQ §4 P0-a 同源机制）。

用法: python3 -m rmlog.gen_code [输出目录]
    缺省输出到本包目录（与 rmlog.h / rmlog.c 同处交付）。

机制说明（IMPL"同源机制选择"一节的代码落点）:
- 错误码唯一数据源 = catalog.py 的 ERRORS 表（含级别/含义/建议动作）;
- C 端 `rmlog_errors.h` 由本模块**生成**，自带级别常量定义与静态码表,
  因此 rmlog.h 只需 include 它而不会产生循环引用;
- C 端禁止手改该文件（文件头声明 GENERATED），改表只改 catalog.py 后重新生成。
"""

import os
import sys

from . import catalog

# 生成的头文件名（C 端 include 用; 与 rmlog.h 同目录）
HEADER_NAME = "rmlog_errors.h"

# 生成的头文件说明头 —— 明确标记"生成物勿手改"，并指向再生成命令
_HEADER_BANNER = """\
/*
 * rmlog_errors.h — 错误码表（C 端）。由 python3 -m rmlog.gen_code 自动生成。
 *
 * 错误码单一来源: rmlog/catalog.py（Python 包内嵌表, 含级别/含义/建议动作）。
 * !! 本文件是生成物, 禁止手改 !!  改错误码请改 catalog.py 后重新生成:
 *     python3 -m rmlog.gen_code
 * 任何对表内容的双端不一致都属缺陷（REQ P0-a: C/Python 双端同源）。
 *
 * 任务: T-20260926-001-logging-platform-p0
 */
#ifndef RMLOG_ERRORS_H
#define RMLOG_ERRORS_H

#ifdef __cplusplus
extern "C" {
#endif
"""

_FOOTER = """\
#ifdef __cplusplus
}
#endif

#endif /* RMLOG_ERRORS_H */
"""


def _c_string(text):
    """Python 字符串 -> C 字符串字面量（处理双引号与反斜杠; 表内容均为受控中文）。"""
    return '"%s"' % text.replace("\\", "\\\\").replace('"', '\\"')


def symbol_for(code):
    """错误码 -> C 宏符号名（E-INIT-001 -> INIT_001; 去掉 E- 前缀防与级别宏混淆）。"""
    return code.replace("E-", "").replace("-", "_")


def render_header():
    """把 catalog 表渲染为 rmlog_errors.h 全文（纯函数, 便于自测对照）。"""
    lines = [_HEADER_BANNER]
    lines.append("/* 表版本: rmlog.catalog.CATALOG_VERSION = %s */" % catalog.CATALOG_VERSION)
    lines.append("")

    # 1) 级别常量: 取值顺序与 rmlog.format.LEVELS 严格一致（自测会对照）。
    #    定义在此处而非 rmlog.h —— 让生成头自包含, rmlog.h 反向引用它。
    lines.append("/* ---- 级别常量（顺序与 Python 端 format.LEVELS 一致） ---- */")
    level_values = {"INFO": 1, "WARN": 2, "ERROR": 3, "FATAL": 4}
    for name, value in level_values.items():
        lines.append("#define RMLOG_LVL_%s %d" % (name, value))
    lines.append("")

    # 2) 每码两个宏: RMLOG_CODE_<sym> = 码字符串字面量（业务直接引用, 零运行时开销）,
    #    RMLOG_LVL_<sym> = 默认级别宏（展开为上面的 RMLOG_LVL_<级别>）
    lines.append("/* ---- 每码常量: RMLOG_CODE_<域>_<序号> 与 RMLOG_LVL_<域>_<序号> ---- */")
    for item in catalog.ERRORS:
        sym = symbol_for(item["code"])
        lines.append("#define RMLOG_CODE_%s %s" % (sym, _c_string(item["code"])))
        lines.append("#define RMLOG_LVL_%s RMLOG_LVL_%s" % (sym, item["level"]))
    lines.append("")

    # 3) 结构化码表（静态数组）: 供 C 端查询函数/调试工具遍历
    lines.append("/* ---- 错误码表（与 catalog.py ERRORS 一一对应, 顺序一致） ---- */")
    lines.append("typedef struct {")
    lines.append("    const char *code;      /* 错误码字符串, 如 \"E-INIT-001\" */")
    lines.append("    int         level;     /* 默认级别（RMLOG_LVL_INFO..FATAL） */")
    lines.append("    const char *meaning;   /* 中文含义 */")
    lines.append("    const char *action;    /* 建议动作 */")
    lines.append("} rmlog_err_entry_t;")
    lines.append("")
    lines.append("static const rmlog_err_entry_t rmlog_error_table[] = {")
    for item in catalog.ERRORS:
        lines.append('    { %s, RMLOG_LVL_%s, %s, %s },' % (
            _c_string(item["code"]),
            symbol_for(item["code"]),
            _c_string(item["meaning"]),
            _c_string(item["action"]),
        ))
    lines.append("};")
    lines.append("")
    lines.append("/* 表长: 与 catalog.ERRORS 条数一致, 供遍历与双端一致性自测 */")
    lines.append("#define RMLOG_ERROR_TABLE_LEN %d" % len(catalog.ERRORS))
    lines.append("")

    # 4) 五域白名单（顺序与 catalog.DOMAINS 一致, 供码格式校验）
    lines.append("/* 五域白名单（顺序与 catalog.DOMAINS 一致） */")
    lines.append("static const char *const rmlog_domains[] = {")
    for domain in catalog.DOMAINS:
        lines.append('    %s,' % _c_string(domain))
    lines.append("};")
    lines.append("#define RMLOG_DOMAIN_COUNT %d" % len(catalog.DOMAINS))
    lines.append("")
    lines.append(_FOOTER)
    return "\n".join(lines)


def write_header(out_dir=None):
    """生成 rmlog_errors.h 到指定目录（缺省: 本包目录, 即与 rmlog.h 同目录）。

    以 UTF-8 无 BOM 写出: 内容含中文注释, gcc 默认按 UTF-8 输入处理;
    若板端工具链报编码警告, 编译时加 -finput-charset=UTF-8 即可。
    """
    if out_dir is None:
        out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, HEADER_NAME)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_header())
    return out_path


def render_doc():
    """把 catalog 表渲染为 ERR-CATALOG.md 全文（给人读的投影；纯函数便于自测对照）。

    为什么文档也要生成: 错误码表一旦同时存在"代码表"与"手写文档"两份,
    迟早漂移 —— 与 C 头文件同理, 文档也走"单一来源生成"路线。
    """
    out = []
    out.append("# ERR-CATALOG — rmlog 错误码表（表版本 %s）" % catalog.CATALOG_VERSION)
    out.append("")
    out.append("> **本文件是生成物（勿手改）**：由 `python3 -m rmlog.gen_code --doc` 从")
    out.append("> `rmlog/catalog.py` 生成 —— catalog.py 是唯一数据源；改错误码请改表后重新生成。")
    out.append("> 级别从低到高：`INFO < WARN < ERROR < FATAL`（含义见 `USAGE.md` §4）。")
    out.append("")
    out.append("错误码格式：`E-<域>-<3位序号>`。五域：%s。" % "、".join(
        "`%s`" % d for d in catalog.DOMAINS))
    for domain, desc in catalog.DOMAINS.items():
        out.append("")
        out.append("## %s 域 — %s" % (domain, desc))
        out.append("")
        out.append("| 错误码 | 默认级别 | 中文含义 | 建议动作 |")
        out.append("|---|---|---|---|")
        prefix = "E-%s-" % domain
        for item in catalog.ERRORS:
            if item["code"].startswith(prefix):
                out.append("| `%s` | %s | %s | %s |" % (
                    item["code"], item["level"], item["meaning"], item["action"]))
    out.append("")
    out.append("## 扩展规则")
    out.append("")
    out.append("1. 新增码只改 `rmlog/catalog.py` 的 `ERRORS` 表（域内序号延续现有最大值），")
    out.append("   然后重新执行 `python3 -m rmlog.gen_code`（生成 C 头）与")
    out.append("   `python3 -m rmlog.gen_code --doc`（生成本文档）；")
    out.append("2. 已发布码的语义与默认级别不得随意变更（C/Python 双端与读端工具都依赖它），")
    out.append("   确需变更时递增 `CATALOG_VERSION` 并同步 `USAGE.md`；")
    out.append("3. 新增域须同步 `catalog.py` 的 `DOMAINS`，生成器与读端工具自动跟随。")
    out.append("")
    return "\n".join(out)


def write_doc(out_path=None):
    """生成 ERR-CATALOG.md（缺省: 产物区根目录, 与 USAGE.md 同层便于查阅）。"""
    if out_path is None:
        out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "ERR-CATALOG.md")
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_doc())
    return out_path


def main(argv):
    """命令行入口:
        python3 -m rmlog.gen_code [输出目录]   生成 C 头文件 rmlog_errors.h
        python3 -m rmlog.gen_code --doc [路径]  生成 ERR-CATALOG.md
    """
    args = argv[1:]
    if args and args[0] == "--doc":
        out_path = args[1] if len(args) > 1 else None
        path = write_doc(out_path)
        print("rmlog.gen_code: 已生成 %s（表版本 %s）" % (path, catalog.CATALOG_VERSION))
        return 0
    out_dir = args[0] if args else None
    path = write_header(out_dir)
    print("rmlog.gen_code: 已生成 %s（%d 个错误码, 表版本 %s）" % (
        path, len(catalog.ERRORS), catalog.CATALOG_VERSION))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
