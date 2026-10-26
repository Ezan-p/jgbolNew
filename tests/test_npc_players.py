import copy
import json
from pathlib import Path
import tempfile
import unittest
from network_redirect import npc_players as npc, role_profile, formation, combat, reborn_stars
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class NpcPlayerTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        self.b=Backend(Path(tmp.name),18770,lambda *a,**k:None);self.addCleanup(self.b.close)
        self.b.profile();self.serial=1000

    def request(self,mid,**data):
        self.serial+=1
        self.packet=encode(mid,dict(serial_num=self.serial,**data))
        self.replies=self.b.respond(self.packet,dict(authenticated=True))
        return [(m,d) for m,_,d in map(decode,self.replies)]

    def event(self,out,ident):
        return next(login_fields(d['data']) for m,d in out if m==2998 and d['id']==ident)

    def database(self):
        return self.b.db.execute('SELECT account,data FROM roles ORDER BY account').fetchall()

    def test_all_identities_legal_unique_and_bound_to_both_versions(self):
        entries=list(npc.catalog().values())
        self.assertEqual(len(entries),1725)
        self.assertEqual(sum(e['version']=='v1' for e in entries),240)
        self.assertEqual(len({e['profile']['role_id'] for e in entries}),1725)
        self.assertEqual(len({e['profile']['role_name'] for e in entries}),1725)
        self.assertEqual({e['profile']['head_type'] for e in entries},role_profile.HEADS)
        for entry in entries:
            p=entry['profile']
            self.assertTrue(2<=len(p['role_name'])<=7 and len(p['role_name'].encode())<32)
            self.assertLessEqual(int(role_profile.RUNES[p['cur_genius_type']]['open_level']),p['level'])
            self.assertEqual(npc.resolve(p['role_id']),entry['npc_id'])
            self.assertEqual(npc.resolve(entry['legacy_role_id']),entry['npc_id'])
        for value in (True,0,-1,700000001.5,float('nan'),float('inf'),'700000001'):
            self.assertIsNone(npc.resolve(value))

    def test_search_pagination_exact_name_and_both_id_types(self):
        baseline=self.database();seen=set()
        for page in (1,2):
            out=self.request(1091,search_type=1,search_index=page,search_string='36')
            result=next(d for m,d in out if m==1092)
            self.assertEqual(result['result'],1)
            ids={p['id'] for p in result['player_list']}
            self.assertFalse(seen&ids);seen|=ids
            self.assertTrue(all(p['level']==36 for p in result['player_list']))
        self.assertEqual(len(seen),30)
        self.assertEqual(next(d for m,d in self.request(1091,search_type=1,search_index=3,search_string='36') if m==1092)['result'],2)
        entry=next(iter(npc.catalog().values()))
        for query in (entry['profile']['role_name'],str(entry['profile']['role_id']),str(entry['legacy_role_id']),entry['npc_id']):
            result=next(d for m,d in self.request(1091,search_type=2,search_index=1,search_string=query) if m==1092)
            self.assertEqual([p['id'] for p in result['player_list']],[entry['profile']['role_id']])
        self.assertEqual(self.database(),baseline)
        self.assertEqual(self.b.respond(self.packet,dict(authenticated=True)),self.replies)

    def test_native_full_lineup_includes_actual_equipment_and_supports(self):
        baseline=self.database()
        for key in ('npc_v1_l01_t5_attack','npc_v1_l99_t1_attack',
                    next(e['npc_id'] for e in npc.catalog().values() if e['version']=='v2' and e['profile']['level']==99 and e['profile']['tier']=='T1')):
            entry=npc.catalog()[key];n=npc.get(key);r=n['role']
            for ident in (entry['legacy_role_id'],entry['profile']['role_id']):
                d=self.event(self.request(1039,des_id=ident,des_type=1,flag=2,fight_id=0),11)
                self.assertEqual(d['role_id'],entry['profile']['role_id'])
                self.assertEqual(d['head_type'],entry['profile']['head_type'])
                self.assertEqual(d['role_name'],entry['profile']['role_name'])
                members=[c for c in r['corteges'] if c['order']]
                chars=list(d['cortege_list'].values())
                self.assertEqual(len(chars),len(members))
                self.assertEqual(sum(c['combat_power'] for c in chars),r['role_combat_power'])
                self.assertEqual(len(d['cheer_cortege']),sum(bool(c.get('cheer_order')) for c in r['corteges']))
                self.assertEqual(len(d['equip_list']),sum(i['attach_type']==5 and i.get('equip_order',0)>0 and int(formation.ITEMS[i['type_id']]['main_type']) in (1,2,3) for i in r['attachments']))
                self.assertEqual(len(d['skill_list']),sum(i['attach_type']==6 and i.get('equip_order',0)>0 and i.get('equip_pos',0)>0 for i in r['attachments']))
                self.assertEqual(sum(len(v) for v in d['ext_skill_list'].values()),sum(i['type_id'] in combat.ESSENCES and i.get('owner_id',0)>0 for i in r['attachments']))
                self.assertEqual(sum(len(v) for v in d['ext_star_list'].values()),sum(i['type_id'] in reborn_stars.STARS and i.get('owner_id',0)>0 for i in r['attachments']))
                self.assertLess(len(self.replies[0]),32768)
        self.assertEqual(self.database(),baseline)

    def test_other_profile_titles_achievements_never_change_self(self):
        entry=next(iter(npc.catalog().values()));ident=entry['profile']['role_id'];baseline=self.database()
        title=next(d for m,d in self.request(1078,des_id=ident,flag=2) if m==1077)
        self.assertEqual((title['role_id'],title['wear_id'],title['title_count']),(ident,0,0))
        result=next(d for m,d in self.request(1067,des_role_id=ident,flag=1) if m==1066)
        self.assertEqual(result['role_id'],ident)
        self.assertEqual(self.database(),baseline)

    def test_collision_stale_invalid_and_unauthenticated(self):
        e=next(iter(npc.catalog().values()));ident=e['profile']['role_id']
        r=self.b.profile('collision');r['role_id']=ident;self.b.save(r,'collision')
        baseline=self.database()
        self.event(self.request(1039,des_id=ident,des_type=1),55)
        found=next(d for m,d in self.request(1091,search_type=2,search_index=1,search_string=str(ident)) if m==1092)
        self.assertEqual(found['result'],2)
        self.event(self.request(1039,des_id=700000000,des_type=1),55)
        self.event(self.request(1039,des_id=ident+0.5,des_type=1),55)
        for typ,index,query in ((0,1,''),(1,0,'36'),(1,1,'100'),(1,1,'abc')):
            self.event(self.request(1091,search_type=typ,search_index=index,search_string=query),55)
        stale=encode(1091,dict(serial_num=self.serial,search_type=1,search_index=1,search_string='99'))
        self.assertEqual(decode(self.b.respond(stale,dict(authenticated=True))[0])[2]['id'],55)
        with self.assertRaises(ValueError):self.b.respond(self.packet,{})
        self.assertEqual(self.database(),baseline)

    def test_cached_snapshots_and_activity_aliases_are_immutable(self):
        from network_redirect import activity_rank,activity_party,activity_land_npc
        for provider in (activity_rank,activity_party,activity_land_npc):
            key,n=next(iter(provider.catalog().items()));before=copy.deepcopy(n)
            d=npc.inspection_data(n,scene_id=930001,count=4)
            self.assertEqual(d['npc_scene_id'],930001)
            self.assertEqual(d['role_id'],n['player_profile']['role_id'])
            self.assertEqual(d['npc_player_id'],n['player_profile']['role_id'])
            self.assertTrue(all(c['order']<=4 for c in d['cortege_list']))
            d['npc_profile']['role_name']='测试改名'
            self.assertEqual(provider.catalog()[key],before)
            original=npc.source_file(npc.catalog()[n['npc_id']]['source_file'])[n['npc_id']]
            self.assertEqual(original['role']['role_id'],n['legacy_role_id'])


if __name__=='__main__':unittest.main()
