# -*- coding: utf-8 -*-
# 第7图「蝴蝶图」复刻 数据来源：《第二章 图表(前15).xlsx》工作表 '7 蝴蝶图'
# 华东36%/42% 西北31%/26% 东北18%/19% 华北13%/12% 华南9%/5%
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'
BLUE_DARK = '#005799'
RED = '#E74E69'
RED_DARK = '#A94E69'
NOTE = '#D9D9D9'

W, H = 676, 391

regions = ['华东', '西北', '东北', '华北', '华南']
v2022 = [36, 31, 18, 13, 9]
v2021 = [42, 26, 19, 12, 5]

# measured bar geometry
row_cy = [158, 190, 222, 254, 286]
BAR_H = 20
BLUE_RIGHT = 289
RED_LEFT = 404
blue_left = [112, 112, 183, 213, 237]
red_right = [612, 558, 516, 474, 432]

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

def textured_bar(x0, x1, y0, y1, light, dark):
    # base light fill
    ax.add_patch(Rectangle((x0, y0), x1-x0, y1-y0, facecolor=light, edgecolor='none', zorder=3))
    # dark vertical stripes every 3px, 1px wide
    x = x0 + 1
    while x < x1:
        ax.add_patch(Rectangle((x, y0), 1, y1-y0, facecolor=dark, edgecolor='none', zorder=4))
        x += 3

for i in range(5):
    cy = row_cy[i]
    ytop = cy - BAR_H/2
    # blue bar (leftwards from BLUE_RIGHT)
    textured_bar(blue_left[i], BLUE_RIGHT, ytop, ytop+BAR_H, BLUE, BLUE_DARK)
    # red bar (rightwards from RED_LEFT)
    textured_bar(RED_LEFT, red_right[i], ytop, ytop+BAR_H, RED, RED_DARK)

# percentage labels outside bars
for i in range(5):
    cy = row_cy[i]
    # left pct: right-aligned just left of blue bar
    ax.text(blue_left[i] - 6, cy, str(v2022[i]) + '%', color='white',
            fontsize=13, ha='right', va='center', zorder=5)
    # right pct: left-aligned just right of red bar
    ax.text(red_right[i] + 6, cy, str(v2021[i]) + '%', color='white',
            fontsize=13, ha='left', va='center', zorder=5)

# region names in center column
for i in range(5):
    ax.text(346, row_cy[i], regions[i], color='white',
            fontsize=14, ha='center', va='center', zorder=5)

# title
ax.text(40, 30, '2022年第一季度销售目标完成情况', color='white',
        fontsize=22, fontweight='bold', ha='left', va='top', zorder=5)

# subtitle
ax.text(40, 76, '华东区域完成率最高达到36%，但是相比去年的42%有所下降', color='white',
        fontsize=14, ha='left', va='top', zorder=5)

# note
ax.text(30, 368, '*注：数据来源于公司销售系统，统计日期截至2022.03.31', color=NOTE,
        fontsize=11, ha='left', va='bottom', zorder=5)

out = r'D:\AAA作业\可视化作业\第二章 图表（前15）\蝴蝶图2\蝴蝶图2_复刻.png'
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
