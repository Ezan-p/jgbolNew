"""Original activity wire contracts [A], explicit offline server inference [B].

All operations mutate a detached role. Backend encodes before commit. No client
victory, reward, cost, clock or claimed balance is accepted as authoritative.
"""
import copy
import json
import secrets
from pathlib import Path
from . import formation, journey, summon
from .protocol import encode
ROOT = Path(__file__).resolve().parents[1]
require = formation.require
ENUMS = json.loads((ROOT/'analysis/evidence/activity_enums.json').read_text())
HANDLED = {1021, 1029, 1030, 1039, 1040, 1041, 1043, 1049, 1064, 1072, 1085, 1126, 1202, 1203, 1205, 1208, 1210, 1211, 1213, 1302, 1329, 1333, 1348, 1349, 1353}
FIGHTS = {2, 3, 4, 5, 6, 10, 11}
PRAY = {int(r['pray_times']): int(r['spirit_coins']) for r in summon.rows('pray_spirit_config.csv')}
QUALITY = {int(r['cortege_quality']): r for r in summon.rows('cortege_quality.csv')}
EXCHANGE = {int(r['index']):r for r in summon.rows('top_score_exchange.csv')}
RANK_SCORE = summon.rows('top_score.csv')
DICE_RATE = {tuple(map(int,x['form_type'].split('|'))):int(x['rate']) for x in summon.rows('luhsing_form_rate.csv')}
CONVERT = {int(r['src_cortege_type']): r for r in summon.rows('convert_output.csv')}


