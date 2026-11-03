"""Actual procs produce native-compatible display metadata, never extra damage."""
import copy
import random
import unittest
from unittest.mock import patch

from network_redirect import combat, combat_engine as engine, journey
from network_redirect.backend import login_fields
from tests.test_battle_replay import decoded_packets
from tests.test_combat_engine import unit
from tests import test_combat_essence_matrix as matrix


class EssenceVisualTests(unittest.TestCase):
    def battle(self, left, right, **kw):
        return engine.Battle({}, (left, right), journey.load_rules(), **kw)

    def test_every_real_essence_tier_emits_its_own_display_code_on_both_sides(self):
        # Reuse the independent outcome scenarios; collect the actual battle,
        # not fabricated display events. This also exercises fifth-slot loadout.
        case = matrix.EquippedEssenceMatrix()
        native_fixture = case.fixture
        captured = []
        def fixture(*a, **kw):
            result = native_fixture(*a, **kw)
            captured.append(result[0])
            return result
        case.fixture = fixture
        from network_redirect import formation
        with patch('network_redirect.combat.secrets.randbelow', return_value=0), \
                patch.dict(formation.SKILLS[101], intensity='30'):
            for tid in matrix.PARAMS:
                for side in (1, 2):
                    with self.subTest(tid=tid, side=side):
                        case.check_case(tid, 5, side, 9, True)
                        b = captured[-1]
                        events = b.actions.events+b.actions.essence_visuals
                        self.assertTrue(any(e['logic_type']//10 == tid and e['who_use'] == side
                                            for e in events), tid)
                        for event in b.actions.essence_visuals:
                            self.assertTrue(0 <= event['cur_action'] <= len(b.actions)+1)
                            self.assertTrue(event['offline_essence_visual'])
                            self.assertEqual(event['skill_result_list'], [dict(
                                field=0, field_plus=0, des_order=event['des_order'])])

    def test_failed_rolls_and_absent_essences_do_not_announce_procs(self):
        for present in (False, True):
            effects = {1:(10,20,0),2:(10,20),3:(10,20),4:(10,0),6:(10,20),
                       7:(10,20),10:(10,20),11:(10,20),15:(99,10),16:(10,10),
                       17:(10,),18:(10,10),19:(10,10)} if present else {}
            b = None
            with patch('network_redirect.combat.secrets.randbelow', return_value=999999):
                b = self.battle([unit(hp=400, essences=effects)], [unit(essences=effects)])
                b.run()
            self.assertEqual(b.actions.essence_visuals, [])

    def test_render_metadata_cannot_change_rng_consumption_damage_or_result(self):
        effects = {k: tuple(float(p.split('|')[4].rstrip('%'))
                           for p in combat.ESSENCES[10200+k]['parameter'].split('/'))
                   for k in range(1,20)}
        for seed in range(6):
            teams = ([unit(i, essences=effects, skills=[(101,1)], magic=100) for i in range(1,9)],
                     [unit(i, essences=effects, skills=[(101,1)], magic=100) for i in range(1,9)])
            before = copy.deepcopy(teams)
            outputs = []
            for display in (True, False):
                rng = random.Random(seed)
                with patch('network_redirect.combat.secrets.randbelow', side_effect=rng.randrange):
                    b = self.battle(*teams)
                    if not display:
                        b.visual = lambda *a, **kw: None
                    result, lineup, actions = b.run()
                outputs.append((result, lineup, list(actions), actions.events,
                                actions.final_hp, actions.damage_totals, rng.getstate()))
            self.assertEqual(outputs[0], outputs[1])
            self.assertEqual(teams, before)

    def test_war_intent_once_per_round_pair_and_no_recursive_combo_notice(self):
        with patch('network_redirect.combat.secrets.randbelow', return_value=0):
            b = self.battle([unit(essences={12:(10,),7:(100,20)})], [unit(hp=100000,max_hp=100000)])
            for r in (1,2,2,3,4):
                b.round = r
                b.attack(b.sides[0][0], b.sides[1])
        codes = [e['logic_type'] for e in b.actions.essence_visuals]
        self.assertEqual(codes.count(101121), 2)
        self.assertEqual(codes.count(101071), 5)
        self.assertEqual(len(b.actions), 10)

    def test_entry_and_reserve_notices_follow_real_deployment_and_keep_hp_delta_separate(self):
        with patch('network_redirect.combat.secrets.randbelow', return_value=0):
            b = self.battle([unit(),unit(5,essences={13:(10,),18:(100,20)},
                                           essence_ids={13:10213,18:10218})], [unit(gongji=1000)])
            self.assertEqual(b.actions.essence_visuals, [])
            b.attack(b.sides[1][0], [b.sides[0][0]])
        strength = [e for e in b.actions.essence_visuals if e['logic_type']==102131]
        self.assertEqual(len(strength), 1)
        self.assertEqual((strength[0]['cur_action'],strength[0]['after_action']), (1,True))
        blessing = next(e for e in b.actions.events if e['logic_type']==102181)
        self.assertEqual(blessing['src_order'], 5)
        self.assertEqual(blessing['skill_result_list'][0]['hp_max_add'], 200)
        self.assertEqual(b.sides[0][1]['max_hp'], 1300)

    def test_poison_clear_expiry_and_lethal_revival_emit_cleanup(self):
        for mode in ('cleanse','expire','death'):
            with self.subTest(mode=mode), patch('network_redirect.combat.secrets.randbelow', return_value=0):
                enemy = unit(essences={19:(100,50)} if mode=='death' else {})
                b = self.battle([unit(gongji=0,essences={16:(100,10)},essence_ids={16:10216})], [enemy])
                b.attack(b.sides[0][0], b.sides[1])
                target=b.sides[1][0]
                if mode=='cleanse': target['essences'][17]=(100,)
                if mode=='death': target['hp']=1
                for r in (2,3,4): b.round=r;b.upkeep()
                codes=[e['logic_type'] for e in b.actions.essence_visuals]
                self.assertIn(102161,codes)
                self.assertIn(101171 if mode=='cleanse' else 102163,codes)
                self.assertNotIn('poison',target)

    def test_intimidation_icon_clears_on_consumption_or_death(self):
        for death in (False, True):
            with patch('network_redirect.combat.secrets.randbelow', return_value=0):
                b=self.battle([unit(essences={1:(100,20,0)},essence_ids={1:10201})], [unit()])
                b.attack(b.sides[0][0],b.sides[1])
                if death:
                    b.sides[0][0]['base_gongji']=10000
                    b.attack(b.sides[0][0],b.sides[1])
                else: b.attack(b.sides[1][0],b.sides[0])
            cleared=[v for v in b.actions.essence_visuals if v['logic_type']==102013]
            self.assertEqual(len(cleared),1)
            self.assertEqual(cleared[0]['who_use'],2)

    def test_event_transport_preserves_visual_metadata_and_original_hp_events(self):
        with patch('network_redirect.combat.secrets.randbelow',return_value=0):
            b=self.battle([unit(gongji=1,essences={1:(100,20,0),7:(100,100)})],
                          [unit(gongji=1,essences={16:(100,1),10:(100,20)})])
            _,_,actions=b.run()
        packets=engine.event_packets(actions,75001)
        restored=decoded_packets(packets)
        from network_redirect import summon
        expected=login_fields(summon.lua(engine.event_data(actions,75001)))
        actual=login_fields(restored[-1][2]['data'])
        self.assertEqual(actual,expected)
        self.assertTrue(actual['essence_visuals'])


if __name__=='__main__': unittest.main()
