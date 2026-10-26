"""Original west-op wire contract; explicit local escort economy and opponents [B]."""
import math
from . import guild as u, journey, activity, guild_offline as offline, guild_npcs, npc_players

# [A] ui_escortUI.lua L84, max_stopable (ordinary grades 3, highest grade 1).
MAX_STOPABLE={1:3,2:3,3:3,4:3,5:1}


def state(s):
    e=s.setdefault('escort',{})
    if e.get('day')!=s['day']:
        e.update(day=s['day'],sent=0,robbed=0,flushes=0,level=1,cards=3,issued={},requests=[],black=e.get('black',[]),targets={},cooldown=0,rob_counts={},rob_limits={},chase_targets={})
        for row in e['black']:row.update(be_grab_times=0,noChase=False)
    e.setdefault('active',None);e.setdefault('credits',0)
    for field in ('rob_counts','rob_limits','chase_targets'):e.setdefault(field,{})
    return e


def book(role,g,ident,now,level=1):
    own=ident==role['role_id']
    row=dict(id=ident,player_name=role['role_name'] if own else '离线取经者',union_name=g['name'] if own else '演武仙盟',
        book_level=level,role_level=role['level'],tao_point=role.get('tao_point',0) if own else 1000,role_rank=5,head_type=1,be_grab_times=0,
        cloud_time_list=[],end_time=now+3600,had_protector=False)
    if not own and npc_players.resolve(ident):
        entry=npc_players.catalog()[npc_players.resolve(ident)];p=entry['profile']
        row.update(npc_id=entry['npc_id'],player_name=p['role_name'],role_level=p['level'],head_type=p['head_type'],tao_point=p['role_combat_power'])
    return row


def migrate_targets(role,s,g,e,now):
    """Migrate saved scene identities and every revenge link before any action."""
    aliases=e.setdefault('legacy_npc_ids',{})
    rows=[v for targets in e['targets'].values() for v in targets]+list(e.get('chase_targets',{}).values())
    references=e.get('raid_log',[])+e['black']
    taken=guild_npcs.occupied(s)|{int(role['role_id'])}|set(aliases.values())
    taken.update(v['id'] for v in rows+references if npc_players.resolve(v['id']))

    def entry_for(ident):
        key=npc_players.resolve(ident) or npc_players.resolve(aliases.get(str(ident)))
        if key:return npc_players.catalog()[key]
        entry=guild_npcs.choose(s,role['level'],excluded_ids=taken)[0]
        taken.add(entry['profile']['role_id'])
        aliases[str(ident)]=entry['profile']['role_id']
        return entry

    for row in rows:
        if row.get('npc_id') and npc_players.resolve(row['id']):continue
        old_id=row['id'];entry=entry_for(old_id);p=entry['profile']
        row.update(id=p['role_id'],npc_id=entry['npc_id'],player_name=p['role_name'],
                   role_level=p['level'],head_type=p['head_type'],tao_point=p['role_combat_power'],
                   scene_id=row.get('scene_id',old_id))
    for row in references:
        if npc_players.resolve(row['id']):continue
        entry=entry_for(row['id']);p=entry['profile']
        row.update(id=p['role_id'],name=p['role_name'])
        if 'player_name' in row:row['player_name']=p['role_name']
        if 'rob_id' in row:row['rob_id']=p['role_id']
    sync_counts(e)


def sync_counts(e):
    """[B] Daily per-identity totals survive route replacement and pursuit."""
    counts=e.setdefault('rob_counts',{});limits=e.setdefault('rob_limits',{})
    rows=[v for targets in e['targets'].values() for v in targets]+list(e.get('chase_targets',{}).values())
    for row in rows:
        key=str(row['id']);counts[key]=max(counts.get(key,0),row.get('be_grab_times',0))
        limits[key]=min(limits.get(key,3),MAX_STOPABLE[row['book_level']])
    for row in rows:row['be_grab_times']=counts[str(row['id'])]
    for row in e['black']:row['be_grab_times']=counts.get(str(row['id']),0)


def chase_target(role,s,g,e,ident,now):
    """Reopen a known blacklisted NPC's route without rerolling their identity."""
    black=next((v for v in e['black'] if v['id']==ident),None)
    if black is None or not npc_players.resolve(ident):return None
    target=next((v for rows in e['targets'].values() for v in rows if v['id']==ident and v['end_time']>now),None)
    if target is None:
        target=e['chase_targets'].get(str(ident))
        if target is None or target['end_time']<=now:
            target=book(role,g,ident,now,black['book_level'])
            target.update(be_grab_times=e['rob_counts'].get(str(ident),0),road_type=black.get('road_type',1))
            e['chase_targets'][str(ident)]=target
    sync_counts(e)
    return target


def black_list(role,s,g,e,now,r):
    for row in e['black']:
        target=chase_target(role,s,g,e,row['id'],now)
        row['noChase']=(target is None or e['robbed']>=r['escort_rob_daily'] or
                        e['rob_counts'].get(str(row['id']),0)>=e['rob_limits'].get(str(row['id']),MAX_STOPABLE[row['book_level']]))
    return e['black']


