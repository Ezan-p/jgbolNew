"""蟠桃会: original UI contracts [A], deterministic offline population/rules [B]."""
import copy
import hashlib
import json
from functools import lru_cache
from pathlib import Path
from . import formation, summon, journey, achievements

ROOT = Path(__file__).resolve().parents[1]
require = formation.require


@lru_cache(maxsize=1)
def rules():
    r = json.loads((ROOT/'server_config/party_rules.json').read_text())
    require(r['mode'] == 'inferred', '蟠桃配置须标记推测规则')
    for k, maximum in [('npc_count', 99), ('boss_hp', 100000000), ('damage_per_peach', 100000000), ('peach_cap', 100)]:
        require(type(r[k]) is int and 1 <= r[k] <= maximum, '蟠桃配置无效：'+k)
    pool=r.get('boss_pool')
    require(isinstance(pool,list) and len(pool)==3 and {b.get('type') for b in pool}=={4020,5025,3015}, '蟠桃首领池无效')
    require(all(b['type'] in journey.NPCS and isinstance(b.get('name'),str) and b['name'] for b in pool), '蟠桃首领配置无效')
    for key in ('daily_rewards',):
        require([x['end'] for x in r[key]] == [1, 3, 10, 100], '蟠桃奖励名次无效')
        for row in r[key]:
            for p in row['prizes']:
                require(len(p) == 4 and p[0] in (5, 11, 12) and (p[0] != 5 or p[1] in formation.ITEMS) and 0 < p[2] <= 100000, '蟠桃奖励无效')
    return r


def stable(*parts):
    return int.from_bytes(hashlib.sha256(':'.join(map(str, parts)).encode()).digest()[:8], 'big')


