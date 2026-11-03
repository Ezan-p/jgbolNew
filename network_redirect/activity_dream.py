"""梦境 1325 / event 169: native puzzle and 1263 prizes [A], offline lifecycle [B]."""
import copy
import json
import secrets
from pathlib import Path

from . import activity as a, formation, npc_players, summon

ROOT = Path(__file__).resolve().parents[1]
MIN_LEVEL = 18
MAX_FRIENDS = 2  # dreamUI.showFriendChooseLayer, original line 844.
COLUMNS = ('dream_prizes', 'own_wish_prizes', 'other_wish_prizes')


def original_spec(value):
    typ, tid, level, count = map(int, value.split('|'))
    return [typ, tid, count, level]


REWARDS = {int(row['index']): {key: [original_spec(p) for p in row[key].split('/')]
                             for key in COLUMNS}
           for row in summon.rows('dream_prize_config.csv')}


def load_rules(path=ROOT / 'server_config/dream_rules.json'):
    r = json.loads(Path(path).read_text())
    a.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
              and isinstance(r.get('revision'), str) and r['revision'], '梦境配置来源无效')
    a.require(type(r.get('enabled')) is bool, '梦境开关无效')
    for key, low, high in (('timezone_offset_hours', 8, 8), ('period_days', 1, 365),
                           ('protect_times', 1, 100), ('npc_friend_count', 2, 20),
                           ('min_charge_rmb', 1, 100000)):
        a.require(type(r.get(key)) is int and low <= r[key] <= high, '梦境配置无效：' + key)
    prizes = r.get('charge_prizes')
    a.require(isinstance(prizes, list) and 1 <= len(prizes) <= 10, '梦境充值奖励缺失')
    for p in prizes:
        a.require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p)
                  and p[0] == 5 and p[1] in formation.ITEMS and 1 <= p[2] <= 100000
                  and p[3] == 1, '梦境充值奖励无效')
    a.require(r['npc_friend_count'] * r['protect_times'] >= 6 * MAX_FRIENDS,
              '梦境好友容量不足以完成六关')
    return r


def period(now, r):
    duration = r['period_days'] * 86400
    anchor = 4 * 86400 - r['timezone_offset_hours'] * 3600
    start = (now - anchor) // duration * duration + anchor
    return start, start + duration


def state(role, now, r):
    activity = role.setdefault('activity', {})
    old = activity.get('dream')
    a.require(not old or now >= old['last_time'], '梦境时钟已回退，请恢复本地时间')
    start, end = period(now, r)
    if not old or old['start'] != start:
        # Earned NPC balances survive refresh, just like the player's inventory.
        activity['dream'] = dict(start=start, end=end, last_time=now, cur_dream=1,
            status=1, take_charge=False, charge_gold=0, token=secrets.token_hex(16),
            receipts=[], received={}, npc_balances=copy.deepcopy(old['npc_balances']) if old else {})
    s = activity['dream']
    s['last_time'] = now
    return s


def status(role, now, r=None):
    r = r or load_rules()
    start, end = period(now, r)
    return dict(begin_time=start-1 if r['enabled'] else 0,
                end_time=end if r['enabled'] else 0, min_level=MIN_LEVEL,
                can_join=r['enabled'] and role.get('level', 1) >= MIN_LEVEL,
                local_refresh_time=end, local_period_days=r['period_days'])


def friends(role, s, r):
    if 'friends' not in s:
        entries = sorted(npc_players.catalog().values(), key=lambda e:
                         (abs(e['profile']['level'] - role['level']), e['profile']['role_id']))
        s['friends'] = [e['npc_id'] for e in entries[:r['npc_friend_count']]]
    result = []
    for key in s['friends']:
        p = npc_players.catalog()[key]['profile']
        result.append(dict(id=p['role_id'], name=p['role_name'], level=p['level'],
                           is_npc=True, received=s['received'].get(str(p['role_id']), 0)))
    return result


def can_take(s, r):
    from . import recharge
    return (s['cur_dream'] == 7 and not s['take_charge']
            and s['charge_gold'] >= r['min_charge_rmb'] * recharge.load_rules()['gold_per_rmb'])


