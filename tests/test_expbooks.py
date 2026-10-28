"""All original scroll IDs over the real wire, plus settlement boundary regressions."""
import copy
import time
import unittest
from pathlib import Path

from network_redirect import achievements, formation as f, summon
from network_redirect.protocol import MAX_PACKET, decode
from tests import test_formation


# Literal original item_base values: protects against replacing tiers with a formula.
BOOK_EXP = [1200, 2480, 10000, 20000, 20000, 32000, 21600, 44000,
            35200, 80000, 50000, 120000, 80000, 200000, 100000, 368000,
            132000, 512000, 208000, 800000, 360000, 1440000, 640000, 2560000,
            1016000, 4000000, 1800000, 7200000, 6000000, 24000000,
            10800000, 44000000, 17064000, 70400000, 24401520, 100672000,
            30400000, 120000000, 38400000, 156000000]


class ExpbookTests(unittest.TestCase):
    setUp = test_formation.FormationTests.setUp
    request = test_formation.FormationTests.request
    events = test_formation.FormationTests.events
    ok = test_formation.FormationTests.ok
    rejected = test_formation.FormationTests.rejected
    add_item = test_formation.FormationTests.add_item

    def configure(self, level=80, companion_level=1, cur_exp=0, extra_cap=0):
        role = self.backend.profile()
        role.update(level=level, cortege_limit_plus=extra_cap)
        role['corteges'][0].update(level=companion_level, cur_exp=cur_exp, culture_point=0)
        self.backend.save(role)
        return role

    def consume(self, rolls, flag=1, reject=False):
        return (self.rejected if reject else self.ok)(1059, first_send=True, flag=flag,
                    cortege_id=self.ids[0], roll_count=len(rolls),
                    roll_list=[dict(type_id=t, count=n) for t, n in rolls])

    def total_exp(self, c):
        q = int(f.BASES[c['type']]['quality'])
        return sum(f.EXPERIENCE[q, n] for n in range(1, c['level'])) + c['cur_exp']

    def test_all_forty_ids_exact_experience_wire_and_achievement(self):
        self.assertEqual(f.EXPERIENCE_BOOKS, set(range(1041, 1081)))
        for tid, xp in enumerate(BOOK_EXP, 1041):
            with self.subTest(type_id=tid):
                role = self.configure()
                role['achievements']['totals'].pop('117', None)
                self.backend.save(role)
                self.add_item(tid)
                out = self.consume([(tid, 1)])
                role = self.backend.profile()
                self.assertEqual(self.total_exp(role['corteges'][0]), xp)
                self.assertEqual(dict(self.events(out))[65]['experience'], xp)
                self.assertEqual(role['achievements']['totals']['117'], 1)
                self.assertTrue(any(m == 1066 and any(a['id'] == 117 and a['times'] == 1
                               for a in data['achievements']) for m, _, data in out))
                self.assertEqual(role['corteges'][0]['culture_point'], (role['corteges'][0]['level'] - 1) * 5)

    def test_every_quality_uses_its_own_level_curve(self):
        baseline = self.configure()
        for quality in range(1, 6):
            tid = next(t for t, r in f.BASES.items() if int(r['quality']) == quality)
            for book, xp in enumerate(BOOK_EXP, 1041):
                with self.subTest(quality=quality, book=book):
                    role = copy.deepcopy(baseline)
                    c = role['corteges'][0]; c['type'] = tid
                    summon.add_item(role, book, 1)
                    f.feed(role, dict(flag=1, first_send=True, cortege_id=c['id'], roll_count=1,
                                     roll_list=[dict(type_id=book, count=1)]), self.backend.formation_rules)
                    self.assertEqual(self.total_exp(c), xp)

    def test_mixed_same_names_and_instance_levels_do_not_merge(self):
        self.configure()
        identity = self.add_item(1041, 2)
        role = self.backend.profile()
        f.lookup(role, 'attachments', identity)['level'] = 99
        self.backend.save(role)
        self.add_item(1043, 1)
        self.add_item(1042, 3)
        other = self.add_item(1080, 1)
        self.consume([(1041, 2), (1043, 1), (1042, 3)])
        role = self.backend.profile()
        self.assertEqual(self.total_exp(role['corteges'][0]), 19840)
        self.assertEqual(f.lookup(role, 'attachments', other)['count'], 1)

    def test_split_stacks_skip_locked_inventory(self):
        self.configure()
        self.add_item(1041, 1); self.add_item(1041, 2)
        locked = self.add_item(1041, 10, is_lock=1)
        self.consume([(1041, 3)])
        role = self.backend.profile()
        self.assertEqual(self.total_exp(role['corteges'][0]), 3600)
        self.assertEqual(f.lookup(role, 'attachments', locked)['count'], 10)
        self.consume([(1041, 1)], reject=True)

    def test_cross_discount_threshold_and_fractional_experience(self):
        self.configure(level=21, companion_level=51, cur_exp=f.EXPERIENCE[5, 51] - 100)
        self.add_item(1041)
        out = self.consume([(1041, 1)])
        c = self.backend.profile()['corteges'][0]
        self.assertEqual((c['level'], c['cur_exp']), (52, 220))
        self.assertEqual(dict(self.events(out))[65]['experience'], 320)
        self.configure(level=21, companion_level=52, cur_exp=0.1)
        self.add_item(1041, 3)
        for _ in range(3): self.consume([(1041, 1)])
        self.assertEqual(self.backend.profile()['corteges'][0]['cur_exp'], 720.1)

    def test_caps_and_overflow_policy(self):
        for player, cap, extra in ((20, 60, 0), (79, 200, 0), (80, 200, 0), (80, 205, 5)):
            with self.subTest(player=player, cap=cap):
                self.configure(player, cap - 1, f.EXPERIENCE[5, cap - 1] - 10, extra)
                self.add_item(1080, 2)
                out = self.consume([(1080, 1)])
                c = self.backend.profile()['corteges'][0]
                self.assertEqual((c['level'], c['cur_exp']), (cap, 0))
                self.assertEqual(dict(self.events(out))[65]['experience'], 10)
                self.consume([(1080, 1)], reject=True)

    def test_level_eighty_removes_discount(self):
        for level, xp in ((79, 240), (80, 1200)):
            self.configure(level, 198)
            self.add_item(1041)
            self.consume([(1041, 1)])
            self.assertEqual(self.backend.profile()['corteges'][0]['cur_exp'], xp)

    def test_invalid_batches_leave_entire_save_unchanged(self):
        self.configure(); self.add_item(1041, 4); self.add_item(1401, 1)
        for rolls in ([], [(1041, 1), (1041, 1)], [(1041, 5)], [(1041, 0)],
                      [(1041, 1), (9999, 1)], [(1041, 1), (1401, 1)]):
            with self.subTest(rolls=rolls): self.consume(rolls, reject=True)
        self.rejected(1059, first_send=False, flag=1, cortege_id=self.ids[0],
                      roll_count=1, roll_list=[dict(type_id=1041, count=1)])
        self.rejected(1059, first_send=True, flag=1, cortege_id=999999,
                      roll_count=1, roll_list=[dict(type_id=1041, count=1)])

    def test_direct_batch_validation_does_not_debit_valid_prefix(self):
        role = self.configure(); summon.add_item(role, 1041, 1)
        before = copy.deepcopy(role)
        with self.assertRaises(f.Rejected):
            f.feed(role, dict(flag=1, first_send=True, cortege_id=self.ids[0], roll_count=2,
                             roll_list=[dict(type_id=1041, count=1), dict(type_id=1080, count=1)]),
                   self.backend.formation_rules)
        self.assertEqual(role, before)

    def test_pills_do_not_award_book_achievement(self):
        self.configure(); self.add_item(1401)
        self.consume([(1401, 1)], flag=2)
        self.assertEqual(self.backend.profile()['achievements']['totals'].get('117', 0), 0)

    def test_inventory_loss_without_book_protocol_does_not_award(self):
        before = self.configure(); summon.add_item(before, 1041, 1)
        for mid, req in ((1051, {'item_type': 1041}), (1088, {}), (1059, {'flag': 2})):
            after = copy.deepcopy(before); f.debit_item(after, 1041, 1)
            achievements.track(after, before, mid, req, 1792987200)
            self.assertEqual(after['achievements']['totals'].get('117', 0), 0)

    def test_replay_and_reopen_preserve_experience_and_achievement(self):
        self.configure(); self.add_item(1080, 2)
        self.consume([(1080, 1)])
        before = self.backend.profile()
        self.assertEqual(self.backend.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.backend.profile(), before)
        self.backend.close()
        self.backend = type(self.backend)(Path(self.directory.name), 18770, lambda *a, **k: None)
        self.assertEqual(self.backend.profile(), before)

    def test_million_scroll_batch_stays_compact_and_debits_once(self):
        self.configure(level=99)
        identity = self.add_item(1041, 1_000_003)
        started = time.perf_counter()
        out = self.consume([(1041, 1_000_000)])
        elapsed = time.perf_counter() - started
        role = self.backend.profile()
        self.assertEqual(self.total_exp(role['corteges'][0]), 1_200_000_000)
        self.assertEqual(dict(self.events(out))[65]['experience'], 1_200_000_000)
        self.assertEqual(f.lookup(role, 'attachments', identity)['count'], 3)
        request = decode(self.packet)[2]
        self.assertEqual(request['roll_count'], 1)
        self.assertEqual(request['roll_list'], [dict(type_id=1041, count=1_000_000)])
        # A million units remain one stack and one wire request, never a million
        # response objects. Use a generous latency ceiling to catch severe stalls.
        self.assertLess(elapsed, 5.0)
        self.assertLess(len(self.replies), 64)
        self.assertLess(sum(map(len, self.replies)), 64 * 1024)
        snapshots = [item for mid, _, data in out if mid == 1035 for item in data['attach_list']]
        self.assertEqual(next(item['count'] for item in snapshots if item['id'] == identity), 3)
        self.assertEqual(self.backend.respond(self.packet, self.state), self.replies)
        self.assertEqual(self.backend.profile(), role)
        self.performance_metrics = dict(scroll_count=1_000_000, elapsed_seconds=elapsed,
                                        response_packets=len(self.replies),
                                        response_bytes=sum(map(len, self.replies)))

    def test_large_scroll_inventory_is_fully_chunked_before_result(self):
        role = self.configure(level=99)
        # Exercise more than four native byte-count packets, with huge stack
        # counts and every original scroll tier; no live account is modified.
        for index in range(600):
            role['attachments'].append(dict(id=f.new_id(role), attach_type=5,
                type_id=1041 + index % 40, count=1_000_000, level=1,
                equip_order=0, equip_pos=0))
        self.backend.save(role)
        started = time.perf_counter()
        out = self.consume([(1041, 1)])
        elapsed = time.perf_counter() - started
        after = self.backend.profile()
        chunks = [(index, data) for index, (mid, _, data) in enumerate(out) if mid == 1035]
        self.assertEqual([data['first_send'] for _, data in chunks], [True, False, False, False, False])
        self.assertTrue(all(0 < data['attach_count'] <= 128 for _, data in chunks))
        snapshot = [item for _, data in chunks for item in data['attach_list']]
        self.assertEqual(len(snapshot), len(after['attachments']))
        self.assertEqual({item['id']: item['count'] for item in snapshot},
                         {item['id']: item['count'] for item in after['attachments']})
        result_index = next(index for index, (mid, _, data) in enumerate(out)
                            if mid == 2998 and data['id'] == 65)
        self.assertLess(chunks[-1][0], result_index)
        self.assertEqual(self.total_exp(after['corteges'][0]), 1200)
        self.assertEqual(sum(item['count'] for item in snapshot if item['type_id'] == 1041), 14_999_999)
        self.assertTrue(all(len(packet) <= MAX_PACKET for packet in self.replies))
        self.assertLess(sum(map(len, self.replies)), 256 * 1024)
        self.assertLess(elapsed, 5.0)
        self.performance_metrics = dict(inventory_stacks=600, inventory_scrolls=600_000_000,
                                        elapsed_seconds=elapsed, inventory_packets=len(chunks),
                                        response_bytes=sum(map(len, self.replies)))

    def test_large_experience_result_keeps_double_precision_on_wire(self):
        self.configure(level=99)
        self.add_item(1080, 20)
        out = self.consume([(1080, 20)])
        expected = 3_120_000_000
        self.assertEqual(dict(self.events(out))[65]['experience'], expected)
        actual = self.backend.profile()['corteges'][0]
        snapshot = next(c for mid, _, data in out if mid == 1034
                        for c in data['cortege_list'] if c['id'] == self.ids[0])
        self.assertEqual(self.total_exp(actual), expected)
        self.assertEqual((snapshot['level'], snapshot['cur_exp']),
                         (actual['level'], actual['cur_exp']))


if __name__ == '__main__': unittest.main()
