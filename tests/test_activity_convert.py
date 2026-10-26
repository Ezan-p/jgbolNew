"""Original 天缘 wire contract, economy, real combat and durable outcomes."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_activity import ActivityCase, NOW
from network_redirect import activity, activity_convert as cv, formation, summon, vip
from network_redirect.backend import Backend
from network_redirect.protocol import decode


class ConvertTests(ActivityCase):
    def setUp(self):
        super().setUp()
        r = self.b.profile()
        self.source = 5020
        r['vip_level'] = 10
        r.setdefault('souls', {})
        if not any(c['type'] == self.source for c in r['corteges']):
            r['corteges'].append(summon.companion(r, self.source))
        summon.add_item(r, 1024, 20)
        self.b.save(r)

    def fight(self, **kw):
        return self.req(1026, **dict(dict(fight_type=10, des_value=self.source), **kw))

    def tokens(self, role):
        return sum(i['count'] for i in role['attachments'] if i['attach_type'] == 5 and i['type_id'] == 1024)

    def test_native_array_real_battle_resources_and_duplicate(self):
        before = self.b.profile()
        with patch.object(cv, 'draw', side_effect=[[2, 3], [1, 1], [3, 2], [2, 1], [1, 5]]):
            events = self.fight()
        self.ok(events)
        cards = next(d for e, d in events if e == 70)
        self.assertEqual(cards, {1: {1: 2, 2: 3}, 2: {1: 1, 2: 1}, 3: {1: 3, 2: 2}, 4: {1: 2, 2: 1}, 5: {1: 1, 2: 5}})
        after = self.b.profile()
        self.assertEqual(after['souls'].get('5011', 0) - before.get('souls', {}).get('5011', 0), 3)
        self.assertEqual(self.tokens(after), self.tokens(before))
        for key in ('strength', 'energy', 'silver_coin', 'gold_coin'):
            self.assertEqual(after[key], before[key])
        self.assertEqual(after['activity']['convert_last_result']['rewards'][0]['object_type'], 10)
        battle = next(d for m, _, d in self.decoded if m == 1027)
        self.assertTrue(1 <= battle['final_result'] <= 3)
        self.assertGreater(len(battle['fight_result']), 0)
        lineup = next(d for m, _, d in self.decoded if m == 1028)
        self.assertEqual(lineup['des_name'], '托塔天王')
        self.assertTrue(any(c['des_type'] == 6001 for c in lineup['lineup']))
        self.assertEqual(after['achievements']['totals']['106'], 1)
        self.assertEqual(self.b.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.b.profile(), after)

    def test_all_seven_reward_outcomes_only_first_card_granted(self):
        for kind, count, _ in cv.outputs(self.source):
            before = self.b.profile()
            with patch.object(cv, 'draw', side_effect=[[kind, count]] + [[2, 5]] * 4):
                self.ok(self.fight())
            after = self.b.profile()
            paid = int(before['convert_fight_count'] > 0)
            self.assertEqual(self.tokens(after) - self.tokens(before), (count if kind == 3 else 0) - paid)
            for tid in (self.source, 5011):
                expected = count if (kind == 1 and tid == self.source or kind == 2 and tid == 5011) else 0
                self.assertEqual(after['souls'].get(str(tid), 0) - before['souls'].get(str(tid), 0), expected)

    def test_exact_weight_boundaries_for_every_original_relationship(self):
        self.assertEqual(len(cv.TABLE), 42)
        for source in cv.TABLE:
            offset = 0
            for kind, count, weight in cv.outputs(source):
                for roll in (offset, offset + weight - 1):
                    with patch.object(cv.secrets, 'randbelow', return_value=roll):
                        self.assertEqual(cv.draw(source), [kind, count])
                offset += weight
            self.assertEqual(offset, 100)

    def test_real_defeat_consumes_attempt_without_reward(self):
        r = self.b.profile()
        for c in r['corteges']:
            c['order'] = 0
        c = summon.companion(r, 2001)
        c['order'] = 1
        r['corteges'].append(c)
        self.b.save(r)
        before = self.b.profile()
        with patch.object(cv, 'draw', side_effect=AssertionError('defeat must not draw')):
            events = self.fight()
        self.ok(events)
        self.assertEqual(next(d for e, d in events if e == 70), {})
        after = self.b.profile()
        self.assertEqual(after['convert_fight_count'], 1)
        self.assertEqual(after['souls'], before['souls'])
        self.assertEqual(after['achievements']['totals']['106'], 1)
        self.assertFalse(1 <= after['activity']['convert_last_result']['result'] <= 3)

    def test_invalid_parameters_reject_atomically(self):
        for req in (dict(des_value=1), dict(des_value=5009), dict(des_type=1), dict(des_id=123)):
            before = self.b.profile()
            self.assertEqual(self.fight(**req)[0][0], 55)
            self.assertEqual(before, self.b.profile())
        r = self.b.profile(); r['level'] = 15; self.b.save(r)
        before = self.b.profile()
        self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_empty_formation_and_missing_or_locked_token_no_charge(self):
        r = self.b.profile()
        for c in r['corteges']: c['order'] = 0
        self.b.save(r)
        before = self.b.profile(); self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(before, self.b.profile())
        r = self.b.profile(); r['corteges'][0]['order'] = 1; r['convert_fight_count'] = 1
        for i in r['attachments']:
            if i['type_id'] == 1024: i['is_lock'] = True
        self.b.save(r)
        before = self.b.profile(); self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_vip_limits_and_month_card_expiry(self):
        for level, limit in enumerate(vip.CONVERT):
            r = self.b.profile(); r.update(vip_level=level, convert_fight_count=limit, month_card_time=NOW)
            self.b.save(r)
            before = self.b.profile(); self.assertEqual(self.fight()[0][0], 55)
            self.assertEqual(before, self.b.profile())
            r['month_card_time'] = NOW + 1; self.b.save(r)
            self.ok(self.fight())
            self.assertEqual(self.b.profile()['convert_fight_count'], limit + 1)
            before = self.b.profile(); self.assertEqual(self.fight()[0][0], 55)
            self.assertEqual(before, self.b.profile())

    def test_midnight_restart_selection_receipt_and_clock_rollback(self):
        self.ok(self.fight())
        before = self.b.profile()
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.b.profile(), before)
        status = self.req(1205, flag=1)
        self.assertEqual(next(d for e, d in status if e == 48)['last_convert_type'], self.source)
        with patch('network_redirect.backend.time.time', return_value=NOW + 86400):
            r = self.b.profile(); r['attachments'] = [i for i in r['attachments'] if i['type_id'] != 1024]; self.b.save(r)
            self.ok(self.fight())
            after = self.b.profile()
            self.assertEqual(after['convert_fight_count'], 1)
            self.assertEqual(after['activity']['convert_total'], 2)
            self.assertEqual(after['achievements']['totals']['106'], 1)
        before = self.b.profile(); self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_target_souls_can_compose(self):
        r = self.b.profile(); r['corteges'] = [c for c in r['corteges'] if c['type'] != 5011]
        r['souls']['5011'] = formation.COMPOSE[5] - 1; self.b.save(r)
        with patch.object(cv, 'draw', return_value=[2, 1]): self.ok(self.fight())
        self.ok(self.req(1083, type_id=5011))
        r = self.b.profile()
        self.assertEqual(r['souls']['5011'], 0)
        self.assertTrue(any(c['type'] == 5011 for c in r['corteges']))

    def test_configuration_validation(self):
        rules = cv.load_rules()
        for key, value in [('enemy_type', 5001), ('enemy_level', 0), ('enemy_skill_level', True), ('card_count', 4), ('mode', 'official')]:
            with self.subTest(key=key), tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp) / 'rules.json'; p.write_text(json.dumps(dict(rules, **{key: value})))
                with self.assertRaises(formation.Rejected): cv.load_rules(p)

    def test_token_market_purchase_then_challenge(self):
        r = self.b.profile(); r['convert_fight_count'] = 1
        r['attachments'] = [i for i in r['attachments'] if i['type_id'] != 1024]
        self.b.save(r)
        self.assertEqual(self.fight()[0][0], 55)
        before = self.b.profile()
        self.ok(self.req(1057, first_send=0, page_id=2, index=16, type_id=1024, count=1))
        self.assertEqual(self.tokens(self.b.profile()), 1)
        self.assertEqual(self.b.profile()['gold_coin'], before['gold_coin'] - 200)
        with patch.object(cv, 'draw', return_value=[2, 1]): self.ok(self.fight())
        self.assertEqual(self.tokens(self.b.profile()), 0)

    def test_encoding_failure_rolls_back_payment_reward_and_receipt(self):
        import struct
        r = self.b.profile(); r['convert_fight_count'] = 1; self.b.save(r)
        before = self.b.profile()
        with patch.object(cv, 'encode', side_effect=struct.error('injected encoding failure')):
            self.assertEqual(self.fight()[0][0], 55)
        self.assertEqual(self.b.profile(), before)


if __name__ == '__main__': unittest.main()
