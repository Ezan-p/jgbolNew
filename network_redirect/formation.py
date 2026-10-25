"""Formation settlement. Client facts [A] and inferred rules [B]: docs/阵容模块规则与调试.md.

All mutations operate on a detached role. Backend serializes every response before
committing; validation failures therefore cannot partially debit an inventory.
"""
from decimal import Decimal, ROUND_FLOOR
import csv
import json
from pathlib import Path
import secrets

from . import summon

ROOT = Path(__file__).resolve().parents[1]
BASES = summon.BASES
SKILLS = {int(r['type_id']): r for r in summon.rows('skill_base.csv')}
ITEMS = {int(r['type_id']): r for r in summon.rows('item_base.csv')}
LEVELS = {int(r['level']): r for r in summon.rows('role_level_config.csv')}
EXPERIENCE = {(int(r['quality']), int(r['level'])): int(r['experience'])
              for r in summon.rows('cortege_experience.csv')}
EVOLVE_COST = {int(r['level']): int(r['count']) for r in summon.rows('cortege_evolution.csv')}
EVOLVE_POINTS = {(int(r['cortege_quality']), int(r['level'])): int(r['culture_point'])
                 for r in summon.rows('cortege_evolve_config.csv')}
COMPOSE = {int(r['cortege_quality']): int(r['spirit_compose_count'])
           for r in summon.rows('cortege_quality.csv')}
EQUIP_COST = {int(r['level']): r for r in summon.rows('equip_enhance_cost.csv')}
EQUIP_WEIGHTS = {int(next(iter(r.values()))): int(r['random_weight'])
                 for r in summon.rows('equip_enhance_weight.csv')}
SKILL_COST = {int(r['skill_level']): r for r in summon.rows('skill_enhance_cost.csv')}
SKILL_WORTH = {int(r['skill_level']): r for r in summon.rows('skill_enhance_worth.csv')}
FATES = summon.rows('fate_config.csv')
ADVANCE_COST = {(int(r['equip_quality']), int(r['advance_level'])): r
                for r in summon.rows('equip_advance_cost.csv')}
STAR_COST = {(int(r['equip_quality']), int(r['star_level'])): list(r.values())[2:]
             for r in summon.rows('equip_star_cost.csv')}
# Repeated headers in this original CSV must be read positionally.
with (ROOT / 'analysis/configs/equip_advance_worth.csv').open(encoding='utf-8-sig', newline='') as source:
    ADVANCE_WORTH = {(int(r[1]), int(r[0])): r[2:] for r in list(csv.reader(source))[1:]}
STATS = ('hp', 'gongji', 'fangyu', 'magic')
BASE_COLUMNS = ('base_max_hp', 'base_gongji', 'base_fangyu', 'base_max_magic')
GROWTH_COLUMNS = ('base_maxhp_plus', 'base_gongji_plus', 'base_fangyu_plus', 'base_maxmagic_plus')
HANDLED = {1076, 1212, 1053, 1055, 1056, 1074, 1079, 1225, 1054, 1024, 1025, 1037, 1052, 1059, 1071, 1073, 1081, 1082, 1083, 1084, 1089, 1343}


