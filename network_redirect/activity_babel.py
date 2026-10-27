"""通天塔：原客户端1353/event203与恢复规则 [A]，缺失地图/平衡 [B]."""
import copy
import secrets
from . import activity as a, journey, summon, activity_babel_npc as npc
from . import battle_replay
from .protocol import encode

FLOORS = summon.rows('babel_tower_floor_prize.csv')
MAX_FLOOR = max(int(row['floor_r']) for row in FLOORS)
GUARDS = (7, 8, 9, 20010, 20011, 20012, 20013, 20014, 20015)
TOOLS = {20003: 20005, 20004: 20006, 20007: 20010, 20008: 20011, 20009: 20012}
GOODS = ((1001, 10, 100, 10), (20016, 1, 50, 5), (20006, 1, 50, 5),
         (1023, 1, 100, 5), (1343, 1, 150, 5), (1034, 1, 100, 5))


def response(op, data):
    return summon.event(203, dict(id=op, data=data))


def generate(s):
    # [B] Connected, resource-solvable 5x8 floor; revisits never refill loot.
    key = str(s['cur_floor'])
    if key not in s['floors']:
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


def state(role, now, r):
    s = role['activity'].setdefault('babel', dict(cur_floor=1, history_floor=1, max_floor=MAX_FLOOR,
        life=100, max_life=100, energy=100, max_energy=100, coin_count=0,
        floors={}, purchases={}, refresh_times=1, day=-1))
    # Migrate old saves without restoring already collected cells or coins.
    s.setdefault('week', npc.week(now, r)); s.setdefault('reached_at', now)
    s.setdefault('opponents', {}); s.setdefault('complete', False)
    s.setdefault('participated', s['history_floor'] > 1)
    now = max(now, s.setdefault('clock', now)); s['clock'] = now
    npc.rollover(role, s, now, r)
    if s['day'] < a.day(now, r):
        s.update(day=a.day(now,r), life=s['max_life'], refresh_times=1, purchases={})
    # [A] Half-hour recovery; [B] one point each tick, cap 100. Above-cap
    # consumable energy is preserved, and full-cap ticks are not banked.
    tick = now // 1800
    previous = s.setdefault('energy_tick', tick)
    if tick > previous:
        if s['energy'] < s['max_energy']:
            s['energy'] = min(s['max_energy'], s['energy'] + tick-previous)
        s['energy_tick'] = tick
    if str(s['cur_floor']) not in s['floors']:
        generate(s)
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
             for tid,n,cost,limit in GOODS]
    return dict(coin_count=s['coin_count'], refresh_times=s['refresh_times'], my_shop=goods,
                my_exchange=[s['purchases'].get(str(i),0) for i in range(1,7)])


def floor_reward(role, s, r):
    pool = next(x for x in FLOORS if int(x['floor_l']) <= s['cur_floor'] <= int(x['floor_r']))
    # CSV contains duplicate entries; keep those multiplicities as weights [B].
    specs = [list(map(int,x.split('|')))+[1] for x in pool['daoju'].split('/')]
    reward = a.prizes(role, [secrets.choice(specs)])
    coins(role, s, r['babel_cell_coins'])
    return reward + [a.prize_spec([5,20000,r['babel_cell_coins'],1])]


def fight(role, s, typ, row, col, jrules):
    a.require(any(1 <= c.get('order',0) <= 8 for c in role['corteges']), '请先上阵神仙')
    a.require(s['life'] > 0, '生命不足，请恢复后挑战守卫')
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
    s['life'] = max(0, s['life']-cost)
    return 1 <= result <= 3, fid, events


def settle(role, req, now, r, jrules, parse):
    a.require(role['level'] >= 36, '通天塔需36级')
    op = req['id']; data = parse(req['data']) if req['data'] else {}
    a.require(isinstance(data,dict), '通天塔参数无效')
    a.require(op in (1,2,3,4,6,7,8,9,10,11), '通天塔操作无效')
    s = state(role, now, r)
    if op == 1:
        return [response(1,info(s))]
    if op == 3:
        return [response(3,npc.ranking(role,s,s['clock'],r))]
    if op in (8,9,4):
        if op == 9:
            a.require(s['refresh_times'] > 0 and s['coin_count'] >= 200, '通天币不足或刷新次数已用完')
            coins(role,s,-200); s['refresh_times'] -= 1; s['purchases'] = {}
        if op == 4:
            idx, n = data.get('index'), data.get('count',1)
            a.require(type(idx) is int and 1 <= idx <= 6 and type(n) is int and 1 <= n <= 100, '兑换数量无效')
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

    target = data.get('target_pos')
    a.require(isinstance(target,dict), '移动目标无效')
    row, col = target.get('row'), target.get('column'); p = s['locale']
    a.require(type(row) is int and type(col) is int and 1 <= row <= 5 and 1 <= col <= 8, '坐标无效')
    a.require(abs(row-p['row'])+abs(col-p['column']) == 1, '只能移动到相邻格')
    a.require(s['energy'] > 0, '行动力不足')
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
    s['energy'] -= 1; s['participated'] = True
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
    events.append(response(2,data))
    if won and typ == 3 and s['cur_floor'] < s['max_floor']:
        s['cur_floor'] += 1
        if s['cur_floor'] > s['history_floor']:
            s['history_floor'] = s['cur_floor']; s['reached_at'] = s['clock']
        generate(s); events.append(response(1,info(s)))
    if fid is not None:
        events.append(summon.event(44,dict(fight_id=fid,fight_type=200)))
    return events
