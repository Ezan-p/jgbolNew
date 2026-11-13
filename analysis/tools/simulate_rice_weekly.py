"""Sample seven daily food openings through 1051, then repeat the runtime draws."""
from collections import Counter
from datetime import datetime, timedelta, timezone
import json
from math import comb
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_rice as rice, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode

FOODS = (1213, 1214, 1215, 1216)
START = int(datetime(2026, 11, 9, 12, tzinfo=timezone(timedelta(hours=8))).timestamp())


def inventory(role, tid):
    return sum(i['count'] for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] == tid)


def wire_week():
    rows = []
    serial = 900000
    with tempfile.TemporaryDirectory(prefix='rice-weekly-') as directory:
        with patch('network_redirect.game_clock.now', return_value=START) as clock:
            backend = Backend(Path(directory), 18770, lambda *a, **k: None)
            try:
                role = backend.profile()
                role.update(level=60, gold_coin=100000, silver_coin=100000)
                activity.prepare(role, START, backend.activity_rules)
                backend.save(role)
                state = {'authenticated': True}
                for day in range(7):
                    clock.return_value = START + day*86400
                    before_day = inventory(backend.profile(), 1217)
                    by_type = {}
                    for tid in FOODS:
                        role = backend.profile()
                        summon.add_item(role, tid, 25)
                        backend.save(role)
                        item = next(i for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] == tid)
                        before = inventory(role, 1217)
                        serial += 1
                        request = encode(1051, dict(serial_num=serial, item_type=tid, item_id=item['id'],
                                                   item_count=25, des_type=1, des_id=0))
                        replies = backend.respond(request, state)
                        decoded = [decode(p) for p in replies]
                        events = [(p['id'], login_fields(p['data'])) for mid, _, p in decoded if mid == 2998]
                        assert not any(kind == 55 for kind, data in events), events
                        reward = next(data for kind, data in events if kind == 21)
                        assert reward['result'] == 1 and reward['count'] == 25
                        assert decoded[-1][0] == 1106
                        assert decoded[-1][2]['req_serial_num'] == serial
                        after = backend.profile()
                        assert inventory(after, tid) == 0
                        gained = inventory(after, 1217) - before
                        displayed = sum(p['attach_count'] for p in reward['attach_list'].values()
                                        if p['object_type'] == 5 and p['attach_type'] == 1217)
                        assert gained == displayed
                        by_type[str(tid)] = gained
                    rows.append(dict(day=day+1, opened=100, opened_per_type=25, five_star_by_type=by_type,
                                     five_star_count=inventory(backend.profile(), 1217)-before_day))
                saved = backend.profile()
                total = inventory(saved, 1217)
                backend.close()
                backend = Backend(Path(directory), 18770, lambda *a, **k: None)
                assert inventory(backend.profile(), 1217) == total
            finally:
                backend.close()
    return dict(method='Backend.respond / original 1051 wire protocol / temporary SQLite account',
                clock='seven consecutive days; 2026-11-09 to 2026-11-15 Asia/Shanghai',
                random_source='unmodified runtime secrets.randbelow', real_account_changed=False,
                days=rows, ordinary_opened=700, five_star_total=total, restart_inventory_verified=True)


def main():
    rules = activity.load_rules()
    drop_weight = rules['rice_rules']['normal_five_star_weight']
    p = drop_weight/10000
    print('Running seven daily openings through the game protocol...', flush=True)
    wire = wire_week()
    print('Wire week complete: ' + str(wire['five_star_total']) + ' five-star dumplings.', flush=True)
    pools = [rules['rice_rules']['pools'][str(rice.FOOD_POOLS[t])] for t in FOODS]
    weeks = 10000
    counts = Counter()
    by_type = Counter()
    print('Sampling 10000 weeks using the unmodified game draw function...', flush=True)
    for week in range(weeks):
        found = 0
        for tid, pool in zip(FOODS, pools):
            for _ in range(175):
                if rice.draw(pool) == [5, 1217, 1, 1]:
                    found += 1
                    by_type[tid] += 1
        counts[found] += 1
    distribution = {str(k): comb(700,k)*p**k*(1-p)**(700-k) for k in range(5)}
    distribution['5+'] = max(0.0, 1-sum(distribution.values()))
    report = dict(revision=rules['rice_rules']['revision'], generated_on='2026-11-13 Asia/Shanghai',
                  assumption='100 ordinary dumplings TOTAL per day, 7 days, 700 per week; each type 25 per day',
                  daily_total=100, days_per_week=7, weekly_total=700, drop_probability=p,
                  wire_week=wire,
                  repeated_weeks=dict(method='activity_rice.draw / actual derived pools / secrets.randbelow unchanged',
                                      weeks=weeks, ordinary_opened=weeks*700,
                                      five_star_total=sum(k*v for k,v in counts.items()),
                                      mean_per_week=sum(k*v for k,v in counts.items())/weeks,
                                      five_star_by_normal_type=dict(sorted(by_type.items())),
                                      weekly_count_histogram=dict(sorted(counts.items()))),
                  theory=dict(distribution=f'Binomial(n=700, p={p:g})', expected_per_day=100*p,
                              expected_per_week=700*p, probability_at_least_one=1-(1-p)**700,
                              weekly_count_probabilities=distribution))
    probability_tag = f'{drop_weight/100:g}'.replace('.', 'p') + 'pct'
    destination = ROOT/f'analysis/evidence/rice/weekly_700_{probability_tag}_20261113.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(destination)


if __name__ == '__main__':
    main()
