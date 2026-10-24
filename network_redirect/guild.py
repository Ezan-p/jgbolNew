"""Original 1301 / event 82 guild contract [A]; local settlement policy [B]."""
import copy
import json
from pathlib import Path
from . import formation, summon, daily, journey
from .protocol import encode
ROOT = Path(__file__).resolve().parents[1]
require = formation.require
HANDLED = {1301}
FIGHTS = {13,14,16,17,19}
OP_LABELS = {1:'创建仙盟',2:'加入仙盟',4:'加入仙盟',5:'批准申请',6:'拒绝申请',11:'任命职位',12:'禅让盟主',19:'修改公告',20:'禁言成员',21:'解除禁言',22:'清空禁言',24:'清空申请',25:'移除成员',51:'更改盟名',71:'修改内部公告'}
MANAGEMENT = {1,2,3,4,5,6,10,11,12,13,19,20,21,22,23,24,25,51,71}


def load_rules(path=ROOT/'server_config/guild_rules.json'):
    r=json.loads(Path(path).read_text())
    require(r.get('schema_version')==1 and r.get('mode')=='inferred','仙盟配置来源无效')
    for k in ('join_level','create_level','create_cost_gold','change_name_cost','member_limit','max_level','level_popularity','initial_money','seed_cost_money','tree_grow_seconds','tree_exp_per_level','cultivate_limit','cultivate_gold','cultivate_gold_rate','cultivate_silver','cultivate_contrib','cultivate_exp','cultivate_pop','donate_limit','donate_money_rate','donate_contrib_rate','store_flush_gold','store_flush_limit','battle_npc','battle_level','battle_daily','tree_boss_hp','tree_fight_cooldown','tree_flush_gold','feast_seconds','feast_gift_limit','feast_grab_limit','team_size','team_daily','search_daily','catch_daily','catch_gold','hunt_daily','wander_daily','hunt_silver','hunt_gold','escort_daily','escort_rob_daily','escort_flush_limit','escort_free_flush','escort_flush_gold','search_card_points'):
        require(type(r.get(k)) is int and 0<r[k]<=1000000,'仙盟配置数值无效: '+k)
    require(r['max_level']<=99 and r['member_limit']<=100,'仙盟等级/人数配置越界')
    require(type(r.get('timezone_offset_hours')) is int and -12<=r['timezone_offset_hours']<=14,'仙盟时区无效')
    require(len(r['store'])==6 and len({x['id'] for x in r['store']})==6,'仙盟商店需要六个唯一货位')
    for row in r['store']:
        daily.validate_prize(row['prize'])
        require(all(type(row[k]) is int and 0<row[k]<=100000 for k in ('id','cost','limit')),'商店配置无效')
    for key in ('tree_rewards','match_rewards','team_rewards','train_rewards','hunt_rewards','escort_compose_rewards'):
        require(isinstance(r.get(key),list) and r[key], '仙盟奖励配置缺失: '+key)
        for prize in r[key]:daily.validate_prize(prize)
    require(len(r['feast_gifts'])==2 and {v['type'] for v in r['feast_gifts']}=={1,2},'宴会礼物配置无效')
    for v in r['feast_gifts']:
        daily.validate_prize([5,v['item'],1,1])
        require(all(type(v[k]) is int and v[k]>0 for k in ('gold','contrib')),'宴会礼物消耗无效')
    return r


def client_config(r):
    rights={1:list(range(1,29)),7:[1,2,3,4,5,8,9,10,11,12,13,14,15,16,17,18,19,24,25,26,27,28]}
    for rank in (2,3,4,5,6):rights[rank]=[3,4,5,14,15,19,25,28]
    return dict(const_config=dict(create_level=r['create_level'],join_level=r['join_level'],apply_level=r['join_level'],
        create_cost_gold=r['create_cost_gold'],change_name_cost=r['change_name_cost'],union_top_level=r['max_level'],
        open_search_gold=True,open_union_match=True,open_world_match=True,open_feast=True,open_west=True,
        west_min_role_level=r['join_level'],open_feast_level=1),
        right_config={k:dict(right_list={n:True for n in v}) for k,v in rights.items()},
        level_config={i:dict(popularity_limit=i*r['level_popularity'],max_count=r['member_limit']) for i in range(1,r['max_level']+1)},west_config={})


