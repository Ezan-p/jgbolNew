"""渡劫: original client contracts, account-local NPC matchmaking and settlement."""
import copy
import secrets
import json
from functools import lru_cache
from . import activity as a, activity_rape_npc as npcs, activity_rank, formation, journey, summon, cheer, combat, reborn_stars
from .protocol import encode


@lru_cache(maxsize=1)
def rules():
    r=json.loads((a.ROOT/'server_config/rape_rules.json').read_text())
    a.require(r['mode']=='inferred' and len(r['power_percent'])==3 and all(type(v)is int and 1<=v<=150 for v in r['power_percent']), '渡劫匹配配置无效')
    a.require(r.get('guards_from_dice') is True and 1<=r['straight_skill_count']<=10 and r['triple_auto_pass'] is False, '渡劫奖盘配置无效')
    a.require(1<=r['revenge_lifetime']<=86400 and set(r['skill_quality_weights'])==set('12345') and all(type(v)is int and 1<=v<=100 for v in r['skill_quality_weights'].values()), '渡劫奖池配置无效')
    a.require(all(type(r.get(k)) is int and 1<=r[k]<=100 for k in ('match_candidates','match_tolerance_percent','recent_npc_limit')), '渡劫NPC随机池配置无效')
    return r


def roll_forms():
    return [secrets.randbelow(6)+1 for _ in range(3)]


def choose(role, index, excluded=(), used=()):
    return npcs.choose(role, index, rules(), excluded, used)


def opponent(role, index, excluded=(), used=()):
    key = choose(role, index, excluded, used); n = npcs.catalog()[key]['role']
    head = next(c for c in n['corteges'] if c.get('order') == 1)
    return dict(npc_id=key, npc_player_id=n['role_id'], show_type=head['type'], level=n['level'], name=n['role_name'],
                has_win=False, top_order=0, cortege_layer=head.get('evolve_level',0), power=n['role_combat_power'])


def next_id(s):
    s['rape_sequence'] = s.get('rape_sequence', 950000)+1
    return s['rape_sequence']


@lru_cache(maxsize=1)
def reward_pool():
    return [int(row['type_id']) for row in summon.rows('skill_name.csv')
            if '渡劫' in row.get('product_desc','') and int(row['type_id']) in formation.SKILLS
            for _ in range(rules()['skill_quality_weights'][str(formation.SKILLS[int(row['type_id'])]['quality'])])]


def ensure(role, now, r):
    s = role['activity']
    s.setdefault('rape_total_refreshes',s.get('rape_refreshes',0))
    boards = s.get('rape_boards')
    if boards is None:
        dice = roll_forms()
        straight = dice[1]-dice[0] == dice[2]-dice[1] and abs(dice[1]-dice[0]) == 1
        pool = reward_pool() or r['rape_skills']
        boards=[];used=[]
        for i in range(3):
            rows={}
            for j in range(dice[i]):
                target=opponent(role,j,used=used);used.append(target['npc_id']);target.update(index=j+1,rand=6-j);rows[str(next_id(s))]=target
            boards.append(dict(version=2,form_type=dice[i],skill_type=secrets.choice(pool),skill_count=rules()['straight_skill_count'] if straight else 1,
                               reward_claimed=False,form_list={'1':{},'2':rows}))
        s['rape_boards']=boards
        npcs.remember(role,used,rules())
    # Upgrade old boards in place without erasing victories or issuing rewards again.
    for i,b in enumerate(boards):
        if b.get('version',1)<2:
            # Keep legacy progress and already-issued rewards; align the die with
            # its existing guards instead of adding or removing live opponents.
            b['form_type']=sum(len(rows) for rows in b['form_list'].values())
            b['version']=2
        b.setdefault('form_type',i+1)
        b['form_list'].setdefault('1',{})
        b.setdefault('reward_claimed', all(t['has_win'] for rows in b['form_list'].values() for t in rows.values()))
        for rows in b['form_list'].values():
            for j,t in enumerate(rows.values()):
                t.setdefault('index',j+1);t.setdefault('rand',3-j)
                if 'npc_id' not in t:
                    won=t['has_win'];t.update(opponent(role,j));t['has_win']=won
    s.setdefault('rape_revenge',{})
    s['rape_revenge']={k:v for k,v in s['rape_revenge'].items() if now-v['time']<rules()['revenge_lifetime']}
    return boards