@lru_cache(maxsize=1)
def catalog():
    from . import npc_players
    pool = json.loads((ROOT/'analysis/npc_design/v1/catalog.json').read_text())['npcs']
    pool = [npc_players.decorate(n) for n in pool]
    pool = sorted((n for n in pool if n['role']['level'] >= 13), key=lambda n: (n['role']['role_combat_power'], n['npc_id']))
    # Keep legacy IDs inspectable in saved historical boards.
    count = 99
    return {950001+i: pool[i*(len(pool)-1)//max(1,count-1)] for i in range(count)}


def week(day):
    return (day-4)//7  # Unix epoch Thursday; Monday is day 4.


def identity(role, ident):
    if ident == role['role_id']:
        return dict(id=ident, role_id=ident, name=role['role_name'], level=role['level'], head_type=role.get('head_type',1), vip=role.get('vip_level',0), power=role.get('role_combat_power',0))
    n = catalog()[ident]; p = n['role']
    return dict(id=ident, role_id=ident, name=p['role_name'], level=p['level'], head_type=p['head_type'], vip=p['vip_level'], power=p['role_combat_power'])


def daily_board(role, day, second, ar):
    # Ranking-only NPC scores: fixed for the entire local day, unrelated to HP.
    ids = sorted(catalog(), key=lambda ident: stable('party-roster', day, ident))[:rules()['npc_count']]
    rows = [dict(identity(role, ident), damage=10000 + stable('party-score', day, ident) % rules()['boss_hp'], lucky=0)
            for ident in ids]
    p = role['activity']['party']
    if p['day'] == day and p['count']:
        rows.append(dict(identity(role,role['role_id']),damage=p['damage'],lucky=0))
    rows.sort(key=lambda x: (-x['damage'], x['id']))
    for i,row in enumerate(rows,1): row.update(rank=i,order=i,liked_times=0,isZan=False)
    return rows


def placement(role, rows):
    return next((x['rank'] for x in rows if x['id']==role['role_id']),0)


def rewards(kind, rank):
    return copy.deepcopy(next((row['prizes'] for row in rules()[kind+'_rewards'] if 0 < rank <= row['end']),[]))


def finish_day(role, ar, now):
    p=role['activity']['party']
    if p['closed']: return
    rows=daily_board(role,p['day'],86400,ar); rank=placement(role,rows)
    star=rows[stable(p['day'],'felstar')%len(rows)] if rows else {}
    p['history']=dict(damage_list=rows[:10],top_list=rows[:10],self_damage_his=p['damage'],self_order=rank,
                      fight_count=p['count'],peach_count=p['peaches'],lucky_point=p['lucky'],felstar_info=star)
    if rank:
        specs=rewards('daily',rank)
        if star['id']==role['role_id']:
            specs += [[5,1001,50,1]]
            achievements.add(role,320,1)
        p['daily_pending'] += specs
        achievements.observe(role,218,int(rank<=100));achievements.observe(role,219,int(rank==1))
    p['closed']=True


def prepare(role, now, ar):
    s=role['activity']; local=now+ar['timezone_offset_hours']*3600; day=local//86400; second=local%86400
    p=s.get('party')
    if p is None:
        oldday=s.get('day',day)
        p=s['party']=dict(version=1,day=oldday,week=week(oldday),count=s.get('party_count',0)+s.get('party_paid',0),
            damage=s.get('party_damage',0),lucky=0,peaches=(s.get('party_count',0)+s.get('party_paid',0))*5,
            week_lucky=0,free=s.get('party_count',0),paid=s.get('party_paid',0),bonus=s.get('party_bonus',0),closed=False,history={},week_history={},pending=[],daily_pending=[],clock=now)
    # Retire weekly luck state, including unclaimed legacy weekly rewards.
    p.update(version=2,lucky=0,week_lucky=0,week_history={},pending=[])
    # Ignore backwards wall-clock movement for simulation and rollover.
    now=max(now,p['clock']);p['clock']=now
    local=now+ar['timezone_offset_hours']*3600;day=local//86400;second=local%86400
    if day>p['day'] or second>=ar['party_period'][1]:finish_day(role,ar,now)
    p['week']=week(day)
    if day>p['day']:p.update(day=day,count=0,damage=0,lucky=0,peaches=0,free=0,paid=0,bonus=0,closed=False)
    # Daily awards are delivered on the next successful transaction; no expiry.
    if p['daily_pending']:
        for spec in p['daily_pending']:journey.grant(role,spec)
        p['daily_pending']=[]
    role['party_take_prize']=1
    role['party_order']=0
    return p


def info(role, ar):
    s=role['activity'];p=s['party'];second=(p['clock']+ar['timezone_offset_hours']*3600)%86400
    rows=daily_board(role,p['day'],second,ar);total=p['damage'];hp=rules()['boss_hp']
    wave=total//hp+1
    pool=rules()['boss_pool']
    boss=pool[stable('party-boss',p['day'])%len(pool)]
    return dict(self_damage=p['damage'],free_count=s['party_count'],pay_count=s['party_paid'],
        damage_list=rows,self_order=placement(role,rows),plus_value=s['party_bonus']*10,plus_count=s['party_bonus'],
        peach_count=p['peaches'],lucky_point=p['lucky'],fight_prize=[],boss_type=boss['type'],boss_level=ar['battle_level'],
        damage=0,total_damage=total,max_hp=hp,cur_hp=hp-total%hp,name=boss['name'],boss_wave=wave)


def record(role, damage, gain, ar):
    s=role['activity'];p=s['party'];p['damage']+=max(0,damage);p['count']+=1
    p['peaches']+=sum(x['attach_count'] for x in gain if x['object_type']==5 and x['attach_type']==1001)
    p.update(free=s['party_count'],paid=s['party_paid'])
    s['party_damage']=p['damage']


def query(role, typ, ar, req):
    p=role['activity']['party']
    if typ==1:return [summon.event(29,info(role,ar))]
    if typ==2:
        h=copy.deepcopy(p['history']) or dict(damage_list=[],top_list=[],self_damage_his=0,self_order=0,fight_count=0,peach_count=0,lucky_point=0,felstar_info={})
        for row in h['top_list']:row['isZan']=p.get('praised_day')==p['day']
        return [summon.event(30,h)]
    if typ==3:require(False,'离线模式，暂不开启')
    require(typ==5 and p['history'].get('top_list'),'暂无可点赞的历史榜单')
    require(p.get('praised_day')!=p['day'],'今日已点赞')
    rank=req.get('flag',1) or 1
    require(1<=rank<=len(p['history']['top_list']),'点赞名次无效')
    p['praised_day']=p['day']
    role['activity']['praised']=True
    p['history']['top_list'][rank-1]['liked_times']+=1
    return [summon.event(141,dict(attach_list=[journey.grant(role,[12,0,1000,1])]))]


def claim(role):
    require(False,'离线模式，暂不开启')


def inspection(role, ident):
    from . import npc_players
    return summon.event(11, npc_players.inspection_data(catalog()[ident], scene_id=ident))


def client_config(role, ar):
    h=role['activity']['party']['history']
    return dict(pay_consume_gold=ar['party_fight_gold'],party_top_list=dict(
        top_list=copy.deepcopy(h.get('top_list',[])),top_order=h.get('self_order',0),damage=h.get('self_damage_his',0)))


def sync(role):
    s=role['activity'];p=s['party']
    s.update(party_count=p['free'],party_paid=p['paid'],party_bonus=p['bonus'],party_damage=p['damage'])
    role.update(party_fight_count=p['free'],party_fight_count_plus=p['paid'],gongji_plus_rate=p['bonus']*10)


def seasonal_rewards(role, now, ar):
    from . import activity_seasonal as season
    return [journey.grant(role,p) for p in season.material_specs(ar)]


def fight_rewards(role, damage, ar):
    count = min(rules()['peach_cap'], max(0, damage) // rules()['damage_per_peach'])
    specs = [[5,1001,count,1]] if count else []
    # Preserve any separately configured non-peach participation rewards.
    specs += [p for p in ar['party_rewards'] if p[:2] != [5,1001]]
    return [journey.grant(role, spec) for spec in specs]
