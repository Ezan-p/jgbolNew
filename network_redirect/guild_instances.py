"""Offline guild team dungeon and spirit-beast training, original callback shapes."""
from . import guild as u,journey,daily,summon,npc_players
from .guild_combat import simulate, replay_damage, record_events, recent_records, client_records
from . import guild_offline as offline, guild_trial


def state(s):
    a=s.setdefault('instances',{})
    if a.get('day')!=s['day']:
        a.update(train_bosses=[],train_floor=1,train_cleared=0,train_floor_attempts=0)
        a.update(train_claimed_stage=0,train_attempts=0,paid_tasks=0,train_hp=None,train_end=0,train_damage={},train_support=0,layer=0,team_opponents={},task_opponents={},search_tiles=[],search_order=[],search_bought={},tasks=[],wander=0,restored_wander_limit=0,field=None,shop_bought={},rank_claimed=False,day=s['day'],team=None,team_fights=0,search=0,points=0,board=[],train_open=False,train_done=False,train_claimed=False,train_record=[],catch=0,reputation=a.get('reputation',0),pets=a.get('pets',[]))
    week=(s['day']+3)//7
    if a.get('week')!=week:
        a['previous_week_score']=0 if a.get('week_claimed') else a.get('week_score',0);a['week_score']=0;a['week']=week;a['week_claimed']=False;a['lucky_week_used']=0;a['lucky_bonus']=0
    for k,v in dict(train_claimed_stage=4 if a.get('train_claimed') else 0,train_end=0,train_damage={},train_support=0,layer=0,paid_tasks=0).items():a.setdefault(k,v)
    offline.pets(a)
    return a


def team_applications(team,r):
    # Keep waiting NPCs in the save, but do not offer approval when full.
    if team and len(team['members'])>=r['team_size']:return {}
    # showJoinTeamPage overwrites each row.id with its table key.
    return {int(key):dict(row) for key,row in (team or {}).get('applications',{}).items()}


def team_info(role,a,g,r):
    t=a['team'];members=[]
    if t:
        for rid in t['members']:
            if rid not in g['members']:continue
            actor=role if int(rid)==role['role_id'] else (npc_players.get(int(rid)) or {}).get('role',{})
            first=next((c for c in sorted(actor.get('corteges',[]),key=lambda c:c.get('order',0)) if 1<=c.get('order',0)<=8),{})
            members.append(dict(g['members'][rid],head_type=first.get('type',5004),
                                cortege_layer=first.get('reborn_layer',0),finish_fam_data=a.get('layer',0)))
    return dict(teams=members,captain=t.get('captain',role['role_id']) if t else 0,max_count=r['team_size'],free_times=r['team_daily'],fight_count=a['team_fights'],
        apply_list=team_applications(t,r),last_search_time=a.get('team_last_fight_time',0) if a['team_fights'] else 0,max_layer=r['team_daily'],cleared_layer=a.get('layer',0),fam_id=1,fam_count=max(1,len(members)),can_support_fight=True)


