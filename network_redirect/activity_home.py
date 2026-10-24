"""洞府 1348 [A]; persistent local economy, missing schedules/shop/boss [B]."""
import copy
import secrets
from . import activity as a, formation, journey, summon
from .protocol import encode


def table(name):return [{k.split('(')[0]:v for k,v in row.items()} for row in summon.rows('hole/'+name+'.csv')]
BUILD={i:{int(next(iter(x.values()))):x for x in table(name)} for i,name in enumerate(
    ('main_building_config','garden_building_config','temple_config','train_building_config','pet_building_config'),1)}
UPGRADE={(int(x['building_type']),int(x['building_level'])):x for x in table('upgrade_building_materials')}
OWNER={int(x['hole_level']):x for x in table('hole_owner_config')}
SEEDS={int(x['seed_index']):x for x in table('garden_seed_config')}
GRIDS={int(x['grid_level']):x for x in table('garden_grid_config')}
TRAIN={(int(x['train_type']),int(x['level'])):x for x in table('hole_train_config')}
EXP={int(x['index']):x for x in table('add_experience_config')}
TEMPLE={(int(x['temple_level']),int(x['pray_count'])):int(x['count_plus']) for x in table('temple_level_plus')}
EXT=table('temple_ext_prize')[0]
KEYS={1:'main_data',2:'garden_data',3:'temple_data',4:'train_data',5:'pet_data'}


def response(op,data):return encode(1348,dict(id=op,data=summon.lua(dict(result=1,**data))))


def cost(role,value,n=1):
    for token in filter(None,value.split('/')):
        p=list(map(int,token.split('|')))
        typ,tid,count=(p[0],0,p[1]) if len(p)==2 else p[:3]
        if typ in (11,12):a.spend(role,'gold_coin' if typ==11 else 'silver_coin',count*n)
        else:a.require(typ==5,'洞府消耗类型未配置');a.consume(role,tid,count*n)


def specs(value):return [list(map(int,t.split('|'))) for t in value.split('/') if t]


def state(role,now,r):
    s=role['activity'].setdefault('home',dict(level=1,build={str(i):0 for i in KEYS},plants={},
        train={str(i):dict(level=0,cur_exp=0) for i in range(1,5)},pray_time=0,pray_count=0,passed=False,day=-1))
    if s['day']!=a.day(now,r):s.update(day=a.day(now,r),train_count={},purchases={},fight_count=r['home_boss_daily_limit'])
    s.setdefault('assistant_until',0);s.setdefault('assistant_from',0)
    from .activity_home_pets import initialize
    initialize(s,r)
    for p in s['plants'].values():
        if not p.get('seed_type'):continue
        # Migrate saves made before the original garden wire contract was audited.
        p.setdefault('start_time',p.get('plant_time',now))
        p.setdefault('total_plus_times',int(SEEDS[p['seed_type']]['friend_plus_times']))
        p.setdefault('event_info',[]);p.setdefault('missed_events',0)
        for event in p['event_info']:
            if not event['end_time'] or now<event['start_time']:continue
            if s['assistant_from']<event['end_time'] and s['assistant_until']>=event['start_time']:
                event['end_time']=0
            elif now>=event['end_time']:
                p['missed_events']+=1;event['end_time']=0
    return s


def point(s):
    base=sum(int(BUILD[i][s['build'][str(i)]]['point_plus']) for i in KEYS)
    return base*(100+int(OWNER[s['level']]['point_plus']))//100


def upgrade_info(s,r):
    return dict(has_passed=s['passed'],fight_count=s['fight_count'],boss_info=dict(cortege_type=r['battle_npc'],
        cortege_layer=0,combat_power=100*s['level'],cortege_count=1,train_level=s['level']))


def info(s,r):
    data={KEYS[i]:dict(level=s['build'][str(i)]) for i in KEYS}
    data.update(base_data=dict(level=s['level'],point=point(s),upgrade_info=upgrade_info(s,r)),
        config_data=dict(activity_flag={},ass_gold=r['home_assistant_gold']),message_data=copy.deepcopy(s.get('messages',[])),friend_list=[],has_invited_flag=False,new_event=s.get('new_event',False))
    data['garden_data'].update(assisant=s['assistant_until'],plant_data={int(k):copy.deepcopy(v) for k,v in s['plants'].items()})
    data['temple_data'].update(pray_time=s['pray_time'],pray_count=s['pray_count'])
    data['train_data'].update(train_info={int(k):v for k,v in s['train'].items()},
        train_count={int(k):v for k,v in s['train_count'].items()})
    from .activity_home_pets import view
    data['pet_data'].update(view(s))
    return data


def shop(s,r):
    return [[dict(item=a.prize_spec(row['reward']),consume=a.prize_spec(row['consume']),
                  limit=row['limit']-s['purchases'].get(str(i),0)) for i,row in enumerate(r['home_shop'],1)]]


