"""All daily bosses against real formations; no live account reads or writes."""
import copy
import csv
import json
import random
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_trial as trial, npc_players
from network_redirect.backend import Backend
from network_redirect.protocol import decode

NOW = 1793073600  # 2026-10-27 12:00 UTC+8


def main():
    out = ROOT / 'analysis/evidence/trial'
    out.mkdir(parents=True, exist_ok=True)
    rules = trial.load_rules()
    rows, bosses = [], []
    with tempfile.TemporaryDirectory() as tmp:
        backend = Backend(Path(tmp), 18770, lambda *a, **k: None)
        try:
            starter = backend.profile()
            templates = [('starter', starter)]
            for level in (10, 30, 60, 99):
                key = f'npc_v2_l{level:02d}_t1_attack'
                role = copy.deepcopy(starter)
                role.update(copy.deepcopy(npc_players.get(key)['role']))
                templates.append((key, role))
            for label, template in templates:
                for tid in trial.POOL:
                    role = copy.deepcopy(template)
                    role.pop('activity', None)
                    activity.prepare(role, NOW, backend.activity_rules)
                    role['activity']['trial_meta']['type_id'] = tid
                    trial.query(role, dict(flag=2, id=0), NOW, backend.activity_rules)
                    boss = role['activity']['trial']
                    unit = boss['unit']
                    bosses.append(dict(sample=label, type_id=tid, name=trial.NAMES[tid], level=unit['level'],
                        hp=unit['hp'], attack=unit['gongji'], defense=unit['fangyu'], magic=unit['magic'],
                        skill=unit['skills'][0][0] if unit['skills'] else 0))
                    rng = random.Random(tid * 100 + role['level'])
                    initial_hp = boss['hp']
                    with patch('secrets.randbelow', side_effect=rng.randrange):
                        for attempt in range(rules['daily_attempts']):
                            packets = trial.battle(role, dict(des_type=8, des_id=tid, des_value=0),
                                NOW + attempt * rules['cooldown_seconds'], backend.activity_rules, backend.journey_rules)
                            decoded = list(map(decode, packets))
                            replay = next(d for m, _, d in decoded if m == 1027)
                            assert 0 <= boss['hp'] <= initial_hp
                            assert replay['fight_round'] == len(replay['fight_result'])
                            if boss['is_dead']:
                                trial.query(role, dict(flag=9, id=0),
                                    NOW + attempt * rules['cooldown_seconds'], backend.activity_rules)
                                assert role['activity']['trial'] is None
                                break
                    rows.append(dict(sample=label, boss=tid, name=trial.NAMES[tid], killed=boss['is_dead'],
                        attempts=attempt + 1, initial_hp=initial_hp, remaining_hp=boss['hp'],
                        damage=boss['damage'], last_result=replay['final_result']))
                subset = [x for x in rows if x['sample'] == label]
                print(label, sum(x['killed'] for x in subset), '/', len(subset), 'bosses killed', flush=True)
        finally:
            backend.close()
    with (out / 'boss_stats.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(bosses[0]))
        writer.writeheader()
        writer.writerows(bosses)
    assert all(row['killed'] for row in rows), 'A sample cannot complete within the daily attempt limit'
    report = dict(passed=True, revision=rules['revision'], real_combat=True, disposable_save=True,
        boss_count=len(trial.POOL), runs=rows, original_sources=[
            'analysis/evidence/lua_named/lua/ui/shilianUI.lua.txt:137-168,328-435,1344-1550',
            'analysis/evidence/activity_enums.json:train_boss_type,train_boss_result',
            'analysis/configs/newbie_content3.csv:16',
            'analysis/configs/cortege/cortege_base_0.csv',
            'analysis/configs/item_base.csv:1041,1042'],
        limits='Fixed-seed progression samples, not a guarantee for every player formation or original server balance.',
        inferred=rules['provenance']['inferred'])
    (out / 'playthrough.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(rows)} real battle/claim runs passed')


if __name__ == '__main__':
    main()
