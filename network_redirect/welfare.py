"""Original actNoticeUI contracts [A], explicitly inferred offline economy [B]."""
import json
import secrets
from pathlib import Path
from . import daily, formation as f, journey, summon, xianling, vip
from .protocol import encode, decode

ROOT = Path(__file__).resolve().parents[1]
TYPES = {20,22,7,16,23,21,24,32,33,34,35,36,48,60,67,71,74}


def load_rules(path=ROOT/'server_config/welfare_rules.json'):
    r=json.loads(Path(path).read_text())
    f.require(r['mode']=='inferred' and r['schema_version']==1, '福利配置来源无效')
    f.require(set(r['order'])==TYPES and len(r['order'])==len(TYPES), '福利分支配置不完整')
    f.require(1<=r['season_days']<=365 and r['gold_per_rmb']>0 and r['fund_price']>0, '福利周期或价格无效')
    def validate(obj):
        if isinstance(obj,dict):
            for k,v in obj.items():
                if k in ('prizes','src','extra','carnival_all'):
                    for p in v: daily.validate_prize(p)
                elif k in ('prize','gift'):daily.validate_prize(v)
                else:validate(v)
        elif isinstance(obj,list):
            for v in obj:validate(v)
    validate(r)
    f.require(len(r['turn'])<=9 and all(len(x['prizes'])==8 for x in r['turn']), '转盘需要八个位置')
    return r


def prepare(role, now, r):
    d=daily.day(now,r)
    s=role.setdefault('welfare',dict(start=now,login_days=[],claims=[],charge_days={},turn_results={},group_count=0,group_paid=0))
    if d not in s['login_days']:s['login_days'].append(d)
    if now>=s['start']+r['season_days']*86400:s.setdefault('end_level',s.get('last_level',role['level']))
    else:s['last_level']=role['level']
    for k in ('first_charge','first_charge_gift','take_charge_gift_time','buy_growup'):role.setdefault(k,0)
    settle_anniversary_mail(role,now,r,s)
    return s


def record_charge(role, gold, now, r, fund=False):
    s=prepare(role,now,r);key=str(daily.day(now,r))
    role['first_charge_gift']=1
    if not fund and not role['first_charge']:
        role['first_charge']=1
        # [A] first-charge-double; [B] eligible local gold products, bonus excluded.
        role['gold_coin']+=gold
    if now>=s['start']+r['season_days']*86400:return
    s['charge_days'][key]=s['charge_days'].get(key,0)+gold
    for typ in (48,67):
        if s['charge_days'][key] > 0:
            count=sum(v>0 for v in s['charge_days'].values())
            for i,row in enumerate(r['nian'],1):
                claim=f'{typ}:{i}'
                if row['day']<=count and claim not in s['claims']:
                    for p in row['prizes']:journey.grant(role,p)
                    s['claims'].append(claim)
    extra_count=s['charge_days'][key]//(r['any_charge_rmb']*r['gold_per_rmb'])
    for i in range(1,extra_count+1):
        if not claimed(s,67,1000+i,daily.day(now,r)):
            for p in r['nian'][0]['prizes']:journey.grant(role,p)
            mark(s,67,1000+i,daily.day(now,r))


def claimed(s,a,i,day=None):return f'{a}:{i}'+(f':{day}' if day is not None else '') in s['claims']
def mark(s,a,i,day=None):s['claims'].append(f'{a}:{i}'+(f':{day}' if day is not None else ''))
def specs(ps):return [daily.spec(p) for p in ps]
def status(s,a,i,ready,day=None):return 3 if claimed(s,a,i,day) else 2 if ready else 1

def first_prizes():
    # [A] CSV field order is object|type|level|count.
    return [[int(a),int(b),int(d),int(c)] for a,b,c,d in (t.split('|') for t in summon.rows('charge_gift_config.csv')[0]['charge_gift'].split('/'))]


