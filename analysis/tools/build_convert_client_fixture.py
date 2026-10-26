"""Generate reversible native Cocos checks; all network requests are intercepted."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
script = r'''
local ms=assert(package.loaded.ms);local ui=assert(ms.d_cortCallUI)
if localConvertFixtureCleanup then localConvertFixtureCleanup() end
local saved={};for k,v in pairs(ui) do saved[k]=v end
local mgr=ms.d_event_mgr;local savedMgr={};for k,v in pairs(mgr) do savedMgr[k]=v end
mgr.g_fight_info={};mgr.g_fight_id_list={}
local player=ms.d_mainUI.g_playerInfo
local chars=ms.d_lineupUI.g_characterInfo
local current=ms.d_activityUI.g_currentActivity
local send,report=ms.d_u.main_server_send_msg,ms.MS_report_error
local countItem,buyItem=ms.d_data.getItemCountByType,ms.d_data.createBuyFixedItem
local saveLevel=ms.d_lineupUI.saveLastFightLevel
local root=CCLayer:create();root:retain()
local function restore()
 root:removeAllChildrenWithCleanup(true);root:release()
 for k in pairs(ui) do if saved[k]==nil then ui[k]=nil end end
 for k,v in pairs(saved) do ui[k]=v end
 for k in pairs(mgr) do if savedMgr[k]==nil then mgr[k]=nil end end
 for k,v in pairs(savedMgr) do mgr[k]=v end
 ms.d_mainUI.g_playerInfo=player;ms.d_lineupUI.g_characterInfo=chars
 ms.d_activityUI.g_currentActivity=current
 ms.d_u.main_server_send_msg=send;ms.MS_report_error=report
 ms.d_data.getItemCountByType=countItem;ms.d_data.createBuyFixedItem=buyItem
 ms.d_lineupUI.saveLastFightLevel=saveLevel
 localConvertFixtureCleanup=nil
end
localConvertFixtureCleanup=restore
local sent,errors,bought={},'',false
ms.d_u.main_server_send_msg=function(mid,d) sent[#sent+1]={mid=mid,data=d} end
ms.MS_report_error=function(e) errors=errors..'\n'..tostring(e) end
ms.d_lineupUI.saveLastFightLevel=function() end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(player)
ms.d_lineupUI.g_characterInfo=ms.d_c.table_copy(chars)
local p=ms.d_mainUI.g_playerInfo
p.level=60;p.convert_fight_count=0;p.convert_fight_limit=3;p.month_card_time=0
p.convert_fight_time=ms.d_time.getTime()
ui.g_self={last_select_type=5011}
local checks={}
local function check(name,fn)
 errors='';local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and errors=='',error=(err or '')..errors}
end
local function close()
 if ui.g_self.main_layer then ui.g_self.main_layer:removeFromParentAndCleanup(true);ui.g_self.main_layer=nil end
end
check('entry_and_target_detail',function()
 ui.show(root);assert(ui.g_self.main_layer)
 local t,n=ui.getLastRightTypeAndName();assert(t==5009 and type(n)=='string')
 ui.pressRight()
end)
check('native_five_star_selection',function()
 close();ui.show(root);ui.pressSelectCort()
 assert(#ui.g_self.cortegeInfos>0)
 for _,c in ipairs(ui.g_self.cortegeInfos) do assert(c.csvInfo.quality>=5) end
 assert(ui.g_self.batchSelectLayer)
 ui.g_self.batchSelectLayer:removeFromParentAndCleanup(true);ui.g_self.batchSelectLayer=nil
end)
check('free_request_original_fields',function()
 local n=#sent;ui.pressFight();assert(#sent==n+1)
 local d=sent[#sent];assert(d.mid==1026 and d.data.fight_type==10 and d.data.des_value==5011 and d.data.des_id==0 and d.data.des_type==0)
end)
check('no_selection_no_request',function()
 local n=#sent;ui.g_self.last_select_type=nil;ui.pressFight();assert(#sent==n);ui.g_self.last_select_type=5011
end)
check('missing_token_purchase',function()
 p.convert_fight_count=1
 ms.d_data.getItemCountByType=function() return 0 end
 ms.d_data.createBuyFixedItem=function(kind,tid) assert(kind==5 and tid==1024);bought=true;return CCLayer:create() end
 local n=#sent;ui.pressFight();assert(#sent==n and bought)
end)
check('token_request',function()
 ms.d_data.getItemCountByType=function() return 2 end
 local n=#sent;ui.pressFight();assert(#sent==n+1)
end)
check('daily_limit_and_monthcard_extra',function()
 p.convert_fight_count=3;p.month_card_time=ms.d_time.getTime()
 local n=#sent;ui.pressFight();assert(#sent==n)
 p.month_card_time=ms.d_time.getTime()+100;ui.pressFight();assert(#sent==n+1)
end)
check('legacy_wrapper_reproduces_missing_cards',function()
 close();ui.callbackOutput({prize_list={{2,3},{1,1},{3,2}}});ui.show(root,true)
 assert(ui.g_self.prize_list==nil and ui.g_self.rewardsCards==nil)
end)
for kind=1,3 do
 check('direct_array_reward_'..kind,function()
  close();ui.callbackOutput({{kind,3},{1,1},{3,2},{2,1},{1,5}});ui.show(root,true)
  assert(#ui.g_self.prize_list==5 and #ui.g_self.rewardsCards==5)
  local sprite,name,n,t=ui.getRewardsInfos();assert(sprite and name and n==3 and t==kind)
  ui.g_self.g_random_index=nil
  local _,_,n2,t2=ui.getUnrewardsInfos();assert(n2==1 and t2==1)
  local _,_,n3,t3=ui.getUnrewardsInfos();assert(n3==2 and t3==3)
  ui.selectRewardsCard(2);assert(ui.g_self.flip_card_index==2)
  ui.showRewardsPageGetItemTip()
 end)
end
for index=1,5 do
 check('countdown_auto_flip_position_'..index,function()
  close();ui.callbackOutput({{2,1},{1,3},{3,2},{2,3},{1,5}});ui.show(root,true)
  local random=math.random
  math.random=function(a,b) assert(a==100000 and b==200000);return 100000+index-1 end
  ui.g_self.time_begin_sec=os.time()-11
  local ok,err=pcall(ui.count_down);math.random=random;assert(ok,err)
  assert(ui.g_self.flip_card_index==index)
  ui.call_back_close();assert(ui.g_self.output==nil and ui.g_self.main_layer)
 end)
end
check('actual_backend_wire_and_native_enemy_substitution',function()
 close();ui.g_self.last_select_type=5011
 local packets=__WIRE__
 local fid
 for _,row in ipairs(packets) do
  if row[1]==1028 then fid=row[2].fight_id;mgr.fight_lineup_1028(nil,row[2],0)
  elseif row[1]==1027 then mgr.fight_result_1027(nil,row[2],0)
  elseif row[1]==2998 then mgr.msg_common_event_2998(nil,row[2],nil) end
 end
 assert(mgr.g_fight_info[fid].line_up_msg.lineup[1].des_type==5009)
 ui.show(root,true);assert(#ui.g_self.rewardsCards==5)
 local _,_,n,t=ui.getRewardsInfos();assert(n==3 and t==2)
end)
check('defeat_empty_array_returns_main',function()
 close();ui.g_self.prize_list=nil;ui.g_self.rewardsCards=nil
 ui.callbackOutput({});ui.show(root,true)
 assert(ui.g_self.main_layer and ui.g_self.prize_list==nil)
end)
restore()
return ms.d_json.encode({checks=checks,original_cocos=true,state_restored=true,network_intercepted=true})
'''
wire = (ROOT / '.runtime/convert-wire-fixture.lua').read_text().removeprefix('return ')
(ROOT / '.runtime/convert-fixture.lua').write_text(script.replace('__WIRE__', wire))
print('Built native 天缘 client fixture')
