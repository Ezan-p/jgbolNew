"""1263 catalogue, durable milestones, real refinement and wire boundaries."""
import copy
import csv
import unittest
from pathlib import Path
from network_redirect import achievements as a, fate_rebuild as fr, formation as f, summon
from network_redirect.backend import Backend
from network_redirect.protocol import decode
import test_achievements as baseline
NOW = baseline.NOW

ROOT = Path(__file__).resolve().parents[1]


class HotupdateTests(unittest.TestCase):
    setUp = baseline.AchievementTests.setUp
    request = baseline.AchievementTests.request
    row = baseline.AchievementTests.row

    def test_exact_official_catalogue_and_only_intended_diff(self):
        def read(path):
            with path.open(encoding='utf-8-sig', newline='') as stream:
                return {int(r['id']): r for r in csv.DictReader(stream)}
        official = read(ROOT/'analysis/evidence/hotupdate_gap_20261031/official_csv/achievements_config.csv')
        old = read(ROOT/'analysis/configs/achievements_config.csv')
        self.assertEqual(a.CATALOG, official)
        self.assertEqual(set(official)-set(old), set(range(580,591)))
        changed = {i for i in old if old[i] != official[i]}
        self.assertEqual(changed, {563,564,565})
        for i in changed:
            self.assertEqual(dict(old[i], max_repeatable_times='400'), official[i])
        self.assertEqual(sum(int(a.OPEN[i]['plus_point']) for i in range(580,591)), 2150)

    def companion(self, role, active=1):
        role.setdefault("summon", {"next_id": 90000})
        c = summon.companion(role, 5022)
        c.update(reborn_layer=9, fate_rebullding_state=active)
        role['corteges'].append(c)
        return c

    def levels(self, c, parts, total):
        for p in parts:
            c[fr.PARTS[p]+'_level'] = min(100, total)
            c[fr.PARTS[p]+'_stars'] = fr.star_count(p)-1
            total -= min(100, total)

    def test_each_threshold_completed_layers_not_partial_stars(self):
        for ident, limit in a.FATE_THRESHOLDS.items():
            with self.subTest(ident=ident):
                role = dict(role_id=1, corteges=[])
                c = self.companion(role)
                parts = range(1,4) if ident <= 585 else range(4,11)
                self.levels(c, parts, limit-1)
                a.refresh(role, NOW)
                self.assertEqual(self.row(role, ident)['times'], 0)
                self.levels(c, parts, limit)
                a.refresh(role, NOW)
                self.assertEqual(self.row(role, ident)['times'], 1)
                a.refresh(role, NOW)
                self.assertEqual(self.row(role, ident)['times'], 1)

    def test_no_cross_companion_sum_inactive_progress_or_reset_farming(self):
        role = dict(role_id=1, corteges=[])
        for _ in range(2):
            c = self.companion(role)
            self.levels(c, range(1,4), 15)
        inactive = self.companion(role, active=0)
        self.levels(inactive, range(1,4), 300)
        a.refresh(role, NOW)
        self.assertEqual(self.row(role, 580)['times'], 2)
        self.assertEqual(self.row(role, 581)['times'], 0)
        c = role['corteges'][0]
        self.levels(c, range(1,4), 300)
        a.refresh(role, NOW)
        point = role['tao_point']
        self.levels(c, range(1,4), 0)
        a.refresh(role, NOW)
        self.assertEqual(role['tao_point'], point)
        self.levels(c, range(1,4), 300)
        a.refresh(role, NOW)
        self.assertEqual(role['tao_point'], point)
        role['corteges'].remove(c)
        a.refresh(role, NOW)
        self.assertEqual(role['tao_point'], point)

    def test_24_cap_all_eleven_rewards_and_migration_idempotency(self):
        role = dict(role_id=1, corteges=[])
        for _ in range(25):
            c = self.companion(role)
            self.levels(c, range(1,4), 300)
            self.levels(c, range(4,11), 500)
        a.refresh(role, NOW)
        for ident in range(580,591):
            self.assertEqual(self.row(role, ident), dict(id=ident, times=24, progress=1))
        self.assertEqual(sum(24*int(a.OPEN[i]['plus_point']) for i in range(580,591)), 51600)
        before = copy.deepcopy(role)
        a.refresh(role, NOW+86400)
        self.assertEqual(role['tao_point'], before['tao_point'])
        self.assertEqual(a.rows(role), a.rows(before))

    def test_real_activation_failure_replay_and_restart(self):
        role = self.b.profile(); role.update(reborn_layer=4)
        c = self.companion(role, active=0); cid = c['id']
        self.b.save(role)
        before = self.b.profile()
        self.request(1357, id=3, data=summon.lua(dict(cortege_id=cid)))
        self.assertEqual(before, self.b.profile())
        summon.add_item(role, 1371, 20); self.b.save(role)
        out = self.request(1357, id=3, data=summon.lua(dict(cortege_id=cid)))
        saved = self.b.profile()
        self.assertEqual(self.row(saved, 580)['times'], 1)
        self.assertTrue(any(m == 1066 and dict(id=580,times=1,progress=0) in d['achievements'] for m,d in out))
        self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
        self.request(1357, id=3, data=summon.lua(dict(cortege_id=cid)))
        self.assertEqual(saved, self.b.profile())
        other = Backend(Path(self.tmp.name), 0, lambda *args, **kw: None)
        try: self.assertEqual(self.row(other.profile(),580)['times'],1)
        finally: other.close()

    def test_real_node_crosses_threshold_and_reset_keeps_award(self):
        role = self.b.profile(); role['reborn_layer']=4
        c = self.companion(role); cid=c['id']
        c.update(spirit_heaven_level=29, spirit_heaven_stars=8)
        raw = list(map(int,fr.COSTS[1,29,9].split('|')))
        self.assertEqual(raw[0],3)
        materials=dict(zip(raw[1::2],raw[2::2]))
        for tid,n in materials.items(): summon.add_item(role,tid,n)
        self.b.save(role)
        self.assertEqual(self.row(self.b.profile(),581)['times'],0)
        out=self.request(1357,id=0,data=summon.lua(dict(cortege_id=cid,soul_part=1,material_list=materials)))
        self.assertEqual(self.row(self.b.profile(),581)['times'],1)
        self.assertTrue(any(m==1066 and any(r['id']==581 for r in d['achievements']) for m,d in out))
        self.request(1357,id=4,data=summon.lua(dict(cortege_id=cid)))
        self.assertEqual(self.row(self.b.profile(),581)['times'],1)

    def test_all_stones_200_to_400_actual_refinements_and_no_401(self):
        for kind in (1,2,3):
            with self.subTest(kind=kind):
                role=self.b.profile(); role.update(level=99,reborn_layer=4)
                for tid in (1333,1369): summon.add_item(role,tid,100000)
                stone=dict(id=f.new_id(role),attach_type=5,type_id=1089+kind,count=1,level=11)
                role['attachments'].append(stone)
                a.state(role)['totals'][str(562+kind)]=199
                self.b.save(role)
                for level in (12,13,14):
                    role=self.b.profile()
                    mat=dict(id=f.new_id(role),attach_type=5,type_id=1089+kind,
                             count=2 if level==14 else 1,level=level-1)
                    role['attachments'].append(mat)
                    if level>=13: a.state(role)['observed'][f"{562+kind}:{mat['id']}"]=1
                    self.b.save(role)
                    out=self.request(1054,flag=5,des_id=stone['id'],stone_pos=0,equip_order=0,src_count=0,src_list=[])
                    saved=self.b.profile()
                    self.assertEqual(self.row(saved,562+kind)['times'],199+level-11)
                    self.assertEqual(self.b.respond(self.packet,{'authenticated':True}),self.replies)
                    self.assertEqual(self.b.profile(),saved)
                self.request(1054,flag=5,des_id=stone['id'],stone_pos=0,equip_order=0,src_count=0,src_list=[])
                self.assertEqual(self.b.profile(),saved)
                a.add(saved,562+kind,197);a.finalize(saved)
                self.assertEqual(self.row(saved,562+kind)['times'],399)
                a.add(saved,562+kind,1);a.finalize(saved)
                point=saved['tao_point'];a.add(saved,562+kind,1);a.finalize(saved)
                self.assertEqual(self.row(saved,562+kind),dict(id=562+kind,times=400,progress=1))
                self.assertEqual(saved['tao_point'],point)

    def test_old_cap_observation_recovery_and_unknown_history(self):
        role=dict(role_id=1,corteges=[],attachments=[])
        s=a.state(role);s['totals']['563']=200
        s['observed'].update({f'563:{n}':1 for n in range(230)})
        a.refresh(role,NOW)
        self.assertEqual(self.row(role,563)['times'],230)
        a.refresh(role,NOW)
        self.assertEqual(self.row(role,563)['times'],230)
        role['attachments']=[dict(id=9999,attach_type=5,type_id=1091,count=1,level=14)]
        a.refresh(role,NOW)
        self.assertEqual(self.row(role,564)['times'],1)  # no invented two historical upgrades

    def test_empty_delta_and_overflow_delta_and_other_role(self):
        role=self.b.profile(); before=copy.deepcopy(role)
        self.assertEqual(a.packets(role,previous=before),[])
        for ident,row in a.OPEN.items(): a.add(role,ident,int(row['full_progress']))
        a.finalize(role)
        packets=[decode(p) for p in a.packets(role,new=1,previous=before)]
        chunks=[d for mid,_,d in packets if mid==1066]
        self.assertGreater(sum(d['achievement_count'] for d in chunks),255)
        role['role_id']=200; self.b.save(role,'friend')
        out=self.request(1067,des_role_id=200,flag=0)
        self.assertEqual(sum(d['achievement_count'] for mid,d in out if mid==1066),258)

    def test_legacy_high_stone_stack_split_does_not_mint_first_awards(self):
        from network_redirect import equipment
        role=self.b.profile()
        stone=dict(id=f.new_id(role),attach_type=5,type_id=1090,count=3,level=12)
        role['attachments'].append(stone)
        a.refresh(role,NOW)
        before=self.row(role,563)['times']
        equipment.split_one(role,stone)
        a.refresh(role,NOW)
        self.assertEqual(self.row(role,563)['times'],before)
        rest=next(x for x in role['attachments'] if x['type_id']==1090 and x['id']!=stone['id'])
        equipment.split_one(role,rest)
        a.refresh(role,NOW)
        self.assertEqual(self.row(role,563)['times'],before)

    def test_failed_refinement_and_ascension_do_not_count_as_refinement(self):
        role=self.b.profile();role.update(level=99,reborn_layer=4)
        stone=dict(id=f.new_id(role),attach_type=5,type_id=1090,count=2,level=10)
        role['attachments'].append(stone);summon.add_item(role,1333,3)
        self.b.save(role)
        self.request(1054,flag=5,des_id=stone['id'],stone_pos=0,equip_order=0,src_count=0,src_list=[])
        saved=self.b.profile()
        self.assertEqual(next(x for x in saved['attachments'] if x['id']==stone['id'])['level'],11)
        self.assertEqual(self.row(saved,563)['times'],0)
        self.request(1054,flag=5,des_id=stone['id'],stone_pos=0,equip_order=0,src_count=0,src_list=[])
        self.assertEqual(self.b.profile(),saved)

    def test_real_400th_then_401st_refinement_and_restart(self):
        role=self.b.profile();role.update(level=99,reborn_layer=4)
        stone=dict(id=f.new_id(role),attach_type=5,type_id=1092,count=2,level=11)
        role['attachments'].append(stone);summon.add_item(role,1369,100)
        # Existing level-12 material has already been credited.
        mat=dict(id=f.new_id(role),attach_type=5,type_id=1092,count=1,level=12)
        role['attachments'].append(mat)
        a.state(role)['observed'][f"565:{mat['id']}"]=1
        a.state(role)['totals']['565']=399
        self.b.save(role)
        self.request(1054,flag=5,des_id=stone['id'],stone_pos=0,equip_order=0,src_count=0,src_list=[])
        self.assertEqual(self.row(self.b.profile(),565)['times'],400)
        point=self.b.profile()['tao_point']
        self.request(1054,flag=5,des_id=stone['id'],stone_pos=0,equip_order=0,src_count=0,src_list=[])
        saved=self.b.profile()
        self.assertEqual(next(x for x in saved['attachments'] if x['id']==stone['id'])['level'],13)
        self.assertEqual(self.row(saved,565)['times'],400)
        self.assertEqual(saved['tao_point'],point)
        other=Backend(Path(self.tmp.name),0,lambda *args,**kw:None)
        try: self.assertEqual(self.row(other.profile(),565)['times'],400)
        finally: other.close()
