"""银行交叉销售关联规则。
教材来源：CDA 教材资料2025/3《CDA 三级认证教材：敏捷数据挖掘》/2.4交叉销售（关联规则与序列模式）/2.4.1.关联规则（银行产品交叉销售分析）.ipynb
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
    from itertools import combinations
    data,out=paths(__file__)
    df=read_csv(data/'bank_prod_order.csv')
    baskets=df.groupby('CSR_ID').PROD.apply(lambda x:frozenset(x.dropna()))
    products=sorted(set().union(*baskets));n=len(baskets);minimum=.02
    # 对应原单元1–7。实现完整Apriori，支持度分母是客户购物篮数。
    supports={};previous=set()
    for p in products:
        item=frozenset([p]);support=sum(item<=b for b in baskets)/n
        if support>=minimum:supports[item]=support;previous.add(item)
    k=2
    while previous:
        candidates={a|b for a in previous for b in previous if len(a|b)==k}
        candidates={s for s in candidates if all(frozenset(t) in previous for t in combinations(s,k-1))}
        current=set()
        for item in sorted(candidates,key=lambda s:tuple(sorted(s))):
            support=sum(item<=b for b in baskets)/n
            if support>=minimum:supports[item]=support;current.add(item)
        previous=current;k+=1
    rules=[]
    for item,support in supports.items():
        if len(item)<2:continue
        for size in range(1,len(item)):
            for combo in combinations(sorted(item),size):
                lhs=frozenset(combo);rhs=item-lhs;conf=support/supports[lhs];lift=conf/supports[rhs]
                if conf>.1 and lift>1:
                    rules.append(dict(antecedent=' + '.join(sorted(lhs)),consequent=' + '.join(sorted(rhs)),support=support,confidence=conf,lift=lift))
    rules=pd.DataFrame(rules).sort_values(['lift','support','antecedent'],ascending=[False,False,True])
    fig,ax=canvas('交叉销售规则的强度','提升度 lift','支持度（%）')
    sc=ax.scatter(rules.lift,rules.support*100,c=rules.confidence,cmap='viridis',s=35,alpha=.7)
    fig.colorbar(sc,ax=ax,label='置信度');save(fig,out,'01_关联规则分布')
    top=rules.head(8).sort_values('lift');labels=top.antecedent+' → '+top.consequent
    fig,ax=canvas('提升度最高的八条规则','提升度 lift','',size=(11,6))
    ax.barh(labels,top.lift,color=COLORS[0]);save(fig,out,'02_交叉销售规则')
    assert rules.support.between(0,1).all() and rules.confidence.between(0,1).all()
    table(rules,out,'关联规则')
    finish(out,transactions=n,products=len(products),minimum_support=minimum,frequent_itemsets=len(supports),rules=len(rules),
           highest_lift=float(rules.lift.max()),note='同一客户重复购买同一产品只记一次；关联规则不代表购买因果关系。')

if __name__=="__main__":
    main()
