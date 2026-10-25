"""Original 3.87 crafting contracts, with explicit inferred server policy.

Called only on Backend's detached role; failures discard every debit and reward.
"""
from collections import defaultdict
from decimal import Decimal
import json
import secrets
from . import formation as f, equipment, summon

HANDLED = {1053, 1055, 1056, 1074, 1079, 1225}
RECIPES = summon.rows('material_transform.csv')
RECYCLE = {int(r['quality']): r for r in summon.rows('equip_transfer_config.csv')}
SELL = {int(r['equip_quality']): r for r in summon.rows('item_sell_config.csv')}
EXCHANGE = summon.rows('item_exchange_config.csv')[0]
SRC = 'src_material(object_type|attach_type|attach_level|attach_count)'
COST = 'cost_material(object_type|attach_type|attach_level|attach_count/..)'
DEST = 'des_material(object_type|attach_type|attach_level|attach_count/..)'


def load_rules():
    r = json.loads((f.ROOT / 'server_config/equipment_crafting_rules.json').read_text())
    f.require(r['schema_version'] == 1 and r['mode'] == 'inferred', '装备配方配置来源无效')
    for k in ('compose_min_level', 'transform_min_level', 'six_star_min_level', 'sale_min_level'):
        f.require(type(r[k]) is int and r[k] in f.LEVELS, '装备开放等级配置无效')
    f.require(type(r['transform_gold']) is int and 0 <= r['transform_gold'] <= 100000, '重铸费用配置无效')
    f.require(r['six_star_min_realm'] == 4, '原客户端升星需要四重境界')
    f.require(r['exchange_shards'] == 40, '碎片兑换配置无效')
    f.require(r['six_star_refund_rate'] == 1 and r['dispose_stones'] == 'return', '装备返还配置无效')
    f.require(type(r['activity_material_count']) is int and 1 <= r['activity_material_count'] <= 50, '合成数量配置无效')
    f.require(type(r['exchange_limit']) is int and 1 <= r['exchange_limit'] <= 100, '兑换次数配置无效')
    f.require(r['activity_material_quality'] in (1, 2, 3, 4, 5), '合成品质配置无效')
    return r


def parts(raw):
    return [tuple(map(int, x.split('|'))) for x in raw.split('/') if x]


def sequence(value):
    if isinstance(value, dict):
        f.require(set(value) == set(range(1, len(value) + 1)), '材料列表格式错误')
        value = [value[n] for n in range(1, len(value) + 1)]
    f.require(isinstance(value, list), '材料列表格式错误')
    return value


def selected(role, entries, count):
    f.require(len(entries) == count and 1 <= count <= 255, '材料数量错误')
    ids = [x['id'] for x in entries]
    f.require(len(set(ids)) == len(ids), '材料不能重复')
    return [f.lookup(role, 'attachments', i) for i in ids]


def free(item):
    f.require(not any(item.get(k) for k in ('equip_order', 'owner_id', 'is_lock', 'innate_owner_id', 'protogenic')), '已装备、锁定或专属物品不能消耗')
    f.require(item['attach_type'] == 6 or item.get('count', 0) > 0, '材料数量不足')


def gear(item):
    f.require(item['attach_type'] == 5 and item['type_id'] in f.ITEMS, '目标不是装备')
    c = f.ITEMS[item['type_id']]
    f.require(int(c['main_type']) in (1, 2, 3), '目标不是装备')
    return int(c['main_type']), int(c['quality'])


def take(role, item, count):
    free(item)
    if item['attach_type'] == 6:
        f.require(count == 1, '每个法术编号只能分解一次')
        role['attachments'].remove(item)
        return
    f.require(type(count) is int and count > 0 and item['count'] >= count, '材料不足')
    item['count'] -= count
    role['attachments'] = [i for i in role['attachments'] if i['id'] != item['id'] or item['count'] > 0]


def grant(role, entries):
    totals = defaultdict(int)
    for kind, tid, level, count, *unused in entries:
        f.require(count > 0 and kind in (5, 6, 11, 12), '奖励配置无效')
        totals[kind, tid, level] += count
    result = []
    for (kind, tid, level), count in totals.items():
        if kind in (11, 12):
            key = 'gold_coin' if kind == 11 else 'silver_coin'
            f.require(role.get(key, 0) + count <= 2147483647, '货币达到上限')
            role[key] = role.get(key, 0) + count
        elif kind == 5 and level == 1 and int(f.ITEMS[tid]['can_stack']):
            summon.add_item(role, tid, count)
        else:
            f.require(tid in (f.ITEMS if kind == 5 else f.SKILLS), '奖励物品不存在')
            for _ in range(count):
                role['attachments'].append(dict(id=f.new_id(role), attach_type=kind, type_id=tid, level=level, count=0 if kind == 6 else 1))
        result.append(dict(object_type=kind, attach_type=tid, attach_level=level, attach_count=count))
    return result


