# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

b = Board()
try:
    b.connect()
    print("CONNECT_OK")
    rc, out, err = b.run("uname -a; echo '---'; whoami; echo '---'; hostname", timeout=30)
    print("rc=%d" % rc)
    print("STDOUT:")
    print(out)
    print("STDERR:")
    print(err)
finally:
    b.close()
