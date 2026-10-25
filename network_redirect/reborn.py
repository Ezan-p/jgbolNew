"""3.87 rebirth contracts [A], explicit missing server policy [B]."""
import copy
import json
from decimal import Decimal
from pathlib import Path
from . import formation as f, summon

ROOT = Path(__file__).resolve().parents[1]
CORTS = {int(r['cortege_type']): r for r in summon.rows('cortege_reborn_config.csv')}
LAYERS = {int(r['layer']): r for r in summon.rows('cortege_reborn_layer.csv')}
VEINS = {(int(r['layer']), int(r['pulse'])): r for r in summon.rows('cortege_reborn_vein.csv')}
EFFECTS = {(int(r['effect_type']), int(r['layer'])): r['plus_list'] for r in summon.rows('cortege_reborn_effect.csv')}
EQUIP = {int(next(iter(r.values()))): r for r in summon.rows('equip_reborn_base.csv')}
CAST = {(int(r['equip_type']), int(r['level'])): r for r in summon.rows('equip_reborn_advance.csv')}
FATES = summon.rows('equip_reborn_fate.csv')
CHAIN = {int(next(iter(r.values()))): r['effect_list'] for r in summon.rows('equip_reborn_level_plus.csv')}
HANDLED = {1328, 1332, 1337, 1338, 1339, 1340, 1341, 1342}
STAT = {1: 'gongji', 2: 'fangyu', 3: 'hp', 4: 'magic'}


def load_rules(path=ROOT / 'server_config/reborn_rules.json'):
    r = json.loads(Path(path).read_text())
    f.require(r['schema_version'] == 1 and r['mode'] == 'inferred', '转生配置须标记 inferred')
    f.require(len(r['realms']) == 4, '主角境界配置须为4阶')
    f.require(r['restore_gold'] == 200, '原版觉醒还原消耗200元宝')
    previous = 0
    for x in r['realms']:
        f.require(type(x['level']) is int and x['level'] in f.LEVELS and
                  type(x['count']) is int and 0 <= x['count'] <= 255 and
                  previous < x['max_layer'] <= 9, '境界配置无效')
        f.require(type(x['boss_layer']) is int and x['boss_layer'] > 0 and x['boss_layer'] % 3 == 0, '首领展示边界须为3的倍数')
        previous = x['max_layer']
        f.require(x['material'] in f.ITEMS and type(x['cost']) is int and x['cost'] > 0, '境界材料配置无效')
    f.require(previous == 9, '境界必须覆盖九转')
    for k in ('daily_divinations', 'buy_limit', 'buy_cost', 'pending_limit'):
        f.require(type(r[k]) is int and (0 if k == 'buy_limit' else 1) <= r[k] <= 10000, '占星配置无效')
    f.require(type(r['equip_realm']) is int and 0 <= r['equip_realm'] <= 4, '装备境界配置无效')
    f.require(r['divination_min_level'] in f.LEVELS and 0 <= r['divination_advance_percent'] <= 100, '占星门槛配置无效')
    f.require(r.get('equip_initial_cast_level') == 1, '封神初始铸造等级配置无效')
    return r


def client_config(rules):
    result = {i: dict(condiction=dict(need_role_level=x['level'], reborn_layer=x['required_layer'],
                       reborn_count=x['count'], consume_list=[prize(x['material'], x['cost'])]),
                    rights=dict(max_cortege_layer=x['max_layer'], boss_layer=x['boss_layer']))
            for i, x in enumerate(rules['realms'], 1)}
    # Original realm-details UI indexes the unascended realm explicitly.
    result[0] = dict(condiction=dict(need_role_level=0, reborn_layer=0, reborn_count=0, consume_list=[]),
                     rights=dict(max_cortege_layer=0, boss_layer=0))
    return result


def prize(t, n=1, level=1):
    return dict(object_type=5, attach_type=t, attach_count=n, attach_level=level)


