"""1246 conversion: original kickUI contract [A], offline target catalog [B]."""
from . import formation as f, summon

ITEM = 1246
CONFIG_SECTION = 27  # common_def.client_config_type.longer_hill
OWNED_ONLY = frozenset((5027, 5046, 5053))  # kickUI:104,1106
MAX_BATCH = 15  # kickUI:1173-1176
MAX_COUNT = 2147483647


def validate(rules):
    f.require(isinstance(rules, dict) and rules.get('mode') == 'inferred', '仙缘果名单须标记 inferred')
    for key, catalog in (('soul_targets', f.BASES), ('realm_targets', f.ITEMS)):
        targets = rules.get(key)
        f.require(isinstance(targets, list) and targets and
                  all(type(t) is int and t in catalog for t in targets), '仙缘果目标不存在')
        f.require(len(targets) == len(set(targets)), '仙缘果目标重复')
        f.require(all(int(catalog[t]['quality']) == 5 for t in targets), '仙缘果仅开放五星目标')
    f.require(all(int(f.ITEMS[t]['main_type']) == 11 for t in rules['realm_targets']), '仙缘果道具目标须为五法界魂')


def client_config(rules):
    # onGetCortList expects object_type -> {template_id: truthy}, not arrays.
    return {10: dict.fromkeys(rules['soul_targets'], True),
            5: dict.fromkeys(rules['realm_targets'], True)}


def usable(item):
    return (item.get('attach_type') == 5 and item.get('type_id') == ITEM
            and item.get('level', 1) == 1 and type(item.get('count')) is int
            and item['count'] > 0 and not any(item.get(k) for k in
                ('is_lock', 'owner_id', 'equip_order', 'equip_pos', 'star_level',
                 'ext_skill_pos', 'ext_awaken_pos')))


def exchange(role, req, rules):
    count, kind, target = req['item_count'], req['des_type'], req['des_id']
    f.require(req['item_type'] == ITEM and type(count) is int and 1 <= count <= MAX_BATCH,
              '仙缘果每次使用1至15颗')
    anchor = f.lookup(role, 'attachments', req['item_id'])
    f.require(usable(anchor), '仙缘果实例无效或已锁定')
    owned = any(c['type'] == target for c in role['corteges'])
    if kind == 10:
        f.require(target in rules['soul_targets'] and (target not in OWNED_ONLY or owned),
                  '该神仙尚未开放仙缘果兑换，或需要先拥有')
        gain = count * (10 if owned else 1)  # kickUI:1187-1199
        previous = role.get('souls', {}).get(str(int(target)), 0)
    else:
        f.require(kind == 5 and target in rules['realm_targets'], '请选择有效的神仙魂魄或五法界魂')
        gain = count * 10
        previous = sum(i['count'] for i in role['attachments']
                       if i.get('attach_type') == 5 and i.get('type_id') == target)
    f.require(type(previous) is int and 0 <= previous <= MAX_COUNT - gain, '兑换后魂魄或界魂数量超出上限')
    stacks = [i for i in role['attachments'] if usable(i)]
    f.require(sum(i['count'] for i in stacks) >= count, '可用仙缘果不足')
    # Validate the whole request first; the original UI counts all stacks but
    # getPropsID sends only one instance ID. Consume that instance first.
    stacks = [anchor] + [i for i in stacks if i is not anchor]
    remaining = count
    for item in stacks:
        take = min(item['count'], remaining)
        item['count'] -= take
        remaining -= take
        if not remaining:
            break
    role['attachments'] = [i for i in role['attachments'] if i not in stacks or i['count'] > 0]
    target = int(target)
    if kind == 10:
        role.setdefault('souls', {})[str(target)] = previous + gain
    else:
        summon.add_item(role, target, gain)
    prize = dict(object_type=kind, attach_type=target, attach_count=gain, attach_level=1)
    return [(21, dict(result=1, type_id=ITEM, count=count, attach_list=[prize]))]
