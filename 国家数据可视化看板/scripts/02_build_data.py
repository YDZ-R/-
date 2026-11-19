"""Build four themed, source-linked datasets and their chart specifications."""
from pathlib import Path
import json
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
facts = pd.read_csv(ROOT/'data/clean/nbs_observations.csv', keep_default_na=False)
tables = {p.stem:json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'data/raw').glob('*.json') if p.stem!='source_manifest'}
ANNUAL = [str(y) for y in range(2011,2026)]
QUARTERS = [f'{y}Q{q}' for y in range(2022,2027) for q in range(1,5) if '2022Q2'<=f'{y}Q{q}'<='2026Q3']

def series(target, table, row, key, label, unit=None, factor=1, subtract=0):
    source_label=tables[table]['tables'][3][row][0]
    rows=facts[(facts.table==table)&(facts.indicator==source_label)]
    values={r.period:None if r.value=='' else round(float(r.value)*factor-subtract,6) for r in rows.itertuples()}
    entry=dict(id=key,label=label,unit=unit if unit is not None else rows.unit.iloc[0],values=values,
               source_table=table,source_indicator=source_label,source_factor=factor,source_subtract=subtract)
    target['series'][key]=entry
    return key

def derived(target,key,label,unit,inputs,operation):
    values={}
    for p in target['periods']:
        row=[target['series'][k]['values'].get(p) for k in inputs]
        value=None if any(v is None for v in row) else operation(row)
        values[p]=None if value is None or not math.isfinite(value) else round(value,6)
    target['series'][key]=dict(id=key,label=label,unit=unit,values=values,derived_from=inputs)
    return key

def theme(key,title,subtitle,accent,periods):
    return dict(id=key,title=title,subtitle=subtitle,accent=accent,periods=periods,
                default_period=periods[-1],series={},groups={},charts=[],cards=[],notes=[])

def chart(target,key,title,kind,keys,section,**kwargs):
    target['charts'].append(dict(id=key,title=title,type=kind,keys=keys,section=section,**kwargs))

def card(t,key,label,**kwargs):t['cards'].append(dict(key=key,label=label,**kwargs))

e=theme('economy','国民经济季度运行','总量、结构与增长动力', '#087b85', QUARTERS)
sector_names=['第一产业','第二产业','第三产业']
industries=[(8,'agriculture','农林牧渔业'),(10,'industry','工业'),(14,'construction','建筑业'),(16,'trade','批发和零售业'),
            (18,'transport','交通运输、仓储和邮政业'),(20,'hospitality','住宿和餐饮业'),(22,'finance','金融业'),
            (24,'estate','房地产业'),(26,'it','信息传输、软件和信息技术服务业'),(28,'business','租赁和商务服务业'),(30,'other','其他服务业')]
for mode,offset in [('current',0),('cumulative',1)]:
    for row,key,label in [(0,'gdp','国内生产总值')]+[(2+i*2,f'sector{i+1}',name) for i,name in enumerate(sector_names)]+industries:
        series(e,'economy_nominal',row+offset,f'{key}_{mode}',label,'万亿元',1e-4)
        series(e,'economy_real_growth',row+offset,f'{key}_growth_{mode}',label,'%',1,100)
    for i,name in enumerate(sector_names):
        derived(e,f'share{i+1}_{mode}',name,'%', [f'sector{i+1}_{mode}',f'gdp_{mode}'],lambda r:100*r[0]/r[1] if r[1] else None)
        series(e,'economy_contribution',2+2*i+offset,f'contrib{i+1}_{mode}',name,'%',1)
    for i,name in enumerate(['最终消费支出','资本形成总额','货物和服务净出口']):
        series(e,'economy_demand',2*i+offset,f'demand{i+1}_{mode}',name,'%',1)
