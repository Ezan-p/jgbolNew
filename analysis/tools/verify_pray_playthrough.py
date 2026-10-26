"""Exercise an isolated account through original wire messages; never edit live saves."""
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


def main():
    now = 1792814400
    serial = 100000
    steps = []
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time', return_value=now):
        backend = Backend(Path(tmp), 18770, lambda *a, **k: None)
        try:
            r = backend.profile()
            r.update(level=15, spirit_retain=0, pray_spirit_times=0)
            two = next(t for t, row in formation.BASES.items() if int(row['quality']) == 2)
            three = next(t for t, row in formation.BASES.items() if int(row['quality']) == 3)
            c = summon.companion(r, three); r['corteges'].append(c)
            r['souls'] = {str(two): 400, str(three): 241, '5004': 252}
            formation.prepare(r, backend.formation_rules)
            activity.prepare(r, now, backend.activity_rules)
            backend.save(r)

            def request(name, rows, cost):
                nonlocal serial
                before = backend.profile()
                serial += 1
                packet = encode(1085, dict(serial_num=serial, object_count=len(rows), object_list=rows))
                reply = backend.respond(packet, {'authenticated': True})
                events = [(d['id'], login_fields(d['data'])) for m, _, d in map(decode, reply) if m == 2998]
                assert not any(e == 55 for e, _ in events), events
                reward = next(d['pray_item_list'][1] for e, d in events if e == 52)
                after = backend.profile()
                assert reward['object_type'] == 11 and reward['attach_count'] in (10, 20, 30)
                assert after['gold_coin'] - before['gold_coin'] == reward['attach_count']
                assert backend.respond(packet, {'authenticated': True}) == reply
                assert backend.profile() == after
                steps.append(dict(name=name, cost=cost, gold=reward['attach_count'],
                                  completed=after['pray_spirit_times'], retained=after['spirit_retain']))
                return after

            def row(kind, ident, count=1):
                return dict(object_type=kind, object_id=ident, count=count)

            r = request('二星魂魄祈福', [row(10, two, 200)], 200)
            assert r['spirit_retain'] == 0
            r = request('三星神仙与魂魄混合祈福', [row(4, c['id']), row(10, three, 241)], 500)
            assert r['spirit_retain'] == 0
            assert all(i.get('innate_owner_id') != c['id'] for i in r['attachments'])
            r = request('五星魂魄手动选择与留存', [row(10, 5004, 252)], 1000)
            assert r['spirit_retain'] == 1016
            backend.close()
            backend = Backend(Path(tmp), 18770, lambda *a, **k: None)
            assert backend.profile() == r
            r = request('重启后第四次仅使用留存', [], 1000)
            assert r['spirit_retain'] == 16
            with patch('network_redirect.backend.time.time', return_value=now + 86400):
                r = request('次日重置费用并保留结余', [row(10, two, 200)], 200)
            assert r['pray_spirit_times'] == 1 and r['spirit_retain'] == 16
            assert r['achievements']['totals']['109'] == 1
        finally:
            backend.close()
    report = dict(ok=True, isolated_save=True, native_soul_type=10, steps=steps,
                  assertions=['real wire encode/decode', 'gold conservation', 'innate spell removal',
                              'same-request replay', 'restart persistence', 'day rollover', 'achievement 109'])
    out = ROOT / 'analysis/evidence/pray/playthrough.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
