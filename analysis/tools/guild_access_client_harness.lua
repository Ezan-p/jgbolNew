local ms=assert(package.loaded.ms);local ui=ms.d_xianmengUI
assert(not guild_fixture_restore and not guildAccessTestRestore)
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,guildConfig=ui.guildConfig,
 send=ms.d_u.main_server_send_msg,info=ms.d_info.show,report=ms.MS_report_error,
 menu=ms.d_u.createMenu,register=rawget(CCMenuItemImage,'registerScriptTapHandler'),
 petOpen=ms.d_petUI.pet_is_open,patched=ms._localGuildAccessRestore~=nil,
 hunt=ms.d_pethuntUI.g_self,huntData=ms.d_pethuntUI.g_data,home=ms.d_petHomeUI.g_self,
 dispatch=ms.d_event_mgr.g_msg_fun}
local results={};local errors={};local sends={};local tips={};local petTap;local taps={};local buttons={}
local function restore()
 ms.d_u.createMenu=saved.menu;rawset(CCMenuItemImage,'registerScriptTapHandler',saved.register)
 if not saved.patched and ms._localGuildAccessRestore then ms._localGuildAccessRestore() end
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config;ui.getGuildConfig(saved.guildConfig)
 ms.d_u.main_server_send_msg=saved.send;ms.d_info.show=saved.info;ms.MS_report_error=saved.report
 ms.d_petUI.pet_is_open=saved.petOpen
 ms.d_pethuntUI.g_self=saved.hunt;ms.d_pethuntUI.g_data=saved.huntData;ms.d_petHomeUI.g_self=saved.home
 ms.d_event_mgr.g_msg_fun=saved.dispatch
 ms.d_mainUI.show();guildAccessTestRestore=nil
end
guildAccessTestRestore=restore
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
for k,v in pairs(__ROLE__) do ms.d_mainUI.g_playerInfo[k]=v end
ms.d_data.g_new_config[8]=__CONFIG__;ui.getGuildConfig(ms.d_data.g_new_config[8])
local function shallow(t) local c={};for k,v in pairs(t or {}) do c[k]=v end;return c end
ms.d_pethuntUI.g_self=shallow(saved.hunt);ms.d_pethuntUI.g_data=shallow(saved.huntData)
ms.d_petHomeUI.g_self=shallow(saved.home)
ms.d_u.main_server_send_msg=function(mid,d) sends[#sends+1]={mid=mid,data=d} end
local dispatch={};for mid,fn in pairs(saved.dispatch) do dispatch[mid]=mid==2999 and fn or function() end end
ms.d_event_mgr.g_msg_fun=dispatch
ms.d_info.show=function(t) tips[#tips+1]=t end
ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
local function step(name,fn)
 sends={};tips={};errors={}
 local ok,err=xpcall(fn,debug.traceback)
 results[#results+1]={name=name,ok=ok and #errors==0,error=err or table.concat(errors,'\n')}
end
-- __ACCESS_PATCH__
local function upvalue(fn,key)
 for i=1,100 do local k,v=debug.getupvalue(fn,i);if k==key then return v end;if not k then break end end
end
local createGuild=assert(upvalue(ui.getServerResponse,'createGuildLayer'))
ms.d_u.createMenu=function(options,...)
 for _,row in pairs(options) do
  if type(row)=='table' and row.npic=='v2/pethuntUI/entrance1.png' then petTap=row.call_back end
 end
 return saved.menu(options,...)
end
rawset(CCMenuItemImage,'registerScriptTapHandler',function(item,fn)
 if fn==upvalue(createGuild,'tapMainMenu') then buttons[#buttons+1]=item;taps[item]=fn end
end)
step('actual_guild_buttons_render_even_if_activity_flag_resets',function()
 ms.d_petUI.pet_is_open=false
 ui.show();ui.getServerResponse(18,__INFO__)
 assert(petTap,'island icon missing')
 local seen={};for _,item in ipairs(buttons) do seen[item:getTag()]=true end
 assert(seen[3] and seen[4],'war icons missing')
end)
local function warTap(tag)
 for _,item in ipairs(buttons) do if item:getTag()==tag then taps[item](tag);return end end
 error('war button missing')
end
for _,tag in ipairs({3,4}) do
 step('war_icon_'..tag..'_shows_exact_notice_without_request',function()
  warTap(tag);assert(#sends==0);assert(#tips==1 and tips[1]=='离线模式，暂未开放')
 end)
end
for _,kind in ipairs({ui.showTypeDef.guildFight,ui.showTypeDef.crossRealm}) do
 step('war_direct_scene_'..kind..'_blocked',function()
  local parent=ui.getXianMengMainLayer();ui.show(kind)
  assert(ui.getXianMengMainLayer()==parent and #sends==0 and tips[1]=='离线模式，暂未开放')
 end)
end
step('war_notifications_disabled',function() assert(ui.getActivityTipNum(3)==0 and ui.getActivityTipNum(4)==0) end)
for _,level in ipairs({49,50,99}) do
 step('actual_island_button_level_'..level,function()
  ms.d_mainUI.g_playerInfo.level=level;petTap()
  if level<50 then assert(#sends==0 and tips[1]=='条件不足，需要仙盟5级以上，人物等级50以上')
  else assert(#tips==0 and #sends==1 and sends[1].mid==1301 and sends[1].data.id==83) end
 end)
end
step('actual_island_button_guild_level_4_rejected',function()
 local info=upvalue(ui.getServerResponse,'selfGuildInfo');info.level=4;petTap();info.level=5
 assert(#sends==0 and #tips==1)
end)
step('task_response_opens_original_island',function()
 ms.d_mainUI.g_playerInfo.level=50;petTap()
 ms.d_pethuntUI.onGetResult(83,__TASKS__)
 assert(ms.d_pethuntUI.g_data.main.result==1)
 assert(ui.getXianMengMainLayer():getChildrenCount()>0)
end)
step('original_pet_home_opens_after_island',function()
 ms.d_petHomeUI.show(ui.getXianMengMainLayer())
 assert(sends[#sends].data.id==88)
 ms.d_petHomeUI.MsgHandle({id=88},__HOME__)
end)
local passed=true;for _,result in ipairs(results) do if not result.ok then passed=false end end
restore()
return table.tostring({passed=passed,checks=results,restored=ms.d_mainUI.g_playerInfo==saved.player and ms.d_u.main_server_send_msg==saved.send})
