"""Native 69/2 and 1051 reward contracts, disposable database only."""
import copy
from collections import Counter
from pathlib import Path
import unittest
from unittest.mock import patch

from network_redirect import guild, guild_offline, item_rewards, summon
from network_redirect.backend import Backend, login_fields
from tests import test_equipment as equipment


class EscortRewardTests(unittest.TestCase):
    setUp = equipment.EquipmentTests.setUp
    req = equipment.EquipmentTests.req
    add = equipment.EquipmentTests.add

    def compose(self, count=1):
        return self.req(1301, id=69, data=summon.lua(dict(flag=2, ten_pick=count)))

    def prepare(self, count=10):
        role = self.b.profile()
        role['gold_coin'] = 10000
        self.b.save(role)
        result = self.req(1301, id=1, data=summon.lua(dict(union_name='经书测试')))
        self.assertFalse(any(event == 55 for event, _ in result), result)
        for tid in (1301, 1302, 1303):
            self.add(tid, count=count)

    def amount(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments']
                   if i['attach_type'] == 5 and i['type_id'] == tid)

    def reward_amount(self, spec):
        return self.b.profile()['gold_coin'] if spec[0] == 11 else self.amount(spec[1])

    def response(self):
        return next(login_fields(d['data']) for m, _, d in self.decoded
                    if m == 1301 and d['id'] == 69)

    def use(self, tid, ident, count=1, **kw):
        args = dict(item_type=tid, item_id=ident, item_count=count, des_type=1, des_id=0)
        args.update(kw)
        return self.req(1051, **args)

    def replay_unchanged(self):
        before = self.b.profile()
        self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
        self.assertEqual(self.b.profile(), before)

    def test_single_each_grade_then_native_use_and_replay(self):
        self.prepare(4)
        for tid in range(1304, 1308):
            peaches = self.amount(1001)
            with patch.object(summon, 'weighted_choice', return_value=str(tid)):
                self.compose()
            prize = self.response()['item_list'][1]
            self.assertEqual(prize, dict(object_type=5, attach_type=tid, attach_count=1, attach_level=1))
            self.assertEqual(self.amount(tid), 1)
            self.assertEqual(self.amount(1001), peaches)
            self.replay_unchanged()
            bag = next(i for i in self.b.profile()['attachments'] if i['type_id'] == tid)
            with patch.object(item_rewards, 'draw', return_value=[5, 1001, (tid-1303)*50, 1]):
                result = self.use(tid, bag['id'])
            self.assertEqual(result[-1][0], 21, result)
            self.assertEqual(self.amount(tid), 0)
            self.assertEqual(self.amount(1001)-peaches, (tid-1303)*50)
            self.replay_unchanged()
            before = self.b.profile()
            self.assertEqual(self.use(tid, bag['id'])[-1][0], 55)
            self.assertEqual(self.b.profile(), before)
        for tid in (1301, 1302, 1303):
            self.assertEqual(self.amount(tid), 0)

    def test_ten_independent_openings_nested_native_rows_and_existing_bags_untouched(self):
        self.prepare(10)
        for tid in range(1304, 1308):
            self.add(tid, count=2)
        bags = ['1304', '1305', '1306', '1307', '1304'] * 2
        specs = [[5,1001,50,1],[11,1,50,1],[5,1029,9,1],[5,6002,5,1],[5,1007,1,1]] * 2
        before = {tuple(p[:2]): self.reward_amount(p) for p in specs}
        with patch.object(summon, 'weighted_choice', side_effect=bags) as bag_draw, \
                patch.object(item_rewards, 'draw', side_effect=specs) as content_draw:
            self.compose(10)
        rows = self.response()['item_list']
        self.assertEqual(self.response()['ten_pick'], 10)
        self.assertEqual(len(rows), 10)
        self.assertEqual(bag_draw.call_count, 10)
        self.assertEqual(content_draw.call_count, 10)
        for index, spec in enumerate(specs, 1):
            self.assertEqual(rows[index][1]['object_type'], spec[0])
            self.assertEqual(rows[index][1]['attach_type'], spec[1])
            self.assertEqual(rows[index][1]['attach_count'], spec[2])
        for spec in specs[:5]:
            self.assertEqual(self.reward_amount(spec)-before[tuple(spec[:2])], spec[2]*2)
        for tid in (1301, 1302, 1303):
            self.assertEqual(self.amount(tid), 0)
        for tid in range(1304, 1308):
            self.assertEqual(self.amount(tid), 2)
        self.replay_unchanged()

    def test_all_bag_contents_inventory_and_exact_quantities(self):
        rules = item_rewards.load_rules()
        for tid in range(1304, 1308):
            for group in rules['pools'][str(tid)]:
                for spec in group['candidates']:
                    with self.subTest(tid=tid, reward=spec):
                        ident = self.add(tid)
                        before = self.reward_amount(spec)
                        with patch.object(item_rewards, 'draw', return_value=spec):
                            result = self.use(tid, ident)
                        self.assertEqual(result[-1][0], 21, result)
                        self.assertEqual(self.reward_amount(spec)-before, spec[2])
                        self.assertEqual(result[-1][1]['attach_list'][1]['object_type'], spec[0])
                        self.assertEqual(result[-1][1]['attach_list'][1]['attach_count'], spec[2])
                        self.replay_unchanged()

    def test_inventory_batch_draws_per_bag_and_aggregates_results(self):
        ident = self.add(1307, count=16)
        specs = [[5, tid, 5, 1] for tid in (6002, 6003, 6005)] * 5
        before = {tid: self.amount(tid) for tid in (6002, 6003, 6005)}
        with patch.object(item_rewards, 'draw', side_effect=specs) as draw:
            event = self.use(1307, ident, 15)[-1]
        self.assertEqual(event[0], 21)
        self.assertEqual(draw.call_count, 15)
        self.assertEqual(self.amount(1307), 1)
        for tid in before:
            self.assertEqual(self.amount(tid)-before[tid], 25)
        self.assertEqual(len(event[1]['attach_list']), 3)
        self.replay_unchanged()

    def test_unopened_bag_survives_backend_restart(self):
        self.prepare(1)
        with patch.object(summon, 'weighted_choice', return_value='1307'):
            self.compose()
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        bag = next(i for i in self.b.profile()['attachments'] if i['type_id'] == 1307)
        before = self.amount(6005)
        with patch.object(item_rewards, 'draw', return_value=[5, 6005, 5, 1]):
            self.assertEqual(self.use(1307, bag['id'])[-1][0], 21)
        self.assertEqual(self.amount(6005)-before, 5)
        self.assertEqual(self.amount(1307), 0)

    def test_missing_fragment_and_invalid_compose_leave_inventory_unchanged(self):
        self.prepare(1)
        for count in (0, 2, 10, True, 1.5, '1'):
            before = self.b.profile()
            self.assertEqual(self.compose(count)[-1][0], 55)
            self.assertEqual(self.b.profile(), before)
        role = self.b.profile()
        role['attachments'] = [i for i in role['attachments'] if i['type_id'] != 1303]
        self.b.save(role)
        before = self.b.profile()
        self.assertEqual(self.compose()[-1][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_forged_locked_and_overdrawn_bag_use_is_atomic(self):
        ident = self.add(1304, count=2)
        for tid, count, kw in ((1305, 1, {}), (1304, 3, {}), (1304, 0, {}),
                               (1304, 16, {}), (1304, 1, {'des_id': 999999})):
            before = self.b.profile()
            self.assertEqual(self.use(tid, ident, count, **kw)[-1][0], 55)
            self.assertEqual(self.b.profile(), before)
        role = self.b.profile()
        next(i for i in role['attachments'] if i['id'] == ident)['is_lock'] = 1
        self.b.save(role)
        before = self.b.profile()
        self.assertEqual(self.use(1304, ident)[-1][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_partial_ten_failure_rolls_back_all_costs_and_rewards(self):
        self.prepare(10)
        before = self.b.profile()
        with patch.object(item_rewards, 'draw', side_effect=[[11, 1, 20, 1], ValueError('invalid reward')]):
            self.assertEqual(self.compose(10)[-1][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_probability_boundaries_and_config_validation(self):
        rules = guild.load_rules()
        weights = rules['escort_compose']['bag_weights']
        counts = Counter()
        for roll in range(100):
            with patch.object(summon.secrets, 'randbelow', return_value=roll):
                counts[summon.weighted_choice(weights)] += 1
        self.assertEqual(dict(counts), {'1304': 60, '1305': 25, '1306': 12, '1307': 3})
        for weights in ({'1304':100}, {'1304':60,'1305':25,'1306':12,'1307':0},
                        {'1304':60,'1305':25,'1306':12,'1307':True}):
            invalid = copy.deepcopy(rules)
            invalid['escort_compose']['bag_weights'] = weights
            with self.assertRaises(ValueError):
                guild_offline.validate_rules(invalid)


if __name__ == '__main__':
    unittest.main()
