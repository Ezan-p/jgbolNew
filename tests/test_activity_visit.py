"""Real 1030 packets: reward identity, rarity, original dice, replay and migration."""
import copy
import itertools
import json
from pathlib import Path
from unittest.mock import patch
from test_activity import ActivityCase, NOW
from network_redirect import activity_visit as v, achievements, formation, summon
from network_redirect.backend import Backend
from network_redirect.protocol import decode


class VisitTests(ActivityCase):
    def call(self, index=0, op=1):
        events = self.req(1030, visit_index=index, op_type=op)
        self.ok(events)
        return next(data for kind, data in events if kind == 42)

    def visit_state(self, index):
        return self.b.profile()['activity']['visits'][str(index)]

    def achieved(self, ident):
        return next(row for row in achievements.rows(self.b.profile()) if row['id'] == ident)['times']

    def test_query_never_draws_or_grants(self):
        self.call()  # Initialize unrelated welfare/login state.
        before = self.b.profile()
        with patch.object(v, 'draw_fu', side_effect=AssertionError), patch.object(v, 'draw_shou', side_effect=AssertionError):
            for op in (0, 1):
                data = self.call(op=op)
                self.assertTrue(all(row['can_visit'] and not row['has_visit'] for row in data['visit_list'].values()))
        self.assertEqual(before, self.b.profile())

    def test_scratch_every_quality_matches_granted_spell(self):
        for day, q in enumerate(range(2, 6)):
            tid = v.SKILLS[q][0]
            with patch('network_redirect.backend.time.time', return_value=NOW+day*86400), patch.object(v, 'draw_shou', return_value=[6, tid, 1, 1]):
                before = self.b.profile()
                data = self.call(3)
                info = data['visit_list'][3]['prize_info']
                self.assertEqual(info, dict(object_type=6, attach_type=tid, attach_count=1, attach_level=1))
                self.assertEqual(before['attachments'], self.b.profile()['attachments'])
                claim = self.call(3, 2)
                added = [i for i in self.b.profile()['attachments'] if i['id'] not in {x['id'] for x in before['attachments']}]
                self.assertEqual(len(added), 1)
                self.assertEqual((added[0]['attach_type'], added[0]['type_id'], added[0]['level']), (6, tid, 1))
                self.assertEqual(added[0]['effect_value'], formation.skill_effect(dict(type_id=tid, level=1)))
                self.assertEqual(self.visit_state(3)['reward_ids'], [added[0]['id']])
                self.assertEqual(claim['local_prizes'][1], info)
                packets = list(map(decode, self.replies))
                received = [item for mid, _, data in packets if mid == 1035 for item in data['attach_list']]
                book = next(item for item in received if item['id'] == added[0]['id'])
                self.assertEqual((book['count'], book['protogenic'], book['equip_pos']), (0, 0, 0))
                self.assertEqual(before['gold_coin'], self.b.profile()['gold_coin'])

    def test_missing_grant_cannot_mark_claimed(self):
        self.call(3)
        before = self.b.profile()
        with patch.object(v.journey, 'grant'):
            self.assertEqual(self.req(1030, visit_index=3, op_type=2)[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_claimed_book_survives_material_cleanup_and_restart(self):
        from network_redirect import recharge
        self.call(3); self.call(3, 2)
        role = self.b.profile()
        ident = role['activity']['visits']['3']['reward_ids'][0]
        summon.add_item(role, 1150, 1)
        recharge.consume(role, 1150, 1)
        self.b.save(role)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.call()
        self.assertTrue(any(i['id'] == ident for i in self.b.profile()['attachments']))
        # Deliberate use as a material must not be undone by later visit queries.
        role = self.b.profile()
        role['attachments'] = [i for i in role['attachments'] if i['id'] != ident]
        self.b.save(role); self.call()
        self.assertFalse(any(i['id'] == ident for i in self.b.profile()['attachments']))

    def test_quality_probability_is_per_tier_not_pool_size(self):
        counts = {q: 0 for q in range(2, 6)}
        for ticket in range(100):
            with patch.object(v.secrets, 'randbelow', return_value=ticket):
                tid = v.draw_shou(self.b.activity_rules['visit_rules'])[1]
                counts[int(formation.SKILLS[tid]['quality'])] += 1
        self.assertEqual(counts, {2: 60, 3: 30, 4: 9, 5: 1})
        self.assertEqual(sum(map(len, v.SKILLS.values())), 54)
        self.assertFalse(set(range(1, 11)) & set().union(*map(set, v.SKILLS.values())))

    def test_all_original_dice_permutations(self):
        for dice in itertools.product(range(1, 7), repeat=3):
            sorted_dice = tuple(sorted(dice))
            expected = {(1,1,1):(10,326), (4,4,4):(8,325), (6,6,6):(16,323)}.get(sorted_dice)
            if expected is None:
                expected = (3,324) if sorted_dice in ((1,2,3),(2,3,4),(3,4,5),(4,5,6)) else (1,None)
            self.assertEqual(v.dice_result(dice), expected)

    def test_lu_amount_and_four_achievements_only_on_claim(self):
        for day, (dice, rate, ident) in enumerate([([6,6,6],16,323),([3,1,2],3,324),([4,4,4],8,325),([1,1,1],10,326)]):
            with patch('network_redirect.backend.time.time', return_value=NOW+day*86400):
                before = self.b.profile()['silver_coin']
                with patch.object(v.secrets, 'randbelow', side_effect=[x-1 for x in dice]):
                    data = self.call(2)
                info = data['visit_list'][2]['prize_info']
                self.assertEqual(list(info['form_type'].values()), dice)
                self.assertEqual(info['total_money'], 10000*rate)
                self.assertEqual(self.achieved(ident), 0)
                self.call(2, 2)
                self.assertEqual(self.b.profile()['silver_coin']-before, 10000*rate)
                self.assertEqual(self.achieved(ident), 1)

    def test_fu_eight_cards_one_reward_and_equipment_achievement(self):
        tid = v.EQUIPMENT[4][0]
        cards = [[5,tid,1,1]] + [[5,1001,5,1]]*7
        before = self.b.profile()
        with patch.object(v, 'draw_fu', side_effect=cards):
            data = self.call(1)
        info = data['visit_list'][1]['prize_info']
        self.assertEqual(len(info), 8)
        self.assertEqual(sum(row['get_flag'] for row in info.values()), 1)
        self.assertEqual(self.achieved(322), 0)
        self.call(1, 2)
        self.assertEqual(self.achieved(322), 1)
        new = [i for i in self.b.profile()['attachments'] if i['id'] not in {x['id'] for x in before['attachments']}]
        self.assertEqual([(i['attach_type'],i['type_id'],i['count']) for i in new], [(5,tid,1)])

    def test_fu_equipment_branch_and_non_equipment_branches(self):
        r = self.b.activity_rules['visit_rules']
        for ticket in (0, 20, 40, 60):
            with patch.object(v.secrets, 'randbelow', return_value=ticket):
                self.assertEqual(v.draw_fu(r), r['fu_rewards'][ticket//20]['reward'])
        for ticket, quality in ((0,2),(60,3),(90,4),(99,5)):
            with patch.object(v.secrets, 'randbelow', side_effect=[80,ticket]):
                reward = v.draw_fu(r)
            self.assertEqual(reward[0],5)
            self.assertEqual(int(formation.ITEMS[reward[1]]['quality']), quality)

    def test_restart_preserves_all_pending_results_and_config_changes(self):
        for index in (1,2,3): self.call(index)
        before = copy.deepcopy(self.b.profile())
        self.b.close();self.b = Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.b.activity_rules['visit_rules']['lu_base_silver'] = 1
        with patch.object(v, 'draw_fu', side_effect=AssertionError), patch.object(v, 'draw_shou', side_effect=AssertionError), patch.object(v.secrets,'randbelow',side_effect=AssertionError):
            self.call()
            for index in (1,2,3): self.call(index)
        self.assertEqual(before, self.b.profile())
        for index in (1,2,3): self.call(index,2)
        for index in (1,2,3): self.assertEqual(self.visit_state(index)['reward'], before['activity']['visits'][str(index)]['reward'])

    def test_replay_and_repeated_claim_cannot_double_grant(self):
        for index in (1,2,3):
            self.call(index)
            packet = self.packet
            before = self.b.profile()
            self.b.respond(packet,self.state_for_replay())
            self.assertEqual(before,self.b.profile())
            self.call(index,2)
            packet = self.packet;before=self.b.profile()
            self.b.respond(packet,self.state_for_replay())
            self.assertEqual(before,self.b.profile())
            self.assertEqual(self.req(1030,visit_index=index,op_type=2)[0][0],55)
            self.assertEqual(before,self.b.profile())

    def state_for_replay(self):
        return {'authenticated':True}

    def test_invalid_and_claim_before_draw_are_atomic(self):
        for index,op in ((0,2),(0,255),(4,1),(255,1),(1,0),(2,0),(3,0),(1,2),(2,2),(3,2)):
            before=self.b.profile()
            self.assertEqual(self.req(1030,visit_index=index,op_type=op)[0][0],55)
            self.assertEqual(before,self.b.profile())

    def test_rollover_and_clock_rollback(self):
        for index in (1,2,3): self.call(index);self.call(index,2)
        with patch('network_redirect.backend.time.time',return_value=NOW-86400):
            self.call()
            self.assertTrue(all(row['claimed'] for row in self.b.profile()['activity']['visits'].values()))
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            data=self.call()
            self.assertFalse(any(row['has_visit'] for row in data['visit_list'].values()))
            self.call(3);self.call(3,2)

    def test_legacy_pending_scratch_preserves_revealed_reward(self):
        role=self.b.profile()
        role['activity']['visits']['3']={'prize_info':v.prize_info([5,1022,1,1])}
        self.b.save(role)
        before=sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==1022)
        with patch.object(v,'draw_shou',side_effect=AssertionError): self.call(3);self.call(3,2)
        after=sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type']==5 and i['type_id']==1022)
        self.assertEqual(after-before,1)
        self.assertEqual(self.visit_state(3)['reward'],[5,1022,1,1])

    def test_bad_config_rejected(self):
        for key,value in (('lu_base_silver',0),('shou_quality_weights',{'2':1,'3':1,'4':1,'5':50}),('fu_equipment_weight',True),('fu_rewards',[{'weight':1,'reward':[6,99999,1,1]}])):
            r=v.load_rules();r[key]=value
            path=Path(self.tmp.name)/'rules.json';path.write_text(json.dumps(r))
            with self.assertRaises(formation.Rejected): v.load_rules(path)

    def test_failed_inventory_encoding_rolls_back_claim(self):
        self.call(3)
        before=self.b.profile()
        with patch.object(self.b, 'inventory', side_effect=ValueError('test encoding failure')):
            self.assertEqual(self.req(1030,visit_index=3,op_type=2)[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.call(3,2)
        self.assertTrue(self.visit_state(3)['claimed'])

    def test_midnight_expires_pending_without_grant(self):
        midnight=(NOW+8*3600)//86400*86400-8*3600+86400
        with patch('network_redirect.backend.time.time',return_value=midnight-1):
            self.call(3)
        before=self.b.profile()['attachments']
        with patch('network_redirect.backend.time.time',return_value=midnight):
            self.assertEqual(self.req(1030,visit_index=3,op_type=2)[0][0],55)
            self.call()
            self.assertEqual(self.b.profile()['activity']['visits'],{})
            self.assertEqual(before,self.b.profile()['attachments'])
            self.call(3);self.call(3,2)

    def test_legacy_pending_fu_and_lu_honor_snapshot(self):
        role=self.b.profile()
        role['activity']['visits']={
            '1':{'reward':[5,2001,1,1],'prize_info':[dict(v.prize_info([5,2001,1,1]),get_flag=j==0) for j in range(8)]},
            '2':{'reward':[12,0,160000,1],'prize_info':dict(v.prize_info([12,0,160000,1]),form_type=[6,6,6],total_money=160000)}}
        self.b.save(role)
        self.call(1);self.call(2);self.call(1,2);self.call(2,2)
        self.assertEqual(self.b.profile()['silver_coin']-role['silver_coin'],160000)
        self.assertEqual(self.achieved(322),1);self.assertEqual(self.achieved(323),1)

    def test_login_installs_scoped_scratch_icon_fix(self):
        source=summon.client_source(self.b.summon_rules)
        self.assertIn('ui._localVisitRestore',source)
        self.assertIn('data.getSmallSkillSprite(tid)',source)
        self.assertNotIn('__VISIT',source)
