import copy
import unittest
from decimal import Decimal
from tests import test_formation as helpers
from pathlib import Path
from network_redirect import formation as f, skill_insight as si, cheer
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode


class InsightTests(unittest.TestCase):
    setUp = helpers.FormationTests.setUp
    request = helpers.FormationTests.request
    events = helpers.FormationTests.events
    ok = helpers.FormationTests.ok
    rejected = helpers.FormationTests.rejected
    add_item = helpers.FormationTests.add_item

    def spell(self, tid, level=1, **extra):
        ident = self.add_item(tid, count=0, attach_type=6, **extra)
        role = self.backend.profile()
        f.lookup(role, 'attachments', ident)['level'] = level
        self.backend.save(role)
        return ident

    def setup_recipe(self, tid=22):
        target = self.spell(tid, 10)
        ids = [self.spell(t) for kind, t, n, level in si.materials(tid) for _ in range(n)]
        return dict(upgrade_type=6, des_id=target, material_count=len(ids), material_list=[dict(id=i) for i in ids])

    def test_all_original_recipes_and_replay(self):
        for tid in si.RECIPES:
            with self.subTest(tid=tid):
                req = self.setup_recipe(tid)
                before = self.backend.profile()
                rows = self.ok(1076, **req)
                after = self.backend.profile()
                item = f.lookup(after, 'attachments', req['des_id'])
                self.assertEqual((item['upgrade_level'], item['level']), (1, 10))
                self.assertEqual(len(after['attachments']), len(before['attachments']) - 2)
                self.assertEqual(after['gold_coin'], before['gold_coin'])
                self.assertEqual(after['silver_coin'], before['silver_coin'])
                self.assertIn((156, {'result': 0, 'des_id': req['des_id'], 'ret_list': {}}), self.events(rows))
                self.assertTrue(any(mid == 1032 and data.get('unit_type') == 6 and data['attr_list'][0] == dict(type=61, value=1) for mid, _, data in rows))
                self.assertEqual(self.backend.respond(self.packet, self.state), self.replies)
                self.rejected(1076, **req)

    def test_invalid_materials_are_atomic(self):
        req = self.setup_recipe()
        for key, value in [('upgrade_type', 5), ('des_id', 999), ('material_list', [req['material_list'][0]] * 2)]:
            self.rejected(1076, **dict(req, **{key:value}))
        self.rejected(1076, **dict(req, material_count=1, material_list=req['material_list'][:1]))
        pristine = self.backend.profile()
        mid = req['material_list'][0]['id']
        for changes in [dict(equip_order=9), dict(owner_id=99), dict(is_lock=1), dict(protogenic=1), dict(upgrade_level=1), dict(awaken=1), dict(type_id=23), dict(level=0)]:
            role = copy.deepcopy(pristine)
            f.lookup(role, 'attachments', mid).update(changes)
            self.backend.save(role)
            self.rejected(1076, **req)
        for changes in [dict(level=9), dict(type_id=206), dict(type_id=25), dict(upgrade_level=1)]:
            role = copy.deepcopy(pristine)
            f.lookup(role, 'attachments', req['des_id']).update(changes)
            self.backend.save(role)
            self.rejected(1076, **req)

    def test_equipped_bonus_and_reconnect(self):
        req = self.setup_recipe()
        role = self.backend.profile()
        target = f.lookup(role, 'attachments', req['des_id'])
        target.update(equip_order=1, equip_pos=2)
        f.prepare(role, self.backend.formation_rules)
        baseline = copy.deepcopy(role)
        self.backend.save(role)
        self.ok(1076, **req)
        after = self.backend.profile()
        c = after['corteges'][0]
        self.assertGreater(c['hp'], baseline['corteges'][0]['hp'])
        self.assertEqual(c['fangyu'], baseline['corteges'][0]['fangyu'])
        expected = copy.deepcopy(after)
        f.prepare(after, self.backend.formation_rules)
        self.assertEqual(after, expected)
        fresh = Backend(Path(self.directory.name), 18770, lambda *a, **k: None)
        try:
            self.assertEqual(f.lookup(fresh.profile(), 'attachments', req['des_id'])['upgrade_level'], 1)
        finally:
            fresh.close()

    def test_conversion_refunds_level_one_and_preserves_level(self):
        req = self.setup_recipe()
        role = self.backend.profile()
        f.lookup(role, 'attachments', req['material_list'][0]['id'])['level'] = 5
        self.backend.save(role)
        self.ok(1076, **req)
        self.add_item(1095)
        before = self.backend.profile()
        rows = self.ok(1212, skill_id=req['des_id'], state=4)
        payload = next(p for e,p in self.events(rows) if e == 89)
        after = self.backend.profile()
        target = f.lookup(after, 'attachments', payload['skill_id'])
        self.assertEqual((target['level'], target['upgrade_level']), (10, 0))
        self.assertEqual(int(f.SKILLS[target['type_id']]['effect_field(1-gongji，2-fangyu，3-magic，4-intensity，5-hp)']), 1)
        self.assertEqual(before['gold_coin']-after['gold_coin'], 200)
        refunds = [i for i in after['attachments'] if i['id'] not in {x['id'] for x in before['attachments']} and i['id'] != target['id']]
        self.assertEqual(sorted((x['type_id'],x['level']) for x in refunds), [(22,1),(25,1)])
        self.rejected(1212, skill_id=req['des_id'], state=4)
        self.rejected(1212, skill_id=target['id'], state=9)

    def test_conversion_validation_and_normal_random(self):
        target = self.spell(22, 7)
        self.rejected(1212, skill_id=target, state=4)
        self.add_item(1095, 2)
        self.rejected(1212, skill_id=target, state=2)
        role = self.backend.profile()
        role['gold_coin'] = 0
        self.backend.save(role)
        self.rejected(1212, skill_id=target, state=4)
        rows = self.ok(1212, skill_id=target, state=0)
        payload = next(p for e,p in self.events(rows) if e == 89)
        self.assertNotEqual(payload['skill_type'], 22)
        self.assertEqual(payload['skill_level'], 7)

    def test_cheer_insight_scales_hp_on_both_sides(self):
        for order in (1, 9):
            name = cheer.NAMES[order - 1]
            item = dict(attach_type=6, type_id=22, level=10, equip_order=order+8, equip_pos=2)
            role = {'cheer_' + name + '_effect':1, name + '_skill_level':100,
                    'cheer_' + name + '_level':10, cheer.skill_mask(order, 2)[0]:cheer.skill_mask(order, 2)[1],
                    'corteges':[dict(id=2, order=0, cheer_order=order)], 'attachments':[item]}
            pending = {1:{s:Decimal(1000) for s in f.STATS}, 2:{s:Decimal(100) for s in f.STATS}}
            before = {s:Decimal(1000) for s in f.STATS}
            cheer.bonuses(role, dict(id=1,order=1), before, pending)
            item['upgrade_level'] = 1
            after = {s:Decimal(1000) for s in f.STATS}
            cheer.bonuses(role, dict(id=1,order=1), after, pending)
            self.assertEqual(after['hp']-before['hp'], Decimal(120)*Decimal(cheer.SKILL[100]['plus_rate']))
            self.assertEqual(after['fangyu'], before['fangyu'])

    def test_insight_cannot_be_enhancement_fodder(self):
        req = self.setup_recipe()
        self.ok(1076, **req)
        target = self.spell(23)
        self.rejected(1071, data='{des_skill_id=%d,src_skill_list={%d}}' % (target, req['des_id']))

if __name__ == '__main__':
    unittest.main()