class Rejected(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Rejected(message)


def load_rules(path=ROOT / 'server_config/formation_rules.json'):
    rules = json.loads(Path(path).read_text(encoding='utf-8'))
    if rules.get('schema_version') != 1 or rules.get('mode') != 'inferred':
        raise ValueError('阵容配置必须明确标记 inferred/schema_version=1')
    for key in ('culture_per_level', 'skill_failure_compensation', 'equipment_batch_count'):
        if type(rules.get(key)) is not int or not 1 <= rules[key] <= 100:
            raise ValueError('阵容配置无效：' + key)
    for key in ('ordinary_points', 'intensive_points', 'peaches_per_attempt', 'gold_per_intensive'):
        if type(rules.get('training', {}).get(key)) is not int or not 1 <= rules['training'][key] <= 100:
            raise ValueError('培养配置无效：' + key)
    values = rules.get('combat_weights', {})
    if not isinstance(values, dict) or set(values) != set(STATS) or any(
            type(v) not in (int, float) or not Decimal(str(v)).is_finite()
            or not 0 < v <= 100 for v in values.values()):
        raise ValueError('战力权重须为0到100之间的有限正数')
    values = rules.get('training', {}).get('stat_units', {})
    if set(values) != set(STATS) or any(type(v) is not int or not 1 <= v <= 100 for v in values.values()):
        raise ValueError('培养属性配置无效')
    if any(v != 1 for v in rules['training']['stat_units'].values()):
        raise ValueError('原版培养预览要求每点对应一点属性')
    advancement = rules.get('equipment_advance', {})
    if not (type(advancement.get('min_role_level')) is int and 1 <= advancement['min_role_level'] <= 200
            and type(advancement.get('pour_star_count')) is int and 1 <= advancement['pour_star_count'] <= 100
            and advancement.get('max_advance_level') == 10 and advancement.get('max_star_level') == 7
            and type(advancement.get('is_open')) is bool):
        raise ValueError('装备升阶配置无效')
    policy = rules.get('combat_power', {})
    if not isinstance(policy, dict) or set(policy) - {'title', 'pet', 'cheer', 'explicit_channels'} or any(type(v) is not bool for v in policy.values()):
        raise ValueError('战力来源开关必须是布尔值')
    policy = rules.get('attribute_policy', {})
    from .combat_power import ATTRIBUTE_STAGES
    require(policy.get('advance_extra_base') == 'pre_fate_panel'
            and policy.get('advance_extra_tiers') == 'highest_unlocked'
            and policy.get('stages') == ATTRIBUTE_STAGES
            and policy.get('rounding') == 'floor_before_collection_and_final', '属性乘区配置无效')
    return rules


def floor(value):
    return int(Decimal(value).to_integral_value(rounding=ROUND_FLOOR))


def lookup(role, key, identity):
    require(type(identity) in (int, float) and identity > 0 and identity == int(identity), '对象编号无效')
    result = next((x for x in role[key] if x['id'] == identity), None)
    require(result is not None, '神仙或物品不存在，请刷新后重试')
    return result


def new_id(role):
    # Shared allocator with summons; also usable before the first summon.
    role.setdefault('summon', {})
    return summon.next_id(role)


def skill_effect(item):
    cfg = SKILLS[item['type_id']]
    field = int(cfg['effect_field(1-gongji，2-fangyu，3-magic，4-intensity，5-hp)'])
    column = {1: 'gongji_plus', 2: 'fangyu_plus', 3: 'magic_plus', 4: 'intensity', 5: 'hp_plus'}[field]
    return floor(Decimal(cfg[column]) + Decimal(cfg['upgrade_plus']) * (item.get('level', 1) - 1))


def equip_effect(item):
    from . import equipment
    return equipment.effect(item)


def advance_worth(item):
    cfg = ITEMS[item['type_id']]
    advance, stars = item.get('advance_level', 0), item.get('star_count', 0)
    if not advance and not stars:
        return Decimal(0), Decimal(0), Decimal(0)
    row = ADVANCE_WORTH.get((int(cfg['quality']), int(cfg['main_type'])))
    require(row and 0 <= advance <= 10 and 0 <= stars <= 7 and advance * 8 + stars <= 80, '装备升阶状态无效')
    values = [Decimal(v) for v in row[advance * 8 + stars - 1].split('|')]
    # [B] The extra tier bonus remains active after pouring subsequent stars.
    extra = Decimal(0)
    for n in range(1, advance + 1):
        tier = row[n * 8 - 1].split('|')
        if len(tier) > 2:
            extra = max(extra, Decimal(tier[2]))
    return values[0], values[1], extra


def prepare(role, rules):
    """Idempotent migration: retain IDs, skill levels, resources and companion progress."""
    before = json.dumps(role, sort_keys=True)
    role.setdefault('attachments', [])
    if 'corteges' not in role:
        role.setdefault('summon', {})
        c = summon.companion(role, 5004)
        c['order'] = 1
        role['corteges'] = [c]
    level = min(max(1, role['level']), max(LEVELS))
    role['cortege_count'] = int(LEVELS[level]['cortege_count'])
    claimed = set()
    for c in role['corteges']:
        base = BASES.get(c['type'])
        if not base:
            continue  # Never rewrite an unknown historical companion.
        c.setdefault('culture_point', 0)
        c.setdefault('cur_exp', 0)
        c['next_exp'] = EXPERIENCE.get((int(base['quality']), c['level']), 0)
        c.setdefault('cheer_order', 0)
        for stat in STATS:
            c.setdefault(stat + '_plus', 0)
        innate = int(base['chushijineng'])
        if innate not in SKILLS:
            continue
        candidates = [i for i in role['attachments'] if i.get('attach_type') == 6 and i.get('protogenic') == 1
                      and i['id'] not in claimed and (i.get('innate_owner_id') == c['id'] or
                      (not i.get('innate_owner_id') and i.get('type_id') == innate and
                       (i.get('owner_id') == c['id'] or (c.get('order', 0) and i.get('equip_order') == c['order']))))]
        if candidates:
            item = candidates[0]
        else:
            item = dict(id=new_id(role), attach_type=6, type_id=innate, count=0,
                        level=int(SKILLS[innate]['begin_level']), protogenic=1)
            role['attachments'].append(item)
        claimed.add(item['id'])
        item.update(innate_owner_id=c['id'], owner_id=c['id'], equip_order=c.get('order', 0) or (c.get('cheer_order', 0) + 8 if c.get('cheer_order') else 0), equip_pos=1)
        item['effect_value'] = skill_effect(item)
    for item in role['attachments']:
        if item.get('attach_type') == 5 and int(ITEMS.get(item.get('type_id'), {}).get('main_type', 0)) in (1, 2, 3):
            item['effect_value'] = equip_effect(item)
    from . import cheer
    cheer.prepare(role)
    recalculate(role, rules)
    return before != json.dumps(role, sort_keys=True)


def recalculate(role, rules):
    from . import combat_power
    combat_power.recalculate(role, rules)


def change_order(role, req):
    changes = req['change_info']
    require(req['flag'] in (0, 4, 5) and 1 <= len(changes) <= 8 and len(changes) == req['count'], '阵容参数无效')
    require(len({x['id'] for x in changes}) == len(changes), '神仙重复')
    require(len({x['new_order'] for x in changes if x['new_order']}) == sum(bool(x['new_order']) for x in changes), '阵位重复')
    roster = role['corteges']
    old_orders = {c['id']: c.get('order', 0) for c in roster}
    for change in changes:
        c = lookup(role, 'corteges', change['id'])
        require(not c.get('cheer_order'), '助威中的神仙不能同时上阵')
        require(0 <= change['new_order'] <= min(8, role['cortege_count']), '阵位尚未开放')
    if req['flag'] == 4:
        require(len(changes) == 1 and changes[0]['new_order'] > 0, '更换神仙参数无效')
        target = changes[0]['new_order']
        incoming = lookup(role, 'corteges', changes[0]['id'])
        previous = incoming.get('order', 0)
        for c in roster:
            if c.get('order') == target:
                c['order'] = previous
        incoming['order'] = target
    else:
        requested = {x['id']: x['new_order'] for x in changes}
        final = [requested.get(c['id'], c.get('order', 0)) for c in roster]
        require(len([p for p in final if p]) == len(set(p for p in final if p)), '阵位被其它神仙占用')
        require(any(final), '至少保留一名上阵神仙')
        for c in roster:
            c['order'] = requested.get(c['id'], c.get('order', 0))
    new_orders = {c['id']: c.get('order', 0) for c in roster}
    moves = {old_orders[k]: new_orders[k] for k in old_orders if old_orders[k]}
    # [B] Replacement retains ordinary gear at the slot; rearranging carries it.
    for item in role['attachments']:
        if item.get('innate_owner_id'):
            item['equip_order'] = new_orders.get(item['innate_owner_id'], 0)
        elif req['flag'] != 4 and item.get('equip_order') in moves:
            item['equip_order'] = moves[item['equip_order']]
    return [(1, {'flag': req['flag']})]


def bind(role, req):
    item = lookup(role, 'attachments', req['src_id'])
    require(req['flag'] in (0, 3) and req['obj_type'] == item['attach_type'], '装备参数无效')
    require(not item.get('protogenic'), '自带法术不能卸下或转移')
    require(req['src_order'] == item.get('equip_order', 0), '装备位置已变化，请刷新后重试')
    order, pos = req['des_order'], req['des_equip_pos']
    if order:
        require(any(c.get('order') == order for c in role['corteges']), '目标阵位没有神仙')
        if item['attach_type'] == 6:
            require(pos in (2, 3), '自带法术槽不能替换')
            require(not any(i['id'] != item['id'] and i['attach_type'] == 6 and i.get('equip_order') == order
                            and i['type_id'] == item['type_id'] for i in role['attachments']), '不能装备重复法术')
        else:
            cfg = ITEMS.get(item['type_id'], {})
            require(item['attach_type'] == 5 and int(cfg.get('main_type', 0)) in (1, 2, 3)
                    and pos == int(cfg['equip_pos']), '物品与装备槽不匹配')
        for other in role['attachments']:
            if other['id'] != item['id'] and other['attach_type'] == item['attach_type'] and other.get('equip_order') == order and other.get('equip_pos') == pos:
                require(not other.get('protogenic'), '不能替换自带法术')
                other['equip_order'], other['equip_pos'] = 0, 0
    item['equip_order'], item['equip_pos'] = order, pos if order else 0
    return [(1, {'flag': req['flag']})]


def debit_item(role, type_id, count):
    require(type(count) is int and count > 0, '物品数量无效')
    stacks = [i for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] == type_id and not i.get('is_lock')]
    require(sum(i['count'] for i in stacks) >= count, '材料不足')
    for item in stacks:
        used = min(count, item['count'])
        item['count'] -= used
        count -= used
    role['attachments'] = [i for i in role['attachments'] if i['attach_type'] == 6 or i['count'] > 0]


