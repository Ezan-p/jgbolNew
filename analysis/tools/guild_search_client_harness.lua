local fixtures=__FIXTURES__
local ms=assert(package.loaded.ms)
local ui=ms.d_secretAreaUI
local live=assert(ui.g_self)
assert(live.main_layer and live.main_layer:getParent(),'open the treasure page first')
local layer=CCLayer:create()
live.main_layer:getParent():addChild(layer,10000)
local state={};for k,v in pairs(live) do state[k]=v end
state.main_layer=layer;state.g_parent_layer=layer
local send=ms.d_u.main_server_send_msg
local createMenu=ms.d_u.createMenu
local confirm=ms.d_quitUI.createYesNoByStyle
local rewards=ms.d_commonLayerUI.showPrizeResLayer
local team=ui.showMyTeam
local close,onekey,sent,rewardCount,closed
local report={checks={},passed=false}
local errors={};local errorHandler=ms.MS_report_error
ms.MS_report_error=function(e) errors[#errors+1]=tostring(e) end
ui.g_self=state
ms.d_u.main_server_send_msg=function(mid,d) sent={mid=mid,data=d} end
ms.d_u.createMenu=function(options,...)
 for _,style in pairs(options) do
  if type(style)=='table' and type(style.call_back)=='function' then
   local line=debug.getinfo(style.call_back,'S').linedefined
   if line==1729 then onekey=style.call_back end
   if style.call_back==ui.pressCloseSearch then close=style.call_back end
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
 -- Prove the unpatched native renderer fails on the exact reported order.
 local page=copy(fixtures.legacy);page.free_times=0;page.token_index=6
 state.prize_data=page;state.free_times=0
 local success,failure=pcall(ui.showPrizePage,layer)
 report.legacy_error=not success and tostring(failure) or nil
 -- Reload the adapter even if an earlier version was injected at login.
 if ms._localGuildActivitiesRestore then ms._localGuildActivitiesRestore() end
 -- __PATCH__
 for _,name in ipairs({'initial','legacy'}) do
  check(name..'_native_onekey_and_rewards',function()
   onekey=nil;close=nil;sent=nil;rewardCount=nil
   ui.callback_fam_search_gold(copy(fixtures[name]))
   controls();assert(onekey,'native one-key callback missing')
   onekey();assert(sent and sent.mid==1301 and sent.data.id==43)
   local request=assert(loadstring('return '..sent.data.data))()
   assert(request.flag==6)
   ui.callback_fam_search_gold(copy(fixtures.sweep))
   controls();assert(rewardCount==5,'reward popup missing')
   assert(state.free_times==0 and state.prize_data.free_times==0)
   assert(not state.prize_btns[1]:isEnabled() and not state.prize_btns[2]:isEnabled())
   local label=tolua.cast(layer:getChildByTag(910043),'CCLabelTTF')
   assert(label and label:getString():find('0',1,true),'zero count missing')
   closed=false;close();assert(closed,'close does not return to team')
  end)
 end
 for position=1,18 do
  check('selected_slot_'..position,function()
   local data=copy(fixtures.initial);data.free_times=0;data.token_index=6
   data.search_order[5],data.search_order[position]=data.search_order[position],data.search_order[5]
   for i=1,5 do data.prize_items[i].had_token=true end
   ui.callback_fam_search_gold(data);controls()
  end)
 end
 check('single_result_in_legacy_slot_25',function()
  local data=copy(fixtures.legacy)
  data.search_order[1],data.search_order[21]=data.search_order[21],data.search_order[1]
  ui.callback_fam_search_gold(data)
  local result=copy(fixtures.sweep);result.flag=2;result.free_times=4;result.search_count=1;result.token_index=2;result.my_broad_data=result.my_broad_data[1]
  ui.callback_fam_search_gold(result);controls()
  assert(state.free_times==4)
 end)
 report.passed=true
end,debug.traceback)
guild_search_restore()
report.restored=true
if not ok then report.error=tostring(err) end
return table.tostring(report)
