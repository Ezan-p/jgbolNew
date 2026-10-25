"""Produce disposable rank packets for the original Lua VM; never opens live DB."""
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from network_redirect import activity, activity_rank as rank, summon
from network_redirect.backend import Backend
from network_redirect.protocol import encode,decode
ROOT=Path(__file__).resolve().parents[2]
NOW=1792933200
lines=['''local ms=assert(package.loaded.ms)
assert(not rank_fixture_restore and not land_fixture_restore,'another fixture is active; restore it before rank testing')
local saved={player=ms.d_mainUI.g_playerInfo,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,config=ms.d_data.g_new_config,time=ms.d_time.getTime}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
ms.d_u.main_server_send_msg=function(...) end
rank_fixture_errors='';rank_fixture_results={}
ms.MS_report_error=function(e) rank_fixture_errors=rank_fixture_errors..'\\n'..tostring(e) end
local cases={};local index=0
local function step(name,fn) cases[#cases+1]={name=name,run=fn} end
local function apply(mid,d)
 if mid==1032 and d.unit_type==1 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1028 then ms.d_event_mgr.fight_lineup_1028(nil,d,0)
 elseif mid==1027 then ms.d_event_mgr.fight_result_1027(nil,d,0)
 elseif mid==1022 then ms.d_event_mgr.msg_update_top_list_1022(nil,d,nil)
 elseif mid==2998 then ms.d_event_mgr.msg_common_event_2998(nil,d,nil) end
end
function rank_fixture_restore()
 if ms.d_rankUI._localRankRestore then ms.d_rankUI._localRankRestore() end
 ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
 ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report;ms.d_time.getTime=saved.time
 rank_fixture_restore=nil
 ms.d_mainUI.show()
 return 'rank fixture restored'
end
function rank_fixture_next()
 if index>0 and rank_fixture_errors~='' then rank_fixture_results[index].error=rank_fixture_errors;rank_fixture_results[index].ok=false end
 index=index+1;if not cases[index] then return 'finished' end
 rank_fixture_errors='';local ok,err=xpcall(cases[index].run,debug.traceback)
 if not ok then rank_fixture_errors=rank_fixture_errors..'\\n'..tostring(err) end
 rank_fixture_results[index]={name=cases[index].name,ok=ok,error=rank_fixture_errors}
 return cases[index].name..': '..rank_fixture_errors
end
''']
lines.append((ROOT/'network_redirect/rank_client.lua').read_text())
lines.append((ROOT/'network_redirect/monument_client.lua').read_text())
with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time',return_value=NOW):
 b=Backend(Path(tmp),18770,lambda *a,**k:None);r=b.profile();r.update(level=60,energy=100,gold_coin=10000,silver_coin=10000)
 for c in r['corteges']:c['level']=100
 activity.prepare(r,NOW,b.activity_rules)
 # Native replay caches persist between fixture runs; use fresh fight IDs.
 r['activity']['fight_id']=int(time.monotonic()*1000)%2000000000
 summon.add_item(r,1021,2);b.save(r)
 lines.append('ms.d_time.getTime=function() return '+str(NOW)+' end')
 for k in ('level','energy','gold_coin','silver_coin','top_order','top_score','top_fight_limit','top_day_prize_time'):lines.append('ms.d_mainUI.g_playerInfo.'+k+'='+str(r.get(k,0)))
 serial=100000
 def request(name,mid,pre='',**d):
  global serial
  serial+=1;packets=b.respond(encode(mid,dict(serial_num=serial,**d)),dict(authenticated=True))
  lines.append('step('+summon.lua(name)+',function() '+pre)
  for p in packets:
   m,_,data=decode(p)
   if m==2998 and data['id']==55:raise AssertionError((name,data))
   if m in (1032,1022,1027,1028,2998):lines.append('apply('+str(m)+','+summon.lua(data)+')')
  lines.append('end)')
 request('board',1021,'ms.d_activityUI.show(3)',flag=0)
 request('inspect_beginner',1039,des_id=930099,des_type=2)
 request('inspect_champion',1039,des_id=930001,des_type=2)
 request('board_again',1021,'ms.d_activityUI.show(3)',flag=0)
 request('battle_win',1026,'ms.d_lineupUI.saveLastFightLevel()',fight_type=2,des_type=2,des_value=99,des_id=930099)
 lines.append("step('return_after_battle',function() assert(ms.d_fightUI.g_fightUI.is_fight_end,'battle still running');ms.d_fightUI.menuHome_private() end)")
 lines.append("step('flip_card',function() ms.d_rankUI.chickRewardsCard(1) end)")
 request('token',1051,'ms.d_rankUI.closeRewardsPage()',item_type=1021,item_count=1,des_type=1)
 request('promotion',1203,exchange_type=7)
 request('records',1244,'ms.d_rankUI._localRankOpenRecords()',fight_type=2)
 lines.append("step('replay_record',function() ms.d_fightrecordUI.play_fightRecord(1) end)")
 lines.append("step('return_after_replay',function() assert(ms.d_fightUI.g_fightUI.is_fight_end,'replay still running');ms.d_fightUI.menuHome_private() end)")
 with patch('network_redirect.backend.time.time',return_value=NOW+86400):
  request('new_day_board',1021,'ms.d_activityUI.show(3);ms.d_time.getTime=function() return '+str(NOW+86400)+' end',flag=0)
  request('daily_prize',1201,flag=2)
 b.close()
lines.append("return 'rank fixture ready: '..#cases..' steps'")
(ROOT/'.runtime/rank-fixture.lua').write_text('\n'.join(lines))
print('Wrote isolated rank fixture')
