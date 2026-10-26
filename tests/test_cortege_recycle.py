"""Original 1086 contract, disposal integrity, reward use, rollback and replay."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect import formation as f, summon, cortege_recycle as r
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode


class RecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.addCleanup(lambda:self.b.close())
        role = self.b.profile(); role['level']=60
        self.ids=[]
        for tid in (4064,4065,4066,4067,4022):
            c=summon.companion(role,tid);role['corteges'].append(c);self.ids.append(c['id'])
        f.prepare(role,self.b.formation_rules);self.b.save(role)
        self.serial=100000;self.state={'authenticated':True}

    def request(self,mid=1086,**kw):
        self.serial+=1
        if mid==1086:kw=dict(flag=0,**{'c%d'%(i+1):v for i,v in enumerate(self.ids)})|kw
        self.packet=encode(mid,dict(serial_num=self.serial,**kw))
        self.replies=self.b.respond(self.packet,self.state)
        self.rows=[decode(x) for x in self.replies]
        self.assertEqual(self.rows[-1][0],1106)
        return [(d['id'],login_fields(d['data'])) for m,_,d in self.rows if m==2998]

    def test_recycle_fate_rewards_consumption_and_reconnect(self):
        with patch.object(r.secrets,'randbelow',return_value=0):
            events=self.request()
        self.assertEqual(events,[(64,{'roll_list':{1:{'type_id':1064,'level':1,'count':6}}})])
        role=self.b.profile()
        self.assertFalse(set(self.ids)&{c['id'] for c in role['corteges']})
        self.assertFalse(any(i.get('innate_owner_id') in self.ids for i in role['attachments']))
        self.assertEqual(sum(i['count'] for i in role['attachments'] if i['type_id']==1064),6)
        self.assertEqual(self.b.respond(self.packet,self.state),self.replies)
        self.assertEqual(self.b.profile(),role)
        # The real book type is accepted by the original experience protocol.
        event=self.request(1059,first_send=True,flag=1,cortege_id=role['corteges'][0]['id'],roll_count=1,
                           roll_list=[dict(type_id=1064,count=1)])
        self.assertEqual(event[-1][0],65)
        self.assertGreater(self.b.profile()['corteges'][0]['level'],1)
        self.b.close();self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertFalse(set(self.ids)&{c['id'] for c in self.b.profile()['corteges']})
        self.assertEqual(sum(i['count'] for i in self.b.profile()['attachments'] if i['type_id']==1064),5)

    def test_fate_and_no_fate_and_all_level_boundaries(self):
        self.assertTrue(r.has_fate({4064,4065,4066,4067,4022}))
        self.assertFalse(r.has_fate({4064}))
        original=self.b.profile()
        for level in (15,29,30,44,45,59,60,74,75,89,90,104,105,150):
            role=copy.deepcopy(original);role['level']=level
            with patch.object(r.secrets,'randbelow',return_value=99):
                event=r.settle(role,dict(flag=0,**{'c%d'%(i+1):v for i,v in enumerate(self.ids)}))
            reward=event[0][1]['roll_list'][0]
            self.assertEqual(int(f.ITEMS[reward['type_id']]['show_level']),min(100,level//15*15))
            self.assertEqual(f.ITEMS[reward['type_id']]['resource'],'20')
        types=[]
        for tid,base in f.BASES.items():
            if int(base['quality'])==4 and not r.has_fate(set(types+[tid])):types.append(tid)
            if len(types)==5:break
        role=copy.deepcopy(original)
        for c,tid in zip(role['corteges'][-5:],types):c['type']=tid
        with patch.object(r.secrets,'randbelow',side_effect=AssertionError('no fate must not roll')):
            r.settle(role,dict(flag=0,**{'c%d'%(i+1):v for i,v in enumerate(self.ids)}))

    def test_invalid_requests_and_atomic_guards(self):
        for kw in (dict(flag=1),dict(c1=0),dict(c1=999999),dict(c1=self.ids[1])):
            before=self.b.profile();self.assertEqual(self.request(**kw)[-1][0],55);self.assertEqual(before,self.b.profile())
        original=self.b.profile()
        for field,value in (('order',2),('cheer_order',1),('is_lock',1),('pending_training',{'points':5}),('type',5002)):
            role=copy.deepcopy(original);role['corteges'][-1][field]=value;self.b.save(role)
            before=self.b.profile();self.assertEqual(self.request()[-1][0],55);self.assertEqual(before,self.b.profile())
        role=copy.deepcopy(original);role['level']=14;self.b.save(role)
        before=self.b.profile();self.assertEqual(self.request()[-1][0],55);self.assertEqual(before,self.b.profile())

    def test_bound_essence_return_and_history(self):
        role=self.b.profile();summon.add_item(role,10101,1)
        item=next(i for i in role['attachments'] if i['type_id']==10101)
        item.update(owner_id=self.ids[0],ext_skill_pos=1,level=3,is_lock=1)
        self.b.save(role)
        self.assertEqual(self.request()[-1][0],64)
        after=self.b.profile();item=next(i for i in after['attachments'] if i['id']==item['id'])
        self.assertEqual((item['owner_id'],item['ext_skill_pos'],item['level'],item['is_lock']),(0,0,3,1))
        self.assertIn(4064,after['handbook']['4'])
        before=self.b.profile();self.assertEqual(self.request()[-1][0],55);self.assertEqual(before,self.b.profile())

    def test_invalid_configuration(self):
        path=Path(self.tmp.name)/'rules.json'
        rules=r.load_rules();rules['fate_advanced_percent']=101;path.write_text(json.dumps(rules))
        with self.assertRaises(f.Rejected):r.load_rules(path)

if __name__=='__main__':unittest.main()
