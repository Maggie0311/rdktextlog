# -*- coding: utf-8 -*-
"""Pinned-version wheel downloader. Queries per-version JSON (small/fast) and
picks a compatible win_amd64/any wheel. Extracts to pylib/."""
import json, os, re, urllib.request, zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
WHEELS = os.path.join(BASE, "wheels")
PYLIB = os.path.join(BASE, "pylib")
os.makedirs(WHEELS, exist_ok=True)
os.makedirs(PYLIB, exist_ok=True)

# (name, pinned version)
PINS = [
    ("paramiko", "5.0.0"),
    ("bcrypt", "4.2.1"),
    ("cryptography", "44.0.0"),
    ("invoke", "2.2.0"),
    ("pynacl", "1.5.0"),
    ("cffi", "1.17.1"),
    ("pycparser", "2.22"),
]

def log(m):
    print(m, flush=True)

def get(name, ver):
    url = "https://pypi.org/pypi/%s/%s/json" % (name, ver)
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)

def ok(py, abi, plat):
    if plat not in ("win_amd64", "any"):
        return False
    if py in ("py3", "py2.py3"):
        return True
    m = re.match(r"^cp(\d+)$", py)
    if not m:
        return False
    n = int(m.group(1))
    if abi == "abi3":
        return n <= 313
    return n == 313

for name, ver in PINS:
    try:
        data = get(name, ver)
        urls = data.get("urls", [])
        cands = []
        for f in urls:
            fn = f["filename"]
            if not fn.endswith(".whl"):
                continue
            parts = fn[:-4].split("-")
            if len(parts) < 4:
                continue
            py, abi, plat = parts[-3], parts[-2], parts[-1]
            if ok(py, abi, plat):
                cands.append((f, py, abi, plat))
        if not cands:
            log("NO-WHEEL %s %s -> %s" % (name, ver, [u["filename"] for u in urls if u["filename"].endswith(".whl")]))
            continue
        cands.sort(key=lambda c: (100 if (c[1].startswith("cp") and not c[2].startswith("abi3")) else (50 if c[2]=="abi3" else 0)) + (10 if c[3]=="win_amd64" else 0), reverse=True)
        f = cands[0][0]
        fn = f["filename"]
        dest = os.path.join(WHEELS, fn)
        if not os.path.exists(dest):
            log("DOWNLOAD %s" % fn)
            urllib.request.urlretrieve(f["url"], dest)
            log("  saved %d bytes" % os.path.getsize(dest))
        else:
            log("CACHED %s" % fn)
        with zipfile.ZipFile(dest) as zf:
            zf.extractall(PYLIB)
        log("  extracted -> pylib")
    except Exception as e:
        log("ERROR %s %s: %r" % (name, ver, e))

log("DONE")
