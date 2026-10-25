import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect.backend import Backend, login_fields
from network_redirect import role_profile as p, summon
from network_redirect.protocol import encode, decode

NOW = 1792900800

class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = patch('network_redirect.backend.time.time', return_value=NOW)
        self.clock.start(); self.addCleanup(self.clock.stop)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.addCleanup(self.b.close)
        self.serial = 1000
        r = self.b.profile(); r.update(level=60, gold_coin=1000)
        summon.add_item(r, 1005, 3); self.b.save(r)

    def request(self, mid, **data):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **data))
        self.replies = self.b.respond(self.packet, dict(authenticated=True))
        return [(m, d) for m, _, d in map(decode, self.replies)]

    def event(self, out, event):
        return next(login_fields(d['data']) for m, d in out if m == 2998 and d['id'] == event)

    def test_query_flags_and_contract(self):
        for flag in (1, 2):
            out = self.request(1307, flag=flag)
            self.assertEqual(self.event(out, 159)['role_info']['union_name'], '')
            title = next(d for m, d in out if m == 1077)
            self.assertTrue({1, 2, 3}.issubset({t['id'] for t in title['titles']}))
            self.assertLess(next(i for i, x in enumerate(out) if x[0] == 1077), next(i for i, x in enumerate(out) if x[0] == 2998))
            self.assertEqual(out[-1][0], 1106)
        self.event(self.request(1307, flag=0), 55)

    def test_rename_consume_replay_restart(self):
        out = self.request(1031, new_name='齐天大圣')
        self.assertEqual(self.event(out, 12), {'result': 1, 'new_name': '齐天大圣'})
        before = self.b.profile()
        self.assertEqual(sum(i['count'] for i in before['attachments'] if i['type_id'] == 1005), 2)
        self.assertEqual(self.b.respond(self.packet, dict(authenticated=True)), self.replies)
        self.assertEqual(self.b.profile(), before)
        other = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        try: self.assertEqual(other.profile()['role_name'], '齐天大圣')
        finally: other.close()

    def test_rename_failures_atomic(self):
        for name, code in [('天', 4), ('一二三四五六七八', 5), ('abc', 3), ('本地行者', 6)]:
            before = self.b.profile()
            self.assertEqual(self.event(self.request(1031, new_name=name), 12)['result'], code)
            self.assertEqual(self.b.profile(), before)
        r = self.b.profile(); r['attachments'] = []; self.b.save(r)
        self.assertEqual(self.event(self.request(1031, new_name='齐天大圣'), 12)['result'], 7)

    def test_duplicate_name_other_account(self):
        r = self.b.profile('other'); r['role_name'] = '齐天大圣'; self.b.save(r, 'other')
        self.assertEqual(self.event(self.request(1031, new_name='齐天大圣'), 12)['result'], 2)

    def test_head_free_then_paid_and_gender(self):
        self.assertEqual(self.b.profile()['head_type'], 1)
        self.assertEqual(self.event(self.request(1069, head_type=201, flag=0), 99)['result'], 1)
        self.assertEqual(self.b.profile()['gold_coin'], 1000)
        for head, flag in [(202, 0), (101, 1), (255, 1), (201, 1), (202, 2)]:
            before = self.b.profile()
            self.assertNotEqual(self.event(self.request(1069, head_type=head, flag=flag), 99)['result'], 1)
            self.assertEqual(self.b.profile(), before)
        out = self.request(1069, head_type=202, flag=1)
        self.assertEqual(self.event(out, 99)['result'], 1)
        self.assertEqual(self.b.profile()['gold_coin'], 800)
        self.assertEqual(self.b.respond(self.packet, dict(authenticated=True)), self.replies)
        self.assertEqual(self.b.profile()['gold_coin'], 800)
        r = self.b.profile(); r['gold_coin'] = 199; self.b.save(r)
        self.assertEqual(self.event(self.request(1069, head_type=203, flag=1), 99)['result'], 8)

    def test_all_runes_level_boundaries(self):
        for tid, row in p.RUNES.items():
            lv = int(row['open_level'])
            r = self.b.profile(); r.update(level=max(1, lv-1), cur_genius_type=506 if tid == 501 else 501); self.b.save(r)
            if lv > 1:
                self.assertEqual(self.event(self.request(1070, type_id=tid), 109)['result'], 2)
            r = self.b.profile(); r['level'] = max(1, lv); self.b.save(r)
            out = self.request(1070, type_id=tid)
            self.assertEqual(self.event(out, 109)['result'], 1)
            self.assertEqual(self.b.profile()['cur_genius_type'], tid)
            attrs = [a for m, d in out if m == 1032 and d['unit_type'] == 1 for a in d['attr_list']]
            self.assertIn({'type': 86, 'value': tid}, attrs)
            self.assertEqual(self.event(self.request(1070, type_id=tid), 109)['result'], 3)
        self.assertEqual(self.event(self.request(1070, type_id=999), 109)['result'], 3)

    def test_title_wear_remove_power_and_no_stats(self):
        before = self.b.profile()
        out = self.request(1078, flag=3, des_id=1)
        self.assertEqual(self.event(out, 175)['wear_id'], 1)
        after = self.b.profile()
        self.assertGreater(after['role_combat_power'], before['role_combat_power'])
        self.assertEqual(after['corteges'][0]['hp'] - before['corteges'][0]['hp'], 50)
        self.event(self.request(1078, flag=3, des_id=143), 55)
        self.assertEqual(self.b.profile()['title_id'], 1)
        self.request(1078, flag=3, des_id=0)
        self.assertEqual(self.b.profile()['role_combat_power'], before['role_combat_power'])
        r = self.b.profile(); p.grant_title(r, 50, NOW); self.b.save(r)
        self.assertEqual(self.event(self.request(1078, flag=3, des_id=50), 175)['wear_id'], 50)

    def test_expiry_and_permanent_awards(self):
        r = self.b.profile(); p.grant_title(r, 103, NOW); self.b.save(r)
        self.request(1078, flag=3, des_id=103)
        end = self.b.profile()['title_endtime']
        with patch('network_redirect.backend.time.time', return_value=end):
            out = self.request(1307, flag=2)
            self.assertEqual(next(d for m, d in out if m == 1077)['wear_id'], 0)
            self.event(self.request(1078, flag=3, des_id=103), 55)
        self.assertIn('3', self.b.profile()['profile_titles'])

    def test_all_original_title_grants_encodable(self):
        r = self.b.profile()
        for tid in p.TITLES: p.grant_title(r, tid, NOW)
        self.b.save(r)
        out = self.request(1078, flag=1, des_id=0)
        self.assertEqual(next(d for m,d in out if m == 1077)['title_count'], len(p.TITLES))
        for tid in p.TITLES:
            out = self.request(1078, flag=3, des_id=tid)
            self.assertEqual(self.event(out, 175)['wear_id'], tid)

    def test_talent_effects_and_probability(self):
        units = ([dict(order=i, hp=100, max_hp=100, gongji=100, fangyu=100) for i in (1, 2)], [])
        for tid in p.RUNES:
            r = dict(level=60, cur_genius_type=tid)
            changed, data = p.talent_units(r, units, 100)
            self.assertTrue(data['use_genius'])
            stat = {501:'gongji',502:'gongji',503:'hp',504:'hp',505:'fangyu',506:'fangyu'}[tid]
            self.assertEqual(sum(u[stat] for u in changed[0]), 220)
            self.assertEqual(sum(u[stat] for u in units[0]), 200)
            if stat == 'hp': self.assertEqual(sum(u['max_hp'] for u in changed[0]), 220)
            self.assertEqual(p.talent_units(r, units, 0)[0], units)

    def test_stale_and_unauthenticated(self):
        self.request(1069, head_type=101, flag=0)
        before = self.b.profile()
        out = self.b.respond(encode(1069, dict(serial_num=self.serial, head_type=102, flag=1)), dict(authenticated=True))
        self.assertEqual(decode(out[0])[2]['id'], 55)
        self.assertEqual(self.b.profile(), before)
        with self.assertRaises(ValueError):
            self.b.respond(encode(1070, dict(serial_num=2000, type_id=502)), {})

if __name__ == '__main__': unittest.main()
