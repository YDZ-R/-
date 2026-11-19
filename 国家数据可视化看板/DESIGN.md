---
name: "国家数据四主题驾驶舱"
description: "以公开统计为依据的浅色交互看板设计系统"
colors:
  primary: "#087b85"
  primary-soft: "#e5f4f5"
  education: "#5572ba"
  population: "#6472b5"
  indigo-soft: "#edf0fa"
  ink: "#173844"
  chart-ink: "#244651"
  muted: "#52717f"
  secondary: "#506c78"
  line: "#dbe7ed"
  ground: "#eef5f8"
  surface: "#fff"
  positive: "#0a7e83"
  negative: "#c65b4c"
  label-dark: "#041015"
  control-surface: "#f8fcfd"
  control-line: "#cfdee6"
  segmented-ground: "#e8f0f3"
  table-head: "#f4f9fb"
  chart-grid: "#e7eff3"
  category-01: "#168e99"
  category-02: "#4b9fd0"
  category-03: "#8581d6"
  category-04: "#48ad95"
  category-05: "#e6b057"
  category-06: "#d98778"
  category-07: "#6a8db4"
  category-08: "#a58bc2"
  category-09: "#79b8c7"
  category-10: "#a5b665"
  category-11: "#d6a07b"
  category-12: "#608f9f"
typography:
  display:
    fontFamily: "\"Microsoft YaHei\",\"Noto Sans SC\",\"PingFang SC\",sans-serif"
    fontSize: "31px"
    fontWeight: 750
    lineHeight: 1.5
    letterSpacing: "-.025em"
  headline:
    fontFamily: "\"Microsoft YaHei\",\"Noto Sans SC\",\"PingFang SC\",sans-serif"
    fontSize: "29px"
    fontWeight: 750
    lineHeight: 1.4
    letterSpacing: "-.015em"
  title:
    fontFamily: "\"Microsoft YaHei\",\"Noto Sans SC\",\"PingFang SC\",sans-serif"
    fontSize: "19px"
    fontWeight: 700
    lineHeight: 1.45
  body:
    fontFamily: "\"Microsoft YaHei\",\"Noto Sans SC\",\"PingFang SC\",sans-serif"
    fontSize: "14px"
    lineHeight: 1.6
  label:
    fontFamily: "\"Microsoft YaHei\",\"Noto Sans SC\",\"PingFang SC\",sans-serif"
    fontSize: "12px"
    lineHeight: 1.45
  panel-title:
    fontFamily: "\"Microsoft YaHei\",\"Noto Sans SC\",\"PingFang SC\",sans-serif"
    fontSize: "16px"
    fontWeight: 700
    lineHeight: 1.6
rounded:
  tag: "4px"
  segment-item: "7px"
  control: "8px"
  segment: "9px"
  filter: "10px"
  insight: "11px"
  card: "12px"
  panel: "15px"
  dialog: "16px"
spacing:
  control-inline: "12px"
  mobile-gap: "9px"
  kpi-gap: "14px"
  panel-gap: "16px"
  section-inset: "18px"
  section-gap: "30px"
  desktop-gutter: "28px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.control}"
    padding: "6px 12px"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "6px 12px"
  period-select:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.control}"
    padding: "6px 12px"
  nav-active:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary}"
    rounded: "{rounded.control}"
    padding: "8px 15px"
  vintage-tag:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary}"
    rounded: "{rounded.tag}"
    padding: "2px 5px"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
  kpi:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "17px 18px 13px"
  segmented-active:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.segment-item}"
    padding: "6px 11px"
---

# Design System: 国家数据四主题驾驶舱

## Overview

**Creative North Star: "清晰可核查的统计驾驶舱"**

以用户固定的季度经济、教育与旅游看板参考为视觉依据，使用雾蓝底色、白色图面、深色中文和克制的分类色，让时间、规模、结构与变化可以在同一屏中比较。界面由工具栏、指标与图组构成，视觉重点始终落在数据。

