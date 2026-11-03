"""银行交易网络。
教材来源：CDA 教材资料2025/4《金融数据分析和数据挖掘案例实战》/补充-社交网络/05-社交网络—银行交易圈实践-社区发现 .ipynb
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
    import networkx as nx
    data,out=paths(__file__)
    df=read_csv(data/'Archive-社交网络-交易对手明细汇总.csv')
    # 对应原单元2–12：保留教材无向交易关系，用NetworkX内置Louvain替代旧community包。
    edges=df[['源客户号','目标客户号']].dropna().drop_duplicates()
    graph=nx.from_pandas_edgelist(edges,'源客户号','目标客户号',create_using=nx.Graph)
    graph.remove_edges_from(list(nx.selfloop_edges(graph)))
    communities=nx.community.louvain_communities(graph,seed=SEED,weight=None)
    partition={node:i for i,group in enumerate(communities) for node in group}
    sizes=pd.Series([len(c) for c in communities]).sort_values(ascending=False)
    fig,ax=canvas('交易网络的社区规模','按规模排列的社区','节点数')
    ax.bar(np.arange(1,len(sizes)+1),sizes,color=COLORS[0]);save(fig,out,'01_社区规模')
    largest=graph.subgraph(max(nx.connected_components(graph),key=len))
    nodes=sorted(largest,key=lambda n:(-largest.degree(n),str(n)))[:120]
    view=largest.subgraph(nodes)
    fig,ax=canvas('最大连通分量中的核心节点','','',size=(10,7))
    pos=nx.spring_layout(view,seed=SEED)
    nx.draw_networkx_edges(view,pos,ax=ax,alpha=.22,width=.6,edge_color='#81949F')
    nx.draw_networkx_nodes(view,pos,ax=ax,node_size=[15+3*view.degree(n) for n in view],node_color=[partition[n] for n in view],cmap='tab20')
    ax.set_axis_off();save(fig,out,'02_交易社区网络')
    pagerank=nx.pagerank(graph,alpha=.85)
    metrics=pd.DataFrame([dict(node=n,community=partition[n],degree=graph.degree(n),pagerank=pagerank[n]) for n in sorted(graph)])
    table(metrics,out,'节点与社区指标')
    assert sum(len(c) for c in communities)==graph.number_of_nodes() and np.isclose(sum(pagerank.values()),1)
    finish(out,raw_rows=len(df),nodes=graph.number_of_nodes(),edges=graph.number_of_edges(),communities=len(communities),
           connected_components=nx.number_connected_components(graph),largest_component_nodes=len(largest),
           modularity=float(nx.community.modularity(graph,communities)),displayed_nodes=len(view),
           note='全图计算社区与PageRank，网络图仅展示最大连通分量中度数前120的诱导子图；不把社区直接标记为欺诈团伙。')

if __name__=="__main__":
    main()
