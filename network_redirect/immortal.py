"""Original 3.87 immortal UI contracts [A], inferred settlement [B].

See docs/神仙模块规则与调试.md. Mutations use detached role copies; Backend
encodes all responses before saving. Never execute client Lua expressions.
"""
import copy
import json
import secrets
from pathlib import Path

from . import formation as f, summon, xianyuan_fruit
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
ESSENCES = {int(r['id']): r for r in summon.rows('ext_skill.csv')}
EXCHANGE = {int(r['cortege_type']): int(r['need_count']) for r in summon.rows('adaptive_spirit_convert.csv')}
COLLECTIONS = {int(r['index']): r for r in summon.rows('collector_cortege.csv')}
LOCK_COST = {int(r['lock_count']): int(r['cost']) for r in summon.rows('ext_skill_lock_cost.csv')}
TRANSFORMS = {int(r['category']): r for r in summon.rows('jingpo_transform.csv')}
DECOMPOSE = {int(s.split('|')[1]): r for r in summon.rows('material_transform.csv')
             if int(r['category']) in (102, 103)
             for s in r['src_material(object_type|attach_type|attach_level|attach_count)'].split('/')}
UPGRADE_COST = {1: 500, 2: 1000, 3: 1500, 4: 3000}  # [A] jpmkUI:55-56
HANDLED = {1048, 1051, 1074, 1305, 1306, 1311, 1322}


def load_rules(path=ROOT / 'server_config/immortal_rules.json'):
    r = json.loads(Path(path).read_text())
    f.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred', '神仙配置须标记 inferred')
    f.require(type(r.get('adaptive_visible')) is bool, '神仙开关无效')
    f.require(r.get('essence_slots') == 4, '普通精魄槽位上限须为4，逆天第五槽独立解锁')
    f.require(r.get('essence_replacement') == 'uniform_unlocked_destroy' and
              r.get('essence_upgrade') == 'deterministic_progress', '精魄结算模式无效')
    f.require(type(r.get('collection_material_count')) is int and 1 <= r['collection_material_count'] <= 100, '收集材料无效')
    prices = r.get('exchange_silver_per_soul', {})
    f.require(set(prices) == {'3', '4', '5'} and all(type(x) is int and 1 <= x <= 1000000 for x in prices.values()), '界魂兑换价格无效')
    f.require(r.get('handbook_unowned_status') == 1 and r.get('handbook_acquired_status') == 2, '图鉴状态无效')
    f.require(r.get('essence_initial_slots') == 1, '初始精魄槽位须为1')
    for k in ('essence_unlock_base_percent', 'essence_unlock_luck_step'):
        f.require(type(r.get(k)) is int and 1 <= r[k] <= 100, '精魄开槽概率无效')
    xianyuan_fruit.validate(r.get('xianyuan_fruit'))
    return r


def client_config(rules):
    return dict({int(q): n for q, n in rules['exchange_silver_per_soul'].items()}, adaptive_visible=rules['adaptive_visible'])


