"""Build original mondayUI callback fixtures from detached temporary saves."""
import copy
import sys
import tempfile
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_monday as m, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode


def main():
    now=int(time.time());r=m.load_rules()
    day,weekday,_=m.calendar(now,r)
    monday=(day-(weekday-1))*86400-r['timezone_offset_hours']*3600+43200
    sunday=monday-86400
    def unpack(packet):return login_fields(decode(packet)[2]['data'])
    with tempfile.TemporaryDirectory() as tmp:
        b=Backend(Path(tmp),18770,lambda *a,**k:None);role=b.profile()
        fixtures=dict(closed=m.snapshot(role,sunday,r))
        fixtures['refresh']=unpack(m.settle(role,1243,dict(index=1),sunday)[0])
        role['activity']['monday']['task']['finish_time']=sunday
        fixtures['task']=m.snapshot(role,sunday,r)
        fixtures['claim']=unpack(m.settle(role,1219,dict(flag=2,level=0,op_type=0),sunday)[0])
        fixtures['open']=m.snapshot(role,monday,r)
        fixtures['opening_claim']=unpack(m.settle(role,1219,dict(flag=2,level=0,op_type=0),monday)[0])
        fixtures['buy']=unpack(m.settle(role,1219,dict(flag=3,level=1,op_type=0),monday)[0])
        fixtures['catalog']=[]
        for index,row in enumerate(r['slots']):
            for entry in row['pool']:
                for spec in m.candidates(entry):
                    preview=copy.deepcopy(role)
                    preview['activity']['monday']['goods'][index]=spec
                    fixtures['catalog'].append(m.snapshot(preview,monday,r))
        fixtures['next']=m.snapshot(role,monday+86400,r)
        b.close()
    text='local FIXTURE='+summon.lua(fixtures)+'\n'+(ROOT/'analysis/tools/monday_client_harness.lua').read_text()
    path=ROOT/'.runtime/monday-native-fixture.lua';path.write_text(text);return path

if __name__=='__main__':print(main())
