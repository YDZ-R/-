"""Emit self-contained dashboard HTML with local ECharts; no server is required."""
from pathlib import Path
import csv
import html
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
template = (ROOT/'scripts/dashboard_template.html').read_text(encoding='utf-8')
revision=hashlib.sha256((ROOT/'assets/app.js').read_bytes()+(ROOT/'assets/style.css').read_bytes()).hexdigest()[:12]
names = {'economy':'季度经济','tourism':'旅游与住宿','education':'教育发展','population':'人口与民生'}
datasets = {key:json.loads((ROOT/f'data/clean/{key}.json').read_text(encoding='utf-8')) for key in names}

def emit(key, destination, nested):
    data = datasets[key]
    nav = ''.join(f'<a href="{("" if nested else "dashboards/") + k + ".html"}"'+
                  (' aria-current="page"' if key == k else '')+f'>{label}</a>' for k,label in names.items())
    replacements = {'__TITLE__':html.escape(data['title']), '__ASSETS__':'../assets/' if nested else 'assets/',
                    '__HOME__':'../index.html' if nested else 'index.html', '__NAV__':nav,'__REV__':revision,
                    '__DATA__':json.dumps(data,ensure_ascii=False,separators=(',',':'),allow_nan=False).replace('</','<\\/')}
    output = template
    for token,value in replacements.items():
        output = output.replace(token,value)
    destination.write_text(output,encoding='utf-8')

emit('economy',ROOT/'index.html',False)
for key in names:
    emit(key,ROOT/f'dashboards/{key}.html',True)
with (ROOT/'data/clean/data_dictionary.csv').open('w',encoding='utf-8-sig',newline='') as stream:
    writer=csv.writer(stream)
    writer.writerow(['主题','指标键','显示名','单位','源表','源指标','转换系数','减去常数','计算依赖','最早有效期','最近有效期','有效观测数'])
    for d in datasets.values():
        for s in d['series'].values():
            valid=sorted(p for p,v in s['values'].items() if v is not None)
            writer.writerow([d['title'],s['id'],s['label'],s['unit'],s.get('source_table','计算指标'),s.get('source_indicator',''),
                             s.get('source_factor',''),s.get('source_subtract',''),';'.join(s.get('derived_from',[])),
                             valid[0] if valid else '',valid[-1] if valid else '',len(valid)])
with (ROOT/'outputs/chart_catalog.csv').open('w',encoding='utf-8-sig',newline='') as stream:
    writer=csv.writer(stream)
    writer.writerow(['主题','图表编号','图表标题','图形类型','章节','指标键'])
    for d in datasets.values():
        for c in d['charts']:
            writer.writerow([d['title'],c['id'],c['title'],c['type'],c['section'],';'.join(c['keys'])])
print('已生成统一入口、四个独立看板及64幅图表目录。')
