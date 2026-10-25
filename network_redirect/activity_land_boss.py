"""逐鹿首领、翻牌、扫荡、符咒合成 [A] contracts / [B] missing server rules."""
import copy
import secrets
from . import activity as a, summon
from . import activity_land as land


def boss(s,r,hell=False,layer=None):
    passed=s['inv_boss_layer' if hell else 'boss_layer'];layer=layer or min(passed+1,r['land_boss_layers'])
    return dict(boss_layer=layer,type_id=r['battle_npc'],fight_power=layer*300,cortege_count=min(8,1+(layer-1)//8),
        need_soul=r['land_boss_soul']*layer,score=layer*100,isweeken=False,is_open=not hell or layer in s['unlocked'],
        unlock_layer=layer,unlock_soul=r['land_hell_unlock_soul'],can_fight_count=r['land_hell_daily']-s['hell_counts'].get(str(layer),0),
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
            land.travel(s,r);target=s['travel'][0];result,_=land.simulate(role,s,r,jrules,target['level']);s['travel']=None
            if 1<=result<=3:
                wins+=1;s['soul_count']+=r['land_travel_soul'];kind=secrets.randbelow(4)+1;land.charm(s,kind,5,1);gains[kind]=gains.get(kind,0)+1
        return [response(22,win_count=wins,reward_soul=wins*r['land_travel_soul'],prize_list=[],
            reward_charm={k:{5:n} for k,n in gains.items()})]
    if op in (12,24):return [response(op,**query(s,r,op==24))]
    if op==26:
        idx=d.get('index');a.require(type(idx)is int and 1<=idx<=min(s['boss_layer'],s['inv_boss_layer']+1) and idx not in s['unlocked'],'冥界首领尚未解锁或已解锁')
        a.spend(s,'soul_count',r['land_hell_unlock_soul']);s['unlocked'].append(idx)
        return [response(26,index=idx)]
    if op==4 and d.get('des_type') in (3,4):
        hell=d['des_type']==4;key='hell' if hell else 'boss';progress='inv_boss_layer' if hell else 'boss_layer';history='inv_history' if hell else 'history'
        layer,n=d.get('des_id'),d.get('cur_num')
        a.require(type(layer)is int and 1<=layer<=min(r['land_boss_layers'],s[progress]+1) and d.get('flag')==1,'首领目标无效')
        a.require(s[key] is None,'请先完成或放弃上一轮翻牌')
        a.require(type(n)is int and 1<=n<=s['grid_count'],'参战神仙数量无效')
        row=boss(s,r,hell,layer)
        if hell:
            a.require(layer in s['unlocked'] and row['can_fight_count']>0,'冥界未解锁或挑战次数不足')
            s['hell_counts'][str(layer)]=s['hell_counts'].get(str(layer),0)+1
        a.spend(s,'soul_count',row['need_soul'])
        result,replay=land.simulate(role,s,r,jrules,layer*(3 if hell else 2),row['cortege_count'],n);win=1<=result<=3
        old=s[history].get(str(layer),{});score=layer*100+(s['grid_count']-n)*10
        newscore=max(old.get('score',0),score) if win else old.get('score',0)
        reward=win and layer>s[progress]
        if win:
            s['total_score']+=newscore-old.get('score',0);s[history][str(layer)]=dict(score=newscore,cur_num=n)
        if reward:
            s[key]=dict(layer=layer,cards=[],rewards=[copy.deepcopy(secrets.choice(r['land_card_rewards'])) for _ in range(3 if hell else 5)])
        return [summon.event(121,replay['fight_events']),response(4,fight_type=4 if hell else 3,des_level=layer,is_win=win,is_reward=reward,
            return_soul=0,card_list=[],cost_gold_list=r['land_card_gold'],final_result_list=[replay])]
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
            p=copy.deepcopy(r['land_card_rewards'][0]);gains.append(dict(layer=layer,prize_list=a.prizes(role,[p])))
        return [response(13,sweep_list=gains)]
    if op in (28,29):
        # Original enum has no active request caller; return persisted history only.
        return [response(op,history=query(s,r,op==29)['data']['history'])]
    a.require(False,'逐鹿操作无效')
