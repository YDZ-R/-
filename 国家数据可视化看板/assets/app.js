'use strict';
(() => {
  const D=DASHBOARD,$=id=>document.getElementById(id);
  const palette=['#168e99','#4b9fd0','#8581d6','#48ad95','#e6b057','#d98778','#6a8db4','#a58bc2','#79b8c7','#a5b665','#d6a07b','#608f9f'];
  const ink='#244651',muted='#52717f',gridColor='#e7eff3';
  const small=()=>window.innerWidth<720;
  const motion=window.matchMedia('(prefers-reduced-motion: reduce)').matches?0:240;
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const state={period:D.default_period,start:D.periods[0],end:D.periods.at(-1),mode:'current',categories:new Set((D.categories||[]).map(c=>c.id)),timer:null};
  const instances=new Map();let expanded=null,expandedRecipe=null,toastTimer=null;
  const resolve=k=>k.replace('@',state.mode);
  const S=k=>D.series[resolve(k)];
  const fmt=(v,d=1)=>Number.isFinite(v)?v.toLocaleString('zh-CN',{maximumFractionDigits:d,minimumFractionDigits:d}):'—';
  const signed=(v,d=1)=>Number.isFinite(v)?(v>0?'+':'')+fmt(v,d):'—';
  const short=s=>s.replace('信息传输、软件和信息技术服务业','信息服务业').replace('交通运输、仓储和邮政业','交运仓储邮政').replace('租赁和商务服务业','租赁商务').replace('普通、职业本专科','本专科').replace('常住人口城镇化率','城镇化率').replace('财政性教育经费/GDP','财政性经费/GDP').replace('货物和服务净出口','净出口').replace('国内旅游人均花费','人均旅游花费').replace('国内居民出境','居民出境');
  function measureLabel(s){
    const k=s.id;
    if(D.id==='economy'){
      const scope=k.endsWith('_current')?'当季':k.endsWith('_cumulative')?'累计':'';
      if(k.includes('_growth_'))return s.label+'实际同比（'+scope+'）';
      if(k.startsWith('share'))return s.label+'增加值占比（'+scope+'）';
      if(k.startsWith('contrib')||k.startsWith('demand'))return s.label+'增长贡献率（'+scope+'）';
      if(scope)return s.label+'（现价，'+scope+'）';
    }
    if(D.id==='education'){
      const metric=k.split('_')[0],suffix={students:'在校生',teachers:'专任教师',schools:'学校数',admissions:'招生人数',graduates:'毕业人数',ratio:'学生/专任教师数',perschool:'每校在校生'}[metric];
      if(suffix&&!k.endsWith('_total'))return s.label+suffix;
    }
    if(D.id==='population'&&['income','urban_income','rural_income'].includes(k))return s.label+'人均可支配收入';
    return s.label;
  }
  function V(k,p=state.period){
    if(D.id==='education'&&['students_total','teachers_total'].includes(k)){
      const metric=k.split('_')[0],vs=[...state.categories].map(c=>S(`${metric}_${c}`)?.values[p]);
      return vs.length&&vs.every(Number.isFinite)?vs.reduce((a,b)=>a+b,0):null;
    }
    return S(k)?.values[p]??null;
  }
  const periods=()=>D.periods.filter(p=>p>=state.start&&p<=state.end);
  function keysFor(r){return r.keys.filter(k=>!r.category||state.categories.has(k.split('_').at(-1)));}
  function latest(k,before=state.period){return [...D.periods].reverse().find(p=>p<=before&&Number.isFinite(V(k,p)))||null;}
  function previousYear(p){return String(Number(p.slice(0,4))-1)+p.slice(4);}
  function yoy(k,p){
    if(D.breaks?.[resolve(k)]?.includes(p))return null;
    const a=V(k,p),b=V(k,previousYear(p));return Number.isFinite(a)&&Number.isFinite(b)&&b!==0?(a/b-1)*100:null;
  }
  function effectivePeriod(r,ks){return r.asof?[...D.periods].reverse().find(p=>p<=state.period&&ks.some(k=>Number.isFinite(V(k,p))))||state.period:state.period;}
  function color(k,i=0){
    const cat=D.categories?.findIndex(c=>k.endsWith('_'+c.id));if(cat>=0)return [palette[4],palette[1],palette[0],palette[2],palette[3],palette[5]][cat];
    const m=k.match(/(?:sector|share|contrib)([123])/);if(m)return [palette[3],palette[1],palette[2]][Number(m[1])-1];
    return palette[i%palette.length];
  }
  function toast(text){$('toast').textContent=text;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,2200);}
  function stop(){clearInterval(state.timer);state.timer=null;$('play').textContent='播放';$('play').setAttribute('aria-pressed','false');}
  function dataTooltip(params){
    const rows=Array.isArray(params)?params:[params];let h='<b>'+esc(rows[0]?.axisValueLabel??rows[0]?.name??'')+'</b>';
    for(const p of rows){let v=Array.isArray(p.value)?p.value.at(-1):p.value;if(v==null||p.seriesName==='辅助')continue;
      const unit=p.seriesId?.split('|').at(-1)||'';h+='<br>'+p.marker+esc(p.seriesName)+'　<b>'+fmt(Number(v),Math.abs(v)>=1000?0:2)+'</b> '+esc(unit);
    }return h;
  }
  function base(unit='',horizontal=false){return {
    animation:!small(),animationDuration:motion,animationDurationUpdate:motion,color:palette,
    textStyle:{fontFamily:'Microsoft YaHei, Noto Sans SC, sans-serif',color:ink},
    grid:{left:horizontal?12:18,right:horizontal?42:22,top:44,bottom:22,containLabel:true},
    tooltip:{trigger:'axis',confine:true,backgroundColor:'#fff',borderColor:'#dce8ed',padding:[10,13],textStyle:{color:ink,fontSize:12},extraCssText:'box-shadow:0 5px 22px #17384415;border-radius:9px;',formatter:dataTooltip},
    legend:{top:2,right:12,left:horizontal?undefined:16,type:'scroll',itemWidth:11,itemHeight:8,textStyle:{fontSize:11,color:muted},formatter:short},
    xAxis:{type:'category',axisLabel:{fontSize:10,color:muted,hideOverlap:true},axisLine:{lineStyle:{color:'#d9e6ec'}},axisTick:{show:false}},
    yAxis:{type:'value',name:unit,nameTextStyle:{color:muted,fontSize:10,align:'left'},nameGap:15,axisLabel:{fontSize:10,color:muted},splitLine:{lineStyle:{color:gridColor,type:'dashed'}}}
  };}
  function lineBar(r,ks,ps,kind){
    const unit=S(ks[0])?.unit||'',o=base(r.type==='baseline'?'基期=100':unit);o.xAxis.data=ps;
    const share=kind==='share',stack=kind==='stacked'||kind==='area'||share;
    if(share)o.yAxis={...o.yAxis,name:'%',min:0,max:100,axisLabel:{color:muted,fontSize:10,formatter:v=>v+'%'}};
    o.series=ks.map((k,i)=>{
      let data=ps.map(p=>V(k,p));
      if(share)data=ps.map(p=>{const row=ks.map(key=>V(key,p));const total=row.reduce((s,x)=>s+(x||0),0);return row.every(Number.isFinite)&&total>0?100*V(k,p)/total:null;});
      if(r.type==='baseline'){const b=V(k,r.base);data=ps.map(p=>Number.isFinite(b)&&b!==0&&Number.isFinite(V(k,p))?V(k,p)/b*100:null);}
      const bar=kind==='bar'||kind==='stacked',c=color(k,i);
      const s={id:k+'|'+(share?'%':r.type==='baseline'?'基期=100':unit),name:S(k).label,type:bar?'bar':'line',data,
        showSymbol:false,symbol:'circle',symbolSize:6,connectNulls:false,barMaxWidth:27,
        lineStyle:{width:2,color:c},itemStyle:{color:c,borderRadius:stack?0:[3,3,0,0]},emphasis:{focus:'series'}};
      if(stack)s.stack='total';if(kind==='area'||share)s.areaStyle={color:c,opacity:.86};
      if(i===0)s.markLine={silent:true,symbol:'none',animation:false,label:{show:false},lineStyle:{color:'#a8bbc4',type:'dashed',width:1},data:[{xAxis:state.period}]};
      if(kind==='bar')s.data=data.map((v,j)=>({value:v,itemStyle:{color:v<0?'#d8897a':ps[j]===state.period?D.accent:'#a0cfd3'}}));
      return s;
    });return o;
  }
  function buildOption(r){
    const ks=keysFor(r),ps=periods(),period=effectivePeriod(r,ks);
    if(!ks.length)return {empty:'所选学段无此口径指标',period,ks};
    const pairs=ks.map((k,i)=>({key:k,name:S(k).label,value:V(k,period),color:color(k,i)})).filter(x=>Number.isFinite(x.value));
    let o,kind=r.type;
    if(['line','bar','area','stacked','share','baseline'].includes(kind))return {option:lineBar(r,ks,ps,kind==='baseline'?'line':kind),period,ks};
    if(kind==='combo'){
      o=base(S(ks[0]).unit);o.grid.right=23;o.xAxis.data=ps;o.yAxis=[o.yAxis,{...o.yAxis,position:'right',name:S(ks[1]).unit,splitLine:{show:false}}];
      o.series=ks.map((k,i)=>({id:k+'|'+S(k).unit,name:S(k).label+(k.includes('_growth')?'实际同比':''),type:i?'line':'bar',yAxisIndex:i,data:ps.map(p=>i?V(k,p):{value:V(k,p),itemStyle:{color:p===state.period?D.accent:'#badfe1'}}),barMaxWidth:31,showSymbol:false,lineStyle:{width:2.6,color:'#e8a23b'},itemStyle:{color:i?'#e8a23b':D.accent}}));
      o.series[0].markLine={silent:true,symbol:'none',label:{show:false},lineStyle:{color:'#adc0c9',type:'dashed'},data:[{xAxis:state.period}]};
    }else if(kind==='rank'){
      const rows=pairs.sort((a,b)=>b.value-a.value).slice(0,r.limit||30).reverse();o=base(S(ks[0]).unit,true);o.legend.show=false;
      o.xAxis={...o.xAxis,type:'value',name:S(ks[0]).unit,nameTextStyle:{color:muted,fontSize:10},splitLine:{lineStyle:{color:gridColor,type:'dashed'}}};
      o.yAxis={type:'category',data:rows.map(x=>short(x.name)),axisLabel:{fontSize:small()?10:11,color:muted},axisTick:{show:false},axisLine:{show:false}};
      o.series=[{id:'rank|'+S(ks[0]).unit,name:S(ks[0]).unit,type:'bar',barMaxWidth:19,data:rows.map(x=>({value:x.value,itemStyle:{color:x.value<0?'#d8897a':D.accent,borderRadius:[0,3,3,0]}})),label:{show:true,position:'right',fontSize:10,color:muted,formatter:p=>fmt(p.value,Math.abs(p.value)>=1000?0:1)}}];
    }else if(['treemap','donut','rose'].includes(kind)){
      if(!pairs.length)return {empty:'该期未公布结构数据',period,ks};
      o=base();o.grid=undefined;o.xAxis=undefined;o.yAxis=undefined;o.legend.show=kind!=='treemap';
      o.tooltip={...o.tooltip,trigger:'item',formatter:p=>'<b>'+esc(p.name)+'</b><br>'+fmt(p.value,Math.abs(p.value)>=1000?0:2)+' '+esc(S(ks[0]).unit)+(p.percent!=null?'<br>占比 '+fmt(p.percent,1)+'%':'')};
      if(kind==='treemap'){
        o.series=[{type:'treemap',left:12,right:12,top:7,bottom:13,roam:false,nodeClick:false,breadcrumb:{show:false},visibleMin:0,
          label:{show:true,fontSize:small()?10:12,color:'#041015',formatter:p=>short(p.name)+'\n'+fmt(p.value,Math.abs(p.value)>=1000?0:1)},
          itemStyle:{borderWidth:2,borderColor:'#fff',gapWidth:2},data:pairs.filter(x=>x.value>0).map(x=>({name:x.name,value:x.value,itemStyle:{color:x.color}}))}];
      }else{
        o.legend={...o.legend,top:undefined,bottom:4,left:10,right:10};
        o.series=[{type:'pie',radius:kind==='rose'?['18%','70%']:['43%','71%'],center:['50%','44%'],roseType:kind==='rose'?'area':undefined,
          label:{show:!small()&&pairs.length<=6,fontSize:10,color:muted,formatter:p=>short(p.name)+' '+fmt(p.percent,1)+'%'},
          labelLine:{length:8,length2:5},avoidLabelOverlap:true,itemStyle:{borderColor:'#fff',borderWidth:2},
          data:pairs.map(x=>({name:x.name,value:x.value,itemStyle:{color:x.color}}))}];
        if(kind==='donut')o.graphic=[{type:'text',left:'center',top:'37%',style:{text:period+'年',fill:ink,fontSize:small()?16:19,fontWeight:700}},{type:'text',left:'center',top:'46%',style:{text:'结构占比',fill:muted,fontSize:11}}];
      }
    }else if(kind==='heatmap'||kind==='correlation'||kind==='calendar'){
      let xs=ps,ys=ks.map(k=>short(S(k).label)),data=[],max=0;
      if(kind==='heatmap'){
        ks.forEach((k,yi)=>ps.forEach((p,xi)=>{let v=r.transform==='yoy'?yoy(k,p):V(k,p);if(Number.isFinite(v)){max=Math.max(max,Math.abs(v));data.push([xi,yi,v]);}}));
        max=r.transform==='yoy'?Math.min(50,Math.max(5,max)):Math.max(5,max);
      }else if(kind==='calendar'){
        xs=['Q1','Q2','Q3','Q4'];ys=[...new Set(ps.map(p=>p.slice(0,4)))];
        ps.forEach(p=>{let v=V(ks[0],p);if(Number.isFinite(v)){max=Math.max(max,v);data.push([Number(p.at(-1))-1,ys.indexOf(p.slice(0,4)),v]);}});
      }else{
        xs=ys;max=1;
        ks.forEach((a,yi)=>ks.forEach((b,xi)=>{const rows=ps.map(p=>[V(a,p),V(b,p)]).filter(r=>r.every(Number.isFinite));let v=correlation(rows);if(v!=null)data.push([xi,yi,v,rows.length]);}));
      }
      if(!data.length)return {empty:kind==='correlation'?'至少需要3个共同有效观测值':'该区间没有可比较的数据',period,ks};
      o=base();o.legend.show=false;o.grid={left:12,right:kind==='correlation'?23:17,top:39,bottom:kind==='correlation'?88:44,containLabel:true};
      o.xAxis={type:'category',data:xs,splitArea:{show:false},axisTick:{show:false},axisLine:{show:false},axisLabel:{fontSize:10,color:muted,rotate:kind==='correlation'?45:0,hideOverlap:true,formatter:v=>kind==='correlation'?short(v).slice(0,7):v}};
      o.yAxis={type:'category',data:ys,axisTick:{show:false},axisLine:{show:false},axisLabel:{fontSize:10,color:muted,formatter:v=>short(v).slice(0,10)}};
      o.visualMap={min:kind==='calendar'?0:-max,max,orient:'horizontal',left:'center',top:0,itemWidth:9,itemHeight:85,calculable:false,textStyle:{color:muted,fontSize:9},text:kind==='correlation'?['1','−1']:kind==='calendar'?[fmt(max,1),'0']:[signed(max,0)+'%',signed(-max,0)+'%'],inRange:{color:kind==='calendar'?['#edf5f7','#9dcdd3','#16899a']:['#d77566','#fbfaf8','#168b9b']},dimension:2};
      o.series=[{type:'heatmap',data:data.map(d=>({value:d})),itemStyle:{borderWidth:2,borderColor:'#fff'},label:{show:data.length<230&&(!small()||kind!=='heatmap'),color:'#041015',fontSize:small()?9:10,formatter:p=>fmt(p.value[2],kind==='correlation'?2:kind==='calendar'?1:0)+(kind==='heatmap'?'%':'')},emphasis:{itemStyle:{borderWidth:2,borderColor:D.accent}}}];
      o.tooltip={...o.tooltip,trigger:'item',formatter:p=>'<b>'+esc(ys[p.value[1]])+' · '+esc(xs[p.value[0]])+'</b><br>'+fmt(p.value[2],2)+(kind==='correlation'?'　r<br>共同观测 n='+p.value[3]:kind==='calendar'?' '+S(ks[0]).unit:'%')};
    }else if(kind==='scatter'){
      o=base();o.legend.show=false;o.grid.bottom=37;
      const allKeys=r.keys,rows=ks.map(k=>{let i=allKeys.indexOf(k);return {key:k,name:S(k).label,x:V(k),y:V(r.ykeys[i]),size:r.sizekeys?V(r.sizekeys[i]):V(k)};}).filter(x=>[x.x,x.y].every(Number.isFinite));
      const biggest=Math.max(1,...rows.map(x=>x.size||0));
      o.xAxis={...o.xAxis,type:'value',name:S(ks[0]).unit,nameLocation:'middle',nameGap:25,scale:true,splitLine:{lineStyle:{color:gridColor}}};o.yAxis={...o.yAxis,name:S(r.ykeys[0]).unit,scale:true};
      o.series=[{type:'scatter',data:rows.map((x,i)=>({name:x.name,value:[x.x,x.y,x.size],symbolSize:17+Math.sqrt(Math.max(0,x.size||0)/biggest)*29,itemStyle:{color:color(x.key,i),opacity:.85}})),label:{show:true,formatter:p=>short(p.name),position:'top',fontSize:10,color:muted},labelLayout:{hideOverlap:true}}];
      o.tooltip={...o.tooltip,trigger:'item',formatter:p=>'<b>'+esc(p.name)+'</b><br>'+fmt(p.value[0],2)+' '+esc(S(ks[0]).unit)+'<br>'+fmt(p.value[1],2)+' '+esc(S(r.ykeys[0]).unit)};
    }else if(kind==='slope'){
      const validPs=ps.filter(p=>p<=state.period);const first=validPs.find(p=>ks.some(k=>Number.isFinite(V(k,p))));if(!first)return {empty:'没有可比较的起点',period,ks};
      o=base(S(ks[0]).unit);o.grid.left=23;o.grid.right=50;o.xAxis.data=[first,state.period];o.legend.top=1;
      o.series=ks.filter(k=>Number.isFinite(V(k,first))&&Number.isFinite(V(k))).map((k,i)=>({id:k+'|'+S(k).unit,name:S(k).label,type:'line',data:[V(k,first),V(k)],symbol:'circle',symbolSize:6,lineStyle:{width:2,color:color(k,i)},itemStyle:{color:color(k,i)},label:{show:true,position:'top',fontSize:9,formatter:p=>fmt(p.value,p.value>=1000?0:1),color:muted},labelLayout:{hideOverlap:true}}));
    }else if(kind==='butterfly'){
      const rows=ks.map(k=>{let i=r.keys.indexOf(k);return {name:short(S(k).label),left:V(k),right:V(r.rightkeys[i])};}).filter(x=>Number.isFinite(x.left)||Number.isFinite(x.right));
      o=base('万人',true);o.xAxis={...o.xAxis,type:'value',axisLabel:{fontSize:10,color:muted,formatter:v=>fmt(Math.abs(v),0)},splitLine:{lineStyle:{color:gridColor}}};o.yAxis={type:'category',data:rows.map(x=>x.name),axisLabel:{color:muted,fontSize:11},axisLine:{show:false},axisTick:{show:false}};
      o.series=[{name:'招生',type:'bar',stack:'flow',barMaxWidth:20,data:rows.map(x=>Number.isFinite(x.left)?-x.left:null),itemStyle:{color:palette[1]}},{name:'毕业',type:'bar',stack:'flow',data:rows.map(x=>x.right),itemStyle:{color:palette[3]}}];
      o.tooltip={...o.tooltip,formatter:params=>'<b>'+esc(params[0].name)+'</b>'+params.map(p=>'<br>'+p.marker+esc(p.seriesName)+'　'+fmt(Math.abs(p.value),1)+' 万人').join('')};
    }else if(kind==='mirror'){
      o=base('亿人次');o.xAxis.data=ps;o.series=ks.map((k,i)=>({id:k+'|亿人次',name:S(k).label+(i===1?'（向下）':''),type:i===2?'line':'bar',data:ps.map(p=>Number.isFinite(V(k,p))?V(k,p)*(i===1?-1:1):null),barMaxWidth:26,showSymbol:false,lineStyle:{width:2,color:palette[2]},itemStyle:{color:[palette[0],palette[5],palette[2]][i]}}));
      o.tooltip={...o.tooltip,formatter:params=>'<b>'+esc(params[0].name)+'</b>'+params.map((p,i)=>'<br>'+p.marker+esc(p.seriesName)+'　'+fmt(i===1?Math.abs(p.value):p.value,2)+' 亿人次').join('')};
    }else if(kind==='parallel'){
      const axes=[['students','在校生\n万人'],['teachers','专任教师\n万人'],['schools','学校\n所'],['ratio','学生/教师\n人']];
      const rows=(D.categories||[]).filter(c=>state.categories.has(c.id)).map(c=>({id:c.id,name:c.label,value:axes.map(([metric])=>V(metric+'_'+c.id))})).filter(r=>r.value.every(Number.isFinite));
      o=base();o.xAxis=o.yAxis=o.grid=undefined;o.color=rows.map(r=>color('students_'+r.id));o.legend.data=rows.map(r=>r.name);
      o.parallel={left:44,right:42,top:82,bottom:24,parallelAxisDefault:{type:'value',nameLocation:'end',nameTextStyle:{color:muted,fontSize:10,lineHeight:14},axisLine:{lineStyle:{color:'#c8dbe3'}},axisLabel:{fontSize:9,color:muted}}};
      o.parallelAxis=axes.map(([,name],dim)=>({dim,name,min:0,max:Math.ceil(Math.max(1,...rows.map(r=>r.value[dim]))*1.05)}));o.series=rows.map(r=>({name:r.name,type:'parallel',lineStyle:{width:2,opacity:.8,color:color('students_'+r.id)},data:[{name:r.name,value:r.value}]}));
      o.tooltip={...o.tooltip,trigger:'item',formatter:p=>'<b>'+esc(p.seriesName)+'</b>'+axes.map(([,label],i)=>'<br>'+label.replace('\n',' ')+'：'+fmt(p.value[i],i===2?0:1)).join('')};
    }else if(kind==='seasonal'){
      o=base(S(ks[0]).unit);o.xAxis.data=['Q1','Q2','Q3','Q4'];const years=[...new Set(ps.map(p=>p.slice(0,4)))];
      o.series=years.map((y,i)=>({id:y+'|'+S(ks[0]).unit,name:y+'年',type:'line',data:[1,2,3,4].map(q=>ps.includes(y+'Q'+q)?V(ks[0],y+'Q'+q):null),connectNulls:false,symbol:'circle',symbolSize:5,lineStyle:{width:y===state.period.slice(0,4)?3:1.7,color:palette[i]},itemStyle:{color:palette[i]}}));
    }else if(kind==='radar'){
      const first=ps[0],rows=[first,state.period];o=base();o.xAxis=o.yAxis=o.grid=undefined;
      o.radar={indicator:ks.map(k=>({name:short(S(k).label),max:100})),center:['50%','53%'],radius:'64%',axisName:{color:muted,fontSize:11},splitArea:{areaStyle:{color:['#fff','#f8fbfc']}}};
      o.series=[{type:'radar',data:rows.map((p,i)=>({name:p,value:ks.map(k=>V(k,p)),lineStyle:{width:2,color:palette[i]},itemStyle:{color:palette[i]},areaStyle:{color:palette[i],opacity:.08}}))}];o.legend.data=rows;o.tooltip={...o.tooltip,trigger:'item'};
    }else if(kind==='waterfall'){
      const prev=D.periods[D.periods.indexOf(state.period)-1],a=V(ks[0],prev),b=V(ks[0]);if(!Number.isFinite(a)||!Number.isFinite(b))return {empty:'缺少上一个季度的规模数据',period,ks};
      o=base(S(ks[0]).unit);o.legend.show=false;o.xAxis.data=[prev,'规模差额',state.period];let delta=b-a;
      o.series=[{name:'辅助',type:'bar',stack:'total',data:[0,Math.min(a,b),0],itemStyle:{color:'transparent'},emphasis:{disabled:true},tooltip:{show:false}},
        {name:'规模',type:'bar',stack:'total',barMaxWidth:46,data:[{value:a,itemStyle:{color:'#a4cfd3'}},{value:Math.abs(delta),itemStyle:{color:delta>=0?palette[3]:palette[5]}},{value:b,itemStyle:{color:D.accent}}],label:{show:true,position:'top',fontSize:11,color:muted,formatter:p=>p.dataIndex===1?signed(delta,2):fmt(p.value,2)}}];
      o.tooltip={...o.tooltip,formatter:params=>{let p=params.find(x=>x.seriesName!=='辅助');return p?esc(p.name)+'<br>'+fmt(p.dataIndex===1?delta:p.value,2)+' '+S(ks[0]).unit:'';}};
    }else if(kind==='dot'){
      const prev=D.periods[D.periods.indexOf(state.period)-1],rows=ks.map((k,i)=>[V(k,prev),V(k),i]).filter(r=>r.slice(0,2).every(Number.isFinite));if(!rows.length)return {empty:'缺少相邻时期对比值',period,ks};
      o=base('%',true);o.xAxis={...o.xAxis,type:'value',splitLine:{lineStyle:{color:gridColor}}};o.yAxis={type:'category',data:ks.map(k=>short(S(k).label)),axisLabel:{color:muted,fontSize:11},axisTick:{show:false},axisLine:{show:false}};
      o.legend.data=[prev||'上期',state.period];
      o.series=[{name:'辅助',type:'custom',silent:true,renderItem:(p,api)=>{let a=api.coord([api.value(0),api.value(2)]),b=api.coord([api.value(1),api.value(2)]);return {type:'line',shape:{x1:a[0],y1:a[1],x2:b[0],y2:b[1]},style:{stroke:'#c4dbe1',lineWidth:3}};},data:rows},
        {name:prev||'上期',type:'scatter',symbolSize:10,data:rows.map(r=>[r[0],r[2]]),itemStyle:{color:'#a6bcc6'}},
        {name:state.period,type:'scatter',symbolSize:12,data:rows.map(r=>[r[1],r[2]]),itemStyle:{color:D.accent}}];
      o.tooltip={...o.tooltip,trigger:'item',formatter:p=>esc(p.seriesName)+'<br>'+esc(ks[p.value[1]]?S(ks[p.value[1]]).label:'')+'：'+fmt(p.value[0],1)+'%'};
    }
    if(!o)return {empty:'暂不支持该图形',period,ks};return {option:o,period,ks};
  }
  function correlation(rows){if(rows.length<3)return null;const n=rows.length,ax=rows.reduce((s,r)=>s+r[0],0)/n,ay=rows.reduce((s,r)=>s+r[1],0)/n;let xx=0,yy=0,xy=0;rows.forEach(([x,y])=>{xx+=(x-ax)**2;yy+=(y-ay)**2;xy+=(x-ax)*(y-ay);});return xx&&yy?xy/Math.sqrt(xx*yy):null;}
  function renderChart(r){
    const el=$('chart-'+r.id),built=buildOption(r),tag=$('vintage-'+r.id);
    tag.textContent=built.period;tag.hidden=!r.asof&&built.period===state.period;
    el.setAttribute('aria-label',r.title+'，观察期 '+state.period+(built.period!==state.period?'，实际数据年 '+built.period:''));
    el.dataset.period=built.period;el.dataset.chartType=r.type;
    if(built.empty){instances.get(r.id)?.dispose();instances.delete(r.id);el.innerHTML='<div class="chart-empty"><strong>'+esc(built.empty)+'</strong><span>可扩大区间或调整观察时期</span></div>';el.dataset.rendered='empty';return;}
    if(!instances.has(r.id)){el.replaceChildren();const instance=echarts.init(el,null,{renderer:small()?'svg':'canvas',devicePixelRatio:Math.min(window.devicePixelRatio||1,2)});instances.set(r.id,instance);instance.on('finished',()=>{el.dataset.settled='true';});instance.on('click',p=>{const candidate=p.name||p.axisValue;if(D.periods.includes(candidate))setPeriod(candidate);else if(p.value&&Array.isArray(p.value)&&r.type==='heatmap'){const target=periods()[p.value[0]];if(target)setPeriod(target);}});}
    el.dataset.settled='false';
    const instance=instances.get(r.id);instance.setOption(built.option,true);el.dataset.rendered='true';
  }
  function renderCards(){
    $('kpis').innerHTML=D.cards.map(c=>{
      const p=c.vintage?latest(c.key):state.period,v=p?V(c.key,p):null;
      let display=v,unit=S(c.key).unit,digits=c.digits??1;
      if(['population','students_total'].includes(c.key)&&Number.isFinite(v)){display=v/10000;unit='亿人';digits=2;}
      if(c.key==='fund_total'&&Number.isFinite(v)){display=v/10000;unit='万亿元';digits=2;}
      let change='该期未公布';
      if(Number.isFinite(v)){
        if(c.delta_kind==='official')change='实际同比 <b class="'+(V(c.delta)>=0?'pos':'neg')+'">'+signed(V(c.delta),1)+'%</b>';
        else if(c.delta_kind==='pp'){
          const prior=D.periods[D.periods.indexOf(p)-1],before=V(c.key,prior),diff=Number.isFinite(before)?v-before:null;
          change=Number.isFinite(diff)?'较上期 <b class="'+(diff>=0?'pos':'neg')+'">'+signed(diff,1)+' pp</b>':'首个可比观察期';
        }else{
          const diff=yoy(c.key,p);change=Number.isFinite(diff)?'同比 <b class="'+(diff>=0?'pos':'neg')+'">'+signed(diff,1)+'%</b>':'没有同口径上年基期';
        }
      }
      return '<article class="kpi"><div class="kpi-top"><span class="kpi-label">'+esc(c.label)+'</span>'+(p&&p!==state.period?'<span class="kpi-vintage">'+esc(p)+'年</span>':'')+'</div><div class="kpi-value">'+fmt(display,digits)+'<span class="kpi-unit">'+esc(unit)+'</span></div><div class="kpi-change">'+change+'</div></article>';
    }).join('');
  }
  function renderInsight(){
    const period=state.period;let html='';
    if(D.id==='economy'){
      let group=D.charts.find(c=>c.id==='rank').keys.map(k=>({k,v:V(k)})).filter(x=>Number.isFinite(x.v)).sort((a,b)=>b.v-a.v),best=group[0],worst=group.at(-1);
      html='GDP '+(state.mode==='current'?'当季':'累计')+'现价规模 <b>'+fmt(V('gdp_@'),2)+' 万亿元</b>，实际同比 <b>'+signed(V('gdp_growth_@'),1)+'%</b>；第三产业占 <b>'+fmt(V('share3_@'),1)+'%</b>。'+(best?'所列行业中，'+esc(short(S(best.k).label))+'增长最快（'+signed(best.v,1)+'%），'+esc(short(S(worst.k).label))+'为'+signed(worst.v,1)+'%。':'');
    }else if(D.id==='tourism'){
      const b=V('trips','2019'),recovery=b&&V('trips')/b*100;
      html='国内出游 <b>'+fmt(V('trips'),2)+' 亿人次</b>，总花费 <b>'+fmt(V('spending'),2)+' 万亿元</b>，每人次花费 <b>'+fmt(V('per_trip'),0)+' 元</b>。'+(Number.isFinite(recovery)?'出游规模相当于2019年的 <b>'+fmt(recovery,1)+'%</b>。':'')+'结构明细按各自实际公布年份展示。';
    }else if(D.id==='education'){
      const keys=[...state.categories].map(c=>'students_'+c),rows=keys.map(k=>({k,v:V(k)})).filter(x=>Number.isFinite(x.v)).sort((a,b)=>b.v-a.v);
      html='所选 <b>'+state.categories.size+' 类学段</b>在校生合计 <b>'+fmt(V('students_total'),1)+' 万人</b>。'+(rows[0]?esc(S(rows[0].k).label)+'规模最大，为 <b>'+fmt(rows[0].v,1)+' 万人</b>。':'')+'学段学生统计与全国教育经费覆盖范围不同，分别解读。';
    }else{
      html='年末总人口 <b>'+fmt(V('population')/10000,2)+' 亿人</b>，城镇化率 <b>'+fmt(V('urbanization'),2)+'%</b>，65岁及以上占 <b>'+fmt(V('old_share'),2)+'%</b>。'+(Number.isFinite(V('income'))?'居民人均可支配收入 <b>'+fmt(V('income'),0)+' 元</b>，城乡收入比 <b>'+fmt(V('urban_rural_ratio'),2)+' 倍</b>。':'该年统一居民收支序列尚未公布。');
    }
    $('insight').innerHTML='<strong>'+esc(period)+' 速读</strong>'+html;
  }
  function renderTable(){
    const series=Object.values(D.series).filter(s=>!D.mode_switch||!s.id.endsWith(state.mode==='current'?'_cumulative':'_current'));
    $('detailRows').innerHTML=series.map(s=>'<tr><td>'+esc(measureLabel(s))+'</td><td>'+fmt(V(s.id),Math.abs(V(s.id))>=1000?0:2)+'</td><td>'+esc(s.unit)+'</td><td>'+esc(state.period)+'</td></tr>').join('');
  }
  function render(){
    $('period').value=state.period;$('timeline').value=D.periods.indexOf(state.period);$('timeline').min=D.periods.indexOf(state.start);$('timeline').max=D.periods.indexOf(state.end);
    $('rangeStart').value=state.start;$('rangeEnd').value=state.end;
    $('prev').disabled=state.period===state.start;$('next').disabled=state.period===state.end;
    document.body.dataset.period=state.period;document.body.dataset.mode=state.mode;
    renderCards();renderInsight();D.charts.forEach(renderChart);renderTable();
    document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===state.mode)));
    document.querySelectorAll('.section-status').forEach(s=>s.textContent=state.period+' · '+(D.mode_switch?(state.mode==='current'?'当季值':'累计值'):'年度数据'));
    document.querySelectorAll('#period option').forEach(o=>o.disabled=o.value<state.start||o.value>state.end);
    if(expandedRecipe&&$('chartDialog').open){const b=buildOption(expandedRecipe);if(b.option)expanded.setOption(b.option,true);}
    history.replaceState(null,'','#period='+encodeURIComponent(state.period)+'&start='+state.start+'&end='+state.end+'&mode='+state.mode);
  }
  function setPeriod(p,manual=true){if(!D.periods.includes(p))return;if(manual)stop();state.period=p<state.start?state.start:p>state.end?state.end:p;render();}
  function download(currentOnly=false){
    const rows=[['主题','指标','时期','数值','单位','数据类型']];
    Object.values(D.series).filter(s=>!D.mode_switch||!s.id.endsWith(state.mode==='current'?'_cumulative':'_current')).forEach(s=>(currentOnly?[state.period]:periods()).forEach(p=>rows.push([D.title,measureLabel(s),p,V(s.id,p)??'',s.unit,s.derived_from?'计算指标':'官方发布值（单位转换后）'])));
    const csv='\ufeff'+rows.map(r=>r.map(v=>'"'+String(v).replaceAll('"','""')+'"').join(',')).join('\r\n');
    const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download=D.title+'_'+(currentOnly?state.period:state.start+'_'+state.end)+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('已导出当前筛选数据');
  }
  function expand(r){
    stop();expandedRecipe=r;const shownPeriod=effectivePeriod(r,keysFor(r));$('expandedTitle').textContent=r.title+' · '+shownPeriod+' · '+S(r.keys[0]).unit;$('chartDialog').showModal();
    requestAnimationFrame(()=>{expanded?.dispose();expanded=echarts.init($('expandedChart'));const built=buildOption(r);if(built.option)expanded.setOption(built.option,true);else expanded.setOption({graphic:{type:'text',left:'center',top:'middle',style:{text:built.empty,fill:muted,fontSize:16}}});});
  }
  const sectionDescriptions={
    '总量与周期':'以现价看规模，以不变价与季调数据看增长','结构与贡献':'三次产业与三大需求，分开观察规模和增长贡献','行业分化':'从行业总量延伸到实际增长差异','周期与比较':'放回季度节奏，比较起点与观察期',
    '需求与复苏':'规模、花费与2019年基准对照','消费结构':'城乡客群、消费结构与人均花费','国际旅游':'双向出行与国际旅游收入','客源与供给':'列示客源国家、旅行社和星级饭店','关联与变化':'观察共同变化，不把相关写成因果',
    '规模与结构':'六类学段的在校生与资源结构','流动与师资':'招生、毕业与教师资源的分化','资源配置':'学校规模、教师数量与学生结构','教育投入':'全国教育经费及其来源，独立于所选学段',
    '人口与城镇化':'人口总量、自然变化与城乡分布','结构与抚养':'年龄结构与抚养压力的共同变化','收入与分配':'城乡差异、收入来源与五等份分组','消费与生活':'收入与消费结构的变化','关联与分化':'在共同非缺失的时期上比较变化'};
  document.documentElement.style.setProperty('--accent',D.accent);
  document.documentElement.style.setProperty('--accent-soft',D.id==='education'||D.id==='population'?'#edf0fa':'#e5f4f5');
  $('pageTitle').textContent=D.title+'驾驶舱';$('pageSubtitle').textContent=D.subtitle+' · '+D.periods[0]+'—'+D.periods.at(-1)+' · '+D.periods.length+(D.mode_switch?'个季度':'年')+' · '+D.charts.length+'组图表';
  $('periodLabel').textContent=D.mode_switch?'观察季度':'观察年份';
  for(const id of ['period','rangeStart','rangeEnd'])$(''+id).innerHTML=D.periods.map(p=>'<option value="'+p+'">'+p+'</option>').join('');
  $('timeline').max=D.periods.length-1;
  $('modeSwitch').hidden=!D.mode_switch;
  if(D.categories){$('categoryFilters').hidden=false;$('categoryChoices').innerHTML=D.categories.map(c=>'<label><input type="checkbox" value="'+c.id+'" checked>'+esc(c.label)+'</label>').join('');}
  const sections=[...new Set(D.charts.map(c=>c.section))];
  $('content').innerHTML=sections.map(section=>{
    const recipes=D.charts.filter(r=>r.section===section),wideIndex=recipes.findIndex(r=>r.wide);
    return '<section class="chart-section"><div class="section-heading"><div><h2>'+esc(section)+'</h2><p>'+esc(sectionDescriptions[section]||'')+'</p></div><span class="section-status"></span></div><div class="chart-grid">'+recipes.map((r,i)=>{
      const span=wideIndex<0?6:i===wideIndex?8:Math.floor(i/2)===Math.floor(wideIndex/2)?4:6;
      let description=r.description||(r.type==='correlation'?'水平值 Pearson r · 共同有效观测':r.transform==='yoy'?'相邻年份同比（%）':r.type==='parallel'?'各轴保留实际单位':r.type==='baseline'?'基期 '+r.base+' = 100':r.type==='share'?'完整分类数据的构成占比（%）':'');
      if(['treemap','donut','rose','butterfly'].includes(r.type))description=(r.type==='butterfly'?'左：招生 · 右：毕业 · ':r.type==='rose'?'扇区面积表示金额 · ':'')+'单位：'+S(r.keys[0]).unit;
      return '<article class="panel" data-span="'+span+'"><div class="panel-heading"><div><h3>'+esc(r.title)+'</h3>'+(description?'<p class="panel-description">'+esc(description)+'</p>':'')+'</div><div class="panel-actions"><span class="vintage-tag" id="vintage-'+r.id+'" hidden></span><button class="expand-button" data-expand="'+r.id+'" aria-label="放大'+esc(r.title)+'"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 4H4v4m12-4h4v4M4 16v4h4m12-4v4h-4"/></svg></button></div></div><div class="chart" id="chart-'+r.id+'" role="img"></div></article>';
    }).join('')+'</div></section>';
  }).join('');
  $('sourceNotes').innerHTML=D.notes.map(n=>'<li>'+esc(n)+'</li>').join('');
  $('period').onchange=e=>setPeriod(e.target.value);$('timeline').oninput=e=>setPeriod(D.periods[+e.target.value]);
  $('prev').onclick=()=>setPeriod(D.periods[D.periods.indexOf(state.period)-1]);$('next').onclick=()=>setPeriod(D.periods[D.periods.indexOf(state.period)+1]);
  for(const id of ['rangeStart','rangeEnd'])$(id).onchange=()=>{stop();let start=$('rangeStart').value,end=$('rangeEnd').value;if(start>end){if(id==='rangeStart')end=start;else start=end;}state.start=start;state.end=end;setPeriod(state.period);};
  $('play').onclick=()=>{if(state.timer){stop();return;}if(state.period===state.end)state.period=state.start;render();$('play').textContent='暂停';$('play').setAttribute('aria-pressed','true');state.timer=setInterval(()=>{let next=D.periods[D.periods.indexOf(state.period)+1];if(!next||next>state.end){stop();return;}setPeriod(next,false);},1500);};
  $('reset').onclick=()=>{stop();state.period=D.default_period;state.start=D.periods[0];state.end=D.periods.at(-1);state.mode='current';state.categories=new Set((D.categories||[]).map(c=>c.id));document.querySelectorAll('#categoryChoices input').forEach(c=>c.checked=true);render();};
  document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>{stop();state.mode=b.dataset.mode;render();});
  document.querySelectorAll('#categoryChoices input').forEach(c=>c.onchange=()=>{if(!c.checked&&state.categories.size===1){c.checked=true;toast('至少保留一个学段');return;}c.checked?state.categories.add(c.value):state.categories.delete(c.value);stop();render();});
  document.querySelectorAll('[data-expand]').forEach(b=>b.onclick=()=>expand(D.charts.find(r=>r.id===b.dataset.expand)));
  $('downloadCsv').onclick=()=>download(false);$('downloadSnapshot').onclick=()=>download(true);
  $('openSources').onclick=()=>{stop();$('sourceDialog').showModal();};
  document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>$(b.dataset.close).close());
  $('savePng').onclick=()=>{if(!expanded)return;const a=document.createElement('a');a.href=expanded.getDataURL({type:'png',pixelRatio:2,backgroundColor:'#fff'});a.download=D.id+'_'+expandedRecipe.id+'_'+state.period+'.png';a.click();};
  $('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{toast('此浏览器暂不支持全屏，可使用浏览器全屏功能');}};
  $('chartDialog').addEventListener('close',()=>{expanded?.dispose();expanded=null;expandedRecipe=null;});
  let resizeTimer,wasSmall=small();window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{if(wasSmall!==small()){wasSmall=small();instances.forEach(c=>c.dispose());instances.clear();render();}else instances.forEach(c=>c.resize());expanded?.resize();},100);});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  const hash=new URLSearchParams(location.hash.slice(1));if(D.periods.includes(hash.get('period')))state.period=hash.get('period');
  if(D.periods.includes(hash.get('start')))state.start=hash.get('start');if(D.periods.includes(hash.get('end')))state.end=hash.get('end');
  if(state.start>state.end){state.start=D.periods[0];state.end=D.periods.at(-1);}if(state.period<state.start||state.period>state.end)state.period=state.end;
  if(D.mode_switch&&hash.get('mode')==='cumulative')state.mode='cumulative';
  try{render();document.body.dataset.ready='true';}catch(error){document.body.dataset.ready='error';$('insight').textContent='图表加载失败，请检查离线资源是否完整。';console.error(error);}
})();
