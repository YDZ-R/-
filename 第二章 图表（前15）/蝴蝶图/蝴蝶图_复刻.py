# -*- coding: utf-8 -*-
# 第6图「蝴蝶图」复刻 数据来源：《第二章 图表(前15).xlsx》工作表 '6 蝴蝶图'
# 华南2238/2066 华北1531/1436 东北1426/1531 西北1321/1265 华东1215/1003
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'
RED = '#E74E69'
NOTE = '#D9D9D9'

W, H = 867, 612
PX_PER_VAL = 0.102

regions = ['华南', '华北', '东北', '西北', '华东']
v2022 = [2238, 1531, 1426, 1321, 1215]
v2021 = [2066, 1436, 1531, 1265, 1003]

# bar geometry
BLUE_RIGHT = 383   # blue bars end here (center divider)
RED_LEFT = 509     # red bars start here (center divider)
BAR_H = 29
row_cy = [210, 284, 357, 430, 504]  # bar center y

fig = plt.figure(figsize=(W/100, H/100), dpi=100)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.set_facecolor(BG)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

# bars
for i in range(5):
    cy = row_cy[i]
    ytop = cy - BAR_H/2
    # blue bar: from BLUE_RIGHT leftwards
    bw = v2022[i] * PX_PER_VAL
    ax.add_patch(Rectangle((BLUE_RIGHT - bw, ytop), bw, BAR_H,
                           facecolor=BLUE, edgecolor='none', zorder=3))
    # red bar: from RED_LEFT rightwards
    rw = v2021[i] * PX_PER_VAL
    ax.add_patch(Rectangle((RED_LEFT, ytop), rw, BAR_H,
                           facecolor=RED, edgecolor='none', zorder=3))

# bar numbers (white, inside bars at outer end)
for i in range(5):
    cy = row_cy[i]
    bw = v2022[i] * PX_PER_VAL
    ax.text(BLUE_RIGHT - bw + 8, cy, str(v2022[i]), color='white',
            fontsize=13, ha='left', va='center', zorder=5)
    rw = v2021[i] * PX_PER_VAL
    ax.text(RED_LEFT + rw - 8, cy, str(v2021[i]), color='white',
            fontsize=13, ha='right', va='center', zorder=5)

# region names (center column)
for i in range(5):
    ax.text(446, row_cy[i], regions[i], color='white',
            fontsize=15, ha='center', va='center', zorder=5)

# top year labels
ax.text(320, 171, '2022', color=BLUE, fontsize=15, ha='center', va='center', zorder=5)
ax.text(536, 171, '2021', color=RED, fontsize=15, ha='center', va='center', zorder=5)

# title
ax.text(58, 46, '2022年上半年各区域对比去年销量', color='white',
        fontsize=28, fontweight='bold', ha='left', va='top', zorder=5)

# subtitle
ax.text(57, 104, '2022年整体销量高于2021年，只有东北区域较2021有所下降', color='white',
        fontsize=16, ha='left', va='top', zorder=5)

# note
ax.text(54, 586, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', color=NOTE,
        fontsize=11, ha='left', va='bottom', zorder=5)

out = r'D:\AAA作业\可视化作业\第二章 图表（前15）\蝴蝶图\蝴蝶图_复刻.png'
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
