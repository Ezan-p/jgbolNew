"""Local and cross-area guild tournament state [B], original UI envelopes [A]."""
from . import guild as u,daily,journey,summon,npc_players,guild_npcs
from .protocol import encode


# The current UI uses match_type - 20 as its stage image number.
# Old union_match_type values (1/5) load z-19/z-15 and crash natively.
CLIENT_MATCH_STAGE = 21


def state(s,cross=False,r=None):
    life=r['match_life'] if r else 100
    key='cross_match' if cross else 'match'
    m=s.setdefault(key,{})
    if m.get('day')!=s['day'] and m.get('settlement'):
        m['history']=(m.get('history',[])+[dict(m['settlement'],day=m['day'])])[-14:]
    if m.get('day')!=s['day']:m.update(npc_roster=[],tournament_leaders=[],settlement=None,total_score=0,life=life,streak=0,max_streak=0,loss_streak=0,target_life={},merit=0,day=s['day'],signed=cross,fights=0,wins=0,score=0,claimed=False,bets={},records=[],purchases={})
    for k,v in dict(life=life,streak=0,max_streak=0,loss_streak=0,target_life={},merit=0).items():m.setdefault(k,v)
    m.setdefault('total_score',m['score'])
    return m


def enter(role,s,g,now,r,cross=False):
    m=state(s,cross,r);start=s['day']*86400-r['timezone_offset_hours']*3600
    stats=dict(match_type=CLIENT_MATCH_STAGE,group_type=7,win_count=m['wins'],lose_count=m['fights']-m['wins'],score=m['score'],life_point=m['life'])
    return dict(area_name='本地区',union_data=stats,owner_data=stats,time_info=dict(begin_time=start,end_time=start+86400),has_match_flag=m['signed'],
        against_data=dict(src=dict(light_up=True,union_name=g['name'],area_name='本地区',life_point=100),des=dict(light_up=True,union_name='离线演武盟',area_name='离线区',life_point=100)))


def targets(role,s,g,r,cross=False):
    m=state(s,cross,r)
    rows=[]
    for i,entry in enumerate(opponents(role,s,g,r,cross),1):
        p=entry['profile'];ident=p['role_id']
        rows.append(dict(index=i,id=ident,role_id=ident,npc_id=entry['npc_id'],name=p['role_name'],level=p['level'],rank=[1,7,2,3,4,5][i-1],head_type=p['head_type'],cortege_layer=p['reborn_layer'],life_point=m['target_life'].get(str(90000+i),r['match_life']),action_point=10,win_count=0,total_count=0,score_point=0,combat_power=p['role_combat_power'],order=i))
    return dict(result=1,des_member_list=rows,top_member_list=rows,src_union_name=g['name'],des_union_name='离线演武盟',
        src_union_life=m['life'],des_union_life=sum(v['life_point'] for v in rows),my_action_point=max(0,r['battle_daily']-m['fights']),my_life_point=m['life'],
        my_win_count=m['wins'],my_keep_win_count=m['streak'],max_win_streak_count=m['max_streak'],merit_point=m['merit'],score_point=m['score'],get_contrib=0,rank_name='盟员',fight_result=1)


def opponents(role,s,g,r,cross=False):
    """[B] Stable daily catalog armies; old scene IDs remain request aliases."""
    m=state(s,cross,r)
    if not m.get('npc_roster'):
        m['npc_roster']=[e['npc_id'] for e in guild_npcs.choose(s,role['level'],6,
                            excluded_ids=guild_npcs.occupied(s))]
    return [npc_players.catalog()[key] for key in m['npc_roster']]


