"""Replay treasure search in native Cocos without spending live account resources.

Run while the secret-area treasure page is open; reloads the latest adapter.
--repair-live also redraws that page from its settled cache, without another draw.
"""
import copy
import json
from pathlib import Path
import sys
import tempfile
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
            initial=req(43,flag=1)
            role=b.profile();role['guild']['instances']['search_order']=list(range(1,19));b.save(role)
            initial=req(43,flag=1)
            sweep=req(43,flag=6)
            legacy=copy.deepcopy(initial)
            for i in range(19,26):legacy['prize_items'][i]=copy.deepcopy(initial['prize_items'][i-18])
            legacy['search_order']=dict(enumerate([15,9,7,3,20,11,17,22,1,6,13,19,8,23,21,5,18,14,10,12,25,24,4,16,2],1))
            legacy['board_size']=25
            return dict(initial=initial,sweep=sweep,legacy=legacy)
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
