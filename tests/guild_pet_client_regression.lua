-- Lua 5.1 adapter checks with delayed native-style reward rendering.
local requests,delays,labels,messages,buttons={},{},{},{},{}
local now=100
local host={}
local function layer() return {getParent=function() return host end} end
local ui={g_self={},g_data={main={task_day=1,task_last_time=200,free_task_times=3,pay_task_times=1,union_task={{index=1},{index=2},{index=3}}}},g_pethuntUI={}}
local nativeCalls,taskOpens=0,0
ui.sendRequest=function(op,data) requests[#requests+1]={op=op,data=data} end
ui.showTaskLayer=function()
 taskOpens=taskOpens+1
 local function attempt(typ)
  local payment=(ui.g_data.main.free_task_times or 0)>0 and 1 or 2
  ui.sendRequest(84,{task_index=ui.g_self.cur_task_index,task_type=typ,pay_type=payment})
 end
 d_ms.d_u.createMenu({
  {npic='v2/pethuntUI/rtask1.png',call_back=function() attempt(1) end},
  {npic='v2/pethuntUI/ctask1.png',call_back=function() attempt(2) end},
  {npic='v2/pethuntUI/mtask1.png',call_back=function() attempt(2) end}})
 if failTask then error('native task render failure') end
end
ui.showMainLayer=function()
 ui.g_pethuntUI.main_layer=layer()
 local main=ui.g_data.main
 for i,task in ipairs(main.union_task) do
  d_ms.d_u.createMenu({{npic='v2/pethuntUI/challenge1.png',tag=i,call_back=function()
   if (main.wander_times or 0)>=5 then return d_ms.d_info.show('游历次数已满') end
   if (main.free_task_times or 0)<=0 and (main.pay_task_times or 0)<=0 then return d_ms.d_info.show('次数不足') end
   ui.showTaskLayer(nil,task)
  end}})
 end
 if failMain then error('native render failure') end
end
ui.showTaskFinish=function()
 d_ms.d_u.delay(ui.g_pethuntUI.main_layer,.75,function()
  for _,prize in ipairs(ui.g_data.task_finish.prize_list) do
   d_ms.d_data.getCertainSmallSprite(prize.object_type,prize.attach_type,prize.attach_level)
   local name=d_ms.d_data.getItemName(prize.attach_type)
   d_ms.d_u.createByStyle({type='label',y=.3,string=name..'X'..prize.attach_count})
  end
 end)
end
ui.onGetResult=function() nativeCalls=nativeCalls+1 end
local ms={d_pethuntUI=ui,d_fightUI={showFightEnd=function() end,menuHome_private=function() end},
 d_petHomeUI={GetResultInsidePetInfo=function() end,createShiLianLayer=function() end,GetResultPrize=function() end},
 d_time={getTime=function() return now end},d_info={show=function(s) messages[#messages+1]=s end},d_u={
  createMenu=function(options) for _,row in ipairs(options) do buttons[row.tag or row.npic]=row.call_back end end,
  delay=function(parent,wait,fn) delays[#delays+1]={parent=parent,wait=wait,fn=fn} end,
  createByStyle=function(options) labels[#labels+1]=options.string end},
 d_data={getCertainSmallSprite=function() end,getItemName=function(tid) assert(tid~=0,'currency is not an item ID');return '道具' end}}
d_ms=ms;package.loaded.ms=ms
local originals={send=ui.sendRequest,main=ui.showMainLayer,task=ui.showTaskLayer,finish=ui.showTaskFinish,result=ui.onGetResult}
dofile('network_redirect/guild_pet_client.lua')
local wrapped=ui.showMainLayer;dofile('network_redirect/guild_pet_client.lua');assert(wrapped==ui.showMainLayer)
ui.showMainLayer(host)
buttons[2]();assert(taskOpens==1 and ui.g_self.cur_task_index==2)
ui.showTaskLayer(nil,ui.g_data.main.union_task[3])
ui.sendRequest(84,{task_index=ui.g_self.cur_task_index,task_type=2})
assert(requests[1].data.task_index==3 and requests[1].data.task_day==1)
local latest={task_day=1,task_last_time=200,free_task_times=0,pay_task_times=0,wander_times=5,
 union_task={{index=1,completed=true},{index=2,completed=true},{index=3,completed=true}}}
ui.onGetResult(84,{result=1,task_type=1,task_index=3,fight_result=true,task_state=latest,
 prize_list={{object_type=5,attach_type=1001,attach_count=5},{object_type=12,attach_type=0,attach_count=3000}}})
assert(ui.g_data.main==latest and #latest.union_task==3 and nativeCalls==0)
local opens=taskOpens
for i=1,3 do buttons[i]();assert(messages[#messages]=='已挑战') end
assert(taskOpens==opens,'completed target opened a task dialog')
ui.showTaskLayer(nil,latest.union_task[3]);assert(taskOpens==opens and messages[#messages]=='已挑战')
for _,op in ipairs({84,85}) do ui.sendRequest(op,{task_index=3}) end
assert(#requests==1 and messages[#messages]=='已挑战','completed target sent another request')
local menu=ms.d_u.createMenu
failMain=true;assert(not pcall(ui.showMainLayer,host));failMain=false
assert(ms.d_u.createMenu==menu,'menu wrapper leaked after render failure')
local reward;for _,row in ipairs(delays) do if row.wait==.75 then reward=row.fn end end
assert(reward)();assert(labels[1]=='道具×5' and labels[2]=='银两×3000')
assert(not pcall(ms.d_data.getItemName,0),'currency fix leaked into shared helpers')
-- A partially completed target remains enterable even with five banked
-- encounters; only the already completed challenge type is blocked.
latest.pay_task_times=1
latest.union_task[3]={index=3,completed=false,completed_modes={true,false}}
ui.showMainLayer(host);buttons[3]()
assert(taskOpens==opens+1 and ui.g_self.cur_task_index==3,'sixth challenge blocked by native encounter cap')
local requestCount=#requests
buttons['v2/pethuntUI/rtask1.png']()
assert(#requests==requestCount and messages[#messages]=='已挑战')
buttons['v2/pethuntUI/ctask1.png']()
assert(#requests==requestCount+1 and requests[#requests].data.task_type==2 and requests[#requests].data.pay_type==2)
ui.sendRequest(84,{task_index=3,task_type=1,pay_type=2})
assert(#requests==requestCount+1,'completed leisure challenge sent a request')
-- Reverse the modes to verify that advanced completion also leaves leisure open.
latest.union_task[3].completed_modes={false,true}
latest.free_task_times=1
buttons['v2/pethuntUI/mtask1.png']()
assert(#requests==requestCount+1 and messages[#messages]=='已挑战')
ui.sendRequest(85,{task_index=3,pay_type=1})
assert(#requests==requestCount+1,'alternate advanced opcode bypassed completion')
buttons['v2/pethuntUI/rtask1.png']()
assert(requests[#requests].data.task_type==1 and requests[#requests].data.pay_type==1)
failTask=true;assert(not pcall(ui.showTaskLayer,nil,latest.union_task[3]));failTask=false
assert(ms.d_u.createMenu==menu,'task menu wrapper leaked after render failure')
latest.union_task[3].completed=true;latest.union_task[3].completed_modes={true,true}
now=200;delays={};requests={};ui.showMainLayer(host);assert(#delays==1)
local messageCount=#messages;buttons[1]();assert(#messages==messageCount,'stale completion blocked daily refresh')
delays[1].fn();assert(#requests==1 and requests[1].op==83)
ui.sendRequest(84,{task_index=3});assert(#requests==1,'stale task was sent or refresh duplicated')
ui.onGetResult(83,{result=1,task_day=2,task_last_time=300,union_task={{index=1},{index=2},{index=3}}})
assert(#ui.g_data.main.union_task==3 and ui.g_data.main.task_day==2)
ui.showTaskLayer(nil,ui.g_data.main.union_task[1]);ui.sendRequest(84,{task_index=1})
assert(requests[2].data.task_day==2)
local timer=delays[#delays].fn
now=300;timer();assert(#requests==3 and requests[3].op==83)
ui.onGetResult(83,{result=2})
ui.sendRequest(84,{task_index=1});assert(#requests==4 and requests[4].op==83,'failed refresh remained locked')
ms._localGuildPetRestore();timer();assert(#requests==4)
assert(ui.sendRequest==originals.send and ui.showMainLayer==originals.main and ui.showTaskLayer==originals.task and ui.showTaskFinish==originals.finish and ui.onGetResult==originals.result)
print('guild pet client regression passed: stable IDs, exact currency labels, retained completed targets, completed click priority, daily refresh, stale request guard, restore')
