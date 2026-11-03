# -*- coding: utf-8 -*-
# 第13图「对比折线图」复刻
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import os

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'
RED = '#E74E69'
NOTE = '#D9D9D9'
W, H = 867, 550

months = ['1月','2月','3月','4月','5月','6月']
v2021 = [1686, 1345, 1934, 1658, 1865, 1936]
v2022 = [1385, 1846, 1654, 1936, 2564, 2236]

X0, X1 = 120, 780
BASE_Y = 430
MAXV = 2800
PX = 320.0 / MAXV

xs = np.linspace(X0, X1, 6)
y21 = [BASE_Y - v*PX for v in v2021]
y22 = [BASE_Y - v*PX for v in v2022]

fig = plt.figure(figsize=(W/100, H/100), dpi=100)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0,0,1,1])
ax.set_xlim(0,W); ax.set_ylim(H,0); ax.set_facecolor(BG)
for s in ax.spines.values(): s.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])

# smooth lines
for ys, c, lab in [(y21, BLUE, '2021年'), (y22, RED, '2022年')]:
    xnew = np.linspace(xs[0], xs[-1], 200)
    spl = make_interp_spline(xs, ys, k=3)
    ax.plot(xnew, spl(xnew), color=c, linewidth=2, label=lab, zorder=3)
    for i in range(6):
        ax.plot(xs[i], ys[i], 'o', color=c, markersize=7, zorder=4)
        ax.text(xs[i], ys[i]-15, str([v2021,v2022][ys==y21][i] if ys is y21 else v2022[i]),
                color='white', fontsize=11, ha='center', va='bottom', zorder=5)

# legend
ax.add_patch(plt.Rectangle((120,100),12,12,facecolor=BLUE))
ax.text(138,106,'2021年',color='white',fontsize=13,va='center')
ax.add_patch(plt.Rectangle((220,100),12,12,facecolor=RED))
ax.text(238,106,'2022年',color='white',fontsize=13,va='center')

# x labels
for i,m in enumerate(months):
    ax.text(xs[i], BASE_Y+25, m, color='white', fontsize=14, ha='center')

# title
ax.text(50, 30, '2021 vs 2022 上半年销量对比', color='white',
        fontsize=26, fontweight='bold', ha='left', va='top')
ax.text(50, 75, '2022年5月销量最高达到2564', color='white', fontsize=16, ha='left', va='top')
ax.text(30, 520, '*注：数据来源于公司销售系统', color=NOTE, fontsize=11, ha='left', va='center')

out = r'D:\AAA作业\可视化作业\第二章 图表（前15）\对比折线图\对比折线图_复刻.png'
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
