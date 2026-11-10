"""Rebuild secret-area targets and sampled actual unit budgets without player saves."""
import csv
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import guild, guild_combat, guild_secret, npc_players


def main():
    rules=guild.load_rules()
    out=ROOT/'analysis/evidence/guild_secret'
    out.mkdir(parents=True,exist_ok=True)
    with (out/'level_power.csv').open('w',newline='') as stream:
        writer=csv.writer(stream)
        writer.writerow(['role_level','floor_1_target','floor_2_target','floor_3_target'])
        for level in range(20,500):
            writer.writerow([level]+[guild_secret.target_power(level,f,rules) for f in (1,2,3)])
    samples=[]
    for level in (20,40,60,80,99,100,200,300,499):
        state={'instances':{},'random_serial':0}
        key=guild_secret.choose({'level':level},state,rules,[])
        npc=npc_players.get(key)
        for floor in (1,2,3):
            units=guild_combat.player_units(npc['role'])
            samples.append(dict(enemy_npc=key,**guild_secret.scale(units,level,floor,rules)))
    payload=dict(revision=rules['revision'],score='0.2*hp + 3*attack + 2.5*defense + 1.5*magic; floor per unit; excludes essence and temporary triggers',samples=samples)
    (out/'sample_units.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    for level in (20,40,60,80,99,100,200,300,499):
        rows=[s for s in samples if s['role_level']==level]
        print('|',level,'|',' | '.join(f"{s['target_power']:,}（{s['attribute_power']:,}）" for s in rows),'|')


if __name__=='__main__':main()
