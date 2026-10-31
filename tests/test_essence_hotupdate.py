"""1263 essence rules: actual wire transactions and deterministic battle boundaries."""
import copy
import csv
import io
from fractions import Fraction as F
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect import combat, combat_power, combat_engine, immortal, summon, spirit_array, journey
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import encode, decode
from tests.test_combat_engine import unit

ROOT = Path(__file__).resolve().parents[1]


class LockTransactions(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.backend.close())
        self.state, self.serial = dict(authenticated=True), 60000
        role = self.backend.profile()
        role.update(level=60, gold_coin=10000)
        c = role['corteges'][0]
        self.cid = c['id']
        c.update(equiped_ext_skill_limit=4, fate_rebullding_state=1, spirit_earth_level=50)
        self.protected = []
        for slot in range(1, 6):
            ident = 80000 + slot
            role['attachments'].append(dict(id=ident, type_id=10200+slot, attach_type=5,
                count=1, level=slot, owner_id=self.cid, ext_skill_pos=slot))
            self.protected.append(ident)
        self.src = 80010
        role['attachments'].append(dict(id=self.src, type_id=10211, attach_type=5, level=1, count=2))
        self.backend.save(role)

    def request(self, locks):
        self.serial += 1
        self.packet = encode(1311, dict(serial_num=self.serial, ext_skill_id=self.src,
                                       des_cortege_id=self.cid, lock_list=locks))
        self.replies = self.backend.respond(self.packet, self.state)
        return [(d['id'], login_fields(d['data'])) for m, _, d in map(decode, self.replies) if m == 2998]

    def test_four_locks_cost_once_replace_fifth_split_stack_and_persist(self):
        before = self.backend.profile()
        self.assertEqual([x[0] for x in self.request('{1,2,3,4}')], [148, 147])
        after = self.backend.profile()
        self.assertEqual(after['gold_coin'], 9000)
        for ident in self.protected[:4]:
            self.assertEqual(next(i for i in before['attachments'] if i['id'] == ident),
                             next(i for i in after['attachments'] if i['id'] == ident))
        self.assertNotIn(self.protected[4], [i['id'] for i in after['attachments']])
        instances = [i for i in after['attachments'] if i['type_id'] == 10211]
        self.assertEqual(len(instances), 2)
        self.assertEqual(sorted(i.get('ext_skill_pos', 0) for i in instances), [0, 5])
        self.assertTrue(all(i['count'] == 1 for i in instances))
        self.assertEqual(self.backend.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.backend.profile(), after)
        self.backend.close()
        self.backend = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.backend.profile()['gold_coin'], 9000)
        self.assertEqual([i for i in self.backend.profile()['attachments'] if i['type_id'] == 10211], instances)

    def test_fifth_can_be_protected_and_only_other_slot_replaced(self):
        self.assertEqual(self.request('{1,2,3,5}')[-1][0], 147)
        role = self.backend.profile()
        self.assertNotIn(self.protected[3], [i['id'] for i in role['attachments']])
        self.assertIn(self.protected[4], [i['id'] for i in role['attachments']])

    def test_invalid_and_insufficient_requests_leave_entire_save_unchanged(self):
        original = self.backend.profile()
        cases = [('{1,2,3,4,5}', None), ('{1,1,2,3}', None), ('{1,2,3,6}', None),
                 ('{[2]=1}', None), ('{true}', None), ('{1.5}', None), ('{1,2,3,4}', 'poor'),
                 ('{1,2,3,4}', 'closed'), ('{1,2,3,4}', 'inactive'),
                 ('{1,2,3,4}', 'gold'), ('{1,2,3,4}', 'locked_source'),
                 ('{1,2,3,4}', 'locked_target'), ('{1,2,3,4}', 'bad_slot')]
        for locks, mode in cases:
            with self.subTest(locks=locks, mode=mode):
                role = copy.deepcopy(original)
                if mode == 'poor': role['gold_coin'] = 999
                if mode == 'closed': role['corteges'][0]['spirit_earth_level'] = 49
                if mode == 'inactive': role['corteges'][0]['fate_rebullding_state'] = 0
                item = lambda ident: next(i for i in role['attachments'] if i['id'] == ident)
                if mode == 'gold': item(self.protected[0])['type_id'] = 10101
                if mode == 'locked_source': item(self.src)['is_lock'] = 1
                if mode == 'locked_target': item(self.protected[4])['is_lock'] = 1
                if mode == 'bad_slot': item(self.protected[4])['ext_skill_pos'] = 6
                self.backend.save(role)
                before = self.backend.profile()
                self.assertEqual(self.request(locks)[0][0], 55)
                self.assertEqual(self.backend.profile(), before)

    def test_no_fifth_ordinary_three_locks_still_cost_700(self):
        role = self.backend.profile()
        role['corteges'][0]['spirit_earth_level'] = 49
        role['attachments'] = [i for i in role['attachments'] if i['id'] != self.protected[4]]
        self.backend.save(role)
        before = self.backend.profile()
        self.assertEqual(self.request('{1,2,3,4}')[0][0], 55)
        self.assertEqual(self.backend.profile(), before)
        self.assertEqual(self.request('{1,2,3}')[-1][0], 147)
        self.assertEqual(self.backend.profile()['gold_coin'], 9300)

    def test_empty_fifth_is_filled_without_destroying_protected_essences(self):
        role = self.backend.profile()
        role['attachments'] = [i for i in role['attachments'] if i['id'] != self.protected[4]]
        self.backend.save(role)
        self.assertEqual(self.request('{1,2,3,4}')[-1][0], 147)
        engraved = next(i for i in self.backend.profile()['attachments'] if i.get('ext_skill_pos') == 5)
        self.assertEqual(engraved['type_id'], 10211)

    def test_gold_predecessor_in_fifth_is_replaced_without_random_choice(self):
        role = self.backend.profile()
        next(i for i in role['attachments'] if i['id'] == self.protected[4])['type_id'] = 10111
        self.backend.save(role)
        with patch('network_redirect.immortal.secrets') as rng:
            rng.choice.side_effect = AssertionError('random replacement')
            self.assertEqual(self.request('{1,2,3,4}')[-1][0], 147)
        self.assertEqual(self.backend.profile()['gold_coin'], 9000)

    def test_response_failure_after_engraving_does_not_commit_cost_or_inventory(self):
        before = self.backend.profile()
        with patch.object(self.backend, 'item_deltas', side_effect=ValueError('encode failure')):
            self.assertEqual(self.request('{1,2,3,4}')[0][0], 55)
        self.assertEqual(self.backend.profile(), before)


