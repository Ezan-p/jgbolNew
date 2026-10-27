"""Spirit arrays: client tables/contracts [A], server composition policy [B]."""
import json
from decimal import Decimal
from . import formation as f, summon

NEEDS = {(int(r['index']), int(r['pos'])): (int(r['stone_type']), int(r['stone_lv']))
         for r in summon.rows('ling_active.csv')}
COSTS = {int(r['index']): list(map(int, r['count'].split('|'))) for r in summon.rows('ling_upgrade.csv')}
STONE_VALUES = {(int(r['type']), int(r['level'])): int(r['count']) for r in summon.rows('ling_stone_value.csv')}
EFFECTS = list(summon.rows('ling_effect.csv'))


def load_rules():
    rules = json.loads((f.ROOT/'server_config/spirit_array_rules.json').read_text())
    f.require(rules['mode'] == 'inferred' and rules['attribute_policy'] == 'named_source_additive_percent'
              and rules['essence_policy'] == 'equipped_only_additive_percentage_points'
              and rules['star_policy'] == 'per_equipped_star_contribution'
              and rules['survival_policy'] == 'sum_136_145_with_star', '灵阵推测规则无效')
    for name, hi in (('max_exchange_batch', 500), ('survival_count_without_star', 10)):
        f.require(type(rules[name]) is int and 1 <= rules[name] <= hi, '灵阵配置数值无效')
    return rules


RULES = load_rules()


def state(role):
    return role.setdefault('spirit_array', [dict(activated=False, skill_list=[0]*i) for i in range(1, 7)])


def effects(role):
    result = {}
    arrays = role.get('spirit_array', [])
    for row in EFFECTS:
        index = int(row['index']) - 1
        if index >= len(arrays) or not arrays[index]['activated']:
            continue
        level = arrays[index]['skill_list'][int(row['pos'])-1]
        if level < int(row['active_level']):
            continue
        key = int(row['name_index'])
        result[key] = result.get(key, Decimal(0)) + Decimal(row['effect_value'].split('/')[level-1])
    return result


def number(value, lo, hi, message):
    f.require(type(value) is int and lo <= value <= hi, message)
    return value


def stones(role, ids):
    if isinstance(ids, dict):
        f.require(set(ids) == set(range(1, len(ids)+1)), '灵石列表无效')
        ids = [ids[i] for i in range(1, len(ids)+1)]
    f.require(isinstance(ids, list) and 0 < len(ids) <= RULES['max_exchange_batch'], '请选择灵石')
    f.require(all(type(i) in (int, float) and i > 0 and int(i) == i for i in ids), '灵石编号无效')
    f.require(len(set(ids)) == len(ids), '灵石不能重复选择')
    items = [f.lookup(role, 'attachments', i) for i in ids]
    for item in items:
        f.require(item.get('attach_type') == 5 and (item['type_id'], item['level']) in STONE_VALUES, '仅可使用4至11级灵石')
        f.require(not any(item.get(k) for k in ('owner_id', 'equip_order', 'is_lock', 'innate_owner_id')), '灵石已装备或锁定')
        f.require(item.get('count', 0) >= 1, '灵石不足')
    return items


