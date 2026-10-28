"""太虚幻境: native 1349 contract [A], versioned offline progression [B].

The original protocol names are misleading: mode=1/undergo is 挑战;
mode=2/challenge is the timed 历劫. Keep these wire names for compatibility.
"""
import copy
import hashlib
import json
import math
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from . import activity as a, formation, journey, summon
from . import battle_replay
from .protocol import encode

GATES = {int(x['id']): x for x in summon.rows('undergo_ordeal/tollgate_config.csv')}
MAPS = {int(x['id']): x for x in summon.rows('undergo_ordeal/map_config.csv')}
NPCS = {int(x['编号']): x for x in summon.rows('undergo_ordeal/npc_list.csv')}
END = 1001


@lru_cache(maxsize=1)
def rules():
    r = json.loads((Path(__file__).resolve().parents[1]/'server_config/taixu_rules.json').read_text())
    a.require(r['schema_version'] == 1 and r['mode'] == 'inferred', '太虚配置版本无效')
    for k in ('undergo_level', 'challenge_daily_limit', 'companion_daily_limit', 'ordeal_window_seconds',
              'arena_level', 'arena_size', 'arena_qualify_count', 'arena_qualify_fights',
              'arena_practice_fights', 'arena_action_points', 'arena_action_cost', 'arena_paid_limit',
              'arena_paid_gold', 'arena_hp_base', 'arena_hp_rank_step', 'arena_hp_damage',
              'arena_win_score', 'arena_win_prize_crystals', 'arena_records'):
        a.require(type(r[k]) is int and 0 < r[k] <= 1000000, '太虚数值无效：'+k)
    a.require(r['challenge_daily_limit'] == 10 and r['companion_daily_limit'] == 4
              and r['ordeal_window_seconds'] == 259200, '历劫次数/时限与原客户端不一致')
    a.require(r['challenge_strength'] == 2 and r['ordeal_strength'] == 0, '历劫体力与原客户端不一致')
    a.require(5 <= r['arena_size'] <= 30 and r['arena_qualify_count'] <= r['arena_size']
              and r['arena_records'] <= 20, '血战人数或战报上限无效')
    groups = r['arena_groups']
    a.require(len(groups) == 4 and groups[0][0] == r['arena_level'] == 50 and groups[-1][1] == 99
              and all(len(v) == 2 and all(type(n) is int for n in v) and v[0] <= v[1] for v in groups)
              and all(groups[i][1]+1 == groups[i+1][0] for i in range(len(groups)-1)), '血战等级分组无效')
    prizes = r['arena_rank_prizes']
    a.require(bool(prizes) and prizes[0]['front'] == 1 and prizes[-1]['back'] == r['arena_size']
              and all(all(type(p[k]) is int and 0 < p[k] <= 1000000
                          for k in ('front', 'back', 'gold', 'holy_peach', 'crystals'))
                      and p['front'] <= p['back'] for p in prizes)
              and all(prizes[i]['back']+1 == prizes[i+1]['front'] for i in range(len(prizes)-1)),
              '血战排名奖励无效')
    return r


def response(op, data):
    return encode(1349, dict(id=op, data=summon.lua(data)))