def new_union(ident,name,r):
    return dict(id=ident,name=name,level=1,popularity=0,money=r['initial_money'],notify='欢迎加入仙盟',notify_ex='',
                members={},applications={},forbidden=[],chat=[],events=[],tree=dict(state=1,seed=1,level=1,exp=0,planted=0,records=[],ranks=[]))


def prepare(role,now,r):
    s=role.setdefault('guild',dict(unions={},next_id=2,applications=[],day=-1))
    if not s['unions']:
        g=new_union(1,'本地仙盟',r)
        g['members']['10001']=dict(id=10001,name='本地盟主',rank=1,level=30,contrib=0,head_type=1,totalcontrib=0,jointime=now,lastlogin=now,online=False,toporder=0,logout_time=0,combat_power=1000)
        s['unions']['1']=g
    for k in ('union_id','union_rank','union_contrib','cur_union_contrib','union_store_flush_time'):role.setdefault(k,0)
    role.setdefault('union_name','')
    day=daily.day(now,r)
    if s['day']!=day:s.update(day=day,cultivations=0,donations=0,purchases={},flushes=0,create_count=0)
    if now>=s.get('feast_buff_end',0):
        role.update(train_tree_rate=0,contrib_plus_rate=0);s['feast_fam_rate']=0
    g=s['unions'].get(str(int(role['union_id'])))
    if g:
        m=g['members'].get(str(int(role['role_id'])))
        if m:
            m.update(name=role['role_name'],level=role['level'],head_type=role.get('head_type',1),online=True,contrib=role['cur_union_contrib'],totalcontrib=role['union_contrib'])
            role.update(union_rank=m['rank'],union_name=g['name'])
        t=g['tree']
        if t['state']==2 and now>=t['planted']+r['tree_grow_seconds']:t['state']=3
        g['level']=min(r['max_level'],1+g['popularity']//r['level_popularity'])
    return s,g


def positive(data,key,maximum=1000000):
    n=data.get(key); require(type(n) is int and 0<n<=maximum,'仙盟参数无效: '+key); return n


def pay(role,key,n):
    require(role.get(key,0)>=n,'元宝不足' if key=='gold_coin' else '银两或贡献不足');role[key]-=n


def contribution(role,n):
    n*=max(1,role.get('contrib_plus_rate',0))
    role['union_contrib']+=n;role['cur_union_contrib']+=n
    return n


def reply(op,data):return encode(1301,dict(id=op,data=summon.lua(data)))
def notice(op,**data):return summon.event(82,dict(event_id=op,result=1,**data))


def info(g,r):
    return dict(id=g['id'],name=g['name'],level=g['level'],popularity=g['popularity'],order=g['id'],
                cur_count=len(g['members']),max_count=r['member_limit'],notify=g['notify'],notify_ex=g['notify_ex'],leader_name=next((m['name'] for m in g['members'].values() if m['rank']==1),''))


def member(role,g):
    m=copy.deepcopy(g['members'][str(int(role['role_id']))]);m.update(union_contrib=role['union_contrib'],cur_union_contrib=role['cur_union_contrib'],contribute=role['union_contrib'])
    m.update(tree_state=g['tree']['state'],can_plant_tree=role['union_rank']==1,can_cultivate_tree=True,can_kill_tree=True,cultivate_time=10,union_protect_card=3,max_protect_card=3,can_search_gold=True,can_match_fight=True,has_action_point=True,is_match_time=True,is_bet_time=False,has_bet=False,cross_fight_flag=False,can_rece_award=False,west_config=dict(max_publish_book=3,stop_book_count=3,next_stop_book_cd=60,flush_stop_cd_gold=10,grade_book_max_count=5,book_worth_config={i:dict(contribute=i*10,crash_card=i,union_money=i*100) for i in range(1,6)}))
    escort=role['guild'].get('escort',{})
    m['union_protect_card']=escort.get('cards',3)
    return m


def authorize(role,r,right):
    require(client_config(r)['right_config'].get(role['union_rank'],{}).get('right_list',{}).get(right,False),'仙盟权限不足')


def tree_data(role,s,g,now,r):
    t=g['tree']
    return dict(tree_state=t['state'],tree_seed_count=t['seed'],union_money=g['money'],require_pop=0,
        init_seed_count=1,seed_cost_money=r['seed_cost_money'],tree_level=t['level'],tree_exp=t['exp'],full_exp=r['tree_exp_per_level'],
        tree_protect_time=t['planted']+r['tree_grow_seconds'],cultivate_time=max(0,r['cultivate_limit']-s['cultivations']),
        cultivate_cost=r['cultivate_gold'],gold_cultivate_rate=r['cultivate_gold_rate'],cultivate_info_list=t['records'],
        cultivate_record_time=s['day'],cultivate_record_count=s['cultivations'],tree_boss_info=dict(boss_hp=t.get('hp',r['tree_boss_hp']),boss_full_hp=r['tree_boss_hp']),
        rank_list=t['ranks'],cooltime=t.get('cooltime',0),flush_protect_cost=r['tree_flush_gold'],max_donate_count=r['donate_limit'],donate_count=s['donations'])


def missions(r):
    # [A] tree_mission_cost_type.silver_coins = 4 (not object_type.silver = 12).
    return [dict(id=1,mission_type=1,cost_type=4,item_count=r['cultivate_silver'],contrib=r['cultivate_contrib'],exp=r['cultivate_exp'],pop=r['cultivate_pop'])]


def store_data(s,r):
    return dict(flush_flag=True,flush_cost=r['store_flush_gold'],item_list=[dict(id=x['id'],item=daily.spec(x['prize']),cost_contrib=x['cost'],buy_times=max(0,x['limit']-s['purchases'].get(str(x['id']),0))) for x in r['store']])


def settle(role,req,now,r,parse,daily_rules):
    op=req['id']; d=parse(req['data']); require(isinstance(d,dict),'仙盟请求格式错误')
    s,g=prepare(role,now,r); rid=str(int(role['role_id']))
    if op==18 and d.get('query_type')==4:
        page=positive(d,'page',10000)
        rows=[info(v,r) for v in s['unions'].values()]
        return [reply(op,dict(query_type=4,page=page,union_list=rows[(page-1)*10:page*10]))]
    if op in (1,2,4):
        require(not role['union_id'],'已经加入仙盟');require(role['level']>=r['create_level' if op==1 else 'join_level'],'等级不足')
        if op==1:
            name=d.get('union_name','');require(isinstance(name,str),'仙盟名称格式无效');name=name.strip();require(2<=len(name)<=10 and len(name.encode())<32 and not any(c in name for c in '\x00\n\r'),'仙盟名称应为2至10字')
            require(all(v['name']!=name for v in s['unions'].values()),'仙盟名称已被使用')
            require(s['create_count']<1,'今日创建次数已用完');pay(role,'gold_coin',r['create_cost_gold'])
            ident=s['next_id'];s['next_id']+=1;s['create_count']+=1
            g=new_union(ident,name,r);s['unions'][str(ident)]=g;rank=1
        else:
            ident=positive(d,'union_id');g=s['unions'].get(str(ident));require(g is not None,'仙盟不存在')
            require(len(g['members'])<r['member_limit'],'仙盟成员已满');rank=5
            # [B] Offline public guild accepts applications immediately.
        g['members'][rid]=dict(id=role['role_id'],name=role['role_name'],rank=rank,level=role['level'],contrib=0,head_type=role.get('head_type',1),totalcontrib=0,jointime=now,lastlogin=now,online=True,toporder=0,logout_time=0,combat_power=role.get('role_combat_power',0))
        role.update(union_id=g['id'],union_rank=rank,union_name=g['name'],union_contrib=0,cur_union_contrib=0)
        return [notice(1 if op==1 else 8),reply(18,dict(query_type=1,union_info=info(g,r),role_info=member(role,g)))]
    require(g is not None and rid in g['members'],'请先加入仙盟')
    if op==18:
        q=d.get('query_type');out=dict(query_type=q,result=1)
        if q==1:out.update(union_info=info(g,r),role_info=member(role,g))
        elif q==2:out.update(flag=d.get('flag',1),member_list=list(g['members'].values()),apply_count=len(g['applications']),req_protect_list={})
        elif q in (3,5,6,7):
            key={3:'forbid_list',5:'apply_list',6:'event_list',7:'chat_list'}[q]
            out[key]=list(g['applications'].values()) if q==5 else g[{3:'forbidden',6:'events',7:'chat'}[q]]
        else:
            from . import guild_activities
            return guild_activities.query(role,s,g,d,now,r)
        return [reply(op,out)]
    if op in (3,13):
        if op==13: require(role['union_rank']==1,'只有盟主可以解散仙盟');require(len(g['members'])==1,'请先移除其他成员')
        else:require(role['union_rank']!=1 or len(g['members'])==1,'盟主请先转让职位')
        del g['members'][rid]
        if not g['members']:del s['unions'][str(g['id'])]
        # Keep account daily quotas across leave/rejoin; only clear membership links.
        if 'instances' in s:s['instances']['team']=None
        if 'escort' in s:s['escort']['active']=None;s['escort']['requests']=[];s['escort']['issued']={}
        if 'match' in s:s['match']['signed']=False
        s['feast_buff_end']=0
        role.update(union_id=0,union_rank=0,union_name='',union_contrib=0,cur_union_contrib=0)
        return [notice(3)]
    if op in (19,71,51):
        authorize(role,r,20 if op==51 else 16)
        key={19:'notify',71:'notify_ex',51:'new_name'}[op];value=d.get(key if op==51 else 'new_notify','')
        require(isinstance(value,str) and not any(c in value for c in '\x00\n\r') and 0<len(value)<= (10 if op==51 else 100),'公告或名称长度无效')
        if op==51:
            require(len(value.encode())<32 and len(value)>=2 and all(v['id']==g['id'] or v['name']!=value for v in s['unions'].values()),'名称无效或重复')
            pay(role,'gold_coin',r['change_name_cost']);g['name']=value;role['union_name']=value
        else:g[key]=value
        return [notice(op,name=value)]
    if op in (5,6,24):
        authorize(role,r,1)
        if op==24:g['applications']={}
        else:
            target=str(positive(d,'role_id'));m=g['applications'].get(target);require(m is not None,'申请不存在')
            if op==5:require(len(g['members'])<r['member_limit'],'成员已满');g['members'][target]=dict(m,rank=5)
            del g['applications'][target]
        return [notice(op)]
    if op in (11,12,20,21,22,25):
        if op==22:authorize(role,r,17);g['forbidden']=[];return [notice(op)]
        target=str(positive(d,'role_id'));m=g['members'].get(target);require(m is not None and target!=rid,'目标成员无效')
        require(m['rank']!=1,'不能操作盟主')
        if op in (11,12):
            require(role['union_rank']==1,'只有盟主可以任命');rank=1 if op==12 else positive(d,'new_rank',7)
            require(rank in range(1,8),'职位无效');m['rank']=rank
            if rank==1:g['members'][rid]['rank']=5;role['union_rank']=5
        elif op==25:authorize(role,r,2);del g['members'][target]
        else:
            authorize(role,r,17)
            g['forbidden']=[v for v in g['forbidden'] if v['id']!=m['id']]
            if op==20:g['forbidden'].append(dict(m))
        return [notice(op,role_id=m['id'])]
    if op==23:return chat(role,d.get('chat_msg',d.get('content','')),now,r)
    if op in (34,35,14,15,36,37,70):
        t=g['tree']
        if op==35:return [reply(op,missions(r))]
        if op==70:return [reply(op,dict(rank_list=t['ranks']))]
        if op in (14,37):
            authorize(role,r,13);require(t['state']==1,'神树已种植')
            if op==37:require(t['seed']==0,'已有树种');require(g['money']>=r['seed_cost_money'],'仙盟资金不足');g['money']-=r['seed_cost_money'];t['seed']+=1
            else:require(t['seed']>0,'没有树种');t.update(state=2,seed=t['seed']-1,planted=now,exp=0,records=[],ranks=[])
        if op==36:
            count=positive(d,'count',r['donate_limit']);require(s['donations']+count<=r['donate_limit'],'今日捐献额度不足')
            pay(role,'gold_coin',count);s['donations']+=count;g['money']+=count*r['donate_money_rate'];contribution(role,count*r['donate_contrib_rate'])
        if op==15:
            authorize(role,r,14);require(t['state']==2,'当前不能培育');require(s['cultivations']<r['cultivate_limit'],'今日培育次数已用完')
            require(d.get('cultivate_record_count')==s['cultivations'] and d.get('cultivate_record_time')==s['day'],'培育任务已过期，请刷新')
            require(d.get('mission_id')==1 and d.get('mission_type')==1 and d.get('cultivate_type') in (1,2),'培育任务无效')
            pay(role,'silver_coin',r['cultivate_silver']);rate=1
            if d['cultivate_type']==2:pay(role,'gold_coin',r['cultivate_gold']);rate=r['cultivate_gold_rate']
            n=contribution(role,r['cultivate_contrib']*rate);s['cultivations']+=1
            rate*=max(1,role.get('train_tree_rate',0))
            t['exp']+=r['cultivate_exp']*rate;t['level']=min(99,t['level']+t['exp']//r['tree_exp_per_level']);t['exp']%=r['tree_exp_per_level']
            g['popularity']+=r['cultivate_pop']*rate
            t['records'].append(dict(name=role['role_name'],id=role['role_id'],cultivate_type=d['cultivate_type'],contrib=n,pop=r['cultivate_pop']*rate,exp=r['cultivate_exp']*rate))
            t['records']=t['records'][-30:];daily.record(role,9,1,now,daily_rules)
            return [reply(op,dict(union_contrib=n)),reply(34,tree_data(role,s,g,now,r))]
        data=tree_data(role,s,g,now,r)
        return [reply(op,data)]
    if op in (38,39,40):
        if op==39:
            require(s['flushes']<r['store_flush_limit'],'今日刷新次数已用完');pay(role,'gold_coin',r['store_flush_gold']);s['flushes']+=1;s['purchases']={};role['union_store_flush_time']=now
        if op==40:
            ident=positive(d,'item_id');count=positive(d,'buy_count',100)
            row=next((x for x in r['store'] if x['id']==ident),None);require(row is not None,'商品不存在')
            require(s['purchases'].get(str(ident),0)+count<=row['limit'],'商品购买次数不足');pay(role,'cur_union_contrib',row['cost']*count)
            prize=list(row['prize']);prize[2]*=count;journey.grant(role,prize);s['purchases'][str(ident)]=s['purchases'].get(str(ident),0)+count
            return [reply(op,dict(item_info=next(x for x in store_data(s,r)['item_list'] if x['id']==ident)))]
        return [reply(op,store_data(s,r))]
    from . import guild_activities
    return guild_activities.settle(role,s,g,op,d,now,r)


def chat(role,msg,now,r):
    s,g=prepare(role,now,r)
    require(g is not None,'请先加入仙盟')
    require(not any(v['id']==role['role_id'] for v in g['forbidden']),'已被禁言')
    require(isinstance(msg,str) and 0<len(msg.strip())<=100 and '\x00' not in msg,'聊天内容无效')
    row=dict(id=role['role_id'],name=role['role_name'],time=now,chat_msg=msg,channel=6,sub_channel=6,vip_level=role.get('vip_level',0),single_score=0,level=role['level'],head_type=role.get('head_type',1),union_name=g['name'])
    g['chat'].append(row);g['chat']=g['chat'][-30:]
    return [encode(1098,row)]
