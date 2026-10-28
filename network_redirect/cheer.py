"""Original Bagua wire/UI contracts [A]; missing server policy in cheer_rules [B]."""
import json
import secrets
from decimal import Decimal
from pathlib import Path
from . import formation as f, summon
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('heaven', 'earth', 'shake', 'sunda', 'water', 'fire', 'hill', 'pool')
NAMES += tuple('un' + n for n in NAMES)
STATS = ('gongji', 'fangyu', 'hp', 'magic')
ROWS = {(int(r['cheer_order']), int(r['level'])): r for r in summon.rows('cortege_cheer_config.csv')}
SKILL = {int(r['level']): r for r in summon.rows('cheer_skill_config.csv')}
ATTRS = json.loads((ROOT / 'analysis/evidence/cheer/role_attributes.json').read_text())


def load_rules(path=ROOT / 'server_config/cheer_rules.json'):
    r = json.loads(path.read_text())
    f.require(r['mode'] == 'inferred' and type(r['is_open']) is bool, '八卦配置模式无效')
    f.require(type(r['is_open_ni']) is int and r['is_open_ni'] in (0, 1, 2), '逆八卦开关无效')
    f.require(len(r['cheer_level_limit']) == len(r['open_cheer_item']) == 16, '八卦需要十六位配置')
    for level, item in zip(r['cheer_level_limit'], r['open_cheer_item']):
        f.require(type(level) is int and 1 <= level <= 200, '八卦等级无效')
        f.require(item['type_id'] in f.ITEMS and type(item['count']) is int and item['count'] > 0, '开位材料无效')
    for key in ('cost_item_count', 'cost_gold_count', 'wash_step', 'skill_wash_max_step'):
        f.require(type(r[key]) is int and 0 < r[key] <= 1000, '八卦消耗或洗炼配置无效')
    f.require(type(r['skill_realm']) is int and 1 <= r['skill_realm'] <= 4, '法术境界无效')
    for item in r['materials_shop']:
        f.require(item['type_id'] in f.ITEMS and all(type(item[k]) is int and item[k] > 0 for k in ('count', 'price')), '八卦材料商店配置无效')
    return r


def client_config(r):
    return {k: r[k] for k in ('is_open', 'is_open_ni', 'cheer_level_limit', 'open_cheer_item', 'cost_item_count', 'cost_gold_count')}


def prepare(role, rules=None):
    role.setdefault('cheer_pending', {})
    for key in ATTRS:
        role.setdefault(key, 0)
    if role.get('cheer_skill_mask_version', 1) < 2:
        # [A] tianShuUI.getBitInGuideIndex discards bit zero before cheer UI indexes it.
        # [B] Migrate the former local zero-based encoding once, preserving bought slots.
        for key in ('cheer_skill_open', 'cheer_skill_ni_open'):
            role[key] = (role[key] & 0xffff) << 1
        role['cheer_skill_mask_version'] = 2
    if rules and rules['is_open']:
        for order in (1, 2):
            if role['level'] >= rules['cheer_level_limit'][order - 1]:
                key = 'cheer_' + NAMES[order - 1] + '_level'
                role[key] = max(1, role[key])
    for order, name in enumerate(NAMES, 1):
        effect_key = 'cheer_' + name + '_effect'
        if role[effect_key] and not any(c.get('order') == role[effect_key] for c in role['corteges']):
            role[effect_key] = 0
        level = role['cheer_' + name + '_level']
        for stat, column in zip(STATS, ('gongji_plus', 'fangyu_plus', 'maxhp_plus', 'maxmagic_plus')):
            # [B] Sum the original per-level increments, mirror positive CSV for reverse positions.
            base = sum((Decimal(ROWS[(order - 1) % 8 + 1, n][column]) for n in range(1, min(10, level) + 1)), Decimal(0))
            role[name + '_' + stat] = int(base * 1000)
            role[name + '_' + stat + '_plus'] = max(0, role[name + '_' + stat] + role.get('cheer_wash', {}).get(name, {}).get(stat, 0))
    role['cheer_count'] = sum(role['cheer_' + name + '_level'] > 0 for name in NAMES)


def attributes(role):
    fields = [dict(type=v, value=role.get(k, 0)) for k, v in ATTRS.items()]
    return [encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=len(part), attr_list=part))
            for i in range(0, len(fields), 100) if (part := fields[i:i + 100])]


def skill_mask(order, pos):
    return ('cheer_skill_open' if order <= 8 else 'cheer_skill_ni_open', 1 << (((order - 1) % 8) * 2 + pos - 1))


def skill_open(role, order, pos):
    key, bit = skill_mask(order, pos)
    return bool(role[key] & bit)


