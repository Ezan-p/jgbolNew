import copy
import random
from unittest.mock import patch
from tests.test_activity import ActivityCase
from network_redirect import activity_land_rewards as rewards, activity_land as land, summon


class LandCardCapTests(ActivityCase):
    def land(self,op,**data):return self.req(1302,id=op,data=summon.lua(data))

    def test_caps_and_shuffle_across_seeded_boards(self):
        for count,limit in ((5,2),(3,1)):
            positions=set()
            for seed in range(200):
                with patch.object(rewards.secrets,'SystemRandom',return_value=random.Random(seed)):
                    cards=rewards.draw_cards(self.b.activity_rules,count,stone_limit=limit)
                self.assertEqual(len(cards),count)
                self.assertLessEqual(sum(p[1]==10000 for p in cards),limit)
                positions.update(i for i,p in enumerate(cards) if p[1]==10000)
                self.assertTrue(all(p in self.b.activity_rules['land_card_rewards'] for p in cards))
            self.assertEqual(positions,set(range(count)))

    def test_actual_first_win_boards_cap_both_stone_quantities(self):
        self.ok(self.land(1))
        for hell in (False,True):
            for roll,quantity in ((0,10),(20,20)):
                role=self.b.profile();s=role['activity']['land']
                s.update(soul_count=10000,unlocked=[1],boss=None,hell=None)
                self.b.save(role)
                with patch.object(rewards.secrets,'SystemRandom') as factory:
                    rng=factory.return_value
                    rng.randrange.side_effect=lambda total:roll if total==100 else 0
                    rng.choice.side_effect=lambda pool:pool[0]
                    out=self.land(4,flag=1,des_type=4 if hell else 3,des_id=1,cur_num=1)
                self.ok(out);self.assertTrue(out[-1][1]['is_win'])
                key='hell' if hell else 'boss';pending=self.b.profile()['activity']['land'][key]
                self.assertEqual(sum(p==[5,10000,quantity,1] for p in pending['rewards']),1 if hell else 2)
                self.ok(self.land(24 if hell else 12))
                self.assertEqual(self.b.profile()['activity']['land'][key],pending)

    def test_legacy_missing_cards_use_remaining_allowance_without_changing_saved_cards(self):
        self.ok(self.land(1))
        for key,count,limit,query in (('boss',5,2,12),('hell',3,1,24)):
            for used in (0,1,limit,limit+1):
                role=self.b.profile();old=[[5,10000,10,1]]*used
                role['activity']['land'][key]=dict(layer=1,cards=[],rewards=copy.deepcopy(old))
                self.b.save(role)
                with patch.object(rewards.secrets,'SystemRandom') as factory:
                    factory.return_value.randrange.return_value=0
                    factory.return_value.choice.side_effect=lambda pool:pool[0]
                    self.ok(self.land(query))
                board=self.b.profile()['activity']['land'][key]['rewards']
                self.assertEqual(board[:used],old)
                self.assertEqual(len(board),count)
                self.assertEqual(sum(p[1]==10000 for p in board),max(limit,used))
                self.ok(self.land(query));self.assertEqual(self.b.profile()['activity']['land'][key]['rewards'],board)
