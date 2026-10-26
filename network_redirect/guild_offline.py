"""Inferred single-player guild world, migrations and reachable chat commands.

NPCs never represent connected accounts. Random choices consume a persisted stream,
so failed transactions and reconnects cannot reroll a pending reward.
"""
import copy
import random
from . import formation, journey
require = formation.require


def roll(s, upper):
    serial=s.get('random_serial',0)
    value=random.Random(f"guild:{s.get('day',0)}:{serial}").randrange(upper)
    s['random_serial']=serial+1
    return value


def capacity(g,r):
    return min(100,r['member_limit']+(g['level']-1)*r['member_growth'])


def npc(ident,name,now,rank=5):
    return dict(id=ident,name=name,rank=rank,level=30,contrib=0,totalcontrib=0,
                head_type=5004,jointime=now,lastlogin=now,online=False,toporder=0,
                logout_time=now,combat_power=1000,npc=True)


def prepare(role,s,g,now,r):
    from .guild import new_union
    from . import guild_npcs
    # IDs above the player-created range; migrate once without overwriting saves.
    if not s.get('offline_world_v1'):
        for ident,name,pop in ((80001,'花果山演武盟',1200),(80002,'蓬莱修行盟',600),(80003,'昆仑问道盟',300)):
            v=new_union(ident,name,r);v['popularity']=pop;v['npc']=True
            v['members']={str(ident*10+i):npc(ident*10+i,name[:3]+str(i),now,1 if i==1 else 5) for i in range(1,4)}
            s['unions'].setdefault(str(ident),v)
        home=s['unions'].get('1')
        if home:
            for i in range(2,5):home['members'].setdefault(str(10000+i),npc(10000+i,'离线道友'+str(i),now))
            if '10001' in home['members']:home['members']['10001']['npc']=True
        s['offline_world_v1']=True
    guild_npcs.migrate(role,s,now)
    if not role['union_id']:
        key=str(int(role['role_id']))
        for v in s['unions'].values():
            pending=v['applications'].get(key)
            if pending and not pending.get('npc') and now>=pending.get('requested_at',now)+3:
                accepted=len(v['members'])<capacity(v,r) and s.get('join_count',0)<r['join_daily']
                if accepted:
                    pending.update(rank=5,jointime=now,online=True);v['members'][key]=pending
                    role.update(union_id=v['id'],union_rank=5,union_name=v['name'],union_contrib=0,cur_union_contrib=0)
                    s['join_count']=s.get('join_count',0)+1
                del v['applications'][key];s.setdefault('pending_notices',[]).append(dict(event_id=8 if accepted else 9,result=1,role_id=int(key)))
                break
    for v in s['unions'].values():
        v['level']=min(r['max_level'],1+v['popularity']//r['level_popularity'])
        v['forbidden']=[m for m in v['forbidden'] if m.get('expires',now+1)>now]
        for m in v['members'].values():
            if m.get('npc'):
                m['online']=(s['day']+m['id'])%3!=0
                m['lastlogin']=now if m['online'] else now-(m['id']%12+1)*3600
        for i,m in enumerate(sorted(v['members'].values(),key=lambda m:(-m.get('totalcontrib',0),m['id'])),1):m['toporder']=i
    for i,v in enumerate(sorted(s['unions'].values(),key=lambda v:(-v['popularity'],-v['level'],v['id'])),1):v['order']=i
    role['union_apply_count']=s.get('apply_count',0);role['union_join_count']=s.get('join_count',0)
    if g:
        a=s.get('instances',{});team=a.get('team')
        if team:
            team['members']=[key for key in team['members'] if key in g['members']]
            team['applications']={key:v for key,v in team.get('applications',{}).items() if key in g['members'] and key not in team['members']}
            if str(team['captain']) not in team['members']:a['team']=None
    if g:
        guild_npcs.recruit(role,s,g,now,r)


def store(s,r):
    if not s.get('store_stock'):s['store_stock']=copy.deepcopy(r['store'])
    return s['store_stock']


def refresh_store(s,r):
    rows=copy.deepcopy(r['store']);shift=1+roll(s,len(rows)-1)
    prizes=[row['prize'] for row in rows]
    for i,row in enumerate(rows):row['prize']=prizes[(i+shift)%len(rows)]
    s['store_stock']=rows


def pets(a):
    if 'pet_entities' not in a:
        mapping={1:101,2:102,3:103,4:104,5:105,6:201,106:201}
        a['pets']=[mapping.get(t,t) for t in a.get('pets',[])]
        a['pet_entities']=[dict(id=i,type_id=t,quality=1,level=1,exp=0,star=1) for i,t in enumerate(a.get('pets',[]),1)]
        a['next_pet_id']=len(a['pet_entities'])+1
    return a['pet_entities']


def add_pet(a,tid,s,r):
    rows=pets(a);require(len(rows)<r['pet_limit'],'兽栏已满')
    p=dict(id=a['next_pet_id'],type_id=tid,quality=1+roll(s,3),level=1,exp=0,star=1)
    a['next_pet_id']+=1;rows.append(p);a['pets']=[v['type_id'] for v in rows]
    return p


def pet_power(p):
    return p['quality']*p['level']*p['star']*20


def pet_command(role,s,g,msg,now,r):
    """Original chat is the accessible UI for features with no proven guild button."""
    from .guild_instances import state
    from . import guild as u
    a=state(s);rows=pets(a);args=msg.split();cmd=args[0]
    if cmd=='/灵兽':
        require(len(args)<=2 and (len(args)==1 or args[1].isdecimal()),'用法：/灵兽 页码')
        page=int(args[1]) if len(args)>1 else 1;require(page>0,'页码无效')
        rows=rows[(page-1)*3:page*3]
        return '；'.join(f"{p['id']}号 类型{p['type_id']} 品质{p['quality']} 等级{p['level']} 星{p['star']} 战力{pet_power(p)}" for p in rows) or '兽栏为空，请先游历捕捉'
    require(cmd in ('/喂养','/升星','/合成'),'命令：/灵兽、/喂养 编号、/升星 编号、/合成 编号 材料编号')
    require(len(args)==(3 if cmd=='/合成' else 2) and all(v.isdecimal() for v in args[1:]),'灵兽命令参数无效')
    p=next((v for v in rows if v['id']==int(args[1])),None);require(p is not None,'灵兽不存在')
    if cmd=='/喂养':
        require(p['level']<r['pet_max_level'],'已达等级上限');u.pay(role,'silver_coin',r['pet_feed_silver']);p['exp']+=r['pet_feed_exp']
        gain,p['exp']=divmod(p['exp'],r['pet_exp_level']);p['level']=min(r['pet_max_level'],p['level']+gain)
    else:
        material=next((v for v in rows if v['id']!=p['id'] and v['type_id']==p['type_id'] and (cmd!='/合成' or v['id']==int(args[2]))),None)
        require(material is not None,'需要另一只同类型灵兽')
        if cmd=='/升星':
            require(p['star']<r['pet_max_star'],'已达星级上限');u.pay(a,'reputation',r['pet_star_reputation']*p['star']);p['star']+=1
        else:
            require(p['quality']<5 and material['quality']>=p['quality'],'需要不低于当前品质的材料，最高品质5');p['quality']+=1
        rows.remove(material)
    a['pets']=[v['type_id'] for v in rows]
    return f"{p['id']}号灵兽：品质{p['quality']} 等级{p['level']} 经验{p['exp']} 星{p['star']} 战力{pet_power(p)}"


def audit(before,role,now,operation,r):
    previous=before.get('guild',{}).get('unions',{})
    for key,g in role.get('guild',{}).get('unions',{}).items():
        old=previous.get(key,{}).get('money',g['money'])
        g['money']=min(r['money_cap'],g['money'])
        if old!=g['money']:
            log=g.setdefault('money_log',[])
            log.append(dict(time=now,actor=role['role_id'],operation=operation,change=g['money']-old,balance=g['money']))
            g['money_log']=log[-200:]


def validate_rules(r):
    from . import daily
    require(type(r.get('npc_recruit_daily',4)) is int and 1<=r.get('npc_recruit_daily',4)<=20,'每日NPC招募人数无效')
    keys=('tree_require_pop','member_growth','apply_daily','join_daily','mute_seconds','money_cap','search_sweep_gold','tree_challenge_contrib','tree_challenge_limit','tree_paid_peaches','tree_level_bonus_percent','match_life','match_loss_life','match_target_loss','match_max_streak','train_hp','train_seconds','train_support_limit','train_attempt_limit','train_resident_required','npc_resident_pets','lucky_reputation_per_draw','lucky_draw_limit','hunt_rank_limit','pet_limit','pet_feed_silver','pet_feed_exp','pet_exp_level','pet_max_level','pet_max_star','pet_star_reputation','catch_success_percent','hunt_paid_limit')
    for k in keys:require(type(r.get(k)) is int and 0<r[k]<=100000000,'离线仙盟配置无效：'+k)
    require(type(r.get('catch_resident_percent'))is int and 0<=r['catch_resident_percent']<=100,'栖息概率配置无效')
    require(type(r['catch_item_bonus'])is int and 0<=r['catch_item_bonus']<=100,'捕捉道具加成无效')
    daily.validate_prize([5,r['catch_item'],1,1])
    require(r['catch_success_percent']<=100 and r['pet_limit']<=240 and r['search_daily']<=25,'概率、兽栏或棋盘配置越界')
    require(r['train_resident_required']==240,'原版试炼需要240只栖息宠物')
    require(type(r.get('team_min_fighters')) is int and r['team_min_fighters']==3,'秘境至少三人出战')
    require(r['train_support_limit']<=20 and r['team_min_fighters']<=r['team_size']<=5,'活动人数配置越界')
    for k in ('hunt_weekend_open','npc_auto_accept','train_weekend_only','lucky_weekend_only'):require(type(r.get(k))is bool,'开关配置无效：'+k)
    for key in ('rank_power','rank_rights','match_merit'):
        require(set(r.get(key,{}))==set(map(str,range(1,8))),'职位配置缺失：'+key)
    for rights in r['rank_rights'].values():require(isinstance(rights,list) and all(type(v)is int and 1<=v<=28 for v in rights),'权限配置无效')
    for k in ('rank_power','match_merit','rank_limits'):
        require(all(type(v)is int and v>0 for v in r[k].values()),'职位数值无效')
    require(r['mission_cost_types'] and all(type(v)is int and v in range(1,5) for v in r['mission_cost_types']),'神树任务池无效')
    require(len(r['hunt_shop_unlock'])==len(r['hunt_rewards']) and all(type(v)is int and v>=0 for v in r['hunt_shop_unlock']),'声望解锁配置无效')
    from . import summon
    valid={int(v['type_id']) for v in summon.rows('animal_base.csv')}
    require(r['pet_types'] and all(type(v)is int and v in valid for v in r['pet_types']),'灵兽类型配置无效')
    require(r['search_rewards'],'寻宝奖励池为空')
    for p in r['search_rewards']:daily.validate_prize(p)
    require(set(r['west_config']['book_worth_config'])==set(map(str,range(1,6))),'取经品质配置不完整')


def funds(g,amount,r):
    require(g['money']+amount>=0,'仙盟资金不足')
    actual=min(r['money_cap'],g['money']+amount)-g['money']
    g['money']+=actual
    return actual
