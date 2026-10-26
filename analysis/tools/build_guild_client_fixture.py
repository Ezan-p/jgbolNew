"""Replay disposable backend responses in the original guild UI, restore references."""
import sys,tempfile
from datetime import datetime,timedelta,timezone
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from network_redirect.backend import Backend
from network_redirect import summon,guild
from network_redirect.protocol import encode,decode
ROOT=Path(__file__).resolve().parents[2]
fixture_now=int(datetime(2026,10,23,12,tzinfo=timezone(timedelta(hours=8))).timestamp())
with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18790,lambda *a,**k:None);r=b.profile();r.update(level=40,gold_coin=100000,silver_coin=100000);b.save(r)
 lines=["""local ms=assert(package.loaded.ms)
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,guildConfig=ms.d_xianmengUI.guildConfig,time=ms.d_time.getTime}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
guild_fixture_now=0;ms.d_time.getTime=function() return guild_fixture_now end
guild_fixture_store_queries=0
ms.d_u.main_server_send_msg=function(mid,data) if mid==1301 and data and data.id==38 then guild_fixture_store_queries=guild_fixture_store_queries+1 end end
local errors='';guild_fixture_results={};guild_fixture_restored=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
local cases={};local nativeTaps={}
local function selectedButton(line,expectedOp,expectedCount)
 local fn=assert(nativeTaps[line],'native button callback missing: '..line)
 for i=1,30 do local name,value=debug.getupvalue(fn,i);if not name then break end
  if name=='applyList' or name=='forbidList' then for _,row in ipairs(value) do row.isChecked=true end end
 end
 local sent;local original=ms.d_u.main_server_send_msg
 ms.d_u.main_server_send_msg=function(mid,d) sent=d end
 local ok,err=xpcall(fn,debug.traceback);ms.d_u.main_server_send_msg=original
 assert(ok,err);assert(sent and sent.id==expectedOp)
 local d=assert(loadstring('return '..sent.data))()
 assert(#d.role_list==expectedCount,'native role_list count');return d
end
local function withOverride(t,key,fn,run)
 local saved=t[key];t[key]=fn
 local ok,err=xpcall(run,debug.traceback);t[key]=saved
 assert(ok,err)
end
local function captureNative(run)
 local register=CCMenuItemImage.registerScriptTapHandler
 withOverride(CCMenuItemImage,'registerScriptTapHandler',function(item,fn)
  nativeTaps[debug.getinfo(fn,'S').linedefined]=fn;return register(item,fn)
 end,run)
end
local function findFunction(fn,line,seen)
 seen=seen or {};if seen[fn] then return end;seen[fn]=true
 if debug.getinfo(fn,'S').linedefined==line then return fn end
 for i=1,100 do local name,value=debug.getupvalue(fn,i);if not name then break end
  if type(value)=='function' then local found=findFunction(value,line,seen);if found then return found end end
 end
end
local function nativeManage(member,choice,rank)
 local ui=ms.d_xianmengUI
 local showMenu=assert(findFunction(ui.getServerResponse,1245),'manage menu unavailable')
 local sent;local confirm;local tip=ui.createTipBox
 withOverride(ms.d_u,'main_server_send_msg',function(mid,d) sent=d end,function()
  captureNative(function() showMenu(ui.getXianMengMainLayer(),ccp(200,300),member) end)
  withOverride(ui,'createTipBox',function(pic,fn,...) confirm=fn;return tip(pic,fn,...) end,function()
   captureNative(function() assert(nativeTaps[1293])(choice) end)
   if choice==1 then assert(nativeTaps[1184])(rank);assert(nativeTaps[1121])() end
   if confirm then confirm() end
  end)
 end)
 assert(sent,'management button sent no request');return sent.id,assert(loadstring('return '..sent.data))()
end
local function captureMenu(run,firstLine)
 local found;local original=ms.d_u.createMenu
 withOverride(ms.d_u,'createMenu',function(options,...)
  for _,v in pairs(options) do
   if type(v)=='table' and type(v.call_back)=='function' and debug.getinfo(v.call_back,'S').linedefined==firstLine then found=v.call_back end
  end
  return original(options,...)
 end,run)
 return assert(found,'button callback not captured: '..firstLine)
end
local function step(name,fn) cases[#cases+1]={name=name,run=fn,hold=name=='pet_lucky_catch' and 16 or (name=='store' or name=='store_refresh') and 12 or 0} end
local function apply(mid,d)
 if mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1098 then ms.d_event_mgr.msg_chat_info_to_client_1098(nil,d,nil)
 elseif mid==1301 then ms.d_event_mgr.msg_union_event_1301(nil,d,nil)
 elseif mid==2998 and d.id==82 then ms.d_xianmengUI.getUnionEvent(assert(loadstring('return '..d.data))()) end
end
"""]
 for k in ('level','gold_coin','silver_coin','union_id','union_rank','union_contrib','cur_union_contrib'):lines.append('ms.d_mainUI.g_playerInfo.'+k+'='+str(r.get(k,0)))
 lines.append('ms.d_data.g_new_config[8]='+summon.lua(guild.client_config(b.guild_rules)))
 lines.append('ms.d_xianmengUI.getGuildConfig(ms.d_data.g_new_config[8])')
 lines.append("step('entrance',function() ms.d_xianmengUI.showFirstPage() end)")
 serial=5000
 def request(name,op,**d):
  global serial
  serial+=1
  with patch('network_redirect.backend.time.time',return_value=fixture_now):replies=b.respond(encode(1301,dict(serial_num=serial,id=op,data=summon.lua(d))),dict(authenticated=True))
  lines.append('step('+summon.lua(name)+',function() guild_fixture_now='+str(fixture_now))
  capture=name in ('applications','leader_mute_list')
  if capture:lines.append("local register=CCMenuItemImage.registerScriptTapHandler;withOverride(CCMenuItemImage,'registerScriptTapHandler',function(item,fn) nativeTaps[debug.getinfo(fn,'S').linedefined]=fn;return register(item,fn) end,function()")
  for p in replies:
   mid,_,data=decode(p)
   if mid==2998 and data['id']==55:raise AssertionError((name,data['data']))
   if mid in (1032,1301,1098) or mid==2998 and data['id']==82:lines.append('apply('+str(mid)+','+summon.lua(data)+')')
  if capture:lines.append('end)')
  lines.append('end)')
 request('union_list',18,query_type=4,page=1)
 request('create',1,union_name='验证仙盟')
 request('union_info',18,query_type=1)
 request('members',18,query_type=2,flag=1)
 request('event_log',18,query_type=6)
 request('applications',18,query_type=5)
 applicants=list(map(int,b.profile()['guild']['unions']['2']['applications']))
 assert len(applicants)>=4,'fresh guild must recruit four real NPCs'
 applicant=applicants[0]
 lines.append("step('leader_native_accept_button',function() selectedButton(922,5,4) end)")
 request('accept_applicants',5,role_list=applicants[:4])
 request('members_after_recruitment',18,query_type=2,flag=1)
 lines.append("step('leader_native_appoint',function() local op,d=nativeManage("+summon.lua(b.profile()['guild']['unions']['2']['members'][str(applicant)])+",1,7);assert(op==11 and d.new_rank==7 and d.role_id=="+str(applicant)+") end)")
 request('leader_appoint_deputy',11,role_id=applicant,new_rank=7)
 request('members_after_appointment',18,query_type=2,flag=1)
 lines.append("step('leader_native_mute',function() local op,d=nativeManage("+summon.lua(b.profile()['guild']['unions']['2']['members'][str(applicant)])+",3);assert(op==20 and d.role_id=="+str(applicant)+") end)")
 request('leader_mute',20,role_id=applicant)
 request('leader_mute_list',18,query_type=3)
 lines.append("step('leader_native_unmute_button',function() selectedButton(1051,21,1) end)")
 request('leader_unmute',21,role_list=[applicant])
 request('leader_clear_mutes',22)
 request('leader_demote',11,role_id=applicant,new_rank=5)
 request('chat_send',23,chat_msg='离线仙盟回放测试')
 request('chat_history',18,query_type=7)
 request('tree_initial',34)
 lines.append("step('tree_open',function() ms.d_worldTreeUI.show(ms.d_xianmengUI.getXianMengMainLayer(),99) end)")
 request('tree_empty',34)
 lines.append("""step('tree_donate_dialog',function() local callback;local original=ms.d_worldTreeUI.createDonateLayer
 withOverride(ms.d_worldTreeUI,'createDonateLayer',function(options,fn) callback=fn;return original(options,fn) end,function() ms.d_worldTreeUI.gotoDonate() end)
 assert(callback,'donation dialog did not open')
 local sent
 withOverride(ms.d_u,'main_server_send_msg',function(mid,data) sent=data end,function() callback(50) end)
 assert(sent and sent.id==36 and assert(loadstring('return '..sent.data))().count==50)
 end)""")
 request('tree_unlock',36,count=50)
 request('tree_plant',14)
 request('tree_growing',34)
 request('tree_donate',36,count=50)
 request('tree_missions',35)
 lines.append("step('tree_close',function() ms.d_worldTreeUI.pressClose() end)")
 lines.append("step('store_entry_request',function() guild_fixture_store_queries=0;ms.d_guildStoreUI.requestStoreInfo();assert(guild_fixture_store_queries==1) end)")
 request('store',38)
 lines.append("step('store_idle_no_refresh_loop',function() assert(ms.d_mainUI.g_playerInfo.union_store_flush_time>ms.d_time.getTime());assert(guild_fixture_store_queries==1,'store auto-requested before deadline') end)")
 request('store_refresh',39)
 lines.append("step('store_paid_refresh_no_loop',function() assert(ms.d_mainUI.g_playerInfo.union_store_flush_time>ms.d_time.getTime());assert(guild_fixture_store_queries==1,'paid refresh restarted request loop') end)")
 request('store_buy',40,item_id=1,buy_count=1)
 lines.append("step('store_buy_preserves_deadline',function() assert(ms.d_mainUI.g_playerInfo.union_store_flush_time>ms.d_time.getTime()) end)")
 request('feast_preview',18,query_type=14)
 request('feast_open',65,feast_type=1)
 request('feast_active',18,query_type=14)
 request('feast_claim',68)
 request('feast_gift',67,gift_type=1,count=1)
 request('feast_active_gift',18,query_type=14)
 request('feast_grab',66,des_id=1)
 request('feast_fortune',18,query_type=15)
 request('match_enter',18,query_type=100)
 request('match_sign',45)
 lines.append("step('match_capture_group',function() local ui=ms.d_guildFightUI;local original=ui.showGroup;ui.showGroup=function(parent,index) ui.showGroup=original;guild_fixture_group_parent=parent;return original(parent,index) end end)")
 request('match_lineup',18,query_type=8)
 lines.append("step('match_group_one',function() ms.d_guildFightUI.showGroup(guild_fixture_group_parent,1) end)")
 lines.append("step('match_group_two',function() ms.d_guildFightUI.showGroup(guild_fixture_group_parent,2) end)")
 request('match_targets',18,query_type=13)
 lines.append("step('team_open',function() ms.d_secretAreaUI.show(ms.d_xianmengUI.getXianMengMainLayer()) end)")
 request('team_before_create',44)
 request('team_list',73)
 request('team_create',26)
 request('team_inside',44)
 request('team_applications',50)
 lines.append("""step('team_accept_button',function()
 local ui=ms.d_secretAreaUI
 local accept=captureMenu(function() ui.showJoinTeamPage() end,979)
 local state=ui.g_self
 for index,check in pairs(state.join_team_btns_checks) do check:setVisible(state.teams_info.team.apply_list_sort[index].id~="""+str(applicants[3])+""") end
 local sent
 withOverride(ui,'send_msg_union_event',function(op,data) assert(op==28);sent=data end,accept)
 assert(sent and #sent.role_list==3,'expected all three NPCs selected')
 local expected={["""+str(applicant)+"""]=true,["""+str(applicants[1])+"""]=true,["""+str(applicants[2])+"""]=true}
 for _,id in ipairs(sent.role_list) do assert(expected[id],'wrong applicant ID');expected[id]=nil end
end)""")
 request('team_accept',28,role_list=applicants[:3])
 lines.append("step('team_four_after_bulk_accept',function() local t=ms.d_secretAreaUI.g_self.teams_info.team;assert(t.max_count==5);assert(#t.teams==4);assert(t.apply_list["+str(applicants[3])+"]) end)")
 request('team_accept_fifth',28,role_list=[applicants[3]])
 lines.append("step('team_full_after_bulk_accept',function() local t=ms.d_secretAreaUI.g_self.teams_info.team;assert(t.max_count==5);assert(#t.teams==5);assert(next(t.apply_list)==nil) end)")
 lines.append("""step('team_client_minimum_and_full_roster',function()
 local ui=ms.d_secretAreaUI;local team=ui.g_self.teams_info.team;local all=team.teams
 for _,count in ipairs({2,3,4,5}) do
  local roster={};for i=1,count do roster[i]=all[i] end
  withOverride(team,'teams',roster,function()
   local sent
   withOverride(ui,'send_msg_union_event',function(op,data) assert(op==41);sent=data end,function() ui.pressFight() end)
   if count<3 then assert(sent==nil,'two players must not start')
   else assert(sent and #sent.fight_list==count,'three to five players must start') end
  end)
 end
end)""")
 request('team_full_applications',50)
 request('treasure_status',43,flag=1)
 request('treasure_move',43,flag=2)
 request('treasure_sweep',43,flag=6)
 request('pet_task',83)
 lines.append("step('pet_hunt_open',function() ms.d_pethuntUI.showMainLayer(ms.d_xianmengUI.getXianMengMainLayer()) end)")
 request('pet_field',86,two_type=1)
 request('pet_task_complete',84,task_index=1,task_type=1,pay_type=1)
 request('pet_wander_update',86,two_type=2)
 request('pet_catch_update',87,two_type=2)
 lines.append("step('pet_shop_entry',function() ms.d_pethuntUI.g_pethuntUI.shop_parent=ms.d_xianmengUI.getXianMengMainLayer() end)")
 request('pet_shop',91,two_type=1)
 request('pet_rank',92,two_type=1,query_type=1)
 fixture_now+=86400
 lines.append("step('pet_home_open',function() ms.d_petHomeUI.show(ms.d_xianmengUI.getXianMengMainLayer()) end)")
 request('pet_train',79)
 lines.append("step('pet_train_open_button',function() local sent;withOverride(ms.d_u,'main_server_send_msg',function(mid,d) sent=d end,function() ms.d_petHomeUI.sendMsgOpenChanllenge() end);assert(sent and sent.id==80,'240-resident trial button did not open') end)")
 lines.append("step('pet_train_member_request',function() local sent;withOverride(ms.d_u,'main_server_send_msg',function(mid,d) sent=d end,function() ms.d_petHomeUI.sendMsgRequestMemberList() end);assert(sent and sent.id==18);local d=assert(loadstring('return '..sent.data))();assert(d.query_type==2 and d.flag==4) end)")
 request('pet_train_member_list',18,query_type=2,flag=4)
 lines.append("step('pet_train_appoint_button',function() local ui=ms.d_petHomeUI;local state=ui.g_self;for key,row in pairs(state.memberList) do if row.id=="+str(applicant)+" then state.CheckBoxBeClicked=key end end;local sent;withOverride(ms.d_u,'main_server_send_msg',function(mid,d) sent=d end,function() ui.sendMsgChooseMember() end);assert(sent and sent.id==81);assert(assert(loadstring('return '..sent.data))().appoint_role=="+str(applicant)+") end)")
 request('pet_train_appoint',81,appoint_role=applicant)
 request('pet_train_battle',80)
 request('pet_train_active',79)
 r=b.profile();r['guild']['instances'].update(train_done=True,train_hp=0);b.save(r)
 request('pet_train_finished',79)
 lines.append("step('pet_train_claim_button',function() local sent;withOverride(ms.d_u,'main_server_send_msg',function(mid,d) sent=d end,function() ms.d_petHomeUI.sendMsgGetPrize() end);assert(sent and sent.id==82) end)")
 request('pet_train_claim',82)
 request('pet_inside',88)
 request('pet_lucky_catch',89)
 lines.append("step('pet_history_request',function() local sent;withOverride(ms.d_u,'main_server_send_msg',function(mid,d) sent=d end,function() ms.d_petHomeUI.sendMsgGetLuckyPetHistory() end);assert(sent and sent.id==94) end)")
 request('pet_history_response',94)
 lines.append("step('escort_open',function() ms.d_escortUI.show(ms.d_xianmengUI.getXianMengMainLayer());ms.d_escortUI.tapMenuMain(1) end)")
 request('escort_road',69,flag=3,road_type=1)
 request('escort_fetch',69,flag=4,road_type=1)
 request('escort_refresh',69,flag=5,road_type=1)
 request('escort_depart',69,flag=6,road_type=1,book_level=b.profile()['guild']['escort']['level'],des_id=0)
 request('cross_schedule',58,query_type=21)
 request('cross_list',58,query_type=30)
 request('cross_enter',58,query_type=32)
 request('cross_shop',58,query_type=33)
 request('leader_members_before_kick',18,query_type=2,flag=1)
 lines.append("step('leader_native_kick',function() local op,d=nativeManage("+summon.lua(b.profile()['guild']['unions']['2']['members'][str(applicants[3])])+",2);assert(op==25 and d.role_id=="+str(applicants[3])+") end)")
 request('leader_kick_member',25,role_id=applicants[3])
 request('leader_members_after_kick',18,query_type=2,flag=1)
 lines.append("step('leader_native_transfer',function() local op,d=nativeManage("+summon.lua(b.profile()['guild']['unions']['2']['members'][str(applicant)])+",4);assert(op==11 and d.new_rank==1 and d.role_id=="+str(applicant)+") end)")
 request('leader_transfer',11,role_id=applicant,new_rank=1)
 request('leader_transfer_info',18,query_type=1)
 lines.append("step('leader_transfer_rank',function() assert(ms.d_mainUI.g_playerInfo.union_rank==5) end)")
 request('former_leader_leave',3)
 lines.append("step('former_leader_unlinked',function() assert(ms.d_mainUI.g_playerInfo.union_id==0) end)")

 lines.append("""local i=0;local hold=0
local function restore()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report;ms.d_time.getTime=saved.time
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
 ms.d_xianmengUI.getGuildConfig(saved.guildConfig)
 ms.d_mainUI.show();guild_fixture_restored=ms.d_mainUI.g_playerInfo==saved.player and ms.d_data.g_new_config==saved.config and ms.d_u.main_server_send_msg==saved.send and ms.d_time.getTime==saved.time
 guild_fixture_restore=nil
end
local scheduler=CCDirector:sharedDirector():getScheduler();local handle
guild_fixture_restore=function() if handle then scheduler:unscheduleScriptEntry(handle) end;restore() end
handle=scheduler:scheduleScriptFunc(function()
 if hold>0 then hold=hold-1;return end
 if i>0 then guild_fixture_results[i]={name=cases[i].name,ok=errors=='',error=errors} end
 i=i+1
 if i>#cases then scheduler:unscheduleScriptEntry(handle);restore();return end
 hold=cases[i].hold or 0
 errors='';local ok,err=xpcall(cases[i].run,debug.traceback)
 if not ok then errors=errors..'\\n'..tostring(err) end
end,0.25,false)
guild_fixture_case_count=#cases
return 'guild fixture started' 
""")
 (ROOT/'.runtime/guild-fixture.lua').write_text('\n'.join(lines));b.close()
print('Wrote isolated guild client fixture')