def state(role, now, r):
    s = role['activity'].setdefault('undergo', dict(gate=101, challenge=101, lineup={}, passed=[], day=-1))
    if s.get('version') != 2:
        # Existing saves used mode=1 for first rewards. Never regrant them.
        s.update(version=2, challenge_passed=[], first_claimed=[g for g in s['passed'] if g % 100 == 9],
                 legacy_maps=[m for m in MAPS if all(g in s['passed'] for g in map_gates(m))],
                 top_big_id=max(1, s['challenge']//100), started=0, clock=now)
    a.require(now >= s['clock'], '本地时间早于历劫存档时间，请恢复时钟后重试')
    today = a.day(now, r)
    if today > s['day']:
        # Only the current map's small gates reset; completed maps never disappear.
        s.update(day=today, count=0, used={}, claims=[], purchases={})
        if s['challenge'] != END:
            s['challenge'] = s['challenge']//100*100+1
    if s['started'] and s['challenge'] != END:
        periods = (now-s['started'])//rules()['ordeal_window_seconds']
        if periods:
            mid = max(1, s['challenge']//100-periods)
            s['challenge'] = mid*100+1
            s['started'] += periods*rules()['ordeal_window_seconds']
    s['clock'] = now
    refresh_shop(s, role, r, today)
    owned = {c['id'] for c in role['corteges']}
    s['lineup'] = {str(p): cid for p, cid in s['lineup'].items() if cid in owned and 1 <= int(p) <= 9}
    if not s['lineup']:
        s['lineup'] = {str(c['order']): c['id'] for c in role['corteges'] if 1 <= c.get('order', 0) <= 9}
    return s


def map_gates(mid):
    return sorted(g for g, cfg in GATES.items() if int(cfg['map_id']) == mid)


def day_prize(s):
    cleared = set(s.get('legacy_maps', [])) | {m for m in MAPS if all(g in s['challenge_passed'] for g in map_gates(m))}
    return {mid: dict(has_get=mid in s['claims']) for mid in sorted(cleared)}


def detail(s, **extra):
    challenge = dict(big_id=s['challenge']//100, small_id=s['challenge'] % 100,
                     top_big_id=s['top_big_id'], cortege_list={int(k): v for k, v in s['used'].items()})
    if s['started'] and s['challenge'] != END:
        challenge['last_challenge_time'] = s['started']
    return dict(detail=dict(map_list=dict(
        undergo=dict(big_id=s['gate']//100, small_id=s['gate'] % 100, total_count=s['count']),
        challenge=challenge), cortege_list={int(v): int(k) for k, v in s['lineup'].items()},
        day_prize=day_prize(s)), **extra)


def refresh_shop(s, role, r, today):
    """Persist six distinct daily offers; preserve same-day usage across migration."""
    revision = r['undergo_shop_revision']
    if s.get('shop_day') == today and s.get('shop_revision') == revision:
        return
    # Old saves used four fixed display indices. Convert before reordering.
    if 'shop_revision' not in s:
        s['purchases'] = {str(tid): s.get('purchases', {}).get(str(i), 0)
                          for i, tid in enumerate((1001, 1343, 1034, 1024), 1)}
    seed = f"{revision}:{today}:{role.get('role_id', role.get('id', 0))}"
    catalog = {row['reward'][1]: row for row in r['undergo_shop']}
    current = s.get('shop', [])
    # A same-day balance update changes quotas, not the selected goods/order.
    if (s.get('shop_day') == today and len(current) == r['undergo_shop_daily_count']
            and len({row['reward'][1] for row in current}) == len(current)
            and all(row['reward'][1] in catalog for row in current)):
        offers = [catalog[row['reward'][1]] for row in current]
    else:
        offers = sorted(r['undergo_shop'], key=lambda row: hashlib.sha256(
            f"{seed}:{row['reward'][1]}".encode()).digest())[:r['undergo_shop_daily_count']]
    s.update(shop=copy.deepcopy(offers), shop_day=today, shop_revision=revision,
             shop_token=hashlib.sha256(seed.encode()).hexdigest()[:24])


def shop(s, r):
    return [dict(a.prize_spec(row['reward']), crystals=row['cost'],
                 buy_times=max(0, row['limit']-s['purchases'].get(str(row['reward'][1]), 0)),
                 shop_token=s['shop_token']) for row in s['shop']]


def next_gate(gid):
    nxt = int(GATES[gid]['next_tollgate'])
    if nxt:
        return nxt
    nxt = int(MAPS[int(GATES[gid]['map_id'])]['next_map'])
    return int(MAPS[nxt]['first_tollgate']) if nxt in MAPS else END


def player_units(role, positions):
    from .combat_loadout import equipped_skills
    units = []
    for pos, cid in positions.items():
        c = next(c for c in role['corteges'] if c['id'] == cid)
        unit = dict(companion_id=cid, type=c['type'], order=pos, level=c['level'],
                    evolve=c.get('evolve_level', 0), reborn=c.get('reborn_layer', 0),
                    **{k: max(1, int(c[k])) for k in formation.STATS})
        unit['max_hp'] = unit['hp']
        unit['skills'] = equipped_skills(role, c.get('order'), companion_id=cid)
        units.append(unit)
    return units


def enemy_units(gid):
    from .activity_home import TRAIN
    cfg = GATES[gid]; units = []
    for token in next(v for k, v in cfg.items() if k.startswith('cortege_list(')).split('/'):
        nid, pos = map(int, token.split('|'))
        if not pos:
            continue
        n = NPCS[nid]; sk = int(n['法术ID'] or 0)
        unit = dict(type=int(n['ID']), order=pos, level=int(cfg['level']), evolve=0,
                    reborn=int(n['是否转生'] or 0), gongji=int(n['攻']), fangyu=int(n['防']),
                    hp=int(n['血']), max_hp=int(n['血']), magic=int(n['法']),
                    skills=[(sk, int(cfg['skill_level']))] if sk in formation.SKILLS else [],
                    skill_probabilities={sk: int(n['法术概率'] or 0)})
        unit['training_bonuses'] = [tuple(map(Fraction, TRAIN[i, int(n[key])]['worth'].split('|')))
                                   if int(n[key]) else (0, 0)
                                   for i, key in enumerate(('攻击修炼', '防御修炼', '法术修炼', '法抗修炼'), 1)]
        units.append(unit)
    return units


def settle(role, req, now, r, jrules, frules, parse):
    from . import feature_levels
    feature_levels.check(role, 1349, req)
    data = parse(req['data']) if req['data'] else {}
    a.require(isinstance(data, dict), '历劫参数无效')
    op = req['id']; s = state(role, now, r)
    if op in (1, 6):
        return [response(op, detail(s))]
    if op == 2:
        return [response(2, {})]
    if op == 3:
        s['shop_view_token'] = s['shop_token']
        return [response(3, shop(s, r))]
    if op == 5:
        idx, n = data.get('index'), data.get('count', 1)
        a.require(type(idx) is int and 1 <= idx <= len(s['shop']) and type(n) is int and n > 0, '兑换参数无效')
        # Native clients send indices only; upgraded clients bind the exact view.
        a.require(data.get('shop_token', s.get('shop_view_token')) == s['shop_token'],
                  '幻境商店已刷新，请重新打开商店后兑换')
        row = s['shop'][idx-1]; key = str(row['reward'][1]); used = s['purchases'].get(key, 0)
        a.require(used+n <= row['limit'], '今日兑换次数不足')
        a.consume(role, 1366, row['cost']*n); s['purchases'][key] = used+n
        p = row['reward']; gain = a.prizes(role, [[p[0], p[1], p[2]*n, p[3]]])
        gain[0]['buy_times'] = row['limit']-used-n
        return [response(5, dict(index=idx, attach_list=gain))]
    if op == 7:
        idx = data.get('index')
        a.require(type(idx) is int and (idx == 0 or idx in MAPS), '领奖地图无效')
        ids = [i for i, p in day_prize(s).items() if not p['has_get'] and idx in (0, i)]
        a.require(ids, '尚未通关历劫地图或今日已领取')
        gain = []
        for i in ids:
            gain += journey.drops(role, next(v for k, v in MAPS[i].items() if k.startswith('pass_map_prize')), True)
            s['claims'].append(i)
        return [response(7, dict(day_prize=day_prize(s), attach_list=gain))]
    a.require(op == 4, '历劫操作无效')
    mode, gid, positions = data.get('mode'), data.get('map_id'), data.get('cortege_list')
    a.require(type(mode) is int and mode in (1, 2) and type(gid) is int and gid in GATES, '历劫关卡无效')
    a.require(isinstance(positions, dict) and 1 <= len(positions) <= 9, '历劫阵容无效')
    a.require(all(type(p) is int and 1 <= p <= 9 and type(cid) in (int, float)
                  and math.isfinite(cid) and cid > 0 and cid == int(cid)
                  for cid, p in positions.items()), '历劫阵位或神仙编号无效')
    a.require(len(set(positions.values())) == len(positions), '神仙不能占用相同阵位')
    positions = {p: int(cid) for cid, p in positions.items()}
    ids = list(positions.values())
    a.require(len(set(ids)) == len(ids), '神仙不能重复上阵')
    a.require(set(ids) <= {c['id'] for c in role['corteges']}, '神仙不属于当前角色')
    mid = gid//100
    if mode == 1:
        a.require(gid <= s['gate'] and s['count'] < rules()['challenge_daily_limit'], '关卡未解锁或今日挑战次数已满')
        a.require(mid == 1 or gid in s['passed'] or mid <= s['challenge']//100, '请先通过上一大关历劫')
    else:
        a.require(gid == s['challenge'] and all(g in s['passed'] for g in map_gates(mid)), '请先通关本大关挑战，并按顺序历劫')
        a.require(all(s['used'].get(str(cid), 0) < rules()['companion_daily_limit'] for cid in ids), '神仙今日历劫次数已满')
    cfg = GATES[gid]
    a.require(role['level'] >= int(cfg['require_level']), '历劫等级不足')
    cost = rules()['challenge_strength' if mode == 1 else 'ordeal_strength']
    a.spend(role, 'strength', cost)
    result, lineup, actions = journey.battle(role, cfg, jrules, units=(player_units(role, positions), enemy_units(gid)), slots=9)
    win = 1 <= result <= 3
    s['lineup'] = {str(p): cid for p, cid in positions.items()}
    gain, first = [], []
    if mode == 1:
        s['count'] += 1
    else:
        if not s['started']:
            s['started'] = now
        for cid in ids:
            s['used'][str(cid)] = s['used'].get(str(cid), 0)+1
    if win:
        suffix = '_lijie' if mode == 2 else ''
        gain = journey.drops(role, next(v for k, v in cfg.items() if k.startswith('com_win_prize'+suffix+'(')))
        passed = s['passed' if mode == 1 else 'challenge_passed']
        if gid not in passed:
            passed.append(gid)
        if mode == 2 and gid not in s['first_claimed']:
            first = journey.drops(role, cfg['first_win_prize_lijie(exp_count|rate)'])
            s['first_claimed'].append(gid)
        key = 'gate' if mode == 1 else 'challenge'
        if gid == s[key]:
            s[key] = next_gate(gid)
        if mode == 2:
            s['top_big_id'] = max(s['top_big_id'], s['challenge']//100)
            if s['challenge']//100 != mid:
                s['started'] = 0
    original = {c['id']: c.get('order', 0) for c in role['corteges']}
    try:
        for c in role['corteges']:
            c['order'] = next((p for p, cid in positions.items() if cid == c['id']), 0)
        rewardcfg = dict(cfg, strenth_consume=str(cost))
        if mode == 2:
            rewardcfg.update(exp=cfg['exp_lijie'], money=cfg['money_lijie'])
        xp, exps, money = journey.experience(role, rewardcfg, win, jrules, frules, now=now)
    finally:
        for c in role['corteges']:
            c['order'] = original[c['id']]
    role['activity']['fight_id'] += 1
    fid = role['activity']['fight_id']; ft = 29+mode
    return journey.combat_engine.event_packets(actions, fid)+[
        encode(1141, dict(fight_id=fid, first_hand=1 if not actions or actions[0]['is_src'] else 2,
                         des_name='太虚幻境守卫', lineup_count=len(lineup), lineup=lineup)),
        *battle_replay.result_packets(1140, dict(fight_id=fid, fight_type=ft, final_result=result, fight_round=len(actions), fight_result=actions)),
        response(6, detail(s)), summon.event(44, dict(fight_id=fid, fight_type=ft, role_add_exp=xp,
            exp_list=exps, silver_coin=money, rewards=gain+first, send_prize_list=gain+first,
            attach_list=gain, first_win_prize=first))]
