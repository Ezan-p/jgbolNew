local ms=assert(package.loaded.ms);local ui=ms.d_pethuntUI;local f=__FIXTURES__
assert(not guildPetRestore and not guild_fixture_restore)
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,guildConfig=ms.d_xianmengUI.guildConfig,
 self=ui.g_self,data=ui.g_data,panels=ui.g_pethuntUI,home=ms.d_petHomeUI.g_self,homeData=ms.d_petHomeUI.g_data,
 send=ms.d_u.main_server_send_msg,dispatch=ms.d_event_mgr.g_msg_fun,report=ms.MS_report_error,time=ms.d_time.getTime,
 menu=ms.d_u.createMenu,obtain=ms.d_petUI.getPetObtainLayer,act=ms.d_fightUI.actFight,patched=ms._localGuildPetRestore~=nil}
local function shallow(t) local c={};for k,v in pairs(t or {}) do c[k]=v end;return c end
local sends={};local taps={};local battles={};local obtainClose;local obtainLayer;local battleReturn
ui.g_self={};ui.g_data={};ui.g_pethuntUI={};ms.d_petHomeUI.g_self=shallow(saved.home);ms.d_petHomeUI.g_data={}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player);ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
for k,v in pairs(f.role) do ms.d_mainUI.g_playerInfo[k]=v end
ms.d_data.g_new_config[8]=f.config;ms.d_xianmengUI.getGuildConfig(f.config)
ms.d_time.getTime=function() return 1792728000 end
guildPetErrors={};guildPetResults={};guildPetCases={}
ms.MS_report_error=function(e) guildPetErrors[#guildPetErrors+1]=tostring(e) end
ms.d_u.main_server_send_msg=function(mid,d) sends[#sends+1]={mid=mid,data=d} end
local dispatch={};for mid,fn in pairs(saved.dispatch) do dispatch[mid]=mid==2999 and fn or function() end end
ms.d_event_mgr.g_msg_fun=dispatch
ms.d_u.createMenu=function(options,...)
 for _,row in pairs(options) do
  if type(row)=='table' and type(row.call_back)=='function' then
   taps[debug.getinfo(row.call_back,'S').linedefined]=row.call_back
   if row.npic=='v2/fightUI/return1.png' then battleReturn=row.call_back end
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
 if not saved.patched and ms._localGuildPetRestore then ms._localGuildPetRestore() end
 ms.d_u.createMenu=saved.menu;ms.d_petUI.getPetObtainLayer=saved.obtain;ms.d_fightUI.actFight=saved.act
 ms.d_time.getTime=saved.time;ms.d_u.main_server_send_msg=saved.send;ms.d_event_mgr.g_msg_fun=saved.dispatch;ms.MS_report_error=saved.report
 ms.d_event_mgr.setSpecialFightType(0)
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config;ms.d_xianmengUI.getGuildConfig(saved.guildConfig)
 ms.d_mainUI.show()
 ui.g_self=saved.self;ui.g_data=saved.data;ui.g_pethuntUI=saved.panels;ms.d_petHomeUI.g_self=saved.home;ms.d_petHomeUI.g_data=saved.homeData
 guildPetRestore=nil
end
-- __PET_PATCH__
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
 battleReturn=nil
 apply('challenge')
 assert(ms.d_fightUI.g_fightUI.last_fight_type==28)
end)
function guildPetBattleReady() return battleReturn~=nil end
step('real_task_battle_return_button_and_reward',function()
 assert(#guildPetErrors==0,table.concat(guildPetErrors,'\n'))
 assert(battleReturn)()
 assert(ui.g_pethuntUI.main_layer)
 assert(ui.g_data.task_finish.task_type==2)
end,2)
return 'ready'
