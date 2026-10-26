"""通幽榜：原版前20名展示 [A]，资料库玩家的离线进度 [B]."""
import math
import copy
from . import activity, npc_players, summon

PRIZES=[row for row in summon.rows('specter_top_prize.csv') if row['top_type']=='1']


def standings(role, state, now, rules):
    # Persist the epoch; queries/restarts never reroll identities or progress.
    today = activity.day(now, rules)
    epoch = state.setdefault('npc_epoch_day', today)
    observed = max(today, state.setdefault('npc_observed_day', epoch))
    state['npc_observed_day'] = observed
    profiles = [entry['profile'] for entry in npc_players.catalog().values()
                if entry['profile']['level'] >= 70]
    powers = [math.log(max(1, p['role_combat_power'])) for p in profiles]
    low, high = min(powers), max(powers)
    rows = []
    for p, power in zip(profiles, powers):
        initial = 1 + int(71 * (power-low) / max(1e-9, high-low))
        layer = min(80, initial + max(0, observed-epoch)//3)
        rows.append(dict(role_id=p['role_id'], name=p['role_name'], level=p['level'],
                         head_type=p['head_type'], layer=layer, is_npc=True))
    mine = dict(role_id=role['role_id'], name=role['role_name'], level=role['level'],
                head_type=role['head_type'], layer=state['boss']-1+int(bool(state.get('complete'))),
                is_npc=False)
    rows.append(mine)
    rows.sort(key=lambda p: (-p['layer'], p['role_id']))
    for index, row in enumerate(rows, 1):
        row['order'] = index
    return dict(top_type=1, my_top=mine, top_data=rows[:20])


def settle_day(role, state, now, rules):
    """[B] Mail the last active day's top-five prize once; no idle-day farming."""
    today=activity.day(now,rules)
    previous=state.setdefault('rank_day',today)
    if today<=previous:return
    end=(previous+1)*86400-rules['timezone_offset_hours']*3600-1
    board=standings(role,state,end,rules)
    mine=board['my_top']
    state['last_rank_result']=dict(day=previous,order=mine['order'],layer=mine['layer'])
    row=next((row for row in PRIZES if int(row['min_order'])<=mine['order']<=int(row['max_order'])),None)
    if row and mine['layer']>0:
        from . import system_mail, welfare
        prizes=[]
        for token in row['prize_list'].split('/'):
            kind,tid,level,count=map(int,token.split('|'));prizes.append([kind,tid,count,level])
        delivery=copy.deepcopy(role)
        system_mail.deliver(delivery,f'abyss-rank-{previous}','九幽通幽榜奖励',
            f"上一活跃日通幽榜第{mine['order']}名，已通关{mine['layer']}层。榜单对手为本地NPC。",
            prizes,now,welfare.load_rules())
        role['welfare']=delivery['welfare']
    state['rank_day']=today
