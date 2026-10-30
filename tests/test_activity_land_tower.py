"""Native portrait requests and the 64 distinct tower encounters."""
import copy
import random
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_land as land, activity_land_encounters as encounters
from network_redirect import activity_land_boss as boss, activity_land_npc as npc, formation, summon, journey
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import MAX_PACKET, decode
from pathlib import Path


class LandTowerTests(ActivityCase):
    def land(self,op,**d):return self.req(1302,id=op,data=summon.lua(d))

    def test_tower_growth_starts_at_the_tuned_level_and_increases_per_floor(self):
        normal=encounters.schedule(False)
        hell=encounters.schedule(True)
        self.assertEqual(normal[0]['level'],3)
        self.assertEqual(hell[0]['level'],4)
        self.assertEqual(normal[0]['power'],1538)
        self.assertGreater(hell[0]['power'],normal[0]['power'])
        self.assertGreater(normal[-1]['power'],normal[0]['power']*200)
        self.assertGreater(hell[-1]['power'],hell[0]['power']*300)
        # Every floor now advances by the configured level step, so template
        # growth is visible in addition to the monotonic carry-forward guard.
        self.assertEqual(normal[1]['level']-normal[0]['level'],6)
        self.assertEqual(hell[1]['level']-hell[0]['level'],8)
        self.assertEqual(normal[-1]['level'],381)
        self.assertEqual(hell[-1]['level'],508)
        self.assertGreater(normal[-1]['power'],198892*2)
        self.assertGreater(hell[-1]['power'],261038*2)
        for rows in (normal,hell):
            for previous,current in zip(rows,rows[1:]):
                for stat in formation.STATS:
                    self.assertGreaterEqual(current['units'][0][stat]*100,
                                            previous['units'][0][stat]*103)

    def test_power_multiplier_scales_actual_units_once_on_all_floors(self):
        configured=copy.deepcopy(encounters.rules())
        boosted=[copy.deepcopy(encounters.schedule(hell)) for hell in (False,True)]
        baseline=dict(configured,normal_stat_multiplier=1,hell_stat_multiplier=1)
        try:
            with patch.object(encounters,'rules',return_value=baseline):
                encounters.schedule.cache_clear()
                old=[copy.deepcopy(encounters.schedule(hell)) for hell in (False,True)]
        finally:
            encounters.schedule.cache_clear()
        self.assertEqual((old[0][0]['power'],old[1][0]['power']),(769,817))
        self.assertEqual((old[0][-1]['power'],old[1][-1]['power']),(476370,629284))
        for mode,multiplier in enumerate((2,4)):
            for before,after in zip(old[mode],boosted[mode]):
                self.assertEqual(before['level'],after['level'])
                self.assertEqual(len(before['units']),len(after['units']))
                # Display power rounds each unit; the small remainder is expected.
                self.assertLessEqual(abs(after['power']-before['power']*multiplier),
                                     len(after['units'])*multiplier)
                for a,b in zip(before['units'],after['units']):
                    self.assertEqual(a['skills'],b['skills'])
                    for stat in formation.STATS:self.assertEqual(b[stat],a[stat]*multiplier)
                    self.assertEqual(b['max_hp'],b['hp'])

    def test_card_pool_has_all_eight_requested_reward_tiers(self):
        self.assertEqual(self.b.activity_rules['land_card_rewards'],[
            [12,0,10000,1],[12,0,30000,1],[11,0,20,1],
            [5,1001,1,1],[5,1001,3,1],[5,10000,5,1],
            [5,10000,10,1],[5,10001,1,1]])

    def test_new_cards_are_unique_shuffled_and_persist_until_claimed(self):
        self.ok(self.land(1))
        pool=self.b.activity_rules['land_card_rewards']
        boards=[]
        for hell in (False,True):
            key='hell' if hell else 'boss'; count=3 if hell else 5
            query,flip,advance=(24,23,25) if hell else (12,14,15)
            role=self.b.profile();s=role['activity']['land']
            s.update(soul_count=10000,unlocked=[1]);self.b.save(role)
            # Fix only the draw RNG; victory still uses the actual battle engine.
            with patch.object(boss.secrets,'SystemRandom',return_value=random.Random(30 if hell else 41)):
                out=self.land(4,flag=1,des_type=4 if hell else 3,des_id=1,cur_num=1)
            self.ok(out);self.assertTrue(out[-1][1]['is_win'])
            pending=self.b.profile()['activity']['land'][key]
            chosen=pending['rewards'];boards.append(chosen)
            self.assertEqual(len(chosen),count)
            self.assertEqual(len({tuple(p) for p in chosen}),count)
            self.assertTrue(all(p in pool for p in chosen))
            self.assertNotEqual(chosen,sorted(chosen,key=pool.index))
            self.ok(self.land(query))
            self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
            self.ok(self.land(query))
            self.assertEqual(self.b.profile()['activity']['land'][key],pending)
            for index in range(count,0,-1):
                before=self.b.profile()
                result=self.land(flip,index=index);self.ok(result)
                self.assertEqual(result[-1][1]['attach_data'],activity.prize_spec(chosen[index-1]))
                extras=self.b.activity_rules['land_full_card_rewards'] if index==1 else []
                self.assertEqual(result[-1][1]['extra_prize_list'],
                    {i:activity.prize_spec(p) for i,p in enumerate(extras,1)} if extras else {})
                rewards=[chosen[index-1]]+extras
                current=self.b.profile()
                cost=self.b.activity_rules['land_card_gold'][count-index]
                for typ,field in ((11,'gold_coin'),(12,'silver_coin')):
                    gain=sum(p[2] for p in rewards if p[0]==typ)
                    self.assertEqual(current[field]-before[field],gain-(cost if typ==11 else 0))
                for tid in (1001,10000,10001):
                    inventory=lambda r:sum(p['count'] for p in r['attachments'] if p['attach_type']==5 and p['type_id']==tid)
                    self.assertEqual(inventory(current)-inventory(before),sum(p[2] for p in rewards if p[:2]==[5,tid]))
                self.assertEqual(self.land(flip,index=index)[0][0],55)
                self.assertEqual(self.b.profile(),current)
            before=self.b.profile()
            self.assertEqual(self.land(flip,index=count+1)[0][0],55)
            self.assertEqual(self.b.profile(),before)
            self.ok(self.land(advance))
            # Clearing an old floor again must not produce another reward board.
            self.ok(self.land(4,flag=1,des_type=4 if hell else 3,des_id=1,cur_num=1))
            self.assertIsNone(self.b.profile()['activity']['land'][key])
        self.assertNotEqual(boards[0][:3],boards[1])
        self.assertEqual({tuple(p) for board in boards for p in board},{tuple(p) for p in pool})

    def test_sweep_keeps_its_peaches_after_card_pool_change(self):
        self.ok(self.land(1));role=self.b.profile()
        role['activity']['land']['boss_layer']=3;self.b.save(role)
        result=self.land(13);self.ok(result)
        self.assertEqual(result[-1][1]['sweep_list'],
                         {i:{1:activity.prize_spec([5,1001,10,1])} for i in range(1,4)})

    def test_legacy_three_card_hell_board_remains_claimable(self):
        self.ok(self.land(1));role=self.b.profile();s=role['activity']['land']
        s['hell']=dict(layer=1,cards=[],rewards=[[5,1343,1,1]]*3)
        self.b.save(role)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.ok(self.land(24))
        for index in (3,1,2):
            result=self.land(23,index=index);self.ok(result)
            self.assertEqual(result[-1][1]['attach_data'],activity.prize_spec([5,1343,1,1]))
        self.ok(self.land(25))
        self.assertEqual(self.b.profile()['activity']['land']['inv_boss_layer'],1)

    def test_tower_detail_preserves_tower_id_for_attack_request(self):
        when=NOW+8*3600
        with patch('network_redirect.backend.time.time',return_value=when):
            self.ok(self.land(1))
            detail=self.land(11,tower_id=14)[-1][1]['tower_info']
            self.assertEqual(detail['tower_id'],14)
            # The native client copies towerInfo.tower_id into the following
            # prey_fight request.  This must remain a valid tower after the
            # query/detail round trip.
            self.ok(self.land(4,flag=1,des_type=2,des_id=detail['tower_id']))

    def test_each_unlocked_map_rebuilds_its_own_towers_and_travel(self):
        self.ok(self.land(1))
        role=self.b.profile();s=role['activity']['land']
        s.update(boss_layer=48,soul_count=10000)
        self.b.save(role)
        for level in (2,3,4):
            self.ok(self.land(2,des_level=level))
            current=self.b.profile()['activity']['land']
            self.assertEqual(set(current['towers']),{str(level*10+i) for i in range(1,5)})
            self.ok(self.land(3));self.assertLessEqual(len(self.b.profile()['activity']['land']['travel']),4)
            self.ok(self.land(17))

    def test_inverse_tower_migrates_legacy_progress_and_clamps_daily_count(self):
        self.ok(self.land(1))
        role=self.b.profile();s=role['activity']['land']
        s.update(boss_layer=0,inv_boss_layer=2,soul_count=10000,
                 inv_history={'1':dict(score=3000,cur_num=1),
                              '2':dict(score=3000,cur_num=1)},
                 hell_counts={'1':99})
        s.pop('unlocked',None)
        self.b.save(role)
        out=self.land(24);self.ok(out)
        data=out[-1][1]['data']
        self.assertEqual(data['boss_info']['boss_layer'],3)
        self.assertFalse(data['boss_info']['is_open'])
        self.assertEqual(data['boss_info']['can_fight_count'],3)
        self.assertTrue(data['history'][1]['is_open'])
        self.assertTrue(data['history'][2]['is_open'])
        self.assertEqual(self.b.profile()['activity']['land']['unlocked'],[1,2])
        # A legacy per-layer counter above the configured daily limit is
        # exposed as zero and cannot be bypassed by submitting a fight.
        self.assertEqual(self.land(4,flag=1,des_type=4,des_id=1,cur_num=1)[0][0],55)

    def test_inverse_tower_native_unlock_button_and_paid_early_entry(self):
        self.ok(self.land(1));role=self.b.profile()
        role['activity']['land']['soul_count']=1000;self.b.save(role)
        row=self.land(24)[-1][1]['data']['boss_info']
        self.assertFalse(row['is_open'])
        self.assertTrue(row['unlock'])  # Native landUI L2410 selects the unlock button.
        self.assertEqual(row['unlock_layer'],1)
        before=self.b.profile()
        self.assertEqual(self.land(4,flag=1,des_type=4,des_id=1,cur_num=1)[0][0],55)
        self.assertEqual(self.b.profile(),before)
        self.ok(self.land(26,index=row['boss_layer']))
        current=self.b.profile()
        self.assertEqual(current['activity']['land']['soul_count'],1000-row['unlock_soul'])
        self.assertTrue(self.land(24)[-1][1]['data']['boss_info']['is_open'])
        self.assertEqual(self.land(26,index=1)[0][0],55)
        self.assertEqual(self.b.profile(),current)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertTrue(self.land(24)[-1][1]['data']['boss_info']['is_open'])
        result=self.land(4,flag=1,des_type=4,des_id=1,cur_num=1)
        self.ok(result);self.assertTrue(result[-1][1]['is_win'])
        self.ok(self.land(25))
        row=self.land(24)[-1][1]['data']['boss_info']
        self.assertEqual(row['boss_layer'],2)
        self.assertFalse(row['is_open']);self.assertTrue(row['unlock'])

    def test_inverse_tower_unlock_rejects_invalid_layers_and_insufficient_soul(self):
        self.ok(self.land(24));role=self.b.profile()
        role['activity']['land']['soul_count']=1000;self.b.save(role)
        before=self.b.profile()
        for index in (0,-1,2,65,True,1.5,'1'):
            self.assertEqual(self.land(26,index=index)[0][0],55)
            self.assertEqual(self.b.profile(),before)
        before['activity']['land']['soul_count']=0;self.b.save(before)
        self.assertEqual(self.land(26,index=1)[0][0],55)
        self.assertEqual(self.b.profile(),before)

    def test_normal_tower_settlement_automatically_opens_inverse_without_charge(self):
        self.ok(self.land(1));role=self.b.profile()
        role['activity']['land']['soul_count']=1000;self.b.save(role)
        result=self.land(4,flag=1,des_type=3,des_id=1,cur_num=1)
        self.ok(result);self.assertTrue(result[-1][1]['is_win'])
        self.assertFalse(self.land(24)[-1][1]['data']['boss_info']['is_open'])
        self.ok(self.land(14,index=1))
        before=self.b.profile()['activity']['land']['soul_count']
        self.ok(self.land(15))
        row=self.land(24)[-1][1]['data']['boss_info']
        self.assertTrue(row['is_open'])
        self.assertEqual(self.b.profile()['activity']['land']['soul_count'],before)
        result=self.land(4,flag=1,des_type=4,des_id=1,cur_num=1)
        self.ok(result);self.assertTrue(result[-1][1]['is_win'])

    def test_inverse_tower_old_normal_progress_unlocks_on_query_and_restart(self):
        self.ok(self.land(1));original=self.b.profile()
        for progress in (0,1,16,32,64):
            with self.subTest(progress=progress):
                role=copy.deepcopy(original);s=role['activity']['land']
                s.update(boss_layer=progress,inv_boss_layer=max(0,progress-1),soul_count=0)
                s.pop('unlocked',None);self.b.save(role)
                row=self.land(24)[-1][1]['data']['boss_info']
                self.assertEqual(row['is_open'],progress>0)
                saved=self.b.profile()['activity']['land']
                self.assertEqual(saved['unlocked'],list(range(1,progress+1)))
                self.assertEqual(saved['soul_count'],0)
                self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
                self.ok(self.land(24))
                self.assertEqual(self.b.profile()['activity']['land'],saved)

    def test_hell_64_shield_events_do_not_truncate_winning_battle(self):
        self.ok(self.land(1));r=self.b.profile();identity=r['role_id']
        r.update(copy.deepcopy(npc.catalog()['npc_v1_l99_t2_attack']['role']))
        r['role_id']=identity
        r['activity']['land'].update(boss_layer=64,inv_boss_layer=63,grid_count=8,
                                    soul_count=10000,unlocked=[64],
                                    charms={str(i):dict(key=(i-1)%4+1,value=30,unlock=True,is_open=True)
                                            for i in land.CHARMS})
        real_battle=journey.battle
        for seed in (1,3,7):
            with self.subTest(seed=seed):
                self.b.save(copy.deepcopy(r));captured=[]
                def battle(*args,**kwargs):
                    result=real_battle(*args,**kwargs);captured.append(result[2]);return result
                # Reproduce the shield proc sequences that exhausted the old
                # 1000-byte budget. Damage, victory and wire encoding stay real.
                with patch('network_redirect.combat.secrets.randbelow',side_effect=random.Random(seed).randrange), \
                     patch.object(journey,'battle',side_effect=battle):
                    out=self.land(4,flag=1,des_type=4,des_id=64,cur_num=8)
                self.ok(out);self.assertTrue(out[-1][1]['is_win'])
                actions=captured[0]
                self.assertEqual(actions.stop_reason,'elimination')
                self.assertFalse(any(actions.final_hp[2].values()))
                replay=out[-1][1]['final_result_list'][1]
                self.assertGreater(len(summon.lua(replay['fight_events']).encode('utf-8')),1000)
                self.assertEqual(out[-2][1],replay['fight_events'])
                self.assertEqual(len(actions),replay['fight_result_msg']['fight_round'])
                self.ok(self.land(23,index=1));self.ok(self.land(25))
                self.assertEqual(self.b.profile()['activity']['land']['inv_boss_layer'],64)

    def test_thirty_round_hp_results_preserve_complete_replay(self):
        self.ok(self.land(1));r=self.b.profile();s=r['activity']['land'];s['grid_count']=8
        enemy=encounters.encounter(64,True)
        # Durable armies reach the shared thirty-round limit. Effect volume must
        # never impose a shorter battle or lose the tail of the replay.
        for u in enemy['units']:
            u.update(hp=1000000,max_hp=1000000,gongji=100,fangyu=10,magic=100,skills=[])
        r['corteges']=[dict(u,id=u['order']) for u in enemy['units']];r['attachments']=[]
        real_battle=journey.battle
        for effects in (False,True):
            with self.subTest(effects=effects):
                enemy['units'][0]['skills']=[(21,1)] if effects else []
                captured=[]
                def battle(*args,**kwargs):
                    result=real_battle(*args,**kwargs);captured.append(result[2]);return result
                with patch('network_redirect.combat.secrets.randbelow',return_value=0), \
                     patch.object(journey,'battle',side_effect=battle):
                    result,replay=land.simulate(r,s,self.b.activity_rules,self.b.journey_rules,
                                              192,8,8,encounter=enemy)
                actions=captured[0]
                self.assertEqual(actions.stop_reason,'round_limit')
                self.assertEqual(actions.rounds,30)
                hp=[sum(actions.final_hp[side].values()) for side in (1,2)]
                self.assertEqual(result==0,hp[0]==hp[1])
                self.assertEqual(1<=result<=3,hp[0]>hp[1])
                if effects:self.assertGreaterEqual(len(summon.lua(replay['fight_events']).encode('utf-8')),4000)
                packets=land.replay_response(4,s,self.b.activity_rules,replay,fight_type=4,des_level=64,
                    is_win=False,is_reward=False,return_soul=0,card_list=[],
                    cost_gold_list=self.b.activity_rules['land_card_gold'])
                from tests.test_battle_replay import decoded_packets
                self.assertTrue(all(len(packet)<=MAX_PACKET for packet in packets))
                restored=decoded_packets(packets)
                self.assertEqual(restored[-1][2]['id'],149)
                self.assertEqual(login_fields(restored[-1][2]['data'])['final_result_list'][1],
                                 login_fields(summon.lua(replay)))

    def test_native_portrait_index_and_inspection_id(self):
        self.ok(self.land(3));s=self.b.profile()['activity']['land']
        # Native sendChallengeRequest forwards the menu tag, not enemy.id.
        target=s['travel'][1]
        out=self.land(3);wire=out[-1][1]['enemy_list'][2]
        self.assertEqual(wire['role_id'],target['id'])
        self.ok(self.req(1039,des_id=wire['role_id'],des_type=1,flag=10,fight_id=0))
        with patch.object(land,'simulate',wraps=land.simulate) as battle:
            self.ok(self.land(4,des_type=1,des_id=2,flag=1))
            self.assertEqual(battle.call_args.kwargs['target'],target['npc_id'])
        self.assertIsNone(self.b.profile()['activity']['land']['travel'])
        before=self.b.profile();self.assertEqual(self.land(4,des_type=1,des_id=2,flag=1)[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_legacy_pending_encounter_after_restart_and_invalid_indices(self):
        self.ok(self.land(3));r=self.b.profile()
        for row in r['activity']['land']['travel']:row.pop('role_id',None)
        self.b.save(r);self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        wire=self.land(3)[-1][1]['enemy_list'][1]
        self.assertEqual(wire['role_id'],wire['id'])
        before=self.b.profile()
        for ident in (0,-1,9,True,1.5,999999):
            self.assertEqual(self.land(4,des_type=1,des_id=ident,flag=1)[0][0],55)
            self.assertEqual(before,self.b.profile())
        self.ok(self.land(4,des_type=1,des_id=wire['id'],flag=1))

    def test_unique_chiefs_monotonic_stats_power_and_original_skills(self):
        normal=encounters.schedule(False);hell=encounters.schedule(True)
        for rows in (normal,hell):
            self.assertEqual(len({e['type_id'] for e in rows}),64)
            self.assertEqual(len({e['name'] for e in rows}),64)
            for i,e in enumerate(rows):
                self.assertEqual(len(e['units']),min(8,1+i//8))
                self.assertEqual(e['units'][0]['type'],e['type_id'])
                self.assertEqual(len({u['type'] for u in e['units']}),len(e['units']))
                for u in e['units']:
                    self.assertEqual(u['skills'],[(int(formation.BASES[u['type']]['chushijineng']),1)])
                if i:
                    self.assertGreater(e['power'],rows[i-1]['power'])
                    for stat in formation.STATS:self.assertGreater(e['units'][0][stat],rows[i-1]['units'][0][stat])
        for a,b in zip(normal,hell):
            self.assertGreater(b['power'],a['power'])
            self.assertEqual(a['type_id'],b['type_id'])

    def test_late_map_never_generates_invisible_portraits(self):
        self.ok(self.land(1));r=self.b.profile();s=r['activity']['land'];s['map_level']=4
        with patch('network_redirect.activity_land.secrets.choice',side_effect=lambda xs:xs[-1]):
            land.travel(s,self.b.activity_rules,r)
        self.assertEqual(len(s['travel']),4)
        # A pre-fix saved seven-person list keeps the four visible choices and
        # its paid travel count, without silently starting another round.
        s['travel']+=copy.deepcopy(s['travel'][:3]);before=s['travel_count'];self.b.save(r)
        self.assertEqual(self.land(4,des_type=1,des_id=5,flag=1)[0][0],55)
        self.ok(self.land(3));s=self.b.profile()['activity']['land']
        self.assertEqual(len(s['travel']),4);self.assertEqual(s['travel_count'],before)

    def test_query_history_and_actual_replay_share_same_encounter(self):
        self.ok(self.land(1));r=self.b.profile();s=r['activity']['land']
        s.update(boss_layer=2,soul_count=10000,history={'1':dict(score=3000,cur_num=1),'2':dict(score=3000,cur_num=1)})
        self.b.save(r)
        out=self.land(12);data=out[-1][1]['data']
        self.assertEqual(data['boss_info']['type_id'],encounters.encounter(3)['type_id'])
        self.assertEqual(data['history'][1]['type_id'],encounters.encounter(1)['type_id'])
        result=self.land(4,des_type=3,des_id=3,flag=1,cur_num=1);self.ok(result)
        replay=result[-1][1]['final_result_list'][1]['line_up_msg']
        self.assertEqual(replay['des_name'],encounters.encounter(3)['name'])
        self.assertEqual(replay['lineup'][1]['des_type'],encounters.encounter(3)['type_id'])
        self.assertEqual(replay['lineup'][1]['des_hp'],encounters.encounter(3)['units'][0]['hp'])
        self.ok(self.land(14,index=1));self.ok(self.land(15))
        self.assertEqual(self.land(12)[-1][1]['data']['boss_info']['type_id'],encounters.encounter(4)['type_id'])

    def test_encounter_cache_and_pending_cards_not_replaced_by_upgrade(self):
        baseline=copy.deepcopy(encounters.schedule())
        e=encounters.encounter(64);e['units'][0]['hp']=1
        self.assertEqual(encounters.schedule(),baseline)
        self.ok(self.land(1));r=self.b.profile();s=r['activity']['land']
        s['boss']=dict(layer=1,cards=[],rewards=copy.deepcopy(self.b.activity_rules['land_card_rewards'][:1])*5)
        self.b.save(r);before=copy.deepcopy(s['boss'])
        self.ok(self.land(12));self.assertEqual(self.b.profile()['activity']['land']['boss'],before)
        self.ok(self.land(14,index=1));self.ok(self.land(15))
        self.assertEqual(self.b.profile()['activity']['land']['boss_layer'],1)
