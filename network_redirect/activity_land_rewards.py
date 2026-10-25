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


def weekly(role,s,now,r):
    # Unix epoch was Thursday; Monday is day 4. Keep the account's last active week.
    week=(a.day(now,r)-4)//7
    previous=s.setdefault('week',week)
    s.setdefault('week_soul',0)
    if week<=previous:return
    if s['week_soul']>0:
        _,mine=npc.ranking(role,s,False,2)
        row=next((v for v in summon.rows('prey_week_rank.csv') if int(v['min_rank'])<=mine['order']<=int(v['max_rank'])),None)
        if row:
            prizes=[]
            for token in row['attach_list(object|type|level|count)'].split('/'):
                kind,tid,level,count=map(int,token.split('|'));prizes.append([kind,tid,count,level])
            state=welfare.prepare(role,now,welfare.load_rules());mails=state.setdefault('mails',{})
            key='land-week-'+str(previous)
            if key not in mails:
                ident=max({800000000}|{m['mail_id'] for m in mails.values()})+1
                mails[key]=dict(mail_id=ident,mail_title='逐鹿周榜奖励',
                    mail_body=f"离线逐鹿周榜第{mine['order']}名。附件永久有效，仅可领取一次。",
                    recv_time=now,send_time=now,prizes=prizes,claimed=False,no_expiry=True,expires_at=None,
                    sender='系统',delivery_key=key)
                news(s,now,f"上周逐鹿排名第{mine['order']}，奖励已发至系统邮件。")
    s['week']=week;s['week_soul']=0