def group(role,now,r):
    s=prepare(role,now,r);g=r['group'];n=s['group_count']
    discount=min([x['discount'] for x in g['discounts'] if n>=x['min_count']] or [1])
    price=int(g['price']*discount)
    return dict(activity_data=dict(end_time=s['start']+r['season_days']*86400,sale_count=n,
        sale_item=dict(item=daily.spec(g['prize']),price=g['price'],o_price=g['original_price'],buy_count=g['limit']),
        discount_list=g['discounts'],libao_item=dict(item=daily.spec(g['gift']),buy_count=g['gift_limit']),libao_attach=dict(attach_list=specs([g['gift']])),
        libao_remain=max(0,g['gift_limit']-int(n>0))),
        role_data=dict(cur_price=price,has_buy=n,ret_gold=max(0,g['price']*n-s['group_paid']),has_libao=n>0))


def catalog(role,now,r):
    s=prepare(role,now,r);d=daily.day(now,r);start=s['start'];end=start+r['season_days']*86400
    money=sum(s['charge_days'].values())/r['gold_per_rmb'];today=s['charge_days'].get(str(d),0)/r['gold_per_rmb']
    count=len(s['login_days']);level=role['level'];vip=role.get('vip_level',0)
    active=start<=now<end
    out={20:dict(prize_list=specs(first_prizes()))}
    out[22]=dict(prize_list={x['level']:specs(x['prizes']) for x in r['fund']},role_info={x['level']:dict(take_prize=claimed(s,22,x['level']),can_take=bool(role['buy_growup'] and level>=x['level'] and not claimed(s,22,x['level']))) for x in r['fund']})
    out[7]=dict(end_time=end,prize_list=[dict(min_level=x['level'],attach_list=specs(x['prizes'])) for x in r['upgrade']],role_info=dict(level=s.get('end_level',level)),had_taken_gift=claimed(s,7,0))
    out[16]=dict(end_time=end,prize_list=[specs(x['prizes']) for x in r['login']],role_info=[dict(take_prize=claimed(s,16,i)) for i in range(1,min(count,len(r['login']))+1)])
    rows={i:dict(prize_info=dict(min_money_range=x['rmb'],prize_list=specs(x['prizes'])),status=status(s,23,i,money>=x['rmb'])) for i,x in enumerate(r['charge'],1)}
    rows.update(start_time=start,end_time=end,total_charge_count=money);out[23]=dict(prize_list=rows)
    out[21]=dict(end_time=end,prize_list=[specs(x['prizes']) for x in r['carnival']],server_prize=specs(r['carnival_all']),
        role_info={i:claimed(s,21,i) for i in range(11)},role_vip_level=vip,can_take_all=money>0 and not claimed(s,21,0),
        vip_list=[dict(min_vip_count=x['count'],had_vip_count=int(vip>=x['vip'])) for x in r['carnival']])
    out[24]=group(role,now,r)
    out[32]=dict(end_time=end,flush_time=(d+1)*86400-r['timezone_offset_hours']*3600,
        combine_list=[dict(src_list=specs(x['src']),des_list=specs(x['prizes'])) for x in r['exchange']],take_flag=[claimed(s,32,i,d) for i in range(1,len(r['exchange'])+1)])
    steps=[]
    for i,x in enumerate(r['turn'],1):
        key=str(i)
        if active and money>=x['rmb'] and key not in s['turn_results']:s['turn_results'][key]=secrets.randbelow(8)+1
        steps.append(0 if claimed(s,33,10*i+s['turn_results'].get(key,0)) else s['turn_results'].get(key,0))
    out[33]=dict(end_time=end,money=money,step_list=steps,prize_data=[dict(money=x['rmb'],prize_list=specs(x['prizes'])) for x in r['turn']],
        pay_flag=[2 if claimed(s,33,i) else 1 if money>=x['rmb'] else 0 for i,x in enumerate(r['turn'],1)],
        prize_ext_data=[dict(item=daily.spec(x['extra'][0]),attach_list=specs(x['extra'])) for x in r['turn']])
    a=r['anniversary'];out[34]=dict(end_time=end,max_gold_count=a['max_gold'],min_money=a['min_rmb'],max_order=1,had_took30='anniversary' in s.get('mails',{}),
        role_charge=dict(charge_gold=money,order=1 if money else 0,had_took=claimed(s,34,0)),prize_list=[specs(a['prizes']),specs(a['prizes'])])
    c=r['common_login'];out[35]=dict(end_time=end,shop_end_time=end,login_days=count,had_took=claimed(s,35,1,d),buy_info=[claimed(s,35,i+2,d) for i in range(len(c['shop']))],
        prize_list=[specs(c['prizes']),[dict(daily.spec(x['prize']),min_vip_level=x['vip'],attach_price=x['price']) for x in c['shop']]])
    progress=s.get('task_progress',{}).get(str(d),{})
    ready=[x['id']==1 or progress.get(str(x['id']),0)>=x['count'] for x in friend_rules()]
    out[36]=dict(end_time=end,server_end_time=end,close_serial='LOCAL-1',old_serial='LOCAL-RETURN',day_tasks={x['id']:dict(had_took=claimed(s,36,x['id'],d),can_take=ready[i] and not claimed(s,36,x['id'],d)) for i,x in enumerate(friend_rules())})
    for a in (48,67):out[a]=dict(end_time=end,days=sum(v>0 for v in s['charge_days'].values()),had_took=today>0,charge_prize=[dict(attach_list=specs(x['prizes'])) for x in r['nian']],other_prize=dict(must_list=specs(r['nian'][-1]['prizes']),rand_list=specs(r['nian'][0]['prizes'])))
    out[60]=dict(end_time=end,base_pay=r['high'][0]['rmb'],up_pay=r['high'][1]['rmb']-r['high'][0]['rmb'],total_charge_money=money,
        gift_list=[dict(status=status(s,60,i,money>=x['rmb']),prize_info=dict(consume_gold=x['price'],worth_gold=x['worth'],prize_list=specs(x['prizes']))) for i,x in enumerate(r['high'],1)])
    days=charge_streak(s,d)
    out[71]=dict(end_time=end,day=days,charge_rmb=today,
        charge_data=[dict(rmb=x['rmb'],status=status(s,71,i,today>=x['rmb'],d),prize_list=specs(x['prizes'])) for i,x in enumerate(r['charge'],1)],
        ext_charge_data=[dict(day=x['days'],linear_day=days,status=status(s,71,100*i,days>=x['days']),prize_list=specs(x['prizes'])) for i,x in enumerate(r['hole_extra'],1)])
    out[74]=dict(id=1,data=dict(isopen=active,rmb=today,total_charge=money,charge_rmb=today,
        charge_data=[dict(rmb=x['rmb'],status=status(s,74,i,today>=x['rmb'],d),prize_list=specs(x['prizes'])) for i,x in enumerate(r['charge'],1)],
        total_charge_data=[dict(rmb=x['rmb'],status=status(s,74,100*i,money>=x['rmb']),prize_list=specs(x['prizes'])) for i,x in enumerate(r['daily_total'],1)]))
    return out


