# -*- coding: utf-8 -*-
# 第12图「菱形走势图」复刻
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import os

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'
NOTE = '#D9D9D9'
W, H = 867, 550

months = ['1月','2月','3月','4月','5月','6月','7月','8月']
rate = [0.536, 0.498, 0.527, 0.708, 0.609, 0.496, 0.586, 0.704]

X0, X1 = 100, 800
BASE_Y = 420
PX = 300  # 0-1 range maps to 300px height

xs = np.linspace(X0, X1, len(months))
ys = [BASE_Y - v*PX for v in rate]

fig = plt.figure(figsize=(W/100, H/100), dpi=100)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0,0,1,1])
ax.set_xlim(0,W); ax.set_ylim(H,0); ax.set_facecolor(BG)
for s in ax.spines.values(): s.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])

# smooth line
xnew = np.linspace(xs[0], xs[-1], 300)
spl = make_interp_spline(xs, ys, k=3)
ynew = spl(xnew)
ax.plot(xnew, ynew, color=BLUE, linewidth=2, zorder=3)

# diamond markers
for i in range(len(months)):
    ax.plot(xs[i], ys[i], marker='D', markersize=9, color=BLUE, zorder=4)
    ax.text(xs[i], ys[i]-18, f'{rate[i]*100:.1f}%', color='white',
            fontsize=12, ha='center', va='bottom', zorder=5)

# x labels
for i,m in enumerate(months):
    ax.text(xs[i], BASE_Y+25, m, color='white', fontsize=14, ha='center', va='center')

# title
ax.text(50, 30, '月度销售目标完成率走势', color='white',
        fontsize=26, fontweight='bold', ha='left', va='top')
ax.text(50, 75, '4月完成率最高达到70.8%', color='white', fontsize=16, ha='left', va='top')

# note
ax.text(30, 520, '*注：数据来源于公司销售系统', color=NOTE, fontsize=11, ha='left', va='center')

out = r'D:\AAA作业\可视化作业\第二章 图表（前15）\菱形走势图\菱形走势图_复刻.png'
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
