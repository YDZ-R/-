"""异常交易识别。
教材来源：CDA 教材资料2025/3《CDA 三级认证教材：敏捷数据挖掘》/3.2违规识别（孤立森林、局部异常因子）/3.2违规识别(IsolationForrest_LOF无监督).ipynb
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
    from sklearn.ensemble import IsolationForest
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score,average_precision_score,precision_score,recall_score
    data,out=paths(__file__)
    df=read_csv(data/'creditcard_sample.csv');features=[f'V{i}' for i in range(1,29)]
    # 对应原单元0–6：孤立森林。Class只用于分层留出和事后评估，不进入训练。
    train,test=train_test_split(df,test_size=.35,stratify=df.Class,random_state=SEED)
    model=IsolationForest(n_estimators=100,max_samples=1024,contamination=.02,max_features=.6,random_state=42,n_jobs=1)
    model.fit(train[features]);anomaly=-model.score_samples(test[features]);flag=model.predict(test[features])==-1
    fig,ax=canvas('异常分数的类别分布','异常分数（越大越异常）','组内密度')
    for cls,color in [(0,COLORS[0]),(1,COLORS[2])]:
        ax.hist(anomaly[test.Class.eq(cls)],bins=25,density=True,alpha=.55,label=f'实际类别 {cls}',color=color)
    ax.legend();save(fig,out,'01_异常分数分布')
    from sklearn.metrics import precision_recall_curve
    precision,recall,_=precision_recall_curve(test.Class,anomaly)
    ap=float(average_precision_score(test.Class,anomaly))
    fig,ax=canvas('稀有异常识别的PR曲线','召回率','精确率')
    ax.plot(recall,precision,lw=2,label=f'AP = {ap:.3f}');ax.axhline(test.Class.mean(),color=COLORS[2],ls='--',label='随机排序基线')
    ax.legend();save(fig,out,'02_异常识别PR曲线')
    table(test[['source_row','Class']].assign(anomaly_score=anomaly,predicted_anomaly=flag),out,'异常评分')
    assert set(train.source_row).isdisjoint(test.source_row)
    finish(out,sample_rows=len(df),train_rows=len(train),test_rows=len(test),fraud_rows=int(df.Class.sum()),
           test_fraud_rows=int(test.Class.sum()),auc=float(roc_auc_score(test.Class,anomaly)),average_precision=ap,
           precision=float(precision_score(test.Class,flag,zero_division=0)),recall=float(recall_score(test.Class,flag)),
           contamination=.02,note='原284807条数据按Class分层抽60000条，保持类别比例；种子241。固定2%异常预算不等于真实欺诈率。')

if __name__=="__main__":
    main()
