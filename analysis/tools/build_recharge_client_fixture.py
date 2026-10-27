"""Build the isolated native gold-card checkout regression; no live role writes."""
import json
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import recharge,summon,welfare
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import encode,decode
import time


def fixture():
    rules=recharge.load_rules()
    data=dict(products=rules['products'],large_count=100,small_count=100,large_rmb=50,small_rmb=5,
              last_order_id='',month=dict(rmb=50,daily_gold=100,expires_at=0,last_claim_at=0),
              single=dict(start_time=0,end_time=2140000000,max_rmb=50,
                          rows=[dict(index=1,rmb=50,status=2,prize_list=[dict(object_type=11,attach_type=0,attach_count=50,attach_level=1)])]))
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),1,lambda *a,**k:None)
        role=b.profile();role['level']=60;summon.add_item(role,1156,9);b.save(role)
        now=int(time.time())
        initial=login_fields(decode(welfare.query(role,now,b.welfare_rules))[2]['data'])
        packets=b.respond(encode(1111,dict(serial_num=1,event_id=251,data=summon.lua(dict(
            item_id=202,order_id='native-fund-checkout',large_count=0,small_count=9)))),dict(authenticated=True))
        purchase=[d for mid,_,d in map(decode,packets) if mid==2998 and d['id']==80]
        packets=b.respond(encode(1127,dict(serial_num=2,flag=2,act_type=22,index=0)),dict(authenticated=True))
        claimed=[d for mid,_,d in map(decode,packets) if mid==2998 and d['id'] in (80,127)]
        flow=dict(initial=initial,purchase=purchase,claimed=claimed)
        b.close()
    source='local FIXTURE='+summon.lua(data)+'\nlocal FUND_FLOW='+summon.lua(flow)+'\n'+(ROOT/'tests/recharge_client_regression.lua').read_text()
    return source.replace('-- INSTALL_PATCH',(ROOT/'network_redirect/vip_client.lua').read_text()+'\n'+(ROOT/'network_redirect/welfare_client.lua').read_text())

if __name__=='__main__':
    path=ROOT/'analysis/evidence/recharge/client_fixture.lua'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(fixture())
    print(path)
