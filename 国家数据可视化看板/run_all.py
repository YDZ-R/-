"""Reproduce the local archived-data build. Does not require NBS login or network."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
for script in ['01_prepare.py','02_build_data.py','03_build.py','04_verify.py']:
    subprocess.run([sys.executable,str(root/'scripts'/script)],cwd=root,check=True)
print('构建与核验完成，请打开 index.html。')
