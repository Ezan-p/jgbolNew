"""九幽宝图：原版操作协议 [A]，持久化奖盘及缺失价格/奖池 [B]。"""
import copy
import secrets
from . import activity as a


def pool(tid,r):
    scale=tid-1430
    return [a.prize_spec([p[0],p[1],p[2]*scale,p[3]]) for p in r['abyss_map_rewards']]


def view(tid,board,r,op):
    return dict(op_type=op,type_id=tid,shop_list=copy.deepcopy(board['goods']),free_times=0 if board['draws'] else 1,
        pay_times=max(0,board['draws']-1),max_pay_times=r['abyss_map_paid_draws'],had_hunt=bool(board['draws']),
        pay_gold_count=r['abyss_map_gold'],remove_count=r['abyss_map_remove_count'],mark_flag=board['quick'])


def grant(role,goods):
    return a.prizes(role,[[p['object_type'],p['attach_type'],p['attach_count'],p['attach_level']] for p in goods])


def settle(role,s,op,d,now,r):
    from .activity_abyss import response
    maps=s.setdefault('maps',{});marks=s.setdefault('map_quick',{})
    tid=d.get('map_type') if op==24 else d.get('type_id')
    a.require(type(tid)is int and 1431<=tid<=1440,'九幽宝图类型无效')
    key=str(tid);board=maps.get(key)
    if op==24:
        n,draws=d.get('treasure_count'),d.get('open_count')
        a.require(type(n)is int and 1<=n<=99 and type(draws)is int and 1<=draws<=1+r['abyss_map_paid_draws'],'批量寻宝次数无效')
        a.require(not board or not board['draws'] or board['draws']>r['abyss_map_paid_draws'],'请先完成当前宝图')
        a.consume(role,tid,n);a.spend(role,'gold_coin',n*(draws-1)*r['abyss_map_gold']);gains=[]
        for _ in range(n):
            available=pool(tid,r)
            for _ in range(draws):
                index=secrets.randbelow(len(available));gains+=grant(role,[available.pop(index)])
        maps.pop(key,None)
        return [response(24,map_type=tid,prize_list=gains)]
    operation=d.get('op_type');a.require(type(operation)is int and operation in (1,2,3,5,6),'宝图操作无效')
    if operation==1:
        if not board or board['draws']>r['abyss_map_paid_draws']:
            a.require(any(i['attach_type']==5 and i['type_id']==tid and i['count']>0 for i in role['attachments']),'九幽宝图不足')
            board=dict(draws=0,goods=pool(tid,r),quick=marks.get(key,False));maps[key]=board
        return [response(3,event_data=view(tid,board,r,1))]
    a.require(board is not None,'请先打开宝图')
    if operation in (5,6):
        a.require(operation==6 or role.get('month_card_time',0)>now,'快速寻宝需要有效月卡')
        board['quick']=operation==5;marks[key]=board['quick']
        return [response(3,event_data=view(tid,board,r,operation))]
    if operation==3:
        maps.pop(key)
        return [response(3,event_data=dict(op_type=3,type_id=tid))]
    a.require(board['draws']<=r['abyss_map_paid_draws'],'该宝图寻宝次数已用完')
    removed=d.get('index_list',[])
    if isinstance(removed,dict):
        a.require(set(removed)==set(range(1,len(removed)+1)),'移除选项无效');removed=list(removed.values())
    a.require(isinstance(removed,list) and len(removed)<=r['abyss_map_remove_count'] and all(type(i)is int and 1<=i<=len(board['goods']) for i in removed) and len(set(removed))==len(removed),'移除选项无效')
    a.require(not removed or board['draws']==0,'开始寻宝后不能更换移除项')
    if board['draws']==0:
        a.consume(role,tid,1)
        for index in removed:board['goods'][index-1]['rm']=True
    else:a.spend(role,'gold_coin',r['abyss_map_gold'])
    available=[i for i,p in enumerate(board['goods']) if not p.get('rm') and not p.get('got')]
    a.require(available,'宝图奖励已用完');index=secrets.choice(available);board['goods'][index]['got']=True;board['draws']+=1
    gain=grant(role,[board['goods'][index]])
    return [response(3,event_data=dict(view(tid,board,r,2),des_index=index+1,prize_list=gain))]
