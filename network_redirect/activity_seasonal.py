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
BATCH_EVENT = 249  # Local 2998 request; native recipe messages remain single-craft.


def craft_status(s, name, now, r):
    day = a.day(now, r)
    return dict(local_craft_remaining=max(0, r['seasonal_craft_daily_limit']-s['counts'].get(f'{name}:{day}', 0)),
                local_craft_reset_time=(day+1)*86400-r['timezone_offset_hours']*3600)


def settle_batch(role, req, now, r, parse):
    data = parse(req['data'])
    a.require(data.get('activity') in ('moon', 'rice'), '合成活动无效')
    a.require(type(data.get('count')) is int and 1 <= data['count'] <= 100, '合成数量须为1至100')
    # Lua's serialized arrays are decoded as integer-keyed dictionaries.
    if isinstance(data.get('material_list'), dict):
        data['material_list'] = list(data['material_list'].values())
    if data['activity']=='rice':
        a.require(isinstance(data.get('material_list'),list) and
                  all(isinstance(i,dict) and type(i.get('id')) in (int,float) for i in data['material_list']),
                  '合成材料列表无效')
    data['flag'] = 1
    return settle(role, 1126 if data['activity']=='rice' else 1333, data, now, r)


def travel_drop(role,now,r):
    if not any(is_open(r,n,now) for n in r['seasonal_games']):return []
    role.setdefault('activity',{});s=state(role);s['travel_wins']=s.get('travel_wins',0)+1
    from . import activity_tangwang
    return a.prizes(role,material_specs(r))+activity_tangwang.travel_drop(role,now,r)


def material_specs(r):
    from . import activity_moon, activity_rice
    # Share probability tables only. Each event executes five fresh random draws.
    return activity_rice.material_specs(r)+activity_moon.material_specs(r)


def use_food(role,req,r):
    from . import activity_moon, activity_rice
    if req['item_type'] in activity_moon.FOODS:return activity_moon.use(role,req,r)
    if req['item_type'] in activity_rice.FOOD_POOLS:return activity_rice.use(role,req,r)
    tid,n=req['item_type'],req['item_count']
    a.require(tid in FOODS and type(n)is int and 1<=n<=100,'节日礼包使用数量无效')
    a.require(req['des_type']==1 and req['des_id'] in (0,role['role_id']),'节日礼包使用目标无效')
    item=formation.lookup(role,'attachments',req['item_id'])
    a.require(item['attach_type']==5 and item['type_id']==tid and item['count']>=n and not item.get('is_lock'),'节日礼包不足或已锁定')
    a.consume(role,tid,n)
    rewards=copy.deepcopy(r['seasonal_food_rewards'][str(tid)])
    for p in rewards:p[2]*=n
    return [summon.event(21,dict(result=1,type_id=tid,count=n,attach_list=a.prizes(role,rewards)))]


def state(role):
    from . import activity_rice
    return activity_rice.state(role['activity'].setdefault('seasonal',dict(supplies={},counts={},rice_news=[],moon_news=[],moon_count=0)))


def is_open(r,name,now):
    cfg=r['seasonal_games'][name]
    if name in ('spring_money','spring_cards','moon','rice'):return cfg['enabled']
    return cfg['enabled'] and cfg['start_time']<=now<cfg['end_time']


def supply(role,s,r,name,now):
    # Permanent events keep old season-claim markers as one lifetime starter set.
    cfg=r['seasonal_games'][name];key=f"{name}:{cfg['start_time']}"
    if name in ('moon','rice'):
        key=f'{name}:permanent'
        # Preserve already claimed starter sets when migrating the seasonal event.
        if any(k.startswith(f'{name}:') for k in s['supplies']):
            s['supplies'][key]=True
    if not is_open(r,name,now) or key in s['supplies']:return
    s['supplies'][key]=True
    for row in (RICE if name=='rice' else MOON).values():a.prizes(role,row['source'])


