#!/usr/bin/env python3
# T-20260930-005：导出业务日志及可选 Linux 证据，缺失项逐项报告。
import argparse, datetime, os, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rmlog.format import parse_line

def run(name, cmd, out):
    path = os.path.join(out, name + '.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            p = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, text=True, timeout=20)
        return p.returncode == 0, 'exit=%d' % p.returncode
    except (OSError, subprocess.SubprocessError) as e:
        with open(path, 'w', encoding='utf-8') as f: f.write('UNAVAILABLE: %s\n' % e)
        return False, str(e)

def main(argv=None):
    p=argparse.ArgumentParser(); p.add_argument('log'); p.add_argument('out'); p.add_argument('--session')
    a=p.parse_args(argv); os.makedirs(a.out, exist_ok=True)
    report=[]
    if os.path.exists(a.log):
        target = os.path.join(a.out, 'business.log')
        selected = total = 0
        with open(a.log, 'r', encoding='utf-8', errors='replace') as src, open(target, 'w', encoding='utf-8') as dst:
            for raw in src:
                total += 1
                ev = parse_line(raw)
                if a.session and (ev is None or ev['attrs'].get('session') != a.session):
                    continue
                dst.write(raw)
                selected += 1
        suffix = ' session=%s' % a.session if a.session else ''
        report.append('business.log: OK%s (%d/%d lines)' % (suffix, selected, total))
    else: report.append('business.log: MISSING')
    for name,cmd in [('journal', ['journalctl','--no-pager','-o','short-precise']),('kernel',['dmesg','--color=never']),('version',['uname','-a'])]:
        ok,detail=run(name,cmd,a.out); report.append('%s: %s (%s)'%(name,'OK' if ok else 'UNAVAILABLE',detail))
    with open(os.path.join(a.out,'MANIFEST.txt'),'w',encoding='utf-8') as f:
        f.write('exported=%s\n'%datetime.datetime.now().isoformat()); f.write('\n'.join(report)+'\n')
    return 0
if __name__=='__main__': raise SystemExit(main())
