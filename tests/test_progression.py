"""Progression, actual protocol transactions, restart and original-table boundaries."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import formation, journey, progression, summon, welfare
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW = 1793073600
MILESTONES = {20: 1, 30: 1, 40: 1, 50: 1, 60: 1, 70: 2, 80: 2, 90: 2, 99: 3}


class ProgressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = patch('network_redirect.backend.time.time', return_value=NOW)
        self.clock.start()
        self.addCleanup(self.clock.stop)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 100000
        self.state = dict(authenticated=True)

    def req(self, mid=1131, **kw):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **kw))
        self.replies = self.b.respond(self.packet, self.state)
        self.decoded = [decode(p) for p in self.replies]
        self.assertEqual(self.decoded[-1][0], 1106)
        return [(d['id'], login_fields(d['data'])) for m, _, d in self.decoded if m == 2998]

    def role(self, **kw):
        r = self.b.profile()
        r.update(kw)
        self.b.save(r)
        return self.b.profile()

    def buns(self, role):
        return sum(i['count'] for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] == 1020)

    def cards(self, role):
        return sum(i['count'] for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] == 1152)

    def test_all_98_exact_thresholds_and_rewards(self):
        r = self.b.profile()
        expected_cards = expected_buns = expected_gold = 0
        for level in range(1, 99):
            before = copy.deepcopy(r)
            need = int(formation.LEVELS[level]['upgrade_exp'])
            progression.add_exp(r, need - 1, NOW)
            self.assertEqual(r['level'], level)
            self.assertEqual(self.cards(r), expected_cards)
            self.assertEqual(self.buns(r), expected_buns)
            self.assertEqual(r['gold_coin'], expected_gold)
            progression.add_exp(r, 1, NOW)
            reached = level + 1
            expected_buns += 1 + reached // 10
            gold = 100 if reached % 10 == 0 else 50 if reached % 5 == 0 else 20
            expected_gold += gold
            expected_cards += MILESTONES.get(reached, 0)
            self.assertEqual((r['level'], r['cur_exp']), (level + 1, 0))
            self.assertEqual(r['cortege_count'], int(formation.LEVELS[level + 1]['cortege_count']))
            self.assertEqual(self.buns(r), expected_buns)
            self.assertEqual(r['gold_coin'], expected_gold)
            self.assertEqual(self.cards(r), expected_cards)
            event = login_fields(decode(progression.upgrade_events(before, r)[0])[2]['data'])
            expected = [(1020, 1 + reached // 10), (1, gold)] + ([(1152, MILESTONES[level+1])] if level+1 in MILESTONES else [])
            gifts = event['gift_lists_by_level'][level+1]
            self.assertEqual([(p['attach_type'], p['attach_count']) for p in gifts.values()], expected)
            self.assertEqual(event['gift_list'], gifts)
        progression.add_exp(r, 10**12, NOW)
        self.assertEqual((r['level'], r['cur_exp']), (99, 22453200))
        self.assertEqual(self.buns(r), 548)
        self.assertEqual(r['gold_coin'], 2980)
        self.assertEqual(self.cards(r), 14)

    def test_cross_all_levels_gives_every_milestone_once_and_fits_wire(self):
        r = self.b.profile(); before = copy.deepcopy(r)
        xp = sum(int(formation.LEVELS[n]['upgrade_exp']) for n in range(1, 99))
        progression.add_exp(r, xp + 17, NOW)
        self.assertEqual((r['level'], r['cur_exp'], self.buns(r), self.cards(r)), (99, 17, 548, 14))
        self.assertEqual(r['gold_coin'], 2980)
        packet = progression.upgrade_events(before, r)[0]
        self.assertLessEqual(len(packet), 32768)
        by_level = login_fields(decode(packet)[2]['data'])['gift_lists_by_level']
        self.assertEqual(set(by_level), set(range(2, 100)))
        for level, gifts in by_level.items():
            self.assertEqual(sum(p['attach_count'] for p in gifts.values() if p['attach_type'] == 1152), MILESTONES.get(level, 0))
        self.b.save(r)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        r = self.b.profile(); before = copy.deepcopy(r)
        progression.add_exp(r, 0, NOW)
        self.assertEqual(self.cards(r), 14)
        self.assertEqual(progression.upgrade_events(before, r), [])

    def test_all_milestones_actual_battle_inventory_sync_and_packet_retry(self):
        total = 0
        for level, cards in MILESTONES.items():
            before = self.role(level=level-1, cur_exp=int(formation.LEVELS[level-1]['upgrade_exp'])-1,
                               strength=60)
            with patch('network_redirect.journey.battle', return_value=(3, [], [])):
                events = self.req(1026, fight_type=1, des_type=1, des_id=101)
            self.assertNotIn(55, [e for e, d in events])
            r = self.b.profile(); total += cards
            self.assertEqual((r['level'], self.cards(r)), (level, total))
            self.assertEqual(self.buns(r) - self.buns(before), 1 + level // 10)
            gold = 100 if level % 10 == 0 else 50 if level % 5 == 0 else 20
            self.assertEqual(r['gold_coin'] - before['gold_coin'], gold)
            gift = next(d for e, d in events if e == 2)['gift_lists_by_level'][level]
            self.assertEqual(gift[3]['attach_count'], cards)
            attrs = {a['type']: a['value'] for m, _, d in self.decoded if m == 1032 and d['unit_type'] == 1 for a in d['attr_list']}
            self.assertEqual(attrs[8], r['gold_coin'])
            synced = [i for m, _, d in self.decoded if m == 1035 for i in d['attach_list']
                      if i['attach_type'] == 5 and i['type_id'] == 1152]
            self.assertEqual(sum(i['count'] for i in synced), total)
            self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
            self.assertEqual(self.b.profile(), r)
        self.assertEqual(total, 14)

    def test_legacy_milestones_not_retroactively_granted_and_new_one_granted(self):
        r = self.role(level=69, cur_exp=0)
        del r['progression']
        self.b.db.execute('UPDATE roles SET data=? WHERE account=?', (json.dumps(r), self.b.account))
        self.b.db.commit()
        r = self.b.profile()
        self.assertEqual(self.cards(r), 0)
        progression.add_exp(r, int(formation.LEVELS[69]['upgrade_exp']), NOW)
        self.assertEqual((r['level'], self.cards(r)), (70, 2))
        self.b.save(r); self.assertEqual(self.cards(self.b.profile()), 2)

    def test_milestone_encoding_failure_rolls_back_xp_and_cards(self):
        self.role(level=98, cur_exp=int(formation.LEVELS[98]['upgrade_exp'])-1)
        before = self.b.profile(); original = summon.event
        def fail(event, data):
            if event == 2: raise ValueError('forced upgrade wire failure')
            return original(event, data)
        with patch.object(summon, 'event', side_effect=fail), patch('network_redirect.journey.battle', return_value=(3, [], [])):
            events = self.req(1026, fight_type=1, des_type=1, des_id=101)
        self.assertIn(55, [e for e, d in events])
        self.assertEqual(self.b.profile(), before)

    def test_multi_level_remainder_and_native_per_level_gifts(self):
        r = self.b.profile(); before = copy.deepcopy(r)
        progression.add_exp(r, 40 + 110 + 120 + 17, NOW)
        self.assertEqual((r['level'], r['cur_exp'], self.buns(r)), (4, 17, 3))
        event = login_fields(decode(progression.upgrade_events(before, r)[0])[2]['data'])
        self.assertEqual((event['old_level'], event['new_level']), (1, 4))
        self.assertEqual(event['gift_list'][1]['attach_count'], 1)
        progression.add_exp(r, 0, NOW)
        self.assertEqual(self.buns(r), 3)

    def test_invalid_exp_and_config(self):
        r = self.b.profile()
        for v in (-1, True, 1.2):
            before = copy.deepcopy(r)
            with self.assertRaises(formation.Rejected): progression.add_exp(r, v, NOW)
            self.assertEqual(r, before)
        for key, value in [('bun_levels_per_increment', 0), ('bun_increment', True),
                           ('gold_rewards', {'normal': 20}),
                           ('gold_rewards', {'normal': True, 'multiple_of_5': 50, 'multiple_of_10': 100}),
                           ('milestone_rewards', {'20': [[11, 1, 100, 1]]}),
                           ('newbie_days', 0), ('level_rewards', [[5, 999999, 1, 1]]),
                           ('milestone_rewards', None), ('milestone_rewards', {'1': [[5, 1152, 1, 1]]}),
                           ('milestone_rewards', {'100': [[5, 1152, 1, 1]]}),
                           ('milestone_rewards', {'020': [[5, 1152, 1, 1]]}),
                           ('milestone_rewards', {'20': [[5, 1152, 0, 1]]}),
                           ('milestone_rewards', {'20': [[5, 999999, 1, 1]]}),
                           ('milestone_rewards', {'20': [[5, 1152, 1, 1]] * 3}),
                           ('newbie_bonus_percent', True), ('newbie_role_bonus_percent', True),
                           ('level_rewards', [[11, 1, -1, 1]])]:
            rules = progression.load_rules(); rules[key] = value
            path = Path(self.tmp.name) / 'invalid.json'; path.write_text(json.dumps(rules))
            with self.assertRaises(formation.Rejected): progression.load_rules(path)

    def test_legacy_migration_preserves_resources_no_retroactive_reward(self):
        r = self.role(level=40, cur_exp=321)
        del r['progression']; r['next_exp'] = 100; r['cortege_count'] = 2
        self.b.db.execute('UPDATE roles SET data=? WHERE account=?', (json.dumps(r), self.b.account))
        self.b.db.commit()
        migrated = self.b.profile()
        self.assertEqual(migrated['cur_exp'], 321)
        self.assertEqual(self.buns(migrated), self.buns(r))
        self.assertEqual(migrated['progression']['rewarded_level'], 40)
        self.assertEqual(migrated['next_exp'], int(formation.LEVELS[40]['upgrade_exp']))
        progression.add_exp(migrated, migrated['next_exp'] - 321, NOW)
        self.assertEqual(self.buns(migrated) - self.buns(r), 5)

    def test_battle_reward_sync_event_order_and_retry(self):
        before = self.role(cur_exp=39)
        events = self.req(1026, fight_type=1, des_type=1, des_id=101)
        self.assertNotIn(55, [e for e, d in events])
        self.assertEqual(events[-1][0], 44)
        self.assertIn(2, [e for e, d in events])
        after = self.b.profile()
        self.assertEqual((after['level'], after['cur_exp']), (2, 9))
        gain = next(d['exp_plus'] for e, d in events if e == 45 and d['obj_type'] == 1)
        self.assertEqual(gain, 10)
        self.assertEqual(self.buns(after) - self.buns(before), 1)
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.b.profile(), after)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.assertEqual(self.b.profile(), after)

    def test_daily_claim_restart_cross_day_expiry_and_no_catchup(self):
        r = self.role(level=3)
        data = next(d for e, d in self.req(flag=1) if e == 140)
        self.assertTrue(data['can_take']); self.assertEqual(data['left_times'], 7)
        self.assertIn(140, [e for e, d in self.req(flag=2)])
        after = self.b.profile()
        self.assertEqual(self.buns(after) - self.buns(r), 2)
        self.assertEqual(after['silver_coin'] - r['silver_coin'], 10000)
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **kw: None)
        self.assertIn(55, [e for e, d in self.req(flag=2)])
        self.assertEqual(self.b.profile(), after)
        with patch('network_redirect.backend.time.time', return_value=NOW + 2 * 86400):
            self.assertIn(140, [e for e, d in self.req(flag=2)])
            self.assertEqual(len(self.b.profile()['progression']['claimed_days']), 2)
        with patch('network_redirect.backend.time.time', return_value=NOW + 7 * 86400):
            self.assertIn(55, [e for e, d in self.req(flag=2)])
            self.assertEqual(progression.info(self.b.profile(), NOW + 7 * 86400)['buff_type'], 0)

    def test_claim_bad_flags_no_mutation_and_high_level_still_claims(self):
        self.assertIn(55, [e for e, d in self.req(flag=2)])
        self.role(level=30)
        for kw in (dict(flag=3), dict(flag=4), dict(flag=9), dict(flag=2, op_type=1), dict(flag=2, id=1)):
            before = self.b.profile()
            self.assertIn(55, [e for e, d in self.req(**kw)])
            self.assertEqual(self.b.profile(), before)
        self.assertIn(140, [e for e, d in self.req(flag=2)])

    def test_bonus_budget_partial_consumption_and_daily_reset(self):
        r = self.role(level=3)
        r['progression']['strength_used'] = 59
        cfg = dict(strenth_consume='3', exp='100', money='120')
        xp, _, silver = journey.experience(r, cfg, True, self.b.journey_rules, self.b.formation_rules, now=NOW)
        self.assertEqual((xp, silver), (60, 140))  # 15*3 + 15*1; silver retains +50%.
        self.assertEqual(r['progression']['strength_used'], 60)
        xp, _, silver = journey.experience(r, cfg, False, self.b.journey_rules, self.b.formation_rules, now=NOW)
        self.assertEqual(xp, 21)
        self.assertEqual(progression.strength_bonus(r, 2, NOW + 86400)[0], 2)

    def test_bonus_level_boundary_and_expiry(self):
        for level, elapsed, expected in [(1, 0, 1), (2, 0, 1), (3, 0, 1), (29, 0, 1),
                                         (30, 0, 0), (1, 6, 1), (1, 7, 0), (3, 7, 0)]:
            r = self.role(level=level)
            self.assertEqual(progression.strength_bonus(r, 1, NOW + elapsed*86400)[0], expected)

    def test_role_bonus_starts_at_one_and_preserves_other_rewards(self):
        cfg = dict(strenth_consume='1', exp='101', money='101')
        for level, expected_xp, expected_silver in [(1, 10, 101), (2, 20, 101),
                                                   (3, 30, 151), (29, 290, 151), (30, 150, 101)]:
            with self.subTest(level=level):
                r = self.role(level=level, cur_exp=0)
                r['progression']['strength_used'] = 0
                for c in r['corteges']:
                    c.update(level=1, cur_exp=0)
                xp, exps, silver = journey.experience(r, cfg, True, self.b.journey_rules,
                                                       self.b.formation_rules, now=NOW)
                self.assertEqual((xp, silver), (expected_xp, expected_silver))
                self.assertTrue(exps)
                self.assertTrue(all(value == expected_silver for value in exps.values()))
                self.assertEqual(progression.info(r, NOW)['exp_add'], 100 if level < 30 else 0)

    def test_bootstrap_and_welfare_hint_do_not_hide_entry(self):
        self.role(level=3)
        events = [login_fields(d['data']) for m, _, d in map(decode, self.b.bootstrap()) if m == 2998 and d['id'] == 80]
        configs = [d[24] for d in events if 24 in d]
        self.assertTrue(configs); self.assertTrue(all(c['buff_data']['buff_type'] == 1 for c in configs))
        hint = login_fields(decode(welfare.hint(self.b.profile(), NOW, self.b.welfare_rules))[2]['data'])
        self.assertTrue(hint[24]['buff_data']['can_take'])

    def test_failed_reward_encoding_rolls_back_claim(self):
        self.role(level=3); before = self.b.profile()
        original = summon.event
        def fail(event, data):
            if event == 140: raise ValueError('forced wire failure')
            return original(event, data)
        with patch.object(summon, 'event', side_effect=fail):
            self.assertIn(55, [e for e, d in self.req(flag=2)])
        self.assertEqual(self.b.profile(), before)

    def test_rank_energy_experience_and_upgrade(self):
        self.role(level=6, cur_exp=int(formation.LEVELS[6]['upgrade_exp']) - 1)
        self.req(1021, flag=0)
        board = next(d for m, _, d in self.decoded if m == 1022)
        target = next(v for v in board['show_list'] if v['top_relation'] == 2)
        events = self.req(1026, fight_type=2, des_type=2, des_id=target['id'], des_value=target['order'])
        self.assertNotIn(55, [e for e, d in events])
        result = next(d['final_result'] for m, _, d in self.decoded if m == 1027)
        xp = int(formation.LEVELS[6]['energy_win_exp' if 1 <= result <= 3 else 'energy_lose_exp'])
        r = self.b.profile()
        self.assertEqual((r['level'], r['cur_exp'], self.buns(r)), (7, xp - 1, 1))
        self.assertIn(2, [e for e, d in events])
        attrs = {a['type']: a['value'] for m, _, d in self.decoded if m == 1032 and d['unit_type'] == 1 for a in d['attr_list']}
        self.assertEqual(attrs[71], 3)

    def test_rape_sweep_recalculates_each_fights_energy_exp(self):
        self.role(level=25, energy=3, gold_coin=100, cur_exp=int(formation.LEVELS[25]['upgrade_exp']) - 1)
        self.req(1029, flag=1)
        with patch('network_redirect.journey.battle', return_value=(3, [], [])):
            events = self.req(1072)
        self.assertNotIn(55, [e for e, d in events])
        r = self.b.profile()
        expected = int(formation.LEVELS[25]['energy_win_exp']) + 2 * int(formation.LEVELS[26]['energy_win_exp']) - 1
        self.assertEqual((r['level'], r['cur_exp'], r['energy'], self.buns(r)), (26, expected, 0, 3))
        self.assertIn(2, [e for e, d in events])

    def test_sweep_and_practice_allowance_follow_level(self):
        r = self.role(cur_exp=39, vip_level=3, strength=60)
        r['journey']['gates']['1:101'] = dict(pass_star=3, day_count=0, flush_count=0)
        self.b.save(r)
        events = self.req(1061, tollgate_type=1, tollgate_id=101, sweep_count=10)
        self.assertNotIn(55, [e for e, d in events])
        r = self.b.profile()
        # 10 at level 1, six fights at 20, then three at 30: 220 total XP.
        self.assertEqual((r['level'], r['cur_exp'], self.buns(r)), (3, 109, 2))
        self.assertIn(63, [e for e, d in events]); self.assertIn(2, [e for e, d in events])
        r['level'] = 4; r['cur_exp'] = int(formation.LEVELS[4]['upgrade_exp']) - 1
        progression.add_exp(r, 1, NOW)
        self.assertEqual(r['level'] - 4 - r.get('rule_index', 0), 1)


if __name__ == '__main__':
    unittest.main()
