"""81-floor real-wire campaign: unchanged catalog army, earned money and crafted drugs only."""
import copy
import argparse
import json
from pathlib import Path
import random
import sys
import tempfile
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity, activity_abyss as ab, activity_drug as drug
from network_redirect import activity_abyss_combat as essence, npc_players, summon, combat
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--army',default='npc_v1_l99_t1_attack')
    parser.add_argument('--floors',type=int,default=81)
    args=parser.parse_args();assert 1<=args.floors<=81
    key=args.army;now=1793160000;serial=800000;trace=[];crafts=[]
    rng=random.Random(281028)
    with tempfile.TemporaryDirectory() as tmp, patch.object(combat.secrets,'randbelow',side_effect=rng.randrange):
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        role=b.profile();identity=role['role_id'];role.update(copy.deepcopy(npc_players.get(key)['role']))
        role.update(role_id=identity,role_name='九幽真实资源验证',gold_coin=0,silver_coin=0,drug_level=1,drug_exp=0,
                    drug_study_flag=0,drug_study_flag2=0)
        role['activity']={}
        banned=set(ab.PILLS)|set(essence.DRUGS)|set(drug.MATERIALS)|set(range(1431,1452))
        role['attachments']=[x for x in role['attachments'] if not (x['attach_type']==5 and x['type_id'] in banned)]
        activity.prepare(role,now,b.activity_rules);b.save(role)
        def request(mid=1329,op=None,**data):
            nonlocal serial
            serial+=1
            payload=dict(id=op,data=summon.lua(data)) if mid==1329 else data
            packet=encode(mid,dict(serial_num=serial,**payload))
            with patch('network_redirect.backend.time.time',return_value=now):raw=b.respond(packet,dict(authenticated=True))
            decoded=list(map(decode,raw))
            events=[(d['id'],login_fields(d['data'])) for mid,_,d in decoded if mid==2998]
            assert not any(i==55 for i,d in events),(mid,op,data,events)
            # Exact retransmission must not spend resources or grant rewards twice.
            before=b.profile()
            with patch('network_redirect.backend.time.time',return_value=now):again=b.respond(packet,dict(authenticated=True))
            assert again==raw and b.profile()==before
            return next((d for i,d in events if i==173 and d['flag']==op),None),decoded
        def count(tid):
            return sum(x['count'] for x in b.profile()['attachments'] if x['attach_type']==5 and x['type_id']==tid)
        def use_xp():
            if b.profile()['drug_level']>=36:return
            items=[dict(type_id=tid,count=count(tid)) for tid in range(1442,1452) if count(tid)]
            if items:request(1059,first_send=True,flag=3,cortege_id=0,roll_count=len(items),roll_list=items)
        def craft(idx):
            row=drug.RECIPES[idx]
            for part,token in enumerate(row['study_material(attach_type|attach_count|need_silver)'].split('/'),1):
                tid,n,_=map(int,token.split('|'));missing=max(0,n-count(tid))
                if missing:request(op=23,index1=idx,index2=part,count=missing)
            result,_=request(op=21,index=idx);tid=result['drug_item'][1]['attach_type']
            crafts.append(dict(floor=b.profile()['activity']['abyss']['boss'],recipe=idx,item=tid,level=b.profile()['drug_level']))
            return tid
        request(op=1);use_xp()
        for idx in (1,6,11,16):request(op=20,index=idx)
        assert b.profile()['gold_coin']==0 and b.profile()['drug_level']==4
        for floor in range(1,args.floors+1):
            if b.profile()['activity']['abyss']['boss_count']>=5:
                now+=86400;request(op=1)
                if b.profile()['activity']['abyss']['bag']:request(op=5)
                use_xp()
            state=b.profile()['activity']['abyss'];assert state['boss']==floor
            # Choose the strongest learned recipe in each ordinary family.
            for slot in range(1,5):
                profile=b.profile();state=profile['activity']['abyss']
                eligible=[idx for idx in state['recipes'] if int(drug.RECIPES[idx]['type'])==slot and
                          int(drug.RECIPES[idx]['min_level'])<=profile['drug_level']]
                idx=max(eligible,key=lambda i:int(drug.RECIPES[i]['attach_type']))
                tid=craft(idx);request(op=17,index=slot,type_id=tid)
            for slot in (5,6):
                profile=b.profile();state=profile['activity']['abyss'];before=essence.effects(ab.BOSSES[floor],state['pills'])
                candidates=[i for i in state['recipes'] if int(drug.RECIPES[i]['type'])==5 and int(drug.RECIPES[i]['min_level'])<=profile['drug_level']]
                if not candidates:continue
                def score(i):
                    tid=int(drug.RECIPES[i]['attach_type'])+60
                    return sum(essence.effects(ab.BOSSES[floor],dict(state['pills'],**{str(slot):tid})).values())
                idx=min(candidates,key=score)
                if score(idx)>=sum(before.values()):continue
                tid=craft(idx);after=essence.effects(ab.BOSSES[floor],dict(state['pills'],**{str(slot):tid}))
                if any(after[k]<v for k,v in before.items()):request(op=17,index=slot,type_id=tid)
            result,decoded=request(op=6)
            profile=b.profile();entry=dict(floor=floor,win=result['is_win'],silver=profile['silver_coin'],gold=profile['gold_coin'],
                crystals=profile['activity']['abyss']['crystals'],drug_level=profile['drug_level'],time=now)
            trace.append(entry)
            assert result['is_win'],entry
            assert any(mid==1028 for mid,_,d in decoded) and any(mid==1027 for mid,_,d in decoded)
            request(op=2,des_area=min(81,floor+1))
            if floor%9==0:print(entry,flush=True)
            if floor==40:
                saved=b.profile();b.close();b=Backend(Path(tmp),18770,lambda *a,**k:None)
                assert saved==b.profile()
        assert bool(b.profile()['activity']['abyss'].get('complete'))==(args.floors==81)
        rank,_=request(op=7,top_type=1)
        if args.floors==81:assert rank['my_top']['order']==1
        now+=3600;request(op=10);request(op=5)
        shop,_=request(op=13);request(op=12,index=1,count=1,shop_day=shop['shop_day'],shop_revision=shop['shop_revision'])
        report=dict(passed=True,date='2026-10-28',army=key,initial_gold=0,initial_silver=0,initial_drug_level=1,
                    preloaded_medicines=False,player_stat_boost=False,forced_victories=False,random_seed=281028,
                    floors=args.floors,days=1+(trace[-1]['time']-trace[0]['time'])//86400,requests=serial-800000,
                    duplicate_replay_every_request=True,restart_floor=40 if args.floors>=40 else None,final_rank=rank['my_top'],steps=trace,crafts=crafts,
                    caveat='Endgame catalog equipment is pre-existing. This verifies activity resources, not whole-game army acquisition time.')
        b.close()
    name='progression_repaired_20261028' if args.floors==81 else 'entry_'+key+'_20261028'
    out=ROOT/('analysis/evidence/abyss/'+name+'.json')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('steps','crafts')},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
