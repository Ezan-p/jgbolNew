"""Every equipped essence/level executes on both sides of the 8/9-slot engine.

Use real inventory and loadout attachment, then deterministic successful/failed
rolls. Assertions check observable damage, HP, actions and status lifetime.
"""
import copy
import csv
from fractions import Fraction as F
from pathlib import Path
import unittest
from unittest.mock import patch

from network_redirect import combat, combat_engine, combat_loadout, formation, journey, summon
from network_redirect import activity_abyss_combat as abyss
from tests.test_combat_engine import unit


EVIDENCE = Path(__file__).resolve().parents[1] / 'analysis/evidence/hotupdate_gap_20261031/official_csv/ext_skill.csv'
with EVIDENCE.open() as source:
    PARAMS = {int(row['id']): row['parameter'] for row in csv.DictReader(source)}


class EquippedEssenceMatrix(unittest.TestCase):
    def fixture(self, tid, level, side, slots, **values):
        # Ninth cell deliberately differs from the owner's permanent position.
        order = 9 if slots == 9 else 1
        subject = unit(order, companion_id=7, hp=1000000, max_hp=1000000,
                       gongji=10000, magic=10000)
        subject.update(values)
        role = dict(corteges=[dict(id=7, type=1001, order=1, equiped_ext_skill_limit=4,
                                  fate_rebullding_state=slots == 9, spirit_earth_level=50)],
                    attachments=[dict(id=31, type_id=tid, level=level, owner_id=7,
                                      attach_type=5, ext_skill_pos=5 if slots == 9 else 1, count=1)])
        before = copy.deepcopy(role)
        combat_loadout.attach_owned_bonuses(role, [subject])
        expected = tuple(F(p.split('|')[level-1].rstrip('%')) for p in PARAMS[tid].split('/'))
        self.assertEqual(subject['essences'], {tid % 100: expected})
        self.assertEqual(subject['essence_ids'], {tid % 100: tid})
        enemy = unit(hp=1000000, max_hp=1000000, gongji=10000, magic=10000)
        sides = ([subject], [enemy]) if side == 1 else ([enemy], [subject])
        battle = combat_engine.Battle({}, sides, journey.load_rules(), slots=slots)
        battle.round = 1
        self.assertEqual(role, before)
        return battle, battle.sides[side-1][0], battle.sides[2-side][0], expected

    def hit(self, battle, actor, target, skill=1, **options):
        start = len(battle.actions)
        battle.attack(actor, [target], skill=skill, **options)
        return [row['damage_list'][target['order']-1] for row in battle.actions[start:]]

    def check_case(self, tid, level, side, slots, succeeds):
        family = tid % 100
        b, subject, enemy, p = self.fixture(tid, level, side, slots)
        # Spell 101 with intensity 30: (10000/4+3*10000)*1.2*2/(N+1).
        spell = F(78000, (4 if slots == 8 else 9) + 1)
        if family == 1:
            self.hit(b, subject, enemy)
            self.assertEqual(enemy.get('attack_reduction', 0), p[1] if succeeds else 0)
            self.assertEqual(self.hit(b, enemy, subject), [int(10000*(1-p[1]/100)) if succeeds else 10000])
            self.assertEqual(self.hit(b, enemy, subject), [10000])
            # Its anti-assault component is unconditional, even if debuff failed.
            enemy['essences'] = {11: (100, 50)}
            self.assertEqual(self.hit(b, enemy, subject), [int(10000*(1+F(1, 2)*(1-p[2]/100)))])
        elif family == 2:
            enemy['fangyu'] = enemy['base_fangyu'] = 1000
            expected = int(10000-1000*(1-p[1]/100)) if succeeds else 9000
            self.assertEqual(self.hit(b, subject, enemy), [expected])
            self.assertEqual(self.hit(b, subject, enemy), [expected])
            self.assertEqual(enemy['fangyu'], 1000*(1-p[1]/100) if succeeds else 1000)
        elif family == 3:
            self.hit(b, enemy, subject)
            self.assertEqual(len(b.actions), 2 if succeeds else 1)
            if succeeds:
                self.assertEqual(b.actions[1]['damage_list'][enemy['order']-1], int(10000*p[1]/100))
                self.assertEqual(b.actions[1]['is_src'], side == 1)
        elif family == 4:
            subject['essences'][11] = (100, 50)
            enemy['essences'] = {3: (100, 50)}
            hits = self.hit(b, subject, enemy)
            self.assertEqual(hits[0], int(10000*(1+F(1, 2)*(1+p[1]/100))))
            self.assertEqual(len(b.actions), 1 if succeeds else 2)
        elif family == 5:
            subject['hp'], enemy['hp'] = 500000, 1000
            self.hit(b, subject, enemy)
            gain = int(1000*p[0]/100)
            self.assertEqual(subject['hp'], 500000+gain)
            self.assertEqual(b.actions.damage_totals[side], 1000)
            self.assertEqual(b.actions.events[0]['logic_type'], tid*10+1)
        elif family == 6:
            self.assertEqual(self.hit(b, enemy, subject), [int(10000*(1-p[1]/100)) if succeeds else 10000])
            self.assertEqual(self.hit(b, enemy, subject, 101), [int(spell)])
        elif family == 7:
            self.assertEqual(self.hit(b, subject, enemy), [10000, int(10000*p[1]/100)] if succeeds else [10000])
        elif family == 8:
            self.assertEqual(self.hit(b, enemy, subject, 101), [int(spell*(1-p[0]/100))])
            self.assertEqual(self.hit(b, enemy, subject), [10000])
        elif family == 9:
            enemy['essences'] = {8: (50,)}
            self.assertEqual(self.hit(b, subject, enemy, 101), [int(spell*(1-F(1, 2)*(1-p[0]/100)))])
            enemy['essences'] = {}
            self.assertEqual(self.hit(b, subject, enemy, 101), [int(spell)])
            subject['skills'] = [(101, 1)]
            bonus = 3 if tid < 10200 else 6
            for draw, expected in (((10+bonus)*10000-1, 101), ((10+bonus)*10000, 1)):
                with patch('network_redirect.combat.secrets.randbelow', return_value=draw):
                    self.assertEqual(combat.select_skill(subject, b.rules), (expected, 1))
            subject['skill_probabilities'] = {101: 0}
            self.assertEqual(combat.select_skill(subject, b.rules), (1, 1))
        elif family == 10:
            subject['hp'] = 100000
            b.upkeep()
            self.assertEqual(subject['hp'], 100000)
            b.round = 2
            b.upkeep()
            self.assertEqual(subject['hp'], 100000+(int(1000000*p[1]/100) if succeeds else 0))
            subject['hp'] = subject['max_hp']-1
            b.upkeep()
            self.assertEqual(subject['hp'], subject['max_hp']-(0 if succeeds else 1))
        elif family == 11:
            self.assertEqual(self.hit(b, subject, enemy), [int(10000*(1+p[1]/100)) if succeeds else 10000])
            self.assertEqual(self.hit(b, subject, enemy, 101), [int(spell)])
        elif family == 12:
            for round_no, times in ((1, 0), (2, 1), (2, 1), (3, 1), (4, 2)):
                b.round = round_no
                self.assertEqual(self.hit(b, subject, enemy), [int(10000*(1+times*p[0]/100))])
        elif family == 13:
            extra = int(1000000*p[0]/100)
            self.assertEqual((subject['hp'], subject['max_hp']), (1000000+extra, 1000000+extra))
            self.assertEqual(subject['base_hp'], 1000000)
            self.hit(b, enemy, subject)
            self.assertEqual(subject['max_hp'], 1000000+extra)
        elif family == 14:
            subject['hp'] = 100000
            subject['essences'][10] = (100, 10)
            b.round = 2
            b.upkeep()
            self.assertEqual(subject['hp'], 100000+int(100000*(1+p[0]/100)))
            self.assertEqual(self.hit(b, enemy, subject, kind='execute'), [0 if succeeds else 10000])
            self.assertEqual(self.hit(b, enemy, subject), [10000])
            self.assertEqual(self.hit(b, enemy, subject, kind='combo'), [10000])
        elif family == 15:
            threshold_hp = int(enemy['max_hp']*p[0]/100)
            enemy['hp'] = threshold_hp+10000
            self.assertEqual(self.hit(b, subject, enemy), [10000])
            enemy['hp'] = threshold_hp+9999
            self.assertEqual(self.hit(b, subject, enemy), [10000, 10000] if succeeds else [10000])
            subject.setdefault('essences', {})[7] = (100, 50)
            enemy['hp'] = threshold_hp+9999
            self.assertEqual(self.hit(b, subject, enemy), [10000, 5000])
        elif family == 16:
            subject['gongji'] = subject['base_gongji'] = 0
            self.hit(b, subject, enemy)
            self.hit(b, subject, enemy)
            self.assertEqual(len(enemy.get('poison', {}).get('layers', [])), 2 if succeeds else 0)
            tick = int(1000000*p[1]/100) if succeeds else 0
            for round_no in (2, 3, 4, 5):
                b.round = round_no
                b.upkeep()
                self.assertEqual(enemy['hp'], 1000000-2*tick*min(3, round_no-1))
            self.assertNotIn('poison', enemy)
            self.assertEqual(b.actions.damage_totals[side], 6*tick)
            self.assertTrue(all(e['logic_type'] == tid*10+2 for e in b.actions.events))
        elif family == 17:
            subject['poison'] = dict(layers=[dict(rate=10, source_side=3-side, logic=101162, remaining=3),
                                           dict(rate=5, source_side=3-side, logic=102162, remaining=3)])
            b.round = 2
            b.upkeep()
            self.assertEqual(subject['hp'], 1000000 if succeeds else 850000)
            self.assertEqual('poison' in subject, not succeeds)
        elif family == 18:
            self.assertEqual(subject['gongji'], int(10000*(1+p[1]/100)) if succeeds else 10000)
            self.assertEqual(subject['magic'], int(10000*(1+p[1]/100)) if succeeds else 10000)
            maximum = 1000000+(int(1000000*p[1]/100) if succeeds else 0)
            self.assertEqual((subject['hp'], subject['max_hp']), (maximum, maximum))
            b.deploy()
            self.assertEqual(subject['max_hp'], maximum)
        elif family == 19:
            enemy['gongji'] = enemy['base_gongji'] = 2000000
            limit = (1 if tid < 10200 else 2) if succeeds else 0
            for attempt in range(limit+1):
                self.hit(b, enemy, subject)
                self.assertEqual(subject['hp'], int(1000000*p[1]/100) if attempt < limit else 0)
            self.assertEqual(subject['revive_count'], limit)
            self.assertEqual([e['logic_type'] for e in b.actions.events], [tid*10+1]*limit)
        else:
            self.fail('Missing essence family scenario: %s' % family)

        # Every HP event must point to an existing action and recipient.
        hp = {(s, u['order']): u['hp'] for s, team in enumerate(b.initial, 1) for u in team}
        for event in b.actions.events:
            self.assertTrue(1 <= event['cur_action'] <= len(b.actions))
            self.assertIn((event['who_use'], event['des_order']), hp)


