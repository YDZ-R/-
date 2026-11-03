"""SARIMA销量预测。
教材来源：CDA 教材资料2025/3《CDA 三级认证教材：敏捷数据挖掘》/4.1时间序列预测/4.1.2销售数据预测(SARIMA).ipynb
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
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from statsmodels.tsa.seasonal import seasonal_decompose
    data,out=paths(__file__)
    df=read_csv(data/'tractor_sales.csv')
    y=pd.Series(df.Number_of_Sold.to_numpy(),index=pd.to_datetime(df.Year_Month,format='%Y-%b')).asfreq('MS')
    train,test=y.iloc[:-12],y.iloc[-12:]
    # 对应原单元2–11及15–16；仅以训练期AIC选型，最后12月不参与选择。
    candidates=[];fitted=[]
    for order in [(0,1,1),(1,1,0),(1,1,1)]:
        result=SARIMAX(np.log(train),order=order,seasonal_order=(0,1,1,12)).fit(disp=False,maxiter=250)
        converged=bool(result.mle_retvals.get('converged',False))
        candidates.append(dict(order=str(order),aic=float(result.aic),converged=converged))
        if converged:fitted.append(result)
    assert fitted,'所有候选未收敛，不能继续发布预测'
    best=min(fitted,key=lambda x:x.aic);forecast=best.get_forecast(12)
    pred=np.exp(forecast.predicted_mean);ci=np.exp(forecast.conf_int())
    assert pred.index.equals(test.index) and train.index.max()<pred.index.min()
    fig,ax=canvas('拖拉机销量：12月留出预测','月份','销量（台）',size=(10,5.5))
    ax.plot(y.index,y,label='实际销量');ax.plot(test.index,pred,label='预测中位数',ls='--')
    ax.fill_between(test.index,ci.iloc[:,0],ci.iloc[:,1],alpha=.25,color=COLORS[1],label='95%预测区间')
    ax.legend();save(fig,out,'01_SARIMA留出预测')
    decomposition=seasonal_decompose(y,model='multiplicative',period=12)
    fig=decomposition.plot();fig.set_size_inches(10,8)
    for ax,label in zip(fig.axes,['销量（台）','趋势','季节因子','剩余因子']):ax.set_ylabel(label)
    fig.axes[0].set_title('月度销量的乘法分解');save(fig,out,'02_销量季节分解')
    table(pd.DataFrame({'actual':test,'prediction_median':pred,'lower_95':ci.iloc[:,0],'upper_95':ci.iloc[:,1],'seasonal_naive':train.iloc[-12:].to_numpy()}),out,'留出预测',index=True)
    table(pd.DataFrame(candidates),out,'训练AIC候选')
    finish(out,months=len(y),train_months=len(train),test_months=len(test),order=list(best.model.order),seasonal_order=list(best.model.seasonal_order),
           rmse=float(np.sqrt(np.mean((test-pred)**2))),mape=float(np.mean(abs((test-pred)/test))*100),
           naive_rmse=float(np.sqrt(np.mean((test-train.iloc[-12:].to_numpy())**2))),
           coverage=float(((test>=ci.iloc[:,0])&(test<=ci.iloc[:,1])).mean()),
           note='exp(对数预测均值)在原尺度是中位数；修正原笔记本预测日期从最后观测月重复开始的问题。')

if __name__=="__main__":
    main()
