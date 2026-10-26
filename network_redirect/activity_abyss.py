"""九幽 [A] original floor/drop/boss tables; [B] offline accumulation/economy."""
import copy
import csv
import secrets
from . import activity as a, formation, journey, summon
from .protocol import encode
from . import activity_abyss_combat as combat
HANG={int(x['layer']):x for x in summon.rows('specter_hang_ouput.csv')}
BOSSES={int(x['layer']):x for x in summon.rows('specter_boss_config.csv')}
NPCS={int(x['type_id']):x for x in summon.rows('elite/specter_cortege_base.csv')}
PILLS={int(x['item_type']):next(v for k,v in x.items() if k.startswith('decrease_list')) for x in summon.rows('specter_pill_config.csv')}


def drop_groups():
    # [A] Four identically named output/weight column pairs. DictReader loses
    # the first three pairs, including every treasure map and drug XP drop.
    with (summon.ROOT/'analysis/configs/specter_hang_ouput.csv').open(encoding='utf-8-sig',newline='') as source:
        rows=csv.reader(source);next(rows)
        return {int(row[0]):[(int(row[i+1]),[list(map(int,t.split('|'))) for t in row[i].split('/')])
                            for i in (1,3,5,7)] for row in rows}


DROPS=drop_groups()


def weighted(rows, weight):
    roll=secrets.randbelow(sum(weight(row) for row in rows))
    for row in rows:
        roll-=weight(row)
        if roll<0:return row


def news(s,text,now):
    row=dict(tip=text,tip_type=3,time=now)
    for key in ('news','pending_news'):
        s.setdefault(key,[]).append(row.copy());s[key]=s[key][-20:]


def grant(role,s,specs):
    """Soul crystals are spendable activity currency, not unusable inventory."""
    gains=[]
    for spec in specs:
        if spec[0]==5 and spec[1]==1441:
            s['crystals']+=spec[2];gains.append(a.prize_spec(spec))
        else:gains+=a.prizes(role,[spec])
    return gains


def response(op,**data):return summon.event(173,dict(flag=op,**data))


