"""Local and cross-area guild tournament state [B], original UI envelopes [A]."""
import copy
import math
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
    if m.get('day')!=s['day']:
        m['previous_roster']=m.get('npc_roster',[])[:]
        m.pop('union_id',None);m.pop('union_snapshot',None)
    if m.get('day')!=s['day']:m.update(npc_roster=[],tournament_leaders=[],settlement=None,total_score=0,life=life,streak=0,max_streak=0,loss_streak=0,target_life={},merit=0,day=s['day'],signed=cross,fights=0,wins=0,draws=0,score=0,claimed=False,bets={},records=[],purchases={},npc_scores={},target_stats={},npc_rounds=[])
    for k,v in dict(life=life,streak=0,max_streak=0,loss_streak=0,target_life={},merit=0).items():m.setdefault(k,v)
    m.setdefault('total_score',m['score'])
    for k,v in dict(npc_scores={},target_stats={},npc_rounds=[]).items():m.setdefault(k,v)
    m.setdefault('draws',0)
    return m


def enter(role,s,g,now,r,cross=False):
    m=state(s,cross,r);start=s['day']*86400-r['timezone_offset_hours']*3600
    group=3 if cross else 7
    stats=dict(match_type=CLIENT_MATCH_STAGE,group_type=group,win_count=m['wins'],lose_count=m['fights']-m['wins']-m['draws'],score=m['score'],life_point=m['life'])
    pending=m['fights']>0 and not m['claimed']
    return dict(area=2,area_name='本地区',union_data=stats,owner_data=stats,time_info=dict(begin_time=start,end_time=start+86400),has_match_flag=m['signed'],
        can_rece_award=pending,prize_list=[dict(match_type=CLIENT_MATCH_STAGE,from_group=group,to_group=group)] if pending else [],
        against_data=dict(src=dict(light_up=True,union_name=g['name'],area_name='本地区',life_point=m['life']),des=dict(light_up=True,union_name='离线演武盟',area_name='离线跨服区' if cross else '本地模拟区',life_point=sum(m['target_life'].get(str(90001+i),r['match_life']) for i in range(6)))))


def targets(role,s,g,r,cross=False):
    m=state(s,cross,r)
    rows=[]
    for i,entry in enumerate(opponents(role,s,g,r,cross),1):
        p=entry['profile'];ident=p['role_id']
        stats=m['target_stats'].get(str(90000+i),{})
        rows.append(dict(index=i,id=ident,role_id=ident,npc_id=entry['npc_id'],name=p['role_name'],level=p['level'],rank=[1,7,2,3,4,5][i-1],head_type=p['head_type'],cortege_layer=p['reborn_layer'],life_point=m['target_life'].get(str(90000+i),r['match_life']),action_point=r['battle_daily'],win_count=stats.get('wins',0),total_count=stats.get('fights',0),score_point=stats.get('merit',0),combat_power=p['role_combat_power'],order=i))
    alive=[v for v in rows if v['life_point']>0]
    return dict(result=1,des_member_list=alive,top_member_list=rows,src_union_name=g['name'],des_union_name='离线演武盟',
        src_union_life=m['life'],des_union_life=sum(v['life_point'] for v in rows),my_action_point=max(0,r['battle_daily']-m['fights']),my_life_point=m['life'],
        my_win_count=m['wins'],my_keep_win_count=m['streak'],max_win_streak_count=m['max_streak'],merit_point=m['merit'],score_point=m['score'],get_contrib=0,rank_name={1:'盟主',7:'副盟主',2:'护法',3:'长老',4:'精英',5:'盟员',6:'见习'}.get(role.get('union_rank'),'盟员'),fight_result=1)


