"""Isolated, original-wire 天缘 playthrough; no live account mutation."""
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_convert as cv, formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
OUT = ROOT / 'analysis/evidence/convert'
NOW = 1792987200  # 2026-10-26 12:00 UTC+8


def main():
    serial = 100000
    steps = []
    with tempfile.TemporaryDirectory() as tmp, patch('network_redirect.backend.time.time', return_value=NOW):
        b = Backend(Path(tmp), 18770, lambda *a, **k: None)
        try:
            r = b.profile(); r.update(level=60, vip_level=3, gold_coin=1000)
            for c in r['corteges']: c['level'] = 100
            r['corteges'].append(summon.companion(r, 5011))
            r['souls'] = {'5009': formation.COMPOSE[5] - 3}
            activity.prepare(r, NOW, b.activity_rules); b.save(r)

            def request(name, mid, expected=True, **data):
                nonlocal serial
                serial += 1
                before = b.profile()
                packet = encode(mid, dict(serial_num=serial, **data))
                reply = b.respond(packet, {'authenticated': True})
                decoded = [decode(p) for p in reply]
                events = [(d['id'], login_fields(d['data'])) for m, _, d in decoded if m == 2998]
                assert (not any(e == 55 for e, _ in events)) == expected, events
                after = b.profile()
                if not expected: assert after == before
                assert b.respond(packet, {'authenticated': True}) == reply
                assert b.profile() == after
                steps.append(dict(name=name, accepted=expected, used=after['convert_fight_count'],
                                  gold=after['gold_coin'], souls=after.get('souls', {}),
                                  receipt=after['activity'].get('convert_last_result')))
                return decoded

            with patch.object(cv, 'draw', side_effect=[[2, 3], [1, 1], [3, 2], [2, 1], [1, 5]]):
                native = request('首战免费胜利并获得目标魂魄', 1026, fight_type=10, des_value=5011)
            fixture = [[m, d] for m, _, d in native if m in (1028, 1027) or m == 2998 and d['id'] == 70]
            (ROOT / '.runtime/convert-wire-fixture.lua').write_text('return ' + summon.lua(fixture))
            request('魂魄合成目标神仙', 1083, type_id=5009)
            request('无魂缘丹拒绝且不扣次数', 1026, False, fight_type=10, des_value=5011)
            request('常驻集市购买魂缘丹', 1057, page_id=2, index=16, type_id=1024, count=1)
            with patch.object(cv, 'draw', return_value=[3, 2]):
                request('道具挑战消耗1颗并返还2颗', 1026, fight_type=10, des_value=5011)
            with patch.object(cv, 'draw', return_value=[1, 1]):
                request('继续挑战获得来源魂魄', 1026, fight_type=10, des_value=5011)
            request('VIP3每日3次用完', 1026, False, fight_type=10, des_value=5011)
            saved = b.profile(); b.close(); b = Backend(Path(tmp), 18770, lambda *a, **k: None)
            assert b.profile() == saved
            request('重启后恢复上次选择', 1205, flag=1)
            with patch('network_redirect.backend.time.time', return_value=NOW + 86400):
                request('次日再次免费', 1026, fight_type=10, des_value=5011)
                assert b.profile()['convert_fight_count'] == 1
            assert b.profile()['achievements']['totals']['106'] == 1
        finally:
            b.close()
    report = dict(ok=True, isolated_save=True, real_combat=True,
                  fixture_setup='level60, companions level100; controlled draw for three reward categories',
                  steps=steps, same_session_replay_checked=True, restart_persistence_checked=True)
    (OUT / 'playthrough.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('天缘 original-wire playthrough: 9 steps passed')


if __name__ == '__main__': main()
