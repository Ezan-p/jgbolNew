"""Explicit local nine-region balance; never scales enemies to the querying player."""
import json
from functools import lru_cache
from pathlib import Path
from . import formation

PATH = Path(__file__).resolve().parents[1] / 'server_config/abyss_rules.json'


@lru_cache(maxsize=1)
def rules():
    return load_rules()


def load_rules(path=PATH):
    cfg = json.loads(Path(path).read_text())
    require = formation.require
    require(cfg.get('mode') == 'inferred' and bool(cfg.get('revision')), '九幽平衡配置需标注推测版本')
    for key in ('region_stat_percent', 'region_crystal_caps'):
        values = cfg.get(key)
        require(isinstance(values, list) and len(values) == 9 and
                all(type(x) is int and 1 <= x <= 100 for x in values), '九幽九狱数值无效：' + key)
        require(values == sorted(values), '九幽分区数值须递增')
    for key in ('magic_attack_cap_percent', 'boss_crystal_divisor', 'boss_silver_base', 'boss_silver_per_floor'):
        require(type(cfg.get(key)) is int and 1 <= cfg[key] <= 1000000, '九幽数值无效：' + key)
    require(cfg.get('essence_scope') == 'leader', '九幽精魄限主冥仙佩戴')
    skill = formation.SKILLS.get(cfg.get('leader_fallback_skill'), {})
    require(skill.get('use_mode(1-active，2-passive)') == '1' and int(skill.get('use_probability', 0)) > 0,
            '九幽补充法术必须可释放')
    weights = cfg.get('quality_weights')
    require(isinstance(weights, list) and len(weights) == 4 and all(
        isinstance(row, list) and len(row) == 4 and all(type(x) is int and 0 <= x <= 100 for x in row)
        and sum(row) == 100 for row in weights), '炼药品质概率无效')
    require(all(weights[0]) and weights[-1] == [0, 0, 0, 100], '药品四品质须可达且熟练配方保证极品')
    require(cfg.get('course_start_level') == 4 and cfg.get('course_finish_floor') == 72, '炼药进阶课程范围无效')
    require(cfg.get('starter_rewards') == [[5, 1442, 40, 1], [12, 0, 100000, 1], [11, 0, 50, 1]],
            '九幽一次性入门补给无效')
    return cfg


def region(floor):
    return (floor - 1) // 9


def crystal_tick(role, state, activity_rules):
    cap = min(activity_rules['abyss_crystal_tick_cap'], rules()['region_crystal_caps'][region(state['layer'])])
    return min(cap, max(1, role.get('role_combat_power', 100) // activity_rules['abyss_power_per_crystal']))


def course_total(floor):
    """XP curve from the starter's level 4 to level 36 by clearing floor 72."""
    from .activity_drug import LEVELS
    cfg = rules(); end = cfg['course_finish_floor']; start = cfg['course_start_level']
    progress = min(floor, end) * (max(LEVELS) - start)
    whole, part = divmod(progress, end)
    level = start + whole
    return sum(LEVELS[k] for k in range(start, level)) + (LEVELS[level] * part // end if part else 0)


def course_level(floor):
    cfg = rules()
    return cfg['course_start_level'] + min(floor, cfg['course_finish_floor']) * (36-cfg['course_start_level']) // cfg['course_finish_floor']


def victory_rewards(floor):
    from .activity_abyss import BOSSES
    cfg = rules(); specs = []
    for token in BOSSES[floor]['prirze_list'].split('/'):
        typ, tid, lv, n = map(int, token.split('|'))
        if typ == 5 and tid == 1441:
            n = max(1, n // cfg['boss_crystal_divisor'])
        specs.append([typ, tid, n, lv])
    specs.append([12, 0, cfg['boss_silver_base'] + cfg['boss_silver_per_floor'] * floor, 1])
    return specs
