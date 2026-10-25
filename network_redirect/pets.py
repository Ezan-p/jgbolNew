"""Independent animal UI: recovered client contracts [A], server policy [B]."""
import json
import secrets
from decimal import Decimal
from pathlib import Path
from . import activity as a, activity_home as h, activity_home_pets as hp, summon


def table(name):
    return [{k.split('(')[0]: v for k, v in r.items()} for r in summon.rows(name + '.csv')]


CONTROL = {(int(r['main_type']), int(r['quality'])): r for r in table('animal_control')}
EXP = {(int(r['main_type']), int(r['level'])): int(r['exp']) for r in table('animal_upgrade')}
VALUES = {(int(r['main_type']), int(r['quality'])): r for r in table('animal_exprience')}
SPECIAL_EXP = {(int(r['type_id']), int(r['quality'])): int(r['base_exp']) for r in table('animal_pet_exp')}
STAR = {int(r['star_level']): r for r in table('animal_train_config')}
GROW = {int(r['index']): [tuple(map(int, p.split('|'))) for p in r['grow_list'].split('/')] for r in table('animal_growup')}
RULES_PATH = Path(__file__).resolve().parents[1] / 'server_config/pet_rules.json'


def load_rules(path=RULES_PATH):
    r = json.loads(Path(path).read_text())
    a.require(r.get('mode') == 'inferred' and r.get('schema_version') == 1, '宠物配置须标记 inferred')
    a.require(r.get('min_train_quality') == 3, '宠物培养品质须与原版星级表一致')
    a.require(type(r.get('upgrade_exp_rate')) in (int, float) and 0 <= r['upgrade_exp_rate'] <= 1, '经验继承率无效')
    a.require(r.get('plus_rate_list') == [0.4, 0.3, 0.7, 0.2], '宠物属性系数须与客户端默认值一致')
    a.require(type(r.get('capacity')) is int and 10 <= r['capacity'] <= 120, '宠物容量无效')
    a.require(r.get('starter_type') in hp.BASE and r.get('starter_quality') in (1, 2, 3, 4), '初始宠物配置无效')
    return r


def growth_range(tid, stat, quality):
    base = int(hp.BASE[tid]['base_'+stat])
    return next(row[quality-1] for row in GROW.values() if row[0][0] <= base <= row[0][1])


def add(home, tid, quality, r=None):
    r = r or load_rules()
    a.require(tid in hp.BASE and (int(hp.BASE[tid]['main_type']), quality) in CONTROL, '灵兽类型或品质无效')
    rows = home.setdefault('pets', [])
    a.require(len(rows) < r['capacity'], '宠物背包已满')
    identity = max(home.get('next_pet_id', 1), max((p['id'] for p in rows), default=0) + 1)
    home['next_pet_id'] = identity + 1
    base = hp.BASE[tid]
    pet = dict(id=identity, type_id=tid, main_type=int(base['main_type']), quality=quality,
               level=1, order=0, cur_exp=0, prob_compen=0, star_level=0, train_levels=[0]*4,
               grow_values=[secrets.randbelow(hi-lo+1)+lo for lo,hi in
                            (growth_range(tid,k,quality) for k in hp.ATTR)])
    rows.append(pet)
    return pet


def sequence(value):
    # table.tostring serializes both dense arrays and numeric-keyed tables.
    if isinstance(value, dict) and set(value) == set(range(1, len(value)+1)):
        value = [value[i] for i in range(1, len(value)+1)]
    a.require(isinstance(value, list), '宠物材料列表无效')
    return value


def materials(home, d, pet, count=None):
    ids = sequence(d.get('src_list', []))
    a.require(0 < len(ids) <= 6 and (count is None or len(ids) == count), '宠物材料数量错误')
    a.require(all(type(i) is int for i in ids) and len(set(ids)) == len(ids), '宠物材料重复或无效')
    by_id = {p['id']: p for p in home['pets']}
    a.require(all(i in by_id and i != pet['id'] and not by_id[i]['order'] for i in ids), '不能消耗出战宠物或自身')
    return [by_id[i] for i in ids]


def experience(p, r):
    base = SPECIAL_EXP.get((p['type_id'], p['quality']), int(VALUES[p['main_type'], p['quality']]['base_exp']))
    invested = p['cur_exp'] + sum(EXP[p['main_type'], n] for n in range(1, p['level']))
    return Decimal(base) + Decimal(invested) * Decimal(str(r['upgrade_exp_rate']))


def fusion_probabilities(main, quality, value):
    """petUI 1492–1539: three-material quality expectation."""
    values = {q: int(VALUES[main, q]['base_quality_value']) for q in range(1, 5)}
    if quality == 4:
        return {4: 1.0}
    cur, nxt = values[quality], values[quality+1]
    if value < cur * 3:
        if quality == 1:
            up = value / (nxt-cur)
            return {quality: 1-up, quality+1: up}
        same = 1-cur*3/(nxt-cur)
        up = (value + (1-same)*(cur-values[quality-1]))/(nxt-values[quality-1])
        return {quality-1: 1-same-up, quality: same, quality+1: up}
    if value < nxt-cur:
        up = value/(nxt-cur)
        return {quality: 1-up, quality+1: up}
    if quality+2 not in values:
        return {quality+1: 1.0}
    up2 = min(1.0, (value+cur-nxt)/(values[quality+2]-nxt))
    return {quality+1: 1-up2, quality+2: up2}


def consume_item(role, raw):
    # Original attachment format is object_type|type_id|level|count.
    typ, tid, level, count = map(int, raw.split('|'))
    a.require(typ == 5 and level == 1, '宠物消耗配置无效')
    a.consume(role, tid, count)