def prepare(role, rules):
    before = copy.deepcopy(role)
    history = role.setdefault('handbook', {})
    for kind in (4, 5, 6, 15):
        history.setdefault(str(kind), [])
    acquired = {k: set(v) for k, v in history.items()}
    for c in role['corteges']:
        acquired['4'].add(c['type'])
        # Old bootstrap encoded the absent field as zero, preventing engraving.
        c['equiped_ext_skill_limit'] = max(c.get('equiped_ext_skill_limit', 0),
                min(3, 1 + c.get('evolve_level', 0) // 6), rules['essence_initial_slots'])
        c.setdefault('next_ext_skill_luck_point', 0)
    for i in role['attachments']:
        kind = str(i.get('attach_type', 0))
        if i.get('type_id') in ESSENCES and kind == '5':
            if not i.get('level'):
                i['level'] = 1
            i.setdefault('prob_compen', 0)
        if kind in acquired:
            acquired[kind].add(i['type_id'])
    role['handbook'] = {k: sorted(v) for k, v in acquired.items()}
    collection_bonuses(role)
    return before != role


def collection_bonuses(role):
    """Rebuild the derived collection cache before any panel settlement."""
    role.setdefault('immortal_collection', {})
    bonuses = dict(hp=0, gongji=0, fangyu=0, magic=0)
    for index, row in COLLECTIONS.items():
        members = collection_members(row)
        active = role['immortal_collection'].get(str(index), [])
        if all(pos in active for pos in range(1, len(members) + 1)):
            stat, value = map(int, row['prize'].split('|'))
            bonuses[{1: 'hp', 2: 'gongji', 3: 'fangyu', 4: 'magic'}[stat]] += value
    role['collection_bonuses'] = bonuses


def collection_members(row):
    return [int(x.split('|')[0]) for x in row['line_up(object_type|attach_type|attach_count|attach_level|attch_weight)'].split('/')]


def collection_snapshot(role, only=None):
    groups = {}
    for index, row in COLLECTIONS.items():
        if only is not None and index != only:
            continue
        members = collection_members(row)
        active = role['immortal_collection'].get(str(index), [])
        group = {pos: int(pos in active) for pos in range(1, len(members) + 1)}
        group['flag'] = sum(not value for value in group.values())  # remaining, not activated
        groups[index] = group
    return dict(line_up=groups)


def handbook(role, rules):
    catalogs = {4: set(f.BASES), 5: set(f.ITEMS), 6: set(f.SKILLS), 15: set()}
    packets = []
    for kind, types in catalogs.items():
        acquired = set(role['handbook'][str(kind)])
        labels = [dict(type_id=t, status=rules['handbook_acquired_status'] if t in acquired
                       else rules['handbook_unowned_status']) for t in sorted(types | acquired)]
        for start in range(0, max(1, len(labels)), 128):
            part = labels[start:start + 128]
            packets.append(encode(1044, dict(first_send=start == 0, object_type=kind,
                                            label_count=len(part), label_list=part)))
    return packets


def essence(role, ident):
    item = f.lookup(role, 'attachments', ident)
    f.require(item['attach_type'] == 5 and item['type_id'] in ESSENCES, '不是可用精魄')
    return item


def engrave(role, req, rules, parse):
    f.require(rules['adaptive_visible'] and role['level'] >= 38, '角色38级开放精魄铭刻与升级')
    src = essence(role, req['ext_skill_id'])
    c = f.lookup(role, 'corteges', req['des_cortege_id'])
    f.require(not src.get('owner_id') and src.get('count', 0) > 0, '请选择未铭刻的精魄')
    f.require(not src.get('is_lock'), '精魄已锁定')
    raw = parse(req['lock_list'])
    f.require(raw or ''.join(req['lock_list'].split()) == '{}', '锁定列表不是合法数据')
    f.require(isinstance(raw, (dict, list)), '锁定列表无效')
    if isinstance(raw, dict):
        f.require(set(raw) == set(range(1, len(raw) + 1)), '锁定列表须为数组')
        locks = list(raw.values())
    else:
        locks = raw
    from .fate_rebuild import essence_slots
    slots = essence_slots(c)
    f.require(all(type(n) is int and n in slots for n in locks) and len(set(locks)) == len(locks), '锁定槽位无效')
    installed = [i for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] in ESSENCES and i.get('owner_id') == c['id']]
    f.require(all(type(i.get('ext_skill_pos')) is int and i['ext_skill_pos'] in slots and i.get('count', 0) > 0 for i in installed), '已铭刻精魄槽位数据无效')
    f.require(all(i['type_id'] != src['type_id'] for i in installed), '不能重复铭刻同一种精魄')
    bypos = {i['ext_skill_pos']: i for i in installed}
    f.require(len(bypos) == len(installed), '已铭刻精魄槽位重复')
    # [A] The fourth price tier protects four purple essences with slot 5 open.
    # Keep the legacy three-lock path that can unlock the fourth ordinary slot.
    max_locks = 4 if len(slots) == 5 else 3
    f.require(set(locks) <= set(bypos) and len(locks) <= max_locks, '锁定槽位不存在或已全部锁定')
    f.require(all(int(f.ITEMS[bypos[p]['type_id']]['quality']) == 5 for p in locks), '只能锁定紫色精魄')
    # [A] Purple (type + 100) replaces its matching gold predecessor.
    predecessor = next((i for i in installed if i['type_id'] == src['type_id'] - 100), None)
    limit = c['equiped_ext_skill_limit']
    luck = c['next_ext_skill_luck_point']
    if predecessor:
        pos = predecessor['ext_skill_pos']
        f.require(pos not in locks, '同系旧精魄已锁定')
    else:
        free = [p for p in slots if p not in bypos]
        candidates = [p for p in slots if p in bypos and p not in locks and not bypos[p].get('is_lock')]
        if free:
            pos = min(free)
        elif c['equiped_ext_skill_limit'] < 4 and (not candidates or secrets.randbelow(100) < min(100, rules['essence_unlock_base_percent'] + c['next_ext_skill_luck_point'])):
            limit += 1
            luck = 0
            pos = limit
        else:
            f.require(candidates, '没有可替换槽位')
            pos = secrets.choice(candidates)
            if c['equiped_ext_skill_limit'] < 4:
                luck = min(100, luck + rules['essence_unlock_luck_step'])
    replaced = bypos.get(pos)
    f.require(not replaced or not replaced.get('is_lock'), '被替换精魄已锁定')
    if locks:
        f.debit_money(role, 'gold_coin', LOCK_COST[len(locks)])
    c['equiped_ext_skill_limit'], c['next_ext_skill_luck_point'] = limit, luck
    if replaced:
        role['attachments'].remove(replaced)
    # A bag stack becomes one independent engraved instance.
    if src['count'] > 1:
        src['count'] -= 1
        engraved = dict(src, id=f.new_id(role), count=1)
        role['attachments'].append(engraved)
    else:
        engraved = src
    engraved.update(owner_id=c['id'], ext_skill_pos=pos, equip_order=0, equip_pos=0)
    return [(148, dict(ext_skill_id=engraved['id'], owner_id=c['id'], object_type=5)), (147, dict(result=0))]


def upgrade(role, req, rules):
    f.require(rules['adaptive_visible'] and role['level'] >= 38, '角色38级开放精魄铭刻与升级')
    item = essence(role, req['ext_skill_id'])
    f.require(item.get('owner_id') and any(c['id'] == item['owner_id'] for c in role['corteges']), '仅可升级已铭刻精魄')
    level, progress = item.get('level', 1), item.get('prob_compen', 0)
    f.require(level in UPGRADE_COST, '精魄已达5级')
    count = req['cost_count']
    f.require(0 < count <= min(500, UPGRADE_COST[level] - progress), '精魄石数量无效')
    f.debit_item(role, 10000, count)
    progress += count
    if progress == UPGRADE_COST[level]:
        level, progress = level + 1, 0
    item.update(level=level, prob_compen=progress)
    return [(146, dict(result=0))]


def exchange(role, req, rules):
    f.require(rules['adaptive_visible'], '界魂兑换未开放')
    item = f.lookup(role, 'attachments', req['item_id'])
    cfg = f.ITEMS.get(item['type_id'], {})
    t, count = req['des_id'], req['item_count']
    f.require(item['attach_type'] == 5 and item['type_id'] == req['item_type'] and int(cfg.get('main_type', 0)) == 11, '请选择正确的界魂')
    f.require(req['des_type'] == 4 and t in EXCHANGE and any(c['type'] == t for c in role['corteges']), '仅能兑换已拥有且开放的神仙魂魄')
    t = int(t)
    base = f.BASES[t]
    f.require(cfg['quality'] == base['quality'] and cfg['sub_type'] == base['category'], '界魂品质或种族不匹配')
    rate = EXCHANGE[t]
    f.require(0 < count <= 999 * rate and count % rate == 0 and item['count'] >= count, '界魂数量不足或无效')
    f.require(not item.get('is_lock'), '界魂已锁定')
    gain = count // rate
    f.debit_money(role, 'silver_coin', rules['exchange_silver_per_soul'][cfg['quality']] * gain)
    item['count'] -= count
    if not item['count']:
        role['attachments'].remove(item)
    souls = role.setdefault('souls', {})
    souls[str(t)] = souls.get(str(t), 0) + gain
    return [(21, dict(type_id=item['type_id'], count=count, result=1))]


def transform(role, req):
    f.require(req['flag'] == 4 and req['count'] == 1 and req['num'] == 1 and len(req['id_list']) == 1, '精魄转换参数无效')
    src = essence(role, req['id_list'][0]['id'])
    cfg = TRANSFORMS.get(src['type_id'])
    f.require(cfg and role['level'] >= int(cfg['min_role_level']), '精魄转换未开放')
    f.require(not src.get('owner_id') and not src.get('is_lock') and src['count'] > 0, '精魄已铭刻、锁定或数量不足')
    targets = [list(map(int, s.split('|'))) for s in cfg['des_material(object_type|attach_type|attach_level|attach_count/..)'].split('/')]
    target = next((r for r in targets if r[1] == req['des_type']), None)
    f.require(target, '目标精魄不在原版转换组中')
    for entry in cfg['cost_material(object_type|attach_type|attach_level|attach_count/..)'].split('/'):
        kind, t, _, n = map(int, entry.split('|'))
        f.require(kind == 5, '转换消耗类型无效')
        f.debit_item(role, t, n)
    src['count'] -= 1
    if src['count'] == 0:
        role['attachments'].remove(src)
    summon.add_item(role, target[1], target[3])
    return [(116, dict(result=1, flag=req['flag'], item_list=[dict(object_type=5, attach_type=target[1], attach_level=target[2], attach_count=target[3])]))]


def decompose(role, req):
    f.require(req['flag'] == 3 and req['count'] == 1 and len(req['id_list']) == 1
              and req['des_type'] == 1 and 1 <= req['num'] <= 255, '精魄分解参数无效')
    src = essence(role, req['id_list'][0]['id'])
    cfg, count = DECOMPOSE.get(src['type_id']), req['num']
    f.require(cfg and role['level'] >= int(cfg['min_role_level']), '精魄不可分解')
    f.require(not src.get('owner_id') and not src.get('is_lock') and src['count'] >= count,
              '精魄已铭刻、锁定或数量不足')
    for entry in cfg['cost_material(object_type|attach_type|attach_level|attach_count/..)'].split('/'):
        kind, t, _, n = map(int, entry.split('|'))
        f.require((kind, t) == (12, 1), '分解消耗类型无效')
        f.debit_money(role, 'silver_coin', n * count)
    src['count'] -= count
    if not src['count']:
        role['attachments'].remove(src)
    kind, t, level, n = map(int, cfg['des_material(object_type|attach_type|attach_level|attach_count/..)'].split('|'))
    f.require(kind == 5, '分解产物类型无效')
    summon.add_item(role, t, n * count)
    return [(116, dict(result=1, flag=3, item_list=[dict(object_type=kind, attach_type=t,
                                                     attach_level=level, attach_count=n * count)]))]


def activate(role, req, rules):
    index, pos = req['index'], req['value']
    f.require(index in COLLECTIONS, '收集组合不存在')
    members = collection_members(COLLECTIONS[index])
    f.require(1 <= pos <= len(members), '收集位置不存在')
    active = role['immortal_collection'].setdefault(str(index), [])
    f.require(pos not in active, '该收集位置已激活')
    f.require(any(c['type'] == members[pos - 1] for c in role['corteges']), '尚未拥有该神仙')
    f.debit_item(role, 1002, rules['collection_material_count'])
    active.append(pos)
    return [(157, dict(activate_data=collection_snapshot(role, index)))]


def settle(role, mid, req, rules, parse):
    if mid == 1311:
        events = engrave(role, req, rules, parse)
    elif mid == 1322:
        events = upgrade(role, req, rules)
    elif mid == 1051:
        from . import item_rewards
        if req['item_type'] in item_rewards.HANDLED:
            events = item_rewards.use(role, req)
        else:
            events = (xianyuan_fruit.exchange(role, req, rules['xianyuan_fruit'])
                      if req['item_type'] == xianyuan_fruit.ITEM else exchange(role, req, rules))
    elif mid == 1074:
        events = decompose(role, req) if req['flag'] == 3 else transform(role, req)
    elif mid == 1306:
        events = activate(role, req, rules)
    else:
        raise f.Rejected('神仙请求无效')
    prepare(role, rules)
    return [summon.event(e, data) for e, data in events]
