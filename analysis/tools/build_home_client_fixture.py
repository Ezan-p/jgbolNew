"""Generate disposable native-UI fixtures; never reads or writes a real save."""
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect.backend import Backend, login_fields
from network_redirect import activity, activity_home as home, summon
from network_redirect.protocol import decode


def main():
    with tempfile.TemporaryDirectory() as tmp:
        backend=Backend(Path(tmp),18770,lambda *a,**k:None)
        try:
            role=backend.profile();role['level']=60;now=1792987200
            activity.prepare(role,now,backend.activity_rules)
            def data(op):
                packet=home.settle(role,dict(id=op,data='{flag=1}'),now,backend.activity_rules,backend.journey_rules,login_fields)[0]
                return login_fields(decode(packet)[2]['data'])
            text='local HOME_PATCH='+summon.lua((ROOT/'network_redirect/home_client.lua').read_text())
            text+='\nlocal HOME_FIXTURE='+summon.lua(data(24))+'\nlocal HOME_SHOP='+summon.lua(data(14))+'\n'
            text+=(ROOT/'analysis/tools/home_client_harness.lua').read_text()
            path=ROOT/'.runtime/home-native-fixture.lua';path.parent.mkdir(exist_ok=True);path.write_text(text)
            print(path)
        finally:backend.close()

if __name__=='__main__':main()
