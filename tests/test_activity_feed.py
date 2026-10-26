"""Native feed packets: score tiers, query purity and persisted daily claims."""
import copy
import json
from pathlib import Path
from unittest.mock import patch

from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_feed as feed, formation, summon
from network_redirect.backend import Backend


class FeedTests(ActivityCase):
    def data(self, count=0):
        events = self.req(1040, feed_count=count)
        self.ok(events)
        return next(d for e, d in events if e == 43)

    def test_query_never_awards_or_consumes_attempt(self):
        self.data()  # Initialize shared welfare/daily state, not a feed claim.
        before = self.b.profile()
        for _ in range(3):
            d = self.data()
            self.assertEqual(d['feed_result'], 1)
            self.assertEqual(d['strength'], 0)
            self.assertEqual(d['feed_data']['feed_list'], {1: 1, 2: 1})
        self.assertEqual(self.b.profile(), before)

    def test_each_tier_boundary_through_wire(self):
        for count, amount in ((1,10),(9,10),(10,20),(19,20),(20,30),(29,30),
                              (30,40),(39,40),(40,50),(49,50),(50,60),(200,60)):
            with self.subTest(count=count):
                r = self.b.profile();r['activity']['feed'] = {};r['strength'] = 999
                self.b.save(r)
                d = self.data(count)
                self.assertEqual(d['feed_result'], 2)
                self.assertEqual(d['strength'], amount)
                self.assertEqual(self.b.profile()['strength'], 999 + amount)
                self.assertEqual(self.b.profile()['achievements']['totals']['108'], 1)

    def test_duplicate_and_restart_query_preserve_earned_reward(self):
        self.data(50)
        before = self.b.profile()
        self.assertEqual(self.data(200)['feed_result'], 4)
        self.assertEqual(self.b.profile(), before)
        self.b.close();self.b = Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        d = self.data()
        self.assertEqual(d['strength'], 60)
        self.assertEqual(d['feed_data']['feed_count'], 50)
        self.assertEqual(d['feed_data']['feed_list'][1], NOW)
        self.assertEqual(self.b.profile(), before)

    def test_second_run_and_new_day(self):
        self.data(60)
        with patch('network_redirect.backend.time.time', return_value=NOW+6*3600):
            before = self.b.profile()['strength']
            d = self.data(10)
            self.assertEqual(d['strength'], 20)
            self.assertEqual(d['personal_best_strength'], 60)
            self.assertEqual(d['feed_data']['feed_count'], 60)
            self.assertEqual(self.b.profile()['strength'], before + 20)
            self.assertEqual(self.data()['strength'], 60)
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            d = self.data()
            self.assertEqual(d['feed_data']['feed_count'], 0)
            self.assertEqual(d['feed_champion']['count'], 0)
            self.assertEqual(d['strength'], 0)
            self.assertEqual(self.data(10)['feed_result'], 2)

    def test_closed_boundaries_do_not_consume_or_award(self):
        self.data()
        for offset in (-1,2*3600,6*3600-1,8*3600):
            with patch('network_redirect.backend.time.time', return_value=NOW+offset):
                before = self.b.profile()
                self.assertEqual(self.data(30)['feed_result'], 3)
                after = self.b.profile()
                self.assertEqual(after['strength'], before['strength'])
                self.assertEqual(after['activity']['feed'], before['activity']['feed'])
                for key in ('feed_time1', 'feed_time2'):
                    self.assertEqual(after.get(key), before.get(key))

    def test_champion_uses_actual_same_day_peers(self):
        role = self.b.profile()
        peer = copy.deepcopy(role);peer.update(role_id=42,role_name='同服玩家',feed_time1=NOW)
        peer['activity']['feed'] = {'1': {'count': 80, 'strength': 60}}
        with patch.object(self.b, 'duty_peers', return_value=[peer]):
            self.assertEqual(self.data(30)['feed_champion'], dict(name='同服玩家',count=80))
            self.assertEqual(self.b.profile()['achievements']['totals'].get('445', 0), 0)
        peer['activity']['day'] -= 1
        with patch.object(self.b, 'duty_peers', return_value=[peer]):
            self.assertEqual(self.data()['feed_champion'], dict(name=role['role_name'],count=30))

    def test_champion_tie_and_success_achievement(self):
        role = self.b.profile()
        peer = copy.deepcopy(role);peer.update(role_id=42,role_name='先完成玩家',feed_time1=NOW-1)
        peer['activity']['feed'] = {'1': {'count': 30, 'strength': 40}}
        with patch.object(self.b, 'duty_peers', return_value=[peer]):
            self.assertEqual(self.data(30)['feed_champion']['name'], '先完成玩家')
            self.assertEqual(self.b.profile()['achievements']['totals'].get('445', 0), 0)
            with patch('network_redirect.backend.time.time', return_value=NOW+21600):
                self.assertEqual(self.data(40)['feed_champion']['name'],role['role_name'])
                self.assertEqual(self.b.profile()['achievements']['totals']['445'], 1)

    def test_bad_tiers_and_invalid_score(self):
        for tiers in ([], [{'min_count': 2, 'strength': 10}],
                      [{'min_count': True, 'strength': 10}],
                      [{'min_count': 1, 'strength': 10}, {'min_count': 1, 'strength': 20}],
                      [{'min_count': 1, 'strength': 10}, {'min_count': 20, 'strength': 9}]):
            rules = copy.deepcopy(self.b.activity_rules);rules['feed_reward_tiers'] = tiers
            path = Path(self.tmp.name)/'rules.json';path.write_text(json.dumps(rules))
            with self.assertRaises(formation.Rejected): activity.load_rules(path)
        before = self.b.profile()
        self.assertEqual(self.req(1040, feed_count=201)[0][0],55)
        self.assertEqual(self.b.profile(), before)

    def test_client_tiers_match_server(self):
        source = summon.client_source(self.b.summon_rules)
        self.assertNotIn('__FEED_REWARD_TIERS__', source)
        self.assertNotIn('__FEED_MAX_COUNT__', source)
        self.assertIn('local tiers='+summon.lua(self.b.activity_rules['feed_reward_tiers']), source)
