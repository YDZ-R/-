"""Verify archived source integrity, unit mappings, aggregates and build coverage."""
from pathlib import Path
import hashlib
import json
import math
import re
import sqlite3
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name,condition,detail=None):
    checks.append(dict(check=name,passed=bool(condition),detail=detail))

def load(relative):return json.loads((ROOT/relative).read_text(encoding='utf-8'))
manifest=load('data/raw/source_manifest.json')
for item in manifest:
    check('原始文件SHA256 '+item['file'],hashlib.sha256((ROOT/'data/raw'/item['file']).read_bytes()).hexdigest()==item['sha256'])
facts=pd.read_csv(ROOT/'data/clean/nbs_observations.csv',dtype={'period':str})
check('主键无重复',not facts.duplicated(['table','indicator','period']).any())
check('空白与观测标记一致',(facts.value.notna()==facts.observed).all())
check('有效数值有限',all(math.isfinite(v) for v in facts.value.dropna()))
with sqlite3.connect(ROOT/'data/clean/nbs.sqlite') as conn:
    count=conn.execute('SELECT COUNT(*) FROM observations').fetchone()[0]
check('SQLite与CSV记录数一致',count==len(facts))
themes={key:load(f'data/clean/{key}.json') for key in ['economy','tourism','education','population']}
all_types=set()
mapped=0
for key,d in themes.items():
    check(key+' 恰有16图',len(d['charts'])==16)
    check(key+' 时期唯一且排序',d['periods']==sorted(set(d['periods'])))
    for s in d['series'].values():
        check(key+'/'+s['id']+' 数值有效',all(v is None or math.isfinite(v) for v in s['values'].values()))
        if 'source_table' in s:
            rows=facts[(facts.table==s['source_table'])&(facts.indicator==s['source_indicator'])]
            same=True
            for r in rows.itertuples():
                expected=None if pd.isna(r.value) else round(r.value*s['source_factor']-s['source_subtract'],6)
                actual=s['values'].get(r.period)
                same &= actual is None if expected is None else actual is not None and math.isclose(expected,actual,abs_tol=1e-8)
                mapped+=1
            check(key+'/'+s['id']+' 源数据映射',same)
        else:
            for period,value in s['values'].items():
                inputs=[d['series'][k]['values'].get(period) for k in s['derived_from']]
                if any(v is None for v in inputs):
                    check(key+'/'+s['id']+'/'+period+' 不补缺',value is None)
    for c in d['charts']:
        all_types.add(c['type'])
        for field in ['keys','rightkeys','ykeys','sizekeys']:
            for k in c.get(field,[]):
                for mode in ['current','cumulative']:
                    check(key+'/'+c['id']+' 指标引用 '+k+' '+mode,k.replace('@',mode) in d['series'])
    document=(ROOT/f'dashboards/{key}.html').read_text(encoding='utf-8')
    check(key+' 离线HTML无占位符',not re.search(r'__[A-Z]+__',document))
    check(key+' 方向约定保留','pinned-reference-20261119' in document)

def aggregate(theme,total,parts,tolerance):
    d=themes[theme];errors=[]
    for period in d['periods']:
        values=[d['series'][k]['values'].get(period) for k in [total]+parts]
        if all(v is not None for v in values):errors.append((period,abs(values[0]-sum(values[1:]))))
    worst=max((e for _,e in errors),default=0)
    check(theme+' '+total+' 分类合计',worst<=tolerance,dict(max_difference=round(worst,6),tolerance=tolerance,periods=len(errors)))

for mode in ['current','cumulative']:
    aggregate('economy','gdp_'+mode,[f'sector{i}_{mode}' for i in [1,2,3]],.000201)
aggregate('tourism','trips',['urban_trips','rural_trips'],.010001)
aggregate('tourism','spending',['urban_spending','rural_spending'],.000021)
aggregate('population','population',['male','female'],1)
aggregate('population','population',['urban','rural'],1)
aggregate('population','population',['young','working','old'],1)
aggregate('population','consumption',[f'spend{i}' for i in range(8)],3)
aggregate('population','income',['wage','business','property','transfer'],2)
# 2020 total is published to whole million yuan, whereas the component tables
# retain 10,000-yuan precision. Their archived difference is 610,000 yuan;
# preserve both values rather than silently balancing them.
aggregate('education','fund_total',['fund_'+k for k in ['public','private','donation','institution','other']],.01)
check('四主题共有64图',sum(len(x['charts']) for x in themes.values())==64)
check('图形类型不少于20种',len(all_types)>=20,sorted(all_types))
quality=load('outputs/data_quality.json')
check('未填充缺失值',quality['filled_cells']==0)
check('官方Excel逐格核对135格',quality['official_excel_matched_cells']==135)
check('本地ECharts完整',(ROOT/'assets/echarts.min.js').stat().st_size>500000)
result=dict(passed=all(x['passed'] for x in checks),checks=len(checks),source_mapped_cells=mapped,
            chart_types=len(all_types),failures=[x for x in checks if not x['passed']],
            aggregates=[x for x in checks if '分类合计' in x['check']],data_quality=quality)
(ROOT/'outputs/verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
assert result['passed'],'核验失败，见 outputs/verification.json'
