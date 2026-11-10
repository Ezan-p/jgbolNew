"""Top-power blood-arena allocation, saved seasons and production battles."""
import copy
import hashlib
import random
import unittest
from pathlib import Path
from unittest.mock import patch

from test_activity_taixu import TaixuCase
from test_activity import NOW
from network_redirect import activity, activity_arena as arena, journey, npc_players
from network_redirect.backend import Backend
from network_redirect.protocol import decode


class ArenaRosterTests(unittest.TestCase):
    def test_all_groups_have_fixed_seats_and_valid_levels(self):
        catalog = npc_players.catalog()
        for week in range(52):
            for group, (lo, hi) in enumerate(arena.rules()['arena_groups'], arena.FIRST_GROUP):
                keys = arena.select_roster(group, 20766 + week*7)
                self.assertEqual(len(keys), 19)
                self.assertEqual(len(set(keys)), 19)
                profiles = [catalog[k]['profile'] for k in keys]
                self.assertTrue(all(lo <= p['level'] <= hi for p in profiles))
                powers = [p['role_combat_power'] for p in profiles]
                self.assertEqual(powers, sorted(powers))
                expected = sorted(
                    (k for k, e in catalog.items() if lo <= e['profile']['level'] <= hi),
                    key=lambda k: (catalog[k]['profile']['role_combat_power'], k), reverse=True)[:15]
                self.assertEqual(list(reversed(keys))[:15], expected)

    def test_remaining_seats_sample_ordinary_pool_without_reserved_npcs(self):
        day = arena.week_start(20766)
        for group, (lo, hi) in enumerate(arena.rules()['arena_groups'], arena.FIRST_GROUP):
            eligible = sorted((e for e in npc_players.catalog().values() if lo <= e['profile']['level'] <= hi),
                              key=lambda e: (e['profile']['role_combat_power'], e['npc_id']))
            reserved = {e['npc_id'] for e in eligible[-15:]}
            pool = [e for e in eligible if e['profile']['tier'].startswith('T') and e['npc_id'] not in reserved]
            expected = [min(pool[i*len(pool)//4:(i+1)*len(pool)//4],
                            key=lambda e: hashlib.sha256(f"{day}:{group}:{e['npc_id']}".encode()).digest())['npc_id']
                        for i in range(4)]
            self.assertEqual(arena.select_roster(group, day)[:4], expected)

    def test_week_stability_and_rotation(self):
        monday = arena.week_start(20766)
        for group in range(4, 8):
            first = arena.select_roster(group, monday)
            for offset in range(7):
                self.assertEqual(arena.select_roster(group, monday+offset), first)
            following = arena.select_roster(group, monday+7)
            self.assertEqual(following[-15:], first[-15:])
            self.assertNotEqual(following[:4], first[:4])
            npc_players.clear_cache()
            self.assertEqual(arena.select_roster(group, monday), first)

    def test_initial_rankings_and_browsed_boards_use_strongest_fifteen(self):
        catalog = npc_players.catalog()
        for group, (lo, hi) in enumerate(arena.rules()['arena_groups'], arena.FIRST_GROUP):
            role = dict(level=lo, role_id=1, role_name='测试', corteges=[])
            s = arena.new_season(role, 20766, NOW)
            expected = sorted((k for k, e in catalog.items() if lo <= e['profile']['level'] <= hi),
                              key=lambda k: (catalog[k]['profile']['role_combat_power'], k), reverse=True)[:15]
            self.assertEqual(arena.ranking(s)[:15], expected)
            self.assertEqual(arena.ranking(s)[-1], 'self')
            s['group'] = 7 if group != 7 else 4
            rows = arena.board(role, s)['rank_data']
            self.assertEqual([r['obj_id'] for r in rows[:15]], [catalog[k]['profile']['role_id'] for k in expected])


class ArenaExtremeIntegrationTests(TaixuCase):
    def top_group(self):
        role = self.b.profile(); role['level'] = 99; self.b.save(role)
        return self.arena_enter()

    def test_existing_season_survives_upgrade_until_next_week(self):
        self.top_group()
        role = self.b.profile(); s = role['activity']['arena']
        # Simulate a pre-update ordinary roster with real progress and records.
        pool = [k for k, e in npc_players.catalog().items()
                if e['profile']['level'] >= 80 and e['profile']['tier'].startswith('T')][:19]
        s['competitors'] = {k: dict(hp=100, score=100) for k in pool}
        s['competitors']['self'] = dict(hp=115, score=101)
        s.update(stage=4, stage_fights=1, fights=5, paid=2, actions=6)
        self.b.save(role)
        with patch('network_redirect.activity_arena.journey.battle', return_value=(4, [], [])):
            self.ok(self.arena_fight())
        old = copy.deepcopy(self.b.profile()['activity']['arena'])
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.ok(self.call(1, mid=1350))
        self.assertEqual(self.b.profile()['activity']['arena'], old)
        with patch('network_redirect.game_clock.now', return_value=NOW+7*86400):
            self.ok(self.call(1, mid=1350))
        fresh = self.b.profile()['activity']['arena']
        self.assertEqual(fresh['stage'], 1)
        self.assertEqual(fresh['records'], [])
        self.assertEqual(sum(k.startswith('npc_extreme') for k in fresh['competitors']), 15)
        self.assertEqual(arena.ranking(fresh)[:15], list(reversed(arena.select_roster(7, fresh['day'])))[:15])

    def test_extreme_inspection_battle_retry_restart_and_replay(self):
        s = self.top_group()
        keys = [k for k in s['competitors'] if k.startswith('npc_extreme')]
        for key in keys:
            with self.subTest(key=key):
                npc = npc_players.get(key); ident = npc['role']['role_id']
                source = copy.deepcopy(npc_players.source_file(npc_players.catalog()[key]['source_file'])[key])
                events = self.call(4, dict(des_id=ident), mid=1350); self.ok(events)
                inspected = next(d for e, d in events if e == 11)
                self.assertEqual(inspected['role_id'], ident)
                self.assertEqual(inspected['role_combat_power'], npc['role']['role_combat_power'])
                self.assertEqual(len(inspected['cortege_list']), 8)
                # Each opponent gets an independent fresh season (ten free qualifiers).
                role = self.b.profile()
                role['activity']['arena'] = arena.new_season(role, activity.day(NOW, self.b.activity_rules), NOW)
                self.b.save(role)
                before = self.b.profile()
                order = arena.ranking(before['activity']['arena']).index(key)+1
                with patch('network_redirect.combat.secrets.randbelow', side_effect=random.Random(83).randrange):
                    self.ok(self.arena_fight(des_id=ident, des_order=order))
                after = self.b.profile(); packets = self.replies
                self.assertEqual(after['activity']['arena']['fights'], before['activity']['arena']['fights']+1)
                record = after['activity']['arena']['records'][-1]
                self.assertEqual(record['des_id'], ident)
                self.assertTrue(any(decode(p)[0] == 1027 for p in packets))
                self.assertEqual(self.b.respond(self.packet, self.state), packets)
                self.assertEqual(self.b.profile(), after)
                self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
                self.assertEqual(self.b.profile(), after)
                self.ok(self.req(1244, fight_type=4, log_time=record['log_time'],
                                 src_id=record['src_id'], match_type=record['match_type']))
                self.assertEqual(self.b.profile(), after)
                self.assertTrue(all(len(p) <= 32768 for p in packets+self.replies))
                self.assertEqual(npc_players.source_file(npc_players.catalog()[key]['source_file'])[key], source)

    def test_top_fifteen_full_loadout_battles(self):
        for key in arena.select_roster(7, activity.day(NOW, self.b.activity_rules)):
            if not key.startswith('npc_extreme'):
                continue
            with self.subTest(key=key):
                npc = npc_players.get(key)
                role = copy.deepcopy(npc['role'])
                role.update(role_id=1, role_name='血战测试')
                role['activity'] = dict(fight_id=0)
                s = arena.new_season(role, activity.day(NOW, self.b.activity_rules), NOW)
                role['activity']['arena'] = s
                with patch('network_redirect.combat.secrets.randbelow', side_effect=random.Random(83).randrange):
                    packets = arena.fight(role, s, dict(fight_type=1, des_type=1,
                        des_id=npc['role']['role_id'], des_order=arena.ranking(s).index(key)+1), NOW, journey.load_rules())
                self.assertEqual(s['fights'], 1)
                # Equal remaining HP is a legitimate draw for a mirror match.
                self.assertIn(s['records'][-1]['final_result'], range(7))
                if s['records'][-1]['final_result'] == 0:
                    self.assertEqual(s['competitors']['self']['score'], 0)
                self.assertTrue(all(len(p) <= 32768 for p in packets))

    def test_lower_group_can_inspect_extreme_but_cannot_challenge(self):
        self.arena_enter()
        events = self.call(2, dict(enter_group=7), mid=1350); self.ok(events)
        board = next(d for e, d in events if e == 199)
        row = board['rank_data'][1]  # Native Lua arrays use one-based keys.
        self.ok(self.call(4, dict(des_id=row['obj_id']), mid=1350))
        before = self.b.profile()
        self.assertEqual(self.arena_fight(des_id=row['obj_id'], des_order=row['order'])[0][0], 55)
        self.assertEqual(self.b.profile(), before)


if __name__ == '__main__':
    unittest.main()