series(e,'economy_qoq',0,'qoq','GDP季调环比','%')
e['mode_switch']=True
card(e,'gdp_@','GDP规模',digits=2,delta='gdp_growth_@',delta_kind='official')
card(e,'gdp_growth_@','实际同比增长',digits=1,delta_kind='pp')
card(e,'share3_@','第三产业占比',digits=1,delta_kind='pp')
card(e,'demand1_@','最终消费贡献率',digits=1,delta_kind='pp')
card(e,'demand2_@','资本形成贡献率',digits=1,delta_kind='pp')
card(e,'demand3_@','净出口贡献率',digits=1,delta_kind='pp')
chart(e,'gdp','GDP规模与实际同比','combo',['gdp_@','gdp_growth_@'],'总量与周期',wide=True)
chart(e,'qoq','季调环比增长动能','bar',['qoq'],'总量与周期',description='季节调整后的当季环比')
chart(e,'sectors','三次产业增加值','stacked',[f'sector{i}_@' for i in [1,2,3]],'结构与贡献')
chart(e,'growth','三次产业实际同比','line',[f'sector{i}_growth_@' for i in [1,2,3]],'结构与贡献')
chart(e,'contribution','三次产业增长贡献率','stacked',[f'contrib{i}_@' for i in [1,2,3]],'结构与贡献',percent=True)
chart(e,'demand','三大需求增长贡献率','stacked',[f'demand{i}_@' for i in [1,2,3]],'结构与贡献',percent=True)
industry_keys=[f'{key}_@' for _,key,_ in industries]
growth_keys=[f'{key}_growth_@' for _,key,_ in industries]
chart(e,'rank','主要行业实际增长排名','rank',growth_keys,'行业分化')
chart(e,'industry_heat','行业增长时间矩阵','heatmap',growth_keys,'行业分化',wide=True)
chart(e,'industry_tree','行业增加值构成','treemap',industry_keys,'行业分化')
chart(e,'bubble','行业规模与增速','scatter',industry_keys,'行业分化',ykeys=growth_keys)
chart(e,'seasonal','GDP的季度季节轮廓','seasonal',['gdp_current'],'周期与比较')
chart(e,'calendar','季度GDP规模热力图','calendar',['gdp_current'],'周期与比较')
chart(e,'demand_delta','需求贡献较上季的变化','dot',[f'demand{i}_@' for i in [1,2,3]],'周期与比较')
chart(e,'sector_radar','产业结构的观察期对比','radar',[f'share{i}_@' for i in [1,2,3]],'周期与比较',compare=True)
chart(e,'waterfall','GDP规模较上季的变化','waterfall',['gdp_current'],'周期与比较',description='现价规模差额，未经季调')
chart(e,'industry_slope','行业增长起点与观察期对比','slope',growth_keys,'周期与比较')
e['notes']=['现价增加值用于规模和结构，不变价指数减100用于实际同比，两者不能相互替代。',
 '当季与累计均直接使用官方发布值；累计增速、贡献率不通过季度增速简单平均。季调环比始终为当季口径。',
 '行业构成不重复计入工业中的制造业；农林牧渔业与第一产业存在统计分类差异，分别保留。',
 '贡献率可能为负或大于100%，图形保留真实符号；季度现价差额并非季调环比增长。']

t=theme('tourism','全国旅游与住宿','需求复苏、消费结构与双向出行','#087b85',ANNUAL)
for row,key,label,unit,factor in [(0,'trips','国内游客','亿人次',.01),(1,'urban_trips','城镇居民出游','亿人次',.01),
 (2,'rural_trips','农村居民出游','亿人次',.01),(3,'spending','国内旅游总花费','万亿元',1e-4),
 (4,'urban_spending','城镇居民旅游花费','万亿元',1e-4),(5,'rural_spending','农村居民旅游花费','万亿元',1e-4),
 (6,'per_trip','国内旅游人均花费','元',1),(7,'urban_per_trip','城镇居民人均花费','元',1),(8,'rural_per_trip','农村居民人均花费','元',1)]:
    series(t,'tourism_domestic',row,key,label,unit,factor)
for row,key,label,unit,factor in [(0,'agencies','旅行社','家',1),(1,'hotels','星级饭店','家',1),
 (2,'inbound','入境游客','亿人次',1e-4),(3,'foreign','外国人入境游客','亿人次',1e-4),(7,'outbound','国内居民出境','亿人次',1e-4)]:
    series(t,'tourism_development',row,key,label,unit,factor)