def settle(role, req, now, arules, parse):
    r = load_rules()
    a.require(role['level'] >= 50, '宠物系统50级开放')
    a.require(req.get('flag') == 1 and req.get('id') in range(1, 7), '宠物操作无效')
    op = req['id']; d = parse(req['data'])
    a.require(isinstance(d, dict), '宠物参数无效')
    home = h.state(role, now, arules)
    # [B] One starter for saves with no acquisition service. No daily duplication.
    if not home.get('independent_pet_initialized'):
        if not home['pets']:
            add(home, r['starter_type'], r['starter_quality'], r)
        home['independent_pet_initialized'] = True
    deleted = []
    if op != 4:
        pid = d.get('des_id')
        a.require(type(pid) is int, '宠物编号无效')
        pet = next((p for p in home['pets'] if p['id'] == pid), None)
        a.require(pet is not None, '宠物不存在')
        control = CONTROL[pet['main_type'], pet['quality']]
        if op == 3:
            a.require(hp.BASE[pet['type_id']]['is_exp_pet'] != 'Y', '经验宠物不能出战')
            active = not pet['order']
            for p in home['pets']: p['order'] = int(active and p['id'] == pid)
        elif op == 1:
            max_level = max(n for main, n in EXP if main == pet['main_type'])
            a.require(pet['level'] < max_level, '宠物已满级')
            sources = materials(home, d, pet)
            pet['cur_exp'] += int(sum((experience(p, r) for p in sources), Decimal(0)))
            while pet['level'] < max_level and pet['cur_exp'] >= EXP[pet['main_type'], pet['level']]:
                pet['cur_exp'] -= EXP[pet['main_type'], pet['level']]
                pet['level'] += 1
            if pet['level'] == max_level: pet['cur_exp'] = 0
            deleted = [p['id'] for p in sources]
        elif op == 2:
            sources = materials(home, d, pet, 3)
            a.require(all(hp.BASE[p['type_id']]['is_exp_pet'] != 'Y' for p in sources+[pet]), '经验宠物不能融合')
            value = pet.get('prob_compen', 0) + sum(int(VALUES[p['main_type'], p['quality']]['base_quality_value']) for p in sources)
            probs = fusion_probabilities(pet['main_type'], pet['quality'], value)
            roll = secrets.randbelow(1000000)/1000000
            quality = max(probs)
            for q, chance in sorted(probs.items()):
                roll -= chance
                if roll < 0:
                    quality = q; break
            # [B] A trained pet retains the minimum quality required by its stars.
            quality = max(quality, 4 if pet['star_level'] > 6 else 3 if pet['star_level'] else 1)
            pet['prob_compen'] = min(1000000,value) if quality <= pet['quality'] else 0
            # [B] Preserve type/level/star; resample growth using the original range table.
            pet['quality'] = quality
            pet['grow_values'] = [secrets.randbelow(hi-lo+1)+lo for lo, hi in
                                  (growth_range(pet['type_id'], k, quality) for k in hp.ATTR)]
            for token in filter(None, STAR[pet['star_level']]['plus_growup_rate'].split('/')):
                stat, rate = map(int, token.split('|'))
                pet['grow_values'][stat-1] = pet['grow_values'][stat-1]*(100+rate)//100
            deleted = [p['id'] for p in sources]
        elif op == 5:
            pos = d.get('pos')
            a.require(pet['quality'] >= r['min_train_quality'] and type(pos) is int and 1 <= pos <= 4, '培养条件不足')
            a.require(pet['star_level'] > 0 and pet['train_levels'][pos-1] < 4, '请先升星或该方向已培养满')
            consume_item(role, STAR[pet['star_level']]['each_stage_consume'])
            pet['train_levels'][pos-1] += 1
        elif op == 6:
            a.require(pet['star_level'] < int(control['max_star_level']), '已达当前品质星级上限')
            a.require(pet['star_level'] == 0 or all(n == 4 for n in pet['train_levels']), '请先完成四个方向培养')
            sources = materials(home, d, pet, 5)
            requirements = []
            for token in STAR[pet['star_level']]['star_consume2'].split('/'):
                typ, quality, count = map(int, token.split('|'))
                requirements.extend([(typ, quality)]*count)
            remaining = list(sources)
            for typ, quality in sorted(requirements, key=lambda x: x[0], reverse=True):
                found = next((p for p in remaining if p['star_level'] == 0 and p['quality'] == quality and
                              (p['type_id'] == typ if typ > 3 else p['main_type'] == typ)), None)
                a.require(found is not None, '升星材料类型或品质不符')
                remaining.remove(found)
            a.require(not remaining, '升星材料数量不符')
            consume_item(role, STAR[pet['star_level']]['star_consume1'])
            pet['star_level'] += 1; pet['train_levels'] = [0]*4
            # [B] Apply the original final-star growth-rate bonus to saved growth.
            for token in filter(None, STAR[pet['star_level']]['plus_growup_rate'].split('/')):
                stat, rate = map(int, token.split('|'))
                pet['grow_values'][stat-1] = pet['grow_values'][stat-1]*(100+rate)//100
            deleted = [p['id'] for p in sources]
        home['pets'] = [p for p in home['pets'] if p['id'] not in deleted]
    return [summon.event(174, dict(flag=op, update_list={p['id']: hp.wire(p) for p in home['pets']},
        del_list=deleted, const_config={k: r[k] for k in ('min_train_quality', 'upgrade_exp_rate', 'plus_rate_list')}))]
