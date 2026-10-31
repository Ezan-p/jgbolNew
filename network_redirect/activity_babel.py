"""通天塔：原客户端1353/event203与恢复规则 [A]，缺失地图/平衡 [B]."""
import copy
import secrets
from . import activity as a, journey, summon, activity_babel_npc as npc
from . import battle_replay
from .protocol import encode

FLOORS = summon.rows('babel_tower_floor_prize.csv')
SECRET_FLOORS = summon.rows('babel_secret_tower_floor_prize.csv')
STAGES = {int(x['stage_index']): [list(map(int, p.split('|'))) for p in x['prize'].split('/')]
          for x in summon.rows('tongtianta_score_awards.csv')}
MAX_FLOOR = max(int(row['floor_r']) for row in FLOORS)
GUARDS = (7, 8, 9, 20010, 20011, 20012, 20013, 20014, 20015)
TOOLS = {20003: 20005, 20004: 20006, 20007: 20010, 20008: 20011, 20009: 20012}
# The client always renders six slots.  The original product table is absent
# from the offline package, so this pool is the explicit local design supplied
# for the offline activity.  A player's six slots are sampled without
# replacement and persisted for the current Babel week.
SHOP_POOL = ((1001, 10, 100, 10), (1022, 1, 100, 3), (1023, 1, 100, 3),
             (20016, 1, 50, 3), (20017, 1, 100, 3), (20018, 1, 250, 2),
             (20019, 1, 500, 1), (20005, 1, 50, 3), (20006, 1, 50, 5),
             (20010, 1, 200, 3), (20011, 1, 150, 3), (20012, 1, 100, 3),
             (1034, 1, 50, 5), (1033, 1, 100, 5), (1032, 1, 300, 3),
             (10000, 2, 100, 3), (10001, 5, 100, 5))
SHOP_SLOT_COUNT = 6
SHOP_POOL_SET = frozenset(SHOP_POOL)


def response(op, data):
    return summon.event(203, dict(id=op, data=data))


def random_floor(s):
    """[B] Random early floor, with every tool and key reachable before use."""
    rng = secrets.SystemRandom()
    cells = {(row, col) for row in range(5) for col in range(8)}
    # Keep a small safe entrance. Distinct stairs guarantee ten distinct maps,
    # even after loot on earlier floors has been collected.
    entrance = {(0, 0), (0, 1), (1, 0)}
    old_stairs = {(row, col) for floor in range(1, 11)
                  for row, line in enumerate(s['floors'].get(str(floor), []))
                  for col, cell in enumerate(line) if cell['elem_type'] == 3}
    stairs = rng.choice(sorted(pos for pos in cells - old_stairs
                               if sum(pos) >= 6))
    blocked = {stairs}
    positions = [(stairs, 3)]
    candidates = sorted(cells - entrance - blocked)
    rng.shuffle(candidates)
    for typ in TOOLS:
        for pos in candidates:
            proposed = blocked | {pos}
            walkable = cells - proposed
            reachable = {(0, 0)}
            pending = [(0, 0)]
            while pending:
                row, col = pending.pop()
                for neighbor in ((row-1, col), (row+1, col), (row, col-1), (row, col+1)):
                    if neighbor in walkable and neighbor not in reachable:
                        reachable.add(neighbor)
                        pending.append(neighbor)
            # No tool, key guard or master can be sealed behind a chest,
            # obstacle or the gated staircase; each blocked cell is accessible.
            if len(reachable) != len(cells) - len(proposed):
                continue
            if not all(any((row+dr, col+dc) in reachable
                           for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)))
                       for row, col in proposed):
                continue
            blocked = proposed
            positions.append((pos, typ))
            candidates.remove(pos)
            break
        else:
            raise RuntimeError('Cannot place Babel floor obstacles')
    # Preserve the original quantities and combat/reward balance.
    occupants = (20005, 20006, 20010, 20011, 20012, 20013, 20014, 20015, 9)
    positions.extend(zip(rng.sample(sorted(cells - entrance - blocked), len(occupants)), occupants))
    grid = [[dict(elem_type=0, visible=False) for _ in range(8)] for _ in range(5)]
    for (row, col), typ in positions:
        grid[row][col]['elem_type'] = typ
    return grid


