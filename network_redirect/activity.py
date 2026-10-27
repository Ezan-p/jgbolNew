"""Original activity wire contracts [A], explicit offline server inference [B].

All operations mutate a detached role. Backend encodes before commit. No client
victory, reward, cost, clock or claimed balance is accepted as authoritative.
"""
import copy
import json
import secrets
from pathlib import Path
from . import formation, journey, summon
from . import battle_replay
from .protocol import encode
ROOT = Path(__file__).resolve().parents[1]
require = formation.require
ENUMS = json.loads((ROOT/'analysis/evidence/activity_enums.json').read_text())
HANDLED = {1131, 1219, 1243, 1309, 1351, 1226, 1227, 1060, 1330, 1334, 1021, 1029, 1030, 1039, 1040, 1041, 1043, 1049, 1064, 1072, 1085, 1126, 1202, 1203, 1205, 1208, 1210, 1211, 1213, 1302, 1303, 1329, 1333, 1348, 1349, 1350, 1353}
FIGHTS = {2, 3, 4, 5, 6, 10, 11, 12}
EXCHANGE = {int(r['index']):r for r in summon.rows('top_score_exchange.csv')}
RANK_SCORE = summon.rows('top_score.csv')
CONVERT = {int(r['src_cortege_type']): r for r in summon.rows('convert_output.csv')}


