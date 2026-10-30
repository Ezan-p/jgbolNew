"""Native trial requests, authoritative combat and persistent journey lifecycle."""
import copy
import json
from pathlib import Path
from unittest.mock import patch

from network_redirect import activity, activity_trial as trial, combat_engine, formation, journey, summon
from network_redirect.backend import Backend
from tests.test_activity import ActivityCase, NOW


class TrialTests(ActivityCase):
    def seed(self, tier_roll=0, now=NOW):
        role = self.b.profile()
        with patch.object(trial.secrets, 'randbelow', side_effect=[0, tier_roll]):
            self.assertEqual(len(trial.encounter(role, now, self.b.activity_rules)), 1)
        self.b.save(role)
        return role['activity']['trial_bosses'][-1]

    def enter(self, seed=True):
        if seed and not getattr(self, '_seeded', False):
            self._seeded = True
            if not self.b.profile()['activity']['trial_bosses']:
                self.seed()
        out = self.req(1064, flag=2)
        self.ok(out)
        return next(d for e, d in out if e == 75)['train_data']

    def fight(self, **args):
        boss = self.b.profile()['activity']['trial_bosses'][0]
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
        self.assertEqual(after['activity']['trial_bosses'][0]['train_times'], 1)
        self.assertLess(after['activity']['trial_bosses'][0]['hp'], boss['hp'])
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

    def test_original_attributes_and_frozen_encounter_difficulty(self):
        self.enter()
        role = self.b.profile()
        boss = copy.deepcopy(role['activity']['trial_bosses'][0])
        _, enemies = journey.fighters(role, boss['config'])
        base = journey.NPCS[boss['type_id']]
        expected = {stat: int(float(base[column]) + float(base[growth]) * 59 * 1.2)
                    for stat, column, growth in zip(formation.STATS, formation.BASE_COLUMNS, formation.GROWTH_COLUMNS)}
        self.assertEqual(boss['max_hp'], expected['hp'] * 12 * 300 // 100)
        self.assertEqual(boss['unit']['skills'], [list(s) for s in enemies[0]['skills']])
        for stat in ('gongji', 'fangyu', 'magic'):
            self.assertEqual(boss['unit'][stat], expected[stat] * 300 // 100)
            self.assertGreater(boss['unit'][stat], enemies[0][stat])
        role['level'] = 99
        self.b.save(role)
        self.enter()
        self.assertEqual(boss, self.b.profile()['activity']['trial_bosses'][0])

    def test_strength_boost_also_applies_at_level_one(self):
        role = self.b.profile()
        role['level'] = 1
        self.b.save(role)
        self.enter()
        boss = self.b.profile()['activity']['trial_bosses'][0]
        _, enemies = journey.fighters(role, boss['config'])
        self.assertEqual(boss['max_hp'], enemies[0]['hp'] * 3 * 300 // 100)
        base = journey.NPCS[boss['type_id']]
        for stat, column in zip(formation.STATS, formation.BASE_COLUMNS):
            if stat != 'hp':
                self.assertEqual(boss['unit'][stat], int(float(base[column])) * 300 // 100)

    def test_wrong_fields_empty_lineup_and_injection_roll_back(self):
        self.enter()
        tid = self.b.profile()['activity']['trial_bosses'][0]['type_id']
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
        hp = self.b.profile()['activity']['trial_bosses'][0]['hp']
        with self.fake_battle(100):
            self.ok(self.fight())
        self.assertEqual(self.enter()['boss_list'][1]['hp'], hp - 100)
        self.assertEqual(self.enter()['friend_damage_list'][1]['damage'], 100)
        before = self.b.profile()
        self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(before, self.b.profile())
        with patch('network_redirect.backend.time.time', return_value=NOW + 60), self.fake_battle(200):
            self.ok(self.fight())
        self.assertEqual(self.b.profile()['activity']['trial_bosses'][0]['hp'], hp - 300)

    def test_final_health_includes_healing_and_damage_is_not_client_owned(self):
        self.enter()
        hp = self.b.profile()['activity']['trial_bosses'][0]['hp']
        with self.fake_battle(hp * 2, hp // 2):
            self.ok(self.fight())
        boss = self.b.profile()['activity']['trial_bosses'][0]
        self.assertEqual(boss['hp'], hp // 2)
        self.assertFalse(boss['is_dead'])
        self.assertEqual(self.req(1064, flag=9)[0][0], 55)

    def test_per_boss_limit_and_daily_clear(self):
        self.enter()
        second = self.seed()
        for i in range(10):
            with patch('network_redirect.backend.time.time', return_value=NOW + i * 60), self.fake_battle(1):
                self.ok(self.fight())
        with patch('network_redirect.backend.time.time', return_value=NOW + 600):
            before = self.b.profile()
            self.assertEqual(self.fight()[0][0], 55)
            self.assertEqual(before, self.b.profile())
            data = self.enter()
            self.assertEqual([b['train_times'] for b in data['boss_list'].values()], [10,0])
            with self.fake_battle(1):
                self.ok(self.fight(des_id=second['type_id'], des_value=second['boss_id']))
            self.assertEqual([b['train_times'] for b in self.b.profile()['activity']['trial_bosses']], [10,1])
        midnight = (activity.day(NOW, self.b.activity_rules) + 1) * 86400 - 8 * 3600
        with patch('network_redirect.backend.time.time', return_value=midnight):
            data = self.enter()
            self.assertTrue(data['no_boss'])
            self.assertEqual(data['train_times'], 0)
            self.assertEqual(data['last_train_time'], 0)
            new = self.seed(now=midnight)
            self.assertGreater(new['boss_id'], second['boss_id'])
            self.assertEqual(new['train_times'], 0)

    def test_claim_exact_preview_once_and_no_query_respawn(self):
        self.enter()
        with self.fake_battle(100, 0):
            self.ok(self.fight())
        before = self.b.profile()
        self.ok(self.req(1064, flag=9))
        after = self.b.profile()
        for _, tid, count, _ in before['activity']['trial_bosses'][0]['rewards']:
            total = lambda role: sum(i['count'] for i in role['attachments'] if i['type_id'] == tid and i['attach_type'] == 5)
            self.assertEqual(total(after) - total(before), count)
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(after, self.b.profile())
        self.assertEqual(self.req(1064, flag=9)[0][0], 55)
        self.assertEqual(after, self.b.profile())
        self.assertTrue(self.enter()['no_boss'])
        self.assertEqual(self.b.profile()['activity']['trial_bosses'], [])

    def test_midnight_expires_pending_reward_and_resets_pity_without_touching_inventory(self):
        self.enter()
        with self.fake_battle(100, 0):
            self.ok(self.fight())
        old = copy.deepcopy(self.b.profile()['activity']['trial_bosses'][0])
        role = self.b.profile()
        role['activity']['trial_meta']['pity_misses'] = 19
        self.b.save(role)
        inventory = copy.deepcopy(role['attachments'])
        midnight = (activity.day(NOW, self.b.activity_rules) + 1) * 86400 - 8 * 3600
        with patch('network_redirect.backend.time.time', return_value=midnight-1):
            self.assertTrue(self.enter()['boss_list'][1]['is_dead'])
        with patch('network_redirect.backend.time.time', return_value=midnight):
            self.assertEqual(self.req(1064, flag=9, id=old['boss_id'])[0][0], 55)
            data = self.enter()
            self.assertTrue(data['no_boss'])
            self.assertEqual(data['pity_misses'], 0)
            self.assertEqual(self.b.profile()['attachments'], inventory)
            self.seed(now=midnight)
            new = self.b.profile()['activity']['trial_bosses'][0]
            self.assertEqual(new['day'], old['day']+1)
            self.assertGreater(new['boss_id'], old['boss_id'])
            self.assertEqual(self.req(1064, flag=9, id=old['boss_id'])[0][0], 55)
            with patch('network_redirect.backend.time.time', return_value=NOW):
                self.assertEqual(self.req(1064, flag=9, id=old['boss_id'])[0][0], 55)

    def test_clock_rollback_rejected(self):
        self.enter()
        before = self.b.profile()
        with patch('network_redirect.backend.time.time', return_value=NOW - 1):
            self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_legacy_earned_reward_migration(self):
        role = self.b.profile()
        role['activity'].pop('trial_meta', None)
        role['activity'].pop('trial_bosses', None)
        role['activity']['trial'] = dict(type_id=1001, is_dead=True, hp=0, max_hp=50000,
            damage=50000, show_level=60, name='旧首领', prize_list=[activity.prize_spec([5, 1001, 10, 1])])
        self.b.save(role)
        self._seeded = True
        self.enter()
        self.ok(self.req(1064, flag=9))
        self.assertEqual(self.b.profile()['activity']['trial_last_claim']['rewards'], [[5, 1001, 10, 1]])
        self.assertTrue(self.enter()['no_boss'])

    def test_server_push_only_and_social_requests_do_not_spawn(self):
        for flag in (3, 4, 5, 7, 8):
            before = self.b.profile()
            self.assertEqual(self.req(1064, flag=flag)[0][0], 55)
            self.assertEqual(before, self.b.profile())
        self.ok(self.req(1064, flag=6))
        self.assertEqual(self.b.profile()['activity']['trial_bosses'], [])

    def test_query_does_not_spawn_and_capacity_reopens_at_kill(self):
        self.assertTrue(self.enter(seed=False)['no_boss'])
        for _ in range(3):
            self.seed()
        role = self.b.profile()
        self.assertEqual(len({b['type_id'] for b in role['activity']['trial_bosses']}), 3)
        with patch.object(trial.secrets, 'randbelow') as roll:
            self.assertEqual(trial.encounter(role, NOW, self.b.activity_rules), [])
            roll.assert_not_called()
        with self.fake_battle(100, 0):
            self.ok(self.fight())
        dead = self.b.profile()['activity']['trial_bosses'][0]
        self.seed()
        bosses = self.b.profile()['activity']['trial_bosses']
        self.assertEqual(sum(not b['is_dead'] for b in bosses), 3)
        self.assertEqual(len(bosses), 4)
        self.ok(self.req(1064, flag=9, id=dead['boss_id']))
        self.assertEqual(self.req(1064, flag=9, id=dead['boss_id'])[0][0], 55)

    def test_encounter_and_tier_roll_boundaries(self):
        for roll, expected in [(0,'low'),(69,'low'),(70,'medium'),(94,'medium'),(95,'high'),(99,'high')]:
            role = self.b.profile()
            role['activity']['trial_bosses'] = []
            with patch.object(trial.secrets, 'randbelow', side_effect=[9, roll]):
                self.assertEqual(len(trial.encounter(role, NOW, self.b.activity_rules)), 1)
            self.assertEqual(role['activity']['trial_bosses'][0]['tier'], expected)
        for roll in (10, 99):
            role = self.b.profile()
            with patch.object(trial.secrets, 'randbelow', return_value=roll) as rng:
                self.assertEqual(trial.encounter(role, NOW, self.b.activity_rules), [])
                self.assertEqual(rng.call_count, 1)

    def test_journey_wire_push_success_only_and_replay_no_reroll(self):
        role = self.b.profile()
        role['strength'] = 100
        for gid, cfg in journey.GATES[1].items():
            if int(cfg['map_id']) == 1:
                role['journey']['gates'][f'1:{gid}'] = dict(pass_star=3, day_count=0, flush_count=0)
        self.b.save(role)
        for fight_type in (1, 20):
            with self.fake_battle(100, 0), patch.object(trial.secrets, 'randbelow', return_value=0):
                out = self.req(1026, fight_type=fight_type, des_type=1, des_id=101)
            self.ok(out)
            push = next(d for e,d in out if e==75)
            self.assertEqual(push['flag'], 5)
            self.assertEqual(out[-1][0], 44)
            before = self.b.profile()
            self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
            self.assertEqual(before,self.b.profile())
        with self.fake_battle(100), patch.object(trial, 'encounter') as encounter:
            self.ok(self.req(1026, fight_type=1, des_type=1, des_id=101))
            encounter.assert_not_called()
        with patch.object(trial, 'encounter') as encounter:
            self.ok(self.req(1061, tollgate_type=1, sweep_count=1, tollgate_id=101))
            encounter.assert_not_called()

    def test_three_tier_attributes_rewards_and_manual_boundaries(self):
        r = trial.load_rules()
        for level in (*range(1,100),100,101):
            base = journey.NPCS[5001]
            raw = {stat: max(1, int(float(base[column])+float(base[growth])*(min(level,100)-1)*1.2))
                   for stat,column,growth in zip(formation.STATS,formation.BASE_COLUMNS,formation.GROWTH_COLUMNS)}
            raw['hp'] *= min(12,3+(min(level,100)-1)//3)
            for roll, multiplier, reward_multiplier in [(0,300,1),(70,450,2),(95,900,4)]:
                role = self.b.profile()
                role['level'] = level
                role['activity']['trial_bosses'] = []
                with patch.object(trial.secrets, 'choice', return_value=5001), patch.object(trial.secrets, 'randbelow', return_value=roll):
                    boss = trial.spawn(role, role['activity'], r)
                for stat in formation.STATS:
                    self.assertEqual(boss['unit'][stat], raw[stat] * multiplier // 100)
                grade = min(19, (level - 1) // 5)
                self.assertEqual(boss['rewards'], [[5,1041+2*grade,3*reward_multiplier,1],[5,1042+2*grade,reward_multiplier,1]])
                self.assertEqual(boss['show_level'], min(level,100))
                self.assertEqual(boss['prize_list'], [activity.prize_spec(p) for p in boss['rewards']])

    def test_level99_top_manuals_claim_exact_preview_for_all_tiers(self):
        for roll, normal, advanced in [(0,3,1),(70,6,2),(95,12,4)]:
            role = self.b.profile()
            role['level'] = 99
            role['activity']['trial_next'] = 0
            self.b.save(role)
            boss = self.seed(tier_roll=roll)
            self.assertEqual(boss['manual_grade'],20)
            self.assertEqual(boss['rewards'],[[5,1079,normal,1],[5,1080,advanced,1]])
            before = self.b.profile()
            with self.fake_battle(1,0):
                self.ok(self.fight())
            self.ok(self.req(1064,flag=9,id=boss['boss_id']))
            after = self.b.profile()
            for tid,count in [(1079,normal),(1080,advanced)]:
                def total(role):
                    return sum(i['count'] for i in role['attachments'] if i['type_id']==tid and i['attach_type']==5)
                self.assertEqual(total(after)-total(before),count)

    def test_multiple_targets_and_stale_instance_rejected(self):
        first, second, third = [self.seed() for _ in range(3)]
        with self.fake_battle(100, 0):
            self.ok(self.req(1026, fight_type=11, des_type=8, des_id=second['type_id'], des_value=second['boss_id']))
        bosses = self.b.profile()['activity']['trial_bosses']
        self.assertFalse(bosses[0]['is_dead'])
        self.assertTrue(bosses[1]['is_dead'])
        self.assertFalse(bosses[2]['is_dead'])
        self.assertEqual(self.req(1064, flag=9)[0][0], 55)
        self.ok(self.req(1064, flag=9, id=second['boss_id']))
        with patch.object(trial.secrets, 'choice', return_value=second['type_id']):
            new = self.seed()
        self.assertNotEqual(new['boss_id'], second['boss_id'])
        with patch('network_redirect.backend.time.time', return_value=NOW + 60):
            self.assertEqual(self.req(1026, fight_type=11, des_type=8, des_id=second['type_id'], des_value=second['boss_id'])[0][0], 55)

    def test_live_v2_migration_preserves_snapshot(self):
        self.seed()
        role = self.b.profile()
        old = role['activity']['trial_bosses'].pop()
        old.pop('boss_id')
        old['hp'] -= 10
        role['activity'].pop('trial_bosses')
        role['activity']['trial'] = copy.deepcopy(old)
        role['activity']['trial_meta'].update(spawned=True,type_id=old['type_id'])
        self.b.save(role)
        self.enter(seed=False)
        migrated = self.b.profile()['activity']['trial_bosses'][0]
        self.assertEqual({k:v for k,v in migrated.items() if k != 'boss_id'},old)

    def test_serialization_failure_rolls_back_reward(self):
        self.enter()
        with self.fake_battle(100, 0):
            self.ok(self.fight())
        before = self.b.profile()
        with patch('network_redirect.backend.activity.attributes', side_effect=ValueError('test')):
            self.assertEqual(self.req(1064, flag=9)[0][0], 55)
        self.assertEqual(before, self.b.profile())
        self.ok(self.req(1064, flag=9))

    def test_twentieth_eligible_win_guarantees_encounter_and_resets(self):
        role = self.b.profile()
        with patch.object(trial.secrets, 'randbelow', return_value=99) as rng:
            for misses in range(1,20):
                self.assertEqual(trial.encounter(role,NOW,self.b.activity_rules), [])
                self.assertEqual(role['activity']['trial_meta']['pity_misses'], misses)
            self.assertEqual(rng.call_count,19)
            self.assertEqual(len(trial.encounter(role,NOW,self.b.activity_rules)),1)
            self.assertEqual(rng.call_count,20)  # Only the tier roll on the guaranteed encounter.
        self.assertEqual(role['activity']['trial_meta']['pity_misses'],0)
        self.assertEqual(role['activity']['trial_bosses'][0]['tier'],'high')
        role['activity']['trial_meta']['pity_misses']=7
        with patch.object(trial.secrets,'randbelow',return_value=0):
            trial.encounter(role,NOW,self.b.activity_rules)
        self.assertEqual(role['activity']['trial_meta']['pity_misses'],0)

    def test_capacity_and_clock_rollback_do_not_accumulate_pity(self):
        for _ in range(3):
            self.seed()
        role=self.b.profile()
        role['activity']['trial_meta']['pity_misses']=8
        with patch.object(trial.secrets,'randbelow') as rng:
            for _ in range(30):
                self.assertEqual(trial.encounter(role,NOW,self.b.activity_rules),[])
            self.assertEqual(role['activity']['trial_meta']['pity_misses'],8)
            role['activity']['trial_bosses'][0]['is_dead']=True
            self.assertEqual(trial.encounter(role,NOW-1,self.b.activity_rules),[])
            rng.assert_not_called()
        with patch.object(trial.secrets,'randbelow',return_value=99):
            trial.encounter(role,NOW,self.b.activity_rules)
        self.assertEqual(role['activity']['trial_meta']['pity_misses'],9)

    def test_v3_shared_attempts_migrate_once_and_new_boss_has_own_budget(self):
        self.seed()
        second=self.seed()
        role=self.b.profile()
        for b in role['activity']['trial_bosses']:
            b.pop('train_times')
        role['activity']['trial_count']=10
        self.b.save(role)
        self.assertEqual([b['train_times'] for b in self.enter()['boss_list'].values()],[0,0])
        with self.fake_battle(1):
            self.ok(self.fight())
        # Attempts are independent; the existing 60-second cooldown remains shared.
        self.assertEqual(self.fight(des_id=second['type_id'],des_value=second['boss_id'])[0][0],55)
        self.assertEqual([b['train_times'] for b in self.enter()['boss_list'].values()],[1,0])
        self.assertNotIn('trial_count',self.b.profile()['activity'])

    def test_v3_carried_bosses_expire_even_when_meta_day_is_current(self):
        self.seed()
        self.seed()
        role=self.b.profile()
        first,second=role['activity']['trial_bosses']
        first.update(day=first['day']-1,is_dead=True,hp=0)
        second.update(day=second['day']-1)
        next_id=role['activity']['trial_meta']['next_id']
        self.b.save(role)
        self.assertTrue(self.enter(seed=False)['no_boss'])
        self.assertEqual(self.b.profile()['activity']['trial_meta']['next_id'],next_id)

    def test_journey_miss_replay_and_failure_do_not_advance_pity_twice(self):
        with self.fake_battle(1,0), patch.object(trial.secrets,'randbelow',return_value=99):
            self.ok(self.req(1026,fight_type=1,des_type=1,des_id=101))
        self.assertEqual(self.b.profile()['activity']['trial_meta']['pity_misses'],1)
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(self.b.profile()['activity']['trial_meta']['pity_misses'],1)
        before=self.b.profile()
        with self.fake_battle(1,0), patch.object(trial.secrets,'randbelow',return_value=99), patch('network_redirect.journey.encode',side_effect=ValueError('test')):
            self.assertEqual(self.req(1026,fight_type=1,des_type=1,des_id=101)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_config_rejects_invalid_limits_rewards_and_unmarked_inference(self):
        for key, value in [('mode', 'official'), ('daily_attempts', 0), ('journey_pity_wins', 0), ('journey_pity_wins', True), ('cooldown_seconds', True),
                           ('boss_level_cap', 999), ('max_alive_bosses', 4), ('manual_level_step', 0),
                           ('manual_pairs', [[1041, 1042]]), ('tiers', []), ('rewards', [[5, -1, 1, 1]])]:
            r = trial.load_rules()
            r[key] = value
            path = Path(self.tmp.name) / 'invalid.json'
            path.write_text(json.dumps(r))
            with self.assertRaises(formation.Rejected):
                trial.load_rules(path)