def generate(s):
    # [B] Randomize only newly created early floors; never refill saved loot.
    key = str(s['cur_floor'])
    if key not in s['floors'] and 1 <= s['cur_floor'] <= 10:
        s['floors'][key] = random_floor(s)
    elif key not in s['floors']:
        grid = [[dict(elem_type=0, visible=False) for _ in range(8)] for _ in range(5)]
        for row, col, typ in ((1,2,20005), (1,3,20012), (1,4,20009), (1,5,20006),
                             (2,2,20003), (2,3,20011), (2,4,20008), (2,5,20004),
                             (3,2,20010), (3,3,20007), (3,4,20015), (4,2,20014),
                             (4,3,20013), (4,7,9), (5,8,3)):
            grid[row-1][col-1]['elem_type'] = typ
        s['floors'][key] = grid
    s['locale'] = dict(row=1, column=1)
    reveal(s)


def reveal(s):
    p = s['locale']; grid = s['floors'][str(s['cur_floor'])]
    for row in range(max(1,p['row']-1), min(5,p['row']+1)+1):
        for col in range(max(1,p['column']-1), min(8,p['column']+1)+1):
            grid[row-1][col-1]['visible'] = True


def valid_shop_goods(goods):
    if not isinstance(goods, list) or len(goods) != SHOP_SLOT_COUNT:
        return False
    normalized = []
    for item in goods:
        if not isinstance(item, (list, tuple)) or len(item) != 4:
            return False
        if not all(type(value) is int for value in item) or tuple(item) not in SHOP_POOL_SET:
            return False
        normalized.append(tuple(item))
    return len(set(normalized)) == SHOP_SLOT_COUNT


def random_shop_goods(previous=None):
    """Draw six distinct pool entries, changing the catalog on a refresh."""
    chosen = secrets.SystemRandom().sample(SHOP_POOL, SHOP_SLOT_COUNT)
    if previous and valid_shop_goods(previous) and tuple(chosen) == tuple(map(tuple, previous)):
        available = [item for item in SHOP_POOL if item not in chosen]
        chosen[-1] = secrets.choice(available)
    return [list(item) for item in chosen]


