"""Players-backed hunting ground: boundary, economy and original score regressions."""
import copy
import math
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity_land as land, activity_land_npc as npc
from network_redirect import activity_land_boss as bosses, activity_land_rewards as rewards
from network_redirect import npc_players, summon, journey, combat_engine, role_profile


class LandPlayersTests(ActivityCase):
    def land(self, op, **data):return self.req(1302,id=op,data=summon.lua(data))
    def team(self, op, **data):return self.req(1303,id=1,op_type=op,data=summon.lua(data))

    def test_players_catalog_both_versions_and_unique_encounters(self):
        keys=set(npc.catalog())
        self.assertEqual({npc_players.catalog()[k]['version'] for k in keys},{'v1','v2'})
        self.ok(self.land(3));s=self.b.profile()['activity']['land']
        self.assertEqual(len(s['travel']),len({m['npc_id'] for m in s['travel']}))
        for m in s['travel']:
            p=npc_players.catalog()[m['npc_id']]['profile']
            self.assertEqual((m['name'],m['npc_player_id']),(p['role_name'],p['role_id']))
        for level in range(1,5):
            r=self.b.profile();s=r['activity']['land'];s['map_level']=level
            land.travel(s,self.b.activity_rules,r)
            self.assertEqual(len(s['travel']),len({m['npc_id'] for m in s['travel']}))
            self.assertTrue(all(m['npc_id'] in keys for m in s['travel']))

    def test_companions_persist_after_growth_day_and_legacy_migration(self):
        self.ok(self.team(1));self.ok(self.team(3,id_list=[940001,940002]))
        r=self.b.profile();s=r['activity']['land'];keys=list(s['companions'])
        members=copy.deepcopy(s['team']['members']);s.pop('players_version');s.pop('companions')
        self.b.save(r);self.ok(self.land(1));s=self.b.profile()['activity']['land']
        self.assertEqual(keys,s['companions']);self.assertEqual(members,s['team']['members'])
        r=self.b.profile();r['level']=99;self.b.save(r)
        with patch('network_redirect.backend.time.time',return_value=NOW+86400):
            self.ok(self.land(1));self.assertEqual(keys,self.b.profile()['activity']['land']['companions'])

    def test_clock_rollback_rejects_without_resetting_quotas(self):
        self.ok(self.land(22));before=self.b.profile()
        with patch('network_redirect.backend.time.time',return_value=NOW-86400):
            self.assertEqual(self.land(3)[0][0],55)
            # profile() may expire unrelated time-limited titles; land and resources remain intact.
            after=self.b.profile()
            self.assertEqual(before['activity']['land'],after['activity']['land'])
            self.assertEqual(before['gold_coin'],after['gold_coin'])
        self.ok(self.land(3))

    def test_original_score_constants_and_formula(self):
        from analysis.tools.luajit_static import parse
        from pathlib import Path
        path=Path('jgbol3.87/assets/release_/a7fdff2d963cdaff0cb07cdc0845f337.data')
        protos=parse(path.read_bytes())['protos']
        self.assertEqual([q['numbers'] for q in protos[1:5]],
                         [[1.2,0.5,20],[1.2,0.5,25],[1.2,0.5,15],[1.2,0.5,30]])
        s=dict(charms={})
        self.assertEqual([bosses.score(s,n) for n in range(1,9)],
                         [3000,2850,2700,2580,2520,2400,2250,2100])
        for i in range(1,45):s['charms'][str(i)]=dict(key=i%4+1,unlock=True,is_open=True)
        expected=max(0,3000-sum(math.floor((11+11**1.2)*0.5*f) for f in (20,25,15,30)))
        self.assertEqual(bosses.score(s,1),expected)
        s['charms']['1']['is_open']=False
        self.assertGreaterEqual(bosses.score(s,1),expected)

    def test_best_score_does_not_overwrite_best_participant_count(self):
        self.ok(self.land(1));r=self.b.profile();r['activity']['land']['soul_count']=10000
        r['corteges'].append(dict(r['corteges'][0],id=max(c['id'] for c in r['corteges'])+1,order=2))
        self.b.save(r)
        self.ok(self.land(4,flag=1,des_type=3,des_id=1,cur_num=1));self.ok(self.land(15))
        self.ok(self.land(4,flag=1,des_type=3,des_id=1,cur_num=2))
        s=self.b.profile()['activity']['land']
        self.assertEqual(s['history']['1'],dict(score=3000,cur_num=1))
        self.assertEqual(s['total_score'],3000)
        self.assertIsNone(s['boss'])

    def test_boss_preview_matches_actual_enemy_units(self):
        self.ok(self.land(1));s=self.b.profile()['activity']['land'];r=self.b.activity_rules
        from network_redirect import combat_power, formation
        for hell in (False,True):
            row=bosses.boss(s,r,hell,64)
            _,units=journey.fighters({'corteges':[]},dict(cortege_list='/'.join([f"{r['battle_npc']}|{64*(3 if hell else 2)}"]*8)))
            self.assertEqual(row['fight_power'],sum(combat_power.score_panel(u,formation.load_rules()['combat_weights']) for u in units))

    def test_ranking_stable_real_id_and_elapsed_week_progress(self):
        self.ok(self.land(1));role=self.b.profile();s=role['activity']['land'];r=self.b.activity_rules
        start=(s['week']*7+4)*86400-r['timezone_offset_hours']*3600
        one,_=npc.ranking(role,s,False,2,start+86400,r)
        two,_=npc.ranking(role,s,False,2,start+2*86400,r)
        final,_=npc.ranking(role,s,False,2,final=True)
        a={x['id']:x for x in one};b={x['id']:x for x in two};c={x['id']:x for x in final}
        for ident,row in a.items():
            if ident==role['role_id']:continue
            self.assertIsNotNone(npc_players.resolve(ident))
            self.assertEqual(b[ident]['soul'],row['soul']*2)
            self.assertEqual(c[ident]['soul'],row['soul']*7)
        before=copy.deepcopy(s['competitors']);s['soul_count']=999999
        self.assertEqual(npc.ranking(role,s,False,2,start+86400,r)[1]['soul'],0)
        self.assertEqual(s['competitors'],before)

    def test_title_achievement_once_and_week_title_expires(self):
        self.ok(self.land(1));r=self.b.profile();s=r['activity']['land']
        s['boss_layer']=60;s['week_soul']=999999;self.b.save(r);self.ok(self.land(1))
        titles=copy.deepcopy(self.b.profile()['profile_titles'])
        self.assertTrue(all(str(i) in titles for i in range(120,125)))
        with patch('network_redirect.backend.time.time',return_value=NOW+2*86400):
            self.ok(self.land(1));r=self.b.profile()
            self.assertEqual(r['profile_titles']['120'],titles['120'])
            self.assertIn('128',r['profile_titles'])
            end=r['profile_titles']['128']['endtime']
        with patch('network_redirect.backend.time.time',return_value=end+1):
            self.ok(self.land(1));r=self.b.profile()
            self.assertFalse(role_profile.available(r['profile_titles']['128'],end+1))
            self.assertEqual(r['profile_titles']['120'],titles['120'])

    def test_sunday_tower_income_settles_into_previous_week_once(self):
        self.ok(self.land(1));s=self.b.profile()['activity']['land'];r=self.b.activity_rules
        monday=((s['week']+1)*7+4)*86400-r['timezone_offset_hours']*3600
        with patch('network_redirect.backend.time.time',return_value=monday-600):
            self.ok(self.land(16,tower_id=14))
        with patch('network_redirect.backend.time.time',return_value=monday+600):
            self.ok(self.land(1));s=self.b.profile()['activity']['land']
            self.assertEqual(s['last_week_result']['soul'],100)
            self.assertEqual(s['week_soul'],0);self.assertEqual(s['soul_count'],100)
            self.ok(self.land(1));self.assertEqual(self.b.profile()['activity']['land'],s)

    def test_encoding_failure_and_duplicate_request_are_atomic(self):
        self.ok(self.land(1));before=self.b.profile()
        with patch('network_redirect.activity_land.response',side_effect=ValueError('encoding failure')):
            self.assertEqual(self.land(22)[0][0],55)
        self.assertEqual(before,self.b.profile())
        self.ok(self.land(22));after=self.b.profile();packet=self.packet
        self.assertEqual(self.b.respond(packet,self.state),self.replies)
        self.assertEqual(after,self.b.profile())

    def test_legacy_scores_migrate_once_without_creating_points(self):
        s=dict(history={'64':dict(score=6400,cur_num=8)},inv_history={'1':dict(score=100,cur_num=1)},charms={},total_score=6500)
        bosses.migrate_scores(s)
        self.assertEqual(s['history']['64']['score'],2100)
        self.assertEqual(s['history']['64']['legacy_score'],6400)
        self.assertEqual(s['total_score'],2200)
        before=copy.deepcopy(s);bosses.migrate_scores(s);self.assertEqual(before,s)

    def test_team_npc_traits_survive_overlapping_snapshot_companion_ids(self):
        self.ok(self.land(1));r=self.b.profile();s=r['activity']['land']
        model=next(n for n in npc.catalog().values() if n['role']['level']==99 and n['tier']=='T1')
        ident=r['role_id'];r.update(copy.deepcopy(model['role']));r['role_id']=ident
        key=next(k for k,n in npc.catalog().items() if n['role']['level']==99 and n['tier']=='T2')
        s['grid_count']=8;s['team']=dict(members=[dict(id=ident),dict(id=940001,npc_id=key)])
        expected=npc.units(key,4);baseline=copy.deepcopy(npc.catalog()[key])
        real=journey.battle;captured=[]
        def battle(role,cfg,rules,**kwargs):
            # Exercise exactly the engine attachment pass that used to replace
            # teammate traits when different snapshots reused companion IDs.
            engine=combat_engine.Battle(role,kwargs['units'],rules)
            captured.extend(engine.sides[0][4:])
            return real(role,cfg,rules,**kwargs)
        with patch.object(journey,'battle',side_effect=battle):
            land.simulate(r,s,self.b.activity_rules,self.b.journey_rules,1,team=True)
        self.assertEqual(len(captured),4)
        for actual,want in zip(captured,expected):
            self.assertLess(actual['companion_id'],0)
            self.assertEqual(actual.get('reborn_traits'),want.get('reborn_traits'))
            self.assertEqual(actual.get('essences'),want.get('essences'))
        self.assertEqual(npc.catalog()[key],baseline)
