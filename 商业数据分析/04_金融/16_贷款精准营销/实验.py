"""贷款精准营销。
教材来源：CDA 教材资料2025/4《金融数据分析和数据挖掘案例实战》/第2章-某银行贷款产品精准营销模型/第二章某银行贷款产品精准营销模型代码通过.ipynb
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
    df=read_csv(data/'tran0917.csv');scoring=read_csv(data/'pred0917.csv')
    cols=['avg_balance','cv_balance','sum_expenditure','card']
    # 对应原单元28、34、36–42；原模型4个解释变量，禁止把loan_date/status/amount当特征。
    for frame in [df,scoring]:
        frame[cols]=frame[cols].apply(pd.to_numeric,errors='coerce').replace([np.inf,-np.inf],np.nan)
    assert df.account_id.is_unique
    train,test=train_test_split(df,test_size=.3,stratify=df.y,random_state=1234)
    bounds=train[cols].quantile([.01,.99])
    def features(frame):return frame[cols].clip(bounds.iloc[0],bounds.iloc[1],axis=1)
    model=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),LogisticRegression(max_iter=1500))
    model.fit(features(train),train.y);prob=model.predict_proba(features(test))[:,1]
    metrics=classification_plots(test.y,prob,out,'贷款需求识别')
    score=scoring[['account_id']].copy();score['probability']=model.predict_proba(features(scoring))[:,1]
    score=score.sort_values('probability',ascending=False);score['priority_rank']=np.arange(1,len(score)+1)
    table(score,out,'教材待评分账户排序');table(test[['account_id','y']].assign(probability=prob),out,'留出预测')
    assert set(train.account_id).isdisjoint(test.account_id)
    finish(out,rows=len(df),train_rows=len(train),scoring_rows=len(scoring),features=cols,**metrics,
           note='客户内的历史快照可能重复出现在待评分文件，故不把该文件称为独立外部测试集。排序是教学示范。')

if __name__=="__main__":
    main()
