"""Original 1085/52 wire lifecycle, conservation, inventory safety and restart."""
import copy
import json
from pathlib import Path
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_pray as pray, formation, summon
from network_redirect.backend import Backend


def offering(typ, ident, n=1):
    return dict(object_type=typ, object_id=ident, count=n)


class PrayTests(ActivityCase):
    def seed(self, retained=0, souls=None, completed=0):
        r = self.b.profile()
        r.update(spirit_retain=retained, pray_spirit_times=completed)
        r['souls'] = {'5004': 1000} if souls is None else souls
        self.b.save(r)
        return self.b.profile()

    def pray(self, *rows):
        return self.req(1085, object_count=len(rows), object_list=list(rows))

    def reject(self, *rows):
        before = self.b.profile()
        self.assertIn(55, [e for e, _ in self.pray(*rows)])
        self.assertEqual(before, self.b.profile())

    def test_costs_gold_event_attrs_remainder_and_fourth_prayer(self):
        before = self.seed()
        for completed, cost in enumerate((200, 500, 1000, 1000)):
            with patch.object(pray.secrets, 'choice', return_value=[11, 0, 20, 1]):
                events = self.pray(offering(10, 5004, 150))
            self.ok(events)
            after = self.b.profile()
            reward = next(d['pray_item_list'][1] for e, d in events if e == 52)
            self.assertEqual((reward['object_type'], reward['attach_count']), (11, 20))
            self.assertEqual(after['gold_coin'] - before['gold_coin'], 20)
            self.assertEqual(after['spirit_retain'], before['spirit_retain'] + 1200 - cost)
            self.assertEqual(after['souls']['5004'], before['souls']['5004'] - 150)
            self.assertEqual(after['pray_spirit_times'], completed + 1)
            attrs = {a['type']: a['value'] for m, _, d in self.decoded if m == 1032
                     and d['unit_type'] == 1 for a in d['attr_list']}
            self.assertEqual(attrs[20], completed + 1)
            self.assertEqual(attrs[10], after['spirit_retain'])
            self.assertEqual(attrs[8], after['gold_coin'])
            self.assertEqual(after['attachments'], before['attachments'])
            before = after
        self.assertEqual(before['achievements']['totals']['109'], 1)

    def test_retained_only_replay_restart_and_snapshot(self):
        self.seed(retained=2708, souls={})
        self.ok(self.pray())
        packet, replies = self.packet, self.replies
        before = self.b.profile()
        self.assertEqual(self.b.respond(packet, self.state), replies)
        self.assertEqual(before, self.b.profile())
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(before, self.b.profile())
        snapshot = self.b.snapshot()
        self.assertEqual(snapshot['spirit_retain'], 2508)
        self.assertEqual(snapshot['pray_spirit_times'], 1)
        self.ok(self.pray())
        self.assertEqual(self.b.profile()['spirit_retain'], 2008)

    def test_soul_quality_values_and_insufficient_atomic(self):
        for q, worth in ((2, 1), (3, 2), (4, 4), (5, 8)):
            tid = next(t for t, c in formation.BASES.items() if int(c['quality']) == q)
            self.seed(souls={str(tid): 201})
            self.ok(self.pray(offering(10, tid, 201)))
            self.assertEqual(self.b.profile()['spirit_retain'], 201 * worth - 200)
        self.seed(souls={'5004': 25})
        self.reject(offering(10, 5004, 26))
        self.reject(offering(10, 5004, 24))
        self.reject(offering(10, 5004, 0))
        self.reject(offering(10, 99999, 25))
        self.reject(offering(5, 1001, 1))
        self.reject(offering(7, 5004, 25))
        self.reject(offering(10, 5004, 25), offering(10, 5004, 25))
        self.reject(offering(10, 5004, 25), offering(4, 999999))

    def companion(self, quality=3):
        r = self.b.profile()
        tid = next(t for t, c in formation.BASES.items() if int(c['quality']) == quality)
        c = summon.companion(r, tid)
        r['corteges'].append(c)
        formation.prepare(r, self.b.formation_rules)
        self.b.save(r)
        return c['id']

    def test_mixed_companion_consumption_removes_only_own_innate_spell(self):
        self.seed(retained=178)
        two, three = self.companion(2), self.companion(3)
        r = self.b.profile()
        # Higher-level donors are allowed after the native confirmation dialog.
        next(c for c in r['corteges'] if c['id'] == three)['level'] = 10
        self.b.save(r)
        before = self.b.profile()
        self.assertTrue(any(i.get('innate_owner_id') == three for i in before['attachments']))
        self.ok(self.pray(offering(4, two), offering(4, three), offering(10, 5004)))
        after = self.b.profile()
        self.assertEqual(after['spirit_retain'], 8)
        self.assertEqual(after['souls']['5004'], 999)
        self.assertEqual(after['corteges'], [c for c in before['corteges'] if c['id'] not in (two, three)])
        self.assertEqual(after['attachments'], [i for i in before['attachments'] if i.get('innate_owner_id') not in (two, three)])
        self.reject(offering(4, three))

    def test_locked_active_cheering_training_essence_and_quality_protection(self):
        self.seed(retained=1000)
        ident = self.companion()
        baseline = self.b.profile()
        for field, value in (('order', 2), ('cheer_order', 1), ('is_lock', True),
                             ('pending_training', {'test': 1})):
            r = copy.deepcopy(baseline)
            next(c for c in r['corteges'] if c['id'] == ident)[field] = value
            self.b.save(r)
            self.reject(offering(4, ident))
        self.b.save(copy.deepcopy(baseline))
        r = self.b.profile()
        r['attachments'].append(dict(id=formation.new_id(r), attach_type=5, type_id=1001,
                                     level=1, count=1, owner_id=ident, ext_skill_pos=1))
        self.b.save(r)
        self.reject(offering(4, ident))
        self.b.save(copy.deepcopy(baseline))
        self.reject(offering(4, ident, 2))
        self.reject(offering(4, ident), offering(4, ident))
        for q in (1, 4, 5):
            invalid = self.companion(q)
            self.reject(offering(4, invalid))

    def test_midnight_reset_keeps_remainder_and_achievement(self):
        r = self.seed(retained=1200, completed=3)
        # Simulate an old save whose daily count exists but achievement is absent.
        r['achievements']['totals'].pop('109', None)
        self.b.db.execute('UPDATE roles SET data=? WHERE account=?', (json.dumps(r), self.b.account))
        self.b.db.commit()
        midnight = ((NOW + 8 * 3600) // 86400 + 1) * 86400 - 8 * 3600
        with patch('network_redirect.backend.time.time', return_value=midnight - 1):
            self.ok(self.req(1205, flag=0))
            self.assertEqual(self.b.profile()['spirit_retain'], 1200)
            self.assertNotIn('109', self.b.profile()['achievements']['totals'])
        with patch('network_redirect.backend.time.time', return_value=midnight):
            self.ok(self.pray())
            r = self.b.profile()
            self.assertEqual((r['pray_spirit_times'], r['spirit_retain']), (1, 1000))
            self.assertEqual(r['achievements']['totals']['109'], 1)
        # Returning the clock to the previous day cannot recover cheap prayers.
        self.reject(offering(10, 5004, 100))

    def test_level_boundaries_overflow_and_encoding_failure_rollback(self):
        self.seed(retained=200)
        r = self.b.profile(); r['level'] = 14; self.b.save(r)
        self.reject()
        r['level'] = 15; self.b.save(r)
        self.ok(self.pray())
        r = self.seed(retained=200); r['gold_coin'] = pray.MAX_VALUE; self.b.save(r)
        self.reject()
        self.seed(retained=pray.MAX_VALUE)
        self.reject(offering(10, 5004, 100))
        self.seed(retained=200)
        before = self.b.profile()
        with patch('network_redirect.backend.activity.attributes', side_effect=OverflowError('encoding failure')):
            self.assertIn(55, [e for e, _ in self.pray()])
        self.assertEqual(before, self.b.profile())

    def test_direct_validation_does_not_partially_consume_and_config_rejects_items(self):
        r = self.seed()
        before = copy.deepcopy(r)
        rows = [offering(10, 5004, 25), offering(4, 999999)]
        with self.assertRaises(formation.Rejected):
            pray.settle(r, dict(object_count=2, object_list=rows), self.b.activity_rules)
        self.assertEqual(r, before)
        with self.assertRaises(formation.Rejected):
            pray.settle(r, dict(object_count=1, object_list=[]), self.b.activity_rules)
        cfg = copy.deepcopy(self.b.activity_rules)
        cfg['pray_rewards'] = [[5, 1001, 20, 1]]
        path = Path(self.tmp.name) / 'invalid.json'; path.write_text(json.dumps(cfg))
        with self.assertRaisesRegex(formation.Rejected, '必须为元宝'):
            activity.load_rules(path)

    def test_native_soul_enum_and_adapter_are_integrated(self):
        self.assertEqual(activity.ENUMS['object_type']['spirit'], 10)
        source = summon.client_source(summon.load_rules())
        self.assertIn('_localPrayRestore', source)
        self.assertNotIn('__PRAY_COSTS__', source)