def status(role,now,r):
    s=state(role);out={}
    for name,field,start in (('rice','dragon_boat_info','start_time'),('moon','midautumn_data','begin_time')):
        cfg=r['seasonal_games'][name]
        supply(role,s,r,name,now)
        out[field]={start:cfg['start_time'] if cfg['enabled'] else 0,'end_time':cfg['end_time'] if cfg['enabled'] else 0}
        out[field].update(craft_status(s,name,now,r))
    out['dragon_boat_info']['luck_list']=copy.deepcopy(s['rice_news'])
    from . import activity_rice
    out['dragon_boat_info'].update(local_permanent=True,local_enabled=r['seasonal_games']['rice']['enabled'],
                                   **activity_rice.progress(s,r))
    out['midautumn_data'].update(local_permanent=True,local_enabled=r['seasonal_games']['moon']['enabled'])
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
    n=req.get('count',1)
    a.require(type(n)is int and 1<=n<=100,'合成数量须为1至100')
    table=RICE if name=='rice' else MOON;idx=req['compose_type'] if name=='rice' else req['src_type']
    a.require(type(idx)is int and idx in table,'合成配方无效');row=table[idx]
    if name=='rice':
        ids=[x['id'] for x in req['material_list']]
        a.require(req['material_count']==len(row['source'])==len(ids) and len(set(ids))==len(ids),'合成材料数量无效')
        items=[next((i for i in role['attachments'] if i['id']==v and i['attach_type']==5),None) for v in ids]
        a.require(all(items) and sorted(i['type_id'] for i in items)==sorted(p[1] for p in row['source']),'合成材料不属于该配方')
        a.require(all(not i.get('is_lock') and not i.get('owner_id') and not i.get('equip_pos') and not i.get('equip_order') and i['count']>=n*next(p[2] for p in row['source'] if p[1]==i['type_id']) for i in items),'所选合成材料不足或不可使用')
    daykey=f'{name}:{a.day(now,r)}';count=s['counts'].get(daykey,0)
    a.require(count+n<=r['seasonal_craft_daily_limit'],'今日剩余合成次数不足')
    if name=='rice':
        for item in items:item['count']-=n*next(p[2] for p in row['source'] if p[1]==item['type_id'])
        role['attachments']=[i for i in role['attachments'] if i not in items or i['count']>0]
    else:
        for typ,tid,needed,lv in row['source']:
            a.require(sum(i['count'] for i in role['attachments'] if i['attach_type']==typ and i['type_id']==tid
                          and not any(i.get(k) for k in ('is_lock','owner_id','equip_pos','equip_order')))>=needed*n,'合成材料不足或不可使用')
        for typ,tid,needed,lv in row['source']:
            remaining=needed*n
            items=[i for i in role['attachments'] if i['attach_type']==typ and i['type_id']==tid and
                   not any(i.get(k) for k in ('is_lock','owner_id','equip_pos','equip_order'))]
            for item in items:
                used=min(item['count'],remaining);item['count']-=used;remaining-=used
            role['attachments']=[i for i in role['attachments'] if i not in items or i['count']>0]
    reward=[copy.deepcopy(row['dest'])];reward[0][2]*=n;s['counts'][daykey]=count+n
    total_key=name+'_count';step=r['seasonal_moon_bonus_every']
    bonuses=(s[total_key]+n)//step-s[total_key]//step
    s[total_key]+=n
    if bonuses:
        bonus=copy.deepcopy(r['seasonal_moon_bonus'])
        for p in bonus:p[2]*=bonuses
        reward.extend(bonus)
    # Bound historical counters while preserving season supplies.
    s['counts']={k:v for k,v in s['counts'].items() if int(k.split(':')[1])>=a.day(now,r)-1}
    if name=='rice':
        from . import activity_rice
        s['rice_news'].insert(0,dict(name=role['role_name'],data=[row['dest'][1]]));s['rice_news']=s['rice_news'][:5]
        return [summon.event(126,dict(result=0,attach_list=a.prizes(role,reward),luck_list=copy.deepcopy(s['rice_news']),
                                     local_rice_progress=activity_rice.progress(s,r),**craft_status(s,name,now,r)))]
    s['moon_news'].insert(0,f"{role['role_name']}合成了{NAMES[row['dest'][1]]}×{n}");s['moon_news']=s['moon_news'][:5]
    return [summon.event(178,dict(flag=1,prize_list=a.prizes(role,reward),**craft_status(s,name,now,r))),summon.event(178,moon_news(s,r))]
