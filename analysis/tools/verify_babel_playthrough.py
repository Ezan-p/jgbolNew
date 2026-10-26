"""60-floor real-combat wire playthrough on a disposable catalog army, no stat boosts."""
import copy
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity, activity_babel as babel, activity_babel_npc as npc, npc_players, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


def main():
    now=1792987200; serial=100000; trace=[]; session=dict(authenticated=True)
    key=max(npc_players.catalog(),key=lambda k:npc_players.catalog()[k]['profile']['role_combat_power'])
    with tempfile.TemporaryDirectory() as tmp:
        backend=Backend(Path(tmp),18770,lambda *a,**k:None)
        role=backend.profile(); identity=role['role_id']; role.update(copy.deepcopy(npc_players.get(key)['role']))
        role.update(role_id=identity,role_name='通天塔通关验证',gold_coin=100000,silver_coin=100000)
        # Only prepaid consumables are seeded; all army stats and enemies are
        # unchanged catalog data. This tests progression, not acquisition time.
        summon.add_item(role,20019,10)
        activity.prepare(role,now,backend.activity_rules); backend.save(role)
        def request(op,**data):
            nonlocal serial
            serial+=1
            with patch('network_redirect.backend.time.time',return_value=now):
                packets=backend.respond(encode(1353,dict(serial_num=serial,id=op,data=summon.lua(data))),session)
            decoded=list(map(decode,packets))
            events=[(d['id'],login_fields(d['data'])) for mid,_,d in decoded if mid==2998]
            assert not any(e==55 for e,_ in events),(op,data,events)
            assert decoded[-1][0]==1106
            return decoded
        def move(row,col):
            s=backend.profile()['activity']['babel']
            if s['energy']<=1:request(10,item_type=20019,count=1)
            if s['life']<30:request(11)
            return request(2,target_pos=dict(row=row,column=col))
        request(1); request(3)
        # Explore the full first floor, including all keys/boxes, both tools,
        # obstacles and all three colored guards; then use a short route.
        path=((1,2),(1,3),(1,4),(1,5),(2,5),(1,5),(1,4),(1,3),(2,3),(2,4),
              (1,4),(1,3),(1,2),(2,2),(3,2),(3,3),(3,4),(4,4),(4,3),(4,2),
              (4,3),(4,4),(4,5),(4,6),(4,7),(5,7),(5,8))
        short=((2,1),(3,1),(4,1),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(4,6),(4,7),(5,7),(5,8))
        for floor in range(1,61):
            wins=0; actions=0
            for row,col in path if floor==1 else short:
                packets=move(row,col)
                replay=next((d for mid,_,d in packets if mid==1027),None)
                if replay:
                    assert 1<=replay['final_result']<=3,(floor,replay['final_result'])
                    assert replay['fight_type']==200
                    assert all(len(x['damage_list'])==8 for x in replay['fight_result'])
                    wins+=1; actions+=replay['fight_round']
            s=backend.profile()['activity']['babel']
            assert s['cur_floor']==min(60,floor+1)
            trace.append(dict(floor=floor,wins=wins,actions=actions,life=s['life'],energy=s['energy'],
                              coins=s['coin_count'],master=npc.choose(floor,9)))
            if floor%10==0:print(f'passed {floor}/60',flush=True)
            if floor==30:
                snapshot=backend.profile(); backend.close()
                backend=Backend(Path(tmp),18770,lambda *a,**k:None)
                assert snapshot==backend.profile()
        s=backend.profile()['activity']['babel']; assert s['complete']
        before=s['coin_count']; move(5,7); move(5,8)
        assert backend.profile()['activity']['babel']['coin_count']==before
        request(8); request(4,index=2,count=5); request(9); request(4,index=2,count=1)
        request(7,floor=1); request(3)
        rank=npc.ranking(backend.profile(),backend.profile()['activity']['babel'],now,backend.activity_rules)
        assert rank['my_top']['order']==1
        now=npc.start(s['week']+1,backend.activity_rules); request(1); request(3)
        role=backend.profile(); mail=next(v for k,v in role['welfare']['mails'].items() if k.startswith('babel-rank-'))
        serial+=1
        with patch('network_redirect.backend.time.time',return_value=now):
            packets=backend.respond(encode(1103,dict(serial_num=serial,mail_id=mail['mail_id'],flag=1)),session)
        assert backend.profile()['welfare']['mails'][mail['delivery_key']]['claimed']
        request(8)
        result=dict(passed=True,date='2026-10-26',army=key,stat_boosts=False,seeded_consumables={'20019':10},
                    seeded_gold=100000,floors=60,wins=sum(v['wins'] for v in trace),requests=serial-100000,
                    restart_at_floor=30,full_first_floor=True,terminal_repeat_safe=True,weekly_mail_claimed=True,
                    balance_claim=False,steps=trace)
        backend.close()
    out=ROOT/'analysis/evidence/babel'; out.mkdir(parents=True,exist_ok=True)
    (out/'playthrough.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='steps'},ensure_ascii=False))


if __name__=='__main__':main()
