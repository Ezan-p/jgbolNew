"""Exact probability intervals plus binary requests on disposable accounts."""
from collections import Counter
import copy
from fractions import Fraction
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from network_redirect import qiankun_bags as q, formation as f, summon, vip, item_rewards
from network_redirect.backend import Backend
from tests import test_equipment as original


class QiankunPoolTests(unittest.TestCase):
    def test_table_rates_and_full_original_equipment_skill_coverage(self):
        rules = q.load_rules()
        expected = {'1034': (65, 30, 5), '1033': (50, 40, 10),
                    '1032': (40, 40, 20), '1031': (69, 30, 1)}
        for tid, weights in expected.items():
            self.assertEqual(tuple(rules['bags'][tid]['tiers'][k]['weight'] for k in q.TIERS), weights)
            self.assertTrue(vip.handles(1051, dict(item_type=int(tid))))
            self.assertNotIn(int(tid), item_rewards.HANDLED)
        used = {p for b in rules['bags'].values() for t in b['tiers'].values()
                for g in t['groups'] for p in q.CATALOG[g['pool']]}
        gear = {(5, t) for t, r in f.ITEMS.items() if r['main_type'] in ('1', '2', '3')
                and r['quality'] in ('2', '3', '4', '5') and not (r['main_type']=='3' and r['quality']=='2')}
        skills = {(6, t) for t, r in f.SKILLS.items() if r['quality'] in ('2','3','4','5')}
        self.assertTrue(gear | skills <= used)
        self.assertEqual(len(q.CATALOG['weapon_5']), 10)
        self.assertEqual(len(q.CATALOG['passive_5']), 8)
        self.assertNotIn((6, 21), q.CATALOG['passive_5'])
        self.assertEqual(q.CATALOG['mahayana'], [(6, 21)])
        self.assertEqual(len(q.CATALOG['manual']), 20)
        self.assertEqual(len(q.CATALOG['manual_advanced']), 20)

    def test_exact_integer_intervals_and_every_candidate_draw(self):
        for bag in q.load_rules()['bags'].values():
            tier_start = 0
            mass = Fraction()
            weights = {k: bag['tiers'][k]['weight'] for k in q.TIERS}
            with patch.object(summon.secrets, 'randbelow', side_effect=range(100)):
                self.assertEqual(dict(Counter(summon.weighted_choice(weights) for _ in range(100))), weights)
            for name in q.TIERS:
                tier = bag['tiers'][name]
                weights = {i: g['weight'] for i, g in enumerate(tier['groups'])}
                with patch.object(summon.secrets, 'randbelow', side_effect=range(100)):
                    self.assertEqual(dict(Counter(summon.weighted_choice(weights) for _ in range(100))), weights)
                group_start = 0
                for group in tier['groups']:
                    candidates = q.CATALOG[group['pool']]
                    for candidate in candidates:
                        mass += Fraction(tier['weight'] * group['weight'], 10000 * len(candidates))
                        # Both ends of the quality and category interval hit the same group.
                        for t, g in ((tier_start, group_start),
                                     (tier_start+tier['weight']-1, group_start+group['weight']-1)):
                            with patch.object(summon.secrets, 'randbelow', side_effect=[t,g]), \
                                 patch.object(q.secrets, 'choice', return_value=candidate) as choose:
                                self.assertEqual(q.draw(bag), [*candidate, group['count'], 1])
                                choose.assert_called_once_with(candidates)
                    group_start += group['weight']
                tier_start += tier['weight']
            self.assertEqual(mass, 1)

    def test_invalid_config_rejected(self):
        import tempfile
        original = q.load_rules()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'rules.json'
            changes = [lambda r: r['bags'].pop('1034'),
                       lambda r: r['bags']['1031'].update(min_vip=0),
                       lambda r: r['bags']['1034']['tiers']['low'].update(weight=64),
                       lambda r: r['bags']['1034']['tiers']['low']['groups'][0].update(weight=0),
                       lambda r: r['bags']['1034']['tiers']['low']['groups'][0].update(pool='missing'),
                       lambda r: r['bags']['1031']['tiers']['high']['groups'][0].update(count=2),
                       lambda r: r['bags']['1032']['tiers']['high']['groups'][3].update(count=1)]
            for change in changes:
                rules = copy.deepcopy(original); change(rules)
                path.write_text(json.dumps(rules))
                with self.assertRaises(f.Rejected): q.load_rules(path)


