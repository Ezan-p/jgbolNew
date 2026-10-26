"""渡劫 players catalog and power-bounded encounter variety, independent of 逐鹿."""
from functools import lru_cache
from . import npc_players, formation


@lru_cache(maxsize=1)
def catalog():
    result = {}
    for key, entry in npc_players.catalog().items():
        raw = npc_players.source_file(entry['source_file'])[key]
        if raw.get('battle_validation', {}).get('status') == 'replay_limit_observed':
            continue
        result[key] = npc_players.get(key)
    formation.require(bool(result), '渡劫NPC玩家配置为空')
    return result


def candidates(role, index, rules, excluded=()):
    own = max(1, sum(c.get('combat_power', 0) for c in role['corteges'] if 1 <= c.get('order', 0) <= 8))
    target = own * rules['power_percent'][index % 3] // 100
    excluded = set(excluded)
    pool = [n for n in catalog().values()
            if n['role']['level'] <= role['level'] and n['npc_id'] not in excluded]
    formation.require(bool(pool), '没有符合等级的渡劫NPC')
    pool.sort(key=lambda n: (abs(n['role']['role_combat_power']-target),
                             abs(n['role']['level']-role['level']), n['npc_id']))
    best = abs(pool[0]['role']['role_combat_power']-target)
    tolerance = max(1, target * rules['match_tolerance_percent'] // 100)
    return [n['npc_id'] for n in pool[:rules['match_candidates']]
            if abs(n['role']['role_combat_power']-target) <= best+tolerance]


def choose(role, index, rules, excluded=(), used=()):
    import secrets
    pool = candidates(role, index, rules, excluded)
    recent = set(role.get('activity', {}).get('rape_recent_npcs', []))
    # Never widen the strength window just to hide repetition in sparse pools.
    unused = [key for key in pool if key not in used]
    fresh = [key for key in unused if key not in recent]
    return secrets.choice(fresh or unused or pool)


def remember(role, keys, rules):
    history = role['activity'].setdefault('rape_recent_npcs', [])
    for key in keys:
        if key in history:
            history.remove(key)
        history.append(key)
    del history[:-rules['recent_npc_limit']]