def debit_money(role, currency, amount):
    require(role.get(currency, 0) >= amount, '银币不足' if currency == 'silver_coin' else '元宝不足')
    role[currency] -= amount


def enhance_equipment(role, req, rules):
    item = lookup(role, 'attachments', req['equip_id'])
    cfg = ITEMS.get(item['type_id'], {})
    require(item['attach_type'] == 5 and int(cfg.get('main_type', 0)) in (1, 2, 3), '只能强化装备')
    require(req['equip_order'] == item.get('equip_order', 0), '装备位置已变化')
    require(not req['inbatch'] or role.get('vip_level', 0) >= 3, 'VIP3开放批量强化')
    top = min(int(cfg['top_level']), role['level'] * 2)  # [A] equipmentUpgradeUI:873.
    steps = rules['equipment_batch_count'] if req['inbatch'] else 1
    result = []
    for _ in range(steps):
        old = item.get('level', 1)
        if old >= top or old not in EQUIP_COST:
            break
        cost = int(EQUIP_COST[old]['star%d_money' % int(cfg['quality'])])
        if role.get('silver_coin', 0) < cost:
            break
        debit_money(role, 'silver_coin', cost)
        item['level'] = min(top, old + summon.weighted_choice(EQUIP_WEIGHTS))
        item['effect_value'] = equip_effect(item)
        result.append(dict(old_level=old, new_level=item['level'], equip_id=item['id'], effect_value=item['effect_value']))
    require(result, '装备已达等级上限或银币不足')
    return [(2, dict(obj_type=5, obj_id=item['id'], upgrade_list=result))]


