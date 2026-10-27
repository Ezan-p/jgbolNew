#!/usr/bin/env python3
"""Audit real item requests using disposable databases, never player saves.

This is a dated diagnostic, not a test asserting that missing features stay
broken. Bag randomness is fixed to isolate routing, debit and achievement
tracking; separate bag tests cover the probability tables.
"""
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import formation, item_rewards, qiankun_bags, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode

NOW = int(datetime(2026, 10, 27, 12, tzinfo=timezone(timedelta(hours=8))).timestamp())
OUTPUT = ROOT / 'analysis/evidence/server_integration/item_branch_probes_2026-10-27.json'


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def snapshot(role, item_type):
    return dict(
        role_sha256=digest(role),
        items=[i for i in role['attachments'] if i['type_id'] == item_type],
        resources={k: role.get(k, 0) for k in ('strength', 'silver_coin', 'gold_coin', 'charge_gold',
                   'vip_level', 'union_id', 'union_contrib', 'cur_union_contrib')},
        achievement_totals={k: role.get('achievements', {}).get('totals', {}).get(k, 0)
                            for k in ('111', '112', '113', '114', '117')},
        companion={k: role['corteges'][0].get(k) for k in ('id', 'type', 'level', 'cur_exp')},
    )


def response_rows(replies):
    result = []
    for packet in replies:
        mid, _, data = decode(packet)
        if mid == 2998:
            data = dict(data, parsed_data=login_fields(data['data']))
        result.append(dict(message_id=mid, data=data))
    return result


def run_case(item_type):
    emitted = []
    with tempfile.TemporaryDirectory(prefix='jgbol-item-audit-') as tmp, \
            patch('network_redirect.backend.time.time', return_value=NOW):
        backend = Backend(Path(tmp), 18770, lambda event, **data: emitted.append(dict(event=event, **data)))
        try:
            role = backend.profile()
            role.update(level=80, gold_coin=100000, strength=0, vip_level=1)
            role['corteges'][0].update(level=1, cur_exp=0)
            backend.save(role)
            prerequisites = []
            if item_type == 1029:
                create = dict(serial_num=10001, id=1, data=summon.lua(dict(union_name='道具审计仙盟')))
                replies = backend.respond(encode(1301, create), {'authenticated': True})
                assert backend.profile().get('union_id', 0) > 0, 'temporary guild creation failed'
                prerequisites.append(dict(message_id=1301, request=create, response=response_rows(replies)))
            role = backend.profile()
            item_id = formation.new_id(role)
            role['attachments'].append(dict(id=item_id, attach_type=5, type_id=item_type, level=1, count=2))
            backend.save(role)
            before = backend.profile()
            if item_type == 1041:
                mid = 1059
                request = dict(serial_num=10002, first_send=True, flag=1,
                               cortege_id=before['corteges'][0]['id'], roll_count=1,
                               roll_list=[dict(type_id=item_type, count=1)])
            else:
                mid = 1051
                request = dict(serial_num=10002, item_type=item_type, item_id=item_id,
                               item_count=1, des_type=1, des_id=0)
            emitted.clear()
            with patch.object(qiankun_bags, 'draw', return_value=[12, 1, 100, 1]):
                replies = backend.respond(encode(mid, request), {'authenticated': True})
            after = backend.profile()
            record = dict(item_type=item_type, name=item_rewards.NAMES[item_type]['name'],
                          prerequisites=prerequisites, message_id=mid, request=request,
                          response=response_rows(replies), emitted=emitted[:],
                          before=snapshot(before, item_type), after=snapshot(after, item_type),
                          role_unchanged=before == after)
            if item_type in qiankun_bags.BAGS:
                record['randomness_override'] = 'draw returns 100 silver per bag; routing/debit/achievement probe only'
            return record
        finally:
            backend.close()


def main():
    paths = ['network_redirect/backend.py', 'network_redirect/immortal.py',
             'network_redirect/item_rewards.py', 'network_redirect/qiankun_bags.py',
             'network_redirect/vip.py', 'network_redirect/achievements.py',
             'network_redirect/formation.py', 'network_redirect/journey.py',
             'analysis/configs/item_base.csv', 'analysis/configs/item_name.csv',
             'analysis/evidence/lua_named/lua/ui/packageUI.lua.txt',
             'analysis/tools/probe_remaining_item_branches.py']
    report = dict(
        audit_date='2026-10-27', timezone='Asia/Shanghai', simulated_now=NOW,
        scope='12 real binary requests on disposable databases; no emulator, official server or real account save used',
        source_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
        cases=[run_case(t) for t in (1020, 1029, 1150, 1151, 1152, 1156, 1363, 1031, 1032, 1033, 1034, 1041)],
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(OUTPUT.relative_to(ROOT))
    for case in report['cases']:
        events = [r['data']['parsed_data'] for r in case['response'] if r['message_id'] == 2998]
        print(case['item_type'], case['name'], 'unchanged=' + str(case['role_unchanged']), events)


if __name__ == '__main__':
    main()
