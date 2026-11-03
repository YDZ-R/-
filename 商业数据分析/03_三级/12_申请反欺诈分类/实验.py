"""申请反欺诈分类。
教材来源：CDA 教材资料2025/3《CDA 三级认证教材：敏捷数据挖掘》/3.1申请反欺诈（决策树系列等）/3.1.1-3.1.2分类（反欺诈_DT_EnsembleMethods）.ipynb
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
    from sklearn.model_selection import train_test_split,GridSearchCV,StratifiedKFold
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.pipeline import make_pipeline
    from sklearn.impute import SimpleImputer
    data,out=paths(__file__)
    df=read_csv(data/'loan_net.csv',skipinitialspace=True)
    X=df.iloc[:,:4];y=df.flag.astype(int)
    # 对应原单元0–2与决策树评估段，缩小网格，保留训练内交叉验证。
    tr,te=train_test_split(np.arange(len(df)),test_size=.4,stratify=y,random_state=1234)
    pipeline=make_pipeline(SimpleImputer(strategy='median'),DecisionTreeClassifier(random_state=1234))
    search=GridSearchCV(pipeline,{'decisiontreeclassifier__max_depth':[2,3,4,5],
                                 'decisiontreeclassifier__min_samples_leaf':[5,20,50]},
                        scoring='roc_auc',cv=StratifiedKFold(4,shuffle=True,random_state=SEED))
    search.fit(X.iloc[tr],y.iloc[tr]);prob=search.predict_proba(X.iloc[te])[:,1]
    metrics=classification_plots(y.iloc[te],prob,out,'网络特征反欺诈')
    table(pd.DataFrame(search.cv_results_)[['params','mean_test_score','std_test_score']],out,'训练内参数比较')
    table(pd.DataFrame({'source_row':te,'actual':y.iloc[te].to_numpy(),'probability':prob}),out,'留出预测')
    assert set(tr).isdisjoint(te)
    finish(out,rows=len(df),train_rows=len(tr),best_params=search.best_params_,cv_auc=float(search.best_score_),**metrics,
           note='精选决策树核心实验，未运行原笔记本全部集成模型；评估限于教材样本。')

if __name__=="__main__":
    main()
