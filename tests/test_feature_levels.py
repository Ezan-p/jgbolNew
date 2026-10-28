"""Original thresholds, real wire rejection, replay and no premature state creation."""
import copy
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import activity, feature_levels as gates, formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode

ROOT = Path(__file__).resolve().parents[1]
NOW = 1792814400


class FeatureLevelTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.b = Backend(Path(directory.name), 18770, lambda *a, **k: None)
        self.addCleanup(self.b.close)
        self.serial = 10000
        clock = patch('network_redirect.backend.time.time', return_value=NOW)
        clock.start()
        self.addCleanup(clock.stop)

    def role(self, level):
        role = self.b.profile()
        role.update(level=level, gold_coin=100000, silver_coin=1000000)
        self.b.save(role, gameplay=False)
        return self.b.profile()

    def request(self, mid, **request):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **request))
        self.replies = self.b.respond(self.packet, {'authenticated': True})
        decoded = [decode(p) for p in self.replies]
        self.assertEqual(decoded[-1][0], 1106)
        self.assertEqual(decoded[-1][2]['req_serial_num'], self.serial)
        return [(d['id'], login_fields(d['data'])) for m, _, d in decoded if m == 2998]

    def test_recovered_activity_thresholds_match_original_assets(self):
        sys.path.insert(0, str(ROOT / 'analysis/tools'))
        self.addCleanup(lambda: sys.path.remove(str(ROOT / 'analysis/tools')))
        spec = importlib.util.spec_from_file_location('audit_levels', ROOT / 'analysis/tools/audit_feature_levels.py')
        audit = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(audit)
        report, _ = audit.audit()
        self.assertEqual(len(report['activity_ids']), 43)
        rune = next(t for t in report['tables'] if t['logical'].endswith('/rune.csv'))
        self.assertEqual(rune['rows'], 6)
        self.assertEqual(set(rune['fields']['open_level']), {'0', '5', '7', '10', '15', '20'})

    def test_fixed_gates_reject_wire_before_preparing_or_spending(self):
        cases = [(mid, {}) for mid in gates.MESSAGES]
        cases += [(1026, {'fight_type': ft}) for ft in gates.FIGHTS]
        cases += [(1049, {'query_type': q}) for q in range(1, 6)]
        cases += [(1201, {'flag': f}) for f in (1, 2)]
        cases += [(1244, {'fight_type': 2})]
        cases += [(1059, {'flag': f}) for f in (2, 3)]
        cases += [(1131, {'flag': 2})]
        cases += [(1328, {'reborn_type': 3, 'id': 5})]
        cases += [(1053, {'compose_type': op}) for op in (2, 3)]
        cases += [(1303, {'id': 1})]
        cases += [(1349, {'id': i, 'data': '{}'}) for i in range(1, 8)]
        for mid, req in cases:
            key = gates.feature(mid, req)
            with self.subTest(mid=mid, req=req, key=key):
                before = self.role(gates.LEVELS[key]-1)
                events = self.request(mid, **req)
                self.assertEqual(events, [(55, {'op_string': f'{gates.NAMES[key]}需角色{gates.LEVELS[key]}级开放'})])
                self.assertEqual(self.b.profile(), before)
                self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
                self.assertEqual(self.b.profile(), before)

    def test_exact_threshold_queries_succeed_after_rejected_request(self):
        # Real settlements at both sides of each threshold, not mocked dispatch.
        cases = [(1021, {'flag': 0}), (1029, {'flag': 1}),
                 (1330, {'flag': 1, 'id': 4, 'data': '{}'}),
                 (1349, {'id': 1, 'data': '{}'}),
                 (1349, {'id': 3, 'data': '{}'}),
                 (1049, {'query_type': 1})]
        for mid, req in cases:
            key = gates.feature(mid, req)
            with self.subTest(key=key):
                self.role(gates.LEVELS[key]-1)
                self.assertEqual(self.request(mid, **req)[0][0], 55)
                self.role(gates.LEVELS[key])
                self.assertNotIn(55, [event for event, _ in self.request(mid, **req)])

    def test_shared_messages_do_not_gate_unrelated_operations(self):
        for mid, req in [(1205, {'flag': 0}), (1205, {'flag': 1}),
                         (1059, {'flag': 1}), (1201, {'flag': 5}),
                         (1026, {'fight_type': 1}), (1026, {'fight_type': 11}),
                         (1244, {'fight_type': 3}), (1131, {'flag': 1}),
                         (1343, {'flag': 1}), (1303, {'id': 2}), (1053, {'compose_type': 1}),
                         (1328, {'reborn_type': 3, 'id': 6})]:
            with self.subTest(mid=mid, req=req):
                self.assertIsNone(gates.feature(mid, req))
        self.role(1)
        for flag in (0, 1):
            self.assertNotIn(55, [event for event, _ in self.request(1205, flag=flag)])

    def test_limited_activity_opening_boundaries(self):
        cases = [
            ('monday', 15, 1219, dict(flag=1, level=0, op_type=0)),
            ('fishrush', 20, 1208, dict(type_id=0, count=1)),
            ('twoyears', 20, 1334, dict(flag=0, index=0)),
            ('rulaitable', 20, 1351, dict(id=0, data='{}')),
            ('tower', 20, 1309, dict(id=1, data='{}')),
            ('destiny', 30, 1227, dict(flag=1, index=0, count=0)),
            ('forge', 30, 1055, dict(flag=0)),
        ]
        for key, level, mid, req in cases:
            with self.subTest(key=key):
                self.assertEqual(gates.LEVELS[key], level)
                before = self.role(level - 1)
                events = self.request(mid, **req)
                self.assertEqual(events, [(55, {'op_string': f'{gates.NAMES[key]}需角色{level}级开放'})])
                self.assertEqual(self.b.profile(), before)
                self.role(level)
                events = self.request(mid, **req)
                self.assertNotIn(55, [event for event, _ in events], events)
                if key == 'forge':
                    self.assertEqual(events[-1][1]['equip_compose']['min_role_level'], 30)

    def test_taixu_shop_purchase_at_12_does_not_unlock_ordeal(self):
        role = self.role(12)
        self.assertNotIn(55, [event for event, _ in self.request(1349, id=3, data='{}')])
        role = self.b.profile()
        offer = role['activity']['undergo']['shop'][0]
        cost = offer['cost']
        summon.add_item(role, 1366, cost)
        self.b.save(role)
        self.assertNotIn(55, [event for event, _ in self.request(
            1349, id=5, data='{index=1,count=1}')])
        after = self.b.profile()
        self.assertEqual(after['activity']['undergo']['purchases'][str(offer['reward'][1])], 1)
        self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
        self.assertEqual(after, self.b.profile())
        self.assertEqual(self.request(1349, id=1, data='{}')[0][0], 55)
        self.assertEqual(after, self.b.profile())

    def test_direct_activity_rejection_does_not_initialize_activity(self):
        role = {'level': 12}
        before = copy.deepcopy(role)
        with self.assertRaisesRegex(formation.Rejected, '13级'):
            activity.settle(role, 1049, {'query_type': 1}, NOW, {}, {}, {}, login_fields)
        self.assertEqual(role, before)

    def test_guild_entry_and_donation_vip_alternative(self):
        self.role(self.b.guild_rules['join_level']-1)
        before = self.b.profile()
        events = self.request(1301, id=18, data='{query_type=4,page=1}')
        self.assertEqual(events[0][0], 55)
        self.assertEqual(before, self.b.profile())
        self.role(35)
        self.assertNotIn(55, [e for e, _ in self.request(1301, id=1, data='{union_name="等级测试"}')])
        before = self.b.profile()
        self.assertIn('36级或VIP1', self.request(1301, id=36, data='{count=1}')[0][1]['op_string'])
        self.assertEqual(before, self.b.profile())
        self.role(36)
        self.assertNotIn(55, [e for e, _ in self.request(1301, id=36, data='{count=1}')])
        # Direct settlement preserves an explicit VIP value for this boundary.
        from network_redirect import guild
        role = self.b.profile()
        role.update(level=35, vip_level=1)
        before = role['gold_coin']
        guild.settle(role, {'id': 36, 'data': '{count=1}'}, NOW,
                     self.b.guild_rules, login_fields, self.b.daily_rules)
        self.assertEqual(role['gold_coin'], before-1)


if __name__ == '__main__':
    unittest.main()