series(t,'tourism_income',0,'inbound_revenue','国际旅游收入','亿美元')
derived(t,'net_trips','入境减出境人次差','亿人次',['inbound','outbound'],lambda r:r[0]-r[1])
derived(t,'hmt','港澳台游客（差额）','亿人次',['inbound','foreign'],lambda r:r[0]-r[1])
derived(t,'spend_gap','城乡人均花费差','元',['urban_per_trip','rural_per_trip'],lambda r:r[0]-r[1])
income_components=[]
for row,label in [(1,'长途交通'),(6,'游览'),(7,'住宿'),(8,'餐饮'),(9,'购物'),(10,'娱乐'),(11,'邮电通讯'),(12,'市内交通'),(13,'其他服务')]:
    key=f'income_part{row}';series(t,'tourism_income',row,key,label,'亿美元');income_components.append(key)
country_keys=[]
for row,label_row in enumerate(tables['tourism_origins']['tables'][3]):
    label=label_row[0].split(' (')[0].replace('入境游客','')
    if label and '洲' not in label and '其他' not in label:
        key=f'country{row}';series(t,'tourism_origins',row,key,label,'万人次');country_keys.append(key)
for key,label in [('trips','国内出游人次'),('spending','国内旅游花费'),('per_trip','每人次花费'),('inbound','入境游客'),('inbound_revenue','国际旅游收入'),('hotels','星级饭店')]:
    card(t,key,label,digits=2 if key in ['trips','spending','inbound'] else 0,vintage=True)
chart(t,'demand','国内出游与旅游花费','combo',['trips','spending'],'需求与复苏',wide=True)
chart(t,'baseline','相对2019年的恢复水平','baseline',['trips','spending','inbound','inbound_revenue'],'需求与复苏',base='2019')
chart(t,'urban','城乡国内出游结构','area',['urban_trips','rural_trips'],'消费结构')
chart(t,'urban_share','城乡花费结构变化','share',['urban_spending','rural_spending'],'消费结构')
chart(t,'percap','城乡人均旅游花费','line',['urban_per_trip','rural_per_trip','per_trip'],'消费结构')
chart(t,'gap','城乡人均花费起点与观察期','slope',['urban_per_trip','rural_per_trip'],'消费结构')
chart(t,'inout','入境与出境双向出行','mirror',['inbound','outbound','net_trips'],'国际旅游')
chart(t,'income','国际旅游收入与入境规模','combo',['inbound_revenue','inbound'],'国际旅游')
chart(t,'income_parts','国际旅游收入构成','donut',income_components,'国际旅游',asof=True)
chart(t,'inbound_mix','入境游客的身份结构','donut',['foreign','hmt'],'国际旅游',asof=True)
chart(t,'country_rank','主要客源国家排名','rank',country_keys,'客源与供给',asof=True,limit=10)
chart(t,'country_tree','列示国家客源分布','treemap',country_keys,'客源与供给',asof=True)
chart(t,'supply','旅行社与星级饭店规模','line',['agencies','hotels'],'客源与供给')
chart(t,'supply_index','住宿与旅行社供给的长期变化','baseline',['agencies','hotels'],'客源与供给',base='2011')
chart(t,'growth_heat','旅游主要指标同比矩阵','heatmap',['trips','spending','per_trip','inbound','inbound_revenue','outbound','agencies','hotels'],'关联与变化',transform='yoy',wide=True)
chart(t,'tour_corr','旅游指标水平值的相关矩阵','correlation',['trips','spending','per_trip','inbound','inbound_revenue','agencies','hotels'],'关联与变化')
t['breaks']={'inbound_revenue':['2014']}
t['notes']=['游客数均为人次，不是去重人数；百万人次除以100转为亿人次，万人次除以10000转为亿人次。',
 '官方表中的空白保留为缺失，未补值。细分结构只显示所选年之前最近实际公布的年份，并在标题旁明确标注真实年份。',
 '星级饭店仅为按星级统计的饭店，不能代表全部住宿业供给。入境与国内居民出境来自不同统计口径，差额仅用于规模对照。',
 '2014年国际旅游收入测算方法与统计口径调整，该年跨口径同比留空；收入构成不重复计入长途交通中的民航、铁路、汽车和轮船。',
 '国内旅游情况表与旅游发展表的金额精度略有差别，国内指标优先使用已用官方Excel逐格核对的国内旅游情况表。']

