"""1263 contracts, persisted rewards and end-to-end star material chain."""
import copy
import csv
import unittest
from pathlib import Path
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity_babel as b, activity_babel_npc as npc
from network_redirect import summon, formation, reborn_stars as stars, equipment_crafting as craft
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode, encode


class HotupdateTables(unittest.TestCase):
    def test_active_original_tables_and_narrow_additions(self):
        root = Path(__file__).resolve().parents[1]
        original = root / 'analysis/evidence/hotupdate_gap_20261031/official_csv'
        for name in summon.BABEL_HOTUPDATE_TABLES:
            with (original/name).open(encoding='utf-8-sig', newline='') as f:
                self.assertEqual(summon.rows(name), list(csv.DictReader(f)), name)
        for name, key in [('item_base.csv','type_id'),('item_name.csv','Ftype_id'),
                          ('material_transform.csv','category'),('material_transform_index.csv','category')]:
            expected = {'1376','1377','1378'} if name.startswith('item_') else {'10'}
            with (original/name).open(encoding='utf-8-sig',newline='') as f:
                rows = [r for r in csv.DictReader(f) if r[key] in expected]
            self.assertEqual([r for r in summon.rows(name) if r[key] in expected], rows)
        self.assertEqual(b.MAX_FLOOR, 70)
        self.assertEqual(len(stars.TRANSFORMS), 30)
        self.assertEqual(set(b.STAGES), {20,40,60,70})

    def test_new_protocol_uses_double_id_and_byte_subtype(self):
        request = dict(serial_num=100, star_id=2**40+7, des_type=6)
        self.assertEqual(decode(encode(1359,request))[2], request)


