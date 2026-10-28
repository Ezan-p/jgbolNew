import copy
import json
import unittest
from datetime import datetime, timezone
from network_redirect import monument_wealth as wealth

MONDAY = int(datetime(2026, 10, 25, 16, tzinfo=timezone.utc).timestamp())


class WealthTests(unittest.TestCase):
    def role(self):
        return dict(role_id=1, role_name='玩家', vip_level=2, corteges=[])

    def test_boundary_snapshot_and_current_week_actions(self):
        role=self.role();s=wealth.prepare(role,MONDAY-86400)
        initial=copy.deepcopy(s['published'])
        wealth.record(role,MONDAY-1,donation_money=109,normal_gift=2,advanced_gift=3)
        self.assertEqual(wealth.ranking(role,MONDAY-1)['fortune_info'],initial)
        wealth.record(role,MONDAY,donation_money=20)
        board=wealth.ranking(role,MONDAY)
        row=next(v for v in board['fortune_info'] if v['id']==1)
        self.assertEqual(row['fortune'],2180)
        self.assertEqual(row['contribute'],109)
        self.assertEqual(s['current']['donation_money'],20)
        self.assertEqual(s['current']['normal_gift'],0)
        self.assertEqual(s['settled_at'],MONDAY)
        self.assertEqual(board['next_settlement'],MONDAY+7*86400)
        self.assertEqual(wealth.ranking(role,MONDAY+86400)['fortune_info'],board['fortune_info'])

    def test_npcs_never_recompute_and_restart_is_idempotent(self):
        role=self.role();s=wealth.prepare(role,MONDAY-1)
        fixed=copy.deepcopy(s['npcs'])
        role['guild']={'unions':{'1':{'feast':{'stats':{'npc':{'fortune':999999}}}}}}
        wealth.prepare(role,MONDAY)
        saved=json.loads(json.dumps(role))
        self.assertEqual(wealth.ranking(role,MONDAY),wealth.ranking(saved,MONDAY))
        self.assertEqual(saved['monument_wealth']['npcs'],fixed)
        wealth.prepare(saved,MONDAY+8*86400)
        self.assertEqual(saved['monument_wealth']['npcs'],fixed)

    def test_long_absence_preserves_played_week_and_no_clock_rollback(self):
        role=self.role();s=wealth.prepare(role,MONDAY-1)
        week=s['week'];wealth.record(role,MONDAY-1,advanced_gift=5)
        wealth.prepare(role,MONDAY+365*86400)
        self.assertEqual(s['settled_week'],week)
        self.assertEqual(next(v for v in s['published'] if v['id']==1)['fortune'],2250)
        before=copy.deepcopy(s)
        wealth.prepare(role,MONDAY)
        self.assertEqual(s,before)

    def test_vip_upgrade_on_boundary_does_not_change_previous_week(self):
        role=self.role();wealth.prepare(role,MONDAY-1)
        role['vip_level']=10
        s=wealth.prepare(role,MONDAY)
        self.assertEqual(next(v for v in s['published'] if v['id']==1)['fortune'],2000)
        self.assertEqual(s['current']['vip_level'],10)
        self.assertEqual(wealth.ranking(role,MONDAY)['current_score'],10000)

    def test_migration_only_imports_known_player_spending_once(self):
        from network_redirect import daily
        role=self.role();week=daily.week(MONDAY-1,wealth.rules())
        role['guild']=dict(day=daily.day(MONDAY-1,wealth.rules()),donations=3,unions={
            '1':dict(feast=dict(week=week,stats={'1':dict(id=1,normal_gift=2,advanced_gift=1),
                                              '2':dict(id=2,normal_gift=100,advanced_gift=100)})),
            '2':dict(feast=dict(week=week,stats={'1':dict(id=1,normal_gift=1,advanced_gift=0)})),
            '3':dict(feast=dict(week=week-1,stats={'1':dict(id=1,normal_gift=99,advanced_gift=99)}))})
        s=wealth.prepare(role,MONDAY-1)
        self.assertEqual((s['current']['donation_money'],s['current']['normal_gift'],s['current']['advanced_gift']),(30,3,1))
        before=copy.deepcopy(s);wealth.prepare(role,MONDAY-1);self.assertEqual(s,before)

    def test_tie_uses_vip_then_donation_gifts_then_id(self):
        rows=[dict(id=ident,vip_level=vip,donation_money=money,advanced_gift=0,normal_gift=0,fortune=100)
              for ident,vip,money in [(1,0,100),(2,1,0),(4,1,20),(3,1,20)]]
        self.assertEqual([v['id'] for v in wealth.ordered(rows)],[3,4,2,1])


if __name__=='__main__':unittest.main()
