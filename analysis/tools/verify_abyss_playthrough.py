"""81-floor wire progression: catalog army plus explicit test-only growth bonuses."""
import copy
import itertools
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity, activity_abyss as abyss, activity_abyss_combat as combat, npc_players, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


def main():
    trace=[];now=1792987200;serial=100000;session=dict(authenticated=True)
    key=max(npc_players.catalog(),key=lambda k:npc_players.catalog()[k]['profile']['role_combat_power'])
    with tempfile.TemporaryDirectory() as tmp:
        backend=Backend(Path(tmp),18770,lambda *a,**k:None)
        role=backend.profile();identity=role['role_id']
        role.update(copy.deepcopy(npc_players.get(key)['role']))
        role.update(role_id=identity,role_name='九幽通关验证',gold_coin=1000000,silver_coin=1000000,drug_level=36)
        # This fixture tests all floors/rewards/protocols, not time-to-progression
        # balance. Only the disposable player's growth is boosted. Original
        # enemies, medicines, damage calculation and outcomes stay untouched.
        for unit in role['corteges']:
            if unit.get('order'):
                for stat,value in (('hp_plus',10000000),('gongji_plus',1000000),('magic_plus',1000000)):
                    unit[stat]=unit.get(stat,0)+value
        activity.prepare(role,now,backend.activity_rules)
        for tid in (1644,1648,1652,1656,1657,1658,1659,1660):summon.add_item(role,tid,200)
        backend.save(role)
        def request(op,**data):
            nonlocal serial
            serial+=1
            with patch('network_redirect.backend.time.time',return_value=now):
                raw=backend.respond(encode(1329,dict(serial_num=serial,id=op,data=summon.lua(data))),session)
            decoded=list(map(decode,raw))
            events=[(d['id'],login_fields(d['data'])) for mid,_,d in decoded if mid==2998]
            assert not any(e==55 for e,_ in events),(op,data,events)
            return next(d for e,d in events if e==173 and d['flag']==op),decoded
        request(1)
        rank,_=request(7,top_type=1);assert len(rank['top_data'])==20
        for layer in range(1,82):
            if backend.profile()['activity']['abyss']['boss_count']>=5:now+=86400
            for slot,tid in enumerate((1644,1648,1652,1656),1):request(17,index=slot,type_id=tid)
            raw=combat.effects(abyss.BOSSES[layer],{})
            # Choose two useful essence medicines, retaining the exact source
            # reductions. No alteration of enemy stats or battle outcomes.
            pair=min(itertools.product(range(1657,1661),repeat=2),
                     key=lambda pair:sum(combat.effects(abyss.BOSSES[layer],dict(enumerate(pair,5))).values()))
            pills={}
            for slot,tid in enumerate(pair,5):
                reduced=combat.effects(abyss.BOSSES[layer],dict(pills,**{str(slot):tid}))
                if any(reduced[k]<v for k,v in raw.items()):
                    request(17,index=slot,type_id=tid);pills[str(slot)]=tid;raw=reduced
            before=backend.profile()['activity']['abyss']['crystals']
            result,packets=request(6)
            fight=next(d for mid,_,d in packets if mid==1027)
            state=backend.profile()['activity']['abyss']
            trace.append(dict(layer=layer,win=result['is_win'],actions=fight['fight_round'],
                              crystals=state['crystals']-before,pills=pills,time=now))
            assert result['is_win'],trace[-1]
            assert fight['fight_type']==26
            request(2,des_area=min(81,layer+1))
            if layer%9==0:print(f'passed {layer}/81',flush=True)
            if layer==40:
                snapshot=backend.profile();backend.close()
                backend=Backend(Path(tmp),18770,lambda *a,**k:None)
                assert snapshot==backend.profile()
        assert backend.profile()['activity']['abyss']['complete']
        rank,_=request(7,top_type=1);assert rank['my_top']['layer']==81 and rank['my_top']['order']==1
        # Completion does not stop hanging, claiming, shopping or daily rewards.
        now+=3600;request(10);request(5);request(12,index=1,count=1)
        now+=86400;request(1)
        assert any(k.startswith('abyss-rank-') for k in backend.profile()['welfare']['mails'])
        result=dict(passed=True,date='2026-10-26',army=key,floors=81,wins=len(trace),requests=serial-100000,
                    simulated_days=1+(trace[-1]['time']-trace[0]['time'])//86400,
                    source='Original boss CSV; real combat engine; temporary database; preloaded catalog army and medicines.',
                    fixture_growth_per_fielded_unit=dict(hp_plus=10000000,gongji_plus=1000000,magic_plus=1000000),
                    balance_claim=False,
                    restart_at_floor=40,final_rank=rank['my_top'],steps=trace)
        backend.close()
    out=ROOT/'analysis/evidence/abyss';out.mkdir(parents=True,exist_ok=True)
    (out/'playthrough.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='steps'},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
