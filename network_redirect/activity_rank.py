"""封神榜: original wire/CSV rules [A], isolated NPC ladder policy [B]."""
import copy
import json
import secrets
from functools import lru_cache
from pathlib import Path
from . import formation, summon, journey, combat, combat_power, reborn_stars, cheer
from .protocol import encode, decode

ROOT = Path(__file__).resolve().parents[1]
require = formation.require
SCORE = summon.rows('top_score.csv')
EXCHANGE = {int(v['index']): v for v in summon.rows('top_score_exchange.csv')}


@lru_cache(maxsize=1)
def rules():
    r = json.loads((ROOT/'server_config/rank_rules.json').read_text())
    require(r['mode'] == 'inferred' and 10 <= r['size'] <= 20000, '封神榜配置无效')
    require(1 <= r['offline_days'] <= 30 and 1 <= r['records'] <= 20, '封神榜存储上限无效')
    require(r['tick_seconds'] == 1800 and r['token_chances'] == 3, '封神榜原版时间或令牌配置无效')
    require(0 < r['max_extra_chances'] <= 65500, '封神榜额外次数无效')
    require(bool(r['cards']), '封神榜奖池为空')
    for row in r['cards']:
        require(len(row) == 5 and all(type(x) is int and x >= 0 for x in row), '封神榜奖池无效')
        require(row[0] == 5 and row[1] in formation.ITEMS and row[2] > 0 and row[3] == 1 and row[4] > 0, '封神榜奖励无效')
    return r


@lru_cache(maxsize=1)
def catalog():
    data = json.loads((ROOT/'analysis/npc_design/v1/catalog.json').read_text())
    candidates = []
    for npc in data['npcs']:
        if npc['role']['level'] < 5 or npc['battle_validation']['status'] == 'replay_limit_observed':
            continue
        npc = copy.deepcopy(npc)
        combat_power.recalculate(npc['role'], formation.load_rules())
        candidates.append(npc)
    require(len(candidates) >= rules()['size'] - 1, '封神榜NPC库数量不足')
    candidates.sort(key=lambda n: (-n['role']['role_combat_power'], n['npc_id']))
    # Equally spaced absolute-power samples: permanent opponents, no player scaling.
    size = rules()['size']
    return {930000+i: candidates[(i-1)*(len(candidates)-1)//(size-2)] for i in range(1, size)}


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
    s.setdefault('rank_pending_score', 0)
    old_day = s['rank_day']
    if day > old_day:
        s['rank_previous_best'] = s['rank_day_best'] if day == old_day+1 else s['rank_order']
        s['rank_pending_score'] = score(s['rank_previous_best'], 'day_score')
        s.update(rank_day=day, rank_day_best=s['rank_order'], rank_extra=0)
    if role['level'] >= 6 and now >= s['rank_clock']:
        ticks = min((now-s['rank_clock'])//r['tick_seconds'], r['offline_days']*48)
        if ticks:
            s['rank_score'] = min(16777215, s['rank_score'] + ticks*score(s['rank_order']))
            s['rank_clock'] = now-(now-s['rank_clock'])%r['tick_seconds']
    elif role['level'] < 6:
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
    return dict(id=ident, type=2, order=order, level=role['level'], name='离线·'+str(ident-930000)+'·'+{'attack':'强袭','magic':'御法','endurance':'固守'}.get(npc['archetype'], '守阵'),
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
            c = next((c for c in role['corteges'] if c.get('order') == 1),role['corteges'][0])
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
        current_order=s['rank_order'])))


def units(role):
    ours = []
    for c in role['corteges']:
        if not 1 <= c.get('order',0) <= 8: continue
        u = dict(companion_id=c['id'], type=c['type'], order=c['order'], level=c['level'], evolve=c.get('evolve_level',0), reborn=c.get('reborn_layer',0), max_hp=c['hp'], **{k:c[k] for k in formation.STATS})
        u['skills'] = [(i['type_id'], i['level']) for i in role['attachments'] if i['attach_type'] == 6 and i.get('equip_order') == c['order'] and i.get('equip_pos',0)>0]
        ours.append(u)
    combat.attach_essences(role, ours); reborn_stars.attach_combat_traits(role, ours)
    return ours


def inspection(role, ident):
    require(ident in catalog(), '封神榜NPC不存在')
    npc = catalog()[ident]['role']; s = role['activity']
    order = next((o for o in range(1, rules()['size']+1) if identity(s,o) == ident), None)
    require(order is not None, '封神榜对手已变化')
    chars = []
    for c in sorted(npc['corteges'],key=lambda c:c.get('order',0)):
        if not c.get('order'): continue
        row = {k:v for k,v in c.items() if k!='id'}
        row.update(type_id=c['type'], max_hp_show=c['hp'], max_magic_show=c['magic'], wuligongji_show=c['gongji'], wulifangyu_show=c['fangyu'])
        chars.append(row)
    data = dict(role_id=ident, role_name=opponent(s,order)['name'], level=npc['level'], vip_level=0, head_type=1, rank=0,
                title_info={}, animal_info={}, hole_train={}, cortege_list=chars, equip_list=[], skill_list=[], ext_skill_list={}, ext_star_list={})
    data.update(cheer.inspection(npc))
    for c in data['cheer_cortege'].values(): c.pop('id',None)
    owners={c['id']:c['order'] for c in npc['corteges'] if c.get('order')}
    for i in npc['attachments']:
        if i['attach_type']==5 and i.get('owner_id') in owners and i['type_id'] in combat.ESSENCES:
            data['ext_skill_list'].setdefault(owners[i['owner_id']],[]).append(dict(type_id=i['type_id'],level=i['level']))
        if i['attach_type']==5 and i.get('owner_id') in owners and i['type_id'] in reborn_stars.STARS:
            data['ext_star_list'].setdefault(owners[i['owner_id']],[]).append(dict(type_id=i['type_id'],level=i['level'],order=i['ext_awaken_pos']))
        if not i.get('equip_order') or not i.get('equip_pos'): continue
        row = dict(i, order=i['equip_order'], goss_plus=i.get('goss_plus',0))
        if i['attach_type'] == 6 and i['equip_order'] <= 8: data['skill_list'].append(row)
        elif i['attach_type'] == 5: data['equip_list'].append(row)
    # Inspecting never copies the NPC inventory into the player's save.
    return summon.event(11, data)


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
                  fight_result_msg=decode(encode(1027,dict(fight_id=fid,fight_type=2,final_result=result,fight_round=len(actions),fight_result=actions)))[2])
    # Check the complete effect packet before committing any cost or rank swap.
    summon.event(121, replay['fight_events'])
    s['rank_records'] = (s['rank_records']+[replay])[-rules()['records']:]
    return win, replay


