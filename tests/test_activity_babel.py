"""Original 1353 wire contract, recovery, local weeks, and exploitable boundaries."""
import copy
from pathlib import Path
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_babel as babel, activity_babel_npc as npc, npc_players, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode


class BabelTests(ActivityCase):
    def call(self, op=1, **data):
        out = self.req(1353, id=op, data=summon.lua(data)); self.ok(out)
        return [v['data'] for e,v in out if e == 203]

    def edit(self, **changes):
        role = self.b.profile(); role['activity']['babel'].update(changes); self.b.save(role)

    def saved(self):
        return self.b.profile()['activity']['babel']

    def reject(self, op, **data):
        before = self.b.profile()
        self.assertEqual(self.req(1353,id=op,data=summon.lua(data))[0][0],55)
        self.assertEqual(before,self.b.profile())

    def test_original_essences_overflow_and_natural_cap(self):
        self.call(); role = self.b.profile()
        for tid in range(20016,20020): summon.add_item(role,tid,2)
        self.b.save(role)
        for tid,n in ((20016,10),(20017,25),(20018,80),(20019,200)):
            old=self.saved()['energy']; self.call(10,item_type=tid,count=1)
            self.assertEqual(self.saved()['energy'],old+n)
        with patch('network_redirect.backend.time.time',return_value=NOW+1800):
            self.call(); self.assertEqual(self.saved()['energy'],415)
        self.reject(10,item_type=20019,count=2)

    def test_half_hour_midnight_and_clock_backwards(self):
        self.call(); self.edit(energy=20,life=10,refresh_times=0,purchases={'2':2})
        with patch('network_redirect.backend.time.time',return_value=NOW+1799):
            self.call(); self.assertEqual(self.saved()['energy'],20)
        with patch('network_redirect.backend.time.time',return_value=NOW+1800):
            self.call(); self.assertEqual(self.saved()['energy'],21)
            self.call(); self.assertEqual(self.saved()['energy'],21)
        with patch('network_redirect.backend.time.time',return_value=NOW+43200):
            self.call(); s=self.saved(); self.assertEqual((s['life'],s['energy'],s['refresh_times']),(100,44,1))
            self.assertFalse(s['purchases'])
        self.call(); self.assertEqual(self.saved()['energy'],44)
        with patch('network_redirect.backend.time.time',return_value=NOW+3*86400):
            self.call(); self.assertEqual(self.saved()['energy'],100)

    def test_zero_life_allows_exploration_not_combat(self):
        self.call(); self.edit(life=0)
        self.call(2,target_pos=dict(row=1,column=2))
        self.assertEqual(self.saved()['life'],0)
        self.reject(2,target_pos=dict(row=1,column=3))
        self.call(11); self.assertEqual(self.saved()['life'],100)
        self.reject(11)

    def test_shop_client_remaining_and_atomic_limits(self):
        self.call(); role=self.b.profile(); summon.add_item(role,20000,2000); self.b.save(role)
        self.call(4,index=2,count=3); shop=self.call(8)[0]
        self.assertEqual(shop['my_shop'][2]['limit']-shop['my_exchange'][2],2)
        self.call(4,index=2,count=2); self.reject(4,index=2,count=1)
        self.call(9); shop=self.call(8)[0]
        self.assertEqual(shop['my_exchange'][2],0)
        self.reject(9)

    def test_tools_keys_loot_and_revisit_no_refill(self):
        self.call()
        with patch('network_redirect.activity_babel.journey.battle',return_value=(3,[],[])):
            for row,col in ((1,2),(1,3),(1,4),(1,5),(2,5)):
                self.call(2,target_pos=dict(row=row,column=col))
        role=self.b.profile()
        self.assertEqual(babel.item_count(role,20012),0)
        self.assertEqual(babel.item_count(role,20006),0)
        self.assertEqual(self.saved()['coin_count'],100)
        self.call(6)
        for col in (2,3,4,5): self.call(2,target_pos=dict(row=1,column=col))
        self.assertEqual(self.saved()['coin_count'],100)
        self.call(6); self.call(2,target_pos=dict(row=2,column=1))
        self.call(2,target_pos=dict(row=2,column=2))
        self.assertEqual(babel.item_count(self.b.profile(),20005),0)

    def test_loss_keeps_guard_and_position_but_spends_resources(self):
        self.call(); self.call(2,target_pos=dict(row=1,column=2)); before=self.saved()
        with patch('network_redirect.activity_babel.journey.battle',return_value=(4,[],[])):
            self.call(2,target_pos=dict(row=1,column=3))
        s=self.saved(); self.assertEqual(s['locale'],before['locale'])
        self.assertEqual(s['floors']['1'][0][2]['elem_type'],20012)
        self.assertEqual((s['life'],s['energy'],s['coin_count']),(80,98,0))
        self.assertEqual([m for m,_,d in self.decoded if m in (1027,1028)],[1028,1027])
        self.assertTrue(any(m==2998 and d['id']==44 for m,_,d in self.decoded))

    def test_master_gate_and_terminal_once(self):
        self.call(); self.edit(locale=dict(row=5,column=7))
        self.reject(2,target_pos=dict(row=5,column=8))
        role=self.b.profile(); s=role['activity']['babel']; s['cur_floor']=60; s['history_floor']=60
        babel.generate(s); s['locale']=dict(row=4,column=6); self.b.save(role)
        with patch('network_redirect.activity_babel.journey.battle',return_value=(3,[],[])):
            self.call(2,target_pos=dict(row=4,column=7))
        self.call(2,target_pos=dict(row=5,column=7)); self.call(2,target_pos=dict(row=5,column=8))
        self.assertTrue(self.saved()['complete']); before=self.saved()['coin_count']
        self.call(2,target_pos=dict(row=5,column=7)); self.call(2,target_pos=dict(row=5,column=8))
        self.assertEqual(self.saved()['coin_count'],before)
        self.assertEqual(self.saved()['cur_floor'],60)

    def test_weekly_rank_mail_reset_preserves_items_and_claim_once(self):
        self.call(); role=self.b.profile(); s=role['activity']['babel']
        s.update(history_floor=60,participated=True,energy=300,life=5)
        summon.add_item(role,20012,3); summon.add_item(role,20000,100)
        self.b.save(role); before=self.saved(); monday=npc.start(before['week']+1,self.b.activity_rules)
        with patch('network_redirect.backend.time.time',return_value=monday):
            self.call(); s=self.saved()
            self.assertEqual((s['cur_floor'],s['history_floor'],s['life'],s['energy']),(1,1,100,300))
            self.assertEqual(s['last_my_top']['order'],1)
            role=self.b.profile(); self.assertEqual(babel.item_count(role,20012),3)
            mails=[v for k,v in role['welfare']['mails'].items() if k.startswith('babel-rank-')]
            self.assertEqual(len(mails),1); self.assertEqual(mails[0]['prizes'],[[5,20000,2000,1]])
            self.call(); self.ok(self.req(1103,mail_id=mails[0]['mail_id'],flag=1))
            self.assertEqual(babel.item_count(self.b.profile(),20000),2100)
            self.req(1103,mail_id=mails[0]['mail_id'],flag=1)
            self.assertEqual(babel.item_count(self.b.profile(),20000),2100)
            self.call(8); self.assertEqual(self.saved()['coin_count'],2100)
        with patch('network_redirect.backend.time.time',return_value=monday+4*604800):
            self.call()
            self.assertEqual(len([k for k in self.b.profile()['welfare']['mails'] if k.startswith('babel-rank-')]),1)

    def test_week_settles_on_login_prepare_without_entering_tower(self):
        self.call(); role=self.b.profile(); s=role['activity']['babel']; s['participated']=True
        monday=npc.start(s['week']+1,self.b.activity_rules)
        activity.prepare(role,monday,self.b.activity_rules)
        self.assertEqual(role['activity']['babel']['history_floor'],1)
        self.assertTrue(any(k.startswith('babel-rank-') for k in role['welfare']['mails']))

    def test_rank_stable_identities_arrival_ties_and_restart(self):
        self.call(); first=self.call(3)[0]
        self.assertEqual(len(first['all_top']),31)
        for row in first['all_top'].values():
            if row['is_npc']: self.assertIsNotNone(npc_players.resolve(row['role_id']))
        snapshot=self.b.profile(); self.b.close(); self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(snapshot,self.b.profile()); self.assertEqual(first,self.call(3)[0])
        s=self.saved(); rows=npc.ranking(self.b.profile(),s,NOW,self.b.activity_rules)['all_top']
        self.assertEqual(rows,sorted(rows,key=lambda v:(-v['history_floor'],v['reached_at'],v['role_id'])))

    def test_legacy_currency_and_map_migration(self):
        self.call(); role=self.b.profile(); s=role['activity']['babel']
        for k in ('coin_inventory','week','clock','energy_tick','opponents'): s.pop(k,None)
        s['coin_count']=120; s['floors']['1'][0][1]['elem_type']=0; self.b.save(role)
        self.call(); self.call()
        self.assertEqual(babel.item_count(self.b.profile(),20000),120)
        self.assertEqual(self.saved()['floors']['1'][0][1]['elem_type'],0)

    def test_replay_and_forged_input_roll_back(self):
        self.call(); role=self.b.profile(); summon.add_item(role,20019,3); self.b.save(role)
        self.call(10,item_type=20019,count=1); packet=self.packet; replies=self.replies; before=self.b.profile()
        self.assertEqual(self.b.respond(packet,self.state),replies); self.assertEqual(self.b.profile(),before)
        for op,data in ((2,dict(target_pos=dict(row=5,column=8))), (2,dict(target_pos=dict(row=True,column=2))),
                        (7,dict(floor=60)), (7,dict(floor=True)), (10,dict(item_type=20019,count=-1)),
                        (10,dict(item_type=20019,count=True)), (4,dict(index=True)), (5,{})):
            self.reject(op,**data)

    def test_entry_level_and_original_config(self):
        role=self.b.profile(); role['level']=35; self.b.save(role); self.reject(1)
        self.assertEqual(self.b.activity_rules['babel_energy_items'],{'20016':10,'20017':25,'20018':80,'20019':200})

    def test_npc_fixed_progression_and_immutable_source(self):
        powers=[]
        for floor in range(1,61):
            key=npc.choose(floor,9); powers.append(npc_players.catalog()[key]['profile']['role_combat_power'])
            self.assertGreaterEqual(len(npc.template(key)),1)
        self.assertEqual(powers,sorted(powers)); self.assertGreater(powers[-1],powers[0]*30)
        self.call(); s=self.saved(); key,units=npc.enemies(s,9,4,7); before=copy.deepcopy(npc.template(key))
        units[0]['hp']=1; self.assertEqual(npc.template(key),before)

    def test_real_catalog_fight_replay_and_fixed_opponent(self):
        self.call(); role=self.b.profile(); ident=role['role_id']
        key=max(npc_players.catalog(),key=lambda k:npc_players.catalog()[k]['profile']['role_combat_power'])
        role.update(copy.deepcopy(npc_players.get(key)['role'])); role['role_id']=ident
        self.b.save(role)
        self.call(2,target_pos=dict(row=1,column=2)); self.call(2,target_pos=dict(row=1,column=3))
        fight=next(d for m,_,d in self.decoded if m==1027)
        self.assertIn(fight['final_result'],(1,2,3)); self.assertEqual(fight['fight_type'],200)
        self.assertGreater(fight['fight_round'],0)
        self.assertTrue(all(len(x['damage_list'])==8 for x in fight['fight_result']))
        self.assertEqual(self.saved()['coin_count'],50)
