"""Tower card draws, bounded activity log and local weekly settlement."""
import copy
import secrets
from . import activity as a, summon, welfare
from . import activity_land_npc as npc


ESSENCE_POOLS = {
    name: {int(row['id']) for row in summon.rows('ext_skill.csv')
           if int(a.formation.ITEMS[int(row['id'])]['quality']) == quality}
    for name, quality in (('yellow', 4), ('purple', 5))
}
CARD_POOLS = {name: {(5, tid, 1, 1) for tid in ids}
              for name, ids in dict(ESSENCE_POOLS, purple_fragment={10001}).items()}
CARD_POOLS.update(stone_10={(5, 10000, 10, 1)}, stone_20={(5, 10000, 20, 1)})
CARD_ORDER = ('stone_10', 'stone_20', 'yellow', 'purple_fragment', 'purple')


def validate_cards(r):
    expected = set().union(*CARD_POOLS.values())
    a.require({tuple(p) for p in r['land_card_rewards']} == expected,
              '猎魂翻牌奖池须包含全部黄紫精魄、紫色精魄碎片及精魄石10个/20个')
    weights = r.get('land_card_weights')
    a.require(isinstance(weights, dict) and set(weights) == set(CARD_POOLS)
              and all(type(v) is int and v > 0 for v in weights.values())
              and sum(weights.values()) == 100, '猎魂翻牌分类概率须为正整数且合计100%')


def draw_cards(r, count, stone_limit=None):
    # Once the board's stone allowance is exhausted, renormalize the remaining
    # categories. Shuffle so the capped categories do not favor early positions.
    pools = {name: [p for p in r['land_card_rewards'] if tuple(p) in prizes]
             for name, prizes in CARD_POOLS.items()}
    rng = secrets.SystemRandom()
    rewards = []
    for _ in range(count):
        categories = [name for name in CARD_ORDER
                      if stone_limit is None or stone_limit > 0 or not name.startswith('stone_')]
        roll = rng.randrange(sum(r['land_card_weights'][name] for name in categories))
        for name in categories:
            roll -= r['land_card_weights'][name]
            if roll < 0:
                rewards.append(copy.deepcopy(rng.choice(pools[name])))
                if stone_limit is not None and name.startswith('stone_'):stone_limit -= 1
                break
    if stone_limit is not None:rng.shuffle(rewards)
    return rewards


def news(s,now,body):
    entries=s.setdefault('news',[])
    entries.append(dict(time=now,body=body))
    del entries[:-30]
    s['had_news']=True


def gain(s,amount):
    s['soul_count']+=amount
    s['week_soul']=s.get('week_soul',0)+amount


def titles(role,s,now):
    # [A] title_config thresholds; [B] seven days from first achievement.
    awarded=s.setdefault('title_layers',[])
    for tid,layer in zip(range(120,125),(32,40,48,55,60)):
        if s['boss_layer']>=layer and tid not in awarded:
            role.setdefault('profile_titles',{})[str(tid)]=dict(id=tid,begintime=now,endtime=now+7*86400)
            awarded.append(tid)


def weekly(role,s,now,r):
    # Unix epoch was Thursday; Monday is day 4. Keep the account's last active week.
    week=(a.day(now,r)-4)//7
    previous=s.setdefault('week',week)
    s.setdefault('week_soul',0)
    if week<=previous:return
    if s['week_soul']>0:
        _,mine=npc.ranking(role,s,False,2,final=True)
        s['last_week_result']=dict(week=previous,rank=mine['order'],soul=s['week_soul'])
        expiry=((previous+2)*7+4)*86400-r['timezone_offset_hours']*3600
        if mine['order']<=10 and now<expiry:
            rank=mine['order'];tid=125+(3 if rank==1 else 2 if rank<=3 else 1 if rank<=6 else 0)
            role.setdefault('profile_titles',{})[str(tid)]=dict(id=tid,begintime=expiry-7*86400,endtime=expiry)
        row=next((v for v in summon.rows('prey_week_rank.csv') if int(v['min_rank'])<=mine['order']<=int(v['max_rank'])),None)
        if row:
            prizes=[]
            for token in row['attach_list(object|type|level|count)'].split('/'):
                kind,tid,level,count=map(int,token.split('|'));prizes.append([kind,tid,count,level])
            state=welfare.prepare(role,now,welfare.load_rules());mails=state.setdefault('mails',{})
            key='land-week-'+str(previous)
            if key not in mails:
                ident=max({800000000}|{m['mail_id'] for m in mails.values()})+1
                mails[key]=dict(mail_id=ident,mail_title='猎魂之地周榜奖励',
                    mail_body=f"离线猎魂之地周榜第{mine['order']}名。附件永久有效，仅可领取一次。",
                    recv_time=now,send_time=now,prizes=prizes,claimed=False,no_expiry=True,expires_at=None,
                    sender='系统',delivery_key=key)
                news(s,now,f"上周逐鹿排名第{mine['order']}，奖励已发至系统邮件。")
    # Close the old week's rank before clearing progression. Growth and wallet
    # belong to the account; clears, first-win cards and map access to the week.
    s.update(week=week,week_soul=0,map_level=1,boss_layer=0,inv_boss_layer=0,
             total_score=0,history={},inv_history={},boss=None,hell=None,
             unlocked=[],hell_counts={},swept=False,tower_id=0,towers={},travel=None)
    news(s,now,'猎魂之地已刷新：镇妖塔与地图进度重置，魂力、阵位和符咒保留。')


# Guard automatic settlement as well as direct activity operations.
from .time_guard import protect as _protect_time_rewards
_protect_time_rewards(globals())
