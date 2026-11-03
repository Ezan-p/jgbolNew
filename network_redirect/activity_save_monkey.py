"""1346 / event 197. Native client mechanics [A]; missing economy/lifecycle [B].

Wire pos_info.x is vertical (inner grid index), y is horizontal (outer index).
Keep the original transposition; never accept client rewards or map contents.
"""
import copy
import csv
import json
import secrets
from pathlib import Path

from . import activity as a, daily, formation, summon, welfare

ROOT = Path(__file__).resolve().parents[1]
TOOLS = (1350, 1351, 1352, 1354)
MONKEYS = {1355: (2, [11, 0, 8, 1]), 1356: (1, [5, 10000, 10, 1])}


with (ROOT / 'analysis/configs/save_monkey/assist_shop_config.csv').open(newline='') as source:
    ASSIST = {int(row['index']): dict(consume=list(map(int,row['consume'].split('|'))),
        prizes=[list(map(int,p.split('|'))) for p in row['target_item'].split('/')])
        for row in csv.DictReader(source)}


def load_rules(path=ROOT / 'server_config/save_monkey_rules.json'):
    r = json.loads(Path(path).read_text())
    a.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
              and isinstance(r.get('revision'), str) and r['revision'], '救悟空配置来源无效')
    a.require(type(r.get('enabled')) is bool, '救悟空开关无效')
    for key, low, high in [('period_days', 1, 365), ('width', 8, 8), ('height', 6, 6),
                           ('piece_per_stone', 1, 100), ('granite_percent', 0, 20), ('hard_stone_percent', 0, 50), ('charge_tool_rmb', 1, 10000)]:
        a.require(type(r.get(key)) is int and low <= r[key] <= high, '救悟空配置无效：'+key)
    def prizes(values):
        a.require(isinstance(values, list) and 1 <= len(values) <= 10, '救悟空奖励缺失')
        for p in values:
            daily.validate_prize(p)
            a.require(p[0] == 5 and p[1] in formation.ITEMS and p[3] == 1, '救悟空物品无效')
    prizes(r['starter'])
    prizes(r['daily_login']); prizes(r['charge_tools'])
    a.require(all(p[1] in TOOLS for p in r['starter']), '初始宝珠配置无效')
    weights = r['contents']
    a.require(isinstance(weights, list) and len(weights) == 7 and
              {v[0] for v in weights} == {0,1350,1351,1352,1353,1355,1356} and
              all(type(v[1]) is int and 0 < v[1] <= 100 for v in weights) and
              sum(v[1] for v in weights) == 100, '救悟空地图权重无效')
    for key in ('point_prizes', 'score_prizes'):
        rows = r[key]
        a.require(isinstance(rows, list) and 1 <= len(rows) <= 5, '救悟空档位无效')
        last = 0
        for row in rows:
            a.require(type(row['point']) is int and last < row['point'] <= 10000, '救悟空门槛无效')
            last = row['point']; prizes(row['prizes'])
            if key == 'score_prizes':
                a.require(all(type(row[k]) is int and 1 <= row[k] <= 10000
                              for k in ('charge_rmb', 'cards')), '救悟空充值特权无效')
    a.require(r['point_prizes'][-1]['point'] <= sum(t['limit'] for t in daily.load_rules()['tasks']),
              '救悟空活跃度无法达成')
    a.require(isinstance(r['shop'], list) and 1 <= len(r['shop']) <= 20, '碎石商店无效')
    for row in r['shop']:
        a.require(all(type(row[k]) is int and 1 <= row[k] <= 10000 for k in ('piece','limit')), '碎石商品无效')
        prizes([row['prize']])
    return r


def period(now, r):
    # Monday 00:00 UTC+8 for the default seven-day period [B].
    anchor = 4*86400 - 8*3600
    start = (now-anchor)//(r['period_days']*86400)*(r['period_days']*86400)+anchor
    return start, start+r['period_days']*86400


