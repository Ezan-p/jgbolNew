"""Permanent Dragon Boat event: derived pools, independently sampled outcomes."""
import copy
import json
from pathlib import Path
from secrets import randbelow
from . import activity_food, formation, summon

FOOD_POOLS = {1213: 1130, 1214: 1131, 1215: 1132, 1216: 1133, 1217: 1217}
FILLINGS = (1209, 1210, 1211, 1212)


def load_rules(moon_rules, path=Path(__file__).resolve().parents[1]/'server_config/rice_rules.json'):
    r = json.loads(Path(path).read_text())
    require = formation.require
    require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
            and isinstance(r.get('revision'), str) and bool(r['revision']), '粽子配置版本无效')
    weight = r.get('normal_five_star_weight')
    require(type(weight) is int and 0 < weight < 10000, '五星粽子产出权重无效')
    pool = r.get('five_star_pool')
    require(isinstance(pool, dict) and isinstance(pool.get('groups'), list)
            and len(pool['groups']) == 6, '五星粽子须配置六类奖励')
    expected = [{(11, 0, 1000, 1)}, {(5, 1152, 1, 1)}]
    for category in (1, 2, 3):
        expected.append({(5, tid, 1, 1) for tid, row in formation.ITEMS.items()
                         if int(row['quality']) == 5 and int(row['main_type']) == category})
    expected.append({(6, tid, 1, 1) for tid, row in formation.SKILLS.items()
                     if tid != 21 and int(row['quality']) == 5 and int(row['use_mode(1-active，2-passive)']) == 2})
    for group, allowed in zip(pool['groups'], expected):
        require(type(group.get('weight')) is int and 0 < group['weight'] <= 10000,
                '五星粽子奖励权重无效')
        candidates = group.get('candidates')
        require(isinstance(candidates, list) and bool(candidates)
                and all(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p)
                        for p in candidates), '五星粽子奖励格式无效')
        require(len(candidates) == len(allowed) and {tuple(p) for p in candidates} == allowed,
                '五星粽子奖励须为指定货币、金卡及五星装备／被动法术白名单（排除大乘经21）')
    require(sum(g['weight'] for g in pool['groups']) == 10000, '五星粽子奖池权重合计须为10000')
    # Derive four pools without mutating the mooncake configuration.
    r['pools'] = copy.deepcopy(moon_rules['pools'])
    for base in r['pools'].values():
        silver = [g for g in base['groups'] if all(p[0] == 12 for p in g['candidates'])]
        require(bool(silver), '普通粽子缺少银两奖励组')
        funding = max(silver, key=lambda g: g['weight'])
        require(funding['weight'] > weight, '普通粽子银两权重不足以分配五星粽子')
        funding['weight'] -= weight
        base['groups'].append(dict(name='五星粽子', weight=weight, candidates=[[5, 1217, 1, 1]]))
    r['pools']['1217'] = copy.deepcopy(pool)
    return r


def client_source(shared):
    source = Path(__file__).with_name('rice_client.lua').read_text().replace(
        '__SEASONAL_CRAFT_HELPER__', Path(__file__).with_name('seasonal_craft_client.lua').read_text())
    source = source.replace('__CRAFT_DAILY_LIMIT__', str(shared['seasonal_craft_daily_limit']))
    return (source.replace('__RICE_ENABLED__', summon.lua(shared['seasonal_games']['rice']['enabled']))
            .replace('__RICE_BONUS_EVERY__', str(shared['seasonal_moon_bonus_every']))
            .replace('__RICE_BONUS_COUNT__', str(sum(p[2] for p in shared['seasonal_moon_bonus'] if p[:2] == [5, 1001]))))


def material_specs(shared):
    if not shared['seasonal_games']['rice']['enabled']:
        return []
    return activity_food.material_specs(shared['moon_rules'], 1208, FILLINGS, randbelow)


def draw(pool):
    return activity_food.draw(pool, randbelow)


def use(role, req, shared):
    return activity_food.use(role, req, shared['rice_rules']['pools'], FOOD_POOLS, draw, '粽子')


def state(seasonal):
    # Legacy saves have no trustworthy lifetime total; start at zero once.
    seasonal.setdefault('rice_count', 0)
    return seasonal


def progress(seasonal, shared):
    count = state(seasonal)['rice_count']
    step = shared['seasonal_moon_bonus_every']
    return dict(rice_count=count, cur_process=count % step, left_process=step-count % step,
                bonus_every=step, bonus_rewards=shared['seasonal_moon_bonus'])


# Guard automatic settlement as well as direct activity operations.
from .time_guard import protect as _protect_time_rewards
_protect_time_rewards(globals())
