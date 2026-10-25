"""Replay disposable backend responses in the original guild UI, restore references."""
import sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from network_redirect.backend import Backend
from network_redirect import summon,guild
from network_redirect.protocol import encode,decode
ROOT=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18790,lambda *a,**k:None);r=b.profile();r.update(level=40,gold_coin=100000,silver_coin=100000);b.save(r)
 lines=["""local ms=assert(package.loaded.ms)
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,guildConfig=ms.d_xianmengUI.guildConfig}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
ms.d_u.main_server_send_msg=function(...) end
local errors='';guild_fixture_results={};guild_fixture_restored=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
local cases={}
local function withOverride(t,key,fn,run)
 local saved=t[key];t[key]=fn
 local ok,err=xpcall(run,debug.traceback);t[key]=saved
 assert(ok,err)
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
local function step(name,fn) cases[#cases+1]={name=name,run=fn,hold=name=='pet_lucky_catch' and 16 or 0} end
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
  serial+=1;replies=b.respond(encode(1301,dict(serial_num=serial,id=op,data=summon.lua(d))),dict(authenticated=True))
  lines.append('step('+summon.lua(name)+',function()')
  for p in replies:
   mid,_,data=decode(p)
   if mid==2998 and data['id']==55:raise AssertionError((name,data['data']))
   if mid in (1032,1301,1098) or mid==2998 and data['id']==82:lines.append('apply('+str(mid)+','+summon.lua(data)+')')
  lines.append('end)')
 request('union_list',18,query_type=4,page=1)
 request('create',1,union_name='验证仙盟')
 request('union_info',18,query_type=1)
 request('members',18,query_type=2,flag=1)
 request('event_log',18,query_type=6)
 request('applications',18,query_type=5)
 applicant=int(next(iter(b.profile()['guild']['unions']['2']['applications'])))
 request('accept_applicant',5,role_id=applicant)
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
 request('store',38)
 request('store_refresh',39)
 request('store_buy',40,item_id=1,buy_count=1)
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
 r=b.profile();g=r['guild']['unions']['2']
 for ident in (710001,710002,710003):g['members'][str(ident)]=guild.offline.npc(ident,'候补道友'+str(ident),0)
 b.save(r)
 request('team_create',26)
 request('team_inside',44)
 request('team_applications',50)
 lines.append("""step('team_accept_button',function()
 local ui=ms.d_secretAreaUI
 local accept=captureMenu(function() ui.showJoinTeamPage() end,979)
 local state=ui.g_self
 for index,check in pairs(state.join_team_btns_checks) do check:setVisible(state.teams_info.team.apply_list_sort[index].id~=710003) end
 local sent
 withOverride(ui,'send_msg_union_event',function(op,data) assert(op==28);sent=data end,accept)
 assert(sent and #sent.role_list==3,'expected all three NPCs selected')
 local expected={["""+str(applicant)+"""]=true,[710001]=true,[710002]=true}
 for _,id in ipairs(sent.role_list) do assert(expected[id],'wrong applicant ID');expected[id]=nil end
end)""")
 request('team_accept',28,role_list=[applicant,710001,710002])
 lines.append("step('team_four_after_bulk_accept',function() local t=ms.d_secretAreaUI.g_self.teams_info.team;assert(t.max_count==5);assert(#t.teams==4);assert(t.apply_list[710003]) end)")
 request('team_accept_fifth',28,role_list=[710003])
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
 lines.append("step('pet_home_open',function() ms.d_petHomeUI.show(ms.d_xianmengUI.getXianMengMainLayer()) end)")
 request('pet_train',79)
 r=b.profile();r['guild']['instances']['train_open']=True;b.save(r)
 request('pet_train_active',79)
 r=b.profile();r['guild']['instances']['train_done']=True;b.save(r)
 request('pet_train_finished',79)
 request('pet_inside',88)
 request('pet_lucky_catch',89)
 request('pet_task',83)
 lines.append("step('pet_hunt_open',function() ms.d_pethuntUI.showMainLayer(ms.d_xianmengUI.getXianMengMainLayer()) end)")
 request('pet_field',86,two_type=1)
 request('pet_wander_update',86,two_type=2)
 request('pet_catch_update',87,two_type=2)
 lines.append("step('pet_shop_entry',function() ms.d_pethuntUI.g_pethuntUI.shop_parent=ms.d_xianmengUI.getXianMengMainLayer() end)")
 request('pet_shop',91,two_type=1)
 request('pet_rank',92,two_type=1,query_type=1)
 lines.append("step('escort_open',function() ms.d_escortUI.show(ms.d_xianmengUI.getXianMengMainLayer());ms.d_escortUI.tapMenuMain(1) end)")
 request('escort_road',69,flag=3,road_type=1)
 request('escort_fetch',69,flag=4,road_type=1)
 request('escort_refresh',69,flag=5,road_type=1)
 request('escort_depart',69,flag=6,road_type=1,book_level=b.profile()['guild']['escort']['level'],des_id=0)
 request('cross_schedule',58,query_type=21)
 request('cross_list',58,query_type=30)
 request('cross_enter',58,query_type=32)
 request('cross_shop',58,query_type=33)

 lines.append("""local i=0;local hold=0
local function restore()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
 ms.d_xianmengUI.getGuildConfig(saved.guildConfig)
 ms.d_mainUI.show();guild_fixture_restored=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local handle
handle=scheduler:scheduleScriptFunc(function()
 if hold>0 then hold=hold-1;return end
 if i>0 then guild_fixture_results[i]={name=cases[i].name,ok=errors=='',error=errors} end
 i=i+1
 if i>#cases then scheduler:unscheduleScriptEntry(handle);restore();return end
 hold=cases[i].hold or 0
 errors='';local ok,err=xpcall(cases[i].run,debug.traceback)
 if not ok then errors=errors..'\\n'..tostring(err) end
end,0.25,false)
return 'guild fixture started' 
""")
 (ROOT/'.runtime/guild-fixture.lua').write_text('\n'.join(lines));b.close()
print('Wrote isolated guild client fixture')