def settle(role,req,now,r,jrules,parse):
    a.require(role['level']>=50,'洞府需50级');s=state(role,now,r)
    d=parse(req['data']) if req['data'] else {};a.require(isinstance(d,dict),'洞府参数无效');op=req['id']
    if op==1:return [response(1,info(s,r))]
    if op==8:
        hours=d.get('hour')
        a.require(s['build']['2']>0,'请先建造药园')
        a.require(type(hours)is int and 1<=hours<=48 and max(now,s['assistant_until'])+hours*3600-now<=48*3600,'助手雇佣时间最多48小时')
        a.spend(role,'gold_coin',hours*r['home_assistant_gold'])
        if s['assistant_until']<now:s['assistant_from']=now
        s['assistant_until']=max(now,s['assistant_until'])+hours*3600
        state(role,now,r)
        return [response(8,dict(assisant=s['assistant_until']))]
    if op in (5,6,7,12,13,23):
        from .activity_home_friends import settle as friends
        return friends(role,s,op,d,now,r)
    if op==19:return [response(19,dict(message_data=copy.deepcopy(s.get('messages',[]))))]
    if op==18:
        if d.get('clean'):s['new_event']=False
        return [response(18,dict(new_event=s.get('new_event',False)))]
    if op in (21,22):
        from .activity_home_pets import settle as pets
        return pets(role,s,op,d,r)
    if op==24:
        a.require(d.get('flag',1)==1,'没有进行中的洞府限时福利')
        return [response(24,dict(flag=1,all_activity=[]))]
    if op in (14,15):
        if op==15:
            i,n=d.get('item_index'),d.get('buy_count',1)
            a.require(d.get('shop_page')==1 and type(i)is int and 1<=i<=len(r['home_shop']) and type(n)is int and n>0,'洞府兑换参数无效')
            row=r['home_shop'][i-1];used=s['purchases'].get(str(i),0)
            a.require(n+used<=row['limit'],'兑换次数不足')
            cost(role,'|'.join(map(str,row['consume'])),n);p=row['reward'];a.prizes(role,[[p[0],p[1],p[2]*n,p[3]]])
            s['purchases'][str(i)]=used+n
            return [response(15,dict(shop_page=1,item_index=i,limit=row['limit']-used-n))]
        a.require(not d.get('flush_flag'),'商店在每日零点自动刷新')
        return [response(14,dict(shop_data=shop(s,r),diff_time=86400-(now+8*3600)%86400,flush_flag=False))]
    if op==2:
        typ=d.get('building_type');a.require(type(typ)is int and typ in KEYS,'洞府建筑无效')
        level=s['build'][str(typ)]+1;row=UPGRADE.get((typ,level))
        a.require(row is not None and level<=int(OWNER[s['level']]['max_building_level']),'建筑已达当前洞府上限')
        for token in filter(None,row['pre_conditions'].split('/')):
            pre,lv=map(int,token.split('|'))
            a.require((s['level'] if pre==0 else s['build'][str(pre)])>=lv,'前置建筑等级不足')
        cost(role,row['cost']);s['build'][str(typ)]=level;role['hole_hp_plus']=point(s);new={}
        if typ==2:
            for i in range(1,int(BUILD[2][level]['grid_count'])+1):
                if str(i) not in s['plants']:s['plants'][str(i)]=dict(level=0);new[i]=s['plants'][str(i)]
        return [response(2,dict(building_type=typ,level=level,point=point(s),new_grids=new))]
    if op in (3,4,9,10):
        idx=d.get('plant_grid');a.require(type(idx)is int and str(idx) in s['plants'],'药田未解锁')
        p=s['plants'][str(idx)]
        if op==9:
            row=GRIDS.get(p['level']+1);a.require(row is not None and s['build']['2']>=int(row['pre']),'药田升级条件不足')
            cost(role,row['cost']);p['level']+=1
            return [response(9,dict(plant_grid=idx,level=p['level']))]
        if op==3:
            seed=d.get('seed_type');a.require(type(seed)is int and seed in SEEDS and not p.get('seed_type'),'种子无效或药田已种植')
            row=SEEDS[seed];cost(role,row['cost'])
            duration=int(row['gain_hour'])*3600
            p.update(seed_type=seed,start_time=now,plant_time=now,gain_time=now+duration,cur_plus_times=0,
                total_plus_times=int(row['friend_plus_times']),missed_events=0,
                event_info=[dict(event_index=1,start_time=now+duration//3,end_time=now+duration*2//3)])
            return [response(3,dict(plant_grid=idx,grid_info=copy.deepcopy(p)))]
        if op==4:
            idx_event=d.get('event_index')
            event=next((e for e in p.get('event_info',[]) if e['event_index']==idx_event),None)
            a.require(event is not None and event['start_time']<=now<event['end_time'],'当前药田没有待处理事件')
            event['end_time']=0
            return [response(4,dict(plant_grid=idx,event_info=copy.deepcopy(p['event_info'])))]
        a.require(p.get('seed_type') and now>=p['gain_time'],'作物尚未成熟')
        row=SEEDS[p['seed_type']];rewards=specs(row['worth'])
        grid_plus=int(GRIDS[p['level']]['gain_plus']) if p['level'] else 0
        hole_plus=int(OWNER[s['level']]['plant_plus'])
        friend_plus=p.get('cur_plus_times',0)*r['home_friend_gain_percent']
        plus=grid_plus+hole_plus+friend_plus
        detail=dict(base_worth=rewards[0][2],grid_plus=grid_plus,hole_plus=hole_plus,friend_plus=friend_plus,
            loss_plus=-min(100,r['home_missed_event_penalty']*p['missed_events']))
        for reward in rewards:reward[2]=max(1,reward[2]*(100+plus)//100*max(0,100-r['home_missed_event_penalty']*p['missed_events'])//100)
        gain=a.prizes(role,rewards);level=p['level'];p.clear();p['level']=level
        return [response(10,dict(plant_grid=idx,prize_list=gain,**detail))]
    if op==11:
        a.require(not s['pray_time'] or a.day(s['pray_time'],r)!=a.day(now,r),'今日已祈愿')
        n=s['pray_count']%7+1;rate=TEMPLE.get((s['build']['3'],n),100)
        rewards=copy.deepcopy(r['home_pray_rewards'])
        for p in rewards:p[2]=max(1,p[2]*rate//100)
        if n==7:
            entries=specs(EXT['ext_list']);roll=secrets.randbelow(sum(p[0] for p in entries))
            for p in entries:
                if roll<p[0]:
                    extra=p[1:];scale=max((int(t.split('|')[1]) for t in EXT['level_plus'].split('/') if int(t.split('|')[0])<=s['build']['3']),default=100)
                    extra[2]=extra[2]*scale//100;rewards.append(extra);break
                roll-=p[0]
        s.update(pray_time=now,pray_count=n)
        return [response(11,dict(pray_time=now,pray_count=n,prize_list=a.prizes(role,rewards)))]
    if op==20:
        typ,way,n=d.get('train_type'),d.get('consume_type'),d.get('use_count',1)
        a.require(type(typ)is int and 1<=typ<=4 and type(way)is int and way in EXP and type(n)is int and 1<=n<=1000,'洞府修炼参数无效')
        tr=s['train'][str(typ)];row=EXP[way];used=s['train_count'].get(str(way),0)
        a.require(not int(row['limit']) or used+n<=int(row['limit']),'今日修炼次数已满')
        maximum=int(BUILD[4][s['build']['4']]['train_level']);a.require(tr['level']<maximum,'请先升级修炼房')
        cost(role,row['consume'],n);s['train_count'][str(way)]=used+n;tr['cur_exp']+=int(row['add_experience'])*n
        while tr['level']<maximum:
            need=int(TRAIN[typ,tr['level']+1]['need_experience'])
            if tr['cur_exp']<need:break
            tr['cur_exp']-=need;tr['level']+=1
        return [response(20,dict(train_type=typ,consume_type=way,train_count=used+n,**tr))]
    if op in (25,26):
        a.require(s['level']<max(OWNER),'洞府规模已满')
        maximum=int(OWNER[s['level']]['max_building_level'])
        a.require(all(s['build'][str(i)]>=maximum for i in (1,2,3)),'请先将主殿、药园和佛堂升至当前上限')
        if op==26:
            a.require(s['passed'],'请先通过红尘劫');cost(role,OWNER[s['level']+1]['upgrade_list']);s['level']+=1;s['passed']=False;role['hole_hp_plus']=point(s)
            return [response(26,dict(level=s['level'],point=point(s)))]
        a.require(s['fight_count']>0 and not s['passed'],'红尘劫次数已用完或已经通过');s['fight_count']-=1
        cfg=dict(cortege_list=f"{r['battle_npc']}|{s['level']*r['battle_level']}")
        a.require(any(c.get('order') for c in role['corteges']),'请先上阵神仙')
        result,lineup,actions=journey.battle(role,cfg,jrules);s['passed']=1<=result<=3
        role['activity']['fight_id']+=1;fid=role['activity']['fight_id']
        return [encode(1028,dict(fight_id=fid,first_hand=1,des_name='红尘劫',lineup_count=len(lineup),lineup=lineup)),
            encode(1027,dict(fight_id=fid,fight_type=34,final_result=result,fight_round=len(actions),fight_result=actions)),
            response(25,dict(has_passed=s['passed'],fight_count=s['fight_count'])),summon.event(44,dict(fight_id=fid,fight_type=34))]
    a.require(False,'洞府操作无效或该限时福利尚未配置')