def enhance_skill(role, req, rules, parse):
    data = parse(req['data'])
    require(isinstance(data, dict), '法术升级数据无效')
    item = lookup(role, 'attachments', data.get('des_skill_id', 0))
    require(item['attach_type'] == 6 and item['type_id'] in SKILLS, '目标不是法术')
    ids = data.get('src_skill_list', {})
    if isinstance(ids, dict):
        require(set(ids) == set(range(1, len(ids) + 1)), '材料列表无效')
        ids = list(ids.values())
    require(isinstance(ids, list) and 1 <= len(ids) <= 500 and len(set(ids)) == len(ids), '材料列表无效或重复')
    cfg, old = SKILLS[item['type_id']], item['level']
    require(old < int(cfg['top_level']) and old in SKILL_COST, '法术已达等级上限')
    worth = Decimal(0)
    for identity in ids:
        material = lookup(role, 'attachments', identity)
        require(material['id'] != item['id'] and material['attach_type'] == 6 and not material.get('protogenic')
                and not material.get('equip_order') and not material.get('owner_id') and not material.get('is_lock')
                and not material.get('upgrade_level') and not material.get('awaken'), '已装备、自带或锁定法术不能作为材料')
        quality = int(SKILLS[material['type_id']]['quality'])
        require(material['level'] in SKILL_WORTH, '材料法术等级无效')
        worth += Decimal(SKILL_WORTH[material['level']]['quality_worth%d' % quality].strip())
    cost = Decimal(SKILL_COST[old]['quality%d_cost' % int(cfg['quality'])])
    rate = min(100, floor(worth * 100 / cost) + item.get('count', 0))
    success = secrets.randbelow(100) < rate
    role['attachments'] = [i for i in role['attachments'] if i['id'] not in ids]
    item['level'] += int(success)
    item['count'] = 0 if success else min(100, item.get('count', 0) + rules['skill_failure_compensation'])
    item['effect_value'] = skill_effect(item)
    return [(2, dict(obj_type=6, obj_id=item['id'], old_level=old, new_level=item['level']))]


