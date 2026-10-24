"""Original seasonal crafting recipes; explicit offline availability and supplies [B]."""
import copy
from . import activity as a, summon, formation


def original_spec(value):
    typ,tid,level,count=map(int,value.split('|'))
    return [typ,tid,count,level]


RICE={int(x['index']):dict(source=[original_spec(v) for v in x['object_type'].split('/')],dest=original_spec(x['sub_type'])) for x in summon.rows('zongzi_formula.csv')}
MOON={original_spec(x['src_type'])[1]:dict(source=[original_spec(x['src_type']),original_spec(x['common_src_type'])],dest=original_spec(x['des_type'])) for x in summon.rows('compose_monthcake.csv')}
NAMES={int(x['Ftype_id']):x['name'] for x in summon.rows('item_name.csv')}
FOODS={1130,1131,1132,1133,1213,1214,1215,1216,1217}


def travel_drop(role,now,r):
    if not any(is_open(r,n,now) for n in r['seasonal_games']):return []
    role.setdefault('activity',{});s=state(role);idx=s.get('travel_wins',0);s['travel_wins']=idx+1;rewards=[]
    for name,table in (('rice',RICE),('moon',MOON)):
        if is_open(r,name,now):
            for typ,tid,n,lv in list(table.values())[idx%4]['source']:
                rewards.append([typ,tid,r['seasonal_travel_material_count'],lv])
    if is_open(r,'spring_money',now):rewards.append([5,1028,1,1])
    if is_open(r,'spring_cards',now) and (idx+1)%5==0:
        from .activity_spring import card
        card(role,(idx//5)%10+1)
        rewards_shown=a.prizes(role,rewards)
        return rewards_shown+[a.prize_spec([5,1094,1,(idx//5)%10+1])]
    return a.prizes(role,rewards)


def use_food(role,req,r):
    tid,n=req['item_type'],req['item_count']
    a.require(tid in FOODS and type(n)is int and 1<=n<=100,'节日礼包使用数量无效')
    a.require(req['des_type']==1 and req['des_id'] in (0,role['role_id']),'节日礼包使用目标无效')
    item=formation.lookup(role,'attachments',req['item_id'])
    a.require(item['attach_type']==5 and item['type_id']==tid and item['count']>=n and not item.get('is_lock'),'节日礼包不足或已锁定')
    a.consume(role,tid,n)
    rewards=copy.deepcopy(r['seasonal_food_rewards'][str(tid)])
    for p in rewards:p[2]*=n
    return [summon.event(21,dict(result=1,type_id=tid,count=n,attach_list=a.prizes(role,rewards)))]


def state(role):return role['activity'].setdefault('seasonal',dict(supplies={},counts={},rice_news=[],moon_news=[],moon_count=0))


def is_open(r,name,now):
    cfg=r['seasonal_games'][name]
    return cfg['enabled'] and cfg['start_time']<=now<cfg['end_time']


def supply(role,s,r,name,now):
    # One starter set per configured season, never one per query or per restart.
    cfg=r['seasonal_games'][name];key=f"{name}:{cfg['start_time']}"
    if not is_open(r,name,now) or key in s['supplies']:return
    s['supplies'][key]=True
    for row in (RICE if name=='rice' else MOON).values():a.prizes(role,row['source'])


def status(role,now,r):
    s=state(role);out={}
    for name,field,start in (('rice','dragon_boat_info','start_time'),('moon','midautumn_data','begin_time')):
        cfg=r['seasonal_games'][name]
        supply(role,s,r,name,now)
        out[field]={start:cfg['start_time'] if cfg['enabled'] else 0,'end_time':cfg['end_time'] if cfg['enabled'] else 0}
    out['dragon_boat_info']['luck_list']=copy.deepcopy(s['rice_news'])
    from .activity_spring import status as spring_status
    out.update(spring_status(role,now,r))
    from .activity_fish import status as fish_status
    out.update(fish_status(role,now,r))
    return out


def moon_news(s,r):
    step=r['seasonal_moon_bonus_every'];left=step-s['moon_count']%step
    return dict(flag=0,mooncake_count=s['moon_count'],cur_process=s['moon_count']%step,left_process=left,broad_list=copy.deepcopy(s['moon_news']))


def settle(role,mid,req,now,r):
    name='rice' if mid==1126 else 'moon';a.require(is_open(r,name,now),'活动尚未开放或已经结束')
    s=state(role)
    if mid==1333 and req['flag']==0:return [summon.event(178,moon_news(s,r))]
    a.require(mid!=1333 or req['flag']==1,'月饼操作无效')
    table=RICE if name=='rice' else MOON;idx=req['compose_type'] if name=='rice' else req['src_type']
    a.require(type(idx)is int and idx in table,'合成配方无效');row=table[idx]
    if name=='rice':
        ids=[x['id'] for x in req['material_list']]
        a.require(req['material_count']==len(row['source'])==len(ids) and len(set(ids))==len(ids),'合成材料数量无效')
        items=[next((i for i in role['attachments'] if i['id']==v and i['attach_type']==5),None) for v in ids]
        a.require(all(items) and sorted(i['type_id'] for i in items)==sorted(p[1] for p in row['source']),'合成材料不属于该配方')
        a.require(all(not i.get('is_lock') and not i.get('owner_id') and not i.get('equip_pos') and i['count']>=next(p[2] for p in row['source'] if p[1]==i['type_id']) for i in items),'所选合成材料不足或不可使用')
    daykey=f'{name}:{a.day(now,r)}';count=s['counts'].get(daykey,0)
    a.require(count<r['seasonal_craft_daily_limit'],'今日合成次数已满')
    for typ,tid,n,lv in row['source']:a.consume(role,tid,n)
    reward=[copy.deepcopy(row['dest'])];s['counts'][daykey]=count+1
    # Bound historical counters while preserving season supplies.
    s['counts']={k:v for k,v in s['counts'].items() if int(k.split(':')[1])>=a.day(now,r)-1}
    if name=='rice':
        s['rice_news'].insert(0,dict(name=role['role_name'],data=[row['dest'][1]]));s['rice_news']=s['rice_news'][:5]
        return [summon.event(126,dict(result=0,attach_list=a.prizes(role,reward),luck_list=copy.deepcopy(s['rice_news'])))]
    s['moon_count']+=1
    if s['moon_count']%r['seasonal_moon_bonus_every']==0:reward.extend(copy.deepcopy(r['seasonal_moon_bonus']))
    s['moon_news'].insert(0,f"{role['role_name']}合成了{NAMES[row['dest'][1]]}");s['moon_news']=s['moon_news'][:5]
    return [summon.event(178,dict(flag=1,prize_list=a.prizes(role,reward))),summon.event(178,moon_news(s,r))]
