"""天机阁: original 1227/event195 and CSV [A], local seasons [B]."""
import copy
import json
from pathlib import Path

from . import feature_levels, formation as f, journey, summon

ROOT = Path(__file__).resolve().parents[1]
SHOP = {int(x['index']): x for x in summon.rows('exchange_zone.csv')}
GIFTS = {kind: {int(x['index']): x for x in summon.rows('gift_config.csv')
                if int(x['gift_type']) == kind} for kind in (1, 2)}


def specs(value):
    # Original CSV is object|type|level|count, not grant's count|level.
    return [[a, b, n, lv] for a, b, lv, n in
            (map(int, token.split('|')) for token in value.split('/') if token)]


def client_tables():
    # The running client's writable CSV cache can differ from the shipped APK.
    # Pin only these two activity tables to the audited 3.87 source, stripping
    # parenthetical CSV header comments just as native csv.open2 does.
    return {'csv_config/exchange_zone.csv': [
                {k.split('(')[0]: v for k, v in SHOP[i].items()} for i in sorted(SHOP)],
            'csv_config/gift_config.csv': [GIFTS[k][i] for k in (1, 2) for i in sorted(GIFTS[k])]}


def load_rules(path=ROOT / 'server_config/pavilion_rules.json'):
    r = json.loads(Path(path).read_text())
    f.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
              and bool(r.get('revision')), '天机配置来源无效')
    f.require(type(r.get('enabled')) is bool, '天机开放开关无效')
    f.require(type(r.get('timezone_offset_hours')) is int
              and -12 <= r['timezone_offset_hours'] <= 14, '天机时区无效')
    for key, upper in (('period_days', 365), ('gold_per_rmb', 1000),
                       ('ascension_extra_rmb', 100000), ('ascension_extra_limit', 100),
                       ('batch_limit', 9999)):
        f.require(type(r.get(key)) is int and 1 <= r[key] <= upper, '天机配置数值无效：' + key)
    f.require(set(SHOP) == set(range(1, 10)), '天机原版商品缺失')
    for row in SHOP.values():
        f.require(int(row['max_buy_count']) > 0 and int(row['goldon_count']) > 0, '天机原表价格无效')
        for p in specs(row['attach_list']) + specs(row['gift_prize']):
            f.require(p[0] == 12 or p[0] == 5 and p[1] in f.ITEMS, '天机奖励物品无效')
    return r


def period(now, r):
    # 1970-01-05 is a Monday. UTC+8 is applied before choosing the period.
    seconds = r['period_days'] * 86400
    anchor = 4 * 86400 - r['timezone_offset_hours'] * 3600
    start = (now - anchor) // seconds * seconds + anchor
    return start, start + seconds


def prepare(role, now, r):
    start, end = period(now, r)
    s = role.setdefault('pavilion', dict(start=start, end=end, clock=now,
                                        charge_gold=0, bricks_earned=0, bought={}, claimed=[]))
    # Keep the high-water clock: rewinding cannot resurrect an earlier season.
    # A legacy seven-day save migrates once, even when its start is identical
    # to (or later than) the new globally aligned fortnight's start.
    if now >= s['clock'] and (start > s['start'] or s['end'] - s['start'] != end - start):
        trial = copy.deepcopy(role)
        recycle(trial, now, s)
        trial['pavilion'].update(start=start, end=end, charge_gold=0, bricks_earned=0,
                                 bought={}, claimed=[])
        role.clear(); role.update(trial)
        s = role['pavilion']
    s['clock'] = max(now, s['clock'])
    return s


