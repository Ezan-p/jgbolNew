"""Original wakeUI/CSV contracts; configurable local server decisions [B]."""
import secrets
import time
from decimal import Decimal
from . import formation as f, summon, reborn as r

STARS = {int(x['ext_skill_type']): x for x in summon.rows('ext_star_config.csv')}
POSITIONS = {int(x['star_pos']): x for x in summon.rows('star_config.csv')}
RELATIONS = summon.rows('star_relation_config.csv')
OPEN = {int(x['element']): int(x['cortege_reborn']) for x in summon.rows('star_element_open.csv')}
EXP = {int(x['quality']): list(map(int, x['level1_up_exp'].split('|'))) for x in summon.rows('star_level_exp.csv')}
DECOMPOSE = {(int(x['quality']), int(x['level'])): x for x in summon.rows('star_decompose_config.csv')}
ELEMENT_RELATIONS = summon.rows('star_element_relation.csv')
AWAKEN = {int(next(iter(x.values()))): x for x in summon.rows('awaken_skill_conf.csv')}


def star(role, ident):
    x = f.lookup(role, 'attachments', ident)
    f.require(x['attach_type'] == 5 and x['type_id'] in STARS, '命星不存在')
    return x


def grant(role, t, n=1, level=1):
    if t in STARS:
        # Stars carry individual levels, locks and ownership. Never merge them.
        for _ in range(n):
            role['attachments'].append(dict(id=f.new_id(role), attach_type=5, type_id=t,
                count=1, level=level, owner_id=0, ext_awaken_pos=0, prob_compen=0))
    else:
        summon.add_item(role, t, n)


