"""Native home social protocol backed by persistent catalog NPC neighbours [B]."""
import copy
from . import activity as a, npc_players
from . import activity_home as h


def roster(role, s):
    if 'neighbours' not in s:
        pool = [e for e in npc_players.catalog().values() if e['profile']['level'] >= 50]
        chosen = []
        for i in range(10):
            target = min(99, max(50, role['level'] - 10 + i * 5))
            entry = min((e for e in pool if e['npc_id'] not in chosen),
                        key=lambda e: (abs(e['profile']['level'] - target), e['profile']['role_id']))
            chosen.append(entry['npc_id'])
        s['neighbours'] = chosen
        # Preserve old cooperation records without keeping fictitious player identities.
        friends = s.setdefault('offline_friends', {})
        for i, key in enumerate(chosen, 900001):
            old = friends.pop(str(i), None)
            if old is not None:
                friends[str(npc_players.catalog()[key]['profile']['role_id'])] = old
    return [npc_players.catalog()[key] for key in s['neighbours']]


def layout(entry):
    level = entry['profile']['level']
    building = min(20, 1 + (level - 50) // 2)
    scale = 3 if level >= 95 else 2 if building > 11 else 1
    return dict(level=scale, build={str(i):building for i in h.KEYS})


def states(role, s, now, r):
    friends = s.setdefault('offline_friends', {})
    for entry in roster(role, s):
        p = entry['profile']; f = friends.setdefault(str(p['role_id']), {})
        if f.get('day') != a.day(now, r):
            start = a.day(now, r) * 86400 - r['timezone_offset_hours'] * 3600
            count = int(h.BUILD[2][layout(entry)['build']['2']]['grid_count'])
            f.update(day=a.day(now, r), invited=False, plants={str(i):dict(
                level=0, seed_type=5, start_time=start, plant_time=start, gain_time=start+86400,
                cur_plus_times=0, total_plus_times=int(h.SEEDS[5]['friend_plus_times']),
                benefit_flag=True, event_info=[], missed_events=0) for i in range(1, count+1)})
        f.setdefault('messages', [])
    return friends


def summary(entry, f, now):
    p = entry['profile']; home = layout(entry)
    # Native getHeadSprite expects a cortege type, not the profile portrait ID.
    raw = npc_players.source_file(entry['source_file'])[entry['npc_id']]['role']
    lead = next(c for c in raw['corteges'] if c.get('order') == 1)
    return dict(id=p['role_id'], name=p['role_name'], level=p['level'], home_level=home['level'],
                point=h.point(home), show_type=lead['type'], reborn_layer=lead.get('reborn_layer', 0),
                has_open=True, has_invited=f['invited'], is_npc=True,
                benefit_flag=any(q['benefit_flag'] and now<q['gain_time'] for q in f['plants'].values()))


def listing(role, s, now, r):
    friends = states(role, s, now, r)
    return {e['profile']['role_id']:summary(e, friends[str(e['profile']['role_id'])], now) for e in roster(role, s)}


def settle(role, s, op, d, now, r):
    friends = states(role, s, now, r)
    entries = roster(role, s)
    if op == 13:
        return [h.response(op, dict(friend_data=listing(role, s, now, r)))]
    fid = d.get('friend_id')
    a.require(type(fid) is int, '洞府好友不存在')
    # Old queued requests can finish, but never publish these compatibility IDs.
    if 900001 <= fid < 900001 + len(entries):
        fid = entries[fid-900001]['profile']['role_id']
    entry = next((e for e in entries if e['profile']['role_id'] == fid), None)
    a.require(entry is not None, '洞府好友不存在')
    f = friends[str(fid)]; profile = entry['profile']
    if op == 6:
        npc = dict(**layout(entry), plants=f['plants'], messages=f['messages'], new_event=False,
                   pets=[], pet_growth={}, assistant_until=0, pray_time=0, pray_count=0,
                   train={str(i):dict(level=0,cur_exp=0) for i in range(1,5)}, train_count={},
                   passed=False, fight_count=0)
        data=h.info(npc,r);data['pet_data']['pet_list']=[]
        return [h.response(op,data)]
    if op == 12:
        msg = d.get('chat_msg')
        a.require(isinstance(msg,str) and 1<=len(msg.strip())<=200 and not any(ord(c)<32 for c in msg), '留言需要1至200字且不能包含控制字符')
        f['messages'] += [f"{role['role_name']}：{msg.strip()}",
                          f"{profile['role_name']}：{profile['signature']}"]
        f['messages'] = f['messages'][-30:]
        return [h.response(op,{})]
    if op == 5:
        a.require(not f['invited'], '今日已经邀请该离线好友')
        targets = [p for p in s['plants'].values() if p.get('seed_type') and now<p['gain_time'] and p['cur_plus_times']<p['total_plus_times']]
        a.require(targets, '请先种植尚可施肥的作物')
        f['invited'] = True
        for p in targets:
            p['cur_plus_times'] += 1
        msg = f"{profile['role_name']}应邀来访，为{len(targets)}块药田施肥。"
        s.setdefault('messages', []).append(msg); s['messages'] = s['messages'][-30:]; s['new_event'] = True
        return [h.response(op, dict(friend_id=fid, plants_plus_time={int(k):p.get('cur_plus_times',0) for k,p in s['plants'].items()}))]
    if op == 23:
        a.require(role.get('month_card_time',0)>now, '一键施肥需要有效月卡')
    idx = d.get('plant_grid')
    if op == 7:
        a.require(type(idx) is int and str(idx) in f['plants'], '药田不存在')
    targets = list(f['plants']) if op == 23 else [str(idx)]
    changed, prizes = {}, {}
    for key in targets:
        p = f['plants'][key]
        if not p['benefit_flag'] or now>=p['gain_time'] or p['cur_plus_times']>=p['total_plus_times']:
            continue
        p['benefit_flag'] = False; p['cur_plus_times'] += 1; changed[int(key)] = p['cur_plus_times']
        prizes[int(key)] = a.prizes(role, [[12,0,r['home_friend_silver'],1]])[0]
    if op == 7:
        a.require(bool(changed), '该药田已施肥或已成熟')
        return [h.response(op, dict(plant_grid=idx,cur_plus_times=changed[idx],prize_list=[prizes[idx]]))]
    return [h.response(op, dict(plants_plus_time=changed,prize_list=prizes))]
