"""Audit every reached level against the user-requested bun, gold and gold-card schedule."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import formation, progression
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode

EXPECTED = {20: 1, 30: 1, 40: 1, 50: 1, 60: 1, 70: 2, 80: 2, 90: 2, 99: 3}


def counts(role):
    return {tid: sum(x['count'] for x in role['attachments'] if x['attach_type'] == 5 and x['type_id'] == tid)
            for tid in (1020, 1152, 1156)}


def main():
    rules = progression.load_rules()
    rows = [dict(level=1, buns=0, gold=0, total_buns=0, total_gold=0, large_cards=0, small_cards=0, total_large_cards=0, passed=True)]
    with tempfile.TemporaryDirectory() as tmp:
        backend = Backend(Path(tmp), 18770, lambda *a, **kw: None)
        try:
            role = backend.profile(); initial_gold = role['gold_coin']
            for level in range(2, 100):
                before = copy.deepcopy(role); initial = counts(role)
                progression.add_exp(role, int(formation.LEVELS[level-1]['upgrade_exp']), r=rules)
                after = counts(role)
                gifts = login_fields(decode(progression.upgrade_events(before, role)[0])[2]['data'])['gift_lists_by_level'][level]
                shown = {tid: sum(x['attach_count'] for x in gifts.values() if x['object_type'] == 5 and x['attach_type'] == tid)
                         for tid in initial}
                delta = {tid: after[tid] - initial[tid] for tid in initial}
                expected = {1020: 1 + level // 10, 1152: EXPECTED.get(level, 0), 1156: 0}
                gold = role['gold_coin'] - before['gold_coin']
                expected_gold = 100 if level % 10 == 0 else 50 if level % 5 == 0 else 20
                shown_gold = sum(x['attach_count'] for x in gifts.values() if x['object_type'] == 11)
                passed = gold == shown_gold == expected_gold and role['level'] == level and role['cur_exp'] == 0 and delta == shown == expected
                rows.append(dict(level=level, buns=delta[1020], gold=gold, total_buns=after[1020], total_gold=role['gold_coin']-initial_gold, large_cards=delta[1152], small_cards=delta[1156],
                                 total_large_cards=after[1152], popup_counts=shown, passed=passed))
            final = counts(role); final_gold = role['gold_coin']
            progression.add_exp(role, 10**12, r=rules)
            capped = role['gold_coin'] == final_gold and counts(role) == final and role['level'] == 99
        finally:
            backend.close()
    report = dict(revision=rules['revision'], passed=all(row['passed'] for row in rows) and capped,
                  levels=rows, totals=final, total_gold=final_gold-initial_gold, full_level_does_not_reward_again=capped,
                  rules_sha256=hashlib.sha256((ROOT/'server_config/progression_rules.json').read_bytes()).hexdigest(),
                  live_account_resources_changed=False)
    path = ROOT/'analysis/evidence/progression_level_rewards_validation.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(f"{sum(row['passed'] for row in rows)}/99 levels passed; totals: {final}; full-level guard: {capped}")
    if not report['passed']: raise SystemExit(1)


if __name__ == '__main__':
    main()
