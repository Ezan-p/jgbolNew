local source=...
local styles,queries={},0
local oldTip='每日完成指定任务可以获得活跃值，活跃值累计周一0点重置'
local layer={getParent=function() return true end}
local ui={g_day={},g_self={daily_main_layer=layer}}
local ms={d_checkinUI=ui,d_hz={gethz=function() return oldTip end},d_u={}}
ms.d_u.createByStyle=function(style) styles[#styles+1]=style;return style end
local create=ms.d_u.createByStyle
ui.showDaily=function(fail)
 ms.d_u.createByStyle({type='label',fontsize=26,string=oldTip})
 for i,row in ipairs(ui.g_day.data.point_data) do
  for _,x in ipairs({0.18,0.484}) do
   ms.d_u.createByStyle({type='label',fontsize=22,string=row.desc,x=x,y=0.6188-(i-1)*0.0528})
  end
 end
 ms.d_u.createByStyle({type='label',fontsize=22,string='chest',x=0.7,y=0.3})
 if fail then error('render failure') end
 return 'rendered'
end
ui.onGetResult=function(data)
 if data.id==1 then ui.g_day.data=data;ui.showDaily() end
 return 'native result'
end
ui.pressDaily=function() queries=queries+1 end
package.loaded.ms=ms
local show,result=ui.showDaily,ui.onGetResult
assert(loadstring(source))();assert(loadstring(source))()
local rows={}
for i=1,11 do rows[i]={desc='task '..i} end
assert(ui.onGetResult({id=1,local_day=20,point_data=rows})=='native result')
assert(#styles==24)
assert(styles[1].string:find('每日0点（北京时间）重置',1,true))
assert(not styles[1].string:find('周一',1,true))
for i=1,11 do
 local left,right=styles[i*2],styles[i*2+1]
 assert(math.abs(left.y-right.y)<0.00001)
 assert(math.abs(left.y-(0.6188-(i-1)*0.04224))<0.00001)
 assert(left.y>=0.1963 and left.fontsize==22)
end
assert(styles[24].x==0.7 and styles[24].y==0.3)
assert(ms.d_u.createByStyle==create)
assert(not pcall(ui.showDaily,true));assert(ms.d_u.createByStyle==create)
ui.onGetResult({id=3,local_day=20,has_prize=false});assert(queries==0)
ui.onGetResult({id=3,local_day=21,has_prize=false});assert(queries==1)
ui.onGetResult({id=1,local_day=21,point_data=rows})
ui.onGetResult({id=3,local_day=21,has_prize=false});assert(queries==1)
layer.getParent=function() return nil end
ui.onGetResult({id=3,local_day=22,has_prize=false});assert(queries==1)
layer.getParent=function() error('removed native node') end
ui.onGetResult({id=3,local_day=22,has_prize=false});assert(queries==1)
ui._localDailyRestore();assert(ui.showDaily==show and ui.onGetResult==result)
assert(loadstring(source))()
return 'Daily client: 11-row layout, daily wording, midnight refresh, closed panel, restoration passed'
