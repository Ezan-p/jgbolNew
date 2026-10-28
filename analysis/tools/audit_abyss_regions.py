"""Reproducible nine-region audit; no live saves or gameplay rules are changed."""
import copy
import csv
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_abyss as abyss, activity_abyss_combat as essence
from network_redirect import activity_drug as drug, combat, journey, npc_players, summon, formation, abyss_balance
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

OUT = ROOT / 'analysis/evidence/abyss'
STATS = ('gongji', 'fangyu', 'hp', 'magic')
NOW = 1793160000  # 2026-10-28 12:00 UTC+8


def main():
    rules = json.loads((ROOT / 'server_config/activity_rules.json').read_text())
    jrules = json.loads((ROOT / 'server_config/journey_rules.json').read_text())
    files = ['network_redirect/activity_abyss.py', 'network_redirect/activity_abyss_combat.py',
             'network_redirect/activity_drug.py', 'network_redirect/combat_engine.py',
             'server_config/activity_rules.json', 'server_config/journey_rules.json', 'server_config/abyss_rules.json',
             'network_redirect/abyss_balance.py',
             'analysis/configs/specter_boss_config.csv', 'analysis/configs/specter_hang_ouput.csv',
             'analysis/configs/elite/specter_cortege_base.csv']
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in files}
    assert set(abyss.BOSSES) == set(abyss.HANG) == set(abyss.DROPS) == set(range(1, 82))
    floors = []
    for floor in range(1, 82):
        row = abyss.BOSSES[floor]
        units = abyss.enemies(dict(boss=floor, reductions=[0]*4))
        low = abyss.enemies(dict(boss=floor, reductions=[10**12]*4))
        assert all(u[k] == 1 for u in low for k in STATS)
        assert all(u[k] > 0 for u in units for k in STATS)
        rewards = [[t, tid, lv, n] for t, tid, n, lv in abyss_balance.victory_rewards(floor)]
        assert all((typ in (11,12) or typ == 5 and tid in formation.ITEMS) and lv > 0 and n > 0
                   for typ, tid, lv, n in rewards)
        groups = abyss.DROPS[floor]
        assert len(groups) == 4 and all(w > 0 for w, _ in groups)
        for _, entries in groups:
            assert entries and all(t == 5 and tid in formation.ITEMS and lv > 0 and n > 0 and w > 0
                                   for t, tid, lv, n, w in entries)
        floors.append(dict(floor=floor, region=abyss.HANG[floor]['title'], units=len(units),
                           **{k: sum(u[k] for u in units) for k in STATS},
                           skills=[u['skills'] for u in units], effects=essence.effects(row, {}),
                           rewards=rewards, crystals=sum(n for t, tid, lv, n in rewards if tid == 1441),
                           drops=[dict(weight=w, items=items) for w, items in groups]))

    recipes = []
    legal = set()
    for idx, row in drug.RECIPES.items():
        minimum = int(row['min_level'])
        stride = 20 if int(row['type']) == 5 else 1
        highest = 3
        assert all(drug.quality_weights(minimum,row)) and drug.quality_weights(36,row)==[0,0,0,100]
        ids = [int(row['attach_type'])+stride*g for g in range(highest+1)]
        legal.update(ids)
        role = dict(drug_level=max(drug.LEVELS), drug_exp=0, attachments=[], summon=dict(next_id=10000))
        for token in row['study_material(attach_type|attach_count|need_silver)'].split('/'):
            tid, n, _ = map(int, token.split('|')); summon.add_item(role, tid, n)
        drug.settle(role, dict(recipes=[idx]), 21, dict(index=idx), rules)
        assert any(i['type_id'] == ids[-1] for i in role['attachments'])
        recipes.append(dict(recipe=idx, name=row['study_name'], min_level=minimum,
                            quality_required_levels=[minimum]*4, mastered_level=minimum+3,
                            reachable_ids=ids, max_grade=highest))

    # Exercise actual requests against an isolated database, including all layer gates.
    wire = []
    with tempfile.TemporaryDirectory() as tmp:
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        rules = b.activity_rules
        jrules = b.journey_rules
        role = b.profile(); role['level'] = 80
        activity.prepare(role, NOW, rules); abyss.state(role, NOW, rules); b.save(role)
        serial = 500000
        def request(op, **data):
            nonlocal serial
            serial += 1
            with patch('network_redirect.backend.time.time', return_value=NOW):
                raw = b.respond(encode(1329, dict(serial_num=serial, id=op, data=summon.lua(data))),
                                dict(authenticated=True))
            return [(d['id'], login_fields(d['data'])) for mid, _, d in map(decode, raw) if mid == 2998]
        for floor in range(1, 82):
            role = b.profile(); role['activity']['abyss']['boss'] = floor; b.save(role)
            result = request(2, des_area=floor)
            assert any(i == 173 and d['specter_data']['cur_layer'] == floor for i, d in result)
            before = b.profile()
            rejected = request(2, des_area=floor+1)
            assert rejected[0][0] == 55 and b.profile() == before
            wire.append(dict(floor=floor, unlocked_accepted=True, next_locked_rejected=True))
        role = b.profile(); state = role['activity']['abyss']; state.update(boss=1, layer=1)
        summon.add_item(role, 1502, 1); summon.add_item(role, 1503, 1); b.save(role)
        first = request(17, index=1, type_id=1502)
        second = request(17, index=1, type_id=1503)
        first_stats = next(d['boss_data']['boss_info'] for i, d in first if i == 173)
        second_stats = next(d['boss_data']['boss_info'] for i, d in request(16) if i == 173)
        no_effect = dict(first_pill=1502, replacement=1503, first_stats=first_stats,
                         replacement_stats=second_stats, accepted=not any(i == 55 for i, d in second),
                         replacement_consumed=not any(i['type_id'] == 1503 for i in b.profile()['attachments']))
        assert first_stats == second_stats and not no_effect['accepted'] and not no_effect['replacement_consumed']
        b.close()

    # Real, unboosted catalog armies. Test each floor independently, not a natural playthrough.
    catalog = npc_players.catalog()
    eligible = sorted((k for k, v in catalog.items() if v['profile']['level'] >= 70),
                      key=lambda k: (catalog[k]['profile']['role_combat_power'], k))
    selected = [eligible[int((len(eligible)-1)*q)] for q in (0, .25, .5, .75, 1)]
    ordinary = {}
    for tid in sorted(legal & abyss.PILLS.keys()):
        idx, value, rate = map(int, abyss.PILLS[tid].split('|'))
        assert rate == 0
        if idx not in ordinary or value > ordinary[idx][1]: ordinary[idx] = (tid, value)
    available_essence = sorted(legal & essence.DRUGS.keys())
    samples = []
    for key in selected:
        role = copy.deepcopy(npc_players.get(key)['role'])
        ours, _ = journey.fighters(role, dict(cortege_list='1001|1'))
        runs = []
        for mode in ('no_medicine', 'level36_medicine'):
            for floor in range(1, 82):
                pills = {}; reductions = [0]*4
                if mode == 'level36_medicine':
                    reductions = [ordinary[i][1] for i in range(1, 5)]
                    pills = {str(i): ordinary[i][0] for i in range(1, 5)}
                    # Fixed heuristic: minimize sum of remaining essence percentage points.
                    pair = min(itertools.product(available_essence, repeat=2),
                               key=lambda p: sum(essence.effects(abyss.BOSSES[floor], dict(zip(('5','6'), p))).values()))
                    current = essence.effects(abyss.BOSSES[floor], pills)
                    for slot, tid in zip(('5', '6'), pair):
                        reduced = essence.effects(abyss.BOSSES[floor], dict(pills, **{slot: tid}))
                        if any(reduced[k] < v for k, v in current.items()):
                            pills[slot] = tid; current = reduced
                rng = random.Random(f'abyss-audit-v1:{key}:{mode}:{floor}')
                with patch.object(combat.secrets, 'randbelow', side_effect=rng.randrange):
                    result, lineup, actions, events = essence.battle(role,
                        (ours, abyss.enemies(dict(boss=floor, reductions=reductions))), jrules,
                        essence.effects(abyss.BOSSES[floor], pills))
                assert 1 <= actions.rounds <= 30
                hp = {str(side): int(sum(values.values())) for side, values in actions.final_hp.items()}
                runs.append(dict(floor=floor, mode=mode, result=result, rounds=actions.rounds,
                                 actions=len(actions), stop=actions.stop_reason, final_hp=hp, pills=pills))
        samples.append(dict(key=key, profile=catalog[key]['profile'], runs=runs))
        print('sample complete:', key, flush=True)

    regions = []
    for start in range(1, 82, 9):
        rows = floors[start-1:start+8]
        regions.append(dict(name=rows[0]['region'], first=start, last=start+8,
                            ranges={k: [min(x[k] for x in rows), max(x[k] for x in rows)] for k in STATS},
                            units=sorted({x['units'] for x in rows}),
                            essence_floors=[x['floor'] for x in rows if x['effects']],
                            crystal_range=[rows[0]['crystals'], rows[-1]['crystals']],
                            sample_results=[dict(key=s['key'], mode=mode,
                                wins=sum(1 <= r['result'] <= 3 for r in s['runs'] if r['mode']==mode and start<=r['floor']<start+9))
                                for s in samples for mode in ('no_medicine','level36_medicine')]))
    report = dict(date='2026-10-28', source_sha256=hashes, floors=floors, regions=regions,
                  recipes=recipes, reachable_craft_items=len(legal), total_drug_variants=len(abyss.PILLS)+len(essence.DRUGS),
                  wire_layer_checks=wire, ordinary_no_effect_reproduction=no_effect,
                  medicine_fixture=dict(ordinary=ordinary, essence_candidates=available_essence,
                      caveat='Preloaded legal level-36 drugs; no player stat boost; no acquisition-time claim; server semantics, not native UI.'),
                  samples=samples, economy=dict(total_boss_crystals=sum(x['crystals'] for x in floors),
                      max_daily_shop_spend=sum(sorted((p['cost']*p['limit'] for p in rules['abyss_shop']),reverse=True)[:6]),
                      max_daily_hang_crystals=86400//rules['abyss_tick_seconds']*rules['abyss_crystal_tick_cap'],
                      region_daily_hang_crystals=[288*x for x in abyss_balance.rules()['region_crystal_caps']]),
                  client_native_verified=False)
    assert hashes == {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}, 'Sources changed during audit'
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'regions_repaired_20261028.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    with (OUT/'regions_floors_repaired_20261028.csv').open('w', newline='', encoding='utf-8-sig') as f:
        columns = ['floor','region','units',*STATS,'crystals','effects']
        writer = csv.DictWriter(f, fieldnames=columns); writer.writeheader()
        writer.writerows({k: json.dumps(r[k],ensure_ascii=False) if k=='effects' else r[k] for k in columns} for r in floors)
    print(json.dumps(dict(floors=len(floors), recipes=len(recipes), battles=sum(len(s['runs']) for s in samples),
                         reachable_craft_items=len(legal), economy=report['economy']), ensure_ascii=False))


if __name__ == '__main__': main()