def state(role,now,r):
    s=role['activity'].setdefault('abyss',dict(layer=1,boss=1,crystals=0,last_time=now,double_end=0,grid_count=30,
        bag=[],reductions=[0]*4,pills={},day=-1))
    s.setdefault('npc_epoch_day',a.day(now,r))
    from .activity_abyss_npc import settle_day
    settle_day(role,s,now,r)
    if s['day']!=a.day(now,r):s.update(day=a.day(now,r),boss_count=0,purchases={},fight_count=0,item_count=0,earned=0,events_finished=0)
    s.setdefault('double_start',s['last_time'])  # compatibility with old saves
    # Old builds granted boss crystals as normal items. Convert once by removing
    # those stacks in the same persisted transaction, without losing the reward.
    legacy=[i for i in role['attachments'] if i['attach_type']==5 and i['type_id']==1441]
    s['crystals']+=sum(i['count'] for i in legacy)
    role['attachments']=[i for i in role['attachments'] if i not in legacy]
    from .activity_abyss_random import accrue
    accrue(s,now,r)
    # [B] Each tick is settled once, bounded by the offline cap; no client time.
    step=r['abyss_tick_seconds'];elapsed=max(0,now-s['last_time'])
    all_ticks=elapsed//step;ticks=min(all_ticks,r['abyss_offline_cap_seconds']//step)
    if ticks:
        earned=items=0
        # [B] Keep the latest capped complete ticks, with each tick attributed to
        # its own local day and only fully covered double periods multiplied.
        for index in range(all_ticks-ticks+1,all_ticks+1):
            at=s['last_time']+index*step;today=a.day(at,r)==s['day']
            count=2 if s['double_start']<=at-step and at<=s['double_end'] else 1
            gain=count*max(1,role.get('role_combat_power',100)//r['abyss_power_per_crystal'])
            s['crystals']+=gain;earned+=gain
            if today:s['earned']+=gain;s['fight_count']+=1
            for _ in range(count):
                if len(s['bag'])>=s['grid_count']:continue
                _,entries=weighted(DROPS[s['layer']],lambda row:row[0])
                typ,tid,lv,n,_=weighted(entries,lambda row:row[4])
                s['bag'].append(a.prize_spec([typ,tid,n,lv]));items+=n
                if today:s['item_count']+=n
        s['last_time']+=all_ticks*step
        news(s,f"第{s['layer']}层挂机结算{ticks}次，获得魂晶{earned}、道具{items}件。"+
             ('临时背包已满，请及时领取。' if len(s['bag'])>=s['grid_count'] else ''),now)
    return s


def specter(s,now):return dict(cur_layer=s['layer'],boss_layer=s['boss'],crystal_count=s['crystals'],event_count=len(s['events']),
    tool_rate=2 if now<s['double_end'] else 1,tool_end_time=s['double_end'],fight_boss_times=s['boss_count'],max_fight_count=5)


def hook(s,now,r):
    return dict(specter_data=specter(s,now),const_config=dict(max_open_area=81,max_event_count=5,
        max_logout_time=r['abyss_offline_cap_seconds'],output_time_rate=2 if now<s['double_end'] else 1,double_product_gold=r['abyss_double_gold']),
        news_list=copy.deepcopy(s.get('news',[])),fight_news=copy.deepcopy(s.get('fight_news',[])))


def bag(s,r):return dict(bag_list=copy.deepcopy(s['bag']),grid_count=s['grid_count'],page_grid=30,open_grid_gold=r['abyss_grid_gold'])


def enemies(s):
    out=[]
    for pos,token in enumerate(next(v for k,v in BOSSES[s['boss']].items() if k and k.startswith('cortege_list')).split('/'),1):
        tid,lv=map(int,token.split('|'));n=NPCS[tid]
        u=dict(type=tid,order=pos,level=1,evolve=0,reborn=0,skills=[])
        for key,column,idx in (('gongji','base_gongji',0),('fangyu','base_fangyu',1),('hp','base_max_hp',2),('magic','base_max_magic',3)):
            u[key]=int(n[column])
        u['max_hp']=u['hp'];sk=int(n['chushijineng'] or 0)
        if sk in formation.SKILLS:u['skills']=[(sk,lv)]
        out.append(u)
    # [B] A drug debuffs the displayed aggregate once, distributed by base
    # attribute. Allocate rounding in slot order; every living unit retains 1.
    for idx,key in enumerate(('gongji','fangyu','hp','magic')):
        total=sum(u[key] for u in out);left=min(s['reductions'][idx],total-len(out))
        remaining=total-len(out)
        for u in out:
            capacity=u[key]-1
            decrement=left*capacity//remaining if remaining else 0
            u[key]-=decrement;left-=decrement;remaining-=capacity
    for u in out:u['max_hp']=u['hp']
    return out


def boss(role,s,now):
    from .activity_drug import bag as drug_bag
    units=enemies(s);raw=enemies(dict(s,reductions=[0]*4))
    caps=[sum(u[k] for u in raw)-len(raw) for k in ('gongji','fangyu','hp','magic')]
    return dict(specter_info=dict(specter(s,now),cur_layer=s['boss']),boss_data=dict(boss_info=[sum(u[k] for u in units) for k in ('gongji','fangyu','hp','magic')],
        pill_list=[min(v,caps[i]) for i,v in enumerate(s['reductions'])],max_list=caps,
        use_pill_list={int(k):v for k,v in s['pills'].items()},drug_bag=drug_bag(role),drug_material=drug_bag(role)[1]))


def shop(s,r):return [dict(a.prize_spec(p['reward']),crystals=p['cost'],buy_times=p['limit']-s['purchases'].get(str(i),0))
    for i,p in enumerate(r['abyss_shop'],1)]


def settle(role,req,now,r,jrules,parse):
    a.require(role['level']>=70,'九幽秘境需70级');d=parse(req['data']) if req['data'] else {}
    a.require(isinstance(d,dict),'九幽参数无效');op=req['id'];s=state(role,now,r)
    if op in (3,24):
        from . import activity_treasure
        return activity_treasure.settle(role,s,op,d,now,r)
    if op==4:
        from . import activity_abyss_random
        return activity_abyss_random.settle(role,s,d,now,r,jrules)
    if op in (8,18,19,20,21,22,23):
        from . import activity_drug
        return activity_drug.settle(role,s,op,d,r)
    if op==7:
        top=d.get('top_type',1);a.require(type(top)is int and top in (1,2),'九幽榜单类型无效')
        from .activity_abyss_npc import standings
        return [response(7,**standings(role,s,now,r))]
    if op in (1,2):
        if op==2:
            dest=d.get('des_area');a.require(type(dest)is int and 1<=dest<=s['boss'] and dest in HANG,'该层尚未解锁');s['layer']=dest
        s['pending_news']=[]
        return [response(op,**hook(s,now,r))]
    if op==15:
        pending=copy.deepcopy(s.get('pending_news',[]));s['pending_news']=[]
        return [response(15,new_list=pending,specter_info=specter(s,now))]
    if op==9:return [response(9,day_record=dict(fight_count=s['fight_count'],now_fight_len=0,win_rate=100,
        crystals=s['earned'],item_count=s['item_count'],event_count=s['events_finished']),specter_info=specter(s,now))]
    if op==10:return [response(10,bag_info=bag(s,r))]
    if op==5:
        a.require(s['bag'],'临时背包为空')
        grant(role,s,[[p['object_type'],p['attach_type'],p['attach_count'],p['attach_level']] for p in s['bag']]);s['bag']=[]
        return [response(5,result=1,bag_info=bag(s,r)),response(10,bag_info=bag(s,r))]
    if op==11:
        a.require(s['grid_count']<60,'临时背包已满级');a.spend(role,'gold_coin',r['abyss_grid_gold']);s['grid_count']+=1
        return [response(11,bag_info=bag(s,r))]
    if op==14:
        n=d.get('buy_hour');a.require(type(n)is int and 1<=n<=48 and max(now,s['double_end'])+3600*n-now<=48*3600,'双倍挂机最多48小时')
        a.spend(role,'gold_coin',r['abyss_double_gold']*n)
        if now>=s['double_end']:s['double_start']=now
        s['double_end']=max(now,s['double_end'])+3600*n
        return [response(14,tool_rate=2,tool_end_time=s['double_end'],output_time_rate=2)]
    if op in (12,13):
        if op==12:
            i,n=d.get('index'),d.get('count',1)
            a.require(type(i)is int and 1<=i<=len(r['abyss_shop']) and type(n)is int and n>0,'九幽兑换参数无效')
            p=r['abyss_shop'][i-1];used=s['purchases'].get(str(i),0)
            a.require(used+n<=p['limit'] and s['crystals']>=p['cost']*n,'魂晶或兑换次数不足')
            s['crystals']-=p['cost']*n;s['purchases'][str(i)]=used+n;reward=p['reward']
            gain=a.prizes(role,[[reward[0],reward[1],reward[2]*n,reward[3]]]);gain[0]['buy_times']=p['limit']-used-n;gain[0]['crystals']=p['cost']
            return [response(12,index=i,attach_list=gain,specter_info=specter(s,now),crystal_count=s['crystals'])]
        return [response(13,shop_list=shop(s,r))]
    if op==16:return [response(16,**boss(role,s,now))]
    if op==17:
        a.require(not s.get('complete'),'九幽已通关，无需继续用药')
        tid,slot=d.get('type_id'),d.get('index')
        a.require(type(tid)is int and type(slot)is int and 1<=slot<=6 and s['pills'].get(str(slot))!=tid,'药品或药槽参数无效')
        if slot<=4:
            a.require(tid in PILLS,'请选择普通属性药品')
            entries=[list(map(int,x.split('|'))) for x in PILLS[tid].split('/')]
            a.require(all(x[0]==slot for x in entries),'药品不适用于此药槽')
        else:
            a.require(tid in combat.DRUGS,'请选择精魄药品')
            before=combat.effects(BOSSES[s['boss']],s['pills'])
            after=combat.effects(BOSSES[s['boss']],dict(s['pills'],**{str(slot):tid}))
            a.require(any(after[k]<v for k,v in before.items()),'该药品不能进一步削弱当前冥仙精魄')
        a.consume(role,tid,1);s['pills'][str(slot)]=tid
        # [B] Replacing a slot discards its previous effect; recompute reductions
        # against unmodified boss stats, preventing repeated multiplicative use.
        s['reductions']=[0]*4;base=enemies(s)
        for used in s['pills'].values():
            if used not in PILLS:continue
            for token in PILLS[used].split('/'):
                idx,value,rate=map(int,token.split('|'))
                stat=sum(u[('gongji','fangyu','hp','magic')[idx-1]] for u in base)
                s['reductions'][idx-1]+=stat*value//100 if rate else value
        return [response(17,**boss(role,s,now))]
    if op==6:
        a.require(s['boss_count']<5 and not s.get('complete'),'今日冥仙挑战次数已满或已经通关九幽')
        a.require(any(c.get('order') for c in role['corteges']),'请先上阵神仙')
        ours,_=journey.fighters(role,dict(cortege_list=f"{r['battle_npc']}|1"));extras=combat.effects(BOSSES[s['boss']],s['pills']);fight_events=[]
        if extras:
            result,lineup,actions,fight_events=combat.battle(role,(ours,enemies(s)),jrules,extras,r['abyss_boss_max_actions'])
        else:result,lineup,actions=journey.battle(role,{},jrules,units=(ours,enemies(s)))
        s['boss_count']+=1;win=1<=result<=3;gain=[]
        if win:
            specs=[]
            for token in BOSSES[s['boss']]['prirze_list'].split('/'):
                typ,tid,lv,n=map(int,token.split('|'));specs.append([typ,tid,n,lv])
            gain=grant(role,s,specs)
            record=dict(tip=f"{role['role_name']}击败第{s['boss']}层冥仙。",tip_type=3,time=now)
            s.setdefault('fight_news',[]).append(record);s['fight_news']=s['fight_news'][-20:]
            news(s,record['tip'],now)
            s['complete']=s['boss']==max(BOSSES);s['boss']=min(max(BOSSES),s['boss']+1);s['pills']={};s['reductions']=[0]*4
        role['activity']['fight_id']+=1;fid=role['activity']['fight_id']
        extra_packet=journey.combat_engine.event_packets(actions,fid)[0]
        return [extra_packet,encode(1028,dict(fight_id=fid,first_hand=1,des_name='冥仙',lineup_count=len(lineup),lineup=lineup)),
            encode(1027,dict(fight_id=fid,fight_type=26,final_result=result,fight_round=len(actions),fight_result=actions)),
            response(6,is_win=win,prize_list=gain,**boss(role,s,now)),summon.event(44,dict(fight_id=fid,fight_type=26))]
    a.require(False,'该九幽操作尚缺可验证的服务端配置')
