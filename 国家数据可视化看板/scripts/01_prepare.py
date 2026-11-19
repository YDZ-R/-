"""Normalize archived NBS table snapshots without filling unpublished cells."""
from pathlib import Path
import csv
import hashlib
import json
import math
import re
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
CLEAN = ROOT / 'data/clean'
CLEAN.mkdir(exist_ok=True)
records, manifest = [], []
quarter = {'一': 1, '二': 2, '三': 3, '四': 4}
for file in sorted(RAW.glob('*.json')):
    if file.name == 'source_manifest.json':
        continue
    source = json.loads(file.read_text(encoding='utf-8'))
    tables = source['tables']
    assert len(tables) == 4 and len(tables[1]) == len(tables[3]), file.name
    columns = []
    for ci, title in enumerate(tables[0][0]):
        match = re.fullmatch(r'(\d{4})年(?:第([一二三四])季度)?', title)
        if match:
            period = match[1] + (f'Q{quarter[match[2]]}' if match[2] else '')
            columns.append((ci, period))
    assert columns and len({p for _, p in columns}) == len(columns), file.name
    count = 0
    for row, label_row in zip(tables[1], tables[3]):
        label = label_row[0].strip()
        assert label, file.name
        unit_match = re.search(r'\(([^()]*)\)', label)
        unit = unit_match[1] if unit_match else ''
        for ci, period in columns:
            original = row[ci].strip() if ci < len(row) else ''
            missing = original in ('', '—', '-', '--', '…', '...', '··', '暂无数据')
            value = None if missing else float(original.replace(',', ''))
            assert value is None or math.isfinite(value), (label, period, original)
            count += value is not None
            records.append(dict(table=source['id'], indicator=label, unit=unit,
                                period=period, value=value, observed=value is not None,
                                raw_text=original))
    manifest.append(dict(file=file.name, title=source['title'], url=source['url'],
                         accessed_date=source['accessed_date'], method=source['capture_method'],
                         periods=sorted(p for _, p in columns), indicators=len(tables[1]),
                         observed_cells=count, sha256=hashlib.sha256(file.read_bytes()).hexdigest()))

df = pd.DataFrame(records).sort_values(['table', 'indicator', 'period'])
assert not df.duplicated(['table', 'indicator', 'period']).any()
df.to_csv(CLEAN / 'nbs_observations.csv', index=False, encoding='utf-8-sig')
df.to_json(CLEAN / 'nbs_observations.json', orient='records', force_ascii=False, indent=2)
with sqlite3.connect(CLEAN / 'nbs.sqlite') as conn:
    df.to_sql('observations', conn, index=False, if_exists='replace')
    conn.execute('CREATE UNIQUE INDEX IF NOT EXISTS observation_key ON observations("table",indicator,period)')

# Independently compare every domestic-tourism cell against the official Excel export.
export = RAW / 'tourism_domestic.xlsx'
sheet = pd.read_excel(export, header=None)
header = next(i for i in sheet.index if str(sheet.iloc[i, 0]).strip() == '指标')
compared = 0
for ri in range(header + 1, len(sheet)):
    label = str(sheet.iloc[ri, 0]).strip()
    matching = df[(df.table == 'tourism_domestic') & (df.indicator == label)]
    if matching.empty:
        continue
    for ci in range(1, len(sheet.columns)):
        title = str(sheet.iloc[header, ci]).strip()
        if not re.fullmatch(r'\d{4}年', title):
            continue
        cell = sheet.iloc[ri, ci]
        if pd.isna(cell):
            assert pd.isna(matching.set_index('period').loc[title[:4], 'value'])
        else:
            actual = float(matching.set_index('period').loc[title[:4], 'value'])
            assert math.isclose(actual, float(cell), abs_tol=1e-9), (label, title)
        compared += 1
assert compared == 135
manifest.append(dict(file=export.name, title='国内旅游情况官方Excel导出',
                     url='https://data.stats.gov.cn/dg/website/page.html#/pc/national/yearData',
                     accessed_date='2026-11-19', method='用户登录后，官方界面选择最近15年，下载Excel',
                     sha256=hashlib.sha256(export.read_bytes()).hexdigest(), verified_cells=compared))
(RAW / 'source_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
summary = dict(tables=len(manifest)-1, indicators=int(df[['table','indicator']].drop_duplicates().shape[0]),
               cells=len(df), observed_cells=int(df.observed.sum()), missing_cells=int((~df.observed).sum()),
               official_excel_matched_cells=compared, filled_cells=0)
(ROOT / 'outputs/data_quality.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False))