def make_case(tid, level):
    def test(self):
        params = tuple(F(p.split('|')[level-1].rstrip('%')) for p in PARAMS[tid].split('/'))
        probability_index = {1: 0, 2: 0, 3: 0, 4: 0, 6: 0, 7: 0, 10: 0,
                             11: 0, 14: 1, 15: 1, 16: 0, 17: 0, 18: 0, 19: 0}.get(tid % 100)
        for side in (1, 2):
            for slots in (8, 9):
                for succeeds in (True, False):
                    draw = (int(params[probability_index]*10000)-(1 if succeeds else 0)
                            if probability_index is not None else (0 if succeeds else 999999))
                    with self.subTest(side=side, slots=slots, succeeds=succeeds), \
                            patch('network_redirect.combat.secrets.randbelow', side_effect=lambda n: draw if n == 1000000 else 0), \
                            patch.dict(formation.SKILLS[101], intensity='30'):
                        self.check_case(tid, level, side, slots, succeeds)
    return test


for _tid in sorted(PARAMS):
    for _level in range(1, 6):
        setattr(EquippedEssenceMatrix, 'test_equipped_%s_level_%s' % (_tid, _level), make_case(_tid, _level))


SPECTER = {int(row['type_id']): row for row in summon.rows('specter_jp_desc.csv')}


