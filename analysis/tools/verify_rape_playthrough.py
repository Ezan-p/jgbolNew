"""Repeatable real-engine 渡劫 samples, using disposable accounts only."""
import copy
import json
import random
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity, activity_rape as rape, activity_rape_npc as npcs
from network_redirect.backend import Backend
from network_redirect.protocol import decode


def main():
    rng=random.Random(20261025);rows=[]
    with tempfile.TemporaryDirectory() as tmp, patch('secrets.randbelow',side_effect=rng.randrange), patch('secrets.choice',side_effect=rng.choice), patch.object(rape,'roll_forms',return_value=[1,3,5]):
        backend=Backend(Path(tmp),18770,lambda *a,**k:None)
        try:
            for level,base in ((8,7),(25,24),(60,60),(99,99)):
                player=next(n for n in npcs.catalog().values() if n['role']['level']==base and n['tier']=='T3' and n['archetype']=='attack')
                role=backend.profile();role.update(copy.deepcopy(player['role']));role.update(level=level,energy=100,gold_coin=10000)
                activity.prepare(role,1792814400,backend.activity_rules)
                boards=rape.ensure(role,1792814400,backend.activity_rules);wins=0
                for i,b in enumerate(boards,1):
                    for ident,target in b['form_list']['2'].items():
                        out=rape.battle(role,dict(fight_type=3,des_type=2,des_value=i,des_id=int(ident)),1792814400,backend.activity_rules,backend.journey_rules)
                        fight=next(d for m,_,d in map(decode,out) if m==1027)
                        wins+=1<=fight['final_result']<=3
                        rows.append(dict(level=level,npc=target['npc_id'],player_power=role['role_combat_power'],npc_power=target['power'],result=fight['final_result'],actions=fight['fight_round']))
                assert wins>=3,(level,wins)
        finally:backend.close()
    report=dict(date='2026-10-26',mode='real_engine_fixed_seed',native_ui_verified=False,battles=rows)
    dest=ROOT/'analysis/evidence/rape/playthrough.json';dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Verified',len(rows),'real battles;',sum(1<=r['result']<=3 for r in rows),'wins;',sum(r['result']==0 for r in rows),'unresolved')

if __name__=='__main__':main()
