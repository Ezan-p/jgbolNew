"""Independent upgrade rolls, legacy saves and unrelated progress protection."""
import copy
import json
import unittest
from decimal import Decimal
from unittest.mock import patch

from network_redirect import equipment as e, formation as f
from tests import test_skills as helpers


class UpgradeProbabilityTests(unittest.TestCase):
    setUp = helpers.SkillTests.setUp

    def test_spell_boundary_repeated_failure_and_legacy_bonus_ignored(self):
        role = self.backend.profile()
        target = role['attachments'][0]
        cost = Decimal(f.SKILL_COST[1]['quality%d_cost' % int(f.SKILLS[target['type_id']]['quality'])])
        worth = Decimal(f.SKILL_WORTH[1]['quality_worth%d' % int(f.SKILLS[212]['quality'])])
        rate = f.floor(worth * 100 / cost)
        self.assertTrue(0 < rate < 100)
        for roll, success in [(rate, False), (rate, False), (rate - 1, True)]:
            mat = dict(id=f.new_id(role), attach_type=6, type_id=212, level=1, count=0)
            role['attachments'].append(mat)
            # Bypass migration to prove settlement itself ignores old pity.
            target['count'] = 99
            req = dict(data=dict(des_skill_id=target['id'], src_skill_list=[mat['id']]))
            with patch.object(f.secrets, 'randbelow', return_value=roll) as rng:
                f.enhance_skill(role, req, self.backend.formation_rules, lambda x: x)
            rng.assert_called_once_with(100)
            self.assertEqual(target['count'], 0)
            self.assertEqual(target['level'], 1 + success)
            self.assertNotIn(mat, role['attachments'])

    def test_stone_boundary_repeated_failure_and_legacy_bonus_ignored(self):
        for tid in e.STONES:
            role = self.backend.profile()
            role.update(level=99, silver_coin=1000000)
            target = dict(id=f.new_id(role), attach_type=5, type_id=tid, level=1, count=1)
            role['attachments'].append(target)
            for roll, success in [(400000, False), (400000, False), (399999, True)]:
                mat = dict(id=f.new_id(role), attach_type=5, type_id=1090, level=1, count=1)
                role['attachments'].append(mat)
                target['prob_compen'] = 99
                silver = role['silver_coin']
                req = dict(flag=3, des_id=target['id'], stone_pos=0, equip_order=0,
                           src_count=1, src_list=[dict(id=mat['id'])])
                with patch.object(e.secrets, 'randbelow', return_value=roll) as rng:
                    result = e.settle(role, req)
                rng.assert_called_once_with(1000000)
                self.assertEqual(result[0][1]['result'], 1 if success else 6)
                self.assertEqual((target['level'], target['prob_compen']), (1 + success, 0))
                self.assertEqual(silver - role['silver_coin'], 10000)
                self.assertNotIn(mat, role['attachments'])

    def test_legacy_migration_persists_and_preserves_other_progress(self):
        role = self.backend.profile()
        role['attachments'][0]['count'] = 25
        for tid in e.STONES:
            role['attachments'].append(dict(id=f.new_id(role), attach_type=5, type_id=tid,
                                            level=3, count=4, prob_compen=35, is_lock=1))
        role['attachments'].append(dict(id=f.new_id(role), attach_type=5, type_id=1001,
                                        level=1, count=10, prob_compen=27))
        expected = copy.deepcopy(role)
        for item in expected['attachments']:
            if item['attach_type'] == 6:
                item['count'] = 0
            elif item['type_id'] in e.STONES:
                item['prob_compen'] = 0
        # Seed the pre-change wire state directly, as an old database would contain it.
        self.backend.db.execute('UPDATE roles SET data=? WHERE account=?',
                                (json.dumps(role), self.backend.account))
        self.backend.db.commit()
        current = self.backend.profile()
        self.assertEqual(current['attachments'], expected['attachments'])
        self.assertEqual(current['silver_coin'], expected['silver_coin'])
        self.assertFalse(f.prepare(current, self.backend.formation_rules))
        with helpers.BackendContext(self.directory.name) as reopened:
            self.assertEqual(reopened.profile()['attachments'], expected['attachments'])


if __name__ == '__main__':
    unittest.main()
