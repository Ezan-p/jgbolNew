"""Level-based guild secret-area opponents; inferred offline balance [B]."""
from fractions import Fraction
from . import combat_power, formation, npc_players


def target_power(level, floor, rules):
    level=max(rules['join_level'],int(level))
    return (rules['secret_power_per_level_squared']*level*level
            *rules['secret_floor_percent'][floor-1]//100)


def choose(role, state, rules, excluded):
    """Keep one eight-unit template all day so every stat grows on later floors."""
    from .guild_offline import roll
    a=state.setdefault('instances',{})
    if a.get('team_enemy_npc'):
        return a['team_enemy_npc']
    excluded=set(excluded)
    candidates=[]
    for key,entry in npc_players.catalog().items():
        if entry['profile']['role_id'] in excluded:continue
        raw=npc_players.source_file(entry['source_file'])[key]
        if raw.get('battle_validation',{}).get('status')=='replay_limit_observed':continue
        if sum(1<=c.get('order',0)<=8 for c in raw['role']['corteges'])!=8:continue
        candidates.append(entry)
    formation.require(candidates,'没有可用的秘境八人NPC阵容')
    target=target_power(role['level'],1,rules)
    candidates.sort(key=lambda e:(abs(e['profile']['level']-role['level']),
                                  abs(e['profile']['role_combat_power']-target),e['npc_id']))
    # Restrict random identities to the closest level and three power neighbours.
    nearest=abs(candidates[0]['profile']['level']-role['level'])
    pool=[e for e in candidates if abs(e['profile']['level']-role['level'])==nearest][:3]
    a['team_enemy_npc']=pool[roll(state,len(pool))]['npc_id']
    return a['team_enemy_npc']


def scale(units, level, floor, rules):
    """Scale actual HP/attack/defense/magic, without editing the shared NPC save.

    The disclosed score uses the standard four-stat weights. Temporary skills
    and essence triggers are retained, but are not added to this budget.
    """
    weights=formation.load_rules()['combat_weights']
    original=sum(unit[stat]*Fraction(str(weights[stat]))
                 for unit in units for stat in combat_power.STATS)
    formation.require(original>0,'秘境NPC基础战力无效')
    target=target_power(level,floor,rules)
    for unit in units:
        for stat in combat_power.STATS:
            unit[stat]=max(1,int(unit[stat]*target//original))
        unit['max_hp']=unit['hp']
    actual=sum(combat_power.score_panel(unit,weights) for unit in units)
    return dict(floor=floor,role_level=level,target_power=target,attribute_power=actual,
                floor_percent=rules['secret_floor_percent'][floor-1],
                units=[dict(order=u['order'],type=u['type'],hp=u['hp'],gongji=u['gongji'],
                            fangyu=u['fangyu'],magic=u['magic'],
                            attribute_power=combat_power.score_panel(u,weights)) for u in units])
