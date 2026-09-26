import os, sys
sys.path.insert(0, r'D:\rdk_x5_software\developer\script')
from rmlog.writer import Writer
w = Writer(log_dir=r'D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\own_run_work\ac6')
w.event('E-SYS-005', 'victim', '崩溃前最后一条里程碑')
w.event('E-INIT-002', 'victim', 'FATAL: 关键组件初始化失败, 即将硬崩溃')
os._exit(1)
