"""Native Cocos validation of complete event transport and actual spirit-task playback."""
import copy
import json
from pathlib import Path
import sys
import subprocess
import time
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis/tools')]
from network_redirect import combat_engine,journey,summon,battle_replay
from network_redirect.protocol import encode,decode
from network_redirect.backend import login_fields
from verify_guild_client import LUA_EVALUATOR
from android_emulator.config import load_config
from observability.collector import processes


def fixture():
    samples=json.loads((ROOT/'.runtime/combat-audit-fixtures.json').read_text())
    actual=samples['3:0:after']
    # JSON numeric-keyed events must be arrays again, as with persisted history.
    actual['fight_events']={int(k) if str(k).isdigit() else k:v for k,v in actual['fight_events'].items()}
    audit=json.loads((ROOT/'analysis/evidence/combat/current_termination_audit.json').read_text())
    actual_hp=next(row['after']['final_hp'] for row in audit['checks'] if row['task']==3 and row['seed']==0)
    def unit(**overrides):
        return dict(dict(type=1001,order=1,level=1,evolve=0,reborn=0,hp=1000,max_hp=1000,gongji=100,fangyu=0,magic=0,skills=[]),**overrides)
    with patch('secrets.randbelow',return_value=0):
        result,lineup,actions=combat_engine.Battle({},([unit(gongji=0)],[unit(gongji=0)]),journey.load_rules()).run()
    assert result==0 and actions.rounds==30 and all(sum(v.values())>0 for v in actions.final_hp.values())
    draw=dict(line_up_msg=decode(encode(1028,dict(fight_id=99001,first_hand=1,des_name='平局结果验收',lineup_count=len(lineup),lineup=lineup)))[2],
        fight_result_msg=decode(encode(1027,dict(fight_id=99001,fight_type=28,final_result=result,fight_round=len(actions),fight_result=actions)))[2],
        fight_events=combat_engine.event_data(actions,99001))
    draw_hp=actions.final_hp
    def mechanism_replay(fid,units,max_actions=None,slots=8):
        rules=journey.load_rules();rules['battle']['mechanics']['rulai_shield_probability']=100
        with patch('secrets.randbelow',return_value=0):
            result,lineup,steps=combat_engine.Battle({},units,rules,max_actions=max_actions,slots=slots).run()
        replay=dict(line_up_msg=decode(encode(1141 if slots==9 else 1028,dict(fight_id=fid,first_hand=1,des_name='机制回放验收',lineup_count=len(lineup),lineup=lineup)))[2],
            fight_result_msg=battle_replay.result_message(dict(fight_id=fid,fight_type=31 if slots==9 else 28,final_result=result,fight_result=steps)),
            fight_events=combat_engine.event_data(steps,fid))
        return replay,steps.final_hp
    healing,healing_hp=mechanism_replay(99003,([unit(gongji=180,essences={5:(50,),16:(100,10)})],
        [unit(type=1002,essences={10:(100,10),19:(100,30)})]))
    shared,shared_hp=mechanism_replay(99004,([unit(gongji=500,magic=500,skills=[(101,1)],skill_probabilities={101:100})],
        [unit(type=1002,hp=2000,max_hp=2000),unit(type=1003,order=2,hp=1000,max_hp=2000,skills=[(21,10)],essences={19:(100,30)})]))
    shared_revive,shared_revive_hp=mechanism_replay(99005,([unit(hp=2000,max_hp=2000,gongji=1500)],
        [unit(type=1002,order=2,hp=3000,max_hp=3000),unit(type=1003,order=3,hp=10,max_hp=2000,skills=[(21,10)],essences={19:(100,30)})]))
    healing_spell,healing_spell_hp=mechanism_replay(99006,([unit(hp=100,magic=100,skills=[(6,1)],skill_probabilities={6:100})],
        [unit(type=1002)]),max_actions=2)
    passives,passives_hp=mechanism_replay(99007,([unit(gongji=600,skills=[(22,1),(42,1),(51,1)],essences={5:(50,),16:(100,10)})],
        [unit(type=1002,skills=[(21,10),(31,1)],essences={10:(100,10)})]))
    long9,long9_hp=mechanism_replay(99008,([unit(order=i,gongji=0) for i in range(1,10)],
        [unit(type=1002,order=i,gongji=0) for i in range(1,10)]),slots=9)
    assert len(long9['fight_result_msg']['fight_result'])==540 and long9['fight_result_msg']['final_result']==0
    with patch('secrets.randbelow',return_value=0):
        talent_result,talent_lineup,talent_steps=journey.battle(dict(level=60,cur_genius_type=502),dict(genius_prob=100),journey.load_rules(),
            units=([unit(gongji=600)],[unit(type=1002)]))
    talent=dict(line_up_msg=decode(encode(1028,dict(fight_id=99009,first_hand=1,des_name='阵雷纹验收',lineup_count=len(talent_lineup),lineup=talent_lineup)))[2],
        fight_result_msg=battle_replay.result_message(dict(fight_id=99009,fight_type=20,final_result=talent_result,fight_result=talent_steps)),
        fight_events=combat_engine.event_data(talent_steps,99009),fight_end_data=dict(talent_steps.talent))
    talent_hp=talent_steps.final_hp
    events={i:dict(cur_action=i%240+1,logic_type=101051,who_use=1,self_use=True,src_order=1,des_order=1,speak='',skill_result_list=[dict(field=65,field_plus=10,des_order=1)]) for i in range(1,401)}
    events['fight_id']=99002
    history=dict(result=1,fight_result_list=[copy.deepcopy(actual) for _ in range(80)])
    def rows(packets):return [dict(mid=mid,data=d) for mid,_,d in map(decode,packets)]
    event_packets=battle_replay.effect_packets(events);response_packets=battle_replay.lua_packets(1301,dict(id=95),history)
    assert len(event_packets)>1 and len(response_packets)>2
    data=dict(actual=actual,draw=draw,healing=healing,shared=shared,shared_revive=shared_revive,healing_spell=healing_spell,passives=passives,long9=long9,talent=talent,long_result_packets=rows(battle_replay.result_packets(1140,long9['fight_result_msg'])),large_events=rows(event_packets),large_response=rows(response_packets),
        large_event_fid=99002,large_event_count=400,history_count=80,actual_actions=len(actual['fight_result_msg']['fight_result']),
        actual_events=len(actual['fight_events'])-1,actual_result=actual['fight_result_msg']['final_result'])
    def client_hp(hp):return {('o' if int(side)==1 else 'e')+str(order):value for side,units in hp.items() for order,value in units.items()}
    data['expected_hp']=dict(actual=client_hp(actual_hp),draw=client_hp(draw_hp),healing=client_hp(healing_hp),shared=client_hp(shared_hp),shared_revive=client_hp(shared_revive_hp),healing_spell=client_hp(healing_spell_hp),passives=client_hp(passives_hp),long9=client_hp(long9_hp),talent=client_hp(talent_hp))
    data['expected_max_hp']={}
    for name in data['expected_hp']:
        data['expected_max_hp'][name]={prefix+str(i):row[side+'_max_hp']
            for i,row in enumerate(data[name]['line_up_msg']['lineup'],1)
            for side,prefix in [('src','o'),('des','e')] if row.get(side+'_type')}
    source=(ROOT/'analysis/tools/battle_pipeline_client_harness.lua').read_text().replace('__FIXTURES__',summon.lua(data))
    source=source.replace('-- __BATTLE_PATCH__',(ROOT/'network_redirect/battle_replay_client.lua').read_text())
    return source,dict(effect_packets=len(event_packets),response_packets=len(response_packets),
        largest_packet=max(map(len,event_packets+response_packets)),actual_actions=data['actual_actions'],actual_events=data['actual_events'],actual_result=data['actual_result'])


