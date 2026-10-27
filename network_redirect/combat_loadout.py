"""Attach each combatant's owner-scoped battle bonuses once to its snapshot.

Permanent equipment/passive/fate/pet values already belong to the panel. This
module only carries essence, star, cultivation and spirit-array combat traits.
"""
from fractions import Fraction
from . import combat, reborn_stars, spirit_array


def equipped_skills(role, order, *, companion_id=None):
    """The original three equipment slots determine active-skill priority."""
    equipped = [item for item in role.get('attachments', []) if item.get('attach_type') == 6
                and item.get('equip_pos', 0) > 0 and
                (order and item.get('equip_order') == order or
                 companion_id and item.get('innate_owner_id') == companion_id)]
    return [(item['type_id'], item['level']) for item in
            sorted(equipped, key=lambda item: (item['equip_pos'], item.get('id', 0)))]


def attach_owned_bonuses(role, units):
    roster = role.get('corteges', [])
    home = role.get('activity', {}).get('home', {}).get('train', {})
    selected = []
    for unit in units:
        if unit.get('_combat_loadout_attached'):
            continue
        cid = unit.get('companion_id')
        owner = next((c for c in roster if c['id'] == cid), None) if cid else next(
            (c for c in roster if c.get('order') == unit['order'] and c['type'] == unit['type']), None)
        # Synthetic fixtures can specify role-wide effects without a roster;
        # explicit companion IDs always require a matching owner.
        synthetic = not cid and 'corteges' not in role and bool(home or role.get('spirit_array'))
        if owner is not None or synthetic:
            selected.append(unit)
    if not selected:
        return
    combat.attach_essences(role, selected)
    reborn_stars.attach_combat_traits(role, selected)
    if home:
        from .activity_home import TRAIN
        bonuses = [tuple(map(Fraction, TRAIN[i, home.get(str(i), {}).get('level', 0)]['worth'].split('|')))
                   if home.get(str(i), {}).get('level', 0) else (Fraction(0), Fraction(0))
                   for i in range(1, 5)]
        for unit in selected:
            unit['training_bonuses'] = bonuses.copy()
    spirit_array.attach_combat(role, selected)
    for unit in selected:
        unit['_combat_loadout_attached'] = True


def player_units(role):
    """Immutable eight-slot snapshot, usable on either side or before re-slotting."""
    from . import journey
    units = journey.fighters(role, dict(cortege_list='1001|1'))[0]
    attach_owned_bonuses(role, units)
    return units
