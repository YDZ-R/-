# -*- coding: utf-8 -*-
import numpy as np, matplotlib, matplotlib.pyplot as plt, os, math
from matplotlib.patches import Circle, Rectangle, Wedge
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
colors=['#0070C0','#E74E69','#5BC0DE','#F5B041','#9B59B6','#1ABC9C']

# 19 南丁格尔圆饼图
fig,ax=newax(600,500)
depts=['销售部','采购部','工程部','财务部','行政部','人力部']
vals=[0.292,0.227,0.175,0.136,0.103,0.067]
cx,cy=300,260
angles=np.linspace(0,2*np.pi,len(depts),endpoint=False)
maxr=140; mv=max(vals)
for i,(a,v) in enumerate(zip(angles,vals)):
    r=v/mv*maxr
    ax.add_patch(Wedge((cx,cy),r,np.degrees(a)-15,np.degrees(a)+15,width=r,facecolor=colors[i],alpha=0.85))
    ax.text(cx+r*1.2*np.cos(a),cy+r*1.2*np.sin(a),depts[i],color='white',fontsize=11,ha='center',va='center')
ax.text(cx,40,'各部门人数占比',color='white',fontsize=20,fontweight='bold',ha='center')
ax.text(30,470,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\南丁格尔圆饼图',exist_ok=True)
plt.savefig(BASE+r'\南丁格尔圆饼图\南丁格尔圆饼图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

# 20 南丁格尔圆环图
fig,ax=newax(600,500)
ages=['[20,30)','[30,40)','[40,50)','>=50']
vals=[0.375,0.292,0.208,0.125]
cx,cy=300,260
angles=np.linspace(0,2*np.pi,len(ages),endpoint=False)
maxr=130; mv=max(vals)
for i,(a,v) in enumerate(zip(angles,vals)):
    r=v/mv*maxr
    ax.add_patch(Wedge((cx,cy),r,np.degrees(a)-20,np.degrees(a)+20,width=40,facecolor=colors[i],alpha=0.85))
ax.text(cx,cy,'年龄分布',color='white',fontsize=14,ha='center',va='center')
for i,(n,v) in enumerate(zip(ages,vals)):
    ax.text(45,100+i*28,n,color=colors[i],fontsize=12)
    ax.add_patch(Rectangle((25,94+i*28),12,12,facecolor=colors[i]))
ax.text(cx,40,'用户年龄分布（圆环）',color='white',fontsize=18,fontweight='bold',ha='center')
ax.text(30,470,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\南丁格尔圆环图',exist_ok=True)
plt.savefig(BASE+r'\南丁格尔圆环图\南丁格尔圆环图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

# 22 仪表盘图
fig,ax=newax(600,450); cx,cy,r=300,280,150
ax.add_patch(Wedge((cx,cy),r,180,360,width=25,facecolor='#2ECC71',alpha=0.6))
ax.add_patch(Wedge((cx,cy),r,180+90,360,width=25,facecolor='#F5B041',alpha=0.6))
ax.add_patch(Wedge((cx,cy),r,180+135,360,width=25,facecolor='#E74E69',alpha=0.6))
ang=math.radians(180+76*1.8)
nx,ny=cx+r*0.8*math.cos(ang),cy+r*0.8*math.sin(ang)
ax.plot([cx,nx],[cy,ny],color='white',linewidth=3)
ax.add_patch(Circle((cx,cy),8,facecolor='white'))
ax.text(cx,cy+50,'76分',color='white',fontsize=28,fontweight='bold',ha='center',va='center')
for v in [0,25,50,75,100]:
    a=math.radians(180+v*1.8)
    ax.text(cx+(r+15)*math.cos(a),cy+(r+15)*math.sin(a),str(v),color='white',fontsize=11,ha='center',va='center')
ax.text(cx,40,'季度KPI完成评分',color='white',fontsize=20,fontweight='bold',ha='center')
ax.text(30,430,'*注：数据来源于公司销售系统',color=NOTE,fontsize=11)
os.makedirs(BASE+r'\仪表盘图',exist_ok=True)
plt.savefig(BASE+r'\仪表盘图\仪表盘图_复刻.png',dpi=100,facecolor=BG,bbox_inches=None,pad_inches=0); plt.close()

print('19,20,22 done')