def prepare(role, rules):
    old = copy.deepcopy(role)
    role.setdefault('reborn_layer', 0)
    for c in role['corteges']:
        for k in ('reborn_layer', 'reborn_vein_level'):
            c.setdefault(k, 0)
        c.setdefault('reborn_plus_type', int(CORTS.get(c['type'], {}).get('plus_type', 1)))
    for item in role['attachments']:
        if item.get('reborn_bit') and item['type_id'] in f.ITEMS and int(f.ITEMS[item['type_id']]['main_type']) in EQUIP:
            item['cast_level'] = max(rules['equip_initial_cast_level'], item.get('cast_level', 0))
    i = min(role['reborn_layer'], 3)
    need = rules['realms'][i]['required_layer']
    role['maxlayer_reborn_count'] = sum(c.get('reborn_layer', 0) >= need for c in role['corteges']) if need else 0
    return old != role


def debit_material(role, tid, count):
    f.require(type(count) is int and count > 0, '材料数量无效')
    available = [x for x in role['attachments'] if x['attach_type'] == 5 and x['type_id'] == tid
                 and not any(x.get(k) for k in ('owner_id', 'equip_order', 'is_lock'))]
    f.require(sum(x['count'] for x in available) >= count, '可用材料不足')
    for item in available:
        used = min(count, item['count'])
        item['count'] -= used
        count -= used
    role['attachments'] = [x for x in role['attachments'] if x['attach_type'] == 6 or x['count'] > 0]


def consume(role, text):
    for part in text.split('/'):
        kind, t, level, count = map(int, part.split('|'))
        f.require(kind == 5 and level == 1, '不支持的转生材料')
        debit_material(role, t, count)


def settle(role, req, rules, parse):
    op, kind = req['id'], req['reborn_type']
    f.require((kind, op) in {(1, 4), (2, 1), (2, 2), (2, 3), (3, 5), (3, 6)}, '转生操作无效')
    d = parse(req['data'])
    f.require(isinstance(d, dict), '转生数据须为参数表')
    if kind == 1:
        layer = role.get('reborn_layer', 0)
        f.require(layer < 4, '主角境界已满')
        cfg = rules['realms'][layer]
        f.require(role['level'] >= cfg['level'], '主角等级不足')
        f.require(sum(c.get('reborn_layer', 0) >= cfg['required_layer'] for c in role['corteges']) >= cfg['count'], '满阶神仙数量不足')
        debit_material(role, cfg['material'], cfg['cost'])
        role['reborn_layer'] = layer + 1
    elif kind == 2:
        c = f.lookup(role, 'corteges', d.get('cortege_id'))
        f.require(c['type'] in CORTS, '该神仙不可转生')
        layer, vein = c.get('reborn_layer', 0), c.get('reborn_vein_level', 0)
        if op == 3:
            dest = d.get('des_type')
            f.require(layer > 0 and type(dest) is int and dest in (1, 2, 3) and dest != c['reborn_plus_type'], '转生属性类型无效')
            f.debit_money(role, 'gold_coin', 50)
            c['reborn_plus_type'] = dest
        else:
            f.require(layer < 9, '神仙已达九转')
            realm = role.get('reborn_layer', 0)
            f.require(realm > 0 and layer < rules['realms'][realm - 1]['max_layer'], '主角境界不足')
            if op == 1:
                f.require(vein < 9, '仙脉已全部点亮')
                row = VEINS[layer + 1, vein + 1]
                supplied = d.get('material_list')
                f.require(isinstance(supplied, dict) and all(type(k) is int and type(v) is int and v > 0 for k,v in supplied.items()), '仙脉材料无效')
                allowed = {int(p.split('|')[1]): int(p.split('|')[3]) for p in row['consume_list'].split('/')}
                count = int(row['fixed_count(fix>0|unfix=0)'])
                if count:
                    f.require(set(supplied) <= set(allowed) and sum(supplied.values()) == count, '仙脉材料种类或数量错误')
                else:
                    f.require(supplied == allowed, '仙脉材料数量错误')
                for t, n in supplied.items():
                    debit_material(role, t, n)
                c['reborn_vein_level'] = vein + 1
            else:
                row = LAYERS[layer + 1]
                f.require(vein == 9 and c['level'] >= int(row['min_level']), '需点亮九脉并达到转生等级')
                consume(role, row['consum_list'])
                quality = int(f.BASES[c['type']]['quality'])
                # [A] ascensionUI.getAscNewLevel keeps experience above min_level.
                exp = c.get('cur_exp', 0) + sum(f.EXPERIENCE[quality, lv] for lv in range(int(row['min_level']), c['level']))
                level = int(row['reset_level'])
                while (quality, level) in f.EXPERIENCE and exp >= f.EXPERIENCE[quality, level] > 0:
                    exp -= f.EXPERIENCE[quality, level]
                    level += 1
                c.update(reborn_layer=layer + 1, reborn_vein_level=0, level=level, cur_exp=exp)
                c['next_exp'] = f.EXPERIENCE.get((quality, c['level']), 0)
                c['culture_point'] = c.get('culture_point', 0) + int(row['ret_culture'])
    else:
        item = f.lookup(role, 'attachments', d.get('equip_id'))
        row = f.ITEMS.get(item['type_id'], {})
        main = int(row.get('main_type', 0))
        f.require(item['attach_type'] == 5 and main in EQUIP and int(row['quality']) == 5, '仅五星装备可转生铸造')
        f.require(d.get('equip_order') == item.get('equip_order', 0), '装备位置已变化')
        if op == 5:
            f.require(role.get('reborn_layer', 0) >= rules['equip_realm'], '主角境界不足')
            f.require(item.get('advance_level', 0) == 10 and not item.get('reborn_bit', 0), '装备需满阶且未转生')
            consume(role, list(EQUIP[main].values())[1])
            item.update(reborn_bit=1, cast_level=rules['equip_initial_cast_level'])
        else:
            f.require(item.get('reborn_bit', 0) > 0, '装备须先转生')
            nxt = item.get('cast_level', 0) + 1
            f.require((main, nxt) in CAST, '装备铸造已满级')
            consume(role, list(CAST[main, nxt].values())[2])
            item['cast_level'] = nxt
        item['effect_value'] = f.equip_effect(item)
    prepare(role, rules)
    return [summon.event(172, dict(flag=op))]


