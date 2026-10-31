"""Equipment/stone values from the 3.87 client; missing stone policy is explicit."""
import copy
import json
import secrets
from decimal import Decimal
from . import formation as f, summon

STONES = {1090: 1, 1091: 2, 1092: 3}
STONE_VALUES = {(int(r['stone_type']), int(r['level'])): r for r in summon.rows('stone_cost_worth.csv')}
# Active release_w 1263 includes levels 13/14; retain the base 3.87 CSV separately.
STONE_REBORN = {(int(r['stone_type']), int(r['level'])): r for r in summon.rows('stone/stone_reborn_cost_worth.csv')}
STONE_MAX_LEVEL = {kind: max(level for k, level in STONE_REBORN if k == kind) for kind in STONES.values()}


def load_rules():
    r = json.loads((f.ROOT / 'server_config/stone_rules.json').read_text())
    f.require(r['mode'] == 'inferred' and r['schema_version'] == 1, '灵石配置来源无效')
    f.require(type(r['failure_compensation_percent']) is int and 1 <= r['failure_compensation_percent'] <= 100, '灵石补偿配置无效')
    f.require(type(r['min_role_level']) is int and r['min_role_level'] in f.LEVELS, '灵石等级配置无效')
    f.require(type(r['reborn_min_realm']) is int and 1 <= r['reborn_min_realm'] <= 4, '灵石升华境界配置无效')
    return r


def base_effect(item):
    # stoneUI.getEquipBaseEffect:803-819: rebirth improves level growth only.
    from . import reborn
    cfg = f.ITEMS[item['type_id']]
    main = int(cfg['main_type'])
    growth = Decimal(cfg['upgrade_plus']) * (item.get('level', 1) - 1)
    result = sum(Decimal(cfg[k]) for k in ('gongji_plus', 'fangyu_plus', 'maxhp_plus')) + growth
    if item.get('reborn_bit'):
        for stat, value in reborn.stat_pairs(reborn.EQUIP[main]['plus_value']):
            result += growth * value / 100 if stat <= 4 else (item.get('level', 1) - 1) * value
    return result * (1 + item.get('star_level', 0))


def stone_rate(kind, level):
    return Decimal(STONE_REBORN[kind, level]['worth'] if level > 10 else STONE_VALUES[kind, level]['base'])


def effect(item):
    # packageUI:1582-1594 displays four separately floored contributions.
    from . import reborn
    base = base_effect(item)
    main = int(f.ITEMS[item['type_id']]['main_type'])
    percent, plus, _ = f.advance_worth(item)
    rate = sum((stone_rate(main, item.get('stone%d_level' % n, 0))
                for n in range(1, 5) if item.get('stone%d_level' % n, 0)), Decimal(0))
    cast_percent = cast_plus = Decimal(0)
    if item.get('reborn_bit') and (main, item.get('cast_level', 0)) in reborn.CAST:
        for stat, value in reborn.stat_pairs(list(reborn.CAST[main, item['cast_level']].values())[3]):
            if stat <= 4:
                cast_percent += value / 100
            else:
                cast_plus += value
    return f.floor(base) + f.floor(base * rate) + f.floor(base * percent + plus) + f.floor(base * cast_percent + cast_plus)


def split_one(role, item):
    """Preserve the selected ID and separate old local stacks before mutation."""
    f.require(item.get('count', 0) > 0, '灵石数量无效')
    if item['count'] > 1:
        f.require(not item.get('owner_id'), '已镶嵌灵石数量异常')
        rest = copy.deepcopy(item)
        rest.update(id=f.new_id(role), count=item['count'] - 1)
        role['attachments'].append(rest)
        # Splitting a legacy stack is not another earned stone achievement.
        observed = role.get('achievements', {}).get('observed', {})
        for ident in (228 + STONES[item['type_id']], 480 + STONES[item['type_id']], 562 + STONES[item['type_id']]):
            previous = observed.get(f"{ident}:{item['id']}")
            if previous is not None:
                observed[f"{ident}:{rest['id']}"] = previous
        item['count'] = 1


def consume_level(role, tid, level, count, exclude):
    candidates = [i for i in role['attachments'] if i['id'] != exclude and i['attach_type'] == 5
                  and i['type_id'] == tid and i.get('level', 1) == level
                  and not any(i.get(k) for k in ('owner_id', 'equip_order', 'is_lock'))]
    f.require(sum(i['count'] for i in candidates) >= count, '对应等级材料不足')
    for i in candidates:
        used = min(count, i['count']); i['count'] -= used; count -= used
    role['attachments'] = [i for i in role['attachments'] if i['attach_type'] != 5 or i['count'] > 0]


