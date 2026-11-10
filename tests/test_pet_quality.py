"""Quality boundaries through native request packets and disposable save files."""
import copy
from unittest.mock import patch
from test_activity import ActivityCase
from test_pets import PetTests
from network_redirect import pets, summon


class PetQualityTests(ActivityCase):
    seed = PetTests.seed
    home = PetTests.home
    call = PetTests.call

    def transform(self, pid, tid):
        self.ok(self.req(1348, id=21, data=summon.lua(dict(pet_id=pid, des_type=tid))))
        return next(p for p in self.home()['pets'] if p['id'] == pid)

    def prepare_transform(self, quality=2, star=0):
        with patch('network_redirect.pets.secrets.randbelow', return_value=0):
            pid, = self.seed([(201, quality)])
        r = self.b.profile(); h = r['activity']['home']
        h['build']['5'] = 1; h['pet_starter_given'] = True
        p = h['pets'][0]; p['star_level'] = star
        if star == 9:
            p['grow_values'] = [v*110//100 for v in p['grow_values']]
        for tid, count in ((1365, 20), (1345, 1000)):
            summon.add_item(r, tid, count)
        self.b.save(r)
        return pid

    def test_fusion_star_protection_and_compensation_via_packets(self):
        # The former quality-2 outcome becomes quality 3, with compensation kept.
        for star, quality, expected in ((0, 3, 2), (1, 3, 3), (6, 3, 3), (7, 4, 4), (9, 4, 4)):
            with self.subTest(star=star):
                pid, *foods = self.seed([(102, quality)]+[(102, 1)]*3)
                r = self.b.profile(); r['activity']['home']['pets'][0]['star_level'] = star
                self.b.save(r)
                with patch('network_redirect.pets.secrets.randbelow', return_value=0):
                    result = self.call(2, des_id=pid, src_list=foods)
                p = self.home()['pets'][0]
                self.assertEqual((p['quality'], p['star_level'], p['prob_compen']), (expected, star, 3))
                self.assertEqual(result['update_list'][pid]['quality'], expected)
                self.assertEqual(len(self.home()['pets']), 1)
                before = self.b.profile()
                self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
                self.assertEqual(self.b.profile(), before)

    def test_fusion_upgrade_still_clears_compensation(self):
        pid, *foods = self.seed([(102, 3)]+[(102, 4)]*3)
        r = self.b.profile(); p = r['activity']['home']['pets'][0]
        p.update(star_level=1, prob_compen=10); self.b.save(r)
        self.call(2, des_id=pid, src_list=foods)
        p = self.home()['pets'][0]
        self.assertEqual((p['quality'], p['star_level'], p['prob_compen']), (4, 1, 0))

    def test_transform_clamps_lower_bound_and_restores_valid_source(self):
        pid = self.prepare_transform()
        before = copy.deepcopy(self.home()['pets'][0])
        changed = self.transform(pid, 202)
        self.assertEqual(changed['grow_values'], [30, 21, 49, 43])
        self.assertEqual(changed['quality'], 2)
        self.assertEqual(self.home()['pet_growth']['202']['2'], changed['grow_values'])
        self.assertEqual(self.transform(pid, 201), before)

    def test_transform_repairs_legacy_memory_without_changing_other_fields(self):
        pid = self.prepare_transform()
        r = self.b.profile(); h = r['activity']['home']
        h['pet_growth']['202'] = {'2': [999, 1, 45, 40]}
        self.b.save(r)
        before = self.home()['pets'][0]
        changed = self.transform(pid, 202)
        self.assertEqual(changed['grow_values'], [40, 20, 45, 40])
        for key in ('id', 'quality', 'level', 'star_level', 'train_levels', 'order', 'cur_exp', 'prob_compen'):
            self.assertEqual(changed[key], before[key])
        self.assertEqual(self.home()['pet_growth']['202']['2'], [40, 20, 45, 40])

    def test_nine_star_memory_uses_bonus_bounds_once(self):
        pid = self.prepare_transform(4, 9)
        r = self.b.profile(); h = r['activity']['home']
        h['pet_growth']['202'] = {'4': [999, 1, 100, 90]}
        self.b.save(r)
        changed = self.transform(pid, 202)
        self.assertEqual(changed['grow_values'], [88, 44, 100, 90])
        self.transform(pid, 201)
        self.assertEqual(self.transform(pid, 202)['grow_values'], [88, 44, 100, 90])

    def test_transform_insufficient_materials_keeps_memory_and_pet(self):
        pid = self.prepare_transform()
        r = self.b.profile(); r['attachments'] = [i for i in r['attachments'] if i['type_id'] != 1365]
        self.b.save(r); before = self.b.profile()
        result = self.req(1348, id=21, data=summon.lua(dict(pet_id=pid, des_type=202)))
        self.assertEqual(result[0][0], 55)
        self.assertEqual(self.b.profile(), before)


del PetTests
