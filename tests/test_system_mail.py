import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from network_redirect import system_mail, welfare, formation
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from analysis.tools.send_launch_gift import build, KEY, MID

NOW=1792915200
class SystemMailTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.b=Backend(Path(self.tmp.name),1,lambda *a,**k:None)
        self.role=self.b.profile(); self.role['level']=99
        self.payload=dict(key='compensation-test',title='维护补偿',body='测试补偿',prizes=[[5,1001,10,1]])
        self.serial=0
    def tearDown(self):
        self.b.close();self.tmp.cleanup()
    def deliver(self,**kw):
        payload=dict(self.payload,**kw)
        result=system_mail.deliver(self.role,now=NOW,rules=self.b.welfare_rules,**payload)
        self.b.save(self.role)
        return result[1]
    def request(self,mid,mail_id,now=NOW):
        self.serial+=1
        packet=encode(mid,dict(serial_num=self.serial,mail_id=mail_id,flag=1))
        with patch('network_redirect.backend.time.time',return_value=now):
            replies=self.b.respond(packet,dict(authenticated=True))
        events=[login_fields(d['data']) for m,_,d in map(decode,replies) if m==2998]
        return packet,replies,events
    def test_permanent_after_ten_years_and_claim_once(self):
        mail=self.deliver()
        _,_,preview=self.request(1102,mail['mail_id'],NOW+10*365*86400)
        content=next(e for e in preview if 'mail_title' in e)
        self.assertIn('永久有效',content['mail_body']);self.assertEqual(content['attach_count'],1)
        packet,replies,events=self.request(1103,mail['mail_id'],NOW+10*365*86400)
        self.assertTrue(any(e.get('result')==1 and 'mail_id' in e for e in events))
        claimed=self.b.profile()
        self.assertEqual(replies,self.b.respond(packet,dict(authenticated=True)))
        self.assertEqual(claimed,self.b.profile())
        _,_,events=self.request(1103,mail['mail_id'])
        self.assertTrue(any('op_string' in e for e in events))
        self.assertEqual(claimed['attachments'],self.b.profile()['attachments'])
    def test_bootstrap_enables_visible_message_menu(self):
        configs=[login_fields(d['data']) for m,_,d in map(decode,self.b.bootstrap()) if m==2998 and d['id']==80]
        menu=configs[0][7]
        self.assertTrue(menu['message'])
        for key in ('collector','Bulletin','setting','service','relogin'):
            self.assertTrue(menu[key])

    def test_original_zero_serial_read_and_no_mutation_watermark(self):
        mail=self.deliver()
        for serial in (0,99999,0):
            packet=encode(1102,dict(serial_num=serial,mail_id=mail['mail_id'],flag=0))
            replies=self.b.respond(packet,dict(authenticated=True))
            events=[login_fields(d['data']) for m,_,d in map(decode,replies) if m==2998]
            self.assertTrue(any(e.get('mail_id')==mail['mail_id'] and 'mail_body' in e for e in events))
            self.assertEqual(self.b.last_welfare_serial,0)
            self.assertFalse(any(decode(p)[0] in (1034,1035) for p in replies))
        _,_,events=self.request(1103,mail['mail_id'])
        self.assertFalse(any('op_string' in e for e in events))

    def test_retry_keeps_claim_and_inventory(self):
        mail=self.deliver();self.request(1103,mail['mail_id'])
        role=self.b.profile();before=copy.deepcopy(role['attachments'])
        status,mail=system_mail.deliver(role,now=NOW,rules=self.b.welfare_rules,**self.payload)
        self.assertEqual(status,'already_claimed');self.assertTrue(mail['claimed'])
        self.assertEqual(before,role['attachments']);self.assertIsNone(mail['expires_at'])
    def test_conflicting_key_or_id_rejected_without_mutation(self):
        mail=self.deliver();before=copy.deepcopy(self.role)
        for change in (dict(prizes=[[5,1001,11,1]]),dict(key='other',mail_id=mail['mail_id'])):
            with self.assertRaises(formation.Rejected):
                system_mail.deliver(self.role,now=NOW,rules=self.b.welfare_rules,**dict(self.payload,**change))
            self.assertEqual(before,self.role)
    def test_invalid_prizes_atomic(self):
        for prizes in ([[5,1001,1,1],[5,999999,1,1]],[[10,99999,1,1]],[[6,202,1,100]],[[15,99999,1,1]],[[5,1001,-1,1]]):
            before=copy.deepcopy(self.role)
            with self.assertRaises(formation.Rejected):
                system_mail.deliver(self.role,now=NOW,rules=self.b.welfare_rules,**dict(self.payload,prizes=prizes))
            self.assertEqual(before,self.role)
    def test_full_launch_gift_through_backend(self):
        prizes,_=build();mail=self.deliver(key=KEY,mail_id=MID,prizes=prizes,title='开服大礼包')
        _,_,events=self.request(1102,MID)
        self.assertEqual(next(e for e in events if 'mail_title' in e)['attach_count'],54)
        _,_,events=self.request(1103,MID)
        self.assertFalse(any('op_string' in e for e in events))
        role=self.b.profile()
        self.assertTrue(role['welfare']['mails'][KEY]['claimed'])
        self.assertTrue({5046,5044,5048,5051}<={c['type'] for c in role['corteges']})
        self.assertTrue(any(p['type_id']==201 for p in role['activity']['home']['pets']))
    def test_dry_run_and_account_isolation_and_audit(self):
        self.b.save(self.role);db=Path(self.tmp.name)/'game.sqlite3'
        before=self.b.profile()
        result=system_mail.issue(db,self.b.account,self.payload,now=NOW)
        self.assertFalse(result['written']);self.assertEqual(before,self.b.profile())
        with self.assertRaises(formation.Rejected):system_mail.issue(db,'missing',self.payload,write=True,now=NOW)
        result=system_mail.issue(db,self.b.account,self.payload,write=True,now=NOW)
        self.assertTrue(result['written'])
        self.assertEqual(self.b.db.execute('select count(*) from system_mail_audit').fetchone()[0],1)
        self.assertEqual(len(list((db.parent/'backups').glob('*.json'))),1)
        self.assertFalse(self.b.profile()['welfare']['mails'][self.payload['key']]['claimed'])
