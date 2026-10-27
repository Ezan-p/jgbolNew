"""Shared seasonal-food mechanics. Each caller supplies its own random draws."""
import copy
from collections import defaultdict
from . import formation, item_rewards, summon


def weighted(values, weights, roll):
    ticket = roll(sum(weights))
    for value, weight in zip(values, weights):
        if ticket < weight:
            return value
        ticket -= weight
    raise AssertionError('Invalid seasonal-food weighted pool')


def material_specs(rules, common, fillings, roll):
    specs = [[5, common, weighted(rules['flour_counts'], rules['flour_weights'], roll), 1]]
    for tid in fillings:
        count = weighted([0, 1, 2], rules['filling_weights'], roll)
        if count:
            specs.append([5, tid, count, 1])
    return specs


def draw(pool, roll):
    groups = pool['groups']
    group = weighted(groups, [g['weight'] for g in groups], roll)
    candidates = group['candidates']
    return copy.deepcopy(candidates[roll(len(candidates))] if len(candidates) > 1 else candidates[0])


def use(role, req, pools, mapping, draw_one, label):
    tid, count = req['item_type'], req['item_count']
    require = formation.require
    require(tid in mapping and type(count) is int and 1 <= count <= 100, f'{label}使用数量无效（1至100个）')
    require(req['des_type'] == 1 and req['des_id'] in (0, role['role_id']), f'{label}使用目标无效')
    item = formation.lookup(role, 'attachments', req['item_id'])
    require(item['attach_type'] == 5 and item['type_id'] == tid and item.get('level', 1) == 1
            and item['count'] >= count and not any(item.get(k) for k in
            ('is_lock', 'owner_id', 'equip_pos', 'equip_order')), f'所选{label}不足、已锁定或不可使用')
    totals = defaultdict(int)
    for _ in range(count):
        typ, target, n, level = draw_one(pools[str(mapping[tid])])
        totals[typ, target, level] += n
    for typ, field in ((11, 'gold_coin'), (12, 'silver_coin')):
        require(role.get(field, 0) + sum(n for (k, _, _), n in totals.items() if k == typ)
                <= 2147483647, f'{label}货币奖励超出上限')
    # Consume exactly the selected stack, then allocate non-stackable instances.
    item['count'] -= count
    if not item['count']:
        role['attachments'].remove(item)
    prizes = [item_rewards.grant(role, [typ, target, n, level])
              for (typ, target, level), n in sorted(totals.items())]
    return [summon.event(21, dict(result=1, type_id=tid, count=count, attach_list=prizes))]
