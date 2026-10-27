"""Native Cocos spirit-land buttons/settlement/animations with disposable storage."""
import json
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from network_redirect import summon, guild, journey
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
            fighters=journey.fighters
            def army(strong):
                def build(*args,**kwargs):
                    armies=fighters(*args,**kwargs)
                    if args[0]['role_id']==role['role_id']:
                        strength=10000000 if strong else 1
                        for unit in armies[0]:unit.update(hp=strength,max_hp=strength,gongji=strength,fangyu=strength,magic=strength)
                    return armies
                return build
            with patch('network_redirect.journey.fighters',side_effect=army(False)):
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
            with patch('network_redirect.journey.fighters',side_effect=army(False)):
                req('trial_fight',80)
            req('trial_after',79)
            with patch('network_redirect.journey.fighters',side_effect=army(True)):
                req('challenge_win',84,task_index=1,task_type=2,pay_type=1)
                req('trial_win',80)
            req('trial_reward_ready',79);req('trial_claim',82);req('trial_next',80)
            for name,won in [('challenge',False),('challenge_win',True),('trial_fight',False),('trial_win',True)]:
                replay=next(login_fields(row['data']['data'])['fight_result_list'][1] for row in data[name]
                            if row['mid']==1301 and row['data']['id'] in (80,85))
                assert (1<=replay['fight_result_msg']['final_result']<=3)==won,name
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
    evaluator=LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame; enter the game before testing'});}},15000);")
    session=frida.get_device(config['serial'],timeout=10).attach(pid);script=session.create_script(evaluator);script.load()
    report={};failure=None;started=False
    def evaluate(code):
        answer=script.exports_sync.evaluate(code)
        if answer.get('status')!=0:raise RuntimeError(answer)
        return answer['result']
    try:
        deadline=time.monotonic()+45
        while evaluate('local ms=package.loaded.ms;return tostring(ms and ms.d_mainUI and ms.d_mainUI.g_playerInfo and ms.d_mainUI.g_playerInfo.role_id~=nil or false)')!='true':
            if time.monotonic()>deadline:raise RuntimeError('Enter the game before running the fixture')
            time.sleep(.5)
        source=fixtures();(ROOT/'.runtime/guild-pet-fixture.lua').write_text(source)
        started=True
        evaluate(source)
        count=int(evaluate('return tostring(#guildPetCases)'))
        for index in range(1,count+1):
            row=login_fields(evaluate('return table.tostring(guildPetRun('+str(index)+'))'))
            print(row['name'],row['ok'],row.get('error',''),flush=True)
            if not row['ok']:break
            deadline=time.monotonic()+row.get('hold',0)
            while time.monotonic()<deadline:time.sleep(.2)
            if row['name'].endswith('_battle_animation'):
                deadline=time.monotonic()+120
                while evaluate('return tostring(guildPetBattleReady())')!='true':
                    if time.monotonic()>deadline:raise RuntimeError('native battle did not finish within 120 seconds')
                    time.sleep(.5)
        report=login_fields(evaluate('return table.tostring({checks=guildPetResults,errors=guildPetErrors,expected=#guildPetCases})'))
    except Exception as e:failure=str(e)
    finally:
        try:report['restored']=not started or evaluate("if guildPetRestore then guildPetRestore() end;return 'restored'")=='restored'
        except Exception as e:
            report['restored']=False;failure=failure or str(e)
        finally:
            for close in (script.unload,session.detach):
                try:close()
                except Exception:pass
    checks=list(report.get('checks',{}).values());errors=report.get('errors',{})
    report.update(passed=bool(not failure and report.get('restored') and len(checks)==report.get('expected') and all(c['ok'] for c in checks) and not errors),native_cocos=True,live_account_resources_changed=False)
    if failure:report['failure']=failure
    path=ROOT/'analysis/evidence/guild/pet_fixes_client_validation.json';path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
