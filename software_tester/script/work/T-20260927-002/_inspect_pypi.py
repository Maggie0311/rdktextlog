# -*- coding: utf-8 -*-
"""Inspect PyPI JSON for the packages paramiko needs, print requires_dist + candidate wheels."""
import json, urllib.request, sys

PKGS = ["paramiko", "bcrypt", "cryptography", "pynacl", "cffi", "pycparser"]

def get(name):
    url = "https://pypi.org/pypi/%s/json" % name
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)

for name in PKGS:
    try:
        data = get(name)
        info = data["info"]
        ver = info["version"]
        reqs = info.get("requires_dist") or []
        print("=" * 70)
        print("PACKAGE %s  latest=%s" % (name, ver))
        print("  requires_dist:")
        for r in reqs:
            print("    - %s" % r)
        print("  wheels (cp313 or abi3, win):")
        for f in data["urls"]:
            fn = f["filename"]
            if fn.endswith(".whl") and ("win_amd64" in fn or "win32" in fn or "none-any" in fn):
                # filter for py3 compatible
                py = fn.split("-")[2]
                if "none-any" in fn or py.startswith("cp3") or py.startswith("py3"):
                    print("    %s" % fn)
    except Exception as e:
        print("ERROR %s: %r" % (name, e))
