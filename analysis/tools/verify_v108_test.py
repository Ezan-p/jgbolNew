"""Spend the actual packaged v108 test allowance through original game rules."""
import copy
import io
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / '.runtime/v108-test/program'
sys.path[:0] = [str(PROGRAM), str(ROOT)]
from offline_android import test_edition_v108 as seed
from network_redirect import formation as f, reborn as r, fate_rebuild as fr, summon, immortal
from network_redirect import activity, activity_home as h, equipment as e, equipment_crafting as crafting
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode

EVIDENCE = ROOT / 'analysis/evidence/v108_test'
NOW = int(time.time())
report = {}


def packets_ok(b):
    packets = b.bootstrap()
    for packet in packets:
        decode(packet)
    return len(packets)


def migration():
    # The source is a generated old starter, not anyone's personal save.
    with tempfile.TemporaryDirectory() as d:
        b = Backend(Path(d), 18776, lambda *a, **k: None, account=seed.ACCOUNT)
        from offline_android.test_edition_seed import build_role
        old = build_role(b, NOW)
        old['gold_coin'] = 4321
        old['role_name'] = '旧档保留测试'
        old['corteges'][0].update(level=150, evolve_level=123)
        old['attachments'][0]['level'] = 70
        old['test_custom_sentinel'] = {'must': ['remain', 123]}
        b.save(old, gameplay=False)
        old = b.profile()
        unrelated = dict(old, role_name='不应修改')
        b.save(unrelated, account='unrelated', gameplay=False)
        other = b.db.execute("select data from roles where account='unrelated'").fetchone()[0]
        b.close()
        a = seed.fixed_accounts_class()(Path(d), 18776, lambda *a, **k: None)
        b = a.backends[seed.ACCOUNT]
        new = b.profile()
        assert new['gold_coin'] == old['gold_coin'] + 100000
        assert new['role_name'] == old['role_name']
        assert new['test_custom_sentinel'] == old['test_custom_sentinel']
        for original in old['corteges']:
            saved = next(c for c in new['corteges'] if c['id'] == original['id'])
            assert all(saved.get(k, 0) == original.get(k, 0) for k in ('type', 'level', 'evolve_level', 'reborn_layer', 'order'))
        plan = seed.material_plan()
        for original in old['attachments']:
            saved = next(i for i in new['attachments'] if i['id'] == original['id'])
            assert saved['level'] == original['level'] and saved['count'] >= original['count']
        assert b.db.execute("select data from roles where account='unrelated'").fetchone()[0] == other
        assert not seed.initialize(b, NOW)
        assert b.profile() == new
        packets_ok(b)
        # Exercise the actual complete() path and silver reserve accounting.
        new = b.profile()
        before_total = new['silver_coin'] + new['test_v108_silver_reserve']
        new['silver_coin'] -= 1500000000
        b.save(new)
        replies = b.complete(1, [])
        decoded = [decode(p) for p in replies]
        assert any(mid == 1032 and data['attr_list'] == [dict(type=7, value=2000000000)] for mid, _, data in decoded)
        after = b.profile()
        assert after['silver_coin'] + after['test_v108_silver_reserve'] == before_total - 1500000000
        request = encode(1348, dict(serial_num=1000, id=2, data=summon.lua(dict(building_type=1))))
        replies = b.respond(request, {'authenticated': True})
        decoded = [decode(p) for p in replies]
        assert not any(mid == 2998 and data.get('id') == 55 for mid, _, data in decoded)
        wire_after = b.profile()
        assert wire_after['activity']['home']['build']['1'] == 1
        assert wire_after['silver_coin'] == 2000000000
        assert wire_after['test_v108_silver_reserve'] == after['test_v108_silver_reserve'] - 2000000
        assert b.respond(request, {'authenticated': True}) == replies
        assert b.profile() == wire_after
        snapshot = copy.deepcopy(wire_after)
        a.close()
        a = seed.fixed_accounts_class()(Path(d), 18776, lambda *a, **k: None)
        assert a.backends[seed.ACCOUNT].profile() == snapshot
        a.close()
    report['migration'] = dict(progress_preserved=True, unrelated_role_unchanged=True,
        additive_gold=100000, once_only=True, restart_does_not_duplicate=True,
        finite_silver_reserve_conserved=True, silver_wire_sync=True, actual_home_protocol_and_replay=True)
    print('Existing progress, additive migration and restart passed', flush=True)