def charge(role, entries, times=1):
    for kind, tid, level, count, *unused in entries:
        if kind in (11, 12):
            f.debit_money(role, 'gold_coin' if kind == 11 else 'silver_coin', count * times)
        else:
            f.require(kind == 5, '消耗材料类型无效')
            equipment.consume_level(role, tid, level, count * times, 0)


def detach_stones(role, item):
    # Return real linked stones, or recover legacy socket-only saves once.
    for pos in range(1, 5):
        level = item.get('stone%d_level' % pos, 0)
        linked = [s for s in role['attachments'] if s.get('owner_id') == item['id'] and s.get('equip_pos') == pos]
        if linked:
            for stone in linked:
                stone.update(owner_id=0, equip_pos=0, equip_order=0)
        elif level:
            grant(role, [(5, 1089 + gear(item)[0], level, 1)])
        item['stone%d_level' % pos] = 0


def invested(item):
    main, quality = gear(item)
    totals = defaultdict(int)
    level = item.get('advance_level', 0)
    for tier in range(level + 1):
        stars = 7 if tier < level else item.get('star_count', 0)
        for star in range(1, stars + 1):
            totals[1309 + main] += int(f.STAR_COST[quality, star][tier].split('|')[main - 1])
        if tier:
            for tid, count in parts(f.ADVANCE_COST[quality, tier][{1:'wuqi_cost',2:'fangyu_cost',3:'fabao_cost'}[main]]):
                totals[tid] += count
    totals[1309 + main] += item.get('cur_spirit_count', 0)
    silver = sum(int(f.EQUIP_COST[n]['star%d_money' % quality]) for n in range(1, item.get('level', 1)))
    return totals, silver


def dispose(role, item, rate=Decimal(0)):
    free(item)
    # Do not duplicate investments from ambiguous historical stacked gear.
    if item.get('count', 1) > 1:
        f.require(item.get('level', 1) == 1 and not any(item.get(k) for k in
                  ('advance_level', 'star_count', 'cur_spirit_count', 'reborn_bit', 'star_level', 'drill_count')), '养成装备叠加数据异常，请先整理')
    equipment.split_one(role, item)
    detach_stones(role, item)
    totals, silver = invested(item)
    rewards = [(5, t, 1, f.floor(n * rate)) for t, n in totals.items() if f.floor(n * rate)]
    if f.floor(silver * rate):
        rewards.append((12, 1, 1, f.floor(silver * rate)))
    take(role, item, 1)
    return rewards


def transform(role, req, rules):
    f.require(role['level'] >= rules['transform_min_level'], '尚未达到装备重铸等级')
    target = f.lookup(role, 'attachments', req['item_id'])
    free(target); main, quality = gear(target)
    allowed = {p[1] for p in parts(EXCHANGE['input'])}
    f.require(quality == 5 and target['type_id'] in allowed and req['state'] in (1, 2), '该装备不能重铸为指定类型')
    candidates = [p[1] for p in parts(EXCHANGE['output']) if int(f.ITEMS[p[1]]['main_type']) == req['state'] and p[1] != target['type_id']]
    f.require(candidates, '没有可用重铸结果')
    f.debit_item(role, 1100, 1)
    f.debit_money(role, 'gold_coin', rules['transform_gold'])
    equipment.split_one(role, target)
    detach_stones(role, target)
    # Replace the instance so the original package reader refreshes csvInfo.
    old = dict(target)
    role['attachments'].remove(target)
    target.update(id=f.new_id(role), type_id=secrets.choice(candidates), equip_pos=0)
    role['attachments'].append(target)
    return [(124, dict(result=0, item_id=target['id'], old_item_id=old['id']))]