def status(now, r=None, role=None):
    r = r or load_rules(); start, end = period(now, r)
    data=dict(start_time=start-1, end_time=end, local_enabled=r['enabled'])
    s=(role or {}).get('activity',{}).get('save_monkey')
    if s and s['start']==start:
        data.update(score_charge=s['charge_gold']//10,
            score_prize_list=prize_rows(s,r['score_prizes'],s['score_claimed'],s['score'],True))
    return data


def cell(r, column, depth):
    if depth == 0:
        return dict(strength=0, stone_type=1, content=0)
    # A clear central route prevents an unbreakable granite wall [B].
    granite = column != r['width']//2 and secrets.randbelow(100) < r['granite_percent']
    value = secrets.randbelow(100); content = 0
    for tid, weight in r['contents']:
        value -= weight
        if value < 0:
            content = tid; break
    hard = not granite and secrets.randbelow(100) < r['hard_stone_percent']
    return dict(strength=2 if hard else 1, stone_type=3 if granite else 2 if hard else 1, content=0 if granite else content)


def state(role, now, r):
    old = role.setdefault('activity', {}).get('save_monkey')
    a.require(not old or now >= old['last_time'], '救悟空时钟已回退，请恢复本地时间')
    start, end = period(now, r)
    if not old or old['start'] != start:
        old = dict(start=start, end=end, last_time=now, deep=0, show_deep=-1,
                   score=0, piece=0, charge_gold=0, score_claimed=[], charge_claimed=[],
                   bought={}, token=secrets.token_hex(16), starter=False, charge_tool_batches=0,
                   grid=[[cell(r, col, dep) for dep in range(r['height'])] for col in range(r['width'])])
        role['activity']['save_monkey'] = old
    old['last_time'] = now
    day = (now+8*3600)//86400
    if old.get('day') != day:
        old.update(day=day, point_claimed=[], login_claimed=False, token=secrets.token_hex(16))
    return old


def deliver_charge(role, s, now, r):
    for i, row in enumerate(r['score_prizes'], 1):
        if i in s['charge_claimed'] or s['score'] < row['point'] or s['charge_gold'] < row['charge_rmb']*10:
            continue
        mails = welfare.prepare(role, now, welfare.load_rules()).setdefault('mails', {})
        key = f"save-monkey:{s['start']}:{i}"
        if key not in mails:
            identity = max([800000000]+[m['mail_id'] for m in mails.values()])+1
            mails[key] = dict(mail_id=identity, mail_title='十万猴急充值特权',
                mail_body='拯救积分与累计充值已达标，道尊金卡请查收。', recv_time=now,
                send_time=now, prizes=[[5,1151,row['cards'],1]], claimed=False)
        s['charge_claimed'].append(i)


def record_charge(role, principal, now, source_item=None):
    r = load_rules()
    if not r['enabled'] or source_item == 1151 or principal <= 0:
        return
    s = state(role, now, r)
    s['charge_gold'] += principal
    batches=s['charge_gold']//(r['charge_tool_rmb']*10)
    count=batches-s['charge_tool_batches']
    if count:
        rewards=copy.deepcopy(r['charge_tools'])
        for p in rewards: p[2]*=count
        a.prizes(role,rewards);s['charge_tool_batches']=batches
    deliver_charge(role, s, now, r)


def adjacent(x, y, radius=1):
    return [(x+dx, y+dy) for dx in range(-radius, radius+1)
            for dy in range(-radius, radius+1) if dx or dy]


def in_grid(s, x, y):
    return 0 <= x < len(s['grid']) and 0 <= y < len(s['grid'][x])