def books(role,g,e,now,road):
    s=role['guild']
    migrate_targets(role,s,g,e,now)
    if str(road) not in e['targets'] or all(v['end_time']<=now for v in e['targets'][str(road)]):
        excluded=guild_npcs.occupied(s)|{v['id'] for rows in e['targets'].values() for v in rows}
        entries=guild_npcs.choose(s,role['level'],3,excluded_ids=excluded)
        e['targets'][str(road)]=[dict(book(role,g,entry['profile']['role_id'],now,1+(e['day']+road+i)%5),scene_id=91000+road+10*i,had_protector=i==2) for i,entry in enumerate(entries)]
    sync_counts(e)
    rows=list(e['targets'][str(road)])
    if e['active'] and e['active']['road']==road:rows.append(e['active']['book'])
    return rows


def settle(role,s,g,d,now,r):
    e=state(s);migrate_targets(role,s,g,e,now);resolve_raid(role,s,g,e,now,r);flag=u.positive(d,'flag',15);out=dict(flag=flag,result=1)
    road=d.get('road_type',e.get('road',1));u.require(type(road)is int and road in (1,2,3),'取经路线无效')
    if flag==1:return [u.reply(69,out)]
    if flag==2:
        n=d.get('ten_pick',1);u.require(type(n)is int and n in (1,10),'合成数量无效')
        for tid in (1301,1302,1303):activity.consume(role,tid,n)
        out.update(ten_pick=n,item_list=[journey.grant(role,p[:2]+[p[2]*n,p[3]]) for p in r['escort_compose_rewards']])
    elif flag in (3,9):
        e['road']=road;active=e['active']
        out.update(book_list=books(role,g,e,now,road),query_type=d.get('query_type',1),can_rece_prize=bool(active and now>=active['book']['end_time']),on_road_type=active['road'] if active else 0)
    elif flag in (4,5):
        u.require(e['active'] is None,'已有取经队伍，请先领取奖励')
        if flag==5:
            u.require(e['flushes']<r['escort_flush_limit'],'刷新次数已用完')
            if e['flushes']>=r['escort_free_flush']:u.pay(role,'gold_coin',r['escort_flush_gold'])
            e['flushes']+=1;e['level']=min(5,e['level']+1+int(offline.roll(s,100)<20))
        out.update(flush_gold=r['escort_flush_gold'],free_flush_count=r['escort_free_flush'],cloud_cost_gold=30,
            book_level=e['level'],flush_count=e['flushes'],flush_west_book=e['flushes'],contribute=e['level']*10,
            protect_list=[dict(id=m['id'],name=m['name'],count=e['credits']) for m in g['members'].values() if m['rank'] in (1,7)] if e['credits'] else [],top_rank_list=[m for m in g['members'].values() if m['rank'] in (1,7)])
    elif flag==6:
        u.require(e['active'] is None and e['sent']<r['escort_daily'],'取经未结束或今日次数已用完')
        u.require(d.get('book_level')==e['level'],'经书等级已改变，请刷新')
        target=d.get('des_id',0);u.require(target==0 or str(target) in g['members'],'护送成员不存在')
        if target:
            u.require(e['credits']>0,'没有可用护送令');e['credits']-=1
        e['sent']+=1;e['road']=road;e['active']=dict(road=road,book=book(role,g,role['role_id'],now,e['level']),raid_checked=False)
        e['active']['book'].update(had_protector=bool(target),protector_id=target,tao_point=role.get('tao_point',0),cloud_time_list=[now,now+3600] if target else [])
        role.update(last_west_book_time=now,west_book_count=e['sent'])
        out.update(book_list=books(role,g,e,now,road));e['level']=1;e['flushes']=0
    elif flag==11:
        a=e['active'];u.require(a is not None and now>=a['book']['end_time'],'取经尚未完成或奖励已领取')
        level=a['book']['book_level'];loss=20 if a['book']['be_grab_times'] else 0;gain=u.contribution(role,level*10*(100-loss)//100);money=offline.funds(g,level*100*(100-loss)//100,r)
        prizes=[journey.grant(role,[5,1300+a['road'],level,1])];e['active']=None
        out.update(contribute=gain,union_money=money,item_info=prizes,can_rece_prize=False,on_road_type=0)
    elif flag==8:
        u.authorize(role,r,26);target=u.positive(d,'des_id');n=u.positive(dict(count=d.get('count',1)),'count',3)
        u.require(str(target) in g['members'] and e['cards']>=n,'护送令不足或成员不存在')
        e['cards']-=n;e['issued'][str(target)]=e['issued'].get(str(target),0)+n
        out.update(left_protect_count=e['cards'],des_id=target)
    elif flag==7:
        key=str(int(role['role_id']));n=e['issued'].pop(key,0);u.require(n>0,'没有可领取的护送令')
        e['credits']+=n
    elif flag==15:
        target=u.positive(d,'des_id');u.require(str(target) in g['members'],'护送成员不存在')
        u.require(target not in e['requests'],'已请求护送');e['requests'].append(target)
        if g['members'][str(target)].get('npc'):
            e['credits']+=1
            if e['active'] and not e['active']['book']['had_protector']:
                e['credits']-=1;e['active']['book'].update(had_protector=True,protector_id=target)
            out['request_protect']=True
    elif flag==12:out['berob_info']=e.get('raid_log',[])
    elif flag==13:out.update(berob_money=sum(v.get('loss',0) for v in e.get('raid_log',[])),union_black_info=black_list(role,s,g,e,now,r))
    elif flag==14:
        target=u.positive(d,'des_id');record=next((v for rows in e['targets'].values() for v in rows if target in (v['id'],v.get('scene_id'))),None)
        if record:target=record['id']
        else:target=e['legacy_npc_ids'].get(str(target),target)
        record=record or next((v for v in e.get('raid_log',[]) if v['id']==target),None)
        u.require(record is not None,'目标不存在')
        u.require(target not in [v['id'] for v in e['black']],'已在黑名单')
        target_road=next((int(road) for road,rows in e['targets'].items() if any(v['id']==target for v in rows)),record.get('road_type',1))
        e['black'].append(dict(id=target,name=record['player_name'],union_name=record['union_name'],black_count=1,book_level=record['book_level'],road_type=target_road,be_grab_times=e['rob_counts'].get(str(target),0),noChase=False));out['des_id']=target
        black_list(role,s,g,e,now,r)
        for row in e.get('raid_log',[]):
            if row['id']==target:row['is_black']=True
    elif flag==10:
        return rob(role,s,g,e,d,now,r)
    # Publish the trip itself instead of relying on a stale player timestamp.
    active=e['active']
    out.update(escort_active=active is not None,escort_end_time=active['book']['end_time'] if active else 0,
               on_road_type=active['road'] if active else 0,can_rece_prize=bool(active and now>=active['book']['end_time']))
    return [u.reply(69,out)]


def rob(role,s,g,e,d,now,r):
    from .guild_combat import simulate
    # 1026 transports des_id as a double; reject fractions, bools and nonfinite IDs.
    value=d.get('des_id')
    u.require(type(value) in (int,float) and math.isfinite(value) and 0<value<=2147483647 and value==int(value),'取经目标编号无效')
    ident=int(value);migrate_targets(role,s,g,e,now)
    target=next((v for rows in e['targets'].values() for v in rows if ident in (v['id'],v.get('scene_id'))),None)
    if target is None or target['end_time']<=now:
        canonical=target['id'] if target else e['legacy_npc_ids'].get(str(ident),ident)
        target=chase_target(role,s,g,e,canonical,now)
    u.require(target is not None and now<target['end_time'],'目标不存在或已抵达')
    ident=target['id']
    u.require(e['robbed']<r['escort_rob_daily'] and e['rob_counts'].get(str(ident),0)<e['rob_limits'][str(ident)],'今日拦截次数已用完')
    if d.get('flush_cd'):u.pay(role,'gold_coin',r['tree_flush_gold'])
    else:u.require(now>=e['cooldown'],'拦截冷却中')
    result,packets,replay=simulate(role,s,r,journey.load_rules(),19,target['player_name'],enemy_npc=target['npc_id']);won=1<=result<=3
    e['robbed']+=1;e['cooldown']=now+60;e['rob_counts'][str(ident)]=e['rob_counts'].get(str(ident),0)+1
    sync_counts(e);black_list(role,s,g,e,now,r)
    role.update(last_stop_book_time=now,stop_book_count=e['robbed'])
    revenge=any(v['id']==ident for v in e['black'])
    gain=u.contribution(role,(15 if revenge else 10) if won else 0)
    from . import summon
    return packets+[u.reply(69,dict(flag=10,result=1 if won else 43,des_id=ident,is_run_kill=revenge,be_grab_times=target['be_grab_times'],contribute=gain,attach_prize_list=[])),summon.event(44,dict(fight_id=s['fight_id'],fight_type=19))]


def resolve_raid(role,s,g,e,now,r):
    a=e['active']
    if not a or a.get('raid_checked') or now<a['book']['end_time']-1800:return
    a['raid_checked']=True
    protected=a['book']['had_protector']
    if offline.roll(s,100)>=(10 if protected else 50):return
    target=next(v for v in books(role,g,e,now,a['road']) if v['id']!=role['role_id'])
    ident=target['id'];a['book']['be_grab_times']+=1
    row=dict(id=ident,name=target['player_name'],player_name=target['player_name'],union_name=target['union_name'],time=now,rob_time=now,rob_id=ident,rob_contrib=a['book']['book_level']*2,is_black=any(v['id']==ident for v in e['black']),book_level=target['book_level'],road_type=a['road'],be_grab_times=1,loss=a['book']['book_level']*20,result=1)
    e['raid_log']=(e.get('raid_log',[])+[row])[-30:]
    g['events'].append('取经遭遇离线拦截，完成奖励减少20%');g['events']=g['events'][-100:]
