"""Behavioral checks for the explicitly inferred summon economy and wire contract."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode
from network_redirect import summon

ROOT = Path(__file__).resolve().parents[1]
NOW = 1792800000


class SummonTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.clock = patch('network_redirect.backend.time.time', return_value=NOW)
        self.clock.start()
        self.addCleanup(self.clock.stop)
        self.events = []
        self.backend = Backend(Path(self.directory.name), 18770,
                               lambda kind, **fields: self.events.append((kind, fields)))
        self.addCleanup(lambda: self.backend.close())
        self.backend.bootstrap()
        self.state = {'authenticated': True}
        self.serial = 100000

    def draw(self, grade=1, payment=1, count=1):
        self.serial += 1
        self.packet = encode(1042, dict(serial_num=self.serial, pick_grade=grade,
                                       pick_type=payment, ten_pick=count))
        return self.backend.respond(self.packet, self.state)

    def result(self, packets, event_id=23):
        for packet in packets:
            mid, _, data = decode(packet)
            if mid == event_id and mid in (1046, 1047):
                return {k:v for k,v in data.items() if k != 'serial_num'}
            if mid == 2998 and data['id'] == event_id:
                return login_fields(data['data'])
        self.fail('Missing event ' + str(event_id))

    def fund(self, gold=10000, tokens=20):
        role = self.backend.profile()
        role['gold_coin'] = gold
        role['attachments'] = [dict(id=20., attach_type=5, type_id=1006, count=min(3,tokens)),
                               dict(id=21., attach_type=5, type_id=1006, count=max(0,tokens-3)),
                               dict(id=22., attach_type=5, type_id=1007, count=tokens)]
        self.backend.save(role)

    def reject_unchanged(self, grade=1, payment=1, count=1):
        before = self.backend.profile()
        packets = self.draw(grade, payment, count)
        self.assertTrue(self.result(packets,55)['op_string'])
        self.assertEqual(decode(packets[-1])[0],1106)
        self.assertEqual(self.backend.profile(),before)

    def test_free_grades_cooldown_and_super_first_five(self):
        for grade in (1, 2, 3):
            result = self.result(self.draw(grade))
            self.assertNotIn('ten_pick', result)
            self.assertEqual(result['time'], self.backend.summon_rules['grades'][str(grade)]['free_cooldown_seconds'])
            if grade == 3:
                self.assertEqual(int(summon.BASES[result['cortege_type']]['quality']),5)
                self.assertEqual(result['first_pick_time'], NOW)
            self.reject_unchanged(grade)
        self.assertEqual(self.backend.profile()['normal_count'],1)

    def test_tokens_split_stacks_ten_rewards_and_ids_not_reused(self):
        self.fund(tokens=10)
        with patch('network_redirect.summon.choose_reward', return_value=(5004,None)):
            result = self.result(self.draw(2,2,10))
        self.assertIs(result['ten_pick'],True)
        self.assertEqual(len(result['event_data']),10)
        role = self.backend.profile()
        self.assertFalse(any(r['type_id']==1006 for r in role['attachments']))
        self.assertEqual(role['souls']['5004'],150)
        self.assertEqual(len(role['corteges']),1)
        self.assertEqual(sum(r['count'] for r in role['attachments'] if r['type_id']==5005),50)
        self.assertGreater(next(r['id'] for r in role['attachments'] if r['type_id']==5005),22)
        self.assertEqual(role['summon']['draw_count']['2'],10)

    def test_single_token_and_gold_leave_free_cooldown_unchanged(self):
        self.fund()
        deadline = self.backend.profile()['summon']['ready_at']
        self.assertNotIn('ten_pick',self.result(self.draw(2,2,0)))
        for grade, cost in ((1,10),(2,100),(3,300)):
            before = self.backend.profile()['gold_coin']
            self.result(self.draw(grade,3,0))
            self.assertEqual(self.backend.profile()['gold_coin'],before-cost)
        self.assertEqual(self.backend.profile()['summon']['ready_at'],deadline)

    def test_configured_gold_exact_balance_and_replay(self):
        for grade, price in ((1, 17), (2, 123), (3, 456)):
            self.backend.summon_rules['grades'][str(grade)]['gold_cost'] = price
            role = self.backend.profile()
            role['gold_coin'] = price
            self.backend.save(role)
            replies = self.draw(grade, 3, 0)
            self.result(replies)
            after = self.backend.profile()
            self.assertEqual(after['gold_coin'], 0)
            self.assertEqual(self.backend.respond(self.packet, self.state), replies)
            self.assertEqual(self.backend.profile(), after)
            self.reject_unchanged(grade, 3, 0)

    def test_insufficient_invalid_and_limits_do_not_mutate(self):
        self.reject_unchanged(2,2,10)
        self.reject_unchanged(3,3)
        for args in ((0,1,1),(4,1,1),(1,2,1),(1,3,10),(2,1,10),(1,1,10),(2,2,2),(2,0,1)):
            self.reject_unchanged(*args)
        self.fund()
        self.backend.summon_rules['grades']['2']['paid_daily_limit']=1
        self.result(self.draw(2,2))
        self.reject_unchanged(2,2)

    def test_gold_ten_exact_cost_rewards_pity_and_replay(self):
        self.fund(tokens=9)
        for grade, price, guaranteed in ((2, 123, 4), (3, 456, 5)):
            config = self.backend.summon_rules['grades'][str(grade)]
            config['gold_cost'] = price
            config['token_reward_basis_points'] = 0
            role = self.backend.profile()
            role['gold_coin'] = price
            role['summon']['draw_count'][str(grade)] = 1
            self.backend.save(role)
            with patch('network_redirect.summon.secrets.randbelow', return_value=0):
                replies = self.draw(grade, 3, 10)
            outcome = self.result(replies)
            self.assertIs(outcome['ten_pick'], True)
            self.assertEqual(len(outcome['event_data']), 10)
            self.assertEqual(int(summon.BASES[outcome['event_data'][10]['cortege_type']]['quality']), guaranteed)
            after = self.backend.profile()
            self.assertEqual(after['gold_coin'], 0)
            self.assertEqual(after['summon']['ready_at'], role['summon']['ready_at'])
            self.assertEqual(after['summon']['paid_count'][str(grade)], 10)
            self.assertEqual(after['summon']['draw_count'][str(grade)], 11)
            self.assertEqual(after['summon']['pity'][str(grade)], 0)
            self.assertFalse(any(i['type_id'] == config['token_id'] for i in after['attachments']))
            self.assertEqual(self.backend.respond(self.packet, self.state), replies)
            self.assertEqual(self.backend.profile(), after)
            self.reject_unchanged(grade, 3, 10)

    def test_gold_ten_insufficient_daily_limit_and_encoding_failure_are_atomic(self):
        self.fund(gold=999,tokens=0)
        self.reject_unchanged(2, 3, 10)
        self.fund(gold=1000)
        self.backend.summon_rules['grades']['2']['paid_daily_limit'] = 9
        self.reject_unchanged(2, 3, 10)
        self.backend.summon_rules['grades']['2']['paid_daily_limit'] = 10
        before = self.backend.profile()
        with patch('network_redirect.backend.encode', side_effect=ValueError('encoding failed')):
            with self.assertRaises(ValueError):
                self.draw(2, 3, 10)
        self.assertEqual(self.backend.profile(), before)

    def test_ten_mixed_payment_matrix_and_token_priority(self):
        for grade in (2, 3):
            price = self.backend.summon_rules['grades'][str(grade)]['gold_cost']
            token_id = 1004 + grade
            for payment in (2, 3):
                for tokens in (0, 1, 7, 9, 10, 13):
                    with self.subTest(grade=grade, payment=payment, tokens=tokens):
                        cost = max(0, 10-tokens) * price
                        self.fund(gold=cost, tokens=tokens)
                        before = self.backend.profile()
                        with patch('network_redirect.summon.choose_reward', return_value=(5004,None)):
                            replies = self.draw(grade,payment,10)
                        self.assertEqual(len(self.result(replies)['event_data']),10)
                        after = self.backend.profile()
                        self.assertEqual(after['gold_coin'],0)
                        self.assertEqual(sum(i['count'] for i in after['attachments'] if i['type_id']==token_id),max(0,tokens-10))
                        self.assertEqual(sum(i['count'] for i in after['attachments'] if i['type_id']==2013-token_id),tokens)
                        self.assertEqual(after['summon']['last_payment']['gold_spent'],cost)
                        self.assertEqual(after['summon']['ready_at'],before['summon']['ready_at'])

    def test_mixed_insufficient_and_reward_tokens_cannot_fund_current_draw(self):
        for payment in (2,3):
            self.fund(gold=299,tokens=7)
            self.reject_unchanged(2,payment,10)
        self.fund(gold=300,tokens=7)
        with patch('network_redirect.summon.choose_reward', return_value=(None,1006)):
            self.result(self.draw(2,3,10))
        role=self.backend.profile()
        self.assertEqual(role['gold_coin'],0)
        self.assertEqual(sum(i['count'] for i in role['attachments'] if i['type_id']==1006),10)

    def test_news_threshold_order_bound_replay_and_restart(self):
        self.fund(tokens=10)
        rewards=[(t,None) for t in (3027,5004,4015,5004,3027,4015,5004,3027,4015,5004)]
        with patch('network_redirect.summon.choose_reward',side_effect=rewards):
            replies=self.draw(3,2,10)
        news=self.result(replies,1047)
        self.assertTrue(news['first_send'])
        self.assertEqual(news['lottery_count'],6)
        self.assertEqual([n['type_id'] for n in news['lottery_list']],[t for t,_ in reversed(rewards[-6:])])
        self.assertTrue(all(n['time']==NOW and n['name']=='本地行者' for n in news['lottery_list']))
        after=self.backend.profile()
        self.assertEqual(self.backend.respond(self.packet,self.state),replies)
        self.assertEqual(self.backend.profile(),after)
        low=next(t for t,r in summon.BASES.items() if int(r['quality'])==3)
        for reward in ((low,None),(None,1006)):
            with patch('network_redirect.summon.choose_reward',return_value=reward):
                self.assertEqual(self.result(self.draw(1,3),1047),news)
        self.backend.close()
        self.backend=Backend(Path(self.directory.name),18770,lambda *a,**k:None)
        self.assertEqual(self.result(self.backend.bootstrap(),1047),news)

    def test_news_encoding_failure_rolls_back_payment_and_rewards(self):
        self.fund(gold=300,tokens=7)
        before=self.backend.profile()
        with patch('network_redirect.summon.choose_reward',return_value=(5004,None)), patch(
                'network_redirect.summon.news_snapshot',side_effect=ValueError('bad news')):
            with self.assertRaises(ValueError):
                self.draw(2,3,10)
        self.assertEqual(self.backend.profile(),before)

    def test_daily_limit_and_midnight_reset_preserve_cooldowns(self):
        role=self.backend.profile()
        role['normal_count']=5
        role['summon']['ready_at']['1']=NOW-1
        self.backend.save(role)
        self.reject_unchanged()
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.assertEqual(self.result(self.draw())['count'],1)

    def test_pity_across_payment_and_ten_draws(self):
        self.fund(tokens=30)
        role=self.backend.profile()
        role['summon']['draw_count']={'3':1}
        self.backend.save(role)
        # Zero random values choose the lowest allowed quality, making the ninth
        # miss / tenth guarantee boundaries deterministic without statistical tests.
        for grade, expected in ((2,4),(3,5)):
            self.backend.summon_rules['grades'][str(grade)]['token_reward_basis_points']=0
            with patch('network_redirect.summon.secrets.randbelow',return_value=0):
                result=self.result(self.draw(grade,2,10))
            entries=list(result['event_data'].values())
            self.assertTrue(all(int(summon.BASES[r['cortege_type']]['quality']) < expected for r in entries[:9]))
            self.assertEqual(int(summon.BASES[entries[9]['cortege_type']]['quality']),expected)
            self.assertEqual(self.backend.profile()['summon']['pity'][str(grade)],0)

    def test_first_super_ten_and_pity_reset_on_natural_high_quality(self):
        self.fund()
        with patch('network_redirect.summon.secrets.randbelow',return_value=0):
            result=self.result(self.draw(3,2,10))
        entries=list(result['event_data'].values())
        self.assertEqual(int(summon.BASES[entries[0]['cortege_type']]['quality']),5)
        self.assertEqual(self.backend.profile()['summon']['pity']['3'],9)
        with patch('network_redirect.summon.secrets.randbelow',return_value=0):
            result=self.result(self.draw(3,3))
        self.assertEqual(int(summon.BASES[result['cortege_type']]['quality']),5)
        self.assertEqual(self.backend.profile()['summon']['pity']['3'],0)

    def test_duplicate_souls_and_activity_are_separate_inventories(self):
        with patch('network_redirect.summon.choose_reward',return_value=(5004,None)):
            packets=self.draw(3)
        self.assertEqual(self.result(packets)['convert_count'],15)
        souls=self.result(packets,1046)
        self.assertTrue(souls['first_send'])
        self.assertEqual(souls['spirit_list'][0],dict(type_id=5004,count=15))
        role=self.backend.profile()
        self.assertEqual(role['corteges'][0]['order'],1)
        self.assertEqual(role['souls'],{'5004':15})
        self.assertIn(5005, [i['type_id'] for i in role['attachments'] if i['attach_type'] == 5])
        self.assertEqual(next(i['count'] for i in role['attachments'] if i['type_id']==5005 and i['attach_type']==5),5)
        self.assertEqual(self.result(self.backend.bootstrap(),1046),souls)

    def test_token_reward_and_activity_window_boundaries(self):
        self.backend.summon_rules['activity']['ends_at']=NOW
        with patch('network_redirect.summon.secrets.randbelow',return_value=0):
            result=self.result(self.draw(1))
        self.assertEqual(result['token_type'],1006)
        self.assertNotIn('cortege_type',result)
        self.assertNotIn('prize_info',result)
        self.assertEqual(len(self.backend.profile()['corteges']),1)
        self.assertIn(1006, [i['type_id'] for i in self.backend.profile()['attachments'] if i['attach_type'] == 5])

    def test_only_five_star_rewards_grant_five_matching_realm_souls(self):
        for grade in (1, 2, 3):
            qualities = (2, 3, 4) if grade == 1 else ((3, 4, 5) if grade == 2 else (4, 5))
            pool = summon.POOLS[self.backend.summon_rules['grades'][str(grade)]['pool']]
            for quality in qualities:
                for category in range(1, 6):
                    type_id = next((t for t in pool if int(summon.BASES[t]['quality']) == quality
                                    and int(summon.BASES[t]['category']) == category), None)
                    if type_id is None:
                        continue
                    for payment in (1, 2, 3) if grade > 1 else (1, 3):
                        with self.subTest(grade=grade, quality=quality, category=category, payment=payment):
                            self.fund()
                            role = self.backend.profile()
                            role['summon']['ready_at'][str(grade)] = NOW
                            role['normal_count'] = 0
                            self.backend.save(role)
                            with patch('network_redirect.summon.choose_reward', return_value=(type_id, None)):
                                result = self.result(self.draw(grade, payment))
                            items = [i for i in self.backend.profile()['attachments'] if 5001 <= i['type_id'] <= 5005]
                            if quality == 5:
                                self.assertEqual([(i['type_id'], i['count']) for i in items], [(5000 + category, 5)])
                                self.assertEqual(result['prize_info'][1], dict(object_type=5, attach_type=5000 + category, attach_count=5))
                            else:
                                self.assertEqual(items, [])
                                self.assertNotIn('prize_info', result)
        for grade, token in ((1, 1006), (2, 1007)):
            self.fund()
            with patch('network_redirect.summon.choose_reward', return_value=(None, token)):
                result = self.result(self.draw(grade, 3))
            self.assertNotIn('prize_info', result)
            self.assertFalse(any(5001 <= i['type_id'] <= 5005 for i in self.backend.profile()['attachments']))

    def test_mixed_ten_only_five_star_slots_grant_souls_and_replay_is_safe(self):
        self.fund(gold=300, tokens=7)
        rewards = [(3027, None), (5004, None), (None, 1007), (5004, None)] + [(3027, None)] * 6
        with patch('network_redirect.summon.choose_reward', side_effect=rewards):
            replies = self.draw(2, 3, 10)
        entries = self.result(replies)['event_data']
        self.assertEqual([i for i, result in entries.items() if 'prize_info' in result], [2, 4])
        after = self.backend.profile()
        self.assertEqual(sum(i['count'] for i in after['attachments'] if i['type_id'] == 5005), 10)
        self.assertEqual(after['gold_coin'], 0)
        self.assertEqual(self.backend.respond(self.packet, self.state), replies)
        self.assertEqual(self.backend.profile(), after)

    def test_five_star_soul_activity_switch_and_window(self):
        for enabled, start, end, expected in ((False, 0, 0, False), (True, NOW+1, 0, False),
                                            (True, 0, NOW, False), (True, NOW, NOW+1, True)):
            self.fund()
            self.backend.summon_rules['activity'] = dict(enabled=enabled, starts_at=start, ends_at=end)
            with patch('network_redirect.summon.choose_reward', return_value=(5004, None)):
                result = self.result(self.draw(2, 3))
            self.assertEqual('prize_info' in result, expected)

    def test_probability_boundaries_and_real_csv_quality(self):
        weights={2:65,3:30,4:5}
        for roll, expected in ((0,2),(64,2),(65,3),(94,3),(95,4),(99,4)):
            with patch('network_redirect.summon.secrets.randbelow',return_value=roll):
                self.assertEqual(summon.weighted_choice(weights),expected)
        self.assertEqual(int(summon.BASES[3027]['quality']),4)
        self.assertIn(3027,summon.POOLS['preview_2'])

    def test_replay_conflict_reconnect_do_not_settle_twice(self):
        first=self.draw(3)
        packet=self.packet
        role=self.backend.profile()
        self.assertEqual(self.backend.respond(packet,self.state),first)
        self.backend.respond(encode(1016,dict(account='local-player',random_key=self.backend.random_key)),{})
        self.assertEqual(self.backend.respond(packet,self.state),first)
        self.assertEqual(self.backend.profile(),role)
        conflict=encode(1042,dict(serial_num=self.serial,pick_grade=2,pick_type=1,ten_pick=1))
        self.result(self.backend.respond(conflict,self.state),55)
        self.assertEqual(self.backend.profile(),role)
        replay=self.backend.respond(encode(1105,dict(req_serial_num=200000)),self.state)
        self.assertEqual(replay[:len(first)],first)
        self.assertEqual(self.backend.profile(),role)

    def test_restart_persists_pity_souls_first_pick_and_remaining_time(self):
        with patch('network_redirect.summon.choose_reward',return_value=(5004,None)):
            self.draw(3)
        before=self.backend.profile()
        self.backend.close()
        self.backend=Backend(Path(self.directory.name),18770,lambda *a,**k:None)
        with patch('network_redirect.backend.time.time',return_value=NOW+123):
            snapshot=self.backend.snapshot()
        self.assertEqual(snapshot['super_time'],259200-123)
        self.assertEqual(snapshot['super_first_pick_time'],NOW)
        self.assertEqual(snapshot['souls'],before['souls'])
        self.assertEqual(snapshot['summon']['draw_count'],before['summon']['draw_count'])

    def test_legacy_migration_preserves_progress_and_infers_only_known_first(self):
        role=self.backend.profile()
        role['summon']=dict(day='2020-01-01',ready_at={'1':NOW-1,'2':NOW+100,'3':NOW+500},
                            last_result=dict(pick_grade=3,cortege_type=4035))
        role['normal_count']=5
        self.backend.save(role)
        snapshot=self.backend.snapshot()
        self.assertEqual(snapshot['normal_count'],0)
        self.assertEqual(snapshot['super_time'],500)
        self.assertEqual(snapshot['summon']['draw_count'],{'3':1})
        self.assertGreater(snapshot['super_first_pick_time'],0)
        self.assertEqual(snapshot['corteges'],role['corteges'])

    def test_encoding_failure_does_not_commit_and_large_roster_is_chunked(self):
        before=self.backend.profile()
        with patch('network_redirect.backend.encode',side_effect=ValueError('encoding failed')):
            with self.assertRaises(ValueError):
                self.draw(3)
        self.assertEqual(self.backend.profile(),before)
        role=self.backend.profile()
        role['corteges']=[dict(role['corteges'][0],id=float(i+100),order=1 if i==0 else 0) for i in range(255)]
        self.backend.save(role)
        with patch('network_redirect.summon.choose_reward',return_value=(4015,None)):
            packets=self.draw(3)
        self.assertEqual(len(self.backend.profile()['corteges']),256)
        chunks=[decode(p)[2] for p in packets if decode(p)[0]==1034]
        self.assertEqual([c['cortege_count'] for c in chunks],[128,128])

    def test_unauthenticated_and_zero_serial_do_not_mutate(self):
        before=self.backend.profile()
        packet=encode(1042,dict(serial_num=0,pick_grade=3,pick_type=1,ten_pick=1))
        with self.assertRaises(ValueError):
            self.backend.respond(packet,{})
        self.result(self.backend.respond(packet,self.state),55)
        self.assertEqual(self.backend.profile(),before)

    def test_rules_fail_closed_and_status_identifies_inference(self):
        base=summon.load_rules()
        path=Path(self.directory.name)/'bad.json'
        variants=[dict(base,news={'min_quality':6,'limit':6}),dict(base,news={'min_quality':4,'limit':7}),dict(base,mode='official'),dict(base,normal_free_daily_limit=6)]
        bad=copy.deepcopy(base)
        bad['grades']['3']['quality_weights']={'2':100}
        variants.append(bad)
        bad=copy.deepcopy(base)
        bad['grades']['2']['token_reward_basis_points']=10001
        variants.append(bad)
        for grade, count in (('1', 1), ('2', 2), ('3', 10)):
            bad = copy.deepcopy(base)
            bad['grades'][grade]['activity_soul_count'] = count
            variants.append(bad)
        for config in variants:
            path.write_text(json.dumps(config))
            with self.assertRaises(ValueError):
                summon.load_rules(path)
        result=subprocess.run([sys.executable,'game_server.py','--summon-status'],cwd=ROOT,
                              capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        status=json.loads(result.stdout)
        self.assertEqual(status['mode'],'inferred')
        self.assertIs(status['ready'],True)
        self.assertIs(status['official_verified'],False)


if __name__ == '__main__':
    unittest.main()