经济和旅游采用青蓝主色，教育与人口采用各自的蓝紫主题色；共同的留白、层级和组件使四个主题保持一致。这里记录的是完成后的原生 HTML/CSS/ECharts 实现，代码与实际输出优先于早期意图；方向标识为 pinned-reference-20261119。

**Key Characteristics:**

- 浅雾蓝画布与白色图面，紧凑而有层级。
- 中文无衬线字体、等宽数字与清晰单位。
- 同一分类跨图保持颜色一致。
- 桌面多列图组，手机按阅读顺序纵向展开。

## Colors

色彩通过主题、类别与中性色三个职责组织；精确值以前置 tokens 为准。

### Primary

- **深青蓝**（primary）：经济与旅游的按钮、选中导航、时间选择及重点数据。
- **浅青蓝**（primary-soft）：对应主题的选中背景与年份标记。

### Secondary

- **教育蓝**（education）与**人口蓝紫**（population）：各主题的操作和当前观察期强调。
- **浅蓝紫**（indigo-soft）：教育和人口的选中背景。
- **石板蓝灰**（secondary）：次要说明、来源、状态与图表描述。

### Tertiary

- **统计分类色**（category-01 至 category-12）：按现有顺序和数据映射用于多系列、分类结构与比较图；它们不是导航装饰色。
- **增长青绿**（positive）与**下降陶红**（negative）：带符号的指标变化。

### Neutral

- **深蓝墨色**（ink / chart-ink）：界面正文与图表正文。
- **蓝灰**（muted）：轴、单位、次级文本。
- **雾蓝画布**（ground）、**白色图面**（surface）和**浅蓝边线**（line）：形成主要层次。
- **极深标签色**（label-dark）：矩形树图与热力图的内部数字，保持分类色块上的可读性。

**The Theme Continuity Rule.** 经济和旅游使用青蓝主题，教育和人口保留已实现的蓝紫主题；所有主题共享同一套中性色与组件结构。

**The Category Identity Rule.** 分类颜色代表稳定的数据类别；教育的平行坐标、面积图和图例沿用同一学段映射。

## Typography

全站使用 Microsoft YaHei、Noto Sans SC、PingFang SC 与 sans-serif 回退；图表使用 Microsoft YaHei、Noto Sans SC 与 sans-serif。数字开启 tabular-nums。没有外部展示字体。

### Hierarchy

- **Display**：指标值，常态（31px / 750）；大屏（36px），手机（27px）。
- **Headline**：页面标题，常态（29px / 750）；中屏（27px），手机（25px）。
- **Title**：图组标题（19px / 700）；手机（18px）。
- **Panel title**：图表标题（16px / 700）；手机（15px）。
- **Body**：基础文字（14px / 1.6）；说明性文字按组件使用（13px）。
- **Label**：指标标签、控件与坐标的常用字号（12px）；图内说明使用（10–11px），手机局部标记可到（9px）。

**The Measured Label Rule.** 图表保留单位，明细与导出使用完整指标名称及口径；缩写只用于需要节省空间的图内标签。

## Layout

主容器居中，最大宽度（1840px），常态左右边距（28px）。顶部白色导航高（66px），时间与筛选工具栏粘附视口顶部。页面标题和操作区先于时间轴、指标、速读、图组与数据明细。滚动条预留稳定槽位，避免模态开关造成页面横移。

桌面图组采用（12）列，标准图占（6）列，主图与侧图采用（8 / 4）列；面板间距（16px）。六项指标分成（6）列，间距（14px）。图表常态高（304px），主侧图组合高（328px）；大屏分别为（326 / 350px）。图组纵向间距（30px）。

在不超过（1180px）时，工具栏换行，指标变为（3）列，主侧图统一为半宽；不超过（720px）时，导航与操作区换行，主容器左右留白（12px），指标变为（2）列，图表顺序堆叠且高度（308px）。不小于（1550px）时放大指标和图表。既有 QA 参考视口为桌面（1265px）和手机（390px）。CSS 的移动断点为 max-width:720px，图表渲染器判断为 innerWidth<720，保持现有边界条件。

