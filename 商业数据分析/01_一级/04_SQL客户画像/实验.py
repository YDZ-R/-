"""SQL客户画像。
教材来源：CDA 教材资料2025/1《CDA 一级认证教材：商业数据分析》/第9章 用户标签体系与用户画像专题/data/accounts.csv
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
    import sqlite3
    data,out=paths(__file__)
    # 将教材MySQL关系模型迁移到Python内置SQLite，不依赖本地数据库账号。
    with sqlite3.connect(':memory:') as conn:
        for name in ['accounts','clients','disp','loans','district']:
            frame=read_csv(data/f'{name}.csv');frame.to_sql(name,conn,index=False)
        query="""SELECT c.client_id,c.sex,c.birth_date,c.district_id,
                  COUNT(DISTINCT d.account_id) AS accounts,
                  COUNT(DISTINCT l.loan_id) AS loans
                  FROM clients c LEFT JOIN disp d ON c.client_id=d.client_id AND d.type='所有者'
                  LEFT JOIN loans l ON d.account_id=l.account_id
                  GROUP BY c.client_id,c.sex,c.birth_date,c.district_id"""
        profile=pd.read_sql_query(query,conn)
    births=pd.to_datetime(profile.birth_date)
    reference=pd.Timestamp('1998-12-31')
    profile['age']=((reference-births).dt.days/365.2425).astype(int)
    profile['age_band']=pd.cut(profile.age,[0,30,45,60,100],labels=['30岁及以下','31–45岁','46–60岁','60岁以上'])
    assert profile.client_id.is_unique
    summary=profile.groupby('age_band',observed=True).agg(customers=('client_id','size'),loan_holders=('loans',lambda x:int(x.gt(0).sum())))
    fig,ax=canvas('教材客户年龄结构','年龄段','客户数')
    ax.bar(summary.index.astype(str),summary.customers,color=COLORS[0]);save(fig,out,'01_年龄结构')
    sex=pd.crosstab(profile.age_band,profile.sex,normalize='index')*100
    fig,ax=canvas('年龄段内的性别构成','年龄段','组内占比（%）')
    sex.plot.bar(stacked=True,ax=ax,color=COLORS[:2],rot=0);ax.set_xlabel('年龄段');ax.legend(title='性别');save(fig,out,'02_客户结构')
    table(profile,out,'客户画像宽表');table(summary,out,'年龄分组',index=True)
    (out/'画像查询.sql').write_text(query,encoding='utf-8')
    finish(out,customers=len(profile),owners=int(profile.accounts.gt(0).sum()),loan_holders=int(profile.loans.gt(0).sum()),
           age_reference=str(reference.date()),note='画像采用教材历史截止日；不将关系表连接后的重复行当作独立客户。')

if __name__=="__main__":
    main()
