"""Permanent Dragon Boat event: identical pools, independently sampled outcomes."""
from pathlib import Path
from secrets import randbelow
from . import activity_food, summon

FOOD_POOLS = {1213: 1130, 1214: 1131, 1215: 1132, 1216: 1133}
FILLINGS = (1209, 1210, 1211, 1212)


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
    return activity_food.use(role, req, shared['moon_rules']['pools'], FOOD_POOLS, draw, '粽子')


def state(seasonal):
    # Legacy saves have no trustworthy lifetime total; start at zero once.
    seasonal.setdefault('rice_count', 0)
    return seasonal


def progress(seasonal, shared):
    count = state(seasonal)['rice_count']
    step = shared['seasonal_moon_bonus_every']
    return dict(rice_count=count, cur_process=count % step, left_process=step-count % step,
                bonus_every=step, bonus_rewards=shared['seasonal_moon_bonus'])