class QiankunWireTests(unittest.TestCase):
    setUp = original.EquipmentTests.setUp
    add = original.EquipmentTests.add
    get = original.EquipmentTests.get
    req = original.EquipmentTests.req

    def use(self, tid, ident, count=1, **changes):
        args = dict(item_type=tid, item_id=ident, item_count=count, des_type=1, des_id=0)
        args.update(changes)
        return self.req(1051, **args)

    def test_every_category_real_wire_persistence_and_replay(self):
        base = self.b.profile(); base['vip_level'] = 1
        for tid, bag in q.load_rules()['bags'].items():
            for tier in bag['tiers'].values():
                for group in tier['groups']:
                    with self.subTest(bag=tid, group=group):
                        self.b.save(copy.deepcopy(base))
                        ident = self.add(int(tid), count=2)
                        kind, target = q.CATALOG[group['pool']][-1]
                        spec = [kind, target, group['count'], 1]
                        before = self.b.profile()
                        with patch.object(q, 'draw', return_value=spec):
                            events = self.use(int(tid), ident)
                        self.assertEqual(events[-1][0], 21, events)
                        prize = next(iter(events[-1][1]['attach_list'].values()))
                        self.assertEqual(prize, dict(object_type=kind, attach_type=target,
                                                     attach_count=spec[2], attach_level=1))
                        self.assertEqual(self.get(ident)['count'], 1)
                        after = self.b.profile()
                        if kind in (11,12):
                            key = 'gold_coin' if kind==11 else 'silver_coin'
                            self.assertEqual(after[key]-before[key], spec[2])
                        else:
                            entries = [x for x in after['attachments'] if x['attach_type']==kind and x['type_id']==target]
                            self.assertTrue(entries)
                            if kind==6 or f.ITEMS[target]['can_stack']=='0':
                                self.assertTrue(all(x['count']==(0 if kind==6 else 1) for x in entries))
                            else:
                                old = sum(x['count'] for x in before['attachments'] if x['attach_type']==kind and x['type_id']==target)
                                self.assertEqual(sum(x['count'] for x in entries)-old, spec[2])
                        with patch.object(q, 'draw', side_effect=AssertionError('replayed draw')):
                            self.assertEqual(self.b.respond(self.packet, {'authenticated':True}), self.replies)
                        self.assertEqual(after, self.b.profile())
        saved = self.b.profile(); self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(saved, self.b.profile())

    def test_independent_batch_instances_and_selected_stack(self):
        role = self.b.profile(); role['vip_level']=1; self.b.save(role)
        first = self.add(1031, count=15); selected = self.add(1031, count=15)
        specs = [[5,2001,1,1], [6,21,1,1], [5,6005,5,1]]*5
        with patch.object(q, 'draw', side_effect=specs) as draw:
            event = self.use(1031, selected, 15)[-1]
        self.assertEqual(event[0], 21)
        self.assertEqual(draw.call_count, 15)
        self.assertEqual(len(event[1]['attach_list']), 15)
        role = self.b.profile()
        self.assertEqual(self.get(first)['count'],15)
        self.assertFalse(any(x['id']==selected for x in role['attachments']))
        for kind, tid in ((5,2001), (6,21)):
            entries = [x for x in role['attachments'] if x['attach_type']==kind and x['type_id']==tid]
            self.assertEqual(len(entries),5)
            self.assertEqual(len({x['id'] for x in entries}),5)
        self.assertEqual(sum(x['count'] for x in role['attachments'] if x['type_id']==6005),25)

    def test_vip_batches_allow_no_high_tier_rewards(self):
        # Exercise real quality/category selection through 1051, without
        # mocking draw(): every batch size may miss high, even repeatedly.
        for vip_level in (1, 10):
            role = self.b.profile(); role['vip_level'] = vip_level; self.b.save(role)
            for tier_roll, kind, target, amount in ((68, 5, 1020, 1), (98, 11, 1, 20)):
                for count in (*range(1, 16), 15):
                    with self.subTest(vip=vip_level, tier_roll=tier_roll, count=count):
                        ident = self.add(1031, count=count)
                        before = self.b.profile()
                        with patch.object(summon.secrets, 'randbelow',
                                          side_effect=[tier_roll, 0] * count) as rng:
                            event = self.use(1031, ident, count)[-1]
                        self.assertEqual(event[0], 21, event)
                        self.assertEqual(rng.call_count, 2 * count)
                        prizes = list(event[1]['attach_list'].values())
                        self.assertEqual(prizes, [dict(object_type=kind, attach_type=target,
                                                      attach_count=amount, attach_level=1)] * count)
                        after = self.b.profile()
                        self.assertFalse(any(x['id'] == ident for x in after['attachments']))
                        if kind == 11:
                            self.assertEqual(after['gold_coin'] - before['gold_coin'], amount * count)
                        else:
                            def total(profile):
                                return sum(x['count'] for x in profile['attachments']
                                           if x['attach_type'] == kind and x['type_id'] == target)
                            self.assertEqual(total(after) - total(before), amount * count)

    def test_invalid_requests_do_not_consume_or_draw(self):
        for tid in q.BAGS:
            ident = self.add(tid, count=16)
            if tid==1031:
                before=self.b.profile()
                self.assertEqual(self.use(tid,ident)[-1][0],55)
                self.assertEqual(before,self.b.profile())
                role=self.b.profile(); role['vip_level']=1;self.b.save(role)
            for changes in ({'item_count':0}, {'item_count':16}, {'item_id':99999999},
                            {'item_type':1032 if tid!=1032 else 1033}, {'des_type':5}, {'des_id':99999}):
                before=self.b.profile()
                with patch.object(q, 'draw', side_effect=AssertionError('invalid draw')):
                    self.assertEqual(self.use(tid,ident,**changes)[-1][0],55)
                self.assertEqual(before,self.b.profile())
            for field in ('level','is_lock','owner_id','equip_pos','equip_order','attach_type'):
                bad=self.add(tid,**{field:2 if field in ('level','attach_type') else 1})
                before=self.b.profile()
                self.assertEqual(self.use(tid,bad)[-1][0],55)
                self.assertEqual(before,self.b.profile())

    def test_currency_overflow_encoding_and_grant_failure_roll_back(self):
        ident=self.add(1034,count=15)
        for field,kind in (('silver_coin',12),('gold_coin',11)):
            role=self.b.profile();role[field]=2147483640;self.b.save(role)
            before=self.b.profile()
            with patch.object(q,'draw',return_value=[kind,1,5,1]):
                self.assertEqual(self.use(1034,ident,2)[-1][0],55)
            self.assertEqual(before,self.b.profile())
        role=self.b.profile();role.update(silver_coin=1000,gold_coin=0);self.b.save(role)
        for obj, method in ((self.b,'inventory'),(item_rewards,'grant')):
            before=self.b.profile()
            with patch.object(obj,method,side_effect=ValueError('injected failure')):
                self.assertEqual(self.use(1034,ident)[-1][0],55)
            self.assertEqual(before,self.b.profile())
