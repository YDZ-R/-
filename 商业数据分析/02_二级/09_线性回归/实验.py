"""线性回归。
教材来源：CDA 教材资料2025/2《CDA 二级认证教材：量化策略分析》/第8章-使用统计学方法进行检验和预测/线性回归/线性回归.ipynb
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
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import make_pipeline
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error,r2_score
    data,out=paths(__file__)
    df=pd.read_excel(data/'LR_practice.xlsx')
    # 对应原单元3、9、42、45、60；异常年龄置缺失，填补仅在训练集学习。
    df['avg_exp']=pd.to_numeric(df.avg_exp,errors='coerce');df=df.dropna(subset=['avg_exp']).copy()
    df['gender']=df.gender.map({'Male':1,'Female':0})
    df['edu_class']=df.edu_class.fillna('缺失')
    df.loc[~df.Age.between(18,100),'Age']=np.nan
    num=['gender','Age','Income','Ownrent','Selfempl','dist_home_val','dist_avg_income']
    cols=num+['edu_class'];train,test=train_test_split(df,test_size=.3,random_state=SEED)
    pre=ColumnTransformer([('num',SimpleImputer(strategy='median'),num),('edu',OneHotEncoder(drop='first',handle_unknown='ignore'),['edu_class'])])
    model=make_pipeline(pre,LinearRegression()).fit(train[cols],train.avg_exp)
    pred=model.predict(test[cols]);residual=test.avg_exp-pred
    fig,ax=canvas('消费金额：留出集实际与预测','实际平均消费金额','预测平均消费金额')
    ax.scatter(test.avg_exp,pred,color=COLORS[0],s=35);lo=min(test.avg_exp.min(),pred.min());hi=max(test.avg_exp.max(),pred.max())
    ax.plot([lo,hi],[lo,hi],color=COLORS[2],ls='--');save(fig,out,'01_实际预测对比')
    fig,ax=canvas('留出集回归残差','预测平均消费金额','实际值−预测值')
    ax.scatter(pred,residual,color=COLORS[0]);ax.axhline(0,color=COLORS[2],ls='--');save(fig,out,'02_回归残差')
    result=test[['id','avg_exp']].assign(prediction=pred,residual=residual);table(result,out,'留出预测')
    names=model[0].get_feature_names_out();table(pd.DataFrame({'feature':names,'coefficient':model[-1].coef_}),out,'回归系数')
    assert set(train.id).isdisjoint(set(test.id))
    finish(out,rows=len(df),train_rows=len(train),test_rows=len(test),rmse=float(np.sqrt(mean_squared_error(test.avg_exp,pred))),
           r2=float(r2_score(test.avg_exp,pred)),note='教材多元回归核心段转换；不把训练拟合优度当作留出预测能力。')

if __name__=="__main__":
    main()