class BabelHotupdateTests(ActivityCase):
    def call(self, op=1, **data):
        out = self.req(1353, id=op, data=summon.lua(data));self.ok(out)
        return [v for e,v in out if e == 203]

    def saved(self): return self.b.profile()['activity']['babel']

    def reject(self, mid=1353, **kw):
        before=self.b.profile()
        self.assertEqual(self.req(mid,**kw)[0][0],55)
        self.assertEqual(self.b.profile(),before)

    def seed_tower(self, floor, **changes):
        self.call()
        role=self.b.profile();s=role['activity']['babel']
        s.update(cur_floor=floor,history_floor=floor,energy=10000,participated=True,**changes)
        b.generate(s);self.b.save(role)

    def stair(self, floor, secret=False):
        role=self.b.profile();s=role['activity']['babel']
        if secret:s=s['secret_run']
        s['cur_floor']=floor;b.generate(s)
        for row in s['floors'][str(floor)]:
            for cell in row:
                if cell['elem_type']==9:cell['elem_type']=0
        s['locale']=dict(row=5,column=7);self.b.save(role)
        return self.call(13 if secret else 2,target_pos=dict(row=5,column=8))

    def test_old_completed_60_save_opens_61_without_refilling_loot(self):
        self.seed_tower(60,max_floor=60,complete=True)
        role=self.b.profile();s=role['activity']['babel'];s['floors']['60'][4][7]['elem_type']=0
        s['floors']['60'][0][1]['elem_type']=0;self.b.save(role)
        self.call();self.assertEqual(self.saved()['max_floor'],70)
        self.assertFalse(self.saved()['complete'])
        self.assertEqual(self.saved()['floors']['60'][0][1]['elem_type'],0)
        self.stair(60);self.assertEqual(self.saved()['cur_floor'],61)
        self.assertEqual(self.saved()['history_floor'],61)

    def test_61_to_70_and_final_completion_once(self):
        self.seed_tower(61)
        for floor in range(61,70):
            self.stair(floor);self.assertEqual(self.saved()['cur_floor'],floor+1)
        result=self.stair(70)
        self.assertTrue(result[0]['data']['completed_now'])
        before=self.b.profile()['attachments']
        self.call(2,target_pos=dict(row=5,column=7))
        result=self.call(2,target_pos=dict(row=5,column=8))
        self.assertFalse(result[0]['data']['completed_now'])
        self.assertEqual(before,self.b.profile()['attachments'])
        self.assertEqual(self.saved()['cur_floor'],70)

    def test_thursday_cumulative_stage_mail_freeze_claim_and_reset(self):
        self.call();role=self.b.profile();s=role['activity']['babel']
        # Start in the next participation week, before its Thursday cutoff.
        monday=npc.start(s['week']+1,self.b.activity_rules)
        with patch('network_redirect.backend.time.time',return_value=monday):
            self.call();self.seed_tower(70)
        cutoff=monday+3*86400
        with patch('network_redirect.backend.time.time',return_value=cutoff-1):
            self.call();self.assertFalse(any(k.startswith('babel-stage-') for k in self.b.profile()['welfare'].get('mails',{})))
        with patch('network_redirect.backend.time.time',return_value=cutoff):
            self.call();role=self.b.profile();s=role['activity']['babel'];week=s['week']
            mails=role['welfare']['mails']
            for stage in (20,40,60,70):
                self.assertEqual(mails[f'babel-stage-{week}-{stage}']['prizes'],b.STAGES[stage])
            self.assertEqual(mails[f'babel-supply-{week}']['prizes'],[[5,1376,1,1],[5,1377,1,1]])
            frozen=copy.deepcopy(s['frozen_top'])
            self.call();self.assertEqual(mails,self.b.profile()['welfare']['mails'])
            mail=mails[f'babel-stage-{week}-20']
            self.ok(self.req(1103,mail_id=mail['mail_id'],flag=1))
            count=b.item_count(self.b.profile(),20000)
            self.req(1103,mail_id=mail['mail_id'],flag=1)
            self.assertEqual(count,b.item_count(self.b.profile(),20000))
        with patch('network_redirect.backend.time.time',return_value=cutoff+86400):
            self.call();self.assertEqual(self.saved()['frozen_top'],frozen)
        with patch('network_redirect.backend.time.time',return_value=monday+7*86400):
            self.call();self.assertEqual(self.saved()['history_floor'],1)
            self.assertEqual(self.saved()['last_top'],frozen)
            self.assertEqual(len([k for k in self.b.profile()['welfare']['mails'] if k.startswith('babel-stage-')]),4)

    def test_progress_after_cutoff_does_not_retroactively_earn_stage(self):
        self.call();self.seed_tower(70)
        self.call()
        self.assertEqual(self.saved()['frozen_mine']['history_floor'],1)
        monday=npc.start(self.saved()['week']+1,self.b.activity_rules)
        with patch('network_redirect.backend.time.time',return_value=monday):self.call()
        self.assertFalse(any(k.startswith('babel-stage-') for k in self.b.profile()['welfare'].get('mails',{})))

    def test_secret_ticket_entry_query_restart_and_invalid_requests(self):
        self.assertNotIn('dungeon',self.call(12)[0]['data'])
        self.reject(id=14,data=summon.lua(dict(floor=1004)))
        role=self.b.profile();summon.add_item(role,1377,3);self.b.save(role)
        for floor in (1,1002,1015,1016,True):self.reject(id=14,data=summon.lua(dict(floor=floor)))
        data=self.call(14,floor=1004)[0]
        self.assertEqual(data['id'],12);self.assertEqual(data['data']['max_floor'],1006)
        self.assertEqual(b.item_count(self.b.profile(),1377),2)
        after=self.b.profile()
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(after,self.b.profile())
        self.call(13,target_pos=dict(row=1,column=2))
        saved=copy.deepcopy(self.saved()['secret_run'])
        self.call(12);self.assertEqual(self.saved()['secret_run'],saved)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.call(12);self.assertEqual(self.saved()['secret_run'],saved)
        self.call(14,floor=1004)
        self.assertEqual(self.saved()['secret_run']['floors']['1004'][0][1]['elem_type'],20005)
        self.assertEqual(b.item_count(self.b.profile(),1377),1)

    def test_secret_unlimited_resources_three_floors_isolated_from_tower(self):
        self.call();role=self.b.profile();summon.add_item(role,1377,1);self.b.save(role)
        normal=copy.deepcopy(self.saved()['floors'])
        self.call(14,floor=1010)
        role=self.b.profile();s=role['activity']['babel']['secret_run'];s.update(life=0,energy=0)
        self.b.save(role)
        self.call(13,target_pos=dict(row=1,column=2))
        self.assertEqual(self.saved()['secret_run']['energy'],0)
        for floor in (1010,1011,1012):self.stair(floor,True)
        s=self.saved()['secret_run'];self.assertEqual(s['cur_floor'],1012);self.assertTrue(s['complete'])
        self.assertEqual(normal,self.saved()['floors']);self.assertEqual(self.saved()['history_floor'],1)
        self.assertEqual(self.saved()['energy'],100)
        before=self.b.profile()['attachments']
        self.call(13,target_pos=dict(row=5,column=7))
        self.call(13,target_pos=dict(row=5,column=8))
        self.assertEqual(before,self.b.profile()['attachments'])

    def test_secret_real_fight_does_not_require_or_reduce_hp_energy(self):
        self.call();role=self.b.profile();summon.add_item(role,1377,1);self.b.save(role)
        self.call(14,floor=1001)
        role=self.b.profile();s=role['activity']['babel']['secret_run'];s.update(life=0,energy=0)
        s['locale']=dict(row=1,column=2);self.b.save(role)
        self.call(13,target_pos=dict(row=1,column=3))
        self.assertEqual(self.saved()['secret_run']['life'],0)
        self.assertEqual(self.saved()['secret_run']['energy'],0)
        self.assertTrue(any(mid==1027 for mid,_,_ in self.decoded))