def opponents(role,s,g,r,cross=False):
    """[B] Stable daily catalog armies; old scene IDs remain request aliases."""
    m=state(s,cross,r)
    if not m.get('npc_roster'):
        from .guild_offline import roll
        taken=guild_npcs.occupied(s)|{int(role['role_id'])}
        taken.update(npc_players.catalog()[key]['profile']['role_id'] for key in m.get('previous_roster',[]))
        other=s.get('match' if cross else 'cross_match',{})
        taken.update(npc_players.catalog()[key]['profile']['role_id'] for key in other.get('npc_roster',[]))
        power=max(1,sum(c.get('combat_power',0) for c in role['corteges'] if 1<=c.get('order',0)<=8))
        candidates=[e for e in npc_players.catalog().values() if e['profile']['role_id'] not in taken
                    and npc_players.source_file(e['source_file'])[e['npc_id']].get('battle_validation',{}).get('status')!='replay_limit_observed']
        selected=[]
        for percent in r['match_power_percent']:
            target=power*percent//100
            candidates.sort(key=lambda e:(abs(e['profile']['role_combat_power']-target),abs(e['profile']['level']-role['level']),e['npc_id']))
            u.require(bool(candidates),'没有可用的仙盟战NPC')
            nearest=abs(candidates[0]['profile']['role_combat_power']-target)
            pool=[e for e in candidates[:6] if abs(e['profile']['role_combat_power']-target)<=nearest+max(1,target//10)]
            chosen=pool[roll(s,len(pool))];selected.append(chosen);candidates.remove(chosen)
        selected.sort(key=lambda e:-e['profile']['role_combat_power'])
        m['npc_roster']=[e['npc_id'] for e in selected]
    return [npc_players.catalog()[key] for key in m['npc_roster']]


def bet_data(role,s,g,now,r,cross=False):
    m=state(s,cross,r);pair=enter(role,s,g,now,r,cross)['against_data']
    ranking=tournament(role,s,g,r,cross)
    for side,ident in (('src',g['id']),('des',90001)):
        team=next(v for v in ranking if v['id']==ident)
        pair[side].update(team,match_type=CLIENT_MATCH_STAGE,level=g['level'] if side=='src' else 1)
    leaders={g['id']:pair['src']['leader_id'],90001:pair['des']['leader_id']}
    costs={i:dict(silver_count=cost,pantao_count=0) for i,cost in enumerate(r['match_bet_silver'],1)}
    start=s['day']*86400-r['timezone_offset_hours']*3600
    return dict(result=1,teams=[dict(pair[k],id=pair[k]['leader_id']) for k in ('src','des')],
                bet_time_info=dict(begin_time=start,end_time=0 if m['fights'] or m['claimed'] else start+86400),
                bet_list={leaders[ident]:True for ident in m['bets'].values() if ident in leaders},
                lineup_list={i:[copy.deepcopy(pair)] for i in range(1,8)},
                bet_info_list={i:copy.deepcopy(costs) for i in range(1,8)},match_type=CLIENT_MATCH_STAGE)


def query(role,s,g,d,now,r,cross=False):
    u.require(r['wars_enabled'],u.WAR_CLOSED)
    op=58 if cross else 18;q=d['query_type'];m=state(s,cross,r)
    if m.get('union_id',g['id'])!=g['id']:
        g=s['unions'].get(str(m['union_id'])) or m['union_snapshot']
    mapping={20:8,21:9,22:10,23:13,24:16,25:17,26:18,27:19,28:12,30:100,32:100}
    typ=mapping.get(q,q);out=dict(query_type=q,result=1)
    if cross and q==30:
        leader=next((v for v in g['members'].values() if v['rank']==1),None)
        out.update(union_list=[dict(u.info(g,r),order=1,leaderid=leader['id'] if leader else 0,score=m['score'])],last_champion=champions(role,s,g,r,cross)[0])
    elif typ==100:out['enter_data']=enter(role,s,g,now,r,cross)
    elif typ in (11,12,13):
        target_data=targets(role,s,g,r,cross);out.update(target_data)
        if cross:out['target_list']=target_data
    elif typ==9:out.update(schedule_list=dict(champion_list=champions(role,s,g,r,cross),match_member=tournament(role,s,g,r,cross),begin_time=s['day']*86400-r['timezone_offset_hours']*3600,end_time=(s['day']+1)*86400-r['timezone_offset_hours']*3600),had_signup=m['signed'],match_list=tournament(role,s,g,r,cross))
    elif typ==8:out.update(bet_data(role,s,g,now,r,cross))
    elif typ in (10,18):out.update(teams=tournament(role,s,g,r,cross),champion_list=champions(role,s,g,r,cross),lineup_list=tournament(role,s,g,r,cross))
    elif typ==17:out.update(member_score={1:member_scores(role,s,g,r,cross),2:targets(role,s,g,r,cross)['top_member_list']},src_direction=1,des_direction=2)
    elif typ==19:out.update(member_list=member_scores(role,s,g,r,cross))
    elif typ==16:
        ranking=tournament(role,s,g,r,cross)
        groups={i:[] for i in range(1,8)};groups[3 if cross else 7]=ranking
        out['union_score']=dict(my_order=next(v['order'] for v in ranking if v['id']==g['id']),top_list=groups)
    elif cross and q in (29,31):out['lineup_info']=lineup(role,d.get('des_id',role['role_id']),r,cross=True)
    elif typ==33:out.update(score=m['score'],shop_list=shop(m,r))
    else:u.require(False,'仙盟赛程查询参数无效')
    return [u.reply(op,out)]


def shop(m,r):
    return [dict(need_score=0,attach_data=dict(daily.spec(p),cost=10,buy_times=max(0,5-m['purchases'].get(str(i),0)))) for i,p in enumerate(r['match_rewards'],1)]


def reward_row(order,cross=False):
    if cross:
        row=next(v for v in summon.rows('cross_match_prize.csv') if int(v['area'])==2 and int(v['group_type'])==3 and int(v['order_min'])<=order<=int(v['order_max']))
        return dict(row,prize_list=row['contrib1'])
    return next(v for v in summon.rows('union_match_prize.csv') if int(v['group_type'])==7 and int(v['min_order'])<=order<=int(v['max_order']))


def rewards(role,s,g,r,cross=False):
    m=state(s,cross,r);ranking=tournament(role,s,g,r,cross)
    order=next(v['order'] for v in ranking if v['id']==g['id'])
    row=reward_row(order,cross)
    specs=[]
    for token in row['prize_list'].split('/'):
        typ,tid,level,count=map(int,token.split('|'));specs.append([typ,tid,count,level])
    winner=g['id'] if next(v['score'] for v in ranking if v['id']==g['id'])>=next(v['score'] for v in ranking if v['id']==90001) else 90001
    for typ,ident in m['bets'].items():
        if ident==winner:specs.append([12,0,2*r['match_bet_silver'][int(typ)-1],1])
    return dict(order=order,ranking=ranking,champion=ranking[0]['id']),specs,int(row['popularity'])


def rollover(role,now,r):
    """Mail unclaimed daily rewards before replacing a tournament (also offline)."""
    if not r['wars_enabled']:return
    from . import system_mail,welfare
    for cross,key in ((False,'match'),(True,'cross_match')):
        s=role.get('guild',{});m=s.get(key,{})
        if m.get('day',daily.day(now,r))==daily.day(now,r) or not (m.get('fights') or m.get('bets')) or m.get('claimed'):continue
        ident=m.get('union_id',int(role.get('union_id',0)))
        g=s.get('unions',{}).get(str(ident)) or m.get('union_snapshot')
        if not g:continue
        old_s=dict(s,day=m['day'])
        if m.get('fights'):
            result,specs,pop=rewards(role,old_s,g,r,cross)
            body='离线NPC积分赛排名第%d名，附排行奖励及押注返还。'%result['order']
        else:
            result=dict(order=0,ranking=tournament(role,old_s,g,r,cross),champion=0)
            specs=[[12,0,sum(r['match_bet_silver'][int(t)-1] for t in m['bets']),1]];pop=0
            body='本日未出战，本轮取消并退还全部押注银两。'
        title=('跨服战争' if cross else '仙盟战争')+'结算奖励'
        system_mail.deliver(role,'guild-'+key+'-'+str(m['day']),title,
                            body,specs,now,welfare.load_rules())
        s=role['guild'];m=s[key];m.update(claimed=True,settlement=result)
        if str(ident) in s['unions']:s['unions'][str(ident)]['popularity']+=pop


def member_scores(role,s,g,r,cross=False):
    m=state(s,cross,r)
    order=next(v['order'] for v in tournament(role,s,g,r,cross) if v['id']==g['id'])
    reward=reward_row(order,cross)
    count=int(reward['prize_list'].split('/')[0].split('|')[-1])
    rows=[dict(id=v['id'],name=v['name'],rank=v['rank'],score_point=m['merit'] if v['id']==role['role_id'] else 0,
               win_count=m['wins'] if v['id']==role['role_id'] else 0,total_count=m['fights'] if v['id']==role['role_id'] else 0,
               prize_count=count if m['fights'] else 0) for v in g['members'].values()]
    rows.sort(key=lambda v:(-v['score_point'],v['id']))
    for i,v in enumerate(rows,1):v['order']=i
    return rows


def npc_round(role,s,g,now,r,jrules,cross):
    """[B] The other fixture advances once per player action, using real armies.

    Queries/reconnects never simulate or reroll a result. Background battle IDs
    live in a detached state so the player's playback ID is not overwritten.
    """
    from .guild_combat import simulate
    m=state(s,cross,r);tournament(role,s,g,r,cross)
    if len(m['npc_rounds'])>=m['fights']:return
    first,second=m['tournament_leaders'][1:3]
    actor=npc_players.get(first)['role'];enemy=npc_players.catalog()[second]
    sandbox=dict(day=s['day'],fight_id=0)
    result,_,replay=simulate(actor,sandbox,r,jrules,17 if cross else 14,
                             enemy['profile']['role_name'],enemy_npc=second)
    winner=90002 if 1<=result<=3 else 90003 if 4<=result<=6 else 0
    for ident in (90002,90003):m['npc_scores'][str(ident)]=m['npc_scores'].get(str(ident),0)+(50 if ident==winner else 1)
    m['npc_rounds'].append(dict(round=m['fights'],src=first,des=second,winner=winner,result=result,
                                time=now,round_count=replay.get('fight_result_msg',{}).get('fight_round',0)))


def settle(role,s,g,op,d,now,r):
    u.require(r['wars_enabled'],u.WAR_CLOSED)
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
    if op in (47,62):
        u.require(m.get('union_id',g['id'])==g['id'],'本日已代表其他仙盟参赛')
        return [u.reply(op,bet_data(role,s,g,now,r,cross))]
    if op in (48,63):
        u.require(m.get('union_id',g['id'])==g['id'],'本日已代表其他仙盟参赛')
        u.authorize(role,r,22 if cross else 19);u.require(m['fights']==0 and not m['claimed'],'开战后不能押注');typ=u.positive(d,'bet_type',3);ident=u.positive(d,'union_id')
        # The current detail panel submits the leader ID as union_id.
        if ident==next(v['id'] for v in g['members'].values() if v['rank']==1):ident=g['id']
        if ident==opponents(role,s,g,r,cross)[0]['profile']['role_id']:ident=90001
        u.require(ident in (g['id'],90001) and str(typ) not in m['bets'],'押注目标无效或已押注')
        u.pay(role,'silver_coin',r['match_bet_silver'][typ-1]);m['bets'][str(typ)]=ident
        m['union_id']=g['id'];m['union_snapshot']={k:copy.deepcopy(g[k]) for k in ('id','name','level','popularity','members')}
        return [u.reply(op,bet_data(role,s,g,now,r,cross))]
    if op in (72,76):
        u.require(m['fights']>0 and not m['claimed'],'尚未参赛或奖励已领取')
        u.require(m.get('union_id',g['id'])==g['id'],'请返回参战仙盟领取，或次日领取结算邮件')
        result,specs,pop=rewards(role,s,g,r,cross)
        prizes=[journey.grant(role,p) for p in specs]
        m.update(settlement=result,claimed=True);g['popularity']+=pop
        return [u.reply(op,dict(result=1,prize_list=prizes))]
    u.require(False,'仙盟赛程操作无效')


def fight(role,s,g,req,now,r,jrules):
    u.require(r['wars_enabled'],u.WAR_CLOSED)
    from .guild_combat import simulate
    cross=req['fight_type'] in (17,23,24,32,33);m=state(s,cross,r)
    u.require(m.get('union_id',g['id'])==g['id'],'本日已代表其他仙盟参战，请次日再战')
    u.authorize(role,r,3);u.require(m['signed'],'请先报名仙盟战');u.require(not m['claimed'],'本轮已结算，请次日再战');u.require(m['fights']<r['battle_daily'],'行动力不足');u.require(m['life']>0,'生命点不足')
    target=req['des_id'];u.require(type(target) in (int,float) and math.isfinite(target) and target==int(target) and 0<target<=2147483647,'对手编号无效')
    target=int(target);roster=opponents(role,s,g,r,cross)
    selected=next((i for i,e in enumerate(roster) if e['profile']['role_id']==target),None)
    if selected is not None:target=90001+selected
    u.require(target in range(90001,90007),'对手不存在')
    u.require(m['target_life'].get(str(target),r['match_life'])>0,'目标已经退场')
    if req['fight_type']==16:u.require(target==90001,'盟主战请选择盟主')
    enemy=roster[target-90001]
    m['union_id']=g['id']
    m['union_snapshot']={k:copy.deepcopy(g[k]) for k in ('id','name','level','popularity','members')}
    result,packets,replay=simulate(role,s,r,jrules,req['fight_type'],enemy['profile']['role_name'],enemy_npc=enemy['npc_id'])
    m['fights']+=1;win=1<=result<=3;lost=4<=result<=6;m['wins']+=int(win)
    m['draws']+=int(result==0)
    ts=m['target_stats'].setdefault(str(target),dict(fights=0,wins=0,merit=0));ts['fights']+=1;ts['wins']+=int(lost)
    ts['merit']+=r['match_merit'].get(str(role['union_rank']),1) if lost else 0
    rank=[1,7,2,3,4,5][target-90001];merit=r['match_merit'][str(rank)]
    if win:
        m['streak']=min(r['match_max_streak'],m['streak']+1);m['max_streak']=max(m['max_streak'],m['streak']);m['loss_streak']=0
        m['merit']+=merit;m['score']+=merit*10
        m['target_life'][str(target)]=max(0,m['target_life'].get(str(target),r['match_life'])-r['match_target_loss'])
    else:
        m['streak']=0;m['score']+=1
        if lost:
            m['life']=max(0,m['life']-r['match_loss_life']);m['loss_streak']+=1
        else:m['loss_streak']=0
    m['total_score']+=merit*10 if win else 1
    m['npc_scores']['90001']=m['npc_scores'].get('90001',0)+(r['match_merit'].get(str(role['union_rank']),1)*10 if lost else 1)
    npc_round(role,s,g,now,r,jrules,cross)
    gain=u.contribution(role,merit*2 if win else 2);m['records'].append(replay);m['records']=m['records'][-10:]
    out=targets(role,s,g,r,cross);out.update(query_type=28 if cross else 12,fight_result=result,get_contrib=gain)
    if cross:out['target_list']=dict(out,prize_list=[])
    return packets+[u.reply(58 if cross else 18,out),summon.event(44,dict(fight_id=replay.get('line_up_msg',{}).get('fight_id',s['fight_id']),fight_type=req['fight_type']))]


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
    if m.get('settlement'):return copy.deepcopy(m['settlement']['ranking'])
    leader=next(v for v in g['members'].values() if v['rank']==1)
    rows=[dict(id=g['id'],union_id=g['id'],name=g['name'],union_name=g['name'],leader_id=int(leader['id']),leader_name=leader['name'],score=m['total_score'],life_point=m['life'],group_type=7,level=g['level'],area='本地区',win_count=m['wins'],lose_count=m['fights']-m['wins']-m['draws'])]
    roster=opponents(role,s,g,r,cross)
    if not m.get('tournament_leaders'):
        from .guild_offline import roll
        excluded=guild_npcs.occupied(s)|{e['profile']['role_id'] for e in roster}
        pool=[e for e in npc_players.catalog().values() if e['profile']['role_id'] not in excluded
              and npc_players.source_file(e['source_file'])[e['npc_id']].get('battle_validation',{}).get('status')!='replay_limit_observed']
        pool.sort(key=lambda e:(abs(e['profile']['role_combat_power']-roster[0]['profile']['role_combat_power']),e['npc_id']))
        pool=pool[:12]
        m['tournament_leaders']=[roster[0]['npc_id']]+[pool.pop(roll(s,len(pool)))['npc_id'] for _ in range(2)]
    for i,name in enumerate(('离线演武盟','离线蓬莱盟','离线昆仑盟'),1):
        score=m['npc_scores'].get(str(90000+i),0)
        p=npc_players.catalog()[m['tournament_leaders'][i-1]]['profile']
        rows.append(dict(id=90000+i,union_id=90000+i,name=name,union_name=name,leader_id=p['role_id'],leader_name=p['role_name'],score=score,life_point=sum(m['target_life'].get(str(90001+j),r['match_life']) for j in range(6)) if i==1 else r['match_life'],group_type=7,level=1,area='离线跨服区' if cross else '本地模拟区',win_count=sum(v['winner']==90000+i for v in m['npc_rounds']) if i>1 else m['fights']-m['wins']-m['draws'],lose_count=sum(v['winner']!=0 and v['winner']!=90000+i for v in m['npc_rounds']) if i>1 else m['wins']))
    rows.sort(key=lambda row:(-row['score'],row['id']))
    for i,row in enumerate(rows,1):row.update(order=i,server_name=row['area'],group_type=3 if cross else 7)
    return rows


def champions(role,s,g,r,cross=False):
    """[B] Current offline champion card, [A] original detail-page field names."""
    winner=tournament(role,s,g,r,cross)[0]
    own=winner['id']==g['id']
    return [dict(winner,week=s['day'],area='本地区' if own else '本地模拟区',
                 level=g['level'] if own else 1,popularity=g['popularity'] if own else 0,
                 top_member=member_scores(role,s,g,r,cross) if own else [dict(id=winner['leader_id'],name=winner['leader_name'],order=1,score_point=winner['score'],win_count=winner.get('win_count',0),total_count=winner.get('win_count',0)+winner.get('lose_count',0),prize_count=0)])]
