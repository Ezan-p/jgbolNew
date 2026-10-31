"""逐鹿首领、翻牌、扫荡、符咒合成 [A] contracts / [B] missing server rules."""
import copy
import secrets
import math
from . import activity as a, summon, activity_land_encounters as encounters
from . import activity_land as land
from .activity_land_rewards import draw_cards


def score(s,n):
    # [A] landUI L117-123 and calcFightScore L2047-2076, including
    # constants recovered from the original LuaJIT number pool.
    value=3000-(0,150,300,420,480,600,750,900)[n-1]
    for kind,factor in enumerate((20,25,15,30),1):
        count=sum(c['key']==kind and c['unlock'] and c['is_open'] for c in s['charms'].values())
        value-=math.floor((count+count**1.2)*0.5*factor)
    return max(0,value)


def migrate_scores(s):
    if s.get('score_version')==2:return
    for key in ('history','inv_history'):
        for row in s[key].values():
            # [B] Old saves did not record equipped charms at battle time.
            # Keep the old value for audit; do not increase a historical score.
            row['legacy_score']=row['score']
            row['score']=min(row['score'],score(dict(charms={}),row['cur_num']))
    s['total_score']=sum(row['score'] for key in ('history','inv_history') for row in s[key].values())
    s['score_version']=2


def migrate_inverse(s,r):
    """Apply normal-tower auto unlocks and restore older inverse progress."""
    unlocked=set()
    raw_unlocked=s.get('unlocked',[])
    for value in raw_unlocked if isinstance(raw_unlocked,(list,tuple,set)) else ():
        if type(value) is int and 1<=value<=r['land_boss_layers']:
            unlocked.add(value)
    # Native land_tip5 promises automatic opening at unlock_layer. The local
    # rule maps each inverse floor to the same cleared normal floor.
    normal=s.get('boss_layer',0)
    if type(normal) is int and normal>0:
        unlocked.update(range(1,min(normal,r['land_boss_layers'])+1))
    # A cleared inverse layer could only have been reached after its unlock.
    # Older saves did not persist the separate unlock list, so derive it from
    # the authoritative progress/history fields.
    progress=s.get('inv_boss_layer',0)
    if type(progress) is int and progress>0:
        unlocked.update(range(1,min(progress,r['land_boss_layers'])+1))
    history=s.get('inv_history',{})
    for key in history if isinstance(history,dict) else ():
        try:layer=int(key)
        except (TypeError,ValueError):continue
        if 1<=layer<=r['land_boss_layers']:
            unlocked.add(layer)
    s['unlocked']=sorted(unlocked)
    s.setdefault('hell_counts',{})


def boss(s,r,hell=False,layer=None):
    passed=s['inv_boss_layer' if hell else 'boss_layer'];layer=layer or min(passed+1,r['land_boss_layers'])
    enemy=encounters.encounter(layer,hell)
    counts=s.get('hell_counts',{})
    used=counts.get(str(layer),0)
    if type(used) is not int:used=0
    remaining=max(0,r['land_hell_daily']-used) if hell else r['land_hell_daily']
    opened=not hell or layer in s.get('unlocked',[])
    return dict(boss_layer=layer,type_id=enemy['type_id'],name=enemy['name'],fight_power=enemy['power'],cortege_count=len(enemy['units']),
        need_soul=r['land_boss_soul']*layer,score=score(s,s['grid_count']),isweeken=False,is_open=opened,
        # landUI L2410 requires this flag to render the paid unlock button.
        unlock=hell and not opened and layer<=passed+1,
        unlock_layer=layer,unlock_soul=r['land_hell_unlock_soul'],can_fight_count=remaining,
        fight_count_limit=r['land_hell_daily'],cur_num=s['grid_count'])


