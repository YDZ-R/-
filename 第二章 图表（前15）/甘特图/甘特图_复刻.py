# -*- coding: utf-8 -*-
# 第10图「甘特图」复刻
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BRIGHT = '#00A3E6'
DARK = '#0070C0'
GRID = '#454866'
NOTE = '#D9D9D9'

W, H = 923, 613

tasks = ['制定计划', '方案设计', '资源调配', '第一阶段', '第二阶段', '第三阶段', '项目总结']
start_day = [0, 12, 21, 32, 46, 71, 86]
duration = [11, 8, 10, 13, 24, 14, 7]
pct = [51, 32, 21, 85, 36, 68, 68]

PX_PER_DAY = 98.0/15.0
X0 = 153  # 3/1
BAR_H = 30
ROW_CY = [168, 231, 294, 357, 419, 482, 544]

dates_x = [153, 251, 349, 447, 545, 643, 741, 838]
dates = ['2022/3/1', '2022/3/16', '2022/3/31', '2022/4/15',
         '2022/4/30', '2022/5/15', '2022/5/30', '2022/6/14']

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

# vertical gridlines
for x in dates_x:
    ax.plot([x, x], [95, 580], color=GRID, linewidth=1, linestyle='--', zorder=1)

# date labels at top
for i, x in enumerate(dates_x):
    ax.text(x, 95, dates[i], color='white', fontsize=13,
            ha='center', va='top', zorder=5)

for i in range(7):
    sx = X0 + start_day[i] * PX_PER_DAY
    total_w = duration[i] * PX_PER_DAY
    done_w = total_w * pct[i] / 100.0
    ytop = ROW_CY[i] - BAR_H/2
    # bright = done
    ax.add_patch(Rectangle((sx, ytop), done_w, BAR_H, facecolor=BRIGHT, edgecolor='none', zorder=3))
    # dark = remaining
    ax.add_patch(Rectangle((sx+done_w, ytop), total_w-done_w, BAR_H, facecolor=DARK, edgecolor='none', zorder=3))
    # task name left
    ax.text(130, ROW_CY[i], tasks[i], color='white', fontsize=15,
            ha='right', va='center', zorder=5)
    # pct label at boundary
    ax.text(sx + done_w + 8, ROW_CY[i], str(pct[i]) + '%', color='white',
            fontsize=14, ha='left', va='center', zorder=5)

# title
ax.text(W/2, 25, '2022年化妆品类目采购项目进度', color='white',
        fontsize=26, fontweight='bold', ha='center', va='top', zorder=5)

# note
ax.text(30, 595, '*注：数据来源于公司销售系统，统计日期截至2022.01.01', color=NOTE,
        fontsize=11, ha='left', va='center', zorder=5)

out = r'D:\AAA作业\可视化作业\第二章 图表（前15）\甘特图\甘特图_复刻.png'
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
