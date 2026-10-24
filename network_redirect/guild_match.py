"""Local and cross-area guild tournament state [B], original UI envelopes [A]."""
from . import guild as u,daily,journey,summon
from .protocol import encode


def state(s,cross=False):
    key='cross_match' if cross else 'match'
    m=s.setdefault(key,{})
    if m.get('day')!=s['day']:m.update(day=s['day'],signed=cross,fights=0,wins=0,score=0,claimed=False,bets={},records=[],purchases={})
    return m


def enter(role,s,g,now,r,cross=False):
    m=state(s,cross);start=s['day']*86400-r['timezone_offset_hours']*3600
    stats=dict(match_type=1 if m['signed'] else 5,group_type=7,win_count=m['wins'],lose_count=m['fights']-m['wins'],score=m['score'],life_point=max(0,100-m['fights']*5))
    return dict(area_name='本地区',union_data=stats,owner_data=stats,time_info=dict(begin_time=start,end_time=start+86400),has_match_flag=m['signed'],
        against_data=dict(src=dict(light_up=True,union_name=g['name'],area_name='本地区',life_point=100),des=dict(light_up=True,union_name='离线演武盟',area_name='离线区',life_point=100)))


def targets(role,s,g,r,cross=False):
    m=state(s,cross)
    rows=[dict(index=i,id=90000+i,role_id=90000+i,name='演武守卫'+str(i),level=r['battle_level'],rank=5,head_type=r['battle_npc'],cortege_layer=0,life_point=100,action_point=10,win_count=0,total_count=0,score_point=0,combat_power=1000,order=i) for i in range(1,7)]
    return dict(result=1,des_member_list=rows,top_member_list=rows,src_union_name=g['name'],des_union_name='离线演武盟',
        src_union_life=100,des_union_life=100,my_action_point=max(0,r['battle_daily']-m['fights']),my_life_point=100,
        my_win_count=m['wins'],my_keep_win_count=m['wins'],score_point=m['score'],get_contrib=0,rank_name='盟员',fight_result=1)


def query(role,s,g,d,now,r,cross=False):
    op=58 if cross else 18;q=d['query_type'];m=state(s,cross)
    mapping={20:8,21:9,22:10,23:13,24:16,25:17,26:18,27:19,28:12,30:100,32:100}
    typ=mapping.get(q,q);out=dict(query_type=q,result=1)
    if cross and q==30:
        out.update(union_list={g['id']:dict(u.info(g,r),order=1,leaderid=role['role_id'],leader_name=role['role_name'],score=m['score'])},last_champion={})
    elif typ==100:out['enter_data']=enter(role,s,g,now,r,cross)
    elif typ in (11,12,13):out.update(targets(role,s,g,r,cross))
    elif typ==9:out.update(schedule_list=dict(champion_list=[],match_member=[],begin_time=now,end_time=now+86400),had_signup=m['signed'],match_list=[])
    elif typ==8:
        pair=enter(role,s,g,now,r,cross)['against_data']
        for side,ident in (('src',g['id']),('des',90001)):pair[side].update(union_id=ident,id=ident,order=1,score=0)
        out.update(lineup_list={i:[pair] for i in range(1,8)},bet_info_list={i:{1:dict(silver_count=0,pantao_count=0)} for i in range(1,8)},match_type=1)
    elif typ in (10,18):out.update(teams=[],champion_list=[],lineup_list=[])
    elif typ==17:out.update(member_score={1:[],2:[]},src_direction=1,des_direction=2)
    elif typ==19:out.update(member_list=[dict(name=role['role_name'],score_point=m['score'],win_count=m['wins'],total_count=m['fights'],prize_count=1)])
    elif typ==16:out.update(union_score=dict(my_order=1,top_list=[dict(order=1,union_name=g['name'],score=m['score'],life_point=100)]))
    elif cross and q in (29,31):out['lineup_info']=lineup(role,d.get('des_id',role['role_id']),r)
    elif typ==33:out.update(score=m['score'],shop_list=shop(m,r))
    else:u.require(False,'仙盟赛程查询参数无效')
    return [u.reply(op,out)]


def shop(m,r):
    return [dict(need_score=0,attach_data=dict(daily.spec(p),cost=10,buy_times=max(0,5-m['purchases'].get(str(i),0)))) for i,p in enumerate(r['match_rewards'],1)]