class HotupdateCombat(unittest.TestCase):
    def battle(self, left=None, right=None):
        rules = journey.load_rules()
        rules['battle']['mechanics']['rulai_shield_probability'] = 0
        return combat_engine.Battle({}, (left or [unit()], right or [unit()]), rules)

    def test_exact_tables_and_every_equipped_parameter(self):
        for name in summon.ESSENCE_HOTUPDATE_TABLES:
            self.assertEqual((ROOT/'analysis/configs/essence_hotupdate'/name).read_bytes(),
                             (ROOT/'analysis/evidence/hotupdate_gap_20261031/official_csv'/name).read_bytes())
        self.assertEqual(immortal.LOCK_COST, {1:100, 2:300, 3:700, 4:1000})
        for row in csv.DictReader(io.StringIO((ROOT/'analysis/evidence/hotupdate_gap_20261031/official_csv/ext_skill.csv').read_text())):
            tid = int(row['id'])
            self.assertEqual(combat_power.ESSENCE_PARAMS[tid], row['parameter'])
            for lv in range(1, 6):
                role = dict(corteges=[dict(id=7, type=1001, order=1, equiped_ext_skill_limit=4)],
                            attachments=[dict(id=1, type_id=tid, level=lv, owner_id=7, ext_skill_pos=1, count=1, attach_type=5)])
                actor = unit()
                combat.attach_essences(role, [actor])
                expected = tuple(F(p.split('|')[lv-1].rstrip('%')) for p in row['parameter'].split('/'))
                self.assertEqual(combat.effect(actor, tid % 100), expected)

    def test_old_poison_cap_and_wrong_duration_are_rejected(self):
        for key, value in [('poison_max_damage', 10000), ('poison_duration_rounds', 2),
                           ('poison_duration_rounds', 3.0), ('poison_stack_policy', 'strongest_only')]:
            with self.subTest(key=key, value=value):
                rules = journey.load_rules()['battle']
                rules['mechanics'][key] = value
                with self.assertRaises(ValueError):
                    combat.validate_rules(rules)

    def test_intimidation_scales_buffed_attack_once(self):
        actor = unit(essences={12:(50,)}, fate_traits={'round_attack':[25]}, attack_reduction=20)
        combat.begin_action(actor, 2)
        self.assertEqual(actor['gongji'], 150)  # 100*1.5*1.25*0.8, not 187.5-20
        combat.begin_action(actor, 2)
        self.assertEqual(actor['gongji'], F(375, 2))

    def test_updated_strength_and_array_are_battle_only(self):
        role = dict(spirit_array=[dict(activated=True,skill_list=[5]*i) for i in range(1,7)])
        actor = unit(essences={13:(15,),16:(25,8)})
        spirit_array.attach_combat(role, [actor])
        self.assertEqual(actor['essences'][13], (17,))
        self.assertEqual(actor['essences'][16], (F(53,2), 8))
        battle = self.battle([actor])
        self.assertEqual(battle.sides[0][0]['max_hp'], 1170)
        self.assertEqual(battle.sides[0][0]['base_hp'], 1000)
        self.assertEqual(actor['max_hp'], 1000)
        absent = unit(essences={})
        spirit_array.attach_combat(role, [absent])
        self.assertEqual(absent['essences'], {})

    def test_poison_stacks_independently_and_expires_after_three_ticks(self):
        battle = self.battle([unit(gongji=0, essences={16:(100,10)})], [unit(hp=10000,max_hp=10000)])
        actor, target = battle.sides[0][0], battle.sides[1][0]
        with patch('network_redirect.combat.roll', side_effect=lambda p: p > 0):
            battle.round = 1
            battle.attack(actor, [target])
            for round_no in (2, 3, 4, 5):
                battle.round = round_no
                battle.upkeep()
                if round_no == 2:
                    actor['essences'][16] = (100,5)
                    battle.attack(actor, [target])
                self.assertEqual(target['hp'], {2:9000,3:7500,4:6000,5:5500}[round_no])
            self.assertNotIn('poison', target)
            battle.round = 6
            battle.upkeep()
            self.assertEqual(target['hp'], 5500)
            self.assertEqual(combat_engine.total_damage(battle.actions), 4500)

    def test_poison_cap_is_per_layer_and_cleanse_removes_all(self):
        battle = self.battle([unit(gongji=0, essences={16:(100,90)})], [unit(hp=2000000,max_hp=2000000)])
        actor, target = battle.sides[0][0], battle.sides[1][0]
        with patch('network_redirect.combat.roll', side_effect=lambda p: p > 0):
            battle.attack(actor, [target]);battle.attack(actor, [target])
            battle.round = 2;battle.upkeep()
            self.assertEqual(target['hp'], 1600000)
            target.setdefault('essences', {})[17] = (100,)
            battle.round = 3;battle.upkeep()
            self.assertNotIn('poison', target)
            self.assertEqual(target['hp'], 1600000)

    def test_lethal_first_layer_does_not_poison_revived_unit_again(self):
        battle = self.battle([unit(gongji=0, essences={16:(100,90)})],
                             [unit(hp=500,max_hp=1000,essences={19:(100,50)},essence_ids={19:10119})])
        actor, target = battle.sides[0][0], battle.sides[1][0]
        with patch('network_redirect.combat.roll', side_effect=lambda p: p > 0):
            battle.attack(actor, [target]);battle.attack(actor, [target])
            battle.round = 2;battle.upkeep()
        self.assertEqual((target['hp'], target['revive_count']), (500,1))
        self.assertNotIn('poison', target)
        self.assertEqual(combat_engine.total_damage(battle.actions), 500)