def handles(mid,req):return mid in (1127,1239,1352,1102,1103) or mid==1201 and req['flag']==6 or mid==1112 and req['event_id']==3


def hint(role,now,r):
    s=prepare(role,now,r);c=catalog(role,now,r)
    flags={a:False for a in r['order']}
    flags[20]=bool(role['first_charge_gift'] and not role['take_charge_gift_time'])
    flags[22]=any(x['can_take'] for x in c[22]['role_info'].values())
    flags[16]=any(not x['take_prize'] for x in c[16]['role_info'])
    flags[35]=not c[35]['had_took']
    for a in (23,60,71,74):
        rows= list(c[a]['prize_list'].values()) if a==23 else c[a]['gift_list'] if a==60 else c[a]['charge_data'] if a==71 else c[a]['data']['charge_data']
        flags[a]=any(isinstance(x,dict) and x.get('status')==2 for x in rows)
    return summon.event(80,{24:dict(activity_info=dict(had_prize_flag=flags,show_icon=False),vip_shop=xianling.hint(role,now,xianling.load_rules()),buff_data=dict(buff_type=0))})


def query(role,now,r):
    c=catalog(role,now,r)
    return summon.event(127,dict(flag=1,order_list=r['order'],all_activity=c))


def settle(role,mid,req,now,r,parse):
    s=prepare(role,now,r);c=catalog(role,now,r);d=daily.day(now,r)
    if mid in (1102,1103):return mail_request(role,mid,req,now,r,s)
    if mid==1127 and req['flag']==1:
        a=req['act_type'];f.require(a==0 or a in TYPES,'福利类型无效')
        return [query(role,now,r)] if a==0 else [summon.event(127,dict(flag=1,act_type=a,activity_data=c[a]))]
    if mid==1352 and req['id']==1:return [summon.event(202,c[74])]
    if mid==1112:
        data=parse(req['data']);f.require(data.get('item_id')==r['fund_product_id'],'本地预购商品无效')
        f.require(not role['buy_growup'],'成长基金已购买')
        # Offline purchase adapter uses the original prebuy protocol; no SDK/payment.
        role['buy_growup']=1
        role['charge_gold']=role.get('charge_gold',0)+r['fund_price']
        vr=vip.load_rules();role['vip_level']=max(role.get('vip_level',0),max(j for j,n in enumerate(vr['thresholds']) if role['charge_gold']>=n))
        vip.prepare(role,vr);record_charge(role,r['fund_price'],now,r,fund=True)
        xianling.record_charge(role,r['fund_price'],now)
        return [summon.event(55,dict(op_string='本地成长基金购买成功'))]
    if mid==1201:
        f.require(role['first_charge_gift'] and not role['take_charge_gift_time'],'尚未首充或礼包已领取')
        ps=[journey.grant(role,p) for p in first_prizes()];role['take_charge_gift_time']=now;role['first_charge_gift']=1
        # [A] event_mgr forwards this payload to firstChargeUI/rechargeUI/actNoticeUI
        # onReceiveGiftResult, which reads data.attach_list directly.
        return [summon.event(60,dict(attach_list=ps))]
    f.require(now<s['start']+r['season_days']*86400 or mid==1127 and req['act_type'] in (7,22),'福利活动已结束')
    if mid==1239:
        n=req['buy_count'];g=r['group'];old=s['group_count']
        f.require(1<=n<=g['limit']-old,'团购数量超出限购')
        new=old+n;discount=min([x['discount'] for x in g['discounts'] if new>=x['min_count']] or [1])
        total=int(g['price']*discount)*new;cost=total-s['group_paid']
        f.require(role['gold_coin']>=cost,'团购元宝不足')
        role['gold_coin']-=cost;s.update(group_count=new,group_paid=total)
        p=list(g['prize']);p[2]*=n;ps=[journey.grant(role,p)]
        if old==0 and g['gift_limit']>0:ps.append(journey.grant(role,g['gift']))
        result=group(role,now,r);result['result']=1;result['role_data']['get_item']=ps
        return [summon.event(135,result)]
    a=req.get('act_type',74);i=req.get('index',0);day=None;reward=[];keys=[]
    if mid==1352:
        f.require(req['id'] in (2,3),'每日充值操作无效');i=parse(req['data']).get('index')
        f.require(type(i) is int and i>0,'每日充值编号无效');i=i*100 if req['id']==2 else i
    else:f.require(req['flag']==2 and a in TYPES,'福利操作无效')
    def take(index,prizes,ready=True,period=None):
        f.require(ready and not claimed(s,a,index,period),'条件未满足或奖励已领取')
        keys.append((index,period));reward.extend(prizes)
    if a==22:
        f.require(i==0 and role['buy_growup'],'请先购买成长基金')
        for x in r['fund']:
            if role['level']>=x['level'] and not claimed(s,a,x['level']):take(x['level'],x['prizes'])
    elif a==7:
        f.require(i==0 and now>=s['start']+r['season_days']*86400,'等级奖励尚未结算')
        lv=s.setdefault('end_level',role['level']);eligible=[x for x in r['upgrade'] if lv>=x['level']]
        f.require(bool(eligible),'等级不足');take(0,eligible[-1]['prizes'])
    elif a==16:
        f.require(i==0,'登录领奖索引无效')
        for k,x in enumerate(r['login'],1):
            if x['day']<=len(s['login_days']) and not claimed(s,a,k):take(k,x['prizes'])
    elif a==23:
        f.require(i==0,'充值领奖索引无效')
        for k,x in enumerate(r['charge'],1):
            if c[23]['prize_list'][k]['status']==2:take(k,x['prizes'])
    elif a==21:
        f.require(0<=i<=10,'全民福利编号无效')
        take(i,r['carnival_all'] if i==0 else r['carnival'][i-1]['prizes'],c[21]['can_take_all'] if i==0 else role.get('vip_level',0)>=i)
    elif a==32:
        f.require(1<=i<=len(r['exchange']),'兑换编号无效');x=r['exchange'][i-1];take(i,x['prizes'],period=d)
        for p in x['src']:
            if p[0] in (11,12):
                k='gold_coin' if p[0]==11 else 'silver_coin';f.require(role[k]>=p[2],'兑换货币不足');role[k]-=p[2]
            else:
                items=[x for x in role['attachments'] if x['type_id']==p[1] and not x.get('is_lock')]
                f.require(sum(x['count'] for x in items)>=p[2],'兑换物品不足');left=p[2]
                for item in items:
                    n=min(left,item['count']);item['count']-=n;left-=n
                role['attachments']=[x for x in role['attachments'] if x['count']>0]
    elif a==33:
        k=i if i<10 else i//10;f.require(1<=k<=len(r['turn']),'转盘档位无效');x=r['turn'][k-1]
        if i<10:take(i,x['extra'],c[33]['pay_flag'][k-1]==1)
        else:
            selected=c[33]['step_list'][k-1];f.require(selected>0 and i%10==selected,'转盘结果不匹配');take(i,[x['prizes'][selected-1]])
    elif a==34:
        f.require(i==0,'返利编号无效');x=r['anniversary']
        f.require(now>=s['start']+(r['season_days']-1)*86400-5,'返利尚未进入结算期')
        gold=int(min(x['max_gold'],c[34]['role_charge']['charge_gold'])*10)
        take(0,[[11,0,gold,1]],gold>0)
    elif a==35:
        f.require(1<=i<=len(r['common_login']['shop'])+1,'登录特惠编号无效')
        if i==1:take(i,r['common_login']['prizes'],period=d)
        else:
            x=r['common_login']['shop'][i-2];take(i,[x['prize']],role.get('vip_level',0)>=x['vip'],d)
            f.require(role['gold_coin']>=x['price'],'元宝不足');role['gold_coin']-=x['price']
    elif a==36:
        f.require(i in c[36]['day_tasks'],'挚友任务编号无效');take(i,next(x['prizes'] for x in friend_rules() if x['id']==i),c[36]['day_tasks'][i]['can_take'],d)
    elif a==60:
        f.require(1<=i<=len(r['high']),'礼包编号无效');x=r['high'][i-1];take(i,x['prizes'],c[60]['gift_list'][i-1]['status']==2)
        f.require(role['gold_coin']>=x['price'],'元宝不足');role['gold_coin']-=x['price']
    elif a in (71,74):
        f.require(i>0,'充值奖励编号无效');k=i//100 if i>=100 else i
        rows=r['hole_extra'] if a==71 and i>=100 else r['daily_total'] if i>=100 else r['charge']
        f.require(1<=k<=len(rows) and (i<100 or i%100==0),'充值奖励编号无效')
        data=c[a] if a==71 else c[a]['data'];field=('ext_charge_data' if a==71 else 'total_charge_data') if i>=100 else 'charge_data'
        take(i,rows[k-1]['prizes'],data[field][k-1]['status']==2,None if i>=100 else d)
    else:f.require(False,'该福利通过模拟充值自动发放')
    f.require(bool(keys),'没有可领取的福利')
    prizes=[journey.grant(role,p) for p in reward]
    for k,period in keys:mark(s,a,k,period)
    if mid==1352:return [summon.event(202,dict(id=req['id'],data=prizes)),summon.event(202,catalog(role,now,r)[74])]
    result=dict(flag=2,act_type=a,index=i,result=1,prize_list=prizes)
    if a==60:result['status_list']={k:x['status'] for k,x in enumerate(catalog(role,now,r)[60]['gift_list'],1)}
    return [summon.event(127,result)]


