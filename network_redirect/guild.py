"""Original 1301 / event 82 guild contract [A]; local settlement policy [B]."""
import copy
import json
from pathlib import Path
from . import formation, summon, daily, journey, guild_offline as offline
from .protocol import encode
ROOT = Path(__file__).resolve().parents[1]
require = formation.require
HANDLED = {1301}
FIGHTS = {13,14,16,17,19}
WAR_FIGHTS = {14,16,17}
WAR_OPS = {45,46,47,48,58,62,63,72,76}
WAR_QUERIES = {8,9,10,11,12,13,16,17,18,19,100}
WAR_CLOSED = '离线模式，暂未开放'
OP_LABELS = {1:'创建仙盟',2:'加入仙盟',4:'加入仙盟',5:'批准申请',6:'拒绝申请',11:'任命职位',12:'禅让盟主',19:'修改公告',20:'禁言成员',21:'解除禁言',22:'清空禁言',24:'清空申请',25:'移除成员',51:'更改盟名',71:'修改内部公告'}
MANAGEMENT = {1,2,3,4,5,6,10,11,12,13,19,20,21,22,23,24,25,51,71}


def load_rules(path=ROOT/'server_config/guild_rules.json'):
    r=json.loads(Path(path).read_text())
    require(r.get('schema_version')==1 and r.get('mode')=='inferred','仙盟配置来源无效')
    require(type(r.get('wars_enabled')) is bool,'仙盟战争开关无效')
    for k in ('join_level','create_level','create_cost_gold','change_name_cost','member_limit','max_level','level_popularity','initial_money','seed_cost_money','tree_grow_seconds','tree_exp_per_level','cultivate_limit','cultivate_gold','cultivate_gold_rate','cultivate_silver','cultivate_contrib','cultivate_exp','cultivate_pop','donate_limit','donate_money_rate','donate_contrib_rate','store_flush_gold','store_flush_limit','battle_npc','battle_level','battle_daily','tree_boss_hp','tree_fight_cooldown','tree_flush_gold','feast_seconds','feast_gift_limit','feast_grab_limit','team_size','team_daily','search_daily','catch_daily','catch_gold','hunt_daily','wander_daily','hunt_silver','hunt_gold','escort_daily','escort_rob_daily','escort_flush_limit','escort_free_flush','escort_flush_gold','search_card_points'):
        require(type(r.get(k)) is int and (0 if k=='wander_daily' else 1)<=r[k]<=1000000,'仙盟配置数值无效: '+k)
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
    for key in ('feast_union_level','feast_npc_grab_seconds','feast_grab_fortune'):
        require(type(r.get(key)) is int and 0 < r[key] <= 100000, '群英会配置无效: '+key)
    require(set(r['feast_box_rewards']) == {'1120','1121'}, '群英会礼盒奖励缺失')
    for prizes in r['feast_box_rewards'].values():
        require(bool(prizes), '群英会礼盒奖励为空')
        for prize in prizes: daily.validate_prize(prize)
    require(bool(r['feast_fortune_rewards']), '群英会福气榜奖励缺失')
    previous=0
    for tier in r['feast_fortune_rewards']:
        require(type(tier['max_rank']) is int and previous<tier['max_rank']<=1000 and bool(tier['prizes']), '福气榜名次无效')
        previous=tier['max_rank']
        for prize in tier['prizes']:daily.validate_prize(prize)
    require(len(r['match_bet_silver']) == 3 and all(type(v) is int and v > 0 for v in r['match_bet_silver']), '盟战押注配置无效')
    require(len(r['match_power_percent']) == 6 and all(type(v) is int and 1 <= v <= 300 for v in r['match_power_percent']), '盟战战力配置无效')
    offline.validate_rules(r)
    return r


def client_config(r):
    rights={int(k):v for k,v in r['rank_rights'].items()}
    return dict(const_config=dict(create_level=r['create_level'],join_level=r['join_level'],apply_level=r['join_level'],
        create_cost_gold=r['create_cost_gold'],change_name_cost=r['change_name_cost'],union_top_level=r['max_level'],
        # These two flags control visibility; disabled wars keep both icons.
        open_search_gold=True,open_union_match=1,open_world_match=1,open_feast=1,open_west=True,
        west_min_role_level=r['join_level'],open_feast_level=r['feast_union_level']),
        right_config={k:dict(right_list={n:True for n in v}) for k,v in rights.items()},
        level_config={i:dict(popularity_limit=i*r['level_popularity'],max_count=min(100,r['member_limit']+(i-1)*r['member_growth'])) for i in range(1,r['max_level']+1)},west_config={**r['west_config'],'book_worth_config':{int(k):v for k,v in r['west_config']['book_worth_config'].items()}})