def team_list(role,a,g,r):
    rows=[]
    if a['team']:
        captain=a['team'].get('captain',int(role['role_id']))
        rows.append(dict(name=g['members'][str(captain)]['name'],captain=captain,count=len(a['team']['members']),avg_level=sum(g['members'][rid]['level'] for rid in a['team']['members'])//len(a['team']['members']),had_fight=a['team_fights']>0))
    else:
        rows=[dict(name=m['name'],captain=m['id'],count=1,avg_level=m['level'],had_fight=False) for key,m in g['members'].items() if key!=str(int(role['role_id']))]
    return dict(teams=rows,max_count=r['team_size'],free_times=r['team_daily'],fight_count=a['team_fights'])


def weekend(s):
    return (s['day']+3)%7>=5


def residents(g,r):
    """[B] NPC members bring communal residents; never player-owned captures."""
    population=g.setdefault('resident_pets',{})
    contributors=g.setdefault('resident_contributors',[])
    for member in g['members'].values():
        if not member.get('npc_id') or member['id'] in contributors:continue
        # Original pet main types 1/2; keep type-specific inspectable counts.
        count=r['npc_resident_pets']
        for tid,n in ((101+member['id']%5,count//2),(201+member['id']%6,count-count//2)):
            population[str(tid)]=population.get(str(tid),0)+n
        contributors.append(member['id'])
    return population


def resident_info(g,r):
    population=residents(g,r)
    return {kind:sum(count for tid,count in population.items() if int(tid)//100==kind) for kind in (1,2,3)}


def lucky_limit(a,r):
    # [A] Every member may adopt on weekends; base quota is missing server data [B].
    return r['lucky_draw_limit']+a.get('lucky_bonus',0)


def train_stage(a,r):
    if a.get('train_bosses'):return 4 if a['train_done'] else a['train_cleared']
    hp=a.get('train_hp')
    return 4 if a['train_done'] else 0 if hp is None else (r['train_hp']-hp)*4//r['train_hp']


def train_info(role,a,g,now,r):
    guild_trial.prepare(a,role['guild'],r)
    boss=guild_trial.current(a)
    # [A] Only has_prize (58) draws the native claim button; had_closed (54)
    # never does. Keep an earned but unclaimed stage available after expiry.
    in_window=not r['train_weekend_only'] or weekend(role['guild'])
    if train_stage(a,r)>a.get('train_claimed_stage',0):result=58
    elif a['train_done']:result=54
    elif not in_window or a['train_open'] and now>=a['train_end']:result=53
    elif a['train_open']:result=1
    else:result=61 if sum(residents(g,r).values())>=r['train_resident_required'] else 41
    # [A] Both native timers treat 0 as an expired timestamp and immediately
    # remove/requery the dialog. last_time is the next calendar transition;
    # rest_time exists only while a challenge is actually running.
    day=role['guild']['day'];weekday=(day+3)%7
    transition=(day+(5-weekday if weekday<5 else 7-weekday))*86400-r['timezone_offset_hours']*3600
    if not r['train_weekend_only']:transition=(day+1)*86400-r['timezone_offset_hours']*3600
    end=a.get('train_end',0)
    return dict(result=result,last_time=min(end,transition) if end>now else transition,rest_time=end if end>now else False,
        pet_info=resident_info(g,r),train_prize={i:dict(add_union_gold=i*100,add_reputation=i*10,prize_list=[daily.spec(p[:2]+[p[2]*i,p[3]]) for p in r['train_rewards']]) for i in range(1,5)},
        boss_type=boss['type_id'],boss_layer=a['train_floor'],cleared_layer=a['train_cleared'],max_layer=4,remaining_attempts=max(0,r['train_attempt_limit']-a['train_floor_attempts']),has_record=bool(a['train_record']),boss_info=dict(type_id=boss['type_id'],boss_hp=a.get('train_hp') if a.get('train_hp') is not None else boss['hp'],boss_full_hp=boss['hp'],level=boss['level']),
        name=g['members'].get(str(a.get('appoint',role['role_id'])),{}).get('name',role['role_name']),support=a.get('train_support',0),can_support=in_window and a['train_open'] and not a['train_done'] and now<a['train_end'] and a.get('train_support',0)<r['train_support_limit'],damage_rank=sorted(a.get('train_damage',{}).values(),key=lambda v:-v['damage']))


def inside(a,now,r,g):
    return dict(result=1,week_reputation=a.get('week_score',0),total_catch_times=lucky_limit(a,r),left_catch_times=max(0,lucky_limit(a,r)-a.get('lucky_week_used',0)),task_last_time=(a['day']+1)*86400-r['timezone_offset_hours']*3600,
                pet_category_info={i:{int(tid):count for tid,count in residents(g,r).items() if int(tid)//100==i} for i in range(1,5)},pet_entities=[dict(p,power=offline.pet_power(p)) for p in offline.pets(a)])


def settle(role,s,g,op,d,now,r):
    a=state(s);rid=str(int(role['role_id']))
    if a['team']:
        # Members can leave/be removed by guild management while this page is open.
        t=a['team'];t['members']=[key for key in t['members'] if key in g['members']]
        t['applications']={key:row for key,row in t.get('applications',{}).items() if key in g['members'] and key not in t['members']}
        if rid not in t['members']:a['team']=None
        elif str(t['captain']) not in t['members']:t['captain']=int(rid)
    if op in (26,27,28,29,30,31,32,33,44,50,73,74,75):
        if op==26:
            u.require(a['team'] is None,'已经在队伍中')
            candidates=[(key,m) for key,m in g['members'].items() if key!=rid and m.get('npc')]
            applications={}
            while candidates:
                key,m=candidates.pop(offline.roll(s,len(candidates)));applications[key]=dict(m,apply_time=now)
            a['team']=dict(members=[rid],captain=int(role['role_id']),applications=applications)
            return [u.notice(op),u.reply(44,dict(result=1,team=team_info(role,a,g,r)))]
        if op==27:
            u.require(a['team'] is None,'已经在队伍中');target=str(u.positive(d,'leader_id'));u.require(target in g['members'] and target!=rid,'队伍不存在')
            u.require(g['members'][target].get('npc'),'离线队长不存在')
            candidates=[key for key,m in g['members'].items() if m.get('npc') and key!=target]
            teammates=[target,rid]
            while candidates and len(teammates)<r['team_size']:
                teammates.append(candidates.pop(offline.roll(s,len(candidates))))
            a['team']=dict(members=teammates,captain=int(target),applications={},application_log=[dict(role_id=int(rid),time=now,status='npc_accepted')])
            return [u.notice(28),u.reply(44,dict(result=1,team=team_info(role,a,g,r)))]
        if op in (31,32):
            u.require(a['team'] is not None,'尚未组队')
            if op==32:u.require(a['team'].get('captain')==int(role['role_id']),'只有队长可以解散')
            a['team']=None
            return [u.notice(op),u.reply(32,dict(result=1)),u.reply(44,dict(result=21,team=team_list(role,a,g,r)))]
        if op==33:
            u.require(a['team'] is not None and a['team'].get('captain')==int(role['role_id']),'只有队长可以移除成员');target=str(u.positive(d,'role_id'));u.require(target in a['team']['members'] and target!=rid,'成员无效');a['team']['members'].remove(target)
        if op in (28,29,30):
            u.require(a['team'] is not None and a['team']['captain']==int(rid),'只有队长可以审核')
            pending=a['team'].setdefault('applications',{})
            if op==30:pending.clear()
            else:
                selected=d.get('role_list',[d.get('role_id')])
                if isinstance(selected,dict):selected=list(selected.values())
                u.require(isinstance(selected,list) and selected and all(type(v)is int and v>0 for v in selected) and len(set(selected))==len(selected),'申请成员列表无效')
                u.require(all(str(v) in pending and str(v) in g['members'] for v in selected),'申请不存在')
                if op==28:
                    slots=max(0,r['team_size']-len(a['team']['members']))
                    u.require(slots>0,'队伍已满')
                    # The original approval button can submit every checked NPC.
                    # Admit as many as fit; leave the remainder waiting.
                    selected=selected[:slots]
                for ident in selected:
                    target=str(ident)
                    if op==28:a['team']['members'].append(target)
                    del pending[target]
            return [u.notice(op),u.reply(op,dict(result=1,team=team_info(role,a,g,r)))]
        if op==50:
            u.require(a['team'] is not None,'请先创建队伍')
            return [u.reply(50,team_applications(a['team'],r))]
        if op==73:return [u.reply(op,dict(result=1,team=team_list(role,a,g,r)))]
        if op==74:u.require(a['team'] is not None,'队伍不存在')
        return [u.reply(op if op in (44,50,74,75) else 44,dict(result=1 if a['team'] else 21,team=team_info(role,a,g,r) if a['team'] else team_list(role,a,g,r)))]
    if op in (41,42):
        u.require(a['team'] is not None,'请先创建队伍')
        if op==41:
            members=a['team']['members']
            u.require(r['team_min_fighters']<=len(members)<=r['team_size'],'秘境需要3至5名队员才能挑战')
            fighters=d.get('fight_list')
            if isinstance(fighters,dict):
                u.require(set(fighters)==set(range(1,len(fighters)+1)),'出战名单格式无效')
                fighters=[fighters[i] for i in range(1,len(fighters)+1)]
            u.require(isinstance(fighters,list) and all(type(v)is int and v>0 for v in fighters),'出战名单格式无效')
            u.require(len(fighters)==len(set(fighters)) and set(map(str,fighters))==set(members),'出战名单必须包含全部队员且不得重复')
            u.require(a['team_fights']<r['team_daily'],'秘境挑战次数已用完')
            actors=[]
            for ident in fighters:
                actor=role if ident==role['role_id'] else (npc_players.get(ident) or {}).get('role')
                u.require(actor is not None,'队员NPC阵容不存在，请重新组队')
                actors.append(actor)
            result,packets,replay=simulate(role,s,r,journey.load_rules(),15,'仙盟秘境',ally_roles=actors)
            a['team_fights']+=1;a['team_last_fight_time']=now;a['team_record']=[replay];a['team']['members']=[str(v) for v in fighters]
            if 1<=result<=3:
                a['layer']=a.get('layer',0)+1
                a['member_contributions']={key:a['layer'] for key in a['team']['members']}
                for p in r['team_rewards']:journey.grant(role,p)
        return record_events(a.get('team_record',[]))+[u.reply(op,dict(result=1,free_times=r['team_daily'],fight_count=a['team_fights'],cleared_layer=a.get('layer',0),max_layer=r['team_daily'],fight_result_list=client_records(a.get('team_record',[]))))]
    if op==43:
        from . import activity
        flag=d.get('flag');u.require(type(flag)is int and flag in range(1,8),'寻宝操作无效')
        bought=a.setdefault('search_bought',{})
        def stock():return [dict(daily.spec(p),cost_score=20,buy_times=max(0,5-bought.get(str(i),0))) for i,p in enumerate(r['train_rewards'],1)]
        if not a.get('search_tiles'):
            a['search_tiles']=[dict(item=daily.spec(r['search_rewards'][offline.roll(s,len(r['search_rewards']))]),had_token=i<a['search']) for i in range(25)]
            positions=list(range(1,26));a['search_order']=[]
            while positions:a['search_order'].append(positions.pop(offline.roll(s,len(positions))))
        prizes=[];sweep_prizes={};new_broadcast=[]
        if flag in (2,6):
            n=1 if flag==2 else r['search_daily']-a['search']
            u.require(n>0 and a['search']+n<=r['search_daily'],'今日寻宝次数已用完')
            if flag==6:u.pay(role,'gold_coin',r['search_sweep_gold'])
            for _ in range(n):
                a['search']+=1;a['points']+=10
                tile=a['search_tiles'][a['search']-1];tile['had_token']=True;item=tile['item']
                prize=[item['object_type'],item['attach_type'],item['attach_count'],item['attach_level']]
                index=a['search_order'][a['search']-1]
                row=dict(index=index,server_index=a['search'],object_type=prize[0],attach_type=prize[1],attach_count=prize[2],attach_level=prize[3],point=10,random_sort=index,name=role['role_name'],tips='寻宝获得10积分')
                a['board'].append(row);new_broadcast.append(row)
                granted=journey.grant(role,prize);prizes.append(granted);sweep_prizes[a['search']]=granted
        if flag==4:
            idx=u.positive(d,'index',len(r['train_rewards']))
            u.require(a['points']>=20 and bought.get(str(idx),0)<5,'积分或购买次数不足')
            a['points']-=20;bought[str(idx)]=bought.get(str(idx),0)+1;prizes=[journey.grant(role,r['train_rewards'][idx-1])]
        if flag==5:
            n=u.positive(d,'index',100);activity.consume(role,1035,n);a['points']+=n*r['search_card_points']
        if flag==7:
            u.require(a['team'] is not None,'请先加入队伍')
            return [u.reply(op,dict(result=1,flag=7,fam_info=team_info(role,a,g,r)))]
        return [u.reply(op,dict(result=1,flag=flag,index=d.get('index',0),attach_list=prizes,free_times=r['search_daily']-a['search'],search_count=a['search'],cleared_layer=a.get('layer',0),max_layer=r['team_daily'],fight_count=a['team_fights'],sweep_gold_cost=r['search_sweep_gold'],token_index=min(a['search']+1,25),my_broad_data=a['board'][-1] if flag==2 else new_broadcast,gold_cost=10,all_point=a['points'],get_point=10,prize_list=sweep_prizes if flag==6 else prizes,prize_items=a['search_tiles'],search_order=a['search_order'],max_free_times=r['search_daily'],broad_data=a['board'],store_items=stock(),board_size=25,flush_time=(s['day']+1)*86400-r['timezone_offset_hours']*3600))]
    if op==79:return [u.reply(op,train_info(role,a,g,now,r))]
    if op in (80,78):
        guild_trial.prepare(a,s,r)
        u.require(not r['train_weekend_only'] or weekend(s),'仙盟试炼仅周末开放')
        if op==80:
            if not a['train_open']:
                u.require(role['union_rank']==1,'只有盟主可以开启仙盟试炼')
            else:u.require(role['union_rank']==1 or a.get('appoint')==role['role_id'],'请由指定成员挑战或参与援助')
            # [A] Both opening (petHomeUI L817) and continued challenge (L1160)
            # enforce the resident count in the original executable client.
            u.require(sum(residents(g,r).values())>=r['train_resident_required'],'试炼挑战需要至少240只仙盟栖息宠物')
        u.require(not a['train_done'],'今日试炼已完成')
        u.require(role['level']>=r['join_level'],'人物等级不足')
        if op==80:
            if not a['train_open']:
                a.update(train_open=True,train_hp=guild_trial.current(a)['hp'],train_end=now+r['train_seconds'],train_damage={},train_support=0,train_attempts=0,train_floor_attempts=0)
            u.require(now<a['train_end'],'试炼已过期')
            u.require(a['train_floor_attempts']<r['train_attempt_limit'],'本层试炼挑战次数已用完')
            a['train_attempts']=a.get('train_attempts',0)+1
            a['train_floor_attempts']+=1
        else:
            u.require(a['train_open'] and now<a['train_end'],'试炼未开启或已过期')
            u.require(a['train_support']<r['train_support_limit'],'援助次数已用完');a['train_support']+=1
            return [u.reply(op,dict(result=1,support=a['train_support']))]
        appointed=a.get('appoint',role['role_id']) if op==80 else role['role_id']
        if str(appointed) not in g['members']:appointed=role['role_id']
        actor=role if appointed==role['role_id'] else (npc_players.get(appointed) or {}).get('role')
        u.require(actor is not None,'指定队员NPC阵容不存在')
        if actor is role:
            result,packets,replay=simulate(role,s,r,journey.load_rules(),27,'仙盟灵兽试炼',a['train_hp'])
        else:
            result,packets,replay=simulate(role,s,r,journey.load_rules(),27,'仙盟灵兽试炼',a['train_hp'],actor_role=actor)
        # Some random gods heal/revive: outgoing damage alone is not a kill.
        remaining=replay.get('boss_remaining_hp',max(0,a['train_hp']-replay_damage(replay)))
        remaining=max(0,min(guild_trial.current(a)['hp'],remaining))
        damage=max(0,a['train_hp']-remaining)
        a['train_hp']=remaining;a['train_record'].append(replay)
        guild_trial.advance(a)
        row=a['train_damage'].setdefault(str(appointed),dict(id=appointed,name=actor['role_name'],damage=0));row['damage']+=damage
        # The open response starts native battle playback and removes pet-home.
        # The native return callback requests 79 after rebuilding that page;
        # pushing 79 here would render into a destroyed Cocos node mid-battle.
        return record_events([replay])+[u.reply(op,dict(result=1,support=a['train_support'],free_times=r['train_attempt_limit'],fight_count=a['train_floor_attempts'],fight_result_list=client_records([replay])))]
    if op==95:return record_events(recent_records(a['train_record']))+[u.reply(op,dict(result=1,free_times=1,fight_count=1 if a['train_record'] else 0,fight_result_list=recent_records(a['train_record'])))]
    if op==81:
        u.require(role['union_rank']==1,'只有盟主可以指定挑战成员');target=d.get('appoint_role');u.require(type(target)is int and str(target) in g['members'],'指定成员不存在');a['appoint']=target
        return [u.reply(op,dict(result=1,name=g['members'][str(target)]['name']))]
    if op==82:
        stage=train_stage(a,r)
        last=a.get('train_claimed_stage',0);u.require(stage>last,'尚未达到下一阶段或奖励已领取')
        count=stage-last
        prizes=[journey.grant(role,p[:2]+[p[2]*count,p[3]]) for p in r['train_rewards']]
        a['train_claimed_stage']=stage;a['train_claimed']=stage==4;a['reputation']+=10*count;a['lucky_bonus']=a.get('lucky_bonus',0)+count
        a['week_score']=a.get('week_score',0)+10*count;a['total_reputation']=a.get('total_reputation',0)+10*count
        money=offline.funds(g,100*count,r)
        return [u.reply(op,dict(result=1,prize_list=prizes,add_reputation=10*count,add_union_gold=money,add_catch_count=count))]
    if op==94:return [catch_update(a,role,None,now)]
    if op==88:return [u.reply(op,inside(a,now,r,g))]
    if op==89:
        u.require(not r['lucky_weekend_only'] or weekend(s),'幸运捕获仅周末开放')
        u.require(a.get('lucky_week_used',0)<lucky_limit(a,r),'本周抽取次数不足，请完成灵兽任务或试炼')
        population=residents(g,r);total=sum(population.values());u.require(total>0,'仙盟暂无栖息宠物')
        u.require(len(offline.pets(a))<r['pet_limit'],'个人兽栏已满')
        choice=offline.roll(s,total);tid=None
        for key,count in sorted(population.items()):
            if choice<count:tid=int(key);break
            choice-=count
        population[str(tid)]-=1
        captured=offline.add_pet(a,tid,s,r);journey.grant(role,[15,tid,1,captured['quality']])
        from .activity_home_pets import wire
        acquired=wire(role['activity']['home']['pets'][-1])
        a['lucky_week_used']=a.get('lucky_week_used',0)+1;a['catch']=a['lucky_week_used']
        return [u.reply(op,dict(result=1,index=1+(tid-1)%5,prize_list=[acquired],left_catch_times=max(0,lucky_limit(a,r)-a['lucky_week_used']))),catch_update(a,role,tid,now)]
    u.require(False,'仙盟副本操作无效')


def catch_update(a,role,tid,now):
    if tid is not None:
        a['catch_history']=(a.get('catch_history',[])+[dict(name=role['role_name'],type_id=tid,time=now)])[-30:]
    return u.reply(94,dict(result=1,catch_list=a.get('catch_history',[])))
