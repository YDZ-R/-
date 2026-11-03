# -*- coding: utf-8 -*-
# 第14图「单值圆环图」复刻 完成率85%
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import os

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'
GRAY = '#2A2E55'
NOTE = '#D9D9D9'
W, H = 600, 500

fig = plt.figure(figsize=(W/100, H/100), dpi=100)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0,0,1,1])
ax.set_xlim(0,W); ax.set_ylim(H,0); ax.set_facecolor(BG)
for s in ax.spines.values(): s.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])

cx, cy, r = 300, 250, 130
# background ring
ax.add_patch(Wedge((cx,cy), r, 0, 360, width=30, facecolor=GRAY, edgecolor='none'))
# progress ring: 85% = 306 degrees
pct = 85
angle = pct * 3.6
ax.add_patch(Wedge((cx,cy), r, 90-angle, 90, width=30, facecolor=BLUE, edgecolor='none'))

# center text
ax.text(cx, cy-10, '85%', color='white', fontsize=36, fontweight='bold', ha='center', va='center')
ax.text(cx, cy+30, '完成率', color='white', fontsize=16, ha='center', va='center')

# title
ax.text(cx, 50, '2022年Q1销售目标完成率', color='white',
        fontsize=20, fontweight='bold', ha='center', va='center')
ax.text(30, 470, '*注：数据来源于公司销售系统', color=NOTE, fontsize=11, ha='left', va='center')

out = r'D:\AAA作业\可视化作业\第二章 图表（前15）\单值圆环图\单值圆环图_复刻.png'
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
