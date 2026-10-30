"""Permanent Mid-Autumn event: local material rolls and independent food draws."""
import json
from pathlib import Path
from secrets import randbelow
from . import activity_food, formation, item_rewards, summon

ROOT = Path(__file__).resolve().parents[1]
FOODS = {1130, 1131, 1132, 1133}
FILLINGS = (1135, 1136, 1137, 1138)


def client_source(shared):
    source = Path(__file__).with_name('moon_client.lua').read_text().replace(
        '__SEASONAL_CRAFT_HELPER__', Path(__file__).with_name('seasonal_craft_client.lua').read_text())
    source = source.replace('__CRAFT_DAILY_LIMIT__', str(shared['seasonal_craft_daily_limit']))
    return (source.replace('__MOON_ENABLED__', summon.lua(shared['seasonal_games']['moon']['enabled']))
            .replace('__MOON_BONUS_EVERY__', str(shared['seasonal_moon_bonus_every']))
            .replace('__MOON_BONUS_COUNT__', str(sum(p[2] for p in shared['seasonal_moon_bonus'] if p[:2] == [5, 1001]))))


def load_rules(path=ROOT/'server_config/moon_rules.json'):
    r = json.loads(Path(path).read_text())
    require = formation.require
    require(r.get('schema_version') == 1 and r.get('mode') == 'inferred', '中秋配置必须标注 inferred')
    require(isinstance(r.get('revision'), str) and bool(r['revision']), '中秋配置版本缺失')
    require(r.get('filling_weights') == [10, 70, 20] and
            all(type(w) is int for w in r['filling_weights']), '中秋馅料须按0/1/2个的10/70/20权重掉落')
    require(r.get('flour_counts') == [2, 3, 4] and r.get('flour_weights') == [1, 1, 1], '面粉和粽叶须等概率掉落2至4个')
    require(set(r.get('pools', {})) == set(map(str, FOODS)), '四种月饼奖池缺失')
    for pool in r['pools'].values():
        groups = pool.get('groups')
        require(isinstance(groups, list) and 1 <= len(groups) <= 40, '月饼奖池分组无效')
        seen = set()
        for group in groups:
            require(type(group.get('weight')) is int and 0 < group['weight'] <= 10000, '月饼权重无效')
            candidates = group.get('candidates')
            require(isinstance(candidates, list) and 1 <= len(candidates) <= 50, '月饼候选奖励无效')
            for p in candidates:
                require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p)
                        and 0 < p[2] <= 1000000 and p[3] == 1 and
                        (p[0] in (11, 12) and p[1] == 0 or
                         p[0] == 5 and p[1] in formation.ITEMS and p[1] not in FOODS | {1134, *FILLINGS} | set(range(1208, 1218)) or
                         p[0] == 6 and p[1] in formation.SKILLS and p[1] > 10), '月饼奖励规格无效')
                require(tuple(p) not in seen, '月饼奖池有重复候选')
                seen.add(tuple(p))
        require(sum(g['weight'] for g in groups) == 10000, '月饼奖池权重合计须为10000')
    return r


def weighted(values, weights):
    return activity_food.weighted(values, weights, randbelow)


def material_specs(shared):
    """One flour roll plus four independent filling rolls per valid settlement."""
    if not shared['seasonal_games']['moon']['enabled']:
        return []
    return activity_food.material_specs(shared['moon_rules'], 1134, FILLINGS, randbelow)


def draw(pool):
    return activity_food.draw(pool, randbelow)


def use(role, req, shared):
    return activity_food.use(role, req, shared['moon_rules']['pools'],
                             {tid: tid for tid in FOODS}, draw, '月饼')
