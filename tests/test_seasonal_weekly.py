"""Weekly food material settlement through wire handlers and durable mail."""
import copy
from pathlib import Path
from unittest.mock import patch

from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_seasonal as season, formation, summon, time_guard
from network_redirect.backend import Backend
from network_redirect.protocol import encode, decode


class SeasonalWeeklyTests(ActivityCase):
    def setup_week(self):
        self.ok(self.req(1205, flag=0))
        role = self.b.profile()
        s = season.state(role)
        self.week = s['craft_weeks']['moon']['week']
        self.boundary = (self.week*7+4)*86400-8*3600
        role['attachments'] = [i for i in role['attachments'] if i['type_id'] not in
                               season.MATERIALS['moon'] | season.MATERIALS['rice']]
        for tid, n, locked in ((1134, 6, 0), (1135, 5, 1), (1208, 10, 0), (1212, 10, 1)):
            role['attachments'].append(dict(id=formation.new_id(role), attach_type=5,
                type_id=tid, count=n, level=1, is_lock=locked))
        for tid in (1130, 1213, 1217):
            summon.add_item(role, tid, 2)
        s.update(moon_count=19, rice_count=9)
        self.b.save(role)
        return copy.deepcopy(role)

    def mails(self):
        return {k:v for k,v in self.b.profile()['welfare'].get('mails',{}).items()
                if k.startswith(('moon-recycle-', 'rice-recycle-'))}

    def count(self, tid):
        return sum(i['count'] for i in self.b.profile()['attachments']
                   if i['attach_type']==5 and i['type_id']==tid)

    def test_boundary_two_independent_mails_new_supplies_and_claim_once(self):
        self.setup_week()
        with patch('network_redirect.game_clock.now', return_value=self.boundary-1):
            self.ok(self.req(1205, flag=0))
            self.assertEqual(self.mails(), {})
        peaches = self.count(1001)
        with patch('network_redirect.game_clock.now', return_value=self.boundary):
            events = self.req(1205, flag=0);self.ok(events)
            self.assertIn(13, [e for e,_ in events])
            mails = self.mails();self.assertEqual(len(mails), 2)
            for name in ('moon', 'rice'):
                mail = mails[f'{name}-recycle-{self.week}']
                self.assertEqual(mail['prizes'], [[5,1001,1 if name=='moon' else 2,1]])
                self.assertTrue(mail['no_expiry'])
                self.assertEqual(season.state(self.b.profile())[name+'_count'], 0)
            self.assertEqual(self.count(1001), peaches)
            self.assertEqual([self.count(t) for t in range(1134,1139)], [60,15,15,15,15])
            self.assertEqual([self.count(t) for t in range(1208,1213)], [60,15,15,15,15])
            for tid in (1130,1213,1217):self.assertEqual(self.count(tid), 2)
            self.b.close();self.b = Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
            self.ok(self.req(1205,flag=0));self.assertEqual(self.mails(), mails)
            for mail in mails.values():
                self.ok(self.req(1103,mail_id=mail['mail_id']))
                self.assertEqual(self.req(1103,mail_id=mail['mail_id'])[0][0],55)
            self.assertEqual(self.count(1001),peaches+3)

    def test_heartbeat_resets_online_status_without_granting_supplies(self):
        self.setup_week()
        with patch('network_redirect.game_clock.now',return_value=self.boundary):
            replies = self.b.respond(encode(2999,{}),self.state)
            events = [d for m,_,d in map(decode,replies) if m==2998]
            self.assertIn(13,[d['id'] for d in events])
            from network_redirect.backend import login_fields
            status = [login_fields(d['data']) for d in events if d['id']==47]
            self.assertTrue(any(s.get('local_seasonal_only') for s in status))
            self.assertEqual(self.count(1134),0);self.assertEqual(self.count(1208),0)
            stable = self.mails()
            self.b.respond(encode(2999,{}),self.state)
            self.assertEqual(self.mails(),stable)

    def test_mail_failure_rolls_back_both_events_and_materials(self):
        before = self.setup_week()
        from network_redirect import system_mail
        original = system_mail.deliver
        def fail_second(role, **kwargs):
            if kwargs['key'].startswith('rice-'):raise formation.Rejected('mail failure')
            return original(role,**kwargs)
        with patch('network_redirect.game_clock.now',return_value=self.boundary), patch.object(system_mail,'deliver',side_effect=fail_second):
            self.assertEqual(self.req(1205,flag=0)[0][0],55)
        after = self.b.profile()
        for key in ('activity','attachments','welfare'):
            self.assertEqual(after.get(key),before.get(key))

    def test_legacy_migration_keeps_inventory_progress_and_claim_then_settles(self):
        role = self.setup_week();s=season.state(role);s.pop('craft_weeks')
        role['activity']['day']-=21
        season.rollover(role,NOW,self.b.activity_rules)
        self.assertEqual(s['moon_count'],19)
        self.assertEqual(s['rice_count'],9)
        self.assertTrue(s['craft_weeks']['moon']['supplied'])
        self.assertEqual(role['attachments'],self.b.profile()['attachments'])
        season.rollover(role,self.boundary,self.b.activity_rules)
        self.assertEqual(s['moon_count'],0)
        self.assertEqual(s['craft_weeks']['moon']['last_recycle']['materials'],11)

    def test_skipped_weeks_disabled_events_and_backward_time_do_not_duplicate(self):
        role=self.setup_week()
        rules=copy.deepcopy(self.b.activity_rules)
        for n in ('moon','rice'):rules['seasonal_games'][n]['enabled']=False
        future=self.boundary+28*86400
        season.rollover(role,future,rules)
        stable=copy.deepcopy(role)
        season.rollover(role,NOW,rules)
        season.rollover(role,future,rules)
        self.assertEqual(role,stable)
        self.assertEqual(len([k for k in role['welfare']['mails'] if '-recycle-' in k]),2)
        self.assertFalse(season.state(role)['craft_weeks']['rice']['supplied'])

    def test_drop_settles_old_stock_before_new_materials(self):
        role=self.setup_week()
        with patch.object(season,'material_specs',return_value=[[5,1134,4,1],[5,1208,3,1]]), patch('network_redirect.activity_tangwang.travel_drop',return_value=[]):
            season.travel_drop(role,self.boundary,self.b.activity_rules)
        for tid,n in ((1134,4),(1208,3)):
            self.assertEqual(sum(i['count'] for i in role['attachments'] if i['type_id']==tid),n)
        self.assertEqual(season.state(role)['craft_weeks']['moon']['last_recycle']['materials'],11)

    def test_time_guard_freezes_settlement_and_maps_mail_sources(self):
        role=self.setup_week()
        role['time_guard']=dict(blocked=['activity_seasonal'],since=NOW)
        stable=copy.deepcopy(role)
        season.rollover(role,self.boundary,self.b.activity_rules)
        self.assertEqual(role,stable)
        for name in ('moon','rice'):
            self.assertEqual(time_guard.mail_scope(f'{name}-recycle-{self.week}'),'activity_seasonal')
        with self.assertRaises(formation.Rejected):
            season.settle(role,1333,dict(flag=0),self.boundary,self.b.activity_rules)

    def test_empty_and_single_material_settlement(self):
        role=self.setup_week()
        role['attachments']=[]
        summon.add_item(role,1138,1)
        season.rollover(role,self.boundary,self.b.activity_rules)
        mails=role['welfare'].get('mails',{})
        self.assertNotIn(f'moon-recycle-{self.week}',mails)
        self.assertNotIn(f'rice-recycle-{self.week}',mails)
        self.assertEqual(role['attachments'],[])
        self.assertEqual(season.state(role)['craft_weeks']['moon']['last_recycle']['peaches'],0)

    def test_quarantined_weekly_mail_cannot_be_claimed(self):
        from network_redirect import welfare
        role=self.setup_week()
        season.rollover(role,self.boundary,self.b.activity_rules)
        role['time_guard']=dict(blocked=['activity_seasonal'],since=self.boundary)
        before=copy.deepcopy(role)
        for name in ('moon','rice'):
            mail=role['welfare']['mails'][f'{name}-recycle-{self.week}']
            with self.assertRaisesRegex(formation.Rejected,'TIME-001'):
                welfare.mail_request(role,1103,dict(mail_id=mail['mail_id']),
                                     self.boundary,self.b.welfare_rules,role['welfare'])
        self.assertEqual(role,before)
