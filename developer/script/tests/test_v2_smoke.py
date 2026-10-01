"""T-20260930-005 / AC2-AC6：第二版故障、队列、导出降级 smoke test。"""
import os, subprocess, sys, tempfile
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
from rmlog.writer import Writer
from rmlog.async_writer import AsyncWriter
from rmlog.session import Session
from rmlog.format import parse_line

def main():
    d=tempfile.mkdtemp(); w=Writer(log_dir=d); session=Session('smoke', session_id='smoke-fixed'); a=AsyncWriter(w,maxsize=1,session=session)
    accepted=sum(a.emit('E-SYS-005','test','x') for _ in range(10)); a.close()
    assert accepted >= 1 and a.dropped >= 1
    a.close()
    events=[parse_line(x) for x in open(os.path.join(d,'rmlog.log'),encoding='utf8')]
    assert any(e and e['attrs'].get('session') == 'smoke-fixed' for e in events)
    demo=tempfile.mkdtemp(); subprocess.check_call([sys.executable, os.path.join(ROOT,'rmlog','fault_demo.py'),demo,'--fail','fsm'])
    text=open(os.path.join(demo,'rmlog.log'),encoding='utf8').read(); assert 'E-FSM-003' in text
    out=tempfile.mkdtemp(); subprocess.check_call([sys.executable,os.path.join(ROOT,'export_evidence.py'),os.path.join(demo,'rmlog.log'),out,'--session','fault-demo-missing']); assert os.path.exists(os.path.join(out,'MANIFEST.txt')); assert open(os.path.join(out,'business.log'),encoding='utf8').read() == ''
    print('V2 SMOKE PASS accepted=%d dropped=%d' % (accepted,a.dropped))
if __name__=='__main__': main()