def settle(role, req):
    rules = load_rules()
    f.require(role['level'] >= rules['min_role_level'], '尚未达到灵石开放等级')
    op, pos = req['flag'], req['stone_pos']
    f.require(op in (1, 2, 3, 4, 5), '灵石操作无效')
    ids = [x['id'] for x in req['src_list']]
    f.require(len(ids) == req['src_count'] and len(ids) == len(set(ids)), '灵石材料重复或数量错误')
    target = f.lookup(role, 'attachments', req['des_id'])
    f.require(target['attach_type'] == 5, '目标类型错误')
    links = []
    if op in (1, 2, 4):
        main = int(f.ITEMS[target['type_id']]['main_type'])
        f.require(main in (1, 2, 3), '目标不是装备')
        f.require(req['equip_order'] == target.get('equip_order', 0), '装备位置已变化')
        if op == 1:
            f.require(not ids and pos == 0, '开孔参数无效')
            limit = {1: 1, 2: 1, 3: 1, 4: 2, 5: 3}[int(f.ITEMS[target['type_id']]['quality'])] + target.get('star_level', 0)
            f.require(target.get('drill_count', 0) < min(4, limit), '装备孔位已满')
            f.debit_item(role, 1093, 1)
            target['drill_count'] = target.get('drill_count', 0) + 1
        else:
            f.require(len(ids) == 1 and 1 <= pos <= target.get('drill_count', 0), '孔位或灵石数量无效')
            stone = f.lookup(role, 'attachments', ids[0])
            f.require(stone['attach_type'] == 5 and STONES.get(stone['type_id']) == main, '灵石类型不匹配')
            key = 'stone%d_level' % pos
            if op == 2:
                f.require(not any(stone.get(k) for k in ('owner_id', 'equip_order')), '灵石已镶嵌')
                f.require(not target.get(key) and not any(i.get('owner_id') == target['id'] and i.get('equip_pos') == pos for i in role['attachments']), '孔位已有灵石')
                stone_rate(main, stone['level'])
                split_one(role, stone)
                stone.update(owner_id=target['id'], equip_pos=pos, equip_order=0)
                target[key] = stone['level']
            else:
                f.require(stone.get('owner_id') == target['id'] and stone.get('equip_pos') == pos, '灵石位置已变化')
                stone.update(owner_id=0, equip_pos=0, equip_order=0)
                target[key] = 0
            links.append(dict(id=stone['id'], owner_id=stone.get('owner_id', 0), equip_pos=stone.get('equip_pos', 0)))
        target['effect_value'] = effect(target)
    else:
        kind = STONES.get(target['type_id'])
        f.require(kind is not None, '目标不是灵石')
        owner = f.lookup(role, 'attachments', target['owner_id']) if target.get('owner_id') else None
        f.require(req['equip_order'] == (owner.get('equip_order', 0) if owner else 0)
                  and pos == target.get('equip_pos', 0), '灵石位置已变化')
        if owner:
            f.require(1 <= pos <= owner.get('drill_count', 0) and owner.get('stone%d_level' % pos) == target['level'], '镶嵌数据不一致')
        old = target['level']
        if op == 3:
            f.require(1 <= old < 10 and ids and target['id'] not in ids, '请选择材料；10级灵石需升华')
            worth = Decimal(0)
            materials = []
            for identity in ids:
                i = f.lookup(role, 'attachments', identity)
                f.require(i['attach_type'] == 5 and i['type_id'] in STONES and 1 <= i['level'] <= 10
                          and i['count'] > 0 and not any(i.get(k) for k in ('owner_id', 'equip_order', 'is_lock')), '已镶嵌、锁定或高级灵石不能作为材料')
                worth += Decimal(STONE_VALUES[STONES[i['type_id']], i['level']]['worth'])
                materials.append(i)
            row = STONE_VALUES[kind, old]
            probability = min(Decimal(100), worth * 100 / Decimal(row['cost']) + target.get('prob_compen', 0))
            split_one(role, target)
            f.debit_money(role, 'silver_coin', int(row['silver_cost']))
            for i in materials:
                i['count'] -= 1
            role['attachments'] = [i for i in role['attachments'] if i['attach_type'] != 5 or i['count'] > 0]
            success = secrets.randbelow(1000000) < probability * 10000
            if success:
                target.update(level=old + 1, prob_compen=0)
            else:
                target['prob_compen'] = min(100, target.get('prob_compen', 0) + rules['failure_compensation_percent'])
        else:
            f.require(not ids, '灵石升华或提炼参数无效')
            f.require(old >= 10, '10级灵石才可升华')
            f.require(old < STONE_MAX_LEVEL[kind], '灵石已达到提炼上限')
            f.require((kind, old + 1) in STONE_REBORN, '灵石提炼配置缺失')
            f.require(role.get('reborn_layer', 0) >= rules['reborn_min_realm'], '灵石升华需要主角境界')
            f.require(old == 10 or role.get('reborn_layer', 0) >= 4, '灵石提炼需要主角四重境界')
            split_one(role, target)
            row = STONE_REBORN[kind, old + 1]
            for part in list(row.values())[2].split('/'):
                typ, tid, count, level = map(int, part.split('|'))
                f.require(typ == 5, '材料类型无效')
                consume_level(role, tid, level, count, target['id'])
            target.update(level=old + 1, prob_compen=0)
            success = True
        if owner:
            owner['stone%d_level' % pos] = target['level']
            owner['effect_value'] = effect(owner)
        return [(83, dict(flag=op, result=1 if success else 6, des_id=target['id']))]
    return [(83, dict(flag=op, result=1, des_id=target['id'], stone_links=links))]
