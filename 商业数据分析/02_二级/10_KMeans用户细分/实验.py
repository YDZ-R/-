"""KMeans用户细分。
教材来源：CDA 教材资料2025/2《CDA 二级认证教材：量化策略分析》/第9章-用户分群/k-means聚类/Kmeans 的应用 - 用户细分.ipynb
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
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    data,out=paths(__file__)
    df=read_csv(data/'profile_bank.csv');cols=['CNT_TBM','CNT_ATM','CNT_POS','CNT_CSC']
    # 对应原单元0–3、13–24；保留降维后分群，用sklearn替代旧因子库。
    z=StandardScaler().fit_transform(df[cols]);pca=PCA(n_components=3,whiten=True).fit(z);scores=pca.transform(z)
    model=KMeans(n_clusters=3,n_init=20,random_state=SEED).fit(scores)
    labels=model.labels_;profile=df.assign(cluster=labels).groupby('cluster')[cols].mean()
    fig,ax=canvas('银行用户行为分群','PC1（白化）','PC2（白化）')
    rng=np.random.default_rng(SEED);idx=rng.choice(len(df),size=min(5000,len(df)),replace=False)
    for k in range(3):
        sel=idx[labels[idx]==k];ax.scatter(scores[sel,0],scores[sel,1],s=8,alpha=.3,label=f'组{k}')
    ax.legend();save(fig,out,'01_用户分群投影')
    fig,ax=canvas('各群的渠道使用次数','业务渠道','群体均值（次）')
    profile.T.plot.bar(ax=ax,color=COLORS[:3],rot=0);ax.legend(title='分群');save(fig,out,'02_渠道画像')
    table(df.assign(cluster=labels),out,'客户分群');table(profile,out,'渠道画像',index=True)
    sil=float(silhouette_score(scores,labels,sample_size=min(2000,len(df)),random_state=SEED))
    finish(out,rows=len(df),k=3,seed=SEED,silhouette_sample=sil,pca_retained_ratio=float(pca.explained_variance_ratio_.sum()),
           cluster_sizes={str(k):int(v) for k,v in pd.Series(labels).value_counts().sort_index().items()},
           note='保留教材3群设定；PCA近似旧因子得分，不声称标签逐个一致。')

if __name__=="__main__":
    main()