def response(role, s, now, r, op, prizes=None):
    dream = dict(cur_dream=s['cur_dream'], status=s['status'], take_charge=s['take_charge'],
                 can_take=can_take(s, r), local_token=s['token'],
                 local_refresh_time=s['end'], local_charge_gold=s['charge_gold'])
    return summon.event(169, dict(flag=op, result=1, dream_data=dream,
        plus_data=dict(min_charge=r['min_charge_rmb'], protect_times=r['protect_times'],
                       charge_prize=[a.prize_spec(p) for p in r['charge_prizes']]),
        prize_list=prizes or [], local_friends=friends(role, s, r),
        local_rewards={i: {k: [a.prize_spec(p) for p in v] for k, v in row.items()}
                       for i, row in REWARDS.items()}, local_activity=status(role, now, r)))


def record_charge(role, principal, now):
    r = load_rules()
    if not r['enabled'] or principal <= 0:
        return
    s = state(role, now, r)
    s['charge_gold'] += principal


def array(value, maximum):
    if isinstance(value, dict):
        a.require(all(type(k) is int for k in value)
                  and set(value) == set(range(1, len(value)+1)), '梦境列表索引无效')
        value = [value[k] for k in range(1, len(value)+1)]
    a.require(isinstance(value, list) and 1 <= len(value) <= maximum
              and all(type(v) is int for v in value), '梦境列表格式无效')
    return value


def settle(role, req, now, parse):
    r = load_rules()
    a.require(r['enabled'], '梦境活动未开放')
    a.require(role['level'] >= MIN_LEVEL, '梦境需角色18级开放')
    op = req['id']
    a.require(op in (1, 2, 3, 4), '梦境操作无效')
    d = parse(req['data'])
    a.require(isinstance(d, dict), '梦境请求格式无效')
    s = state(role, now, r)
    if op == 1:
        a.require(not d, '梦境进入参数无效')
        return [response(role, s, now, r, op)]
    expected = {2: {'answer', 'local_token'}, 3: {'des_list', 'index', 'local_token'},
                4: {'local_token'}}[op]
    a.require(set(d) == expected and d.get('local_token') == s['token'],
              '梦境进度已变化，请重新进入活动')
    stage = s['cur_dream']
    if op == 2:
        a.require(stage <= 6 and s['status'] == 1, '请先完成本关祝福')
        answer = array(d['answer'], 9)
        a.require(answer == list(range(1, 10)), '拼图错误')
        reward = a.prizes(role, REWARDS[stage]['dream_prizes'])
        s['status'] = 2
    elif op == 3:
        a.require(stage <= 6 and s['status'] == 2, '请先完成本关解梦')
        targets = array(d['des_list'], MAX_FRIENDS)
        a.require(len(set(targets)) == len(targets), '不能重复选择同一好友')
        a.require(type(d['index']) is int and 1 <= d['index'] <= 4, '祝福语无效')
        roster = {p['id']: p for p in friends(role, s, r)}
        a.require(all(t in roster and t != role['role_id'] for t in targets), '请选择梦境好友')
        for target in targets:
            a.require(s['received'].get(str(target), 0) < r['protect_times'],
                      roster[target]['name'] + '本期收到的祝福已达上限')
        # Own prize is once per stage, irrespective of selecting one or two friends [B].
        reward = a.prizes(role, REWARDS[stage]['own_wish_prizes'])
        for target in targets:
            key = str(target)
            s['received'][key] = s['received'].get(key, 0) + 1
            balance = s['npc_balances'].setdefault(key, {})
            for typ, tid, count, level in REWARDS[stage]['other_wish_prizes']:
                item = f'{typ}:{tid}:{level}'
                balance[item] = balance.get(item, 0) + count
        s['receipts'].append(dict(stage=stage, targets=targets, index=d['index'], time=now,
                                  prizes=copy.deepcopy(REWARDS[stage]['other_wish_prizes'])))
        s['cur_dream'] += 1
        s['status'] = 1
    else:
        a.require(can_take(s, r), '需完成六关及祝福、满足本期充值条件且未领取')
        reward = a.prizes(role, r['charge_prizes'])
        s['take_charge'] = True
    s['token'] = secrets.token_hex(16)
    return [response(role, s, now, r, op, reward)]
