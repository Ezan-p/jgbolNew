"""1263 ascension/recycle/level limits, including real wire and persistence."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import formation as f, summon, journey, activity, activity_home as home
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode

ROOT = Path(__file__).resolve().parents[1]
TABLES = ('cortege_evolution.csv', 'cortege_evolve_config.csv', 'cortege_devolve.csv',
          'cortege_experience.csv', *(f'hole/{n}.csv' for n in (
              'main_building_config', 'garden_building_config', 'temple_config',
              'upgrade_building_materials', 'garden_grid_config',
              'temple_level_plus', 'temple_ext_prize')))


class HotupdateValues(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = f.load_rules()

    def fixture(self, quality=5):
        tid = next(t for t, r in f.BASES.items() if int(r['quality']) == quality)
        role = dict(level=99, attachments=[], corteges=[], summon={}, silver_coin=0)
        c = summon.companion(role, tid)
        c.update(culture_point=0, cur_exp=0, order=1)
        role['corteges'] = [c]
        home.storage(role)['build']['1'] = 50
        return role, c

    def test_original_tables_exact_and_complete(self):
        for name in TABLES:
            with self.subTest(table=name):
                self.assertEqual((ROOT/'analysis/configs/immortal_hotupdate'/name).read_bytes(),
                                 (ROOT/'analysis/evidence/hotupdate_gap_20261031/official_csv'/name).read_bytes())
        self.assertEqual(set(f.EVOLVE_COST), set(range(1, 500)))
        self.assertEqual(set(f.DEVOLVE), set(range(1, 500)))
        for q in range(1, 6):
            self.assertTrue(all((q, n) in f.EVOLVE_POINTS for n in range(1, 500)))
            self.assertEqual({n for quality, n in f.EXPERIENCE if quality == q}, set(range(1, 601)))
        self.assertEqual(f.EVOLVE_COST[499], 1200)
        self.assertEqual(int(f.DEVOLVE[499]['jiehun_count']), 312728)
        self.assertEqual(f.EXPERIENCE[5, 600], 6938176129)

    def test_every_extended_recycle_tier_all_categories(self):
        for quality in (4, 5):
            types = {int(row['category']): t for t, row in f.BASES.items() if int(row['quality']) == quality}
            for category, tid in types.items():
                for level in range(121, 500):
                    with self.subTest(quality=quality, category=category, level=level):
                        role, c = self.fixture(quality)
                        points = sum(f.EVOLVE_POINTS[quality, n] for n in range(1, level+1))
                        c.update(type=tid, evolve_level=level, culture_point=points-100+23, hp_plus=100)
                        summon.add_item(role, 1002, 3)
                        events = f.evolve(role, dict(flag=1, cortege_id=c['id']))
                        reward = events[0][1]['attach_list'][0]
                        item = f.ITEMS[reward['attach_type']]
                        self.assertEqual((int(item['quality']), int(item['sub_type'])), (quality, category))
                        self.assertEqual(reward['attach_count'], int(f.DEVOLVE[level]['jiehun_count']))
                        self.assertEqual((c['evolve_level'], c['culture_point'], c['hp_plus']), (0, 23, 0))
                        self.assertFalse(any(i['type_id'] == 1002 for i in role['attachments']))
                        before = copy.deepcopy(role)
                        with self.assertRaises(f.Rejected):
                            f.evolve(role, dict(flag=1, cortege_id=c['id']))
                        self.assertEqual(role, before)

    def test_caps_follow_buildings_and_role_boundary(self):
        role, c = self.fixture()
        for level, top in ((0,200),(20,300),(21,310),(30,400),(40,500),(50,600)):
            role['activity']['home']['build']['1'] = level
            role['cortege_limit_plus'] = 0  # stale cached bonus must not gate growth
            for q in range(1, 6):
                self.assertEqual(f.companion_level_cap(role, q), top)
        role['level'] = 79
        self.assertEqual(f.companion_level_cap(role, 5), 237)
        role['level'] = 80
        self.assertEqual(f.companion_level_cap(role, 5), 600)

    def test_recycle_restrictions_and_insufficient_souls(self):
        for quality in range(1, 6):
            role, c = self.fixture(quality)
            c['evolve_level'] = 299
            role['souls'] = {str(c['type']): f.EVOLVE_COST[300]-1}
            before = copy.deepcopy(role)
            with self.assertRaises(f.Rejected):
                f.evolve(role, dict(flag=0, cortege_id=c['id']))
            self.assertEqual(role, before)
            if quality < 4:
                summon.add_item(role, 1002, 3)
                before = copy.deepcopy(role)
                with self.assertRaises(f.Rejected):
                    f.evolve(role, dict(flag=1, cortege_id=c['id']))
                self.assertEqual(role, before)

    def test_books_and_pills_cross_all_new_levels_and_stop_at_600(self):
        for quality in range(1, 6):
            for flag, subtype in ((1, 99), (2, 100)):
                role, c = self.fixture(quality)
                c.update(level=300, culture_point=0)
                tid, row = next((t,r) for t,r in f.ITEMS.items() if int(r['main_type']) == 5
                               and int(r['sub_type']) == subtype and int(r['experience_plus']) > 0)
                need = sum(f.EXPERIENCE[quality, n] for n in range(300, 600))
                count = (need+int(row['experience_plus'])-1)//int(row['experience_plus'])
                summon.add_item(role, tid, count+1)
                req = dict(flag=flag, first_send=True, cortege_id=c['id'], roll_count=1,
                           roll_list=[dict(type_id=tid, count=count)])
                f.feed(role, req, self.rules)
                self.assertEqual((c['level'], c['cur_exp']), (600, 0))
                self.assertEqual(c['culture_point'], f.level_culture_points(quality, 300, 600, self.rules))
                self.assertEqual(c['next_exp'], f.EXPERIENCE[quality, 600])
                before = copy.deepcopy(role)
                with self.assertRaises(f.Rejected):
                    f.feed(role, req, self.rules)
                self.assertEqual(role, before)

    def test_battle_experience_crosses_old_caps(self):
        for level in (199, 299, 399, 599, 600):
            role, c = self.fixture()
            c.update(level=level, cur_exp=0)
            with patch('network_redirect.progression.add_exp'), patch('network_redirect.progression.strength_bonus', return_value=(0,0)):
                journey.experience(role, dict(strenth_consume='0', exp=str(f.EXPERIENCE[5,level]), money='0'),
                                   True, journey.load_rules(), self.rules)
            self.assertEqual(c['level'], min(600, level+1))
            self.assertEqual(c['cur_exp'], 0)


class HotupdateWire(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a,**k: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 100000
        self.state = {'authenticated': True}
        clock = patch('network_redirect.backend.time.time', return_value=1793419200)
        clock.start(); self.addCleanup(clock.stop)
        role = self.b.profile()
        role['level'] = 99
        activity.prepare(role, 1793419200, self.b.activity_rules)
        home.state(role, 1793419200, self.b.activity_rules)
        c = role['corteges'][0]
        c.update(type=5002, level=599, evolve_level=498, culture_point=126780,
                 cur_exp=0, level_culture_version=3)
        role['souls'] = {'5002': 1200}
        role['activity']['home']['build'].update({'1':50,'2':49,'3':49})
        role['activity']['home']['level'] = 2
        summon.add_item(role, 1002, 3)
        f.prepare(role, self.b.formation_rules)
        self.cid = c['id']
        self.b.save(role)

    def request(self, mid, ok=True, **data):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **data))
        self.replies = self.b.respond(self.packet, self.state)
        decoded = [decode(p) for p in self.replies]
        errors = [login_fields(d['data']) for m,_,d in decoded if m == 2998 and d['id'] == 55]
        self.assertEqual(bool(errors), not ok, errors)
        return decoded

    def test_evolve_replay_restart_large_potential_and_recycle(self):
        decoded = self.request(1084, flag=0, cortege_id=self.cid)
        r = self.b.profile(); c = r['corteges'][0]
        self.assertEqual((c['evolve_level'], c['culture_point']), (499,127180))
        self.assertTrue(any(m == 1032 and any(x['type']==90 and x['value']==127180 for x in d['attr_list']) for m,_,d in decoded))
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.b.profile(), r)
        self.request(1084, ok=False, flag=0, cortege_id=self.cid)
        self.assertEqual(self.b.profile(), r)
        self.b.close(); self.b = Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile()['corteges'][0]['culture_point'],127180)
        self.request(1084, flag=1, cortege_id=self.cid)
        c = self.b.profile()['corteges'][0]
        self.assertEqual((c['evolve_level'],c['culture_point']),(0,0))
        before = self.b.profile()
        self.request(1084,ok=False,flag=1,cortege_id=self.cid)
        self.assertEqual(self.b.profile(),before)

    def test_large_experience_feed_and_restart(self):
        r=self.b.profile();c=r['corteges'][0]
        tid=next(t for t,row in f.ITEMS.items() if int(row['main_type'])==5 and int(row['sub_type'])==99 and int(row['experience_plus'])>0)
        c['cur_exp']=f.EXPERIENCE[5,599]-1
        summon.add_item(r,tid,2);self.b.save(r)
        decoded=self.request(1059,flag=1,first_send=True,cortege_id=self.cid,roll_count=1,roll_list=[dict(type_id=tid,count=1)])
        wire=next(d['cortege_list'][0] for m,_,d in decoded if m==1034)
        self.assertEqual((wire['level'],wire['next_exp']),(600,6938176129))
        r=self.b.profile()
        self.request(1059,ok=False,flag=1,first_send=True,cortege_id=self.cid,roll_count=1,roll_list=[dict(type_id=tid,count=1)])
        self.assertEqual(r,self.b.profile())
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(self.b.profile()['corteges'][0]['level'],600)

    def test_building_20_to_50_with_original_costs_and_prerequisites(self):
        r=self.b.profile();s=r['activity']['home']
        s['build'].update({'1':20,'2':20,'3':20});self.b.save(r)
        for target in range(21,51):
            r=self.b.profile();r['silver_coin']=2000000000
            summon.add_item(r,1362,100000);self.b.save(r)
            for typ in (1,2,3):
                funded=self.b.profile();funded['silver_coin']=2000000000;self.b.save(funded)
                before=self.b.profile();row=home.UPGRADE[typ,target]
                decoded=self.request(1348,id=2,data=summon.lua(dict(building_type=typ)))
                after=self.b.profile()
                silver=sum(int(p.split('|')[2]) for p in row['cost'].split('/') if p.startswith('12|'))
                self.assertEqual(before['silver_coin']-after['silver_coin'],silver)
                self.assertEqual(after['activity']['home']['build'][str(typ)],target)
            self.assertEqual(f.companion_level_cap(after,5),200+int(home.BUILD[1][target]['coretege_limit_plus']))
        before=self.b.profile()
        self.request(1348,ok=False,id=2,data=summon.lua(dict(building_type=1)))
        self.assertEqual(self.b.profile(),before)

    def test_failed_recycle_and_upgrade_are_atomic(self):
        r=self.b.profile();r['attachments']=[i for i in r['attachments'] if i['type_id']!=1002]
        self.b.save(r);before=self.b.profile()
        self.request(1084,ok=False,flag=1,cortege_id=self.cid)
        self.assertEqual(self.b.profile(),before)
        r=self.b.profile();r['activity']['home']['build'].update({'1':20,'2':19,'3':20})
        r['silver_coin']=2000000000;summon.add_item(r,1362,100000);self.b.save(r);before=self.b.profile()
        self.request(1348,ok=False,id=2,data=summon.lua(dict(building_type=1)))
        self.assertEqual(self.b.profile(),before)

    def test_high_building_dependencies_and_unchanged_other_building_caps(self):
        r=self.b.profile();s=r['activity']['home']
        s['build'].update({'2':50,'3':50,'4':20,'5':20})
        s['plants']={'1':dict(level=29)}
        s.update(pray_count=6,pray_time=0)
        r['gold_coin']=1000;self.b.save(r)
        self.request(1348,id=9,data='{plant_grid=1}')
        self.assertEqual(self.b.profile()['activity']['home']['plants']['1']['level'],30)
        self.request(1348,id=11,data='{}')
        self.assertEqual(self.b.profile()['activity']['home']['pray_count'],7)
        for typ in (4,5):
            before=self.b.profile()
            self.request(1348,ok=False,id=2,data=summon.lua(dict(building_type=typ)))
            self.assertEqual(self.b.profile(),before)
