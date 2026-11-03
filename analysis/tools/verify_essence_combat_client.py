"""Play isolated, real-loadout essence fixtures in the logged-in native client.

The existing battle harness blocks gameplay sends and restores hooks/UI. No
backend profile or APK is changed. --fixtures-only needs no running emulator.
"""
import argparse
import copy
import json
from pathlib import Path
import sys
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis/tools')]
from network_redirect import combat_engine, combat_loadout, battle_replay, journey, summon
from network_redirect.backend import login_fields
from network_redirect.protocol import encode, decode
from tests.test_combat_engine import unit

NATIVE_ART = {1:'weisheshu_001.ccbi', 2:'pojia001.ccbi', 4:'fashufanghu.ccbi',
              5:'xixue001.ccbi', 6:'gedang001.ccbi', 8:'fashufanghu001.ccbi',
              9:'fashuchuantou001.ccbi', 10:'huifu001.ccbi', 12:'zhanyi001.ccbi',
              13:'zhiliao001.ccbi', 16:'zhongdushu_001.ccbi', 18:'zhufu001.ccbi',
              19:'fuhuo001.ccbi'}


def fixtures():
    data = dict(expected_hp={}, expected_max_hp={}, expected_names={}, expected_art={}, team_hp_delta={})
    summary = {}
    groups = {
        'physical': ([1, 2, 5, 7, 11], [3, 6, 10, 12, 14]),
        'parry': ([4, 11], [3, 19]),
        'magic': ([9, 16], [8, 17]),
        'poison': ([5, 16], [10, 14, 19]),
        'entry': ([13, 18], [13, 18]),
        'execute': ([15], [14]),
        'reserve': ([13, 18], []),
        'passive9': ([1, 7, 13], [2, 16, 17]),
    }
    for base in (10100, 10200):
        for group, families in groups.items():
            name = '%s_%s' % (base, group)
            teams = []
            for side, kinds in enumerate(families, 1):
                owner = dict(corteges=[dict(id=7, type=1000+side, order=1,
                                          equiped_ext_skill_limit=4,
                                          fate_rebullding_state=1, spirit_earth_level=50)],
                             attachments=[dict(id=30+i, type_id=base+k, level=5, owner_id=7,
                                               attach_type=5, ext_skill_pos=i, count=1)
                                          for i, k in enumerate(kinds, 1)])
                actor = unit(type=1000+side, companion_id=7, hp=40000, max_hp=50000,
                             gongji=5000, fangyu=300, magic=1000)
                if group == 'magic':
                    actor.update(skills=[(101, 1)], skill_probabilities={101: 100})
                if group == 'execute' and side == 2:
                    actor['hp'] = 6000
                if group == 'reserve' and side == 1:
                    actor['order'] = 5
                if group == 'passive9':
                    actor['order'] = 9
                    actor['skills'] = [(2, 1)]
                combat_loadout.attach_owned_bonuses(owner, [actor])
                teams.append([actor])
                if group == 'reserve' and side == 1:
                    teams[-1].insert(0, unit(hp=1, max_hp=100, gongji=1))
            original = copy.deepcopy(teams)
            with patch('network_redirect.combat.secrets.randbelow', return_value=0):
                battle = combat_engine.Battle({}, teams, journey.load_rules(), slots=9 if group=='passive9' else 8)
                result, lineup, actions = battle.run()
            assert teams == original
            fid = 99600+len(summary)
            data[name] = dict(
                line_up_msg=decode(encode(1141 if group=='passive9' else 1028, dict(fight_id=fid, first_hand=1,
                    des_name='精魄触发验收', lineup_count=len(lineup), lineup=lineup)))[2],
                fight_result_msg=battle_replay.result_message(dict(fight_id=fid, fight_type=31 if group=='passive9' else 28,
                    final_result=result, fight_result=actions)),
                fight_events=combat_engine.event_data(actions, fid))
            data['expected_hp'][name] = {('o' if side == 1 else 'e')+str(order): hp
                for side, rows in actions.final_hp.items() for order, hp in rows.items()}
            data['expected_max_hp'][name] = {prefix+str(u['order']): u['max_hp']
                for prefix, team in zip(('o', 'e'), battle.sides) for u in team}
            data['team_hp_delta'][name] = {prefix: sum(
                row.get('hp_max_add', 0) for event in actions.events if event['who_use']==side
                for row in event['skill_result_list']) for prefix, side in (('o',1),('e',2))}
            packets = combat_engine.event_packets(actions, fid)
            codes = sorted({e['logic_type'] for e in actions.events+actions.essence_visuals
                            if e['logic_type'] % 1000 not in (13, 162, 163)})
            data['expected_names'][name] = sorted({
                'skill/ext/%dn.png' % ((5 if code//1000 == 102 else 4)*100+code//10%100)
                for code in codes})
            data['expected_art'][name] = sorted({NATIVE_ART[e['logic_type']//10%100]
                for e in actions.events+actions.essence_visuals
                if e['logic_type']%10==1 and e['logic_type']//10%100 in NATIVE_ART
                and e.get('visual_detail')!='assault_bonus'})
            summary[name] = dict(essences=[[base+k for k in ks] for ks in families],
                                 level=5, rounds=actions.rounds, actions=len(actions),
                                 events=len(actions.events), result=result,
                                 visual_notices=len(actions.essence_visuals), triggered_codes=codes,
                                 expected_art=data['expected_art'][name],
                                 largest_event_packet=max(map(len, packets)))
    covered = {tid for row in summary.values() for team in row['essences'] for tid in team}
    assert covered == set(range(10101, 10120)) | set(range(10201, 10220))
    triggered = {c//10 for row in summary.values() for c in row['triggered_codes']}
    assert triggered == covered, covered-triggered
    source = (ROOT/'analysis/tools/battle_pipeline_client_harness.lua').read_text()
    source = source.replace('state.g_hp.o_all==initialTotals.o and state.g_hp.e_all==initialTotals.e',
        'state.g_hp.o_all==initialTotals.o+fixtures.team_hp_delta[name].o and state.g_hp.e_all==initialTotals.e+fixtures.team_hp_delta[name].e')
    source = source.rsplit("return 'ready'", 1)[0] + (ROOT/'analysis/tools/essence_visual_client_harness.lua').read_text() + "\nreturn 'ready'"
    source = source.replace('__FIXTURES__', summon.lua(data))
    source = source.replace('-- __BATTLE_PATCH__', (ROOT/'network_redirect/battle_replay_client.lua').read_text())
    return source, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures-only', action='store_true')
    parser.add_argument('--case', action='append')
    parser.add_argument('--report', default='analysis/evidence/combat/essence_visual_native_20261104.json')
    parser.add_argument('--audit-report', action='append', help='Audit saved native reports without connecting a device')
    args = parser.parse_args()
    source, summary = fixtures()
    if args.audit_report:
        verified, names, resources = [], set(), set()
        for path in args.audit_report:
            report = json.loads((ROOT/path).read_text())
            assert report['passed'] and report['restored'] and report['native_cocos'], path
            for name, result in report['battles'].items():
                assert result['hp_matches_server'] and not result['errors'], name
                visuals = result['visuals']
                expected_names = {'skill/ext/%dn.png' % ((5 if code//1000==102 else 4)*100+code//10%100)
                                  for code in summary[name]['triggered_codes']}
                assert all(visuals['visible_names'].get(pic,0)>0 for pic in expected_names), name
                assert all(visuals['animations'].get(art,0)>0 for art in summary[name]['expected_art']), name
                names.update(expected_names);resources.update(summary[name]['expected_art']);verified.append(name)
        print(json.dumps(dict(passed=True, native_cocos=True, reports=args.audit_report,
            battles=verified, visible_essence_names=sorted(names), native_essence_animations=sorted(resources)),
            ensure_ascii=False, indent=2))
        return
    if args.fixtures_only:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    names = args.case or list(summary)
    if set(names)-summary.keys():
        parser.error('unknown fixture')
    import frida
    from verify_guild_client import LUA_EVALUATOR
    from android_emulator.config import load_config
    from observability.collector import processes
    config = load_config(ROOT/'game.json')
    pid = next(p for p, n in processes(config).items() if n == config['package'])
    evaluator = LUA_EVALUATOR.replace('pending={code,resolve};',
        "const task={code,resolve};pending=task;setTimeout(()=>{if(pending===task){pending=null;resolve({status:-1,result:'No Lua frame'});}},15000);")
    session = frida.get_device(config['serial'], timeout=10).attach(pid)
    script = session.create_script(evaluator)
    report = dict(fixtures=summary, battles={}, native_cocos=True,
                  gameplay_sends_blocked=True, live_account_resources_changed=False)
    started = False
    def evaluate(code):
        answer = script.exports_sync.evaluate(code)
        if answer.get('status') != 0:
            raise RuntimeError(answer)
        return answer['result']
    try:
        script.load()
        assert evaluate('local ms=package.loaded.ms;return tostring(ms.d_mainUI.g_playerInfo.role_id~=nil)') == 'true'
        evaluate("assert(not battlePipelineRestore and not guildPetRestore and not guild_fixture_restore,'another fixture is active');return 'ready'")
        started = True
        evaluate(source)
        for name in names:
            evaluate("return battlePipelineStart('%s')" % name)
            deadline, progress = time.monotonic()+300, time.monotonic()+20
            while True:
                state = login_fields(evaluate('return battlePipelinePoll()'))
                if state['errors']:
                    raise RuntimeError(state['errors'])
                if state['ended'] and state['button_ready']:
                    break
                if time.monotonic() > deadline:
                    raise RuntimeError('%s playback timeout: %s' % (name, state))
                if time.monotonic() > progress:
                    print(name, state['step'], '/', state['render_steps'], flush=True)
                    progress = time.monotonic()+20
                time.sleep(.3)
            report['battles'][name] = login_fields(evaluate("return battlePipelineCheck('%s')" % name))
            print(name, 'HP, native names and effects passed', flush=True)
        report['passed'] = True
    except Exception as error:
        report.update(passed=False, error=str(error))
    finally:
        try:
            report['restored'] = not started or evaluate("if battlePipelineRestore then return battlePipelineRestore() end;return 'restored'") == 'restored'
        except Exception as error:
            report.update(restored=False, restore_error=str(error))
        script.unload()
        session.detach()
    report['passed'] = bool(report.get('passed') and report.get('restored'))
    destination = ROOT/args.report
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(passed=report['passed'], restored=report['restored'],
                         battles=len(report['battles']), error=report.get('error')), ensure_ascii=False))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
