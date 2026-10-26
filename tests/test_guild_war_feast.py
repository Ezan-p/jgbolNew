"""Native protocol, persisted quotas and real NPC wars on disposable accounts."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect import guild, guild_feast, guild_match, summon, npc_players
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW = 1792728000  # Friday 2026-10-23 12:00 UTC+8


class GuildWarFeastTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.addCleanup(lambda:self.b.close());self.serial=1000
        self.now=NOW
        clock=patch('network_redirect.backend.time.time',side_effect=lambda:self.now)
        clock.start();self.addCleanup(clock.stop)
        role=self.b.profile();role.update(level=40,gold_coin=100000,silver_coin=100000,vip_level=1);self.b.save(role)
        self.req(1,union_name='演武测试盟')
        role=self.b.profile();role['guild']['unions']['2'].update(money=20000,popularity=2000);self.b.save(role)
        for ident in list(role['guild']['unions']['2']['applications']):self.req(5,role_id=int(ident))

    def send(self,mid,data,ok=True):
        self.serial+=1;data=dict(data,serial_num=self.serial)
        replies=self.b.respond(encode(mid,data),{'authenticated':True})
        rows=[(mid,d) for mid,_,d in map(decode,replies)]
        errors=[d for mid,d in rows if mid==2998 and d['id']==55]
        self.assertEqual(bool(errors),not ok,errors)
        return rows

    def req(self,op,ok=True,**data):
        rows=self.send(1301,dict(id=op,data=summon.lua(data)),ok)
        return [login_fields(d['data']) for mid,d in rows if mid==1301]

    def role(self):return self.b.profile()

    def feast(self):return self.req(18,query_type=14)[-1]['feast_data']

    def battle(self,cross=False,target=None):
        if target is None:target=self.req(58 if cross else 18,query_type=23 if cross else 13)[-1]['des_member_list'][6]['id']
        return self.send(1026,dict(fight_type=17 if cross else 14,des_type=1,des_value=0,des_id=target,fight_id=0))

    def test_original_three_feast_tiers_cost_funds_and_grant_exact_csv(self):
        for typ in (1,2,3):
            with self.subTest(typ=typ):
                self.now=NOW+(typ-1)*7*86400
                before=self.role();self.req(65,feast_type=typ);row=guild_feast.FEAST[typ];after=self.role()
                self.assertEqual(before['gold_coin'],after['gold_coin'])
                self.assertEqual(before['guild']['unions']['2']['money']-after['guild']['unions']['2']['money'],int(row['cost_gold']))
                self.assertEqual(self.feast()['feast_end_time'],self.now+86400)
                before=self.role();out=self.req(68)[-1];after=self.role()
                self.assertEqual(after['strength']-before['strength'],int(row['strength']))
                self.assertEqual(after['energy']-before['energy'],int(row['energy']))
                self.assertEqual(out['prize_list'][1]['attach_count'],typ)
                self.assertEqual(after['train_tree_rate'],typ)
                self.req(68,ok=False)

    def test_week_duration_midnight_sunday_and_restart(self):
        self.now=NOW+11*3600;self.req(65,feast_type=1);end=self.feast()['feast_end_time']
        self.now+=2*3600
        self.assertEqual((self.feast()['feast_stat'],self.feast()['feast_end_time']),(0,end))
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.feast()['feast_end_time'],end)
        self.now=end;self.assertEqual(self.feast()['feast_stat'],54)
        self.req(65,ok=False,feast_type=1)
        self.now=NOW+2*86400;self.req(65,ok=False,feast_type=1)
        self.now=NOW+3*86400;self.req(65,feast_type=1)

    def test_level_funds_and_formal_members_are_authoritative(self):
        role=self.role();role['guild']['unions']['2']['members']['1']['rank']=7;self.b.save(role)
        self.req(65,ok=False,feast_type=1)
        role=self.role();role['guild']['unions']['2']['members']['1']['rank']=1;self.b.save(role)
        role=self.role();g=role['guild']['unions']['2'];g.update(popularity=0,money=100);self.b.save(role)
        before=self.role();self.req(65,ok=False,feast_type=1);self.assertEqual(before,self.role())
        role=self.role();role['guild']['unions']['2']['popularity']=2000;self.b.save(role)
        self.req(65,ok=False,feast_type=1)
        role=self.role();role['guild']['unions']['2']['money']=10000;self.b.save(role);self.req(65,feast_type=1)
        role=self.role();role['guild']['unions']['2']['members']['1']['rank']=6;self.b.save(role)
        self.req(68,ok=False);self.req(66,ok=False,des_id=1)
        self.assertTrue(all(v['can_grab']==0 for v in self.feast()['gift_data'].values()))

    def test_grab_numeric_flag_quota_expiry_and_failed_request_atomicity(self):
        self.b.guild_rules['feast_grab_limit']=1;self.req(65,feast_type=1)
        gifts=self.feast()['gift_data'];self.assertEqual(len(gifts),3)
        self.assertTrue(all(type(v['can_grab']) is int and v['can_grab']==1 for v in gifts.values()))
        self.req(66,des_id=1);before=self.role()
        self.req(66,ok=False,des_id=1);self.assertEqual(before,self.role())
        self.req(66,ok=False,des_id=2);self.assertEqual(before,self.role())
        self.assertTrue(all(v['can_grab']==0 for v in self.feast()['gift_data'].values()))
        self.now+=86400;self.assertFalse(self.feast()['can_rece_award'])
        self.assertEqual(self.role()['last_feast_grab_count'],0)

    def test_future_gift_not_grabbable_and_legacy_feast_keeps_deadline(self):
        self.req(65,feast_type=1);role=self.role();f=role['guild']['unions']['2']['feast']
        f.pop('week');f['gifts'][0]['begin_time']=NOW+100;self.b.save(role)
        self.assertEqual(self.feast()['gift_data'][1]['can_grab'],0);self.req(66,ok=False,des_id=1)
        self.assertEqual(self.feast()['feast_end_time'],NOW+86400)
        self.now+=100;self.req(66,des_id=1)

    def test_send_both_tiers_npc_collection_and_fortune(self):
        self.req(65,feast_type=1)
        self.req(67,ok=False,gift_type=1,count=1);self.req(67,ok=False,gift_type=1,count=6)
        self.req(67,gift_type=1,count=2);self.req(67,ok=False,gift_type=2,count=2)
        before=self.role();self.now+=60;self.feast()
        self.assertEqual(self.role()['gold_coin'],before['gold_coin'])
        self.assertEqual(self.feast()['gift_data'][4]['count'],0)
        self.req(67,gift_type=2,count=2)
        row=next(v for v in self.req(18,query_type=15)[-1]['fortune_info'].values() if v['id']==1)
        self.assertEqual((row['normal_gift'],row['advanced_gift'],row['contribute']),(2,2,120))

    def test_nonvip_gift_rejected_without_spending(self):
        self.req(65,feast_type=1);role=self.role();role['vip_level']=0;self.b.save(role);before=self.role()
        self.req(67,ok=False,gift_type=1,count=2);self.assertEqual(before,self.role())

    def test_tree_buff_is_limited_50_percent_not_global_multiplier(self):
        self.req(65,feast_type=2);self.req(68)
        before=self.role();self.req(36,count=1)
        self.assertEqual(self.role()['cur_union_contrib']-before['cur_union_contrib'],1)
        self.req(14)
        for index,expected in enumerate((15,15,10)):
            before=self.role();s=before['guild']
            self.req(15,mission_id=1,mission_type=1,cultivate_type=1,cultivate_record_time=s['day'],cultivate_record_count=index)
            self.assertEqual(self.role()['cur_union_contrib']-before['cur_union_contrib'],expected)
        self.assertEqual((self.role()['train_tree_rate'],self.role()['contrib_plus_rate']),(0,0))

    def test_box_use_native_protocol_and_locked_atomicity(self):
        for tid in (1120,1121):
            role=self.role();summon.add_item(role,tid,3);self.b.save(role)
            item=next(v for v in self.role()['attachments'] if v['type_id']==tid)
            request=dict(item_type=tid,item_id=item['id'],item_count=2,des_type=1,des_id=0)
            before=self.role();rows=self.send(1051,request)
            event=next(login_fields(d['data']) for mid,d in rows if mid==2998 and d['id']==21)
            self.assertTrue(event['attach_list']);self.assertGreater(self.role()['silver_coin'],before['silver_coin'])
            role=self.role();next(v for v in role['attachments'] if v['id']==item['id'])['is_lock']=True;self.b.save(role)
            before=self.role();self.send(1051,dict(request,item_count=1),ok=False);self.assertEqual(before,self.role())

    def test_local_cross_rosters_disjoint_power_ordered_and_stable(self):
        local=self.req(18,query_type=13)[-1]['des_member_list']
        cross=self.req(58,query_type=23)[-1]['des_member_list']
        self.assertFalse({v['id'] for v in local.values()} & {v['id'] for v in cross.values()})
        for rows in (local,cross):
            power=[rows[i]['combat_power'] for i in range(1,7)];self.assertEqual(power,sorted(power,reverse=True))
            self.assertTrue(all(npc_players.resolve(v['id']) for v in rows.values()))
        self.assertEqual(local,self.req(18,query_type=13)[-1]['des_member_list'])

    def test_real_wars_keep_ids_separate_and_background_results_persistent(self):
        self.req(45)
        for cross in (False,True):
            rows=self.battle(cross);line=next(d for mid,d in rows if mid==1028);result=next(d for mid,d in rows if mid==1027)
            end=next(login_fields(d['data']) for mid,d in rows if mid==2998 and d['id']==44)
            self.assertEqual(line['fight_id'],result['fight_id']);self.assertEqual(line['fight_id'],end['fight_id'])
            m=self.role()['guild']['cross_match' if cross else 'match']
            self.assertEqual(len(m['npc_rounds']),1);self.assertGreater(m['npc_rounds'][0]['round_count'],0)
            self.assertEqual(len(m['target_stats']),1)
            before=copy.deepcopy(m);self.req(58 if cross else 18,query_type=24 if cross else 16)
            self.assertEqual(before,self.role()['guild']['cross_match' if cross else 'match'])

    def test_betting_three_native_buttons_and_response_contract(self):
        self.req(45)
        for op,bet,q in ((47,48,8),(62,63,20)):
            data=self.req(op)[-1];self.assertEqual(len(data['teams']),2)
            self.assertEqual(set(data['bet_info_list'][7]),{1,2,3})
            target=data['teams'][1]['id']
            for typ in (1,2,3):
                before=self.role()['silver_coin'];out=self.req(bet,bet_type=typ,union_id=target)[-1]
                self.assertTrue(out['bet_list'][target]);self.assertEqual(before-self.role()['silver_coin'],self.b.guild_rules['match_bet_silver'][typ-1])
                self.req(bet,ok=False,bet_type=typ,union_id=target)

    def test_reward_freezes_ranking_and_shop_does_not_reduce_rank_score(self):
        self.battle(True)
        role=self.role();role['guild']['cross_match']['score']=100;self.b.save(role)
        before=self.req(58,query_type=24)[-1]['union_score']
        self.req(58,query_type=34,index=1,count=2)
        self.assertEqual(before,self.req(58,query_type=24)[-1]['union_score'])
        self.req(76);saved=self.role();self.req(76,ok=False);self.assertEqual(saved,self.role())
        self.assertFalse(self.req(58,query_type=32)[-1]['enter_data']['can_rece_award'])

    def test_next_day_mails_unclaimed_reward_once_and_resets_action(self):
        self.req(45);self.battle();before=self.role()
        self.now+=86400;self.req(18,query_type=13)
        role=self.role();mails={k:v for k,v in role['welfare']['mails'].items() if k.startswith('guild-match-')}
        self.assertEqual(len(mails),1);self.assertTrue(next(iter(mails.values()))['prizes'])
        self.assertEqual(before['silver_coin'],role['silver_coin'])
        self.assertEqual(role['guild']['match']['fights'],0)
        self.req(18,query_type=13);self.assertEqual(mails,{k:v for k,v in self.role()['welfare']['mails'].items() if k.startswith('guild-match-')})

    def test_invalid_target_and_repeated_defeated_target_do_not_spend(self):
        self.req(45);role=self.role();s=role['guild'];g=s['unions']['2'];r=self.b.guild_rules
        for ident in (True,90001.5,float('inf'),float('nan'),-1):
            with self.assertRaises(guild.formation.Rejected):guild_match.fight(role,s,g,dict(fight_type=14,des_id=ident),NOW,r,self.b.journey_rules)
        real_id=guild_match.opponents(role,s,g,r)[0]['profile']['role_id']
        guild_match.state(s,False,r)['target_life']['90001']=0;self.b.save(role);before=self.role()
        self.send(1026,dict(fight_type=14,des_type=1,des_value=0,des_id=90001,fight_id=0),ok=False)
        self.assertEqual(before,self.role());self.assertNotIn(real_id,[v['id'] for v in self.req(18,query_type=13)[-1]['des_member_list'].values()])

    def test_native_grouped_rank_and_cross_target_envelope(self):
        self.assertEqual(self.req(58,query_type=32)[-1]['enter_data']['union_data']['group_type'],3)
        target=self.req(58,query_type=23)[-1]
        self.assertEqual(target['target_list']['des_member_list'],target['des_member_list'])
        for op,q,group in ((18,16,7),(58,24,3)):
            rank=self.req(op,query_type=q)[-1]['union_score']['top_list']
            self.assertEqual(len(rank[group]),4)
            self.assertTrue(all(row['group_type']==group and row['server_name'] for row in rank[group].values()))
        self.assertEqual(guild_match.reward_row(1,True)['prize_list'],'5|1029|1|20/5|1001|1|500')
        self.assertEqual(guild_match.reward_row(1,True)['popularity'],'250')

    def test_cross_native_query_fight_settles_and_wraps_result(self):
        target=self.req(58,query_type=23)[-1]['des_member_list'][6]['id']
        out=self.req(58,query_type=28,des_id=target)[-1]
        self.assertEqual(out['target_list']['my_action_point'],self.b.guild_rules['battle_daily']-1)
        self.assertIn(out['target_list']['fight_result'],range(1,7))
        self.assertEqual(out['target_list']['prize_list'],{})
        self.assertEqual(self.role()['guild']['cross_match']['fights'],1)

    def test_fortune_weekly_mail_is_claimable_once_after_reconnect(self):
        self.req(65,feast_type=1);self.req(67,gift_type=2,count=2)
        self.now+=3*86400;self.feast()
        role=self.role();mails={k:v for k,v in role['welfare']['mails'].items() if k.startswith('guild-feast-')}
        self.assertEqual(len(mails),1);mail=next(iter(mails.values()))
        self.assertTrue(mail['no_expiry']);self.assertTrue(mail['prizes'])
        self.send(1103,dict(mail_id=mail['mail_id']))
        claimed=self.role();self.send(1103,dict(mail_id=mail['mail_id']),ok=False)
        self.assertEqual(claimed,self.role())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.feast();self.assertEqual(len([k for k in self.role()['welfare']['mails'] if k.startswith('guild-feast-')]),1)

    def test_unused_bet_is_refunded_and_affiliation_cleared_next_day(self):
        self.req(48,bet_type=3,union_id=2);old=self.role();self.now+=86400
        self.req(18,query_type=13);role=self.role()
        mail=next(v for k,v in role['welfare']['mails'].items() if k.startswith('guild-match-'))
        self.assertEqual(mail['prizes'],[[12,0,10000,1]])
        self.assertNotIn('union_id',role['guild']['match'])
        self.send(1103,dict(mail_id=mail['mail_id']))
        self.assertEqual(self.role()['silver_coin'],old['silver_coin']+10000)

    def test_settled_score_can_be_read_after_switching_guild(self):
        self.req(45);self.battle();self.req(72)
        role=self.role();other=copy.deepcopy(role['guild']['unions']['2']);other.update(id=3,name='另一个盟')
        role['guild']['unions']['3']=other;role['union_id']=3;self.b.save(role)
        self.assertEqual(self.req(18,query_type=16)[-1]['union_score']['my_order'],role['guild']['match']['settlement']['order'])
        self.req(48,ok=False,bet_type=1,union_id=3)
        self.now+=86400;self.req(18,query_type=13)
        self.assertNotIn('union_id',self.role()['guild']['match'])