def query(role,s,g,d,now,r,cross=False):
    op=58 if cross else 18;q=d['query_type'];m=state(s,cross,r)
    mapping={20:8,21:9,22:10,23:13,24:16,25:17,26:18,27:19,28:12,30:100,32:100}
    typ=mapping.get(q,q);out=dict(query_type=q,result=1)
    if cross and q==30:
        leader=next((v for v in g['members'].values() if v['rank']==1),None)
        out.update(union_list=[dict(u.info(g,r),order=1,leaderid=leader['id'] if leader else 0,score=m['score'])],last_champion=champions(role,s,g,r,cross)[0])
    elif typ==100:out['enter_data']=enter(role,s,g,now,r,cross)
    elif typ in (11,12,13):out.update(targets(role,s,g,r,cross))
    elif typ==9:out.update(schedule_list=dict(champion_list=champions(role,s,g,r,cross),match_member=tournament(role,s,g,r,cross),begin_time=s['day']*86400-r['timezone_offset_hours']*3600,end_time=(s['day']+1)*86400-r['timezone_offset_hours']*3600),had_signup=m['signed'],match_list=tournament(role,s,g,r,cross))
    elif typ==8:
        pair=enter(role,s,g,now,r,cross)['against_data']
        own_leader=next(v['id'] for v in g['members'].values() if v['rank']==1)
        enemy_leader=opponents(role,s,g,r,cross)[0]['profile']['role_id']
        for side,ident in (('src',g['id']),('des',90001)):pair[side].update(union_id=ident,id=ident,leader_id=own_leader if side=='src' else enemy_leader,match_type=CLIENT_MATCH_STAGE,level=g['level'] if side=='src' else 1,order=1,score=0)
        start=s['day']*86400-r['timezone_offset_hours']*3600
        out.update(bet_time_info=dict(begin_time=start,end_time=0 if m['fights'] or m['claimed'] else start+86400),bet_list={own_leader if ident==g['id'] else enemy_leader:True for ident in m['bets'].values()},lineup_list={i:[pair] for i in range(1,8)},bet_info_list={i:{1:dict(silver_count=0,pantao_count=0)} for i in range(1,8)},match_type=CLIENT_MATCH_STAGE)
    elif typ in (10,18):out.update(teams=tournament(role,s,g,r,cross),champion_list=champions(role,s,g,r,cross),lineup_list=tournament(role,s,g,r,cross))
    elif typ==17:out.update(member_score={1:[dict(name=role['role_name'],score_point=m['merit'],win_count=m['wins'],total_count=m['fights'])],2:targets(role,s,g,r,cross)['des_member_list']},src_direction=1,des_direction=2)
    elif typ==19:out.update(member_list=[dict(name=role['role_name'],score_point=m['score'],win_count=m['wins'],total_count=m['fights'],prize_count=1)])
    elif typ==16:out.update(union_score=dict(my_order=next(v['order'] for v in tournament(role,s,g,r,cross) if v['id']==g['id']),top_list=tournament(role,s,g,r,cross)))
    elif cross and q in (29,31):out['lineup_info']=lineup(role,d.get('des_id',role['role_id']),r,cross=True)
    elif typ==33:out.update(score=m['score'],shop_list=shop(m,r))
    else:u.require(False,'仙盟赛程查询参数无效')
    return [u.reply(op,out)]


def shop(m,r):
    return [dict(need_score=0,attach_data=dict(daily.spec(p),cost=10,buy_times=max(0,5-m['purchases'].get(str(i),0)))) for i,p in enumerate(r['match_rewards'],1)]


def settle(role,s,g,op,d,now,r):
    cross=op in (58,62,63,76);m=state(s,cross,r)
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
    if op in (47,62):return [u.reply(op,dict(result=1,bet_list=m['bets'],lineup_list={},bet_info_list={1:dict(silver_count=sum(1000 if k=='1' else 5000 for k in m['bets']),pantao_count=0)},match_type=1))]
    if op in (48,63):
        u.authorize(role,r,22 if cross else 19);u.require(m['fights']==0 and not m['claimed'],'开战后不能押注');typ=u.positive(d,'bet_type',2);ident=u.positive(d,'union_id')
        # The current detail panel submits the leader ID as union_id.
        if ident==next(v['id'] for v in g['members'].values() if v['rank']==1):ident=g['id']
        if ident==opponents(role,s,g,r,cross)[0]['profile']['role_id']:ident=90001
        u.require(ident in (g['id'],90001) and str(typ) not in m['bets'],'押注目标无效或已押注')
        u.pay(role,'silver_coin',1000 if typ==1 else 5000);m['bets'][str(typ)]=ident
        return [u.notice(op),u.reply(47 if op==48 else 62,dict(result=1,bet_list=m['bets']))]
    if op in (72,76):
        u.require(m['fights']>0 and not m['claimed'],'尚未参赛或奖励已领取')
        ranking=tournament(role,s,g,r,cross);order=next(v['order'] for v in ranking if v['id']==g['id'])
        row=next(v for v in summon.rows('union_match_prize.csv') if int(v['group_type'])==7 and int(v['min_order'])<=order<=int(v['max_order']))
        m['settlement']=dict(order=order,ranking=ranking,champion=ranking[0]['id'])
        prizes=[]
        for token in row['prize_list'].split('/'):
            typ,tid,level,count=map(int,token.split('|'));prizes.append(journey.grant(role,[typ,tid,count,level]))
        g['popularity']+=int(row['popularity']);m['claimed']=True
        for typ,ident in m['bets'].items():
            if ident==(g['id'] if next(v['score'] for v in ranking if v['id']==g['id'])>=next(v['score'] for v in ranking if v['id']==90001) else 90001):
                prizes.append(journey.grant(role,[12,0,2*(1000 if typ=='1' else 5000),1]))
        return [u.reply(op,dict(result=1,prize_list=prizes))]
    u.require(False,'仙盟赛程操作无效')


