"""Generate isolated real-client UI probes from a temporary backend save."""
import sys, tempfile, copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect.backend import Backend, login_fields
from network_redirect import activity, activity_party as party, summon
from network_redirect.protocol import decode
NOW=1792814400
with tempfile.TemporaryDirectory() as tmp:
    b=Backend(Path(tmp),18770,lambda *a,**kw:None)
    r=b.profile();r.update(level=60,gold_coin=10000)
    activity.prepare(r,NOW,b.activity_rules)
    result=activity.battle(r,dict(fight_type=6,des_type=0,des_id=0,des_value=0),NOW,b.activity_rules,b.journey_rules,b.formation_rules)
    live=party.info(r,b.activity_rules)
    live['fight_prize']=[activity.prize_spec([5,1001,5,1])]
    activity.prepare(r,NOW+2*86400,b.activity_rules)
    history=login_fields(decode(party.query(r,2,b.activity_rules,{} )[0])[2]['data'])
    weekly=login_fields(decode(party.query(r,3,b.activity_rules,{} )[0])[2]['data'])
    top=party.client_config(r,b.activity_rules)['party_top_list']
    b.close()
script='''local ms=assert(package.loaded.ms);local ui=ms.d_worldBossUI
local saved={};for k,v in pairs(ui) do saved[k]=v end
local send=ms.d_u.main_server_send_msg;local report=ms.MS_report_error
local act=ms.d_activityUI;local oldself=act.g_self;local oldstatus=act.g_yishiStatus;local oldcurrent=act.g_currentActivity
local player=ms.d_mainUI.g_playerInfo;local oldplayer={};for k,v in pairs(player) do oldplayer[k]=v end
local root=CCLayer:create();ms.d_mainUI.g_mainUI.main_layer:addChild(root,9999)
act.g_self={main_layer=root};act.g_yishiStatus={party_free_count=0,party_pay_count=0};act.g_currentActivity=6
ms.d_u.main_server_send_msg=function() end
local errors='';ms.MS_report_error=function(e) errors=errors..'\\n'..tostring(e) end
party_fixture_results={}
local function check(name,fn)
 errors='';local ok,err=xpcall(fn,debug.traceback)
 party_fixture_results[#party_fixture_results+1]={name=name,ok=ok and errors=='',error=(err or '')..errors}
end
ui.setPeriod({{begin_seconds=0,end_seconds=86400}})
check('entry',function() ui.show() end)
'''
script += '\nlocal live='+summon.lua(live)+'\nlocal history='+summon.lua(history)+'\nlocal weekly='+summon.lua(weekly)+'\n'
script += '''check('fight_data_and_rank',function() ui.getFightInfo(live);ui.showStartFightPage();ui.pullDownRankLayer() end)
check('fight_reward',function() ui.showAward() end)
check('history_and_felstar',function() ui.getFightNewsRes(history) end)
check('weekly_rank_and_prize_button',function() player.party_take_prize=0;ui.getLuckRankRes(weekly) end)
'''
script += '\nui.g_topList='+summon.lua(top)+'\n'
script += '''check('champion_notice',function() ui.getWorldBossRankLayer(true) end)
check('exhausted',function() live.free_count=10;live.pay_count=5;ui.getFightInfo(live);ui.showStartFightPage() end)
root:removeFromParentAndCleanup(true)
for k in pairs(ui) do if saved[k]==nil then ui[k]=nil end end;for k,v in pairs(saved) do ui[k]=v end
for k in pairs(player) do if oldplayer[k]==nil then player[k]=nil end end;for k,v in pairs(oldplayer) do player[k]=v end
act.g_self=oldself;act.g_yishiStatus=oldstatus;act.g_currentActivity=oldcurrent
ms.d_u.main_server_send_msg=send;ms.MS_report_error=report
local out={};for _,v in ipairs(party_fixture_results) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\\n')
'''
(ROOT/'.runtime/party-fixture.lua').write_text(script)
print('Built 7 original-client probes')
