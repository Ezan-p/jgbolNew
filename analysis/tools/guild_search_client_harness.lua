local fixtures=__FIXTURES__
local ms=assert(package.loaded.ms)
local ui=ms.d_secretAreaUI
local live=assert(ui.g_self)
local layer=CCLayer:create()
CCDirector:sharedDirector():getRunningScene():addChild(layer,10000)
local state={};for k,v in pairs(live) do state[k]=v end
state.main_layer=layer;state.g_parent_layer=layer
local send=ms.d_u.main_server_send_msg
local createMenu=ms.d_u.createMenu
local confirm=ms.d_quitUI.createYesNoByStyle
local rewards=ms.d_commonLayerUI.showPrizeResLayer
local team=ui.showMyTeam
local close,onekey,single,sent,rewardCount,closed,primary,primaryCount
local report={checks={},passed=false}
local errors={};local errorHandler=ms.MS_report_error
ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
ui.g_self=state
ms.d_u.main_server_send_msg=function(mid,d) sent={mid=mid,data=d} end
ms.d_u.createMenu=function(options,...)
 for _,style in pairs(options) do
  if type(style)=='table' and type(style.call_back)=='function' then
   local line=debug.getinfo(style.call_back,'S').linedefined
   if style.npic and style.npic:find('onekey_',1,true) then onekey=style.call_back end
   if style.npic=='v2/secretArea/explore1.png' then single=style.call_back end
   if style.call_back==ui.pressCloseSearch then close=style.call_back end
  end
 end
 if options[6] and options[6].call_back==ui.getTeamsInfo then
  primary=options[5].call_back;primaryCount=0
  for _,style in ipairs(options) do
   if style.call_back==ui.pressFight or style.call_back==ui.pressExplore then primaryCount=primaryCount+1 end
  end
 end
 return createMenu(options,...)
end
ms.d_quitUI.createYesNoByStyle=function(parent,style,yes) yes() end
ms.d_commonLayerUI.showPrizeResLayer=function(parent,prizes,...)
 rewardCount=#prizes
 return rewards(parent,prizes,...)
end
ui.showMyTeam=function() closed=true end
guild_search_restore=function()
 ui.g_self=live
 ms.d_u.main_server_send_msg=send;ms.d_u.createMenu=createMenu
 ms.d_quitUI.createYesNoByStyle=confirm;ms.d_commonLayerUI.showPrizeResLayer=rewards
 ms.MS_report_error=errorHandler;ui.showMyTeam=team
 layer:stopAllActions();layer:removeFromParentAndCleanup(true)
 guild_search_restore=nil
end
local function copy(data) return ms.d_c.table_copy(data) end
local function check(name,fn)
 errors={}
 local ok,err=xpcall(fn,debug.traceback)
 if #errors>0 then ok=false;err=table.concat(errors,'\n') end
 report.checks[#report.checks+1]={name=name,ok=ok,error=not ok and tostring(err) or nil}
 assert(ok,name..': '..tostring(err))
end
local function controls()
 assert(#state.prize_sprites_btns==18,'carousel must have 18 slots')
 assert(state.prize_btns[3] and state.prize_btns[3]:isEnabled(),'close button missing')
 assert(close,'native close callback missing')
end
local ok,err=xpcall(function()
 if ms._localGuildActivitiesRestore then ms._localGuildActivitiesRestore() end
 -- __PATCH__
 check('continue_after_first_win_and_stop_after_three',function()
  for floor=0,2 do
   state.teams_info=copy(fixtures.team);state.teams_info.team.cleared_layer=floor;state.fight_count=floor;state.free_times=3
   state.teams_info.team.last_search_time=ms.d_time.getTime()
   ui.showTeamPage()
   assert(primary==ui.pressFight,'unfinished exploration must retain the fight action')
   assert(primaryCount==1,'challenge and treasure must not appear together')
  end
  sent=nil;primary()
  local request=assert(loadstring('return '..sent.data.data))()
  assert(sent.data.id==41 and #request.fight_list==3,'continue must send the full team')
  state.teams_info=copy(fixtures.complete);state.fight_count=3
  ui.showTeamPage()
  assert(primary==ui.pressExplore,'three floors must switch to treasure')
  assert(primaryCount==1,'completed exploration must have only one action')
  state.teams_info=copy(fixtures.team);state.teams_info.team.can_continue=false;state.teams_info.team.fight_count=3;state.fight_count=3
  ui.showTeamPage()
  assert(primary==ui.pressExplore and primaryCount==1,'exhausted attempts must show only treasure')
 end)
 check('single_draw_slot_18_and_sweep_remaining',function()
  ui.callback_fam_search_gold(copy(fixtures.initial));controls()
  sent=nil;assert(single);single()
  local request=assert(loadstring('return '..sent.data.data))()
  assert(sent.data.id==43 and request.flag==2)
  ui.callback_fam_search_gold(copy(fixtures.single));controls()
  assert(rewardCount==1 and state.free_times==4)
  assert(state.prize_data.prize_items[1].had_token)
  sent=nil;assert(onekey);onekey()
  request=assert(loadstring('return '..sent.data.data))()
  assert(sent.data.id==43 and request.flag==6)
  ui.callback_fam_search_gold(copy(fixtures.sweep));controls()
  assert(rewardCount==4 and state.free_times==0)
  assert(not state.prize_btns[1]:isEnabled() and not state.prize_btns[2]:isEnabled())
  local label=tolua.cast(layer:getChildByTag(910043),'CCLabelTTF')
  assert(label and label:getString():find('0',1,true),'zero count missing')
  closed=false;close();assert(closed,'close does not return to team')
 end)
 for position=1,18 do
  check('selected_slot_'..position,function()
   local data=copy(fixtures.initial);data.free_times=0;data.token_index=2
   local old
   for i,v in ipairs(data.search_order) do if v==position then old=i end end
   data.search_order[1],data.search_order[old]=data.search_order[old],data.search_order[1]
   data.prize_items[1].had_token=true
   ui.callback_fam_search_gold(data);controls()
  end)
 end
 report.passed=true
end,debug.traceback)
guild_search_restore()
report.restored=true
if not ok then report.error=tostring(err) end
return table.tostring(report)
