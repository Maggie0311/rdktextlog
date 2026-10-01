#!/usr/bin/env python3
# T-20260930-005：导出业务日志及可选 Linux 证据，缺失项逐项报告。
import argparse, datetime, os, subprocess, sys

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
    # 业务日志是一个文件族：主文件可能在轮转窗口内暂时不存在，副本仍是有效证据。
    members = []
    if os.path.exists(a.log):
        members.append(a.log)
    for i in range(1, 10000):
        path = a.log + '.%d' % i
        if os.path.exists(path):
            members.append(path)
        elif members and i > 1:
            break
    if members:
        target = os.path.join(a.out, 'business.log')
        selected = total = 0
        source_report = []
        with open(target, 'w', encoding='utf-8') as dst:
            for member in members:
                source_total = source_selected = 0
                try:
                    with open(member, 'r', encoding='utf-8', errors='replace') as src:
                        for raw in src:
                            total += 1; source_total += 1
                            ev = parse_line(raw)
                            if a.session and (ev is None or ev['attrs'].get('session') != a.session):
                                continue
                            dst.write(raw); selected += 1; source_selected += 1
                    source_report.append('%s: OK (%d/%d lines)' % (os.path.basename(member), source_selected, source_total))
                except OSError as exc:
                    source_report.append('%s: UNAVAILABLE (%s)' % (os.path.basename(member), exc))
        suffix = ' session=%s' % a.session if a.session else ''
        report.append('business.log: OK%s (%d/%d lines; %d sources)' % (suffix, selected, total, len(members)))
        report.extend(source_report)
    else:
        report.append('business.log: MISSING (no main log or rotation members)')
    for name,cmd in [('journal', ['journalctl','--no-pager','-o','short-precise']),('kernel',['dmesg','--color=never']),('version',['uname','-a'])]:
        ok,detail=run(name,cmd,a.out); report.append('%s: %s (%s)'%(name,'OK' if ok else 'UNAVAILABLE',detail))
    with open(os.path.join(a.out,'MANIFEST.txt'),'w',encoding='utf-8') as f:
        f.write('exported=%s\n'%datetime.datetime.now().isoformat()); f.write('\n'.join(report)+'\n')
    return 0
if __name__=='__main__': raise SystemExit(main())
