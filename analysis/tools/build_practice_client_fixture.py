"""Build isolated native Cocos tests from genuine backend protocol responses."""
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_practice as practice, summon
from network_redirect.backend import Backend
from network_redirect.protocol import encode, decode

fixtures = {}
with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time', return_value=1792814400):
    b = Backend(Path(tmp), 18770, lambda *a, **k: None)
    r = b.profile(); r['level'] = 60
    for c in r['corteges']: c['level'] = 100
    activity.prepare(r, 1792814400, b.activity_rules)
    r['activity']['fight_id'] = int(time.monotonic()*1000) % 2000000000
    b.save(r)
    for serial, stat in enumerate(practice.FIELDS, 100001):
        with patch.object(practice, 'draw', return_value=stat):
            replies = b.respond(encode(1026, dict(serial_num=serial, fight_type=4, des_type=1)), {'authenticated': True})
        rows = []
        for reply in replies:
            mid, _, data = decode(reply)
            assert not (mid == 2998 and data['id'] == 55), data
            if mid in (1027, 1028) or mid == 2998 and data['id'] in (5, 121):
                rows.append([mid, data])
        fixtures[stat] = rows
    b.close()

script = r'''
local ms=assert(package.loaded.ms);local ui=ms.d_practiceUI;local mgr=ms.d_event_mgr
if practiceFixtureRestore then practiceFixtureRestore() end
local saved={}
for _,t in ipairs({ui,mgr,ms.d_activityUI,ms.d_lineupUI,ms.d_fightUI}) do
 local old={};for k,v in pairs(t) do old[k]=v end;saved[#saved+1]={t=t,old=old}
end
local oldPlayer=ms.d_mainUI.g_playerInfo
local oldSend,oldReport=ms.d_u.main_server_send_msg,ms.MS_report_error
local root=CCLayer:create();root:retain()
function practiceFixtureRestore()
 root:removeAllChildrenWithCleanup(true);root:release()
 for _,entry in ipairs(saved) do
  for k in pairs(entry.t) do if entry.old[k]==nil then entry.t[k]=nil end end
  for k,v in pairs(entry.old) do entry.t[k]=v end
 end
 ms.d_mainUI.g_playerInfo=oldPlayer;ms.d_u.main_server_send_msg=oldSend;ms.MS_report_error=oldReport
 practiceFixtureRestore=nil
end
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(oldPlayer)
local p=ms.d_mainUI.g_playerInfo;p.level=5;p.rule_index=0
p.max_hp_plus=0;p.max_magic_plus=0;p.gongji_plus=0;p.fangyu_plus=0
ms.d_activityUI.g_self={main_layer=root}
mgr.g_fight_info={};mgr.g_fight_id_list={}
ms.d_lineupUI.saveLastFightLevel=function() end
local sent,errors,checks={},'',{}
ms.d_u.main_server_send_msg=function(mid,d) sent[#sent+1]={mid=mid,data=d} end
ms.MS_report_error=function(e) errors=errors..'\n'..tostring(e) end
local star=3;ms.d_fightUI.getLastFightStar=function() return star end
local function check(name,fn)
 errors='';local ok,err=xpcall(fn,debug.traceback)
 checks[#checks+1]={name=name,ok=ok and errors=='',error=(err or '')..errors}
end
local function show()
 root:removeAllChildrenWithCleanup(true);ui.g_mainLayer=nil;ui.g_resLayer=nil;ui.show()
end
check('entry_and_native_request',function()
 show();assert(ui.g_practiceCount==1)
 ui.startPractice();local q=sent[#sent]
 assert(q.mid==1026 and q.data.fight_type==4 and q.data.des_type==1 and q.data.des_id==0 and q.data.des_value==0)
end)
check('exhausted_and_levelup',function()
 p.rule_index=1;show();assert(ui.g_practiceCount==0)
 local n=#sent;ui.startPractice();assert(#sent==n)
 p.level=6;show();assert(ui.g_practiceCount==1)
end)
local fixtures=__FIXTURES__
for _,stat in ipairs({'hp','magic','gongji','fangyu'}) do
 check('backend_wire_single_reward_'..stat,function()
  show();ui.g_increasedValue={};local fid
  for _,row in ipairs(fixtures[stat]) do
   if row[1]==1028 then fid=row[2].fight_id;mgr.fight_lineup_1028(nil,row[2],0)
   elseif row[1]==1027 then mgr.fight_result_1027(nil,row[2],0)
   elseif row[1]==2998 then mgr.msg_common_event_2998(nil,row[2],nil) end
  end
  assert(mgr.g_fight_info[fid].line_up_msg.lineup[1].des_type==5001)
  local n=0;for k,v in pairs(ui.g_increasedValue) do n=n+1;assert(v>0) end;assert(n==1)
  star=3;ui.createPracticeResBox();assert(ui.g_resLayer)
  assert(next(ui.g_increasedValue)==nil,'unconsumed reward leaks into next result')
  ui.practiceButtonTaped(1)
 end)
end
check('defeat_retry_and_return',function()
 show();star=0;ui.g_increasedValue={};ui.createPracticeResBox()
 local n=#sent;ui.practiceButtonTaped(2);assert(#sent==n+1 and sent[#sent].data.fight_type==4)
 ui.practiceButtonTaped(1)
end)
local strings={win=ms.d_hz.gethz('practiceWinHint'),lose=ms.d_hz.gethz('practiceLoseHint'),limit=ms.d_hz.gethz('noPracticeCount')}
practiceFixtureRestore()
return ms.d_json.encode({checks=checks,strings=strings,original_cocos=true,network_intercepted=true,state_restored=true})
'''
path = ROOT / '.runtime/practice-fixture.lua'
path.write_text(script.replace('__FIXTURES__', summon.lua(fixtures)))
print(path)

