"""Exercise original wire requests, limits, persistence and atomic settlement."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from network_redirect import activity, formation, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW=1792814400  # 2026-10-24 12:00 Asia/Shanghai
class ActivityCase(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.addCleanup(lambda:self.b.close());self.serial=100000;self.state={'authenticated':True}
        self.clock=patch('network_redirect.backend.time.time',return_value=NOW);self.clock.start();self.addCleanup(self.clock.stop)
        r=self.b.profile();r.update(level=60,gold_coin=100000,silver_coin=100000,energy=100)
        for c in r['corteges']:c.update(level=100)
        activity.prepare(r,NOW,self.b.activity_rules);self.b.save(r)
    def req(self,mid,**data):
        self.serial+=1;self.packet=encode(mid,dict(serial_num=self.serial,**data))
        self.replies=self.b.respond(self.packet,self.state)
        self.decoded=[decode(p) for p in self.replies]
        self.assertEqual(self.decoded[-1][0],1106)
        self.assertEqual(self.decoded[-1][2]['req_serial_num'],self.serial)
        return [(d['id'],login_fields(d['data'])) for m,_,d in self.decoded if m==2998]
    def ok(self,events):self.assertNotIn(55,[e for e,_ in events],events)

    def legacy_babel_floor(self):
        """Persist an old fixed floor for coordinate-based compatibility cases."""
        from network_redirect import activity_babel as babel
        role = self.b.profile()
        state = babel.state(role, NOW, self.b.activity_rules)
        fixture = dict(cur_floor=11, floors={})
        babel.generate(fixture)
        state['floors']['1'] = fixture['floors']['11']
        state['locale'] = dict(row=1, column=1)
        self.b.save(role)

class ActivityTests(ActivityCase):
    def test_boards_and_bootstrap_limits(self):
        for flag,e in ((0,47),(1,48)):
            out=self.req(1205,flag=flag);self.ok(out);self.assertEqual(out[-1][0],e)
        snapshot=self.b.snapshot();self.assertEqual(snapshot['top_fight_limit'],self.b.activity_rules['rank_daily_limit'])
        self.assertEqual(snapshot['convert_fight_limit'],self.b.activity_rules['convert_daily_limit'])
    def test_feed_time_limits_duplicate_and_rollover(self):
        self.ok(self.req(1040,feed_count=0))
        self.assertEqual(self.req(1040,feed_count=30)[-1][1]['feed_result'],2)
        before=self.b.profile();self.assertEqual(self.req(1040,feed_count=30)[-1][1]['feed_result'],4)
        self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.assertEqual(self.req(1040,feed_count=30)[-1][1]['feed_result'],2)
    def test_feed_invalid_count_and_closed_time(self):
        before=self.b.profile();self.assertEqual(self.req(1040,feed_count=201)[0][0],55)
        self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+3*3600):
            self.assertEqual(self.req(1040,feed_count=1)[-1][1]['feed_result'],3)
    def test_all_three_visits_two_phase_and_duplicate(self):
        self.ok(self.req(1030,visit_index=0,op_type=0))
        for i in (1,2,3):
            self.assertEqual(self.req(1030,visit_index=i,op_type=2)[0][0],55)
            self.ok(self.req(1030,visit_index=i,op_type=1))
            before=self.b.profile();self.ok(self.req(1030,visit_index=i,op_type=1));self.assertEqual(before,self.b.profile())
            self.ok(self.req(1030,visit_index=i,op_type=2))
            before=self.b.profile();self.assertEqual(self.req(1030,visit_index=i,op_type=2)[0][0],55);self.assertEqual(before,self.b.profile())
    def test_visit_restart_preserves_pending_and_claim(self):
        self.ok(self.req(1030,visit_index=1,op_type=1));before=self.b.profile()
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(before,self.b.profile());self.ok(self.req(1030,visit_index=1,op_type=2))
    def test_pray_original_value_and_carryover(self):
        r=self.b.profile();r['souls']={'5004':100};self.b.save(r)
        self.ok(self.req(1085,object_count=1,object_list=[dict(object_type=10,object_id=5004,count=26)]))
        r=self.b.profile();self.assertEqual(r['spirit_retain'],8);self.assertEqual(r['souls']['5004'],74)
    def test_pray_duplicate_selection_and_active_companion_atomic(self):
        r=self.b.profile();r['souls']={'5004':100};self.b.save(r);before=self.b.profile()
        row=dict(object_type=10,object_id=5004,count=26)
        self.assertEqual(self.req(1085,object_count=2,object_list=[row,row])[0][0],55);self.assertEqual(before,self.b.profile())
        self.assertEqual(self.req(1085,object_count=1,object_list=[dict(object_type=4,object_id=r['corteges'][0]['id'],count=1)])[0][0],55)
        self.assertEqual(before,self.b.profile())
    @patch('network_redirect.activity_practice.draw', return_value='hp')
    def test_training_win_updates_bonus_and_exhaustion(self, _draw):
        r=self.b.profile();r['rule_index']=55;self.b.save(r)
        hp=self.b.profile()['corteges'][0]['hp']
        self.ok(self.req(1026,fight_type=4,des_type=1,des_id=0,des_value=0))
        r=self.b.profile();self.assertEqual(r['rule_index'],56);self.assertEqual(r['corteges'][0]['hp'],hp+1120)
        self.assertEqual(self.req(1026,fight_type=4,des_type=1)[0][0],55)
    def test_rank_fight_daily_score_and_exchange(self):
        self.ok(self.req(1021,flag=0));self.ok(self.req(1026,fight_type=2,des_type=2,des_value=99,des_id=930099))
        r=self.b.profile();self.assertEqual(r['activity']['rank_order'],99)
        self.assertEqual(self.req(1201,flag=2)[0][0],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.ok(self.req(1021,flag=0));self.assertEqual(self.req(1201,flag=2)[0][0],55)
        self.ok(self.req(1203,exchange_type=5));before=self.b.profile()
        self.assertEqual(self.req(1203,exchange_type=5)[0][0],55);self.assertEqual(before,self.b.profile())
    def test_rank_rejects_forged_target_and_insufficient_energy(self):
        before=self.b.profile();self.assertEqual(self.req(1026,fight_type=2,des_type=2,des_value=1,des_id=77)[0][0],55)
        self.assertEqual(before,self.b.profile())
    @patch('network_redirect.activity_rape.roll_forms', return_value=[1,3,5])
    @patch('network_redirect.activity_rape.journey.battle', return_value=(1,[],[]))
    def test_rape_fight_full_board_grants_skill_once(self, *_):
        self.ok(self.req(1029,flag=1))
        ids=list(map(int,self.b.profile()['activity']['rape_boards'][0]['form_list']['2']))
        for ident in ids:self.ok(self.req(1026,fight_type=3,des_type=2,des_value=1,des_id=ident))
        r=self.b.profile();self.assertTrue(all(x['has_win'] for x in r['activity']['rape_boards'][0]['form_list']['2'].values()))
        before=self.b.profile();self.assertEqual(self.req(1026,fight_type=3,des_type=2,des_value=1,des_id=ids[-1])[0][0],55);self.assertEqual(before,self.b.profile())
    @patch('network_redirect.activity_rape.roll_forms', return_value=[1,3,5])
    def test_rape_refresh_and_sweep(self, *_):
        self.ok(self.req(1029,flag=1))
        ident=int(next(iter(self.b.profile()['activity']['rape_boards'][0]['form_list']['2'])))
        self.ok(self.req(1041,form_index=1,object_type=2,object_id=ident))
        self.ok(self.req(1072));self.assertEqual(self.decoded[-2][2]['id'],114)
        for _ in range(self.b.activity_rules['rape_free_refreshes']):self.ok(self.req(1029,flag=2))
        self.assertEqual(self.req(1029,flag=2)[0][0],55)
    @patch('network_redirect.duty_balance.weighted', side_effect=lambda rows: rows[0])
    @patch('network_redirect.duty_balance.guard_reward', side_effect=lambda number:
           dict(round=number, difficulty=1, reward=[12, 0, 3000, 1]))
    def test_duty_query_start_fight_claim(self, *_pickers):
        self.ok(self.req(1043,flag=1));self.assertIsNone(self.b.profile()['activity']['duty'])
        self.ok(self.req(1043,flag=0))
        self.assertEqual(self.req(1026,fight_type=5,des_type=3,des_value=1)[0][0],55)
        self.ok(self.req(1043,plus_type=1,plus_index=1))
        for rnd in range(1,4):self.ok(self.req(1026,fight_type=5,des_type=3,des_value=rnd))
        self.ok(self.req(1043,plus_type=3));self.assertEqual(self.req(1043,plus_type=3)[0][0],55)
        self.ok(self.req(1043,plus_type=2,plus_index=1))
    def test_party_open_and_closed_and_bonus(self):
        self.ok(self.req(1049,query_type=1));self.ok(self.req(1202,flag=1));self.ok(self.req(1026,fight_type=6))
        self.assertEqual(self.req(1201,flag=1)[0][0],55)  # weekly prize, not immediate daily participation
        self.b.activity_rules['party_period']=[39600,46800]
        with patch('network_redirect.backend.time.time',return_value=NOW+7200):self.assertEqual(self.req(1026,fight_type=6)[0][0],55)
    def test_convert_first_free_and_monthcard_extra(self):
        r=self.b.profile();r['vip_level']=3;tid=next(iter(activity.CONVERT))
        if not any(c['type']==tid for c in r['corteges']):r['corteges'].append(summon.companion(r,tid))
        r['attachments']=[i for i in r['attachments'] if i['type_id']!=1024];self.b.save(r)
        self.ok(self.req(1026,fight_type=10,des_value=tid))
        self.assertEqual(self.b.profile()['convert_fight_count'],1)
        # Result may itself return a token. Remove it to verify the paid boundary.
        r=self.b.profile();r['attachments']=[i for i in r['attachments'] if i['type_id']!=1024];self.b.save(r)
        before=self.b.profile();self.assertEqual(self.req(1026,fight_type=10,des_value=tid)[0][0],55);self.assertEqual(before,self.b.profile())
        r=self.b.profile();summon.add_item(r,1024,10);r['convert_fight_count']=3;r['month_card_time']=NOW;self.b.save(r)
        self.assertEqual(self.req(1026,fight_type=10,des_value=tid)[0][0],55)
        r=self.b.profile();r['month_card_time']=NOW+1;self.b.save(r)
        self.ok(self.req(1026,fight_type=10,des_value=tid));self.assertEqual(self.b.profile()['convert_fight_count'],4)
        self.assertEqual(self.req(1026,fight_type=10,des_value=tid)[0][0],55)

    def test_abyss_multiguard_pill_reduces_total_once(self):
        from network_redirect import activity_abyss as ab
        layer=next(k for k,v in ab.BOSSES.items() if '/' in next(v for k,v in v.items() if k and k.startswith('cortege_list')))
        s=dict(boss=layer,reductions=[0]*4);base=ab.enemies(s)
        s['reductions']=[10000,3000,100000,100]
        reduced=ab.enemies(s)
        for index,key in enumerate(('gongji','fangyu','hp','magic')):
            self.assertEqual(sum(u[key] for u in reduced),max(len(base),sum(u[key] for u in base)-s['reductions'][index]))
        self.assertTrue(all(u['hp']>0 for u in reduced))

    def test_replay_same_packet_and_changed_payload(self):
        self.ok(self.req(1040,feed_count=30));before=self.b.profile();packet=self.packet;replies=self.replies
        self.assertEqual(self.b.respond(packet,self.state),replies);self.assertEqual(before,self.b.profile())
        out=self.b.respond(encode(1040,dict(serial_num=self.serial,feed_count=20)),self.state)
        self.assertEqual(decode(out[0])[2]['id'],55);self.assertEqual(before,self.b.profile())
    def test_serialization_failure_rolls_back(self):
        before=self.b.profile()
        with patch('network_redirect.backend.activity.attributes',side_effect=ValueError('test')):
            self.assertEqual(self.req(1040,feed_count=30)[0][0],55)
        self.assertEqual(before,self.b.profile())
    def test_config_validation(self):
        for key,value in [('mode','official'),('feed_periods',[[1,2],[1,3]]),('rank_daily_limit',-1),('battle_npc',-999)]:
            r=copy.deepcopy(self.b.activity_rules);r[key]=value;p=Path(self.tmp.name)/'bad.json';p.write_text(json.dumps(r))
            with self.assertRaises(formation.Rejected):activity.load_rules(p)
    def test_trial_kill_claim_restart_and_daily_limit(self):
        from network_redirect import activity_trial
        role=self.b.profile()
        with patch.object(activity_trial.secrets,'randbelow',return_value=0):
            activity_trial.encounter(role,NOW,self.b.activity_rules)
        self.b.save(role)
        out=self.req(1064,flag=2);self.ok(out)
        boss=out[-1][1]['train_data']['boss_list'][1]
        self.assertEqual(self.req(1064,flag=9)[0][0],55)
        with patch('network_redirect.activity.journey.battle',return_value=(3,[dict(src_hp=1,des_hp=50000)],
                [dict(is_src=True,damage_count=8,damage_list=[50000000,0,0,0,0,0,0,0])])):
            self.ok(self.req(1026,fight_type=11,des_type=8,des_id=boss['type_id']))
        self.assertTrue(self.b.profile()['activity']['trial_bosses'][0]['is_dead'])
        self.ok(self.req(1064,flag=9));before=self.b.profile()
        self.assertEqual(self.req(1064,flag=9)[0][0],55);self.assertEqual(before,self.b.profile())
    def test_query_lineup_and_rank_challenge_relation(self):
        self.ok(self.req(1021,flag=0))
        ranks=next(d for m,_,d in self.decoded if m==1022)
        self.assertEqual(sum(x['top_relation']==2 for x in ranks['show_list']),5)
        out=self.req(1039,des_type=2,des_id=930099);self.ok(out)
        self.assertIn('owner_cheer_info',out[-1][1]);self.assertIn('type_id',out[-1][1]['cortege_list'][1])
    def test_babel_movement_rewards_persist_and_teleport_validation(self):
        self.legacy_babel_floor()
        self.ok(self.req(1353,id=1,data='{}'))
        self.ok(self.req(1353,id=2,data='{target_pos={row=1,column=2}}'))
        self.ok(self.req(1353,id=2,data='{target_pos={row=1,column=3}}'))
        s=self.b.profile()['activity']['babel'];self.assertEqual(s['coin_count'],50)
        self.assertEqual(self.req(1353,id=7,data='{floor=60}')[0][0],55)
        before=self.b.profile();self.assertEqual(self.req(1353,id=2,data='{target_pos={row=5,column=8}}')[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.ok(self.req(1353,id=6,data='{}'))
        for col in (2,3):self.ok(self.req(1353,id=2,data=summon.lua(dict(target_pos=dict(row=1,column=col)))))
        self.assertEqual(self.b.profile()['activity']['babel']['coin_count'],50)
    def test_babel_shop_costs_limits_and_restoration(self):
        self.ok(self.req(1353,id=1,data='{}'));r=self.b.profile();s=r['activity']['babel'];s.update(life=50,energy=20);summon.add_item(r,20000,1000);summon.add_item(r,20016,1);self.b.save(r)
        shop=next(data['data'] for event,data in self.req(1353,id=8,data='{}')
                   if event==203 and data['id']==8)
        index=max(range(1,7), key=lambda i: shop['my_shop'][i]['limit'])
        buy_count=shop['my_shop'][index]['limit']
        cost=shop['my_shop'][index]['need_coin'];r=self.b.profile();summon.add_item(r,20000,cost*buy_count+200);self.b.save(r)
        self.ok(self.req(1353,id=4,data=summon.lua(dict(index=index,count=buy_count))))
        before=self.b.profile();self.assertEqual(self.req(1353,id=4,data=summon.lua(dict(index=index,count=1)))[0][0],55);self.assertEqual(before,self.b.profile())
        self.ok(self.req(1353,id=10,data='{item_type=20016,count=1}'))
        self.ok(self.req(1353,id=11,data='{}'))
        r=self.b.profile();self.assertEqual(r['activity']['babel']['energy'],30);self.assertEqual(r['activity']['babel']['life'],100)
        self.ok(self.req(1353,id=9,data='{}'));self.assertEqual(self.req(1353,id=9,data='{}')[0][0],55)

class UndergoTests(ActivityCase):
    # Reuse only setup/request helpers, not duplicate the parent test cases.
    def test_undergo_original_entry_and_nine_position_battle(self):
        out=self.req(1349,id=1,data='{}');self.ok(out)
        self.assertIn(1349,[m for m,_,d in self.decoded])
        role=self.b.profile();cid=role['corteges'][0]['id'];before=role['strength']
        self.ok(self.req(1349,id=4,data=summon.lua(dict(mode=1,map_id=101,cortege_list={cid:9}))))
        self.assertEqual(self.b.profile()['strength'],before-2)
        replay=next(d for m,_,d in self.decoded if m==1140)
        self.assertTrue(all(len(a['damage_list'])==9 for a in replay['fight_result']))
        self.assertEqual(self.b.profile()['activity']['undergo']['count'],1)
        self.assertEqual(self.b.profile()['corteges'][0]['order'],role['corteges'][0]['order'])
    def test_undergo_forged_lineup_and_progress_rollback(self):
        self.ok(self.req(1349,id=1,data='{}'));before=self.b.profile()
        for d in (dict(mode=1,map_id=201,cortege_list={1:1}),dict(mode=1,map_id=101,cortege_list={1:999999}),
                  dict(mode=2,map_id=101,cortege_list={before['corteges'][0]['id']:1})):
            self.assertEqual(self.req(1349,id=4,data=summon.lua(d))[0][0],55)
            self.assertEqual(before,self.b.profile())
    def test_undergo_shop_and_day_prize(self):
        self.ok(self.req(1349,id=1,data='{}'))
        self.ok(self.req(1349,id=3,data='{}'))
        r=self.b.profile();summon.add_item(r,1366,10000);self.b.save(r)
        self.ok(self.req(1349,id=5,data='{index=1,count=1}'))
        self.assertEqual(self.req(1349,id=7,data='{index=1}')[0][0],55)
        r=self.b.profile();r['activity']['undergo']['challenge_passed']=list(range(101,110));self.b.save(r)
        self.ok(self.req(1349,id=7,data='{index=1}'));before=self.b.profile()
        self.assertEqual(self.req(1349,id=7,data='{index=1}')[0][0],55);self.assertEqual(before,self.b.profile())


class HomeAbyssTests(ActivityCase):
    def test_home_pet_transform_source_materials_memory_and_restart(self):
        self.ok(self.req(1348,id=1,data='{}'));r=self.b.profile();r['activity']['home']['build']['5']=1
        summon.add_item(r,1365,3);summon.add_item(r,1345,45);self.b.save(r)
        self.ok(self.req(1348,id=22,data='{}'))
        pet=self.b.profile()['activity']['home']['pets'][0];self.assertEqual(pet['type_id'],201)
        data=next(login_fields(d['data']) for m,_,d in self.decoded if m==1348)
        self.assertNotIn('main_type',data['update_list'][1])
        self.ok(self.req(1348,id=21,data='{pet_id=1,des_type=202}'))
        changed=self.b.profile()['activity']['home']['pets'][0]
        self.assertEqual(changed['type_id'],202);self.assertEqual(changed['grow_values'],[v+d for v,d in zip(pet['grow_values'],[-9,-14,15,9])])
        before=self.b.profile();self.assertEqual(self.req(1348,id=21,data='{pet_id=1,des_type=202}')[0][0],55);self.assertEqual(before,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.ok(self.req(1348,id=21,data='{pet_id=1,des_type=201}'))
        self.assertEqual(self.b.profile()['activity']['home']['pets'][0],pet)
        self.ok(self.req(1348,id=22,data='{}'));self.assertEqual(len(self.b.profile()['activity']['home']['pets']),1)
        self.assertEqual(sum(i['count'] for i in self.b.profile()['attachments'] if i['type_id']==1365),1)

    def test_home_friends_protocol_fertilize_restart_and_daily_reset(self):
        self.ok(self.req(1348,id=13,data='{}'))
        data=next(login_fields(d['data']) for m,_,d in self.decoded if m==1348)
        self.assertEqual(len(data['friend_data']),10)
        self.assertTrue(all(v['is_npc'] for v in data['friend_data'].values()))
        self.ok(self.req(1348,id=6,data='{friend_id=900001}'))
        silver=self.b.profile()['silver_coin']
        self.ok(self.req(1348,id=7,data='{friend_id=900001,plant_grid=1}'))
        self.assertEqual(self.b.profile()['silver_coin'],silver+10000)
        before=self.b.profile();self.assertEqual(self.req(1348,id=7,data='{friend_id=900001,plant_grid=1}')[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.assertEqual(self.req(1348,id=23,data='{friend_id=900001}')[0][0],55)
        r=self.b.profile();r['month_card_time']=NOW+86400;self.b.save(r)
        self.ok(self.req(1348,id=23,data='{friend_id=900001}'))
        self.assertEqual(self.b.profile()['silver_coin'],silver+20000)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.ok(self.req(1348,id=23,data='{friend_id=900001}'));self.assertEqual(self.b.profile()['silver_coin'],silver+20000)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.ok(self.req(1348,id=7,data='{friend_id=900001,plant_grid=1}'))
        self.assertEqual(self.b.profile()['silver_coin'],silver+30000)

    def test_home_invitation_messages_and_harvest_details(self):
        r=self.b.profile();r['silver_coin']=1000000000;self.b.save(r)
        for typ in (1,2):self.ok(self.req(1348,id=2,data=summon.lua(dict(building_type=typ))))
        self.ok(self.req(1348,id=3,data='{plant_grid=1,seed_type=1}'))
        self.ok(self.req(1348,id=5,data='{friend_id=900001}'))
        before=self.b.profile();self.assertEqual(self.req(1348,id=5,data='{friend_id=900001}')[0][0],55);self.assertEqual(before,self.b.profile())
        self.ok(self.req(1348,id=12,data=summon.lua(dict(friend_id=900001,chat_msg='药田照料测试'))))
        self.ok(self.req(1348,id=6,data='{friend_id=900001}'))
        data=next(login_fields(d['data']) for m,_,d in self.decoded if m==1348)
        self.assertIn('药田照料测试',data['message_data'][1])
        self.ok(self.req(1348,id=18,data='{clean=true}'));self.assertFalse(self.b.profile()['activity']['home']['new_event'])
        with patch('network_redirect.backend.time.time',return_value=NOW+23*3600):
            self.ok(self.req(1348,id=10,data='{plant_grid=1}'))
            data=next(login_fields(d['data']) for m,_,d in self.decoded if m==1348)
            self.assertEqual(data['base_worth'],800);self.assertEqual(data['friend_plus'],5)
            self.assertEqual(data['loss_plus'],-10);self.assertEqual(data['prize_list'][1]['attach_count'],756)

    def test_treasure_map_costs_shielding_restart_and_batch(self):
        r=self.b.profile();r['level']=80;summon.add_item(r,1431,3);self.b.save(r)
        self.ok(self.req(1329,id=3,data='{op_type=1,type_id=1431}'));gold=self.b.profile()['gold_coin']
        self.ok(self.req(1329,id=3,data='{op_type=2,type_id=1431,index_list={1,2}}'))
        board=self.b.profile()['activity']['abyss']['maps']['1431'];self.assertTrue(all(board['goods'][i]['rm'] for i in (0,1)))
        self.assertEqual(self.b.profile()['gold_coin'],gold)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile()['activity']['abyss']['maps']['1431'],board)
        for _ in range(3):self.ok(self.req(1329,id=3,data='{op_type=2,type_id=1431}'))
        self.assertEqual(self.b.profile()['gold_coin'],gold-60)
        before=self.b.profile();self.assertEqual(self.req(1329,id=3,data='{op_type=2,type_id=1431}')[0][0],55);self.assertEqual(before,self.b.profile())
        self.ok(self.req(1329,id=24,data='{map_type=1431,treasure_count=2,open_count=2}'))
        self.assertEqual(self.b.profile()['gold_coin'],gold-100)
        self.assertEqual(self.req(1329,id=3,data='{op_type=1,type_id=1431}')[0][0],55)

    def test_treasure_map_invalid_removal_quick_monthcard_and_atomic_batch(self):
        r=self.b.profile();r['level']=80;summon.add_item(r,1431,1);self.b.save(r)
        self.ok(self.req(1329,id=3,data='{op_type=1,type_id=1431}'));before=self.b.profile()
        for data in ('{op_type=2,type_id=1431,index_list={1,1}}','{op_type=2,type_id=1431,index_list={1,2,3}}','{op_type=5,type_id=1431}'):
            self.assertEqual(self.req(1329,id=3,data=data)[0][0],55);self.assertEqual(before,self.b.profile())
        self.assertEqual(self.req(1329,id=24,data='{map_type=1431,treasure_count=2,open_count=2}')[0][0],55);self.assertEqual(before,self.b.profile())
        r=self.b.profile();r['month_card_time']=NOW+100;self.b.save(r)
        self.ok(self.req(1329,id=3,data='{op_type=5,type_id=1431}'));self.ok(self.req(1329,id=3,data='{op_type=6,type_id=1431}'))
    def test_drug_experience_pills_original_values_and_atomic_selection(self):
        r=self.b.profile();r['level']=80;summon.add_item(r,1442,10);self.b.save(r)
        out=self.req(1059,first_send=True,flag=3,cortege_id=0,roll_count=1,roll_list=[dict(type_id=1442,count=10)])
        self.ok(out);self.assertEqual(out[-1],(65,dict(flag=3)))
        r=self.b.profile();self.assertEqual((r['drug_level'],r['drug_exp']),(2,30))
        summon.add_item(r,1442,2);self.b.save(r);before=self.b.profile()
        self.assertEqual(self.req(1059,first_send=True,flag=3,cortege_id=0,roll_count=2,roll_list=[dict(type_id=1442,count=1),dict(type_id=1442,count=1)])[0][0],55)
        self.assertEqual(before,self.b.profile())
    def test_abyss_random_events_persist_answers_and_reject_duplicate_rewards(self):
        from network_redirect.activity_abyss_random import create
        r=self.b.profile();r['level']=80;self.b.save(r)
        self.ok(self.req(1329,id=1,data='{}'))
        r=self.b.profile();s=r['activity']['abyss'];s['events']=[create(k,self.b.activity_rules) for k in (1,5,2,4)]
        s['crystals']=500;summon.add_item(r,1001,2);self.b.save(r)
        self.ok(self.req(1329,id=4,data='{op_type=0}'));e=self.b.profile()['activity']['abyss']['events'][0]
        self.assertNotIn('answer',self.replies[-2].decode('latin1'))
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile()['activity']['abyss']['events'][0],e)
        self.ok(self.req(1329,id=4,data=summon.lua(dict(op_type=1,num=str(e['answer'])))))
        before=self.b.profile();self.assertEqual(self.req(1329,id=4,data=summon.lua(dict(op_type=1,num=e['answer'])))[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.ok(self.req(1329,id=4,data='{op_type=0}'));e=self.b.profile()['activity']['abyss']['events'][0]
        self.ok(self.req(1329,id=4,data=summon.lua(dict(op_type=1,cortege_type=e['answer']))))
        self.ok(self.req(1329,id=4,data='{op_type=0}'));self.ok(self.req(1329,id=4,data='{op_type=1,index=1}'))
        self.ok(self.req(1329,id=4,data='{op_type=0}'))
        s=self.b.profile()['activity']['abyss'];self.assertEqual(s['events'],[]);self.assertTrue(400<=s['crystals']<=500)
        self.assertEqual(self.req(1329,id=4,data='{op_type=0}')[0][0],55)

    def test_abyss_random_queue_cap_give_up_and_four_guesses(self):
        r=self.b.profile();r['level']=80;self.b.save(r);self.ok(self.req(1329,id=1,data='{}'))
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.ok(self.req(1329,id=1,data='{}'));self.assertEqual(len(self.b.profile()['activity']['abyss']['events']),5)
        from network_redirect.activity_abyss_random import create
        r=self.b.profile();s=r['activity']['abyss'];e=create(1,self.b.activity_rules);e['answer']=99;s['events']=[e];self.b.save(r)
        self.ok(self.req(1329,id=4,data='{op_type=0}'))
        for n in (1,2,3,4):self.ok(self.req(1329,id=4,data=summon.lua(dict(op_type=1,num=n))))
        self.assertEqual(self.b.profile()['activity']['abyss']['events'],[])

    def test_abyss_random_soul_boss_uses_server_damage_and_free_limit(self):
        from network_redirect.activity_abyss_random import create
        r=self.b.profile();r['level']=80;self.b.save(r);self.ok(self.req(1329,id=1,data='{}'))
        r=self.b.profile();e=create(3,self.b.activity_rules);e['hp']=100000000;r['activity']['abyss']['events']=[e];self.b.save(r)
        self.ok(self.req(1329,id=4,data='{op_type=0}'));gold=self.b.profile()['gold_coin']
        for i in range(4):
            hp=self.b.profile()['activity']['abyss']['events'][0]['hp']
            self.ok(self.req(1329,id=4,data='{op_type=1}'))
            self.assertLess(self.b.profile()['activity']['abyss']['events'][0]['hp'],hp)
            fight=next(d for m,_,d in self.decoded if m==1027);self.assertEqual(fight['fight_type'],25)
        self.assertEqual(self.b.profile()['gold_coin'],gold-self.b.activity_rules['abyss_event_fight_gold'])
        self.ok(self.req(1329,id=4,data='{op_type=2}'));self.assertEqual(self.b.profile()['activity']['abyss']['events'],[])

    def test_home_original_garden_fields_and_manual_bug_resolution(self):
        r=self.b.profile();r['silver_coin']=1000000000;self.b.save(r)
        for typ in (1,2):self.ok(self.req(1348,id=2,data=summon.lua(dict(building_type=typ))))
        self.ok(self.req(1348,id=3,data='{plant_grid=1,seed_type=1}'))
        grid=next(login_fields(d['data'])['grid_info'] for mid,_,d in self.decoded if mid==1348)
        self.assertEqual(grid['start_time'],NOW);self.assertEqual(grid['total_plus_times'],5)
        event=grid['event_info'][1];self.assertGreater(event['end_time'],event['start_time'])
        with patch('network_redirect.backend.time.time',return_value=event['start_time']):
            self.ok(self.req(1348,id=4,data='{plant_grid=1,event_index=1}'))
            before=self.b.profile();self.assertEqual(self.req(1348,id=4,data='{plant_grid=1,event_index=1}')[0][0],55)
            self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=grid['gain_time']+1):
            self.ok(self.req(1348,id=10,data='{plant_grid=1}'))
            reward=next(login_fields(d['data'])['prize_list'][1] for mid,_,d in self.decoded if mid==1348)
            self.assertEqual(reward['attach_count'],800)

    def test_home_assistant_covers_events_and_expired_contract_does_not(self):
        r=self.b.profile();r['silver_coin']=1000000000;self.b.save(r)
        for typ in (1,2):self.ok(self.req(1348,id=2,data=summon.lua(dict(building_type=typ))))
        self.ok(self.req(1348,id=8,data='{hour=1}'))
        before=self.b.profile();self.assertEqual(self.req(1348,id=8,data='{hour=48}')[0][0],55);self.assertEqual(before,self.b.profile())
        self.ok(self.req(1348,id=3,data='{plant_grid=1,seed_type=1}'))
        with patch('network_redirect.backend.time.time',return_value=NOW+23*3600):
            self.ok(self.req(1348,id=10,data='{plant_grid=1}'))
            reward=next(login_fields(d['data'])['prize_list'][1] for mid,_,d in self.decoded if mid==1348)
            self.assertEqual(reward['attach_count'],720)
            self.ok(self.req(1348,id=8,data='{hour=24}'))
            self.ok(self.req(1348,id=3,data='{plant_grid=1,seed_type=1}'))
        with patch('network_redirect.backend.time.time',return_value=NOW+46*3600):
            self.ok(self.req(1348,id=10,data='{plant_grid=1}'))
            reward=next(login_fields(d['data'])['prize_list'][1] for mid,_,d in self.decoded if mid==1348)
            self.assertEqual(reward['attach_count'],800)

    def test_home_upgrade_seed_harvest_and_restart(self):
        r=self.b.profile();r['silver_coin']=1000000000;self.b.save(r)
        self.ok(self.req(1348,id=1,data='{}'))
        self.ok(self.req(1348,id=2,data='{building_type=1}'))
        self.ok(self.req(1348,id=2,data='{building_type=2}'))
        self.ok(self.req(1348,id=3,data='{plant_grid=1,seed_type=1}'))
        before=self.b.profile();self.assertEqual(self.req(1348,id=10,data='{plant_grid=1}')[0][0],55);self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+23*3600):
            self.ok(self.req(1348,id=10,data='{plant_grid=1}'))
            before=self.b.profile();self.assertEqual(self.req(1348,id=10,data='{plant_grid=1}')[0][0],55);self.assertEqual(before,self.b.profile())
    def test_home_pray_and_forged_build_atomic(self):
        self.ok(self.req(1348,id=1,data='{}'))
        r=self.b.profile();r['activity']['home']['build']['3']=1;self.b.save(r)
        self.ok(self.req(1348,id=11,data='{}'));before=self.b.profile()
        self.assertEqual(self.req(1348,id=11,data='{}')[0][0],55);self.assertEqual(before,self.b.profile())
        self.assertEqual(self.req(1348,id=2,data='{building_type=99}')[0][0],55);self.assertEqual(before,self.b.profile())
    def test_abyss_accumulation_claim_and_forged_floor(self):
        r=self.b.profile();r['level']=80;self.b.save(r)
        self.ok(self.req(1329,id=1,data='{}'));before=self.b.profile()
        self.assertEqual(self.req(1329,id=2,data='{des_area=81}')[0][0],55);self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+300):
            self.ok(self.req(1329,id=10,data='{}'));s=self.b.profile()['activity']['abyss'];self.assertEqual(len(s['bag']),1)
            self.ok(self.req(1329,id=10,data='{}'));self.assertEqual(self.b.profile()['activity']['abyss'],s)
            self.ok(self.req(1329,id=5,data='{}'));before=self.b.profile()
            self.assertEqual(self.req(1329,id=5,data='{}')[0][0],55);self.assertEqual(before,self.b.profile())
    def test_abyss_boss_replay_and_daily_limit(self):
        r=self.b.profile();r['level']=80;self.b.save(r)
        for _ in range(5):
            self.ok(self.req(1329,id=6,data='{}'));self.assertIn(1027,[m for m,_,d in self.decoded])
        before=self.b.profile();self.assertEqual(self.req(1329,id=6,data='{}')[0][0],55);self.assertEqual(before,self.b.profile())
    def test_drug_recipe_materials_craft_recycle_and_slot(self):
        r=self.b.profile();r['level']=80;self.b.save(r)
        self.ok(self.req(1329,id=20,data='{index=1}'));before=self.b.profile()
        self.assertEqual(self.req(1329,id=20,data='{index=1}')[0][0],55);self.assertEqual(before,self.b.profile())
        for i,n in ((1,2),(2,1),(3,8)):
            self.ok(self.req(1329,id=23,data=summon.lua(dict(index1=1,index2=i,count=n))))
        with patch('network_redirect.activity_drug.secrets.randbelow',return_value=0):
            self.ok(self.req(1329,id=21,data='{index=1}'))
        r=self.b.profile();self.assertEqual(r['drug_study_flag'],2);self.assertEqual(r['drug_exp'],10)
        self.assertEqual(self.req(1329,id=21,data='{index=1}')[0][0],55)
        self.ok(self.req(1329,id=17,data='{index=1,type_id=1501}'))
        r=self.b.profile();self.assertEqual(r['activity']['abyss']['reductions'][0],10000)
        self.assertEqual(self.req(1329,id=17,data='{index=1,type_id=1501}')[0][0],55)
        r=self.b.profile();summon.add_item(r,1501,1);self.b.save(r)
        self.ok(self.req(1329,id=8,data='{type_id=1501,num=1}'))
        self.assertEqual(self.req(1329,id=8,data='{type_id=1501,num=1}')[0][0],55)
    def test_home_training_bonus_applies_to_simulation(self):
        from network_redirect import journey
        r=self.b.profile();self.ok(self.req(1348,id=1,data='{}'));r=self.b.profile()
        r['silver_coin']=1000000000;r['activity']['home']['build']['4']=1;self.b.save(r)
        self.ok(self.req(1348,id=20,data='{train_type=1,consume_type=1,use_count=10}'))
        r=self.b.profile();self.assertEqual(r['activity']['home']['train']['1']['level'],1)
        cfg=dict(cortege_list='1001|1')
        # A large HP target keeps the first attack from being clamped by death.
        units=journey.fighters(r,cfg);units[1][0].update(hp=1000000,max_hp=1000000,fangyu=1)
        units[0][0]['skills']=[]
        actions=journey.battle(r,cfg,self.b.journey_rules,units=units)[2]
        trained=actions[0]['damage_list'][0]
        r['activity']['home']['train']['1']['level']=0
        plain=journey.battle(r,cfg,self.b.journey_rules,units=units)[2][0]['damage_list'][0]
        self.assertGreater(trained,plain)

    def test_home_seventh_prayer_uses_original_level_multiplier(self):
        self.ok(self.req(1348,id=1,data='{}'))
        r=self.b.profile();s=r['activity']['home'];s['build']['3']=8;s['pray_count']=6;s['pray_time']=NOW-86400;self.b.save(r)
        with patch('network_redirect.activity_home.secrets.randbelow',return_value=0):
            self.ok(self.req(1348,id=11,data='{}'))
        self.assertEqual(sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type']==5 and i['type_id']==5001),15)

    def test_abyss_zero_serial_poll_does_not_break_mutation_replay(self):
        r=self.b.profile();r['level']=80;self.b.save(r)
        self.ok(self.req(1329,id=1,data='{}'));serial=self.b.last_activity_serial
        poll=encode(1329,dict(serial_num=0,id=15,data='{}'))
        out=[decode(p) for p in self.b.respond(poll,self.state)]
        self.assertEqual([d['id'] for m,_,d in out if m==2998],[173])
        self.assertNotIn(1106,[m for m,_,d in out]);self.assertEqual(self.b.last_activity_serial,serial)
        bad=[decode(p) for p in self.b.respond(encode(1329,dict(serial_num=0,id=6,data='{}')),self.state)]
        self.assertEqual(bad[0][2]['id'],55)
        self.ok(self.req(1329,id=6,data='{}'))

if __name__=='__main__':unittest.main()

class LandTests(ActivityCase):
    def land(self,op,**data):return self.req(1302,id=op,data=summon.lua(data))
    def test_travel_fight_restart_and_forged_target(self):
        self.ok(self.land(1));self.ok(self.land(3));before=self.b.profile()
        self.ok(self.land(3));self.assertEqual(before,self.b.profile())
        self.assertEqual(self.land(4,flag=1,des_type=1,des_id=999)[0][0],55);self.assertEqual(before,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        out=self.land(4,flag=1,des_type=1,des_id=942001);self.ok(out)
        d=out[-1][1];self.assertTrue(d['is_win']);self.assertEqual(d['soul_count'],100)
        replay=d['final_result_list'][1];self.assertEqual(replay['fight_result_msg']['fight_type'],21)
        for row in replay['line_up_msg']['lineup'].values():
            for key in ('src_hp','src_max_hp','des_hp','des_max_hp'):self.assertIn(key,row)
        self.assertEqual(self.land(4,flag=1,des_type=1,des_id=942001)[0][0],55)
        s=self.b.profile()['activity']['land'];self.assertEqual(s['soul_count'],100);self.assertEqual(s['travel_count'],1)
    def test_charm_unlock_equip_unequip_and_atomic_compose(self):
        self.ok(self.land(1))
        charm_query=self.land(6)[-1][1]
        self.assertEqual(len(charm_query['charm_show']),44)
        self.assertEqual(charm_query['charm_show'][1],dict(unlock=True,is_open=False,key=0,value=0))
        r=self.b.profile();s=r['activity']['land'];s['soul_count']=10000;s['bag']={'1':{'5':4}};self.b.save(r)
        self.ok(self.land(7,index=1,is_unlock=False));self.ok(self.land(8,index=1,key=1,value=5))
        self.assertEqual(self.b.profile()['activity']['land']['bag']['1']['5'],3)
        self.ok(self.land(8,index=1,key=0,value=0));self.assertEqual(self.b.profile()['activity']['land']['bag']['1']['5'],4)
        row=dict(key=1,value=5)
        with patch('network_redirect.activity_land_boss.secrets.randbelow',side_effect=[0,99]):
            self.ok(self.land(19,charm_info=[row]*4))
        self.assertEqual(self.b.profile()['activity']['land']['bag']['1']['10'],1)
        before=self.b.profile();self.assertEqual(self.land(19,charm_info=[row]*4)[0][0],55);self.assertEqual(before,self.b.profile())
        self.ok(self.land(20,charm_info=[dict(key=1,value=10),dict(key=2,value=10)]))
        self.assertEqual(self.b.profile()['activity']['land']['bag']['2']['10'],1)
    def test_boss_cards_no_duplicate_advance_and_sweep(self):
        self.ok(self.land(1));r=self.b.profile();r['activity']['land']['soul_count']=10000;self.b.save(r)
        self.ok(self.land(12));self.ok(self.land(4,flag=1,des_type=3,des_id=1,cur_num=1))
        pending=self.b.profile()['activity']['land']['boss'];self.assertIsNotNone(pending)
        self.assertEqual(self.land(4,flag=1,des_type=3,des_id=1,cur_num=1)[0][0],55)
        # A card can itself award gold; verify the fee after including that gain.
        gold=lambda spec:spec[2] if spec[0]==11 else 0
        before=self.b.profile()['gold_coin'];self.ok(self.land(14,index=1))
        self.assertEqual(before+gold(pending['rewards'][0]),self.b.profile()['gold_coin'])
        self.assertEqual(self.land(14,index=1)[0][0],55)
        self.ok(self.land(14,index=2))
        self.assertEqual(self.b.profile()['gold_coin'],before-20+sum(gold(p) for p in pending['rewards'][:2]))
        for i in (3,4):self.ok(self.land(14,index=i))
        last=self.land(14,index=5);self.ok(last);self.assertEqual(last[-1][1]['extra_prize_list'][1]['attach_count'],20)
        self.assertEqual(self.land(14,index=5)[0][0],55)
        self.ok(self.land(15));self.assertEqual(self.b.profile()['activity']['land']['boss_layer'],1)
        self.assertEqual(self.land(15)[0][0],55)
        repeat=self.land(4,flag=1,des_type=3,des_id=1,cur_num=1);self.ok(repeat)
        self.assertFalse(repeat[-1][1]['is_reward']);self.assertIsNone(self.b.profile()['activity']['land']['boss'])
        self.ok(self.land(13));self.assertEqual(self.land(13)[0][0],55)
        self.assertTrue(self.land(24)[-1][1]['data']['boss_info']['is_open'])
        self.ok(self.land(4,flag=1,des_type=4,des_id=1,cur_num=1));self.ok(self.land(25))
        self.assertEqual(self.b.profile()['activity']['land']['inv_boss_layer'],1)
    def test_tower_capture_ticks_no_double_and_leave(self):
        when=NOW+8*3600
        with patch('network_redirect.backend.time.time',return_value=when):
            self.ok(self.land(1));self.ok(self.req(1303,id=1,op_type=1,data='{}'))
            self.ok(self.land(11,tower_id=11));self.ok(self.land(4,flag=1,des_type=2,des_id=11))
            self.assertEqual(self.b.profile()['activity']['land']['tower_id'],11)
        with patch('network_redirect.backend.time.time',return_value=when+600):
            self.ok(self.land(1));self.assertEqual(self.b.profile()['activity']['land']['soul_count'],100)
            self.ok(self.land(1));self.assertEqual(self.b.profile()['activity']['land']['soul_count'],100)
            self.ok(self.land(5,tower_id=11));self.assertEqual(self.b.profile()['activity']['land']['tower_id'],0)
    def test_map_grid_gates_and_daily_travel_cap(self):
        self.ok(self.land(1));self.assertEqual(self.land(2,des_level=2)[0][0],55)
        self.assertEqual(self.land(9,grid_count=3)[0][0],55)
        self.ok(self.land(22));self.assertEqual(self.b.profile()['activity']['land']['travel_count'],5)
        r=self.b.profile();s=r['activity']['land'];s.update(boss_layer=16,soul_count=10000,travel_count=30);self.b.save(r)
        self.ok(self.land(2,des_level=2));self.ok(self.land(9,grid_count=3))
        self.assertEqual(self.land(3)[0][0],55)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.ok(self.land(3))

    def test_public_tower_auto_and_cross_day_income(self):
        when=NOW+11*3600+50*60
        with patch('network_redirect.backend.time.time',return_value=when):
            self.ok(self.land(1));self.ok(self.land(21,auto_tower=1))
            self.assertEqual(self.b.profile()['activity']['land']['tower_id'],14)
            self.ok(self.land(21,auto_tower=0))
        with patch('network_redirect.backend.time.time',return_value=when+1200):
            self.ok(self.land(1));s=self.b.profile()['activity']['land']
            self.assertEqual(s['soul_count'],100);self.assertEqual(s['tower_id'],0)

    def test_large_land_replay_stays_encodable(self):
        from network_redirect import activity_land as land
        r=self.b.profile();s=land.state(r,NOW,self.b.activity_rules)
        from network_redirect import journey
        unit=dict(type=1001,order=1,level=1,evolve=0,reborn=0,hp=100000000,max_hp=100000000,magic=1,gongji=1,fangyu=1,skills=[])
        with patch.object(journey,'fighters',return_value=([unit],[copy.deepcopy(unit)])):
            result,replay=land.simulate(r,s,self.b.activity_rules,self.b.journey_rules,1)
        # Two main actions per complete round; no legacy 80-action cutoff.
        self.assertEqual(len(replay['fight_result_msg']['fight_result']),60)
        self.assertEqual(replay['fight_result_msg']['fight_result'][-1]['cur_round'],30)
        packet=land.response(4,s,self.b.activity_rules,final_result_list=[replay])
        self.assertLess(len(packet),32768)

class AbyssExtraTests(ActivityCase):
    def simulate(self,effects,ours=None,enemy=None,limit=6):
        from network_redirect import activity_abyss_combat as c
        def unit():return dict(type=1001,order=1,level=1,evolve=0,reborn=0,hp=1000,max_hp=1000,gongji=100,fangyu=0,magic=0,skills=[])
        left,right=unit(),unit();left.update(ours or {});right.update(enemy or {})
        return c.battle({},([left],[right]),self.b.journey_rules,effects,limit)
    def test_extra_damage_armor_block_magic_and_strong(self):
        self.assertEqual(self.simulate({10106:90})[2][0]['damage_list'][0],10)
        self.assertEqual(self.simulate({10111:30})[2][1]['damage_list'][0],130)
        self.assertEqual(self.simulate({10102:50},ours={'fangyu':100})[2][1]['damage_list'][0],50)
        self.assertEqual(self.simulate({10113:50})[1][0]['des_max_hp'],1500)
        with patch('network_redirect.activity_abyss_combat.secrets.randbelow',return_value=0):
            plain=self.simulate({},ours={'skills':[(101,1)]})[2][0]['damage_list'][0]
            reduced=self.simulate({10108:50},ours={'skills':[(101,1)]})[2][0]['damage_list'][0]
        self.assertEqual(reduced,plain//2)
    def test_extra_counter_combo_execute_and_fury(self):
        actions=self.simulate({10103:50})[2];self.assertFalse(actions[1]['is_src']);self.assertEqual(actions[1]['damage_list'][0],50)
        actions=self.simulate({10107:50})[2];self.assertFalse(actions[2]['is_src']);self.assertEqual(actions[2]['damage_list'][0],50)
        actions=self.simulate({10115:95})[2];self.assertFalse(actions[2]['is_src']);self.assertEqual(actions[2]['damage_list'][0],100)
        actions=self.simulate({10112:20})[2]
        hit=next(x for x in actions if x['cur_round']==2 and not x['is_src']);self.assertEqual(hit['damage_list'][0],120)
    def test_extra_healing_and_one_revive_emit_original_events(self):
        for effect,logic,expected in ((10105,101051,10),(10110,101101,100)):
            result,lineup,actions,events=self.simulate({effect:10})
            event=next(x for x in events if x['logic_type']==logic)
            self.assertEqual(event['skill_result_list'][0]['field_plus'],expected)
            self.assertEqual(event['who_use'],2);self.assertTrue(event['self_use'])
            self.assertLessEqual(event['cur_action'],len(actions))
        result,lineup,actions,events=self.simulate({10119:50},enemy={'hp':50,'max_hp':50})
        revives=[e for e in events if e['logic_type']==101191]
        self.assertEqual(len(revives),1);self.assertEqual(revives[0]['cur_action'],1)
        self.assertEqual(revives[0]['skill_result_list'][0]['field_plus'],25)
        self.assertTrue(1<=result<=3)
    def test_extra_slot_original_drugs_and_no_effect_rollback(self):
        from network_redirect import activity_abyss as ab,activity_abyss_combat as c
        r=self.b.profile();r['level']=99;s=ab.state(r,NOW,self.b.activity_rules);s['boss']=46
        summon.add_item(r,1597,3);self.b.save(r)
        self.ok(self.req(1329,id=17,data='{index=5,type_id=1597}'))
        r=self.b.profile();s=r['activity']['abyss'];self.assertEqual(c.effects(ab.BOSSES[46],s['pills'])[10115],0)
        before=copy.deepcopy(r)
        self.assertEqual(self.req(1329,id=17,data='{index=6,type_id=1597}')[0][0],55);self.assertEqual(before,self.b.profile())
        self.assertEqual(self.req(1329,id=17,data='{index=1,type_id=1597}')[0][0],55)
        self.ok(self.req(1329,id=16,data='{}'))
        payload=next(d for e,d in self.req(1329,id=16,data='{}') if e==173)
        self.assertEqual(payload['specter_info']['cur_layer'],46)

class SeasonalTests(ActivityCase):
    def item(self,tid):return next(i for i in self.b.profile()['attachments'] if i['attach_type']==5 and i['type_id']==tid)
    def count(self,tid):return sum(i['count'] for i in self.b.profile()['attachments'] if i['attach_type']==5 and i['type_id']==tid)
    def test_starter_supplies_once_recipe_and_food(self):
        self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1208),60);self.assertEqual(self.count(1134),60)
        before=self.b.profile();self.ok(self.req(1205,flag=0));self.assertEqual(before,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1208),60)
        ids=[dict(id=self.item(t)['id']) for t in (1208,1209)]
        events=self.req(1126,compose_type=1,material_count=2,material_list=ids);self.ok(events)
        self.assertEqual(events[-1][1]['result'],0);self.assertEqual(self.count(1208),45);self.assertEqual(self.count(1213),1)
        before=self.b.profile();self.assertEqual(self.req(1126,compose_type=1,material_count=2,material_list=ids)[0][0],55);self.assertEqual(before,self.b.profile())
        item=self.item(1213);old=self.count(1022)
        with patch('network_redirect.activity_rice.randbelow',return_value=0):
            self.ok(self.req(1051,item_type=1213,item_id=item['id'],item_count=1,des_type=1,des_id=0))
        self.assertEqual(self.count(1022),old+2);self.assertEqual(self.count(1213),0)
        self.assertEqual(self.req(1051,item_type=1213,item_id=item['id'],item_count=1,des_type=1,des_id=0)[0][0],55)
    def test_moon_news_bonus_and_source_validation(self):
        self.ok(self.req(1205,flag=0));self.ok(self.req(1333,flag=0,src_type=0))
        r=self.b.profile();summon.add_item(r,1134,1000);summon.add_item(r,1135,1000);self.b.save(r)
        for _ in range(10):self.ok(self.req(1333,flag=1,src_type=1135))
        self.assertEqual(self.count(1130),10)
        self.assertEqual(self.b.profile()['activity']['seasonal']['moon_count'],10)
        news=self.req(1333,flag=0,src_type=0)[-1][1];self.assertEqual(news['left_process'],10);self.assertIsInstance(news['broad_list'][1],str)
        before=self.b.profile();self.assertEqual(self.req(1333,flag=1,src_type=9999)[0][0],55);self.assertEqual(before,self.b.profile())
    def test_closed_season_and_independent_random_materials(self):
        from network_redirect.activity_seasonal import travel_drop
        r=self.b.profile();a=self.b.activity_rules
        with patch('network_redirect.activity_tangwang.randbelow',return_value=99), patch('network_redirect.activity_moon.randbelow',side_effect=[0,10,0,0,0]*4), patch('network_redirect.activity_rice.randbelow',side_effect=[0,0,0,10,0]*4):
            for _ in range(4):self.assertEqual(len(travel_drop(r,NOW,a)),4)
        self.assertEqual(r['activity']['seasonal']['travel_wins'],4)
        self.assertEqual(sum(i['count'] for i in r['attachments'] if i['type_id']==1208),8)

        for cfg in a['seasonal_games'].values():cfg['enabled']=False
        self.assertEqual(travel_drop(r,NOW,a),[])
        self.assertEqual(self.req(1333,flag=0,src_type=0)[0][0],55)
        self.ok(self.req(1205,flag=0));self.assertEqual(self.count(1208),0)

class SpringTests(ActivityCase):
    def test_daily_worship_exchange_and_rollover(self):
        self.ok(self.req(1205,flag=0));self.ok(self.req(1210,flag=1));before=self.b.profile()
        self.assertEqual(self.req(1210,flag=1)[0][0],55);self.assertEqual(before,self.b.profile())
        row=self.b.profile()['activity']['seasonal']['spring']['shop'][0]
        from network_redirect.activity_caishen import offer_id
        ident=offer_id(self.b.profile()['activity']['seasonal']['spring'],row,self.b.activity_rules)
        gain=self.req(1211,prize_id=ident,count=1);self.ok(gain)
        self.assertEqual(next(d for e,d in gain if e==87)['attach_count'],row['reward'][2])
        before=self.b.profile();self.assertEqual(self.req(1211,prize_id=ident,count=1)[0][0],55);self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):self.ok(self.req(1210,flag=1))
        self.assertEqual(self.b.profile()['activity']['seasonal']['spring']['purchases'],{})
    def test_card_combinations_duplicate_and_inventory(self):
        from network_redirect.activity_tangwang import COMBINATIONS, card
        self.ok(self.req(1205,flag=0))
        count=lambda:sum(c['count'] for c in self.b.profile()['attachments'] if c['type_id']==1094)
        self.assertEqual(count(),4);self.ok(self.req(1205,flag=0));self.assertEqual(count(),4)
        for recipe in COMBINATIONS:
            role=self.b.profile();chosen=[card(role,level)['id'] for level in recipe];self.b.save(role)
            before=self.b.profile();self.assertEqual(self.req(1213,count=4,card_list=[dict(id=chosen[0])]*4)[0][0],55);self.assertEqual(before,self.b.profile())
            self.ok(self.req(1213,count=4,card_list=[dict(id=i) for i in chosen]))
            self.assertEqual(self.req(1213,count=4,card_list=[dict(id=i) for i in chosen])[0][0],55)
        self.assertEqual(count(),4)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.ok(self.req(1205,flag=0));self.assertEqual(count(),4)
