"""Players-backed 渡劫 diversity without invented stats or reward changes."""
import copy
import random
from unittest.mock import patch
from tests.test_activity import ActivityCase
from network_redirect import activity_rape as rape, activity_rape_npc as npc, npc_players, formation


class RapePlayersTests(ActivityCase):
    def setUp(self):
        super().setUp()
        rng=random.Random(2610)
        p=patch('secrets.choice',side_effect=rng.choice);p.start();self.addCleanup(p.stop)
        p=patch.object(rape,'roll_forms',return_value=[4,6,2]);p.start();self.addCleanup(p.stop)

    def board(self,flag=1):
        self.ok(self.req(1029,flag=flag))
        return [t for b in self.b.profile()['activity']['rape_boards'] for rows in b['form_list'].values() for t in rows.values()]

    def test_players_sources_identity_inspection_and_real_battle(self):
        catalog=npc.catalog()
        self.assertGreater(len(catalog),1500)
        self.assertEqual({npc_players.catalog()[k]['version'] for k in catalog},{'v1','v2'})
        rows=self.board()
        for t in rows:
            p=npc_players.catalog()[t['npc_id']]['profile']
            self.assertEqual((t['name'],t['npc_player_id']),(p['role_name'],p['role_id']))
        r=self.b.profile();ident,t=next(iter(r['activity']['rape_boards'][0]['form_list']['2'].items()))
        view=next(d for e,d in self.req(1039,des_type=2,des_id=int(ident)) if e==11)
        self.assertEqual(view['npc_player_id'],t['npc_player_id'])
        self.assertEqual(view['role_combat_power'],t['power'])
        snapshot=copy.deepcopy(catalog[t['npc_id']])
        self.ok(self.req(1026,fight_type=3,des_type=2,des_value=1,des_id=int(ident)))
        self.assertEqual(snapshot,catalog[t['npc_id']])

    def test_refresh_variety_bounded_power_and_history(self):
        r=self.b.profile()
        # A representative player, not the tiny default starter at level 60.
        source=npc.catalog()['npc_v2_l60_t3_attack']['role']
        r['corteges']=copy.deepcopy(source['corteges']);r['attachments']=copy.deepcopy(source['attachments']);self.b.save(r)
        seen=set();previous=set()
        for i in range(8):
            rows=self.board(1 if i==0 else 3);keys=[t['npc_id'] for t in rows]
            self.assertEqual(len(keys),len(set(keys)))
            if i==1:self.assertFalse(previous.intersection(keys))
            seen.update(keys);previous=set(keys)
            role=self.b.profile()
            for b in role['activity']['rape_boards']:
                for j,t in enumerate(b['form_list']['2'].values()):
                    self.assertIn(t['npc_id'],npc.candidates(role,j,rape.rules()))
                    self.assertLessEqual(t['level'],role['level'])
            self.assertLessEqual(len(role['activity']['rape_recent_npcs']),108)
        self.assertGreater(len(seen),48)
        before=self.b.profile();self.board();self.assertEqual(before,self.b.profile())

    def test_single_refresh_changes_identity_and_retains_slot(self):
        self.board();r=self.b.profile();rows=r['activity']['rape_boards'][0]['form_list']['2'];ident,old=next(iter(rows.items()))
        self.ok(self.req(1041,form_index=1,object_type=2,object_id=int(ident)))
        new=next(iter(self.b.profile()['activity']['rape_boards'][0]['form_list']['2'].values()))
        self.assertNotEqual(new['npc_player_id'],old['npc_player_id'])
        self.assertEqual((new['index'],new['rand']),(old['index'],old['rand']))
        self.assertEqual(self.b.profile()['activity']['rape_recent_npcs'][-1],new['npc_id'])

    def test_sparse_pool_falls_back_without_raising_difficulty(self):
        r=self.b.profile();r['level']=8
        for c in r['corteges']:c['combat_power']=1
        for i in range(3):
            pool=npc.candidates(r,i,rape.rules())
            r['activity']['rape_recent_npcs']=pool
            self.assertIn(npc.choose(r,i,rape.rules(),used=pool),pool)
            self.assertTrue(all(npc.catalog()[k]['role']['level']<=8 for k in pool))

    def test_larger_pool_keeps_original_power_window_at_all_stages(self):
        for level in (8,25,60,99):
            role=npc.catalog()[f'npc_v2_l{level:02d}_t3_attack']['role']
            for index in range(3):
                old=npc.candidates(role,index,dict(rape.rules(),match_candidates=24))
                expanded=npc.candidates(role,index,rape.rules())
                self.assertTrue(set(old)<set(expanded))
                target=role['role_combat_power']*rape.rules()['power_percent'][index]//100
                distance=lambda key:abs(npc.catalog()[key]['role']['role_combat_power']-target)
                bound=distance(old[0])+max(1,target*rape.rules()['match_tolerance_percent']//100)
                self.assertTrue(all(distance(key)<=bound for key in expanded))
                self.assertLessEqual(len(expanded),72)

    def test_exclusion_does_not_shift_power_window(self):
        role=dict(level=8,corteges=[dict(order=1,combat_power=100)],activity={})
        pool={key:dict(npc_id=key,role=dict(level=8,role_combat_power=power))
              for key,power in (('near',55),('distant',1000))}
        with patch.object(npc,'catalog',return_value=pool):
            self.assertEqual(npc.candidates(role,0,rape.rules()),['near'])
            with self.assertRaises(formation.Rejected):
                npc.choose(role,0,rape.rules(),excluded=['near'])

    def test_single_refresh_without_alternative_does_not_charge(self):
        self.board();before=self.b.profile()
        ident,old=next(iter(before['activity']['rape_boards'][0]['form_list']['2'].items()))
        only={old['npc_id']:npc.catalog()[old['npc_id']]}
        with patch.object(npc,'catalog',return_value=only):
            events=self.req(1041,form_index=1,object_type=2,object_id=int(ident))
        self.assertIn(55,[e for e,d in events])
        self.assertEqual(before,self.b.profile())

    def test_legacy_player_slots_and_identity_migrate_without_progress_loss(self):
        self.board();role=self.b.profile();boards=role['activity']['rape_boards']
        first=boards[0];first['form_list']['1']=first['form_list'].pop('2')
        first['reward_claimed']=True
        for target in first['form_list']['1'].values():
            target['has_win']=True
            del target['npc_id'];del target['npc_player_id']
            target['name']='旧玩家'
        existing=next(iter(boards[1]['form_list']['2'].values()))
        key=existing['npc_id'];del existing['npc_player_id']
        del role['activity']['rape_recent_npcs']
        saved=copy.deepcopy(boards);self.b.save(role);self.board();after=self.b.profile()
        self.assertEqual(role['attachments'],after['attachments'])
        migrated=after['activity']['rape_boards'][0]
        self.assertTrue(migrated['reward_claimed'])
        self.assertEqual(list(migrated['form_list']['1']),list(saved[0]['form_list']['1']))
        for ident,t in migrated['form_list']['1'].items():
            self.assertTrue(t['has_win'])
            self.assertEqual(t['npc_player_id'],npc_players.catalog()[t['npc_id']]['profile']['role_id'])
            self.assertIn(t['npc_id'],after['activity']['rape_recent_npcs'])
            view=next(d for e,d in self.req(1039,des_type=1,des_id=int(ident)) if e==11)
            self.assertEqual(view['role_name'],t['name'])
        restored=next(iter(after['activity']['rape_boards'][1]['form_list']['2'].values()))
        self.assertEqual(restored['npc_id'],key)
        self.assertEqual(restored['npc_player_id'],npc_players.catalog()[key]['profile']['role_id'])
        from network_redirect.backend import Backend
        from pathlib import Path
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.board();self.assertEqual(after,self.b.profile())
