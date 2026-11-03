"""Original 1353 wire contract, recovery, local weeks, and exploitable boundaries."""
import copy
import random
import unittest
from collections import Counter, deque
from pathlib import Path
from unittest.mock import patch
from tests.test_activity import ActivityCase, NOW
from network_redirect import activity, activity_babel as babel, activity_babel_npc as npc, npc_players, summon
from network_redirect.backend import Backend, login_fields
from network_redirect.protocol import decode


def route_to(grid, start, target):
    """Walk only cleared cells, then interact with the requested destination."""
    pending = deque([(start, [])])
    seen = {start}
    while pending:
        (row, col), route = pending.popleft()
        if (row, col) == target:
            return route
        for pos in ((row-1, col), (row+1, col), (row, col-1), (row, col+1)):
            r, c = pos
            if (1 <= r <= 5 and 1 <= c <= 8 and pos not in seen
                    and (pos == target or grid[r-1][c-1]['elem_type'] == 0)):
                seen.add(pos)
                pending.append((pos, route + [pos]))
    raise AssertionError(f'Unreachable target: {target}')


class BabelMapTests(unittest.TestCase):
    def test_random_maps_are_distinct_and_resource_solvable(self):
        expected = Counter([0] * 25 + [3, 9, 20003, 20004, 20005, 20006,
                           20007, 20008, 20009, 20010, 20011, 20012, 20013, 20014, 20015])
        first_floors = set()
        for seed in range(100):
            state = dict(floors={})
            signatures = set()
            with patch.object(babel.secrets, 'SystemRandom', return_value=random.Random(seed)):
                for floor in range(1, 11):
                    state['cur_floor'] = floor
                    babel.generate(state)
                    grid = state['floors'][str(floor)]
                    signature = tuple(c['elem_type'] for row in grid for c in row)
                    self.assertEqual(Counter(signature), expected)
                    self.assertNotIn(signature, signatures)
                    signatures.add(signature)
                    if floor == 1:
                        first_floors.add(signature)
                    self.assertEqual(grid[0][0]['elem_type'], 0)
                    self.assertEqual(sum(c['visible'] for row in grid for c in row), 4)
                    # Treat all locks as impassable, and assume guard victories.
                    # Every free cell and every lock's approach must be reachable.
                    walkable = copy.deepcopy(grid)
                    for row in walkable:
                        for cell in row:
                            if cell['elem_type'] not in (*babel.TOOLS, 3):
                                cell['elem_type'] = 0
                    for row in range(1, 6):
                        for col in range(1, 9):
                            route_to(walkable, (1, 1), (row, col))
        self.assertEqual(len(first_floors), 100)

    def test_secret_floors_keep_existing_layout(self):
        for floor in (1001, 1015):
            state = dict(cur_floor=floor, floors={})
            babel.generate(state)
            grid = state['floors'][str(floor)]
            self.assertEqual(grid[0][1]['elem_type'], 20005)
            self.assertEqual(grid[3][6]['elem_type'], 9)
            self.assertEqual(grid[4][7]['elem_type'], 3)

    def test_late_maps_unique_solvable_and_boss_only_route_bounded(self):
        expected = Counter([0] * 25 + [3, 9, 20003, 20004, 20005, 20006,
                           20007, 20008, 20009, 20010, 20011, 20012, 20013, 20014, 20015])
        for seed in range(100):
            signatures = set()
            with patch.object(babel.secrets, 'SystemRandom', return_value=random.Random(seed)):
                for floor in range(11, 71):
                    # No prior maps: uniqueness must not depend on intact loot
                    # or generation order, including teleport/legacy saves.
                    state = dict(cur_floor=floor, floors={})
                    babel.generate(state)
                    grid = state['floors'][str(floor)]
                    signature = tuple(c['elem_type'] for row in grid for c in row)
                    self.assertEqual(Counter(signature), expected)
                    self.assertNotIn(signature, signatures)
                    signatures.add(signature)
                    self.assertEqual([grid[r][c]['elem_type'] for r,c in ((0,0),(0,1),(1,0))], [0]*3)
                    self.assertEqual(sum(c['visible'] for row in grid for c in row), 4)
                    boss = next((r,c) for r,line in enumerate(grid,1) for c,cell in enumerate(line,1)
                                if cell['elem_type'] == 9)
                    stairs = next((r,c) for r,line in enumerate(grid,1) for c,cell in enumerate(line,1)
                                  if cell['elem_type'] == 3)
                    path = route_to(grid, (1,1), boss) + route_to(grid, boss, stairs)
                    minimum = 7 + (floor-11)//20
                    self.assertTrue(minimum <= len(path) <= minimum+2, (seed, floor, path))
                    self.assertEqual(abs(boss[0]-stairs[0])+abs(boss[1]-stairs[1]), 1)
                    # Assuming victories, all keys/tools are accessible without
                    # spending any consumables; every lock can be approached.
                    walkable = copy.deepcopy(grid)
                    for row in walkable:
                        for cell in row:
                            if cell['elem_type'] not in (*babel.TOOLS, 3):
                                cell['elem_type'] = 0
                    for row in range(1,6):
                        for col in range(1,9):
                            route_to(walkable, (1,1), (row,col))

    def test_same_random_stream_still_produces_sixty_distinct_late_maps(self):
        signatures = set()
        for floor in reversed(range(11,71)):
            with patch.object(babel.secrets, 'SystemRandom', return_value=random.Random(0)):
                state = dict(cur_floor=floor, floors={})
                babel.generate(state)
            signature = tuple(c['elem_type'] for row in state['floors'][str(floor)] for c in row)
            self.assertNotIn(signature, signatures)
            signatures.add(signature)


