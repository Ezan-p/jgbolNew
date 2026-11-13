"""Shared bonuses must not leak into Bagua; native previews use personal panels."""
import copy
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from network_redirect import cheer, combat_power as cp, immortal, summon
from network_redirect.backend import Backend
from network_redirect.protocol import decode


class CheerAttributeTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.backend = Backend(Path(tmp.name), 18770, lambda *a, **k: None)
        self.addCleanup(self.backend.close)
        self.rules = self.backend.formation_rules
        self.role = self.backend.profile()
        self.role['attachments'] = []
        self.support = self.add(5013, cheer_order=1, evolve_level=2)
        self.role.update(cheer_heaven_level=7, cheer_heaven_effect=1)
        self.role['cheer_targets']['heaven'] = self.role['corteges'][0]['id']
        cheer.prepare(self.role)

    def add(self, kind, **fields):
        c = summon.companion(self.role, kind)
        c.update(fields)
        self.role['corteges'].append(c)
        return c

    def calculate(self):
        cp.recalculate(self.role, self.rules, now=100)

    def panel(self, c):
        return {s: c[s] for s in cp.STATS}

    def gain(self):
        target = self.role['corteges'][0]
        trace = self.role['combat_power_breakdown']['companions'][str(target['id'])]
        return {s: Decimal(trace['cheer'][s]) - Decimal(trace['pet'][s]) for s in cp.STATS}

    def test_shared_sources_only_affect_main_and_substitute(self):
        reverse = self.add(5002, cheer_order=9)
        bag = self.add(5003)
        substitute = self.add(5004, order=8)
        self.calculate()
        baseline = {c['id']: self.panel(c) for c in self.role['corteges']}
        before_gain = self.gain()
        self.role.update(max_hp_plus=12775, gongji_plus=630, fangyu_plus=1300,
                         max_magic_plus=2060, hole_hp_plus=10000,
                         title_id=1, title_begintime=0)
        self.role['immortal_collection'] = {
            str(k): list(range(1, len(immortal.collection_members(row)) + 1))
            for k, row in immortal.COLLECTIONS.items()}
        self.role['combat_sources'] = {'cortege': dict.fromkeys(cp.STATS, 17)}
        self.calculate()
        self.assertTrue(any(self.role['collection_bonuses'].values()))
        for c in (self.support, reverse, bag):
            self.assertEqual(self.panel(c), baseline[c['id']])
        self.assertEqual(self.gain(), before_gain)
        for c in (self.role['corteges'][0], substitute):
            for stat, fixed in zip(cp.STATS, (12775, 630, 1300, 2060)):
                expected = fixed + self.role['collection_bonuses'][stat] + 50 + 17
                if stat == 'hp':
                    expected += 10000
                self.assertEqual(c[stat] - baseline[c['id']][stat], expected)

    def test_screenshot_level_one_two_evolutions_and_personal_culture(self):
        self.role.update(max_hp_plus=12775, gongji_plus=630, fangyu_plus=1300,
                         max_magic_plus=2060)
        self.calculate()
        self.assertEqual(self.panel(self.support), dict(hp=668, gongji=362, fangyu=137, magic=276))
        self.assertEqual(self.gain(), dict(hp=Decimal('96.86'), gongji=Decimal('34.028'),
                                          fangyu=Decimal('12.878'), magic=Decimal('25.944')))
        self.support.update(hp_plus=100, gongji_plus=20, fangyu_plus=30, magic_plus=40)
        self.calculate()
        self.assertEqual(self.panel(self.support), dict(hp=768, gongji=382, fangyu=167, magic=316))

    def test_all_sixteen_slots_use_displayed_personal_panel(self):
        # Fractional growth, personal flat/rate sources and protocol limits all
        # used to diverge from the support base, even without shared bonuses.
        self.support.update(level=2, combat_sources={'fam': {'gongji': 13},
                            'cortege': {'hp': 11, 'magic': 10**30, 'fangyu': -1000}})
        self.role['combat_sources'] = {'fam': dict.fromkeys(cp.STATS, 200),
                                       'cortege': dict.fromkeys(cp.STATS, 10000)}
        for order, name in enumerate(cheer.NAMES, 1):
            with self.subTest(order=order):
                for direction in cheer.NAMES:
                    self.role['cheer_targets'][direction] = 0
                self.support['cheer_order'] = order
                self.role['cheer_' + name + '_level'] = 7
                self.role['cheer_targets'][name] = self.role['corteges'][0]['id']
                cheer.prepare(self.role)
                self.calculate()
                self.assertEqual(self.support['gongji'], 429)
                self.assertEqual(self.support['hp'], 713)
                self.assertEqual(self.support['magic'], cp.LIMIT)
                self.assertEqual(self.support['fangyu'], 0)
                expected = {s: Decimal(self.support[s]) * self.role[name + '_' + s + '_plus'] / 1000
                            for s in cp.STATS}
                self.assertEqual(self.gain(), expected)
                before = copy.deepcopy(self.role)
                self.calculate()
                self.assertEqual(self.role, before)
                self.role['corteges'].reverse()
                self.calculate()
                self.assertEqual(self.role['combat_power_breakdown'], before['combat_power_breakdown'])
                self.role['corteges'].reverse()

    def test_moving_between_bag_support_and_formation_reapplies_scope(self):
        self.role.update(max_hp_plus=1000, hole_hp_plus=2000, title_id=1, title_begintime=0)
        for order, slot, hp in ((0, 0, 668), (0, 1, 668), (0, 9, 668), (8, 0, 3718), (0, 1, 668)):
            with self.subTest(order=order, cheer_order=slot):
                self.support.update(order=order, cheer_order=slot)
                self.calculate()
                self.assertEqual(self.support['hp'], hp)

    def test_old_cached_panel_is_rebuilt_on_load_and_sent_on_reconnect(self):
        self.role.update(level=99, max_hp_plus=12775, gongji_plus=630,
                         fangyu_plus=1300, max_magic_plus=2060, max_combat_power=9999999)
        self.support.update(hp=13443, gongji=992, fangyu=1437, magic=2336)
        # Write an old-version snapshot directly, bypassing the new save-time
        # calculation, then exercise the real migration and protocol path.
        self.backend.db.execute('UPDATE roles SET data=? WHERE account=?',
                                (json.dumps(self.role), self.backend.account))
        self.backend.db.commit()
        restored = self.backend.profile()
        support = next(c for c in restored['corteges'] if c['id'] == self.support['id'])
        expected = dict(hp=668, gongji=362, fangyu=137, magic=276)
        self.assertEqual(self.panel(support), expected)
        self.assertEqual(restored['max_combat_power'], 9999999)
        for field in ('max_hp_plus', 'gongji_plus', 'fangyu_plus', 'max_magic_plus'):
            self.assertEqual(restored[field], self.role[field])
        wire = [decode(p) for p in self.backend.bootstrap(reconnect=True)]
        sent = next(c for mid, _, d in wire if mid == 1034
                    for c in d['cortege_list'] if c['id'] == support['id'])
        self.assertEqual(self.panel(sent), expected)
        self.assertEqual((sent['level'], sent['evolve_level']), (1, 2))


if __name__ == '__main__':
    unittest.main()