def friend_rules():
    rows=[]
    for row in summon.rows('old_task_prize.csv'):
        field=next(k for k in row if k.startswith('prize_list'))
        ps=[[int(a),int(b),int(d),int(c)] for a,b,c,d in (x.split('|') for x in row[field].split('/'))]
        rows.append(dict(id=int(row['task_index']),count=int(row['do_times']),prizes=ps))
    return rows


def track(role,mid,req,events,now,r):
    """Only authoritative successful settlements count, never client progress."""
    s=prepare(role,now,r);gains={}
    if mid==1045 and req.get('pick_grade')==2:gains[3]=req.get('ten_pick') or 1
    for packet in events:
        m,_,data=decode(packet)
        if m not in (1027,1140):continue
        ft=data['fight_type'];win=1<=data['final_result']<=3
        if ft==6:gains[2]=1
        if ft in (2,3):gains[4]=1
        if ft==30 and win:gains[5]=1
        if ft in (1,20) and win:gains[6]=1
    if mid==1061:gains[6]=req['sweep_count']
    progress=s.setdefault('task_progress',{}).setdefault(str(daily.day(now,r)),{})
    for k,n in gains.items():progress[str(k)]=progress.get(str(k),0)+n


def charge_streak(s,day):
    # A missed day breaks consecutive recharge; yesterday's streak is retained
    # until today's first recharge, allowing an already earned milestone claim.
    cursor=day if s['charge_days'].get(str(day),0)>0 else day-1
    count=0
    while s['charge_days'].get(str(cursor),0)>0:
        count+=1;cursor-=1
    s['max_streak']=max(s.get('max_streak',0),count)
    return s['max_streak']


