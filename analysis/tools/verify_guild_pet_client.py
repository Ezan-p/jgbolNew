"""Native Cocos spirit-land buttons/settlement/animations with disposable storage."""
import json
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from network_redirect import summon, guild
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from verify_guild_client import LUA_EVALUATOR
from android_emulator.config import load_config
from observability.collector import processes


def fixtures():
    data={};serial=100
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time',return_value=1792728000):
        b=Backend(Path(tmp),18790,lambda *a,**k:None)
        try:
            role=b.profile();role.update(level=50,gold_coin=100000,silver_coin=100000);summon.add_item(role,1341,2);b.save(role)
            def req(name,op,**args):
                nonlocal serial
                serial+=1
                rows=[decode(p) for p in b.respond(encode(1301,dict(serial_num=serial,id=op,data=summon.lua(args))),{'authenticated':True})]
                assert not any(mid==2998 and d['id']==55 for mid,_,d in rows),rows
                data[name]=[dict(mid=mid,data=d) for mid,_,d in rows if mid==1301 or mid==2998 and d['id']==121]
            req('create',1,union_name='灵宠修复验收')
            role=b.profile();role['guild']['unions']['2']['popularity']=4000;b.save(role)
            req('accept',5,role_list=list(map(int,role['guild']['unions']['2']['applications'])))
            req('info',18,query_type=1);req('tasks',83)
            req('challenge',84,task_index=1,task_type=2,pay_type=1)
            # The capture cases need an earned encounter independently of battle outcome.
            req('puzzle',84,task_index=2,task_type=1,pay_type=1)
            req('field',86,two_type=1);req('explore',86,two_type=2)
            req('capture',87,two_type=2,catch_type=1341);req('leave',87,two_type=1)
            req('more_tasks',84,task_index=3,task_type=1,pay_type=1)
            req('explore_again',86,two_type=2)
            role=b.profile();summon.add_item(role,1338,5);b.save(role)
            with patch('network_redirect.guild_offline.roll',side_effect=lambda s,n:n-1):
                for i in range(1,4):req('failure'+str(i),87,two_type=2,catch_type=1338)
            req('home',88);req('trial',79)
            req('trial_fight',80);req('trial_after',79)
            role=b.profile()
            data['role']={k:role[k] for k in ('role_id','union_id','union_rank','level','gold_coin','silver_coin')}
            data['config']=guild.client_config(b.guild_rules)
        finally:b.close()
    source=(ROOT/'analysis/tools/guild_pet_client_harness.lua').read_text()
    source=source.replace('__FIXTURES__',summon.lua(data)).replace('-- __PET_PATCH__',(ROOT/'network_redirect/guild_pet_client.lua').read_text())
    return source


def main():
    import frida
    config=load_config(ROOT/'game.json');pid=next(p for p,n in processes(config).items() if n==config['package'])
    session=frida.get_device(config['serial'],timeout=10).attach(pid);script=session.create_script(LUA_EVALUATOR);script.load()
    report={};failure=None
    def evaluate(code):
        answer=script.exports_sync.evaluate(code)
        if answer.get('status')!=0:raise RuntimeError(answer)
        return answer['result']
    try:
        source=fixtures();(ROOT/'.runtime/guild-pet-fixture.lua').write_text(source)
        evaluate(source)
        count=int(evaluate('return tostring(#guildPetCases)'))
        for index in range(1,count+1):
            row=login_fields(evaluate('return table.tostring(guildPetRun('+str(index)+'))'))
            print(row['name'],row['ok'],row.get('error',''),flush=True)
            if not row['ok']:break
            deadline=time.monotonic()+row.get('hold',0)
            while time.monotonic()<deadline:time.sleep(.2)
            if row['name']=='real_task_battle_animation':
                deadline=time.monotonic()+120
                while evaluate('return tostring(guildPetBattleReady())')!='true':
                    if time.monotonic()>deadline:raise RuntimeError('native battle did not finish within 120 seconds')
                    time.sleep(.5)
        report=login_fields(evaluate('return table.tostring({checks=guildPetResults,errors=guildPetErrors,expected=#guildPetCases})'))
    except Exception as e:failure=str(e)
    finally:
        try:report['restored']=evaluate("if guildPetRestore then guildPetRestore() end;return 'restored'")=='restored'
        finally:script.unload();session.detach()
    checks=list(report.get('checks',{}).values());errors=report.get('errors',{})
    report.update(passed=bool(not failure and report.get('restored') and len(checks)==report.get('expected') and all(c['ok'] for c in checks) and not errors),native_cocos=True,live_account_resources_changed=False)
    if failure:report['failure']=failure
    path=ROOT/'analysis/evidence/guild/pet_fixes_client_validation.json';path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
