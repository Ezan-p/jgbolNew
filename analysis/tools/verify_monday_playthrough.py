"""Three-week real-protocol playthrough, all nine actual task sources."""
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import summon, activity_monday as m
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


def main():
    start=1792987200-6*86400 # Tuesday before 2026-10-26
    steps=[]; tasks=set(); bought=set(); serial=200000
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time',return_value=start) as clock:
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        role=b.profile();role.update(level=60,vip_level=1,gold_coin=100000,silver_coin=1000000,strength=1000,energy=1000)
        for c in role['corteges']:c.update(level=100,culture_point=1000)
        if not any(c['type']==5020 for c in role['corteges']):role['corteges'].append(summon.companion(role,5020))
        summon.add_item(role,1001,100);summon.add_item(role,1024,100);b.save(role)
        def request(mid,expected=True,**data):
            nonlocal serial
            serial+=1;before=b.profile();packet=encode(mid,dict(serial_num=serial,**data))
            replies=b.respond(packet,{'authenticated':True})
            events=[(v['id'],login_fields(v['data'])) for code,_,v in map(decode,replies) if code==2998]
            errors=[v for eid,v in events if eid==55]
            assert bool(errors)!=expected,(mid,data,errors)
            after=b.profile()
            if not expected:assert after==before
            assert b.respond(packet,{'authenticated':True})==replies
            assert b.profile()==after
            steps.append(dict(day=m.calendar(int(clock.return_value),m.load_rules())[1],mid=mid,
                              request=data,accepted=expected,jade=after['activity']['monday']['jade']))
            return events
        def call(flag=1,level=0,expected=True):return request(1219,expected,op_type=0,flag=flag,level=level)
        for day in range(22):
            clock.return_value=start+day*86400
            call();state=b.profile()['activity']['monday'];weekday=m.calendar(int(clock.return_value),m.load_rules())[1]
            if day==21:break
            if weekday==1:
                call(2);call(2,expected=False)
                for index in (1,2,3) if day==6 else (1,2,3,4):
                    call(3,index);bought.add(index)
                request(1243,False,index=1)
            else:
                for i in range(1,5):request(1243,index=i)
                request(1243,False,index=1)
                kind=state['task']['cur_task'];tasks.add(kind)
                if kind in (1,9):request(1026,fight_type=1,des_type=1,des_id=101)
                elif kind in (2,4):
                    request(1029,flag=1)
                    board=b.profile()['activity']['rape_boards'][0]
                    typ,targets=next((t,v) for t,v in board['form_list'].items() if v);ident=next(iter(targets))
                    request(1026,fight_type=3,des_type=int(typ),des_value=1,des_id=int(ident))
                elif kind==3:
                    request(1043,flag=0);request(1043,flag=0,plus_type=1,plus_index=1)
                    request(1026,fight_type=5,des_type=1,des_value=1)
                elif kind==5:request(1029,flag=2)
                elif kind==6:
                    cid=b.profile()['corteges'][0]['id']
                    request(1081,cortege_id=cid,train_type=1,intensive=False)
                    request(1082,cortege_id=cid,confirm=False)
                elif kind==7:request(1030,visit_index=1,op_type=1)
                elif kind==8:request(1026,fight_type=10,des_value=5020)
                assert b.profile()['activity']['monday']['task']['finish_time'],kind
                call(2);call(2,expected=False);call(3,1,False)
            if day==8:
                before=b.profile();b.close();b=Backend(Path(tmp),18770,lambda *a,**k:None)
                assert b.profile()==before
        mails=[v for k,v in b.profile()['welfare']['mails'].items() if k.startswith('monday-recycle-')]
        assert len(mails)==1 and mails[0]['prizes']==[[12,0,40000,1]],mails
        request(1103,mail_id=mails[0]['mail_id'])
        assert tasks==set(range(1,10)),tasks
        assert bought=={1,2,3,4}
        assert b.profile()['achievements']['totals']['125']==1
        b.close()
    out=ROOT/'analysis/evidence/monday';out.mkdir(exist_ok=True)
    (out/'playthrough.json').write_text(json.dumps(dict(passed=True,temporary_database=True,
        gameplay_resources_seeded=True,jade_seeded=False,real_combat=True,days=22,
        nine_task_sources=sorted(tasks),four_slots_exchanged=sorted(bought),requests=len(steps),
        replayed_every_packet=True,restart_verified=True,recycle_mail_verified=True,steps=steps),ensure_ascii=False,indent=2)+'\n')
    print(f'{len(steps)} requests, nine actual task sources, three Mondays, recycle and restart passed')

if __name__=='__main__':main()
