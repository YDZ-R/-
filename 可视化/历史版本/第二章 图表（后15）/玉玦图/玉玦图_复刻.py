# -*- coding: utf-8 -*-
import numpy as np, matplotlib, matplotlib.pyplot as plt, os
from matplotlib.patches import Circle, Rectangle, Wedge, FancyArrow
matplotlib.rcParams['font.sans-serif']=['Microsoft YaHei','SimHei']
matplotlib.rcParams['axes.unicode_minus']=False
BG='#1A1E43'; BLUE='#0070C0'; NOTE='#D9D9D9'
def newax(w,h):
    fig=plt.figure(figsize=(w/100,h/100),dpi=100); fig.patch.set_facecolor(BG)
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,w); ax.set_ylim(h,0); ax.set_facecolor(BG)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    return fig,ax
BASE=r'D:\AAA作业\可视化作业\第二章 图表（后15）'

# 16 波浪水球图
fig,ax=newax(600,500); cx,cy,r=300,250,120
ax.add_patch(Circle((cx,cy),r,fill=False,edgecolor=BLUE,linewidth=3))
ax.add_patch(Circle((cx,cy),r,facecolor=BLUE,alpha=0.7,edgecolor='none'))
pct=0.65; wy=cy+r*(1-2*pct)
ax.add_patch(Rectangle((cx-r,cy-r),2*r,wy-(cy-r),facecolor=BG,edgecolor='none'))
xw=np.linspace(cx-r,cx+r,100); yw=wy+8*np.sin((xw-cx)/r*4)
ax.plot(xw,yw,color=BLUE,linewidth=2)
ax.text(cx,cy,'65%',color='white',fontsize=36,fontweight='bold',ha='center',va='center')
ax.text(cx,50,'项目完成进度',color='white',fontsize=20,fontweight='bold',ha='center')
ax.text(30,470,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\波浪水球图',exist_ok=True)
plt.savefig(BASE+r'\波浪水球图\波浪水球图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

# 17 玉玦图 (环形分段)
fig,ax=newax(600,500); cx,cy,r=300,250,100
data=[('[20,30)',0.375,'#0070C0'),('[30,40)',0.292,'#E74E69'),('[40,50)',0.208,'#5BC0DE'),('>=50',0.125,'#F5B041')]
start=90
for name,v,c in data:
    ang=v*360
    ax.add_patch(Wedge((cx,cy),r,start-ang,start,width=25,facecolor=c,edgecolor='none'))
    start-=ang
ax.text(cx,cy,'用户年龄分布',color='white',fontsize=14,ha='center',va='center')
for i,(name,v,c) in enumerate(data):
    ax.text(50,100+i*30,name,color=c,fontsize=13,va='center')
    ax.add_patch(Rectangle((30,93+i*30),12,12,facecolor=c))
ax.text(30,470,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\玉玦图',exist_ok=True)
plt.savefig(BASE+r'\玉玦图\玉玦图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

# 18 跑道图 (水平跑道+进度)
fig,ax=newax(800,450)
depts=['销售部','采购部','工程部','财务部','行政部','人力部']
vals=[451,326,293,238,226,130]
maxv=702
for i,(d,v) in enumerate(zip(depts,vals)):
    y=80+i*55
    ax.add_patch(Rectangle((180,y),500,25,facecolor='#2A2E55'))
    ax.add_patch(Rectangle((180,y),500*v/maxv,25,facecolor=BLUE))
    ax.text(170,y+12,d,color='white',fontsize=14,ha='right',va='center')
    ax.text(690,y+12,str(v),color='white',fontsize=13,va='center')
ax.text(40,30,'各部门人数对比',color='white',fontsize=24,fontweight='bold')
ax.text(30,430,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\跑道图',exist_ok=True)
plt.savefig(BASE+r'\跑道图\跑道图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

print('16-18 done')
