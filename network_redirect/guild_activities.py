"""Guild shared activities: original client messages [A], offline schedules [B]."""
from . import guild as u, summon, journey, daily
from .protocol import encode
FEAST={int(v['award_type']):v for v in summon.rows('union_feast_award.csv')}


def feast(s,g,now,r):
    f=g.setdefault('feast',dict(day=-1,type=0,end=0,gifts=[],claimed=[],grabbed={},sent=0))
    if f['day']!=s['day']:f.update(stats={},log=[],ended=False,day=s['day'],type=0,end=0,gifts=[],claimed=[],grabbed={},sent=0)
    if f['type'] and now>=f['end'] and not f.get('ended'):
        f['ended']=True;g['events'].append('宴席已经结束（'+str(f['end'])+'）');g['events']=g['events'][-100:]
    return f


def feast_data(role,s,g,now,r):
    f=feast(s,g,now,r);rid=str(int(role['role_id']))
    gifts=[dict(v,can_grab=now<f['end'] and rid not in v['grabbed'] and v['count']>0) for v in f['gifts']]
    return dict(feast_stat=53 if not f['type'] else 54 if now>=f['end'] else 0,feast_type=f['type'],
        send_gift={v['type']:dict(cost_gold=v['gold'],contribute=v['contrib']) for v in r['feast_gifts']},max_grab_count=r['feast_grab_limit'],
        member_count=len(g['members']),feast_end_time=f['end'],gift_data=gifts,
        can_rece_award=bool(f['type']) and now<f['end'] and rid not in f['claimed'])


def query(role,s,g,d,now,r):
    q=d['query_type']
    if q==14:return [u.reply(18,dict(query_type=q,feast_data=feast_data(role,s,g,now,r)))]
    if q==15:
        rows=sorted((v for union in s['unions'].values() if union.get('feast',{}).get('day')==s['day'] for v in union['feast'].get('stats',{}).values()),key=lambda v:(-v['fortune'],-v['contribute'],v['id']))
        for i,row in enumerate(rows,1):row['rank']=i
        return [u.reply(18,dict(query_type=q,order=next((v['rank'] for v in rows if v['id']==role['role_id']),0),fortune_info=rows))]
    from . import guild_match
    return guild_match.query(role,s,g,d,now,r)


def settle(role,s,g,op,d,now,r):
    if op==69:
        from . import guild_escort
        return guild_escort.settle(role,s,g,d,now,r)
    if op in (83,84,85,86,87,91,92):
        from . import guild_hunt
        return guild_hunt.settle(role,s,g,op,d,now,r)
    if op in (26,27,28,29,30,31,32,33,41,42,43,44,50,73,74,75,78,79,80,81,82,88,89,95):
        from . import guild_instances
        return guild_instances.settle(role,s,g,op,d,now,r)
    if op in (45,46,47,48,58,62,63,72,76):
        from . import guild_match
        return guild_match.settle(role,s,g,op,d,now,r)
    if op in (65,66,67,68):
        f=feast(s,g,now,r);rid=str(int(role['role_id']))
        stats=f.setdefault('stats',{}).setdefault(rid,dict(id=role['role_id'],name=role['role_name'],rank=0,fortune=0,contribute=0,normal_gift=0,advanced_gift=0))
        if op==65:
            u.authorize(role,r,24);u.require(not f['type'],'今日已举办宴会')
            typ=u.positive(d,'feast_type',3);row=FEAST[typ];u.pay(role,'gold_coin',int(row['cost_gold']))
            f.update(type=typ,end=now+r['feast_seconds']);g['popularity']+=int(row['popularity'])
            g['events'].append(role['role_name']+'举办了宴席');g['events']=g['events'][-100:]
        else:
            u.authorize(role,r,25);u.require(f['type'] and now<f['end'],'宴会尚未开放或已结束')
            if op==68:
                u.require(rid not in f['claimed'],'宴会奖励已领取');row=FEAST[f['type']]
                typ,tid,level,count=map(int,row['attach_data'].split('|'))
                journey.grant(role,[typ,tid,count,level])
                role['strength']+=int(row['strength']);role['energy']+=int(row['energy']);f['claimed'].append(rid)
                role.update(last_rece_award_time=now,train_tree_rate=int(row['rate_times(plan_tree_rate|contrib_rate)']),contrib_plus_rate=int(row['rate_times(plan_tree_rate|contrib_rate)']))
                s['feast_buff_end']=f['end'];s['feast_fam_rate']=int(row['fam_property_rate'])
            elif op==67:
                typ=u.positive(d,'gift_type',2);gift_cfg=next(v for v in r['feast_gifts'] if v['type']==typ);count=u.positive(d,'count',r['feast_gift_limit']);u.require(f['sent']+count<=r['feast_gift_limit'],'今日赠礼次数不足')
                u.pay(role,'gold_coin',gift_cfg['gold']*count);f['sent']+=count
                gain=u.contribution(role,gift_cfg['contrib']*count)
                stats['contribute']+=gain;stats['fortune']+=gift_cfg['contrib']*count;stats['normal_gift' if typ==1 else 'advanced_gift']+=count
                f['gifts'].append(dict(des_id=len(f['gifts'])+1,id=len(f['gifts'])+1,name=role['role_name'],gift_type=gift_cfg['item'],count=count,begin_time=now,end_time=f['end'],grabbed=[]))
            else:
                ident=u.positive(d,'des_id');gift=next((v for v in f['gifts'] if v['des_id']==ident),None)
                u.require(gift is not None and gift['count']>0 and rid not in gift['grabbed'],'礼物不存在、已抢完或已领取')
                u.require(f['grabbed'].get(rid,0)<r['feast_grab_limit'],'今日抢礼次数已用完')
                journey.grant(role,[5,gift['gift_type'],1,1]);gift['count']-=1;gift['grabbed'].append(rid);f['grabbed'][rid]=f['grabbed'].get(rid,0)+1
                stats['fortune']+=5;f.setdefault('log',[]).append(dict(role_id=int(rid),gift_id=ident,time=now,gift_type=gift['gift_type']));f['log']=f['log'][-100:]
                role.update(last_feast_grab_time=now,last_feast_grab_count=f['grabbed'][rid])
        return [u.reply(op,dict(result=1,gift_data=feast_data(role,s,g,now,r)['gift_data']))]
    u.require(False,'该仙盟操作尚未完成接入')
