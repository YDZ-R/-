"""贷前信用风险。
教材来源：CDA 教材资料2025/4《金融数据分析和数据挖掘案例实战》/第5章-贷前信用风险预测模型（A卡）/第5章贷前信用风险预测模型（A卡）代码通过.ipynb
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
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    data,out=paths(__file__)
    df=read_csv(data/'creditdata_small.csv').drop_duplicates('ID').copy()
    df=df.dropna(subset=['TARGET']);df['TARGET']=df.TARGET.astype(int)
    train,test=train_test_split(df,test_size=.33,stratify=df.TARGET,random_state=1223)
    # 对应原单元13–43、57：训练分箱→WOE→IV/相关筛选→逻辑回归→信用分。
    # 不依赖toad；分箱、缺失处理、IV均只从训练集学习。
    train_columns={};test_columns={};ivs={};rows=[]
    for col in df.columns.drop(['ID','TARGET']):
        s=train[col]
        if s.isna().mean()>.9 or s.nunique()<2:continue
        if pd.api.types.is_numeric_dtype(s):
            cuts=np.unique(s.dropna().quantile([.2,.4,.6,.8]).to_numpy())
            edges=np.r_[-np.inf,cuts,np.inf]
            tr_bins=pd.cut(s,bins=edges,duplicates='drop').astype('string').fillna('MISSING')
            te_bins=pd.cut(test[col],bins=edges,duplicates='drop').astype('string').fillna('MISSING')
        else:
            tr_bins=s.astype('string').fillna('MISSING');te_bins=test[col].astype('string').fillna('MISSING')
        stats=pd.crosstab(tr_bins,train.TARGET).reindex(columns=[0,1],fill_value=0)
        good=(stats[0]+.5)/(stats[0].sum()+.5*len(stats));bad=(stats[1]+.5)/(stats[1].sum()+.5*len(stats))
        woe=np.log(good/bad);ivs[col]=float(((good-bad)*woe).sum())
        train_columns[col]=tr_bins.map(woe).astype(float).fillna(0);test_columns[col]=te_bins.map(woe).astype(float).fillna(0)
        for key,value in woe.items():rows.append(dict(feature=col,bin=str(key),woe=float(value),iv=ivs[col]))
    wtrain=pd.DataFrame(train_columns,index=train.index);wtest=pd.DataFrame(test_columns,index=test.index)
    selected=[];corr=wtrain.corr().abs()
    for col in sorted(ivs,key=ivs.get,reverse=True):
        if ivs[col]>=.02 and not any(corr.loc[col,c]>.7 for c in selected):selected.append(col)
        if len(selected)==12:break
    assert selected,'无满足IV阈值的特征'
    model=LogisticRegression(max_iter=1500).fit(wtrain[selected],train.TARGET)
    prob=model.predict_proba(wtest[selected])[:,1]
    metrics=classification_plots(test.TARGET,prob,out,'贷前WOE风险模型')
    # 教材基准分600、好坏比35、PDO=50；此处明确用好/坏赔率。
    p=np.clip(prob,1e-8,1-1e-8);scores=600+50/np.log(2)*np.log((1-p)/p/35)
    table(pd.DataFrame({'ID':test.ID,'actual':test.TARGET,'probability':prob,'score':scores}),out,'留出信用评分')
    table(pd.DataFrame(rows),out,'训练分箱WOE与IV')
    table(pd.DataFrame({'feature':selected,'coefficient':model.coef_[0],'iv':[ivs[c] for c in selected]}),out,'入模变量')
    assert set(train.ID).isdisjoint(test.ID) and np.isfinite(scores).all()
    finish(out,rows=len(df),train_rows=len(train),selected_features=selected,base_score=600,base_good_bad_odds=35,pdo=50,**metrics,
           note='以训练集五分位箱替代教材toad决策树分箱与逐步回归，保留WOE评分卡逻辑；不是复现同一组最优系数，不用于真实授信。')

if __name__=="__main__":
    main()
