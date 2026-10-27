"""如来转世盘: native 3.87 contracts/box CSV [A], missing event economy [B]."""
import json
import secrets
from pathlib import Path

from . import activity as a, formation as f, summon

ROOT = Path(__file__).resolve().parents[1]
BAGS = {}
for row in summon.rows('happiness_bag_config.csv'):
    tid, count = map(int, row['attach_type|attach_count'].split('|'))
    BAGS.setdefault(int(row['item_type']), {})[(int(row['object_type']), tid)] = count


def load_rules(path=ROOT / 'server_config/rulai_rules.json'):
    r = json.loads(Path(path).read_text())
    f.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
              and isinstance(r.get('revision'), str) and bool(r['revision']), '如来转盘配置来源无效')
    f.require(type(r.get('enabled')) is bool, '如来转盘开放开关无效')
    f.require(type(r.get('timezone_offset_hours')) is int and -12 <= r['timezone_offset_hours'] <= 14, '如来转盘时区无效')
    for key, upper in [('period_days', 365), ('gold_per_rmb', 1000),
                       ('rmb_per_draw', 100000), ('bonus_rmb', 1000000)]:
        f.require(type(r.get(key)) is int and 1 <= r[key] <= upper, '如来转盘数值无效：' + key)
    pool, bonus = r.get('pool'), r.get('bonus')
    f.require(isinstance(pool, list) and len(pool) == 8, '原版如来转盘必须有八格奖励')
    f.require(isinstance(bonus, list) and 1 <= len(bonus) <= 8, '如来转盘豪礼无效')
    for row in pool:
        f.require(isinstance(row, dict) and type(row.get('weight')) is int and 1 <= row['weight'] <= 1000000, '如来转盘权重无效')
    for p in [row.get('reward') for row in pool] + bonus:
        f.require(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p), '如来转盘奖励格式无效')
        # Native wheel renders item icons and quantities; use stackable items only.
        typ, tid, n, lv = p
        f.require(typ == 5 and tid in f.ITEMS and f.ITEMS[tid]['can_stack'] == '1'
                  and 1 <= n <= 100000 and lv == 1, '如来转盘道具奖励无效')
    return r


def period(now, r):
    duration = r['period_days'] * 86400
    anchor = 4 * 86400 - r['timezone_offset_hours'] * 3600
    start = (now - anchor) // duration * duration + anchor
    return start, start + duration


def state(role, now, r):
    start, end = period(now, r)
    store = role.setdefault('activity', {})
    s = store.get('rulai')
    if s is None or now >= s['clock'] and start > s['start']:
        s = dict(start=start, end=end, clock=now, charge_gold=0, draws=0, claimed=False, last_prize=0)
        store['rulai'] = s
    s['clock'] = max(s['clock'], now)
    return s


def guard(s, now, r):
    f.require(r['enabled'] and s['start'] <= now < s['end'], '如来转盘尚未开放或已经结束')
    f.require(now >= s['clock'], '如来转盘时钟已回退，请恢复本地时间')


def remaining(s, r):
    return max(0, s['charge_gold'] // (r['rmb_per_draw'] * r['gold_per_rmb']) - s['draws'])


def bonus_status(s, r):
    return 3 if s['claimed'] else 2 if s['charge_gold'] >= r['bonus_rmb'] * r['gold_per_rmb'] else 1


def snapshot(s, r):
    count = remaining(s, r)
    pay = s['charge_gold'] // r['gold_per_rmb']
    status = bonus_status(s, r)
    return dict(cur_count=count, order_pay=pay, end_time=s['end'] if r['enabled'] else 0,
                random_table=[a.prize_spec(row['reward']) for row in r['pool']],
                order_list=[dict(desc=f"本期每累计充值{r['rmb_per_draw']}元获得1次抽奖", status=True),
                            dict(desc=f"已获得{count + s['draws']}次，已使用{s['draws']}次", status=count > 0),
                            dict(desc=f"累计充值{r['bonus_rmb']}元可领本期豪礼", status=status >= 2)],
                ext_info=dict(item=a.prize_spec(r['bonus'][0]),
                              attach_list=[a.prize_spec(p) for p in r['bonus']],
                              prize_flag=status, reach_money=r['bonus_rmb']))


def schedule(now, r):
    start, end = period(now, r)
    return [dict(start_time=start if r['enabled'] else 0, end_time=end if r['enabled'] else 0)]


def sync(role, now):
    r = load_rules()
    s = state(role, now, r)
    flag = r['enabled'] and (remaining(s, r) > 0 or bonus_status(s, r) == 2)
    return summon.event(80, dict(local_rulai=dict(times=schedule(now, r), flag=flag, pack_data=snapshot(s, r))))


def record_charge(role, amount, now):
    r = load_rules()
    if not r['enabled'] or amount <= 0:
        return
    s = state(role, now, r)
    guard(s, now, r)
    s['charge_gold'] += amount  # Base paid gold only; no first-charge/bonus gold.


def draw(r):
    pick = secrets.randbelow(sum(row['weight'] for row in r['pool']))
    for i, row in enumerate(r['pool'], 1):
        if pick < row['weight']:
            return i
        pick -= row['weight']
    raise AssertionError('unreachable weighted draw')


def settle(role, req, now):
    r = load_rules()
    op = req['id']
    f.require(type(op) is int and op in (0, 1, 2), '如来转盘操作无效')
    # Original actions send an empty literal table. Never accept client rewards.
    f.require(''.join(req['data'].split()) == '{}', '如来转盘参数无效')
    s = state(role, now, r)
    guard(s, now, r)
    if op == 0:
        return [summon.event(200, dict(id=0, pack_data=snapshot(s, r)))]
    if op == 1:
        f.require(remaining(s, r) > 0, '抽奖次数不足')
        index = draw(r)
        gains = a.prizes(role, [r['pool'][index - 1]['reward']])
        s['draws'] += 1
        s['last_prize'] = index
        data = dict(id=1, prize_index=index, prize_list=gains)
    else:
        f.require(bonus_status(s, r) == 2, '累计充值不足或豪礼已领取')
        gains = a.prizes(role, r['bonus'])
        s['claimed'] = True
        data = dict(id=2, prize_list=gains)
    data['flag'] = remaining(s, r) > 0 or bonus_status(s, r) == 2
    return [summon.event(200, data)]


def use_bag(role, req):
    tid, n = req['item_type'], req['item_count']
    f.require(tid in BAGS and type(n) is int and 1 <= n <= 15, '如来福袋每次可使用1至15个')
    target = (req['des_type'], req['des_id'])
    f.require(target in BAGS[tid], '如来福袋兑换目标无效')
    item = f.lookup(role, 'attachments', req['item_id'])
    f.require(item['attach_type'] == 5 and item['type_id'] == tid and item['count'] >= n
              and not item.get('is_lock') and not item.get('owner_id') and not item.get('equip_pos'), '如来福袋不足或不可使用')
    item['count'] -= n
    role['attachments'] = [i for i in role['attachments'] if i is not item or i['count'] > 0]
    gain = a.prizes(role, [[target[0], int(target[1]), BAGS[tid][target] * n, 1]])
    return [summon.event(21, dict(result=1, type_id=tid, count=n, attach_list=gain))]
