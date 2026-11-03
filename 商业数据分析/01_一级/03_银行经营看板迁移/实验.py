"""银行经营看板迁移。
教材来源：CDA 教材资料2025/1《CDA 一级认证教材：商业数据分析》/第5章 业务数据分析/第5章  PowerBI业务看板案例-银行案例/银行案例数据 - 学员用.xlsx
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
    file=data/'银行案例数据 - 学员用.xlsx'
    df=pd.read_excel(file,sheet_name='销售数据')
    product=pd.read_excel(file,sheet_name='品类说明表')
    df=df.merge(product,on='品类编号',how='left',validate='many_to_one')
    assert df['品类名称'].notna().all()
    sales=float(df['购买金额'].sum());target=25_000_000;day=29;days=31
    groups=df.groupby('品类名称')['购买金额'].sum().sort_values()
    fig,ax=canvas('银行产品购买金额','购买金额（万元）','',size=(10,6))
    ax.barh(groups.index,groups.values/10000,color=COLORS[0]);save(fig,out,'01_产品销售结构')
    fig,axes=plt.subplots(1,2,figsize=(11,5))
    axes[0].bar(['截至29日','月度目标'],[sales/10000,target/10000],color=COLORS[:2]);axes[0].set(title='月度目标进度',ylabel='购买金额（万元）')
    matrix=df.pivot_table(index='年龄',columns='风险编号',values='购买金额',aggfunc='sum',fill_value=0)/10000
    im=axes[1].imshow(matrix,cmap='YlGnBu',aspect='auto');axes[1].set(title='年龄与风险偏好',xticks=range(len(matrix.columns)),xticklabels=matrix.columns,yticks=range(len(matrix)),yticklabels=matrix.index)
    fig.colorbar(im,ax=axes[1],label='购买金额（万元）');save(fig,out,'02_目标与客群')
    applications=pd.read_excel(data/'归因分析数据.xlsx',sheet_name='贷款申请表')
    channels=applications['申请渠道'].value_counts().rename_axis('channel').to_frame('applications')
    table(groups.to_frame('amount'),out,'产品销售汇总',index=True);table(matrix,out,'年龄风险矩阵',index=True);table(channels,out,'贷款渠道汇总',index=True)
    remaining=max(0,target-sales)
    finish(out,purchase_records=len(df),sales=sales,target=target,achievement=sales/target,
           linear_pace_estimate=sales/day*days,required_daily_for_remaining_days=remaining/(days-day),
           application_rows=len(applications),note='线性进度只是情景测算；贷款申请与理财销售没有可核验主键，分别汇总。')

if __name__=="__main__":
    main()
