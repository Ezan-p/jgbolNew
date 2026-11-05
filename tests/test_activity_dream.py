"""Real wire requests, 1263 reward amounts/levels, persistence and replay boundaries."""
import csv
import tempfile
from pathlib import Path
from unittest.mock import patch

from test_activity import ActivityCase, NOW
from network_redirect import activity_dream as d, summon, formation
from network_redirect.backend import Backend, login_fields


class DreamTests(ActivityCase):
    def call(self, op=1, **data):
        if op != 1:
            data.setdefault('local_token', self.saved()['token'])
        events = self.req(1325, id=op, data=summon.lua(data))
        self.ok(events)
        return next(v for e, v in events if e == 169)

    def saved(self):
        return self.b.profile()['activity']['dream']

    def count(self, tid, level=1):
        return sum(i['count'] for i in self.b.profile()['attachments']
                   if i['attach_type'] == 5 and i['type_id'] == tid and i['level'] == level)

    def solve(self):
        return self.call(2, answer=list(range(1, 10)))

    def bless(self, two=False):
        s = self.saved()
        ids = [p['id'] for p in d.friends(self.b.profile(), s, d.load_rules())]
        return self.call(3, des_list=ids[:2 if two else 1], index=1)

    def reject(self, op, data):
        before = self.b.profile()
        events = self.req(1325, id=op, data=summon.lua(data))
        self.assertEqual(events[0][0], 55, events)
        self.assertEqual(self.b.profile(), before)

    def test_original_table_and_status_contract(self):
        original = Path(__file__).resolve().parents[1] / 'analysis/evidence/original_activities_20261102/csv/dream_prize_config.csv'
        with original.open(encoding='utf-8-sig', newline='') as f:
            self.assertEqual(summon.rows('dream_prize_config.csv'), list(csv.DictReader(f)))
        status = next(v for e, v in self.req(1205, flag=0) if e == 47)['dream_data']
        self.assertEqual(status['min_level'], 18)
        self.assertTrue(status['can_join'])
        self.assertLess(status['begin_time'], NOW)
        self.assertGreater(status['end_time'], NOW)
        data = self.call()
        self.assertEqual(data['dream_data']['cur_dream'], 1)
        self.assertEqual(data['plus_data']['min_charge'], 30)
        self.assertEqual(len(data['local_rewards']), 6)
        self.assertEqual(len(data['local_friends']), 6)
        self.assertEqual(data['local_rewards'][2]['dream_prizes'][1]['attach_level'], 6)

    def test_full_six_stages_exact_rewards_and_friend_balances(self):
        self.call()
        baseline = {(p[1], p[3]): self.count(p[1], p[3])
                    for row in d.REWARDS.values() for values in row.values() for p in values}
        for stage in range(1, 7):
            solved = self.solve()
            self.assertEqual(solved['dream_data']['status'], 2)
            self.assertEqual(solved['dream_data']['cur_dream'], stage)
            self.assertEqual(self.bless(two=True)['dream_data']['cur_dream'], stage+1)
        expected = {}
        for row in d.REWARDS.values():
            for name in ('dream_prizes', 'own_wish_prizes'):
                for _, tid, n, lv in row[name]:
                    expected[tid, lv] = expected.get((tid, lv), 0) + n
        for (tid, lv), n in expected.items():
            self.assertEqual(self.count(tid, lv)-baseline[tid, lv], n, (tid, lv))
        self.assertEqual(len(self.saved()['receipts']), 6)
        self.assertEqual(list(self.saved()['received'].values()), [6, 6])
        for balance in self.saved()['npc_balances'].values():
            self.assertEqual(balance, {'5:1001:1': 408})
        self.assertFalse(self.call()['dream_data']['can_take'])
        self.reject(2, dict(answer=list(range(1,10)), local_token=self.saved()['token']))

    def test_invalid_answers_and_claims_never_mutate(self):
        self.call()
        for answer in ([], [1], list(range(9)), [1]*9, list(range(1,9))+[True],
                       {1:1, 3:3}, list(range(1,11)), '1,2,3,4,5,6,7,8,9'):
            self.reject(2, dict(answer=answer, local_token=self.saved()['token']))
        self.reject(2, dict(answer=list(range(1,10))))
        self.reject(4, dict(local_token=self.saved()['token']))
        self.reject(0, {})
        self.reject(1, dict(cur_dream=6))
        self.reject(3, dict(des_list=[1], index=1, local_token=self.saved()['token']))

    def test_stale_requests_and_wire_replays(self):
        self.call(); token = self.saved()['token']; self.solve()
        packet, response = self.packet, self.replies
        before = self.b.profile()
        self.assertEqual(self.b.respond(packet, self.state), response)
        self.assertEqual(self.b.profile(), before)
        self.reject(2, dict(answer=list(range(1,10)), local_token=token))
        self.bless(); self.reject(2, dict(answer=list(range(1,10)), local_token=token))
        self.assertEqual(self.saved()['cur_dream'], 2)

    def test_friend_selection_validation_and_atomic_capacity(self):
        entered = self.call(); ids = [p['id'] for p in entered['local_friends'].values()]
        self.solve(); token = self.saved()['token']
        for targets, index in (([],1), (ids[:3],1), ([ids[0]]*2,1), ([12345],1),
                               ([self.b.profile()['role_id']],1), (ids[:1],0), (ids[:1],5)):
            self.reject(3, dict(des_list=targets,index=index,local_token=token))
        role = self.b.profile(); role['activity']['dream']['received'][str(ids[1])] = 6
        self.b.save(role)
        self.reject(3, dict(des_list=ids[:2],index=1,local_token=token))
        self.assertEqual(self.saved()['npc_balances'], {})
        self.call(3, des_list=ids[:1], index=4)
        self.assertEqual(self.saved()['npc_balances'][str(ids[0])]['5:1001:1'], 68)

    def test_restart_mid_stage_and_next_period(self):
        self.call(); self.solve(); self.bless(); self.solve()
        before = self.saved(); inventory = self.b.profile()['attachments']
        self.b.close(); self.b = Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.call()['dream_data']['status'],2)
        self.assertEqual(self.saved(),before)
        with patch('network_redirect.game_clock.now',return_value=before['end']):
            self.reject(3,dict(des_list=[1],index=1,local_token=before['token']))
            fresh=self.call()['dream_data']
            self.assertEqual((fresh['cur_dream'],fresh['status']), (1,1))
            self.assertNotEqual(fresh['local_token'],before['token'])
            self.assertEqual(self.saved()['charge_gold'],0)
            self.assertEqual(self.saved()['receipts'],[])
            self.assertEqual(self.saved()['npc_balances'],before['npc_balances'])
            self.assertEqual(self.b.profile()['attachments'],inventory)

    def test_no_daily_reset_and_clock_rollback(self):
        self.call(); self.solve()
        with patch('network_redirect.game_clock.now',return_value=NOW+86400):
            self.assertEqual(self.call()['dream_data']['status'],2)
        self.reject(1,{})

    def test_level_and_disable(self):
        role=self.b.profile();role['level']=17;self.b.save(role)
        self.assertFalse(d.status(role,NOW)['can_join']);self.reject(1,{})
        role['level']=18;self.b.save(role);self.call()
        with patch.object(d,'load_rules',return_value=dict(d.load_rules(),enabled=False)):
            self.reject(1,{})
            self.assertFalse(d.status(role,NOW)['can_join'])

    def test_earned_gold_card_redemption_and_charge_claim_once(self):
        self.call()
        for _ in range(6):self.solve();self.bless()
        self.assertEqual(self.saved()['charge_gold'],0, 'awarding a card is not redeeming it')
        role=self.b.profile();card=next(i for i in role['attachments'] if i['type_id']==1152)
        self.ok(self.req(1051,item_type=1152,item_id=card['id'],item_count=1,des_type=1,des_id=0))
        self.assertEqual(self.saved()['charge_gold'],500)
        self.assertTrue(self.call()['dream_data']['can_take'])
        before=self.count(1369); token=self.saved()['token']
        self.assertTrue(self.call(4)['dream_data']['take_charge'])
        self.assertEqual(self.count(1369)-before,3)
        self.reject(4,dict(local_token=token))
        self.reject(4,dict(local_token=self.saved()['token']))

    def test_charge_threshold_principal_and_period_isolation(self):
        self.call(); role=self.b.profile()
        d.record_charge(role,299,NOW);self.b.save(role)
        for _ in range(6):self.solve();self.bless()
        self.assertFalse(self.call()['dream_data']['can_take'])
        role=self.b.profile();d.record_charge(role,1,NOW);self.b.save(role)
        self.assertTrue(self.call()['dream_data']['can_take'])
        end=self.saved()['end']
        with patch('network_redirect.game_clock.now',return_value=end):
            self.assertFalse(self.call()['dream_data']['can_take'])
            self.assertEqual(self.saved()['charge_gold'],0)

    def test_encoding_failure_rolls_back_rewards_and_npc_credits(self):
        self.call(); self.solve(); before=self.b.profile()
        with patch.object(d,'response',side_effect=ValueError('encode failed')):
            s=self.saved()
            ids=[p['id'] for p in d.friends(before,s,d.load_rules())][:2]
            self.reject(3,dict(des_list=ids,index=1,local_token=s['token']))
        self.assertEqual(self.b.profile(),before)

    def test_config_validation(self):
        base=d.load_rules()
        for field,value in [('enabled',1),('period_days',0),('npc_friend_count',1),
                            ('charge_prizes',[[5,1369,-1,1]]),('mode','original')]:
            with tempfile.TemporaryDirectory() as tmp:
                import json
                p=Path(tmp)/'rules.json';p.write_text(json.dumps(dict(base,**{field:value})))
                with self.assertRaises(formation.Rejected):d.load_rules(p)
