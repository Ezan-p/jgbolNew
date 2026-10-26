"""Exercise all home progression through native packets in a disposable save."""
import copy
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import npc_players, summon, activity_home as h
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


def main():
    now=1792987200  # 2026-10-26 noon UTC+8
    report=dict(date='2026-10-26',native_ui_verified=False,fixture='temporary account with funded materials and catalog combat lineup',battles=[])
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time',side_effect=lambda:now):
        b=Backend(Path(tmp),18770,lambda *a,**k:None); serial=900000; client={'authenticated':True}
        try:
            r=b.profile()
            entry=max((e for e in npc_players.catalog().values() if e['profile']['level']==99),key=lambda e:e['profile']['role_combat_power'])
            npc=npc_players.get(entry['npc_id'])['role']
            for key in ('corteges','attachments','level'):
                r[key]=copy.deepcopy(npc[key])
            r.update(gold_coin=1000000,silver_coin=2000000000)
            for tid in (1361,1362,1363,1364,1365,1345):summon.add_item(r,tid,400000 if tid==1364 else 100000)
            b.save(r)
            def request(op,**data):
                nonlocal serial
                serial+=1; packets=[decode(p) for p in b.respond(encode(1348,dict(serial_num=serial,id=op,data=summon.lua(data))),client)]
                errors=[login_fields(d['data']) for mid,_,d in packets if mid==2998 and d['id']==55]
                assert not errors,(op,data,errors)
                if op==25:
                    fight=next(d for mid,_,d in packets if mid==1027)
                    assert 1<=fight['final_result']<=3,fight
                    report['battles'].append(dict(result=fight['final_result'],actions=fight['fight_round']))
                return next(login_fields(d['data']) for mid,_,d in packets if mid==1348 and d['id']==op)
            request(1)
            for lv in range(1,21):
                # Test funding only; building levels always change through 1348/2.
                r=b.profile();r['silver_coin']=2000000000;b.save(r)
                for typ in h.KEYS:request(2,building_type=typ)
                if lv in (11,20):
                    request(25);request(26)
            report['final_home']=request(1)['base_data']
            assert report['final_home']['level']==3 and report['final_home']['point']==56250
            assert b.profile()['cortege_limit_plus']==100
            for lv in range(12):request(9,plant_grid=1)
            request(3,plant_grid=1,seed_type=1);request(8,hour=24)
            ids=list(request(13)['friend_data'])
            for fid in ids[:5]:request(5,friend_id=fid)
            request(6,friend_id=ids[0]);request(7,friend_id=ids[0],plant_grid=1)
            request(12,friend_id=ids[0],chat_msg='洞府通关验证')
            request(1)
            request(20,train_type=1,consume_type=1,use_count=10)
            for typ in range(1,5):
                while True:
                    tr=b.profile()['activity']['home']['train'][str(typ)]
                    if tr['level']==40:break
                    remaining=sum(int(h.TRAIN[typ,lv]['need_experience']) for lv in range(tr['level']+1,41))-tr['cur_exp']
                    request(20,train_type=typ,consume_type=3,use_count=min(1000,(remaining+199)//200))
            report['training_levels']={k:v['level'] for k,v in b.profile()['activity']['home']['train'].items()}
            request(21,pet_id=b.profile()['activity']['home']['pets'][0]['id'],des_type=202)
            request(15,shop_page=1,item_index=2,buy_count=1)
            for day in range(7):
                request(11)
                if day==0:
                    now+=23*3600
                    gain=request(10,plant_grid=1)
                    assert gain['prize_list'][1]['attach_count']==1640,gain
                    report['harvest']=gain
                    now+=3600
                else:now+=86400
            all_data=request(24,flag=1)['all_activity']
            for main,groups in all_data[72].items():
                for idx,row in groups['target_list'].items():
                    if row['status']==2:request(24,flag=2,act_type=72,main_type=main,index=idx)
            request(24,flag=2,act_type=69)
            for idx in range(4):request(24,flag=2,act_type=70,index=idx)
            mails=[m for k,m in b.profile()['welfare']['mails'].items() if k.startswith('home-race-')]
            assert len(mails)==1
            report['weekly_mail']=dict(title=mails[0]['mail_title'],prizes=mails[0]['prizes'])
            saved=b.profile();b.close();b=Backend(Path(tmp),18770,lambda *a,**k:None)
            assert saved==b.profile()
            report.update(persistent_restart=True,requests=serial-900000,pet_type=saved['activity']['home']['pets'][0]['type_id'],
                          neighbours=len(ids),goals_claimed=len(saved['activity']['home']['welfare']['claims']))
        finally:b.close()
    out=ROOT/'analysis/evidence/home';out.mkdir(exist_ok=True)
    (out/'playthrough.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
