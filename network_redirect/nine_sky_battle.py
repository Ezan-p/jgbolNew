"""Nine Sky random encounters using saved local NPC loadouts and real combat.

Encounter difficulty is fixed by the sky, independent of the player's power.
Reward granting belongs to activity_nine_sky's atomic roll transaction.
"""
import copy
from functools import lru_cache
import secrets

from . import combat_power, formation, journey, npc_players
from .combat_loadout import player_units


@lru_cache(maxsize=1)
def catalog():
    """Exclude snapshots already known to exceed the local replay limits."""
    result = {}
    for key, entry in npc_players.catalog().items():
        raw = npc_players.source_file(entry['source_file'])[key]
        if raw.get('battle_validation', {}).get('status') == 'replay_limit_observed':
            continue
        if any(1 <= c.get('order', 0) <= 8 for c in raw['role']['corteges']):
            result[key] = entry
    formation.require(bool(result), '九重天本地NPC配置为空')
    return result


@lru_cache(maxsize=128)
def template(key):
    # player_units attaches this NPC's own skills/essences/star/training traits.
    # Returned snapshots are copied before scaling or entering the battle.
    return player_units(npc_players.get(key)['role'])


def choose(s, target):
    """Prefer nearby native strength, never repeat a weekly identity early."""
    pool = catalog()
    history = s.setdefault('battle_seen', [])
    seen = set(history)
    eligible = [key for key in pool if key not in seen]
    if not eligible:
        # An exceptionally long week may exhaust all available NPCs. Restart
        # the deck, avoiding an immediate repeat of its final identity.
        last = history[-1] if history else None
        history.clear()
        eligible = [key for key in pool if key != last] or list(pool)
        s['battle_cycles'] = s.get('battle_cycles', 0) + 1
    eligible.sort(key=lambda key: (
        abs(pool[key]['profile']['role_combat_power'] - target), key))
    key = secrets.choice(eligible[:60])
    history.append(key)
    return key


def enemies(key, floor, r):
    """Preserve each loadout's proportions while scaling its four base stats."""
    army = copy.deepcopy(template(key))
    weights = formation.load_rules()['combat_weights']
    baseline = sum(combat_power.score_panel(unit, weights) for unit in army)
    formation.require(baseline > 0, '九重天NPC战斗属性无效')
    target = r['battle_floor_power'][floor - 1]
    for unit in army:
        for stat in formation.STATS:
            unit[stat] = max(1, unit[stat] * target // baseline)
        unit['max_hp'] = unit['hp']
    power = sum(combat_power.score_panel(unit, weights) for unit in army)
    return army, power


def reward(r):
    pick = secrets.randbelow(sum(row['weight'] for row in r['battle_pool']))
    for row in r['battle_pool']:
        if pick < row['weight']:
            return list(row['reward'])
        pick -= row['weight']


def encounter(role, s, r, floor=None):
    floor = s['floor'] if floor is None else floor
    formation.require(type(floor) is int and 1 <= floor <= 9, '九重天战斗层数无效')
    target = r['battle_floor_power'][floor - 1]
    key = choose(s, target)
    army, power = enemies(key, floor, r)
    ours = player_units(role)
    result, _, actions = journey.battle(role, {}, journey.load_rules(), units=(ours, army))
    win = 1 <= result <= 3
    profile = catalog()[key]['profile']
    record = dict(floor=floor, npc_id=key, name=profile['role_name'],
                  enemy_name=profile['role_name'], win=win, won=win, result=result,
                  rounds=getattr(actions, 'rounds', len(actions)),
                  enemy_power=power, target_power=target, enemy_count=len(army),
                  enemy_types=[unit['type'] for unit in army])
    s['battle_count'] = s.get('battle_count', 0) + 1
    s['battle_wins'] = s.get('battle_wins', 0) + int(win)
    s['last_battle'] = copy.deepcopy(record)
    return record, reward(r) if win else None
