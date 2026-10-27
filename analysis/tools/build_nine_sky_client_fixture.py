"""Generate real native response tables from an isolated account."""
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import activity_nine_sky as n, summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import decode


def main():
    now=int(time.time())
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None);role=b.profile();role['level']=60;role['gold_coin']=1000000
        def req(op,**data):
            if op==4:
                snapshot=n.snapshot(role['activity']['nine_sky'])
                data.update(shop_day=snapshot['shop_day'],shop_revision=snapshot['shop_revision'])
            return login_fields(decode(n.settle(role,dict(id=op,data=summon.lua(data)),now,login_fields)[0])[2]['data'])
        f=dict(now=now,status=n.status(now),entry=req(1))
        f['single']=req(2,count=1,index=0)
        f['after_single']=req(1)
        cfg=n.load_rules();cfg['treasure_basis_points']=10000;cfg['double_basis_points']=10000;cfg['battle_basis_points']=0
        rewards=[row['reward'] for row in cfg['treasure_pool']]
        with patch.object(n,'load_rules',return_value=cfg), patch.object(n,'treasure',side_effect=(rewards*3)[:10]):
            f['ten']=req(2,count=10,index=1)
        f['palace']=req(1)
        index=role['activity']['nine_sky']['palace_count']
        f['palace_buy']=req(5,buy_type=1,index=1,count=1,shop_index=index)
        f['card_buy']=req(5,buy_type=2,index=1,count=1,shop_index=index)
        s=role['activity']['nine_sky'];s['stars']=10000;s['credits']=500;s['cards']={'50':2,'200':2,'500':2}
        f['rich']=req(1);f['big']=req(3,buy_type=1,first_send=True);f['small']=req(3,buy_type=2,first_send=True)
        f['big_buy']=req(4,buy_type=1,index=1,count=1,card_list={200:1})
        f['small_buy']=req(4,buy_type=2,index=1,count=1)
        f['floors']=[];s['palaces']={}
        for floor in range(1,10):
            s.update(floor=floor,steps=sum(n.LEVELS[:floor-1]),cur_map=0,cur_point=dict(x=0,y=0))
            f['floors'].append(req(1))
        now=n.snapshot(s)['next_daily_refresh']
        f['daily_big']=req(3,buy_type=1,first_send=True)
        b.close()
    source='local FIXTURE='+summon.lua(f)+'\n'+(ROOT/'analysis/tools/nine_sky_client_harness.lua').read_text().replace('-- INSTALL_PATCH',(ROOT/'network_redirect/nine_sky_client.lua').read_text())
    path=ROOT/'.runtime/nine-sky-native-fixture.lua';path.write_text(source);print(path)

if __name__=='__main__':main()