def query(s,r,hell=False):
    key='hell' if hell else 'boss';pending=s[key];history=s['inv_history' if hell else 'history']
    data=dict(boss_info=boss(s,r,hell),history={int(k):dict(boss(s,r,hell,int(k)),**v) for k,v in history.items()},
        is_clear=s['inv_boss_layer' if hell else 'boss_layer']>=r['land_boss_layers'],is_sweep=not s['swept'] and s['boss_layer']>0,
        card_info=copy.deepcopy(pending['cards']) if pending else [],cost_gold_list=r['land_card_gold'])
    return dict(is_turn_card=pending is not None,data=data)


def selection(data):
    value=data.get('charm_info')
    if isinstance(value,dict):
        a.require(set(value)==set(range(1,len(value)+1)),'符咒选择索引无效');value=list(value.values())
    a.require(isinstance(value,list) and all(isinstance(x,dict) and type(x.get('key'))is int and 1<=x['key']<=4 and type(x.get('value'))is int and x['value'] in land.CONVERT for x in value),'符咒选择无效')
    return value


def settle(role,s,op,d,now,r,jrules):
    response=lambda op,**data:land.response(op,s,r,**data)
    if op in (19,20):
        selected=selection(d)
        if op==20:
            a.require(len(selected)==2,'请选择来源和目标符咒');src,dest=selected
            a.require(src['key']!=dest['key'] and src['value']==dest['value'],'转换需要同级不同属性')
            land.charm(s,src['key'],src['value'],-1);a.spend(s,'soul_count',int(land.CONVERT[src['value']]['convert_cost']))
            land.charm(s,dest['key'],dest['value'],1)
            return [response(20,charm_get=land.bag(s))]
        a.require(2<=len(selected)<=4 and selected[0]['value']<max(land.CONVERT),'请选择2至4张符咒，主符咒不能已满级')
        src=selected[0];power=sum(int(land.CONVERT[x['value']]['compose_value']) for x in selected)
        target=src['value']+5;need=int(land.CONVERT[target]['compose_value'])
        for x in selected:land.charm(s,x['key'],x['value'],-1)
        success=secrets.randbelow(need)<min(power,need);critical=success and target<max(land.CONVERT) and secrets.randbelow(100)<int(land.CONVERT[src['value']]['critical_chance'])
        # [B] Retain the principal charm on failure, consume donors.
        land.charm(s,src['key'],target+5 if critical else target if success else src['value'],1)
        return [response(19,result=3 if critical else 1 if success else 2,charm_get=land.bag(s))]
    if op==22:
        a.require(land.status(now,r)['cur_status']==1 and not s['travel'],'请先结束当前游历')
        n=min(5,r['land_daily_travel']-s['travel_count']);a.require(n>0,'今日游历次数已满');wins=0;gains={}
        for _ in range(n):
            land.travel(s,r,role);target=s['travel'][0];result,_=land.simulate(role,s,r,jrules,target['level'],target=target.get('npc_id'));s['travel']=None
            if 1<=result<=3:
                wins+=1;land.gain(s,r['land_travel_soul']);kind=secrets.randbelow(4)+1;land.charm(s,kind,5,1);gains[kind]=gains.get(kind,0)+1
        land.news(s,now,f'批量游历{n}次，获胜{wins}次，获得{wins*r["land_travel_soul"]}魂力。')
        return [response(22,win_count=wins,reward_soul=wins*r['land_travel_soul'],prize_list=[],
            reward_charm={k:{5:n} for k,n in gains.items()})]
    if op in (12,24):return [response(op,**query(s,r,op==24))]
    if op==26:
        # Paid opening is the alternative to waiting for normal-tower progress;
        # still require sequential inverse progression and reject duplicates.
        idx=d.get('index');a.require(type(idx)is int and 1<=idx<=min(r['land_boss_layers'],s['inv_boss_layer']+1) and boss(s,r,True,idx)['unlock'],'冥界首领尚未解锁或已解锁')
        a.spend(s,'soul_count',r['land_hell_unlock_soul']);s['unlocked'].append(idx)
        return [response(26,index=idx)]
    if op==4 and d.get('des_type') in (3,4):
        hell=d['des_type']==4;key='hell' if hell else 'boss';progress='inv_boss_layer' if hell else 'boss_layer';history='inv_history' if hell else 'history'
        layer,n=d.get('des_id'),d.get('cur_num')
        a.require(type(layer)is int and 1<=layer<=min(r['land_boss_layers'],s[progress]+1) and d.get('flag')==1,'首领目标无效')
        a.require(s[key] is None,'请先完成或放弃上一轮翻牌')
        a.require(type(n)is int and 1<=n<=s['grid_count'],'参战神仙数量无效')
        a.require(n<=sum(1 for c in role['corteges'] if 1<=c.get('order',0)<=8),'实际参战神仙不足')
        row=boss(s,r,hell,layer)
        if hell:
            a.require(layer in s['unlocked'] and row['can_fight_count']>0,'冥界未解锁或挑战次数不足')
            s['hell_counts'][str(layer)]=s['hell_counts'].get(str(layer),0)+1
        a.spend(s,'soul_count',row['need_soul'])
        encounter=encounters.encounter(layer,hell)
        result,replay=land.simulate(role,s,r,jrules,encounter['level'],row['cortege_count'],n,
                                  encounter=encounter);win=1<=result<=3
        old=s[history].get(str(layer),{});earned=score(s,n)
        newscore=max(old.get('score',0),earned) if win else old.get('score',0)
        reward=win and layer>s[progress]
        if win:
            s['total_score']+=newscore-old.get('score',0)
            if not old or earned>old['score']:
                s[history][str(layer)]=dict(score=newscore,cur_num=n)
        land.news(s,now,f"{'冥界' if hell else '普通'}首领第{layer}层：{'胜利' if win else '未获胜'}。")
        if reward:
            rewards=draw_cards(r,3 if hell else 5)
            s[key]=dict(layer=layer,cards=[],rewards=copy.deepcopy(rewards))
        return land.replay_response(4,s,r,replay,fight_type=4 if hell else 3,des_level=layer,is_win=win,is_reward=reward,
            return_soul=0,card_list=[],cost_gold_list=r['land_card_gold'])
    if op in (14,23):
        key='hell' if op==23 else 'boss';pending=s[key];idx=d.get('index')
        a.require(pending is not None and type(idx)is int and 1<=idx<=(3 if op==23 else 5) and all(x['position']!=idx for x in pending['cards']),'翻牌位置无效或已翻开')
        a.spend(role,'gold_coin',r['land_card_gold'][len(pending['cards'])]);gain=a.prizes(role,[pending['rewards'][idx-1]])[0]
        pending['cards'].append(dict(position=idx,attach_data=gain))
        extra=a.prizes(role,r['land_full_card_rewards']) if len(pending['cards'])==len(pending['rewards']) else []
        return [response(op,index=idx,attach_data=gain,extra_prize_list=extra)]
    if op in (15,25):
        hell=op==25;key='hell' if hell else 'boss';progress='inv_boss_layer' if hell else 'boss_layer'
        a.require(s[key] is not None,'没有待结算的首领');s[progress]=max(s[progress],s[key]['layer']);s[key]=None
        land.state(role,now,r)
        return [response(op,boss_info=boss(s,r,hell),is_sweep=not s['swept'])]
    if op==13:
        a.require(s['boss_layer']>0 and not s['swept'] and s['boss'] is None,'没有可扫荡首领或今日已扫荡')
        s['swept']=True;gains=[]
        for layer in range(1,s['boss_layer']+1):
            gains.append(a.prizes(role,r['land_sweep_rewards']))
        return [response(13,sweep_list=gains)]
    if op in (28,29):
        # Original enum has no active request caller; return persisted history only.
        return [response(op,history=query(s,r,op==29)['data']['history'])]
    a.require(False,'逐鹿操作无效')