def advance_equipment(role, req, rules):
    config = rules['equipment_advance']
    require(config['is_open'] and role['level'] >= config['min_role_level'], '尚未达到装备注灵等级')
    item = lookup(role, 'attachments', req['equip_id'])
    cfg = ITEMS.get(item['type_id'], {})
    kind, quality = int(cfg.get('main_type', 0)), int(cfg.get('quality', 0))
    require(item['attach_type'] == 5 and kind in (1, 2, 3) and quality in (4, 5), '只有四星、五星装备能注灵升阶')
    require(req['equip_order'] == item.get('equip_order', 0) and req['flag'] in (1, 2), '装备升阶参数无效')
    advance, stars = item.get('advance_level', 0), item.get('star_count', 0)
    require(advance < config['max_advance_level'], '装备已达最高阶')
    if req['flag'] == 1:
        require(stars < config['max_star_level'], '请先升阶')
        needed = int(STAR_COST[quality, stars + 1][advance].split('|')[kind - 1])
        current = item.get('cur_spirit_count', 0)
        require(0 <= current < needed, '注灵进度无效')
        # [B] One material grants one progress; one-key fills the next star.
        count = needed - current if req['is_one_key'] else min(config['pour_star_count'], needed - current)
        debit_item(role, {1: 1310, 2: 1311, 3: 1312}[kind], count)
        current += count
        item['star_count'] = stars + int(current == needed)
        item['cur_spirit_count'] = 0 if current == needed else current
    else:
        require(stars == config['max_star_level'], '需要注满七星才能升阶')
        costs = ADVANCE_COST[quality, advance + 1][{1: 'wuqi_cost', 2: 'fangyu_cost', 3: 'fabao_cost'}[kind]]
        for entry in costs.split('/'):
            type_id, count = map(int, entry.split('|'))
            debit_item(role, type_id, count)
        item.update(advance_level=advance + 1, star_count=0, cur_spirit_count=0)
    item['effect_value'] = equip_effect(item)
    return [(115, dict(flag=req['flag'], result=1, equip_id=item['id']))]


def training(role, mid, req, rules):
    c = lookup(role, 'corteges', req['cortege_id'])
    require(role['level'] >= 5, '角色5级开放培养')
    cfg = rules['training']
    pending = c.get('pending_training')
    if mid == 1082:
        require(pending is not None, '没有待确认的培养结果')
        if req['confirm']:
            require(c['culture_point'] >= pending['points'], '潜力不足')
            for stat, delta in pending['deltas'].items():
                c[stat + '_plus'] += delta
            c['culture_point'] -= pending['points']
        del c['pending_training']
        c.update(train_increase_field=0, train_decrease_field=0, train_change_value=0)
        return [(4, dict(cortege_id=c['id'], train_result=2 if req['confirm'] else 3))]
    require(not pending, '请先保存或放弃上次培养结果')
    # Original trainingUI.createStartTrainingInfo:598-603 disables the
    # training button at companion level 1, even with evolution potential.
    require(c['level'] > 1, '神仙升至2级后才能培养')
    require(req['train_type'] in (1, 2), '培养类型无效')
    attempts = 10 if req['train_type'] == 2 else 1
    points = attempts * cfg['intensive_points' if req['intensive'] else 'ordinary_points']
    require(c['culture_point'] >= points, '潜力不足')
    debit_item(role, 1001, attempts * cfg['peaches_per_attempt'])
    if req['intensive']:
        debit_money(role, 'gold_coin', attempts * cfg['gold_per_intensive'])
    # [B] Uniformly select an attribute; conserve potential until confirmation.
    stat = secrets.choice(STATS)
    deltas = {s: (points * cfg['stat_units'][s] if s == stat else 0) for s in STATS}
    c['pending_training'] = dict(points=points, deltas=deltas)
    field = {'hp': 86, 'magic': 87, 'gongji': 88, 'fangyu': 89}[stat]
    c.update(train_increase_field=field, train_decrease_field=90, train_change_value=points)
    return [(4, dict(cortege_id=c['id'], train_result=1, increase_field=field, decrease_field=90, train_point=points))]


