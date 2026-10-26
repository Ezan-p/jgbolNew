"""名人山: original event 130 and five destinations [A], offline standings [B]."""
import copy
import json
from pathlib import Path
from . import activity, daily, formation, guild, guild_match, journey, summon
from .protocol import encode
ROOT=Path(__file__).resolve().parents[1]
ENUMS=activity.ENUMS
CONSTS=ENUMS['const_def']
ATTRS={k:v for k,v in ENUMS['role_property'].items() if k.startswith('single_') or k in ('win_streak_count','max_win_streak_count')}


def load_rules(path=ROOT/'server_config/monument_rules.json'):
    r=json.loads(Path(path).read_text())
    formation.require(r['mode']=='inferred','名人山配置来源无效')
    for key in ('cross_min_level','battle_npc','battle_level','win_score','lose_score','challenge_gold','flush_gold'):
        formation.require(type(r[key]) is int and 0<r[key]<=100000,'名人山数值无效: '+key)
    formation.require(r['battle_npc'] in summon.BASES,'名人山模型无效')
    formation.require(len(r['npc_scores'])==5 and all(type(v) is int and 0<=v<=1000000 for v in r['npc_scores']),'名人山榜单无效')
    formation.require(type(r['timezone_offset_hours']) is int and -12<=r['timezone_offset_hours']<=14,'名人山时区无效')
    formation.require(len(r['phase_seconds'])==4 and r['phase_seconds']==sorted(set(r['phase_seconds'])) and r['phase_seconds'][0]==0 and r['phase_seconds'][-1]==86400,'论道赛程配置无效')
    for n,ps in r['streak_prizes'].items():
        formation.require(str(int(n))==n and 0<int(n)<=25 and bool(ps),'连胜奖励无效')
        for p in ps:daily.validate_prize(p)
    return r


def prepare(role,now,r):
    s=role.setdefault('monument',{})
    day=daily.day(now,r)
    for k in ATTRS:role.setdefault(k,0)
    if s.get('day')!=day:
        if 'day' in s:
            s['previous_champion']=copy.deepcopy(standings(role,r)[0])
        s.update(day=day,streak_claimed=[],rank_claimed=False,fights=0,records=[],refresh=0)
        for k in ('single_free_challenge','single_charge_challenge','single_free_flush_count','single_charge_flush_count','win_streak_count','max_win_streak_count'):
            role[k]=0
        role['single_next_flush_time']=now
    current_phase=phase(now,r)
    if s.get('phase')!=current_phase:
        s['phase']=current_phase
        role['single_free_challenge']=role['single_charge_challenge']=0
    role['single_rank']=next(x['rank'] for x in standings(role,r) if x['player_id']==role['role_id'])
    return s


def avatar(role):
    c=next((c for c in role['corteges'] if c.get('order')==1),role['corteges'][0])
    return dict(show_type=c['type'],cortege_layer=c.get('evolve_level',0))


def standings(role,r):
    rows=[dict(player_id=92001+i,name='离线论道者'+str(i+1),area='本地模拟区',score=v,show_type=r['battle_npc'],cortege_layer=0) for i,v in enumerate(r['npc_scores'])]
    rows.append(dict(player_id=role['role_id'],name=role['role_name'],area='本地区',score=role.get('single_score',0),**avatar(role)))
    rows.sort(key=lambda v:(-v['score'],v['player_id']))
    for i,v in enumerate(rows,1):v.update(rank=i,win_score=r['win_score'],tao_point=role.get('tao_point',0) if v['player_id']==role['role_id'] else 0)
    return rows


def phase(now,r):
    second=(now+r['timezone_offset_hours']*3600)%86400
    return 1 if second<r['phase_seconds'][1] else 2 if second<r['phase_seconds'][2] else 3


def client_config(now,r):
    start=daily.day(now,r)*86400-r['timezone_offset_hours']*3600
    # [B] Daily schedule; original client computes normal/king/paid stages [A].
    return dict(begin_fight_time=start,end_fight_time=start+86399,start_kingfight_time=start+r['phase_seconds'][1],
                start_chargefight_time=start+r['phase_seconds'][2],single_next_flush_time=now,
                single_free_chanllenge_limit=CONSTS['single_free_chanllenge_limit'],
                single_charge_chanllenge_limit=CONSTS['single_charge_chanllenge_limit'],
                single_free_flush_limit=CONSTS['single_free_flush_limit'])


