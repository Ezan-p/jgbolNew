"""Build isolated anniversary payloads without touching a live account."""
import copy
import sys
import tempfile
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity_yuanshi as y, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode


def main():
    now = int(time.time())
    with tempfile.TemporaryDirectory() as tmp:
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        role = b.profile(); role.update(level=60, gold_coin=100000)
        def req(flag, index=0):
            return login_fields(decode(y.settle(role, dict(flag=flag, index=index), now)[0])[2]['data'])
        f = dict(now=now, config=y.client_config(now), entry=req(0), wish=req(2))
        s = role['activity']['yuanshi']; s['offering_stock'] = 1
        f['shop'] = req(3); f['buy'] = req(4, 1)
        s['progress'] = 100
        f['ready'] = req(0); f['claim'] = req(2); f['soul'] = req(2)
        y.record_charge(role, 500, now)
        f['charged'] = req(0); f['gift'] = req(1, 1)
        s['activated'] = [s['day'] - 4 + i for i in range(5)]
        s['gift_counts'] = [1] * 5
        f['all_gifts'] = req(0)
        b.close()
    patch = (ROOT/'network_redirect/yuanshi_client.lua').read_text()
    source = 'assert(loadstring(' + summon.lua(summon.client_source(summon.load_rules())) + '))\n' + 'local FIXTURE=' + summon.lua(f) + '\n' + (ROOT/'analysis/tools/yuanshi_client_harness.lua').read_text().replace('-- INSTALL_PATCH', patch)
    path = ROOT/'.runtime/yuanshi-native-fixture.lua'; path.write_text(source)
    print(path)


if __name__ == '__main__': main()