class BabelTests(ActivityCase):
    SHOP_POOL = {
        1001: (10, 100, 10), 1022: (1, 100, 3), 1023: (1, 100, 3),
        20016: (1, 50, 3), 20017: (1, 100, 3), 20018: (1, 250, 2),
        20019: (1, 500, 1), 20005: (1, 50, 3), 20006: (1, 50, 5),
        20010: (1, 200, 3), 20011: (1, 150, 3), 20012: (1, 100, 3),
        1034: (1, 50, 5), 1033: (1, 100, 5), 1032: (1, 300, 3),
        10000: (2, 100, 3), 10001: (5, 100, 5),
    }

    def call(self, op=1, **data):
        out = self.req(1353, id=op, data=summon.lua(data)); self.ok(out)
        return [v['data'] for e,v in out if e == 203]

    def edit(self, **changes):
        role = self.b.profile(); role['activity']['babel'].update(changes); self.b.save(role)

    def saved(self):
        return self.b.profile()['activity']['babel']

    def reject(self, op, **data):
        before = self.b.profile()
        self.assertEqual(self.req(1353,id=op,data=summon.lua(data))[0][0],55)
        self.assertEqual(before,self.b.profile())

    def visit_element(self, typ):
        state = self.saved()
        grid = state['floors'][str(state['cur_floor'])]
        target = next((r, c) for r, row in enumerate(grid, 1)
                      for c, cell in enumerate(row, 1) if cell['elem_type'] == typ)
        start = (state['locale']['row'], state['locale']['column'])
        # Other guards/tools can be crossed safely after their own interaction.
        # Pickups and guards are handled first by the full-floor walk below.
        pending = deque([(start, [])]); seen = {start}
        while pending:
            (row, col), path = pending.popleft()
            if (row, col) == target:
                for r, c in path:
                    self.call(2, target_pos=dict(row=r, column=c))
                return
            for pos in ((row-1, col), (row+1, col), (row, col-1), (row, col+1)):
                r, c = pos
                if (1 <= r <= 5 and 1 <= c <= 8 and pos not in seen
                        and (pos == target or grid[r-1][c-1]['elem_type'] not in (*babel.TOOLS, 3))):
                    seen.add(pos); pending.append((pos, path + [pos]))
        self.fail(f'Unreachable element {typ}')

    def test_random_first_ten_floors_full_wire_playthrough(self):
        self.call(); self.edit(energy=10000)
        with patch('network_redirect.activity_babel.journey.battle', return_value=(3, [], [])):
            for floor in range(1, 11):
                for typ in (20005, 20006, 20010, 20011, 20012, 20013, 20014, 20015,
                            20003, 20004, 20007, 20008, 20009, 9, 3):
                    grid = self.saved()['floors'][str(floor)]
                    if any(c['elem_type'] == typ for row in grid for c in row):
                        self.visit_element(typ)
                self.assertEqual(self.saved()['cur_floor'], floor + 1)
                self.assertEqual(self.saved()['coin_count'], 500 * floor)
        for typ in (20005, 20006, 20010, 20011, 20012):
            self.assertEqual(babel.item_count(self.b.profile(), typ), 0)

    def test_random_map_persists_and_only_regenerates_next_week(self):
        self.call()
        with patch('network_redirect.activity_babel.journey.battle', return_value=(3, [], [])):
            self.visit_element(20005)
        floors = self.saved()['floors']
        self.call(); self.call(6); self.call(7, floor=1)
        self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.call()
        self.assertEqual(self.saved()['floors'], floors)
        monday = npc.start(self.saved()['week'] + 1, self.b.activity_rules)
        with patch('network_redirect.backend.time.time', return_value=monday), \
                patch.object(babel, 'random_floor', wraps=babel.random_floor) as generate:
            self.call(); self.call()
            self.assertEqual(generate.call_count, 1)
        self.assertTrue(any(c['elem_type'] == 20005 for row in self.saved()['floors']['1'] for c in row))

    def test_late_floors_full_wire_loot_budget_and_terminal_once(self):
        self.call(); self.edit(cur_floor=11, history_floor=11, energy=10000)
        self.call()
        with patch('network_redirect.activity_babel.journey.battle', return_value=(3, [], [])):
            for floor in range(11,71):
                self.edit(life=100)
                for typ in (20005,20006,20010,20011,20012,20013,20014,20015,
                            20003,20004,20007,20008,20009,9,3):
                    grid = self.saved()['floors'][str(floor)]
                    if any(c['elem_type'] == typ for row in grid for c in row):
                        if typ == 3 and floor == 70:
                            terminal = next((r,c) for r,line in enumerate(grid,1)
                                            for c,cell in enumerate(line,1) if cell['elem_type'] == 3)
                        self.visit_element(typ)
                self.assertEqual(self.saved()['cur_floor'], min(floor+1,70))
                self.assertEqual(self.saved()['coin_count'], 500*(floor-10) + (50 if floor == 70 else 0))
                for typ in (20005,20006,20010,20011,20012):
                    self.assertEqual(babel.item_count(self.b.profile(),typ), 0)
        self.assertTrue(self.saved()['complete'])
        before = self.b.profile()['attachments']
        row,col = terminal
        neighbor = (row-1,col) if row > 1 else (row+1,col)
        self.call(2,target_pos=dict(zip(('row','column'),neighbor)))
        self.call(2,target_pos=dict(row=row,column=col))
        self.assertEqual(self.b.profile()['attachments'], before)

    def test_late_map_saved_loot_survives_queries_teleport_restart_and_old_layout(self):
        for legacy in (False, True):
            with self.subTest(legacy=legacy):
                if legacy:
                    self.legacy_babel_floor(40)
                else:
                    self.call(); self.edit(cur_floor=40, history_floor=40, energy=10000)
                self.call()
                with patch('network_redirect.activity_babel.journey.battle', return_value=(3, [], [])):
                    self.visit_element(20005)
                self.call(7, floor=40)
                floors = self.saved()['floors']
                self.call(); self.call(6); self.call(7,floor=40)
                self.b.close(); self.b = Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
                self.call()
                self.assertEqual(self.saved()['floors'], floors)
                self.assertFalse(any(c['elem_type'] == 20005 for row in floors['40'] for c in row))

    def test_floor_reward_entry_probabilities_and_coin_budget(self):
        self.call()
        for floor, count in ((11,9),(16,7),(21,9),(26,10),(31,8),(36,8),
                             (41,9),(46,10),(51,9),(56,8),(61,7),(66,7)):
            role = self.b.profile(); s = role['activity']['babel']; s['cur_floor'] = floor
            before = babel.item_count(role,20000)
            with patch.object(babel.secrets,'choice',side_effect=lambda entries: entries[0]) as draw:
                rewards = babel.floor_reward(role,s,self.b.activity_rules)
            entries = draw.call_args.args[0]
            self.assertEqual(len(entries), count)
            self.assertEqual(babel.item_count(role,20000)-before, 50)
            self.assertEqual(rewards[-1]['attach_count'], 50)
            if floor == 31:
                self.assertEqual(entries.count([5,10001,1,1]), 2)  # 2/8, not 1/7
            if floor == 11:
                self.assertEqual(sum(p[1] == 1092 for p in entries), 2)  # quantities 4/5 kept separate

    def test_original_essences_overflow_and_natural_cap(self):
        self.call(); role = self.b.profile()
        for tid in range(20016,20020): summon.add_item(role,tid,2)
        self.b.save(role)
        for tid,n in ((20016,10),(20017,25),(20018,80),(20019,200)):
            old=self.saved()['energy']; self.call(10,item_type=tid,count=1)
            self.assertEqual(self.saved()['energy'],old+n)
        with patch('network_redirect.backend.time.time',return_value=NOW+1800):
            self.call(); self.assertEqual(self.saved()['energy'],415)
        self.reject(10,item_type=20019,count=2)

    def test_half_hour_midnight_and_clock_backwards(self):
        self.call(); shop = self.call(8)[0]
        limits = shop['my_shop']
        index = next(i for i in range(1, 7) if limits[i]['limit'] >= 2)
        self.edit(energy=20,life=10,refresh_times=0,purchases={str(index):2})
        with patch('network_redirect.backend.time.time',return_value=NOW+1799):
            self.call(); self.assertEqual(self.saved()['energy'],20)
        with patch('network_redirect.backend.time.time',return_value=NOW+1800):
            self.call(); self.assertEqual(self.saved()['energy'],21)
            self.call(); self.assertEqual(self.saved()['energy'],21)
        with patch('network_redirect.backend.time.time',return_value=NOW+43200):
            self.call(); s=self.saved(); self.assertEqual((s['life'],s['energy'],s['refresh_times']),(100,44,1))
            self.assertEqual(s['purchases'], {})
        self.call(); self.assertEqual(self.saved()['energy'],44)
        with patch('network_redirect.backend.time.time',return_value=NOW+3*86400):
            self.call(); self.assertEqual(self.saved()['energy'],100)

    def test_zero_life_allows_exploration_not_combat(self):
        self.legacy_babel_floor()
        self.call(); self.edit(life=0)
        self.call(2,target_pos=dict(row=1,column=2))
        self.assertEqual(self.saved()['life'],0)
        self.reject(2,target_pos=dict(row=1,column=3))
        self.call(11); self.assertEqual(self.saved()['life'],100)
        self.reject(11)

    def test_shop_client_remaining_and_atomic_limits(self):
        self.call(); shop=self.call(8)[0]
        index = next(i for i in range(1, 7) if shop['my_shop'][i]['limit'] >= 3)
        cost = shop['my_shop'][index]['need_coin']
        role=self.b.profile(); summon.add_item(role,20000,cost * 10 + 200); self.b.save(role)
        self.call(4,index=index,count=3); shop=self.call(8)[0]
        self.assertEqual(shop['my_shop'][index]['limit']-shop['my_exchange'][index],
                         shop['my_shop'][index]['limit']-3)
        remaining = shop['my_shop'][index]['limit'] - 3
        if remaining:
            self.call(4,index=index,count=remaining)
        self.reject(4,index=index,count=1)
        self.call(9); shop=self.call(8)[0]
        self.assertEqual(list(shop['my_exchange'].values()), [0] * len(shop['my_shop']))
        self.reject(9)

    def shop_signature(self, data):
        return tuple((item['reward'][1]['attach_type'], item['reward'][1]['attach_count'],
                      item['need_coin'], item['limit']) for item in data['my_shop'].values())

    def test_paid_refresh_does_not_block_daily_reset_after_restart(self):
        self.call()
        role = self.b.profile(); summon.add_item(role, 20000, 2000); self.b.save(role)
        midnight = (activity.day(NOW, self.b.activity_rules) + 1) * 86400 - self.b.activity_rules['timezone_offset_hours'] * 3600
        with patch('network_redirect.backend.time.time', return_value=midnight - 1):
            first = self.call(8)[0]
            paid = self.call(9)[0]
            packet, replies = self.packet, self.replies
            self.assertEqual(paid['coin_count'], first['coin_count'] - 200)
            self.assertEqual(paid['refresh_times'], 0)
            self.assertNotEqual(self.shop_signature(first), self.shop_signature(paid))
            before = self.b.profile()
            self.assertEqual(self.b.respond(packet, self.state), replies)
            self.assertEqual(self.b.profile(), before)
            self.call(4, index=1, count=1)
            before = self.saved()
            self.reject(9)
            self.b.close(); self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
            self.call(8)
            self.assertEqual(self.saved(), before)

        with patch('network_redirect.backend.time.time', return_value=midnight):
            reset = self.call(8)[0]
            self.assertEqual(reset['refresh_times'], 1)
            self.assertEqual(reset['coin_count'], before['coin_count'])
            self.assertEqual(list(reset['my_exchange'].values()), [0] * 6)
            self.assertNotEqual(self.shop_signature(paid), self.shop_signature(reset))
            self.assertEqual(self.saved()['week'], before['week'])
            self.assertEqual(self.saved()['floors'], before['floors'])
            self.assertEqual(reset, self.call(8)[0])
            paid_again = self.call(9)[0]
            self.assertEqual(paid_again['refresh_times'], 0)
            self.assertEqual(paid_again['coin_count'], reset['coin_count'] - 200)
        # Clock rollback must not grant another automatic or paid refresh.
        self.assertEqual(paid_again, self.call(8)[0])
        self.reject(9)

    def test_legacy_shop_migrates_without_refilling_same_day(self):
        self.call()
        role = self.b.profile(); s = role['activity']['babel']
        s.pop('shop_day', None)
        s.update(refresh_times=0, purchases={'1': 1})
        self.b.save(role)
        before = self.call(8)[0]
        self.assertEqual(before['refresh_times'], 0)
        self.assertEqual(before['my_exchange'][1], 1)
        # Also cover a legacy save first loaded on a later day.
        role = self.b.profile(); role['activity']['babel'].pop('shop_day', None); self.b.save(role)
        with patch('network_redirect.backend.time.time', return_value=NOW + 86400):
            after = self.call(8)[0]
        self.assertEqual(after['refresh_times'], 1)
        self.assertEqual(list(after['my_exchange'].values()), [0] * 6)
        self.assertNotEqual(self.shop_signature(before), self.shop_signature(after))

    def test_shop_daily_reset_runs_once_when_login_skips_days_and_week(self):
        self.call(); self.edit(refresh_times=0, purchases={'1': 1})
        later = npc.start(self.saved()['week'] + 2, self.b.activity_rules)
        with patch.object(babel, 'random_shop_goods', wraps=babel.random_shop_goods) as draw:
            role = self.b.profile()
            activity.prepare(role, later, self.b.activity_rules)
            self.b.save(role)
            with patch('network_redirect.backend.time.time', return_value=later):
                reset = self.call(8)[0]
                self.assertEqual(reset, self.call(8)[0])
            self.assertEqual(draw.call_count, 1)
        self.assertEqual(reset['refresh_times'], 1)
        self.assertEqual(list(reset['my_exchange'].values()), [0] * 6)
        self.assertEqual(self.saved()['shop_day'], activity.day(later, self.b.activity_rules))

    def assert_shop_subset(self, data):
        self.assertEqual(len(data['my_shop']), 6)
        ids = []
        for item in data['my_shop'].values():
            reward = item['reward'][1]
            tid = reward['attach_type']; ids.append(tid)
            self.assertIn(tid, self.SHOP_POOL)
            quantity, price, limit = self.SHOP_POOL[tid]
            self.assertEqual((reward['attach_count'], item['need_coin'], item['limit']),
                             (quantity, price, limit))
        self.assertEqual(len(ids), len(set(ids)), '随机商品不能重复占槽')

    def test_shop_random_subset_is_stable_until_week_rollover(self):
        self.call(); first = self.call(8)[0]
        self.assert_shop_subset(first)
        self.assertEqual(first, self.call(8)[0])
        before = self.saved()
        role=self.b.profile(); summon.add_item(role,20000,1000); self.b.save(role)
        self.call(4, index=1, count=1)
        self.assertEqual(self.saved()['purchases'].get('1'), 1)

        # Reopening the local backend on the same day retains the selection and
        # purchase counters. A later week also crosses the daily boundary.
        snapshot = self.b.profile(); self.b.close()
        self.b = Backend(Path(self.tmp.name), 18770, lambda *a, **k: None)
        self.assertEqual(snapshot, self.b.profile())
        reopened = self.call(8)[0]
        self.assertEqual(self.shop_signature(first), self.shop_signature(reopened))

        next_week = npc.start(before['week'] + 1, self.b.activity_rules)
        with patch('network_redirect.backend.time.time', return_value=next_week):
            refreshed = self.call(8)[0]
        self.assert_shop_subset(refreshed)
        self.assertEqual(list(refreshed['my_exchange'].values()), [0] * len(refreshed['my_shop']))
        self.assertEqual(self.saved()['week'], npc.week(next_week, self.b.activity_rules))

    def test_tools_keys_loot_and_revisit_no_refill(self):
        self.legacy_babel_floor()
        self.call()
        with patch('network_redirect.activity_babel.journey.battle',return_value=(3,[],[])):
            for row,col in ((1,2),(1,3),(1,4),(1,5),(2,5)):
                self.call(2,target_pos=dict(row=row,column=col))
        role=self.b.profile()
        self.assertEqual(babel.item_count(role,20012),0)
        self.assertEqual(babel.item_count(role,20006),0)
        self.assertEqual(self.saved()['coin_count'],100)
        self.call(6)
        for col in (2,3,4,5): self.call(2,target_pos=dict(row=1,column=col))
        self.assertEqual(self.saved()['coin_count'],100)
        self.call(6); self.call(2,target_pos=dict(row=2,column=1))
        self.call(2,target_pos=dict(row=2,column=2))
        self.assertEqual(babel.item_count(self.b.profile(),20005),0)

    def test_loss_keeps_guard_and_position_but_spends_resources(self):
        self.legacy_babel_floor()
        self.call(); self.call(2,target_pos=dict(row=1,column=2)); before=self.saved()
        with patch('network_redirect.activity_babel.journey.battle',return_value=(4,[],[])):
            self.call(2,target_pos=dict(row=1,column=3))
        s=self.saved(); self.assertEqual(s['locale'],before['locale'])
        self.assertEqual(s['floors']['1'][0][2]['elem_type'],20012)
        self.assertEqual((s['life'],s['energy'],s['coin_count']),(80,98,0))
        self.assertEqual([m for m,_,d in self.decoded if m in (1027,1028)],[1028,1027])
        self.assertTrue(any(m==2998 and d['id']==44 for m,_,d in self.decoded))

    def test_master_gate_and_terminal_once(self):
        self.legacy_babel_floor()
        self.call(); self.edit(locale=dict(row=5,column=7))
        self.reject(2,target_pos=dict(row=5,column=8))
        role=self.b.profile(); s=role['activity']['babel']; s['cur_floor']=70; s['history_floor']=70
        babel.generate(s); self.b.save(role)
        with patch('network_redirect.activity_babel.journey.battle',return_value=(3,[],[])):
            self.visit_element(9)
        grid=self.saved()['floors']['70']
        terminal=next((r,c) for r,line in enumerate(grid,1) for c,cell in enumerate(line,1) if cell['elem_type']==3)
        previous=self.saved()['locale']
        self.visit_element(3)
        self.assertTrue(self.saved()['complete']); before=self.saved()['coin_count']
        self.call(2,target_pos=previous); self.call(2,target_pos=dict(zip(('row','column'),terminal)))
        self.assertEqual(self.saved()['coin_count'],before)
        self.assertEqual(self.saved()['cur_floor'],70)

    def test_weekly_rank_mail_reset_preserves_items_and_claim_once(self):
        self.call(); role=self.b.profile(); s=role['activity']['babel']
        s.update(history_floor=60,participated=True,energy=300,life=5)
        # Simulate a legacy participating save without a Thursday snapshot.
        s.pop('frozen_week', None)
        summon.add_item(role,20012,3); summon.add_item(role,20000,100)
        self.b.save(role); before=self.saved(); monday=npc.start(before['week']+1,self.b.activity_rules)
        with patch('network_redirect.backend.time.time',return_value=monday):
            self.call(); s=self.saved()
            self.assertEqual((s['cur_floor'],s['history_floor'],s['life'],s['energy']),(1,1,100,300))
            self.assertEqual(s['last_my_top']['order'],1)
            role=self.b.profile(); self.assertEqual(babel.item_count(role,20012),3)
            mails=[v for k,v in role['welfare']['mails'].items() if k.startswith('babel-rank-')]
            self.assertEqual(len(mails),1); self.assertEqual(mails[0]['prizes'],[[5,20000,2000,1]])
            self.call(); self.ok(self.req(1103,mail_id=mails[0]['mail_id'],flag=1))
            self.assertEqual(babel.item_count(self.b.profile(),20000),2100)
            self.req(1103,mail_id=mails[0]['mail_id'],flag=1)
            self.assertEqual(babel.item_count(self.b.profile(),20000),2100)
            self.call(8); self.assertEqual(self.saved()['coin_count'],2100)
        with patch('network_redirect.backend.time.time',return_value=monday+4*604800):
            self.call()
            self.assertEqual(len([k for k in self.b.profile()['welfare']['mails'] if k.startswith('babel-rank-')]),1)

    def test_week_settles_on_login_prepare_without_entering_tower(self):
        self.call(); role=self.b.profile(); s=role['activity']['babel']; s['participated']=True
        s.pop('frozen_week', None)
        monday=npc.start(s['week']+1,self.b.activity_rules)
        activity.prepare(role,monday,self.b.activity_rules)
        self.assertEqual(role['activity']['babel']['history_floor'],1)
        self.assertTrue(any(k.startswith('babel-rank-') for k in role['welfare']['mails']))

    def test_rank_stable_identities_arrival_ties_and_restart(self):
        self.call(); first=self.call(3)[0]
        self.assertEqual(len(first['all_top']),31)
        for row in first['all_top'].values():
            if row['is_npc']: self.assertIsNotNone(npc_players.resolve(row['role_id']))
        snapshot=self.b.profile(); self.b.close(); self.b=Backend(Path(self.tmp.name),18770,lambda *a,**k:None)
        self.assertEqual(snapshot,self.b.profile()); self.assertEqual(first,self.call(3)[0])
        s=self.saved(); rows=npc.ranking(self.b.profile(),s,NOW,self.b.activity_rules)['all_top']
        self.assertEqual(rows,sorted(rows,key=lambda v:(-v['history_floor'],v['reached_at'],v['role_id'])))

    def test_legacy_currency_and_map_migration(self):
        self.legacy_babel_floor()
        self.call(); role=self.b.profile(); s=role['activity']['babel']
        for k in ('coin_inventory','week','clock','energy_tick','opponents'): s.pop(k,None)
        s['coin_count']=120; s['floors']['1'][0][1]['elem_type']=0; self.b.save(role)
        self.call(); self.call()
        self.assertEqual(babel.item_count(self.b.profile(),20000),120)
        self.assertEqual(self.saved()['floors']['1'][0][1]['elem_type'],0)

    def test_partial_legacy_state_migrates_shared_fight_and_limits(self):
        self.call(); role=self.b.profile(); s=role['activity']['babel']
        role['activity'].pop('fight_id', None)
        s.update(max_life=0, max_energy='bad', life=-5, energy=-1,
                 purchases={'1': 999, '2': 'bad'}, day=activity.day(NOW, self.b.activity_rules), coin_count='bad')
        s['floors']='bad'; s['locale']={'row':'bad','column':99}
        self.b.save(role)
        # A direct 1353 query must migrate the save before any battle request.
        self.call()
        migrated=self.saved()
        self.assertEqual(self.b.profile()['activity']['fight_id'], 100000)
        self.assertEqual((migrated['max_life'], migrated['max_energy'], migrated['life'], migrated['energy']),
                         (100, 100, 100, 100))
        self.assertEqual(migrated['purchases'], {'1': migrated['shop_goods'][0][3]})
        self.assertEqual(migrated['day'], activity.day(NOW, self.b.activity_rules))

    def test_replay_and_forged_input_roll_back(self):
        self.call(); role=self.b.profile(); summon.add_item(role,20019,3); self.b.save(role)
        self.call(10,item_type=20019,count=1); packet=self.packet; replies=self.replies; before=self.b.profile()
        self.assertEqual(self.b.respond(packet,self.state),replies); self.assertEqual(self.b.profile(),before)
        for op,data in ((2,dict(target_pos=dict(row=5,column=8))), (2,dict(target_pos=dict(row=True,column=2))),
                        (7,dict(floor=60)), (7,dict(floor=True)), (10,dict(item_type=20019,count=-1)),
                        (10,dict(item_type=20019,count=True)), (4,dict(index=True)), (5,{})):
            self.reject(op,**data)

    def test_entry_level_and_original_config(self):
        role=self.b.profile(); role['level']=35; self.b.save(role); self.reject(1)
        self.assertEqual(self.b.activity_rules['babel_energy_items'],{'20016':10,'20017':25,'20018':80,'20019':200})

    def test_npc_fixed_progression_and_immutable_source(self):
        powers=[]
        for floor in range(1,61):
            key=npc.choose(floor,9); powers.append(npc_players.catalog()[key]['profile']['role_combat_power'])
            self.assertGreaterEqual(len(npc.template(key)),1)
        self.assertEqual(powers,sorted(powers)); self.assertGreater(powers[-1],powers[0]*30)
        self.call(); s=self.saved(); key,units=npc.enemies(s,9,4,7); before=copy.deepcopy(npc.template(key))
        units[0]['hp']=1; self.assertEqual(npc.template(key),before)

    def test_real_catalog_fight_replay_and_fixed_opponent(self):
        self.legacy_babel_floor()
        self.call(); role=self.b.profile(); ident=role['role_id']
        activity_state=copy.deepcopy(role['activity'])
        key=max(npc_players.catalog(),key=lambda k:npc_players.catalog()[k]['profile']['role_combat_power'])
        role.update(copy.deepcopy(npc_players.get(key)['role'])); role['role_id']=ident
        # Expanded NPC profiles carry their own activity data; preserve this
        # test's legacy map instead of replacing it with a new random floor.
        role['activity']=activity_state
        self.b.save(role)
        self.call(2,target_pos=dict(row=1,column=2)); self.call(2,target_pos=dict(row=1,column=3))
        from test_battle_replay import decoded_packets
        fight=next(d for m,_,d in decoded_packets(self.replies) if m==1027)
        self.assertIn(fight['final_result'],(1,2,3)); self.assertEqual(fight['fight_type'],200)
        self.assertGreater(fight['fight_round'],0)
        self.assertTrue(all(len(x['damage_list'])==8 for x in fight['fight_result']))
        self.assertEqual(self.saved()['coin_count'],50)
