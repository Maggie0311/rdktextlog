# -*- coding: utf-8 -*-
"""Direct wheel downloader (bypasses pip, which is blocked by sandbox mkdtemp issue).

Downloads paramiko + transitive deps as platform wheels and extracts them to pylib/.
Uses only urllib + zipfile + os.makedirs (all verified to work under the sandbox).
"""
import json, os, re, sys, urllib.request, zipfile, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
WHEELS = os.path.join(BASE, "wheels")
PYLIB = os.path.join(BASE, "pylib")
os.makedirs(WHEELS, exist_ok=True)
os.makedirs(PYLIB, exist_ok=True)

PYVER = (3, 13)  # target python3 = 3.13.14

# top-level closure for core paramiko SSH usage
PACKAGES = ["paramiko", "bcrypt", "cryptography", "invoke", "pynacl", "cffi", "pycparser"]

def log(msg):
    print(msg, flush=True)

def get_json(name):
    url = "https://pypi.org/pypi/%s/json" % name
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)

def tags_ok(py, abi, plat):
    if plat not in ("win_amd64", "any"):
        return False
    if py in ("py3", "py2.py3"):
        return True
    m = re.match(r"^cp(\d+)$", py)
    if not m:
        return False
    n = int(m.group(1))
    if abi == "abi3":
        return n <= PYVER[1]
    if abi == "none":
        return n == PYVER[1]
    return n == PYVER[1]

def pick_wheel(files):
    cands = []
    for f in files:
        fn = f["filename"]
        if not fn.endswith(".whl"):
            continue
        parts = fn[:-4].split("-")
        if len(parts) < 4:
            continue
        py, abi, plat = parts[-3], parts[-2], parts[-1]
        if tags_ok(py, abi, plat):
            cands.append((f, py, abi, plat))
    if not cands:
        return None
    # prefer cp313-specific over abi3 over pure, prefer win_amd64 over any
    def score(c):
        f, py, abi, plat = c
        s = 0
        if py.startswith("cp") and not abi.startswith("abi3"):
            s += 100
        elif abi == "abi3":
            s += 50
        if plat == "win_amd64":
            s += 10
        return s
    cands.sort(key=score, reverse=True)
    return cands[0][0]

for name in PACKAGES:
    try:
        data = get_json(name)
        ver = data["info"]["version"]
        f = pick_wheel(data["urls"])
        if not f:
            log("NO-WHEEL %s (latest %s) — files: %s" % (
                name, ver, [u["filename"] for u in data["urls"] if u["filename"].endswith(".whl")][:8]))
            continue
        fn = f["filename"]
        url = f["url"]
        dest = os.path.join(WHEELS, fn)
        if os.path.exists(dest):
            log("CACHED %s" % fn)
        else:
            log("DOWNLOAD %s  (%s)  %d bytes" % (fn, f.get("packagetype"), f.get("size", 0)))
            urllib.request.urlretrieve(url, dest)
            log("  -> saved %s (%d bytes)" % (fn, os.path.getsize(dest)))
        # extract
        with zipfile.ZipFile(dest) as zf:
            zf.extractall(PYLIB)
        log("  -> extracted into pylib")
    except Exception as e:
        log("ERROR %s: %r" % (name, e))

log("DONE")
