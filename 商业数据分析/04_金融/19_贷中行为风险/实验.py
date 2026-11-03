"""贷中行为风险。
教材来源：CDA 教材资料2025/4《金融数据分析和数据挖掘案例实战》/第6章-贷中信用风险预测模型（B卡）/第6章贷中信用风险预测模型（B卡）代码通过.ipynb
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
    from sklearn.pipeline import make_pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    data,out=paths(__file__)
    balance=read_csv(data/'CreditBalance.csv');labels=read_csv(data/'label.csv')
    # 对应原单元13–21：3/6/12个月还款、逾期和额度特征；按客户留出。
    assert not labels.duplicated(['Cust_ID','Account_ID']).any()
    base=balance.merge(labels[['Cust_ID','Account_ID','Credit_Limit']],on=['Cust_ID','Account_ID'],validate='many_to_one')
    base['pay_ratio']=base.Payment/base.Balance.where(base.Balance.gt(0))
    base['utilization']=base.Balance.clip(lower=0)/base.Credit_Limit.where(base.Credit_Limit.gt(0))
    blocks=[]
    for window in [3,6,12]:
        recent=base.loc[base.Period.between(13-window,12)]
        features=recent.groupby('Cust_ID').agg(balance_mean=('Balance','mean'),pay_ratio=('pay_ratio','mean'),
                    delq1_rate=('Delq1','mean'),delq3_max=('Delq3','max'),utilization=('utilization','mean'),spend_mean=('Spend','mean'))
        blocks.append(features.add_suffix(f'_L{window}M'))
    abt=pd.concat(blocks,axis=1)
    account=labels.groupby('Cust_ID').agg(accounts=('Account_ID','nunique'),limit_total=('Credit_Limit','sum'),target=('label','max'))
    abt=abt.join(account,how='inner',validate='one_to_one').replace([np.inf,-np.inf],np.nan)
    tr,te=train_test_split(abt,test_size=.33,stratify=abt.target,random_state=1234)
    cols=list(abt.columns.drop('target'))
    model=make_pipeline(SimpleImputer(strategy='median',keep_empty_features=True),StandardScaler(),LogisticRegression(max_iter=1500))
    model.fit(tr[cols],tr.target);prob=model.predict_proba(te[cols])[:,1]
    metrics=classification_plots(te.target,prob,out,'贷中行为风险')
    table(abt,out,'客户行为宽表',index=True);table(te[['target']].assign(probability=prob),out,'客户留出预测',index=True)
    assert abt.index.is_unique and set(tr.index).isdisjoint(te.index)
    finish(out,balance_rows=len(balance),account_rows=len(labels),customers=len(abt),train_customers=len(tr),feature_count=len(cols),**metrics,
           note='精选还款/逾期/额度聚合与逻辑回归，未使用toad。教材未提供标签实际起止日期，当前是客户留出验证，不宣称时间外泛化。')

if __name__=="__main__":
    main()