def replay_packets(record):
    effects = {int(k) if str(k).isdigit() else k:v for k,v in record['fight_events'].items()}
    return [summon.event(121, effects), encode(1028, record['line_up_msg']), encode(1027, record['fight_result_msg'])]


def battle(role, req, now, arules, jrules):
    from . import activity as a
    s = role['activity']; target = req['des_value']
    require(role['level'] >= 6, '封神榜需6级')
    require(target in challenge_orders(s) and req['des_type'] == 2 and req['des_id'] == identity(s,target), '封神榜对手已变化，请刷新')
    require(s['rank_count'] < role['top_fight_limit']+s['rank_extra'], '今日封神榜次数已用完')
    require(any(c.get('order') for c in role['corteges']), '请先上阵神仙')
    a.spend(role,'energy',1); s['rank_count'] += 1; role['top_fight_time'] = now
    win, replay = simulate(role, target, now, jrules)
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
    return replay_packets(replay)+[client_state(role),board(role)]+([summon.event(33,rewards)] if win else [])+[summon.event(44,dict(fight_id=replay['fight_id'],fight_type=2))]


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
        return [summon.event(80,dict(local_rank_records=meta)),record_packets(dict(records=s['rank_records']))[0],
                summon.event(80,dict(local_rank_show_records=True))]
    if mid == 1051:
        n = req['item_count'] or 1
        require(1 <= n <= 100 and req['des_type'] in (0,1) and req['des_id'] in (0,role['role_id']), '封神令牌使用参数无效')
        require(req['item_id'] == 0 or any(i['id']==req['item_id'] and i['type_id']==1021 and i['attach_type']==5 and not i.get('owner_id') and not i.get('is_lock') for i in role['attachments']), '封神令牌不存在')
        require(s['rank_extra']+3*n <= rules()['max_extra_chances'], '今日额外挑战次数已达上限')
        a.consume(role,1021,n); s['rank_extra'] += 3*n
        prepare(role,now,arules)
        return [client_state(role),board(role),summon.event(21,dict(result=1,type_id=1021,count=n))]
    if mid == 1201:
        require(s['rank_pending_score']>0 and not s['rank_claimed'], '暂无昨日奖励或今日已领取')
        gain = s['rank_pending_score']; s['rank_score'] = min(16777215,s['rank_score']+gain)
        s['rank_pending_score']=0; s['rank_claimed']=True; role['top_day_prize_time']=now
        return [client_state(role),board(role),summon.event(34,dict(attach_count=gain))]
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
        return [client_state(role),board(role),summon.event(36,a.prizes(role,specs))]
    raise formation.Rejected('封神榜操作无效')
