"""从任意工作目录运行20个精选实验；--only 01 08可只运行指定实验。"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time

def main():
    root=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser()
    parser.add_argument('--only',nargs='+',help='实验编号，例如01 08')
    args=parser.parse_args()
    selected=set(args.only or [])
    labs=json.loads((root/'sources.json').read_text(encoding='utf-8'))
    if selected-set(m['id'] for m in labs):parser.error('包含不存在的实验编号')
    env=os.environ.copy();env['PYTHONIOENCODING']='utf-8'
    # 控制教学实验的线性代数线程数，避免不同机器无效争抢资源。
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:env[key]='1'
    start=time.perf_counter()
    for lab in labs:
        if selected and lab['id'] not in selected:continue
        script=root/lab['folder']/'实验.py'
        print(f'\n[{lab["id"]}/20] {lab["title"]}',flush=True)
        subprocess.run([sys.executable,str(script)],cwd=root,env=env,check=True)
    print(f'\n所选实验运行完毕，用时{time.perf_counter()-start:.1f}秒。')
    if not selected:subprocess.run([sys.executable,str(root/'verify.py')],cwd=root,env=env,check=True)

if __name__=='__main__':main()
