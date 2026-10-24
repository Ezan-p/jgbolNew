"""Original home friend wire contracts; explicitly offline NPC cooperation [B]."""
import copy
from . import activity as a
from . import activity_home as h


def states(s,now,r):
    friends=s.setdefault('offline_friends',{})
    for cfg in r['home_offline_friends']:
        f=friends.setdefault(str(cfg['id']),{})
        if f.get('day')!=a.day(now,r):
            start=now-(now+8*3600)%86400
            f.update(day=a.day(now,r),invited=False,plants={str(i):dict(level=0,seed_type=1,
                start_time=start,plant_time=start,gain_time=start+int(h.SEEDS[1]['gain_hour'])*3600,
                cur_plus_times=0,total_plus_times=int(h.SEEDS[1]['friend_plus_times']),
                benefit_flag=True,event_info=[],missed_events=0) for i in range(1,4)})
        f.setdefault('messages',[])
    return friends


def summary(cfg,f,now):
    return dict(id=cfg['id'],name=cfg['name'],level=50,home_level=1,point=0,show_type=1001,
        reborn_layer=0,has_open=True,has_invited=f['invited'],
        benefit_flag=any(p['benefit_flag'] and now<p['gain_time'] for p in f['plants'].values()))


def settle(role,s,op,d,now,r):
    friends=states(s,now,r)
    if op==13:return [h.response(op,dict(friend_data={c['id']:summary(c,friends[str(c['id'])],now) for c in r['home_offline_friends']}))]
    fid=d.get('friend_id');a.require(type(fid)is int and str(fid) in friends,'洞府好友不存在')
    f=friends[str(fid)];cfg=next(c for c in r['home_offline_friends'] if c['id']==fid)
    if op==6:
        npc=copy.deepcopy(s);npc.update(level=1,build={str(i):1 for i in h.KEYS},plants=f['plants'],messages=f['messages'],new_event=False,pets=[],pet_growth={})
        data=h.info(npc,r);data['base_data']['upgrade_info'].update(has_passed=False,fight_count=0)
        return [h.response(op,data)]
    if op==12:
        msg=d.get('chat_msg');a.require(isinstance(msg,str) and 1<=len(msg.strip())<=200 and '\x00' not in msg,'留言需要1至200字')
        f['messages'].append(f"{role['role_name']}：{msg.strip()}");f['messages']=f['messages'][-30:]
        return [h.response(op,{})]
    if op==5:
        a.require(not f['invited'],'今日已经邀请该离线好友');f['invited']=True
        helped=0
        for p in s['plants'].values():
            if p.get('seed_type') and now<p['gain_time'] and p['cur_plus_times']<p['total_plus_times']:
                p['cur_plus_times']+=1;helped+=1
        s.setdefault('messages',[]).append(f"{cfg['name']}应邀来访，为{helped}块药田施肥。")
        s['messages']=s['messages'][-30:];s['new_event']=True
        return [h.response(op,{})]
    if op==23:a.require(role.get('month_card_time',0)>now,'一键施肥需要有效月卡')
    idx=d.get('plant_grid')
    if op==7:a.require(type(idx)is int and str(idx) in f['plants'],'药田不存在')
    targets=list(f['plants']) if op==23 else [str(idx)]
    changed={};prizes={}
    for key in targets:
        p=f['plants'][key]
        if not p['benefit_flag'] or now>=p['gain_time'] or p['cur_plus_times']>=p['total_plus_times']:continue
        p['benefit_flag']=False;p['cur_plus_times']+=1;changed[int(key)]=p['cur_plus_times']
        prizes[int(key)]=a.prizes(role,[[12,0,r['home_friend_silver'],1]])[0]
    if op==7:
        a.require(bool(changed),'该药田已施肥或已成熟')
        return [h.response(op,dict(plant_grid=idx,cur_plus_times=changed[idx],prize_list=[prizes[idx]]))]
    return [h.response(op,dict(plants_plus_time=changed,prize_list=prizes))]
