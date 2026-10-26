"""Original weekly feast/CSV rewards [A]; catalog guests and gift contents [B]."""
from . import guild as u, daily, journey, summon

FEAST = {int(v['award_type']): v for v in summon.rows('union_feast_award.csv')}


def rollover(role, now, r):
    """[B] Missing fortune-rank rewards use the existing permanent mail UI."""
    from . import system_mail, welfare
    current = daily.week(now, r)
    weeks = {}
    for g in role.get('guild', {}).get('unions', {}).values():
        f = g.get('feast', {})
        week = f.get('week', (f.get('day', daily.day(now, r))+3)//7)
        if week >= current: continue
        for row in f.get('stats', {}).values():
            merged = weeks.setdefault(week, {})
            previous = merged.setdefault(row['id'], dict(row, fortune=0, contribute=0))
            previous['fortune'] += row['fortune']; previous['contribute'] += row['contribute']
    for week, scores in weeks.items():
        history = role.get('guild', {}).get('feast_rank_history', {})
        if str(week) in history: continue
        rows = sorted(scores.values(), key=lambda v: (-v['fortune'], -v['contribute'], v['id']))
        order = next((i for i,v in enumerate(rows,1) if v['id']==role['role_id'] and v['fortune']>0), 0)
        tier = next((v for v in r['feast_fortune_rewards'] if 0 < order <= v['max_rank']), None)
        if not tier: continue
        system_mail.deliver(role, 'guild-feast-'+str(week), '群英会福气榜奖励',
                            '本地群英会周榜第%d名。奖励为离线补全规则。'%order,
                            tier['prizes'], now, welfare.load_rules())
        history = role['guild'].setdefault('feast_rank_history', {})
        history[str(week)] = dict(order=order, fortune=scores[role['role_id']]['fortune'])


def account(role, s, r):
    a = s.setdefault('feast_account', {})
    if a.get('day') != s['day']:
        # Preserve legacy usage on upgrade, including a reconnect that day.
        used = role.get('last_feast_grab_count', 0) if daily.day(role.get('last_feast_grab_time', 0), r) == s['day'] else 0
        a.update(day=s['day'], grabbed=used, sent=0)
    role['last_feast_grab_count'] = a['grabbed']
    return a


def stats(f, ident, name):
    return f.setdefault('stats', {}).setdefault(str(ident), dict(
        id=ident, name=name, rank=0, fortune=0, contribute=0, normal_gift=0, advanced_gift=0))


def gift(f, member, cfg, count, now, npc=False):
    ident = max((v['id'] for v in f['gifts']), default=0) + 1
    row = dict(id=ident, des_id=ident, sender_id=member['id'], name=member['name'],
               gift_type=cfg['item'], count=count, begin_time=now, end_time=f['end'],
               grabbed=[], npc=npc)
    f['gifts'].append(row)
    return row


def feast(s, g, now, r):
    week = (s['day'] + 3) // 7
    f = g.setdefault('feast', {})
    # Retain paid legacy feasts until their original deadline, never charge again.
    if f and 'week' not in f:
        f['week'] = (f.get('day', s['day']) + 3) // 7
    if not f or f.get('week') != week and now >= f.get('end', 0):
        f.clear()
        f.update(week=week, day=s['day'], type=0, end=0, gifts=[], claimed=[],
                 grabbed={}, sent=0, stats={}, log=[], ended=False, npc_seeded=False)
    for key,value in dict(type=0,end=0,gifts=[],claimed=[],grabbed={},sent=0,stats={},log=[],ended=False,npc_seeded=False).items():
        f.setdefault(key,value)
    if f['type'] and now < f['end'] and not f.get('npc_seeded'):
        from .guild_offline import roll
        donors = [m for m in g['members'].values() if m.get('npc_id') and m['rank'] != 6]
        for _ in range(min(3, len(donors))):
            m = donors.pop(roll(s, len(donors)))
            cfg = r['feast_gifts'][1 if f['type'] == 3 and not f['gifts'] else 0]
            gift(f, m, cfg, 1, now, npc=True)
            row = stats(f, m['id'], m['name'])
            row['fortune'] += cfg['contrib']; row['contribute'] += cfg['contrib']
            row['normal_gift' if cfg['type'] == 1 else 'advanced_gift'] += 1
        f['npc_seeded'] = True
    # NPCs actually receive sent gifts, so "previous batch not collected" can end.
    for v in f['gifts']:
        if f.get('ended') or v.get('npc') or min(now,f['end']) < v['begin_time'] + r['feast_npc_grab_seconds']:
            continue
        for m in g['members'].values():
            if v['count'] <= 0: break
            if not m.get('npc_id') or m['rank'] == 6 or str(m['id']) in v['grabbed']: continue
            v['count'] -= 1; v['grabbed'].append(str(m['id']))
            stats(f, m['id'], m['name'])['fortune'] += r['feast_grab_fortune']
    if f['type'] and now >= f['end'] and not f.get('ended'):
        f['ended'] = True
        g['events'].append('群英会已经结束（' + str(f['end']) + '）')
        g['events'] = g['events'][-100:]
    return f


def data(role, s, g, now, r):
    f = feast(s, g, now, r); a = account(role, s, r); rid = str(int(role['role_id']))
    active = bool(f['type']) and now < f['end']
    allowed = role['union_rank'] != 6 and a['grabbed'] < r['feast_grab_limit']
    # guildPartyUI L588 compares to the NUMBER 1; true disables the native button.
    gifts = [dict(v, can_grab=int(active and allowed and v['begin_time'] <= now < v['end_time']
                                 and rid not in v['grabbed'] and v['count'] > 0)) for v in f['gifts']]
    return dict(feast_stat=0 if active else 54 if f['type'] else 53, feast_type=f['type'],
                send_gift={v['type']: dict(cost_gold=v['gold'], contribute=v['contrib']) for v in r['feast_gifts']},
                max_grab_count=r['feast_grab_limit'], member_count=sum(m['rank'] != 6 for m in g['members'].values()),
                feast_end_time=f['end'], gift_data=gifts,
                can_rece_award=active and role['union_rank'] != 6 and rid not in f['claimed'] and a.get('claimed_week') != f['week'])


def ranking(role, s, now, r):
    rows = []
    for g in s['unions'].values():
        f = feast(s, g, now, r)
        rows.extend(dict(v) for v in f['stats'].values())
    # One account can have participated in more than one guild; merge its score.
    merged = {}
    for row in rows:
        previous = merged.setdefault(row['id'], dict(row, fortune=0, contribute=0, normal_gift=0, advanced_gift=0))
        for k in ('fortune', 'contribute', 'normal_gift', 'advanced_gift'): previous[k] += row[k]
    rows = sorted(merged.values(), key=lambda v: (-v['fortune'], -v['contribute'], v['id']))
    for i, row in enumerate(rows, 1): row['rank'] = i
    return dict(query_type=15, order=next((v['rank'] for v in rows if v['id'] == role['role_id']), 0), fortune_info=rows)


def settle(role, s, g, op, d, now, r):
    f = feast(s, g, now, r); a = account(role, s, r); rid = str(int(role['role_id']))
    prizes = []
    if op == 65:
        u.authorize(role, r, 24)
        u.require(role['union_rank'] == 1, '只有盟主可以开启群英会')
        u.require(g['level'] >= r['feast_union_level'], '仙盟等级不足，无法开启群英会')
        u.require((s['day'] + 3) % 7 != 6, '周日不能开启群英会')
        u.require(not f['type'] and a.get('opened_week') != f['week'], '本周已举办群英会')
        typ = u.positive(d, 'feast_type', 3); row = FEAST[typ]
        # Original dialog formats cost_gold as "仙盟资金%d".
        u.require(g['money'] >= int(row['cost_gold']), '仙盟资金不足')
        g['money'] -= int(row['cost_gold'])
        f.update(type=typ, end=now+r['feast_seconds'], opened=now)
        a['opened_week'] = f['week']; g['popularity'] += int(row['popularity'])
        g['events'].append(role['role_name']+'举办了群英会'); g['events'] = g['events'][-100:]
    else:
        u.authorize(role, r, 25); u.require(role['union_rank'] != 6, '正式成员才能参加群英会')
        u.require(f['type'] and now < f['end'], '群英会尚未开放或已结束')
        rowstats = stats(f, role['role_id'], role['role_name'])
        if op == 68:
            u.require(rid not in f['claimed'] and a.get('claimed_week') != f['week'], '本周群英会祝福已领取')
            row = FEAST[f['type']]; typ, tid, level, count = map(int, row['attach_data'].split('|'))
            prizes.append(journey.grant(role, [typ, tid, count, level]))
            role['strength'] += int(row['strength']); role['energy'] += int(row['energy'])
            f['claimed'].append(rid); a['claimed_week'] = f['week']
            role.update(last_rece_award_time=now, train_tree_rate=int(row['rate_times(plan_tree_rate|contrib_rate)']),
                        contrib_plus_rate=int(row['rate_times(plan_tree_rate|contrib_rate)']))
            s['feast_buff_end'] = now+r['feast_seconds']; s['feast_fam_rate'] = int(row['fam_property_rate'])
        elif op == 67:
            u.require(role.get('vip_level', 0) >= 1, 'VIP1及以上才能赠送礼盒')
            count = u.positive(d, 'count', sum(m['rank'] != 6 for m in g['members'].values()))
            u.require(count >= 2, '每批至少赠送2个礼盒')
            u.require(a['sent']+count <= r['feast_gift_limit'], '今日赠礼数量已达上限')
            u.require(not any(v.get('sender_id') == role['role_id'] and v['count'] > 0 for v in f['gifts']), '上批礼盒尚未被抢完')
            typ = u.positive(d, 'gift_type', 2); cfg = r['feast_gifts'][typ-1]
            u.pay(role, 'gold_coin', cfg['gold']*count); a['sent'] += count; f['sent'] += count
            gain = u.contribution(role, cfg['contrib']*count)
            rowstats['contribute'] += gain; rowstats['fortune'] += cfg['contrib']*count
            rowstats['normal_gift' if typ == 1 else 'advanced_gift'] += count
            gift(f, g['members'][rid], cfg, count, now)
        elif op == 66:
            ident = u.positive(d, 'des_id')
            v = next((v for v in data(role, s, g, now, r)['gift_data'] if v['des_id'] == ident), None)
            u.require(v is not None and v['can_grab'] == 1, '礼物未开放、已领完或今日领取次数不足')
            v = next(v for v in f['gifts'] if v['des_id'] == ident)
            prizes.append(journey.grant(role, [5, v['gift_type'], 1, 1]))
            v['count'] -= 1; v['grabbed'].append(rid); a['grabbed'] += 1; f['grabbed'][rid] = a['grabbed']
            rowstats['fortune'] += r['feast_grab_fortune']
            role.update(last_feast_grab_time=now, last_feast_grab_count=a['grabbed'])
        else: u.require(False, '群英会操作无效')
    return [u.reply(op, dict(result=1, gift_data=data(role, s, g, now, r)['gift_data'], prize_list=prizes))]


def open_box(role, req, now, r):
    """Native inventory use-item entry: missing official drop table is explicit [B]."""
    tid, n = req['item_type'], req['item_count']
    u.require(tid in (1120, 1121) and type(n) is int and 1 <= n <= 100, '礼盒数量无效')
    u.require(req['des_type'] == 1 and req['des_id'] in (0, role['role_id']), '礼盒使用目标无效')
    item = u.formation.lookup(role, 'attachments', req['item_id'])
    u.require(item['attach_type'] == 5 and item['type_id'] == tid and item['count'] >= n and not item.get('is_lock'), '礼盒不足或已锁定')
    item['count'] -= n
    if not item['count']: role['attachments'].remove(item)
    prizes = [journey.grant(role, [p[0], p[1], p[2]*n, p[3]]) for p in r['feast_box_rewards'][str(tid)]]
    return [summon.event(21, dict(result=1, type_id=tid, count=n, attach_list=prizes))]
