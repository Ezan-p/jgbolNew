"""Weighted escort refresh through the native 1301/69 protocol, temporary saves."""
import copy
from collections import Counter
from pathlib import Path
import unittest
from unittest.mock import patch

from network_redirect import guild, guild_offline, summon
from network_redirect.backend import Backend
from tests import test_guild as base


class EscortRefreshTests(unittest.TestCase):
    setUp = base.GuildTests.setUp
    req = base.GuildTests.req
    create = base.GuildTests.create
    role = base.GuildTests.role

    def refresh(self):
        result = self.req(69, flag=5)
        self.assertFalse(any(i == 55 for _, i, _ in result), result)
        return result[-1][2]

    def replay_unchanged(self):
        before = self.role()
        self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
        self.assertEqual(self.role(), before)

    def test_probability_intervals_from_every_refreshable_grade(self):
        self.create()
        self.req(69, flag=4)
        baseline = self.role()
        for previous in range(1, 5):
            counts = Counter()
            for roll in range(100):
                role = copy.deepcopy(baseline)
                role['guild']['escort'].update(level=previous, flushes=0)
                self.b.save(role)
                with patch.object(summon.secrets, 'randbelow', return_value=roll):
                    result = self.refresh()
                counts[result['book_level']] += 1
                self.assertEqual(result['contribute'], result['book_level'] * 10)
                self.assertEqual(result['flush_count'], 1)
                self.assertEqual(result['flush_west_book'], 1)
            self.assertEqual(dict(counts), {2: 60, 3: 25, 4: 12, 5: 3})

    def test_downgrade_repeat_costs_and_no_last_refresh_guarantee(self):
        self.create()
        gold = self.role()['gold_coin']
        with patch.object(summon, 'weighted_choice', side_effect=['4', '2', '2', '3', '2']) as draw:
            for index, grade in enumerate((4, 2, 2, 3, 2), 1):
                result = self.refresh()
                self.assertEqual(result['book_level'], grade)
                self.assertEqual(result['flush_count'], index)
                self.assertEqual(self.role()['gold_coin'], gold - (index - 1) * 10)
                self.replay_unchanged()
            self.assertEqual(draw.call_count, 5)
            for call in draw.call_args_list:
                self.assertEqual(call.args, (self.b.guild_rules['escort_refresh']['grade_weights'],))
            before = self.role()
            self.assertEqual(self.req(69, flag=5)[-1][1], 55)
            self.assertEqual(self.role(), before)
            self.assertEqual(draw.call_count, 5)

    def test_all_refreshes_can_repeat_low_grade_without_guarantee(self):
        self.create()
        with patch.object(summon, 'weighted_choice', return_value='2') as draw:
            for _ in range(5):
                self.assertEqual(self.refresh()['book_level'], 2)
        self.assertEqual(draw.call_count, 5)

    def test_highest_grade_stops_refresh_without_charging_or_drawing(self):
        self.create()
        with patch.object(summon, 'weighted_choice', return_value='5') as draw:
            self.assertEqual(self.refresh()['book_level'], 5)
            before = self.role()
            self.assertEqual(self.req(69, flag=5)[-1][1], 55)
            self.assertEqual(self.role(), before)
        self.assertEqual(draw.call_count, 1)

    def test_insufficient_gold_and_active_trip_do_not_consume_refresh(self):
        self.create()
        with patch.object(summon, 'weighted_choice', return_value='3'):
            self.refresh()
        role = self.role()
        role['gold_coin'] = 9
        self.b.save(role)
        before = self.role()
        with patch.object(summon, 'weighted_choice') as draw:
            self.assertEqual(self.req(69, flag=5)[-1][1], 55)
            self.assertEqual(self.role(), before)
            self.assertEqual(self.req(69, flag=6, book_level=3, road_type=2)[-1][1], 69)
            before = self.role()
            self.assertEqual(self.req(69, flag=5)[-1][1], 55)
            self.assertEqual(self.role(), before)
            draw.assert_not_called()

    def test_reconnect_queries_and_dispatch_keep_current_grade(self):
        self.create()
        with patch.object(summon, 'weighted_choice', side_effect=['4', '2']):
            self.refresh()
            self.refresh()
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        with patch.object(summon, 'weighted_choice') as draw:
            for road in (1, 2, 3):
                result = self.req(69, flag=4, road_type=road)[-1][2]
                self.assertEqual((result['book_level'], result['flush_count']), (2, 2))
            before = self.role()
            self.assertEqual(self.req(69, flag=6, road_type=3, book_level=4)[-1][1], 55)
            self.assertEqual(self.role(), before)
            self.req(69, flag=6, road_type=3, book_level=2)
            self.replay_unchanged()
            escort = self.role()['guild']['escort']
            self.assertEqual(escort['active']['book']['book_level'], 2)
            self.assertEqual((escort['level'], escort['flushes']), (1, 0))
            with patch('network_redirect.game_clock.now', return_value=base.NOW + 3601), \
                    patch.object(guild_offline, 'roll', return_value=99):
                result = self.req(69, flag=11)[-1][2]
                self.assertEqual(result['contribute'], 20)
                self.assertEqual(result['union_money'], 200)
                self.assertEqual(result['item_info'][1]['attach_type'], 1303)
                self.assertEqual(result['item_info'][1]['attach_count'], 2)
            draw.assert_not_called()

    def test_invalid_probabilities_are_rejected(self):
        rules = guild.load_rules()
        invalid_weights = (None, [], {'2': 100},
                           {'1': 1, '2': 59, '3': 25, '4': 12, '5': 3},
                           {'2': 60, '3': 25, '4': 15, '5': 0},
                           {'2': 60, '3': 25, '4': 12, '5': True},
                           {'2': 60, '3': 25, '4': 12, '5': -3},
                           {'2': 60.0, '3': 25, '4': 12, '5': 3},
                           {'2': 60, '3': 25, '4': 12, '5': 4},
                           {'2': 25, '3': 25, '4': 25, '5': 25})
        for weights in invalid_weights:
            with self.subTest(weights=weights):
                invalid = copy.deepcopy(rules)
                invalid['escort_refresh']['grade_weights'] = weights
                with self.assertRaises(ValueError):
                    guild_offline.validate_rules(invalid)
        for refresh in (None, {}, {'mode': 'official', 'reason': 'unknown'}):
            invalid = copy.deepcopy(rules)
            invalid['escort_refresh'] = refresh
            with self.assertRaises(ValueError):
                guild_offline.validate_rules(invalid)


if __name__ == '__main__':
    unittest.main()