# Optional three-step animation acceptance; uses the same disposable backend battle.
replay = r'''
local ms=assert(package.loaded.ms)
assert(not practiceReplayRestore,'finish previous replay first')
assert(not land_fixture_restore and not rank_fixture_restore,'another activity fixture is active')
local p=ms.d_mainUI.g_playerInfo
local send,report,save=ms.d_u.main_server_send_msg,ms.MS_report_error,ms.d_lineupUI.saveLastFightLevel
local mgr=ms.d_event_mgr;local fights,ids=mgr.g_fight_info,mgr.g_fight_id_list
local dispatch=mgr.g_msg_fun
local errors=''
ms.d_mainUI.g_playerInfo=ms.d_c.table_copy(p)
ms.d_mainUI.g_playerInfo.level=60;ms.d_mainUI.g_playerInfo.rule_index=1
ms.d_u.main_server_send_msg=function(mid,...) if mid==2999 then return send(mid,...) end end
local isolated={};for mid,fn in pairs(dispatch) do isolated[mid]=mid==2999 and fn or function() end end
mgr.g_msg_fun=isolated
ms.MS_report_error=function(e) errors=errors..'\n'..tostring(e) end
ms.d_lineupUI.saveLastFightLevel=function() end
mgr.g_fight_info={};mgr.g_fight_id_list={}
function practiceReplayRestore()
 ms.d_mainUI.g_playerInfo=p;ms.d_u.main_server_send_msg=send;ms.MS_report_error=report
 ms.d_lineupUI.saveLastFightLevel=save;mgr.g_fight_info=fights;mgr.g_fight_id_list=ids
 mgr.g_msg_fun=dispatch
 practiceReplayRestore=nil;practiceReplayFinish=nil;practiceReplayStart=nil
 ms.d_mainUI.show()
end
function practiceReplayFinish()
 local f=ms.d_fightUI.g_fightUI
 if not f.is_fight_end then return ms.d_json.encode({finished=false,errors=errors}) end
 local result=f.last_final_result
 ms.d_fightUI.menuHome_private()
 local out={finished=true,result=result,errors=errors,result_layer=ms.d_practiceUI.g_resLayer~=nil,
            unconsumed_reward=next(ms.d_practiceUI.g_increasedValue)~=nil,network_intercepted=true}
 practiceReplayRestore();out.state_restored=true
 return ms.d_json.encode(out)
end
function practiceReplayStart()
ms.d_practiceUI.g_increasedValue={}
local fid
for _,row in ipairs(__WIRE__) do
 if row[1]==1028 then fid=row[2].fight_id;mgr.fight_lineup_1028(nil,row[2],0)
 elseif row[1]==1027 then mgr.fight_result_1027(nil,row[2],0)
 elseif row[1]==2998 then mgr.msg_common_event_2998(nil,row[2],nil) end
end
mgr.msg_common_event_2998(nil,{id=44,data='{fight_id='..fid..',fight_type=4}'},nil)
return ms.d_json.encode({started=true,enemy=5001,errors=errors})
end
ms.d_activityUI.show(2)
return 'practice scene requested; call practiceReplayStart after scene transition'
'''
(ROOT / '.runtime/practice-replay.lua').write_text(replay.replace('__WIRE__', summon.lua(fixtures['hp'])))
(ROOT / '.runtime/practice-replay-start.lua').write_text('return practiceReplayStart()')
(ROOT / '.runtime/practice-replay-finish.lua').write_text('return practiceReplayFinish()')