def usable(s, x, y, tid):
    if not in_grid(s, x, y): return False
    g = s['grid']; current = g[x][y]
    destroyable = lambda i,j: in_grid(s,i,j) and g[i][j]['strength'] > 0 and g[i][j]['stone_type'] != 3
    if tid == 1350:
        return destroyable(x,y) and any(in_grid(s,i,j) and g[i][j]['strength'] == 0
            for i,j in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
    if tid == 1351:
        return current['strength'] == 0 and any(destroyable(i,j) for i,j in adjacent(x,y))
    if tid == 1352:
        return any(destroyable(i,j) for i,j in ((x,y),(x+1,y),(x,y+1),(x+1,y+1)))
    return False


def use(role, s, d, r):
    tid = d['item_type']
    a.require(type(tid) is int and tid in TOOLS, '宝珠类型无效')
    if tid == 1354:
        a.require(set(d) == {'item_type','local_token'}, '火眼金睛参数无效')
        a.require(s['show_deep'] < s['deep'], '火眼金睛正在使用中')
        a.consume(role, tid, 1)
        s['show_deep'] = s['deep']+29  # Thirty absolute depth rows, including the current top row [B endpoint].
        return [], []
    a.require(set(d) == {'item_type','pos_info','local_token'} and isinstance(d['pos_info'],dict), '宝珠位置无效')
    pos = d['pos_info']
    a.require(set(pos) == {'x','y'} and all(type(v) is int for v in pos.values()), '宝珠位置无效')
    x,y = pos['y']-1, pos['x']-1
    a.require(usable(s,x,y,tid), '使用位置不正确，花岗岩不可破坏')
    a.consume(role,tid,1)
    pending = [(x,y)] if tid == 1350 else (adjacent(x,y) if tid == 1351 else [(x,y),(x+1,y),(x,y+1),(x+1,y+1)])
    rewards=[]; bombs=[]; hit=set()
    while pending:
        cx,cy = pending.pop()
        if not in_grid(s,cx,cy): continue
        c=s['grid'][cx][cy]
        if not c['strength'] or c['stone_type']==3 or (cx,cy) in hit: continue
        hit.add((cx,cy));c['strength']-=1
        if c['strength']: continue
        s['piece'] += r['piece_per_stone']
        content=c['content']; c['content']=0
        if content==1353:
            bombs.append(dict(x=cx+1,y=cy+1))
            # Missing server geometry: Chebyshev radius two, clipped to window [B].
            pending.extend(adjacent(cx,cy,2))
        elif content in MONKEYS:
            score, prize=MONKEYS[content];s['score']+=score;rewards.append(prize)
        elif content:
            rewards.append([5,content,1,1])
    # Move only one row per action; the native checkFade animates one row [B].
    if all(c[1]['strength']==0 or c[1]['stone_type']==3 for c in s['grid']):
        for col, cells in enumerate(s['grid']):
            cells.pop(0);cells.append(cell(r,col,s['deep']+r['height']))
        s['deep']+=1
    return a.prizes(role,rewards), bombs


def prize_rows(s, rows, claimed, total, charge=False):
    result=[]
    for i,row in enumerate(rows,1):
        v=dict(point=row['point'], status=3 if i in claimed else 2 if total>=row['point'] else 1,
               prize_list=[a.prize_spec(p) for p in row['prizes']])
        if charge:
            v['charge_data']=dict(point=row['charge_rmb'], status=3 if i in s['charge_claimed'] else 2 if total>=row['point'] else 1,
                                  prize_list=[a.prize_spec([5,1151,row['cards'],1])])
        result.append(v)
    return result


def response(role,s,now,r,op,prizes=None,extra=None):
    dr=daily.load_rules(); ds=daily.prepare(role,now,dr)
    boxes=prize_rows(s,r['point_prizes'],s['point_claimed'],ds['total'])
    grid=copy.deepcopy(s['grid'])
    for x,col in enumerate(grid):
        for y,c in enumerate(col):
            content=c.pop('content')
            visible=s['deep']+y<=s['show_deep'] or any(in_grid(s,i,j) and s['grid'][i][j]['strength']==0 for i,j in adjacent(x,y))
            if content and visible: c['item']=a.prize_spec([5,content,1,1])
    data=dict(id=op,result=1,grid_conf=grid,deep=s['deep'],show_deep=s['show_deep'],score=s['score'],
        piece=s['piece'],score_charge=s['charge_gold']//10,
        score_prize_list=prize_rows(s,r['score_prizes'],s['score_claimed'],s['score'],True),
        point_prize_flag=any(b['status']==2 for b in boxes),
        point=ds['total'],point_prize=boxes,
        point_data=[dict(desc=t['desc'],cur_point=ds['points'].get(str(t['id']),0),point_limit=t['limit']) for t in dr['tasks']],
        shop_list=[dict(piece=row['piece'],left_times=row['limit']-s['bought'].get(str(i),0),
                        item=a.prize_spec(row['prize'])) for i,row in enumerate(r['shop'],1)],
        prize_list=prizes or [],qibaofu_list=[],local_token=s['token'],local_activity=status(now,r),
        local_assist=ASSIST,local_reset_time=min(s['end'],(s['day']+1)*86400-8*3600))
    if extra: data.update(extra)
    return summon.event(197,data)


def settle(role,req,now,parse):
    r=load_rules();a.require(r['enabled'],'十万猴急活动未开放')
    op=req['id'];d=parse(req['data'])
    a.require(type(op) is int and op in (1,2,3,4,5,6,7,9) and isinstance(d,dict), '救悟空操作无效')
    s=state(role,now,r);reward=[];extra={}
    if op in (1,4,6):
        a.require(not d,'救悟空查询参数无效')
        if op==1 and not s['starter']:
            reward=a.prizes(role,r['starter']);s['starter']=True
        if op==1 and not s['login_claimed']:
            reward+=a.prizes(role,r['daily_login']);s['login_claimed']=True
    else:
        a.require(d.get('local_token')==s['token'],'救悟空进度已变化，请重新进入活动')
        if op==2:
            reward,bombs=use(role,s,d,r);extra=dict(item_type=d['item_type'],qibaofu_list=bombs)
        elif op in (3,7):
            a.require(set(d)=={'prize_id','local_token'} and type(d['prize_id']) is int, '礼包编号无效')
            rows=r['score_prizes'] if op==3 else r['point_prizes']
            claimed=s['score_claimed'] if op==3 else s['point_claimed']
            i=d['prize_id'];a.require(1<=i<=len(rows),'礼包编号无效')
            total=s['score'] if op==3 else daily.prepare(role,now,daily.load_rules())['total']
            a.require(total>=rows[i-1]['point'] and i not in claimed,'条件不足或礼包已领取')
            reward=a.prizes(role,rows[i-1]['prizes']);claimed.append(i);extra=dict(prize_id=i,status=3)
        elif op==9:
            a.require(set(d)=={'index','count','local_token'} and type(d['index']) is int and
                      type(d['count']) is int and 1<=d['count']<=15,'仙人助力兑换参数无效')
            row=ASSIST.get(d['index']);a.require(row is not None,'仙人助力商品不存在')
            n=d['count']
            for tid,cost in zip((1350,1351,1352),row['consume']):
                if cost: a.consume(role,tid,cost*n)
            specs=copy.deepcopy(row['prizes'])
            for p in specs: p[2]*=n
            reward=a.prizes(role,specs)
        else:
            a.require(set(d)=={'index','count','local_token'} and type(d['index']) is int and
                      type(d['count']) is int and 1<=d['count']<=99,'兑换参数无效')
            i,n=d['index'],d['count'];a.require(1<=i<=len(r['shop']),'商品不存在')
            row=r['shop'][i-1];bought=s['bought'].get(str(i),0)
            a.require(bought+n<=row['limit'] and s['piece']>=row['piece']*n,'碎石不足或兑换次数不足')
            s['piece']-=row['piece']*n;s['bought'][str(i)]=bought+n
            p=list(row['prize']);p[2]*=n;reward=a.prizes(role,[p])
        s['token']=secrets.token_hex(16)
    deliver_charge(role,s,now,r)
    return [response(role,s,now,r,op,reward,extra)]