def six_star(role, req, rules):
    f.require(role['level'] >= rules['six_star_min_level'], '尚未达到装备升星等级')
    f.require(role.get('reborn_layer', 0) >= rules['six_star_min_realm'], '装备升星需要主角四重境界')
    item = f.lookup(role, 'attachments', req['equipid'])
    main, quality = gear(item)
    f.require(quality == 5 and item.get('star_level', 0) == 0, '仅未升星五星装备可升星')
    f.require(item.get('count') == 1, '升星目标须为独立装备，旧叠加装备请先整理')
    f.require(req['equip_order'] == item.get('equip_order', 0), '装备位置已变化')
    material = f.lookup(role, 'attachments', req['material_equipid'])
    f.require(material['id'] != item['id'] and material['attach_type'] == 5 and material['type_id'] == item['type_id'] and not material.get('star_level'), '需要另一件未升星同名装备')
    free(material)
    f.debit_item(role, 1369, 20)
    refunds = dispose(role, material, Decimal(str(rules['six_star_refund_rate'])))
    item['star_level'] = 1
    return [(201, dict(equip_id=item['id'], attach_list=grant(role, refunds)))]


def sell(role, req, rules, parse):
    f.require(role['level'] >= rules['sale_min_level'], '尚未达到出售等级')
    data = parse(req['data'])
    ids = sequence(data.get('equip_list', []))
    items = selected(role, [dict(id=i) for i in ids], len(ids))
    total = 0
    for item in items:
        free(item)
        _, quality = gear(item)
        f.require(quality < 4 and item.get('advance_level', 0) == 0, '批量出售仅支持未进阶的一至三星装备')
        _, silver = invested(item)
        row = SELL[quality]
        total += f.floor(Decimal(row['base_sell_price']) + Decimal(row['price_attenuation']) * silver)
        dispose(role, item)
    grant(role, [(12, 1, 1, total)])
    return [(16, dict(result=1, silver_coin=total))]


def recipe_for(item, flag):
    tables = RECIPES if flag in (2, 3) else summon.rows('jingpo_transform.csv' if flag == 4 else 'skill_material_transform.csv')
    for row in tables:
        category = int(row['category'])
        if flag == 2 and category >= 100 or flag == 3 and category < 100:
            continue
        for src in parts(row[SRC]):
            if (item['attach_type'], item['type_id'], item.get('level', 1)) == src[:3]:
                return row, src
    raise f.Rejected('该物品没有对应转换配方')


def apply_recipe(role, item, flag, times, desired=1):
    row, src = recipe_for(item, flag)
    f.require(role['level'] >= int(row['min_role_level']), '尚未达到材料转换等级')
    take(role, item, src[3] * times)
    charge(role, parts(row[COST]), times)
    dest = parts(row[DEST]); rewards = []
    if flag == 4:
        dest = [x for x in dest if x[1] == desired]
        f.require(len(dest) == 1, '精魄转换目标无效')
        rewards = [(*dest[0][:3], dest[0][3] * times)]
    elif int(row['is_random']):
        weights = {n: x[4] for n, x in enumerate(dest)}
        f.require(all(w > 0 for w in weights.values()), '随机配方权重无效')
        rewards = [dest[summon.weighted_choice(weights)][:4] for _ in range(times)]
    else:
        rewards = [(*x[:3], x[3] * times) for x in dest]
    return rewards


def material_transform(role, req):
    flag, times = req['flag'], req['num']
    f.require(flag in (1, 2, 3, 4, 5) and 1 <= times <= 255, '材料转换参数无效')
    items = selected(role, req['id_list'], req['count'])
    from . import immortal
    if flag == 4:
        return immortal.transform(role, req)
    if flag == 3 and len(items) == 1 and items[0]['type_id'] in immortal.ESSENCES:
        return immortal.decompose(role, req)
    rewards, compensation = [], []
    if flag == 1:
        f.require(times == 1 and req['des_type'] == 1, '装备分解参数无效')
        for item in items:
            main, quality = gear(item)
            f.require(quality in RECYCLE and not item.get('star_level') and not item.get('reborn_bit'), '该装备不能分解')
            row = RECYCLE[quality]
            f.require(role['level'] >= int(row['min_role_level']), '尚未达到装备分解等级')
            compensation += dispose(role, item, Decimal(row['exchange_rate']))
            if main == 3:
                rewards += parts(row['is_fabao'])
            else:
                rewards += [(5, int(row['des_type']), 1, int(row['des_count']))] + parts(row['attach_list'])
    else:
        f.require(len(items) == 1, '请选择一种转换材料')
        if flag != 4:
            f.require(req['des_type'] == 1, '材料转换目标无效')
        rewards = apply_recipe(role, items[0], flag, times, req['des_type'])
    prizes = grant(role, rewards)
    refunds = grant(role, compensation)
    return [(116, dict(flag=flag, result=1, item_list=prizes + refunds, attach_list=prizes + refunds,
                      transform_list=prizes, compensate_list=refunds))]


