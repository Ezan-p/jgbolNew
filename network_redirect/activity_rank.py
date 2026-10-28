"""封神榜: original wire/CSV rules [A], isolated NPC ladder policy [B]."""
import copy
import json
import secrets
from functools import lru_cache
from pathlib import Path
from . import formation, summon, journey, combat, combat_power, reborn_stars, cheer
from . import battle_replay
from .protocol import encode, decode

ROOT = Path(__file__).resolve().parents[1]
require = formation.require
SCORE = summon.rows('top_score.csv')


@lru_cache(maxsize=1)
def rules():
    r = json.loads((ROOT/'server_config/rank_rules.json').read_text())
    require(r['mode'] == 'inferred' and 10 <= r['size'] <= 20000, '封神榜配置无效')
    require(1 <= r['offline_days'] <= 30 and 1 <= r['records'] <= 20, '封神榜存储上限无效')
    require(r['tick_seconds'] == 86400 and r['token_chances'] == 3, '封神榜每日结算或令牌配置无效')
    require(0 < r['max_extra_chances'] <= 65500, '封神榜额外次数无效')
    require(bool(r['cards']), '封神榜奖池为空')
    for row in r['cards']:
        require(len(row) == 5 and all(type(x) is int and x >= 0 for x in row), '封神榜奖池无效')
        require(row[0] == 5 and row[1] in formation.ITEMS and row[2] > 0 and row[3] == 1 and row[4] > 0, '封神榜奖励无效')
    return r


# Keep extracted original CSVs intact; UI and server share the configured rules.
EXCHANGE = {v['index']: dict(score=v['score'], promote_order=v['promote_order'],
    **{'prize_list(object_type|sub_type|count/...)': '|'.join(map(str,v['prize']))})
    for v in rules()['exchanges']}


def client_source():
    exchange = [dict(score=v['score'], promoteOrder=v['promote_order'],
        object_type=v['prize'][0], sub_type=v['prize'][1], count=v['prize'][2])
        for v in rules()['exchanges']]
    scores = [dict(upper=int(v['begin']), lower=int(v['end']), score=int(v['day_score'])) for v in SCORE]
    return Path(__file__).with_name('rank_client.lua').read_text().replace(
        '__RANK_EXCHANGES__', summon.lua(exchange)).replace('__RANK_DAILY_SCORES__', summon.lua(scores))


