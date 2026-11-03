# -*- coding: utf-8 -*-
import numpy as np, matplotlib, matplotlib.pyplot as plt, os
from matplotlib.patches import Rectangle, Circle
matplotlib.rcParams['font.sans-serif']=['Microsoft YaHei','SimHei']
matplotlib.rcParams['axes.unicode_minus']=False
BG='#1A1E43'; BLUE='#0070C0'; RED='#E74E69'; NOTE='#D9D9D9'
def newax(w,h):
    fig=plt.figure(figsize=(w/100,h/100),dpi=100); fig.patch.set_facecolor(BG)
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,w); ax.set_ylim(h,0); ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    return fig,ax
BASE=r'D:\AAA作业\可视化作业\第二章 图表（后15）'

# 23 柱形折线图: 柱=销量, 线=同比
fig,ax=newax(800,450)
years=['2017','2018','2019','2020','2021','2022']
sales=[1603,2106,2406,3265,3721,3921]
yoy=[27.0,31.4,14.2,35.7,14.0,5.4]
X0,X1=100,750; BASE_Y=380; PX_B=280/4000
xs=np.linspace(X0,X1,6)
for i in range(6):
    ax.add_patch(Rectangle((xs[i]-25,BASE_Y-sales[i]*PX_B),50,sales[i]*PX_B,facecolor=BLUE))
    ax.text(xs[i],BASE_Y-sales[i]*PX_B-10,str(sales[i]),color='white',fontsize=12,ha='center')
# yoy line on right axis
yoy_max=40; PX_Y=250/yoy_max
ax.plot(xs,[BASE_Y-v*PX_Y for v in yoy],color=RED,linewidth=2,marker='o',markersize=6)
for i in range(6):
    ax.text(xs[i],BASE_Y-yoy[i]*PX_Y-10,f'{yoy[i]}%',color=RED,fontsize=11,ha='center')
for i,y in enumerate(years): ax.text(xs[i],BASE_Y+25,y,color='white',fontsize=13,ha='center')
ax.text(50,30,'年度销量及同比增速',color='white',fontsize=22,fontweight='bold')
ax.text(30,430,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\柱形折线图',exist_ok=True)
plt.savefig(BASE+r'\柱形折线图\柱形折线图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

# 24 目标柱形图: 实际 vs 目标
fig,ax=newax(800,450)
items=['口红','面膜','隔离','防晒','精华','面霜']
actual=[653,523,648,856,714,785]
target=[700,500,600,900,600,600]
X0,X1=100,750; BASE_Y=380; PX=280/1000
xs=np.linspace(X0,X1,6)
for i in range(6):
    ax.add_patch(Rectangle((xs[i]-30,BASE_Y-actual[i]*PX),28,actual[i]*PX,facecolor=BLUE))
    ax.plot([xs[i]-35,xs[i]+5],[BASE_Y-target[i]*PX]*2,color='#F5B041',linewidth=2)
    ax.text(xs[i]-16,BASE_Y-actual[i]*PX-8,str(actual[i]),color='white',fontsize=11,ha='center')
for i,y in enumerate(items): ax.text(xs[i],BASE_Y+25,y,color='white',fontsize=13,ha='center')
ax.text(50,30,'商品实际销量vs目标',color='white',fontsize=22,fontweight='bold')
ax.text(30,430,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\目标柱形图',exist_ok=True)
plt.savefig(BASE+r'\目标柱形图\目标柱形图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

# 25 子弹图
fig,ax=newax(800,450)
items=['口红','面膜','隔离','防晒','精华','面霜']
actual=[653,523,648,856,714,785]
target=[700,500,600,900,600,600]
scale=1000; PX=500/scale
for i,(it,a,t) in enumerate(zip(items,actual,target)):
    y=70+i*55
    ax.add_patch(Rectangle((200,y),scale*PX,20,facecolor='#2A2E55'))
    ax.add_patch(Rectangle((200,y),600*PX,20,facecolor='#444866'))
    ax.add_patch(Rectangle((200,y),800*PX,20,facecolor='#555977'))
    ax.add_patch(Rectangle((200,y),a*PX,20,facecolor=BLUE))
    ax.plot([200+t*PX,200+t*PX],[y-3,y+23],color='#F5B041',linewidth=2)
    ax.text(190,y+10,it,color='white',fontsize=13,ha='right',va='center')
ax.text(50,30,'商品销量子弹图',color='white',fontsize=22,fontweight='bold')
ax.text(30,430,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\子弹图',exist_ok=True)
plt.savefig(BASE+r'\子弹图\子弹图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

# 26 柱形圆 (条形+圆形标记)
fig,ax=newax(800,450)
regions=['华北','华南','东北','西北','西南','华东']
vals=[2354,1902,3524,2698,2896,2563]
yoy=[12,25,16,21,18,25]
maxv=4500; PX=500/maxv
for i,(r,v,g) in enumerate(zip(regions,vals,yoy)):
    y=70+i*55
    ax.add_patch(Rectangle((180,y),v*PX,25,facecolor=BLUE))
    ax.add_patch(Circle((180+v*PX+20,y+12),8,facecolor='#F5B041'))
    ax.text(170,y+12,r,color='white',fontsize=13,ha='right',va='center')
    ax.text(180+v*PX+35,y+12,f'+{g}%',color='#F5B041',fontsize=12,va='center')
ax.text(50,30,'各区域销量及同比',color='white',fontsize=22,fontweight='bold')
ax.text(30,430,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\柱形圆',exist_ok=True)
plt.savefig(BASE+r'\柱形圆\柱形圆_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

print('23-26 done')