class SpecterEssenceMatrix(unittest.TestCase):
    hit = EquippedEssenceMatrix.hit
    check_case = EquippedEssenceMatrix.check_case

    def fixture(self, tid, level, side, slots):
        row = dict(ext_skill_list='1|%s|%s|0' % (tid, level))
        effects = abyss.effects(row, {})
        expected = tuple(F(p.split('|')[level-1].rstrip('%'))
                         for p in SPECTER[tid]['desc_value'].split('/'))
        subject = unit(hp=1000000, max_hp=1000000, gongji=10000, magic=10000,
                       extras=effects)
        self.assertEqual(combat.effect(subject, tid % 100), expected)
        enemy = unit(hp=1000000, max_hp=1000000, gongji=10000, magic=10000)
        b = combat_engine.Battle({}, ([enemy], [subject]), journey.load_rules())
        b.round = 1
        return b, b.sides[1][0], b.sides[0][0], expected

    def test_complete_catalog(self):
        self.assertEqual(set(PARAMS), set(range(10101, 10120)) | set(range(10201, 10220)))
        self.assertEqual(len(SPECTER), 12)

    def test_all_suppressants_only_reduce_named_effects_and_never_go_negative(self):
        # Each tier's drug is intended to completely suppress its own tier,
        # except the original 1619 war-intent value (30 versus tier-2's 40).
        for level, drugs in enumerate(((1597, 1598, 1599, 1600), (1617, 1618, 1619, 1620),
                                       (1637, 1638, 1639, 1640), (1657, 1658, 1659, 1660)), 1):
            row = dict(ext_skill_list='/'.join('1|%s|%s|0' % (tid, level) for tid in SPECTER))
            expected = dict.fromkeys(SPECTER, 0)
            if level == 2:
                expected[10112] = 10
            self.assertEqual(abyss.effects(row, dict(enumerate(drugs))), expected)
            weak = dict(ext_skill_list='/'.join('1|%s|1|0' % tid for tid in SPECTER))
            self.assertEqual(abyss.effects(weak, dict(enumerate(drugs))), dict.fromkeys(SPECTER, 0))
        row = dict(ext_skill_list='1|10102|1|0/1|10105|1|0')
        self.assertEqual(abyss.effects(row, {1: 1597}), {10102: 0, 10105: 10})


def make_specter_case(tid, level):
    def test(self):
        # Even the largest random draw must trigger the NPC's documented 100%.
        with patch('network_redirect.combat.secrets.randbelow', return_value=999999), \
                patch.dict(formation.SKILLS[101], intensity='30'):
            self.check_case(tid, level, 2, 8, True)
    return test


for _tid in sorted(SPECTER):
    for _level in range(1, 5):
        setattr(SpecterEssenceMatrix, 'test_specter_%s_level_%s' % (_tid, _level), make_specter_case(_tid, _level))


if __name__ == '__main__':
    unittest.main()