def divination(role, req, rules, parse, now=None):
    f.require(role['level'] >= rules['divination_min_level'], '占星尚未开放')
    now = time.time() if now is None else now
    day = int((now + 8 * 3600) // 86400)
    state = role.setdefault('divination', dict(day=day, divi_count=rules['daily_divinations'],
              buy_count=rules['buy_limit'], cur_pos=1, star_list=[], has_half=True))
    if state['day'] != day:
        state.update(day=day, divi_count=rules['daily_divinations'], buy_count=rules['buy_limit'], has_half=True)
    op = req['event_type']
    f.require(op in range(1, 7), '占星操作无效')
    data = parse(req['data'])
    prizes = []
    if op in (2, 3):
        f.require(state['divi_count'] > 0, '占星次数不足')
        available = rules['pending_limit'] - len(state['star_list'])
        f.require(available > 0, '请先领取命星')
        count = 1 if op == 2 else min(available, state['divi_count'])
        for _ in range(count):
            row = POSITIONS[state['cur_pos']]
            cost = int(row['consume_silver'])
            if op == 3 and role['silver_coin'] < cost and prizes:
                break
            f.debit_money(role, 'silver_coin', cost)
            weights = [list(map(int, x.split('|'))) for x in list(row.values())[2].split('/')]
            selected = weights[summon.weighted_choice({i:x[0] for i,x in enumerate(weights)})]
            _, kind, t, n, level = selected
            p = r.prize(t, n, level)
            state['star_list'].append(p)
            prizes.append(p)
            children = {int(x['star_pos_b']): int(x['switch_weight']) for x in RELATIONS if int(x['star_pos_a']) == state['cur_pos']}
            state['cur_pos'] = summon.weighted_choice(children) if children and secrets.randbelow(100) < rules['divination_advance_percent'] else 1
            state['divi_count'] -= 1
    elif op == 4:
        state['cur_pos'] = 1
    elif op == 5:
        f.require(state['star_list'], '没有可领取的命星')
        f.require(sum(x['count'] for x in role['attachments'] if x['type_id'] in STARS and not x.get('owner_id')) + sum(x['attach_count'] for x in state['star_list']) <= 200, '命星背包已满')
        for p in state['star_list']:
            grant(role, p['attach_type'], p['attach_count'], p['attach_level'])
        state['star_list'] = []
    elif op == 6:
        count = data.get('count')
        f.require(type(count) is int and count > 0 and count % 10 == 0 and count <= state['buy_count'], '购买次数无效')
        cost = count * rules['buy_cost'] // (2 if state['has_half'] else 1)
        f.debit_money(role, 'gold_coin', cost)
        state['buy_count'] -= count
        state['divi_count'] += count
        state['has_half'] = False
    return [summon.event(190, dict(state, result=1, event_type=op, buy_cost=rules['buy_cost'], max_count=200, prize_list=prizes))]


def settle(role, mid, req, rules, parse):
    if mid == 1337:
        return divination(role, req, rules, parse)
    if mid in (1332, 1342):
        return awaken(role, mid, req, rules)
    if mid in (1338, 1339):
        c = f.lookup(role, 'corteges', req['des_cortege_id'])
        element = req['element_id']
        f.require(element in OPEN and c.get('reborn_layer', 0) >= OPEN[element], '命星位置尚未开放')
        innate = next((x for x in role['attachments'] if x.get('innate_owner_id') == c['id']), {})
        f.require(innate.get('awaken', 0) > 0, '天赋法术须先觉醒')
        old = next((x for x in role['attachments'] if x['type_id'] in STARS and x.get('owner_id') == c['id'] and x.get('ext_awaken_pos') == element), None)
        if mid == 1339:
            f.require(old is not None, '该位置没有命星')
            old.update(owner_id=0, ext_awaken_pos=0)
        else:
            item = star(role, req['ext_star_id'])
            f.require(not item.get('owner_id') and req['replace'] in (0, 1), '命星已装备或替换参数无效')
            f.require(not old or req['replace'] == 1, '该位置已有命星')
            f.require(not any(x['type_id'] in STARS and x.get('owner_id') == c['id'] and x.get('ext_awaken_pos') != element and x['type_id'] % 1000 == item['type_id'] % 1000 for x in role['attachments']), '不能装备同类型命星')
            if old:
                old.update(owner_id=0, ext_awaken_pos=0)
            # A stack from a historical save is split before equipping.
            if item['count'] > 1:
                extra = dict(item, id=f.new_id(role), count=item['count'] - 1)
                role['attachments'].append(extra)
                item['count'] = 1
            item.update(owner_id=c['id'], ext_awaken_pos=element)
        return [summon.event((192 if req['replace'] else 186) if mid == 1338 else 187, dict(result=1))]
    if mid == 1340:
        item = star(role, req['ext_star_id'])
        f.require(item['level'] < 10 and item['count'] == 1, '命星已满级或需先拆分堆叠')
        need = EXP[int(f.ITEMS[item['type_id']]['quality'])][item['level'] - 1]
        n = req['cost_count']
        f.require(type(n) is int and 0 < n <= need - item.get('prob_compen', 0), '星尘数量无效')
        f.debit_item(role, 10300, n)
        item['prob_compen'] = item.get('prob_compen', 0) + n
        if item['prob_compen'] == need:
            item['level'] += 1
            item['prob_compen'] = 0
        return [summon.event(188, dict(result=1))]
    f.require(mid == 1341, '命星操作无效')
    ids = [x['id'] for x in req['star_list']]
    f.require(len(ids) == req['count'] and 0 < len(ids) <= 255 and len(set(ids)) == len(ids), '分解列表无效')
    dust, returned = 0, []
    for ident in ids:
        item = star(role, ident)
        f.require(not item.get('owner_id') and not item.get('is_lock'), '已装备或锁定命星不可分解')
        row = DECOMPOSE[int(f.ITEMS[item['type_id']]['quality']), item['level']]
        dust += (int(row['count']) + item.get('prob_compen', 0) * 4 // 5) * item['count']
        if int(row['output']):
            returned.append(r.prize(item['type_id'], item['count']))
    role['attachments'] = [x for x in role['attachments'] if x['id'] not in ids]
    grant(role, 10300, dust)
    for p in returned:
        grant(role, p['attach_type'], p['attach_count'])
    return [summon.event(189, dict(result=1, prize_list=[r.prize(10300, dust)] + returned))]


def awaken(role, mid, req, rules):
    item = f.lookup(role, 'attachments', req['des_id'])
    f.require(item['attach_type'] == 6 and item.get('protogenic') == 1, '只能觉醒天赋法术')
    c = f.lookup(role, 'corteges', item.get('innate_owner_id'))
    f.require(c.get('reborn_layer', 0) > 0, '神仙须先转生')
    if mid == 1342:
        f.require(item.get('awaken', 0) in AWAKEN, '法术尚未觉醒')
        f.debit_money(role, 'gold_coin', rules['restore_gold'])
        for x in role['attachments']:
            if x['type_id'] in STARS and x.get('owner_id') == c['id']:
                x.update(owner_id=0, ext_awaken_pos=0)
        for material in item.pop('awaken_materials', []):
            material['id'] = f.new_id(role)
            role['attachments'].append(material)
        item['awaken'] = 0
        return [summon.event(191, dict(result=1))]
    kind = req['awaken_type']
    f.require(kind in AWAKEN and not item.get('awaken', 0), '觉醒类型无效或已觉醒')
    row = AWAKEN[kind]
    f.require(item['level'] >= int(list(row.values())[1]), '天赋法术等级不足')
    ids = [x['id'] for x in req['material_list']]
    f.require(req['material_count'] == len(ids) == 2 and len(set(ids)) == 2 and item['id'] not in ids, '觉醒材料无效')
    materials = [f.lookup(role, 'attachments', i) for i in ids]
    required = sorted(int(x.split('|')[1]) for x in list(row.values())[2].split('/'))
    f.require(sorted(x['type_id'] for x in materials) == required, '觉醒法术种类不符')
    f.require(all(x['attach_type'] == 6 and not x.get('protogenic') and not x.get('equip_order') and not x.get('owner_id') and not x.get('is_lock') for x in materials), '觉醒材料不可使用')
    item['awaken_materials'] = materials
    role['attachments'] = [x for x in role['attachments'] if x['id'] not in ids]
    item['awaken'] = kind
    return [summon.event(183, dict(result=0))]


def bonuses(role, c, values):
    innate = next((x for x in role['attachments'] if x.get('innate_owner_id') == c['id']), {})
    kind = innate.get('awaken', 0)
    if kind in AWAKEN:
        values[{1:'gongji', 2:'fangyu', 3:'magic'}[kind]] += int(AWAKEN[kind]['plus_value'])
    equipped = [x for x in role['attachments'] if x['type_id'] in STARS and x.get('owner_id') == c['id']]
    elements = {x.get('ext_awaken_pos') for x in equipped}
    for row in ELEMENT_RELATIONS:
        if {int(row['element_a']), int(row['element_b'])} <= elements:
            for stat, value in r.stat_pairs(list(row.values())[3]):
                values[r.STAT[int(stat)]] += value
    for item in equipped:
        row = STARS.get(item['type_id'])
        if not row or item.get('owner_id') != c['id'] or list(row.values())[1] != 'LINEUP':
            continue
        stat, rate, value = map(Decimal, list(row.values())[5].split('/')[item['level'] - 1].split('|'))
        if int(stat) == 10:
            # Skill-strength modifiers belong to battle, not the four base stats.
            continue
        s = r.STAT[int(stat)]
        values[s] = values[s] * (1 + rate / 100) + value


def combat_traits(role, c):
    """[A] CSV coefficients; [B] composition in the local battle simulator."""
    traits = dict(spell_rate=0., spell_flat=0., crit=0., crit_damage=0.,
                  resist=0., reduction=0., survival=0., survival_count=0)
    for item in role['attachments']:
        row = STARS.get(item['type_id'])
        if not row or item.get('owner_id') != c['id']:
            continue
        values = list(map(float, list(row.values())[5].split('/')[item['level'] - 1].split('|')))
        kind = item['type_id'] % 1000
        if kind in (309, 310):
            traits['spell_rate'] += values[1]
            traits['spell_flat'] += values[2]
        elif kind in (311, 312, 313, 314):
            traits[{311:'crit',312:'crit_damage',313:'resist',314:'reduction'}[kind]] += values[0]
        elif kind == 315:
            traits['survival'] += values[0]
            traits['survival_count'] += int(values[1])
    traits['awake_skills'] = {x['type_id']: int(row['plus_rate(整数>0)'])
        for x in role['attachments'] if x.get('innate_owner_id') == c['id'] and x.get('awaken')
        for row in summon.rows('awaken_skill_rate.csv') if int(row['skill_type']) == x['type_id']}
    return traits


def spell_power(base, skill_id, traits):
    return int(base * (1 + traits.get('awake_skills', {}).get(skill_id, 0) / 100)
               * (1 + traits.get('spell_rate', 0) / 100) + traits.get('spell_flat', 0))


def combat_hit(hit, hp, normal, attack, defend):
    # [B] Base critical damage is 150%; rates from ext_star_config are percent.
    if normal and attack.get('crit', 0) > defend.get('resist', 0) and secrets.randbelow(1000000) < max(0, attack.get('crit', 0) - defend.get('resist', 0)) * 10000:
        hit = int(hit * max(1, (150 + attack.get('crit_damage', 0) - defend.get('reduction', 0)) / 100))
    if hit >= hp and defend.get('survival_count', 0) and secrets.randbelow(1000000) < defend.get('survival', 0) * 10000:
        defend['survival_count'] -= 1
        hit = hp - 1
    return min(hit, hp, 2147483647)


def attach_combat_traits(role, units):
    for unit in units:
        c = next((c for c in role.get('corteges', []) if c.get('order') == unit['order'] and c['type'] == unit['type']), None)
        if c:
            unit['reborn_traits'] = combat_traits(role, c)