u=theme('education','全国教育发展','六类学段的规模、资源与投入','#5572ba',ANNUAL)
cats=[('preschool','学前教育',7),('primary','小学',5),('middle','初中',3),('high','普通高中',2),('higher','普通、职业本专科',0),('special','特殊教育',6)]
u['categories']=[dict(id=k,label=n) for k,n,_ in cats]
for table,metric,unit in [('education_students','students','万人'),('education_teachers','teachers','万人'),('education_schools','schools','所')]:
    for key,label,row in cats:series(u,table,row,f'{metric}_{key}',label,unit)
for table,metric in [('education_admissions','admissions'),('education_graduates','graduates')]:
    for key,label,row in cats:
        if key=='preschool':continue
        index={'higher':0,'high':2,'middle':3,'primary':5,'special':6}[key]
        series(u,table,index,f'{metric}_{key}',label,'万人')
for key,label,_ in cats:
    derived(u,f'ratio_{key}',label,'人/教师',[f'students_{key}',f'teachers_{key}'],lambda r:r[0]/r[1] if r[1] else None)
    derived(u,f'perschool_{key}',label,'人/所',[f'students_{key}',f'schools_{key}'],lambda r:10000*r[0]/r[1] if r[1] else None)
fund_types=[('total','教育经费总投入'),('public','国家财政性'),('private','民办学校办学'),('donation','社会捐赠'),('institution','事业收入'),('other','其他经费')]
for key,label in fund_types:series(u,'education_funding_'+key,0,'fund_'+key,label,'亿元',1e-4)
series(u,'annual_gdp',1,'annual_gdp','年度GDP','亿元')
derived(u,'fund_gdp','财政性教育经费/GDP','%',['fund_public','annual_gdp'],lambda r:100*r[0]/r[1] if r[1] else None)
derived(u,'fund_public_share','财政性教育经费占比','%',['fund_public','fund_total'],lambda r:100*r[0]/r[1] if r[1] else None)
derived(u,'students_total','六类在校生合计','万人',[f'students_{k}' for k,_,_ in cats],sum)
derived(u,'teachers_total','六类专任教师合计','万人',[f'teachers_{k}' for k,_,_ in cats],sum)
for key,label in [('students_total','六类学段在校生'),('students_higher','本专科在校生'),('teachers_total','六类专任教师'),('schools_higher','普通、职业高校'),('students_preschool','学前在园人数'),('fund_total','教育经费投入')]:
    card(u,key,label,digits=1 if key not in ['schools_higher','fund_total'] else 0,vintage=True)
