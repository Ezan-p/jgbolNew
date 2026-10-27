"""Inventory containers: original identity [A], explicit offline pools [B].

Special choice/activity containers keep their own handlers. No CSV is rewritten.
All settlement runs on Backend's detached role and commits after wire encoding.
"""
from collections import defaultdict
import json
import secrets

from . import formation as f, summon, journey

NAMES = {int(r['Ftype_id']): r for r in summon.rows('item_name.csv')}
SPECIAL = frozenset([1031, 1032, 1033, 1034, 1037, 1120, 1121, 1243, 1249, 1324, 1346,
                     1367, 1368, 1808, *range(1101, 1111), *range(1213, 1218)])
# Same main_type does not imply a container: gold cards recharge and fruit exchanges.
NON_CONTAINERS = frozenset([1150, 1151, 1152, 1156, 1246])
CONTAINERS = frozenset(t for t, r in f.ITEMS.items()
                       if int(r['main_type']) in (6, 7, 8)) - NON_CONTAINERS
HANDLED = CONTAINERS - SPECIAL
PATH = f.ROOT / 'server_config/item_reward_rules.json'


def valid_prize(p):
    f.require(isinstance(p, list) and len(p) == 4
              and all(type(v) is int for v in p), '宝箱奖励格式无效')
    kind, tid, count, level = p
    f.require(1 <= count <= 1000000 and level == 1 and (
        kind in (11, 12) and tid == 1 or
        kind == 5 and tid in f.ITEMS and tid not in CONTAINERS or
        kind == 6 and tid in f.SKILLS or kind == 10 and tid in f.BASES), '宝箱奖励无效或循环产出宝箱')


def load_rules():
    r = json.loads(PATH.read_text(encoding='utf-8'))
    f.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred', '宝箱配置须标注推测来源')
    f.require(set(r['items']) == set(map(str, HANDLED)), '宝箱配置未完整覆盖道具')
    for pool in r['pools'].values():
        f.require(isinstance(pool, list) and pool, '宝箱奖池不能为空')
        for group in pool:
            f.require(type(group['weight']) is int and 0 < group['weight'] <= 1000000
                      and isinstance(group['candidates'], list) and group['candidates'], '宝箱概率配置无效')
            for prize in group['candidates']:
                valid_prize(prize)
            f.require(len({tuple(p) for p in group['candidates']}) == len(group['candidates']), '宝箱候选重复')
    for rule in r['items'].values():
        f.require(rule['mode'] in ('fixed', 'random') and bool(rule.get('reason')), '宝箱规则来源缺失')
        if rule['mode'] == 'random':
            f.require(rule['pool'] in r['pools'], '宝箱奖池不存在')
        else:
            f.require(isinstance(rule['prizes'], list) and rule['prizes'], '礼包奖励缺失')
            for p in rule['prizes']:
                valid_prize(p)
    patches = r['fragment_overrides']
    f.require(set(patches) == {'10001'}, '碎片覆盖范围无效')
    patch = patches['10001']
    f.require(patch['from'] == [5, 10204, 1, 1, 30]
              and patch['to'] == [5, 10203, 1, 1, 30] and patch.get('reason'), '精魄碎片修正规则无效')
    return r


def draw(groups):
    group = groups[summon.weighted_choice({i: g['weight'] for i, g in enumerate(groups)})]
    return secrets.choice(group['candidates'])


def grant(role, spec):
    from . import equipment_crafting as c
    kind, target, count, level = spec
    # Crafting's typed allocator respects can_stack=0 for equipment as well as stones.
    if kind in (5, 6, 11, 12):
        return c.grant(role, [(kind, target, level, count)])[0]
    return journey.grant(role, spec)


def use(role, req):
    tid, count = req['item_type'], req['item_count']
    f.require(tid in HANDLED and type(count) is int and 1 <= count <= 15, '宝箱类型或数量无效（每批1至15个）')
    f.require(req['des_type'] == 1 and req['des_id'] in (0, role['role_id']), '宝箱使用目标无效')
    item = f.lookup(role, 'attachments', req['item_id'])
    f.require(item['attach_type'] == 5 and item['type_id'] == tid and item.get('level', 1) == 1
              and item['count'] >= count and not any(item.get(k) for k in
              ('is_lock', 'owner_id', 'equip_pos', 'equip_order')), '宝箱不足、已锁定或不可使用')
    rules = load_rules()
    rule = rules['items'][str(tid)]
    if rule['mode'] == 'random':
        specs = [draw(rules['pools'][rule['pool']]) for _ in range(count)]
    else:
        specs = [[k, t, n * count, lv] for k, t, n, lv in rule['prizes']]
    totals = defaultdict(int)
    for kind, target, n, level in specs:
        totals[kind, target, level] += n
    for kind, field in ((11, 'gold_coin'), (12, 'silver_coin')):
        f.require(role.get(field, 0) + sum(n for (k, _, _), n in totals.items() if k == kind)
                  <= 2147483647, '宝箱货币奖励超出上限')
    item['count'] -= count
    if not item['count']:
        role['attachments'].remove(item)
    prizes = [grant(role, [k, t, n, lv]) for (k, t, lv), n in sorted(totals.items())]
    return [(21, dict(result=1, type_id=tid, count=count, attach_list=prizes))]


def recipe_destinations(row, source_type):
    """Keep original rows intact; correct only the documented duplicate slot [B]."""
    from . import equipment_crafting as c
    dest = c.parts(row[c.DEST])
    if source_type == 10001:
        patch = load_rules()['fragment_overrides']['10001']
        old, new = tuple(patch['from']), tuple(patch['to'])
        f.require(dest.count(old) == 1 and new not in dest, '原始精魄配方已变化，请复核覆盖规则')
        dest = [new if p == old else p for p in dest]
    return dest