def stat_pairs(text):
    return [tuple(map(Decimal, p.split('|'))) for p in text.split('/') if p]


def bonuses(role, c, values, equipped):
    """[B] stacking order; every coefficient is an original CSV value [A]."""
    layer = c.get('reborn_layer', 0)
    rate = sum((Decimal(LAYERS[n]['four_plus_rate']) for n in range(1, layer + 1)), Decimal(0)) / 100
    for s in values:
        values[s] *= 1 + rate
    for n in range(1, layer + 1):
        for stat, value in stat_pairs(EFFECTS[c.get('reborn_plus_type', 1) or 1, n]):
            values[STAT[int(stat)]] += value
    for (l, p), row in VEINS.items():
        if l <= layer or (l == layer + 1 and p <= c.get('reborn_vein_level', 0)):
            for stat, value in stat_pairs(row['effect_list(1=gongji|2=fangyu|3=hp|4=fa)']):
                values[STAT[int(stat)]] += value
    casts = []
    for item in equipped:
        main = int(f.ITEMS.get(item['type_id'], {}).get('main_type', 0))
        if main not in EQUIP or not item.get('reborn_bit'):
            continue
        # Individual equipment effects belong to its base, not the companion.
        level = item.get('cast_level', 0)
        if (main, level) in CAST:
            casts.append(level)
    types = {x['type_id'] for x in equipped if x.get('reborn_bit')}
    for row in FATES:
        if set(map(int, row['equip_list'].split('|'))) <= types:
            for stat, value in stat_pairs(row['effect_list']):
                values[STAT[int(stat)]] *= 1 + value / 100
    # charPositionUI:2020-2050 selects the six-star chain instead of cast chain.
    six_star = {int(f.ITEMS[i['type_id']]['main_type']) for i in equipped
                if i.get('attach_type') == 5 and i['type_id'] in f.ITEMS
                and int(f.ITEMS[i['type_id']]['main_type']) in (1, 2, 3) and i.get('star_level') == 1}
    chain = 5 if six_star == {1, 2, 3} else min(casts) if len(casts) == 3 else 0
    if chain:
        for stat, value in stat_pairs(CHAIN[chain]):
            values[STAT[int(stat) - 4]] += value