def new_union(ident,name,r):
    return dict(id=ident,name=name,level=1,popularity=0,money=r['initial_money'],notify='欢迎加入仙盟',notify_ex='',
                members={},applications={},forbidden=[],chat=[],events=[],tree=dict(state=1,seed=1,level=1,exp=0,planted=0,records=[],ranks=[]))


def prepare(role,now,r):
    from . import guild_match,guild_feast
    guild_feast.rollover(role,now,r)
    guild_match.rollover(role,now,r)
    s=role.setdefault('guild',dict(unions={},next_id=2,applications=[],day=-1))
    if not s['unions']:
        g=new_union(1,'本地仙盟',r)
        g['members']['10001']=dict(id=10001,name='本地盟主',rank=1,level=30,contrib=0,head_type=1,totalcontrib=0,jointime=now,lastlogin=now,online=False,toporder=0,logout_time=0,combat_power=1000)
        s['unions']['1']=g
    for k in ('union_id','union_rank','union_contrib','cur_union_contrib','union_store_flush_time'):role.setdefault(k,0)
    role.setdefault('union_name','')
    day=daily.day(now,r)
    if s['day']!=day:
        previous_day=s['day']
        s.update(day=day,cultivations=0,donations=0,purchases={},flushes=0,create_count=0,apply_count=0,join_count=0,tree_reward_count=0,store_stock=[])
        if previous_day>=0:offline.refresh_store(s,r)
    # [A] guildStoreUI L370-378 requests the store again when this deadline
    # expires. It is the NEXT refresh time, never the last refresh timestamp.
    # [B] Automatic free restocking shares the local daily reset at UTC+8.
    role['union_store_flush_time']=(day+1)*86400-r['timezone_offset_hours']*3600
    if now>=s.get('feast_buff_end',0):
        role.update(train_tree_rate=0,contrib_plus_rate=0);s['feast_fam_rate']=0
    from . import guild_feast
    guild_feast.account(role,s,r)
    g=s['unions'].get(str(int(role['union_id'])))
    if g:
        m=g['members'].get(str(int(role['role_id'])))
        if m:
            m.update(name=role['role_name'],level=role['level'],head_type=role.get('head_type',1),online=True,contrib=role['cur_union_contrib'],totalcontrib=role['union_contrib'])
            role.update(union_rank=m['rank'],union_name=g['name'])
        t=g['tree']
        if t['state']==2 and now>=t['planted']+r['tree_grow_seconds']:t['state']=3
        g['level']=min(r['max_level'],1+g['popularity']//r['level_popularity'])
    offline.prepare(role,s,g,now,r)
    return s,s['unions'].get(str(int(role['union_id'])))


def positive(data,key,maximum=2147483647):
    n=data.get(key); require(type(n) is int and 0<n<=maximum,'仙盟参数无效: '+key); return n


def selected_members(data):
    """[A] Native accept/reject/unmute buttons submit a selected role_list."""
    values=data.get('role_list')
    if values is None:return [str(positive(data,'role_id'))]
    if isinstance(values,dict):
        require(all(type(key)is int for key in values) and set(values)==set(range(1,len(values)+1)),'成员选择列表无效')
        values=[values[i] for i in range(1,len(values)+1)]
    require(isinstance(values,list) and 0<len(values)<=100 and
            all(type(v)is int and 0<v<=2147483647 for v in values) and
            len(set(values))==len(values),'成员选择列表无效')
    return list(map(str,values))


def pay(role,key,n):
    require(role.get(key,0)>=n,'元宝不足' if key=='gold_coin' else '银两或贡献不足');role[key]-=n


def contribution(role,n):
    role['union_contrib']+=n;role['cur_union_contrib']+=n
    return n


def reply(op,data):return encode(1301,dict(id=op,data=summon.lua(data)))
def notice(op,**data):return summon.event(82,dict(event_id=op,result=1,**data))


def info(g,r):
    return dict(id=g['id'],name=g['name'],level=g['level'],popularity=g['popularity'],order=g.get('order',1),
                cur_count=len(g['members']),max_count=offline.capacity(g,r),notify=g['notify'],notify_ex=g['notify_ex'],leader_name=next((m['name'] for m in g['members'].values() if m['rank']==1),''))


def member(role,g,r):
    from . import guild_match
    m=copy.deepcopy(g['members'][str(int(role['role_id']))]);m.update(union_contrib=role['union_contrib'],cur_union_contrib=role['cur_union_contrib'],contribute=role['union_contrib'])
    m.update(tree_state=g['tree']['state'],can_plant_tree=role['union_rank']==1,can_cultivate_tree=True,can_kill_tree=True,cultivate_time=10,union_protect_card=3,max_protect_card=3,can_search_gold=True,can_match_fight=True,has_action_point=True,is_match_time=True,is_bet_time=False,has_bet=False,cross_fight_flag=False,can_rece_award=False,west_config=client_config(r)['west_config'])
    match=guild_match.state(role['guild'],False,r) if r['wars_enabled'] else {}
    rights=client_config(r)['right_config'][role['union_rank']]['right_list']
    m.update(can_plant_tree=bool(rights.get(13)) and g['popularity']>=r['tree_require_pop'],cultivate_time=max(0,r['cultivate_limit']-role['guild']['cultivations']),has_action_point=match.get('fights',0)<r['battle_daily'] and match.get('life',r['match_life'])>0,is_bet_time=not match.get('fights') and not match.get('claimed'),has_bet=bool(match.get('bets')),cross_fight_flag=True,can_rece_award=bool(match.get('fights')) and not match.get('claimed'))
    if not r['wars_enabled']:
        m.update(can_match_fight=False,has_action_point=False,is_match_time=False,is_bet_time=False,has_bet=False,cross_fight_flag=False,can_rece_award=False)
    escort=role['guild'].get('escort',{})
    m['union_protect_card']=escort.get('cards',3)
    return m


def authorize(role,r,right):
    require(client_config(r)['right_config'].get(role['union_rank'],{}).get('right_list',{}).get(right,False),'仙盟权限不足')


def tree_data(role,s,g,now,r):
    t=g['tree']
    return dict(tree_state=t['state'],tree_seed_count=t['seed'],union_money=g['money'],require_pop=r['tree_require_pop'],
        init_seed_count=1,seed_cost_money=r['seed_cost_money'],tree_level=t['level'],tree_exp=t['exp'],full_exp=r['tree_exp_per_level'],
        tree_protect_time=t['planted']+r['tree_grow_seconds'],cultivate_time=max(0,r['cultivate_limit']-s['cultivations']),
        cultivate_cost=r['cultivate_gold'],gold_cultivate_rate=r['cultivate_gold_rate'],cultivate_info_list=t['records'],
        cultivate_record_time=s['day'],cultivate_record_count=s['cultivations'],tree_boss_info=dict(boss_hp=t.get('hp',r['tree_boss_hp']*(100+(t['level']-1)*10)//100),boss_full_hp=r['tree_boss_hp']*(100+(t['level']-1)*10)//100),
        rank_list=t['ranks'],cooltime=t.get('cooltime',0),flush_protect_cost=r['tree_flush_gold'],max_donate_count=r['donate_limit'],donate_count=s['donations'],donate_rate=r['donate_money_rate'])


def missions(r,s=None):
    # [A] tree_mission_cost_type.silver_coins = 4 (not object_type.silver = 12).
    rows=[dict(id=1,mission_type=1,cost_type=4,item_count=r['cultivate_silver'],contrib=r['cultivate_contrib'],exp=r['cultivate_exp'],pop=r['cultivate_pop'])]
    if s is not None:
        cost=r['mission_cost_types'][(s['day']+s['cultivations'])%len(r['mission_cost_types'])]
        tid={2:1021,3:1002}.get(cost,0)
        rows.append(dict(id=2,mission_type=2,cost_type=cost,item_id=tid,item_type=tid,item_count=r['cultivate_silver']*2 if cost==4 else 1,contrib=r['cultivate_contrib']*2,exp=r['cultivate_exp']*2,pop=r['cultivate_pop']*2))
    return rows


def store_data(s,r,refreshed=False):
    # [A] The original UI compares this field to numeric 1, not Lua true.
    return dict(flush_flag=int(refreshed),flush_cost=r['store_flush_gold'],item_list=[dict(id=x['id'],item=daily.spec(x['prize']),cost_contrib=x['cost'],buy_times=max(0,x['limit']-s['purchases'].get(str(x['id']),0))) for x in offline.store(s,r)])


def settle(role,req,now,r,parse,daily_rules):
    op=req['id']; d=parse(req['data']); require(isinstance(d,dict),'仙盟请求格式错误')
    if op in WAR_OPS or op==18 and d.get('query_type') in WAR_QUERIES:
        require(r['wars_enabled'],WAR_CLOSED)
    s,g=prepare(role,now,r); rid=str(int(role['role_id']))
    if op==18 and d.get('query_type')==4:
        page=positive(d,'page',10000)
        rows=sorted((info(v,r) for v in s['unions'].values()),key=lambda v:v['order'])
        return [reply(op,dict(query_type=4,page=page,union_list=rows[(page-1)*10:page*10]))]
    if op in (1,2,4):
        require(not role['union_id'],'已经加入仙盟');require(role['level']>=r['create_level' if op==1 else 'join_level'],'等级不足')
        if op==1:
            name=d.get('union_name','');require(isinstance(name,str),'仙盟名称格式无效');name=name.strip();require(2<=len(name)<=10 and len(name.encode())<32 and not any(c in name for c in '\x00\n\r'),'仙盟名称应为2至10字')
            require(all(v['name']!=name for v in s['unions'].values()),'仙盟名称已被使用')
            pay(role,'gold_coin',r['create_cost_gold'])
            ident=s['next_id'];s['next_id']+=1;s['create_count']+=1
            g=new_union(ident,name,r);s['unions'][str(ident)]=g;rank=1
        else:
            ident=positive(d,'union_id');g=s['unions'].get(str(ident));require(g is not None,'仙盟不存在')
            require(len(g['members'])<offline.capacity(g,r),'仙盟成员已满');rank=5
            require(s.get('join_count',0)<r['join_daily'],'今日加入次数已用完')
            if op==4:
                require(s.get('apply_count',0)<r['apply_daily'],'今日申请次数已用完');s['apply_count']=s.get('apply_count',0)+1
                for other in s['unions'].values():other['applications'].pop(rid,None)
                g['applications'][rid]=dict(offline.npc(int(rid),role['role_name'],now),npc=False,requested_at=now,level=role['level'],head_type=role.get('head_type',1),combat_power=role.get('role_combat_power',0),vip_level=role.get('vip_level',0))
                if not r['npc_auto_accept']:return [notice(7,role_id=int(rid))]
            g['applications'].pop(rid,None);s['join_count']=s.get('join_count',0)+1
            # [B] Offline public guild accepts applications immediately.
        g['members'][rid]=dict(id=role['role_id'],name=role['role_name'],rank=rank,level=role['level'],contrib=0,head_type=role.get('head_type',1),totalcontrib=0,jointime=now,lastlogin=now,online=True,toporder=0,logout_time=0,combat_power=role.get('role_combat_power',0))
        for other in s['unions'].values():other['applications'].pop(rid,None)
        role.update(union_id=g['id'],union_rank=rank,union_name=g['name'],union_contrib=0,cur_union_contrib=0)
        return ([notice(7,role_id=int(rid))] if op==4 else [])+[notice(1 if op==1 else 8),reply(18,dict(query_type=1,union_info=info(g,r),role_info=member(role,g,r)))]
    if op == 18 and d.get('query_type') == 15:
        from . import guild_activities
        return guild_activities.query(role,s,g,d,now,r)
    # [A] Monument opens public schedules/fortune without a membership check.
    # [B] A nonmember observes the existing public guild; this never joins it.
    if g is None and (op == 18 and d.get('query_type') in (8,9,10,15,18) or
                      op == 58 and d.get('query_type') in (20,21,22,26,30)):
        public = min(s['unions'].values(), key=lambda v: v['id'])
        if op == 58:
            from . import guild_match
            return guild_match.query(role,s,public,d,now,r,True)
        from . import guild_activities
        return guild_activities.query(role,s,public,d,now,r)
    require(g is not None and rid in g['members'],'请先加入仙盟')
    if op==18:
        q=d.get('query_type');out=dict(query_type=q,result=1)
        if q==1:out.update(union_info=info(g,r),role_info=member(role,g,r))
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
        if op==24:g['applications']={};return [notice(op)]
        targets=selected_members(d)
        require(all(key in g['applications'] and key not in g['members'] for key in targets),'申请不存在')
        if op==5:
            room=offline.capacity(g,r)-len(g['members']);require(room>0,'成员已满')
            targets=targets[:room]
        for target in targets:
            m=g['applications'].pop(target)
            if op==5:g['members'][target]=dict(m,rank=5,jointime=now)
        return [notice(op)]+([notice(9,role_id=int(key)) for key in targets] if op==6 else [])
    if op in (11,12,20,21,22,25):
        if op==22:authorize(role,r,17);g['forbidden']=[];return [notice(op)]
        if op==21:
            authorize(role,r,17);targets=selected_members(d)
            require(all(key!=rid and key in g['members'] and r['rank_power'][str(role['union_rank'])]>r['rank_power'][str(g['members'][key]['rank'])] for key in targets),'目标成员无效或权限不足')
            g['forbidden']=[v for v in g['forbidden'] if str(v['id']) not in targets]
            return [notice(op)]
        target=str(positive(d,'role_id'));m=g['members'].get(target);require(m is not None and target!=rid,'目标成员无效')
        require(r['rank_power'][str(role['union_rank'])]>r['rank_power'][str(m['rank'])],'不能操作同级或上级成员')
        if op in (11,12):
            rank=1 if op==12 else positive(d,'new_rank',7)
            # [A] Native "禅让" sends rank_appoint(11), new_rank=leader(1).
            # Keep the older explicit transfer event(12) as an alias.
            if rank==1:require(role['union_rank']==1,'只有盟主可以禅让')
            else:
                authorize(role,r,{7:6,2:7,3:8,4:9,5:10,6:10}[rank])
                require(r['rank_power'][str(role['union_rank'])]>r['rank_power'][str(rank)],'不能任命同级或上级')
                require(sum(v['rank']==rank for v in g['members'].values() if v['id']!=m['id'])<r['rank_limits'].get(str(rank),100),'该职位人数已满')
            m['rank']=rank
            if rank==1:g['members'][rid]['rank']=5;role['union_rank']=5
        elif op==25:
            authorize(role,r,2);del g['members'][target]
            g['forbidden']=[v for v in g['forbidden'] if v['id']!=m['id']]
            # Removed members cannot remain eligible for an escort or a team.
            escort=s.get('escort',{})
            escort['requests']=[ident for ident in escort.get('requests',[]) if ident!=m['id']]
            escort.get('issued',{}).pop(target,None)
            active=escort.get('active')
            if active and active['book'].get('protector_id')==m['id']:
                active['book'].update(had_protector=False,protector_id=0,cloud_time_list=[])
        else:
            authorize(role,r,17)
            g['forbidden']=[v for v in g['forbidden'] if v['id']!=m['id']]
            if op==20:g['forbidden'].append(dict(m,expires=now+r['mute_seconds'],reason=str(d.get('reason','仙盟管理'))[:100],operator=role['role_id'],time=now))
        return [notice(op,role_id=m['id'])]
    if op==23:return chat(role,d.get('chat_msg',d.get('content','')),now,r)
    if op in (34,35,14,15,36,37,70):
        t=g['tree']
        if op==35:return [reply(op,missions(r,s))]
        if op==70:return [reply(op,dict(rank_list=t['ranks']))]
        if op in (14,37):
            authorize(role,r,13);require(t['state']==1,'神树已种植')
            if op==37:require(t['seed']==0,'已有树种');require(g['money']>=r['seed_cost_money'],'仙盟资金不足');g['money']-=r['seed_cost_money'];t['seed']+=1
            else:require(g['popularity']>=r['tree_require_pop'],'仙盟威望不足，请先捐献或举办宴席');require(t['seed']>0,'没有树种');t.pop('hp',None);t.update(state=2,seed=t['seed']-1,planted=now,exp=0,records=[],ranks=[])
        if op==36:
            count=positive(d,'count',r['donate_limit']);require(s['donations']+count<=r['donate_limit'],'今日捐献额度不足')
            pay(role,'gold_coin',count);s['donations']+=count;offline.funds(g,count*r['donate_money_rate'],r);g['popularity']+=count;contribution(role,count*r['donate_contrib_rate'])
        if op==15:
            authorize(role,r,14);require(t['state']==2,'当前不能培育');require(s['cultivations']<r['cultivate_limit'],'今日培育次数已用完')
            require(d.get('cultivate_record_count')==s['cultivations'] and d.get('cultivate_record_time')==s['day'],'培育任务已过期，请刷新')
            mission=next((v for v in missions(r,s) if v['id']==d.get('mission_id') and v['mission_type']==d.get('mission_type')),None)
            require(mission is not None and d.get('cultivate_type') in (1,2),'培育任务无效')
            if mission['cost_type']==4:pay(role,'silver_coin',mission['item_count'])
            elif mission['cost_type']==1:
                ids=d.get('id_list',{});ids=list(ids.values()) if isinstance(ids,dict) else ids
                require(isinstance(ids,list) and len(ids)==mission['item_count'] and all(type(i)is int for i in ids) and len(set(ids))==len(ids),'装备选择无效')
                equips=[i for i in role['attachments'] if i['id'] in ids and i['attach_type']==5 and int(formation.ITEMS.get(i['type_id'],{}).get('main_type',0)) in (1,2,3) and not any(i.get(k) for k in ('owner_id','equip_order','equip_pos','is_lock','innate_owner_id'))]
                require(len(equips)==len(ids),'不能消耗已装备、锁定或本命装备')
                role['attachments']=[i for i in role['attachments'] if i not in equips]
            else:
                from .activity import consume
                consume(role,mission['item_id'],mission['item_count'])
            rate=1
            if d['cultivate_type']==2:pay(role,'gold_coin',r['cultivate_gold']);rate=r['cultivate_gold_rate']
            gain=mission['contrib']*rate*(100+(t['level']-1)*r['tree_level_bonus_percent'])//100
            exp=mission['exp']*rate
            if role.get('contrib_plus_rate',0)>0:
                gain=gain*150//100;role['contrib_plus_rate']-=1
            if role.get('train_tree_rate',0)>0:
                exp=exp*150//100;role['train_tree_rate']-=1
            n=contribution(role,gain);s['cultivations']+=1
            t['exp']+=exp;t['level']=min(99,t['level']+t['exp']//r['tree_exp_per_level']);t['exp']%=r['tree_exp_per_level']
            g['popularity']+=mission['pop']*rate
            t['records'].append(dict(name=role['role_name'],id=role['role_id'],cultivate_type=d['cultivate_type'],contrib=n,pop=mission['pop']*rate,exp=exp))
            t['records']=t['records'][-30:];daily.record(role,9,1,now,daily_rules)
            return [reply(op,dict(union_contrib=n)),reply(34,tree_data(role,s,g,now,r)),reply(35,missions(r,s))]
        data=tree_data(role,s,g,now,r)
        return [reply(op,data)]
    if op in (38,39,40):
        if op==39:
            require(s['flushes']<r['store_flush_limit'],'今日刷新次数已用完');pay(role,'gold_coin',r['store_flush_gold']);s['flushes']+=1;s['purchases']={};offline.refresh_store(s,r)
        if op==40:
            ident=positive(d,'item_id');count=positive(d,'buy_count',100)
            row=next((x for x in offline.store(s,r) if x['id']==ident),None);require(row is not None,'商品不存在')
            require(s['purchases'].get(str(ident),0)+count<=row['limit'],'商品购买次数不足');pay(role,'cur_union_contrib',row['cost']*count)
            prize=list(row['prize']);prize[2]*=count;journey.grant(role,prize);s['purchases'][str(ident)]=s['purchases'].get(str(ident),0)+count
            return [reply(op,dict(item_info=next(x for x in store_data(s,r)['item_list'] if x['id']==ident)))]
        return [reply(op,store_data(s,r,refreshed=op==39))]
    from . import guild_activities
    return guild_activities.settle(role,s,g,op,d,now,r)


def chat(role,msg,now,r):
    s,g=prepare(role,now,r)
    require(g is not None,'请先加入仙盟')
    require(not any(v['id']==role['role_id'] for v in g['forbidden']),'已被禁言')
    require(isinstance(msg,str) and 0<len(msg.strip())<=100 and '\x00' not in msg,'聊天内容无效')
    if msg.startswith('/'):
        result=offline.pet_command(role,s,g,msg,now,r)
        msg=result
    row=dict(id=role['role_id'],name=role['role_name'],time=now,chat_msg=msg,channel=6,sub_channel=6,vip_level=role.get('vip_level',0),single_score=0,level=role['level'],head_type=role.get('head_type',1),union_name=g['name'])
    g['chat'].append(row);g['chat']=g['chat'][-30:]
    return [encode(1098,row)]