def main():
    import frida
    config=load_config(ROOT/'game.json');pid=next(p for p,n in processes(config).items() if n==config['package'])
    evaluator=LUA_EVALUATOR.replace('pending={code,resolve};',"const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    session=frida.get_device(config['serial'],timeout=10).attach(pid);script=session.create_script(evaluator);script.load()
    report={};started=False
    def evaluate(code):
        answer=script.exports_sync.evaluate(code)
        if answer.get('status')!=0:raise RuntimeError(answer)
        return answer['result']
    try:
        assert evaluate('local ms=package.loaded.ms;return tostring(ms.d_mainUI.g_playerInfo.role_id~=nil)')=='true'
        source,report=fixture();(ROOT/'.runtime/battle-pipeline-fixture.lua').write_text(source)
        started=True;evaluate(source)
        report['transport']=login_fields(evaluate('return battlePipelineTransport()'));print('transport',report['transport'],flush=True)
        report['battles']={}
        for name in (sys.argv[1:] or ['draw','actual','healing','shared','shared_revive','healing_spell','passives','long9','talent']):
            evaluate("return battlePipelineStart('"+name+"')")
            deadline=time.monotonic()+(900 if name=='long9' else 300)
            progress_at=time.monotonic()+30
            while True:
                state=login_fields(evaluate('return battlePipelinePoll()'))
                if state['errors']:raise RuntimeError(state['errors'])
                if time.monotonic()>=progress_at:
                    print(name, 'step', state['step'], '/', state['render_steps'], flush=True);progress_at=time.monotonic()+30
                if state['ended'] and (state['button_ready'] or name in ('long9','talent')):break
                if time.monotonic()>deadline:raise RuntimeError(f'{name}: playback timeout; {state}')
                time.sleep(.3)
            report['battles'][name]=login_fields(evaluate("return battlePipelineCheck('"+name+"')"))
            print(name,report['battles'][name],flush=True)
            if name in ('draw','actual'):
                time.sleep(1)
                shot=subprocess.run([str(ROOT/'.runtime/sdk/platform-tools/adb'),'-s',config['serial'],'exec-out','screencap','-p'],capture_output=True,timeout=30,check=True)
                (ROOT/f'.runtime/battle-{name}.png').write_bytes(shot.stdout)
        report['passed']=True
    except Exception as e:report.update(passed=False,error=str(e))
    finally:
        try:report['restored']=not started or evaluate('return battlePipelineRestore()')=='restored'
        except Exception as e:report.update(restored=False,restore_error=str(e))
        for close in (script.unload,session.detach):
            try:close()
            except Exception:pass
    report.update(native_cocos=True,live_account_resources_changed=False)
    report['passed']=bool(report.get('passed') and report['restored'])
    destination=ROOT/'analysis/evidence/combat/current_client_pipeline.json';destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
    if not report['passed']:raise SystemExit(1)


if __name__=='__main__':main()
