"""Build East Sea native-client fixtures without touching live accounts."""
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import activity_fish as fish, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode


def main():
    now=1792814400
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None);role=b.profile();role['gold_coin']=1000000
        r=b.activity_rules
        with patch.object(fish,'randbelow',side_effect=[0]*5):status=fish.status(role,now,r)
        summon.add_item(role,1027,10000)
        def req(tid,count=1):return login_fields(decode(fish.settle(role,dict(type_id=tid,count=count),now,r)[0])[2]['data'])
        f=dict(now=now,status=status,single=req(0),ten=req(0,10),exchange=req(1007))
        f['shops']=[]
        for idx in range(6):
            role['activity']['seasonal']['fish'].pop('shop')
            with patch.object(fish,'randbelow',side_effect=[0,0,0,0,idx]):f['shops'].append(fish.status(role,now,r))
        f['tomorrow']=fish.status(role,status['search_gold_data']['next_daily_refresh'],r)
        f['next_week']=fish.status(role,status['search_gold_data']['next_weekly_refresh'],r)
        b.close()
    source='local FIXTURE='+summon.lua(f)+'\n'+(ROOT/'analysis/tools/fish_client_harness.lua').read_text().replace('-- INSTALL_PATCH',(ROOT/'network_redirect/fish_client.lua').read_text())
    path=ROOT/'.runtime/fish-native-fixture.lua';path.write_text(source);print(path)

if __name__=='__main__':main()
