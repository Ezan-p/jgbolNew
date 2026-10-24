"""历劫 [A] client tables, 1349 and nine-position replay; [B] local settlement."""
import copy
from . import activity as a, formation, journey, summon
from .protocol import encode
GATES={int(x['id']):x for x in summon.rows('undergo_ordeal/tollgate_config.csv')}
MAPS={int(x['id']):x for x in summon.rows('undergo_ordeal/map_config.csv')}
NPCS={int(x['编号']):x for x in summon.rows('undergo_ordeal/npc_list.csv')}


def response(op,data):return encode(1349,dict(id=op,data=summon.lua(data)))


def state(role,now,r):
    s=role['activity'].setdefault('undergo',dict(gate=101,challenge=101,lineup={},passed=[],day=-1))
    if s['day']!=a.day(now,r):
        s.update(day=a.day(now,r),count=0,challenge=101,used={},claims=[],purchases={})
    if not s['lineup']:s['lineup']={str(c['order']):c['id'] for c in role['corteges'] if c.get('order')}
    return s


def day_prize(s):
    return {mid:dict(has_get=mid in s['claims']) for mid in MAPS
            if all(gid in s['passed'] for gid,c in GATES.items() if int(c['map_id'])==mid)}


def detail(s):
    return dict(detail=dict(map_list=dict(undergo=dict(big_id=s['gate']//100,small_id=s['gate']%100,total_count=s['count']),
        challenge=dict(big_id=s['challenge']//100,small_id=s['challenge']%100,cortege_list={int(k):v for k,v in s['used'].items()})),
        cortege_list={int(k):v for k,v in s['lineup'].items()},day_prize=day_prize(s)))


def shop(s,r):
    return [dict(a.prize_spec(row['reward']),crystals=row['cost'],buy_times=row['limit']-s['purchases'].get(str(i),0))
            for i,row in enumerate(r['undergo_shop'],1)]


def next_gate(gid):
    nxt=int(GATES[gid]['next_tollgate'])
    if nxt:return nxt
    mid=int(GATES[gid]['map_id']);nxt=int(MAPS[mid]['next_map'])
    return int(MAPS[nxt]['first_tollgate']) if nxt in MAPS else gid


def settle(role,req,now,r,jrules,frules,parse):
    a.require(role['level']>=12,'历劫需12级')
    data=parse(req['data']) if req['data'] else {};a.require(isinstance(data,dict),'历劫参数无效')
    op=req['id'];s=state(role,now,r)
    if op in (1,6):return [response(op,detail(s))]
    if op==2:return [response(2,{})]
    if op==3:return [response(3,shop(s,r))]
    if op==5:
        idx,n=data.get('index'),data.get('count',1)
        a.require(type(idx)is int and 1<=idx<=len(r['undergo_shop']) and type(n)is int and n>0,'兑换参数无效')
        row=r['undergo_shop'][idx-1];used=s['purchases'].get(str(idx),0)
        a.require(used+n<=row['limit'],'今日兑换次数不足')
        a.consume(role,1366,row['cost']*n);s['purchases'][str(idx)]=used+n
        p=row['reward'];gain=a.prizes(role,[[p[0],p[1],p[2]*n,p[3]]]);gain[0]['buy_times']=row['limit']-used-n
        return [response(5,dict(index=idx,attach_list=gain))]
    if op==7:
        idx=data.get('index');a.require(type(idx)is int and (idx==0 or idx in MAPS),'领奖地图无效')
        ids=[i for i,p in day_prize(s).items() if not p['has_get'] and idx in (0,i)]
        a.require(ids,'尚未通关地图或今日已领取')
        gain=[]
        for i in ids:
            gain+=journey.drops(role,next(v for k,v in MAPS[i].items() if k.startswith('pass_map_prize')),True)
            s['claims'].append(i)
        return [response(7,dict(day_prize=day_prize(s),attach_list=gain))]
    a.require(op==4,'历劫操作无效')
    mode,gid,positions=data.get('mode'),data.get('map_id'),data.get('cortege_list')
    a.require(type(mode)is int and mode in (1,2) and type(gid)is int and gid in GATES,'历劫关卡无效')
    a.require(isinstance(positions,dict) and 1<=len(positions)<=9,'历劫阵容无效')
    ids=list(positions.values());a.require(len(set(ids))==len(ids),'神仙不能重复上阵')
    a.require(all(type(p)is int and 1<=p<=9 for p in positions),'历劫阵位无效')
    if mode==1:
        a.require(gid<=s['gate'] and s['count']<10,'关卡未解锁或今日历劫次数已满')
    else:
        a.require(gid==s['challenge'] and gid in s['passed'],'请先通关对应历劫关卡，并按顺序挑战')
        a.require(all(s['used'].get(str(int(cid)),0)<4 for cid in ids),'神仙今日挑战次数已满')
    cfg=GATES[gid];a.require(role['level']>=int(cfg['require_level']),'历劫等级不足')
    a.spend(role,'strength',int(cfg['strenth_consume']))
    ours=[]
    for pos,cid in positions.items():
        c=next((c for c in role['corteges'] if c['id']==cid),None);a.require(c is not None,'神仙不属于当前角色')
        unit=dict(type=c['type'],order=pos,level=c['level'],evolve=c.get('evolve_level',0),reborn=c.get('reborn_layer',0),
                  **{k:max(1,int(c[k])) for k in formation.STATS})
        unit['max_hp']=unit['hp'];unit['skills']=[(x['type_id'],x['level']) for x in role['attachments']
            if x['attach_type']==6 and c.get('order') and x.get('equip_order')==c['order'] and x.get('equip_pos')]
        ours.append(unit)
    enemies=[]
    for token in next(v for k,v in cfg.items() if k.startswith('cortege_list(')).split('/'):
        nid,pos=map(int,token.split('|'))
        if not pos:continue
        n=NPCS[nid];sk=int(n['法术ID'] or 0)
        enemies.append(dict(type=int(n['ID']),order=pos,level=int(cfg['level']),evolve=0,reborn=int(n['是否转生'] or 0),
            gongji=int(n['攻']),fangyu=int(n['防']),hp=int(n['血']),max_hp=int(n['血']),magic=int(n['法']),
            skills=[(sk,int(cfg['skill_level']))] if sk in formation.SKILLS else [],skill_probabilities={sk:int(n['法术概率'] or 0)}))
    result,lineup,actions=journey.battle(role,{},jrules,units=(ours,enemies),slots=9);win=1<=result<=3
    s['lineup']={str(p):int(cid) for p,cid in positions.items()}
    gain=[]
    if mode==1:s['count']+=1
    else:
        for cid in ids:s['used'][str(int(cid))]=s['used'].get(str(int(cid)),0)+1
    if win:
        suffix='_lijie' if mode==1 else ''
        gain+=journey.drops(role,next(v for k,v in cfg.items() if k.startswith('com_win_prize'+suffix+'(')))
        if gid not in s['passed'] and mode==1:
            gain+=journey.drops(role,cfg['first_win_prize_lijie(exp_count|rate)'])
            s['passed'].append(gid)
        key='gate' if mode==1 else 'challenge'
        if gid==s[key]:s[key]=next_gate(gid)
    # [B] Apply the common role/companion progression algorithm to the selected
    # nine-position formation, restoring the normal formation afterwards.
    original={c['id']:c.get('order',0) for c in role['corteges']}
    for c in role['corteges']:c['order']=next((p for p,cid in positions.items() if cid==c['id']),0)
    rewardcfg=dict(cfg)
    if mode==1:rewardcfg.update(exp=cfg['exp_lijie'],money=cfg['money_lijie'])
    xp,exps,money=journey.experience(role,rewardcfg,win,jrules,frules)
    for c in role['corteges']:c['order']=original[c['id']]
    role['activity']['fight_id']+=1;fid=role['activity']['fight_id'];ft=29+mode
    return [encode(1141,dict(fight_id=fid,first_hand=1,des_name='历劫守卫',lineup_count=len(lineup),lineup=lineup)),
        encode(1140,dict(fight_id=fid,fight_type=ft,final_result=result,fight_round=len(actions),fight_result=actions)),
        response(6,detail(s)),summon.event(44,dict(fight_id=fid,fight_type=ft,
            role_add_exp=xp,exp_list=exps,silver_coin=money,rewards=gain,send_prize_list=gain))]