def load_rules(path=ROOT/'server_config/activity_rules.json'):
    r=json.loads(Path(path).read_text())
    require(r.get('schema_version')==1 and r.get('mode')=='inferred','活动配置必须标注 inferred')
    require(isinstance(r.get('revision'),str) and bool(r['revision']),'活动配置版本缺失')
    require(type(r.get('timezone_offset_hours')) is int and -12<=r['timezone_offset_hours']<=14,'活动时区无效')
    for key in ('feed_max_count',
                'rank_daily_limit','rank_initial_order',
                'rape_free_refreshes','rape_refresh_gold','rape_single_refresh_gold','duty_daily_runs',
                'duty_initial_bonus','duty_silver_per_round','party_free_count','party_paid_count',
                'party_fight_gold','party_bonus_gold','party_bonus_limit','convert_daily_limit',
                'battle_level','battle_silver','home_boss_daily_limit','home_assistant_gold','home_missed_event_penalty',
                'abyss_offline_cap_seconds','abyss_tick_seconds','abyss_power_per_crystal','abyss_double_gold','abyss_grid_gold','babel_cell_coins','drug_craft_exp','drug_quality_level_step',
                'abyss_event_seconds','abyss_event_boss_hp','abyss_event_fight_gold','abyss_steal_max','abyss_map_paid_draws','abyss_map_gold','abyss_map_remove_count','land_tower_start_hour','land_daily_travel','land_daily_attack','land_travel_soul','land_charm_exchange','land_tower_tick','land_tower_soul','land_tower_total','land_tower_duration','land_boss_layers','land_boss_soul','land_hell_unlock_soul','land_hell_daily','land_max_actions','abyss_boss_max_actions'):
        require(type(r.get(key)) is int and 0<r[key]<=1000000,'活动数值无效：'+key)
    from . import activity_feed, activity_trial
    activity_trial.load_rules()
    activity_feed.validate(r)
    # Legacy action-budget keys are accepted but no longer truncate battles.
    require(r['land_tower_start_hour']<24 and r['land_boss_layers']<=99 and r['land_daily_travel']<=100,'逐鹿时段或关卡上限无效')
    require(isinstance(r.get('land_card_gold'),list) and len(r['land_card_gold'])==5 and r['land_card_gold'][0]==0 and all(type(v)is int and 0<=v<=100000 for v in r['land_card_gold']),'逐鹿翻牌费用无效')
    require(r['rank_initial_order']<=65535 and r['rank_daily_limit']<=255,'活动次数超过协议范围')
    require(r['duty_daily_runs']==3,'原版天命界面固定每日3次')
    from . import duty_balance, activity_convert, activity_practice, activity_pavilion
    from . import activity_hunt
    activity_hunt.load_rules()
    activity_pavilion.load_rules()
    from . import activity_monday
    activity_monday.load_rules()
    from . import activity_yuanshi
    activity_yuanshi.load_rules()
    from . import activity_rulai
    activity_rulai.load_rules()
    from . import activity_nine_sky
    activity_nine_sky.load_rules()
    duty_balance.rules()
    activity_convert.load_rules()
    activity_practice.load_rules()
    require(r.get('convert_item') == 1024, '原版天缘消耗魂缘丹1024')
    require(r['home_missed_event_penalty']<=100,'药田损失不能超过100%')
    require(type(r.get('home_friend_gain_percent'))is int and 0<=r['home_friend_gain_percent']<=100,'施肥增益无效')
    require(type(r.get('home_friend_silver'))is int and 0<r['home_friend_silver']<=1000000,'施肥奖励无效')
    require(type(r.get('home_starter_pet'))is int and r['home_starter_pet'] in range(201,207),'洞府初始灵兽配置无效')
    for periods in (r.get('feed_periods'), [r.get('party_period')]):
        require(isinstance(periods,list) and bool(periods),'活动时段缺失')
        for p in periods:require(isinstance(p,list) and len(p)==2 and all(type(v)is int for v in p) and 0<=p[0]<p[1]<=86400,'活动时段无效')
    require(len(r['feed_periods'])==2 and r['feed_periods'][0][1]<=r['feed_periods'][1][0],'包子时段重叠')
    require(r.get('battle_npc') in journey.NPCS and r.get('convert_item') in formation.ITEMS,'活动物品/对手配置无效')
    require(len(r.get('rape_skills',[]))==3 and all(t in formation.SKILLS for t in r['rape_skills']),'渡劫法术配置无效')
    require(r.get('seasonal_enabled') is False,'限时活动处理器尚未实现，不能配置为启用')
    require(set(r.get('seasonal_games',{}))=={'rice','moon','spring_money','spring_cards','fish'},'限时活动分项配置无效')
    for cfg in r['seasonal_games'].values():
        require(isinstance(cfg,dict) and type(cfg.get('enabled'))is bool and all(type(cfg.get(k))is int for k in ('start_time','end_time')) and 0<cfg['start_time']<cfg['end_time']<=2147483647,'限时活动时间配置无效')
    require(all(type(r.get(k))is int and 1<=r[k]<=1000 for k in ('seasonal_craft_daily_limit','seasonal_moon_bonus_every')),'节日制作次数配置无效')
    from . import activity_moon
    r['moon_rules'] = activity_moon.load_rules()
    require(set(r.get('seasonal_food_rewards',{}))=={'1217'},'历史五星粽子奖励配置无效')
    for rewards in r['seasonal_food_rewards'].values():
        require(isinstance(rewards,list) and 1<=len(rewards)<=10,'节日礼包奖励无效')
        for p in rewards:
            require(isinstance(p,list) and len(p)==4 and all(type(v)is int for v in p) and 0<p[2]<=1000 and p[3]==1 and (p[0] in (11,12) or p[0]==5 and p[1] in formation.ITEMS or p[0]==6 and p[1] in formation.SKILLS),'节日礼包奖励无效')
    require(isinstance(r.get('abyss_eye_choices'),list) and len(r['abyss_eye_choices'])==4 and len(set(r['abyss_eye_choices']))==4 and all(t in formation.BASES for t in r['abyss_eye_choices']),'火眼金睛选项无效')
    from . import activity_visit
    r['visit_rules'] = activity_visit.load_rules()
    for key in ('pray_rewards','party_rewards','home_pray_rewards','abyss_event_rewards','abyss_pray_consumes','abyss_map_rewards','land_card_rewards','land_full_card_rewards','seasonal_moon_bonus'):
        require(isinstance(r.get(key),list) and len(r[key])>0,'活动奖励缺失')
        for p in r[key]:
            require(isinstance(p,list) and len(p)==4 and all(type(v)is int for v in p),'活动奖励格式错误')
            typ,tid,n,lv=p
            require(0<n<=1000000 and 1<=lv<=200 and ((typ in (11,12)) or (typ==5 and tid in formation.ITEMS)),'活动奖励无效')
    require(all(p[0]==11 and p[1]==0 and p[3]==1 for p in r['pray_rewards']),'神石祈福奖励必须为元宝')
    require(len(r['abyss_map_rewards'])==12 and r['abyss_map_remove_count']+r['abyss_map_paid_draws']<12,'宝图奖盘或次数无效')
    require(set(r.get('train_increase',{}))==set(formation.STATS) and all(type(v)is int and 0<v<=10000 for v in r['train_increase'].values()),'修炼属性配置无效')
    for name in ('undergo_shop','home_shop','abyss_shop'):
        require(isinstance(r.get(name),list) and 1<=len(r[name])<=30,'活动商店配置无效')
        for goods in r[name]:
            p=goods.get('reward')
            require(isinstance(p,list) and len(p)==4 and all(type(v)is int for v in p) and p[0]==5 and p[1] in formation.ITEMS and 1<=p[2]<=100000 and p[3]==1,'活动商品无效')
            require(type(goods.get('limit'))is int and 1<=goods['limit']<=1000,'活动限购无效')
            if name=='home_shop':
                require(type(goods.get('page',1))is int and goods.get('page',1) in (1,2),'洞府商店分页无效')
                q=goods.get('consume')
                require(isinstance(q,list) and len(q)==4 and all(type(v)is int for v in q) and q[0]==5 and q[1] in formation.ITEMS and 0<q[2]<=1000000 and q[3]==1,'洞府商品消耗无效')
            else:require(type(goods.get('cost'))is int and 0<goods['cost']<=1000000,'活动商品价格无效')
    from . import activity_fish
    activity_fish.validate(r)
    from . import activity_caishen
    activity_caishen.validate(r)
    from . import activity_tangwang
    r['tangwang_rules'] = activity_tangwang.load_rules()
    require(r.get('babel_energy_items')=={'20016':10,'20017':25,'20018':80,'20019':200} and all(type(v) is int for v in r['babel_energy_items'].values()),'通天塔恢复配置须符合原版仙露数值')
    require(r['abyss_tick_seconds']<=r['abyss_offline_cap_seconds'] and r['abyss_offline_cap_seconds']//r['abyss_tick_seconds']<=2000,'挂机结算周期过长')
    return r


def day(now,r):return (now+r['timezone_offset_hours']*3600)//86400

def prepare(role,now,r,peers=None):
    from . import activity_pavilion
    activity_pavilion.prepare(role,now,activity_pavilion.load_rules())
    s=role.setdefault('activity',{})
    from . import activity_tangwang
    activity_tangwang.state(role,now,r['tangwang_rules'])
    if 'fish' in s.get('seasonal',{}):
        from . import activity_fish
        activity_fish.rollover(role,now,r)
    if 'spring' in s.get('seasonal',{}):
        from . import activity_caishen
        activity_caishen.rollover(role,now,r)
    if 'nine_sky' in s:
        from . import activity_nine_sky
        activity_nine_sky.state(role,now,activity_nine_sky.load_rules())
    if 'yuanshi' in s:
        from . import activity_yuanshi, welfare
        activity_yuanshi.state(role,now,activity_yuanshi.load_rules())
    s.setdefault('rank_order',r['rank_initial_order']);s.setdefault('rank_score',0)
    s.setdefault('fight_id',100000);s.setdefault('duty_best',0)
    s.setdefault('duty_runs',0);s.setdefault('duty',None)
    for k,v in dict(drug_level=1,drug_exp=0,drug_study_flag=0,drug_study_flag2=0).items():role.setdefault(k,v)
    role.setdefault('rule_index',0)
    for k in ('max_hp_plus','gongji_plus','fangyu_plus','max_magic_plus'):role.setdefault(k,0)
    if 'hunt' in s:
        from . import activity_hunt
        activity_hunt.state(role,now,r)
    if 'babel' in s:
        from . import activity_babel
        activity_babel.state(role,now,r)
    if 'home' in s:
        from . import activity_home
        activity_home.state(role,now,r)
    from . import activity_party
    activity_party.prepare(role,now,r)
    from . import activity_duty
    activity_duty.prepare(role,now,r,peers)
    from . import activity_trial
    activity_trial.prepare(role,now,r)
    if s.get('day') is None or s['day']<day(now,r):
        s.update(day=day(now,r),feed={},visits={},rank_count=0,rank_claimed=False,
                 rape_refreshes=0,rape_total_refreshes=0,rape_boards=None,party_count=0,
                 party_paid=0,party_damage=0,party_bonus=0,party_claimed=False,praised=False)
        role.update(pray_spirit_times=0,convert_fight_count=0,party_fight_count=0,party_fight_count_plus=0,
                    gongji_plus_rate=0)
    activity_party.sync(role)
    from . import vip
    role.update(top_order=s['rank_order'],top_score=s['rank_score'],top_fight_limit=vip.limit(role,vip.RANK,r['rank_daily_limit']),
                rape_flush_limit=vip.limit(role,vip.RAPE,r['rape_free_refreshes']),convert_fight_limit=vip.limit(role,vip.CONVERT,r['convert_daily_limit']))
    from . import activity_rank
    activity_rank.prepare(role,now,r)
    return s


def spend(role,key,n):
    require(type(n)is int and n>=0 and role.get(key,0)>=n,'元宝不足' if key=='gold_coin' else '资源不足')
    role[key]-=n


def consume(role,tid,n):
    require(type(n)is int and n>0,'消耗数量无效')
    items=[i for i in role['attachments'] if i['attach_type']==5 and i['type_id']==tid and not i.get('owner_id') and not i.get('equip_pos') and not i.get('is_lock')]
    require(sum(i['count'] for i in items)>=n,'道具不足')
    for i in items:
        take=min(i['count'],n);i['count']-=take;n-=take
    role['attachments']=[i for i in role['attachments'] if i not in items or i['count']>0]


def prizes(role,specs):return [journey.grant(role,p) for p in specs]

def prize_spec(spec):
    return dict(object_type=spec[0],attach_type=spec[1],attach_count=spec[2],attach_level=spec[3])

def visit_list(role,r):
    from . import activity_visit
    return activity_visit.visit_list(role)


def feed_data(role,r):
    f=role['activity']['feed']
    return dict(feed_list=[role.get('feed_time'+str(i),2) if str(i) in f else 1 for i in (1,2)],
                feed_count=max((v['count'] for v in f.values()),default=0))


def statuses(role,now,r,flag,peers=None):
    from .activity_land import status as land_status
    s=role['activity']
    if flag==0:
        from . import activity_nine_sky
        from . import activity_pavilion, activity_hunt
        from . import activity_yuanshi, welfare
        from .activity_seasonal import status as seasonal_status
        return summon.event(47,dict(visit_list=visit_list(role,r),feed_data=feed_data(role,r),
                                   pavilion_data=activity_pavilion.status(role,now,peers),
                                   hunt_data=activity_hunt.status(role,now,r),
                                   nine_sky_data=activity_nine_sky.status(now),
                                   yuanshi_info=activity_yuanshi.client_config(now),
                                   spring_info=welfare.spring_info(role,now,welfare.load_rules()),
                                   imperial_exam=dict(start_time=0,end_time=0),**seasonal_status(role,now,r)))
    require(flag==1,'未知活动页')
    return summon.event(48,dict(party_start_period=[dict(begin_seconds=r['party_period'][0],end_seconds=r['party_period'][1])],
        last_convert_type=s.get('last_convert_type',0),cur_fight_count=r['duty_daily_runs']-s['duty_runs'],
        max_fight_count=r['duty_daily_runs'],party_seld_order=role.get('party_order',0),
        party_free_count=s['party_count'],party_pay_count=s['party_paid'],prey_status_info=land_status(now,r)))


def feed(role,req,now,r,peers=None):
    from . import activity_feed
    return activity_feed.settle(role,req,now,r,peers)


def visit(role,req,r):
    from . import activity_visit
    return activity_visit.settle(role,req,r['visit_rules'])


def pray(role,req,r):
    from . import activity_pray
    return activity_pray.settle(role,req,r)


def rank(role,r):
    from . import activity_rank
    return activity_rank.board(role)


def rank_score(order,column):
    return next(int(row[column]) for row in RANK_SCORE if int(row['begin'])<=order<=int(row['end']))


def rape_board(role,now,r,update=1):
    from . import activity_rape
    return activity_rape.board(role,now,r,update)


def duty_data(role,r,result=None):
    from . import activity_duty
    return activity_duty.data(role,r,result)


def party_info(role,r):
    from . import activity_party
    return activity_party.info(role,r)


def query_lineup(role,req,r):
    s=role['activity'];ident=req['des_id']
    from . import activity_rape
    packet=activity_rape.inspection(role,ident)
    if packet is not None:
        require(req['des_type'] in (1,2),'渡劫阵容类型无效')
        return [packet]
    from . import activity_rank, activity_land_npc
    if 940000<=ident<943000:
        require(req['des_type']==1,'逐鹿阵容目标类型无效')
        packet=activity_land_npc.inspection(role,ident)
        require(packet is not None,'逐鹿对手已失效')
        return [packet]
    if ident in activity_rank.catalog():
        require(req['des_type'] in (1,2),'阵容目标类型无效')
        return [activity_rank.inspection(role,ident)]
    from . import activity_party
    if ident in activity_party.catalog():
        require(req['des_type'] in (1,2),'蟠桃阵容类型无效')
        return [activity_party.inspection(role,ident)]
    own=ident==role['role_id']
    gs=role.get('guild',{});g=gs.get('unions',{}).get(str(int(role.get('union_id',0))))
    if g and (str(int(ident)) in g['members'] or ident in range(90001,90007) or ident in range(91001,91004)):
        from . import guild,guild_match
        return [summon.event(11,guild_match.lineup(role,ident,guild.load_rules()))]
    valid=own or req['des_type']==2 and any(str(int(ident)) in b['form_list'].get('2',{}) for b in (s['rape_boards'] or []))
    require(valid,'阵容目标不存在')
    if own:chars=copy.deepcopy([c for c in role['corteges'] if c.get('order')])
    else:
        _,enemies=journey.fighters(role,dict(cortege_list=f"{r['battle_npc']}|{r['battle_level']}"))
        chars=[dict(c,id=ident,evolve_level=0,reborn_layer=0) for c in enemies]
    for c in chars:
        c.pop('skills',None)
        c.update(type_id=c['type'],max_hp_show=c['hp'],max_magic_show=c['magic'],
                 wuligongji_show=c['gongji'],wulifangyu_show=c['fangyu'])
    data=dict(role_id=ident,role_name=role['role_name'] if own else '本地活动对手',level=role['level'] if own else r['battle_level'],
        vip_level=0,head_type=1,rank=0,owner_cheer_info={},title_info={},animal_info={},hole_train={},
        cortege_list=chars,cheer_cortege=[],skill_list=[],equip_list=[],ext_skill_list=[],ext_star_list=[])
    from . import cheer
    data.update(cheer.inspection(role, own))
    return [summon.event(11,data)]


def battle(role,req,now,r,jrules,frules):
    ft=req['fight_type'];s=role['activity'];target=None
    if ft==11:
        from . import activity_trial
        return activity_trial.battle(role,req,now,r,jrules)
    if ft==4:
        from . import activity_practice
        return activity_practice.battle(role,req,now,r,jrules)
    if ft==10:
        from . import activity_convert
        return activity_convert.battle(role,req,now,r,jrules)
    if ft==5:
        from . import activity_duty
        return activity_duty.battle(role,req,now,r,jrules)
    if ft in (3,12):
        from . import activity_rape
        return activity_rape.battle(role,req,now,r,jrules)
    if ft==2:
        from . import activity_rank
        return activity_rank.battle(role,req,now,r,jrules)
    require(role['level']>={2:6,3:8,4:5,5:12,6:13,10:16,11:1}[ft],'等级不足')
    if ft==6:
        second=(now+r['timezone_offset_hours']*3600)%86400
        require(r['party_period'][0]<=second<r['party_period'][1],'蟠桃会尚未开放')
        require(day(now,r)==s['party']['day'] and now>=s['party']['clock'],'蟠桃会时钟已回退，请恢复本地时间')
        require(req['des_value'] in (0,1),'蟠桃挑战类型无效')
        if req['des_value']==0:
            require(s['party_count']<r['party_free_count'],'免费挑战次数已用完')
            s['party_count']+=1
        else:
            require(s['party_paid']<r['party_paid_count'],'今日蟠桃会次数已用完')
            spend(role,'gold_coin',r['party_fight_gold']);s['party_paid']+=1
        role['party_fight_count']=s['party_count'];role['party_fight_count_plus']=s['party_paid']
    require(any(c.get('order') for c in role['corteges']),'请先上阵神仙')
    cfg=dict(cortege_list=f"{r['battle_npc']}|{r['battle_level']}")
    if ft==6:
        from . import activity_party
        boss=activity_party.info(role,r)
        cfg=dict(cortege_list=f"{boss['boss_type']}|{boss['boss_level']}")
    units=journey.fighters(role,cfg)
    if ft==6:
        for u in units[0]:u['gongji']=u['gongji']*(100+s['party_bonus']*10)//100
        hp=boss['cur_hp']
        units[1][0].update(hp=hp,max_hp=activity_party.rules()['boss_hp'])
    result,lineup,actions=journey.battle(role,cfg,jrules,units=units);win=1<=result<=3
    events=[];s['fight_id']+=1;fid=s['fight_id']
    if ft==6:
        damage=min(hp,journey.combat_engine.total_damage(actions))
        gain=prizes(role,r['party_rewards'])+activity_party.seasonal_rewards(role,now,r)
        activity_party.record(role,damage,gain,r)
        info=party_info(role,r);info.update(fight_prize=gain,cur_damage=damage)
        events.append(summon.event(29,info))
    if win and ft in (2,3):role['silver_coin']+=r['battle_silver']
    return journey.combat_engine.event_packets(actions,fid)+[encode(1028,dict(fight_id=fid,first_hand=1,des_name=boss['name'] if ft==6 else '本地活动对手',lineup_count=len(lineup),lineup=lineup)),
        *battle_replay.result_packets(1027, dict(fight_id=fid,fight_type=ft,final_result=result,fight_round=len(actions),fight_result=actions))]+events+[
        summon.event(44,dict(fight_id=fid,fight_type=ft))]


def settle(role,mid,req,now,r,jrules,frules,parse,peers=None):
    from . import feature_levels
    feature_levels.check(role, mid, req)
    s=prepare(role,now,r,peers)
    if mid==1131:
        from . import progression
        return progression.settle(role,req,now)
    if mid==1051 and req['item_type']==1243:
        from . import activity_nine_sky
        return activity_nine_sky.use_bag(role,req)
    if mid==1309:
        from . import activity_nine_sky
        return activity_nine_sky.settle(role,req,now,parse,peers)
    if mid==1351:
        from . import activity_rulai
        return activity_rulai.settle(role,req,now)
    if mid==1051 and req['item_type'] in (1367,1368):
        from . import activity_rulai
        return activity_rulai.use_bag(role,req)
    if mid==1334:
        from . import activity_yuanshi, welfare
        return activity_yuanshi.settle(role,req,now)
    if mid==1051 and req['item_type']==1808:
        from . import activity_yuanshi, welfare
        return activity_yuanshi.use_bag(role,req)
    if mid==1226:
        from . import activity_hunt
        return activity_hunt.settle(role,req,now,r)
    if mid==1051 and req['item_type'] in (1036,1037,1324):
        from . import activity_hunt
        return activity_hunt.use_item(role,req,now,r)
    if mid==1227:
        from . import activity_pavilion
        return activity_pavilion.settle(role,req,now,peers)
    if mid in (1219, 1243):
        from . import activity_monday
        return activity_monday.settle(role,mid,req,now)
    if mid == 1350:
        from . import activity_arena
        return activity_arena.settle(role,req,now,r,jrules,parse)
    if mid == 1244 and req['fight_type'] == 4:
        from . import activity_arena
        return activity_arena.replay(role,req)
    from . import activity_duty
    if mid==1043:
        return activity_duty.update(role,req,now,r,peers)
    if mid==1026 and req['fight_type']==5:
        return activity_duty.battle(role,req,now,r,jrules,peers)
    if mid==1049 and req['query_type']==4:
        activity_duty.guard(role,now,r)
        return [summon.event(39,activity_duty.rank_data(role,peers))]
    if mid==1039 and 2**40<=req['des_id']<2**41:
        return activity_duty.inspection(role,req,peers)
    if mid in (1029,1041,1060,1072) or mid==1026 and req['fight_type'] in (3,12):
        from . import activity_rape
        return activity_rape.settle(role,mid,req,now,r,jrules,parse)
    if mid == 1051 and req['item_type'] == 1346:
        from . import pets
        return pets.use_box(role,req)
    if mid == 1330:
        from . import pets
        return pets.settle(role,req,now,r,parse)
    if mid in (1021,1203,1244) or mid==1026 and req['fight_type']==2 or mid==1201 and req['flag']==2 or mid==1051 and req['item_type']==1021:
        from . import activity_rank
        return activity_rank.settle(role,mid,req,now,r,jrules)
    if mid==1208:
        from .activity_fish import settle as fish
        return fish(role,req,now,r)
    if mid in (1210,1211,1213):
        from .activity_spring import settle as spring
        return spring(role,mid,req,now,r)
    if mid==1051:
        from .activity_seasonal import use_food
        return use_food(role,req,r)
    if mid in (1126,1333):
        from .activity_seasonal import settle as seasonal
        return seasonal(role,mid,req,now,r)
    if mid==1059:
        from .activity_drug import use_exp
        return use_exp(role,req)
    if mid==1329:
        from . import activity_abyss
        return activity_abyss.settle(role,req,now,r,jrules,parse)
    if mid==1303:
        from . import activity_land_team
        return activity_land_team.settle(role,req,now,r,parse)
    if mid==1302:
        from . import activity_land
        return activity_land.settle(role,req,now,r,jrules,parse)
    if mid==1348:
        from . import activity_home
        return activity_home.settle(role,req,now,r,jrules,parse)
    if mid==1349:
        from . import activity_undergo
        return activity_undergo.settle(role,req,now,r,jrules,frules,parse)
    if mid==1353:
        from . import activity_babel
        return activity_babel.settle(role,req,now,r,jrules,parse)
    if mid==1205:
        from . import activity_rulai
        return [activity_rulai.sync(role,now), statuses(role,now,r,req['flag'],peers)]
    if mid==1040:return feed(role,req,now,r,peers)
    if mid==1030:return visit(role,req,r)
    if mid==1085:
        require(s['day']==day(now,r),'祈福日期已回退，请恢复本地时间')
        return pray(role,req,r)
    if mid==1039:return query_lineup(role,req,r)
    if mid==1064:
        from . import activity_trial
        return activity_trial.query(role,req,now,r)
    if mid==1026:return battle(role,req,now,r,jrules,frules)
    if mid==1049:
        typ=req['query_type'];require(1<=typ<=5,'未知排行查询')
        if typ in (1,2,3,5):
            from . import activity_party
            return activity_party.query(role,typ,r,req)
    if mid==1202:
        require(day(now,r)==s['party']['day'] and now>=s['party']['clock'],'蟠桃会时钟已回退，请恢复本地时间')
        require(req['flag']==1,'鼓舞操作无效')
        require(r['party_period'][0]<=(now+r['timezone_offset_hours']*3600)%86400<r['party_period'][1],'蟠桃会尚未开放')
        require(role['level']>=13 and s['party_bonus']<r['party_bonus_limit'],'蟠桃加成已达上限')
        spend(role,'gold_coin',r['party_bonus_gold']*(s['party_bonus']+1));s['party_bonus']+=1
        s['party']['bonus']=s['party_bonus']
        role['gongji_plus_rate']=s['party_bonus']*10
        return [summon.event(32,{})]
    if mid==1201:
        from . import activity_party
        require(req['flag']==1 and role['level']>=13,'蟠桃领奖条件不足')
        return activity_party.claim(role)
    raise formation.Rejected('活动操作参数无效')


def attributes(role):
    fields = {7:'silver_coin',8:'gold_coin',101:'strength',102:'energy',20:'pray_spirit_times',
              73:'rule_index',75:'max_hp_plus',76:'max_magic_plus',77:'gongji_plus',78:'fangyu_plus',
              48:'convert_fight_limit',49:'convert_fight_count',50:'convert_fight_time',
              61:'top_fight_limit',62:'rape_flush_limit',112:'party_fight_count',113:'party_fight_count_plus',
              132:'top_day_prize_time',133:'top_fight_time',134:'top_fight_count',136:'top_fight_count_plus',137:'top_first_promote_time',138:'top_first_promote_prize',30:'role_combat_power',10:'spirit_retain',85:'gongji_plus_rate',124:'party_take_prize'}
    role['top_score']=role['activity']['rank_score'];role['top_order']=role['activity']['rank_order']
    fields.update({582:'drug_level',583:'drug_exp',584:'drug_study_flag',585:'drug_study_flag2',614:'hole_hp_plus',131:'top_score',3:'level',5:'cur_exp',6:'next_exp'})
    for i,key in enumerate(('gongji','fangyu','fashang','fakang'),1):
        name='train_'+key+'_index';fields[615+i]=name
        role[name]=role['activity'].get('home',{}).get('train',{}).get(str(i),{}).get('level',0)
    # Original 1032 handler writes field 134 directly to the remaining-count label.
    values={t:int(role.get(k,0)) for t,k in fields.items()}
    values[134]=max(0,role['top_fight_limit']+role.get('top_fight_count_plus',0)-role['activity']['rank_count'])
    attrs=[dict(type=t,value=value) for t,value in values.items()]
    return [encode(1032,dict(id=role['role_id'],unit_type=1,attr_count=len(attrs),attr_list=attrs))]
