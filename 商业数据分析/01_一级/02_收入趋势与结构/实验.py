"""收入趋势与结构。
教材来源：CDA 教材资料2025/1《CDA 一级认证教材：商业数据分析》/第3章 商业数据分析框架/案例1：收入趋势分析/案例1：收入趋势分析原始数据.xlsx
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
    df=pd.read_excel(data/'案例1：收入趋势分析原始数据.xlsx')
    df['date']=pd.to_datetime(dict(year=df['订单年份'],month=df['订单月份'],day=1))
    monthly=df.groupby('date')['销售额'].sum().sort_index()
    # 只对有完整上一年同月的月份计算同比，不用行号错配月份。
    result=monthly.to_frame('sales');result['yoy_pct']=monthly.div(monthly.shift(12)).sub(1).mul(100)
    fig,ax=canvas('月度销售额趋势','月份','销售额（元）',size=(10,5.5))
    ax.plot(monthly.index,monthly.values,lw=2.2);ax.tick_params(axis='x',rotation=30)
    save(fig,out,'01_收入趋势')
    latest=int(df['订单年份'].max())
    current=df.loc[df['订单年份'].eq(latest)].groupby('销售省份')['销售额'].sum().sort_values(ascending=False)
    fig,ax=canvas(f'{latest}年销售额前十省份','销售额（元）','')
    top=current.head(10).sort_values();ax.barh(top.index,top.values,color=COLORS[0]);save(fig,out,'02_省份收入结构')
    table(result,out,'月度销售与同比',index=True);table(current.to_frame('sales'),out,'省份销售',index=True)
    assert np.isclose(monthly.sum(),df['销售额'].sum())
    annual=df.groupby('订单年份')['销售额'].sum()
    finish(out,raw_rows=len(df),months=len(monthly),annual_sales={str(k):float(v) for k,v in annual.items()},
           latest_year=latest,top_province=current.idxmax(),top_province_share=float(current.iloc[0]/current.sum()))

if __name__=="__main__":
    main()
