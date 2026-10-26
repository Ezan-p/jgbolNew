"""Tower schedule [B], built from original character identities/stats/skills [A]."""
import copy
import json
from functools import lru_cache
from pathlib import Path
from . import formation, journey, combat_power, summon

ROOT = Path(__file__).resolve().parents[1]
NAMES = {int(row['type_id']): row['name'] for row in summon.rows('cortege/cortege_name_0.csv')}


@lru_cache(maxsize=1)
def rules():
    r = json.loads((ROOT/'server_config/land_boss_rules.json').read_text())
    formation.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred', '镇妖塔配置来源无效')
    floors = r['floors']
    formation.require(len(floors) == 64 and [f['layer'] for f in floors] == list(range(1,65)), '镇妖塔必须配置完整64层')
    formation.require(len({f['type_id'] for f in floors}) == 64 and len({f['name'] for f in floors}) == 64, '镇妖塔首领不能重复')
    for f in floors:
        tid = f['type_id']
        formation.require(type(tid) is int and tid in formation.BASES and tid in journey.NPCS
                          and NAMES.get(tid) == f['name'], '镇妖塔首领必须使用原版神仙')
        formation.require(int(journey.NPCS[tid]['chushijineng']) in formation.SKILLS, '镇妖塔首领法术缺失')
    formation.require(1 <= r['normal_level_step'] < r['hell_level_step'] <= 3
                      and r['skill_level'] == 1 and r['guard_layer_step'] == 8, '镇妖塔成长配置无效')
    return r


@lru_cache(maxsize=2)
def schedule(hell=False):
    r = rules(); leaders = []; result = []
    weights = formation.load_rules()['combat_weights']
    for floor in r['floors']:
        layer = floor['layer']; level = layer*r['hell_level_step' if hell else 'normal_level_step']
        _, units = journey.fighters({'corteges':[]}, dict(
            cortege_list=f"{floor['type_id']}|{level}", skill_level=r['skill_level']))
        lead = units[0]
        if leaders:
            # Different archetypes have different base ratios. Prevent a change
            # of character from making a later chief weaker in any base stat.
            for stat in formation.STATS:lead[stat] = max(lead[stat],leaders[-1][stat]+1)
        lead['max_hp'] = lead['hp']; leaders.append(lead)
        count = min(8,1+(layer-1)//r['guard_layer_step'])
        army = copy.deepcopy(list(reversed(leaders[-count:])))
        for order,unit in enumerate(army,1):unit['order'] = order
        result.append(dict(layer=layer, name=('冥界·' if hell else '')+floor['name'],
                           type_id=floor['type_id'], units=army, level=level,
                           power=sum(combat_power.score_panel(u,weights) for u in army)))
    return result


def encounter(layer,hell=False):
    formation.require(type(layer) is int and 1 <= layer <= len(rules()['floors']), '镇妖塔层数无效')
    # Never expose a cached battle army to mutation by a caller or engine.
    return copy.deepcopy(schedule(hell)[layer-1])