def settle(role, req, r):
    prepare(role, r)
    flag, order, identity, pos = (req[k] for k in ('flag', 'order', 'id', 'client_flag'))
    f.require(r['is_open'] and 1 <= order <= 16 and 1 <= flag <= 15, '八卦操作参数无效')
    f.require(role['level'] >= r['cheer_level_limit'][order - 1], '未达到八卦开启等级')
    f.require(order <= 8 or r['is_open_ni'] >= (1 if flag in (1, 2, 8, 12) else 2), '逆八卦功能未开启')
    name = NAMES[order - 1]
    level_key, effect_key = 'cheer_' + name + '_level', 'cheer_' + name + '_effect'
    skill_key = name + '_skill_level'
    result = dict(flag=flag, result=1, cheer_order=order, client_flag=pos)
    if flag == 8:
        f.require(role[level_key] == 0, '该八卦位已开启')
        if 4 <= order <= 8 or order >= 11:
            f.require(role['cheer_' + NAMES[order - 2] + '_level'] > 0, '请先开启前方阵位')
        if order > 8:
            # [A] Original canShowChangeBtn requires all eight positive positions.
            f.require(all(role['cheer_' + n + '_level'] > 0 for n in NAMES[:8]), '请先开启全部正八卦位')
            # [B] Enforce the original first-entry (order 9) flow on direct requests too.
            f.require(order == 9 or role['cheer_unheaven_level'] > 0, '请先开启逆·乾阵位')
        item = r['open_cheer_item'][order - 1]
        f.debit_item(role, item['type_id'], item['count'])
        role[level_key] = 1
    else:
        f.require(role[level_key] > 0, '八卦位尚未开启')
        if flag == 1:
            c = f.lookup(role, 'corteges', identity) if identity else None
            if c:
                f.require(not c.get('order') and c.get('cheer_order', 0) in (0, order), '该神仙已在阵中')
                f.require(not any(x['id'] != identity and x['type'] == c['type'] and (x.get('order') or x.get('cheer_order')) for x in role['corteges']), '阵中已有同名神仙')
            for x in role['corteges']:
                if x.get('cheer_order') == order:
                    x['cheer_order'] = 0
            if c:
                c['cheer_order'] = order
        elif flag == 2:
            c = f.lookup(role, 'corteges', identity) if identity else None
            f.require(c is None or 1 <= c.get('order', 0) <= 8, '加成目标必须为上阵神仙')
            role[effect_key] = c['order'] if c else 0
        elif flag == 3:
            f.require(role[level_key] < 10, '八卦位已满级')
            cost = int(ROWS[(order - 1) % 8 + 1, role[level_key] + 1]['upgrade_cost'])
            f.debit_item(role, 1015, cost)
            role[level_key] += 1
        elif flag in (4, 13):
            f.require(role[level_key] == 10, '八卦位满级后才可洗炼')
            if flag == 13:
                f.require(role.get('reborn_layer', 0) >= 4 and any(skill_open(role, order, p) for p in (2, 3)), '需境界四且开启法术位')
                f.require(role[skill_key] < 500, '法术位已满级')
            f.debit_item(role, 1015, r['cost_item_count'])
            f.debit_money(role, 'gold_coin', r['cost_gold_count'])
            if flag == 4:
                src = secrets.randbelow(4) + 1
                dst = secrets.choice([x for x in range(1, 5) if x != src])
                step = min(r['wash_step'], role[name + '_' + STATS[src - 1] + '_plus'])
                pending = dict(src_index=src, des_index=dst, modify_value=step, plus_level=0)
            else:
                cap = 500
                pending = dict(src_index=1, des_index=2, modify_value=0,
                               plus_level=min(cap - role[skill_key], secrets.randbelow(r['skill_wash_max_step']) + 1))
            role['cheer_pending'][str(order)] = pending
            result.update(pending)
        elif flag == 7:
            pending = role['cheer_pending'].get(str(order))
            result.update(pending or dict(result=2))
        elif flag in (5, 6, 14, 15):
            pending = role['cheer_pending'].get(str(order))
            f.require(pending is not None, '没有待处理的洗炼结果')
            f.require(bool(pending['plus_level']) == (flag in (14, 15)), '洗炼类型不匹配')
            if flag == 6:
                wash = role.setdefault('cheer_wash', {}).setdefault(name, {})
                for idx, sign in ((pending['src_index'], -1), (pending['des_index'], 1)):
                    stat = STATS[idx - 1]
                    wash[stat] = wash.get(stat, 0) + sign * pending['modify_value']
            if flag == 15:
                role[skill_key] += pending['plus_level']
            del role['cheer_pending'][str(order)]
        elif flag == 9:
            f.require(pos in (2, 3) and not skill_open(role, order, pos), '法术位参数无效或已开启')
            f.require(role.get('reborn_layer', 0) >= r['skill_realm'], '未达到助阵法术开启境界')
            f.debit_item(role, r['open_cheer_item'][order - 1]['type_id'], 1)
            key, bit = skill_mask(order, pos)
            role[key] |= bit
        elif flag == 10:
            cap = 500
            f.require(any(skill_open(role, order, p) for p in (2, 3)) and role[skill_key] < cap, '法术位未开启或已满级')
            f.require(str(order) not in role['cheer_pending'], '请先处理待确认洗炼')
            _, material, _, count = map(int, SKILL[role[skill_key]]['consume_list'].split('|'))
            f.debit_item(role, material, count)
            role[skill_key] += 1
        elif flag == 11:
            f.require(pos in (2, 3) and skill_open(role, order, pos), '法术位尚未开启')
            item = f.lookup(role, 'attachments', identity) if identity else None
            if item:
                cfg = f.SKILLS.get(item['type_id'], {})
                f.require(item['attach_type'] == 6 and int(cfg.get('use_mode(1-active，2-passive)', 0)) == 2 and not item.get('protogenic') and not item.get('equip_order'), '只能装备闲置被动法术')
                f.require(not any(i['type_id'] == item['type_id'] and i.get('equip_order') == order + 8 for i in role['attachments']), '不能装备同名法术')
            for i in role['attachments']:
                if i.get('equip_order') == order + 8 and i.get('equip_pos') == pos:
                    i.update(equip_order=0, equip_pos=0)
            if item:
                item.update(equip_order=order + 8, equip_pos=pos)
        elif flag == 12:
            c = f.lookup(role, 'corteges', identity)
            f.require(c.get('cheer_order') == order, '该神仙不在此助阵位')
            result['skill_id'] = next((i['id'] for i in role['attachments'] if i.get('innate_owner_id') == identity), 0)
    prepare(role)
    return [summon.event(95, result)]