students=[f'students_{k}' for k,_,_ in cats];teachers=[f'teachers_{k}' for k,_,_ in cats]
chart(u,'students','六类学段在校生规模','area',students,'规模与结构',category=True,wide=True)
chart(u,'student_tree','观察期在校生构成','treemap',students,'规模与结构',category=True)
chart(u,'student_share','在校生结构的长期变化','share',students,'规模与结构',category=True)
chart(u,'parallel','六类学段资源画像','parallel',students,'规模与结构',category=True,axes=['students','teachers','schools','ratio'])
chart(u,'butterfly','招生与毕业生对照','butterfly',[f'admissions_{k}' for k,_,_ in cats if k!='preschool'],'流动与师资',rightkeys=[f'graduates_{k}' for k,_,_ in cats if k!='preschool'],category=True)
chart(u,'ratios','学生与专任教师的数量比','line',[f'ratio_{k}' for k,_,_ in cats],'流动与师资',category=True)
chart(u,'slope','在校生规模的起点与观察期','slope',students,'流动与师资',category=True)
chart(u,'school_trend','学校数量变化','line',[f'schools_{k}' for k,_,_ in cats],'流动与师资',category=True)
chart(u,'school_scatter','学校、教师与在校生','scatter',[f'schools_{k}' for k,_,_ in cats],'资源配置',ykeys=teachers,sizekeys=students,category=True)
chart(u,'schoolsize','平均每校在校生','rank',[f'perschool_{k}' for k,_,_ in cats],'资源配置',category=True)
chart(u,'edu_heat','六类在校生同比变化','heatmap',students,'资源配置',category=True,transform='yoy')
chart(u,'teacher_share','专任教师结构','share',teachers,'资源配置',category=True)
fund_parts=['fund_'+k for k,_ in fund_types if k!='total']
chart(u,'funds','教育经费投入及来源','stacked',fund_parts,'教育投入',wide=True)
chart(u,'fund_gdp','财政性经费投入强度','line',['fund_gdp','fund_public_share'],'教育投入')
chart(u,'fund_share','经费来源结构','share',fund_parts,'教育投入')
chart(u,'fund_rose','最近公布的经费来源','rose',fund_parts,'教育投入',asof=True)
u['notes']=['本看板选取学前、小学、初中、普通高中、普通职业本专科、特殊教育六类，合计不含中等职业教育、研究生和成人教育，不能解释为全国全部学历教育在校生总数。',
 '不同学段学校数是分类统计口径，不据此推算全国不重复的校园数量。学生/专任教师、每校学生由同年同类数据计算，并非官方调整后的生师比。',
 '学前教育未提供同口径招生与毕业序列，因此招生毕业对照只展示其他五类。',
 '教育经费是全国教育投入，覆盖范围大于六类学段，不用全国经费除以六类学生计算所谓生均经费。',
 '国家财政性、民办学校办学、社会捐赠、事业收入、其他经费作为来源分类；不重复加入财政预算内经费或事业收入中的学杂费。',
 '经费明细缺失年份保留为空。财政性经费/GDP使用同年年度GDP，可用年份以实际交集为准。2020年总投入与五项来源合计相差0.0061亿元，保留各表原值。']

p=theme('population','人口与居民生活','人口结构、城镇化与收入消费','#6472b5',ANNUAL)
for row,key,label in [(0,'population','年末总人口'),(1,'male','男性人口'),(2,'female','女性人口'),(3,'urban','城镇人口'),(4,'rural','乡村人口')]:
    series(p,'population_total',row,key,label,'万人')
for row,key,label in [(0,'birth','出生率'),(1,'death','死亡率'),(2,'natural','自然增长率')]:series(p,'population_rates',row,key,label,'‰')
for row,key,label,unit in [(1,'young','0—14岁','万人'),(2,'working','15—64岁','万人'),(3,'old','65岁及以上','万人'),(4,'dependency','总抚养比','%'),(5,'young_dependency','少儿抚养比','%'),(6,'old_dependency','老年抚养比','%')]:series(p,'population_age',row,key,label,unit)
for table,key,label in [('living_income','income','全国居民'),('living_urban_income','urban_income','城镇居民'),('living_rural_income','rural_income','农村居民')]:series(p,table,0,key,label,'元')
series(p,'living_income',2,'median_income','收入中位数','元')
for row,key,label in [(4,'wage','工资性收入'),(6,'business','经营净收入'),(8,'property','财产净收入'),(10,'transfer','转移净收入')]:series(p,'living_income',row,key,label,'元')
series(p,'living_spending',0,'consumption','居民人均消费支出','元')
spend_keys=[]
for i,label in enumerate(['食品烟酒','衣着','居住','生活用品及服务','交通通信','教育文化娱乐','医疗保健','其他用品及服务']):
    key=f'spend{i}';series(p,'living_spending',4+i*2,key,label,'元');spend_keys.append(key)
quintile_keys=[]
for i,label in enumerate(['低收入组','中间偏下组','中间收入组','中间偏上组','高收入组']):
    key=f'quintile{i}';series(p,'living_quintiles',i,key,label,'元');quintile_keys.append(key)
