"""Original 25-entry roster; real packets through newly opened rebirth paths."""
from collections import Counter
import copy
import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import reborn, fate_rebuild, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

ROOT = Path(__file__).resolve().parents[1]
ADDED = {5001:3, 5004:3, 5013:2, 5015:3, 5035:2, 5018:3,
         5031:3, 5033:3, 5050:3, 5045:1, 5047:3}


class RebornHotupdateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        clock = patch('network_redirect.backend.time.time', return_value=1793419200)
        clock.start(); self.addCleanup(clock.stop)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 100000
        self.state = dict(authenticated=True)

    def fixture(self, tid):
        role = self.b.profile()
        role.update(level=99, reborn_layer=4, gold_coin=1000)
        role['corteges'] = [summon.companion(role, tid)]
        role['attachments'] = []
        c = role['corteges'][0]
        c.update(level=200, order=1, culture_point=0)
        self.cid = c['id']
        materials = {1371}
        for row in reborn.VEINS.values():
            materials.update(int(p.split('|')[1]) for p in row['consume_list'].split('/'))
        for row in reborn.LAYERS.values():
            materials.update(int(p.split('|')[1]) for p in row['consum_list'].split('/'))
        for tid in materials:
            summon.add_item(role, tid, 100000)
        self.b.save(role)

    def request(self, mid=1328, ok=True, **kw):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **kw))
        self.replies = self.b.respond(self.packet, self.state)
        self.decoded = [decode(p) for p in self.replies]
        self.assertEqual(self.decoded[-1][0], 1106)
        events = [(d['id'], login_fields(d['data'])) for m, _, d in self.decoded if m == 2998]
        self.assertEqual(any(i == 55 for i, _ in events), not ok, events)
        if mid == 1328 and ok:
            self.assertIn((172, {'flag': kw['id']}), events)
        return events

    def op(self, op, ok=True, **data):
        return self.request(id=op, reborn_type=2, ok=ok,
                            data=summon.lua(dict(cortege_id=self.cid, **data)))

    def fate(self, ok=True):
        return self.request(1357, id=3, ok=ok, data=summon.lua(dict(cortege_id=self.cid)))

    @staticmethod
    def stock(role):
        result = Counter()
        for i in role['attachments']:
            if i['attach_type'] == 5:
                result[i['type_id']] += i['count']
        return result

    def test_original_roster_exact_and_fate_subset(self):
        name = 'cortege_reborn_config.csv'
        original = (ROOT/'analysis/evidence/hotupdate_gap_20261031/official_csv'/name).read_bytes()
        self.assertEqual(hashlib.sha256(original).hexdigest(),
                         'b414e026631006c61598da4090bd926dbab55d2a581f7fb83b5fd3114ef72fe5')
        self.assertEqual((ROOT/'analysis/configs/immortal_hotupdate'/name).read_bytes(), original)
        with (ROOT/'analysis/configs'/name).open(encoding='utf-8-sig', newline='') as src:
            baseline = {int(r['cortege_type']):r for r in csv.DictReader(src)}
        self.assertEqual(len(baseline), 14)
        self.assertEqual(len(reborn.CORTS), 25)
        self.assertEqual(set(reborn.CORTS)-set(baseline), set(ADDED))
        for tid, row in baseline.items():
            self.assertEqual(reborn.CORTS[tid], row)
        self.assertEqual({t:int(reborn.CORTS[t]['plus_type']) for t in ADDED}, ADDED)
        self.assertEqual(len(fate_rebuild.ACTIVE), 15)
        self.assertLessEqual(fate_rebuild.ACTIVE, set(reborn.CORTS))
        self.assertEqual(fate_rebuild.ACTIVE & set(ADDED), {5013})

    def test_all_eleven_nine_rebirths_and_monkey_fate(self):
        for tid, direction in ADDED.items():
            with self.subTest(cortege=tid):
                self.fixture(tid)
                self.assertEqual(self.b.profile()['corteges'][0]['reborn_plus_type'], direction)
                self.fate(ok=False)
                for layer in range(1, 10):
                    role = self.b.profile()
                    role['corteges'][0].update(level=int(reborn.LAYERS[layer]['min_level']), cur_exp=0)
                    self.b.save(role)
                    for pulse in range(1, 10):
                        row = reborn.VEINS[layer, pulse]
                        allowed = {int(p.split('|')[1]):int(p.split('|')[3]) for p in row['consume_list'].split('/')}
                        fixed = int(row['fixed_count(fix>0|unfix=0)'])
                        cost = {next(iter(allowed)):fixed} if fixed else allowed
                        before = self.b.profile()
                        self.op(1, material_list=cost)
                        after = self.b.profile()
                        self.assertEqual(self.stock(before)-self.stock(after), Counter(cost))
                        self.assertEqual(after['corteges'][0]['reborn_vein_level'], pulse)
                    before = self.b.profile()
                    self.op(2)
                    after = self.b.profile(); c = after['corteges'][0]
                    row = reborn.LAYERS[layer]
                    cost = {int(p.split('|')[1]):int(p.split('|')[3]) for p in row['consum_list'].split('/')}
                    self.assertEqual(self.stock(before)-self.stock(after), Counter(cost))
                    self.assertEqual((c['reborn_layer'], c['reborn_vein_level'], c['level']),
                                     (layer, 0, int(row['reset_level'])))
                    self.assertEqual(c['culture_point'], 150*layer)
                    self.assertTrue(any(m == 1032 and d.get('id') == self.cid and
                                        any(a['type'] == 224 and a['value'] == layer for a in d['attr_list'])
                                        for m, _, d in self.decoded))
                before = self.b.profile()
                self.op(2, ok=False)
                self.assertEqual(self.b.profile(), before)
                if tid == 5013:
                    self.fate()
                    after = self.b.profile()
                    self.assertEqual(self.stock(before)-self.stock(after), Counter({1371:20}))
                    self.assertEqual(after['corteges'][0]['fate_rebullding_state'], 1)
                    self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
                    self.assertEqual(self.b.profile(), after)
                    self.fate(ok=False)
                    self.assertEqual(self.b.profile(), after)
                    self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
                    self.assertEqual(self.b.profile(), after)
                else:
                    self.fate(ok=False)
                    self.assertEqual(self.b.profile(), before)

    def test_old_save_directions_migrate_once_and_preserve_paid_choices(self):
        self.fixture(5013)
        role = self.b.profile()
        role['corteges'] = []
        for tid in ADDED:
            c = summon.companion(role, tid)
            c.update(reborn_layer=0, reborn_plus_type=1, reborn_vein_level=0)
            role['corteges'].append(c)
        role['corteges'][0].update(reborn_layer=1, reborn_plus_type=2)
        self.b.save(role)
        expected = self.b.profile()
        role = copy.deepcopy(expected)
        # Write a legacy database record, bypassing the current save migration.
        for c in role['corteges'][1:]:
            c['reborn_plus_type'] = 1
        self.b.db.execute('UPDATE roles SET data=? WHERE account=?',
                          (json.dumps(role), self.b.account)); self.b.db.commit()
        migrated = self.b.profile()
        self.assertEqual(migrated, expected)
        self.assertEqual(self.b.profile(), migrated)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.b.profile(), migrated)

    def test_monkey_guards_and_replay_are_atomic(self):
        self.fixture(5013)
        before = self.b.profile()
        for op, data in ((2, {}), (3, {'des_type':1}), (1, {'material_list':{10000:1}})):
            self.op(op, ok=False, **data)
            self.assertEqual(self.b.profile(), before)
        role = self.b.profile(); role['reborn_layer'] = 0; self.b.save(role)
        before = self.b.profile()
        self.op(1, ok=False, material_list={10000:300})
        self.assertEqual(self.b.profile(), before)
        role['reborn_layer'] = 4; self.b.save(role)
        with patch.object(Backend, 'companion_deltas', side_effect=ValueError('encode failure')):
            self.op(1, ok=False, material_list={10000:300})
        self.assertEqual(self.b.profile(), role)
        self.op(1, material_list={10000:300})
        after = self.b.profile()
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.b.profile(), after)
        self.fixture(2001)
        before = self.b.profile()
        self.op(1, ok=False, material_list={10000:300})
        self.assertEqual(self.b.profile(), before)

    def test_newly_opened_attribute_change_survives_restart(self):
        self.fixture(5013)
        role = self.b.profile(); role['corteges'][0]['reborn_layer'] = 1; self.b.save(role)
        before = self.b.profile()
        self.op(3, des_type=3)
        after = self.b.profile()
        self.assertEqual(after['gold_coin'], before['gold_coin']-50)
        self.assertEqual(after['corteges'][0]['reborn_plus_type'], 3)
        self.assertNotEqual(after['corteges'][0]['gongji'], before['corteges'][0]['gongji'])
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.b.profile(), after)


if __name__ == '__main__':
    unittest.main()