def match_info(role,now,r):
    s=prepare(role,now,r);rows=standings(role,r)
    enemies=[x for x in rows if x['player_id']!=role['role_id']]
    offset=s['refresh']%len(enemies);enemies=enemies[offset:]+enemies[:offset]
    return dict(top1=rows[0],top2=rows[1],top3=rows[2],enemy=enemies[:3] if phase(now,r)==1 else enemies,
                has_qulify=role['level']>=r['cross_min_level'],next_flush_cost=r['flush_gold'],
                next_challenge_cost=r['challenge_gold'] if phase(now,r)==1 else CONSTS['king_fight_charge_cost'] if phase(now,r)==2 else CONSTS['allcharge_fight_cost'],can_take_rank_prize=s['fights']>0 and not s['rank_claimed'])


def champions(role,now,r,grules,arules):
    prepare(role,now,r);activity.prepare(role,now,arules)
    s,g=guild.prepare(role,now,grules)
    # Use one existing public guild as the spectator reference, never join on query.
    g=g or min(s['unions'].values(),key=lambda v:v['id'])
    result={}
    for kind,cross in ((3,False),(4,True)):
        winner=guild_match.tournament(role,s,g,grules,cross)[0]
        leader=next((m for m in g['members'].values() if m['rank']==1),None)
        own=winner['id']==g['id'] and leader and leader['id']==role['role_id']
        result[kind]=dict(name=winner['name'],show_type=r['battle_npc'],cortege_layer=0)
        if own:result[kind].update(avatar(role))
    from . import activity_rank
    if role['activity']['rank_order']==1:
        result[1]=dict(name=role['role_name'],**avatar(role))
    else:
        champion=activity_rank.opponent(role['activity'],1)
        result[1]=dict(name=champion['name'],show_type=champion['cortege'],cortege_layer=champion['cortege_layer'])
    result[2]=copy.deepcopy(standings(role,r)[0])
    from . import guild_feast
    stats=guild_feast.ranking(role,s,now,grules)['fortune_info']
    if stats:
        v=min(stats,key=lambda v:(-v['fortune'],-v['contribute'],v['id']))
        result[5]=dict(name=v['name'],show_type=r['battle_npc'],cortege_layer=0)
        if v['id']==role['role_id']:result[5].update(avatar(role))
    else:result[5]=dict(name='虚位以待')
    return dict(champion_list=result)


def handles(mid,d):
    return mid in (1128,1231,1232,1233,1234,1235,1236,1238) or mid==1026 and d['fight_type']==18 or mid==1244 and d['fight_type']==3 or mid==1039 and 92001<=d['des_id']<=92005


def attributes(role):
    rows=[dict(type=v,value=role.get(k,0)) for k,v in ATTRS.items()]
    rows += [dict(type=8,value=role['gold_coin']),dict(type=7,value=role['silver_coin'])]
    return encode(1032,dict(id=role['role_id'],unit_type=1,attr_count=len(rows),attr_list=rows))


def rank_prizes(rank):
    rows=[{k.split('(')[0]:v for k,v in row.items()} for row in summon.rows('rank_prize.csv')]
    row=max((v for v in rows if int(v['min_order'])<=rank),key=lambda v:int(v['min_order']))
    # [A] data.getItemListFromStr reads object/type/level/count.
    return [[a,b,d,c] for a,b,c,d in (map(int,p.split('|')) for p in row['prize'].split('/'))]


