"""Export every stage/difficulty and sample real NPC player progression.

This is local balance evidence, never a claim about original server tables.
All activity progress and rewards live in disposable roles.
"""
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
from network_redirect import activity, activity_duty as duty, duty_balance as balance, npc_players
from network_redirect.backend import Backend
from network_redirect.protocol import decode


def main():
    out = ROOT/'analysis/evidence/duty'; out.mkdir(parents=True, exist_ok=True)
    rows = []
    for group in range(4, 9):
        for stage in range(1, 121):
            plan = balance.stage(group, stage)
            for difficulty, power in enumerate(plan['targets'], 1):
                rows.append(dict(group=group, stage=stage, difficulty=difficulty, npc_id=plan['npc_id'],
                    name=plan['name'], archetype=plan['archetype'], source_level=plan['level'],
                    source_power=plan['power'], target_power=power,
                    stat_scale=round(power/plan['power'], 6),
                    source_file=npc_players.catalog()[plan['npc_id']]['source_file']))
    with (out/'stage_schedule.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

    now = 1792814400; results = []
    with tempfile.TemporaryDirectory() as tmp:
        backend = Backend(Path(tmp), 18770, lambda *a, **k: None)
        try:
            for level in (12, 18, 24, 30, 60, 99):
                for tier in (1, 3, 5):
                    key = f'npc_v2_l{level:02d}_t{tier}_attack'
                    npc = npc_players.get(key)
                    for difficulty in (1, 2, 3):
                        seed = level*100+tier*10+difficulty
                        rng = random.Random(seed)
                        role = backend.profile(); role.update(copy.deepcopy(npc['role']))
                        activity.prepare(role, now, backend.activity_rules)
                        duty.start(role, backend.activity_rules)
                        duty.update(role, dict(plus_type=1, plus_index=3, flag=0), now, backend.activity_rules)
                        d = role['activity']['duty']; grades = {}; max_actions = 0; drops = []; exchanges = 0
                        with patch('secrets.randbelow', side_effect=rng.randrange):
                            for stage in range(1, 121):
                                packets = duty.battle(role, dict(des_value=stage, des_type=difficulty, des_id=0), now,
                                                      backend.activity_rules, backend.journey_rules)
                                fight = next(data for mid, _, data in map(decode, packets) if mid == 1027)
                                grade = fight['final_result']; grades[grade] = grades.get(grade, 0)+1
                                max_actions = max(max_actions, fight['fight_round'])
                                if not 1 <= grade <= 3:
                                    break
                                if d['phase'] == 'prize':
                                    drops.extend(p for p in duty.pending(d) if p[0] != 12)
                                    duty.update(role, dict(plus_type=3, plus_index=1, flag=0), now, backend.activity_rules)
                                if d['phase'] == 'exchange':
                                    # Prefer attack, then defence, then the cheapest affordable option.
                                    options = [(i, o) for i, o in enumerate(d['offers'], 1) if o['star'] <= d['stars']-d['used']]
                                    idx, _ = min(options, key=lambda x: ((176,177,174,175).index(x[1]['field']), x[1]['star']))
                                    duty.update(role, dict(plus_type=2, plus_index=idx, flag=0), now, backend.activity_rules)
                                    exchanges += 1
                        row = dict(npc_id=key, group=d['group'], power=npc['role']['role_combat_power'], difficulty=difficulty,
                            cleared=d['round']-1, final_grade=grade, grades=grades, max_actions=max_actions,
                            stars=d['stars'], used=d['used'], bonus=d['bonus'], exchanges=exchanges,
                            drops=drops, seed=seed, reached_test_limit=d['round'] == 121)
                        results.append(row)
                        print(key, difficulty, 'cleared', row['cleared'], 'grade', grade, flush=True)
        finally:
            backend.close()
    (out/'balance_playthrough.json').write_text(json.dumps(dict(date='2026-10-26', mode='real_engine_npc_samples',
        revision=balance.rules()['revision'], stage_schedule_rows=len(rows), max_stage_tested=120,
        notes='Fixed attack archetype samples; tactical matchups are not guaranteed monotone by power. No production saves modified.',
        runs=results), ensure_ascii=False, indent=2)+'\n')
    print('Verified', len(results), 'real NPC progression runs and exported', len(rows), 'stage/difficulty rows')


if __name__ == '__main__':
    main()
