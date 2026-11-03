"""分层抽样。
教材来源：CDA 教材资料2025/2《CDA 二级认证教材：量化策略分析》/第6章-市场调研与数据预处理/1数据采集与处理 1 数据采集方法/抽样.ipynb
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
    df=read_csv(data/'clients.csv')
    n=1000;counts=df.Dist.value_counts().sort_index()
    # 按总体地区占比分配名额，最大余数法确保恰好1000人。
    quotas=counts/len(df)*n;allocation=np.floor(quotas).astype(int)
    extra=n-int(allocation.sum());allocation.loc[(quotas-allocation).nlargest(extra).index]+=1
    stratified=pd.concat([g.sample(n=int(allocation[k]),random_state=SEED) for k,g in df.groupby('Dist')])
    simple=df.sample(n,random_state=SEED)
    systematic=df.iloc[np.floor(np.arange(n)*len(df)/n).astype(int)]
    proportions=pd.DataFrame({'总体':df.Dist.value_counts(normalize=True),'简单随机':simple.Dist.value_counts(normalize=True),
                              '分层':stratified.Dist.value_counts(normalize=True),'系统':systematic.Dist.value_counts(normalize=True)}).fillna(0).sort_index()
    errors=(proportions.drop(columns='总体').sub(proportions['总体'],axis=0)).abs().sum()/2
    fig,ax=canvas('三种抽样的地区结构误差','抽样方式','总变差距离')
    ax.bar(errors.index,errors.values,color=COLORS[:3]);save(fig,out,'01_抽样结构误差')
    fig,ax=canvas('人口最多的12个地区：样本与总体','地区编号','占比（%）',size=(11,5.5))
    proportions.loc[counts.nlargest(12).index,['总体','分层','简单随机']].mul(100).plot.bar(ax=ax,color=COLORS[:3],rot=0)
    ax.set_xlabel('地区编号')
    save(fig,out,'02_地区分层对比')
    assert len(stratified)==n and stratified.Client_id.is_unique
    table(stratified,out,'分层样本');table(proportions,out,'地区比例对比',index=True)
    finish(out,population=len(df),sample_rows=n,strata=len(counts),seed=SEED,total_variation=errors.to_dict(),
           note='系统抽样对原始排序敏感，此处只展示本次固定顺序结果。')

if __name__=="__main__":
    main()
