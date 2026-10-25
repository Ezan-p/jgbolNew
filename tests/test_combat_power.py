"""Permanent score invariants, real CSV sources, wire refresh and persistence."""
import copy
from decimal import Decimal
from pathlib import Path
import tempfile
import unittest

from network_redirect import combat_power as cp, formation as f, summon, cheer
from network_redirect.backend import Backend
from network_redirect.protocol import decode, encode


class CombatPowerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(self.backend.close)
        self.rules = self.backend.formation_rules
        self.role = self.backend.profile()

    def calculate(self, now=100):
        cp.recalculate(self.role, self.rules, now=now)
        return self.role['corteges'][0]

    def test_idempotent_and_explanation_does_not_mutate(self):
        self.calculate()
        before = copy.deepcopy(self.role)
        self.assertEqual(cp.explain(self.role, self.rules, 100), self.role['combat_power_breakdown'])
        self.calculate()
        self.assertEqual(before, self.role)
        self.assertEqual(self.role['role_combat_power'], self.role['corteges'][0]['combat_power'])

    def test_base_growth_real_csv(self):
        c = self.role['corteges'][0]
        c.update(type=5001, level=2)
        self.role['attachments'] = []
        self.calculate()
        self.assertEqual([c[s] for s in ('gongji','fangyu','hp','magic')], [233,133,561,147])
        self.assertEqual(c['combat_power'], 1364)

    def test_attachment_order_cannot_change_passive_panel(self):
        passive = next(t for t,r in f.SKILLS.items() if int(r['use_mode(1-active，2-passive)']) == 2
                       and int(r['effect_field(1-gongji，2-fangyu，3-magic，4-intensity，5-hp)']) == 1)
        self.role['attachments'] += [dict(id=900, attach_type=5, type_id=2001, level=2, equip_order=1),
                                    dict(id=901, attach_type=6, type_id=passive, level=1, equip_order=1)]
        self.calculate()
        expected = copy.deepcopy(self.role['combat_power_breakdown'])
        self.role['attachments'].reverse()
        self.calculate()
        self.assertEqual(expected, self.role['combat_power_breakdown'])

    def test_current_decreases_peak_survives_reconnect(self):
        c = self.role['corteges'][0]
        c['gongji_plus'] = 5000
        self.backend.save(self.role)
        peak = self.role['role_combat_power']
        c['gongji_plus'] = 0
        self.backend.save(self.role)
        restored = self.backend.profile()
        self.assertLess(restored['role_combat_power'], peak)
        self.assertEqual(restored['max_combat_power'], peak)
        wire = [decode(p) for p in self.backend.bootstrap(reconnect=True)]
        self.assertEqual(next(d['role_combat_power'] for m,_,d in wire if m == 1017), restored['role_combat_power'])
        attrs = [a for m,_,d in wire if m == 1032 and d['unit_type'] == 1 for a in d['attr_list']]
        self.assertIn(dict(type=39,value=peak), attrs)

    def test_title_expiry_reversible(self):
        baseline = copy.deepcopy(self.calculate())
        self.role.update(title_id=1, title_begintime=100, title_endtime=200)
        self.assertEqual(self.calculate(99)['combat_power'], baseline['combat_power'])
        self.assertEqual(self.calculate(100)['combat_power'], baseline['combat_power'] + 360)
        self.assertEqual(self.calculate(200)['combat_power'], baseline['combat_power'])
        self.assertEqual(self.role['max_combat_power'], baseline['combat_power'] + 360)

    def test_cheer_is_transferred_once_and_bag_excluded(self):
        support = summon.companion(self.role, 5002)
        support.update(order=0, cheer_order=1)
        self.role.update(cheer_heaven_level=1, cheer_heaven_effect=1)
        cheer.prepare(self.role)
        self.role['corteges'].append(support)
        self.role['attachments'] = []
        baseline = copy.deepcopy(self.calculate())
        trace = self.role['combat_power_breakdown']['companions'][str(baseline['id'])]
        source = self.role['combat_power_breakdown']['companions'][str(support['id'])]
        gain = Decimal(trace['cheer']['hp']) - Decimal(trace['pet']['hp'])
        self.assertEqual(gain, Decimal(source['fates_and_advance']['hp']) * Decimal('0.04'))
        self.assertEqual(self.role['role_combat_power'], baseline['combat_power'])
        support['cheer_order'] = 0
        self.assertLess(self.calculate()['combat_power'], baseline['combat_power'])
        self.assertEqual(self.role['combat_power_breakdown']['member_ids'], [baseline['id']])

    def test_pet_position_and_home_training(self):
        base = copy.deepcopy(self.calculate())
        self.role['activity'] = {'home': {'pets': [dict(type_id=101,order=1,grow_values=[100,200,300,400])],
                                        'train': {'1': {'level':1}}}}
        c = self.calculate()
        self.assertEqual(c['gongji'], cp.floor(Decimal(base['gongji']) * Decimal('1.01') + 500 + 100))
        self.assertEqual(c['hp'], base['hp'])
        self.role['activity']['home']['pets'][0]['order'] = 0
        self.calculate()
        self.assertEqual(c['gongji'], cp.floor(Decimal(base['gongji']) * Decimal('1.01') + 500))

    def test_cached_fields_and_temporary_effects_not_scored(self):
        base = self.calculate()['combat_power']
        self.role.update(max_hp_rate=99, animal_hp_plus=999, role_collect_hp_plus=999)
        self.role['corteges'][0].update(plus_rate=999, poison_buff_last_round=9, combat_power=999999)
        self.assertEqual(self.calculate()['combat_power'], base)

    def test_explicit_channels_clamp_and_remove(self):
        base = self.calculate()['combat_power']
        self.role['combat_sources'] = {'fam': {'gongji': 10}, 'cortege': {'hp': 50}}
        self.assertGreater(self.calculate()['combat_power'], base)
        self.role['combat_sources'] = {'cortege': {'gongji': 10**30}}
        self.assertEqual(self.calculate()['combat_power'], cp.LIMIT)
        self.role['combat_sources'] = {}
        self.assertEqual(self.calculate()['combat_power'], base)
        self.assertEqual(self.role['max_combat_power'], cp.LIMIT)

    def test_equipping_wire_total_and_single_match_saved_state(self):
        self.role['attachments'].append(dict(id=900,attach_type=5,type_id=2001,count=1,level=1,equip_order=0,equip_pos=0))
        self.backend.save(self.role)
        request = encode(1037,dict(serial_num=100001,flag=3,obj_type=5,src_id=900,src_order=0,des_order=1,des_equip_pos=1))
        packets = self.backend.respond(request, {'authenticated':True})
        role = self.backend.profile()
        rows = [decode(p) for p in packets]
        totals = [a['value'] for m,_,d in rows if m == 1032 and d['unit_type']==1 for a in d['attr_list'] if a['type']==30]
        scores = [a['value'] for m,_,d in rows if m == 1032 and d['unit_type']==4 for a in d['attr_list'] if a['type']==58]
        self.assertEqual(totals, [role['role_combat_power']])
        self.assertEqual(scores, [role['corteges'][0]['combat_power']])
        self.assertEqual(self.backend.respond(request, {'authenticated':True}), packets)

    def test_collection_cache_is_rebuilt_not_readded(self):
        self.role['collection_bonuses'] = dict(hp=999999)
        base = self.calculate()['hp']
        self.calculate()
        self.assertEqual(self.role['corteges'][0]['hp'], base)
        self.assertEqual(self.role['collection_bonuses']['hp'], 0)

    def test_invalid_source_values_are_rejected(self):
        for value in ('NaN', 'Infinity', True, 'wrong'):
            self.role['combat_sources'] = {'fam': {'hp': value}}
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.calculate()

    def engraved(self, kind, level=1, slot=1, **extra):
        item = dict(id=900 + len(self.role['attachments']), attach_type=5, type_id=kind,
                    level=level, ext_skill_pos=slot, count=1, owner_id=self.role['corteges'][0]['id'])
        item.update(extra)
        self.role['attachments'].append(item)
        self.role['corteges'][0]['equiped_ext_skill_limit'] = 4
        return item

    def test_v11_reference_and_single_final_floor(self):
        self.assertEqual(cp.score_panel(dict(gongji=10000, fangyu=5000, magic=3000, hp=20000), self.rules['combat_weights']), 51000)
        self.assertEqual(cp.score_panel(dict(gongji=0, fangyu=1, magic=1, hp=3), self.rules['combat_weights']), 4)

    def test_all_190_scores_and_no_double_multiplier(self):
        c = self.role['corteges'][0]
        for kind, scores in cp.ESSENCE_SCORES.items():
            for level, score in enumerate(scores, 1):
                self.role['attachments'] = []
                self.engraved(kind, level)
                with self.subTest(kind=kind, level=level):
                    self.assertEqual(cp.essence_score(self.role, c)['total'], score)
        self.assertEqual(cp.ESSENCE_SCORES[10101][0], 419)
        self.assertEqual(cp.ESSENCE_SCORES[10216][4], 17280)

    def test_combinations_use_original_parameters_and_half_up(self):
        c = self.role['corteges'][0]
        for types, expected, correction in (
                ((10114,10110), 59+813+122, 'lucky_heal'),
                ((10104,10111), 150+1325+80, 'parry_assault'),
                ((10107,10115), 538+504-35, 'combo_execute'),
                ((10214,10210), 157+2240+896, 'lucky_heal')):
            self.role['attachments'] = []
            for slot, kind in enumerate(types, 1):
                self.engraved(kind, slot=slot)
            score = cp.essence_score(self.role, c)
            self.assertEqual(score['total'], expected)
            self.assertNotEqual(score['corrections'][correction], 0)

    def test_inactive_invalid_duplicate_essences(self):
        c = self.role['corteges'][0]
        self.engraved(10114,5,1)
        self.engraved(10214,1,2)
        self.engraved(10110,1,3)
        self.engraved(10216,5,4, owner_id=999)
        self.engraved(10216,5,5)
        self.engraved(10216,6,4)
        self.engraved(10216,5,4,count=0)
        c['equiped_ext_skill_limit'] = 3
        report = cp.essence_score(self.role,c)
        self.assertEqual(report['total'], 157+813+325)
        self.role['attachments'].reverse()
        self.assertEqual(report, cp.essence_score(self.role,c))
        c['equiped_ext_skill_limit'] = 0
        self.assertEqual(cp.essence_score(self.role,c)['total'],0)

    def test_essence_changes_score_but_not_permanent_stats(self):
        base=copy.deepcopy(self.calculate())
        self.engraved(10213)
        changed=self.calculate()
        self.assertEqual([base[s] for s in f.STATS],[changed[s] for s in f.STATS])
        self.assertEqual(changed['combat_power'],base['combat_power']+288)
        self.assertEqual(self.role['role_combat_power'],changed['combat_power'])

    def test_invalid_policy_is_rejected(self):
        rules = copy.deepcopy(self.rules)
        rules['combat_power']['title'] = 'yes'
        path = Path(self.tmp.name) / 'rules.json'
        import json
        path.write_text(json.dumps(rules))
        with self.assertRaises(ValueError):
            f.load_rules(path)


if __name__ == '__main__':
    unittest.main()