def board(role, now, r, update=1):
    boards=copy.deepcopy(ensure(role,now,r))
    for b in boards:
        b.pop('reward_claimed',None);b.pop('version',None)
        b['form_list']={int(t):{int(k):{f:v for f,v in row.items() if f not in ('npc_id','power')} for k,row in rows.items()} for t,rows in b['form_list'].items()}
    return dict(time=now,update_type=update,used_count=role['activity']['rape_refreshes'],free_count=max(0,role['rape_flush_limit']-role['activity']['rape_refreshes']),gold_cost=r['rape_refresh_gold'],rape_list=boards)


def messages(role):
    return summon.event(78,{int(k):{f:v for f,v in row.items() if f!='npc_id'} for k,row in role['activity'].get('rape_revenge',{}).items()})


def inspection(role, ident):
    s=role['activity']; target=next((v for b in s.get('rape_boards') or [] for rows in b['form_list'].values() for k,v in rows.items() if int(k)==ident),None)
    if target is None:target=next((v for v in s.get('rape_revenge',{}).values() if v['id']==ident),None)
    if target is None:return None
    from . import npc_players
    return summon.event(11, npc_players.inspection_data(npcs.catalog()[target['npc_id']], scene_id=ident))


def battle(role, req, now, r, jrules):
    a.require(role['level']>=8,'渡劫需8级');boards=ensure(role,now,r);s=role['activity'];ft=req['fight_type']
    if ft==12:
        target=s['rape_revenge'].get(str(int(req['des_id'])))
        a.require(target is not None and not target['has_win'] and req['des_type']==1 and req['des_value']==target['skill_type'],'反击请求已失效')
    else:
        idx=req['des_value'];a.require(1<=idx<=3,'渡劫阵位无效');b=boards[idx-1]
        target=b['form_list'].get(str(req['des_type']),{}).get(str(int(req['des_id'])))
        a.require(target is not None and not target['has_win'],'对手不存在或已击败')
    a.require(any(1<=c.get('order',0)<=8 for c in role['corteges']),'请先上阵神仙');a.spend(role,'energy',1)
    result,lineup,actions=journey.battle(role,{},jrules,units=(activity_rank.units(role),activity_rank.units(npcs.catalog()[target['npc_id']]['role'])))
    win=1<=result<=3;events=[];s['fight_id']+=1;fid=s['fight_id']
    if win:target['has_win']=True
    if ft==12:
        if win:
            journey.grant(role,(6,target['skill_type'],1,1))
            role['silver_coin']+=r['battle_silver']
        events.append(summon.event(77,dict(result=0 if win else 1,request_id=int(req['des_id']))))
    else:
        passed=all(t['has_win'] for rows in b['form_list'].values() for t in rows.values());count=0
        if passed and not b['reward_claimed']:
            count+=b['skill_count'];journey.grant(role,(6,b['skill_type'],b['skill_count'],1));b['reward_claimed']=True
        events.append(summon.event(41,dict(fight_result=result,form_index=idx,pass_one_form=passed,pass_all_form=all(x['reward_claimed'] for x in boards),skill_count=count,skill_type=b['skill_type'])))
        # One optional local rematch per day, only after a real loss; no inventory theft.
        if not win and s.get('rape_revenge_day')!=s['day']:
            ident=next_id(s);s['rape_revenge_day']=s['day']
            s['rape_revenge'][str(ident)]=dict(id=int(req['des_id']),npc_id=target['npc_id'],name=target['name'],level=target['level'],time=now,skill_type=b['skill_type'],has_win=False)
            events.append(messages(role))
    return journey.combat_engine.event_packets(actions,fid)+[encode(1028,dict(fight_id=fid,first_hand=1,des_name=target['name'],lineup_count=len(lineup),lineup=lineup)),encode(1027,dict(fight_id=fid,fight_type=ft,final_result=result,fight_round=len(actions),fight_result=actions))]+events+[summon.event(44,dict(fight_id=fid,fight_type=ft))]


