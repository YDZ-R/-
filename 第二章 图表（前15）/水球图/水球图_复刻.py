# -*- coding: utf-8 -*-
# 第15图「水球图」复刻 完成率65%
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import os

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'
NOTE = '#D9D9D9'
W, H = 600, 500

fig = plt.figure(figsize=(W/100, H/100), dpi=100)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0,0,1,1])
ax.set_xlim(0,W); ax.set_ylim(H,0); ax.set_facecolor(BG)
for s in ax.spines.values(): s.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])

cx, cy, r = 300, 250, 120
# circle outline
circle = Circle((cx,cy), r, fill=False, edgecolor=BLUE, linewidth=3)
ax.add_patch(circle)

# wave fill: 65% filled
pct = 0.65
water_y = cy + r*(1-2*pct)  # water surface y
# clip to circle
circle_patch = Circle((cx,cy), r, facecolor=BLUE, alpha=0.7, edgecolor='none')
ax.add_patch(circle_patch)
# cover top part with bg to make water level
cover = Rectangle((cx-r, cy-r), 2*r, water_y-(cy-r), facecolor=BG, edgecolor='none')
ax.add_patch(cover)
# wave line
xw = np.linspace(cx-r, cx+r, 100)
yw = water_y + 8*np.sin((xw-cx)/r*3)
ax.plot(xw, yw, color=BLUE, linewidth=2)

# text
ax.text(cx, cy, '65%', color='white', fontsize=36, fontweight='bold', ha='center', va='center')
ax.text(cx, 50, '项目完成进度', color='white', fontsize=20, fontweight='bold', ha='center', va='center')
ax.text(30, 470, '*注：数据来源于公司销售系统', color=NOTE, fontsize=11, ha='left', va='center')

out = r'D:\AAA作业\可视化作业\第二章 图表（前15）\水球图\水球图_复刻.png'
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