def fight(role,s,g,req,now,r,jrules):
    from .guild_combat import simulate
    cross=req['fight_type'] in (17,23,24,32,33);m=state(s,cross,r)
    u.authorize(role,r,3);u.require(m['signed'],'请先报名仙盟战');u.require(not m['claimed'],'本轮已结算，请次日再战');u.require(m['fights']<r['battle_daily'],'行动力不足');u.require(m['life']>0,'生命点不足')
    target=int(req['des_id']);roster=opponents(role,s,g,r,cross)
    selected=next((i for i,e in enumerate(roster) if e['profile']['role_id']==target),None)
    if selected is not None:target=90001+selected
    u.require(target in range(90001,90007),'对手不存在')
    u.require(m['target_life'].get(str(target),r['match_life'])>0,'目标已经退场')
    if req['fight_type']==16:u.require(target==90001,'盟主战请选择盟主')
    enemy=roster[target-90001]
    result,packets,replay=simulate(role,s,r,jrules,req['fight_type'],enemy['profile']['role_name'],enemy_npc=enemy['npc_id'])
    m['fights']+=1;win=1<=result<=3;m['wins']+=int(win)
    rank=[1,7,2,3,4,5][target-90001];merit=r['match_merit'][str(rank)]
    if win:
        m['streak']=min(r['match_max_streak'],m['streak']+1);m['max_streak']=max(m['max_streak'],m['streak']);m['loss_streak']=0
        m['merit']+=merit;m['score']+=merit*10
        m['target_life'][str(target)]=max(0,m['target_life'].get(str(target),r['match_life'])-r['match_target_loss'])
    else:m['life']=max(0,m['life']-r['match_loss_life']);m['streak']=0;m['loss_streak']+=1;m['score']+=1
    m['total_score']+=merit*10 if win else 1
    gain=u.contribution(role,merit*2 if win else 2);m['records'].append(replay);m['records']=m['records'][-10:]
    out=targets(role,s,g,r,cross);out.update(query_type=28 if cross else 12,fight_result=result,get_contrib=gain)
    return packets+[u.reply(58 if cross else 18,out),summon.event(44,dict(fight_id=s['fight_id'],fight_type=req['fight_type']))]


def lineup(role,ident,r,cross=False):
    import copy
    npc=npc_players.get(ident)
    s=role.get('guild',{});g=s.get('unions',{}).get(str(int(role.get('union_id',0))))
    if npc is None and g and ident in range(90001,90007):
        npc=npc_players.get(opponents(role,s,g,r,cross)[int(ident)-90001]['npc_id'])
    if npc is not None:
        data=npc_players.inspection_data(npc)
        data['role_id']=ident
        if g and str(ident) in g['members']:data['union_name']=g['name']
        return data
    own=ident==role['role_id']
    chars=copy.deepcopy([c for c in role['corteges'] if c.get('order')]) if own else [dict(c,id=ident,evolve_level=0,reborn_layer=0) for c in journey.fighters(role,dict(cortege_list=f"{r['battle_npc']}|{r['battle_level']}"))[1]]
    for c in chars:
        c.pop('skills',None)
        c.update(type_id=c['type'],max_hp_show=c['hp'],max_magic_show=c['magic'],wuligongji_show=c['gongji'],wulifangyu_show=c['fangyu'])
    from . import cheer
    data = dict(role_id=ident,role_name=role['role_name'] if own else '离线仙盟对手',level=role['level'] if own else r['battle_level'],vip_level=0,head_type=5004,rank=0,owner_cheer_info={},title_info={},animal_info={},hole_train={},cortege_list=chars,cheer_cortege=[],skill_list=[],equip_list=[],ext_skill_list=[],ext_star_list=[])
    data.update(cheer.inspection(role, own))
    return data


def tournament(role,s,g,r,cross=False):
    """Daily four-guild offline points cup; no fake online matchmaking."""
    m=state(s,cross,r)
    leader=next(v for v in g['members'].values() if v['rank']==1)
    rows=[dict(id=g['id'],union_id=g['id'],name=g['name'],union_name=g['name'],leader_id=leader['id'],leader_name=leader['name'],score=m['total_score'],life_point=m['life'],group_type=7)]
    roster=opponents(role,s,g,r,cross)
    if not m.get('tournament_leaders'):
        excluded=guild_npcs.occupied(s)|{e['profile']['role_id'] for e in roster}
        m['tournament_leaders']=[roster[0]['npc_id']]+[e['npc_id'] for e in guild_npcs.choose(s,role['level'],2,excluded_ids=excluded)]
    for i,name in enumerate(('离线演武盟','离线蓬莱盟','离线昆仑盟'),1):
        score=10+((s['day']+i+(3 if cross else 0))%4)*10
        p=npc_players.catalog()[m['tournament_leaders'][i-1]]['profile']
        rows.append(dict(id=90000+i,union_id=90000+i,name=name,union_name=name,leader_id=p['role_id'],leader_name=p['role_name'],score=score,life_point=100,group_type=7))
    rows.sort(key=lambda row:(-row['score'],row['id']))
    for i,row in enumerate(rows,1):row['order']=i
    return rows


def champions(role,s,g,r,cross=False):
    """[B] Current offline champion card, [A] original detail-page field names."""
    winner=tournament(role,s,g,r,cross)[0]
    own=winner['id']==g['id']
    return [dict(winner,week=s['day'],area='本地区' if own else '本地模拟区',
                 level=g['level'] if own else 1,popularity=g['popularity'] if own else 0,
                 top_member=[])]
