"""共享的文件与绘图工具；各实验的业务计算保留在各自的实验.py中。"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

SEED=241
COLORS=['#277D8E','#80BABB','#E6A18C','#8196C2','#C3AF74']
fonts={f.name for f in font_manager.fontManager.ttflist}
font=next((f for f in ['Microsoft YaHei','SimHei','Noto Sans CJK SC','Noto Sans SC'] if f in fonts),'DejaVu Sans')
plt.rcParams.update({'font.family':font,'axes.unicode_minus':False,'font.size':11,
                     'axes.spines.top':False,'axes.spines.right':False,
                     'axes.titleweight':'bold','axes.titlesize':15,'axes.titlepad':16,
                     'axes.labelcolor':'#334A54','text.color':'#243F4B',
                     'axes.prop_cycle':matplotlib.cycler(color=COLORS)})

def paths(script):
    lab=Path(script).resolve().parent
    out=lab/'outputs';out.mkdir(exist_ok=True)
    return lab/'data',out

def read_csv(path,**kwargs):
    for encoding in ['utf-8-sig','gb18030']:
        try:return pd.read_csv(path,encoding=encoding,**kwargs)
        except UnicodeDecodeError:continue
    raise ValueError(f'无法识别数据编码：{path}')

def canvas(title,xlabel='',ylabel='',size=(9,5.5)):
    fig,ax=plt.subplots(figsize=size)
    ax.set(title=title,xlabel=xlabel,ylabel=ylabel)
    ax.grid(axis='y',color='#E4ECEE',linewidth=.6);ax.set_axisbelow(True)
    return fig,ax

def save(fig,out,name):
    fig.tight_layout(pad=1.4)
    fig.savefig(out/f'{name}.png',dpi=200,facecolor='white',bbox_inches='tight')
    plt.close(fig)

def table(df,out,name,index=False):
    df.to_csv(out/f'{name}.csv',index=index,encoding='utf-8-sig')

def finish(out,**values):
    def convert(v):
        if isinstance(v,np.generic):return v.item()
        if isinstance(v,Path):return str(v)
        raise TypeError(type(v).__name__)
    text=json.dumps(values,ensure_ascii=False,indent=2,default=convert,allow_nan=False)
    (out/'results.json').write_text(text,encoding='utf-8')
    print(text)

def classification_plots(y,prob,out,title,threshold=.5):
    """统一画测试集ROC、概率分布，阈值固定，不拿测试集选择阈值。"""
    from sklearn.metrics import roc_curve,roc_auc_score,average_precision_score,confusion_matrix,precision_score,recall_score
    y=np.asarray(y);prob=np.asarray(prob);pred=(prob>=threshold).astype(int)
    assert len(y)==len(prob) and np.isfinite(prob).all()
    fpr,tpr,_=roc_curve(y,prob)
    auc=float(roc_auc_score(y,prob))
    fig,ax=canvas(title+'：留出集ROC','假阳性率','真阳性率')
    ax.plot(fpr,tpr,lw=2.3,label=f'AUC = {auc:.3f}');ax.plot([0,1],[0,1],color='#ABB7BC',ls='--')
    ax.legend();save(fig,out,'01_ROC曲线')
    fig,ax=canvas(title+'：预测概率分布','预测为正类的概率','组内密度')
    for cls,color in [(0,COLORS[0]),(1,COLORS[2])]:
        ax.hist(prob[y==cls],bins=np.linspace(0,1,21),density=True,alpha=.55,label=f'实际类别 {cls}',color=color)
    ax.axvline(threshold,color='#687D87',ls='--',label=f'展示阈值 {threshold:g}')
    ax.legend();save(fig,out,'02_预测概率分布')
    table(pd.DataFrame(confusion_matrix(y,pred),index=['实际0','实际1'],columns=['预测0','预测1']),out,'混淆矩阵',index=True)
    return dict(test_rows=len(y),positive_rows=int(y.sum()),auc=auc,
                average_precision=float(average_precision_score(y,prob)),threshold=threshold,
                precision=float(precision_score(y,pred,zero_division=0)),recall=float(recall_score(y,pred,zero_division=0)),
                ks=float((tpr-fpr).max()))
