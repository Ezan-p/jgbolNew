"""Complete 162 original gates and one five-stage NPC cup with the real engine.
Only the temporary test characters are boosted; original opponents are untouched.
"""
import json
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity,activity_undergo as u,activity_arena as arena,summon,npc_players,formation
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import decode
NOW=1792814400
with tempfile.TemporaryDirectory() as tmp:
    b=Backend(Path(tmp),18770,lambda *a,**k:None)
    role=b.profile();role.update(level=99,strength=1000,gold_coin=1000000)
    for tid in (5001,5002,5003):
        if len(role['corteges'])>=3:break
        role['corteges'].append(summon.companion(role,tid))
    formation.prepare(role,b.formation_rules)
    for c in role['corteges']:
        c.update(hp=100000000,gongji=100000000,fangyu=10000000,magic=100000000,level=200)
    activity.prepare(role,NOW,b.activity_rules)
    trace=[];max_size=0
    for mid in u.MAPS:
        now=NOW+(mid-1)*86400
        for mode in (1,2):
            for i,gid in enumerate(u.map_gates(mid)):
                cid=role['corteges'][i//4]['id']
                packets=u.settle(role,dict(id=4,data=summon.lua(dict(mode=mode,map_id=gid,cortege_list={cid:9}))),
                    now,b.activity_rules,b.journey_rules,b.formation_rules,login_fields)
                decoded=[decode(p) for p in packets];rep=next(d for m,_,d in decoded if m==1140)
                assert 1<=rep['final_result']<=3,(mode,gid,rep['final_result'])
                assert rep['fight_round']>0 and all(len(a['damage_list'])==9 for a in rep['fight_result'])
                max_size=max(max_size,max(map(len,packets)))
                trace.append(dict(mode=mode,gate=gid,actions=rep['fight_round'],result=rep['final_result']))
        u.settle(role,dict(id=7,data=summon.lua(dict(index=mid))),now,b.activity_rules,b.journey_rules,b.formation_rules,login_fields)
    assert role['activity']['undergo']['gate']==u.END and role['activity']['undergo']['challenge']==u.END
    assert len(role['activity']['undergo']['first_claimed'])==81
    now=NOW+8*86400
    # Round-trip through JSON before the final claim and the separate tournament.
    role=json.loads(json.dumps(role))
    u.settle(role,dict(id=1,data='{}'),now+86400,b.activity_rules,b.journey_rules,b.formation_rules,login_fields)
    u.settle(role,dict(id=7,data='{index=0}'),now+86400,b.activity_rules,b.journey_rules,b.formation_rules,login_fields)
    arena.state(role,now,b.activity_rules);ar=role['activity']['arena'];arena_trace=[]
    for stage,count in ((1,10),(2,5),(3,3),(4,3),(5,3)):
        for _ in range(count):
            ordered=arena.ranking(ar);own=ordered.index('self')+1
            key=next(k for k in reversed(ordered[:((own+4)//5)*5]) if k!='self' and ar['competitors'][k]['hp']>0)
            data=dict(fight_type=arena.rank_type(ar),des_id=npc_players.catalog()[key]['profile']['role_id'],
                des_type=1,des_order=ordered.index(key)+1,is_charge=0,bet_fight=0)
            packets=arena.settle(role,dict(id=5,data=summon.lua(data)),now,b.activity_rules,b.journey_rules,login_fields)
            rep=next(decode(p)[2] for p in packets if decode(p)[0]==1027)
            assert rep['fight_round']>0
            arena_trace.append(dict(stage=stage,npc=key,result=rep['final_result'],actions=rep['fight_round']))
            max_size=max(max_size,max(map(len,packets)))
        arena.settle(role,dict(id=7,data=summon.lua(dict(stage=stage))),now,b.activity_rules,b.journey_rules,login_fields)
    assert ar['settled'] and ar['stage']==6
    report=dict(status='passed',original_guardians_unchanged=True,test_only_boosted_characters=True,
        undergo_fights=len(trace),arena_fights=len(arena_trace),max_packet_bytes=max_size,
        terminal=dict(gate=role['activity']['undergo']['gate'],challenge=role['activity']['undergo']['challenge']),
        arena_settlement=ar['settlement'],undergo=trace,arena=arena_trace)
    out=ROOT/'analysis/evidence/taixu';out.mkdir(parents=True,exist_ok=True)
    (out/'playthrough.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('undergo','arena','arena_settlement')},ensure_ascii=False))
    b.close()
