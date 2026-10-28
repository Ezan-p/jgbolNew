local ms=assert(package.loaded.ms)
local ui=assert(ms.d_tianShuUI)
local saved,checks={},{}
local function replace(t,k,v) saved[#saved+1]={t=t,k=k,v=t[k]};t[k]=v end
local function check(name,fn)
 local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]=name..':'..tostring(ok)..':'..(err or '')
end
local originallyPatched=ui._localTianShuRestore~=nil
local ok,err=xpcall(function()
 for _,k in ipairs({'g_taskConfig','goldConfig','g_monthCardTag','g_taskProgressTable','g_taskPrizeTable','bit',
  'g_FirstMenuItem','g_SecondMenuItem','g_takePrizeTag','g_isAllPrizeTaken','g_currentParent','g_taskMenuItem','g_mainLayer','g_taskTableView','g_isInThisPage'}) do
  replace(ui,k,ui[k])
 end
 replace(ms.d_mainUI,'g_playerInfo',{role_id=1,level=99,task_progress=32766,task_prize=0})
 replace(ms.d_mainUI,'g_isNeedGuide',false)
 replace(ms.d_data,'g_new_config',{[2]=__REWARDS__,[4]={pay_consume_gold=20}})
 replace(ms.d_worldBossUI,'g_payFightGold',20)
 ui.g_taskConfig=nil
 __ADAPTER__
 check('native_config',function()
  ms.d_data.getGoldConfig();ui.getTaskConfig()
  assert(#ui.g_taskConfig==14)
  assert(ui.goldConfig[1][1].attach_count==20 and ui.goldConfig[7][1].attach_count==100)
  assert(ui.g_taskConfig[14].desc=='绑定本地游戏账号')
  assert(ui.g_monthCardTag==nil and ui.goldConfig[12][1].attach_count==50)
 end)
 check('native_bits_and_order',function()
  ui.getTaskStatus()
  assert(ui.g_taskProgressTable[1]==1 and ui.g_taskPrizeTable[1]==0)
  assert(ui.canTakenFirstPrize() and ui.canTakenPrize())
  assert(ui.getFirstPrizeIndex(ui.g_taskProgressTable,ui.g_taskPrizeTable)==1)
 end)
 for _,status in ipairs({'pending','ready','claimed'}) do
  check('native_cells_'..status,function()
   local player=ms.d_mainUI.g_playerInfo
   player.task_progress=status=='pending' and 0 or 32766
   player.task_prize=status=='claimed' and 32766 or 0
   ui.getTaskStatus()
   local parent=CCNode:create()
   for i=1,14 do ui.createCellOnAdvance(parent,i,CCSizeMake(600,150)) end
   assert(parent:getChildrenCount()>0)
  end)
 end
 local sent={}
 replace(ms.d_u,'main_server_send_msg',function(mid,data) sent[#sent+1]={mid=mid,data=data} end)
 check('native_claim_request',function()
  ui.getTaskPrize(10);assert(sent[#sent].mid==1201)
  assert(sent[#sent].data.flag==4 and sent[#sent].data.id==10)
 end)
 check('native_guide_claim_request',function()
  ms.d_mainUI.g_isNeedGuide=true
  ui.getTaskPrize(1);assert(sent[#sent].mid==1204 and sent[#sent].data.stage==13)
  ms.d_mainUI.g_isNeedGuide=false
 end)
 check('progress_and_claim_sync',function()
  ms.d_data.callback_update_config({local_tian_shu={task_progress=32766,task_prize=2}})
  ui.getTaskStatus();assert(ui.g_taskPrizeTable[1]==1 and ui.g_taskPrizeTable[10]==0)
  assert(ui.getFirstPrizeIndex(ui.g_taskProgressTable,ui.g_taskPrizeTable)==2)
 end)
 local destinations={}
 for _,name in ipairs({'gotoMap','gotoSubLevelMap','startEnhanceGuide','gotoPractice','gotoRankTask',
  'gotoCrossDoomTask','gotoEndlessFightTask','gotoPackage','gotoWorldBossTask','gotoRegisterInfo'}) do
  replace(ui,name,function() destinations[#destinations+1]=name end)
 end
 replace(ms.d_u,'remove',function() end)
 check('native_destinations',function()
  for _,id in ipairs({2,3,4,5,6,7,8,9,10,11,12,13,14}) do ui.gotoTakeTask(id) end
  assert(#destinations==13)
 end)
 replace(ui,'g_currentParent',{removeChildByTag=function() end})
 replace(ui,'g_taskMenuItem',{setVisible=function() end})
 replace(ui,'g_isInThisPage',false)
 local monthOpened=false
 replace(ms.d_monthCardUI,'show',function() monthOpened=true end)
 replace(ms.d_info,'show',function() end)
 check('native_reward_callback',function()
  ui.g_takePrizeTag=13
  ui.getTaskPrizeRes({task_stage=13,prize_list=ui.goldConfig[13]})
 end)
 check('native_level9_gold_callback',function()
  ui.g_takePrizeTag=12
  ui.getTaskPrizeRes({task_stage=12,prize_list=ui.goldConfig[12]})
  assert(not monthOpened)
 end)
 check('account_switch_clears_completion_cache',function()
  ms.d_mainUI.g_playerInfo.task_prize=32766;assert(ui.isAllPrizeTaken())
  ms.d_mainUI.g_playerInfo.task_prize=0;assert(not ui.isAllPrizeTaken())
 end)
end,debug.traceback)
if not originallyPatched and ui._localTianShuRestore then ui._localTianShuRestore() end
for i=#saved,1,-1 do local s=saved[i];s.t[s.k]=s.v end
if not ok then checks[#checks+1]='harness:false:'..err end
return table.concat(checks,'\n')
