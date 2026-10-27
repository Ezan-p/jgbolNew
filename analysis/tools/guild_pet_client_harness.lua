local ms=assert(package.loaded.ms);local ui=ms.d_pethuntUI;local f=__FIXTURES__
assert(not guildPetRestore and not guild_fixture_restore)
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,guildConfig=ms.d_xianmengUI.guildConfig,
 self=ui.g_self,data=ui.g_data,panels=ui.g_pethuntUI,home=ms.d_petHomeUI.g_self,homeData=ms.d_petHomeUI.g_data,
 send=ms.d_u.main_server_send_msg,dispatch=ms.d_event_mgr.g_msg_fun,report=ms.MS_report_error,time=ms.d_time.getTime,
 menu=ms.d_u.createMenu,obtain=ms.d_petUI.getPetObtainLayer,act=ms.d_fightUI.actFight,patched=ms._localGuildPetRestore~=nil}
local function shallow(t) local c={};for k,v in pairs(t or {}) do c[k]=v end;return c end
local patchedFunctions={}
for _,entry in ipairs({{ui,'onGetResult'},{ui,'sendRequest'},{ui,'showTaskLayer'},{ui,'showMainLayer'},{ui,'showTaskFinish'},
 {ms.d_fightUI,'showFightEnd'},{ms.d_fightUI,'menuHome_private'},
 {ms.d_petHomeUI,'GetResultInsidePetInfo'},{ms.d_petHomeUI,'createShiLianLayer'},{ms.d_petHomeUI,'GetResultPrize'},
 {ms,'_localGuildPetRestore'}}) do patchedFunctions[#patchedFunctions+1]={entry[1],entry[2],entry[1][entry[2]]} end
local mapShow=ms.d_mapUI.show;local mapCalls=0
ms.d_mapUI.show=function(...) mapCalls=mapCalls+1;return mapShow(...) end
local taskRewards={};local rewardCount=0;local rewardLabels={}
local getItems=ms.d_messageUI.createGetItemsLayer;local rewardParent
ms.d_messageUI.createGetItemsLayer=function(parent,...)
 rewardParent=parent;return getItems(parent,...)
end
local properties=ms.d_u.setProperties;local timers={};local trialButtons={}
ms.d_u.setProperties=function(parent,node,options,...)
 if options.y==0.78 and (options.x==0.7 or options.x==0.75) then timers[#timers+1]=node end
 return properties(parent,node,options,...)
end
local sends={};local taps={};local battles={};local obtainClose;local obtainLayer;local battleReturn;local taskQueries=0
ui.g_self={};ui.g_data={};ui.g_pethuntUI={};ms.d_petHomeUI.g_self=shallow(saved.home);ms.d_petHomeUI.g_data={}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player);ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
for k,v in pairs(f.role) do ms.d_mainUI.g_playerInfo[k]=v end
ms.d_data.g_new_config[8]=f.config;ms.d_xianmengUI.getGuildConfig(f.config)
ms.d_time.getTime=function() return 1792728000 end
guildPetErrors={};guildPetResults={};guildPetCases={}
ms.MS_report_error=function(e) guildPetErrors[#guildPetErrors+1]=tostring(e) end
ms.d_u.main_server_send_msg=function(mid,d)
 sends[#sends+1]={mid=mid,data=d};if mid==1301 and d.id==83 then taskQueries=taskQueries+1 end
end
local dispatch={};for mid,fn in pairs(saved.dispatch) do dispatch[mid]=mid==2999 and fn or function() end end
ms.d_event_mgr.g_msg_fun=dispatch
ms.d_u.createMenu=function(options,...)
 for _,row in pairs(options) do
  if type(row)=='table' and type(row.call_back)=='function' then
   taps[debug.getinfo(row.call_back,'S').linedefined]=row.call_back
   if row.npic=='v2/fightUI/return1.png' then battleReturn=row.call_back end
   if row.npic then trialButtons[row.npic]=row.call_back end
  end
 end
 return saved.menu(options,...)
end
ms.d_petUI.getPetObtainLayer=function(pet,close,...)
 obtainClose=close;obtainLayer=saved.obtain(pet,close,...);return obtainLayer
end
ms.d_fightUI.actFight=function(replay,kind)
 assert(replay.line_up_msg and #replay.fight_result_msg.fight_result>0)
 battles[#battles+1]={kind=kind,replay=replay}
end
function guildPetRestore()
 if ms._localGuildPetRestore then ms._localGuildPetRestore() end
 for _,entry in ipairs(patchedFunctions) do entry[1][entry[2]]=entry[3] end
 ms.d_mapUI.show=mapShow;ms.d_messageUI.createGetItemsLayer=getItems;ms.d_u.setProperties=properties
 ms.d_u.createMenu=saved.menu;ms.d_petUI.getPetObtainLayer=saved.obtain;ms.d_fightUI.actFight=saved.act
 ms.d_time.getTime=saved.time;ms.d_u.main_server_send_msg=saved.send;ms.d_event_mgr.g_msg_fun=saved.dispatch;ms.MS_report_error=saved.report
 ms.d_event_mgr.setSpecialFightType(0)
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config;ms.d_xianmengUI.getGuildConfig(saved.guildConfig)
 ms.d_mainUI.show()
 ui.g_self=saved.self;ui.g_data=saved.data;ui.g_pethuntUI=saved.panels;ms.d_petHomeUI.g_self=saved.home;ms.d_petHomeUI.g_data=saved.homeData
 guildPetRestore=nil
end
if ms._localGuildPetRestore then ms._localGuildPetRestore() end
-- __PET_PATCH__
local taskFinish=ui.showTaskFinish
ui.showTaskFinish=function(parent,kind,won,...)
 taskRewards[#taskRewards+1]={won=won,parent=parent or ui.g_pethuntUI.main_layer}
 return taskFinish(parent,kind,won,...)
end
local style=ms.d_u.createByStyle
ms.d_u.createByStyle=function(options,...)
 if options.type=='label' and options.y==0.3 then rewardLabels[#rewardLabels+1]=options.string end
 return style(options,...)
end
local oldRestore=guildPetRestore
guildPetRestore=function() ms.d_u.createByStyle=style;return oldRestore() end
local function apply(name)
 for _,row in ipairs(f[name]) do
  if row.mid==2998 then ms.d_event_mgr.msg_common_event_2998(nil,row.data,nil)
  else ms.d_event_mgr.msg_union_event_1301(nil,row.data,nil) end
 end
end
local function step(name,fn,hold) guildPetCases[#guildPetCases+1]={name=name,fn=fn,hold=hold or 0} end
function guildPetRun(i)
 local c=guildPetCases[i];sends={};local ok,err=xpcall(c.fn,debug.traceback)
 local row={name=c.name,ok=ok,error=err or '',hold=c.hold};guildPetResults[#guildPetResults+1]=row;return row
end
local function sent(op)
 for _,row in ipairs(sends) do if row.data.id==op then return assert(loadstring('return '..row.data.data))() end end
 error('request missing: '..op)
end
local function huntLayer() return ui.g_pethuntUI.field_layer:getChildByTag(ui.tagDef.hunt_layer) end
step('open_actual_task_dialog_and_challenge_button',function()
 ms.d_xianmengUI.show();apply('info');apply('tasks')
 ui.showMainLayer(ms.d_xianmengUI.getXianMengMainLayer());ui.g_self.cur_task_index=1
 ui.showTaskLayer(nil,ui.g_data.main.union_task[1]);assert(taps[602],'challenge button missing')()
 local d=sent(84);assert(d.task_index==1 and d.task_type==2 and d.pay_type==1)
 assert(d.task_day==ui.g_data.main.task_day,'task request lost its day')
end)
step('settlement_counters_before_battle_playback',function()
 apply('challenge');assert(#battles==1 and battles[1].kind==28)
 local result;for _,row in ipairs(f.challenge) do if row.mid==1301 and row.data.id==84 then result=assert(loadstring('return '..row.data.data))() end end
 assert(ui.g_data.main.free_task_times==result.task_state.free_task_times)
 assert(ui.g_data.task_finish.task_type==2)
end)
step('task_return_rebuild_keeps_updated_counter',function()
 ms.d_xianmengUI.show(ms.d_xianmengUI.showTypeDef.pet)
 assert(ui.g_data.main.free_task_times<=3)
 apply('puzzle')
 assert(ui.g_data.main.free_task_times<=2)
 assert(#ui.g_data.main.union_task==2 and ui.g_data.main.union_task[2].index==3,'completed target still visible')
 ui.g_self.cur_task_index=2;ui.showTaskLayer(nil,ui.g_data.main.union_task[2])
 assert(ui.g_self.cur_task_index==3,'compacted task list lost stable target index')
end,2)
step('wild_explore_opens_capture_dialog',function()
 ms.d_xianmengUI.show(ms.d_xianmengUI.showTypeDef.pet);apply('field');apply('explore')
 assert(huntLayer());assert(ui.g_data.field_boss.left_times==3)
end)
step('capture_success_runs_native_animation_and_pet_popup',function() apply('capture') end,7)
step('capture_popup_close_unlocks_and_removes_dialog',function()
 assert(obtainClose and obtainLayer,'pet popup did not finish rendering')
 assert(#guildPetErrors==0,table.concat(guildPetErrors,'\n'))
 ms.d_u.remove(obtainLayer);obtainClose();obtainClose=nil;obtainLayer=nil
 assert(not ui.g_self.playing_hunt_ani);assert(not huntLayer())
 apply('leave');assert(not ui.g_self.playing_hunt_ani)
end)
step('retry_capture_failure_keeps_dialog_interactive',function()
 apply('explore_again');apply('failure1')
end,7)
step('failed_capture_unlocks_for_next_attempt',function()
 assert(not ui.g_self.playing_hunt_ani);assert(huntLayer());assert(ui.g_data.field_boss.left_times==2)
 apply('failure2')
end,7)
step('last_capture_failure_runs_exit_animation',function()
 assert(not ui.g_self.playing_hunt_ani);apply('failure3')
end,10)
step('exhausted_capture_dialog_removed_and_can_exit',function()
 assert(not ui.g_self.playing_hunt_ani);assert(not huntLayer())
 assert(#guildPetErrors==0,table.concat(guildPetErrors,'\n'))
end)
step('trial_random_five_star_boss_renders_and_plays',function()
 ms.d_petHomeUI.show(ui.g_pethuntUI.main_layer);apply('home')
 ms.d_petHomeUI.showShilianLayer();apply('trial');apply('trial_fight')
 assert(battles[#battles].kind==27)
 apply('trial_after')
end)
step('real_task_battle_animation',function()
 ms.d_event_mgr.setSpecialFightType(0)
 ms.d_fightUI.actFight=saved.act
 battleReturn=nil;rewardCount=#taskRewards
 apply('challenge')
 assert(ms.d_fightUI.g_fightUI.last_fight_type==28)
end)
function guildPetBattleReady() return battleReturn~=nil end
step('real_task_battle_return_button_and_reward',function()
 assert(#guildPetErrors==0,table.concat(guildPetErrors,'\n'))
 assert(battleReturn)()
 assert(mapCalls==0,'battle return opened Journey')
 assert(ui.g_pethuntUI.main_layer:getParent(),'task page is detached')
 assert(#taskRewards==rewardCount+1 and taskRewards[#taskRewards].won==2 and taskRewards[#taskRewards].parent:getParent(),'failure settlement popup missing')
 assert(ui.g_data.task_finish.task_type==2)
end,2)
step('real_task_win_battle_animation',function()
 assert(ui.g_pethuntUI.main_layer:isRunning(),'task page did not become active')
 battleReturn=nil;rewardCount=#taskRewards;rewardLabels={};apply('challenge_win')
end)
step('task_win_reward_on_live_task_page',function()
 assert(battleReturn)();assert(mapCalls==0)
 assert(#taskRewards==rewardCount+1 and taskRewards[#taskRewards].won==1,'win reward missing')
 assert(taskRewards[#taskRewards].parent:getParent())
end,2)
step('real_trial_loss_battle_animation',function()
 assert(ui.g_pethuntUI.main_layer:isRunning(),'winning task page did not become active')
 local found=false;for _,label in ipairs(rewardLabels) do if label=='银两×1000' then found=true end end
 assert(found,'silver reward name/count missing: '..table.concat(rewardLabels,','))
 assert(#ui.g_data.main.union_task==0,'completed daily targets still visible')
 battleReturn=nil;apply('trial_fight')
end)
step('trial_loss_stays_until_return_then_reopens_trial',function()
 assert(ms.d_fightUI.g_fightUI.layerFightEnd:isRunning(),'result panel auto-exited')
 assert(battleReturn)();assert(mapCalls==0)
 apply('home');sent(79)
 timers={};trialButtons={};apply('trial_after')
 assert(ms.d_petHomeUI.g_self.g_Shilian_layer:getParent())
 assert(#timers==1,'overlapping trial timers')
 assert(not trialButtons['v2/petHomeUI/pos1.png'],'formation option still present')
 assert(trialButtons['v2/petHomeUI/challenge1.png'])
end,2)
step('real_trial_win_battle_animation',function()
 assert(ms.d_petHomeUI.g_self.g_Shilian_layer:isRunning(),'trial page did not become active')
 battleReturn=nil;apply('trial_win')
end)
step('trial_win_return_claim_and_continue',function()
 assert(ms.d_fightUI.g_fightUI.layerFightEnd:isRunning())
 assert(battleReturn)();apply('home');sent(79);apply('trial_reward_ready')
 trialButtons={};rewardParent=nil;timers={};apply('trial_claim')
 assert(rewardParent==ms.d_petHomeUI.g_self.g_Shilian_layer and rewardParent:getParent(),'reward popup lost during rebuild')
 assert(ms.d_petHomeUI.g_self.g_data.result==1 and ms.d_petHomeUI.g_self.g_data.boss_layer==2)
 assert(#timers==1 and not trialButtons['v2/petHomeUI/pos1.png'])
 assert(trialButtons['v2/petHomeUI/challenge1.png'],'next challenge missing')()
 sent(80)
 assert(#guildPetErrors==0,table.concat(guildPetErrors,'\n'))
end,2)
step('claimed_trial_page_remains_active',function()
 assert(ms.d_petHomeUI.g_self.g_Shilian_layer:isRunning());assert(rewardParent:isRunning())
end)
step('pet_shop_native_batch_purchase_and_tiered_prices',function()
 ms.d_xianmengUI.show(ms.d_xianmengUI.showTypeDef.pet)
 ui.showMainLayer(ms.d_xianmengUI.getXianMengMainLayer())
 assert(taps[235],'shop entrance missing')();assert(sent(91).two_type==1);apply('shop')
 local rows=ui.g_data.shop.item_list
 assert(rows[3].buy_reputation==20 and rows[4].buy_reputation==40 and rows[5].buy_reputation==60)
 local before=rows[4].left_times
 sends={}
 ui.showBatchBuy(nil,rows[4],4)
 assert(taps[1661],'batch count control missing')(3)
 assert(taps[1686],'batch confirm missing')()
 local d=sent(91);assert(d.index==4 and d.buy_count==4 and d.two_type==2)
 apply('shop_buy_four')
 assert(ui.g_data.shop.item_list[4].left_times==before-4)
 assert(ui.g_data.shop.cur_reputation==840 and ui.g_data.shop.item_list[4].buy_reputation==40)
end)
step('daily_expiry_refreshes_open_task_page',function()
 ms.d_time.getTime=function() return f.next_day_time end
 ms.d_xianmengUI.show(ms.d_xianmengUI.showTypeDef.pet)
 ui.showMainLayer(ms.d_xianmengUI.getXianMengMainLayer())
 taskQueries=0
end,2)
step('daily_refresh_replaces_targets_and_keeps_stable_indices',function()
 assert(taskQueries==1,'expired open page did not request one refresh')
 apply('next_day_tasks')
 assert(#ui.g_data.main.union_task==3 and ui.g_data.main.free_task_times==3)
 ui.g_self.cur_task_index=1;ui.showTaskLayer(nil,ui.g_data.main.union_task[1])
 ui.sendRequest(84,{task_index=ui.g_self.cur_task_index,task_type=2,pay_type=1})
 local d=sent(84);assert(d.task_day==ui.g_data.main.task_day and d.task_index==1)
end)
return 'ready'