def compose(role, req):
    t = req['type_id']
    require(t in BASES, '未知神仙')
    require(not any(c['type'] == t for c in role['corteges']), '已拥有该神仙')
    count = COMPOSE[int(BASES[t]['quality'])]
    souls = role.setdefault('souls', {})
    require(souls.get(str(t), 0) >= count, '魂魄不足')
    souls[str(t)] -= count
    role['corteges'].append(summon.companion(role, t))
    return [(26, dict(type_id=t, cortege_type=t))]


def evolve(role, req):
    require(req['flag'] in (0, 1), '飞升参数无效')
    c = lookup(role, 'corteges', req['cortege_id'])
    quality = int(BASES[c['type']]['quality'])
    require(not c.get('pending_training'), '请先处理待确认的培养结果')
    if req['flag'] == 1:
        level = c.get('evolve_level', 0)
        cfg = next((r for r in summon.rows('cortege_devolve.csv') if int(r['evolve_level']) == level), None)
        require(cfg and quality in (4, 5), '该神仙不能回收飞升')
        refund = next((int(k) for k, r in ITEMS.items() if int(r['main_type']) == 11
                       and int(r['quality']) == quality and int(r['sub_type']) == int(BASES[c['type']]['category'])), None)
        require(refund, '缺少对应界魂配置')
        for entry in cfg['consume_item_list(object|type|level|count/..)'].split('/'):
            kind, type_id, _, count = map(int, entry.split('|'))
            require(kind == 5, '回收材料类型无效')
            debit_item(role, type_id, count)
        gained = int(cfg['jiehun_count'])
        summon.add_item(role, refund, gained)
        # [B] Undo evolution potential before allowing it to be earned again.
        total = c['culture_point'] + sum(c.get(s + '_plus', 0) for s in STATS)
        points = sum(EVOLVE_POINTS[quality, n] for n in range(1, level + 1))
        c['culture_point'] = max(0, total - points)
        for s in STATS:
            c[s + '_plus'] = 0
        c['evolve_level'] = 0
        return [(123, dict(attach_list=[dict(object_type=5, attach_type=refund, attach_count=gained, attach_level=1)]))]
    level = c.get('evolve_level', 0) + 1
    require(level in EVOLVE_COST and (quality, level) in EVOLVE_POINTS, '已达飞升上限')
    souls = role.setdefault('souls', {})
    require(souls.get(str(c['type']), 0) >= EVOLVE_COST[level], '飞升魂魄不足')
    souls[str(c['type'])] -= EVOLVE_COST[level]
    c['evolve_level'] = level
    c['culture_point'] += EVOLVE_POINTS[quality, level]
    return [(50, dict(cortege_id=c['id'], evolve_level=level))]


def feed(role, req, rules):
    require(req['flag'] in (1, 2) and req['first_send'], '经验物品请求无效')
    require(req['flag'] != 2 or role['level'] >= 65, '角色65级开放经验丹')
    c = lookup(role, 'corteges', req['cortege_id'])
    rolls = req['roll_list']
    require(rolls and len(rolls) == req['roll_count'] and len({r['type_id'] for r in rolls}) == len(rolls), '经验书列表无效')
    quality = int(BASES[c['type']]['quality'])
    top = min(max(l for q, l in EXPERIENCE if q == quality), 200 + role.get('cortege_limit_plus', 0))
    if role['level'] < 80:
        top = min(top, role['level'] * 3)
    require(c['level'] < top, '神仙已达当前等级上限')
    gain = 0
    for r in rolls:
        cfg = ITEMS.get(r['type_id'], {})
        require(int(cfg.get('experience_plus', 0)) > 0
                and int(cfg.get('sub_type', 0)) == {1: 99, 2: 100}[req['flag']], '经验物品与页面不匹配')
        debit_item(role, r['type_id'], r['count'])
        gain += int(cfg['experience_plus']) * r['count']
    remaining = Decimal(gain)
    applied = Decimal(0)
    while remaining > 0 and c['level'] < top:
        rate = Decimal('0.2') if role['level'] < 80 and c['level'] >= floor(Decimal(role['level']) * Decimal('2.5')) else Decimal(1)
        needed = Decimal(EXPERIENCE[quality, c['level']]) - Decimal(str(c['cur_exp']))
        cost = needed / rate
        if remaining < cost:
            applied += remaining * rate
            c['cur_exp'] += float(remaining * rate)
            break
        applied += needed
        remaining -= cost
        c['cur_exp'] = 0
        c['level'] += 1
        c['culture_point'] += rules['culture_per_level']
    c['next_exp'] = EXPERIENCE.get((quality, c['level']), 0)
    return [(65, dict(flag=req['flag'], cortege_id=c['id'], experience=float(applied)))]