def state(role, now, r):
    # `activity.prepare` normally creates the shared fight counter.  Older
    # offline saves can enter this handler directly (or predate that field),
    # so migrate it here as well before a guard battle allocates a replay id.
    activity = role.setdefault('activity', {})
    if type(activity.get('fight_id')) is not int or activity['fight_id'] < 0:
        activity['fight_id'] = 100000
    defaults = dict(cur_floor=1, history_floor=1, max_floor=MAX_FLOOR,
        life=100, max_life=100, energy=100, max_energy=100, coin_count=0,
        floors={}, purchases={}, refresh_times=1, day=-1)
    s = activity.get('babel')
    if not isinstance(s, dict):
        s = activity['babel'] = copy.deepcopy(defaults)
    # Keep malformed/partial legacy sections from turning a read-only query
    # into a permanent KeyError/TypeError.  Valid above-cap energy remains
    # untouched; only impossible values are repaired.
    if type(s.get('max_life')) is not int or s['max_life'] <= 0:
        s['max_life'] = 100
    if type(s.get('max_energy')) is not int or s['max_energy'] <= 0:
        s['max_energy'] = 100
    if type(s.get('life')) is not int or s['life'] < 0:
        s['life'] = s['max_life']
    else:
        s['life'] = min(s['life'], s['max_life'])
    if type(s.get('energy')) is not int or s['energy'] < 0:
        s['energy'] = s['max_energy']
    # Expand an old completed 60-floor save without restoring any old loot.
    if s.get('max_floor') == 60 and s.get('complete'):
        s['complete'] = False
        grid = s.get('floors', {}).get('60') if isinstance(s.get('floors'), dict) else None
        if isinstance(grid, list) and len(grid) == 5 and isinstance(grid[4], list) and len(grid[4]) == 8:
            grid[4][7] = dict(elem_type=3, visible=True)
    s['max_floor'] = MAX_FLOOR
    for key in ('cur_floor', 'history_floor'):
        if type(s.get(key)) is not int or not 1 <= s[key] <= s['max_floor']:
            s[key] = 1
    if s['history_floor'] < s['cur_floor']:
        s['history_floor'] = s['cur_floor']
    if type(s.get('floors')) is not dict:
        s['floors'] = {}
    current_key = str(s['cur_floor'])
    grid = s['floors'].get(current_key)
    valid_grid = (isinstance(grid, list) and len(grid) == 5 and
                  all(isinstance(row, list) and len(row) == 8 and
                      all(isinstance(cell, dict) and type(cell.get('elem_type')) is int
                          and type(cell.get('visible')) is bool for cell in row)
                      for row in grid))
    if not valid_grid:
        s['floors'].pop(current_key, None)
    locale = s.get('locale')
    if (not isinstance(locale, dict) or type(locale.get('row')) is not int or
            type(locale.get('column')) is not int or
            not 1 <= locale['row'] <= 5 or not 1 <= locale['column'] <= 8):
        s['locale'] = dict(row=1, column=1)
    if type(s.get('purchases')) is not dict:
        s['purchases'] = {}
    if type(s.get('refresh_times')) is not int or not 0 <= s['refresh_times'] <= 1:
        s['refresh_times'] = 1
    if type(s.get('day')) is not int:
        s['day'] = -1
    if type(s.get('opponents')) is not dict:
        s['opponents'] = {}
    # Migrate old saves without restoring already collected cells or coins.
    if type(s.get('week')) is not int:
        s['week'] = npc.week(now, r)
    if type(s.get('reached_at')) is not int:
        s['reached_at'] = now
    if type(s.get('complete')) is not bool:
        s['complete'] = False
    if type(s.get('participated')) is not bool:
        s['participated'] = s['history_floor'] > 1
    if type(s.get('clock')) is not int:
        s['clock'] = now
    now = max(now, s['clock']); s['clock'] = now
    previous_week = s['week']
    npc.rollover(role, s, now, r)
    npc.settle_week(role, s, now, r)
    week_changed = s['week'] != previous_week
    if (week_changed or type(s.get('shop_week')) is not int or
            s.get('shop_week') != s['week'] or not valid_shop_goods(s.get('shop_goods'))):
        old_goods = s.get('shop_goods') if valid_shop_goods(s.get('shop_goods')) else None
        s['shop_week'] = s['week']
        s['shop_goods'] = random_shop_goods(old_goods if week_changed else None)
        s['purchases'] = {}
        s['refresh_times'] = 1
    elif type(s.get('refresh_times')) is not int or not 0 <= s['refresh_times'] <= 1:
        s['refresh_times'] = 1
    # Limit values belong to the persisted catalog.  This also migrates old
    # purchase counters after the six slots have changed.
    s['purchases'] = {
        str(i): min(s['shop_goods'][i - 1][3], value)
        for i in range(1, SHOP_SLOT_COUNT + 1)
        for value in [s['purchases'].get(str(i), 0)]
        if type(value) is int and value > 0
    }
    if s['day'] < a.day(now, r):
        # Life is daily; the shop catalog and its limits are weekly.
        s.update(day=a.day(now,r), life=s['max_life'])
    # [A] Half-hour recovery; [B] one point each tick, cap 100. Above-cap
    # consumable energy is preserved, and full-cap ticks are not banked.
    tick = now // 1800
    if type(s.get('energy_tick')) is not int:
        s['energy_tick'] = tick
    previous = s['energy_tick']
    if tick > previous:
        if s['energy'] < s['max_energy']:
            s['energy'] = min(s['max_energy'], s['energy'] + tick-previous)
        s['energy_tick'] = tick
    if str(s['cur_floor']) not in s['floors']:
        generate(s)
    if type(s.get('coin_count')) is not int or s['coin_count'] < 0:
        s['coin_count'] = 0
    if not s.get('coin_inventory'):
        existing = item_count(role, 20000)
        if s['coin_count'] > existing:
            a.prizes(role, [[5,20000,s['coin_count']-existing,1]])
        s['coin_inventory'] = True
    s['coin_count'] = item_count(role, 20000)
    return s


def item_count(role, tid):
    return sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==tid)


def coins(role, s, n):
    if n > 0:
        a.prizes(role, [[5,20000,n,1]])
    else:
        a.consume(role, 20000, -n)
    s['coin_count'] = item_count(role, 20000)


def info(s):
    return dict(**{k:copy.deepcopy(s[k]) for k in ('cur_floor','history_floor','max_floor','life',
                'max_life','energy','max_energy','locale','complete')},
                dungeon=copy.deepcopy(s['floors'][str(s['cur_floor'])]))


def shop(s):
    # [A] Client subtracts my_exchange from limit itself (Lua L1113-1114).
    goods = [dict(reward=[a.prize_spec([5,tid,n,1])], need_coin=cost, limit=limit)
             for tid,n,cost,limit in s['shop_goods']]
    return dict(coin_count=s['coin_count'], refresh_times=s['refresh_times'], my_shop=goods,
                my_exchange=[s['purchases'].get(str(i),0) for i in range(1,7)])


