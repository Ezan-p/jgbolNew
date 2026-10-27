-- Lua 5.1 adapter checks with delayed native-style reward rendering.
local requests,delays,labels={},{},{}
local now=100
local host={}
local function layer() return {getParent=function() return host end} end
local ui={g_self={},g_data={main={task_day=1,task_last_time=200,union_task={{index=1},{index=3}}}},g_pethuntUI={}}
local nativeCalls=0
ui.sendRequest=function(op,data) requests[#requests+1]={op=op,data=data} end
ui.showTaskLayer=function() end
ui.showMainLayer=function() ui.g_pethuntUI.main_layer=layer() end
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
 d_time={getTime=function() return now end},d_u={
  delay=function(parent,wait,fn) delays[#delays+1]={parent=parent,wait=wait,fn=fn} end,
  createByStyle=function(options) labels[#labels+1]=options.string end},
 d_data={getCertainSmallSprite=function() end,getItemName=function(tid) assert(tid~=0,'currency is not an item ID');return '道具' end}}
d_ms=ms;package.loaded.ms=ms
local originals={send=ui.sendRequest,main=ui.showMainLayer,task=ui.showTaskLayer,finish=ui.showTaskFinish,result=ui.onGetResult}
dofile('network_redirect/guild_pet_client.lua')
local wrapped=ui.showMainLayer;dofile('network_redirect/guild_pet_client.lua');assert(wrapped==ui.showMainLayer)
ui.showMainLayer(host)
ui.g_self.cur_task_index=2;ui.showTaskLayer(nil,ui.g_data.main.union_task[2])
ui.sendRequest(84,{task_index=ui.g_self.cur_task_index,task_type=2})
assert(requests[1].data.task_index==3 and requests[1].data.task_day==1)
local latest={task_day=1,task_last_time=200,union_task={}}
ui.onGetResult(84,{result=1,task_type=1,task_index=3,fight_result=true,task_state=latest,
 prize_list={{object_type=5,attach_type=1001,attach_count=5},{object_type=12,attach_type=0,attach_count=3000}}})
assert(ui.g_data.main==latest and #latest.union_task==0 and nativeCalls==0)
local reward;for _,row in ipairs(delays) do if row.wait==.75 then reward=row.fn end end
assert(reward)();assert(labels[1]=='道具×5' and labels[2]=='银两×3000')
assert(not pcall(ms.d_data.getItemName,0),'currency fix leaked into shared helpers')
now=200;delays={};requests={};ui.showMainLayer(host);assert(#delays==1)
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
print('guild pet client regression passed: stable IDs, exact currency labels, disappearing targets, daily refresh, stale request guard, restore')