def direct_training(role, req):
    c = lookup(role, 'corteges', req['cortege_id'])
    points, field = req['train_point'], req['train_field']
    require(role['level'] >= 5 and c['level'] > 1, '尚未达到定向培养等级')
    require(not c.get('pending_training'), '请先处理待确认的培养结果')
    require(field in (1, 2, 3, 4) and 0 < points <= c['culture_point'] and points % 5 == 0, '定向培养点数无效')
    debit_item(role, 1343, points // 5)
    c[STATS[field - 1] + '_plus'] += points
    c['culture_point'] -= points
    return [(176, dict(cortege_id=c['id'], train_field=field, train_point=points))]


def impart(role, req, rules):
    src = lookup(role, 'corteges', req['src_id'])
    dst = lookup(role, 'corteges', req['des_id'])
    require(src['id'] != dst['id'] and (src['level'] > 1 or src['cur_exp'] > 0), '传承对象无效')
    require(dst['level'] < min(200, role['level'] * 2), '接收神仙已达传承等级限制')
    require(not src.get('pending_training') and not dst.get('pending_training'), '请先处理待确认的培养结果')
    # [A] inheritUI computes target experience + all source accumulated XP.
    debit_item(role, 1002, 1)
    q1, q2 = int(BASES[src['type']]['quality']), int(BASES[dst['type']]['quality'])
    total = src['cur_exp'] + sum(EXPERIENCE[q1, n] for n in range(1, src['level']))
    dst['cur_exp'] += total
    while dst['level'] < 200 and dst['cur_exp'] >= EXPERIENCE[q2, dst['level']]:
        dst['cur_exp'] -= EXPERIENCE[q2, dst['level']]
        dst['level'] += 1
        dst['culture_point'] += rules['culture_per_level']
    if dst['level'] == 200:
        dst['cur_exp'] = 0
    # [B] Reset the donor, retain its identity, formation and innate skill.
    # Returning trained potential as peaches is visible in inheritUI:1094-1105.
    trained = sum(src.get(s + '_plus', 0) for s in STATS)
    if trained:
        summon.add_item(role, 1001, trained)
    src.update(level=1, cur_exp=0, culture_point=sum(EVOLVE_POINTS[q1, n] for n in range(1, src.get('evolve_level', 0) + 1)))
    for s in STATS:
        src[s + '_plus'] = 0
    return [(8, dict(src_id=src['id'], des_id=dst['id']))]


def settle(role, mid, req, rules, parse):
    if mid == 1024:
        result = change_order(role, req)
    elif mid == 1025:
        result = impart(role, req, rules)
    elif mid == 1037:
        result = bind(role, req)
    elif mid == 1052:
        result = enhance_equipment(role, req, rules)
    elif mid in (1053, 1055, 1056, 1074, 1079, 1225):
        from . import equipment_crafting
        result = equipment_crafting.settle(role, mid, req, parse)
    elif mid == 1054:
        from . import equipment
        result = equipment.settle(role, req)
    elif mid == 1071:
        result = enhance_skill(role, req, rules, parse)
    elif mid in (1076, 1212):
        from . import skill_insight
        result = skill_insight.insight(role, req) if mid == 1076 else skill_insight.convert(role, req)
    elif mid == 1073:
        result = advance_equipment(role, req, rules)
    elif mid in (1081, 1082):
        result = training(role, mid, req, rules)
    elif mid == 1089:
        result = direct_training(role, req)
    elif mid == 1083:
        result = compose(role, req)
    elif mid == 1084:
        result = evolve(role, req)
    elif mid == 1059:
        result = feed(role, req, rules)
    elif mid == 1343:
        item = lookup(role, 'attachments', req['des_id'])
        require(req['flag'] in (1, 2), '锁定参数无效')
        item['is_lock'] = 1 if req['flag'] == 1 else 0
        result = [(193, dict(des_id=item['id'], id=item['id'], flag=req['flag'], is_lock=item['is_lock']))]
    else:
        raise Rejected('阵容操作尚未实现')
    prepare(role, rules)
    return [summon.event(event, payload) for event, payload in result]
