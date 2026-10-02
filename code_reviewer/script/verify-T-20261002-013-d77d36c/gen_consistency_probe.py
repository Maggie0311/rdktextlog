"""复审留档：验证 d77d36c 上生成物与生成器渲染逐字节一致（F-05 核销证据）。"""
import os
import pathlib
import sys

ROOT = r"D:\rdk_x5_software\code_reviewer\script\verify-T-20261002-013-d77d36c\developer\script"
sys.path.insert(0, ROOT)

from rmlog import gen_code  # noqa: E402

here = pathlib.Path(r"D:\rdk_x5_software\code_reviewer\script\verify-T-20261002-013-d77d36c")
regenerated = here / "regenerated"
regenerated.mkdir(exist_ok=True)

schema_out = gen_code.write_schema(str(regenerated))
header_out = gen_code.write_header(str(regenerated))

committed_schema = pathlib.Path(ROOT) / "shared" / "rmlog_schema.h"
committed_header = pathlib.Path(ROOT) / "rmlog" / "rmlog_errors.h"

schema_same = pathlib.Path(schema_out).read_bytes() == committed_schema.read_bytes()
header_same = pathlib.Path(header_out).read_bytes() == committed_header.read_bytes()

print("schema_identical=%s" % schema_same)
print("header_identical=%s" % header_same)
# 校验 schema banner 中已无残留 rmlog_errors 文件名（F-05）
text = committed_schema.read_text(encoding="utf-8")
print("schema_has_rmlog_errors_h_ref=%s" % ("rmlog_errors.h" in text))
print("schema_banner_line2=%r" % text.splitlines()[1])
sys.exit(0 if (schema_same and header_same) else 1)
