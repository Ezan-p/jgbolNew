"""Build native UI fixtures from temporary-role 1030 responses; no live grants."""
import sys
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity_visit as v, summon
from network_redirect.backend import login_fields
from network_redirect.protocol import decode, encode


def main():
    rules=v.load_rules()
    def response(role,index,op):
        return login_fields(decode(v.settle(role,dict(visit_index=index,op_type=op),rules)[0])[2]['data'])
    role=dict(activity={'visits':{}},attachments=[],silver_coin=0,gold_coin=0)
    fixture=dict(query=response(role,0,1),skills=sorted(t for pool in v.SKILLS.values() for t in pool),scratch=[])
    # Put the spell in a continuation packet, as in a large real inventory.
    fixture['inventory_prefix'] = decode(encode(1035, dict(first_send=True, attach_count=128,
        attach_list=[dict(id=10000+i, attach_type=5, type_id=1001, count=1, level=1)
                     for i in range(128)])))[2]
    for tid in fixture['skills']:
        role=dict(activity={'visits':{}},attachments=[],silver_coin=0,gold_coin=0)
        with patch.object(v,'draw_shou',return_value=[6,tid,1,1]):
            draw=response(role,3,1)
        claim=response(role,3,2)
        inventory=decode(encode(1035,dict(first_send=False,attach_count=len(role['attachments']),
                                        attach_list=role['attachments'])))[2]
        fixture['scratch'].append(dict(draw=draw,claim=claim,inventory=inventory))
    role=dict(activity={'visits':{}},attachments=[],silver_coin=0,gold_coin=0)
    with patch.object(v,'draw_fu',return_value=[5,v.EQUIPMENT[4][0],1,1]): fixture['fu']=response(role,1,1)
    with patch.object(v.secrets,'randbelow',return_value=5): fixture['lu']=response(role,2,1)
    fixture['lu_claim']=response(role,2,2)
    path=ROOT/'.runtime/visit-native-fixture.lua'
    path.write_text('local FIXTURE='+summon.lua(fixture)+'\n'+(ROOT/'analysis/tools/visit_client_harness.lua').read_text().replace('-- INSTALL_PATCH', (ROOT/'network_redirect/visit_client.lua').read_text()))
    print(path)

if __name__=='__main__':main()
