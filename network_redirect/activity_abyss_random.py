"""九幽五类随机事件：客户端玩法/字段 [A]，发生频率与奖池 [B]。"""
import copy
import secrets
from . import activity as a, journey, summon
from .protocol import encode
SOUL_NPCS=(7221,7222,7223)  # [A] cortege_base_0: name=jiuyousuiji


def create(kind,r):
    e=dict(kind=kind)
    if kind==1:e.update(answer=secrets.randbelow(99)+1,minimum=0,maximum=100,left=4)
    if kind==3:e.update(hp=r['abyss_event_boss_hp'],max_hp=r['abyss_event_boss_hp'],attempts=0,
                        npc_type=secrets.choice(SOUL_NPCS),level=1)
    if kind==5:
        choices=list(r['abyss_eye_choices']);secrets.SystemRandom().shuffle(choices)
        e.update(choices=choices,answer=secrets.choice(choices))
    return e


def accrue(s,now,r):
    s.setdefault('events',[]);s.setdefault('last_event',now);s.setdefault('events_finished',0)
    elapsed=max(0,now-s['last_event']);ticks=elapsed//r['abyss_event_seconds']
    count=min(ticks,5-len(s['events']))
    for _ in range(count):
        event=create(secrets.randbelow(5)+1,r)
        if event['kind']==3:
            # [B] Soul encounter level follows the hanging floor; keep the
            # original monster growth and a minimum encounter HP budget.
            event['level']=s['layer'];row=journey.NPCS[event['npc_type']]
            event['hp']=event['max_hp']=max(r['abyss_event_boss_hp'],int(float(row['base_max_hp'])+
                float(row['base_maxhp_plus'])*(event['level']-1)))
        s['events'].append(event)
    if count:
        from .activity_abyss import news
        # The client updates its event badge only for type-4 tips.
        news(s,'九幽随机事件已积累，请及时查看。',now)
        s['news'][-1]['tip_type']=s['pending_news'][-1]['tip_type']=4
    if ticks:s['last_event']=now-elapsed%r['abyss_event_seconds']


def view(e,r):
    data=dict(event_type=e['kind'])
    if e['kind']==1:data.update(min_num=e['minimum'],max_num=e['maximum'],left_times=e['left'])
    if e['kind']==2:data.update(item_list=[a.prize_spec(p) for p in r['abyss_event_rewards']],
        consume_list=[a.prize_spec(p) for p in r['abyss_pray_consumes']])
    if e['kind']==3:data.update(boss_info=dict(is_dead=e['hp']==0,hp=e['hp'],max_hp=max(e['hp'],e.get('max_hp',r['abyss_event_boss_hp'])),
        free_times=max(0,3-e['attempts']),cortege_type=e.get('npc_type',7221),level=e.get('level',1),
        star=int(journey.NPCS[e.get('npc_type',7221)]['quality'])),
        attach_list=[a.prize_spec(p) for p in r['abyss_event_rewards']],consume_item=a.prize_spec([5,1023,1,1]),cost_gold=r['abyss_event_fight_gold'])
    if e['kind']==5:data.update(cortege_type=e['answer'],cortege_list=e['choices'])
    return data


def settle(role,s,d,now,r,jrules):
    from .activity_abyss import response, grant, news
    op=d.get('op_type');a.require(type(op)is int and op in (0,1,2),'随机事件操作无效')
    a.require(s['events'],'暂无随机事件')
    e=s['events'][0];kind=e['kind'];data=view(e,r);packets=[];done=False;won=False
    if op==0:e['opened']=True
    else:a.require(e.get('opened'),'请先查看当前随机事件')
    if op==2:data.update(op_type=2,sucess=True);done=True
    elif kind==4:
        a.require(op==0,'妙手空空无需提交选择')
        lost=min(s['crystals'],secrets.randbelow(r['abyss_steal_max']+1));s['crystals']-=lost
        data.update(steal_count=lost,crystal_count=s['crystals']);done=True
    elif op==1:
        if kind==1:
            num=d.get('num')
            if isinstance(num,str) and num.isdecimal() and len(num)<=3:num=int(num)
            a.require(type(num)is int and e['minimum']<num<e['maximum'] and e['left']>0,'请输入提示范围内的整数')
            e['left']-=1;won=num==e['answer']
            if num<e['answer']:e['minimum']=num
            if num>e['answer']:e['maximum']=num
            data=view(e,r);data['is_win']=won;done=won or e['left']==0
        elif kind==5:
            chosen=d.get('cortege_type');a.require(type(chosen)is int and chosen in e['choices'],'神仙选项无效')
            won=chosen==e['answer'];data['is_right']=won;done=True
        elif kind==2:
            index=d.get('index');a.require(type(index)is int and 1<=index<=len(r['abyss_pray_consumes']),'祈福物品无效')
            typ,tid,n,_=r['abyss_pray_consumes'][index-1]
            if typ==5:a.consume(role,tid,n)
            else:a.spend(role,'gold_coin' if typ==11 else 'silver_coin',n)
            won=True;done=True
        elif kind==3:
            a.require(any(c.get('order') for c in role['corteges']),'请先上阵神仙')
            if e['attempts']>=3:
                have=sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==1023 and not i.get('is_lock'))
                if have:a.consume(role,1023,1)
                else:a.spend(role,'gold_coin',r['abyss_event_fight_gold'])
            ours,enemies=journey.fighters(role,dict(cortege_list=f"{e.get('npc_type',7221)}|{e.get('level',1)}"))
            enemies=enemies[:1];enemies[0].update(hp=e['hp'],max_hp=max(e['hp'],e.get('max_hp',r['abyss_event_boss_hp'])))
            result,lineup,actions=journey.battle(role,{},jrules,units=(ours,enemies))
            damage=journey.combat_engine.total_damage(actions)
            e['hp']=max(0,e['hp']-damage);e['attempts']+=1;won=e['hp']==0;done=won;data=view(e,r)
            role['activity']['fight_id']+=1;fid=role['activity']['fight_id']
            packets=journey.combat_engine.event_packets(actions,fid)+[encode(1028,dict(fight_id=fid,first_hand=1,des_name='魂仙',lineup_count=len(lineup),lineup=lineup)),
                encode(1027,dict(fight_id=fid,fight_type=25,final_result=result,fight_round=len(actions),fight_result=actions))]
    if won:data['prize_list']=grant(role,s,[copy.deepcopy(secrets.choice(r['abyss_event_rewards']))])
    if done:
        s['events'].pop(0);s['events_finished']+=1
        news(s,'随机事件已结束，剩余'+str(len(s['events']))+'个。',now)
        s['news'][-1]['tip_type']=s['pending_news'][-1]['tip_type']=4
    packets.append(response(4,event_data=data))
    if kind==3 and op==1:packets.append(summon.event(44,dict(fight_id=fid,fight_type=25)))
    return packets
