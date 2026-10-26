"""Produce disposable land packets for the original Lua VM; never opens live DB."""
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from network_redirect import activity, summon
from network_redirect.backend import Backend
from network_redirect.protocol import encode,decode
ROOT=Path(__file__).resolve().parents[2]
NOW=1792814400
lines=['''local ms=assert(package.loaded.ms)
assert(not land_fixture_restore,'restore previous land fixture first')
local saved={player=ms.d_mainUI.g_playerInfo,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,config=ms.d_data.g_new_config,time=ms.d_time.getTime}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
ms.d_u.main_server_send_msg=function(...) end
land_fixture_errors='';land_fixture_results={}
ms.MS_report_error=function(e) land_fixture_errors=land_fixture_errors..'\\n'..tostring(e) end
local cases={};local index=0
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1028 then ms.d_event_mgr.fight_lineup_1028(nil,d,0)
 elseif mid==1027 then ms.d_event_mgr.fight_result_1027(nil,d,0)
 elseif mid==1022 then ms.d_event_mgr.msg_update_top_list_1022(nil,d,nil)
 elseif mid==2995 then ms.d_event_mgr.msg_send_tip_info_2995(nil,d,nil)
 elseif mid==2998 then ms.d_event_mgr.msg_common_event_2998(nil,d,nil) end
end
function land_fixture_restore()
 if ms.d_landUI.g_landUI and ms.d_landUI.g_landUI.main_layer then ms.d_landUI.pressClose() end
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report;ms.d_time.getTime=saved.time
 land_fixture_restore=nil
 ms.d_mainUI.show()
 return 'land fixture restored'
end
function land_fixture_next()
 index=index+1;if not cases[index] then return 'finished' end
 land_fixture_errors='';local ok,err=xpcall(cases[index].run,debug.traceback)
 if not ok then land_fixture_errors=land_fixture_errors..'\\n'..tostring(err) end
 land_fixture_results[index]={name=cases[index].name,ok=ok,error=land_fixture_errors}
 return cases[index].name..': '..land_fixture_errors
end
''']
with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time',return_value=NOW):
 b=Backend(Path(tmp),18770,lambda *a,**k:None);r=b.profile();r.update(level=60,energy=100,gold_coin=10000,silver_coin=10000)
 for c in r['corteges']:c['level']=100
 activity.prepare(r,NOW,b.activity_rules);b.save(r)
 lines.append('ms.d_time.getTime=function() return '+str(NOW)+' end')
 for k in ('level','energy','gold_coin','silver_coin','role_id'):lines.append('ms.d_mainUI.g_playerInfo.'+k+'='+str(r.get(k,0)))
 serial=100000
 def request(name,mid=1302,pre='',**d):
  global serial
  serial+=1;packets=b.respond(encode(mid,dict(serial_num=serial,**d)),dict(authenticated=True))
  lines.append('step('+summon.lua(name)+',function() '+pre)
  for p in packets:
   m,_,data=decode(p)
   if m==2998 and data['id']==55:raise AssertionError((name,data))
   if m in (1032,1027,1028,2995,2998):lines.append('apply('+str(m)+','+summon.lua(data)+')')
  lines.append('end)')
 def land(name,op,pre='',**d):request(name,id=op,data=summon.lua(d),pre=pre)
 def team(name,op,**d):request(name,1303,id=1,op_type=op,data=summon.lua(d))
 land('enter',1,pre='ms.d_mainUI.show();ms.d_activityUI.show(8)')
 land('travel',3)
 land('travel_battle',4,pre='ms.d_lineupUI.saveLastFightLevel()',flag=1,des_type=1,des_id=942001)
 land('battle_return',1)
 land('rank',18,flag=1)
 land('week_rank',18,flag=2)
 land('hell_rank',27)
 land('news',10)
 land('return_map',1)
 request('team_enter',1303,id=1,op_type=9,data=summon.lua(dict(query_type=1)),pre='ms.d_teamUI.queryTeam(1,ms.d_landUI.g_landUI.main_layer,100)')
 team('team_create',1)
 team('team_applications',10)
 team('team_accept',3,id_list=[940001,940002])
 team('team_order',11,id_list=[940002,r['role_id'],940001])
 team('team_dismiss',7)
 r=b.profile();r['activity']['land']['boss_layer']=3;b.save(r)
 land('boss',12)
 land('sweep',13)
 with patch('network_redirect.backend.time.time',return_value=NOW+8*3600):
  land('tower_map',1,pre='ms.d_time.getTime=function() return '+str(NOW+8*3600)+' end')
  land('tower_detail',11,tower_id=12)
 b.close()
lines.append("return 'land fixture ready: '..#cases..' steps'")
(ROOT/'.runtime/land-fixture.lua').write_text('\n'.join(lines))
(ROOT/'.runtime/land-players-client-check.lua').write_text(
 'local install=function()\n'+'\n'.join(lines)+'\nend\ninstall()\n'+
 (ROOT/'analysis/tools/land_players_client_harness.lua').read_text())
print('Wrote isolated land fixture')
