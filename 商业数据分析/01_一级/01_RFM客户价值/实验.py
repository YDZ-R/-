"""RFM客户价值。
教材来源：CDA 教材资料2025/1《CDA 一级认证教材：商业数据分析》/第2章 数据分析方法/1、分析的基础范式/data-无答案/1-2RFM模型.xlsx
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
    df=pd.read_excel(data/'1-2RFM模型.xlsx',sheet_name='原始数据')
    df['销售日期']=pd.to_datetime(df['销售日期'])
    # 教材的F指购买次数，同一流水号多行商品先汇成一次交易；退货单独审计。
    returned=df['销售金额'].le(0)
    valid=df.loc[~returned].copy()
    orders=valid.groupby(['用户编号','流水号'],as_index=False).agg(date=('销售日期','max'),amount=('销售金额','sum'))
    origin=orders.date.max()+pd.Timedelta(days=1)
    rfm=orders.groupby('用户编号').agg(last_date=('date','max'),F=('流水号','nunique'),M=('amount','sum'))
    rfm['R']=(origin-rfm.last_date).dt.days
    # 中位数划分八类，不用相同的R方向给高分；阈值一并保存，避免口径不明。
    med=rfm[['R','F','M']].median()
    rfm['R高']=rfm.R.le(med.R);rfm['F高']=rfm.F.gt(med.F);rfm['M高']=rfm.M.gt(med.M)
    names={'111':'重要价值','101':'重要发展','011':'重要保持','001':'重要挽留',
           '110':'一般价值','100':'一般发展','010':'一般保持','000':'一般挽留'}
    code=rfm[['R高','F高','M高']].astype(int).astype(str).agg(''.join,axis=1)
    rfm['segment']=code.map(names)
    segments=rfm.groupby('segment').agg(customers=('R','size'),amount=('M','sum')).sort_values('customers')
    fig,ax=canvas('RFM八类客户规模','客户数','')
    ax.barh(segments.index,segments.customers,color=COLORS[0]);save(fig,out,'01_RFM客户规模')
    fig,ax=canvas('客户频次与消费金额','购买次数 F','消费金额 M（元）')
    points=ax.scatter(rfm.F,rfm.M,c=rfm.R,cmap='viridis_r',s=14,alpha=.5)
    ax.set_yscale('symlog',linthresh=100);fig.colorbar(points,ax=ax,label='距末次购买天数 R')
    save(fig,out,'02_频次金额分布')
    assert segments.customers.sum()==len(rfm) and np.isclose(rfm.M.sum(),orders.amount.sum())
    table(rfm,out,'客户RFM',index=True);table(segments,out,'分群汇总',index=True)
    finish(out,raw_rows=len(df),excluded_nonpositive_rows=int(returned.sum()),customers=len(rfm),orders=len(orders),
           reference_date=str(origin.date()),median_thresholds=med.to_dict(),largest_segment=segments.customers.idxmax())

if __name__=="__main__":
    main()
