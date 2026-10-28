"""Weekly wealth snapshots; fixed NPC benchmarks and player-only accounting [B]."""
import copy
import json
from functools import lru_cache
from pathlib import Path
from . import daily, formation


@lru_cache(maxsize=1)
def rules():
    r = json.loads((Path(__file__).resolve().parents[1] / 'server_config/wealth_rules.json').read_text())
    formation.require(r['mode'] == 'inferred' and r['timezone_offset_hours'] == 8, '财富榜周期配置无效')
    for key in ('vip_points', 'donation_money_per_point', 'normal_gift_points', 'advanced_gift_points'):
        formation.require(type(r[key]) is int and 0 < r[key] <= 100000, '财富榜评分配置无效')
    identities = set()
    for row in r['npcs']:
        formation.require(type(row['id']) is int and row['id'] > 0 and row['id'] not in identities and bool(row['name']), '财富榜NPC配置无效')
        identities.add(row['id'])
        for key in ('vip_level', 'donation_money', 'normal_gift', 'advanced_gift'):
            formation.require(type(row[key]) is int and 0 <= row[key] <= 1000000, '财富榜NPC评分无效')
    formation.require(bool(identities), '财富榜NPC缺失')
    return r


def scored(row, r):
    row = copy.deepcopy(row)
    row['fortune'] = (row['vip_level'] * r['vip_points']
                      + row['donation_money'] // r['donation_money_per_point']
                      + row['normal_gift'] * r['normal_gift_points']
                      + row['advanced_gift'] * r['advanced_gift_points'])
    # Native column retained in the protocol; its client caption is now 捐赠资金.
    row['contribute'] = row['donation_money']
    return row


def ordered(rows):
    rows = sorted(rows, key=lambda v: (-v['fortune'], -v['vip_level'], -v['donation_money'],
                                     -v['advanced_gift'], -v['normal_gift'], v['id']))
    for rank, row in enumerate(rows, 1):
        row['rank'] = rank
    return rows


def player(role):
    from .monument import avatar
    return dict(id=int(role['role_id']), name=role['role_name'], vip_level=int(role.get('vip_level', 0)),
                donation_money=0, normal_gift=0, advanced_gift=0, **avatar(role))


def prepare(role, now):
    r = rules(); week = daily.week(now, r)
    s = role.get('monument_wealth')
    if s is None:
        current = player(role)
        # Only identifiable current-week gifts and today's paid donations survive
        # migration. Total guild contribution also includes unrelated activities.
        gstate = role.get('guild', {})
        if gstate.get('day') == daily.day(now, r):
            from . import guild
            current['donation_money'] = gstate.get('donations', 0) * guild.load_rules()['donate_money_rate']
        for g in gstate.get('unions', {}).values():
            f = g.get('feast', {})
            if f.get('week', (f.get('day', -10) + 3) // 7) != week:
                continue
            for row in f.get('stats', {}).values():
                if row['id'] == current['id']:
                    for key in ('normal_gift', 'advanced_gift'):
                        current[key] += row.get(key, 0)
        npcs = [scored(row, r) for row in r['npcs']]
        s = role['monument_wealth'] = dict(version=1, week=week, current=current,
                                          npcs=npcs, published=ordered(copy.deepcopy(npcs)), settled_week=None)
    if week > s['week']:
        s['published'] = ordered(copy.deepcopy(s['npcs']) + [scored(s['current'], r)])
        s['settled_week'] = s['week']
        s['settled_at'] = ((s['week'] + 1) * 7 - 3) * 86400 - 8 * 3600
        # No artificial empty weeks during a long absence; preserve the last
        # played week's result and start a fresh ledger on return.
        s['week'] = week
        s['current'] = player(role)
    # Observe VIP changes only after settling the old week; an upgrade on Monday
    # cannot retroactively raise Sunday's result. Backward clocks never reopen it.
    from .monument import avatar
    s['current'].update(name=role['role_name'], vip_level=int(role.get('vip_level', 0)), **avatar(role))
    return s


def record(role, now, *, donation_money=0, normal_gift=0, advanced_gift=0):
    s = prepare(role, now)
    for key, count in (('donation_money', donation_money), ('normal_gift', normal_gift), ('advanced_gift', advanced_gift)):
        s['current'][key] += count


def ranking(role, now):
    s = prepare(role, now)
    rows = copy.deepcopy(s['published'])
    return dict(query_type=15, fortune_info=rows,
                order=next((v['rank'] for v in rows if v['id'] == role['role_id']), 0),
                wealth_weekly=True, settled_week=s['settled_week'] if s['settled_week'] is not None else -1,
                next_settlement=((s['week'] + 1) * 7 - 3) * 86400 - 8 * 3600,
                current_score=scored(s['current'], rules())['fortune'])
