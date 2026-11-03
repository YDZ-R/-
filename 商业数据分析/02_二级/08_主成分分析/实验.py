"""主成分分析。
教材来源：CDA 教材资料2025/2《CDA 二级认证教材：量化策略分析》/第7章-特征降维方法/在 Python 中实现主成分分析.ipynb
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
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    data,out=paths(__file__)
    df=read_csv(data/'profile_telecom.csv');cols=['cnt_call','cnt_msg','cnt_wei','cnt_web']
    # 对应原单元3–7：标准化、白化PCA、方差贡献和得分。
    z=StandardScaler().fit_transform(df[cols])
    full=PCA().fit(z);pca=PCA(n_components=2,whiten=True).fit(z);scores=pca.transform(z)
    fig,ax=canvas('电信行为主成分的方差贡献','主成分','解释方差比例')
    ax.bar(range(1,5),full.explained_variance_ratio_,color=COLORS[1]);ax.plot(range(1,5),full.explained_variance_ratio_.cumsum(),'o-',color=COLORS[0],label='累计比例')
    ax.set_xticks(range(1,5));ax.legend();save(fig,out,'01_主成分贡献率')
    fig,ax=canvas('用户行为的二维主成分投影','PC1（白化得分）','PC2（白化得分）')
    sc=ax.scatter(scores[:,0],scores[:,1],c=df.cnt_web,s=23,alpha=.7,cmap='viridis')
    fig.colorbar(sc,ax=ax,label='上网次数');save(fig,out,'02_PCA客户投影')
    loading=pd.DataFrame(pca.components_.T,index=cols,columns=['PC1','PC2'])
    table(loading,out,'主成分系数',index=True);table(pd.DataFrame(scores,columns=['PC1','PC2']).assign(ID=df.ID),out,'主成分得分')
    assert np.isclose(full.explained_variance_ratio_.sum(),1)
    finish(out,rows=len(df),features=cols,explained_ratio=pca.explained_variance_ratio_.tolist(),
           cumulative_two=float(pca.explained_variance_ratio_.sum()),note='PCA轴的正负号可整体翻转，不代表业务方向发生变化。')

if __name__=="__main__":
    main()
