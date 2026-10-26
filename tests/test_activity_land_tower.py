"""Native portrait requests and the 64 distinct tower encounters."""
import copy
from unittest.mock import patch
from tests.test_activity import ActivityCase
from network_redirect import activity_land as land, activity_land_encounters as encounters
from network_redirect import activity_land_boss as boss, formation, summon
from network_redirect.backend import Backend
from pathlib import Path


class LandTowerTests(ActivityCase):
    def land(self,op,**d):return self.req(1302,id=op,data=summon.lua(d))

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