def load_rules(path=ROOT/'server_config/activity_rules.json'):
    r=json.loads(Path(path).read_text())
    require(r.get('schema_version')==1 and r.get('mode')=='inferred','活动配置必须标注 inferred')
    require(isinstance(r.get('revision'),str) and bool(r['revision']),'活动配置版本缺失')
    require(type(r.get('timezone_offset_hours')) is int and -12<=r['timezone_offset_hours']<=14,'活动时区无效')
    for key in ('feed_max_count','feed_base_strength','feed_strength_per_bun','feed_max_strength',
                'rank_daily_limit','rank_initial_order',
                'rape_free_refreshes','rape_refresh_gold','rape_single_refresh_gold','duty_daily_runs',
                'duty_round_limit','duty_silver_per_round','party_free_count','party_paid_count',
                'party_fight_gold','party_bonus_gold','party_bonus_limit','convert_daily_limit',
                'battle_level','battle_silver','trial_daily_limit','trial_bosses_per_day','trial_boss_hp','trial_cooldown_seconds','home_boss_daily_limit','home_assistant_gold','home_missed_event_penalty',
                'abyss_offline_cap_seconds','abyss_tick_seconds','abyss_power_per_crystal','abyss_double_gold','abyss_grid_gold','babel_cell_coins','drug_craft_exp','drug_quality_level_step',
                'abyss_event_seconds','abyss_event_boss_hp','abyss_event_fight_gold','abyss_steal_max','abyss_map_paid_draws','abyss_map_gold','abyss_map_remove_count','land_tower_start_hour','land_daily_travel','land_daily_attack','land_travel_soul','land_charm_exchange','land_tower_tick','land_tower_soul','land_tower_total','land_tower_duration','land_boss_layers','land_boss_soul','land_hell_unlock_soul','land_hell_daily','land_max_actions','abyss_boss_max_actions'):
        require(type(r.get(key)) is int and 0<r[key]<=1000000,'活动数值无效：'+key)
    require(r['abyss_boss_max_actions']<=80,'冥仙精魄战报超过协议上限')
    require(r['land_tower_start_hour']<24 and r['land_boss_layers']<=99 and r['land_daily_travel']<=100 and r['land_max_actions']<=80,'逐鹿时段或关卡上限无效')
    require(isinstance(r.get('land_card_gold'),list) and len(r['land_card_gold'])==5 and r['land_card_gold'][0]==0 and all(type(v)is int and 0<=v<=100000 for v in r['land_card_gold']),'逐鹿翻牌费用无效')
    require(r['rank_initial_order']<=65535 and r['rank_daily_limit']<=255,'活动次数超过协议范围')
    require(r['home_missed_event_penalty']<=100,'药田损失不能超过100%')
    require(type(r.get('home_friend_gain_percent'))is int and 0<=r['home_friend_gain_percent']<=100,'施肥增益无效')
    require(type(r.get('home_friend_silver'))is int and 0<r['home_friend_silver']<=1000000,'施肥奖励无效')
    friends=r.get('home_offline_friends')
    require(isinstance(friends,list) and 1<=len(friends)<=20,'离线洞府好友配置无效')
    require(all(isinstance(f,dict) and type(f.get('id'))is int and 900000<=f['id']<1000000 and isinstance(f.get('name'),str) and 1<=len(f['name'])<=20 for f in friends),'离线洞府好友字段无效')
    require(len({f['id'] for f in friends})==len(friends),'离线洞府好友编号重复')
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
    require(all(type(r.get(k))is int and 1<=r[k]<=1000 for k in ('seasonal_craft_daily_limit','seasonal_moon_bonus_every','seasonal_travel_material_count','fish_daily_nets','fish_gold_per_net','fish_per_catch')),'节日制作次数配置无效')
    require(type(r.get('spring_daily_coins'))is int and 1<=r['spring_daily_coins']<=10000,'财神奖励无效')
    require(isinstance(r.get('spring_card_rewards'),list) and len(r['spring_card_rewards'])==4,'字牌奖励缺失')
    require(set(r.get('seasonal_food_rewards',{}))==set(map(str,(1130,1131,1132,1133,1213,1214,1215,1216,1217))),'节日礼包奖励不完整')
    for rewards in list(r['seasonal_food_rewards'].values())+[r['spring_card_rewards']]:
        require(isinstance(rewards,list) and 1<=len(rewards)<=10,'节日礼包奖励无效')
        for p in rewards:
            require(isinstance(p,list) and len(p)==4 and all(type(v)is int for v in p) and 0<p[2]<=1000 and p[3]==1 and (p[0] in (11,12) or p[0]==5 and p[1] in formation.ITEMS or p[0]==6 and p[1] in formation.SKILLS),'节日礼包奖励无效')
    require(isinstance(r.get('abyss_eye_choices'),list) and len(r['abyss_eye_choices'])==4 and len(set(r['abyss_eye_choices']))==4 and all(t in formation.BASES for t in r['abyss_eye_choices']),'火眼金睛选项无效')
    for key in ('visit_rewards','visit_fu_pool','pray_rewards','party_rewards','trial_rewards','home_pray_rewards','abyss_event_rewards','abyss_pray_consumes','abyss_map_rewards','land_card_rewards','land_full_card_rewards','seasonal_moon_bonus','fish_pool'):
        require(isinstance(r.get(key),list) and len(r[key])>0,'活动奖励缺失')
        for p in r[key]:
            require(isinstance(p,list) and len(p)==4 and all(type(v)is int for v in p),'活动奖励格式错误')
            typ,tid,n,lv=p
            require(0<n<=1000000 and 1<=lv<=200 and ((typ in (11,12)) or (typ==5 and tid in formation.ITEMS)),'活动奖励无效')
    require(len(r['visit_rewards'])==3,'福禄寿奖励必须三组')
    require(len(r['abyss_map_rewards'])==12 and r['abyss_map_remove_count']+r['abyss_map_paid_draws']<12,'宝图奖盘或次数无效')
    require(set(r.get('train_increase',{}))==set(formation.STATS) and all(type(v)is int and 0<v<=10000 for v in r['train_increase'].values()),'修炼属性配置无效')
    for name in ('undergo_shop','home_shop','abyss_shop','spring_shop','fish_shop'):
        require(isinstance(r.get(name),list) and 1<=len(r[name])<=30,'活动商店配置无效')
        for goods in r[name]:
            p=goods.get('reward')
            require(isinstance(p,list) and len(p)==4 and all(type(v)is int for v in p) and p[0]==5 and p[1] in formation.ITEMS and 1<=p[2]<=100000 and p[3]==1,'活动商品无效')
            require(type(goods.get('limit'))is int and 1<=goods['limit']<=1000,'活动限购无效')
            if name=='home_shop':
                q=goods.get('consume')
                require(isinstance(q,list) and len(q)==4 and all(type(v)is int for v in q) and q[0]==5 and q[1] in formation.ITEMS and 0<q[2]<=1000000 and q[3]==1,'洞府商品消耗无效')
            else:require(type(goods.get('cost'))is int and 0<goods['cost']<=1000000,'活动商品价格无效')
    require(len(r['fish_shop'])%5==0 and len({x['reward'][1] for x in r['fish_shop']})==len(r['fish_shop']),'东海商品须为完整五项分页且类型不重复')
    require(5<=len(r['fish_pool'])<=20 and len(r['fish_pool'])%5==0,'原版东海奖池预览需要每行五项完整配置')
    require(set(r.get('babel_energy_items',{}))=={'20016','20017','20018','20019'} and all(type(v)is int and 1<=v<=100 for v in r['babel_energy_items'].values()),'通天塔恢复配置无效')
    require(r['abyss_tick_seconds']<=r['abyss_offline_cap_seconds'] and r['abyss_offline_cap_seconds']//r['abyss_tick_seconds']<=2000,'挂机结算周期过长')
    return r


def day(now,r):return (now+r['timezone_offset_hours']*3600)//86400

def prepare(role,now,r):
    s=role.setdefault('activity',{})
    s.setdefault('rank_order',r['rank_initial_order']);s.setdefault('rank_score',0)
    s.setdefault('fight_id',100000);s.setdefault('duty_best',0)
    for k,v in dict(drug_level=1,drug_exp=0,drug_study_flag=0,drug_study_flag2=0).items():role.setdefault(k,v)
    role.setdefault('rule_index',0)
    for k in ('max_hp_plus','gongji_plus','fangyu_plus','max_magic_plus'):role.setdefault(k,0)
    if s.get('day')!=day(now,r):
        s.update(day=day(now,r),feed={},visits={},rank_count=0,rank_claimed=False,
                 rape_refreshes=0,rape_boards=None,duty_runs=0,duty=None,party_count=0,
                 party_paid=0,party_damage=0,party_bonus=0,party_claimed=False,praised=False,
                 trial=None,trial_count=0,trial_next=0,trial_spawned=0)
        role.update(pray_spirit_times=0,convert_fight_count=0,party_fight_count=0,party_fight_count_plus=0,
                    gongji_plus_rate=0,party_take_prize=0)
    for key,value in dict(trial=None,trial_count=0,trial_next=0,trial_spawned=0).items():s.setdefault(key,value)
    role.update(top_order=s['rank_order'],top_score=s['rank_score'],top_fight_limit=r['rank_daily_limit'],
                rape_flush_limit=r['rape_free_refreshes'],convert_fight_limit=r['convert_daily_limit'])
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
    visits=role['activity']['visits']
    out=[]
    for i,p in enumerate(r['visit_rewards'],1):
        state=visits.get(str(i),{})
        info=copy.deepcopy(state.get('prize_info',prize_spec(p)))
        out.append(dict(can_visit=True,has_visit=bool(state.get('claimed')),prize_info=info))
    return out


def feed_data(role,r):
    f=role['activity']['feed']
    return dict(feed_list=[role.get('feed_time'+str(i),2) if str(i) in f else 1 for i in (1,2)],
                feed_count=max((v['count'] for v in f.values()),default=0))


def statuses(role,now,r,flag):
    from .activity_land import status as land_status
    s=role['activity']
    if flag==0:
        from .activity_seasonal import status as seasonal_status
        return summon.event(47,dict(visit_list=visit_list(role,r),feed_data=feed_data(role,r),
                                   spring_info=dict(start_time=0,end_time=0),
                                   imperial_exam=dict(start_time=0,end_time=0),**seasonal_status(role,now,r)))
    require(flag==1,'未知活动页')
    return summon.event(48,dict(party_start_period=[dict(begin_seconds=r['party_period'][0],end_seconds=r['party_period'][1])],
        last_convert_type=s.get('last_convert_type',0),cur_fight_count=r['duty_daily_runs']-s['duty_runs'],
        max_fight_count=r['duty_daily_runs'],party_seld_order=1 if s['party_count'] else 0,
        party_free_count=r['party_free_count'],party_pay_count=r['party_paid_count'],prey_status_info=land_status(now,r)))


def feed(role,req,now,r):
    s=role['activity'];n=req['feed_count'];result=1;strength=0
    if n:
        require(1<=n<=r['feed_max_count'],'包子数量超出有效范围')
        second=(now+r['timezone_offset_hours']*3600)%86400
        slot=next((str(i) for i,(a,b) in enumerate(r['feed_periods'],1) if a<=second<b),None)
        if slot is None:result=3
        elif slot in s['feed']:result=4
        else:
            strength=min(r['feed_max_strength'],r['feed_base_strength']+n*r['feed_strength_per_bun'])
            role['strength']+=strength;s['feed'][slot]=dict(count=n,strength=strength)
            role['feed_time'+slot]=now;result=2
    data=feed_data(role,r)
    return [summon.event(43,dict(feed_result=result,server_time=now,strength=strength,
        feed_data=data,feed_time=[dict(begin_seconds=a,end_seconds=b) for a,b in r['feed_periods']],
        feed_champion=dict(name=role['role_name'] if data['feed_count'] else '',count=data['feed_count'])))]


def visit(role,req,r):
    i,op=req['visit_index'],req['op_type'];s=role['activity']['visits']
    if i:
        require(i in (1,2,3) and op in (1,2),'拜访参数无效')
        state=s.setdefault(str(i),{})
        require(not state.get('claimed'),'今日已拜访该仙人')
        if op==1 and not state:
            p=prize_spec(r['visit_rewards'][i-1])
            if i==1:
                cards=[secrets.choice(r['visit_fu_pool']) for _ in range(8)]
                state['reward']=cards[0]
                state['prize_info']=[dict(prize_spec(card),get_flag=j==0) for j,card in enumerate(cards)]
            elif i==2:
                dice=[secrets.randbelow(6)+1 for _ in range(3)]
                reward=copy.deepcopy(r['visit_rewards'][1]);reward[2]*=DICE_RATE.get(tuple(sorted(dice)),1)
                state['reward']=reward;state['prize_info']=dict(prize_spec(reward),form_type=dice,total_money=reward[2])
            else:state['prize_info']=p
        elif op==2:
            require('prize_info' in state,'请先开始拜访')
            prizes(role,[state.get('reward',r['visit_rewards'][i-1])]);state['claimed']=True
    return [summon.event(42,dict(visit_index=i,op_type=op,result=1,visit_list=visit_list(role,r)))]


def pray(role,req,r):
    require(role['level']>=15,'祈福需15级')
    index=role.get('pray_spirit_times',0)+1
    require(index in PRAY,'今日祈福次数已用完')
    rows=req['object_list'];require(len(rows)<=255,'祭品数量过多')
    seen=set();value=0;remove=[]
    for row in rows:
        typ,ident,n=row['object_type'],row['object_id'],row['count']
        require((typ,ident) not in seen and type(n)is int and n>0,'祭品重复或数量无效');seen.add((typ,ident))
        if typ==7:
            tid=int(ident);require(tid==ident and tid in formation.BASES,'未知魂魄')
            require(role.get('souls',{}).get(str(tid),0)>=n,'魂魄不足')
            role['souls'][str(tid)]-=n
            value += n*int(QUALITY[int(formation.BASES[tid]['quality'])]['spirit_worth'])
        else:
            require(typ==4 and n==1,'祭品类型无效')
            c=next((c for c in role['corteges'] if c['id']==ident),None)
            require(c is not None and not c.get('order') and not c.get('cheer_order') and not c.get('is_lock'),'该神仙不能献祭')
            require(not any(i.get('owner_id')==ident for i in role['attachments']),'请先卸下精魄')
            tid=c['type'];q=int(formation.BASES[tid]['quality'])
            require(q<=3,'只能献祭三星及以下神仙')
            remove.append(c);value += int(QUALITY[q]['cortage_worth'])
    value += role.get('spirit_retain',0)
    require(value>=PRAY[index],'祭品魂值不足')
    role['spirit_retain']=value-PRAY[index]
    role['corteges']=[c for c in role['corteges'] if c not in remove]
    role['pray_spirit_times']=index
    return [summon.event(52,dict(pray_item_list=prizes(role,[secrets.choice(r['pray_rewards'])])))]


def rank(role,r):
    s=role['activity'];order=s['rank_order']
    rows=[dict(id=10000+o,type=2,order=o,level=max(1,r['battle_level']),name='本地守榜者'+str(o),cortege=r['battle_npc'],cortege_layer=0,
               top_relation=2,combat_power=100) for o in sorted(set(max(1,order-v) for v in (1,2,5,10,20))) if o!=order]
    eligible=sum(1<<(i-2) for i,row in EXCHANGE.items() if int(row['promote_order']) and s.get('rank_reached_order',100000)<=int(row['promote_order']))
    claimed=sum(1<<(i-2) for i in s.get('rank_promotions',[]))
    return encode(1022,dict(need_update=True,self_order=order,self_score=s['rank_score'],promote_time=eligible,
             promote_prize=claimed,fight_count=max(0,r['rank_daily_limit']-s['rank_count']),show_count=len(rows),show_list=rows))


def rank_score(order,column):
    return next(int(row[column]) for row in RANK_SCORE if int(row['begin'])<=order<=int(row['end']))


def rape_board(role,now,r,update=1):
    s=role['activity']
    if s['rape_boards'] is None:
        s['rape_boards']=[dict(skill_type=tid,skill_count=1,form_list={'2':{str(i*10+j):dict(
            show_type=r['battle_npc'],level=r['battle_level'],name='本地渡劫守卫',has_win=False,top_order=0,cortege_layer=0)
            for j in range(1,4)}}) for i,tid in enumerate(r['rape_skills'],1)]
    boards=copy.deepcopy(s['rape_boards'])
    for b in boards:b['form_list']={int(t):{int(i):v for i,v in rows.items()} for t,rows in b['form_list'].items()}
    return dict(time=now,update_type=update,used_count=s['rape_refreshes'],free_count=r['rape_free_refreshes'],gold_cost=r['rape_refresh_gold'],rape_list=boards)


def duty_data(role,r,result=2):
    s=role['activity'];d=s.get('duty') or dict(round=1,stars=0,used=0,bonus=[0]*4)
    fields=[ENUMS['cortege_property'][k] for k in ('max_hp_rate','max_magic_rate','gongji_rate','fangyu_rate')]
    data=dict(result=result,cur_round=d['round'],max_fight_round=s['duty_best'],fight_count=r['duty_daily_runs']-s['duty_runs'],
        max_get_star=s['duty_best']*3,cur_get_star=d['stars'],cur_used_star=d['used'],expect_order=1,
        last_exchange_rate=10,
        plus_list=[dict(zip(fields,d['bonus'])),dict.fromkeys(fields,0)],
        lineup_list=[dict(type=r['battle_npc'],gold=0,stars=i) for i in (1,2,3)])
    if d.get('phase')=='exchange':
        data['star_exchange']=[dict(star=3,field=f,value=10) for f in fields]
    if d.get('pending_silver'):
        data['silver_prize']=[prize_spec([12,0,d['pending_silver'],1])]
    return data


def party_info(role,r):
    s=role['activity']
    return dict(self_damage=s['party_damage'],free_count=s['party_count'],pay_count=s['party_paid'],
        damage_list=[],self_order=1,plus_value=s['party_bonus']*10,plus_count=s['party_bonus'],
        peach_count=(s['party_count']+s['party_paid'])*5,lucky_point=0,
        fight_prize=[],boss_type=r['battle_npc'],boss_level=r['battle_level'],
        damage=0,total_damage=s['party_damage'],max_hp=10000000,cur_hp=max(0,10000000-s['party_damage']),name='本地蟠桃守卫')


def trial_state(role,r):
    s=role['activity']
    if s['trial'] is None and s['trial_spawned']<r['trial_bosses_per_day']:
        s['trial_spawned']+=1
        s['trial']=dict(type_id=r['battle_npc'],show_level=role['level'],name='本地试炼首领',
            hp=r['trial_boss_hp'],max_hp=r['trial_boss_hp'],is_dead=False,damage=0,
            prize_list=[prize_spec(p) for p in r['trial_rewards']])
    return s['trial']


def trial_query(role,req,now,r):
    s=role['activity'];boss=trial_state(role,r);flag=req['flag']
    require(flag in (1,2,3,4,5,6,7,9),'试炼操作无效')
    if flag==9:
        require(boss is not None and boss['is_dead'],'首领尚未击败或已领奖')
        gain=prizes(role,r['trial_rewards']);s['trial']=None
        return [summon.event(75,dict(flag=9,result=1,train_data=dict(prize=gain)))]
    if flag in (2,5):
        # Encounter generation is a local substitute for the missing server trigger.
        return [summon.event(75,dict(flag=2,result=1 if boss else 2,train_data=dict(
            boss_list=[boss] if boss else [],friend_damage_list=[],have_broad=False,
            last_train_time=s['trial_next'],train_times=s['trial_count'],day_max_train_num=r['trial_daily_limit'])))]
    if flag in (3,6):return [summon.event(75,dict(flag=flag,result=1,train_data=dict(friend_list=[])))]
    # No remote player or fabricated invitation is silently treated as real.
    require(flag==1,'离线存档中没有可邀请或接受的其他玩家')
    return [summon.event(75,dict(flag=1,result=5,train_data={}))]


def query_lineup(role,req,r):
    s=role['activity'];ident=req['des_id']
    own=ident==role['role_id']
    valid=own or req['des_type']==2 and (10000<ident<10000+s['rank_order'] or
        any(str(int(ident)) in b['form_list'].get('2',{}) for b in (s['rape_boards'] or [])))
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
    return [summon.event(11,data)]


def battle(role,req,now,r,jrules,frules):
    ft=req['fight_type'];s=role['activity'];target=None
    require(role['level']>={2:6,3:8,4:5,5:12,6:13,10:16,11:1}[ft],'等级不足')
    if ft==4:
        require(role['rule_index']<role['level']-4,'修炼次数已用完')
    elif ft==2:
        require(s['rank_count']<r['rank_daily_limit'],'今日封神榜次数已用完')
        target=req['des_value'];require(target in {max(1,s['rank_order']-v) for v in (1,2,5,10,20)} and target<s['rank_order'] and req['des_id']==10000+target and req['des_type']==2,'封神榜对手已变化')
        spend(role,'energy',1);s['rank_count']+=1
    elif ft==3:
        rape_board(role,now,r);idx=req['des_value']
        require(1<=idx<=3,'渡劫阵位无效')
        target=s['rape_boards'][idx-1]['form_list'].get(str(req['des_type']),{}).get(str(int(req['des_id'])))
        require(target is not None and not target['has_win'],'对手不存在或已击败');spend(role,'energy',1)
    elif ft==5:
        d=s.get('duty');require(d is not None and req['des_value']==d['round'] and req['des_type'] in (1,2,3),'请先开始天命之战')
        require(d['round']<=r['duty_round_limit'],'已完成本轮天命之战')
        require(d.get('phase')=='fight','请先完成祝福或领奖')
    elif ft==6:
        second=(now+r['timezone_offset_hours']*3600)%86400
        require(r['party_period'][0]<=second<r['party_period'][1],'蟠桃会尚未开放')
        require(req['des_value'] in (0,1),'蟠桃挑战类型无效')
        if req['des_value']==0:
            require(s['party_count']<r['party_free_count'],'免费挑战次数已用完')
            s['party_count']+=1
        else:
            require(s['party_paid']<r['party_paid_count'],'今日蟠桃会次数已用完')
            spend(role,'gold_coin',r['party_fight_gold']);s['party_paid']+=1
        role['party_fight_count']=s['party_count'];role['party_fight_count_plus']=s['party_paid']
    elif ft==10:
        require(role['convert_fight_count']<r['convert_daily_limit']+int(role.get('month_card_time',0)>now),'今日唤神次数已用完')
        require(req['des_value'] in CONVERT and any(c['type']==req['des_value'] for c in role['corteges']),'唤神来源无效')
        if role['convert_fight_count']>0:consume(role,r['convert_item'],1)
        role['convert_fight_count']+=1;role['convert_fight_time']=now
        s['last_convert_type']=req['des_value']
    elif ft==11:
        trial=trial_state(role,r)
        require(trial is not None and not trial['is_dead'] and req['des_value']==trial['type_id'],'试炼首领不存在或已击败')
        require(s['trial_count']<r['trial_daily_limit'] and now>=s['trial_next'],'试炼次数不足或正在冷却')
        s['trial_count']+=1;s['trial_next']=now+r['trial_cooldown_seconds']
    require(any(c.get('order') for c in role['corteges']),'请先上阵神仙')
    cfg=dict(cortege_list=f"{r['battle_npc']}|{r['battle_level']}")
    units=journey.fighters(role,cfg)
    if ft==5:
        for u in units[0]:
            for stat,bonus in zip(('hp','magic','gongji','fangyu'),s['duty']['bonus']):
                u[stat]=u[stat]*(100+bonus)//100
            u['max_hp']=u['hp']
        for u in units[1]:
            for stat in formation.STATS:u[stat]*=max(1,s['duty']['round']*req['des_type'])
            u['max_hp']=u['hp']
    if ft==6:
        for u in units[0]:u['gongji']=u['gongji']*(100+s['party_bonus']*10)//100
        units[1][0].update(hp=10000000,max_hp=10000000)
    if ft==11:units[1][0].update(hp=trial['hp'],max_hp=trial['max_hp'])
    result,lineup,actions=journey.battle(role,cfg,jrules,units=units);win=1<=result<=3
    events=[];s['fight_id']+=1;fid=s['fight_id']
    if ft==4 and win:
        role['rule_index']+=1
        for key,field,attr in [('hp','max_hp_plus',75),('gongji','gongji_plus',77),('fangyu','fangyu_plus',78),('magic','max_magic_plus',76)]:
            role[field]+=r['train_increase'][key];events.append(summon.event(5,dict(addition_field=attr,addition_value=r['train_increase'][key])))
    elif ft==2:
        score=rank_score(target,'score') if win else 0
        if win:s['rank_order']=target;s['rank_score']+=score;s['rank_reached_order']=target
        reward=dict(prize_spec([13,0,score,1]),flag=True)
        events += [rank(role,r),summon.event(33,[reward,dict(prize_spec([5,1001,1,1]),flag=False),
                                                 dict(prize_spec([12,0,r['battle_silver'],1]),flag=False)])]
    elif ft==3:
        if win:target['has_win']=True
        idx=req['des_value'];b=s['rape_boards'][idx-1];passed=all(v['has_win'] for rows in b['form_list'].values() for v in rows.values())
        if passed and win:journey.grant(role,(6,b['skill_type'],1,1))
        events.append(summon.event(41,dict(fight_result=result,form_index=idx,pass_one_form=passed,
            pass_all_form=all(all(v['has_win'] for rows in b['form_list'].values() for v in rows.values()) for b in s['rape_boards']),
            skill_count=1 if passed and win else 0,skill_type=b['skill_type'])))
    elif ft==5:
        d=s['duty']
        if win:
            d['round']+=1;d['stars']+=req['des_type'];s['duty_best']=max(s['duty_best'],d['round']-1)
            if d['round']%3==1:
                d['pending_silver']=3*r['duty_silver_per_round'];d['phase']='prize'
        else:d['phase']='finished'
        events.append(summon.event(19,duty_data(role,r,8 if win else 9)))
    elif ft==6:
        damage=sum(sum(a['damage_list']) for a in actions if a['is_src']);s['party_damage']+=damage
        info=party_info(role,r);info.update(fight_prize=prizes(role,r['party_rewards']),cur_damage=damage)
        events.append(summon.event(29,info))
    elif ft==10 and win:
        row=CONVERT[req['des_value']];col=next(k for k in row if k.startswith('output('))
        entries=[list(map(int,x.split('/'))) for x in row[col].split('|')];roll=secrets.randbelow(sum(x[2] for x in entries))
        typ,n,_=entries[-1]
        for t,c,w in entries:
            if roll<w:typ,n=t,c;break
            roll-=w
        tid=int(row['des_cortege_type']) if typ==2 else req['des_value']
        gain=prizes(role,[[5,r['convert_item'],n,1] if typ==3 else [7,tid,n,1]])
        # [A] cortCallUI indexes numeric {result_type,count} pairs; the first
        # pair is the settled reward, remaining pairs are the unchosen cards.
        cards=[[typ,n]]+[x[:2] for x in entries if x[:2]!=[typ,n]][:2]
        while len(cards)<3:cards.append([typ,n])
        events.append(summon.event(70,dict(prize_list=cards,attach_list=gain)))
    elif ft==11:
        damage=sum(sum(a['damage_list']) for a in actions if a['is_src'])
        trial['hp']=max(0,trial['hp']-damage);trial['is_dead']=trial['hp']==0
        trial['damage']+=damage
        events.append(summon.event(75,dict(flag=8,result=7 if trial['is_dead'] else 1,
            train_data=dict(prize=[],hp=trial['hp'],train_times=s['trial_count'],last_train_time=s['trial_next'],
                friend_damage_list=[dict(name=role['role_name'],damage=trial['damage'])]))))
    if win and ft in (2,3):role['silver_coin']+=r['battle_silver']
    return [encode(1028,dict(fight_id=fid,first_hand=1,des_name='本地活动对手',lineup_count=len(lineup),lineup=lineup)),
        encode(1027,dict(fight_id=fid,fight_type=ft,final_result=result,fight_round=len(actions),fight_result=actions))]+events+[
        summon.event(44,dict(fight_id=fid,fight_type=ft))]


def settle(role,mid,req,now,r,jrules,frules,parse):
    s=prepare(role,now,r)
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
    if mid==1205:return [statuses(role,now,r,req['flag'])]
    if mid==1040:return feed(role,req,now,r)
    if mid==1030:return visit(role,req,r)
    if mid==1085:return pray(role,req,r)
    if mid==1039:return query_lineup(role,req,r)
    if mid==1064:return trial_query(role,req,now,r)
    if mid==1026:return battle(role,req,now,r,jrules,frules)
    if mid==1203:
        cfg=EXCHANGE.get(req['exchange_type']);require(cfg is not None,'积分兑换项目无效')
        cost=int(cfg['score']);promotion=int(cfg['promote_order'])
        require(s['rank_score']>=cost,'积分不足')
        if promotion:
            claims=s.setdefault('rank_promotions',[])
            require(s['rank_order']<=promotion and req['exchange_type'] not in claims,'未达晋升名次或已领取')
            claims.append(req['exchange_type'])
        s['rank_score']-=cost
        spec=[[int(v) for v in x.split('|')]+[1] for x in cfg['prize_list(object_type|sub_type|count/...)'].split('/')]
        return [rank(role,r),summon.event(36,prizes(role,spec))]
    if mid==1072:
        require(role['level']>=25 or role.get('vip_level',0)>=5,'渡劫扫荡需25级或VIP5')
        rape_board(role,now,r)
        pending=[(i,t,int(ident),j) for i,b in enumerate(s['rape_boards'],1) for t,rows in b['form_list'].items()
                 for j,(ident,v) in enumerate(rows.items(),1) if not v['has_win']]
        require(pending and role['energy']>0,'没有可扫荡的对手或精力不足')
        pending=pending[:role['energy']]
        spend(role,'gold_coin',0 if role.get('vip_level',0)>=5 else len(pending))
        results=[]
        from .protocol import decode
        for idx,t,ident,j in pending:
            output=battle(role,dict(fight_type=3,des_value=idx,des_type=int(t),des_id=ident),now,r,jrules,frules)
            for packet in output:
                m,_,data=decode(packet)
                if m==2998 and data['id']==41:
                    result=parse(data['data']);result['index']=j;results.append(result)
        data={i:v for i,v in enumerate(results,1)}
        data['pass_all_form']=all(all(v['has_win'] for rows in b['form_list'].values() for v in rows.values()) for b in s['rape_boards'])
        return [summon.event(114,data)]
    if mid==1021:
        require(role['level']>=6,'封神榜需6级');return [rank(role,r)]
    if mid==1029:
        require(role['level']>=8 and req['flag'] in (1,2,3),'渡劫请求无效')
        if req['flag']!=1:
            if req['flag']==2:require(s['rape_refreshes']<r['rape_free_refreshes'],'免费刷新次数已用完')
            else:spend(role,'gold_coin',r['rape_refresh_gold'])
            s['rape_refreshes']+=1;s['rape_boards']=None
        return [summon.event(40,rape_board(role,now,r,req['flag']))]
    if mid==1041:
        require(role['level']>=8,'渡劫需8级');rape_board(role,now,r)
        idx=req['form_index'];require(1<=idx<=3,'阵位无效')
        rows=s['rape_boards'][idx-1]['form_list'].get(str(req['object_type']),{})
        old=rows.get(str(int(req['object_id'])));require(old is not None and not old['has_win'],'不可刷新该对手')
        spend(role,'gold_coin',r['rape_single_refresh_gold']);new=copy.deepcopy(old)
        nid=max(map(int,rows))+1;del rows[str(int(req['object_id']))];rows[str(nid)]=new
        return [summon.event(40,dict(update_type=5,form_index=idx,old_type=req['object_type'],old_id=req['object_id'],
            new_type=req['object_type'],new_id=nid,new_show_type=new['show_type'],new_top_order=0,new_level=new['level'],new_name=new['name'],cortege_layer=0))]
    if mid==1043:
        require(role['level']>=12,'天命之战需12级');op=req['plus_type']
        if op==0:
            if s['duty'] is None or s['duty'].get('phase')=='finished':
                if req['flag']==1:return [summon.event(19,duty_data(role,r,2 if s['duty_runs']<r['duty_daily_runs'] else 7))]
                require(s['duty_runs']<r['duty_daily_runs'],'今日天命之战次数已用完')
                s['duty_runs']+=1;s['duty']=dict(round=1,stars=0,used=0,bonus=[0]*4,phase='initial')
            return [summon.event(19,duty_data(role,r,1 if s['duty']['phase']=='initial' else 5 if s['duty']['phase']=='exchange' else 3))]
        require(s['duty'] is not None,'请先开始天命之战');d=s['duty']
        if op in (1,2):
            idx=req['plus_index'];require(1<=idx<=4,'加成无效')
            if op==1:require(d.get('phase')=='initial','初始祝福已选择')
            else:
                require(d.get('phase')=='exchange' and d['stars']-d['used']>=3,'星数不足或尚未到献祭轮次')
                d['used']+=3
            d['bonus'][idx-1]+=10;d['phase']='fight'
            return [summon.event(19,duty_data(role,r,3))]
        if op==3:
            require(d.get('pending_silver',0)>0,'暂无可领取奖励')
            prizes(role,[[12,0,d.pop('pending_silver'),1]])
            d['phase']='exchange' if d['round']<=r['duty_round_limit'] else 'finished'
            return [summon.event(19,duty_data(role,r,5 if d['phase']=='exchange' else 2))]
        require(op in (4,5),'天命操作无效');require(s['duty_runs']<r['duty_daily_runs'],'今日天命之战次数已用完')
        require(d.get('phase')=='finished','本轮挑战尚未结束')
        s['duty_runs']+=1;s['duty']=dict(round=max(1,s['duty_best']//2) if op==5 else 1,stars=0,used=0,bonus=[0]*4,phase='initial')
        return [summon.event(19,duty_data(role,r,1))]
    if mid==1049:
        typ=req['query_type'];require(1<=typ<=5,'未知排行查询')
        if typ==1:return [summon.event(29,party_info(role,r))]
        if typ==2:return [summon.event(30,dict(damage_list=[],top_list=[],self_damage_his=s['party_damage'],self_order=1,
            fight_count=s['party_count']+s['party_paid'],peach_count=(s['party_count']+s['party_paid'])*5,lucky_point=0,felstar_info={}))]
        if typ==3:return [summon.event(28,dict(lucky_list=[],self_lucky=0,self_lucky_his=0,self_order=0))]
        if typ==4:return [summon.event(39,dict(all_top_list={i:[] for i in range(4,9)},duty_group=min(8,max(4,role['cortege_count'])),expect_order=0,max_get_star=s['duty_best']*3,max_fight_round=s['duty_best']))]
        require(not s.get('praised'),'今日已点赞');s['praised']=True
        return [summon.event(141,dict(attach_list=prizes(role,[[12,0,1000,1]])))]
    if mid==1202:
        require(role['level']>=13 and s['party_bonus']<r['party_bonus_limit'],'蟠桃加成已达上限')
        spend(role,'gold_coin',r['party_bonus_gold']*(s['party_bonus']+1));s['party_bonus']+=1
        role['gongji_plus_rate']=s['party_bonus']*10
        return [summon.event(32,{})]
    if mid==1201:
        if req['flag']==2:
            require(s['rank_count']>0 and not s['rank_claimed'],'尚未参战或今日已领奖')
            score=rank_score(s['rank_order'],'day_score')
            s['rank_claimed']=True;s['rank_score']+=score;role['top_day_prize_time']=now
            return [rank(role,r),summon.event(34,dict(attach_count=score))]
        require(req['flag']==1 and s['party_count']+s['party_paid']>0 and not s['party_claimed'],'暂无可领取的蟠桃奖励')
        s['party_claimed']=True
        role['party_take_prize']=1
        return [summon.event(31,dict(attach_list=prizes(role,r['party_rewards'])))]
    raise formation.Rejected('活动操作参数无效')


def attributes(role):
    fields = {7:'silver_coin',8:'gold_coin',101:'strength',102:'energy',20:'pray_spirit_times',
              73:'rule_index',75:'max_hp_plus',76:'max_magic_plus',77:'gongji_plus',78:'fangyu_plus',
              48:'convert_fight_limit',49:'convert_fight_count',50:'convert_fight_time',
              61:'top_fight_limit',62:'rape_flush_limit',112:'party_fight_count',113:'party_fight_count_plus',
              132:'top_day_prize_time',30:'role_combat_power',10:'spirit_retain',85:'gongji_plus_rate',124:'party_take_prize'}
    role['top_score']=role['activity']['rank_score'];role['top_order']=role['activity']['rank_order']
    fields.update({582:'drug_level',583:'drug_exp',584:'drug_study_flag',585:'drug_study_flag2',614:'hole_hp_plus',131:'top_score',3:'level',5:'cur_exp',6:'next_exp'})
    for i,key in enumerate(('gongji','fangyu','fashang','fakang'),1):
        name='train_'+key+'_index';fields[615+i]=name
        role[name]=role['activity'].get('home',{}).get('train',{}).get(str(i),{}).get('level',0)
    attrs=[dict(type=t,value=int(role.get(k,0))) for t,k in fields.items()]
    return [encode(1032,dict(id=role['role_id'],unit_type=1,attr_count=len(attrs),attr_list=attrs))]
