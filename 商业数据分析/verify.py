"""检查实际实验结果与教材数据来源，避免只提交未运行的转换代码。"""
from pathlib import Path
import ast
import hashlib
import json
from collections import Counter
from PIL import Image

def main():
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'sources.json').read_text(encoding='utf-8'))
    assert len(manifest)==20 and Counter(m['book_number'] for m in manifest)=={1:5,2:5,3:5,4:5}
    summaries=[]
    for lab in manifest:
        folder=root/lab['folder'];out=folder/'outputs'
        ast.parse((folder/'实验.py').read_text(encoding='utf-8'))
        for source in lab['sources']:
            file=folder/'data'/source.get('distributed_file',source['file'])
            expected=source.get('distributed_sha256',source['sha256'])
            assert hashlib.sha256(file.read_bytes()).hexdigest()==expected,file
        metrics=json.loads((out/'results.json').read_text(encoding='utf-8'))
        assert metrics and (out/'results.json').stat().st_size>50
        figures=sorted(out.glob('*.png'))
        assert len(figures)>=2,(lab['id'],len(figures))
        for figure in figures:
            with Image.open(figure) as image:
                assert min(image.info.get('dpi',(0,0)))>=150
                assert image.width>=1000 and image.height>=600
                image.verify()
        assert list(out.glob('*.csv')),lab['id']
        summaries.append({'id':lab['id'],'book':lab['book'],'title':lab['title'],'figures':len(figures),'status':'通过'})
    result={'experiments':len(manifest),'per_book':dict(Counter(m['book'] for m in manifest)),
            'total_figures':sum(m['figures'] for m in summaries),'source_hashes':'通过',
            'checks':'脚本语法、来源哈希、实际结果、CSV、图片完整性与分辨率','details':summaries}
    (root/'运行核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'核验通过：{len(manifest)}个实验，{result["total_figures"]}张图，各套教材5个实验。')

if __name__=='__main__':main()
