"""Native trial requests, authoritative combat and persistent daily lifecycle."""
import copy
import json
from pathlib import Path
from unittest.mock import patch

from network_redirect import activity, activity_trial as trial, combat_engine, formation, journey, summon
from network_redirect.backend import Backend
from tests.test_activity import ActivityCase, NOW


class TrialTests(ActivityCase):
    def enter(self):
        out = self.req(1064, flag=2)
        self.ok(out)
        return next(d for e, d in out if e == 75)['train_data']

    def fight(self, **args):
        boss = self.b.profile()['activity']['trial']
        return self.req(1026, **dict(dict(fight_type=11, des_type=8,
                                        des_id=boss['type_id'], des_value=0), **args))

    def fake_battle(self, damage=100, remaining=None):
        actions = combat_engine.Actions()
        actions.append(dict(is_src=True, damage_count=8, damage_list=[damage, 0, 0, 0, 0, 0, 0, 0]))
        actions.damage_totals[1] = damage
        if remaining is not None:
            actions.final_hp = {2: {1: remaining}}
        return patch.object(journey, 'battle', return_value=(3 if remaining == 0 else 4,
                            [dict(src_hp=100, des_hp=100)], actions))

    def test_original_request_and_real_replay(self):
        data = self.enter()
        boss = data['boss_list'][1]
        before = self.b.profile()
        self.ok(self.fight())
        after = self.b.profile()
        lineup = next(d for m, _, d in self.decoded if m == 1028)
        replay = next(d for m, _, d in self.decoded if m == 1027)
        self.assertEqual(lineup['des_name'], trial.NAMES[boss['type_id']])
        self.assertEqual(lineup['lineup'][0]['des_type'], boss['type_id'])
        self.assertEqual(lineup['lineup'][0]['des_hp'], boss['hp'])
        self.assertGreater(len(replay['fight_result']), 0)
        self.assertEqual(after['activity']['trial_count'], 1)
        self.assertLess(after['activity']['trial']['hp'], boss['hp'])
        for k in ('strength', 'energy', 'gold_coin', 'silver_coin'):
            self.assertEqual(before[k], after[k])

    def test_same_day_pool_preview_and_reconnect(self):
        first = self.enter()
        self.assertIn(first['boss_list'][1]['type_id'], trial.POOL)
        self.assertEqual(first['day_max_train_num'], 10)
        self.assertEqual(first['have_broad'], 0)
        self.assertEqual(first, self.enter())
        before = self.b.profile()
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(before, self.b.profile())
        self.assertEqual(first, self.enter())

    def test_original_attributes_and_frozen_daily_difficulty(self):
        self.enter()
        role = self.b.profile()
        boss = copy.deepcopy(role['activity']['trial'])
        _, enemies = journey.fighters(role, boss['config'])
        base = journey.NPCS[boss['type_id']]
        expected = {stat: int(float(base[column]) + float(base[growth]) * 59 * 1.2)
                    for stat, column, growth in zip(formation.STATS, formation.BASE_COLUMNS, formation.GROWTH_COLUMNS)}
        self.assertEqual(boss['max_hp'], expected['hp'] * 12)
        self.assertEqual(boss['unit']['skills'], [list(s) for s in enemies[0]['skills']])
        for stat in ('gongji', 'fangyu', 'magic'):
            self.assertEqual(boss['unit'][stat], expected[stat])
            self.assertGreater(boss['unit'][stat], enemies[0][stat])
        role['level'] = 99
        self.b.save(role)
        self.enter()
        self.assertEqual(boss, self.b.profile()['activity']['trial'])

    def test_growth_boost_preserves_level_one_base(self):
        role = self.b.profile()
        role['level'] = 1
        self.b.save(role)
        self.enter()
        boss = self.b.profile()['activity']['trial']
        _, enemies = journey.fighters(role, boss['config'])
        self.assertEqual(boss['max_hp'], enemies[0]['hp'] * 3)
        for stat in ('gongji', 'fangyu', 'magic'):
            self.assertEqual(boss['unit'][stat], enemies[0][stat])

    def test_wrong_fields_empty_lineup_and_injection_roll_back(self):
        self.enter()
        tid = self.b.profile()['activity']['trial']['type_id']
        for bad in (dict(des_value=tid, des_id=0), dict(des_id=1001), dict(des_type=7)):
            before = self.b.profile()
            self.assertEqual(self.fight(**bad)[0][0], 55)
            self.assertEqual(before, self.b.profile())
        role = self.b.profile()
        for c in role['corteges']:
            c['order'] = 0
        self.b.save(role)
        role = self.b.profile()
        self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(role, self.b.profile())

    def test_damage_cooldown_reconnect_and_no_query_reset(self):
        self.enter()
        hp = self.b.profile()['activity']['trial']['hp']
        with self.fake_battle(100):
            self.ok(self.fight())
        self.assertEqual(self.enter()['boss_list'][1]['hp'], hp - 100)
        self.assertEqual(self.enter()['friend_damage_list'][1]['damage'], 100)
        before = self.b.profile()
        self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(before, self.b.profile())
        with patch('network_redirect.backend.time.time', return_value=NOW + 60), self.fake_battle(200):
            self.ok(self.fight())
        self.assertEqual(self.b.profile()['activity']['trial']['hp'], hp - 300)

    def test_final_health_includes_healing_and_damage_is_not_client_owned(self):
        self.enter()
        hp = self.b.profile()['activity']['trial']['hp']
        with self.fake_battle(hp * 2, hp // 2):
            self.ok(self.fight())
        boss = self.b.profile()['activity']['trial']
        self.assertEqual(boss['hp'], hp // 2)
        self.assertFalse(boss['is_dead'])
        self.assertEqual(self.req(1064, flag=9)[0][0], 55)

    def test_daily_limit_and_midnight_refresh(self):
        self.enter()
        for i in range(10):
            with patch('network_redirect.backend.time.time', return_value=NOW + i * 60), self.fake_battle(1):
                self.ok(self.fight())
        with patch('network_redirect.backend.time.time', return_value=NOW + 600):
            before = self.b.profile()
            self.assertEqual(self.fight()[0][0], 55)
            self.assertEqual(before, self.b.profile())
        midnight = (activity.day(NOW, self.b.activity_rules) + 1) * 86400 - 8 * 3600
        with patch('network_redirect.backend.time.time', return_value=midnight), patch.object(trial.secrets, 'choice', return_value=trial.POOL[-1]):
            data = self.enter()
        self.assertEqual(data['train_times'], 0)
        self.assertEqual(data['last_train_time'], 0)
        self.assertEqual(data['boss_list'][1]['type_id'], trial.POOL[-1])

    def test_claim_exact_preview_once_and_no_respawn(self):
        self.enter()
        with self.fake_battle(100, 0):
            self.ok(self.fight())
        before = self.b.profile()
        self.ok(self.req(1064, flag=9))
        after = self.b.profile()
        for _, tid, count, _ in trial.load_rules()['rewards']:
            total = lambda role: sum(i['count'] for i in role['attachments'] if i['type_id'] == tid and i['attach_type'] == 5)
            self.assertEqual(total(after) - total(before), count)
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(after, self.b.profile())
        self.assertEqual(self.req(1064, flag=9)[0][0], 55)
        self.assertEqual(after, self.b.profile())
        self.assertTrue(self.enter()['daily_complete'])
        self.assertIsNone(self.b.profile()['activity']['trial'])

    def test_pending_reward_survives_shared_reset_and_new_boss_after_claim(self):
        self.enter()
        with self.fake_battle(100, 0):
            self.ok(self.fight())
        old = copy.deepcopy(self.b.profile()['activity']['trial'])
        with patch('network_redirect.backend.time.time', return_value=NOW + 86400):
            role = self.b.profile()
            activity.prepare(role, NOW + 86400, self.b.activity_rules)
            self.b.save(role)
            self.assertEqual(old, self.b.profile()['activity']['trial'])
            self.assertTrue(self.enter()['boss_list'][1]['is_dead'])
            self.ok(self.req(1064, flag=9))
            self.assertFalse(self.enter()['boss_list'][1]['is_dead'])
            self.assertEqual(self.b.profile()['activity']['trial']['day'], old['day'] + 1)

    def test_clock_rollback_rejected(self):
        self.enter()
        before = self.b.profile()
        with patch('network_redirect.backend.time.time', return_value=NOW - 1):
            self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_legacy_earned_reward_migration(self):
        role = self.b.profile()
        role['activity'].pop('trial_meta', None)
        role['activity']['trial'] = dict(type_id=1001, is_dead=True, hp=0, max_hp=50000,
            damage=50000, show_level=60, name='旧首领', prize_list=[activity.prize_spec([5, 1001, 10, 1])])
        self.b.save(role)
        self.enter()
        self.ok(self.req(1064, flag=9))
        self.assertEqual(self.b.profile()['activity']['trial_last_claim']['rewards'], [[5, 1001, 10, 1]])
        self.assertTrue(self.enter()['daily_complete'])

    def test_server_push_only_and_social_requests_do_not_spawn(self):
        for flag in (3, 4, 5, 7, 8):
            before = self.b.profile()
            self.assertEqual(self.req(1064, flag=flag)[0][0], 55)
            self.assertEqual(before, self.b.profile())
        self.ok(self.req(1064, flag=6))
        self.assertIsNone(self.b.profile()['activity']['trial'])

    def test_journey_encounter_once_and_same_daily_boss(self):
        role = self.b.profile()
        with patch.object(trial.secrets, 'randbelow', return_value=0):
            self.assertEqual(len(trial.encounter(role, NOW, self.b.activity_rules)), 1)
            self.assertEqual(trial.encounter(role, NOW, self.b.activity_rules), [])
        tid = role['activity']['trial']['type_id']
        self.b.save(role)
        self.assertEqual(self.enter()['boss_list'][1]['type_id'], tid)

    def test_serialization_failure_rolls_back_reward(self):
        self.enter()
        with self.fake_battle(100, 0):
            self.ok(self.fight())
        before = self.b.profile()
        with patch('network_redirect.backend.activity.attributes', side_effect=ValueError('test')):
            self.assertEqual(self.req(1064, flag=9)[0][0], 55)
        self.assertEqual(before, self.b.profile())
        self.ok(self.req(1064, flag=9))

    def test_config_rejects_invalid_limits_rewards_and_unmarked_inference(self):
        for key, value in [('mode', 'official'), ('daily_attempts', 0), ('cooldown_seconds', True),
                           ('boss_level_cap', 999), ('rewards', [[5, -1, 1, 1]])]:
            r = trial.load_rules()
            r[key] = value
            path = Path(self.tmp.name) / 'invalid.json'
            path.write_text(json.dumps(r))
            with self.assertRaises(formation.Rejected):
                trial.load_rules(path)
