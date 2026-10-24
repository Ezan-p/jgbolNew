"""通天塔：原客户端 1353/event203 协议 [A]，缺失地图生成与平衡 [B]。"""
import copy
import secrets
from . import activity as a, journey, formation, summon
from .protocol import encode
FLOORS=summon.rows('babel_tower_floor_prize.csv')


def response(op,data):return summon.event(203,dict(id=op,data=data))


def generate(s):
    # [B] Connected 5x8 layout. Each floor's claimed contents persist on revisits.
    key=str(s['cur_floor'])
    if key not in s['floors']:
        grid=[[dict(elem_type=0,visible=False) for _ in range(8)] for _ in range(5)]
        for row,col,typ in ((1,2,20005),(1,3,20012),(1,4,20009),(1,5,20006),
                (2,2,20003),(2,3,20011),(2,4,20008),(2,5,20004),
                (3,2,20010),(3,3,20007),(3,4,20015),(4,2,20014),(4,3,20013),(4,7,9),(5,8,3)):
            grid[row-1][col-1]['elem_type']=typ
        s['floors'][key]=grid
    s['locale']=dict(row=1,column=1)
    reveal(s)


def reveal(s):
    p=s['locale'];grid=s['floors'][str(s['cur_floor'])]
    for row in range(max(1,p['row']-1),min(5,p['row']+1)+1):
        for col in range(max(1,p['column']-1),min(8,p['column']+1)+1):grid[row-1][col-1]['visible']=True


def state(role,now,r):
    s=role['activity'].setdefault('babel',dict(cur_floor=1,history_floor=1,max_floor=60,life=100,max_life=100,
        energy=100,max_energy=100,coin_count=0,floors={},purchases={},refresh_times=1,day=-1))
    if s['day']!=a.day(now,r):
        s.update(day=a.day(now,r),energy=s['max_energy'],refresh_times=1,purchases={})
    if str(s['cur_floor']) not in s['floors']:generate(s)
    if not s.get('coin_inventory'):
        existing=sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==20000)
        if s['coin_count']>existing:a.prizes(role,[[5,20000,s['coin_count']-existing,1]])
        s['coin_inventory']=True
    s['coin_count']=sum(i['count'] for i in role['attachments'] if i['attach_type']==5 and i['type_id']==20000)
    return s


def coins(role,s,n):
    if n>0:a.prizes(role,[[5,20000,n,1]])
    else:a.consume(role,20000,-n)
    s['coin_count']+=n


def info(s):
    return dict(**{k:s[k] for k in ('cur_floor','history_floor','max_floor','life','max_life','energy','max_energy','locale')},
        dungeon=copy.deepcopy(s['floors'][str(s['cur_floor'])]))


def shop(s):
    goods=[dict(reward=[a.prize_spec([5,tid,n,1])],need_coin=cost,limit=limit) for tid,n,cost,limit in
           ((1001,10,100,10),(20016,1,50,5),(20006,1,50,5),(1023,1,100,5),(1343,1,150,5),(1034,1,100,5))]
    for i,row in enumerate(goods,1):row['limit']-=s['purchases'].get(str(i),0)
    return dict(coin_count=s['coin_count'],refresh_times=s['refresh_times'],my_shop=goods,
                my_exchange=[s['purchases'].get(str(i),0) for i in range(1,len(goods)+1)])


