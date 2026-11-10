"""Native home ordeal contract [A], fixed two-stage enemy balance [B]."""
import json
from fractions import Fraction
from functools import lru_cache

from . import activity as a, formation, journey
from .combat_power import score_panel


@lru_cache(maxsize=1)
def rules():
    from .activity_home import OWNER, TRAIN
    cfg = json.loads((a.ROOT / 'server_config/home_ordeal_rules.json').read_text())
    a.require(cfg['schema_version'] == 1 and cfg['mode'] == 'inferred', '红尘劫配置版本无效')
    a.require(set(cfg['stages']) == {str(lv) for lv in OWNER if lv < max(OWNER)}, '红尘劫阶段配置无效')
    for row in cfg['stages'].values():
        row.setdefault('non_hp_stat_percent', 100)
        types = row['cortege_types']
        a.require(isinstance(types, list) and 1 <= len(types) <= 8
                  and all(type(t) is int and t in journey.NPCS and t != journey.SKIP_CORTEGE_TYPE for t in types),
                  '红尘劫敌方阵容无效')
        for key, maximum in (('level', 600), ('skill_level', 100), ('train_level', 40),
                             ('stat_percent', 10000), ('non_hp_stat_percent', 10000), ('hp_multiplier', 1000)):
            a.require(type(row[key]) is int and 1 <= row[key] <= maximum, '红尘劫敌方数值无效')
        a.require(all((i, row['train_level']) in TRAIN for i in range(1, 5)), '红尘劫修炼配置无效')
    return cfg


def enemies(level):
    """One authoritative snapshot for both the native preview and simulation."""
    from .activity_home import TRAIN
    row = rules()['stages'][str(level)]
    cfg = dict(cortege_list='/'.join(f"{t}|{row['level']}" for t in row['cortege_types']),
               skill_level=row['skill_level'])
    _, units = journey.fighters({'corteges': []}, cfg)
    bonuses = [tuple(map(Fraction, TRAIN[i, row['train_level']]['worth'].split('|'))) for i in range(1, 5)]
    for unit in units:
        for stat in formation.STATS:
            unit[stat] = max(1, unit[stat] * row['stat_percent'] // 100)
            if stat != 'hp':
                unit[stat] = max(1, unit[stat] * row['non_hp_stat_percent'] // 100)
        unit['hp'] *= row['hp_multiplier']
        unit['max_hp'] = unit['hp']
        unit['training_bonuses'] = bonuses.copy()
    return cfg, units


def preview(s):
    from .activity_home import OWNER
    complete = s['level'] >= max(OWNER)
    # Preserve the native boss_info shape even when the final scale hides it.
    boss = dict(cortege_type=0, cortege_layer=0, combat_power=0, cortege_count=0, train_level=0)
    if not complete:
        _, units = enemies(s['level'])
        weights = formation.load_rules()['combat_weights']
        boss.update(cortege_type=units[0]['type'], cortege_layer=units[0]['reborn'],
                    combat_power=sum(score_panel(u, weights) for u in units), cortege_count=len(units),
                    train_level=rules()['stages'][str(s['level'])]['train_level'])
    return dict(has_passed=bool(s['passed']), fight_count=s['fight_count'], boss_info=boss,
                is_max_scale=complete)


def require_ready(s):
    from .activity_home import OWNER
    a.require(s['level'] < max(OWNER), '洞府规模已满')
    # homeUI.isAllBuildFix (L919–930), also present in the official hot update:
    # ISGE 1,scale jumps to the checks when scale <= 1; scale > 1 returns true.
    if s['level'] <= 1:
        minimum = int(OWNER[s['level']]['max_building_level'])
        a.require(all(s['build'][str(i)] >= minimum for i in (1, 2, 3)),
                  f'请先将主殿、药园和佛堂升至{minimum}级')
