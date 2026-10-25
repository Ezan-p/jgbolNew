"""Original 1303 / event145 contract, account-local three-member NPC teams."""
import copy
from . import activity as a, summon
from .protocol import encode
from . import activity_land as land, activity_land_npc as npc


def summary(role,s,now,r):
    team=s.get('team')
    return dict(has_team=bool(team),is_captain=bool(team and team['captain_id']==role['role_id']),
                begin_time=land.status(now,r)['begin_time'],end_time=(s['day']+1)*86400-r['timezone_offset_hours']*3600)


def member(role,s):
    army=sorted((c for c in role['corteges'] if c.get('order')),key=lambda c:c['order'])
    head=army[0] if army else dict(type=1,reborn_layer=0)
    return dict(id=role['role_id'],name=role['role_name'],head_type=head['type'],type_id=head['type'],
                cortege_layer=head.get('reborn_layer',0),power=sum(c.get('combat_power',0) for c in army[:s['grid_count']]),level=role['level'])


def available(role,s):
    return [dict(name=m['name']+'的队伍',captain_id=m['id'],count=1,avg_power=m['power'],members=[m]) for m in npc.roster(role,s)]


def data(role,s):
    team=s.get('team')
    result=dict(all_teams=available(role,s),apply_count=0,apply_list=[])
    if team:
        members=[member(role,s) if m['id']==role['role_id'] else copy.deepcopy(m) for m in team['members']]
        result.update(my_team=members,captain_id=team['captain_id'],apply_list=copy.deepcopy(team['applications']),
                      apply_count=len(team['applications']),is_lock=team.get('locked',False))
    return result


def settle(role,req,now,r,parse):
    a.require(req['id']==1 and role['level']>=38,'该组队类型尚未开放')
    d=parse(req['data']) if req['data'] else {};a.require(isinstance(d,dict),'组队参数无效')
    s=land.state(role,now,r);op=req['op_type'];team=s.get('team')
    def reply(code=1,extra=None,operation=None):
        return summon.event(145,dict(id=1,op_type=operation or op,result=code,team_data=extra if extra is not None else data(role,s)))
    if op==9:
        q=d.get('query_type',1);a.require(type(q)is int and 1<=q<=4,'查询类型无效')
        result=data(role,s);result['query_type']=q
        if q==3:
            ids=id_list(d);row=next((t for t in result['all_teams'] if t['captain_id']==ids[0]),None)
            a.require(row is not None,'队伍不存在');result.update(one_team=row['members'],captain_id=row['captain_id'])
        return [reply(extra=result)]
    a.require(not s['tower_id'],'请先退出占塔再调整队伍')
    if op==1:
        a.require(not team,'已有队伍')
        s['team']=dict(captain_id=role['role_id'],members=[member(role,s)],applications=npc.roster(role,s),locked=False)
    elif op==2:
        a.require(not team,'已有队伍');ids=id_list(d)
        row=next((t for t in available(role,s) if t['captain_id']==ids[0]),None)
        a.require(row is not None,'队伍不存在')
        # NPC immediately accepts, and delegates command to the local player.
        s['team']=dict(captain_id=role['role_id'],members=[member(role,s),row['members'][0]],applications=[],locked=False)
        return [reply(),reply(operation=1),update(role,s,now,r)]
    else:
        a.require(team is not None,'尚未组队')
        a.require(op==6 or team['captain_id']==role['role_id'],'只有队长可操作')
        if op in (6,7):s['team']=None
        elif op==10:pass
        elif op==5:team['applications']=[]
        elif op in (3,4,8,11,14):
            ids=id_list(d)
            if op in (3,4):
                choices={m['id']:m for m in team['applications']}
                a.require(all(i in choices for i in ids),'申请已失效')
                if op==3:
                    a.require(not team.get('locked') and len(team['members'])+len(ids)<=3,'队伍已锁定或人数已满')
                    team['members'].extend(choices[i] for i in ids)
                team['applications']=[m for m in team['applications'] if m['id'] not in ids]
            else:
                choices={m['id']:m for m in team['members']}
                a.require(all(i in choices for i in ids),'队员不存在')
                if op==8:
                    a.require(role['role_id'] not in ids,'不能踢出自己')
                    team['members']=[m for m in team['members'] if m['id'] not in ids]
                elif op==11:
                    a.require(set(ids)==set(choices),'出场顺序必须包含全部队员')
                    team['members']=[choices[i] for i in ids]
                else:
                    # Offline companions keep local command available.
                    a.require(ids==[role['role_id']],'离线队伍由当前玩家指挥');team['captain_id']=role['role_id']
        elif op in (12,13):team['locked']=op==12
        else:a.require(False,'组队操作无效')
    return [reply(),update(role,s,now,r)]


def id_list(d):
    values=d.get('id_list')
    if isinstance(values,dict):
        a.require(set(values)==set(range(1,len(values)+1)),'成员索引无效');values=list(values.values())
    a.require(isinstance(values,list) and values and len(values)<=3 and all(type(i)is int or type(i)is float and i.is_integer() for i in values) and len(set(values))==len(values),'成员参数无效')
    return [int(i) for i in values]


def update(role,s,now,r):
    return encode(2995,dict(tip_type=2,tip_info=summon.lua(dict(team_info=summary(role,s,now,r)))))
