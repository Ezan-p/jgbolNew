"""Full offline 逐鹿 wire flows and immutable NPC/save boundaries."""
import copy
from pathlib import Path
from unittest.mock import patch
from tests.test_activity import ActivityCase,NOW
from network_redirect import activity_land as land, activity_land_npc as npc, summon
from network_redirect.backend import Backend


class OfflineLandTests(ActivityCase):
    def land(self,op,**d):return self.req(1302,id=op,data=summon.lua(d))
    def team(self,op,**d):return self.req(1303,id=1,op_type=op,data=summon.lua(d))
    def test_npc_inspect_and_restart(self):
        self.ok(self.land(3));s=self.b.profile()['activity']['land'];target=s['travel'][0]
        self.assertIn(target['npc_id'],npc.catalog());self.assertEqual(target['object_type'],1)
        expected=npc.power(npc.catalog()[target['npc_id']],s['grid_count'])
        self.assertEqual(target['fight_power'],expected)
        self.ok(self.req(1039,des_id=target['id'],des_type=1,flag=10,fight_id=0))
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(s,self.b.profile()['activity']['land'])
        before=copy.deepcopy(npc.catalog()[target['npc_id']])
        self.ok(self.land(4,flag=1,des_type=1,des_id=target['id']))
        self.assertEqual(before,npc.catalog()[target['npc_id']])
        self.assertEqual(self.land(4,flag=1,des_type=1,des_id=target['id'])[0][0],55)
    def test_team_lifecycle_atomic_capacity_order_and_lock(self):
        self.ok(self.team(9,query_type=1));self.ok(self.team(1));self.ok(self.team(10))
        self.ok(self.team(3,id_list=[940001,940002]))
        before=self.b.profile();self.assertEqual(self.team(3,id_list=[940003])[0][0],55);self.assertEqual(before,self.b.profile())
        ids=[940002,before['role_id'],940001];self.ok(self.team(11,id_list=ids))
        self.assertEqual([m['id'] for m in self.b.profile()['activity']['land']['team']['members']],ids)
        self.ok(self.team(8,id_list=[940001]));self.ok(self.team(12))
        self.assertEqual(self.team(3,id_list=[940003])[0][0],55)
        self.ok(self.team(13));self.ok(self.team(4,id_list=[940003]));self.ok(self.team(5));self.ok(self.team(7))
        self.ok(self.team(2,id_list=[940001]));self.ok(self.team(6))
        self.assertIsNone(self.b.profile()['activity']['land']['team'])
    def test_team_tower_battle_and_cannot_change_while_occupied(self):
        when=NOW+8*3600
        with patch('network_redirect.backend.time.time',return_value=when):
            self.ok(self.land(1));self.assertEqual(self.land(4,flag=1,des_type=2,des_id=11)[0][0],55)
            self.ok(self.team(1));self.ok(self.team(3,id_list=[940001,940002]))
            out=self.land(4,flag=1,des_type=2,des_id=11);self.ok(out)
            replay=out[-1][1]['final_result_list'][1]
            army=[u for u in replay['line_up_msg']['lineup'].values() if u['src_hp']>0]
            self.assertGreater(len(army),2);self.assertTrue(out[-1][1]['is_win'])
            self.assertEqual(self.team(7)[0][0],55)
            self.ok(self.land(5,tower_id=11));self.ok(self.team(7))
    def test_week_reward_once_offline_no_phantom_weeks(self):
        self.ok(self.land(1));r=self.b.profile();s=r['activity']['land'];s['week_soul']=999999;s['soul_count']=7;self.b.save(r)
        with patch('network_redirect.backend.time.time',return_value=NOW+8*86400):
            self.ok(self.land(1));r=self.b.profile();m=[m for k,m in r['welfare']['mails'].items() if k.startswith('land-week-')]
            self.assertEqual(len(m),1);self.assertEqual(m[0]['prizes'][0],[5,10000,1200,1])
            self.assertEqual(r['activity']['land']['soul_count'],7)
            self.ok(self.land(1));self.assertEqual(r,self.b.profile())
            gold=r['gold_coin'];self.ok(self.req(1102,mail_id=m[0]['mail_id'],flag=1))
            self.ok(self.req(1103,mail_id=m[0]['mail_id'],flag=1))
            self.assertEqual(self.b.profile()['gold_coin'],gold+500)
            after=self.b.profile();self.req(1103,mail_id=m[0]['mail_id'],flag=1);self.assertEqual(after,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+40*86400):
            self.ok(self.land(1));self.assertEqual(len([k for k in self.b.profile()['welfare']['mails'] if k.startswith('land-week-')]),1)
    def test_rankings_logs_and_sweep_wire_shape(self):
        self.ok(self.land(22));self.ok(self.land(10));self.assertFalse(self.b.profile()['activity']['land']['had_news'])
        out=self.land(18,flag=1);self.ok(out);rows=out[-1][1]['top_data'];self.assertGreater(len(rows),1)
        out=self.land(27);self.ok(out)
        r=self.b.profile();r['activity']['land']['boss_layer']=3;self.b.save(r)
        out=self.land(13);self.ok(out);self.assertEqual(len(out[-1][1]['sweep_list']),3)
        self.assertIn('attach_count',out[-1][1]['sweep_list'][1][1])
    def test_invalid_types_rollback_and_no_battle_during_tower_time(self):
        self.ok(self.land(3));before=self.b.profile()
        for op,d in [(3,dict(id_list=[True])),(9,dict(query_type=True)),(11,dict(id_list={2:940001}))]:
            self.assertEqual(self.team(op,**d)[0][0],55);self.assertEqual(before,self.b.profile())
        with patch('network_redirect.backend.time.time',return_value=NOW+8*3600):
            self.assertEqual(self.land(4,flag=1,des_type=1,des_id=942001)[0][0],55)
    def test_pending_boss_cards_survive_midnight_and_restart(self):
        self.ok(self.land(1));r=self.b.profile();r['activity']['land']['soul_count']=1000;self.b.save(r)
        self.ok(self.land(4,flag=1,des_type=3,des_id=1,cur_num=1));self.ok(self.land(14,index=1))
        pending=self.b.profile()['activity']['land']['boss']
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.ok(self.land(12));self.assertEqual(pending,self.b.profile()['activity']['land']['boss'])
            self.assertEqual(self.land(14,index=1)[0][0],55);self.ok(self.land(15))

    def test_complete_64_layers_both_worlds_real_battles(self):
        self.ok(self.land(1));r=self.b.profile();identity=r['role_id']
        # A designed endgame army with a full set of activity charms. This is
        # an isolated flow fixture for the stronger towers, not a natural grind.
        model=next(n for n in npc.catalog().values() if n['role']['level']==99 and n['tier']=='T2')
        r.update(copy.deepcopy(model['role']));r['role_id']=identity
        r['activity']['land'].update(soul_count=100000,
            charms={str(i):dict(key=(i-1)%4+1,value=30,unlock=True,is_open=True)
                    for i in land.CHARMS})
        self.b.save(r)
        for layer in range(1,65):
            s=self.b.profile()['activity']['land']
            result=self.land(4,flag=1,des_type=3,des_id=layer,cur_num=s['grid_count']);self.ok(result)
            self.assertTrue(result[-1][1]['is_win'],('normal',layer))
            self.ok(self.land(14,index=1));self.ok(self.land(15))
            s=self.b.profile()['activity']['land'];grid=s['grid_count']+1
            if grid in land.GRIDS and layer>=int(land.GRIDS[grid]['boss_layer']):self.ok(self.land(9,grid_count=grid))
            if layer in (16,32,48):self.ok(self.land(2,des_level=layer//16+1))
            self.assertTrue(self.land(24)[-1][1]['data']['boss_info']['is_open'])
            result=self.land(4,flag=1,des_type=4,des_id=layer,cur_num=self.b.profile()['activity']['land']['grid_count']);self.ok(result)
            self.assertTrue(result[-1][1]['is_win'],('hell',layer))
            self.ok(self.land(23,index=1));self.ok(self.land(25))
        s=self.b.profile()['activity']['land'];self.assertEqual((s['boss_layer'],s['inv_boss_layer'],s['grid_count'],s['map_level']),(64,64,8,4))
        self.ok(self.land(13))
        self.assertEqual(self.land(4,flag=1,des_type=3,des_id=65,cur_num=8)[0][0],55)
