"""Compare the old transport-induced stop with complete simulation on a read-only save copy."""
import argparse
import copy
import json
from pathlib import Path
import random
import sqlite3
import sys
import time
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import guild,guild_combat,journey,combat_engine,summon


def read_role(account):
    with sqlite3.connect(f'file:{ROOT}/.runtime/offline/game.sqlite3?mode=ro',uri=True) as db:
        row=db.execute('SELECT data FROM roles WHERE account=?',(account,)).fetchone()
    if not row:raise ValueError('Account does not exist')
    return json.loads(row[0])


def compare(original,seeds=range(3)):
    gr=guild.load_rules();jr=journey.load_rules();native=journey.battle
    native_can=combat_engine.Battle.can_act
    report=[];fixtures={}
    def old_limit(self):
        if len(self.actions)>=self.limit:self.actions.stop_reason='action_limit';return False
        if self.event_bytes>=self.policy['event_budget_bytes']:self.actions.stop_reason='event_budget';return False
        return True
    for task,npc in sorted(original['guild']['instances'].get('task_opponents',{}).items()):
        for seed in seeds:
            pair=dict(task=int(task),npc=npc,seed=seed)
            for variant in ('before','after'):
                role=copy.deepcopy(original);s,g=guild.prepare(role,int(time.time()),gr);captured={};rng=random.Random(seed)
                def battle(owner,cfg,rules,**kw):
                    rules=copy.deepcopy(rules)
                    rules['battle']['max_actions']=60 if variant=='before' else jr['battle']['max_actions']
                    rules['battle']['mechanics']['event_budget_bytes']=1000 if variant=='before' else jr['battle']['mechanics']['event_budget_bytes']
                    result,lineup,actions=native(owner,cfg,rules,**kw)
                    captured.update(result=result,actions=len(actions),rounds=max([a['cur_round'] for a in actions],default=0),
                        events=len(actions.events),event_bytes=len(summon.lua(combat_engine.event_data(actions,1)).encode()),
                        stop_reason=actions.stop_reason,final_hp=actions.final_hp)
                    return result,lineup,actions
                with patch('network_redirect.journey.battle',side_effect=battle),patch('network_redirect.combat_engine.Battle.can_act',old_limit if variant=='before' else native_can),patch('secrets.randbelow',side_effect=rng.randrange):
                    _,packets,replay=guild_combat.simulate(role,s,gr,jr,28,'仙盟任务守卫',enemy_npc=npc)
                captured['packet_max_bytes']=max(map(len,packets));captured['packet_count']=len(packets)
                pair[variant]=captured
                fixtures[f'{task}:{seed}:{variant}']=replay
            report.append(pair)
    return report,fixtures


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--account',required=True)
    args=parser.parse_args();role=read_role(args.account);rows,fixtures=compare(role)
    report=dict(read_only_save=True,modified_player_resources=False,seeded_comparisons=len(rows),checks=rows,
        reproduced=any(r['before']['stop_reason']=='event_budget' and r['after']['stop_reason']=='elimination' for r in rows),
        incomplete_results_never_win=all(r['after']['result']==0 for r in rows if r['after']['stop_reason']=='action_limit'))
    destination=ROOT/'analysis/evidence/combat/current_termination_audit.json';destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'.runtime/combat-audit-fixtures.json').write_text(json.dumps(fixtures,ensure_ascii=False))
    print(json.dumps(dict(reproduced=report['reproduced'],checks=len(rows),report=str(destination)),ensure_ascii=False))


if __name__=='__main__':main()
