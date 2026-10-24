"""Replay disposable backend responses in the original guild UI, restore references."""
import sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from network_redirect.backend import Backend
from network_redirect import summon,guild
from network_redirect.protocol import encode,decode
ROOT=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as tmp:
 b=Backend(Path(tmp),18790,lambda *a,**k:None);r=b.profile();r.update(level=30,gold_coin=100000,silver_coin=100000);b.save(r)
 lines=["""local ms=assert(package.loaded.ms)
local saved={player=ms.d_mainUI.g_playerInfo,config=ms.d_data.g_new_config,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,guildConfig=ms.d_xianmengUI.guildConfig}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
ms.d_u.main_server_send_msg=function(...) end
local errors='';guild_fixture_results={};guild_fixture_restored=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
local cases={}
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
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
 request('chat_send',23,chat_msg='离线仙盟回放测试')
 request('chat_history',18,query_type=7)
 request('tree_initial',34)
 lines.append("step('tree_open',function() ms.d_worldTreeUI.show(ms.d_xianmengUI.getXianMengMainLayer(),99) end)")
 request('tree_empty',34)
 request('tree_plant',14)
 request('tree_growing',34)
 request('tree_donate',36,count=100)
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
 request('match_enter',18,query_type=100)
 request('match_sign',45)
 request('match_targets',18,query_type=13)
 lines.append("step('team_open',function() ms.d_secretAreaUI.show(ms.d_xianmengUI.getXianMengMainLayer()) end)")
 request('team_list',73)
 request('team_create',26)
 request('team_inside',44)
 lines.append("step('pet_home_open',function() ms.d_petHomeUI.show(ms.d_xianmengUI.getXianMengMainLayer()) end)")
 request('pet_train',79)
 r=b.profile();r['guild']['instances']['train_open']=True;b.save(r)
 request('pet_train_active',79)
 r=b.profile();r['guild']['instances']['train_done']=True;b.save(r)
 request('pet_train_finished',79)
 request('pet_inside',88)
 lines.append("step('pet_hunt_open',function() ms.d_pethuntUI.showMainLayer(ms.d_xianmengUI.getXianMengMainLayer()) end)")
 request('pet_task',83)
 request('pet_field',86,two_type=1)
 lines.append("step('pet_shop_entry',function() ms.d_pethuntUI.g_pethuntUI.shop_parent=ms.d_xianmengUI.getXianMengMainLayer() end)")
 request('pet_shop',91,two_type=1)
 request('pet_rank',92,two_type=1,query_type=1)
 lines.append("step('escort_open',function() ms.d_escortUI.show(ms.d_xianmengUI.getXianMengMainLayer());ms.d_escortUI.tapMenuMain(1) end)")
 request('escort_road',69,flag=3,road_type=1)
 request('escort_fetch',69,flag=4,road_type=1)
 request('escort_refresh',69,flag=5,road_type=1)
 request('escort_depart',69,flag=6,road_type=1,book_level=2,des_id=0)
 request('cross_schedule',58,query_type=21)
 request('cross_list',58,query_type=30)
 request('cross_enter',58,query_type=32)
 request('cross_shop',58,query_type=33)

 lines.append("""local i=0
local function restore()
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
 ms.d_xianmengUI.getGuildConfig(saved.guildConfig)
 ms.d_mainUI.show();guild_fixture_restored=true
end
local scheduler=CCDirector:sharedDirector():getScheduler();local handle
handle=scheduler:scheduleScriptFunc(function()
 if i>0 then guild_fixture_results[i]={name=cases[i].name,ok=errors=='',error=errors} end
 i=i+1
 if i>#cases then scheduler:unscheduleScriptEntry(handle);restore();return end
 errors='';local ok,err=xpcall(cases[i].run,debug.traceback)
 if not ok then errors=errors..'\\n'..tostring(err) end
end,1,false)
return 'guild fixture started' 
""")
 (ROOT/'.runtime/guild-fixture.lua').write_text('\n'.join(lines));b.close()
print('Wrote isolated guild client fixture')
