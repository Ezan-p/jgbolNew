"""通天塔固定难度守卫与离线周榜 [B]; immutable players catalog identities."""
import copy
import math
from functools import lru_cache
from . import npc_players, journey, combat, reborn_stars


@lru_cache(maxsize=1)
def pool():
    rows = []
    for key, entry in npc_players.catalog().items():
        p = entry['profile']
        if not 24 <= p['level'] <= 90:
            continue
        raw = npc_players.source_file(entry['source_file'])[key]
        if raw.get('battle_validation', {}).get('status') == 'replay_limit_observed':
            continue
        rows.append((p['role_combat_power'], key))
    return sorted(rows)


def choose(floor, kind):
    # Same opponent for the same floor/type, independent of player's growth.
    factor = {20012: .65, 20011: .8, 20010: 1., 20015: .8,
              20014: 1., 20013: 1.15, 7: .65, 8: 1., 9: 1.25}[kind]
    target = 8000 * (600000 / 8000) ** ((floor - 1) / 59) * factor
    return min(pool(), key=lambda row: (abs(math.log(row[0] / target)), row[1]))[1]


@lru_cache(maxsize=128)
def template(key):
    role = npc_players.get(key)['role']
    units = journey.fighters(role, dict(cortege_list='1001|1'))[0]
    combat.attach_essences(role, units)
    reborn_stars.attach_combat_traits(role, units)
    return units


def enemies(s, kind, row, column):
    identity = f"{s['cur_floor']}:{row}:{column}"
    key = s['opponents'].setdefault(identity, choose(s['cur_floor'], kind))
    return key, copy.deepcopy(template(key))


def week(now, rules):
    return ((now + rules['timezone_offset_hours'] * 3600) // 86400 - 4) // 7


def start(week_id, rules):
    return (week_id * 7 + 4) * 86400 - rules['timezone_offset_hours'] * 3600


def reward(order):
    return next((coins for end, coins in ((1, 2000), (3, 1500), (10, 1000), (30, 500), (31, 200))
                 if order <= end), 0)


@lru_cache(maxsize=1)
def competitors():
    eligible = [(power, key) for power, key in pool()
                if npc_players.catalog()[key]['profile']['level'] >= 36]
    return [key for _, key in (eligible[i * (len(eligible)-1) // 29] for i in range(30))]


def ranking(role, s, now, rules):
    begin = start(s['week'], rules)
    elapsed = max(0, min(604799, now - begin))
    rows = []
    for i, key in enumerate(competitors()):
        p = npc_players.catalog()[key]['profile']
        # Thirty fixed competitors reach 5..59 floors over the week. Their
        # arrival times are reproducible; ties use the original time rule.
        goal = 5 + i * 54 // 29
        interval = 604800 // goal
        floor = min(goal, 1 + elapsed // interval)
        rows.append(dict(role_id=p['role_id'], name=p['role_name'], npc_id=key,
                         history_floor=floor, reached_at=begin + (floor-1)*interval, is_npc=True))
    mine = dict(role_id=role['role_id'], name=role['role_name'], history_floor=s['history_floor'],
                reached_at=s['reached_at'], is_npc=False)
    rows.append(mine)
    rows.sort(key=lambda row: (-row['history_floor'], row['reached_at'], row['role_id']))
    for order, row in enumerate(rows, 1):
        row.update(order=order, reward_count=reward(order), layer=row['history_floor'])
    return dict(all_top=rows, last_top=copy.deepcopy(s.get('last_top', [])), my_top=mine,
                last_my_top=copy.deepcopy(s.get('last_my_top', {})))


def rollover(role, s, now, rules):
    current = week(now, rules)
    if current <= s['week']:
        return
    old_week = s['week']
    board = ranking(role, s, start(old_week+1, rules)-1, rules)
    s['last_top'] = board['all_top']
    s['last_my_top'] = copy.deepcopy(board['my_top'])
    if s.get('participated'):
        from . import system_mail, welfare
        mine = board['my_top']
        delivery = copy.deepcopy(role)
        system_mail.deliver(delivery, f'babel-rank-{old_week}', '通天塔离线周榜奖励',
                            f"上次参与周排名第{mine['order']}，到达{mine['history_floor']}层。对手为本地NPC。",
                            [[5, 20000, mine['reward_count'], 1]], now, welfare.load_rules())
        role['welfare'] = delivery['welfare']
    s.update(week=current, cur_floor=1, history_floor=1, reached_at=now,
             floors={}, opponents={}, complete=False, participated=False)