def progression():
    with tempfile.TemporaryDirectory() as d:
        a = seed.fixed_accounts_class()(Path(d), 18776, lambda *a, **k: None)
        b = a.backends[seed.ACCOUNT]
        role = b.profile()
        report['initial'] = dict(gold=role['gold_coin'], silver_wallet=role['silver_coin'],
            silver_reserve=role['test_v108_silver_reserve'], items=len(role['attachments']),
            bootstrap_packets=packets_ok(b))
        role = b.profile()
        original_silver = role['silver_coin'] + role['test_v108_silver_reserve']
        def checkpoint():
            b.save(role)
            packets_ok(b)
        def reb(kind, op, data):
            r.settle(role, dict(reborn_type=kind, id=op, data=data), b.reborn_rules, lambda x: x)
        for _ in range(4):
            reb(1, 4, {})
        book = 1080
        def feed_to(c, target):
            exp = sum(f.EXPERIENCE[5, lv] for lv in range(c['level'], target)) - c['cur_exp']
            if exp > 0:
                worth = int(f.ITEMS[book]['experience_plus'])
                f.feed(role, dict(flag=1, first_send=True, cortege_id=c['id'], roll_count=1,
                    roll_list=[dict(type_id=book, count=(exp + worth - 1) // worth)]), b.formation_rules)
        targets = [next(c for c in role['corteges'] if c['type'] == tid) for tid in seed.COMPANIONS]
        for c in targets:
            for _ in range(499):
                f.evolve(role, dict(flag=0, cortege_id=c['id']))
            for layer in range(1, 10):
                feed_to(c, 200)
                for vein in range(1, 10):
                    row = r.VEINS[layer, vein]
                    parts = [list(map(int, p.split('|'))) for p in row['consume_list'].split('/')]
                    fixed = int(row['fixed_count(fix>0|unfix=0)'])
                    materials = {parts[0][1]: fixed} if fixed else {p[1]: p[3] for p in parts}
                    reb(2, 1, dict(cortege_id=c['id'], material_list=materials))
                reb(2, 2, dict(cortege_id=c['id']))
            feed_to(c, 200)
            assert (c['evolve_level'], c['reborn_layer']) == (499, 9)
        checkpoint()
        print('Both companions: ascension 499 and rebirth 9 passed', flush=True)
        for c in targets:
            def fate(op, **data):
                fr.settle(role, dict(id=op, data=dict(cortege_id=c['id'], **data)), lambda x: x)
            fate(3)
            # Round-robin levels satisfy seven-soul aggregate gates.
            for level in range(max(fr.MAX_LEVEL.values())):
                for part in fr.PARTS:
                    if level >= fr.MAX_LEVEL[part]:
                        continue
                    for star in range(1, fr.star_count(part) + 1):
                        tokens = list(map(int, fr.COSTS[part, level, star].split('|')))
                        materials = dict(zip(tokens[1::2], tokens[2::2])) if tokens[0] == 3 else {tokens[1]: tokens[-1]}
                        fate(0, soul_part=part, material_list=materials)
            assert all(fr.progress(c, p) == (fr.MAX_LEVEL[p], 0) for p in fr.PARTS)
            checkpoint()
            print('Full fate paths passed:', c['type'], flush=True)
        for tid in seed.EQUIPMENT:
            item = next(i for i in role['attachments'] if i['type_id'] == tid and i['attach_type'] == 5)
            original = summon.weighted_choice
            try:
                summon.weighted_choice = lambda weights: 1
                while item['level'] < 198:
                    f.enhance_equipment(role, dict(equip_id=item['id'], equip_order=item.get('equip_order', 0), inbatch=True), b.formation_rules)
                    seed.refill_silver(role)
            finally:
                summon.weighted_choice = original
            for advance in range(10):
                for star in range(7):
                    f.advance_equipment(role, dict(equip_id=item['id'], equip_order=item.get('equip_order', 0), flag=1, is_one_key=True), b.formation_rules)
                f.advance_equipment(role, dict(equip_id=item['id'], equip_order=item.get('equip_order', 0), flag=2, is_one_key=True), b.formation_rules)
            reb(3, 5, dict(equip_id=item['id'], equip_order=item.get('equip_order', 0)))
            kind = int(f.ITEMS[tid]['main_type'])
            while (kind, item['cast_level'] + 1) in r.CAST:
                reb(3, 6, dict(equip_id=item['id'], equip_order=item.get('equip_order', 0)))
            assert (item['advance_level'], item['reborn_bit'], item['cast_level']) == (10, 1, 4)
        checkpoint()
        print('Two equipment pieces: 198 / advance 10 / deified cast 4 passed', flush=True)
        activity.prepare(role, NOW, b.activity_rules)
        def home(op, **data):
            result = h.settle(role, dict(id=op, data=data), NOW, b.activity_rules, b.journey_rules, lambda x: x)
            for packet in result:
                decode(packet)
            seed.refill_silver(role)
        s = h.state(role, NOW, b.activity_rules)
        while any(s['build'][str(k)] < max(h.BUILD[k]) for k in h.KEYS):
            advanced = False
            for kind in h.KEYS:
                level = s['build'][str(kind)] + 1
                if level not in h.BUILD[kind]:
                    continue
                row = h.UPGRADE[kind, level]
                requirements = [list(map(int, p.split('|'))) for p in row['pre_conditions'].split('/') if p]
                if all((s['level'] if pre == 0 else s['build'][str(pre)]) >= lv for pre, lv in requirements):
                    home(2, building_type=kind)
                    advanced = True
            if not advanced:
                assert s['level'] < max(h.OWNER)
                f.recalculate(role, b.formation_rules)
                home(25)
                assert s['passed'], 'Seed lineup could not defeat home scale gate'
                home(26)
        for idx in s['plants']:
            while s['plants'][idx]['level'] < max(h.GRIDS):
                home(9, plant_grid=int(idx))
        # Max buildings do not necessarily force the last home scale challenge.
        while s['level'] < max(h.OWNER):
            f.recalculate(role, b.formation_rules)
            home(25)
            assert s['passed']
            home(26)
        checkpoint()
        for c in targets:
            feed_to(c, 600)
            assert c['level'] == 600
        checkpoint()
        report['home'] = dict(scale=s['level'], buildings=dict(s['build']), garden_grids={k:v['level'] for k,v in s['plants'].items()})
        print('All home buildings / eight garden grids / both level 600 passed', flush=True)
        for gear_tid in (2044, 3003, 4003):
            gear = next(i for i in role['attachments'] if i['type_id'] == gear_tid and i.get('equip_order'))
            donor = next(i for i in role['attachments'] if i['type_id'] == gear_tid and not i.get('equip_order'))
            crafting.six_star(role, dict(equipid=gear['id'], equip_order=gear['equip_order'], material_equipid=donor['id']), crafting.load_rules())
            for _ in range(4):
                e.settle(role, dict(flag=1, des_id=gear['id'], equip_order=gear['equip_order'], stone_pos=0, src_count=0, src_list=[]))
            assert gear['drill_count'] == 4
        for tid, kind in e.STONES.items():
            targets_stone = [i for i in role['attachments'] if i['type_id'] == tid and i['level'] == 1][:4]
            assert len(targets_stone) == 4
            for stone in targets_stone:
                def op(flag, donors=()):
                    result = e.settle(role, dict(flag=flag, des_id=stone['id'], equip_order=0,
                        stone_pos=0, src_count=len(donors), src_list=[dict(id=i['id']) for i in donors]))
                    assert result[0][1]['result'] == 1
                    seed.refill_silver(role)
                while stone['level'] < 10:
                    donors = [i for i in role['attachments'] if i['type_id'] == tid and i['level'] == 10 and i['id'] != stone['id']][:2]
                    assert len(donors) == 2
                    op(3, donors)
                while stone['level'] < e.STONE_MAX_LEVEL[kind]:
                    op(5)
                assert stone['level'] == 14
            gear = next(i for i in role['attachments'] if i.get('equip_order') and int(f.ITEMS[i['type_id']]['main_type']) == kind and i['attach_type'] == 5)
            for pos, stone in enumerate(targets_stone, 1):
                e.settle(role, dict(flag=2, des_id=gear['id'], equip_order=gear['equip_order'], stone_pos=pos, src_count=1, src_list=[dict(id=stone['id'])]))
            assert all(gear['stone%d_level' % pos] == 14 for pos in range(1,5))
        checkpoint()
        assert all(sum(i['count'] for i in role['attachments'] if i['type_id'] == t and i['attach_type'] == 5) >= 20 for t in immortal.ESSENCES)
        assert role['gold_coin'] == 110000 - seed.material_plan()['home_gold_cost']
        report['progression'] = dict(companions=[dict(type=c['type'], level=c['level'], ascension=c['evolve_level'], rebirth=c['reborn_layer']) for c in targets],
            fate_caps=fr.MAX_LEVEL, equipment_advance=10, equipment_cast=4,
            stones_per_type=4, stone_level=14, drilled_and_inlaid_holes=12, essences_retained_each=20,
            essence_types=len(immortal.ESSENCES), gold_remaining=role['gold_coin'],
            silver_spent=original_silver - role['silver_coin'] - role['test_v108_silver_reserve'])
        saved = b.profile()
        a.close()
        a = seed.fixed_accounts_class()(Path(d), 18776, lambda *a, **k: None)
        assert a.backends[seed.ACCOUNT].profile() == saved
        packets_ok(a.backends[seed.ACCOUNT])
        a.close()
        print('All twelve stones level 14, reserved essences and final restart passed', flush=True)


if __name__ == '__main__':
    migration()
    progression()
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / 'progression-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
