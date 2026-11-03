"""Native encounters: real combat, reward confirmation and resumed ten-roll movement."""
import json
import sys
import time
from verify_guild_client import LUA_EVALUATOR
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from android_emulator.config import load_config
from observability.collector import processes
from build_nine_sky_client_fixture import main as build


def main():
    import frida
    build()
    fixture=(ROOT/'.runtime/nine-sky-native-fixture.lua').read_text().split('local ms=assert(package.loaded.ms)',1)[0]
    from network_redirect import nine_sky_battle as battle, activity_nine_sky as sky, summon
    from network_redirect.npc_players import get
    key=min(battle.catalog(),key=lambda k:battle.catalog()[k]['profile']['role_combat_power'])
    encounters=[]
    for stat in (1000000,1):
        role=get(key)['role'];role['attachments']=[];role['activity']={};role['spirit_array']={}
        for unit in role['corteges']:
            for name in battle.formation.STATS:unit[name]=stat
        record,reward=battle.encounter(role,dict(floor=1),sky.load_rules())
        record['rewards']=[dict(object_type=1,attach_type=-1,attach_count=1,attach_level=100)] if record['won'] else []
        encounters.append(record)
    assert encounters[0]['won'] and not encounters[1]['won']
    fixture+='\nFIXTURE.ten.local_battles='+summon.lua(encounters)+'\n'
    fixture+='for i=1,2 do FIXTURE.ten.map_event_list[i].local_battle_index=i end\n'
    source=fixture+(ROOT/'analysis/tools/nine_sky_encounter_harness.lua').read_text().replace('-- INSTALL_PATCH',(ROOT/'network_redirect/nine_sky_client.lua').read_text())
    config=load_config(ROOT/'game.json');device=frida.get_device(config['serial'],timeout=10)
    pid=next(p for p,n in processes(config).items() if n==config['package']);session=device.attach(pid)
    script=session.create_script(LUA_EVALUATOR);messages=[]
    def evaluate(code):
        result=script.exports_sync.evaluate(code)
        if result.get('status')!=0:raise RuntimeError(result)
        return result['result']
    try:
        script.load();evaluate(source)
        deadline=time.monotonic()+180
        while time.monotonic()<deadline:
            time.sleep(.5)
            result=evaluate('return nine_sky_animation_result or "WAIT"')
            if result.startswith(('PASS:', 'FAIL:')):
                messages.append(dict(payload=dict(status=0,result=result)));break
    except Exception as error:
        messages.append(dict(error=str(error)))
    finally:
        try:evaluate("if nine_sky_animation_restore then nine_sky_animation_restore() end;return 'restored'")
        finally:script.unload();session.detach()
    passed=any(m.get('payload',{}).get('result','').startswith('PASS:') for m in messages)
    report=dict(passed=passed,native_timed_animation=True,native_battles=True,ten_rolls=True,account_resources_changed=False,raw=messages)
    (ROOT/'analysis/evidence/nine_sky/encounter_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
    if not passed:raise SystemExit(1)

if __name__=='__main__':main()
