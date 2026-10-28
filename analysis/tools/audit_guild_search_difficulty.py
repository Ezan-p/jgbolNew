"""Audit current secret-area NPC selection; isolated roles, no balance changes."""
import json
import sys
from pathlib import Path
from functools import lru_cache
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import guild_combat, npc_players


def audit():
    catalog=npc_players.catalog()
    # Use one fixed real five-member NPC formation for each power bracket.
    ordered=sorted(catalog.values(),key=lambda x:x['profile']['role_combat_power'])
    cases=[]
    for name,offset in [('low',0),('middle',len(ordered)//2),('high',len(ordered)-5)]:
        selected=ordered[offset:offset+5]
        actors=[npc_players.get(v['npc_id'])['role'] for v in selected]
        _,_,power=guild_combat.joint_units(actors)
        role=actors[0];excluded=[a['role_id'] for a in actors]
        samples=[]
        for seed in range(64):
            state={'day':20754,'random_serial':seed*3}
            enemies=[guild_combat.choose_enemy(role,state,power=power,layer=layer,excluded=excluded) for layer in range(3)]
            powers=[catalog[key]['profile']['role_combat_power'] for key in enemies]
            samples.append(dict(seed=seed,enemies=enemies,powers=powers,strictly_increasing=powers[0]<powers[1]<powers[2]))
        example=next((s for s in samples if any(b<a for a,b in zip(s['powers'],s['powers'][1:]))),samples[0])
        details=[]
        for floor,key in enumerate(example['enemies'],1):
            enemy=npc_players.get(key)
            units=guild_combat.player_units(enemy['role'])
            details.append(dict(floor=floor,npc_id=key,name=enemy['role']['role_name'],catalog_power=catalog[key]['profile']['role_combat_power'],actual_power=enemy['role']['role_combat_power'],unit_count=len(units),hp=sum(u['hp'] for u in units),attack=sum(u['gongji'] for u in units),defense=sum(u['fangyu'] for u in units),magic=sum(u['magic'] for u in units)))
        cases.append(dict(bracket=name,team=[x['npc_id'] for x in selected],joint_power=power,target_powers=[max(1,power)*(75+layer*8)//100 for layer in range(3)],samples=64,strictly_increasing_samples=sum(s['strictly_increasing'] for s in samples),decreasing_samples=sum(any(b<a for a,b in zip(s['powers'],s['powers'][1:])) for s in samples),example_seed=example['seed'],example=details))
    report=dict(target_percent_by_floor=[75,83,91],strict_growth_guaranteed=False,enemy_stats_scaled_by_floor=False,selection='Random among up to 8 nearby catalog powers; same floor opponent is persisted.',cases=cases,live_account_resources_changed=False)
    dest=ROOT/'analysis/evidence/guild/search_difficulty_audit.json'
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


def main():
    # Catalog traversal spans 100 files; isolate a larger cache to this audit.
    cached=lru_cache(maxsize=None)(npc_players.source_file.__wrapped__)
    with patch.object(npc_players,'source_file',cached):audit()


if __name__=='__main__':main()