def recycle(role, now, old):
    """Retire every old brick, including locked stacks and unclaimed mail."""
    def brick(p):
        return p[0] == 5 and p[1] == 1141

    items = role.get('attachments', [])
    retired = [i for i in items if i['attach_type'] == 5 and i['type_id'] == 1141]
    bag_count = sum(i['count'] for i in retired)
    role['attachments'] = [i for i in items if not (i['attach_type'] == 5 and i['type_id'] == 1141)]
    pending_count = 0
    for m in role.get('welfare', {}).get('mails', {}).values():
        if m['claimed']:
            continue
        count = sum(p[2] for p in m['prizes'] if brick(p))
        if not count:
            continue
        pending_count += count
        m['prizes'] = [p for p in m['prizes'] if not brick(p)]
        m['claimed'] = not m['prizes']
        m['mail_body'] += f'\n本期刷新，未领取的{count}金砖已按1:1兑换蟠桃，转入“天机阁金砖返还”邮件。'
    count = bag_count + pending_count
    if count:
        mail(role, f"pavilion-recycle-{old['start']}-{old['end']}", '天机阁金砖返还',
             [[5, 1001, count, 1]], now,
             body=f'天机阁常驻活动每14天刷新一次，本期进度已重置。剩余金砖共{count}个'
                  f'（背包{bag_count}个、未领取邮件{pending_count}个），已按1:1兑换为蟠桃{count}个，'
                  '请领取附件。旧金砖不再保留；累充、全民充值送豪礼、兑换次数和首次兑换资格重新计算。')
    role['pavilion']['last_recycle'] = dict(start=old['start'], end=old['end'],
                                           bag_count=bag_count, pending_count=pending_count, count=count)


def guard(s, now, r):
    f.require(r['enabled'] and s['start'] <= now < s['end'], '天机阁尚未开放')
    f.require(now >= s['clock'], '天机阁时钟已回退，请恢复本地时间')


def totals(role, peers, s):
    # Actual local saves only; no invented purchases or recharge NPCs.
    states = [s] + [p['pavilion'] for p in peers or []
                    if p.get('pavilion', {}).get('start') == s['start']
                    and p['pavilion'].get('end') == s['end']]
    return sum(p['bricks_earned'] for p in states)


def gift_states(s, total):
    return {i: dict(state=3 if i in s['claimed'] else 2 if total >= int(row['money']) else 1,
                    count=total) for i, row in GIFTS[2].items()}


