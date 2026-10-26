"""Build isolated native 3.87 callbacks; network sends are captured, never sent."""
import copy
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_duty as duty, summon
from network_redirect.backend import Backend

NOW = 1792814400
with tempfile.TemporaryDirectory() as tmp:
    b = Backend(Path(tmp), 18770, lambda *a, **k: None)
    role = b.profile(); role['level'] = 60
    r = b.activity_rules
    activity.prepare(role, NOW, r)
    fixtures = {'entry': duty.data(role, r)}
    duty.start(role, r); fixtures['initial'] = duty.data(role, r)
    duty.update(role, dict(plus_type=1, plus_index=3, flag=0), NOW, r)
    fixtures['fight'] = duty.data(role, r)
    d = role['activity']['duty']
    d.update(round=4, stars=27, phase='prize', pending_silver=3000)
    duty.remember(d); duty.record(role)
    fixtures['prize'] = duty.data(role, r)
    fixtures['win_prize'] = duty.data(role, r, 8)
    duty.update(role, dict(plus_type=3, plus_index=1, flag=0), NOW, r)
    fixtures['exchange'] = duty.data(role, r)
    fixtures['mixed_exchange'] = copy.deepcopy(fixtures['exchange'])
    fixtures['mixed_exchange'].update(cur_get_star=108, cur_used_star=0,
        star_exchange=[dict(field=f, value=5*(i+1), star=9*(i+1)) for i, f in enumerate(duty.FIELDS)])
    index = next(i for i, o in enumerate(d['offers'], 1) if o['star'] <= d['stars']-d['used'])
    duty.update(role, dict(plus_type=2, plus_index=index, flag=0), NOW, r)
    d.update(round=31, stars=270); duty.remember(d); duty.record(role)
    fixtures['stage31'] = duty.data(role, r)
    fixtures['win_next'] = duty.data(role, r, 8)
    for label, reward in [('bag', [5, 1032, 1, 1]), ('silver_bag', [5, 1033, 1, 1]),
                          ('cloth_bag', [5, 1034, 1, 1]), ('gold', [11, 0, 30, 1])]:
        d.update(phase='prize', pending_rewards=[reward], after_prize='fight')
        fixtures[label+'_prize'] = duty.data(role, r)
        fixtures[label+'_win'] = duty.data(role, r, 8)
        duty.update(role, dict(plus_type=3, plus_index=1, flag=0), NOW, r)
        fixtures[label+'_claimed'] = duty.data(role, r)
    d['phase'] = 'finished'
    fixtures['half'] = duty.data(role, r)
    fixtures['lose'] = duty.data(role, r, 9)
    rank = duty.rank_data(role)
    role['activity']['duty_runs'] = 3
    fixtures['exhausted'] = duty.data(role, r)
    activity.prepare(role, NOW+86400, r)
    fixtures['yesterday'] = duty.data(role, r)
    b.close()

