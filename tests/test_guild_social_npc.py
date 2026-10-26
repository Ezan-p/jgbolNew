"""Catalog identity and real combat contracts for simulated guild social play."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect import guild_match, npc_players, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

NOW = 1792814400


class GuildSocialNpcTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.b.close())
        self.clock = patch('network_redirect.backend.time.time', return_value=NOW)
        self.clock.start(); self.addCleanup(self.clock.stop)
        self.serial = 1000
        role = self.b.profile(); role.update(level=30, gold_coin=100000, silver_coin=100000)
        self.b.save(role)
        self.req(1, union_name='道友测试盟')

    def req(self, op, **data):
        self.serial += 1
        packets = self.b.respond(encode(1301, dict(serial_num=self.serial, id=op, data=summon.lua(data))), {'authenticated': True})
        decoded = [(mid, d) for mid, _, d in map(decode, packets)]
        self.assertFalse(any(mid == 2998 and d['id'] == 55 for mid, d in decoded), decoded)
        return [login_fields(d['data']) for mid, d in decoded if mid == 1301]

    def test_match_display_inspection_and_combat_share_catalog_army(self):
        self.req(45)
        rows = self.req(18, query_type=13)[-1]['des_member_list']
        self.assertEqual(len(rows), 6)
        self.assertEqual(len({r['id'] for r in rows.values()}), 6)
        for row in rows.values():
            npc = npc_players.get(row['id'])
            self.assertEqual(row['name'], npc['role']['role_name'])
            self.assertEqual(row['head_type'], npc['role']['head_type'])
            view = guild_match.lineup(self.b.profile(), row['id'], self.b.guild_rules)
            self.assertEqual(view['npc_player_id'], row['id'])
            self.assertGreater(len(view['cortege_list']), 1)
        leader = rows[1]
        with patch('network_redirect.guild_combat.simulate', return_value=(1, [], {})) as battle:
            role = self.b.profile(); role['guild']['fight_id'] = 1
            guild_match.fight(role, role['guild'], role['guild']['unions']['2'],
                              dict(fight_type=16, des_id=leader['id']), NOW, self.b.guild_rules, self.b.journey_rules)
            self.assertEqual(battle.call_args.kwargs['enemy_npc'], leader['npc_id'])
        self.assertEqual(self.req(18, query_type=13)[-1]['des_member_list'], rows)

    def test_npc_leader_betting_uses_leader_identity_after_transfer(self):
        role = self.b.profile(); applicant = int(next(iter(role['guild']['unions']['2']['applications'])))
        self.req(5, role_id=applicant)
        self.req(12, role_id=applicant)
        data = self.req(18, query_type=8)[-1]
        self.assertEqual(data['lineup_list'][6][1]['src']['leader_id'], applicant)
        self.req(48, bet_type=1, union_id=applicant)
        self.assertTrue(self.req(18, query_type=8)[-1]['bet_list'][applicant])

    def test_escort_catalog_targets_raid_identity_and_real_battle(self):
        data = self.req(69, flag=3, road_type=1)[-1]
        targets = data['book_list']; self.assertEqual(len(targets), 3)
        target = targets[1]
        self.assertEqual(target['player_name'], npc_players.get(target['id'])['role']['role_name'])
        self.assertEqual(self.req(69, flag=3, road_type=1)[-1]['book_list'], targets)
        self.req(69, flag=10, des_id=target['id'])
        self.req(69, flag=6, road_type=1, book_level=1, des_id=0)
        with patch('network_redirect.backend.time.time', return_value=NOW+1801), patch('network_redirect.guild_offline.roll', return_value=0):
            raid = self.req(69, flag=12)[-1]['berob_info'][1]
            self.assertEqual(raid['rob_id'], target['id'])
            self.req(69, flag=14, des_id=raid['rob_id'])
            self.assertTrue(self.req(69, flag=12)[-1]['berob_info'][1]['is_black'])

    def test_feast_npc_gifts_once_without_spending_player_quota(self):
        role = self.b.profile()
        for ident in list(role['guild']['unions']['2']['applications']):
            self.req(5, role_id=int(ident))
        self.req(65, feast_type=1)
        before = self.b.profile()
        data = self.req(18, query_type=14)[-1]['feast_data']
        gifts = data['gift_data']; self.assertEqual(len(gifts), 3)
        self.assertTrue(all(npc_players.resolve(g['sender_id']) for g in gifts.values()))
        self.req(18, query_type=14)
        self.assertEqual(before['gold_coin'], self.b.profile()['gold_coin'])
        self.assertEqual(self.b.profile()['guild']['unions']['2']['feast']['sent'], 0)
        self.assertEqual(len(self.b.profile()['guild']['unions']['2']['feast']['gifts']), 3)
        self.req(66, des_id=gifts[1]['des_id'])
        fortune = self.req(18, query_type=15)[-1]['fortune_info']
        self.assertEqual(len(fortune), 4)

    def test_saved_match_roster_survives_restart_and_changes_next_day(self):
        first = self.req(18, query_type=13)[-1]['des_member_list']
        saved = copy.deepcopy(self.b.profile()['guild']['match']['npc_roster'])
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(first, self.req(18, query_type=13)[-1]['des_member_list'])
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.req(18, query_type=13)
        self.assertNotEqual(saved, self.b.profile()['guild']['match']['npc_roster'])

    def test_escort_legacy_targets_migrate_before_direct_rob_and_preserve_revenge(self):
        from network_redirect import guild_escort
        role=self.b.profile();s=role['guild'];g=s['unions']['2'];e=guild_escort.state(s)
        e['targets']={'1':[guild_escort.book(role,g,91001+10*i,NOW,2) for i in range(3)]}
        e['targets']['1'][0]['be_grab_times']=2
        e['black']=[dict(id=91001,name='离线取经者',union_name='演武仙盟',book_level=2)]
        e['raid_log']=[dict(id=91001,rob_id=91001,name='离线取经者',player_name='离线取经者',union_name='演武仙盟',book_level=2)]
        s['fight_id']=1
        with patch('network_redirect.guild_combat.simulate',return_value=(1,[],{})) as battle:
            packets=guild_escort.rob(role,s,g,e,dict(des_id=91001.0),NOW,self.b.guild_rules)
        targets=e['targets']['1']
        self.assertEqual(len({t['id'] for t in targets}),3)
        self.assertTrue(all(npc_players.resolve(t['id']) for t in targets))
        target=targets[0]
        self.assertEqual(target['be_grab_times'],3)
        self.assertEqual(target['end_time'],NOW+3600)
        self.assertEqual(battle.call_args.kwargs['enemy_npc'],target['npc_id'])
        self.assertEqual(e['black'][0]['id'],target['id'])
        self.assertEqual(e['raid_log'][0]['rob_id'],target['id'])
        self.assertEqual(e['raid_log'][0]['player_name'],target['player_name'])
        result=next(login_fields(d['data']) for mid,_,d in map(decode,packets) if mid==1301)
        self.assertTrue(result['is_run_kill'])
        saved=copy.deepcopy(e)
        guild_escort.migrate_targets(role,s,g,e,NOW)
        self.assertEqual(saved,e)

    def test_escort_old_blacklist_without_active_targets_gets_real_identity(self):
        from network_redirect import guild_escort
        role=self.b.profile();s=role['guild'];g=s['unions']['2'];e=guild_escort.state(s)
        e['black']=[dict(id=91001,name='离线取经者',union_name='演武仙盟',book_level=1)]
        e['raid_log']=[dict(id=91001,rob_id=91001,name='离线取经者',player_name='离线取经者')]
        guild_escort.migrate_targets(role,s,g,e,NOW)
        self.assertTrue(npc_players.resolve(e['black'][0]['id']))
        self.assertEqual(e['black'][0]['id'],e['raid_log'][0]['rob_id'])
        self.assertEqual(e['black'][0]['name'],e['raid_log'][0]['player_name'])

    def test_escort_binary_fight_accepts_catalog_double_id(self):
        target=self.req(69,flag=3,road_type=1)[-1]['book_list'][1]
        self.serial+=1
        packet=encode(1026,dict(serial_num=self.serial,fight_type=19,des_type=1,
                              des_value=0,des_id=target['id'],fight_id=0))
        rows=list(map(decode,self.b.respond(packet,{'authenticated':True})))
        self.assertFalse(any(mid==2998 and data['id']==55 for mid,_,data in rows))
        self.assertTrue(any(mid==1027 for mid,_,data in rows))

    def test_escort_rejects_fractional_and_nonfinite_binary_target_ids(self):
        from network_redirect import guild_escort, formation
        role=self.b.profile();s=role['guild'];g=s['unions']['2'];e=guild_escort.state(s)
        for ident in (True,91001.5,float('nan'),float('inf'),-1):
            with self.subTest(ident=ident),self.assertRaises(formation.Rejected):
                guild_escort.rob(role,s,g,e,dict(des_id=ident),NOW,self.b.guild_rules)

    def blacklist_target(self, quality=2):
        target=self.req(69,flag=3,road_type=1)[-1]['book_list'][1]
        role=self.b.profile();row=role['guild']['escort']['targets']['1'][0]
        row['book_level']=quality
        role['guild']['escort']['rob_limits'].pop(str(row['id']),None)
        self.b.save(role)
        self.req(69,flag=14,des_id=target['id'])
        return target['id']

    def test_expired_blacklist_target_can_be_chased_without_changing_npc(self):
        ident=self.blacklist_target()
        original=npc_players.resolve(ident)
        with patch('network_redirect.backend.time.time',return_value=NOW+3601):
            row=self.req(69,flag=13)[-1]['union_black_info'][1]
            self.assertFalse(row['noChase'])
            target=self.b.profile()['guild']['escort']['chase_targets'][str(ident)]
            self.assertEqual(target['npc_id'],original)
            self.assertEqual(target['id'],ident)
            self.req(69,flag=10,des_id=ident)
            self.assertEqual(self.b.profile()['guild']['escort']['rob_counts'][str(ident)],1)
        with patch('network_redirect.backend.time.time',return_value=NOW+7202):
            self.req(69,flag=13)
            target=self.b.profile()['guild']['escort']['chase_targets'][str(ident)]
            self.assertEqual((target['id'],target['npc_id'],target['be_grab_times']),(ident,original,1))

    def test_blacklist_next_day_preserves_npc_and_renews_daily_quota(self):
        ident=self.blacklist_target(quality=5)
        self.req(69,flag=10,des_id=ident)
        self.assertTrue(self.req(69,flag=13)[-1]['union_black_info'][1]['noChase'])
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            row=self.req(69,flag=13)[-1]['union_black_info'][1]
            self.assertEqual(row['id'],ident)
            self.assertEqual(row['be_grab_times'],0)
            self.assertFalse(row['noChase'])
            self.req(69,flag=10,des_id=ident)
            self.assertEqual(self.b.profile()['guild']['escort']['rob_counts'][str(ident)],1)
            self.assertTrue(self.req(69,flag=13)[-1]['union_black_info'][1]['noChase'])

    def test_blacklist_refresh_cannot_bypass_per_identity_limit(self):
        self.b.guild_rules['escort_rob_daily']=10
        ident=self.blacklist_target(quality=2)
        for index in range(3):
            with patch('network_redirect.backend.time.time',return_value=NOW+3601*index):
                self.req(69,flag=10,des_id=ident)
        with patch('network_redirect.backend.time.time',return_value=NOW+10803):
            row=self.req(69,flag=13)[-1]['union_black_info'][1]
            self.assertTrue(row['noChase']);self.assertEqual(row['be_grab_times'],3)
            self.req(69,flag=3,road_type=1)
            before=self.b.profile()
            self.serial+=1
            packet=encode(1301,dict(serial_num=self.serial,id=69,data=summon.lua(dict(flag=10,des_id=ident))))
            replies=list(map(decode,self.b.respond(packet,{'authenticated':True})))
            self.assertTrue(any(mid==2998 and d['id']==55 for mid,_,d in replies))
            self.assertEqual(before,self.b.profile())

    def test_blacklist_no_chase_reflects_account_daily_limit(self):
        ident=self.blacklist_target(quality=2)
        role=self.b.profile();role['guild']['escort']['robbed']=self.b.guild_rules['escort_rob_daily'];self.b.save(role)
        row=self.req(69,flag=13)[-1]['union_black_info'][1]
        self.assertEqual(row['id'],ident)
        self.assertTrue(row['noChase'])
