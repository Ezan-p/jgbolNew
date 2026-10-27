"""Build isolated Caishen native fixtures; never read or write live accounts."""
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import activity_spring as spring, activity_caishen as cs, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode


def main():
    now=1792814400
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None);role=b.profile();r=b.activity_rules
        with patch.object(cs,'randbelow',return_value=0):status=spring.status(role,now,r)
        summon.add_item(role,1028,10000)
        def result(mid,req):return login_fields(decode(cs.settle(role,mid,req,now,r)[0])[2]['data'])
        f=dict(now=now,status=status,visit=result(1210,dict(flag=1)),
               exchange=result(1211,dict(prize_id=status['visit_caishen']['prize_list'][0]['prize_id'],count=1)))
        f['shops']=[]
        for idx in range(5):
            role['activity']['seasonal']['spring'].pop('shop')
            with patch.object(cs,'randbelow',side_effect=[0,0,0,0,idx]):f['shops'].append(spring.status(role,now,r))
        f['tomorrow']=spring.status(role,status['visit_caishen']['next_daily_refresh'],r)
        f['next_week']=spring.status(role,status['visit_caishen']['next_weekly_refresh'],r)
        b.close()
    source='local FIXTURE='+summon.lua(f)+'\n'+(ROOT/'analysis/tools/caishen_client_harness.lua').read_text().replace('-- INSTALL_PATCH',(ROOT/'network_redirect/caishen_client.lua').read_text())
    path=ROOT/'.runtime/caishen-native-fixture.lua';path.write_text(source);print(path)

if __name__=='__main__':main()
