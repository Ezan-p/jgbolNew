"""捕魂达人 1226/event155. Shipped tables [A], missing server policies [B]."""
import copy
import hashlib
import json
import secrets
from pathlib import Path
from . import formation as f, summon, journey, welfare
from . import activity_hunt_geometry as geometry

ROOT = Path(__file__).resolve().parents[1]
BALLS = {int(v['ball_type']): {k:int(v[k]) for k in ('need_energy','bump_times')}
         for v in summon.rows('hunt_ball_config.csv')}
SOULS = {int(v['soul_type']): {k:int(v[k]) for k in ('soul_value','base_count','rand_count','rand_weight')}
         for v in summon.rows('hunt_soul_config.csv')}
PRIZES = {kind:summon.rows('hunt_'+kind+'_prize.csv') for kind in ('day','week')}


def load_rules(path=ROOT/'server_config/hunt_rules.json'):
    r=json.loads(Path(path).read_text())
    f.require(r.get('schema_version')==1 and r.get('mode')=='inferred' and bool(r.get('revision')), '捕魂配置来源无效')
    for k,limit in [('daily_shots',1000),('daily_refreshes',100),('energy_exchange_rate',1000),
                    ('store_refresh_soul',100000),('capture_radius',50),('combo_percent_per_extra',100),
                    ('combo_max_percent',200),('npc_count',99),('npc_daily_min',100000),('npc_daily_max',100000)]:
        f.require(type(r.get(k)) is int and 0<r[k]<=limit,'捕魂配置无效：'+k)
    f.require(r['npc_daily_min']<=r['npc_daily_max'],'捕魂NPC积分范围无效')
    f.require(len(r['shop'])==6,'离线灵魂商店须配置六件商品')
    for row in r['shop']:
        p=row['reward']
        f.require(len(p)==4 and all(type(v)is int for v in p) and p[0]==5 and p[1] in f.ITEMS
                  and 0<p[2]<=1000 and p[3]==1,'捕魂商品无效')
        f.require(type(row['cost']) is int and 0<row['cost']<=100000
                  and type(row['limit']) is int and 0<row['limit']<=100,'捕魂价格或限购无效')
    f.require(r['soul_box_pool']==list(range(5001,5006)),'灵魂宝箱必须产出五星五界魂')
    f.require(bool(r['upgrade_box_pool']) and len(set(r['upgrade_box_pool'])) == len(r['upgrade_box_pool'])
              and all(t in (1310,1311,1312,1313,1314,1320,1321,1322,1323)
                      for t in r['upgrade_box_pool']),'升阶宝箱必须产出装备升阶材料')
    return r


def day(now, ar):return (now+ar['timezone_offset_hours']*3600)//86400
def week(d):return (d-4)//7
def stable(*args):return int.from_bytes(hashlib.sha256(':'.join(map(str,args)).encode()).digest()[:8],'big')


def rewards(kind,rank):
    row=next((v for v in PRIZES[kind] if int(v['min_rank'])<=rank<=int(v['max_rank'])),None)
    if not row:return []
    return [[a,b,n,lv] for a,b,lv,n in (map(int,v.split('|')) for v in row['attach_list(object|type|level|count)'].split('/'))]


