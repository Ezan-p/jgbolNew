"""Create temporary-account response fixtures for original Cocos widgets."""
import sys
import tempfile
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_pavilion as p, summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import decode


def main():
    now=int(time.time())
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        role=b.profile(); r=p.load_rules()
        p.record_charge(role,10000,now)
        summon.add_item(role,1141,3000)
        def req(flag,index=0,count=0,ten_card=0,five_card=0):
            return login_fields(decode(p.settle(role,dict(flag=flag,index=index,count=count,ten_card=ten_card,five_card=five_card),now)[0])[2]['data'])
        fixtures=dict(entry=req(1),status=p.status(role,now),exchange=req(2,3,2),gift=req(3,1))
        b.close()
    script='local FIXTURE='+summon.lua(fixtures)+'\n'+(ROOT/'analysis/tools/pavilion_client_harness.lua').read_text().replace('-- INSTALL_PATCH', (ROOT/'network_redirect/pavilion_client.lua').read_text().replace('__PAVILION_TABLES__',summon.lua(p.client_tables())))
    path=ROOT/'.runtime/pavilion-native-fixture.lua';path.write_text(script)
    print(path)

if __name__=='__main__':main()
