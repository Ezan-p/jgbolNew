"""Play through a whole local hunt week with real packets and earned scores."""
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_hunt as h, activity_hunt_geometry as g
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode


def main():
    start=1792944000  # Monday 2026-10-26 00:00 UTC+8
    requests=shots=clears=traps=earned=0;days=[];clock=start+3600
    with tempfile.TemporaryDirectory() as tmp,patch('network_redirect.backend.time.time',side_effect=lambda:clock):
        b=Backend(Path(tmp),18770,lambda *a,**k:None);role=b.profile();role['level']=60;b.save(role)
        def req(flag,count=0,index=0):
            nonlocal requests
            requests+=1
            packets=b.respond(encode(1226,dict(serial_num=100000+requests,flag=flag,count=count,index=index)),dict(authenticated=True))
            events=[decode(p)[2] for p in packets if decode(p)[0]==2998]
            assert not any(v['id']==55 for v in events),events
            return next(login_fields(v['data']) for v in events if v['id']==155)
        for d in range(7):
            clock=start+d*86400+3600;req(1)
            while True:
                s=b.profile()['activity']['hunt'];choices=[]
                for ball,row in h.BALLS.items():
                    if row['need_energy']>s['energy']:continue
                    for angle in range(30,151):
                        move,caught=g.trace(s['points'],angle,row['bump_times'],30)
                        base=sum(h.SOULS[s['points'][i]['soul_type']]['soul_value'] for i in caught)
                        gain=base+base*min(100,10*max(0,len(caught)-1))//100
                        choices.append((gain/row['need_energy'],gain,-row['need_energy'],ball,angle))
                if not choices:break
                _,gain,_,ball,angle=max(choices)
                if gain==0 and s['refreshes']<3:req(4);continue
                out=req(2,ball,angle)['move_result'];shots+=1;earned+=out['base_soul']+out['extra_soul']
                clears+=out['board_cleared'];traps+=out['trap_hit']
            s=b.profile()['activity']['hunt'];days.append(dict(day=d+1,score=s['day_score'],shots=s['shots'],energy=s['energy']))
            for flag in (5,8,9,12,13):req(flag)
        s=b.profile()['activity']['hunt'];assert s['week_score']==earned and s['soul']==earned
        clock=start+7*86400+3600;rank=req(10);weekly_rank=rank['my_order']['order']
        if rank['had_prize']:req(11);assert req(10)['had_got_prize']
        # Spend only earned currency; one purchase, one energy exchange, both survive restart.
        req(6,1,1);req(3,1)
        before=b.profile();b.close();b=Backend(Path(tmp),18770,lambda *a,**k:None)
        assert b.profile()==before
        report=dict(passed=True,requests=requests,shots=shots,board_clears=clears,trap_hits=traps,
                    earned_soul=earned,weekly_rank=weekly_rank,weekly_claimed=rank['had_prize'],days=days,
                    persistent_restart=True,production_save_changed=False,
                    note='Temporary level60 account; no injected energy, soul, scores or rewards; aim chosen by server geometry search.')
        b.close()
    out=ROOT/'analysis/evidence/hunt';out.mkdir(parents=True,exist_ok=True)
    (out/'playthrough.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
