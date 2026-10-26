"""Bounded activity log and original prey_week_rank rewards, local weekly settlement."""
from . import activity as a, summon, welfare
from . import activity_land_npc as npc


def news(s,now,body):
    entries=s.setdefault('news',[])
    entries.append(dict(time=now,body=body))
    del entries[:-30]
    s['had_news']=True


def gain(s,amount):
    s['soul_count']+=amount
    s['week_soul']=s.get('week_soul',0)+amount


def titles(role,s,now):
    # [A] title_config thresholds; [B] seven days from first achievement.
    awarded=s.setdefault('title_layers',[])
    for tid,layer in zip(range(120,125),(32,40,48,55,60)):
        if s['boss_layer']>=layer and tid not in awarded:
            role.setdefault('profile_titles',{})[str(tid)]=dict(id=tid,begintime=now,endtime=now+7*86400)
            awarded.append(tid)


def weekly(role,s,now,r):
    # Unix epoch was Thursday; Monday is day 4. Keep the account's last active week.
    week=(a.day(now,r)-4)//7
    previous=s.setdefault('week',week)
    s.setdefault('week_soul',0)
    if week<=previous:return
    if s['week_soul']>0:
        _,mine=npc.ranking(role,s,False,2,final=True)
        s['last_week_result']=dict(week=previous,rank=mine['order'],soul=s['week_soul'])
        expiry=((previous+2)*7+4)*86400-r['timezone_offset_hours']*3600
        if mine['order']<=10 and now<expiry:
            rank=mine['order'];tid=125+(3 if rank==1 else 2 if rank<=3 else 1 if rank<=6 else 0)
            role.setdefault('profile_titles',{})[str(tid)]=dict(id=tid,begintime=expiry-7*86400,endtime=expiry)
        row=next((v for v in summon.rows('prey_week_rank.csv') if int(v['min_rank'])<=mine['order']<=int(v['max_rank'])),None)
        if row:
            prizes=[]
            for token in row['attach_list(object|type|level|count)'].split('/'):
                kind,tid,level,count=map(int,token.split('|'));prizes.append([kind,tid,count,level])
            state=welfare.prepare(role,now,welfare.load_rules());mails=state.setdefault('mails',{})
            key='land-week-'+str(previous)
            if key not in mails:
                ident=max({800000000}|{m['mail_id'] for m in mails.values()})+1
                mails[key]=dict(mail_id=ident,mail_title='猎魂之地周榜奖励',
                    mail_body=f"离线猎魂之地周榜第{mine['order']}名。附件永久有效，仅可领取一次。",
                    recv_time=now,send_time=now,prizes=prizes,claimed=False,no_expiry=True,expires_at=None,
                    sender='系统',delivery_key=key)
                news(s,now,f"上周逐鹿排名第{mine['order']}，奖励已发至系统邮件。")
    s['week']=week;s['week_soul']=0
