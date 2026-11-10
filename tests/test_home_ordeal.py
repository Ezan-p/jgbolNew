"""Home scale challenges: native protocol, fixed enemies and durable settlement."""
import copy
from pathlib import Path
from unittest.mock import patch

from test_activity import ActivityCase, NOW
from network_redirect import activity_home as h, activity_home_ordeal as ordeal
from network_redirect import combat, combat_power, formation, journey, summon
from network_redirect.backend import Backend, login_fields


class HomeOrdealTests(ActivityCase):
    def home(self, op, **data):
        self.ok(self.req(1348, id=op, data=summon.lua(data)))
        return next(login_fields(d['data']) for mid, _, d in self.decoded if mid == 1348 and d['id'] == op)

    def rejected(self, op, **data):
        before = self.b.profile()
        self.assertEqual(self.req(1348, id=op, data=summon.lua(data))[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def prepare(self, level=1, passed=False):
        self.home(1)
        role = self.b.profile()
        s = role['activity']['home']
        s.update(level=level, passed=passed)
        s['build'].update({str(i): 11 for i in (1, 2, 3)})
        for tid in (1362, 1363):
            summon.add_item(role, tid, 2000)
        self.b.save(role)
        return role

    def test_preview_is_actual_team_and_independent_of_generic_npc(self):
        role = self.prepare()
        powers = []
        for lv, count, train in ((1, 3, 5), (2, 5, 10)):
            s = copy.deepcopy(role['activity']['home']);s['level'] = lv
            p = h.upgrade_info(s, dict(battle_npc=999999, battle_level=999))['boss_info']
            cfg, units = ordeal.enemies(lv)
            self.assertEqual(p['cortege_type'], units[0]['type'])
            self.assertEqual((p['cortege_count'], p['train_level']), (count, train))
            self.assertEqual(p['combat_power'], sum(combat_power.score_panel(u, formation.load_rules()['combat_weights']) for u in units))
            self.assertTrue(all(len(u['training_bonuses']) == 4 and u['max_hp'] == u['hp'] for u in units))
            powers.append(p['combat_power'])
            units[0]['hp'] = 1
            self.assertGreater(ordeal.enemies(lv)[1][0]['hp'], 1)
        self.assertGreater(powers[1], powers[0])

    def test_native_first_scale_building_gate_and_second_scale_exemption(self):
        self.prepare()
        for building in ('1', '2', '3'):
            role = self.b.profile();role['activity']['home']['build'][building] = 10;self.b.save(role)
            self.rejected(25);self.rejected(26)
            role['activity']['home']['build'][building] = 11;self.b.save(role)
        with patch.object(h.journey, 'battle', return_value=(4, [], [])) as battle:
            self.assertFalse(self.home(25)['has_passed'])
            self.assertEqual(len(battle.call_args.kwargs['units'][1]), 3)
        self.prepare(2)
        with patch.object(h.journey, 'battle', return_value=(4, [], [])):
            self.home(25)

    def test_losses_exhaust_daily_pool_and_retry_after_midnight(self):
        self.prepare()
        with patch.object(h.journey, 'battle', return_value=(4, [], [])):
            for left in (2, 1, 0):
                result = self.home(25, has_passed=True, final_result=3)
                self.assertEqual(result, dict(result=1, has_passed=False, fight_count=left))
            self.rejected(25)
            self.rejected(26, has_passed=True)
            with patch('network_redirect.game_clock.now', return_value=NOW + 86400):
                self.assertEqual(self.home(25)['fight_count'], 2)
        self.rejected(25)  # Backdated request cannot refill the pool.

    def test_win_replay_restart_and_daily_reset_preserve_pass(self):
        self.prepare()
        with patch.object(h.journey, 'battle', return_value=(2, [], [])):
            result = self.home(25)
        self.assertTrue(result['has_passed'])
        saved = self.b.profile()
        self.b.respond(self.packet, self.state)
        self.assertEqual(saved, self.b.profile())
        self.rejected(25)
        self.b.close();self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        with patch('network_redirect.game_clock.now', return_value=NOW + 86400):
            stage = self.home(1)['base_data']['upgrade_info']
            self.assertTrue(stage['has_passed']);self.assertEqual(stage['fight_count'], 3)
            self.rejected(25)
            self.assertEqual(self.home(26)['level'], 2)

    def test_two_upgrade_costs_stage_refresh_and_max_scale(self):
        self.prepare()
        with patch.object(h.journey, 'battle', return_value=(3, [], [])):
            self.home(25)
        before = self.b.profile()
        first = self.home(26)
        role = self.b.profile()
        self.assertEqual(role['gold_coin'], before['gold_coin'] - 1000)
        count = lambda r, tid: sum(i['count'] for i in r['attachments'] if i['type_id'] == tid)
        self.assertEqual(count(role, 1362), count(before, 1362) - 1000)
        self.assertFalse(first['upgrade_info']['has_passed'])
        self.assertEqual(first['upgrade_info']['fight_count'], 2)
        self.assertEqual(first['upgrade_info']['boss_info']['cortege_count'], 5)
        self.rejected(26)
        with patch.object(h.journey, 'battle', return_value=(1, [], [])):
            self.home(25)
        last = self.home(26)
        self.assertEqual(count(self.b.profile(), 1363), count(role, 1363) - 100)
        self.assertEqual(last['level'], 3)
        self.assertTrue(last['upgrade_info']['is_max_scale'])
        self.assertEqual(last['upgrade_info']['fight_count'], 1)
        self.assertEqual(last['upgrade_info']['boss_info']['cortege_count'], 0)
        self.assertEqual(self.b.profile()['hole_hp_plus'], last['point'])
        self.rejected(25);self.rejected(26)

    def test_material_failure_keeps_pass_and_partial_costs_rollback(self):
        role = self.prepare(passed=True)
        role['attachments'] = [i for i in role['attachments'] if i['type_id'] != 1362]
        self.b.save(role);self.rejected(26)
        role = self.prepare(2, passed=True)
        role['attachments'] = [i for i in role['attachments'] if i['type_id'] != 1363]
        self.b.save(role);self.rejected(26)

    def test_no_active_slots_or_low_role_level_never_consumes_attempt(self):
        role = self.prepare()
        for c in role['corteges']:c['order'] = 9
        self.b.save(role);self.rejected(25)
        role['level'] = 49;self.b.save(role);self.rejected(25)

    def test_encoding_failure_rolls_back_battle_and_upgrade(self):
        self.prepare()
        original = h.encode
        def fail(mid, data):
            if mid == 1348 and data['id'] in (25, 26):
                raise formation.Rejected('test encoding failure')
            return original(mid, data)
        with patch.object(h.journey, 'battle', return_value=(3, [], [])), patch.object(h, 'encode', side_effect=fail):
            self.rejected(25)
        self.prepare(passed=True)
        with patch.object(h, 'encode', side_effect=fail):self.rejected(26)

    def test_real_engine_training_and_both_outcomes(self):
        for lv in (1, 2):
            cfg, enemies = ordeal.enemies(lv)
            strong = dict(type=5004, order=1, level=100, evolve=0, reborn=0,
                          hp=10000000, max_hp=10000000, gongji=10000000, fangyu=10000000,
                          magic=10000000, skills=[])
            for expected, ours in ((3, strong), (4, dict(strong, hp=1, max_hp=1, gongji=1, fangyu=1, magic=1))):
                result, lineup, actions = journey.battle({'corteges': []}, cfg, self.b.journey_rules,
                                                       units=([ours], copy.deepcopy(enemies)))
                self.assertEqual(result, expected)
                self.assertTrue(lineup and actions)
            attacker = enemies[0]
            target = dict(strong, hp=100000, max_hp=100000, fangyu=1)
            trained = combat.damage(attacker, target, 1, 1, self.b.journey_rules['battle'], settle=False)
            plain = combat.damage(dict(attacker, training_bonuses=[(0, 0)] * 4), target, 1, 1,
                                  self.b.journey_rules['battle'], settle=False)
            self.assertGreater(trained, plain)

    def test_draw_does_not_grant_upgrade(self):
        self.prepare()
        with patch.object(h.journey, 'battle', return_value=(0, [], [])):
            result = self.home(25)
        self.assertFalse(result['has_passed'])
        self.assertEqual(result['fight_count'], 2)
        self.rejected(26)

    def test_real_protocol_two_wins_and_expansions(self):
        from network_redirect import npc_players
        self.prepare()
        entry = max((e for e in npc_players.catalog().values() if e['profile']['level'] == 99),
                    key=lambda e: e['profile']['role_combat_power'])
        npc = npc_players.get(entry['npc_id'])['role']
        role = self.b.profile()
        for key in ('corteges', 'attachments', 'level'):
            role[key] = copy.deepcopy(npc[key])
        for tid, count in ((1362, 1000), (1363, 100)):
            summon.add_item(role, tid, count)
        self.b.save(role)
        for level, count in ((2, 2), (3, 1)):
            self.assertTrue(self.home(25)['has_passed'])
            expanded = self.home(26)
            self.assertEqual((expanded['level'], expanded['upgrade_info']['fight_count']), (level, count))
        saved = self.b.profile()
        self.b.respond(self.packet, self.state)
        self.assertEqual(saved, self.b.profile())
        self.b.close();self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(saved, self.b.profile())

    def test_real_protocol_battle_has_replay_and_return_event(self):
        self.prepare()
        result = self.home(25)
        lineup = next(d for mid, _, d in self.decoded if mid == 1028)
        replay = next(d for mid, _, d in self.decoded if mid == 1027)
        returned = next(login_fields(d['data']) for mid, _, d in self.decoded if mid == 2998 and d['id'] == 44)
        self.assertEqual(replay['fight_type'], 34)
        self.assertEqual(returned, dict(fight_id=lineup['fight_id'], fight_type=34))
        self.assertEqual(result['has_passed'], 1 <= replay['final_result'] <= 3)
        self.assertGreater(replay['fight_round'], 0)
        self.assertEqual(result['fight_count'], 2)
