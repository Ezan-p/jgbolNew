"""Role progression: original CSV/protocol [A], configurable missing balance [B]."""
import json
import time
from pathlib import Path

from . import formation, summon

ROOT = Path(__file__).resolve().parents[1]


def load_rules(path=ROOT / 'server_config/progression_rules.json'):
    r = json.loads(Path(path).read_text())
    formation.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
                      and isinstance(r.get('revision'), str) and bool(r['revision']), '升级配置来源无效')
    for key, low, high in (('newbie_days', 1, 30), ('newbie_max_level', 4, 99),
                           ('newbie_daily_strength', 1, 10000), ('newbie_bonus_percent', 0, 300),
                           ('timezone_offset_hours', -12, 14)):
        formation.require(type(r.get(key)) is int and low <= r[key] <= high, '升级配置数值无效：' + key)
    for key in ('level_rewards', 'newbie_daily_rewards'):
        rewards = r.get(key)
        formation.require(isinstance(rewards, list) and 1 <= len(rewards) <= 3, '升级奖励配置无效')
        for p in rewards:
            formation.require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p), '升级奖励格式无效')
            kind, tid, count, level = p
            formation.require(1 <= count <= 1000000 and level == 1 and
                              (kind == 5 and tid in formation.ITEMS or kind in (11, 12) and tid == 1), '升级奖励物品无效')
    return r


def day(now, r):
    return (int(now) + r['timezone_offset_hours'] * 3600) // 86400


def prepare(role, now=None, r=None):
    r = r or load_rules()
    now = int(time.time()) if now is None else now
    level = role['level']
    formation.require(type(level) is int and level in formation.LEVELS, '主角等级无效')
    role.setdefault('cur_exp', 0)
    formation.require(type(role['cur_exp']) is int and role['cur_exp'] >= 0, '主角经验无效')
    role['next_exp'] = int(formation.LEVELS[level]['upgrade_exp'])
    role['cortege_count'] = int(formation.LEVELS[level]['cortege_count'])
    if level == max(formation.LEVELS):
        role['cur_exp'] = min(role['cur_exp'], role['next_exp'])
    # Existing saves start here; historical rewards are not guessed and reissued.
    s = role.setdefault('progression', dict(rewarded_level=level, start_day=day(now, r),
                                          claimed_days=[], strength_day=day(now, r), strength_used=0))
    s['rewarded_level'] = max(level, s['rewarded_level'])
    if s['strength_day'] != day(now, r):
        s.update(strength_day=day(now, r), strength_used=0)
    return s


def add_exp(role, amount, now=None, r=None):
    from . import journey
    r = r or load_rules()
    formation.require(type(amount) is int and amount >= 0, '主角经验增量无效')
    s = prepare(role, now, r)
    old = role['level']
    role['cur_exp'] += amount
    while role['level'] < max(formation.LEVELS):
        need = int(formation.LEVELS[role['level']]['upgrade_exp'])
        if role['cur_exp'] < need:
            break
        role['cur_exp'] -= need
        role['level'] += 1
        if role['level'] > s['rewarded_level']:
            for reward in r['level_rewards']:
                journey.grant(role, reward)
            s['rewarded_level'] = role['level']
    prepare(role, now, r)
    return role['level'] - old


def strength_bonus(role, consumed, now=None, r=None):
    """Return eligible points and percent; count each attempted point, including losses."""
    r = r or load_rules()
    now = int(time.time()) if now is None else now
    s = prepare(role, now, r)
    eligible = 0
    if (0 <= day(now, r) - s['start_day'] < r['newbie_days']
            and 3 <= role['level'] < r['newbie_max_level']):
        eligible = min(consumed, max(0, r['newbie_daily_strength'] - s['strength_used']))
        s['strength_used'] += eligible
    return eligible, r['newbie_bonus_percent']


def info(role, now, r=None):
    r = r or load_rules()
    s = prepare(role, now, r)
    today = day(now, r)
    left = max(0, r['newbie_days'] - max(0, today - s['start_day']))
    active = left > 0 and role['level'] >= 3
    return dict(flag=1, buff_type=1 if active else 0,
                can_take=active and today not in s['claimed_days'],
                left_times=max(0, r['newbie_days'] - len(s['claimed_days'])), left_days=left,
                exp_add=r['newbie_bonus_percent'] if active and role['level'] < r['newbie_max_level'] else 0,
                exp_plus=0, expect_level=r['newbie_max_level'], max_strength=r['newbie_daily_strength'],
                attach_list=[dict(object_type=p[0], attach_type=p[1], attach_count=p[2], attach_level=p[3])
                             for p in r['newbie_daily_rewards']])


def settle(role, req, now):
    from . import journey
    r = load_rules()
    formation.require(req.get('op_type') == 0 and req.get('id') == 0, '升级福利请求参数无效')
    flag = req.get('flag')
    formation.require(flag in (1, 2), '当前没有合服或限时双倍经验活动')
    data = info(role, now, r)
    if flag == 2:
        formation.require(data['can_take'], '今日升级福利已领取或活动未开放／已结束')
        for p in r['newbie_daily_rewards']:
            journey.grant(role, p)
        role['progression']['claimed_days'].append(day(now, r))
        data = dict(flag=2, attach_list=data['attach_list'])
    return [summon.event(FRIEND_BUFF_EVENT, data)]


def upgrade_events(before, role):
    """The native playerLevelUp loops new_level..old_level+1, one gift list per level."""
    count = max(0, role['progression']['rewarded_level'] - before['progression']['rewarded_level'])
    if role['level'] <= before['level']:
        return []
    gifts = [dict(object_type=p[0], attach_type=p[1], attach_count=p[2], attach_level=p[3])
             for p in load_rules()['level_rewards']] if count else []
    return [summon.event(2, dict(obj_type=1, old_level=before['level'], new_level=role['level'], gift_list=gifts))]


FRIEND_BUFF_EVENT = 140  # [A] common_event_type.friend_buff