def bonuses(role, c, values, pending):
    """[B] Explicit chosen target; positive and reverse support sum without feedback."""
    for order, name in enumerate(NAMES, 1):
        if (role.get('cheer_' + name + '_level', 0) <= 0
                or role.get('cheer_' + name + '_effect', 0) != c['order']):
            continue
        supporter = next((x for x in role['corteges'] if x.get('cheer_order') == order and not x.get('order')), None)
        if not supporter or supporter['id'] not in pending:
            continue
        for stat in STATS:
            values[stat] += pending[supporter['id']][stat] * Decimal(role.get(name + '_' + stat + '_plus', 0)) / 1000
        for item in role['attachments']:
            if item.get('equip_order') != order + 8 or item.get('equip_pos') not in (2, 3):
                continue
            if not skill_open(role, order, item['equip_pos']):
                continue
            cfg = f.SKILLS.get(item['type_id'], {})
            field = int(cfg.get('effect_field(1-gongji，2-fangyu，3-magic，4-intensity，5-hp)', 0))
            if field in (1, 2, 3, 5) and int(cfg.get('use_mode(1-active，2-passive)', 0)) == 2:
                stat = {1: 'gongji', 2: 'fangyu', 3: 'magic', 5: 'hp'}[field]
                rate = Decimal(SKILL[min(500, role.get(name + '_skill_level', 0))]['plus_rate'])
                values[stat] += pending[c['id']][stat] * Decimal(f.skill_effect(item)) / 100 * rate
                from .skill_insight import hp_percent
                values['hp'] += pending[c['id']]['hp'] * hp_percent(item) / 100 * rate


def market_goods(role):
    r = load_rules()
    if not r['is_open'] or role['level'] < r['cheer_level_limit'][0]:
        return {}
    names = {int(x['Ftype_id']): x['name'] for x in summon.rows('item_name.csv')}
    return {200 + n: dict(index=200+n, object_type=5, type_id=x['type_id'], count=x['count'],
                         name=names[x['type_id']], buy_price=x['price'], origin_price=x['price'],
                         money_type=11, vip_level=0, order=200+n, begin_time=0, end_time=0,
                         buy_limit_times=0, is_day_limit=0)
            for n,x in enumerate(r['materials_shop'],1)}


def inspection(role, own=True):
    import copy
    corts = {}
    if own:
        for c in role['corteges']:
            if c.get('cheer_order'):
                corts[c['cheer_order']] = dict(copy.deepcopy(c), type_id=c['type'])
    skills = [dict(copy.deepcopy(i), order=i['equip_order']) for i in role['attachments']
              if own and i['attach_type'] == 6 and i.get('equip_order',0)>8]
    return dict(owner_cheer_info={v:role.get(k,0) if own else 0 for k,v in ATTRS.items()},
                cheer_cortege=corts, skill_list=skills)
