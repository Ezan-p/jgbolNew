"""Audit current reforge behavior using disposable databases, never live saves."""
import copy
import json
from pathlib import Path
import sys
from unittest.mock import patch
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tests.test_equipment_crafting import CraftingTests
from network_redirect import equipment_crafting as crafting, formation, equipment, summon
from network_redirect.backend import Backend


def run():
    report = {"client_date": "2026-10-28", "live_inventory_modified": False,
              "checks": [], "observations": []}
    case = CraftingTests()
    case.setUp()
    try:
        baseline = copy.deepcopy(case.b.profile())

        def reset():
            case.b.save(copy.deepcopy(baseline))

        def check(name, value):
            assert value, name
            report["checks"].append(name)

        names = {int(r['Ftype_id']): r['name'] for r in summon.rows('item_name.csv')}
        allowed = [p[1] for p in crafting.parts(crafting.EXCHANGE['input'])]
        report['equipment'] = [{"id": t, "name": names[t],
                                "category": int(formation.ITEMS[t]['main_type'])} for t in allowed]
        report['rules'] = {k: crafting.load_rules()[k] for k in ('transform_min_level', 'transform_gold')}
        # Capture the exact candidate sets for all ten sources and both target types.
        for tid in allowed:
            for state in (1, 2):
                reset()
                ident = case.add(tid)
                case.add(1100, count=2)
                seen = []
                def choose(pool):
                    seen.extend(pool)
                    return pool[0]
                with patch.object(crafting, 'secrets', SimpleNamespace(choice=choose)):
                    event = case.req(1225, item_id=ident, state=state)[-1]
                expected = [t for t in allowed if int(formation.ITEMS[t]['main_type']) == state and t != tid]
                check(f'candidate_pool_{tid}_to_{state}', event[0] == 124 and seen == expected)

        reset()
        ident = case.add(2001, level=50, advance_level=3, star_count=2, cur_spirit_count=1,
                         drill_count=2, stone1_level=10, reborn_bit=1, cast_level=1)
        stone = case.add(1090, level=10, owner_id=ident, equip_pos=1)
        token = case.add(1100, count=2)
        before = case.b.profile()
        old = case.get(ident)
        event = case.req(1225, item_id=ident, state=2)[-1]
        new = case.get(event[1]['item_id'])
        keys = ('level', 'advance_level', 'star_count', 'cur_spirit_count', 'drill_count', 'reborn_bit', 'cast_level')
        check('growth_inheritance', all(new[k] == old[k] for k in keys))
        check('one_token_no_currency', case.get(token)['count'] == 1 and
              all(case.b.profile()[k] == before[k] for k in ('gold_coin', 'silver_coin')))
        check('new_instance_old_removed', new['id'] != ident and not any(i['id'] == ident for i in case.b.profile()['attachments']))
        check('linked_stone_returned', all(case.get(stone)[k] == 0 for k in ('owner_id', 'equip_pos', 'equip_order'))
              and all(new[f'stone{n}_level'] == 0 for n in range(1, 5)))
        check('effect_recalculated', new['effect_value'] == equipment.effect(new))
        saved = case.b.profile()
        check('same_packet_replay', case.b.respond(case.packet, {'authenticated': True}) == case.replies and case.b.profile() == saved)
        check('old_item_new_serial_rejected', case.req(1225, item_id=ident, state=2)[-1][0] == 55 and case.b.profile() == saved)
        case.b.close()
        case.b = Backend(Path(case.tmp.name), 18770, lambda *a, **kw: None)
        check('reload_persistence', case.b.profile() == saved)

        blocked = [('level_24', {}, 24, 1, True), ('worn', {'equip_order': 1}, 99, 1, True),
                   ('locked', {'is_lock': 1}, 99, 1, True), ('owned', {'owner_id': 123}, 99, 1, True),
                   ('exclusive', {'innate_owner_id': 123}, 99, 1, True),
                   ('no_token', {}, 99, 1, False), ('bad_state', {}, 99, 3, True)]
        for name, fields, level, state, token_present in blocked:
            reset()
            ident = case.add(2001, **fields)
            if token_present:
                case.add(1100)
            role = case.b.profile(); role['level'] = level; case.b.save(role)
            before = case.b.profile()
            event = case.req(1225, item_id=ident, state=state)[-1]
            check(name + '_atomic_rejection', event[0] == 55 and before == case.b.profile())
        for name, tid in [('non_whitelisted_five_star', next(t for t,r in formation.ITEMS.items()
                           if int(r['quality']) == 5 and int(r['main_type']) == 1 and t not in allowed)),
                          ('talisman', 4001), ('non_equipment', 1100)]:
            reset(); ident = case.add(tid); case.add(1100)
            before = case.b.profile()
            check(name + '_atomic_rejection', case.req(1225, item_id=ident, state=1)[-1][0] == 55 and before == case.b.profile())
        reset(); ident = case.add(2001); case.add(1100)
        role = case.b.profile(); role['level'] = 25; case.b.save(role)
        check('level_25_allowed', case.req(1225, item_id=ident, state=1)[-1][0] == 124)

        reset(); ident = case.add(2001, star_level=1); case.add(1100)
        event = case.req(1225, item_id=ident, state=2)[-1]
        report['observations'].append({'name': 'six_star_backend_accepts', 'event': event[0],
                                       'star_level_after': case.get(event[1]['item_id'])['star_level']})
        reset()
        ident = case.add(2001, count=2, level=30, drill_count=1, stone1_level=3)
        stone = case.add(1090, level=3, owner_id=ident, equip_pos=1)
        case.add(1100, count=2)
        case.req(1225, item_id=ident, state=2)
        rest = next(i for i in case.b.profile()['attachments'] if i['type_id'] == 2001 and i['id'] != ident)
        case.req(1225, item_id=rest['id'], state=2)
        returned = [i for i in case.b.profile()['attachments'] if i['type_id'] == 1090 and i['level'] == 3 and not i.get('owner_id')]
        report['observations'].append({'name': 'legacy_stack_stone_duplication', 'initial_stones': 1,
                                       'returned_stones': sum(i['count'] for i in returned),
                                       'inherited_level_on_remainder': rest['level']})
    finally:
        case.doCleanups()
    return report


if __name__ == '__main__':
    result = run()
    destination = ROOT / 'analysis/evidence/equipment_transform/audit_20261028.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'checks_passed': len(result['checks']), 'observations': result['observations'],
                      'report': str(destination)}, ensure_ascii=False))
