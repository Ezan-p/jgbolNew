"""Verify actual guild island/war buttons in Cocos, with disposable responses."""
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import guild, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from android_emulator.config import load_config
from observability.collector import processes
from verify_guild_client import LUA_EVALUATOR


def fixture():
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time', return_value=1792728000):
        b=Backend(Path(tmp),18790,lambda *a,**k:None)
        try:
            role=b.profile();role.update(level=50,gold_coin=10000);b.save(role)
            serial=100
            def request(op,**data):
                nonlocal serial
                serial+=1
                rows=[decode(p) for p in b.respond(encode(1301,dict(serial_num=serial,id=op,data=summon.lua(data))),{'authenticated':True})]
                assert not any(m==2998 and d['id']==55 for m,_,d in rows),rows
                return next(login_fields(d['data']) for m,_,d in rows if m==1301)
            request(1,union_name='入口验证仙盟')
            role=b.profile();role['guild']['unions']['2']['popularity']=4000;b.save(role)
            info=request(18,query_type=1);tasks=request(83);home=request(88)
            role=b.profile();config=guild.client_config(b.guild_rules)
        finally:b.close()
    source=(ROOT/'analysis/tools/guild_access_client_harness.lua').read_text()
    for marker,value in (('__ROLE__',{k:role[k] for k in ('level','union_id','union_rank','role_id','union_name')}),('__CONFIG__',config),('__INFO__',info),('__TASKS__',tasks),('__HOME__',home)):
        source=source.replace(marker,summon.lua(value))
    access=(ROOT/'network_redirect/guild_access_client.lua').read_text().replace('__GUILD_WARS_ENABLED__','false')
    return source.replace('-- __ACCESS_PATCH__',access)


def main():
    import frida
    config=load_config(ROOT/'game.json')
    pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=10).attach(pid)
    script=session.create_script(LUA_EVALUATOR);script.load()
    report={}
    try:
        source=fixture()
        (ROOT/'.runtime/guild-access-fixture.lua').write_text(source)
        answer=script.exports_sync.evaluate('local ok,result=xpcall(function()\n'+source+'\nend,debug.traceback);if not ok then error(result) end;return result')
        if answer.get('status')!=0:raise RuntimeError(answer)
        report=login_fields(answer['result'])
    finally:
        restored=script.exports_sync.evaluate("if guildAccessTestRestore then guildAccessTestRestore() end;return 'restored'")
        if restored.get('status')!=0:print('RESTORE FAILED:',restored)
        script.unload();session.detach()
    report.update(native_cocos=True,live_account_resources_changed=False)
    (ROOT/'analysis/evidence/guild/access_client_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report.get('passed'):raise SystemExit(1)


if __name__=='__main__':main()