def settle(role, req, parse, profile_rules):
    f.require(profile_rules['ling_is_open'] and role['level'] >= profile_rules['ling_open_level'], '灵阵尚未开启')
    op = number(req['id'], 1, 6, '灵阵操作无效')
    data = parse(req['data'])
    f.require(isinstance(data, dict), '灵阵参数无效')
    arrays = state(role)
    if op in (4, 5):
        return [summon.event(165, dict(flag=op, ling_info=arrays))]
    result = dict(flag=op)
    selected, refund = [], 0
    if op == 6:
        selected = stones(role, data.get('id_list'))
        refund = sum(STONE_VALUES[x['type_id'], x['level']] for x in selected)
    else:
        stage = number(data.get('goss_id'), 1, 6, '灵阵阶数无效')
        array = arrays[stage-1]
        f.require(stage == 1 or arrays[stage-2]['activated'] and all(x == 5 for x in arrays[stage-2]['skill_list']), '上一阶灵阵技能尚未满级')
        result['goss_id'] = stage
        if op == 2:
            f.require(not array['activated'] and all(array['skill_list']), '请先镶嵌全部阵位，已激活灵阵不能重复激活')
            array['activated'] = True
        else:
            pos = number(data.get('pos'), 1, stage, '灵阵位置无效')
            result['pos'] = pos
            level = array['skill_list'][pos-1]
            if op == 1:
                f.require(not array['activated'] and level == 0, '该阵位已镶嵌')
                selected = stones(role, data.get('id_list'))
                kind, minimum = NEEDS[stage, pos]
                f.require(len(selected) == 1 and selected[0]['type_id'] == kind and selected[0]['level'] >= minimum, '灵石类型或等级不符合镶嵌条件')
                refund = STONE_VALUES[kind, selected[0]['level']] - STONE_VALUES[kind, minimum]
                array['skill_list'][pos-1] = 1
            elif op == 3:
                f.require(array['activated'] and 1 <= level < 5, '灵阵未激活或技能已满级')
                f.debit_item(role, 1315, COSTS[stage][level-1])
                array['skill_list'][pos-1] += 1
    for item in selected:
        item['count'] -= 1
    role['attachments'] = [x for x in role['attachments'] if x.get('count', 1) > 0]
    result['ret_items'] = []
    if refund:
        summon.add_item(role, 1315, refund)
        result['ret_items'] = [dict(object_type=5, attach_type=1315, attach_count=refund)]
    return [summon.event(165, result)]


# [B] Apply percentages to the named source, not to the final aggregated panel.
def base_bonuses(role, c, values):
    if 1 <= c.get('order', 0) <= 8:
        e = effects(role)
        for key, stat in ((1,'hp'), (2,'gongji'), (3,'fangyu'), (4,'magic')):
            values[stat] *= 1 + e.get(key, Decimal(0))/100


def final_bonuses(role, c, values):
    if 1 <= c.get('order', 0) <= 8:
        e = effects(role)
        for key, stat in ((119,'hp'), (120,'gongji'), (121,'fangyu'), (122,'magic')):
            values[stat] += e.get(key, 0)


# effect ID -> (essence family, parameter index); only enhance an equipped essence.
ESSENCE_MAP = {100:(1,1),101:(4,1),102:(5,0),103:(17,0),104:(19,0),105:(8,0),
    106:(2,1),107:(18,1),108:(13,0),109:(18,0),110:(12,0),111:(16,1),
    112:(6,1),113:(3,1),114:(11,1),115:(14,0),116:(10,1),117:(15,0),118:(7,0)}


def attach_combat(role, units):
    from fractions import Fraction as F
    e = effects(role)
    for unit in units:
        # Battle rosters also include the ninth cell of the original 历劫 grid.
        # Ownership is resolved before re-slotting by combat_loadout.
        if not 1 <= unit.get('order', 0) <= 9:
            continue
        for key, (kind, index) in ESSENCE_MAP.items():
            values = unit.get('essences', {}).get(kind)
            if values is not None and key in e:
                values = [F(v) for v in values]
                values[index] += F(e[key])
                unit['essences'][kind] = tuple(values)
        traits = unit.setdefault('reborn_traits', {})
        for key, name in ((132,'resist'),(133,'reduction'),(134,'crit'),(135,'crit_damage'),(136,'survival'),(145,'survival')):
            traits[name] = traits.get(name, 0) + float(e.get(key, 0))
        if e.get(136) or e.get(145):
            traits['survival_count'] = max(RULES['survival_count_without_star'], traits.get('survival_count', 0))
        training = list(unit.get('training_bonuses', [(0, 0)]*4))
        unit['training_bonuses'] = [(F(a)+F(e.get(128+i,0)), F(b)+F(e.get(124+i,0))) for i,(a,b) in enumerate(training)]


def star_bonus(role, c, stat, contribution):
    if not 1 <= c.get('order', 0) <= 8:
        return contribution
    e = effects(role)
    flat, rate = {'gongji':(137,138), 'fangyu':(139,140), 'hp':(141,142), 'magic':(0,143)}[stat]
    return contribution * (1 + e.get(rate, Decimal(0))/100) + e.get(flat, 0)
