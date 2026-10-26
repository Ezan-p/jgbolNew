import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect import achievements as a, formation as f, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW = 1792900800


class AchievementTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.clock = patch('network_redirect.backend.time.time', return_value=NOW)
        self.clock.start(); self.addCleanup(self.clock.stop)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *x, **kw: None)
        self.addCleanup(self.b.close)
        self.serial = 100

    def row(self, role, ident): return next(r for r in a.rows(role) if r['id'] == ident)

    def request(self, mid, **data):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **data))
        self.replies = self.b.respond(self.packet, dict(authenticated=True))
        return [(m, d) for m, _, d in map(decode, self.replies)]

    def test_catalogue_and_wire_capacity(self):
        self.assertEqual((len(a.CATALOG), len(a.OPEN)), (276, 247))
        role = self.b.profile()
        out = list(map(decode, a.packets(role)))
        self.assertEqual(out[0][2]['attr_list'][0]['type'], 27)
        self.assertEqual(out[1][2]['achievement_count'], 247)
        self.assertEqual(len(out[1][2]['achievements']), 247)

    def test_native_menu_and_login_snapshot(self):
        out = [(m, d) for m, _, d in map(decode, self.b.bootstrap())]
        config = login_fields(out[0][1]['data'])
        self.assertTrue(config[7]['achievement'])
        self.assertEqual(next(d for m, d in out if m == 1066)['new'], 0)
        self.assertEqual(len(a.state(self.b.profile())['days']), 1)
        self.b.bootstrap(reconnect=True)
        self.assertEqual(len(a.state(self.b.profile())['days']), 1)

    def test_self_query_and_invalid_requests(self):
        for flag in (0, 1):
            out = self.request(1067, des_role_id=1, flag=flag)
            self.assertEqual(next(d for m, d in out if m == 1066)['role_id'], 1)
            self.assertEqual(out[-1][0], 1106)
        for target, flag in ((1, 2), (999, 0)):
            before = self.b.profile()
            out = self.request(1067, des_role_id=target, flag=flag)
            self.assertFalse(any(m == 1066 for m, d in out))
            self.assertEqual(self.b.profile(), before)

    def test_other_role_query_does_not_award_or_count_login(self):
        target = self.b.profile('friend'); target['role_id'] = 200
        a.add(target, 101); self.b.save(target, 'friend')
        before = self.b.profile()
        out = self.request(1067, des_role_id=200, flag=0)
        row = next(d for m, d in out if m == 1066)
        self.assertEqual(row['role_id'], 200)
        self.assertEqual(next(v for v in row['achievements'] if v['id'] == 101)['times'], 1)
        self.assertEqual(self.b.profile(), before)
        self.assertEqual(a.state(self.b.profile('friend'))['days'], [])

    def test_every_open_rule_completes_and_closed_rules_do_not(self):
        role = dict(role_id=1, attachments=[], corteges=[])
        for ident, cfg in a.CATALOG.items():
            a.add(role, ident, int(cfg['full_progress']))
        a.finalize(role)
        self.assertTrue(all(r['times'] == 1 for r in a.rows(role)))
        self.assertTrue(set(a.state(role)['totals']).isdisjoint(str(i) for i in set(a.CATALOG)-set(a.OPEN)))
        self.assertGreater(role['tao_point'], 0)

    def test_repeat_caps_and_unsigned_short(self):
        role = dict(role_id=1)
        a.add(role, 460, 2000); a.add(role, 459, 100000); a.add(role, 101, 900)
        a.finalize(role)
        self.assertEqual(self.row(role, 460)['times'], 1100)
        self.assertEqual(self.row(role, 459)['times'], 65535)
        self.assertEqual(self.row(role, 101)['times'], 1)
        for packet in a.packets(role): decode(packet)

    def test_vip_multiplier_and_first_category(self):
        role = dict(role_id=1)
        a.add(role, 101); a.add(role, 201); a.add(role, 202); a.finalize(role)
        self.assertEqual(role['tao_point'], 6)
        for ident, cfg in a.OPEN.items():
            if cfg['category'] == '1': a.add(role, ident)
        a.finalize(role)
        self.assertEqual(self.row(role, 401)['times'], 1)
        old = role['tao_point']; a.finalize(role); self.assertEqual(role['tao_point'], old)

    def test_daily_rollover_and_per_gate_count(self):
        role = self.b.profile()
        a.daily_add(role, 446, 60, NOW, '1:1'); a.daily_add(role, 446, 60, NOW, '1:2')
        self.assertEqual(self.row(role, 446)['progress'], 60)
        a.refresh(role, NOW+86400)
        self.assertEqual(self.row(role, 446)['progress'], 0)
        a.daily_add(role, 446, 99, NOW+86400, '1:1'); a.refresh(role, NOW+172800)
        self.assertEqual(self.row(role, 446)['times'], 1)

    def test_login_distinct_days(self):
        role = self.b.profile()
        for n in range(5): a.login(role, NOW+n*86400); a.login(role, NOW+n*86400+1)
        self.assertEqual(self.row(role, 402)['times'], 1)
        self.assertEqual(self.row(role, 403)['progress'], 5)

    def test_unique_object_milestones_survive_recycling(self):
        role = self.b.profile()
        item = dict(id=777, attach_type=6, type_id=22, level=10, count=0)
        role['attachments'].append(item); a.refresh(role, NOW)
        n = self.row(role, 416)['times']
        item['level'] = 1; a.refresh(role, NOW); item['level'] = 10; a.refresh(role, NOW)
        self.assertEqual(self.row(role, 416)['times'], n)
        role['attachments'].append(dict(item, id=778)); a.refresh(role, NOW)
        self.assertEqual(self.row(role, 416)['times'], n+1)

    def test_insight_real_request_atomic_replay_and_restart(self):
        role = self.b.profile(); role['level'] = 60
        ids = []
        for tid, lv in ((22, 10), (22, 1), (25, 1)):
            ident = f.new_id(role); ids.append(ident)
            role['attachments'].append(dict(id=ident, attach_type=6, type_id=tid, level=lv, count=0))
        self.b.save(role)
        req = dict(upgrade_type=6, des_id=ids[0], material_count=2, material_list=[dict(id=i) for i in ids[1:]])
        out = self.request(1076, **req)
        role = self.b.profile()
        self.assertEqual(self.row(role, 459)['times'], 1)
        update = next(d for m, d in out if m == 1066)
        self.assertEqual(update['new'], 1)
        self.assertIn(dict(id=459, times=1, progress=0), update['achievements'])
        self.assertEqual(self.b.respond(self.packet, dict(authenticated=True)), self.replies)
        self.assertEqual(self.b.profile(), role)
        self.request(1076, **req)
        self.assertEqual(self.b.profile(), role)
        other = Backend(Path(self.tmp.name), 18770, lambda *x, **k:None)
        try: self.assertEqual(self.row(other.profile(), 459)['times'], 1)
        finally: other.close()

    def test_simulation_receipts_and_all_rules(self):
        role = self.b.profile()
        for ident, cfg in a.OPEN.items():
            receipt = 'fixture:'+str(ident)
            self.assertTrue(a.simulate(role, ident, int(cfg['full_progress']), receipt, NOW))
            self.assertFalse(a.simulate(role, ident, int(cfg['full_progress']), receipt, NOW))
        self.assertTrue(all(r['times'] for r in a.rows(role)))
        with self.assertRaises(ValueError): a.simulate(role, 101, 2, 'fixture:101', NOW)
        with self.assertRaises(ValueError): a.simulate(role, 110, 1, 'closed', NOW)
        self.b.save(role)
        self.assertFalse(a.simulate(self.b.profile(), 101, 1, 'fixture:101', NOW))

    def test_failed_results_and_query_events_do_not_award(self):
        role = self.b.profile(); before = copy.deepcopy(role)
        a.record_events(role, [summon.event(43, dict(feed_result=4)), summon.event(40, dict(update_type=1))], NOW, login_fields)
        self.assertEqual(role, before)
        a.record_events(role, [summon.event(43, dict(feed_result=2))], NOW, login_fields)
        self.assertEqual(self.row(role, 108)['times'], 1)

    def test_simulator_preview_is_read_only(self):
        self.b.profile()
        path = Path(self.tmp.name)/'events.json'
        path.write_text(json.dumps([dict(id=134, amount=1, receipt='cross:one')]))
        before = (Path(self.tmp.name)/'game.sqlite3').read_bytes()
        import sys
        result = subprocess.run([sys.executable, 'simulate_achievements.py', '--directory', self.tmp.name,
            '--events', str(path)], text=True, capture_output=True, check=True)
        self.assertFalse(json.loads(result.stdout)['applied'])
        self.assertEqual((Path(self.tmp.name)/'game.sqlite3').read_bytes(), before)

    def test_rules_validation(self):
        self.assertEqual(a.load_rules()['mode'], 'inferred')
        p = Path(self.tmp.name)/'bad.json'; p.write_text('{"schema_version":1,"mode":"official"}')
        with self.assertRaises(ValueError): a.load_rules(p)

    def test_semantic_simulation_covers_missing_services(self):
        role = self.b.profile()
        for event in a.FACT_EVENTS:
            a.simulate_fact(role, event, 1, event, NOW)
            for ident in a.FACT_EVENTS[event]: self.assertEqual(self.row(role, ident)['times'], 1)
        for event in ('party_daily_rank', 'party_week_rank', 'cross_rank', 'feed_rank'):
            a.simulate_fact(role, event, 1, event, NOW)
        for target in range(1, 11):
            for event in ('follow', 'follower'): a.simulate_fact(role, event, target, f'{event}:{target}', NOW)
        a.simulate_fact(role, 'follow', 1, 'duplicate-target', NOW)
        self.assertEqual(len(a.state(role)['simulation_follow']), 10)
        for result in (323,324,325,326): a.simulate_fact(role, 'fortune', result, str(result), NOW)
        for stage in (4,6): a.simulate_fact(role, 'spirit_array', dict(stage=stage,level=5), 'array:'+str(stage), NOW)
        for ident in (218,219,220,221,236,237,238,302,303,304,305,323,324,325,326,445,461,462,463,464,465,560,561,562):
            self.assertEqual(self.row(role, ident)['times'], 1, ident)

    def test_simulated_rank_streak_requires_consecutive_days(self):
        role = self.b.profile()
        a.simulate_fact(role, 'duty_rank', 1, 'day1', NOW)
        a.simulate_fact(role, 'duty_rank', 1, 'day1-again', NOW)
        self.assertEqual(self.row(role, 431)['progress'], 1)
        a.simulate_fact(role, 'duty_rank', 2, 'day2', NOW+86400)
        self.assertEqual(self.row(role, 431)['times'], 1)
        a.simulate_fact(role, 'duty_rank', 0, 'day3', NOW+172800)
        self.assertEqual(self.row(role, 432)['progress'], 0)
        a.simulate_fact(role, 'duty_rank', 1, 'gap', NOW+4*86400)
        self.assertEqual(self.row(role, 432)['progress'], 1)
        for n in range(1,10): a.simulate_fact(role, 'duty_rank', 1, 'streak:'+str(n), NOW+(4+n)*86400)
        self.assertEqual(self.row(role, 439)['times'], 1)

    def test_rank_hold_resets_when_rank_is_lost(self):
        role = self.b.profile(); role.setdefault('activity', {})['rank_order'] = 1
        a.refresh(role, NOW); a.refresh(role, NOW+86399)
        self.assertEqual(self.row(role, 425)['times'], 0)
        role['activity']['rank_order'] = 2; a.refresh(role, NOW+86400)
        self.assertEqual(self.row(role, 424)['times'], 1)
        self.assertEqual(self.row(role, 425)['times'], 0)
        role['activity']['rank_order'] = 1; a.refresh(role, NOW+86401); a.refresh(role, NOW+172801)
        self.assertEqual(self.row(role, 425)['times'], 1)

    def test_evolution_counts_successful_operation_not_old_history(self):
        role = self.b.profile(); c = role['corteges'][0]; c['evolve_level'] = 10
        before = copy.deepcopy(role); c['evolve_level'] = 11
        a.track(role, before, 1084, dict(flag=0), NOW)
        self.assertEqual(self.row(role, 460)['times'], 1)
        c['evolve_level'] = 0; before = copy.deepcopy(role); c['evolve_level'] = 1
        a.track(role, before, 1084, dict(flag=0), NOW)
        self.assertEqual(self.row(role, 460)['times'], 2)

    def test_escort_uses_achievement_tao_instead_of_combat_power(self):
        from network_redirect.guild_escort import book
        role = self.b.profile(); role['tao_point'] = 65; role['role_combat_power'] = 100000
        self.assertEqual(book(role, dict(name='测试盟'), role['role_id'], NOW)['tao_point'], 65)
        self.assertEqual(book(role, dict(name='测试盟'), 999, NOW)['tao_point'], 1000)
