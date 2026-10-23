"""Original protocol round trips with isolated, persistent immortal inventories."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from network_redirect.backend import Backend, login_fields
from network_redirect import formation, immortal, summon
from network_redirect.protocol import encode, decode


class ImmortalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(lambda: self.b.close())
        self.serial = 100000
        self.state = dict(authenticated=True)
        r = self.b.profile()
        r.update(level=60, gold_coin=10000, silver_coin=1000000)
        self.b.save(r)
        self.cid = r['corteges'][0]['id']

    def req(self, mid, **values):
        self.serial += 1
        self.packet = encode(mid, dict(serial_num=self.serial, **values))
        self.replies = self.b.respond(self.packet, self.state)
        self.decoded = [decode(x) for x in self.replies]
        self.assertEqual(self.decoded[-1][0], 1106)
        self.assertEqual(self.decoded[-1][2]['req_serial_num'], self.serial)
        return [(d['id'], login_fields(d['data'])) for m, _, d in self.decoded if m == 2998]

    def item(self, t, n=1, **kwargs):
        r = self.b.profile()
        ident = formation.new_id(r)
        r['attachments'].append(dict(id=ident, type_id=t, attach_type=5, level=1, count=n, **kwargs))
        self.b.save(r)
        return ident

    def get(self, ident):
        return next(i for i in self.b.profile()['attachments'] if i['id'] == ident)

    def engrave(self, ident, locks='{}'):
        return self.req(1311, ext_skill_id=ident, des_cortege_id=self.cid, lock_list=locks)

    def test_original_visibility_and_complete_first_open_handbook(self):
        boot = [decode(p) for p in self.b.bootstrap()]
        cfg = login_fields(boot[0][2]['data'])[15]
        self.assertTrue(cfg['adaptive_visible'])
        self.assertEqual(cfg[5], 5000)
        self.assertIn(1046, [m for m, _, d in boot])
        self.assertEqual(self.req(1048, flag=0)[-1][0], 25)
        labels = [d for m, _, d in self.decoded if m == 1044]
        self.assertEqual({d['object_type'] for d in labels}, {4, 5, 6, 15})
        cort = {x['type_id']: x['status'] for d in labels if d['object_type'] == 4 for x in d['label_list']}
        self.assertEqual(cort[5004], 2)
        self.assertEqual(cort[5001], 1)
        self.assertTrue(all(d['label_count'] <= 128 for d in labels))
        self.assertEqual(self.decoded[-2][0], 2998)

    def test_handbook_history_survives_removal_and_restart(self):
        r = self.b.profile()
        r['corteges'].append(summon.companion(r, 5001))
        self.b.save(r)
        r = self.b.profile()
        r['corteges'] = [c for c in r['corteges'] if c['type'] != 5001]
        self.b.save(r)
        self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertIn(5001, self.b.profile()['handbook']['4'])

    def test_refresh_initializes_and_chunks_souls(self):
        r = self.b.profile()
        r['souls'] = {str(t): 1 for t in list(formation.BASES)[:300]}
        self.b.save(r)
        self.req(1033, flag=2)
        souls = [d for m, _, d in self.decoded if m == 1046]
        self.assertGreater(len(souls), 1)
        self.assertTrue(souls[0]['first_send'])
        self.assertTrue(all(not d['first_send'] for d in souls[1:]))
        self.assertEqual(sum(d['spirit_count'] for d in souls), len(r['souls']))
        self.assertEqual(self.decoded[-2][2]['id'], 1)

    def test_engrave_splits_stack_and_awards_do_not_merge_into_owned(self):
        ident = self.item(10101, 2)
        events = self.engrave(ident)
        self.assertEqual([e for e, _ in events], [148, 147])
        r = self.b.profile()
        own = [i for i in r['attachments'] if i.get('owner_id') == self.cid and i['type_id'] == 10101]
        self.assertEqual((len(own), own[0]['count'], own[0]['ext_skill_pos']), (1, 1, 1))
        self.assertEqual(self.get(ident)['count'], 1)
        summon.add_item(r, 10101, 3)
        self.b.save(r)
        self.assertEqual(self.get(own[0]['id'])['count'], 1)
        self.assertEqual(self.get(ident)['count'], 4)

    def test_engrave_failure_increases_luck_and_success_opens_slot(self):
        first, second, third = [self.item(t) for t in (10101, 10102, 10103)]
        self.engrave(first)
        with patch('network_redirect.immortal.secrets.randbelow', return_value=99):
            self.engrave(second)
        c = self.b.profile()['corteges'][0]
        self.assertEqual((c['equiped_ext_skill_limit'], c['next_ext_skill_luck_point']), (1, 10))
        with patch('network_redirect.immortal.secrets.randbelow', return_value=0):
            self.engrave(third)
        c = self.b.profile()['corteges'][0]
        self.assertEqual((c['equiped_ext_skill_limit'], c['next_ext_skill_luck_point']), (2, 0))
        self.assertEqual(self.get(third)['ext_skill_pos'], 2)

    def test_flying_six_and_twelve_automatically_unlock_slots(self):
        for level, slots in ((5, 1), (6, 2), (12, 3), (60, 3)):
            r = self.b.profile()
            r['corteges'][0].update(evolve_level=level, equiped_ext_skill_limit=1)
            self.b.save(r)
            self.assertEqual(self.b.profile()['corteges'][0]['equiped_ext_skill_limit'], slots)

    def test_purple_replaces_same_family_gold_and_locked_slot_is_safe(self):
        r = self.b.profile();r['corteges'][0]['equiped_ext_skill_limit'] = 4;self.b.save(r)
        gold = self.item(10101);purple = self.item(10201)
        self.engrave(gold);self.engrave(purple)
        self.assertEqual(self.get(purple)['ext_skill_pos'], 1)
        self.assertNotIn(gold, [i['id'] for i in self.b.profile()['attachments']])
        for t in (10102, 10103, 10104):self.engrave(self.item(t))
        ident = self.item(10105)
        self.engrave(ident, '{1}')
        self.assertEqual(self.get(purple)['owner_id'], self.cid)
        self.assertEqual(self.b.profile()['gold_coin'], 9900)
        self.assertNotEqual(self.get(ident)['ext_skill_pos'], 1)

    def test_invalid_locks_and_duplicate_or_early_engraving_are_atomic(self):
        first = self.item(10101, 2);second = self.item(10102)
        self.engrave(first)
        for ident, locks in ((first, '{}'), (second, '{1,1}'), (second, '{4}'),
                             (second, '{1}'), (second, '{[1]=os.execute("bad")}')):
            before = self.b.profile()
            self.assertEqual(self.engrave(ident, locks)[0][0], 55)
            self.assertEqual(before, self.b.profile())
        r = self.b.profile();r['level'] = 37;self.b.save(r)
        before = self.b.profile();self.assertEqual(self.engrave(second)[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_upgrade_consumes_exact_progress_and_caps_at_five(self):
        ident = self.item(10101);stones = self.item(10000, 7000);self.engrave(ident)
        for level, need in immortal.UPGRADE_COST.items():
            for _ in range(need // 500):
                self.assertEqual(self.req(1322, ext_skill_id=ident, cost_count=500)[-1][0], 146)
            self.assertEqual(self.get(ident)['level'], level + 1)
            self.assertEqual(self.get(ident)['prob_compen'], 0)
        before = self.b.profile()
        self.assertEqual(self.req(1322, ext_skill_id=ident, cost_count=1)[0][0], 55)
        self.assertEqual(before, self.b.profile())
        self.assertEqual(self.get(stones)['count'], 1000)

    def test_upgrade_rejects_overpayment_unowned_and_short_balance(self):
        ident = self.item(10101);self.item(10000, 499)
        self.assertEqual(self.req(1322, ext_skill_id=ident, cost_count=1)[0][0], 55)
        self.engrave(ident)
        for count in (0, 501, 500):
            before = self.b.profile()
            self.assertEqual(self.req(1322, ext_skill_id=ident, cost_count=count)[0][0], 55)
            self.assertEqual(before, self.b.profile())
        self.req(1322, ext_skill_id=ident, cost_count=200)
        self.assertEqual(self.get(ident)['prob_compen'], 200)

    def test_exchange_realms_counts_currency_and_failures(self):
        category = int(formation.BASES[5004]['category'])
        ident = self.item(5000 + category, 10)
        self.assertEqual(self.req(1051, item_type=5000 + category, item_id=ident, item_count=3, des_type=4, des_id=5004)[0][0], 21)
        self.assertEqual(self.b.profile()['souls']['5004'], 3)
        self.assertEqual(self.get(ident)['count'], 7)
        self.assertEqual(self.b.profile()['silver_coin'], 985000)
        for changes in (dict(des_id=5001), dict(item_count=8), dict(item_count=0), dict(item_type=5000), dict(des_type=5)):
            before = self.b.profile()
            data = dict(item_type=5000 + category, item_id=ident, item_count=1, des_type=4, des_id=5004);data.update(changes)
            self.assertEqual(self.req(1051, **data)[0][0], 55)
            self.assertEqual(before, self.b.profile())

    def test_transform_original_group_level_material_and_no_owned_merge(self):
        source = self.item(10207, 2);pill = self.item(1342, 1)
        dest = self.item(10211);self.engrave(dest)
        self.assertEqual(self.req(1074, flag=4, num=1, des_type=10211, count=1, id_list=[dict(id=source)])[-1][1]['result'], 1)
        self.assertEqual(self.get(source)['count'], 1)
        self.assertEqual(self.get(dest)['count'], 1)
        self.assertNotIn(pill, [i['id'] for i in self.b.profile()['attachments']])
        before = self.b.profile()
        self.assertEqual(self.req(1074, flag=4, num=1, des_type=10201, count=1, id_list=[dict(id=source)])[0][0], 55)
        self.assertEqual(before, self.b.profile())

    def test_collection_activation_is_per_slot_persistent_and_applies_once(self):
        r = self.b.profile()
        for t in (5011, 5009, 5020):r['corteges'].append(summon.companion(r, t))
        self.b.save(r);self.item(1002, 4)
        baseline = self.b.profile()['corteges'][0]['fangyu']
        events = self.req(1305)
        self.assertEqual(events[0][1]['line_up'][12]['flag'], 4)
        for pos in range(1, 5):
            result = self.req(1306, index=12, value=pos)[-1][1]
            self.assertEqual(result['activate_data']['line_up'][12]['flag'], 4 - pos)
        r = self.b.profile()
        self.assertEqual(r['collection_bonuses']['fangyu'], 100)
        self.assertEqual(r['corteges'][0]['fangyu'], baseline + 100)
        for _ in range(3):self.assertEqual(self.b.profile(), r)
        self.assertEqual(self.req(1306, index=12, value=4)[0][0], 55)
        self.assertEqual(self.b.profile(), r)

        attrs = [a for m, _, d in map(decode, self.b.bootstrap()) if m == 1032
                 for a in d['attr_list']]
        self.assertIn(dict(type=89, value=100), attrs)

    def test_replay_and_reused_serial_never_consume_twice(self):
        ident = self.item(10101);self.engrave(ident)
        packet, replies, before = self.packet, self.replies, self.b.profile()
        self.assertEqual(self.b.respond(packet, self.state), replies)
        self.assertEqual(self.b.profile(), before)

        conflicting = encode(1322, dict(serial_num=self.serial, ext_skill_id=ident, cost_count=1))
        result = self.b.respond(conflicting, self.state)
        self.assertEqual(decode(result[0])[2]['id'], 55)
        self.assertEqual(self.b.profile(), before)

    def test_decompose_original_cost_yield_and_atomic_rejection(self):
        gold, purple = self.item(10101, 2), self.item(10201)
        before = self.b.profile()['silver_coin']
        for ident, count, gain in ((gold, 2, 40), (purple, 1, 100)):
            result = self.req(1074, flag=3, count=1, num=count, id_list=[dict(id=ident)], des_type=1)
            self.assertEqual(result[-1], (116, dict(result=1, flag=3, item_list={1: dict(object_type=5, attach_type=10000, attach_level=1, attach_count=gain)})))
        self.assertEqual(self.b.profile()['silver_coin'], before - 3000)
        self.assertEqual(sum(i['count'] for i in self.b.profile()['attachments'] if i['type_id'] == 10000), 140)
        ident = self.item(10102, is_lock=True)
        before = self.b.profile()
        self.assertEqual(self.req(1074, flag=3, count=1, num=1, id_list=[dict(id=ident)], des_type=1)[0][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_encode_failure_rolls_back_entire_transaction(self):
        ident = self.item(10101)
        before = self.b.profile()
        with patch('network_redirect.backend.immortal.handbook', side_effect=ValueError('injected serialization error')):
            self.assertEqual(self.engrave(ident)[0][0], 55)
        self.assertEqual(self.b.profile(), before)

    def test_bad_config_fails_closed(self):
        for changes in (dict(essence_slots=5), dict(mode='official'), dict(exchange_silver_per_soul={'5': -1}), dict(essence_unlock_base_percent=True)):
            r = copy.deepcopy(self.b.immortal_rules);r.update(changes)
            path = Path(self.tmp.name) / 'rules.json';path.write_text(json.dumps(r))
            with self.assertRaises(formation.Rejected):immortal.load_rules(path)


if __name__ == '__main__':
    unittest.main()
