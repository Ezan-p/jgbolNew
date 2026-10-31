"""70-floor plus five secret runs real-combat wire playthrough on a disposable catalog army, no stat boosts."""
import copy
import json
from collections import deque
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
    now=1792987200; serial=100000; trace=[]; secret_trace=[]; active_secret=False; session=dict(authenticated=True)
    key=max(npc_players.catalog(),key=lambda k:npc_players.catalog()[k]['profile']['role_combat_power'])
    with tempfile.TemporaryDirectory() as tmp:
        backend=Backend(Path(tmp),18770,lambda *a,**k:None)
        role=backend.profile(); identity=role['role_id']; role.update(copy.deepcopy(npc_players.get(key)['role']))
        role.update(role_id=identity,role_name='通天塔通关验证',gold_coin=100000,silver_coin=100000)
        # Only prepaid consumables are seeded; all army stats and enemies are
        # unchanged catalog data. This tests progression, not acquisition time.
        summon.add_item(role,20019,10)
        summon.add_item(role,1377,5)
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
            if active_secret:
                return request(13,target_pos=dict(row=row,column=col))
            if s['energy']<=1:request(10,item_type=20019,count=1)
            if s['life']<30:request(11)
            return request(2,target_pos=dict(row=row,column=col))
        request(1); request(3)
        # Explore the full first floor, including all keys/boxes, both tools,
        # obstacles and all three colored guards. Find routes from saved maps,
        # so the early random floors exercise the same protocol as fixed ones.
        def route(typ):
            s=backend.profile()['activity']['babel']
            if active_secret:s=s['secret_run']
            grid=s['floors'][str(s['cur_floor'])]
            target=next(((r,c) for r,line in enumerate(grid,1) for c,cell in enumerate(line,1)
                         if cell['elem_type']==typ),None)
            if target is None:return []
            start=(s['locale']['row'],s['locale']['column'])
            pending=deque([(start,[])]); seen={start}
            while pending:
                (row,col),path=pending.popleft()
                if (row,col)==target:return path
                for r,c in ((row-1,col),(row+1,col),(row,col-1),(row,col+1)):
                    if (1<=r<=5 and 1<=c<=8 and (r,c) not in seen and
                            ((r,c)==target or grid[r-1][c-1]['elem_type'] not in (*babel.TOOLS,3))):
                        seen.add((r,c)); pending.append(((r,c),path+[(r,c)]))
            raise AssertionError(('unreachable',s['cur_floor'],typ))
        for floor in range(1,babel.MAX_FLOOR+1):
            wins=0; actions=0
            targets=(20005,20006,20010,20011,20012,20013,20014,20015,
                     20003,20004,20007,20008,20009,9,3) if floor==1 else (9,3)
            for typ in targets:
                for row,col in route(typ):
                    packets=move(row,col)
                    replay=next((d for mid,_,d in packets if mid==1027),None)
                    if replay:
                        assert 1<=replay['final_result']<=3,(floor,replay['final_result'])
                        assert replay['fight_type']==200
                        assert all(len(x['damage_list'])==8 for x in replay['fight_result'])
                        wins+=1; actions+=replay['fight_round']
            s=backend.profile()['activity']['babel']
            assert s['cur_floor']==min(babel.MAX_FLOOR,floor+1)
            trace.append(dict(floor=floor,wins=wins,actions=actions,life=s['life'],energy=s['energy'],
                              coins=s['coin_count'],master=npc.choose(floor,9)))
            if floor%10==0:print(f'passed {floor}/{babel.MAX_FLOOR}',flush=True)
            if floor==30:
                snapshot=backend.profile(); backend.close()
                backend=Backend(Path(tmp),18770,lambda *a,**k:None)
                assert snapshot==backend.profile()
        s=backend.profile()['activity']['babel']; assert s['complete']
        before=s['coin_count']; move(5,7); move(5,8)
        assert backend.profile()['activity']['babel']['coin_count']==before
        # Paid native group entrances and all three floors, with real guards.
        normal_before=copy.deepcopy(backend.profile()['activity']['babel'])
        active_secret=True
        for entrance in (1001,1004,1007,1010,1013):
            request(14,floor=entrance)
            for floor in range(entrance,entrance+3):
                wins=0
                for typ in (20005,20006,20010,20011,20012,20013,20014,20015,
                            20003,20004,20007,20008,20009,9,3):
                    for row,col in route(typ):
                        packets=move(row,col)
                        replay=next((d for mid,_,d in packets if mid==1027),None)
                        if replay:
                            assert 1<=replay['final_result']<=3,(floor,replay['final_result'])
                            wins+=1
                run=backend.profile()['activity']['babel']['secret_run']
                assert run['cur_floor']==min(entrance+2,floor+1)
                assert (run['life'],run['energy'])==(100,100)
                secret_trace.append(dict(floor=floor,wins=wins))
            assert run['complete']
            print(f'passed secret {entrance}..{entrance+2}',flush=True)
        active_secret=False
        normal_after=backend.profile()['activity']['babel']
        for field in ('cur_floor','history_floor','life','energy','floors','complete'):
            assert normal_after[field]==normal_before[field],field
        assert babel.item_count(backend.profile(),1377)==0
        request(8); request(4,index=2,count=1); request(9); request(4,index=2,count=1)
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
        result=dict(passed=True,date='2026-10-31',army=key,stat_boosts=False,seeded_consumables={'20019':10},
                    seeded_gold=100000,floors=babel.MAX_FLOOR,secret_floors=secret_trace,seeded_secret_tickets=5,wins=sum(v['wins'] for v in trace),requests=serial-100000,
                    restart_at_floor=30,full_first_floor=True,terminal_repeat_safe=True,weekly_mail_claimed=True,
                    balance_claim=False,steps=trace)
        backend.close()
    out=ROOT/'analysis/evidence/babel_hotupdate'; out.mkdir(parents=True,exist_ok=True)
    (out/'playthrough.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='steps'},ensure_ascii=False))


if __name__=='__main__':main()