def floor_reward(role, s, r):
    secret = s.get('secret', False)
    pool = next(x for x in (SECRET_FLOORS if secret else FLOORS)
                if int(x['floor_l']) <= s['cur_floor'] <= int(x['floor_r']))
    # CSV contains duplicate entries; keep those multiplicities as weights [B].
    # One secret entry already contains its level; do not append a fifth field.
    specs = []
    for raw in pool['daoju'].split('/'):
        spec = list(map(int, raw.split('|')))
        if len(spec) == 3:
            spec.append(1)
        specs.append(spec)
    reward = a.prizes(role, [secrets.choice(specs)])
    if secret:
        return reward
    coins(role, s, r['babel_cell_coins'])
    return reward + [a.prize_spec([5,20000,r['babel_cell_coins'],1])]


def fight(role, s, typ, row, col, jrules):
    a.require(any(1 <= c.get('order',0) <= 8 for c in role['corteges']), '请先上阵神仙')
    a.require(s.get('secret') or s['life'] > 0, '生命不足，请恢复后挑战守卫')
    key, enemies = npc.enemies(s, typ, row, col)
    ours = journey.fighters(role, dict(cortege_list='1001|1'))[0]
    result, lineup, actions = journey.battle(role, {}, jrules, units=(ours,enemies))
    role['activity']['fight_id'] += 1; fid = role['activity']['fight_id']
    name = npc.npc_players.catalog()[key]['profile']['role_name']
    events = journey.combat_engine.event_packets(actions,fid) + [
        encode(1028,dict(fight_id=fid,first_hand=1,des_name='守塔·'+name,lineup_count=len(lineup),lineup=lineup)),
        *battle_replay.result_packets(1027, dict(fight_id=fid,fight_type=200,final_result=result,fight_round=len(actions),fight_result=actions))]
    maximum = sum(u['max_hp'] for u in ours)
    remaining = getattr(actions, 'final_hp', {}).get(1)
    lost = max(0, maximum-sum(remaining.values())) if remaining is not None else journey.combat_engine.total_damage(actions,2)
    cost = max(1, (100*lost+maximum-1)//max(1,maximum))
    if not 1 <= result <= 3:
        cost = max(20, cost)
    if not s.get('secret'):
        s['life'] = max(0, s['life']-cost)
    return 1 <= result <= 3, fid, events


def settle(role, req, now, r, jrules, parse):
    a.require(role['level'] >= 36, '通天塔需36级')
    op = req['id']; data = parse(req['data']) if req['data'] else {}
    a.require(isinstance(data,dict), '通天塔参数无效')
    a.require(op in (1,2,3,4,6,7,8,9,10,11,12,13,14), '通天塔操作无效')
    s = state(role, now, r)
    if op in (12, 13, 14):
        return secret_settle(role, s, op, data, r, jrules)
    if op == 1:
        return [response(1,info(s))]
    if op == 3:
        return [response(3,npc.ranking(role,s,s['clock'],r))]
    if op in (8,9,4):
        if op == 9:
            a.require(s['refresh_times'] > 0 and s['coin_count'] >= 200, '通天币不足或刷新次数已用完')
            coins(role,s,-200); s['refresh_times'] -= 1
            s['shop_goods'] = random_shop_goods(s['shop_goods'])
            s['purchases'] = {}
        if op == 4:
            idx, n = data.get('index'), data.get('count',1)
            a.require(type(idx) is int and 1 <= idx <= SHOP_SLOT_COUNT and type(n) is int and 1 <= n <= 100, '兑换数量无效')
            goods = shop(s)['my_shop'][idx-1]; count = s['purchases'].get(str(idx),0)
            a.require(n <= goods['limit']-count and s['coin_count'] >= goods['need_coin']*n, '兑换次数或通天币不足')
            coins(role,s,-goods['need_coin']*n); s['purchases'][str(idx)] = count+n
            p = goods['reward'][0]
            a.prizes(role, [[p['object_type'],p['attach_type'],p['attach_count']*n,p['attach_level']]])
        return ([response(4,{})] if op==4 else []) + [response(8,shop(s))]
    if op == 11:
        a.require(s['life'] < s['max_life'], '生命已满')
        a.spend(role,'gold_coin',200); s['life'] = s['max_life']
        return [response(11,dict(life=s['life']))]
    if op == 10:
        tid, n = data.get('item_type'), data.get('count',1)
        a.require(type(tid) is int and tid in (20016,20017,20018,20019) and type(n) is int and 1 <= n <= 100, '恢复道具无效')
        a.consume(role,tid,n)
        s['energy'] += r['babel_energy_items'][str(tid)]*n
        return [response(10,dict(energy=s['energy']))]
    if op in (6,7):
        dest = 1 if op==6 else data.get('floor')
        a.require(type(dest) is int and 1 <= dest <= s['history_floor'], '尚未到达该层')
        if op == 7:
            a.spend(role,'gold_coin',20)
        s['cur_floor'] = dest; generate(s)
        return [response(1,info(s))]

    return move(role, s, data, r, jrules)


def secret_settle(role, tower, op, data, r, jrules):
    """[A] Five three-floor runs; one ticket each teleport; no HP/energy cap.

    [B] A paid teleport creates a fresh run, discarding the previous run.
    Queries/reconnects preserve it; ordinary tower weekly resets do not erase it.
    """
    s = tower.get('secret_run')
    if op == 14:
        floor = data.get('floor')
        a.require(type(floor) is int and floor in (1001, 1004, 1007, 1010, 1013), '请选择秘境副本入口')
        a.consume(role, 1377, 1)
        s = tower['secret_run'] = dict(secret=True, cur_floor=floor, history_floor=floor,
            max_floor=floor+2, life=100, max_life=100, energy=100, max_energy=100,
            floors={}, opponents={}, complete=False, clock=tower['clock'])
        generate(s)
    if op in (12, 14):
        return [response(12, info(s) if s else {})]
    a.require(isinstance(s, dict), '请使用入场券进入秘境')
    s['clock'] = tower['clock']
    return move(role, s, data, r, jrules)


def move(role, s, data, r, jrules):
    secret = s.get('secret', False)
    move_op, info_op = (13, 12) if secret else (2, 1)
    target = data.get('target_pos')
    a.require(isinstance(target,dict), '移动目标无效')
    row, col = target.get('row'), target.get('column'); p = s['locale']
    a.require(type(row) is int and type(col) is int and 1 <= row <= 5 and 1 <= col <= 8, '坐标无效')
    a.require(abs(row-p['row'])+abs(col-p['column']) == 1, '只能移动到相邻格')
    a.require(secret or s['energy'] > 0, '行动力不足')
    grid = s['floors'][str(s['cur_floor'])]; cell = grid[row-1][col-1]; typ = cell['elem_type']
    a.require(typ != 1, '不可进入边界')
    if typ == 3:
        a.require(not any(c['elem_type']==9 for line in grid for c in line), '请先击败本层守塔者')
    if typ in TOOLS:
        a.consume(role,TOOLS[typ],1)
    events, reward, fid, won = [], [], None, True
    completed_now = False
    if typ in GUARDS:
        won, fid, events = fight(role,s,typ,row,col,jrules)
    if not secret:
        s['energy'] -= 1
        s['participated'] = True
    if won:
        if typ in (5,20007,20008,20009) or typ in GUARDS:
            reward = floor_reward(role,s,r)
            if typ in (20010,20011,20012):
                reward += a.prizes(role,[[5,typ,1,1]])
        if typ in (20005,20006):
            reward = a.prizes(role,[[5,typ,1,1]])
        s['locale'] = dict(row=row,column=col)
        if typ not in (0,3):
            cell['elem_type'] = 0
        if typ == 3 and s['cur_floor'] == s['max_floor']:
            # [B] Terminal staircase becomes ordinary ground; one completion
            # payout per week. Never roll back the final move as an error.
            if not s['complete']:
                completed_now = True
                reward += floor_reward(role,s,r)
            s['complete'] = True; cell['elem_type'] = 0
        reveal(s)
    data = dict(locale=copy.deepcopy(s['locale']), life=s['life'], energy=s['energy'],
                update=copy.deepcopy(grid), fight_flag=fid is not None, completed_now=completed_now)
    if reward:
        data['rewards'] = reward
    events.append(response(move_op,data))
    if won and typ == 3 and s['cur_floor'] < s['max_floor']:
        s['cur_floor'] += 1
        if s['cur_floor'] > s['history_floor']:
            s['history_floor'] = s['cur_floor']; s['reached_at'] = s['clock']
        generate(s); events.append(response(info_op,info(s)))
    if secret and completed_now:
        # Keep the final map visible until the player chooses a new paid run.
        events.append(response(info_op, info(s)))
    if fid is not None:
        events.append(summon.event(44,dict(fight_id=fid,fight_type=200)))
    return events
