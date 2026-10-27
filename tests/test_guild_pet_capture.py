"""Capture inventory must not depend on unrelated seasonal reward settings."""
import copy
import unittest
from unittest.mock import patch

from network_redirect import activity_home, formation, pets, summon
from tests.test_guild_activity_fixes import GuildActivityFixTests


class GuildPetCaptureTests(unittest.TestCase):
    setUp = GuildActivityFixTests.setUp
    req = GuildActivityFixTests.req

    def encounter(self):
        self.req(84, task_index=1, task_type=1, pay_type=1)
        data = self.req(86, two_type=2)[0]
        role = self.b.profile()
        summon.add_item(role, 1341, 1)
        self.b.save(role)
        return data

    def test_first_capture_is_independent_of_seasonal_reward_loader(self):
        encounter = self.encounter()
        role = self.b.profile()
        self.assertNotIn('home', role.get('activity', {}))
        with patch('network_redirect.activity.load_rules',
                   side_effect=formation.Rejected('字牌奖励缺失')) as unrelated:
            result = self.req(87, two_type=2, catch_type=1341)[0]
        unrelated.assert_not_called()
        self.assertEqual(result['flag'], 1)
        pet = result['animal_list'][1]
        self.assertEqual(pet['type_id'], encounter['boss_info']['type_id'])
        role = self.b.profile()
        stored = role['activity']['home']['pets']
        self.assertEqual(len(stored), 1)
        self.assertEqual((stored[0]['id'], stored[0]['quality']), (pet['id'], pet['quality']))
        self.assertFalse(any(i['type_id'] == 1094 for i in role['attachments']))
        self.assertFalse(any(i['type_id'] == 1341 for i in role['attachments']))
        # The first home visit can initialize its calendar without discarding
        # the pet acquired before the player ever opened the home page.
        home = activity_home.state(role, self.now, self.b.activity_rules)
        self.assertEqual(home['pets'], stored)
        self.assertEqual(len(home['pets']), 1)
        before = self.b.profile()
        self.req(87, ok=False, two_type=2, catch_type=1341)
        self.assertEqual(self.b.profile(), before)

    def test_existing_home_progress_is_untouched_by_capture(self):
        self.encounter()
        role = self.b.profile()
        home = activity_home.state(role, self.now, self.b.activity_rules)
        # A deliberately old calendar ensures capture does not settle home
        # purchases, training limits, or a weekly competition as a side effect.
        home.update(day=home['day']-1, purchases={'1': 2}, train_count={'1': 3},
                    fight_count=1, pray_time=self.now-60)
        home['welfare']['week'] -= 1
        existing = pets.add(home, 102, 1)
        self.b.save(role)
        before = copy.deepcopy(home)
        self.req(87, two_type=2, catch_type=1341)
        after = self.b.profile()['activity']['home']
        self.assertEqual(after['pets'][0], existing)
        self.assertEqual(len(after['pets']), len(before['pets'])+1)
        self.assertEqual({k: v for k, v in after.items() if k not in ('pets', 'next_pet_id')},
                         {k: v for k, v in before.items() if k not in ('pets', 'next_pet_id')})

    def test_full_pet_inventory_rejects_capture_atomically(self):
        self.encounter()
        role = self.b.profile()
        home = activity_home.storage(role)
        original = pets.add(home, 102, 1)
        home['pets'] = [dict(copy.deepcopy(original), id=i+1)
                        for i in range(pets.load_rules()['capacity'])]
        home['next_pet_id'] = len(home['pets'])+1
        self.b.save(role)
        before = self.b.profile()
        self.req(87, ok=False, two_type=2, catch_type=1341)
        self.assertEqual(self.b.profile(), before)


del GuildActivityFixTests
