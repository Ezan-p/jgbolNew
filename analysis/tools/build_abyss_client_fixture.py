"""Generate disposable packets for detached original Cocos UI validation."""
import copy
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity, activity_abyss as abyss, activity_abyss_random as events, activity_treasure as maps, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode


def main():
    now=1792987200
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None)
        role=b.profile();role.update(level=80,gold_coin=100000,drug_level=36)
        activity.prepare(role,now,b.activity_rules)
        s=abyss.state(role,now,b.activity_rules);s.update(boss=81,layer=81)
        s=abyss.state(role,now+3600,b.activity_rules)
        fixtures={}
        for op in (1,7,9,10,13,16):
            packet=abyss.settle(role,dict(id=op,data='{}'),now+3600,b.activity_rules,b.journey_rules,login_fields)[0]
            fixtures[str(op)]=login_fields(decode(packet)[2]['data'])
        for region in range(1,10):
            s.update(boss=1+(region-1)*9,layer=1+(region-1)*9)
            fixtures['region'+str(region)]={}
            for op in (1,16):
                packet=abyss.settle(role,dict(id=op,data='{}'),now+3600,b.activity_rules,b.journey_rules,login_fields)[0]
                fixtures['region'+str(region)][str(op)]=login_fields(decode(packet)[2]['data'])
        s.update(boss=81,layer=81)
        for kind in range(1,6):
            s['events']=[events.create(kind,b.activity_rules)]
            packet=events.settle(role,s,dict(op_type=0),now+3600,b.activity_rules,b.journey_rules)[0]
            fixtures['event'+str(kind)]=login_fields(decode(packet)[2]['data'])
        summon.add_item(role,1431,2)
        for label,data in (('map',dict(op_type=1,type_id=1431)),('map_draw',dict(op_type=2,type_id=1431,index_list=[1,2]))):
            fixtures[label]=login_fields(decode(maps.settle(role,s,3,data,now+3600,b.activity_rules)[0])[2]['data'])
        b.close()
    script='local FIXTURE='+summon.lua(fixtures)+'\n'
    script+='local ABYSS_PATCH='+summon.lua((ROOT/'network_redirect/abyss_client.lua').read_text())+'\n'
    script+=(ROOT/'analysis/tools/abyss_client_harness.lua').read_text()
    out=ROOT/'.runtime/abyss-native-fixture.lua';out.write_text(script)
    print(out)


if __name__=='__main__':main()
