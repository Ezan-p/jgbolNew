"""Build real server payloads against a disposable Rulai account."""
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_rulai as r, summon
from network_redirect.backend import Backend,login_fields
from network_redirect.protocol import decode


def main():
    now=int(time.time())
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None);role=b.profile();role['level']=60
        def req(op):
            return login_fields(decode(r.settle(role,dict(id=op,data='{}'),now)[0])[2]['data'])
        f=dict(now=now,times=r.schedule(now,r.load_rules()),entry=req(0))
        r.record_charge(role,3000,now)
        f['charged']=req(0);f['sync']=login_fields(decode(r.sync(role,now))[2]['data'])
        f['draws']=[]
        for i in range(1,9):
            with patch.object(r,'draw',return_value=i):f['draws'].append(req(1))
        f['bonus']=req(2);f['claimed']=req(0)
        b.close()
    source='assert(loadstring('+summon.lua(summon.client_source(summon.load_rules()))+'))\n'
    source+='local FIXTURE='+summon.lua(f)+'\n'+(ROOT/'analysis/tools/rulai_client_harness.lua').read_text().replace('-- INSTALL_PATCH',(ROOT/'network_redirect/rulai_client.lua').read_text())
    path=ROOT/'.runtime/rulai-native-fixture.lua';path.write_text(source);print(path)

if __name__=='__main__':main()