def settle_anniversary_mail(role,now,r,s):
    end=s['start']+r['season_days']*86400
    if now<end-86400-5:return
    mails=s.setdefault('mails',{})
    if 'anniversary' in mails:return
    money=sum(s['charge_days'].values())/r['gold_per_rmb']
    if money<r['anniversary']['min_rmb']:return
    # Single local participant is rank one; both original preview rows apply.
    prizes=r['anniversary']['prizes']*2
    mails['anniversary']=dict(mail_id=800000001,mail_title='感恩充值特惠奖励',
        mail_body='充值达标及本地排行奖励，请领取附件。',recv_time=now,
        send_time=now,prizes=prizes,claimed=False)


def mail_snapshot(role,now,r):
    s=prepare(role,now,r)
    return summon.event(13,[m['mail_id'] for m in s.get('mails',{}).values()])


def mail_request(role,mid,req,now,r,s):
    mail=next((m for m in s.get('mails',{}).values() if m['mail_id']==req['mail_id']),None)
    f.require(mail is not None,'邮件不存在')
    if mid==1102:
        ps=[] if mail['claimed'] else specs(mail['prizes'])
        return [summon.event(14,dict(mail_id=mail['mail_id'],mail_title=mail['mail_title'],
            mail_body=mail['mail_body'],recv_time=mail['recv_time'],send_time=mail['send_time'],
            attach_count=len(ps),attach_list=ps,flag=req['flag']))]
    f.require(not mail['claimed'],'邮件附件已领取')
    prizes=[journey.grant(role,p) for p in mail['prizes']];mail['claimed']=True
    return [summon.event(15,dict(result=1,mail_id=mail['mail_id'],attach_count=len(prizes),attach_list=prizes))]
