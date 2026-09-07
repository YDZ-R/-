import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [2354, 1902, 3524, 2698, 2896, 2563]

BG = '#1A1E43'
TEXT = '#FFFFFF'
NOTE = '#D9D9D9'
GRID = (0.72, 0.76, 0.82, 0.30)
DEEP = '#0072C2'
MID = '#00A0E4'
BRIGHT = '#00B0F0'

fig, ax = plt.subplots(figsize=(8.67, 6.43), dpi=150)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_position([0.132, 0.156, 0.785, 0.527])

fig.text(0.03, 0.93, '3月各区域销量分布', fontsize=34, fontweight='bold',
         color=TEXT, ha='left', va='top')
fig.text(0.03, 0.835, '东北销量最多占总销量的22%，华南销量最低',
         fontsize=25, color=TEXT, ha='left', va='top')

x = np.arange(len(regions))
width = 0.31
y_max = 4000

for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(left=False, bottom=False, labelleft=True, labelbottom=True,
               colors=TEXT, labelsize=14)
ax.set_xticks(x)
ax.set_xticklabels(regions)
ax.set_ylim(0, y_max)
ax.set_yticks([0, 1000, 2000, 3000, 4000])
ax.set_yticklabels(['0', '1000', '2000', '3000', '4000'])
ax.set_xlim(x.min() - 0.6, x.max() + 0.6)

cmap = LinearSegmentedColormap.from_list('grad', [DEEP, MID, BRIGHT])
for i, v in enumerate(sales):
    x0 = i - width / 2
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    im = ax.imshow(grad, extent=[x0, x0 + width, 0, v], aspect='auto',
                   cmap=cmap, zorder=2)
    rect = Rectangle((x0, 0), width, v, transform=ax.transData,
                     facecolor='none', edgecolor='none', zorder=3)
    ax.add_patch(rect)
    im.set_clip_path(rect)
    ax.text(i, v + 100, str(v), ha='center', va='bottom',
            fontsize=15, color=TEXT, fontweight='bold')

ax.yaxis.grid(True, color=GRID, linewidth=1.0, linestyle='--')
ax.set_axisbelow(True)

fig.text(0.03, 0.08, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         fontsize=16, color=NOTE, ha='left', va='bottom')

plt.savefig('D:/AAA作业/可视化作业/渐变柱形图_复刻.png', dpi=150,
            facecolor=BG)
plt.close()
print('done')
