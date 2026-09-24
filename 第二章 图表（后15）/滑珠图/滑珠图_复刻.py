# -*- coding: utf-8 -*-
import numpy as np, matplotlib, matplotlib.pyplot as plt, os
from matplotlib.patches import Rectangle, Circle
matplotlib.rcParams['font.sans-serif']=['Microsoft YaHei','SimHei']
matplotlib.rcParams['axes.unicode_minus']=False
BG='#1A1E43'; BLUE='#0070C0'; LBLUE='#82ADD7'; RED='#E74E69'; NOTE='#D9D9D9'
def newax(w,h):
    fig=plt.figure(figsize=(w/100,h/100),dpi=100); fig.patch.set_facecolor(BG)
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,w); ax.set_ylim(h,0); ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    return fig,ax
BASE=r'D:\AAA作业\可视化作业\第二章 图表（后15）'

# 27 簇状柱形折线图
fig,ax=newax(800,450)
regions=['华北','华南','东北','西北','西南','华东']
v22=[2354,1902,3524,2698,2896,2563]
v21=[2021,1563,3213,2531,2631,2361]
yoy=[16,22,10,7,10,9]
X0,X1=120,750; BASE_Y=380; PX=280/4000
xs=np.linspace(X0,X1,6)
for i in range(6):
    ax.add_patch(Rectangle((xs[i]-30,BASE_Y-v22[i]*PX),25,v22[i]*PX,facecolor=BLUE))
    ax.add_patch(Rectangle((xs[i]+5,BASE_Y-v21[i]*PX),25,v21[i]*PX,facecolor=LBLUE))
ax.plot(xs,[BASE_Y-v*3 for v in yoy],color=RED,linewidth=2,marker='o',markersize=6)
for i,y in enumerate(regions): ax.text(xs[i],BASE_Y+25,y,color='white',fontsize=13,ha='center')
ax.text(50,30,'各区域销量对比及同比',color='white',fontsize=22,fontweight='bold')
ax.text(30,430,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\簇状柱形折线图',exist_ok=True)
plt.savefig(BASE+r'\簇状柱形折线图\簇状柱形折线图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

# 28 复合柱形图: 月度细柱+季度粗背景
fig,ax=newax(850,450)
months=['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月']
monthly=[2354,1902,3524,2698,2896,2563,3156,2896,3621,2635]
quarter=[7780,7780,7780,8157,8157,8157,9673,9673,9673,8387]
BASE_Y=380; PX=280/10000; X0=100; gap=65
# quarter background blocks
ax.add_patch(Rectangle((X0,100),3*gap,280,facecolor='#2A2E55',alpha=0.5))
ax.add_patch(Rectangle((X0+3*gap,100),3*gap,280,facecolor='#333860',alpha=0.5))
ax.add_patch(Rectangle((X0+6*gap,100),3*gap,280,facecolor='#2A2E55',alpha=0.5))
for i in range(10):
    x=X0+i*gap+15
    ax.add_patch(Rectangle((x,BASE_Y-monthly[i]*PX),30,monthly[i]*PX,facecolor=BLUE))
    ax.text(x+15,BASE_Y+20,months[i],color='white',fontsize=12,ha='center')
ax.text(50,30,'月度及季度销量复合图',color='white',fontsize=22,fontweight='bold')
ax.text(30,430,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\复合柱形图',exist_ok=True)
plt.savefig(BASE+r'\复合柱形图\复合柱形图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

# 29 滑珠图
fig,ax=newax(700,400)
regions=['华东','西北','东北','华北','华南']
rate=[35,51,62,74,86]
for i,(r,v) in enumerate(zip(regions,rate)):
    y=80+i*50
    ax.add_patch(Rectangle((180,y),400,12,facecolor='#2A2E55'))
    ax.add_patch(Circle((180+v*4,y+6),10,facecolor=BLUE))
    ax.text(170,y+6,r,color='white',fontsize=14,ha='right',va='center')
    ax.text(600,y+6,f'{v}%',color='white',fontsize=13,va='center')
ax.text(50,30,'各区域目标完成率',color='white',fontsize=22,fontweight='bold')
ax.text(30,380,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\滑珠图',exist_ok=True)
plt.savefig(BASE+r'\滑珠图\滑珠图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

# 30 对比滑珠图
fig,ax=newax(700,400)
regions=['华东','西北','东北','华北','华南']
r22=[35,51,62,74,86]; r21=[45,39,53,69,92]
for i in range(5):
    y=80+i*50
    ax.add_patch(Rectangle((180,y),400,10,facecolor='#2A2E55'))
    ax.add_patch(Circle((180+r22[i]*4,y+5),8,facecolor=BLUE))
    ax.add_patch(Circle((180+r21[i]*4,y+5),8,facecolor=LBLUE))
    ax.text(170,y+5,regions[i],color='white',fontsize=14,ha='right',va='center')
ax.text(50,30,'各区域完成率对比（2021 vs 2022）',color='white',fontsize=20,fontweight='bold')
ax.add_patch(Rectangle((180,30),10,10,facecolor=BLUE)); ax.text(195,35,'2022',color='white',fontsize=12,va='center')
ax.add_patch(Rectangle((260,30),10,10,facecolor=LBLUE)); ax.text(275,35,'2021',color='white',fontsize=12,va='center')
ax.text(30,380,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\对比滑珠图',exist_ok=True)
plt.savefig(BASE+r'\对比滑珠图\对比滑珠图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

print('27-30 done')