class FateStarHotupdateTests(ActivityCase):
    def add(self,tid,n=1,**kw):
        role=self.b.profile();ident=formation.new_id(role)
        role['attachments'].append(dict(id=ident,attach_type=5,type_id=tid,count=n,level=1,**kw))
        self.b.save(role);return ident

    def reject(self,mid,**kw):
        before=self.b.profile();self.assertEqual(self.req(mid,**kw)[0][0],55)
        self.assertEqual(self.b.profile(),before)

    def test_attribute_conversion_cost_and_duplicate_request(self):
        for source,cost in ((13301,0),(14301,200)):
            ident=self.add(source);self.add(1376)
            before=self.b.profile()
            with patch.object(stars.secrets,'choice',side_effect=lambda pool:pool[-1]):
                out=self.req(1359,star_id=ident,des_type=6);self.ok(out)
            target=out[-1][1]['new_star_type']
            self.assertEqual(out[-1][1]['result'],0)
            self.assertIn(target,[source+6,source+7,source+8,source+9])
            after=self.b.profile();self.assertEqual(after['gold_coin'],before['gold_coin']-cost)
            self.assertEqual(b.item_count(after,1376),b.item_count(before,1376)-1)
            self.assertNotIn(ident,[i['id'] for i in after['attachments']])
            self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
            self.assertEqual(after,self.b.profile())
            self.assertTrue(any(mid==1035 for mid,_,_ in self.decoded))

    def test_reject_invalid_conversion_without_debit(self):
        self.add(1376,20)
        for kw in ({'is_lock':1},{'owner_id':123},{'ext_awaken_pos':1},{'prob_compen':1}):
            ident=self.add(14301,**kw);self.reject(1359,star_id=ident,des_type=6)
        ident=self.add(14301)
        for subtype in (0,2,3,5,255):self.reject(1359,star_id=ident,des_type=subtype)
        role=self.b.profile();next(i for i in role['attachments'] if i['id']==ident)['level']=2;self.b.save(role)
        self.reject(1359,star_id=ident,des_type=6)
        role=self.b.profile();role['level']=37;self.b.save(role)
        self.reject(1359,star_id=self.add(13301),des_type=6)

    def test_conversion_insufficient_gold_and_ticket(self):
        ident=self.add(14301);self.reject(1359,star_id=ident,des_type=6)
        self.add(1376);role=self.b.profile();role['gold_coin']=199;self.b.save(role)
        self.reject(1359,star_id=ident,des_type=6)

    def test_fragments_divination_claim_synthesis_and_conversion_chain(self):
        role=self.b.profile();role.update(level=99,silver_coin=2000000)
        day=(NOW+8*3600)//86400
        role['divination']=dict(day=day,divi_count=1,buy_count=1,cur_pos=16,star_list=[],has_half=True)
        self.b.save(role)
        # Choose the actual 1378 entry from the original weighted position pool.
        pool=[list(map(int,x.split('|'))) for x in list(stars.POSITIONS[16].values())[2].split('/')]
        idx=next(i for i,x in enumerate(pool) if x[2]==1378)
        with patch.object(summon,'weighted_choice',side_effect=lambda weights:idx if idx in weights and len(weights)==len(pool) else next(iter(weights))):
            self.ok(self.req(1337,event_type=2,data='{}'))
        self.assertEqual(self.b.profile()['divination']['star_list'][0]['attach_type'],1378)
        self.ok(self.req(1337,event_type=5,data='{}'))
        self.assertEqual(b.item_count(self.b.profile(),1378),1)
        role=self.b.profile();summon.add_item(role,1378,19);self.b.save(role)
        shard=next(i for i in self.b.profile()['attachments'] if i['type_id']==1378)
        before=self.b.profile()['silver_coin']
        with patch.object(summon,'weighted_choice',return_value=0):
            self.ok(self.req(1074,flag=2,num=1,des_type=1,count=1,id_list=[dict(id=shard['id'])]))
        self.assertEqual(self.b.profile()['silver_coin'],before-500000)
        self.assertEqual(b.item_count(self.b.profile(),1378),0)
        star=next(i for i in self.b.profile()['attachments'] if i['type_id']==14301)
        self.assertEqual((star['count'],star['level']),(1,1))
        self.add(1376);self.ok(self.req(1359,star_id=star['id'],des_type=6))

    def test_fragment_batch_distinct_stars_and_atomic_failure(self):
        ident=self.add(1378,40)
        self.reject(1074,flag=2,num=2,des_type=1,count=1,id_list=[dict(id=ident)])
        role=self.b.profile();role['silver_coin']=1000000;self.b.save(role)
        with patch.object(summon,'weighted_choice',return_value=0):
            self.ok(self.req(1074,flag=2,num=2,des_type=1,count=1,id_list=[dict(id=ident)]))
        result=[i for i in self.b.profile()['attachments'] if i['type_id']==14301]
        self.assertEqual(len(result),2);self.assertTrue(all(i['count']==1 for i in result))
        self.assertNotEqual(result[0]['id'],result[1]['id'])

    def test_full_star_bag_can_claim_material_only(self):
        role=self.b.profile();stars.grant(role,10301,200)
        role['divination']=dict(day=(NOW+8*3600)//86400,divi_count=0,buy_count=0,cur_pos=1,
            star_list=[dict(object_type=5,attach_type=1378,attach_count=1,attach_level=1)],has_half=True)
        role['level']=99;self.b.save(role)
        self.ok(self.req(1337,event_type=5,data='{}'))
        self.assertEqual(b.item_count(self.b.profile(),1378),1)

    def test_fragment_shortage_lock_and_full_bag_reject_atomically(self):
        ident=self.add(1378,19)
        role=self.b.profile();role['silver_coin']=2000000;self.b.save(role)
        params=dict(flag=2,num=1,des_type=1,count=1,id_list=[dict(id=ident)])
        self.reject(1074,**params)
        role=self.b.profile();fragment=next(i for i in role['attachments'] if i['id']==ident)
        fragment.update(count=20,is_lock=1);self.b.save(role)
        self.reject(1074,**params)
        role=self.b.profile();next(i for i in role['attachments'] if i['id']==ident)['is_lock']=0
        stars.grant(role,10301,200);self.b.save(role)
        self.reject(1074,**params)


if __name__=='__main__': unittest.main()
