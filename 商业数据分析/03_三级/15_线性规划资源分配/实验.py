"""线性规划资源分配。
教材来源：CDA 教材资料2025/3《CDA 三级认证教材：敏捷数据挖掘》/4.2运筹优化/4.2.1线性规划.ipynb
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
    from scipy.optimize import linprog
    data,out=paths(__file__)
    source=(data/'productivity.lp').read_text(encoding='utf-8')
    # 原笔记本通过CPLEX读取lp；系数原样迁移到SciPy HiGHS，不依赖商业授权。
    assert '50 x1 + 100 x2' in source and '2 x1 + x2 <= 400' in source
    profit=np.array([50.,100.]);A=np.array([[1.,1.],[2.,1.],[0.,1.]])
    capacity=np.array([300.,400.,250.])
    result=linprog(-profit,A_ub=A,b_ub=capacity,bounds=[(0,None),(0,None)],method='highs')
    assert result.success,result.message
    x=result.x;use=A@x
    assert np.all(use<=capacity+1e-8) and np.all(x>=0) and np.isclose(profit@x,27500)
    fig,ax=canvas('生产资源分配的可行域','产品 x1 数量','产品 x2 数量')
    vertices=np.array([[0,0],[200,0],[100,200],[50,250],[0,250]])
    ax.fill(vertices[:,0],vertices[:,1],color=COLORS[1],alpha=.4,label='可行域')
    grid=np.linspace(0,210,200)
    ax.plot(grid,300-grid,label='x1+x2≤300');ax.plot(grid,400-2*grid,label='2x1+x2≤400')
    ax.axhline(250,color=COLORS[2],label='x2≤250');ax.scatter(*x,color='#B35F47',s=90,zorder=5,label='最优解')
    ax.set(xlim=(0,210),ylim=(0,330));ax.legend(fontsize=9);save(fig,out,'01_线性规划可行域')
    fig,ax=canvas('最优方案的资源使用','约束编号','资源数量')
    pd.DataFrame({'使用量':use,'上限':capacity},index=['约束1','约束2','约束3']).plot.bar(ax=ax,color=COLORS[:2],rot=0)
    save(fig,out,'02_约束资源使用')
    table(pd.DataFrame({'constraint':['r1','r2','r3'],'used':use,'capacity':capacity,'slack':capacity-use,'marginal_profit':-result.ineqlin.marginals}),out,'约束与影子价格')
    finish(out,x1=float(x[0]),x2=float(x[1]),maximum_profit=float(profit@x),slack=(capacity-use).tolist(),
           note='教材模型是连续线性规划，不额外声称存在整数批量或现实生产约束。')

if __name__=="__main__":
    main()
