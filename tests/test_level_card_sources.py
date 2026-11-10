"""Exclusive code issuance, generic award rejection and persistence guard."""
import copy
import csv
from pathlib import Path
import re
import unittest
from unittest.mock import patch

from tests import test_gift_codes as original
from network_redirect import equipment_crafting, formation, gift_codes, item_rewards, journey, level_card, summon


class LevelCardSourceTests(unittest.TestCase):
    setUp = original.GiftCodeTests.setUp
    backend = original.GiftCodeTests.backend
    request = original.GiftCodeTests.request
    claims = original.GiftCodeTests.claims

    def packs(self):
        return [r for r in self.b.gift_code_rules['codes'] if r['group'].startswith('gift-level-card-')]

    def test_three_exact_independent_packs_replay_reload_and_use(self):
        packs = self.packs()
        self.assertEqual([r['prizes'] for r in packs], [[[5,1901,n,1]] for n in (10,20,50)])
        total = 0
        for row, count in zip(packs, (10,20,50)):
            result = self.request(row['code'])
            self.assertEqual(result['result'], 1)
            self.assertEqual(result['attach_list'][1]['attach_count'], count)
            total += count
            self.assertEqual(level_card.inventory_count(self.b.profile()), total)
            before = self.b.profile()
            self.assertEqual(self.b.respond(self.packet, {'authenticated': True}), self.replies)
            self.assertEqual(before, self.b.profile())
            self.assertEqual(self.request(row['code'])['result'], 13)
            self.assertEqual(level_card.inventory_count(self.b.profile()), total)
        self.assertEqual(total, 80)
        self.b.close(); self.b = self.backend()
        self.assertEqual(level_card.inventory_count(self.b.profile()), 80)
        for row in packs:
            self.assertEqual(self.request(row['code'])['result'], 13)
        role = self.b.profile()
        item = next(i for i in role['attachments'] if i['type_id'] == 1901)
        from network_redirect.protocol import encode
        self.serial += 1
        self.b.respond(encode(1051, dict(serial_num=self.serial, item_type=1901,
                           item_id=item['id'], item_count=1, des_type=1, des_id=0)), {'authenticated': True})
        self.assertEqual(level_card.inventory_count(self.b.profile()), 79)
        self.assertEqual(self.b.profile()['level'], role['level']+1)

    def test_generic_awards_and_direct_inventory_increase_are_rejected(self):
        before = self.b.profile()
        for grant in (lambda r: summon.add_item(r,1901,1),
                      lambda r: journey.grant(r,[5,1901,1,1]),
                      lambda r: journey.grant(r,[5,1901,1,2]),
                      lambda r: item_rewards.grant(r,[5,1901,1,1]),
                      lambda r: equipment_crafting.grant(r,[(5,1901,2,1)])):
            role = copy.deepcopy(before)
            with self.assertRaisesRegex(formation.Rejected, '只能通过激活码'):
                grant(role)
            self.assertEqual(role, before)
        role = copy.deepcopy(before)
        role['attachments'].append(dict(id=999999,attach_type=5,type_id=1901,count=1,level=1))
        with self.assertRaisesRegex(formation.Rejected, '只能通过激活码'):
            self.b.save(role)
        self.assertEqual(before, self.b.profile())

    def test_success_does_not_leave_generic_grants_authorized(self):
        self.assertEqual(self.request(self.packs()[0]['code'])['result'], 1)
        role = self.b.profile()
        with self.assertRaises(formation.Rejected):
            summon.add_item(role, 1901, 1)
        next(i for i in role['attachments'] if i['type_id']==1901)['count'] += 1
        with self.assertRaises(formation.Rejected):
            self.b.save(role)
        self.assertEqual(level_card.inventory_count(self.b.profile()), 10)

    def test_misconfigured_box_cannot_issue_cards_or_consume_the_box(self):
        rules = item_rewards.load_rules()
        tid = next(int(t) for t, rule in rules['items'].items() if rule['mode'] == 'random')
        role = self.b.profile()
        summon.add_item(role, tid, 1)
        self.b.save(role)
        before = self.b.profile()
        item = next(i for i in before['attachments'] if i['type_id'] == tid)
        from network_redirect.protocol import encode, decode
        from network_redirect.backend import login_fields
        self.serial += 1
        with patch.object(item_rewards, 'draw', return_value=[5,1901,50,1]):
            packets = self.b.respond(encode(1051, dict(serial_num=self.serial, item_type=tid,
                item_id=item['id'],item_count=1,des_type=1,des_id=0)), {'authenticated': True})
        events = [login_fields(d['data']) for mid, _, d in map(decode, packets)
                  if mid == 2998 and d['id'] == 55]
        self.assertTrue(any('只能通过激活码' in e['op_string'] for e in events), events)
        self.assertEqual(before, self.b.profile())

    def test_failed_code_issuance_rolls_back_claim_and_authorization(self):
        row = self.packs()[0]
        before, claims = self.b.profile(), self.claims()
        with patch.object(self.b, 'inventory', side_effect=ValueError('encode failure')):
            self.assertEqual(self.request(row['code'])['result'], 15)
        self.assertEqual(before, self.b.profile())
        self.assertEqual(claims, self.claims())
        with self.assertRaises(formation.Rejected):
            summon.add_item(self.b.profile(), 1901, 1)
        self.assertEqual(self.request(row['code'])['result'], 1)

    def test_current_gameplay_configs_have_no_level_card_rewards(self):
        root = Path(__file__).resolve().parents[1]
        # Reserve the item ID outside the catalog and the three code rewards.
        token = re.compile(r'(?<!\d)1901(?!\d)')
        for path in (root/'server_config').glob('*.json'):
            if path.name != 'gift_code_rules.json':
                self.assertIsNone(token.search(path.read_text()), str(path))
        for path in (root/'analysis/configs').rglob('*.csv'):
            if path.name in ('item_base.csv','item_name.csv'):
                continue
            # Check typed reward/recipe fields, avoiding unrelated row IDs 1901.
            with path.open(encoding='utf-8-sig', newline='') as source:
                for row in csv.reader(source):
                    for value in row:
                        if '|' in value:
                            self.assertNotRegex(value, r'(?:^|/)5\|1901\|', str(path))
        rules = gift_codes.load_rules()
        issuers = [r for r in rules['codes'] if any(p[:2] == [5,1901] for p in r['prizes'])]
        self.assertEqual(issuers, self.packs())