script = r'''
local ms=assert(package.loaded.ms);local ui=assert(ms.d_endlessFightUI)
local act=ms.d_activityUI;local login=ms.d_loginUI
local saved={};for k,v in pairs(ui) do saved[k]=v end
local auxiliary={}
for _,name in ipairs({'d_messageUI','d_commonLayerUI','d_lineupUI','d_mysteryUI'}) do
 local t=ms[name];local old={};for k,v in pairs(t) do old[k]=v end
 auxiliary[#auxiliary+1]={target=t,old=old}
end
local oldself,oldstatus,oldcurrent,oldrun=act.g_self,act.g_yishiStatus,act.g_currentActivity,act.g_isCurrentSenceRun
local oldscene=login.g_currentSence
local gid=act.activityID.tianmingzhizhan;local oldguide=act.g_activityGuide[gid]
local send=ms.d_u.main_server_send_msg;local report=ms.MS_report_error
local root=CCLayer:create();CCDirector:sharedDirector():getRunningScene():addChild(root,9999)
act.g_self={main_layer=root};act.g_yishiStatus={cur_fight_count=3,max_fight_count=3}
act.g_currentActivity=gid;act.g_isCurrentSenceRun=true;act.g_activityGuide[gid]=true
login.g_currentSence=login.senceID.adventure
for _,k in ipairs({'g_mainLayer','g_startPageLayer','g_fightTypeLayer','g_bounsTypeLayer','g_bounsIntroLayer','g_rankLayer','g_rankMenu'}) do ui[k]=nil end
local sent={};ms.d_u.main_server_send_msg=function(mid,d) sent[#sent+1]={mid=mid,data=d} end
local errors='';ms.MS_report_error=function(e) errors=errors..'\n'..tostring(e) end
local results={}
local function check(name,fn)
 errors='';local ok,err=xpcall(fn,debug.traceback)
 results[#results+1]={name=name,ok=ok and errors=='',error=(err or '')..errors}
end
'''
script += '\nlocal fixtures='+summon.lua(fixtures)+'\nlocal rank='+summon.lua(rank)+'\n'
script += r'''
for _,name in ipairs({'entry','initial','fight','prize','exchange','stage31','half','exhausted','yesterday',
 'bag_prize','gold_prize','bag_claimed','gold_claimed','silver_bag_prize','cloth_bag_prize','mixed_exchange'}) do
 check(name,function() ui.getEndlessFightRes(fixtures[name]) end)
end
check('win_prize_return',function() ui.getEndlessFightRes(fixtures.win_prize);ui.showFightRes() end)
check('win_next_return',function() ui.getEndlessFightRes(fixtures.win_next);ui.showFightRes() end)
check('bag_win_return',function() ui.getEndlessFightRes(fixtures.bag_win);ui.showFightRes() end)
check('gold_win_return',function() ui.getEndlessFightRes(fixtures.gold_win);ui.showFightRes() end)
check('loss_return',function() ui.getEndlessFightRes(fixtures.lose);ui.showFightLosePage() end)
check('rank_all_groups',function() ui.getRankInfo(rank);for i=1,5 do ui.createRankCells(i) end end)
check('native_next_stage_request',function()
 ui.g_dataTable=fixtures.stage31;ui.chooseFightType(3)
 local req=sent[#sent];assert(req.mid==1026 and req.data.des_value==31 and req.data.des_type==3 and req.data.des_id==0)
end)
check('native_blessing_request',function()
 ui.g_isInitBonus=true;ui.getBouns(3)
 assert(sent[#sent].data.plus_type==1 and sent[#sent].data.plus_index==3)
end)
check('native_exchange_request',function()
 ui.g_isInitBonus=false;ui.getBouns(2)
 assert(sent[#sent].data.plus_type==2 and sent[#sent].data.plus_index==2)
end)
check('native_claim_request',function()
 ui.ensurePrizeCallBack();assert(sent[#sent].data.plus_type==3)
end)
root:removeFromParentAndCleanup(true)
for k in pairs(ui) do if saved[k]==nil then ui[k]=nil end end
for k,v in pairs(saved) do ui[k]=v end
for _,entry in ipairs(auxiliary) do
 for k in pairs(entry.target) do if entry.old[k]==nil then entry.target[k]=nil end end
 for k,v in pairs(entry.old) do entry.target[k]=v end
end
act.g_self=oldself;act.g_yishiStatus=oldstatus;act.g_currentActivity=oldcurrent;act.g_isCurrentSenceRun=oldrun
act.g_activityGuide[gid]=oldguide;login.g_currentSence=oldscene
ms.d_u.main_server_send_msg=send;ms.MS_report_error=report
local out={};for _,v in ipairs(results) do out[#out+1]=v.name..':'..tostring(v.ok)..':'..v.error end
return table.concat(out,'\n')
'''
(ROOT/'.runtime/duty-fixture.lua').write_text(script)
print('Built 26 original-client callback checks; no real save or request is changed')