def ranking(role,s,kind,period,score,r,progress=1):
    # [B] Stable, account-local NPC competitors; never ranks by spendable balance.
    from . import npc_players
    pool=sorted(npc_players.catalog().values(),key=lambda v:v['npc_id'])
    out=[]
    for i in range(r['npc_count']):
        p=pool[i*(len(pool)-1)//max(1,r['npc_count']-1)]['profile']
        days=range(period*7+4,period*7+11) if kind=='week' else [period]
        value=sum(r['npc_daily_min']+stable(p['role_id'],d,'hunt')%(r['npc_daily_max']-r['npc_daily_min']+1) for d in days)
        value=int(value*progress)
        if value:out.append(dict(role_id=p['role_id'],name=p['role_name'],soul_count=value))
    if score>0:out.append(dict(role_id=role['role_id'],name=role['role_name'],soul_count=score))
    out.sort(key=lambda v:(-v['soul_count'],v['role_id']))
    for i,v in enumerate(out,1):v['order']=i
    mine=next((dict(v) for v in out if v['role_id']==role['role_id']),dict(order=0,soul_count=0,name=role['role_name']))
    return out[:100],mine


def mail(role,key,title,prizes,now):
    if not prizes:return
    mails=welfare.prepare(role,now,welfare.load_rules()).setdefault('mails',{})
    if key not in mails:
        ident=max({800000000}|{m['mail_id'] for m in mails.values()})+1
        mails[key]=dict(mail_id=ident,mail_title=title,mail_body='捕魂达人离线榜单结算。附件永久有效，仅可领取一次。',
                        recv_time=now,send_time=now,prizes=copy.deepcopy(prizes),claimed=False,
                        no_expiry=True,expires_at=None,sender='系统',delivery_key=key)


def history(s,kind,rows):
    """[B] Historical boards retain each participant's highest observed period."""
    records=s.setdefault('history_'+kind,{})
    for row in rows:
        key=str(row['role_id'])
        if row['soul_count']>records.get(key,{}).get('soul_count',0):records[key]=dict(row)
    out=sorted((dict(v) for v in records.values()),key=lambda v:(-v['soul_count'],v['role_id']))
    for i,v in enumerate(out,1):v['order']=i
    return out


def state(role,now,ar,r=None):
    r=r or load_rules();d=day(now,ar);w=week(d)
    s=role.setdefault('activity',{}).get('hunt')
    if s is None:
        s=dict(version=1,day=d,week=w,clock=now,energy=400,soul=0,day_score=0,week_score=0,
               best_day=0,best_week=0,shots=0,refreshes=0,points=geometry.board(SOULS),
               shop_day=(now+ar['timezone_offset_hours']*3600-21600)//86400,bought={},last_week={},last_day={})
        role['activity']['hunt']=s
    # Queries never rewind stored periods. Mutations separately reject rollback.
    if now<s['clock']:return s
    s['clock']=now
    if d>s['day']:
        rows,mine=ranking(role,s,'day',s['day'],s['day_score'],r)
        history(s,'day',rows)
        s['last_day']=dict(period=s['day'],top_list=rows,my_order=mine)
        s['best_day']=max(s['best_day'],s['day_score'])
        mail(role,'hunt-day-'+str(s['day']),'捕魂达人日榜奖励',rewards('day',mine['order']),now)
        s.update(energy=min(1000,s['energy']+400*(d-s['day'])),day=d,day_score=0,shots=0,refreshes=0)
    if w>s['week']:
        old=s['last_week']
        if old and not old['claimed']:
            mail(role,'hunt-week-'+str(old['period']),'捕魂达人未领周榜奖励',old['prizes'],now)
        rows,mine=ranking(role,s,'week',s['week'],s['week_score'],r)
        history(s,'week',rows)
        end=((s['week']+2)*7+4)*86400-ar['timezone_offset_hours']*3600
        if 0<mine['order']<=10 and now<end:
            rank=mine['order'];tid=130+(3 if rank==1 else 2 if rank<=3 else 1 if rank<=6 else 0)
            role.setdefault('profile_titles',{})[str(tid)]=dict(id=tid,begintime=end-604800,endtime=end)
        s['last_week']=dict(period=s['week'],top_list=rows,my_order=mine,prizes=rewards('week',mine['order']),claimed=False)
        s['best_week']=max(s['best_week'],s['week_score'])
        s.update(week=w,week_score=0)
        # A long absence cannot resurrect an old award week or its title.
        if s['last_week']['period']<w-1:
            old=s['last_week'];mail(role,'hunt-week-'+str(old['period']),'捕魂达人未领周榜奖励',old['prizes'],now)
            s['last_week']={}
    shop_day=(now+ar['timezone_offset_hours']*3600-21600)//86400
    if shop_day>s['shop_day']:s.update(shop_day=shop_day,bought={})
    return s


def status(role,now,ar):
    s=state(role,now,ar) if role.get('level',1)>=20 or 'hunt' in role.get('activity',{}) else {}
    last=s.get('last_week',{})
    return dict(begin_time=1,end_time=2147483647,is_open=True,
                has_week_prize=bool(last.get('prizes')) and not last.get('claimed',False))


def snapshot(s,r,points=True):
    data=dict(left_energy=s['energy'],left_soul_count=s['soul'],left_ball_times=r['daily_shots']-s['shots'],
              left_flush_times=r['daily_refreshes']-s['refreshes'])
    if points:data['point_list']=copy.deepcopy(s['points'])
    return data


def store(s,r):
    from .activity import prize_spec
    return dict(flush_need_soul=r['store_refresh_soul'],item_list=[dict(prize_spec(v['reward']),
                need_soul=v['cost'],buy_times=v['limit']-s['bought'].get(str(i),0)) for i,v in enumerate(r['shop'],1)])


def settle(role,req,now,ar):
    r=load_rules();f.require(role['level']>=20,'捕魂达人20级开放')
    s=state(role,now,ar,r);f.require(now>=s['clock'],'捕魂时间已回退，请恢复本地时间')
    flag=req['flag'];count=req.get('count',0);index=req.get('index',0)
    f.require(type(flag)is int and 1<=flag<=13,'捕魂操作无效')
    f.require(type(count)is int and type(index)is int,'捕魂参数无效')
    result=dict(flag=flag)
    if flag==1:
        result.update(role_hunt_data=snapshot(s,r),hunt_const_config=dict(max_energy=1000,energy_exchange_rate=r['energy_exchange_rate']))
    elif flag==2:
        f.require(count in BALLS and 30<=index<=150,'摄魂珠档位或角度无效')
        ball=BALLS[count];f.require(s['shots']<r['daily_shots'],'今日发射次数已用尽')
        f.require(s['energy']>=ball['need_energy'],'摄魂能量不足')
        move,caught=geometry.trace(s['points'],index,ball['bump_times'],r['capture_radius'])
        base=sum(SOULS[s['points'][i]['soul_type']]['soul_value'] for i in caught)
        bonus=base*min(r['combo_max_percent'],max(0,len(caught)-1)*r['combo_percent_per_extra'])//100
        s['energy']-=ball['need_energy'];s['shots']+=1;s['soul']+=base+bonus
        s['day_score']+=base+bonus;s['week_score']+=base+bonus
        s['points']=[v for i,v in enumerate(s['points']) if i not in caught]
        cleared=not s['points']
        if cleared:s['points']=geometry.board(SOULS)
        move.update(extra_soul=bonus,base_soul=base,captured_count=len(caught),board_cleared=cleared)
        result.update(role_hunt_data=snapshot(s,r,points=cleared),move_result=move)
    elif flag==3:
        f.require(1<=count<=1000 and index==0 and s['energy']+count<=1000,'能量兑换数量无效或超过上限')
        from .activity import spend
        spend(s,'soul',count*r['energy_exchange_rate']);s['energy']+=count
        result['role_hunt_data']=snapshot(s,r,False)
    elif flag==4:
        f.require(s['refreshes']<r['daily_refreshes'],'今日刷新次数已用尽')
        s['refreshes']+=1;s['points']=geometry.board(SOULS);result['role_hunt_data']=snapshot(s,r)
    elif flag==5:result['store_data']=store(s,r)
    elif flag==6:
        f.require(1<=index<=len(r['shop']) and 1<=count<=100,'商品或购买数量无效')
        row=r['shop'][index-1];key=str(index);bought=s['bought'].get(key,0)
        f.require(bought+count<=row['limit'],'商品剩余次数不足')
        from .activity import spend
        spend(s,'soul',row['cost']*count);p=list(row['reward']);p[2]*=count
        prize=journey.grant(role,p);s['bought'][key]=bought+count
        result.update(role_hunt_data=snapshot(s,r,False),item_index=index,buy_times=row['limit']-bought-count,attach_list=[prize])
    elif flag==7:
        from .activity import spend
        spend(s,'soul',r['store_refresh_soul']);s['bought']={}
        result.update(role_hunt_data=snapshot(s,r,False),store_data=store(s,r))
    elif flag in (8,9,12,13):
        weekly=flag in (9,13);kind='week' if weekly else 'day';period=s[kind]
        score=s[kind+'_score']
        seconds=(now+ar['timezone_offset_hours']*3600)%86400
        progress=(seconds/86400+(s['day']-(s['week']*7+4) if weekly else 0))/(7 if weekly else 1)
        rows,mine=ranking(role,s,kind,period,score,r,progress)
        if flag in (12,13):
            rows=history(s,kind,rows)
            mine=next((dict(v) for v in rows if v['role_id']==role['role_id']),dict(order=0,soul_count=0))
        result.update(top_list=rows,my_order=mine)
    elif flag==10:
        last=s['last_week'];result.update(top_list=copy.deepcopy(last.get('top_list',[])),
            my_order=copy.deepcopy(last.get('my_order',dict(order=0,soul_count=0))),
            had_prize=bool(last.get('prizes')),had_got_prize=last.get('claimed',False))
    elif flag==11:
        last=s['last_week'];f.require(last.get('prizes') and not last['claimed'],'没有可领取的上周奖励')
        result['prize_list']=[journey.grant(role,p) for p in last['prizes']];last['claimed']=True
    return [summon.event(155,result)]


def use_item(role,req,now,ar):
    r=load_rules();tid,n=req['item_type'],req['item_count']
    f.require(tid in (1036,1037,1324) and type(n)is int and 1<=n<=100,'捕魂奖励道具数量无效')
    f.require(req['des_type']==1 and req['des_id'] in (0,role['role_id']),'道具使用目标无效')
    item=f.lookup(role,'attachments',req['item_id'])
    f.require(item['attach_type']==5 and item['type_id']==tid and item['count']>=n
              and not item.get('is_lock') and not item.get('owner_id') and not item.get('equip_pos'),'道具不足或不可使用')
    s=state(role,now,ar,r);f.require(now>=s['clock'],'捕魂时间已回退，请恢复本地时间')
    item['count']-=n
    if not item['count']:role['attachments'].remove(item)
    prizes=[]
    if tid==1036:s['soul']+=100*n  # [A] face value; [B] card does not inflate competition scores.
    else:
        pool=r['soul_box_pool' if tid==1037 else 'upgrade_box_pool'];counts={}
        for _ in range(n):
            target=secrets.choice(pool);counts[target]=counts.get(target,0)+1
        prizes=[journey.grant(role,[5,t,c,1]) for t,c in sorted(counts.items())]
    return [summon.event(21,dict(result=1,type_id=tid,count=n,attach_list=prizes,soul_gain=100*n if tid==1036 else 0))]
