"""Role level card: actual wire settlement, persistence and native Lua bridge."""
import copy
from pathlib import Path
import unittest
from unittest.mock import patch

from tests import test_progression as original
from network_redirect import formation as f, level_card, progression, summon
from network_redirect.backend import Backend


class LevelCardTests(unittest.TestCase):
    setUp = original.ProgressionTests.setUp
    req = original.ProgressionTests.req

    def setup_card(self, level=19, exp=37, count=2, **item_fields):
        role = self.b.profile()
        role.update(level=level, cur_exp=exp)
        role['progression']['rewarded_level'] = level
        level_card.grant_code_prize(role, [5, level_card.ITEM, count, 1])
        item = next(i for i in role['attachments'] if i['type_id'] == level_card.ITEM)
        item.update(item_fields)
        self.b.save(role, level_card_grant=count)  # Isolated fixture, no player grant.
        return item['id']

    def use(self, ident, **kw):
        data = dict(item_type=1901, item_id=ident, item_count=1, des_type=1, des_id=0)
        data.update(kw)
        return self.req(1051, **data)

    def test_all_levels_preserve_experience_and_issue_normal_rewards(self):
        baseline = self.b.profile()
        for level in range(1, 99):
            with self.subTest(level=level):
                role = copy.deepcopy(baseline)
                need = int(f.LEVELS[level]['upgrade_exp'])
                role.update(level=level, cur_exp=need-1)
                role['progression']['rewarded_level'] = level
                level_card.grant_code_prize(role, [5, 1901, 1, 1])
                ident = next(i['id'] for i in role['attachments'] if i['type_id'] == 1901)
                expected = copy.deepcopy(role)
                progression.add_exp(expected, need, original.NOW)
                expected['attachments'] = [i for i in expected['attachments'] if i['id'] != ident]
                level_card.use(role, dict(item_type=1901, item_id=ident, item_count=1,
                                          des_type=1, des_id=0), original.NOW)
                self.assertEqual(role['level'], level+1)
                self.assertEqual(role['cur_exp'], need-1)
                self.assertEqual(role, expected)

    def test_wire_rewards_sync_replay_and_reload(self):
        ident = self.setup_card()
        before = self.b.profile()
        ordered_events = self.use(ident)
        events = dict(ordered_events)
        after = self.b.profile()
        self.assertEqual((after['level'], after['cur_exp']), (20, 37))
        self.assertEqual(after['gold_coin']-before['gold_coin'], 100)
        self.assertEqual(events[21]['count'], 1)
        self.assertEqual(events[2]['new_level'], 20)
        self.assertEqual(events[2]['old_level'], 19)
        event_ids = [eid for eid, _ in ordered_events]
        self.assertLess(event_ids.index(2), event_ids.index(21))
        upgrade_index = next(i for i, (mid, _, data) in enumerate(self.decoded)
                             if mid == 2998 and data['id'] == 2)
        self.assertTrue(any(mid == 1032 for mid, _, _ in self.decoded[:upgrade_index]))
        self.assertEqual(after['cortege_count'], int(f.LEVELS[20]['cortege_count']))
        attrs = {a['type']: a['value'] for mid, _, data in self.decoded
                 if mid == 1032 and data['unit_type'] == 1 for a in data['attr_list']}
        self.assertEqual((attrs[3], attrs[5]), (20, 37))
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(after, self.b.profile())
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.assertEqual(after, self.b.profile())

    def test_last_card_removed_and_max_level_no_consumption(self):
        ident = self.setup_card(level=98, count=2)
        self.assertIn(2, dict(self.use(ident)))
        before = self.b.profile()
        self.assertEqual(before['level'], 99)
        self.assertIn(55, dict(self.use(ident)))
        self.assertEqual(before, self.b.profile())
        role = before
        role.update(level=30, cur_exp=0)
        role['progression']['rewarded_level'] = 30
        self.b.save(role)
        self.assertIn(21, dict(self.use(ident)))
        self.assertFalse(any(i['id'] == ident for i in self.b.profile()['attachments']))
        before = self.b.profile()
        self.assertIn(55, dict(self.use(ident)))
        self.assertEqual(before, self.b.profile())

    def test_invalid_requests_and_inventory_do_not_mutate_save(self):
        ident = self.setup_card()
        for kw in ({'item_count': 0}, {'item_count': 2}, {'des_type': 4},
                   {'des_id': 999999}, {'item_id': 999999}):
            with self.subTest(kw=kw):
                before = self.b.profile()
                self.assertIn(55, dict(self.use(ident, **kw)))
                self.assertEqual(before, self.b.profile())
        baseline = self.b.profile()
        for fields in ({'is_lock': 1}, {'owner_id': 22}, {'equip_pos': 1},
                       {'level': 2}, {'type_id': 1152}, {'count': 0}):
            with self.subTest(fields=fields):
                role = copy.deepcopy(baseline)
                next(i for i in role['attachments'] if i['id'] == ident).update(fields)
                self.b.save(role)
                before = self.b.profile()
                self.assertIn(55, dict(self.use(ident)))
                self.assertEqual(before, self.b.profile())

    def test_encoding_failure_rolls_back_level_rewards_and_card(self):
        ident = self.setup_card()
        before = self.b.profile()
        with patch.object(self.b, 'journey_attributes', side_effect=ValueError('encode failure')):
            self.assertIn(55, dict(self.use(ident)))
        self.assertEqual(before, self.b.profile())

    def test_catalog_payload_and_client(self):
        from lupa.lua51 import LuaRuntime
        from offline_android.pack_payload import collect_files
        from network_redirect import item_rewards, item_sale
        self.assertIn(1901, f.ITEMS)
        self.assertNotIn(1901, item_rewards.HANDLED)
        self.assertNotIn(1901, item_sale.PRICES)
        files = collect_files()
        for path in ('network_redirect/level_card.py', 'network_redirect/level_card_client.lua',
                     'analysis/configs/local_items/item_base.csv', 'analysis/configs/local_items/item_name.csv'):
            self.assertIn(path, files)
        vm = LuaRuntime()
        vm.execute((Path(__file__).with_name('level_card_client_regression.lua')).read_text(),
                   level_card.client_source())
        vm.execute('assert(loadstring(...))', summon.client_source(summon.load_rules()))