def settle(role,mid,d,now,r,grules,arules,jrules):
    s=prepare(role,now,r)
    if mid==1128:return [summon.event(130,champions(role,now,r,grules,arules))]
    cfg=summon.event(80,{19:client_config(now,r)})
    if mid==1232:return [cfg,summon.event(100,match_info(role,now,r))]
    if mid==1236:
        rows=[dict(player_id=v['player_id'],player_name=v['name'],rank=v['rank'],score=v['score'],area=v['area']) for v in standings(role,r)]
        return [encode(1237,dict(top_count=len(rows),top_list=rows))]
    if mid in (1039,1233):
        ident=d['des_id'];formation.require(ident==role['role_id'] or 92001<=ident<=92005,'论道目标不存在')
        data=guild_match.lineup(role,ident,r);data['role_name']=next(v['name'] for v in standings(role,r) if v['player_id']==ident)
        return [summon.event(11 if mid==1039 else 101,data)]
    if mid==1231:return [summon.event(104,dict(prize_info={int(n):[daily.spec(p) for p in ps] for n,ps in r['streak_prizes'].items()},got_prize={n:True for n in s['streak_claimed']}))]
    if mid==1244:
        return record_packets(s)
    formation.require(role['level']>=r['cross_min_level'],'未达到跨服论道等级')
    if mid==1234:
        formation.require(d['is_charge'] in (0,1),'刷新参数无效')
        if d['is_charge']:
            guild.pay(role,'gold_coin',r['flush_gold']);role['single_charge_flush_count']+=1;role['single_charge_flush_time']=now
        else:
            formation.require(role['single_free_flush_count']<CONSTS['single_free_flush_limit'] and now>=role['single_next_flush_time'],'免费刷新次数不足或冷却中')
            role['single_free_flush_count']+=1;role['single_next_flush_time']=now+CONSTS['single_free_flush_interval']
        s['refresh']+=1
        return [cfg,summon.event(102,match_info(role,now,r))]
    if mid==1235:
        n=d['streak_count'];formation.require(str(n) in r['streak_prizes'] and n<=role['max_win_streak_count'] and n not in s['streak_claimed'],'连胜不足或奖励已领取')
        ps=[journey.grant(role,p) for p in r['streak_prizes'][str(n)]];s['streak_claimed'].append(n)
        return [summon.event(103,dict(streak_count=n,prize_info=ps))]
    if mid==1238:
        formation.require(s['fights']>0 and not s['rank_claimed'],'尚未参战或今日奖励已领取')
        rank=role['single_rank'];ps=[journey.grant(role,p) for p in rank_prizes(rank)];s['rank_claimed']=True
        return [summon.event(128,dict(rank=rank,prize_info=ps))]
    if mid==1026:
        valid={x['player_id']:x for x in match_info(role,now,r)['enemy']}
        formation.require(d['des_id'] in valid,'对手已刷新，请重新选择')
        formation.require(d['des_value'] in (0,1),'挑战付费参数无效')
        formation.require(d['des_type']==valid[d['des_id']]['rank'],'对手排名已变化')
        if d['des_value']==0:
            formation.require(phase(now,r)!=3,'当前阶段仅能付费挑战')
            limit=CONSTS['single_free_chanllenge_limit'] if phase(now,r)==1 else CONSTS['king_free_challenge_limit']
            formation.require(role['single_free_challenge']<limit,'免费挑战次数已用完');role['single_free_challenge']+=1
        else:
            limit=CONSTS['single_charge_chanllenge_limit'] if phase(now,r)==1 else CONSTS['king_charge_challenge_limit']
            formation.require(role['single_charge_challenge']<limit,'付费挑战次数已用完')
            guild.pay(role,'gold_coin',match_info(role,now,r)['next_challenge_cost']);role['single_charge_challenge']+=1
        from .guild_combat import simulate
        target=valid[d['des_id']];result,packets,replay=simulate(role,s,r,jrules,18,target['name'])
        win=1<=result<=3;gain=r['win_score'] if win else r['lose_score']
        role['single_score']+=gain;role['win_streak_count']=role['win_streak_count']+1 if win else 0
        role['max_win_streak_count']=max(role['max_win_streak_count'],role['win_streak_count']);role['single_last_challenge_time']=now
        s['fights']+=1;s['records']=(s['records']+[dict(replay,time=now,name=target['name'],src_name=role['role_name'],vip_level=role.get('vip_level',0),tao_point=role.get('tao_point',0),role_combat_power=role.get('role_combat_power',0))])[-5:]
        prepare(role,now,r)
        return packets+[summon.event(105,dict(add_score=gain,prize_list=[])),summon.event(44,dict(fight_id=s['fight_id'],fight_type=18))]
    raise formation.Rejected('名人山操作无效')


def record_packets(s):
    # [A] event 152 accumulates records; event 44/118 opens the record page.
    from .guild_combat import recent_records
    rows=[]
    for v in recent_records(s['records']):
        info=dict(name=v['src_name'],vip_level=v['vip_level'],tao_point=v['tao_point'],role_combat_power=v['role_combat_power'])
        rows.append(dict(final_result=v['fight_result_msg']['final_result'],fight_data=dict(
            src_info=info,des_info=dict(name=v['name']),logtime=v['time'],
            lineup_list=v['line_up_msg']['lineup'],result_list=v['fight_result_msg']['fight_result'],
            elite_logic={int(k) if str(k).isdigit() else k:value for k,value in v['fight_events'].items()})))
    records={i:v for i,v in enumerate(rows,1)}
    return [summon.event(152,dict(fight_type=118,records=records)),summon.event(44,dict(fight_type=118))]


def weekly_html():
    # Public page contains no account, credential or private save data.
    return ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>名人山周刊</title><body><h1>名人山·本地周刊</h1><p>【B】离线模拟版，非原服历史新闻。</p>'
            '<p>名人山展示跨服仙盟战、仙盟战、财富榜、封神榜、跨服论道五类荣誉。冠军与榜单按本地存档更新。</p>'
            '<p>财富榜尚无人参与时显示“虚位以待”；在仙盟宴席赠礼后可查看记录。未加入仙盟也可浏览公开赛程。</p>'
            '<p>跨服论道采用每日模拟赛事，免费挑战和刷新额度沿用原版常量，奖励与离线规则详见项目名人山规则文档。</p>'
            '<p>关闭此窗口返回游戏。</p></body></html>').encode('utf-8')