def settle(role,req,now,r,jrules,parse):
    a.require(role['level']>=36,'通天塔需36级')
    op=req['id'];data=parse(req['data']) if req['data'] else {};a.require(isinstance(data,dict),'通天塔参数无效')
    s=state(role,now,r)
    if op==1:return [response(1,info(s))]
    if op==3:
        mine=dict(name=role['role_name'],history_floor=s['history_floor'],reward_count=0,layer=s['history_floor'],order=1)
        return [response(3,dict(all_top=[mine],last_top=[],my_top=mine))]
    if op in (8,9,4):
        if op==9:
            a.require(s['refresh_times']>0 and s['coin_count']>=200,'通天币不足或刷新次数已用完')
            coins(role,s,-200);s['refresh_times']-=1;s['purchases']={}
        if op==4:
            idx,n=data.get('index'),data.get('count',1)
            a.require(type(idx)is int and 1<=idx<=6 and type(n)is int and 1<=n<=100,'兑换数量无效')
            goods=shop(s)['my_shop'][idx-1];count=s['purchases'].get(str(idx),0)
            a.require(n<=goods['limit'] and s['coin_count']>=goods['need_coin']*n,'兑换次数或通天币不足')
            coins(role,s,-goods['need_coin']*n);s['purchases'][str(idx)]=count+n
            p=goods['reward'][0];a.prizes(role,[[p['object_type'],p['attach_type'],p['attach_count']*n,p['attach_level']]])
        return ([response(4,{})] if op==4 else [])+[response(8,shop(s))]
    if op==11:
        a.require(s['life']<s['max_life'],'生命已满');a.spend(role,'gold_coin',200);s['life']=s['max_life']
        return [response(11,dict(life=s['life']))]
    if op==10:
        tid,n=data.get('item_type'),data.get('count',1)
        a.require(tid in (20016,20017,20018,20019) and type(n)is int and 1<=n<=100,'恢复道具无效')
        a.require(s['energy']<s['max_energy'],'行动力已满');a.consume(role,tid,n)
        s['energy']=min(s['max_energy'],s['energy']+r['babel_energy_items'][str(tid)]*n)
        return [response(10,dict(energy=s['energy']))]
    if op in (6,7):
        dest=1 if op==6 else data.get('floor')
        a.require(type(dest)is int and 1<=dest<=s['history_floor'],'尚未到达该层')
        if op==7:a.spend(role,'gold_coin',20)
        s['cur_floor']=dest;generate(s)
        return [response(1,info(s))]
    a.require(op==2,'通天塔操作无效')
    target=data.get('target_pos');a.require(isinstance(target,dict),'移动目标无效')
    row,col=target.get('row'),target.get('column');p=s['locale']
    a.require(type(row)is int and type(col)is int and 1<=row<=5 and 1<=col<=8,'坐标无效')
    a.require(abs(row-p['row'])+abs(col-p['column'])==1,'只能移动到相邻格')
    a.require(s['life']>0 and s['energy']>0,'生命或行动力不足')
    grid=s['floors'][str(s['cur_floor'])];cell=grid[row-1][col-1];typ=cell['elem_type'];events=[];reward=[];fighting=False
    a.require(typ!=1,'不可进入边界')
    tools={20003:20005,20004:20006,20007:20010,20008:20011,20009:20012}
    if typ in tools:a.consume(role,tools[typ],1)
    guards=(7,8,9,20010,20011,20012,20013,20014,20015)
    if typ in guards:
        a.require(any(c.get('order') for c in role['corteges']),'请先上阵神仙')
        result,lineup,actions=journey.battle(role,dict(cortege_list=f"{r['battle_npc']}|{max(1,s['cur_floor']*2)}"),jrules)
        role['activity']['fight_id']+=1;fid=role['activity']['fight_id'];fighting=True
        events=[encode(1028,dict(fight_id=fid,first_hand=1,des_name='通天塔守卫',lineup_count=len(lineup),lineup=lineup)),
                encode(1027,dict(fight_id=fid,fight_type=200,final_result=result,fight_round=len(actions),fight_result=actions))]
        lost=sum(sum(x['damage_list']) for x in actions if not x['is_src'])
        maximum=sum(x.get('src_max_hp',0) for x in lineup)
        s['life']=max(0,s['life']-max(1,100*lost//max(1,maximum)))
        if not 1<=result<=3:
            s['energy']-=1
            return events+[response(2,dict(locale=p,life=s['life'],energy=s['energy'],update=grid,fight_flag=True)),summon.event(44,dict(fight_id=fid,fight_type=200))]
    if typ in (5,20007,20008,20009) or typ in guards:
        pool=next(x for x in FLOORS if int(x['floor_l'])<=s['cur_floor']<=int(x['floor_r']))
        specs=[list(map(int,x.split('|')))+[1] for x in pool['daoju'].split('/')]
        reward=a.prizes(role,[secrets.choice(specs)]);coins(role,s,r['babel_cell_coins'])
        if typ in (20010,20011,20012):reward+=a.prizes(role,[[5,typ,1,1]])
    if typ in (20005,20006):reward=a.prizes(role,[[5,typ,1,1]])
    s['energy']-=1;s['locale']=dict(row=row,column=col)
    if typ not in (0,3):cell['elem_type']=0
    reveal(s)
    data=dict(locale=s['locale'],life=s['life'],energy=s['energy'],update=copy.deepcopy(grid),fight_flag=fighting)
    if reward:data['rewards']=reward
    events.append(response(2,data))
    if typ==3:
        a.require(s['cur_floor']<s['max_floor'],'已到达顶层')
        s['cur_floor']+=1;s['history_floor']=max(s['history_floor'],s['cur_floor']);generate(s)
        events.append(response(1,info(s)))
    if fighting:events.append(summon.event(44,dict(fight_id=fid,fight_type=200)))
    return events
