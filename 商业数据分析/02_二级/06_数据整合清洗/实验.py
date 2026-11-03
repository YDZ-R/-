"""数据整合清洗。
教材来源：CDA 教材资料2025/2《CDA 二级认证教材：量化策略分析》/第4章- 数据处理(pandas)/第4章  数据整合和数据清洗.ipynb
属于课程精选实验，具体转换范围见同目录README。
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from common import paths, read_csv, canvas, save, table, finish, classification_plots, COLORS, SEED
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    data,out=paths(__file__)
    # 对应原单元3–4：分块读取与纵向拼接；单元93：分位数盖帽。
    chunks=list(pd.read_csv(data/'big.csv',chunksize=900))
    raw=pd.concat(chunks,ignore_index=True)
    before=len(raw);df=raw.drop_duplicates().copy()
    cols=['CNT_TBM','CNT_ATM','CNT_POS']
    for c in cols:df[c]=pd.to_numeric(df[c],errors='raise')
    missing=df[cols].isna().sum()
    clean=df.copy();bounds={}
    for c in cols:
        lo,hi=df[c].quantile([.01,.99]);bounds[c]=[float(lo),float(hi)]
        clean[c]=df[c].fillna(df[c].median()).clip(lo,hi)
    totals=df.groupby('ID')[cols].sum()
    # 横向拼接保留一对一客户键，验证没有笛卡尔积。
    wide=df[['ID']].drop_duplicates().merge(totals.add_suffix('_SUM'),on='ID',validate='one_to_one')
    assert len(wide)==df.ID.nunique() and len(raw)==sum(len(c) for c in chunks)
    fig,ax=canvas('渠道业务次数均值','渠道','平均次数')
    means=pd.DataFrame({'原始':df[cols].mean(),'盖帽后':clean[cols].mean()})
    means.plot.bar(ax=ax,color=COLORS[:2],rot=0);save(fig,out,'01_渠道清洗对比')
    fig,ax=canvas('POS次数的分位数盖帽','处理阶段','POS次数')
    ax.boxplot([df.CNT_POS.dropna(),clean.CNT_POS.dropna()],tick_labels=['原始','1%–99%盖帽'],showfliers=True,flierprops={'markersize':2,'alpha':.25})
    save(fig,out,'02_POS分布对比')
    table(clean,out,'清洗数据');table(wide,out,'客户汇总宽表')
    finish(out,raw_rows=before,clean_rows=len(clean),chunks=len(chunks),duplicate_rows=before-len(df),
           missing_cells=int(missing.sum()),customers=len(wide),cap_bounds=bounds,
           note='教材预处理练习；未人为制造缺失，盖帽的统计影响不等同于发现业务错误。')

if __name__=="__main__":
    main()
