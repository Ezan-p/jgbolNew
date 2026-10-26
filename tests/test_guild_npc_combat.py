"""Guild combat uses immutable NPC player formations, not fixed placeholder mobs."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from network_redirect import guild, guild_combat, guild_instances, npc_players, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW=1792814400


class GuildNpcCombatTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.backend=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.addCleanup(self.backend.close)
        clock=patch('network_redirect.backend.time.time',return_value=NOW)
        clock.start();self.addCleanup(clock.stop)
        self.serial=17000
        self.backend.guild_rules.update(pet_role_level=0,pet_union_level=0,wander_daily=3,train_weekend_only=False,lucky_weekend_only=False,hunt_weekend_open=True)
        role=self.backend.profile();role.update(level=40,gold_coin=100000,silver_coin=100000)
        summon.add_item(role,1338,100)
        self.backend.save(role)

    def request(self,op,**data):
        self.serial+=1
        response=self.backend.respond(encode(1301,dict(serial_num=self.serial,id=op,data=summon.lua(data))),{'authenticated':True})
        rows=[(mid,x['id'],login_fields(x['data'])) for mid,_,x in map(decode,response) if mid in (2998,1301)]
        self.assertFalse(any(kind==55 for _,kind,_ in rows),rows)
        return sorted(rows,key=lambda row:row[0]==1301)

    def seed_residents(self):
        self.request(18,query_type=5)
        role=self.backend.profile();g=role['guild']['unions'][str(role['union_id'])]
        for key in list(g['applications'])[:4]:self.request(5,role_id=int(key))
        self.request(88)
        role=self.backend.profile();role['guild']['instances']['week_score']=30;self.backend.save(role)

    def team(self):
        self.request(4,union_id=1)
        self.request(26)
        pending=self.request(50)[-1][2]
        self.request(28,role_list=list(pending))
        return self.backend.profile()['guild']['instances']['team']['members']

    def test_real_npc_team_fields_and_joint_battle(self):
        ids=self.team()
        before=self.backend.profile()
        source={key:npc_players.get(int(key)) for key in ids if int(key)!=before['role_id']}
        self.assertEqual(len(ids),5)
        info=self.request(44)[-1][2]['team']
        for row in info['teams'].values():
            if row['id']==before['role_id']:continue
            actor=source[str(row['id'])]['role']
            first=min((c for c in actor['corteges'] if 1<=c.get('order',0)<=8),key=lambda c:c['order'])
            self.assertEqual(row['head_type'],first['type'])
        reply=self.request(41,fight_list=list(map(int,ids)))[-1][2]
        replay=reply['fight_result_list'][1]
        participants=replay['participants']
        self.assertEqual({p['role_id'] for p in participants.values()},set(map(int,ids)))
        self.assertEqual(len(participants),8)
        lineup=replay['line_up_msg']['lineup']
        for unit in participants.values():
            actor=before if unit['role_id']==before['role_id'] else source[str(unit['role_id'])]['role']
            original=next(c for c in actor['corteges'] if c.get('order')==unit['source_order'])
            self.assertEqual(lineup[unit['order']]['src_type'],original['type'])
        enemy=npc_players.get(replay['enemy_npc'])
        self.assertNotIn(enemy['role']['role_id'],map(int,ids))
        self.assertGreater(sum(bool(row.get('des_type')) for row in lineup.values()),1)
        self.assertLess(len(summon.lua(reply).encode()),32767)
        for key,snapshot in source.items():self.assertEqual(npc_players.get(int(key)),snapshot)
        saved=copy.deepcopy(self.backend.profile()['guild']['instances'])
        replayed=self.request(42)[-1][2]
        self.assertEqual(replayed['fight_result_list'],reply['fight_result_list'])
        self.assertEqual(self.backend.profile()['guild']['instances'],saved)

    def test_npc_captain_assembles_playable_party(self):
        self.request(4,union_id=1)
        listing=self.request(73)[-1][2]['team']['teams']
        captain=next(iter(listing.values()))['captain']
        self.request(27,leader_id=captain)
        team=self.backend.profile()['guild']['instances']['team']
        self.assertEqual(team['captain'],captain)
        self.assertGreaterEqual(len(team['members']),3)
        self.assertLessEqual(len(team['members']),5)
        self.request(41,fight_list=list(map(int,team['members'])))
        self.assertEqual(self.backend.profile()['guild']['instances']['team_fights'],1)

    def test_opponent_selection_stays_saved_on_failed_floor(self):
        ids=self.team();role=self.backend.profile();s=role['guild']
        actors=[role if int(key)==role['role_id'] else npc_players.get(int(key))['role'] for key in ids]
        _,_,replay=guild_combat.simulate(role,s,self.backend.guild_rules,self.backend.journey_rules,15,'仙盟秘境',ally_roles=actors)
        serial=s['random_serial'];first=copy.deepcopy(s['instances']['team_opponents'])
        _,_,second=guild_combat.simulate(role,s,self.backend.guild_rules,self.backend.journey_rules,15,'仙盟秘境',ally_roles=actors)
        self.assertEqual(first,s['instances']['team_opponents'])
        self.assertEqual(serial,s['random_serial'])
        self.assertEqual(second['enemy_npc'],replay['enemy_npc'])

    def test_selected_npc_fights_training_with_own_formation(self):
        self.request(1,union_name='试炼道友盟')
        self.seed_residents()
        self.request(18,query_type=5)
        role=self.backend.profile();g=role['guild']['unions'][str(role['union_id'])]
        target=next(m['id'] for m in g['members'].values() if m.get('npc_id'))
        self.request(81,appoint_role=target)
        self.request(80)
        a=self.backend.profile()['guild']['instances']
        replay=a['train_record'][0]
        self.assertEqual(replay['actor_role_id'],target)
        self.assertIn(str(target),a['train_damage'])
        self.assertEqual(a['train_damage'][str(target)]['name'],npc_players.get(target)['role']['role_name'])
        expected={c['order']:c['type'] for c in npc_players.get(target)['role']['corteges'] if 1<=c.get('order',0)<=8}
        actual={i:row['src_type'] for i,row in enumerate(replay['line_up_msg']['lineup'],1) if row.get('src_type')}
        self.assertEqual(actual,expected)

    def test_removed_member_is_not_retained_in_party(self):
        ids=self.team();role=self.backend.profile();s=role['guild'];g=s['unions'][str(role['union_id'])]
        target=next(key for key in ids if int(key)!=role['role_id'])
        del g['members'][target];self.backend.save(role)
        team=self.request(44)[-1][2]['team']
        self.assertNotIn(int(target),{m['id'] for m in team['teams'].values()})
        self.assertNotIn(target,self.backend.profile()['guild']['instances']['team']['members'])

    def test_catch_history_query_is_a_real_native_request(self):
        self.request(1,union_name='捕获史仙盟')
        self.seed_residents()
        empty=self.request(94)[-1][2]
        self.assertEqual(empty['catch_list'],{})
        self.request(89)
        history=self.request(94)[-1][2]['catch_list']
        self.assertEqual(len(history),1)
        self.assertEqual(history[1]['name'],self.backend.profile()['role_name'])
        self.assertEqual(self.request(94)[-1][2]['catch_list'],history)

    def test_capture_before_pet_home_does_not_push_pet_home_history(self):
        self.request(1,union_name='游历首次捕捉')
        role=self.backend.profile();summon.add_item(role,1338,1);self.backend.save(role)
        self.request(86,two_type=2)
        target=self.backend.profile()['guild']['instances']['field']['type_id']
        with patch('network_redirect.guild_offline.roll',return_value=0):
            rows=self.request(87,two_type=2,catch_type=1338)
        self.assertNotIn(94,{op for _,op,_ in rows})
        self.assertIn(93,{op for _,op,_ in rows})
        self.assertEqual(next(data for _,op,data in rows if op==87)['flag'],1)
        history=self.request(94)[-1][2]['catch_list']
        self.assertEqual(len(history),1)
        self.assertEqual(history[1]['type_id'],target)
        self.assertEqual(history[1]['name'],self.backend.profile()['role_name'])

    def test_hunt_npc_guard_and_real_player_ranking(self):
        self.request(4,union_id=1)
        main=self.request(83)[-1][2]
        self.assertEqual(main['cur_reputation'],0)
        responses=self.request(84,task_index=1,task_type=2,pay_type=1)
        replay=next(data for mid,op,data in responses if mid==1301 and op==85)['fight_result_list'][1]
        self.assertIsNotNone(npc_players.get(replay['enemy_npc']))
        ranks=self.request(92,two_type=1,query_type=2)[-1][2]['rank_data']
        for row in ranks.values():
            if row['id']==self.backend.profile()['role_id']:continue
            self.assertEqual(row['name'],npc_players.get(row['id'])['role']['role_name'])

    def test_training_stage_claim_button_and_repeat_challenge(self):
        self.request(1,union_name='分段试炼盟')
        self.seed_residents()
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[]),damage_total=100))
        with patch('network_redirect.guild_instances.simulate',return_value=fake):
            for _ in range(3):self.request(80)
        role=self.backend.profile();a=role['guild']['instances']
        self.assertEqual(a['train_hp'],9700)
        self.assertEqual(a['train_end'],NOW+self.backend.guild_rules['train_seconds'])
        a['train_hp']=7000;self.backend.save(role)
        self.assertEqual(self.request(79)[-1][2]['result'],58)
        self.request(82)
        self.assertEqual(self.request(79)[-1][2]['result'],1)
        role=self.backend.profile();role['guild']['instances']['train_end']=NOW-1;self.backend.save(role)
        self.assertEqual(self.request(79)[-1][2]['result'],53)

    def test_trial_inactive_and_expired_timers_do_not_requery_loop(self):
        self.request(1,union_name='试炼倒计时盟')
        self.seed_residents()
        unopened=self.request(79)[-1][2]
        self.assertGreater(unopened['last_time'],NOW)
        self.assertIs(unopened['rest_time'],False)
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[]),damage_total=100))
        with patch('network_redirect.guild_instances.simulate',return_value=fake):rows=self.request(80)
        self.assertNotIn(79,{op for _,op,_ in rows})
        active=self.request(79)[-1][2]
        self.assertEqual(active['rest_time'],NOW+self.backend.guild_rules['train_seconds'])
        expired=active['rest_time']+1
        with patch('network_redirect.backend.time.time',return_value=expired):
            result=self.request(79)[-1][2]
            self.assertEqual(result['result'],53)
            self.assertGreater(result['last_time'],expired)
            self.assertIs(result['rest_time'],False)
            self.assertEqual(self.backend.profile()['guild']['instances']['train_end'],active['rest_time'])

    def test_joint_slots_keep_original_owned_effects(self):
        ids=self.team();role=self.backend.profile()
        actors=[role if int(key)==role['role_id'] else npc_players.get(int(key))['role'] for key in ids]
        joint,sources,_=guild_combat.joint_units(actors)
        for unit,source in zip(joint,sources):
            owner=next(actor for actor in actors if actor['role_id']==source['role_id'])
            original=next(u for u in guild_combat.player_units(owner) if u['order']==source['source_order'])
            for field in ('type','skills','essences','reborn_traits','training_bonuses'):
                self.assertEqual(unit.get(field),original.get(field))
            self.assertLess(unit['companion_id'],0)

    def test_native_capture_picker_consumes_selected_item(self):
        self.request(1,union_name='捕捉道具盟')
        role=self.backend.profile();summon.add_item(role,1338,2);summon.add_item(role,1340,2);self.backend.save(role)
        self.request(86,two_type=2)
        before=self.backend.profile();gold=before['gold_coin']
        count=lambda r,kind:sum(x['count'] for x in r['attachments'] if x['type_id']==kind)
        self.request(87,two_type=2,catch_type=1340)
        after=self.backend.profile()
        self.assertEqual(count(after,1340),count(before,1340)-1)
        self.assertEqual(count(after,1338),count(before,1338))
        self.assertEqual(after['gold_coin'],gold)

    def test_original_weekend_and_240_resident_gate(self):
        from datetime import datetime, timezone
        friday=int(datetime(2026,10,23,4,tzinfo=timezone.utc).timestamp())
        saturday=friday+86400
        self.backend.guild_rules.update(train_weekend_only=True,lucky_weekend_only=True,hunt_weekend_open=False)
        self.request(1,union_name='原版试炼门槛')
        with patch('network_redirect.backend.time.time',return_value=friday):
            self.assertEqual(self.request(79)[-1][2]['result'],53)
            self.assertGreater(self.request(83)[-1][2]['free_task_times'],0)
        with patch('network_redirect.backend.time.time',return_value=saturday):
            self.assertEqual(self.request(79)[-1][2]['result'],41)
            self.assertEqual(self.request(83)[-1][2]['union_task'],{})
            self.seed_residents()
            role=self.backend.profile();g=role['guild']['unions'][str(role['union_id'])]
            self.assertEqual(sum(g['resident_pets'].values()),240)
            self.assertEqual(len(role['guild']['instances']['pet_entities']),0)
            self.assertEqual(self.request(79)[-1][2]['result'],61)
            self.request(80)
            before=self.backend.profile();self.request(89);after=self.backend.profile()
            self.assertEqual(sum(after['guild']['unions'][str(after['union_id'])]['resident_pets'].values()),239)
            self.assertEqual(len(after['activity']['home']['pets']),len(before.get('activity',{}).get('home',{}).get('pets',[]))+1)
            self.assertEqual(after['guild']['instances']['lucky_week_used'],1)
            self.request(88)
            self.assertEqual(sum(self.backend.profile()['guild']['unions'][str(after['union_id'])]['resident_pets'].values()),239)

    def rejected(self,op,**data):
        before=self.backend.profile();self.serial+=1
        response=self.backend.respond(encode(1301,dict(serial_num=self.serial,id=op,data=summon.lua(data))),{'authenticated':True})
        self.assertTrue(any(mid==2998 and row['id']==55 for mid,_,row in map(decode,response)))
        self.assertEqual(self.backend.profile(),before)

    def test_default_calendar_rejects_out_of_window_mutations(self):
        from datetime import datetime, timezone
        friday=int(datetime(2026,10,23,4,tzinfo=timezone.utc).timestamp())
        self.backend.guild_rules.update(train_weekend_only=True,lucky_weekend_only=True,hunt_weekend_open=False)
        with patch('network_redirect.backend.time.time',return_value=friday):
            self.request(1,union_name='周末校验盟');self.seed_residents()
            self.rejected(80);self.rejected(89);self.rejected(92,two_type=2)
            self.request(84,task_index=1,task_type=1,pay_type=1)
        with patch('network_redirect.backend.time.time',return_value=friday+86400):
            self.request(83)
            self.rejected(84,task_index=1,task_type=1,pay_type=1)

    def test_exhausted_capture_distinguishes_residence_from_escape(self):
        self.request(1,union_name='栖息捕捉盟')
        discovered=self.request(86,two_type=2)
        self.assertEqual(next(row[2] for row in discovered if row[1]==93)['update_list'],{})
        self.request(88)
        role=self.backend.profile();a=role['guild']['instances'];a['field']['tries']=1
        tid=a['field']['type_id'];self.backend.save(role)
        with patch('network_redirect.guild_offline.roll',side_effect=[99,0]):
            result=self.request(87,two_type=2)
        capture=next(row[2] for row in result if row[1]==87)
        self.assertEqual(capture['flag'],3)
        role=self.backend.profile();g=role['guild']['unions'][str(role['union_id'])]
        self.assertEqual(g['resident_pets'][str(tid)],1)
        self.assertEqual(role['guild']['instances']['pet_entities'],[])
        role['guild']['instances']['field']=dict(type_id=tid,tries=1);self.backend.save(role)
        with patch('network_redirect.guild_offline.roll',side_effect=[99,99]):
            result=self.request(87,two_type=2)
        self.assertEqual(next(row[2] for row in result if row[1]==87)['flag'],4)
        role=self.backend.profile();self.assertEqual(role['guild']['unions'][str(role['union_id'])]['resident_pets'][str(tid)],1)

    def test_continued_training_requires_240_residents_without_side_effects(self):
        self.request(1,union_name='继续挑战门槛');self.seed_residents()
        fake=(4,[],dict(fight_result_msg=dict(fight_result=[]),damage_total=100))
        with patch('network_redirect.guild_instances.simulate',return_value=fake) as battle:
            self.request(80);self.request(89)
            role=self.backend.profile();g=role['guild']['unions'][str(role['union_id'])]
            self.assertEqual(sum(g['resident_pets'].values()),239)
            self.assertEqual(role['guild']['instances']['train_attempts'],1)
            self.rejected(80)
            battle.assert_called_once()
            self.assertEqual(self.backend.profile()['guild']['instances']['train_attempts'],1)


if __name__=='__main__':unittest.main()
