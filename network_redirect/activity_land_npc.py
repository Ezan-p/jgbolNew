"""Local player substitutes for 逐鹿; immutable catalog, account-local behavior."""
import copy
from functools import lru_cache
from . import activity as a, formation, combat, reborn_stars, npc_players


@lru_cache(maxsize=1)
def catalog():
    result = {}
    for key, entry in npc_players.catalog().items():
        raw = npc_players.source_file(entry['source_file'])[key]
        if raw.get('battle_validation', {}).get('status') == 'replay_limit_observed':
            continue
        result[key] = npc_players.get(key)
    a.require(bool(result), '逐鹿NPC配置为空')
    return result


def units(key, count):
    role = catalog()[key]['role']
    result = []
    # Preserve original formation positions, equipment, skills and combat traits.
    for c in sorted(role['corteges'], key=lambda c: c.get('order', 0)):
        if not 1 <= c.get('order', 0) <= count:
            continue
        u = dict(companion_id=c['id'], type=c['type'], order=c['order'], level=c['level'],
                 evolve=c.get('evolve_level', 0), reborn=c.get('reborn_layer', 0),
                 max_hp=c['hp'], **{k:c[k] for k in formation.STATS})
        u['skills'] = [(i['type_id'], i['level']) for i in role['attachments']
                      if i['attach_type'] == 6 and i.get('equip_order') == c['order'] and i.get('equip_pos', 0)>0]
        result.append(u)
    combat.attach_essences(role, result)
    reborn_stars.attach_combat_traits(role, result)
    return result


def power(n, count):
    return sum(c['combat_power'] for c in n['role']['corteges'] if 1 <= c.get('order', 0) <= count)


def choose(role, s, index=0, fixed=False, excluded=()):
    count = s['grid_count']
    if fixed:
        level = (24, 50, 70, 90)[s['map_level']-1]
        pool = [n for n in catalog().values() if n['role']['level'] == level and n['tier'] == ('T5','T4','T3')[index%3] and n['npc_id'] not in excluded]
        return sorted(pool, key=lambda n:n['npc_id'])[s['day']%len(pool)]['npc_id']
    own = sum(c.get('combat_power', 0) for c in role['corteges'] if 1 <= c.get('order', 0) <= count)
    target = max(1, own) * (55, 80, 105)[index%3] // 100
    pool = [n for n in catalog().values() if n['role']['level'] <= role['level'] and n['npc_id'] not in excluded]
    pool.sort(key=lambda n:(abs(power(n,count)-target),n['npc_id']))
    # Alternate equally useful archetypes without changing the actual stats.
    return pool[min(s.get('travel_count',0)%2, len(pool)-1)]['npc_id']


def view(key, count, ident, soul=0):
    n = catalog()[key]; role=n['role']; army=units(key,count); head=army[0]
    return dict(id=ident, npc_id=key, npc_player_id=role['role_id'], object_type=1, type_id=head['type'], head_type=head['type'],
                name=role.get('role_name',role.get('name','离线修士')), union_name='离线修士', cortege_layer=head['reborn'],
                cortege_count=len(army), fight_power=power(n,count), power=power(n,count),
                expect_soul=soul, level=role['level'], had_soulcount=0)


def roster(role, s):
    if 'companions' not in s:
        keys = []
        for i in range(3):keys.append(choose(role,s,i,excluded=keys))
        s['companions'] = keys
    keys = s['companions']
    # Stable IDs distinct from real accounts and the other offline activities.
    return [view(k,s['grid_count'],940001+i) for i,k in enumerate(keys)]


def migrate(role,s):
    """Keep saved scene IDs, pending opponents and already accepted teammates."""
    if s.get('players_version') == 1:return
    known=[]
    team=s.get('team')
    if team:known=team['members']+team['applications']
    keys=[]
    for i in range(3):
        old=next((m.get('npc_id') for m in known if m['id']==940001+i),None)
        keys.append(old if old in catalog() and old not in keys else choose(role,s,i,excluded=keys))
    s['companions']=keys
    for m in list(s.get('travel') or [])+known:
        if m.get('npc_id') in catalog():
            m.update(view(m['npc_id'],s['grid_count'],m['id'],m.get('expect_soul',0)))
    for t in s.get('towers',{}).values():
        t.setdefault('npc_id',choose(role,s,(t['position']-1)%3,fixed=True))
    competitors(s)
    s['players_version']=1


def competitors(s):
    if 'competitors' not in s:
        pool = sorted((n for n in catalog().values() if n['role']['level'] >= 38),
                      key=lambda n:(n['role']['level'],power(n,8),n['npc_id']))
        s['competitors'] = [pool[i*(len(pool)-1)//59]['npc_id'] for i in range(60)]
    return [catalog()[key] for key in s['competitors']]


def ranking(role,s,hell,flag,now=None,r=None,final=False):
    rows=[]
    elapsed = 7*86400 if final or now is None else max(0,min(7*86400,
        now-((s['week']*7+4)*86400-r['timezone_offset_hours']*3600)))
    for n in competitors(s):
        # Simulated progress is a design rule; never presented as online results.
        layer=min(64,max(1,n['role']['level']//2+(5-int(n['tier'][1]))*7))
        inv=max(0,layer-12)
        daily=100+n['role']['level']*5+(5-int(n['tier'][1]))*100
        rows.append(dict(id=n['role']['role_id'],name=n['role']['name'],layer=inv if hell else layer,
                         inv_layer=inv,score=(inv if hell else layer)*2100,
                         soul=daily*elapsed//86400,order=0))
    history=s['inv_history' if hell else 'history']
    mine=dict(id=role['role_id'],name=role.get('role_name',role.get('name','离线修士')),layer=s['inv_boss_layer' if hell else 'boss_layer'],
              inv_layer=s['inv_boss_layer'],score=sum(v['score'] for v in history.values()),soul=s.get('week_soul',0),order=0)
    rows.append(mine)
    rows.sort(key=lambda v:(-v['layer'], -v['score'],v['id']) if flag==1 or hell else (-v['soul'],v['id']))
    for i,row in enumerate(rows,1):row['order']=i
    return rows[:50],mine


def inspection(role,ident):
    """Return only known, current local participants; never look up real accounts."""
    from . import summon, cheer
    s=role['activity'].get('land')
    if not s:return None
    candidates=list(s.get('travel') or [])
    if s.get('team'):candidates+=s['team']['members']+s['team']['applications']
    candidates+=roster(role,s)
    for t in s.get('towers',{}).values():
        if t.get('npc_id'):candidates.append(dict(id=940100+t['id'],npc_id=t['npc_id']))
    target=next((m for m in candidates if m['id']==ident and m.get('npc_id')),None)
    if not target:return None
    from . import npc_players
    return summon.event(11, npc_players.inspection_data(catalog()[target['npc_id']], scene_id=ident, count=s['grid_count']))
