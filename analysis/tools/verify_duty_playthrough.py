"""Real combat, 3 x 105 stages; disposable strong test role, unchanged enemies."""
import json
import random
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_duty as duty
from network_redirect.backend import Backend
from network_redirect.protocol import decode


def main():
    now = 1792814400; rng = random.Random(20261026); runs = []
    with tempfile.TemporaryDirectory() as tmp, patch('secrets.randbelow', side_effect=rng.randrange):
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        try:
            for difficulty in (1, 2, 3):
                role = b.profile(); role['level'] = 60
                activity.prepare(role, now, b.activity_rules)
                # Explicit test fixture. The production enemy/strength config is
                # never changed and all wins are decided by the real engine.
                for c in role['corteges']:
                    if c.get('order'):
                        c.update(hp=1000000, magic=1000000, gongji=1000000, fangyu=1000000)
                duty.start(role, b.activity_rules)
                duty.update(role, dict(plus_type=1, plus_index=3, flag=0), now, b.activity_rules)
                rows = []; initial_silver = role['silver_coin']
                for stage in range(1, 106):
                    info = duty.data(role, b.activity_rules)
                    assert info['cur_round']+1 == stage
                    packets = duty.battle(role, dict(fight_type=5, des_value=stage, des_type=difficulty, des_id=0), now, b.activity_rules, b.journey_rules)
                    fight = next(data for mid, _, data in map(decode, packets) if mid == 1027)
                    assert 1 <= fight['final_result'] <= 3, (difficulty, stage, fight['final_result'])
                    assert fight['fight_round'] > 0
                    assert decode(packets[-1])[2]['id'] == 44
                    rows.append(dict(stage=stage, result=fight['final_result'], actions=fight['fight_round'], max_packet=max(map(len, packets))))
                    d = role['activity']['duty']
                    if d['phase'] == 'prize':
                        assert duty.data(role, b.activity_rules)['result'] == 6
                        duty.update(role, dict(plus_type=3, plus_index=1, flag=0), now, b.activity_rules)
                        duty.update(role, dict(plus_type=2, plus_index=3, flag=0), now, b.activity_rules)
                assert role['silver_coin']-initial_silver == 35*3000
                runs.append(dict(difficulty=difficulty, stages=rows, stars=d['stars'], used=d['used'], silver=role['silver_coin']-initial_silver))
        finally:
            b.close()
    out = ROOT/'analysis/evidence/duty'
    out.mkdir(parents=True, exist_ok=True)
    (out/'playthrough.json').write_text(json.dumps(dict(date='2026-10-26', mode='real_engine_disposable_strong_role',
        unchanged_enemy_and_drop_config=True, balance_validation=False, runs=runs), ensure_ascii=False, indent=2)+'\n')
    print('Verified 315 real battles, 105 claims and exchanges, 3 difficulties; this is flow validation, not balance validation')


if __name__ == '__main__':
    main()