## Elevation & Depth

采用浅层材质：白色面板与浅边框为主，指标、粘性工具栏和分段选中项有轻微阴影；对话框和提示提供临时前景层。准确阴影值收录于 sidecar extensions.shadows。

**The Quiet Depth Rule.** 常态图面以白色、浅边框和间距分组；显著阴影留给模态层，指标仅用轻微环境阴影。

## Shapes

使用温和圆角矩形：普通控件（8px）、指标（12px）、图表（15px）、对话框（16px），小型年份标记（4px）。手机图表面板为（12px）、指标为（10px）。面板裁剪内容，图表保持完整矩形图面；没有装饰性异形容器。

## Components

### Buttons

主按钮为主题色底、白字与加粗文字；普通按钮为白底深字和浅蓝边框。常态最小高度（36px），内边距（6px 12px）。悬停时普通按钮转浅主题底与主题边框，主按钮亮度降至（.94）。禁用项不透明度（.4）。所有交互元素以主题色（3px）焦点轮廓和（3px）外偏移标识键盘焦点。

### Inputs / Fields

时期选择、区间选择、步进按钮和原生范围滑块组成连续工具栏。选择器白底、浅边线与控件圆角；当前时期文字为主题色。复选框、滑块与输入光标使用主题色。工具栏换行后保留操作顺序。

### Navigation

四主题导航位于白色顶部栏。未选中项为蓝灰文字，悬停使用浅灰蓝底，当前页使用浅主题底与主题色加粗文字；手机四项平均分配可用宽度。品牌使用内联线条 SVG。

### Chips / Tags

小型实际发布年份标记采用浅主题底、主题色文字和紧凑圆角，仅表达数据年份；不承担额外筛选含义。

### Cards / Containers

图表面板使用白色、浅边框和面板圆角；标题、说明与放大按钮在图面之上。六项指标卡采用轻阴影、大数值和紧随数字的单位。速读条使用近白浅蓝底，突出观察年份与关键数值。

### Segmented Control

经济主题的当季/累计切换使用浅蓝灰底槽与白色选中块；选中项为主题色加粗文字和轻阴影，状态由 aria-pressed 表示。

### Charts / Detail / Dialog

图表共用轻虚线网格、紧凑图例、蓝灰坐标与持续单位。矩形树图、环图、玫瑰图和蝴蝶图在面板说明保留单位。热力图与矩形树图使用深色内部标签，教育平行坐标沿用学段图例颜色。明细表右对齐数值，包含完整指标名称、单位和时期；表头粘附且容器可滚动。

桌面图表使用 Canvas，手机使用 SVG 并关闭图表动画。常态桌面图表动画（240ms），减少动态效果偏好下为（0ms）；CSS 平滑滚动也关闭。放大对话框保留 Canvas，使用白底（2倍）PNG 导出；对话框遮罩将暂时任务与底层图组区分。

## Do's and Don'ts

### Do:

- Do 保留雾蓝背景、白色面板及各主题现有主色。
- Do 使用统一时间轴联动图表、指标和明细，并保留实际发布年份标记。
- Do 在图表说明或坐标轴上持续显示单位；保留完整指标名称与统计口径。
- Do 保持分类图例、数据标记和跨图类别颜色一致。
- Do 在手机上采用单列图表与两列指标，并保留可操作的筛选工具。

### Don't:

- Don't 添加栅格主视觉或装饰性照片抢占统计图表空间。
- Don't 把教育和人口的蓝紫主题强行改成通用青蓝。
- Don't 用浅色文字覆盖矩形树图或热力图的数据块；沿用深色标签。
- Don't 通过补造缺失年份、隐藏口径差异或只给缩写来制造完整感。
