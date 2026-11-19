"""Package just this project. No deletion, nested archives, credentials or caches."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
for required in ['index.html','DESIGN.md','.impeccable/design.json','outputs/verification.json']:
    assert (ROOT/required).is_file(),f'缺少交付文件：{required}'
excluded={'.git','.impeccable','__pycache__','.venv','_work','releases'}
manifest_path=ROOT/'outputs/package_manifest.json'
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and (not any(x in excluded for x in p.relative_to(ROOT).parts)
             or p.relative_to(ROOT).as_posix()=='.impeccable/design.json')
             and not p.name.startswith('~$') and p.suffix not in {'.pyc','.zip'} and p!=manifest_path)
manifest=[dict(file=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
files.append(manifest_path)
release=ROOT/'releases/国家数据四主题看板.zip'
release.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(release,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as archive:
    for file in files:archive.write(file,ROOT.name+'/'+file.relative_to(ROOT).as_posix())
with zipfile.ZipFile(release) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist())==len(files)
    for item in manifest:
        assert hashlib.sha256(archive.read(ROOT.name+'/'+item['file'])).hexdigest()==item['sha256']
destination=ROOT.parent.parent/'国家数据可视化看板_完整项目.zip'
assert destination.resolve().parent==ROOT.parent.parent.resolve()
shutil.copyfile(release,destination)
digest=hashlib.sha256(release.read_bytes()).hexdigest()
assert hashlib.sha256(destination.read_bytes()).hexdigest()==digest
print(json.dumps(dict(files=len(files),bytes=release.stat().st_size,sha256=digest,release=str(release),copy=str(destination)),ensure_ascii=False))
