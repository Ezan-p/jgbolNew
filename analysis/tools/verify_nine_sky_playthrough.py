"""Play from sky1 to sky9 using real Backend packets and disposable storage."""
import json
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import decode,encode
from network_redirect import summon


def main():
    now=int(time.time());history=[];serial=100000
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time',return_value=now):
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        role=b.profile();role.update(level=60,gold_coin=100000,silver_coin=100000);b.save(role)
        wire={'authenticated':True}
        def request(op=1,**args):
            nonlocal serial
            if op==4:
                saved=b.profile()['activity']['nine_sky']
                args.update(shop_day=saved['shop_day'],shop_revision=saved['shop_revision'])
            serial+=1;packet=encode(1309,dict(serial_num=serial,id=op,data=summon.lua(args)))
            result=b.respond(packet,wire);events=[(d['id'],login_fields(d['data'])) for mid,_,d in map(decode,result) if mid==2998]
            assert not any(e==55 for e,_ in events),events
            data=next(d for e,d in events if e==164)
            history.append(dict(operation=op,args=args,snapshot=data['local_snapshot']))
            return data
        request()
        while b.profile()['activity']['nine_sky']['floor']<9:
            s=b.profile()['activity']['nine_sky']
            request(2,count=1 if s['free_times'] else 10,index=0 if s['free_times'] else 1)
            assert len(history)<700
        request(3,buy_type=1,first_send=True)
        request(4,buy_type=1,index=1,count=1,card_list={})
        before=b.profile();b.close()
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        assert b.profile()==before
        request()
        state=b.profile()['activity']['nine_sky']
        report=dict(passed=True,requests=len(history),rolls=state['rolls'],steps=state['steps'],floor=state['floor'],
                    stars=state['stars'],gold_spent=100000-b.profile()['gold_coin'],
                    restart_preserved=True,star_shop_reward=state['shop'][0]['reward'],
                    battle_count=state.get('battle_count',0),battle_wins=state.get('battle_wins',0),
                    live_account_modified=False,temporary_starting_gold=100000,history=history)
        b.close()
    out=ROOT/'analysis/evidence/nine_sky/playthrough.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='history'},ensure_ascii=False))

if __name__=='__main__':main()
