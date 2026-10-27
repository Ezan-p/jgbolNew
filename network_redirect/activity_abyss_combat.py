"""冥仙精魄: original descriptions/drugs [A], deterministic local resolution [B].

Events 121 carry healing/revival to the unmodified replay. Extra attacks are real
1027 actions. Damage uses the shared V1.1 candidate reconstruction.
"""
import copy
import secrets
from . import formation, journey, summon, reborn_stars, combat
DESC={int(x['type_id']):[int(v.rstrip('%')) for v in x['reduce_value'].split('|')] for x in summon.rows('specter_jp_desc.csv')}
DRUGS={int(x['drug_type']):[list(map(int,t.split('|'))) for t in next(v for k,v in x.items() if k.startswith('effect1')).split('/')]
       for x in summon.rows('specter_extr_skill_drug.csv')}


def effects(row,pills):
    out={}
    for token in filter(None,row['ext_skill_list'].split('/')):
        _,tid,level,_=map(int,token.split('|'));out[tid]=DESC[tid][level-1]
    for tid in pills.values():
        if tid not in DRUGS:continue
        for fields in DRUGS[tid]:
            kind=fields[0]
            if kind in out:out[kind]=max(0,out[kind]-sum(fields[3:]))
    return out


def battle(role,units,rules,effect_values,max_actions=None):
    from .combat_engine import Battle
    # The historical 80-action override was a serialization workaround. Use
    # the common combat limit now that extra events are transported in chunks.
    result, lineup, actions = Battle(role, units, rules, extras=effect_values, max_actions=max_actions).run()
    return result, lineup, actions, actions.events