def settle(role,mid,req,now,r,jrules,parse):
    a.require(role['level']>=8,'渡劫需8级');s=role['activity'];ensure(role,now,r)
    if mid==1026:return battle(role,req,now,r,jrules)
    if mid==1060:
        key=str(int(req['request_id']));a.require(key in s['rape_revenge'],'反击消息不存在或已过期')
        del s['rape_revenge'][key]
        return [summon.event(84,dict(request_id=req['request_id']))]
    if mid==1029:
        flag=req['flag']
        a.require(flag in (1,2,3,4),'渡劫请求无效')
        if flag==4:
            # Explicit Continue, not an ordinary query/reconnect. A second click
            # cannot spend again once the first request has created a new board.
            a.require(all(b['reward_claimed'] for b in s['rape_boards']),'请先击败本盘全部守卫')
            flag=2 if s['rape_refreshes']<role['rape_flush_limit'] else 3
        if flag!=1:
            if flag==2:
                a.require(s['rape_refreshes']<role['rape_flush_limit'],'免费刷新次数已用完')
                s['rape_refreshes']+=1
            else:a.spend(role,'gold_coin',r['rape_refresh_gold'])
            s['rape_boards']=None
            s['rape_total_refreshes']=s.get('rape_total_refreshes',0)+1
        return [messages(role),summon.event(40,board(role,now,r,flag))]
    if mid==1041:
        idx=req['form_index'];a.require(1<=idx<=3,'阵位无效');rows=s['rape_boards'][idx-1]['form_list'].get(str(req['object_type']),{})
        key=str(int(req['object_id']));old=rows.get(key);a.require(old is not None and not old['has_win'],'不可刷新该对手')
        used=[t['npc_id'] for b in s['rape_boards'] for group in b['form_list'].values() for t in group.values()]
        new=opponent(role,list(rows).index(key),[old['npc_id']],used);a.spend(role,'gold_coin',r['rape_single_refresh_gold'])
        new.update(index=old['index'],rand=old['rand'])
        ident=next_id(s)
        # Preserve visual slot ordering across refreshes and subsequent sweeps.
        replaced={str(ident) if k==key else k:new if k==key else v for k,v in rows.items()}
        rows.clear();rows.update(replaced)
        npcs.remember(role,[new['npc_id']],rules())
        return [summon.event(40,dict(update_type=5,form_index=idx,old_type=req['object_type'],old_id=req['object_id'],new_type=req['object_type'],new_id=ident,new_show_type=new['show_type'],new_top_order=0,new_level=new['level'],new_name=new['name'],cortege_layer=new['cortege_layer']))]
    a.require(mid==1072 and (role['level']>=25 or role.get('vip_level',0)>=5),'渡劫扫荡需25级或VIP5')
    pending=[(i,t,int(k),j) for i,b in enumerate(s['rape_boards'],1) for t,rows in b['form_list'].items() for j,(k,v) in enumerate(rows.items(),1) if not v['has_win']][:role['energy']]
    a.require(bool(pending),'没有可扫荡的对手或精力不足');a.spend(role,'gold_coin',0 if role.get('vip_level',0)>=5 else len(pending));results={}
    from .protocol import decode
    for idx,t,ident,j in pending:
        for packet in battle(role,dict(fight_type=3,des_value=idx,des_type=int(t),des_id=ident),now,r,jrules):
            m,_,d=decode(packet)
            if m==2998 and d['id']==41:
                v=parse(d['data']);v['index']=j;results[len(results)+1]=v
    results['pass_all_form']=all(b['reward_claimed'] for b in s['rape_boards'])
    return [messages(role),summon.event(114,results)]
