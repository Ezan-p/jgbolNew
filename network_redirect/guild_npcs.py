"""[B] Shared guild NPC selection over the immutable local players catalogue.

Only guild links and social state are saved here. The actual roster remains in
analysis/npc_design and is retrieved through npc_players.get(role_id).
"""
from . import npc_players


def choose(s, level, count=1, excluded_ids=(), tiers=None):
    """Choose without replacement near the requested level, using saved RNG."""
    from .guild_offline import roll
    excluded = set(excluded_ids)
    rows = [e for e in npc_players.catalog().values()
            if e['profile']['role_id'] not in excluded
            and (tiers is None or e['profile']['tier'] in tiers)]
    rows.sort(key=lambda e: (abs(e['profile']['level'] - level), e['npc_id']))
    # Keep a small level neighbourhood while allowing different builds/identities.
    pool = rows[:max(30, count * 4)]
    selected = []
    for _ in range(min(count, len(pool))):
        selected.append(pool.pop(roll(s, len(pool))))
    return selected


def member(entry, now, rank=5):
    p = entry['profile']
    return dict(id=p['role_id'], name=p['role_name'], rank=rank, level=p['level'],
                contrib=0, totalcontrib=0, head_type=p['head_type'],
                vip_level=p['vip_level'], jointime=now, lastlogin=now,
                online=False, toporder=0, logout_time=now,
                combat_power=p['role_combat_power'], npc=True, npc_id=entry['npc_id'])


def occupied(s):
    return {m['id'] for g in s['unions'].values()
            for section in ('members', 'applications') for m in g[section].values()}


def migrate(role, s, now):
    """Replace old placeholder identities once, preserving membership and links."""
    if s.get('npc_players_version') == 1:
        return
    replacements = {}
    taken = occupied(s) | {int(role['role_id'])}
    for g in s['unions'].values():
        for section in ('members', 'applications'):
            rows = g[section]
            for key, old in list(rows.items()):
                if old['id'] == int(role['role_id']) or not old.get('npc'):
                    continue
                resolved = npc_players.resolve(old['id'])
                entry = (npc_players.catalog()[resolved] if resolved else
                         choose(s, role['level'], 1, taken)[0])
                fresh = member(entry, now, old.get('rank', 5))
                # Social progress belongs to the save, combat identity to catalog.
                for field in ('contrib', 'totalcontrib', 'jointime', 'requested_at', 'apply_time'):
                    if field in old:
                        fresh[field] = old[field]
                taken.add(fresh['id'])
                replacements[str(old['id'])] = str(fresh['id'])
                del rows[key]
                rows[str(fresh['id'])] = fresh
        for row in g['forbidden']:
            key = replacements.get(str(row['id']))
            if key and key in g['members']:
                row.update({field: g['members'][key][field]
                            for field in ('id', 'name', 'head_type', 'level')})
    a = s.get('instances', {})
    t = a.get('team')
    if t:
        t['members'] = [replacements.get(str(v), str(v)) for v in t['members']]
        t['captain'] = int(replacements.get(str(t['captain']), t['captain']))
        t['applications'] = {replacements.get(str(k), str(k)): dict(v,
                              id=int(replacements.get(str(k), k)))
                             for k, v in t.get('applications', {}).items()}
        current = s['unions'].get(str(int(role.get('union_id', 0))), {})
        for key in t['applications']:
            if key in current.get('members', {}):
                t['applications'][key].update(current['members'][key])
    if 'appoint' in a:
        a['appoint'] = int(replacements.get(str(a['appoint']), a['appoint']))
    for field in ('member_contributions', 'train_damage'):
        if field in a:
            a[field] = {replacements.get(str(k), str(k)): v for k, v in a[field].items()}
            if field == 'train_damage':
                for k, row in a[field].items():
                    row['id'] = int(k)
    e = s.get('escort', {})
    e['requests'] = [int(replacements.get(str(v), v)) for v in e.get('requests', [])]
    e['issued'] = {replacements.get(str(k), str(k)): v for k, v in e.get('issued', {}).items()}
    if e.get('active'):
        book = e['active'].get('book', {})
        if book.get('protector_id'):
            book['protector_id'] = int(replacements.get(str(book['protector_id']), book['protector_id']))
    s['npc_players_version'] = 1


def recruit(role, s, g, now, r):
    """Four daily applicants let a new leader form a five-person dungeon party."""
    from .guild_offline import capacity
    if role['union_rank'] != 1 or g.get('players_recruit_day') == s['day']:
        return
    g['players_recruit_day'] = s['day']
    count = min(r.get('npc_recruit_daily', 4), max(0, capacity(g, r) - len(g['members']) - len(g['applications'])))
    for entry in choose(s, role['level'], count, occupied(s) | {int(role['role_id'])}):
        m = member(entry, now)
        m['requested_at'] = now
        g['applications'][str(m['id'])] = m
        s.setdefault('pending_notices', []).append(dict(event_id=7, result=1, role_id=m['id']))