def compose_list(role, rules):
    state = role.get('equipment_forge', {})
    appoint = []
    for tid, c in f.ITEMS.items():
        if int(c['main_type']) in (1, 2, 3) and int(c['quality']) in (4, 5):
            appoint.append(dict(material_type=tid, material_quality=rules['activity_material_quality'], material_count=rules['activity_material_count'], flag=1 if str(tid) in state.get('appointed', []) else 0))
    exchange = dict(count_limit=rules['exchange_limit'], exchanged_count=state.get('exchanged', 0))
    for tid in (6001, 6002, 6003, 6004):
        exchange[tid] = dict(need_count=rules['activity_material_count'], need_quality=rules['activity_material_quality'])
    return dict(equip_compose=dict(start_time=1, end_time=2147483647, appoint=appoint, exchange=exchange))


def random_list():
    rows = {}
    for row in RECIPES:
        for kind, tid, level, count in parts(row[SRC]):
            c = f.ITEMS.get(tid, {})
            if kind == 5 and int(c.get('main_type', 0)) == 12 and int(row['category']) in (1, 2, 3):
                rows[int(c['quality']), int(c['sub_type'])] = dict(compose_quality=int(c['quality']), compose_maintype=int(c['sub_type']), material_count=count)
    return list(rows.values())


def compose(role, req, rules):
    f.require(role['level'] >= rules['compose_min_level'], '尚未达到装备合成等级')
    op = req['compose_type']
    f.require(op in (1, 2, 3), '装备合成类型无效')
    items = selected(role, req['material_list'], req['material_count'])
    if op == 1:
        f.require(len(items) == 1, '请选择一叠装备碎片')
        c = f.ITEMS.get(items[0]['type_id'], {})
        f.require(items[0]['attach_type'] == 5 and int(c.get('main_type', 0)) == 12
                  and req['equip_type'] == int(c['sub_type']) and req['equip_quality'] == req['material_quality'] == int(c['quality']), '碎片类型或品质错误')
        rewards = apply_recipe(role, items[0], 2, 1)
        f.require(all(x[0] == 5 and int(f.ITEMS[x[1]]['main_type']) in (1, 2, 3) for x in rewards), '该碎片不能合成装备')
    else:
        target = req['equip_type']; c = f.ITEMS.get(target, {})
        f.require(c and req['equip_quality'] == int(c['quality']) and req['material_quality'] == rules['activity_material_quality'] and len(items) == rules['activity_material_count'], '活动合成配置已变化')
        state = role.setdefault('equipment_forge', dict(appointed=[], exchanged=0))
        if op == 2:
            main, quality = int(c['main_type']), int(c['quality'])
            f.require(main in (1, 2, 3) and quality in (4, 5) and str(target) not in state['appointed'], '该装备不可锻造或已锻造')
            f.debit_item(role, (1007 if quality == 5 else 1010) + main, 1)
            state['appointed'].append(str(target))
            rewards = [(5, target, 1, 1)]
        else:
            f.require(target in (6001, 6002, 6003, 6004) and state['exchanged'] < rules['exchange_limit'], '碎片兑换次数已满或目标错误')
            state['exchanged'] += 1
            rewards = [(5, target, 1, rules['exchange_shards'])]
        for item in items:
            _, q = gear(item)
            f.require(q == rules['activity_material_quality'] and item.get('level', 1) == 1
                      and not any(item.get(k) for k in ('advance_level', 'star_count', 'cur_spirit_count', 'reborn_bit', 'star_level')), '请选择未养成的对应品质装备')
            dispose(role, item)
    prizes = grant(role, rewards)
    return [(6, dict(compose_type=op, equip_type=rewards[0][1], attach_list=prizes))]


def settle(role, mid, req, parse):
    r = load_rules()
    if mid == 1055:
        f.require(req['flag'] in (0, 1), '配方查询参数无效')
        return [(98, random_list()), (7, dict(compose_list(role, r), show=req['flag'] == 0))]
    if mid == 1053:
        return compose(role, req, r)
    if mid == 1056:
        return sell(role, req, r, parse)
    if mid == 1074:
        return material_transform(role, req)
    if mid == 1079:
        return six_star(role, req, r)
    return transform(role, req, r)
