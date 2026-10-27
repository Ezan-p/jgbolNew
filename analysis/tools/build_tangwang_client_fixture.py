"""Generate detached native-card fixtures; never touch a real account."""
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from network_redirect import activity, activity_tangwang as tw, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode


def main():
    now=1792814400
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time',return_value=now):
        b=Backend(Path(tmp),18770,lambda *a,**k:None);role=b.profile();r=b.activity_rules
        activity.prepare(role,now,r)
        with patch.object(tw,'randbelow',side_effect=[0,20,40,52]):status=tw.status(role,now,r)
        for lv in range(1,9):
            for _ in range(3):tw.card(role,lv)
        cards=[i.copy() for i in role['attachments'] if tw.is_card(i)]
        locked=tw.card(role,1);locked['is_lock']=1;cards.append(locked.copy())
        ids=[next(c['id'] for c in cards if c['level']==lv) for lv in (1,2,3,4)]
        with patch.object(tw,'randbelow',return_value=99):
            reward=login_fields(decode(tw.settle(role,dict(count=4,card_list=[dict(id=i) for i in ids]),now,r)[0])[2]['data'])
        f=dict(now=now,status=status,cards=cards,reward=reward)
        f['next_week']=tw.status(role,status['tangwang_info']['next_weekly_refresh'],r)
        f['new_cards']=[i.copy() for i in role['attachments'] if tw.is_card(i)]
        b.close()
    source='local FIXTURE='+summon.lua(f)+'\n'+(ROOT/'analysis/tools/tangwang_client_harness.lua').read_text().replace('-- INSTALL_PATCH',(ROOT/'network_redirect/tangwang_client.lua').read_text())
    path=ROOT/'.runtime/tangwang-native-fixture.lua';path.write_text(source);print(path)

if __name__=='__main__':main()