def settle(role,s,g,op,d,now,r):
    cross=op in (58,62,63,76);m=state(s,cross)
    if op==58:
        if d.get('query_type')==28:
            return fight(role,s,g,dict(fight_type=17,des_id=u.positive(d,'des_id')),now,r,journey.load_rules())
        if d.get('query_type')==34:
            idx=u.positive(d,'index',len(r['match_rewards']));n=u.positive(d,'count',5)
            u.require(m['score']>=10*n and m['purchases'].get(str(idx),0)+n<=5,'战场积分或购买次数不足')
            m['score']-=10*n;m['purchases'][str(idx)]=m['purchases'].get(str(idx),0)+n
            p=list(r['match_rewards'][idx-1]);p[2]*=n;prize=journey.grant(role,p)
            return [u.reply(58,dict(query_type=34,result=1,score=m['score'],attach_list=[prize]))]
        return query(role,s,g,d,now,r,True)
    if op==45:
        u.authorize(role,r,18);u.require(not m['signed'],'已经报名');m['signed']=True
        return [u.notice(op),u.reply(18,dict(query_type=100,enter_data=enter(role,s,g,now,r)))]
    if op==46:return [u.reply(18,dict(query_type=11,**targets(role,s,g,r)))]
    if op in (47,62):return [u.reply(op,dict(result=1,bet_list={},lineup_list={},bet_info_list={},match_type=1))]
    if op in (48,63):
        u.authorize(role,r,22 if cross else 19);typ=u.positive(d,'bet_type',2);ident=u.positive(d,'union_id')
        u.require(ident in (g['id'],90001) and str(typ) not in m['bets'],'押注目标无效或已押注')
        u.pay(role,'silver_coin',1000 if typ==1 else 5000);m['bets'][str(typ)]=ident
        return [u.notice(op),u.reply(47 if op==48 else 62,dict(result=1,bet_list=m['bets']))]
    if op in (72,76):
        u.require(m['fights']>0 and not m['claimed'],'尚未参赛或奖励已领取')
        row=next(v for v in summon.rows('union_match_prize.csv') if int(v['group_type'])==7 and int(v['min_order'])==1)
        prizes=[]
        for token in row['prize_list'].split('/'):
            typ,tid,level,count=map(int,token.split('|'));prizes.append(journey.grant(role,[typ,tid,count,level]))
        g['popularity']+=int(row['popularity']);m['claimed']=True
        for typ,ident in m['bets'].items():
            if ident==(g['id'] if m['wins']*2>=m['fights'] else 90001):
                prizes.append(journey.grant(role,[12,0,2*(1000 if typ=='1' else 5000),1]))
        return [u.reply(op,dict(result=1,prize_list=prizes))]
    u.require(False,'仙盟赛程操作无效')


def fight(role,s,g,req,now,r,jrules):
    from .guild_combat import simulate
    cross=req['fight_type'] in (17,23,24,32,33);m=state(s,cross)
    u.authorize(role,r,3);u.require(m['signed'],'请先报名仙盟战');u.require(m['fights']<r['battle_daily'],'行动力不足')
    target=int(req['des_id']);u.require(target in range(90001,90007),'对手不存在')
    result,packets,replay=simulate(role,s,r,jrules,req['fight_type'],'离线演武盟')
    m['fights']+=1;win=1<=result<=3;m['wins']+=int(win);m['score']+=10 if win else 1
    gain=u.contribution(role,10 if win else 2);m['records'].append(replay);m['records']=m['records'][-10:]
    out=targets(role,s,g,r,cross);out.update(query_type=28 if cross else 12,fight_result=result,get_contrib=gain)
    return packets+[u.reply(58 if cross else 18,out),summon.event(44,dict(fight_id=s['fight_id'],fight_type=req['fight_type']))]


def lineup(role,ident,r):
    import copy
    own=ident==role['role_id']
    chars=copy.deepcopy([c for c in role['corteges'] if c.get('order')]) if own else [dict(c,id=ident,evolve_level=0,reborn_layer=0) for c in journey.fighters(role,dict(cortege_list=f"{r['battle_npc']}|{r['battle_level']}"))[1]]
    for c in chars:
        c.pop('skills',None)
        c.update(type_id=c['type'],max_hp_show=c['hp'],max_magic_show=c['magic'],wuligongji_show=c['gongji'],wulifangyu_show=c['fangyu'])
    return dict(role_id=ident,role_name=role['role_name'] if own else '离线仙盟对手',level=role['level'] if own else r['battle_level'],vip_level=0,head_type=5004,rank=0,owner_cheer_info={},title_info={},animal_info={},hole_train={},cortege_list=chars,cheer_cortege=[],skill_list=[],equip_list=[],ext_skill_list=[],ext_star_list=[])
