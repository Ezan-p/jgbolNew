"""Render new rank rules in native Cocos using disposable packets and blocked sends."""
import json
import runpy
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from android_emulator.config import load_config,device_environment
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def main():
    import frida
    runpy.run_path(str(ROOT/'analysis/tools/build_rank_client_fixture.py'))
    config=load_config(ROOT/'game.json')
    pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=10).attach(pid)
    evaluator=LUA_EVALUATOR.replace('pending={code,resolve};',"const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    script=session.create_script(evaluator);report=dict(native_cocos=True,live_save_modified=False)
    output=ROOT/'analysis/evidence/rank';output.mkdir(exist_ok=True)
    def check(code):
        result=script.exports_sync.evaluate(code)
        if result.get('status')!=0:raise RuntimeError(result)
        return result['result']
    try:
        script.load()
        check((ROOT/'.runtime/rank-fixture.lua').read_text())
        report['board']=check("local ui=package.loaded.ms.d_rankUI;ui.g_rankUI=nil;ui.g_isInRankPage=false;ui.g_isInChangePage=false;local v=rank_fixture_next();assert(rank_fixture_errors=='',rank_fixture_errors);package.loaded.ms.d_activityUI.show();ui.showRankUI();assert(rank_fixture_errors=='',rank_fixture_errors);return v")
        report['daily']=check("""local ms=package.loaded.ms;local ui=ms.d_rankUI
assert(ui.getScoreSpeedByOrder(1)==4400 and ui.getScoreSpeedByOrder(100)==3584)
assert(ms.d_hz.gethz('fengshenbang_rank_credits_speed')=='日积分: %d')
assert(ms.d_hz.gethz('fengshenbang_rank_credits_tip')=='（每日零点刷新一次）')
assert(not ui.g_rankUI.show_labels.top_day_rewards_button:isVisible())
return 'daily labels and automatic settlement verified'""")
        report['closed']=check("""local ms=package.loaded.ms;local send,info=ms.d_u.main_server_send_msg,ms.d_info.show
local count=0;ms.d_u.main_server_send_msg=function() error('unexpected request') end
ms.d_info.show=function(text) assert(text=='离线模式，暂未开启');count=count+1 end
local ok,err=pcall(function() ms.d_rankUI.requestCrossRankFromRank();ms.d_rankUI.requestCrossRank();ms.d_crossRankUI.show() end)
ms.d_u.main_server_send_msg=send;ms.d_info.show=info;assert(ok,err);assert(count==3)
return 'all cross tournament entries blocked without requests'""")
        report['exchanges']=check("""local ms=package.loaded.ms;local ui=ms.d_rankUI;local rows=ms.d_data.g_topScoreExchangeTable
assert(#rows==9 and rows[1].score==5000 and rows[1].count==100)
assert(rows[2].score==0 and rows[2].sub_type==1343 and rows[2].count==1)
assert(rows[2].costItem==1001 and rows[2].costCount==1000 and rows[2].exchangeIndex==3)
local tiers={{500,50},{100,100},{50,200},{30,300},{20,400},{10,1000},{1,2000}}
for i,t in ipairs(tiers) do local row=rows[i+2];assert(row.promoteOrder==t[1] and row.object_type==11 and row.count==t[2]) end
ui.goToCreditsChargePage();assert(rank_fixture_errors=='',rank_fixture_errors)
assert(#ui.g_label_info==9)
assert(ui.g_label_info[2].text:getString()=='需蟠桃: 1000')
local names={'蟠桃: 100','圣母蟠桃: 1','元宝: 50'}
for _,node in pairs(ui.g_chargeNode) do
 local i=node:getTag()
 if names[i] then
  local label=tolua.cast(node:getChildren():objectAtIndex(3),'CCLabelTTF'):getString()
  assert(label:find(names[i],1,true),label)
 end
end
local count,send,info=ms.d_data.getItemCountByType,ms.d_u.main_server_send_msg,ms.d_info.show
local sent={};local notice
ms.d_u.main_server_send_msg=function(mid,data) assert(mid==1203);sent[#sent+1]=data.exchange_type end
ms.d_info.show=function(text) notice=text end
local ok,err=pcall(function()
 ms.d_data.getItemCountByType=function(kind,id) assert(kind==5 and id==1001);return 999 end
 ui.update_label_state(2);assert(not ui.g_label_info[2].btn:isVisible())
 ui.chargeButtonCallBack(2);assert(#sent==0 and notice=='蟠桃不足')
 ms.d_data.getItemCountByType=function() return 1000 end
 ui.update_label_state(2);assert(ui.g_label_info[2].btn:isVisible())
 ui.chargeButtonCallBack(2);assert(sent[1]==3)
 ui.g_rankInfo.self_score=5000;ui.chargeButtonCallBack(1);assert(sent[2]==1)
end)
ms.d_data.getItemCountByType=count;ms.d_u.main_server_send_msg=send;ms.d_info.show=info
assert(ok,err);ui.update_label_state(2)
ms.d_data.callback_update_config({local_rank={score=7777,previous_best=20,pending_score=0,current_order=100}})
assert(ui.g_rankInfo.self_score==7777)
assert(not ui.g_rankUI.show_labels.top_day_rewards_button:isVisible())
return 'all 9 exchange and promotion cells rendered'""")
        shot=subprocess.run([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'],env=device_environment(config),capture_output=True,timeout=15,check=True)
        (output/'peach_exchange_native.png').write_bytes(shot.stdout)
        report['passed']=True
    finally:
        try:report['restore']=check("if rank_fixture_restore then return rank_fixture_restore() end;return 'no fixture'")
        finally:script.unload();session.detach()
        (output/'peach_exchange_client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
