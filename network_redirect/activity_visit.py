"""三星赐福: native two-stage games [A], configurable missing reward pools [B]."""
import copy
import json
import secrets
from pathlib import Path
from . import formation, journey, summon

ROOT = Path(__file__).resolve().parents[1]
FORMS = {tuple(map(int, row['form_type'].split('|'))): row
         for row in summon.rows('luhsing_form_rate.csv')}
ACHIEVEMENTS = {'liuliudashun': 323, 'tonghuashun': 324, 'fafafa': 325, 'kaimenhong': 326}
# Quality-one rows are internal combat actions, not collectible spell books.
SKILLS = {q: sorted(t for t, row in formation.SKILLS.items()
                    if int(row['quality']) == q and int(row['top_level']) > 1)
          for q in range(2, 6)}
EQUIPMENT = {q: sorted(t for t, row in formation.ITEMS.items()
                       if int(row['quality']) == q and int(row['main_type']) in (1, 2, 3))
             for q in range(2, 6)}


def load_rules(path=ROOT/'server_config/visit_rules.json'):
    r = json.loads(Path(path).read_text())
    require = formation.require
    require(r.get('schema_version') == 1 and r.get('mode') == 'inferred', '三星赐福配置必须标注 inferred')
    require(isinstance(r.get('revision'), str) and bool(r['revision']), '三星赐福配置版本缺失')
    require(type(r.get('lu_base_silver')) is int and 0 < r['lu_base_silver'] <= 1000000, '禄星基础银币无效')
    for key, pool in (('shou_quality_weights', SKILLS), ('fu_quality_weights', EQUIPMENT)):
        weights = r.get(key)
        require(isinstance(weights, dict) and set(weights) == set('2345'), '赐福品质分档无效')
        require(all(type(v) is int and 0 < v <= 10000 for v in weights.values()), '赐福品质权重无效')
        require(all(weights[str(q)] > weights[str(q+1)] for q in range(2, 5)), '高品质赐福概率必须更低')
        require(all(pool.values()), '赐福品质奖池为空')
    require(type(r.get('fu_equipment_weight')) is int and 0 < r['fu_equipment_weight'] <= 10000, '福星装备权重无效')
    require(isinstance(r.get('fu_rewards'), list) and 0 < len(r['fu_rewards']) <= 20, '福星奖池无效')
    for row in r['fu_rewards']:
        require(isinstance(row, dict) and type(row.get('weight')) is int and 0 < row['weight'] <= 10000, '福星奖励权重无效')
        p = row.get('reward')
        require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p), '福星奖励格式无效')
        kind, tid, count, level = p
        require(0 < count <= 1000000 and level == 1 and
                (kind in (11, 12) and tid == 0 or kind == 5 and tid in formation.ITEMS), '福星奖励无效')
    return r


def weighted(entries):
    """Draw a category first so pool size cannot increase its rarity's chance."""
    ticket = secrets.randbelow(sum(weight for _, weight in entries))
    for value, weight in entries:
        if ticket < weight:
            return value
        ticket -= weight
    raise AssertionError('invalid weighted pool')


def draw_quality(pool, weights):
    q = weighted([(q, weights[str(q)]) for q in sorted(pool)])
    return secrets.choice(pool[q])


def draw_fu(r):
    p = weighted([(row['reward'], row['weight']) for row in r['fu_rewards']]
                 + [(None, r['fu_equipment_weight'])])
    return copy.deepcopy(p) if p is not None else [5, draw_quality(EQUIPMENT, r['fu_quality_weights']), 1, 1]


def draw_shou(r):
    return [6, draw_quality(SKILLS, r['shou_quality_weights']), 1, 1]


def dice_result(dice):
    row = FORMS.get(tuple(sorted(dice)), {})
    return int(row.get('rate', 1)), ACHIEVEMENTS.get(row.get('resource'))


def prize_info(p):
    return dict(object_type=p[0], attach_type=p[1], attach_count=p[2], attach_level=p[3])


def visit_list(role):
    visits = role['activity']['visits']
    return [dict(can_visit=True, has_visit=bool(visits.get(str(i), {}).get('claimed')),
                 prize_info=copy.deepcopy(visits.get(str(i), {}).get('prize_info', {})))
            for i in (1, 2, 3)]


def settle(role, req, r):
    i, op = req['visit_index'], req['op_type']
    receipt = {}
    formation.require(i in (0, 1, 2, 3) and (op in (0, 1) if i == 0 else op in (1, 2)), '拜访参数无效')
    if i:
        visits = role['activity']['visits']
        state = visits.get(str(i), {})
        formation.require(not state.get('claimed'), '今日已拜访该仙人')
        if op == 1 and 'prize_info' not in state:
            if i == 1:
                cards = [draw_fu(r) for _ in range(8)]
                reward = cards[0]
                info = [dict(prize_info(card), get_flag=j == 0) for j, card in enumerate(cards)]
            elif i == 2:
                dice = [secrets.randbelow(6)+1 for _ in range(3)]
                rate, _ = dice_result(dice)
                reward = [12, 0, r['lu_base_silver']*rate, 1]
                info = dict(prize_info(reward), form_type=dice, total_money=reward[2])
            else:
                reward = draw_shou(r)
                info = prize_info(reward)
            state = dict(version=2, reward=reward, prize_info=info)
            visits[str(i)] = state
        elif op == 2:
            formation.require('prize_info' in state, '请先开始拜访')
            reward = state.get('reward')
            # Legacy Shou stored only its already-revealed prize. Honor it once;
            # never reroll a pending scratch card or depend on a changed config.
            if reward is None:
                info = state['prize_info']
                formation.require(i == 3 and isinstance(info, dict), '拜访奖励存档无效')
                reward = [info[k] for k in ('object_type', 'attach_type', 'attach_count', 'attach_level')]
                state['reward'] = reward
            old_ids = {item['id'] for item in role['attachments']}
            journey.grant(role, reward)
            if i == 3:
                # Keep the actual instances with the claim, not just the displayed
                # book type. A consumed book must never be reissued on a query.
                added = [item for item in role['attachments'] if item['id'] not in old_ids]
                if reward[0] == 6:
                    formation.require(len(added) == reward[2] and all(
                        item['attach_type'] == 6 and item['type_id'] == reward[1]
                        and item['level'] == reward[3] and not item.get('protogenic')
                        for item in added), '寿星奖励未入包，请重试')
                state['reward_ids'] = [item['id'] for item in added]
                receipt = dict(local_prizes=[prize_info(reward)])
            state['claimed'] = True
    return [summon.event(42, dict(visit_index=i, op_type=op, result=1,
                                 visit_list=visit_list(role), **receipt))]
