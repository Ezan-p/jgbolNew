"""Native practice protocol, genuine combat, permanent rewards and atomicity."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.test_activity import ActivityCase, NOW
from network_redirect import activity_practice as practice, formation, journey, summon
from network_redirect.backend import Backend


class PracticeTests(ActivityCase):
    def fight(self, **kw):
        return self.req(1026, **dict(dict(fight_type=4, des_type=1, des_id=0, des_value=0), **kw))

    def test_four_rewards_real_combat_wire_and_no_resource_cost(self):
        for stat, (field, attr) in practice.FIELDS.items():
            before = self.b.profile()
            with patch.object(practice, 'draw', return_value=stat):
                events = self.fight()
            self.ok(events)
            after = self.b.profile()
            amount = self.b.activity_rules['train_increase'][stat]
            self.assertEqual([d for e, d in events if e == 5],
                             [dict(addition_field=attr, addition_value=amount)])
            self.assertEqual(after['rule_index'], before['rule_index']+1)
            for other, (key, _) in practice.FIELDS.items():
                self.assertEqual(after[key]-before[key], amount if other == stat else 0)
            for old, new in zip(before['corteges'], after['corteges']):
                for other in formation.STATS:
                    self.assertEqual(new[other]-old[other], amount if other == stat else 0)
            for key in ('strength', 'energy', 'gold_coin', 'silver_coin', 'cur_exp', 'attachments'):
                self.assertEqual(after[key], before[key])
            lineup = next(d for m, _, d in self.decoded if m == 1028)
            fight = next(d for m, _, d in self.decoded if m == 1027)
            self.assertEqual(lineup['des_name'], '阎罗王')
            self.assertEqual([c['des_type'] for c in lineup['lineup'] if c['des_type']], [5001])
            self.assertTrue(1 <= fight['final_result'] <= 3)
            self.assertGreater(fight['fight_round'], 0)
            self.assertEqual(next(d for e, d in events if e == 44)['fight_id'], fight['fight_id'])
            self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
            self.assertEqual(self.b.profile(), after)

    def test_original_enemy_stats_and_progression_independent_of_player(self):
        r = practice.load_rules()
        for index in (0, 1, 30, 55, max(formation.LEVELS)-5):
            cfg = practice.encounter(index, r)
            _, enemies = journey.fighters(self.b.profile(), cfg)
            self.assertEqual(len(enemies), 1)
            e = enemies[0]
            self.assertEqual((e['type'], e['level'], e['skills']), (5001, index+1, [(207, 1)]))
            self.assertEqual(e['hp'], 522+39*index)
            self.assertEqual(e['gongji'], int(218+15.7*index))

    def test_real_loss_retry_and_timeout_never_grant_or_consume(self):
        r = self.b.profile()
        for c in r['corteges']: c['order'] = 0
        c = summon.companion(r, 2001); c['order'] = 1; r['corteges'].append(c)
        self.b.save(r)
        for _ in range(2):
            before = self.b.profile()
            with patch.object(practice, 'draw', side_effect=AssertionError('loss must not draw')):
                events = self.fight()
            self.ok(events)
            after = self.b.profile()
            self.assertNotIn(5, [e for e, _ in events])
            self.assertEqual(after['rule_index'], before['rule_index'])
            self.assertEqual(after['activity']['practice_last_result']['enemy_level'], 1)
            self.assertFalse(1 <= after['activity']['practice_last_result']['result'] <= 3)
            for key in ('strength', 'energy', 'silver_coin', 'gold_coin', *[f for f, _ in practice.FIELDS.values()]):
                self.assertEqual(after[key], before[key])
        with patch.object(practice.journey, 'battle', return_value=(0, [], [])):
            self.ok(self.fight())
        self.assertIsNone(self.b.profile()['activity']['practice_last_result']['reward'])
        r = self.b.profile()
        for c in r['corteges']: c['level'] = 100
        self.b.save(r)
        self.ok(self.fight())
        self.assertEqual(self.b.profile()['rule_index'], 1)

    def test_unlock_exhaustion_levelup_midnight_restart_and_legacy_bonuses(self):
        r = self.b.profile(); r.update(level=4, rule_index=0, max_hp_plus=60, gongji_plus=15,
                                     fangyu_plus=15, max_magic_plus=30); self.b.save(r)
        before = self.b.profile(); self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(before, self.b.profile())
        r['level'] = 5; self.b.save(r)
        with patch.object(practice, 'draw', return_value='hp'):
            self.ok(self.fight())
        saved = self.b.profile()
        self.assertEqual(saved['max_hp_plus'], 80)
        self.assertEqual(saved['max_magic_plus'], 30)
        self.assertEqual(self.fight()[0][0], 55)
        with patch('network_redirect.backend.time.time', return_value=NOW+86400):
            self.ok(self.req(1205, flag=1))
            self.assertEqual(self.fight()[0][0], 55)
            self.assertEqual(self.b.profile()['rule_index'], 1)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.b.profile()['activity']['practice_last_result'], saved['activity']['practice_last_result'])
        self.assertEqual(self.b.profile()['max_hp_plus'], 80)
        r = self.b.profile(); r['level'] = 6; self.b.save(r)
        self.ok(self.fight()); self.assertEqual(self.b.profile()['rule_index'], 2)
        self.assertEqual(self.fight()[0][0], 55)

    def test_invalid_targets_empty_formation_and_encode_failure_atomic(self):
        for kw in (dict(des_type=2), dict(des_id=5001), dict(des_value=1)):
            before = self.b.profile(); self.assertEqual(self.fight(**kw)[0][0], 55)
            self.assertEqual(before, self.b.profile())
        before = self.b.profile()
        with patch.object(practice, 'encode', side_effect=ValueError('wire failure')):
            self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(before, self.b.profile())
        r = self.b.profile()
        for c in r['corteges']: c['order'] = 0
        self.b.save(r); before = self.b.profile()
        self.assertEqual(self.fight()[0][0], 55); self.assertEqual(before, self.b.profile())

    def test_reward_weights_and_invalid_configuration(self):
        rules = practice.load_rules()
        for i, stat in enumerate(practice.FIELDS):
            with patch.object(practice.secrets, 'randbelow', return_value=i):
                self.assertEqual(practice.draw(rules), stat)
        for key, value in [('enemy_type', 5002), ('enemy_first_level', 0), ('enemy_skill_level', True),
                           ('reward_weights', {'hp': 1}), ('reward_weights', dict.fromkeys(practice.FIELDS, -1))]:
            cfg = copy.deepcopy(rules); cfg[key] = value
            path = Path(self.tmp.name)/'invalid.json'; path.write_text(json.dumps(cfg))
            with self.assertRaises(formation.Rejected): practice.load_rules(path)

    def test_full_level_cap_progression(self):
        # Endgame formation uses real base/growth stats and ordinary battle engine.
        r = self.b.profile(); r['level'] = max(formation.LEVELS)
        for c in r['corteges']: c['order'] = 0
        for order, tid in enumerate((5004, 5009, 5011, 5020), 1):
            c = summon.companion(r, tid); c.update(order=order, level=100)
            r['corteges'].append(c)
        self.b.save(r)
        for stage in range(1, r['level']-3):
            self.ok(self.fight())
            after = self.b.profile()
            self.assertEqual(after['rule_index'], stage)
            self.assertEqual(after['activity']['practice_last_result']['enemy_level'], stage)
        self.assertEqual(self.fight()[0][0], 55)


if __name__ == '__main__':
    unittest.main()
