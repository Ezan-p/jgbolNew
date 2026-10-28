"""Multiple seeds and original catalog archetypes, with legally mastered medicine."""
import copy
import itertools
import json
from pathlib import Path
import random
import sys
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import activity_abyss as ab, activity_abyss_combat as essence, combat, journey, npc_players


def main():
    catalog=npc_players.catalog();rules=journey.load_rules();records=[]
    for archetype in ('attack','magic','endurance'):
        key=max((k for k,v in catalog.items() if v['profile']['level']>=70 and
                 v['profile']['preferred_archetype']==archetype),key=lambda k:catalog[k]['profile']['role_combat_power'])
        role=copy.deepcopy(npc_players.get(key)['role']);ours,_=journey.fighters(role,dict(cortege_list='1001|1'))
        seeds=[]
        for seed in range(5):
            failed=[];wins=0;longest=0
            for floor in range(1,82):
                pair=min(itertools.product(range(1657,1661),repeat=2),key=lambda p:
                         sum(essence.effects(ab.BOSSES[floor],dict(zip(('5','6'),p))).values()))
                pills=dict(zip(('1','2','3','4','5','6'),(1644,1648,1652,1656,*pair)))
                state=dict(boss=floor,reductions=[0]*4);state['reductions']=ab.reductions(state,pills)
                with patch.object(combat.secrets,'randbelow',side_effect=random.Random(f'{key}:{seed}:{floor}').randrange):
                    result,_,actions,_=essence.battle(role,(ours,ab.enemies(state)),rules,essence.effects(ab.BOSSES[floor],pills))
                longest=max(longest,len(actions))
                if 1<=result<=3:wins+=1
                else:failed.append(floor)
            seeds.append(dict(seed=seed,wins=wins,failed=failed,max_actions=longest))
        records.append(dict(key=key,profile=catalog[key]['profile'],seeds=seeds))
        print(key,seeds,flush=True)
    report=dict(date='2026-10-28',battles=1215,player_stat_boost=False,preloaded_legal_mastered_medicine=True,
                records=records,all_floors_all_seeds=all(x['wins']==81 for r in records for x in r['seeds']))
    (ROOT/'analysis/evidence/abyss/multi_seed_balance_20261028.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()
