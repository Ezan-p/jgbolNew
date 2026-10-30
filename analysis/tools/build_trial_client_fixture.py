"""Generate native UI fixtures from disposable backend state, never live inventory."""
import copy
import sys
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_trial as trial, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


def main():
    now = int(time.time())
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time', return_value=now):
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        role = b.profile()
        role['level'] = 20
        activity.prepare(role, now, b.activity_rules)
        with patch.object(trial.secrets, 'choice', return_value=5022), patch.object(trial.secrets, 'randbelow', return_value=0):
            trial.encounter(role, now, b.activity_rules)
        b.save(role)
        serial = 100000
        def req(mid, **data):
            nonlocal serial
            serial += 1
            packets = b.respond(encode(mid, dict(serial_num=serial, **data)), dict(authenticated=True))
            rows = [decode(p) for p in packets]
            events = [login_fields(d['data']) for m, _, d in rows if m == 2998 and d['id'] == 75]
            assert not any(m == 2998 and d['id'] == 55 for m, _, d in rows), rows
            return events[0], [[m, d] for m, _, d in rows if m in (1027, 1028) or m == 2998 and d['id'] in (75, 121)]
        f = dict(now=now, pool=trial.POOL)
        f['entry'], _ = req(1064, flag=2)
        f['fight'], f['wire'] = req(1026, fight_type=11, des_type=8, des_id=5022)
        # Native UI kill/claim paths use a separately prepared dead disposable boss.
        role = b.profile()
        role['activity']['trial_bosses'][0].update(hp=0, is_dead=True)
        b.save(role)
        f['dead'], _ = req(1064, flag=2)
        f['claim'], _ = req(1064, flag=9)
        f['complete'], _ = req(1064, flag=2)
        f['kill'] = copy.deepcopy(f['fight'])
        f['kill']['result'] = 7
        f['kill']['train_data']['hp'] = 0
        role = b.profile()
        for tid, roll in [(5022,0),(5001,70),(5045,95)]:
            with patch.object(trial.secrets, 'choice', return_value=tid), patch.object(trial.secrets, 'randbelow', side_effect=[0,roll]):
                trial.encounter(role, now, b.activity_rules)
        for boss,count in zip(role['activity']['trial_bosses'],(10,0,3)):
            boss['train_times']=count
        b.save(role)
        f['multiple'], _ = req(1064, flag=2)
        b.close()
    f['pool'] = list(f['pool'])
    source = 'local FIXTURE=' + summon.lua(f) + '\n'
    source += (ROOT / 'analysis/tools/trial_client_harness.lua').read_text().replace(
        '-- INSTALL_PATCH', (ROOT / 'network_redirect/trial_client.lua').read_text())
    path = ROOT / '.runtime/trial-native-fixture.lua'
    path.write_text(source)
    print(path)


if __name__ == '__main__':
    main()
