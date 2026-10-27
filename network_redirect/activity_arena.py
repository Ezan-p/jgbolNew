"""太虚血战: original arenaUI/event 199 contract, local NPC tournament.

A session advances explicitly through qualification, practice and three blood
stages. NPC identities and combat builds come from players/catalog.json.
"""
import copy
import hashlib
from . import activity as a, activity_undergo as undergo, activity_rank, npc_players, journey, summon
from .protocol import encode, decode

STAGES = {1: '冲榜赛', 2: '练习赛', 3: '血战第一阶段', 4: '血战第二阶段', 5: '血战第三阶段', 6: '本届已结算'}
FIRST_GROUP = 4  # Preserve native group IDs and existing 50+ season rosters.


def rules():
    return undergo.rules()


def group_for(level):
    return next(i for i, bounds in enumerate(rules()['arena_groups'], FIRST_GROUP) if bounds[0] <= level <= bounds[1])


def select_roster(group, day):
    a.require(FIRST_GROUP <= group < FIRST_GROUP+len(rules()['arena_groups']), '血战分组无效')
    lo, hi = rules()['arena_groups'][group-FIRST_GROUP]
    pool = [e for e in npc_players.catalog().values() if lo <= e['profile']['level'] <= hi]
    a.require(len(pool) >= rules()['arena_size']-1, '本地NPC库不足以组成血战分组')
    # Stratify by power, so each bracket includes attainable and aspirational opponents.
    pool.sort(key=lambda e: (e['profile']['role_combat_power'], e['npc_id']))
    count = rules()['arena_size']-1; result = []
    for i in range(count):
        band = pool[i*len(pool)//count:(i+1)*len(pool)//count]
        chosen = min(band, key=lambda e: hashlib.sha256(f"{day}:{group}:{e['npc_id']}".encode()).digest())
        result.append(chosen['npc_id'])
    return result


def new_season(role, day, now):
    group = group_for(role['level'])
    s = dict(version=2, day=day, clock=now, group=group, viewing=group, stage=1,
             stage_fights=0, fights=0, paid=0, actions=rules()['arena_action_points'],
             records=[], replays={}, settled=False, qualification_claimed=[], competitors={})
    for i, key in enumerate(reversed(select_roster(group, day))):
        s['competitors'][key] = dict(score=(rules()['arena_size']-i)*100, hp=rules()['arena_hp_base'])
    s['competitors']['self'] = dict(score=0, hp=rules()['arena_hp_base'])
    return s


def state(role, now, arules):
    a.require(role['level'] >= rules()['arena_level'], f"血战需{rules()['arena_level']}级")
    s = role['activity'].get('arena')
    day = a.day(now, arules)
    if s:
        a.require(now >= s['clock'], '本地时间早于血战存档时间，请恢复时钟后重试')
        # Old low-level seasons remain playable after reaching the entry level.
        # Keep all progress/rewards/opponents; only relocate the removed group.
        if s['group'] < FIRST_GROUP:
            s['group'] = group_for(role['level'])
        if s['viewing'] < FIRST_GROUP:
            s['viewing'] = s['group']
        s['version'] = 2
    if s is None or s['settled'] and day > s['day']:
        s = new_season(role, day, now)
        role['activity']['arena'] = s
    s['clock'] = now
    return s


def rank_type(s):
    return min(3, s['stage'])


def ranking(s):
    return sorted(s['competitors'], key=lambda k: (-s['competitors'][k]['hp'] if s['stage'] >= 3 else 0,
                                                  -s['competitors'][k]['score'], k))


def row(role, key, progress, order):
    if key == 'self':
        p = role
        c = next((c for c in role['corteges'] if c.get('order') == 1), role['corteges'][0])
        tid, layer = c['type'], c.get('reborn_layer', 0)
    else:
        entry = npc_players.catalog()[key]; p = entry['profile']
        n = npc_players.source_file(entry['source_file'])[key]['role']
        c = next(c for c in n['corteges'] if c.get('order') == 1)
        tid, layer = c['type'], c.get('reborn_layer', 0)
    return dict(obj_type=1, obj_id=p['role_id'], name=p['role_name'], level=p['level'],
                head_type=p.get('head_type', 101), vip_level=p.get('vip_level', 0),
                cortege_type=tid, cortege_layer=layer, inherit_level=p.get('reborn_layer', 0),
                tao_point=p.get('tao_point', 0), role_combat_power=p.get('role_combat_power', 0),
                area_name='', order=order, hp_point=progress['hp'], score=progress['score'], is_me=key == 'self')


def prize_specs(prize):
    # User-requested ranking rewards; leave the original CSV and first-win crystals intact.
    return [[11, 0, prize['gold'], 1], [5, 1343, prize['holy_peach'], 1]]


def prize_info():
    return [dict(front=p['front'], back=p['back'], min=p['front'], max=p['back'],
                 prize_list=[a.prize_spec(spec) for spec in prize_specs(p)])
            for p in rules()['arena_rank_prizes']]


def schedule(now, stage):
    # Native views need timestamps. This is a local, explicitly advanced schedule;
    # never advertise fictitious remote players or depend on weekly wall time.
    current = min(stage, 3)
    periods = [dict(start_time=now+(i-current)*86400-1,
                    end_time=now+(i-current+1)*86400-1) for i in range(1, 4)]
    grade = max(1, min(3, stage-2))
    blood = [dict(start_time=now+(i-grade)*86400-1, end_time=now+(i-grade+1)*86400-1)
             for i in range(1, 4)]
    return dict(match_time_list=periods,
                grade_time_list={1: [dict(periods[0])], 2: [dict(periods[1])], 3: blood})


def entry(role, s, now):
    return dict(id=1, role_group=s['group'], group_type_level={i: dict(index=i, min_level=b[0], max_level=b[1],
                inherit_level=0, pick_num=rules()['arena_qualify_count']) for i, b in enumerate(rules()['arena_groups'], FIRST_GROUP)},
                schedule_list=schedule(now, s['stage']), offline=True)


def board(role, s, op=2):
    own = s['viewing'] == s['group']
    if own:
        rows = [row(role, k, s['competitors'][k], i) for i, k in enumerate(ranking(s), 1)]
    else:
        rows = [row(role, k, dict(hp=rules()['arena_hp_base'], score=(rules()['arena_size']-i)*100), i)
                for i, k in enumerate(reversed(select_roster(s['viewing'], s['day'])), 1)]
    limit = rules()['arena_practice_fights' if s['stage'] == 2 else 'arena_qualify_fights']
    remaining = max(0, limit-s['stage_fights'])
    return dict(id=op, enter_group=s['viewing'], rank_type=rank_type(s), rank_data=rows,
                rank_prize_info={i: prize_info() for i in range(1, 4)},
                event_info=dict(in_rank=own and not s['settled'], cur_fight_count=remaining,
                    buy_fight_challenge=rules()['arena_paid_gold'], solo_bet_fight=0, enhance_may_add=0,
                    solo_rank_last_half=0, action_point=s['actions'], buy_action_point=rules()['arena_paid_gold'],
                    fight_records=copy.deepcopy(list(reversed(s['records'])))),
                local_arena=dict(stage=s['stage'], title=STAGES[s['stage']], own=own,
                    can_advance=own and not s['settled'] and (s['stage_fights'] > 0 or s['competitors']['self']['hp'] <= 0),
                    stage_fights=s['stage_fights'], action_cost=rules()['arena_action_cost'], paid_left=max(0, rules()['arena_paid_limit']-s['paid']),
                    settled=s['settled'], settlement=s.get('settlement', {})), reward_score=0)


def response(data):
    return summon.event(199, data)


def resolve_target(role, s, data):
    ident = data.get('des_id')
    a.require(type(ident) in (int, float) and ident == int(ident), '血战对手编号无效')
    key = npc_players.resolve(ident)
    a.require(key in s['competitors'] and key != 'self', '血战对手不在本届参赛名单')
    return key


def settle_prizes(role, s):
    a.require(not s['settled'], '本届血战已经结算')
    order = ranking(s).index('self')+1
    prize = next((p for p in rules()['arena_rank_prizes'] if p['front'] <= order <= p['back']), None)
    gain = []
    reputation = prize['reputation'] if prize else 0
    if prize:
        for spec in prize_specs(prize):
            gain.append(journey.grant(role, spec))
    # No unverified role property is written: local blood-reputation is persisted
    # as an activity statistic and shown on the settlement screen.
    s['reputation'] = s.get('reputation', 0)+reputation
    s.update(settled=True, stage=6, settlement=dict(order=order, reputation=reputation, attach_list=gain))
    return gain


def advance(role, s):
    a.require(s['viewing'] == s['group'] and not s['settled'], '只能推进自己分组的未结束赛程')
    a.require(s['stage_fights'] > 0 or s['competitors']['self']['hp'] <= 0, '本阶段至少完成一场战斗后再推进')
    if s['stage'] == 5:
        return settle_prizes(role, s)
    if s['stage'] == 1:
        order = ranking(s).index('self')+1
        if order > rules()['arena_qualify_count']:
            return settle_prizes(role, s)
        for i, key in enumerate(ranking(s), 1):
            s['competitors'][key]['hp'] = rules()['arena_hp_base']+(rules()['arena_size']-i)*rules()['arena_hp_rank_step']
    # Resolve one deterministic round among NPCs at each explicit transition.
    # These do not mutate source NPC builds or attack an absent player.
    if s['stage'] >= 3:
        keys = [k for k in ranking(s) if k != 'self' and s['competitors'][k]['hp'] > 0]
        for k1, k2 in zip(keys[::2], keys[1::2]):
            p1 = npc_players.catalog()[k1]['profile']['role_combat_power']
            p2 = npc_players.catalog()[k2]['profile']['role_combat_power']
            winner, loser = (k1, k2) if p1 >= p2 else (k2, k1)
            s['competitors'][winner]['score'] += rules()['arena_win_score']
            s['competitors'][loser]['hp'] = max(0, s['competitors'][loser]['hp']-rules()['arena_hp_damage'])
    s.update(stage=s['stage']+1, stage_fights=0, actions=rules()['arena_action_points'])
    return []


def fight(role, s, data, now, jrules):
    a.require(s['viewing'] == s['group'] and not s['settled'], '请进入自己的血战分组')
    a.require(type(data.get('fight_type')) is int and data['fight_type'] == rank_type(s), '赛程已变化，请刷新血战')
    a.require(data.get('des_type') == 1, '血战目标类型无效')
    a.require(data.get('bet_fight', 0) in (0, False), '离线血战不开放赌斗')
    key = resolve_target(role, s, data); positions = ranking(s)
    target_order = positions.index(key)+1; self_order = positions.index('self')+1
    a.require(type(data.get('des_order')) is int and data['des_order'] == target_order, '对手排名已变化，请刷新')
    a.require(target_order <= ((self_order+4)//5)*5, '请选择当前可挑战范围内的对手')
    mine = s['competitors']['self']; enemy = s['competitors'][key]
    a.require(s['stage'] < 3 or mine['hp'] > 0 and enemy['hp'] > 0, '参赛者血量已耗尽，请推进赛程')
    a.require(any(1 <= c.get('order', 0) <= 8 for c in role['corteges']), '请先上阵神仙')
    paid = data.get('is_charge', 0)
    a.require(type(paid) in (int, bool) and paid in (0, 1), '付费挑战参数无效')
    if s['stage'] == 1:
        available = s['stage_fights'] < rules()['arena_qualify_fights']
    elif s['stage'] == 2:
        available = s['stage_fights'] < rules()['arena_practice_fights']
    else:
        available = s['actions'] >= rules()['arena_action_cost']
    a.require(available or paid and s['paid'] < rules()['arena_paid_limit'], '本阶段次数不足，请推进赛程或使用付费挑战')
    if not available:
        a.spend(role, 'gold_coin', rules()['arena_paid_gold']); s['paid'] += 1
    elif s['stage'] >= 3:
        s['actions'] -= rules()['arena_action_cost']
    npc = npc_players.get(key)
    result, lineup, actions = journey.battle(role, {}, jrules, units=(activity_rank.units(role), activity_rank.units(npc['role'])))
    win = 1 <= result <= 3
    gain = []; reward_score = 0
    if s['stage'] == 1 and win:
        mine['score'] = max(mine['score']+rules()['arena_win_score'], enemy['score']+1)
        if key not in s['qualification_claimed']:
            gain = [journey.grant(role, [5, 1366, rules()['arena_qualify_prize_crystals'], 1])]
            s['qualification_claimed'].append(key)
    elif s['stage'] >= 3:
        if win:
            reward_score = rules()['arena_win_score']; mine['score'] += reward_score
            enemy['hp'] = max(0, enemy['hp']-rules()['arena_hp_damage'])
        elif s['stage'] == 5:
            mine['hp'] = max(0, mine['hp']-rules()['arena_hp_damage'])
    s['fights'] += 1; s['stage_fights'] += 1
    role['activity']['fight_id'] += 1; fid = role['activity']['fight_id']
    packets = journey.combat_engine.event_packets(actions, fid)+[
        encode(1028, dict(fight_id=fid, first_hand=1, des_name=npc['role']['role_name'], lineup_count=len(lineup), lineup=lineup)),
        encode(1027, dict(fight_id=fid, fight_type=32, final_result=result, fight_round=len(actions), fight_result=actions))]
    log_time = max(now, s['records'][-1]['log_time']+1 if s['records'] else now)
    record = dict(src_name=role['role_name'], des_name=npc['role']['role_name'], src_id=role['role_id'],
                  des_id=npc['role']['role_id'], final_result=result, log_time=log_time, match_type=rank_type(s), fight_id=fid)
    s['records'] = (s['records']+[record])[-rules()['arena_records']:]
    # Event 121 mixes numeric effect indices with "fight_id" on the wire.
    # Persist string keys like JSON does, so formation.prepare's sorted save
    # comparison can handle battles with effects before the first DB write.
    # replay_packets restores numeric indices for the native Lua client.
    saved_effects = {str(k): v for k, v in journey.combat_engine.event_data(actions, fid).items()}
    s['replays'][str(fid)] = dict(line_up_msg=decode(packets[-2])[2], fight_result_msg=decode(packets[-1])[2],
                                  fight_events=saved_effects)
    keep = {str(r['fight_id']) for r in s['records']}
    s['replays'] = {k: v for k, v in s['replays'].items() if k in keep}
    out = board(role, s, 5); out['reward_score'] = reward_score
    out['event_info']['reward_score'] = reward_score
    return packets+[response(out), summon.event(44, dict(fight_id=fid, fight_type=32,
                     rewards=gain, attach_list=gain, send_prize_list=gain, role_add_exp=0, exp_list={}, silver_coin=0))]


def replay(role, data):
    s = role['activity'].get('arena', {})
    record = next((r for r in s.get('records', []) if r['log_time'] == data.get('log_time')
                   and r['src_id'] == data.get('src_id') and r['match_type'] == data.get('match_type')), None)
    a.require(record is not None, '血战战报不存在或已过期')
    saved = s['replays'][str(record['fight_id'])]
    return activity_rank.replay_packets(saved)+[response(board(role, s, 5)),
        summon.event(44, dict(fight_id=record['fight_id'], fight_type=32, rewards=[], attach_list=[],
                             send_prize_list=[], role_add_exp=0, exp_list={}, silver_coin=0))]


def settle(role, req, now, arules, jrules, parse):
    data = parse(req['data']) if req['data'] else {}
    a.require(isinstance(data, dict), '血战参数无效')
    s = state(role, now, arules); op = req['id']
    if op == 1:
        return [response(entry(role, s, now))]
    if op in (2, 3):
        group = data.get('enter_group', s['group'])
        a.require(type(group) is int and FIRST_GROUP <= group < FIRST_GROUP+len(rules()['arena_groups']), '血战分组无效')
        s['viewing'] = group
        return [response(board(role, s, op))]
    if op == 4:
        ident = data.get('des_id'); key = npc_players.resolve(ident)
        allowed = set(s['competitors']) if s['viewing'] == s['group'] else set(select_roster(s['viewing'], s['day']))
        a.require(key in allowed, '玩家不在当前血战分组')
        return [npc_players.inspection(key)]
    if op == 5:
        return fight(role, s, data, now, jrules)
    if op == 7:
        a.require(type(data.get('stage')) is int and data['stage'] == s['stage'], '赛程已变化，请刷新')
        gain = advance(role, s)
        out = board(role, s)
        out['local_entry'] = entry(role, s, now)
        # Display only the rewards from this settlement, never historical prizes
        # on ordinary board refreshes or replay returns. Event 33 keeps bag sync.
        if gain:
            out['local_prizes'] = gain
        return [response(out)]+([summon.event(33, gain)] if gain else [])
    a.require(False, '血战操作无效')
