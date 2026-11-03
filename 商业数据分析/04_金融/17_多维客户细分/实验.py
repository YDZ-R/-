"""多维客户细分。
教材来源：CDA 教材资料2025/4《金融数据分析和数据挖掘案例实战》/第3章-多维特征的客户细分/第3章多维特征的客户细分代码通过.ipynb
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
    from sklearn.preprocessing import QuantileTransformer,StandardScaler
    from sklearn.decomposition import FactorAnalysis
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    data,out=paths(__file__)
    bank=read_csv(data/'data_clust.csv',skipinitialspace=True)
    # 对应原单元9–21、23–34：修订错误值，家庭与爱好分开提取因子、分群。
    for c in ['interested_travel','computer_owner','HH_adults_num']:bank[c]=bank[c].fillna(bank[c].mode()[0])
    bank['HH_has_children']=bank.HH_has_children.map({'N':0,'Y':1}).fillna(0)
    bank['interested_reading']=pd.to_numeric(bank.interested_reading.replace('.','0'),errors='raise').gt(1.5).astype(int)
    interest=['interested_travel','computer_owner','interested_golf','interested_gambling','interested_reading']
    bank['interest']=bank[interest].sum(axis=1)/5
    hh=['age','marital','HH_adults_num','home_value','risk_score','HH_grandparent','HH_head_age','loan_ratio']
    hb=['HH_dieting','auto_member','interest','interested_sport']
    data_hh=StandardScaler().fit_transform(QuantileTransformer(n_quantiles=100,output_distribution='normal',random_state=SEED).fit_transform(bank[hh]))
    data_hb=StandardScaler().fit_transform(QuantileTransformer(n_quantiles=100,output_distribution='normal',random_state=SEED).fit_transform(bank[hb]))
    # 按样本数换算对数似然停止阈值，避免十余万行下绝对容差过严。
    tolerance=len(bank)*1e-5
    fa_hh=FactorAnalysis(n_components=4,rotation='varimax',svd_method='lapack',tol=tolerance,random_state=SEED,max_iter=1000).fit(data_hh)
    fa_hb=FactorAnalysis(n_components=3,rotation='varimax',svd_method='lapack',tol=tolerance,random_state=SEED,max_iter=1000).fit(data_hb)
    assert fa_hh.n_iter_<1000 and fa_hb.n_iter_<1000,'因子分析未收敛'
    score_hh=StandardScaler().fit_transform(fa_hh.transform(data_hh));score_hb=StandardScaler().fit_transform(fa_hb.transform(data_hb))
    labels_hh=KMeans(n_clusters=3,n_init=15,random_state=SEED).fit_predict(score_hh)
    labels_hb=KMeans(n_clusters=2,n_init=15,random_state=SEED).fit_predict(score_hb)
    profile=pd.DataFrame(data_hh,columns=hh).assign(cluster=labels_hh).groupby('cluster').mean()
    fig,ax=canvas('家庭维度分群的标准化画像','特征','家庭分群',size=(11,5.5))
    im=ax.imshow(profile,cmap='RdBu_r',aspect='auto',vmin=-1.5,vmax=1.5)
    ax.grid(False)
    ax.set(xticks=range(len(hh)),xticklabels=hh,yticks=range(3),yticklabels=['组0','组1','组2']);ax.tick_params(axis='x',rotation=30)
    fig.colorbar(im,ax=ax,label='变换后均值');save(fig,out,'01_家庭分群画像')
    matrix=pd.crosstab(labels_hh,labels_hb)
    fig,ax=canvas('家庭与兴趣的交叉细分','兴趣分群','家庭分群')
    im=ax.imshow(matrix,cmap='YlGnBu',aspect='auto');ax.set(xticks=range(2),xticklabels=['组0','组1'],yticks=range(3),yticklabels=['组0','组1','组2'])
    ax.grid(False)
    for i in range(3):
        for j in range(2):ax.text(j,i,str(matrix.iloc[i,j]),ha='center',va='center',color='white' if im.norm(matrix.iloc[i,j])>.55 else '#172C37')
    fig.colorbar(im,ax=ax,label='客户数');save(fig,out,'02_家庭兴趣交叉分群')
    table(profile,out,'标准化家庭画像',index=True);table(matrix,out,'交叉分群人数',index=True)
    table(pd.DataFrame({'source_row':np.arange(len(bank)),'household_cluster':labels_hh,'hobby_cluster':labels_hb}),out,'客户双维分群')
    finish(out,rows=len(bank),household_groups=3,hobby_groups=2,
           factor_iterations=[int(fa_hh.n_iter_),int(fa_hb.n_iter_)],factor_tolerance_per_observation=1e-5,
           household_silhouette=float(silhouette_score(score_hh,labels_hh,sample_size=min(1500,len(bank)),random_state=SEED)),
           note='sklearn旋转因子替代旧FactorAnalysis库；保留家庭4因子/3群、兴趣3因子/2群框架，标签不要求与教材逐一相同。')

if __name__=="__main__":
    main()