def extra(s, r):
    return min(r['ascension_extra_limit'], s['charge_gold'] // (r['gold_per_rmb'] * r['ascension_extra_rmb']))


def catalog(role, now, r, peers=None):
    s = prepare(role, now, r)
    gifts = gift_states(s, totals(role, peers, s))
    ex = extra(s, r)
    return dict(flag=1, begin_time=s['start'], end_time=s['end'],
                charge_money=s['charge_gold'] / r['gold_per_rmb'],
                had_prize=any(g['state'] == 2 for g in gifts.values()), charge_info=gifts,
                exchange_info={i: dict(state=3 if s['bought'].get(str(i), 0) else 1,
                    left_buy_count=int(row['max_buy_count']) + (ex if i == 1 else 0) - s['bought'].get(str(i), 0),
                    # Native L509-511: "recharge need_charge more to raise
                    # the limit by plus_times". This is the next increment,
                    # not the number of increases already earned.
                    left_count=0, plus_times=1 if i == 1 and ex < r['ascension_extra_limit'] else 0,
                    need_charge=max(0, (ex + 1) * r['ascension_extra_rmb'] - s['charge_gold'] // r['gold_per_rmb'])
                        if i == 1 and ex < r['ascension_extra_limit'] else 0)
                    for i, row in SHOP.items()})


def status(role, now, peers=None):
    r = load_rules()
    data = catalog(role, now, r, peers)
    active = r['enabled'] and now >= role['pavilion']['clock']
    return dict(begin_time=data['begin_time'] if active else 0,
                end_time=data['end_time'] if active else 0, had_prize=active and data['had_prize'])


def update(role, now, peers=None):
    return summon.event(80, dict(local_pavilion=dict(
        status=status(role, now, peers), data=catalog(role, now, load_rules(), peers))))


def mail(role, key, title, prizes, now, body='天机阁活动奖励，请领取附件。'):
    from . import system_mail, welfare
    # deliver replaces the detached role, so callers must not keep state aliases.
    return system_mail.deliver(role, key=key, title=title,
        body=body, prizes=prizes,
        now=now, rules=welfare.load_rules())


def record_charge(role, gold, now):
    """Called only after a new, validated local recharge order succeeds."""
    r = load_rules()
    # Recharge bypasses the activity request gate; use the same unlock level.
    # Ignore locked-period principal entirely so it cannot earn rewards later.
    if not r['enabled'] or role.get('level', 1) < feature_levels.LEVELS['destiny']:
        return
    s = prepare(role, now, r)
    guard(s, now, r)
    f.require(type(gold) is int and gold > 0, '天机充值金额无效')
    old = s['charge_gold']; s['charge_gold'] += gold
    gain = s['charge_gold'] // r['gold_per_rmb'] - old // r['gold_per_rmb']
    # [B] Each type-1 cumulative milestone pays once per period, in addition to
    # the native 1 RMB = 1 brick base rate. Only credited principal counts.
    for row in GIFTS[1].values():
        threshold = int(row['money']) * r['gold_per_rmb']
        if old < threshold <= s['charge_gold']:
            gain += specs(row['gift_list'])[0][2]
    s['bricks_earned'] += gain
    if gain:
        mail(role, f"pavilion-charge-{s['start']}-{s['end']}-{s['charge_gold']}",
             '天机阁充值金砖', [[5, 1141, gain, 1]], now)


def settle(role, req, now, peers=None):
    from . import activity
    r = load_rules(); s = prepare(role, now, r); guard(s, now, r)
    flag, index, count, ten, five = (req[k] for k in ('flag', 'index', 'count', 'ten_card', 'five_card'))
    f.require(all(type(x) is int and x >= 0 for x in (flag, index, count, ten, five)), '天机请求参数无效')
    if flag == 1:
        f.require(index == count == ten == five == 0, '天机查询参数无效')
        return [summon.event(195, catalog(role, now, r, peers))]
    if flag == 3:
        f.require(index in GIFTS[2] and count == ten == five == 0, '天机领奖参数无效')
        f.require(gift_states(s, totals(role, peers, s))[index]['state'] == 2, '全民好礼未达成或已领取')
        gain = activity.prizes(role, specs(GIFTS[2][index]['gift_list']))
        s['claimed'].append(index)
        return [summon.event(195, dict(flag=3, index=index, prize_list=gain,
                  snapshot=catalog(role, now, r, peers),
                  had_prize=any(v['state'] == 2 for v in gift_states(s, totals(role, peers, s)).values())))]
    f.require(flag == 2 and index in SHOP and 1 <= count <= r['batch_limit'], '天机兑换参数无效')
    row = SHOP[index]; bought = s['bought'].get(str(index), 0)
    limit = int(row['max_buy_count']) + (extra(s, r) if index == 1 else 0)
    f.require(bought + count <= limit, '本期礼包兑换次数已用完')
    f.require(ten + five <= count, '一个礼包只能使用一张减金砖卡')
    cost = max(0, int(row['goldon_count']) * count - ten * 10 - five * 5)
    for tid, amount in ((1141, cost), (1143, ten), (1142, five)):
        if amount:
            activity.consume(role, tid, amount)
    gain = activity.prizes(role, [[a, b, n * count, lv] for a, b, n, lv in specs(row['attach_list'])])
    s['bought'][str(index)] = bought + count
    notifications = []
    if bought == 0:
        mail(role, f"pavilion-first-{s['start']}-{s['end']}-{index}", '天机阁首次兑换好礼',
             specs(row['gift_prize']), now)
        from . import welfare
        notifications.append(welfare.mail_snapshot(role, now, welfare.load_rules()))
    return [summon.event(195, dict(flag=2, index=index, count=count,
                                   snapshot=catalog(role, now, r, peers),
                                   left_count=0, attach_list=gain))] + notifications
