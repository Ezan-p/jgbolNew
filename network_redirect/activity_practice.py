"""主角修炼: original practiceUI contracts [A], explicit offline balance [B]."""
import json
import secrets
from pathlib import Path

from . import formation, journey, summon
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
# Native event_mgr.train_role -> practiceUI.createPracticeContent consumes ONE field.
FIELDS = {'hp': ('max_hp_plus', 75), 'magic': ('max_magic_plus', 76),
          'gongji': ('gongji_plus', 77), 'fangyu': ('fangyu_plus', 78)}
NAMES = {int(row['type_id']): row['name'] for row in summon.rows('cortege/cortege_name_0.csv')}


def load_rules(path=ROOT / 'server_config/practice_rules.json'):
    r = json.loads(Path(path).read_text())
    formation.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
                      and isinstance(r.get('revision'), str) and bool(r['revision']), '主角修炼配置来源无效')
    formation.require(type(r.get('enemy_type')) is int and r['enemy_type'] == 5001,
                      '主角修炼对手必须为阎罗王')
    for key, high in (('enemy_first_level', 100), ('enemy_levels_per_win', 2), ('enemy_skill_level', 10)):
        formation.require(type(r.get(key)) is int and 1 <= r[key] <= high, '修炼对手成长配置无效')
    formation.require(r['enemy_first_level'] + (max(formation.LEVELS)-5)*r['enemy_levels_per_win'] <= 255,
                      '修炼对手等级超过协议上限')
    weights = r.get('reward_weights')
    formation.require(isinstance(weights, dict) and set(weights) == set(FIELDS)
                      and all(type(v) is int and 1 <= v <= 10000 for v in weights.values()), '修炼奖励权重无效')
    return r


def encounter(index, rules):
    # Progress, not current player strength/level, determines the next challenge.
    # A player can improve their formation and retry the same opponent for free.
    return dict(cortege_list=f"{rules['enemy_type']}|{rules['enemy_first_level'] + index*rules['enemy_levels_per_win']}",
                skill_level=rules['enemy_skill_level'])


def draw(rules):
    roll = secrets.randbelow(sum(rules['reward_weights'].values()))
    for stat in FIELDS:
        weight = rules['reward_weights'][stat]
        if roll < weight:
            return stat
        roll -= weight
    raise AssertionError('unreachable reward draw')


def battle(role, req, now, rules, jrules):
    r = load_rules()
    formation.require(role['level'] >= 5, '主角修炼需要角色5级')
    formation.require(req.get('des_type') == 1 and req.get('des_id', 0) == 0
                      and req.get('des_value', 0) == 0, '主角修炼挑战目标无效')
    index = role['rule_index']
    formation.require(type(index) is int and index >= 0, '修炼进度无效')
    formation.require(index < role['level']-4, '修炼次数已用完，请先提升主角等级')
    formation.require(any(1 <= c.get('order', 0) <= 8 for c in role['corteges']), '请先上阵神仙')
    cfg = encounter(index, r)
    result, lineup, actions = journey.battle(role, cfg, jrules)
    state = role['activity']
    state['fight_id'] += 1
    fid = state['fight_id']
    reward, events = None, []
    if 1 <= result <= 3:
        stat = draw(r)
        field, attr = FIELDS[stat]
        value = rules['train_increase'][stat]
        role['rule_index'] = index + 1
        role[field] += value
        reward = dict(stat=stat, addition_field=attr, addition_value=value)
        events.append(summon.event(5, dict(addition_field=attr, addition_value=value)))
    # Existing accumulated bonuses are preserved, including legacy four-stat wins.
    state['practice_last_result'] = dict(fight_id=fid, stage=index+1, result=result, time=now,
                                        enemy_type=r['enemy_type'], enemy_level=int(cfg['cortege_list'].split('|')[1]),
                                        reward=reward, revision=r['revision'])
    return journey.combat_engine.event_packets(actions, fid) + [
        encode(1028, dict(fight_id=fid, first_hand=1, des_name=NAMES[r['enemy_type']],
                         lineup_count=len(lineup), lineup=lineup)),
        encode(1027, dict(fight_id=fid, fight_type=4, final_result=result,
                         fight_round=len(actions), fight_result=actions))] + events + [
        summon.event(44, dict(fight_id=fid, fight_type=4))]
