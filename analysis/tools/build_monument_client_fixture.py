"""Render disposable backend packets through original client callbacks; restore player."""
import sys,tempfile,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from network_redirect.backend import Backend,login_fields
from network_redirect import summon,monument,guild,guild_match
from network_redirect.protocol import encode,decode
ROOT=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as t:
 b=Backend(Path(t),18790,lambda *a,**k:None);r=b.profile();r.update(level=30,gold_coin=10000,silver_coin=10000);b.save(r)
 lines=['''local ms=assert(package.loaded.ms)
local saved={player=ms.d_mainUI.g_playerInfo,send=ms.d_u.main_server_send_msg,report=ms.MS_report_error,config=ms.d_data.g_new_config,guild=ms.d_xianmengUI.guildConfig,time=ms.d_time.getTime}
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(saved.player)
ms.d_data.g_new_config=ms.d_c.table_copy(saved.config)
ms.d_u.main_server_send_msg=function(...) end
for i=1,20 do local n,v=debug.getupvalue(ms.d_crossRankUI.show,i);if n=="g_self" then v.main_layer=nil end end
for i=1,20 do local n=debug.getupvalue(ms.d_crossRankUI.getResFromServer,i);if n=="g_vsList" or n=="g_top_list" then debug.setupvalue(ms.d_crossRankUI.getResFromServer,i,{}) end end
local errors='';monument_fixture_results={};monument_fixture_restored=false
ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
local cases={}
local function step(name,fn,hold) cases[#cases+1]={name=name,run=fn,hold=hold or 0} end
local function apply(mid,d)
 if mid==1301 then ms.d_event_mgr.msg_union_event_1301(nil,d,0)
 elseif mid==1032 then ms.d_event_mgr.msg_modify_attr_1032(nil,d,nil)
 elseif mid==1028 then ms.d_event_mgr.fight_lineup_1028(nil,d,0)
 elseif mid==1027 then ms.d_event_mgr.fight_result_1027(nil,d,0)
 elseif mid==1022 then ms.d_event_mgr.msg_update_top_list_1022(nil,d,nil)
 elseif mid==1237 then ms.d_event_mgr.msg_get_single_toplist_1237(nil,d,nil)
 elseif mid==2998 then ms.d_event_mgr.msg_common_event_2998(nil,d,nil) end
end
''']
 lines.append((ROOT/'network_redirect/monument_client.lua').read_text())
 for k in ('level','gold_coin','silver_coin','union_id','union_rank','union_contrib','cur_union_contrib',*monument.ATTRS):lines.append('ms.d_mainUI.g_playerInfo.'+k+'='+str(r.get(k,0)))
 lines += ['ms.d_monumentUI.g_self.Config=nil', 'ms.d_xianmengUI.getGuildConfig('+summon.lua(guild.client_config(b.guild_rules))+')','ms.d_crossRankUI.initData('+summon.lua(monument.client_config(int(time.time()),b.monument_rules))+')']
 serial=5000
 def request(name,mid,pre='',**d):
  global serial
  serial+=1;replies=b.respond(encode(mid,dict(serial_num=serial,**d)),dict(authenticated=True))
  lines.append('step('+summon.lua(name)+',function() '+pre)
  for p in replies:
   m,_,data=decode(p)
   if m==2998 and data['id']==55:raise AssertionError((name,data))
   if m in (1301,1032,1022,1027,1028,1237,2998):lines.append('apply('+str(m)+','+summon.lua(data)+')')
  lines.append('end,'+str(30 if mid==1026 else 0)+')')
 request('champions',1128)
 request('cross_guild_schedule',1301,'ms.d_monumentUI.onClick(1)',id=58,data=summon.lua(dict(query_type=21)))
 request('cross_guild_local_list',1301,id=58,data=summon.lua(dict(query_type=30)))
 request('cross_guild_champions',1301,id=58,data=summon.lua(dict(query_type=22)))
 request('champions_again',1128)
 request('guild_schedule',1301,'ms.d_monumentUI.onClick(2)',id=18,data=summon.lua(dict(query_type=9)))
 lines.append("step('guild_champion_popup',function() local ui=ms.d_guildFightUI;local original=ui.createChampionLayer;ui.createChampionLayer(ms.d_guildFightUI.dataTable.main_layer,"+summon.lua(guild_match.champions(b.profile(),b.profile()['guild'],b.profile()['guild']['unions']['1'],b.guild_rules))+") end)")
 request('champions_fortune',1128)
 request('fortune_empty',1301,'ms.d_monumentUI.onClick(3)',id=18,data=summon.lua(dict(query_type=15)))
 request('champions_rank',1128)
 request('rank',1021,'ms.d_monumentUI.onClick(4)',flag=0)
 request('champions_cross',1128)
 request('cross_match',1232,'ms.d_monumentUI.onClick(5)')
 request('cross_refresh',1234,is_charge=0)
 request('cross_leaderboard',1236)
 request('cross_streak_prizes',1231)
 request('cross_main_for_lineup',1232)
 request('cross_lineup',1039,des_id=92001,des_type=1)
 request('cross_main_for_record',1232)
 info=monument.match_info(b.profile(),int(time.time()),b.monument_rules);target=info['enemy'][0]
 request('cross_battle',1026,'ms.d_lineupUI.saveLastFightLevel()',fight_type=18,des_id=target['player_id'],des_type=target['rank'],des_value=0)
 request('cross_after_battle',1232)
 request('cross_records',1244,fight_type=3)
 lines.append("step('play_record',function() ms.d_fightrecordUI.play_fightRecord(1) end,30)")
 request('cross_after_replay',1232)
 request('cross_main_for_claim',1232)
 request('cross_rank_claim',1238)
 lines.append("step('return_monument',function() ms.d_crossRankUI.menuClose() end)")
 request('champions_end',1128)
 from unittest.mock import patch
 start=monument.client_config(int(time.time()),b.monument_rules)['begin_fight_time']
 for label,offset in (('king_phase',21*3600),('paid_phase',23*3600+1)):
  at=start+offset
  with patch('network_redirect.backend.time.time',return_value=at):
   request(label,1232,'ms.d_time.getTime=function() return '+str(at)+' end')
 lines.append("step('restore_time',function() ms.d_time.getTime=saved.time end)")


 lines.append('''local i=0;local hold=0
local scheduler=CCDirector:sharedDirector():getScheduler();local handle
handle=scheduler:scheduleScriptFunc(function()
 if hold>0 then hold=hold-1;return end
 if i>0 then monument_fixture_results[i]={name=cases[i].name,ok=errors=='',error=errors} end
 i=i+1
 if i>#cases then
  scheduler:unscheduleScriptEntry(handle)
  ms.d_time.getTime=saved.time
  ms.d_u.main_server_send_msg=saved.send;ms.MS_report_error=saved.report
  ms.d_mainUI.g_playerInfo=saved.player;ms.d_data.g_new_config=saved.config
  ms.d_xianmengUI.getGuildConfig(saved.guild);ms.d_crossRankUI.initData(saved.config[19])
  ms.d_mainUI.show();monument_fixture_restored=true;return
 end
 hold=cases[i].hold
 errors='';local ok,err=xpcall(cases[i].run,debug.traceback)
 if not ok then errors=errors..'\\n'..tostring(err) end
end,0.5,false)
return 'monument fixture started'
''')
 output='monument-fixture.lua'
 if '--public-only' in sys.argv:
  selected=['champions','cross_guild_schedule','cross_guild_local_list','cross_guild_champions','champions_again','guild_schedule','guild_champion_popup','champions_fortune','fortune_empty']
  select='local wanted='+summon.lua({k:True for k in selected})+";local filtered={};for _,c in ipairs(cases) do if wanted[c.name] then filtered[#filtered+1]=c end end;cases=filtered\n"
  lines[-1]=lines[-1].replace('local i=0;',select+'local i=0;')
  output='monument-public-fixture.lua'
 (ROOT/'.runtime'/output).write_text('\n'.join(lines));b.close()
print('Wrote isolated monument fixture')
