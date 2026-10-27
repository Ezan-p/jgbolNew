"""Journey integration tests using real wire packets and isolated SQLite saves."""
import copy
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import journey, formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW = 1792771200


class JourneyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.time = patch('network_redirect.backend.time.time', return_value=NOW)
        self.time.start()
        self.addCleanup(self.time.stop)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 100000
        self.state = dict(authenticated=True)

    def req(self, mid, **kw):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **kw))
        self.replies = self.b.respond(self.packet, self.state)
        self.decoded = [decode(p) for p in self.replies]
        self.assertEqual(self.decoded[-1][0], 1106)
        self.assertEqual(self.decoded[-1][2]['req_serial_num'], self.serial)
        self.events = [(d['id'], login_fields(d['data'])) for m, _, d in self.decoded if m == 2998]
        return self.events

    def fight(self, gid=101, kind=1):
        return self.req(1026, fight_type=1 if kind == 1 else 20, des_type=1, des_id=gid)

    def fixture(self, **kw):
        r = self.b.profile()
        r.update(kw)
        self.b.save(r)
        return self.b.profile()

    def clear_map(self, mid=1, stars=3):
        r = self.b.profile()
        for gid, cfg in journey.GATES[1].items():
            if int(cfg['map_id']) == mid:
                r['journey']['gates'][f'1:{gid}'] = dict(pass_star=stars, day_count=0, flush_count=0)
        self.b.save(r)

    def test_initial_query_not_all_stages_unlocked(self):
        self.req(1018, flag=1)
        rows = [g for m, _, d in self.decoded if m == 1020 for g in d['tollgate_list']]
        self.assertEqual([(g['tollgate_type'], g['tollgate_id']) for g in rows], [(1, 101)])
        self.assertEqual(len(journey.GATES[1]), 597)
        self.assertEqual(len(journey.GATES[2]), 67)

    def test_fight_native_replay_rewards_and_progress(self):
        before = self.b.profile()
        self.fight()
        after = self.b.profile()
        self.assertNotIn(55, [k for k, _ in self.events])
        result = next(d for m, _, d in self.decoded if m == 1027)
        self.assertEqual(result['final_result'], 3)
        self.assertTrue(result['fight_result'])
        self.assertEqual(after['strength'], before['strength'] - 1)
        self.assertEqual(after['silver_coin'], before['silver_coin'] + 150)
        self.assertEqual(after['cur_exp'], 5)
        self.assertTrue(journey.unlocked(after, 1, 102))
        mids = [m for m, _, d in self.decoded]
        self.assertLess(mids.index(1028), mids.index(1027))
        self.assertEqual(self.events[-1][0], 44)
        self.assertEqual(after['corteges'][0]['cur_exp'], 100)
        self.assertEqual([d['tollgate_id'] for m, _, d in self.decoded if m == 1019], [101])
        opened = [g for m, _, d in self.decoded if m == 1020 for g in d['tollgate_list']]
        self.assertEqual([g['tollgate_id'] for g in opened], [102])
        self.assertTrue(all(not d['first_send'] for m, _, d in self.decoded if m == 1020))

    def test_repeat_packet_does_not_charge_or_roll_again(self):
        self.fight()
        before = self.b.profile()
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.b.profile(), before)
        bad = encode(1026, dict(serial_num=self.serial, fight_type=1, des_type=1, des_id=102))
        self.assertEqual(decode(self.b.respond(bad, self.state)[0])[2]['id'], 55)
        self.assertEqual(self.b.profile(), before)

    def test_locked_invalid_or_wrong_target_never_charges(self):
        for kw in [dict(des_id=201), dict(des_id=0), dict(des_id=101.5), dict(des_id=float('nan')),
                   dict(fight_type=3), dict(des_type=4), dict(des_value=1)]:
            with self.subTest(kw=kw):
                before = self.b.profile()
                self.req(1026, **dict(dict(fight_type=1, des_type=1, des_value=0, des_id=101), **kw))
                self.assertEqual(self.events[0][0], 55)
                self.assertEqual(self.b.profile(), before)

    def test_no_strength_and_no_lineup_reject(self):
        self.fixture(strength=0)
        before = self.b.profile()
        self.fight()
        self.assertEqual(self.b.profile(), before)
        r = self.fixture(strength=10)
        r['corteges'][0]['order'] = 0
        self.b.save(r)
        self.fight()
        self.assertEqual(self.events[0][0], 55)

    def test_loss_is_real_does_not_unlock_or_award_win(self):
        self.fixture(level=60, strength=30)
        self.clear_map()
        # Original elite stats substantially exceed the starter's stats.
        with patch('network_redirect.journey.secrets.randbelow', return_value=99):
            self.fight(101, 2)
        r = self.b.profile()
        result = next(d['final_result'] for m, _, d in self.decoded if m == 1027)
        self.assertGreaterEqual(result, 4)
        self.assertEqual(r['elite_fight_count'], 1)
        self.assertEqual(r['journey']['gates']['2:101']['pass_star'], 0)
        self.assertFalse(journey.unlocked(r, 2, 201))
        self.assertEqual(r['strength'], 28)

    def test_hp_star_thresholds(self):
        self.assertEqual([journey.stars(n, 100) for n in (1, 39, 40, 69, 70, 100)], [1, 1, 2, 2, 3, 3])

    def test_placeholder_is_not_a_fifty_million_hp_enemy_or_shifted_reserve(self):
        for kind, gid in ((1, 2008), (1, 6710), (2, 2601), (2, 6701)):
            cfg = journey.GATES[kind][gid]
            enemies = journey.fighters(self.b.profile(), cfg)[1]
            self.assertFalse(any(u['type'] == 8888 for u in enemies))
            expected = [(i, int(token.split('|')[0])) for i, token in enumerate(cfg['cortege_list'].split('/'), 1)
                        if int(token.split('|')[0]) != 8888]
            self.assertEqual([(u['order'], u['type']) for u in enemies], expected)
        from network_redirect import npc_players
        key = max(npc_players.catalog(), key=lambda k: npc_players.catalog()[k]['profile']['role_combat_power'])
        role = npc_players.get(key)['role']
        for kind, gid in ((1, 6710), (2, 6701)):
            result, lineup, actions = journey.battle(role, journey.GATES[kind][gid], self.b.journey_rules)
            self.assertIn(result, (1, 2, 3))
            self.assertEqual(actions.stop_reason, 'elimination')
            replay = decode(encode(1028, dict(lineup_count=len(lineup), lineup=lineup)))[2]
            self.assertEqual(replay['lineup'][4]['des_type'], 0)
            self.assertNotEqual(replay['lineup'][5]['des_type'], 0)

    def test_first_drop_and_first_three_star_once(self):
        r = self.b.profile()
        cfg = journey.GATES[1][105]
        with patch('network_redirect.journey.secrets.randbelow', return_value=0):
            first, _ = journey.attempt(r, 1, 105, cfg, 3, NOW, self.b.journey_rules, self.b.formation_rules)
            second, _ = journey.attempt(r, 1, 105, cfg, 3, NOW, self.b.journey_rules, self.b.formation_rules)
        self.assertEqual({i['attach_type'] for i in first['send_prize_list']}, {2038, 2030})
        self.assertEqual(second['send_prize_list'], [])

    def test_full_star_map_reward_exactly_once_and_persistent(self):
        self.req(1201, flag=3, id=1)
        self.assertEqual(self.events[0][0], 55)
        self.clear_map()
        self.req(1201, flag=3, id=1)
        r = self.b.profile()
        self.assertEqual(r['journey']['claimed_maps'], [1])
        self.assertEqual(sum(i['count'] for i in r['attachments'] if i['type_id'] == 1022), 1)
        self.req(1201, flag=3, id=1)
        self.assertEqual(self.b.profile(), r)
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.b.profile()['journey']['claimed_maps'], [1])

    def test_first_win_extra_companion_experience_only_once(self):
        r = self.fixture(level=30, strength=60)
        cfg = journey.GATES[1][308]
        self.assertEqual(cfg['first_win_prize'], '800|100')
        with patch('network_redirect.journey.secrets.randbelow', return_value=0):
            first, _ = journey.attempt(r, 1, 308, cfg, 3, NOW, self.b.journey_rules, self.b.formation_rules)
            repeat, _ = journey.attempt(r, 1, 308, cfg, 3, NOW, self.b.journey_rules, self.b.formation_rules)
        self.assertEqual(first['exp_list'][1], int(cfg['exp']) + 800)
        self.assertEqual(repeat['exp_list'][1], int(cfg['exp']))

    def test_sweep_gate_level_vip_cooldown_and_resources(self):
        self.fight()
        self.req(1061, tollgate_type=1, sweep_count=1, tollgate_id=101)
        self.assertEqual(self.events[0][0], 55)
        self.fixture(level=30, strength=60)
        before = self.b.profile()
        self.req(1061, tollgate_type=1, sweep_count=10, tollgate_id=101)
        self.assertEqual(self.events[0][0], 63)
        self.assertEqual(len(self.events[0][1]), 10)
        r = self.b.profile()
        self.assertEqual(r['strength'], 50)
        self.assertEqual(r['silver_coin'] - before['silver_coin'], 1500)
        self.assertEqual(r['last_sweep_time'], NOW)
        self.req(1061, tollgate_type=1, sweep_count=1, tollgate_id=101)
        self.assertEqual(self.events[0][0], 55)
        self.assertEqual(self.b.profile(), r)

    def test_sweep_does_not_upgrade_historical_stars(self):
        self.fixture(level=30)
        self.clear_map(stars=1)
        self.req(1061, tollgate_type=1, sweep_count=1, tollgate_id=105)
        self.assertEqual(journey.progress(self.b.profile(), 1, 105)['pass_star'], 1)
        self.assertFalse(any(i['type_id'] == 2030 for i in self.b.profile()['attachments']))

    def test_sweep_rejects_batch_over_limits_atomically(self):
        self.fixture(level=30, strength=5)
        self.clear_map()
        for n in (0, 11, 10):
            before = self.b.profile()
            self.req(1061, tollgate_type=1, sweep_count=n, tollgate_id=101)
            self.assertEqual(self.events[0][0], 55)
            self.assertEqual(before, self.b.profile())

    def test_sweep_cooldown_refresh_prices_and_limit(self):
        self.fixture(level=30, gold_coin=100, last_sweep_time=NOW)
        before = self.b.profile()
        self.req(1062, cost_gold=0)
        self.assertEqual(before, self.b.profile())
        self.req(1062, cost_gold=5)
        self.assertEqual(self.b.profile()['gold_coin'], 95)
        self.assertEqual(next(d['error_code'] for m, _, d in self.decoded if m == 1063), 0)
        self.assertEqual(self.b.profile()['last_sweep_time'], 0)
        self.req(1062, cost_gold=5)
        self.assertEqual(self.events[0][0], 55)
        self.fixture(last_sweep_time=NOW, sweep_flush_count=30)
        self.req(1062, cost_gold=5)
        self.assertEqual(self.events[0][0], 55)

    def test_normal_refresh_vip_and_official_price(self):
        self.fight()
        self.fixture(gold_coin=100)
        self.req(1050, tollgate_type=1, tollgate_id=101)
        self.assertEqual(self.events[0][0], 55)
        self.fixture(vip_level=1)
        self.req(1050, tollgate_type=1, tollgate_id=101)
        self.assertEqual(self.events[-1][0], 56)
        self.assertEqual(self.events[-1][1], dict(tollgate_id=101, day_fight_count=0, day_flush_count=1))
        r = self.b.profile()
        self.assertEqual(r['gold_coin'], 80)
        self.assertEqual(journey.progress(r, 1, 101), dict(pass_star=3, day_count=0, flush_count=1))

    def test_elite_vip_extra_attempts_and_thirty_global_cap(self):
        r = self.fixture(level=30, vip_level=1, strength=60, gold_coin=100)
        self.clear_map()
        r = self.b.profile()
        r['journey']['gates']['2:101'] = dict(pass_star=3, day_count=0, flush_count=0)
        self.b.save(r)
        self.req(1061, tollgate_type=2, tollgate_id=101, sweep_count=5)
        r = self.b.profile()
        self.assertEqual((r['elite_fight_count'], r['strength']), (5, 50))
        self.req(1050, tollgate_type=2, tollgate_id=101)
        r = self.b.profile()
        self.assertEqual(r['gold_coin'], 70)
        self.assertEqual(self.events[-1][1], dict(tollgate_id=101, day_fight_count=0, day_flush_count=1))
        normal = [g for m, _, d in self.decoded if m == 1020 for g in d['tollgate_list'] if g['tollgate_type'] == 1]
        self.assertEqual(normal[0]['day_count'], 0)
        self.fixture(elite_fight_count=30, last_sweep_time=0)
        before = self.b.profile()
        self.req(1061, tollgate_type=2, tollgate_id=101, sweep_count=1)
        self.assertEqual(self.events[0][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_daily_rollover_retains_stars_and_cooldown(self):
        self.fight()
        r = self.b.profile()
        r.update(last_sweep_time=NOW, sweep_flush_count=2)
        journey.prepare(r, NOW + 86400, self.b.journey_rules)
        self.assertEqual(journey.progress(r, 1, 101), dict(day_count=0, flush_count=0, pass_star=3))
        self.assertEqual(r['sweep_flush_count'], 0)
        self.assertEqual(r['last_sweep_time'], NOW)

    def test_recovery_caps_no_overcap_truncation(self):
        r = self.fixture(strength=29, energy=14)
        journey.prepare(r, NOW + 3600, self.b.journey_rules)
        self.assertEqual((r['strength'], r['energy']), (30, 15))
        r['strength'] = 60
        journey.prepare(r, NOW + 7200, self.b.journey_rules)
        self.assertEqual(r['strength'], 60)

    def test_eat_and_buy_resource_item_and_limits(self):
        r = self.fixture(strength=0, gold_coin=100)
        summon.add_item(r, 1022, 1)
        self.b.save(r)
        item = next(i for i in r['attachments'] if i['type_id'] == 1022)
        self.req(1051, item_type=1022, item_id=item['id'], item_count=0, des_type=1)
        self.assertEqual(self.b.profile()['strength'], 10)
        self.req(1058, type_id=1022)
        r = self.b.profile()
        self.assertEqual((r['strength'], r['gold_coin'], r['strength_item_count']), (20, 80, 2))
        self.fixture(strength_item_count=10)
        self.req(1058, type_id=1022)
        self.assertEqual(self.events[0][0], 55)

    def test_large_progress_chunks_and_complete_catalog(self):
        for mid in journey.MAPS[1]:
            self.clear_map(mid)
        self.req(1018, flag=1)
        chunks = [d for m, _, d in self.decoded if m == 1020]
        self.assertGreater(len(chunks), 1)
        self.assertTrue(chunks[0]['first_send'])
        self.assertTrue(all(not c['first_send'] for c in chunks[1:]))
        self.assertEqual(sum(c['tollgate_count'] for c in chunks), 598)

    def test_all_catalog_enemies_and_rewards_resolve(self):
        r = self.fixture(level=99)
        for kind, gates in journey.GATES.items():
            for gid, cfg in gates.items():
                with self.subTest(kind=kind, gid=gid):
                    ours, enemies = journey.fighters(r, cfg)
                    self.assertTrue(1 <= len(enemies) <= 8)
                    with patch('network_redirect.journey.secrets.randbelow', return_value=0):
                        result, lineup, actions = journey.battle(r, cfg, self.b.journey_rules)
                    for mid, fields in ((1028, dict(fight_id=1, first_hand=1, lineup_count=len(lineup), lineup=lineup)),
                                        (1027, dict(fight_id=1, fight_type=1 if kind == 1 else 20,
                                                    final_result=result, fight_round=len(actions), fight_result=actions))):
                        decoded = decode(encode(mid, fields))[2]
                        self.assertEqual(decoded['fight_id'], 1)
                    self.assertTrue(actions)
                    for field in ('random_prize', 'first_random_prize', 'com_win_prize'):
                        with patch('network_redirect.journey.secrets.randbelow', return_value=0):
                            journey.drops(copy.deepcopy(r), cfg[field])

    def test_role_level_up_and_slots(self):
        self.fixture(cur_exp=39)
        self.fight()
        r = self.b.profile()
        self.assertEqual((r['level'], r['cur_exp'], r['next_exp']), (2, 4, 110))
        self.assertEqual(r['cortege_count'], int(formation.LEVELS[2]['cortege_count']))

    def test_bad_config_fails_closed(self):
        rules = copy.deepcopy(self.b.journey_rules)
        rules['battle']['max_actions'] = 256
        p = Path(self.tmp.name) / 'bad.json'
        p.write_text(json.dumps(rules))
        with self.assertRaises(formation.Rejected):
            journey.load_rules(p)

    def test_every_catalog_probability_has_exact_integer_boundary(self):
        # Exhaust the uniform RNG domain: no flaky approximate statistics.
        rates = {p[4] for gates in journey.GATES.values() for cfg in gates.values()
                 for field in ('first_random_prize', 'random_prize', 'com_win_prize')
                 for p in journey.reward_entries(cfg[field])}
        for rate in rates:
            hits = 0
            with patch('network_redirect.journey.grant', return_value={'hit': True}):
                for roll in range(100):
                    with patch('network_redirect.journey.secrets.randbelow', return_value=roll):
                        hits += len(journey.drops({}, f'5|1022|1|1|{rate}'))
            self.assertEqual(hits, rate, rate)
        with patch('network_redirect.journey.grant', side_effect=lambda r, p: p), \
                patch('network_redirect.journey.secrets.randbelow', side_effect=[9, 10, 99, 0]):
            rewards = journey.drops({}, '5|1022|1|1|10/5|1023|1|1|10/11|1|30|1|100/12|1|99|1|0')
        self.assertEqual(rewards, [(5, 1022, 1, 1), (11, 1, 30, 1)])

    def test_bad_rewards_reject_before_any_roll_or_grant(self):
        for spec in ('5|1022|1|1|-1', '5|1022|1|1|101', '5|1022|0|1|10',
                     '5|1022|1|0|10', '5|1022|1|1', '5|1022|1|1|10|99'):
            with self.subTest(spec=spec), patch('network_redirect.journey.secrets.randbelow') as rng, \
                    patch('network_redirect.journey.grant') as grant:
                with self.assertRaises(formation.Rejected):
                    journey.drops({}, '5|1022|1|1|100/' + spec)
                rng.assert_not_called()
                grant.assert_not_called()

    def test_catalog_rejects_unreachable_bad_reward_and_enemy(self):
        cfg = journey.GATES[2][6701]
        for change in ({'random_prize': '5|999999|1|1|0'}, {'cortege_list': '999999|1'},
                       {'first_win_prize': '100|101'}, {'pre_tollgate': '999999'}):
            with self.subTest(change=change), patch.dict(cfg, change):
                with self.assertRaises(formation.Rejected):
                    journey.load_rules()

    def test_failed_first_attempt_retains_first_win_and_three_star_rewards(self):
        role = self.b.profile()
        cfg = journey.GATES[1][105]
        for result in (0, 4, 5, 6):
            outcome, events = journey.attempt(role, 1, 105, cfg, result, NOW, self.b.journey_rules, self.b.formation_rules)
            self.assertEqual(outcome['send_prize_list'], [])
            self.assertEqual(events, [])
            self.assertEqual(journey.progress(role, 1, 105)['pass_star'], 0)
        with patch('network_redirect.journey.secrets.randbelow', return_value=0):
            outcome, _ = journey.attempt(role, 1, 105, cfg, 3, NOW, self.b.journey_rules, self.b.formation_rules)
        self.assertEqual({p['attach_type'] for p in outcome['send_prize_list']}, {2038, 2030})

    def test_elite_reward_preserves_original_item_level(self):
        role = self.b.profile()
        with patch('network_redirect.journey.secrets.randbelow', return_value=99):
            rewards = journey.drops(role, journey.GATES[2][201]['com_win_prize'])
        self.assertEqual(rewards[0]['attach_level'], 4)
        self.assertTrue(any(i['type_id'] == 1090 and i['level'] == 4 for i in role['attachments']))

    def test_sweep_rolls_each_attempt_and_late_failure_rolls_back(self):
        self.fixture(level=30, strength=60)
        self.clear_map()
        spec = '5|1022|1|1|50'
        with patch.dict(journey.GATES[1][101], random_prize=spec), \
                patch('network_redirect.journey.secrets.randbelow', side_effect=[49, 50, 0]):
            self.req(1061, tollgate_type=1, tollgate_id=101, sweep_count=3)
        results = next(data for event, data in self.events if event == 63)
        self.assertEqual([sum(p['attach_type'] == 1022 for p in r['send_prize_list'].values())
                          for r in results.values()], [1, 0, 1])
        self.assertEqual(sum(i['count'] for i in self.b.profile()['attachments'] if i['type_id'] == 1022), 2)
        self.fixture(last_sweep_time=0)
        before = self.b.profile()
        real_attempt = journey.attempt
        calls = []
        def fail_second(*args, **kwargs):
            calls.append(1)
            if len(calls) == 2:
                raise ValueError('second settlement failure')
            return real_attempt(*args, **kwargs)
        with patch('network_redirect.journey.attempt', side_effect=fail_second):
            self.req(1061, tollgate_type=1, tollgate_id=101, sweep_count=3)
        self.assertEqual(self.events[0][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_query_validates_flag_and_encodes_before_save(self):
        before = self.b.profile()
        self.req(1018, flag=255)
        self.assertEqual(self.events[0][0], 55)
        self.assertEqual(self.b.profile(), before)
        with patch('network_redirect.journey.encode', side_effect=ValueError('snapshot failure')):
            self.req(1018, flag=1)
        self.assertEqual(self.events[0][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_query_rollover_syncs_elite_limit_and_all_gate_counts(self):
        self.fixture(level=30, elite_fight_count=30, strength=0)
        self.clear_map()
        role = self.b.profile()
        role['journey']['gates']['1:101']['day_count'] = 99
        role['journey']['gates']['2:101'] = dict(pass_star=3, day_count=3, flush_count=1)
        self.b.save(role)
        with patch('network_redirect.backend.time.time', return_value=NOW + 86400):
            self.req(1018, flag=2)
        attrs = {a['type']: a['value'] for mid, _, data in self.decoded if mid == 1032 for a in data['attr_list']}
        self.assertEqual((attrs[513], attrs[101]), (0, 30))
        rows = [g for mid, _, data in self.decoded if mid == 1020 for g in data['tollgate_list']]
        self.assertTrue(all(g['day_count'] == g['flush_count'] == 0 for g in rows))
        self.assertFalse(any(mid == 1019 for mid, _, data in self.decoded))

    def test_heartbeat_rollover_refreshes_gate_cache_once(self):
        self.fight()
        with patch('network_redirect.backend.time.time', return_value=NOW + 86400):
            packets = self.b.respond(encode(2999, {}), self.state)
            second = self.b.respond(encode(2999, {}), self.state)
        rows = [g for mid, _, data in map(decode, packets) if mid == 1020 for g in data['tollgate_list']]
        self.assertTrue(rows)
        self.assertTrue(all(g['day_count'] == 0 for g in rows))
        self.assertTrue(all(not data['first_send'] for mid, _, data in map(decode, packets) if mid == 1020))
        self.assertFalse(any(decode(p)[0] == 1020 for p in second))

    def test_first_operation_after_midnight_syncs_other_gate_counts(self):
        self.clear_map()
        role = self.b.profile()
        role['journey']['gates']['1:102']['day_count'] = 99
        self.b.save(role)
        with patch('network_redirect.backend.time.time', return_value=NOW + 86400):
            self.fight()
        rows = [g for mid, _, data in self.decoded if mid == 1020 for g in data['tollgate_list']]
        self.assertEqual(next(g['day_count'] for g in rows if g['tollgate_type'] == 1 and g['tollgate_id'] == 102), 0)
        self.assertEqual([d['tollgate_id'] for mid, _, d in self.decoded if mid == 1019], [101])

    def test_wire_encode_failure_rolls_back(self):
        before = self.b.profile()
        with patch('network_redirect.journey.encode', side_effect=ValueError('wire error')):
            self.fight()
        self.assertEqual(self.events[0][0], 55)
        self.assertEqual(self.b.profile(), before)


class DamageCodecTests(unittest.TestCase):
    def test_native_counted_primitive_array(self):
        values = dict(damage_count=3, damage_list=[-1, 0, 2147483647])
        packet = encode(105, values)
        self.assertEqual(decode(packet)[2]['damage_list'], values['damage_list'])
        self.assertEqual(packet[-12:], struct.pack('<iii', *values['damage_list']))
        for v in [dict(damage_count=2, damage_list=[1]), dict(damage_count=9, damage_list=[0]*9)]:
            with self.assertRaises(ValueError):
                encode(105, v)


if __name__ == '__main__':
    unittest.main()