for i,key,label in [(0,'engel','全国居民'),(1,'urban_engel','城镇居民'),(2,'rural_engel','农村居民')]:series(p,'living_engel',i,key,label,'%')
derived(p,'urbanization','常住人口城镇化率','%',['urban','population'],lambda r:100*r[0]/r[1] if r[1] else None)
derived(p,'old_share','65岁及以上占比','%',['old','population'],lambda r:100*r[0]/r[1] if r[1] else None)
derived(p,'urban_rural_ratio','城乡居民收入比','倍',['urban_income','rural_income'],lambda r:r[0]/r[1] if r[1] else None)
derived(p,'income_gap','城乡居民收入差','元',['urban_income','rural_income'],lambda r:r[0]-r[1])
for key,label in [('population','年末总人口'),('urbanization','常住人口城镇化率'),('old_share','65岁及以上占比'),('income','居民人均可支配收入'),('consumption','居民人均消费支出'),('urban_rural_ratio','城乡居民收入比')]:card(p,key,label,digits=2 if key=='urban_rural_ratio' else 1,vintage=True)
chart(p,'population','人口总量与自然增长','combo',['population','natural'],'人口与城镇化',wide=True)
chart(p,'rates','出生、死亡与自然增长','line',['birth','death','natural'],'人口与城镇化')
chart(p,'urban_rural','城乡人口结构','area',['urban','rural'],'结构与抚养')
chart(p,'age','人口年龄结构变化','share',['young','working','old'],'结构与抚养')
chart(p,'age_tree','观察期年龄结构','treemap',['young','working','old'],'结构与抚养')
chart(p,'dependency','少儿与老年抚养比','line',['young_dependency','old_dependency','dependency'],'结构与抚养')
chart(p,'income','城乡居民收入轨迹','line',['urban_income','rural_income','income'],'收入与分配')
chart(p,'income_slope','城乡收入起点与观察期','slope',['urban_income','rural_income'],'收入与分配')
chart(p,'income_mix','居民可支配收入来源','area',['wage','business','property','transfer'],'收入与分配')
chart(p,'quintiles','五等份收入组的收入水平','rank',quintile_keys,'收入与分配')
chart(p,'spending','居民人均收入与消费','combo',['income','consumption'],'消费与生活')
chart(p,'consume_tree','人均消费的八类构成','treemap',spend_keys,'消费与生活')
chart(p,'consume_share','消费结构的长期变化','share',spend_keys,'消费与生活')
chart(p,'engel','城乡恩格尔系数','line',['engel','urban_engel','rural_engel'],'消费与生活')
chart(p,'living_heat','居民生活指标同比矩阵','heatmap',['income','consumption','urban_income','rural_income','spend4','spend5','spend6'],'关联与分化',transform='yoy')
chart(p,'pop_corr','人口与收入水平的相关矩阵','correlation',['urbanization','old_share','income','consumption','urban_rural_ratio'],'关联与分化')
p['notes']=['总人口、城乡与性别人口使用年末口径，人口率单位为千分比。年龄划分采用0—14、15—64、65岁及以上。',
 '居民收支序列采用本次国家数据公开表，包含表内2011、2012年的历史数值，不自行拼接旧表或补造年份。',
 '收入和消费均为人均名义金额；收入比不等于收入差。未用收入水平同比代替官方实际收入增速。',
 '八类消费为支出分类，服务性消费属于交叉分类，不重复计入八类合计。',
 '水平值Pearson相关仅使用共同非缺失年份，趋势可能造成高相关，不能据此推断因果。']

themes=[e,t,u,p]
for item in themes:
    item['source_url']='https://data.stats.gov.cn/dg/website/page.html#/pc/national/home'
    item['accessed_date']='2026-11-19'
    item['notes'].append('未公布值不作0处理，亦不插值。同比只比较相邻年份；相关分析在共同非缺失的观测上计算。')
    item['chart_count']=len(item['charts'])
    assert len(item['charts'])>=16 and len({c['id'] for c in item['charts']})==len(item['charts'])
    (ROOT/f'data/clean/{item["id"]}.json').write_text(json.dumps(item,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
index=[dict(id=x['id'],title=x['title'],periods=len(x['periods']),charts=len(x['charts']),series=len(x['series'])) for x in themes]
(ROOT/'outputs/catalog.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(index,ensure_ascii=False))