@lru_cache(maxsize=1)
def catalog():
    data = json.loads((ROOT/'analysis/npc_design/v1/catalog.json').read_text())
    candidates = []
    for npc in data['npcs']:
        if npc['role']['level'] < 5 or npc['battle_validation']['status'] == 'replay_limit_observed':
            continue
        from . import npc_players
        npc = npc_players.decorate(npc)
        combat_power.recalculate(npc['role'], formation.load_rules())
        candidates.append(npc)
    require(len(candidates) >= rules()['size'] - 1, '封神榜NPC库数量不足')
    candidates.sort(key=lambda n: (-n['role']['role_combat_power'], n['npc_id']))
    # Equally spaced absolute-power samples: permanent opponents, no player scaling.
    size = rules()['size']
    ladder = {930000+i: candidates[(i-1)*(len(candidates)-1)//(size-2)] for i in range(1, size)}
    # Keep permanent scene IDs (and saved swaps) intact; only replace five templates.
    elite_keys = rules().get('elite_npcs', [])
    if elite_keys:
        require(len(elite_keys) == 5 and len(set(elite_keys)) == 5, '封神榜前五配置无效')
        elites = npc_players.source_file(rules()['elite_catalog'])
        for order, key in enumerate(elite_keys, 1):
            require(key in elites, '封神榜前五模板不存在')
            npc = npc_players.decorate(elites[key])
            require(npc['battle_validation']['status'] != 'replay_limit_observed', '封神榜前五模板回放风险')
            combat_power.recalculate(npc['role'], formation.load_rules())
            require(npc['role']['role_combat_power'] > ladder[930000+order]['role']['role_combat_power'],
                    '封神榜前五战力须高于原模板')
            ladder[930000+order] = npc
        powers = [n['role']['role_combat_power'] for n in ladder.values()]
        require(powers == sorted(powers, reverse=True), '封神榜战力顺序无效')
        require(len({n['npc_id'] for n in ladder.values()}) == len(ladder), '封神榜模板重复')
    return ladder


def score(order, column='score'):
    return next(int(v[column]) for v in SCORE if int(v['begin']) <= order <= int(v['end']))


def masks(s):
    eligible = sum(1 << (i-2) for i,v in EXCHANGE.items() if int(v['promote_order']) and s.get('rank_reached_order', 20001) <= int(v['promote_order']))
    claimed = sum(1 << (i-2) for i in s.get('rank_promotions', []) if i in EXCHANGE and int(EXCHANGE[i]['promote_order']))
    return eligible, claimed


def prepare(role, now, arules):
    s = role['activity']; r = rules(); day = (now+arules['timezone_offset_hours']*3600)//86400
    if 'rank_version' not in s:
        order = max(1, min(r['size'], s['rank_order']))
        # Preserve old rank, currency, claims and daily usage on migration.
        s.update(rank_version=1, rank_order=order, rank_clock=now, rank_day=day,
                 rank_day_best=order, rank_previous_best=0, rank_pending_score=0,
                 rank_extra=0, rank_origin_order=order, rank_slots={}, rank_records=[], rank_defence_day=day)
    if s.get('rank_reward_version', 1) < 2:
        # Preserve claims by rank threshold, never by the newly reordered row ID.
        old_to_new = {6: 4, 7: 5, 8: 9, 9: 10}
        s['rank_promotions'] = sorted({old_to_new[i] for i in s.get('rank_promotions', []) if i in old_to_new})
        # A pending legacy daily award is credited once during migration.
        s['rank_score'] = min(16777215, s['rank_score'] + s.get('rank_pending_score', 0))
        s.update(rank_reward_version=2, rank_pending_score=0)
    old_day = s['rank_day']
    if day > old_day:
        elapsed = day-old_day
        s['rank_previous_best'] = s['rank_day_best'] if elapsed == 1 else s['rank_order']
        if role['level'] >= 6:
            days = min(elapsed, r['offline_days'])
            first_order = s['rank_day_best'] if elapsed <= r['offline_days'] else s['rank_order']
            gain = score(first_order, 'day_score') + (days-1)*score(s['rank_order'], 'day_score')
            s['rank_score'] = min(16777215, s['rank_score']+gain)
            role['top_day_prize_time'] = day*86400-arules['timezone_offset_hours']*3600
        s.update(rank_day=day, rank_day_best=s['rank_order'], rank_extra=0)
    s.update(rank_pending_score=0, rank_claimed=True)
    s['rank_clock'] = max(now, s['rank_clock'])
    role.update(top_order=s['rank_order'], top_score=s['rank_score'], top_fight_count=s['rank_count'],
                top_fight_count_plus=s['rank_extra'], top_first_promote_time=masks(s)[0], top_first_promote_prize=masks(s)[1])
    return s


def identity(s, order):
    if order == s['rank_order']:
        return None
    return s['rank_slots'].get(str(order), 930000+order if order < rules()['size'] else 930000+s.get('rank_origin_order', rules()['size']-1))


def swap(s, target):
    old = s['rank_order']; npc_id = identity(s, target)
    s['rank_slots'][str(old)] = npc_id
    s['rank_slots'].pop(str(target), None)
    s['rank_order'] = target


def opponent(s, order):
    ident = identity(s, order); npc = catalog()[ident]; role = npc['role']
    head = next(c for c in role['corteges'] if c['order'] == 1)
    return dict(id=ident, type=2, order=order, level=role['level'], name=role['role_name'],
                cortege=head['type'], cortege_layer=head.get('evolve_level', 0), combat_power=role['role_combat_power'])


def challenge_orders(s):
    order = s['rank_order']; size = rules()['size']
    orders = {max(1, order-v) for v in (1, 2, 5, 10, 20)} - {order}
    # Top ranks can keep playing and earning daily participation rewards.
    for lower in range(order+1, min(size, order+5)+1):
        if len(orders) < 5: orders.add(lower)
    revenge = s.get('rank_revenge')
    if revenge:
        orders.update(o for o in range(1, size+1) if identity(s, o) == revenge)
    return orders


def board(role):
    s = role['activity']; orders = challenge_orders(s)
    rows = []
    for order in sorted(orders | set(range(1, 11))):
        if order == s['rank_order']:
            c = next((c for c in role['corteges'] if c.get('order') == 1),next(iter(role['corteges']), {'type': 4061}))
            rows.append(dict(id=role['role_id'], type=1, order=order, name=role['role_name'], level=role['level'], cortege=c['type'], cortege_layer=c.get('evolve_level',0), top_relation=1))
        else:
            row = opponent(s, order)
            row.update(top_relation=3 if row['id'] == s.get('rank_revenge') else 2 if order in orders else 1)
            rows.append(row)
    eligible, claimed = masks(s)
    return encode(1022, dict(need_update=True, self_order=s['rank_order'], self_score=s['rank_score'], promote_time=eligible,
                            promote_prize=claimed, fight_count=max(0, role['top_fight_limit']+s['rank_extra']-s['rank_count']), show_count=len(rows), show_list=rows))


def client_state(role):
    s = role['activity']
    return summon.event(80, dict(local_rank=dict(previous_best=s['rank_previous_best'], pending_score=s['rank_pending_score'],
        current_order=s['rank_order'], score=s['rank_score'],
        promote_time=masks(s)[0], promote_prize=masks(s)[1])))


def units(role):
    from .combat_loadout import player_units
    return player_units(role)


def inspection(role, ident):
    require(ident in catalog(), '封神榜NPC不存在')
    npc = catalog()[ident]['role']; s = role['activity']
    order = next((o for o in range(1, rules()['size']+1) if identity(s,o) == ident), None)
    require(order is not None, '封神榜对手已变化')
    from . import npc_players
    return summon.event(11, npc_players.inspection_data(catalog()[ident], scene_id=ident))


def simulate(role, order, now, jrules, defence=False):
    s = role['activity']; target = opponent(s, order); npc = catalog()[target['id']]['role']
    result, lineup, actions = journey.battle(role, {}, jrules, units=(units(role), units(npc)))
    win = 1 <= result <= 3
    s['fight_id'] += 1; fid = s['fight_id']; old = s['rank_order']
    if (win and order < old) or (result >= 4 and order > old): swap(s, order)
    if win:
        s['rank_reached_order'] = min(s.get('rank_reached_order', 20001), s['rank_order'])
        if s.get('rank_revenge') == target['id']: s.pop('rank_revenge')
    elif defence and result >= 4: s['rank_revenge'] = target['id']
    s['rank_day_best'] = min(s['rank_day_best'], s['rank_order'])
    replay = dict(fight_id=fid, time=now, name=target['name'], src_name=role['role_name'], vip_level=role.get('vip_level',0), tao_point=role.get('tao_point',0),
                  role_combat_power=role.get('role_combat_power',0), target_id=target['id'], target_power=target['combat_power'], defence=defence,
                  old_order=old, new_order=s['rank_order'], stop_reason=getattr(actions,'stop_reason','elimination'),
                  fight_events=journey.combat_engine.event_data(actions,fid),
                  line_up_msg=decode(encode(1028,dict(fight_id=fid,first_hand=1,des_name=target['name'],lineup_count=len(lineup),lineup=lineup)))[2],
                  fight_result_msg=battle_replay.result_message(dict(fight_id=fid,fight_type=2,final_result=result,fight_round=len(actions),fight_result=actions)))
    # Check the complete effect packet before committing any cost or rank swap.
    from .battle_replay import effect_packets
    effect_packets(replay['fight_events'])
    s['rank_records'] = (s['rank_records']+[replay])[-rules()['records']:]
    return win, replay


def replay_packets(record):
    from .battle_replay import effect_packets
    effects = {int(k) if str(k).isdigit() else k:v for k,v in record['fight_events'].items()}
    return effect_packets(effects)+[encode(1028, record['line_up_msg']), *battle_replay.result_packets(1027, record['fight_result_msg'])]


def battle(role, req, now, arules, jrules):
    from . import activity as a
    s = role['activity']; target = req['des_value']
    require(role['level'] >= 6, '封神榜需6级')
    require(target in challenge_orders(s) and req['des_type'] == 2 and req['des_id'] == identity(s,target), '封神榜对手已变化，请刷新')
    require(s['rank_count'] < role['top_fight_limit']+s['rank_extra'], '今日封神榜次数已用完')
    require(any(c.get('order') for c in role['corteges']), '请先上阵神仙')
    a.spend(role,'energy',1); s['rank_count'] += 1; role['top_fight_time'] = now
    win, replay = simulate(role, target, now, jrules)
    from . import progression, formation
    xp = int(formation.LEVELS[role['level']]['energy_win_exp' if win else 'energy_lose_exp'])
    progression.add_exp(role, xp, now)
    rewards = []
    if win:
        gain = score(s['rank_order']); s['rank_score'] = min(16777215, s['rank_score']+gain)
        cards = rules()['cards']; roll = secrets.randbelow(sum(v[4] for v in cards)); chosen = cards[-1]
        for card in cards:
            if roll < card[4]: chosen = card; break
            roll -= card[4]
        journey.grant(role,chosen[:4]); role['silver_coin'] += arules['battle_silver']
        # Original rankUI flips exactly five cards; flag marks the ONE award.
        rewards = [dict(a.prize_spec(v[:4]),flag=i==0) for i,v in enumerate([chosen]+[cards[(cards.index(chosen)+i)%len(cards)] for i in range(1,5)])]
    prepare(role,now,arules)
    return replay_packets(replay)+[summon.event(45,dict(fight_id=replay['fight_id'],obj_type=1,exp_plus=xp)),client_state(role),board(role)]+([summon.event(33,rewards)] if win else [])+[summon.event(44,dict(fight_id=replay['fight_id'],fight_type=2))]


def settle(role, mid, req, now, arules, jrules):
    from . import activity as a
    s = role['activity']; require(role['level'] >= 6, '封神榜需6级')
    if mid == 1021:
        require(req['flag'] in (0,1), '封神榜查询无效')
        # One local defensive encounter on the first visit of a new day, never
        # replay every missed day or charge stamina for an offline NPC attack.
        if s['rank_defence_day'] < s['rank_day']:
            s['rank_defence_day'] = s['rank_day']
            if s['rank_order'] < rules()['size'] and s.get('rank_reached_order'):
                simulate(role, min(rules()['size'],s['rank_order']+1),now,jrules,True)
        prepare(role,now,arules)
        return [client_state(role),board(role)]
    if mid == 1026: return battle(role,req,now,arules,jrules)
    if mid == 1244:
        from .monument import record_packets
        from .guild_combat import recent_records
        meta=[]
        for v in recent_records(s['rank_records']):
            result=v['fight_result_msg']['final_result']
            label=('守' if v['defence'] else '攻')+('胜' if 1<=result<=3 else '败' if result>=4 else '平')+'·'+v['name'].removeprefix('离线·')
            meta.append(dict(label=label,power=v.get('target_power',0)))
        return [summon.event(80,dict(local_rank_records=meta))]+record_packets(dict(records=s['rank_records']))[:-1]+[
                summon.event(80,dict(local_rank_show_records=True))]
    if mid == 1051:
        n = req['item_count'] or 1
        require(type(n) is int and 1 <= n <= 100 and req['des_type'] in (0,1) and req['des_id'] in (0,role['role_id']), '封神令牌使用参数无效')
        require(req['item_id'] == 0 or any(i['id']==req['item_id'] and i['type_id']==1021 and i['attach_type']==5 and i['count']>0 and not i.get('owner_id') and not i.get('equip_pos') and not i.get('is_lock') for i in role['attachments']), '封神令牌不存在')
        gain = rules()['token_chances'] * n
        require(s['rank_extra']+gain <= rules()['max_extra_chances'], '今日额外挑战次数已达上限')
        a.consume(role,1021,n); s['rank_extra'] += gain
        prepare(role,now,arules)
        return [client_state(role),summon.event(21,dict(result=1,type_id=1021,count=n,effect_value=gain))]
    if mid == 1201:
        raise formation.Rejected('排名日积分每日零点自动入账，无需手动领取')
    if mid == 1203:
        cfg = EXCHANGE.get(req['exchange_type']); require(cfg is not None,'积分兑换项目无效')
        cost, promotion = int(cfg['score']), int(cfg['promote_order'])
        require(s['rank_score'] >= cost,'积分不足')
        if promotion:
            claims = s.setdefault('rank_promotions',[])
            require(s.get('rank_reached_order',20001)<=promotion and req['exchange_type'] not in claims,'未达晋升名次或已领取')
            claims.append(req['exchange_type'])
        s['rank_score'] -= cost
        specs = [[int(v) for v in x.split('|')]+[1] for x in cfg['prize_list(object_type|sub_type|count/...)'].split('/')]
        rewards = a.prizes(role,specs)
        prepare(role,now,arules)
        # Refresh the open exchange page in place; 1022 navigates back to the board.
        return [client_state(role),summon.event(36,rewards)]
    raise formation.Rejected('封神榜操作无效')
