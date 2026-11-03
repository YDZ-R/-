"""效应分解预报。
教材来源：CDA 教材资料2025/1《CDA 一级认证教材：商业数据分析》/第10章 使用效应分解方法做预报/AirPassengers.csv
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
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    data,out=paths(__file__)
    df=read_csv(data/'AirPassengers.csv')
    y=pd.Series(df.AIR.to_numpy(),index=pd.to_datetime(df.DATE,format='%m/%d/%Y')).asfreq('MS')
    assert y.notna().all() and (y>0).all()
    # 迁移教材趋势×季节×随机效应思路；预测只用训练段，保留最后12个月评估。
    decomposition=seasonal_decompose(y,model='multiplicative',period=12)
    fig=decomposition.plot();fig.set_size_inches(10,8)
    for ax,label in zip(fig.axes,['旅客量（千人）','趋势','季节因子','剩余因子']):ax.set_ylabel(label)
    fig.axes[0].set_title('航空旅客量的乘法效应分解');save(fig,out,'01_趋势季节分解')
    train,test=y.iloc[:-12],y.iloc[-12:]
    model=ExponentialSmoothing(train,trend='add',seasonal='mul',seasonal_periods=12,initialization_method='estimated').fit()
    prediction=model.forecast(12);naive=train.iloc[-12:].to_numpy()
    fig,ax=canvas('效应预报的12个月留出验证','年份','旅客量（千人）')
    ax.plot(y.index,y,label='实际');ax.plot(test.index,prediction,label='Holt-Winters',ls='--')
    ax.plot(test.index,naive,label='去年同期',color=COLORS[2],ls=':');ax.legend();save(fig,out,'02_效应法留出预测')
    result=pd.DataFrame({'actual':test,'forecast':prediction,'seasonal_naive':naive})
    table(result,out,'留出预测',index=True)
    finish(out,months=len(y),train_months=len(train),test_months=len(test),
           rmse=float(np.sqrt(np.mean((test-prediction)**2))),mape=float(np.mean(abs((test-prediction)/test))*100),
           naive_rmse=float(np.sqrt(np.mean((test-naive)**2))),note='此项为效应分解法的Python迁移，不声称数值等于PowerBI内部实现。')

if __name__=="__main__":
    main()
