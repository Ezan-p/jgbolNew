"""Disposable hunt account and native event payloads; no live DB mutations."""
import sys
import tempfile
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_hunt as h, summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import decode


def main():
    now=int(time.time())
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None);role=b.profile();role['level']=60
        ar=b.activity_rules;s=h.state(role,now,ar);s['soul']=100000
        s['points']=[dict(x=0,y=180,soul_type=1),dict(x=0,y=280,soul_type=2),dict(x=300,y=400,soul_type=5)]
        def req(flag,count=0,index=0):
            return login_fields(decode(h.settle(role,dict(flag=flag,count=count,index=index),now,ar)[0])[2]['data'])
        fixtures=dict(now=now,status=h.status(role,now,ar),entry=req(1),shot=req(2,1,90),
                      exchange=req(3,10),refresh=req(4),shop=req(5),buy=req(6,2,1),store_refresh=req(7))
        for flag in (8,9,10,12,13):fixtures['rank'+str(flag)]=req(flag)
        rows,mine=h.ranking(role,s,'week',s['week']-1,100000,h.load_rules())
        s['last_week']=dict(period=s['week']-1,top_list=rows,my_order=mine,prizes=h.rewards('week',1),claimed=False)
        fixtures['winner']=req(10);fixtures['prize']=req(11)
        b.close()
    script='local FIXTURE='+summon.lua(fixtures)+'\n'+(ROOT/'analysis/tools/hunt_client_harness.lua').read_text()
    path=ROOT/'.runtime/hunt-native-fixture.lua';path.write_text(script);print(path)


if __name__=='__main__':main()
