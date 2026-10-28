"""Replay treasure search in native Cocos without spending live account resources.

Uses an isolated scene layer and reloads the latest adapter.
--repair-live also redraws that page from its settled cache, without another draw.
"""
import copy
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import time
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from network_redirect import summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def fixtures():
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time',return_value=1792728000):
        b=Backend(Path(tmp),18790,lambda *a,**k:None)
        try:
            role=b.profile();role.update(level=50,gold_coin=100000);b.save(role)
            serial=0
            def req(op,**data):
                nonlocal serial
                serial+=1
                rows=[decode(p) for p in b.respond(encode(1301,dict(serial_num=serial,id=op,data=summon.lua(data))),{'authenticated':True})]
                assert not any(m==2998 and d['id']==55 for m,_,d in rows),rows
                return next((login_fields(d['data']) for m,_,d in rows if m==1301 and d['id']==op),None)
            req(1,union_name='探宝回归')
            role=b.profile()
            req(5,role_list=list(map(int,role['guild']['unions']['2']['applications'])))
            req(26)
            applicants=list(map(int,b.profile()['guild']['instances']['team']['applications']))
            req(28,role_list=applicants[:2])
            role=b.profile();a=role['guild']['instances']
            a.update(layer=1,team_fights=1,team_last_fight_time=1792728000)
            b.save(role)
            team=req(44)
            initial=req(43,flag=1)
            role=b.profile();role['guild']['instances']['search_order']=list(range(18,0,-1));b.save(role)
            initial=req(43,flag=1)
            single=req(43,flag=2)
            sweep=req(43,flag=6)
            role=b.profile();role['guild']['instances'].update(layer=3,team_fights=3);b.save(role)
            complete=req(44)
            return dict(initial=initial,single=single,sweep=sweep,team=team,complete=complete)

        finally:b.close()


def main():
    import frida
    config=load_config(ROOT/'game.json')
    pid=next(p for p,n in processes(config).items() if n==config['package'])
    evaluator=LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    session=frida.get_device(config['serial'],timeout=10).attach(pid)
    script=session.create_script(evaluator);script.load()
    def evaluate(code):
        result=script.exports_sync.evaluate(code)
        if result.get('status')!=0:raise RuntimeError(result)
        return result['result']
    report={'native_cocos':True,'live_account_resources_changed':False}
    try:
        source=(ROOT/'analysis/tools/guild_search_client_harness.lua').read_text()
        source=source.replace('__FIXTURES__',summon.lua(fixtures()))
        source=source.replace('-- __PATCH__',(ROOT/'network_redirect/guild_activity_client.lua').read_text())
        report.update(login_fields(evaluate(source)))
        if report.get('passed'):
            preview=source[:source.index('local ok,err=xpcall(function()')]
            preview+="ui.callback_fam_search_gold(copy(fixtures.initial));return 'preview'"
            evaluate(preview)
            time.sleep(.5)
            raw=subprocess.check_output([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'])
            (ROOT/'analysis/evidence/guild/search_18_slots.png').write_bytes(raw)
            evaluate("guild_search_restore();return 'restored'")
            report['screenshot']='search_18_slots.png'
            preview=source[:source.index('local ok,err=xpcall(function()')]
            preview+="state.teams_info=copy(fixtures.team);state.teams_info.team.last_search_time=ms.d_time.getTime();state.fight_count=1;state.free_times=3;ui.showTeamPage();return 'team preview'"
            evaluate(preview)
            time.sleep(.5)
            raw=subprocess.check_output([str(config['adb_path']),'-s',config['serial'],'exec-out','screencap','-p'])
            (ROOT/'analysis/evidence/guild/search_single_action.png').write_bytes(raw)
            evaluate("guild_search_restore();return 'restored'")
            report['team_screenshot']='search_single_action.png'
        if report.get('passed') and '--repair-team' in sys.argv:
            report['live_team_page']=evaluate('''
local ui=package.loaded.ms.d_secretAreaUI;local s=ui.g_self
local ok,parent=pcall(function() return s.main_layer:getParent() end)
if not ok or not parent or not s.teams_info or not s.teams_info.team or s.teams_info.team.cleared_layer==nil then return 'not visible' end
local send=ui.send_msg_union_event
ui.send_msg_union_event=function(op,data) if op~=41 then return send(op,data) end end
local rendered,err=pcall(ui.showTeamPage)
ui.send_msg_union_event=send
if not rendered then error(err) end
return 'refreshed without combat'
''')
        if report.get('passed') and '--repair-live' in sys.argv:
            report['live_page_repaired']=evaluate("local u=package.loaded.ms.d_secretAreaUI;u.showPrizePage(u.g_self.main_layer);assert(u.g_self.prize_btns[3]:isEnabled());return 'repaired'")=='repaired'
    finally:
        try:evaluate("if guild_search_restore then guild_search_restore() end;return 'restored'")
        finally:script.unload();session.detach()
        dest=ROOT/'analysis/evidence/guild/search_client_validation.json'
        dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report.get('passed'):raise SystemExit(1)


if __name__=='__main__':main()
