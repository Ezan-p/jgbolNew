"""Deterministic permanent panel settlement; inferred policy, never official formula.

The breakdown is derived output only. Never use cached panel/source attributes as
inputs. Battle triggers and temporary scenario effects stay in combat_engine.
"""
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
import json
from pathlib import Path
import copy
import time
from . import summon

STATS = ('hp', 'gongji', 'fangyu', 'magic')
ATTR = {1: 'gongji', 2: 'fangyu', 3: 'hp', 4: 'magic'}
LIMIT = 2147483647  # 1032 signed int32 is narrower than the snapshot fields.
DEFAULT_POLICY = dict(title=True, pet=True, cheer=True, explicit_channels=True)
TITLES = {int(r['title_id']): r for r in summon.rows('title_config.csv')}
PETS = {int(r['type_id']): {k.split('(')[0]: v for k, v in r.items()}
        for r in summon.rows('animal_base.csv')}
CHEER = {(int(r['cheer_order']), int(r['level'])): r for r in summon.rows('cortege_cheer_config.csv')}
HOME_TRAIN = {(int(r['train_type']), int(r['level'])): r
              for r in summon.rows('hole/hole_train_config.csv')}
DIRECTIONS = ('heaven', 'earth', 'shake', 'sunda', 'water', 'fire', 'hill', 'pool')


ATTRIBUTE_STAGES = ['base_and_culture', 'evolution', 'equipment', 'passive_skills', 'rebirth',
                    'awakening_and_stars', 'fates_and_advance', 'collection_role_and_home',
                    'title', 'home_training', 'pet', 'cheer', 'explicit_channels']

SCORE_VERSION = '1.1'
ESSENCE_CONFIG = json.loads((Path(__file__).resolve().parents[1] /
                            'server_config/essence_power_v1_1.json').read_text())
ESSENCE_SCORES = {int(k): v for k, v in ESSENCE_CONFIG['scores'].items()}
ESSENCE_PARAMS = {int(r['id']): r['parameter'] for r in summon.rows('ext_skill.csv')}
if (ESSENCE_CONFIG.get('version') != SCORE_VERSION or ESSENCE_CONFIG.get('mode') != 'inferred'
        or set(ESSENCE_SCORES) != set(range(10101, 10120)) | set(range(10201, 10220))
        or any(len(v) != 5 or any(type(n) is not int or n < 0 for n in v) for v in ESSENCE_SCORES.values())):
    raise ValueError('精魄V1.1评分表须包含38种精魄的190项非负整数评分')


def essence_score(role, c):
    """V1.1 fixed scores; combat effects never get applied to permanent stats here."""
    from .fate_rebuild import essence_slots
    slots = essence_slots(c)
    candidates = []
    for item in role.get('attachments', []):
        kind, level, pos = item.get('type_id'), item.get('level'), item.get('ext_skill_pos')
        if (item.get('attach_type') != 5 or item.get('owner_id') != c['id']
                or kind not in ESSENCE_SCORES or type(level) is not int or not 1 <= level <= 5
                or type(pos) is not int or pos not in slots or item.get('count', 0) <= 0):
            continue
        candidates.append(dict(id=item['id'], type_id=kind, level=level, slot=pos,
                               family=kind % 100, base=ESSENCE_SCORES[kind][level - 1]))
    # Corrupt duplicate slots/families: deterministic strongest-first selection.
    chosen, occupied = {}, set()
    for item in sorted(candidates, key=lambda x: (-x['base'], x['id'])):
        if item['family'] not in chosen and item['slot'] not in occupied:
            chosen[item['family']] = item
            occupied.add(item['slot'])
    def rate(family, parameter):
        item = chosen[family]
        raw = ESSENCE_PARAMS[item['type_id']].split('/')[parameter].split('|')[item['level'] - 1]
        return Decimal(raw.rstrip('%')) / 100
    def rounded(value):
        return int(value.to_integral_value(rounding=ROUND_HALF_UP))
    corrections = dict(lucky_heal=0, parry_assault=0, combo_execute=0)
    if 14 in chosen and 10 in chosen:
        corrections['lucky_heal'] = rounded(rate(14, 0) * chosen[10]['base'])
    if 4 in chosen and 11 in chosen:
        corrections['parry_assault'] = rounded(Decimal('0.30') * rate(4, 1) * chosen[11]['base'])
    if 7 in chosen and 15 in chosen:
        corrections['combo_execute'] = -rounded(rate(7, 0) * chosen[15]['base'])
    base = sum(x['base'] for x in chosen.values())
    return dict(version=SCORE_VERSION, selected=sorted(chosen.values(), key=lambda x: x['family']),
                base=base, corrections=corrections, total=base + sum(corrections.values()))


def score_panel(panel, weights, essence=0):
    return bounded(sum(Decimal(panel[s]) * Decimal(str(weights[s])) for s in STATS) + essence)


def floor(value):
    return int(Decimal(value).to_integral_value(rounding=ROUND_FLOOR))


def bounded(value):
    return max(0, min(LIMIT, floor(value)))


def record(trace, stage, values):
    # Exact decimal cumulative subtotals avoid float noise in saved explanations.
    trace[stage] = {s: str(values[s]) for s in STATS}


def add_title(role, values, now):
    row = TITLES.get(role.get('title_id', 0))
    if not row or now < role.get('title_begintime', 0):
        return
    end = role.get('title_endtime', 0)
    if (end and now >= end) or (int(row['category(1permanent|2tmp)']) == 2 and not end):
        return
    for stat in filter(None, row['plus_list'].split('|')):
        if int(stat) in ATTR:
            values[ATTR[int(stat)]] += Decimal(row['plus_value'])


def add_pet(role, c, values):
    if not 1 <= c.get('order', 0) <= 8:
        return
    pets = role.get('activity', {}).get('home', {}).get('pets', [])
    pet = next((p for p in pets if p.get('order') == 1), None)
    if not pet or pet['type_id'] not in PETS:
        return
    from . import pets as rules
    row = PETS[pet['type_id']]
    main = int(row['main_type'])
    control = rules.CONTROL[main, pet.get('quality', 1)]
    star = pet.get('star_level', 0)
    train = rules.STAR[star]
    growth = pet.get('grow_values', [int(row['base_' + ATTR[n]]) for n in range(1, 5)])
    stages = pet.get('train_levels', [0] * 4)
    if len(growth) != 4 or len(stages) != 4:
        raise ValueError('灵兽成长与培养属性必须有四项')
    rates = rules.load_rules()['plus_rate_list']
    attrs = {n: Decimal(str(growth[n-1])) * pet.get('level', 1) * Decimal(str(rates[n-1])) for n in range(1, 5)}
    stars = dict(tuple(map(int, pair.split('|'))) for pair in train['star_plus'].split('/'))
    previous = sum(Decimal(rules.STAR[n]['each_stage_plus'])*4 for n in range(star))
    # Original plus_order is a list of formation-position/attribute pairs.
    for direction, entry in enumerate(row['plus_order'].split('/'), 1):
        if direction > int(control['max_open_pos']):
            break
        pos, stat = map(int, entry.split('|'))
        if pos != c['order']:
            continue
        value = attrs[stat]
        if control['open_special'] == 'Y':
            for special in row['special_property'].split('/'):
                target, source, _, divisor = map(int, special.split('|'))
                if target == pos and source in attrs and divisor:
                    value += attrs[source] / divisor
        rate = previous + Decimal(train['each_stage_plus']) * stages[direction-1]
        values[ATTR[stat]] += floor(value * (1 + rate/100) + stars.get(direction, 0))


def add_cheer(role, c, values, pending):
    if 'cheer_pending' in role:
        from .cheer import bonuses
        bonuses(role, c, values, pending)
        return
    # Legacy external callers without migrated Bagua state.
    order = c['order']
    level = role.get('cheer_' + DIRECTIONS[order - 1] + '_level', 1)
    supporters = [x for x in role['corteges'] if not x.get('order')
                  and x.get('cheer_order') == order and x['id'] in pending]
    if not supporters:
        return
    supporter = min(supporters, key=lambda x: x['id'])
    for stat, column in zip(STATS, ('maxhp_plus', 'gongji_plus', 'fangyu_plus', 'maxmagic_plus')):
        rate = sum((Decimal(CHEER[order, n][column]) for n in range(1, min(10, level) + 1)
                    if (order, n) in CHEER), Decimal(0))
        values[stat] += pending[supporter['id']][stat] * rate


# Source channels for missing producers. Explicit inputs live under
# combat_sources, NOT on output fields; this prevents feeding derived caches back.
FLAT_CHANNELS = {'cortege', 'elite', 'goss_cortege', 'goss_equip', 'goss_skill',
                 'free_order', 'cheer_skill'}
RATE_CHANNELS = {'genius', 'fam', 'prey', 'goss', 'special_attack'}


def add_channels(role, c, values):
    for owner in (role, c):
        sources = owner.get('combat_sources', {})
        for name, source in sources.items():
            if name not in FLAT_CHANNELS | RATE_CHANNELS:
                raise ValueError('未知战力来源: ' + name)
            if not isinstance(source, dict) or set(source) - set(STATS):
                raise ValueError('战力来源只能包含四维属性')
            for value in source.values():
                if isinstance(value, bool) or not isinstance(value, (int, float, str)):
                    raise ValueError('战力来源数值无效')
                try:
                    valid = Decimal(str(value)).is_finite()
                except ArithmeticError:
                    valid = False
                if not valid:
                    raise ValueError('战力来源数值须为有限数')
        for stat in STATS:
            flat = sum((Decimal(str(v.get(stat, 0))) for k, v in sources.items() if k in FLAT_CHANNELS), Decimal(0))
            rate = sum((Decimal(str(v.get(stat, 0))) for k, v in sources.items() if k in RATE_CHANNELS), Decimal(0))
            # Explicit percentage channels use percent units, never cached plus_rate.
            values[stat] = values[stat] * (1 + rate / 100) + flat


def explain(role, rules, now=None):
    """Read-only diagnostic; input role, inventory and historical peak stay untouched."""
    detached = copy.deepcopy(role)
    recalculate(detached, rules, now)
    return detached['combat_power_breakdown']


def recalculate(role, rules, now=None):
    """[B] Server formula using [A] base/growth/equipment/fate coefficients."""
    from . import formation as f, reborn, reborn_stars, immortal, spirit_array
    immortal.collection_bonuses(role)
    BASES, SKILLS, ITEMS, FATES = f.BASES, f.SKILLS, f.ITEMS, f.FATES
    BASE_COLUMNS, GROWTH_COLUMNS = f.BASE_COLUMNS, f.GROWTH_COLUMNS
    equip_effect, skill_effect, advance_worth = f.equip_effect, f.skill_effect, f.advance_worth
    now = int(time.time()) if now is None else now
    policy = dict(DEFAULT_POLICY, **rules.get('combat_power', {}))
    reports = {}
    pending = {}

    active_types = {c['type'] for c in role['corteges'] if c.get('order', 0) or c.get('cheer_order', 0)}
    for c in role['corteges']:
        base = BASES.get(c['type'])
        if not base:
            continue
        values = {s: Decimal(base[b]) + Decimal(base[g]) * (c['level'] - 1) + c.get(s + '_plus', 0)
                  for s, b, g in zip(STATS, BASE_COLUMNS, GROWTH_COLUMNS)}
        from . import fate_rebuild
        fate_rebuild.base_bonuses(c, base, values)
        trace = {}
        record(trace, 'base_and_culture', values)
        # [A] feishengUI.createCharInfo:453-556: floor(growth * 3) per
        # evolution, rounded BEFORE multiplying by the evolution count.
        # Keep this separate from trained potential so recycling removes it
        # and repeated settlement never compounds previously stored panels.
        for stat, growth in zip(STATS, GROWTH_COLUMNS):
            values[stat] += floor(Decimal(base[growth]) * 3) * c.get('evolve_level', 0)
        record(trace, 'evolution', values)
        spirit_array.base_bonuses(role, c, values)
        ling = spirit_array.effects(role) if 1 <= c.get('order', 0) <= 8 else {}
        equipped = [i for i in role['attachments'] if
                    (i.get('innate_owner_id') == c['id']) or
                    (not i.get('innate_owner_id') and 1 <= c.get('order', 0) <= 8
                     and i.get('equip_order') == c['order'])]
        extra_rates = {s: Decimal(0) for s in STATS}
        passive_rates = {s: Decimal(0) for s in STATS}
        for item in equipped:
            if item['attach_type'] == 5 and item['type_id'] in ITEMS and int(ITEMS[item['type_id']]['main_type']) in (1, 2, 3):
                item['effect_value'] = equip_effect(item)
                values[{1: 'gongji', 2: 'fangyu', 3: 'hp'}[int(ITEMS[item['type_id']]['main_type'])]] += Decimal(item['effect_value']) * (1 + ling.get({1:7, 2:8, 3:9}[int(ITEMS[item['type_id']]['main_type'])], Decimal(0))/100)
                extra_rates[{1: 'gongji', 2: 'fangyu', 3: 'hp'}[int(ITEMS[item['type_id']]['main_type'])]] += advance_worth(item)[2]
            elif item['attach_type'] == 6 and item['type_id'] in SKILLS:
                item['effect_value'] = skill_effect(item)
                cfg = SKILLS[item['type_id']]
                if int(cfg['use_mode(1-active，2-passive)']) == 2:
                    field = int(cfg['effect_field(1-gongji，2-fangyu，3-magic，4-intensity，5-hp)'])
                    if field in (1, 2, 3, 5):
                        s = {1: 'gongji', 2: 'fangyu', 3: 'magic', 5: 'hp'}[field]
                        passive_rates[s] += Decimal(item['effect_value']) / 100 * (1 + ling.get({1:5, 2:6, 3:0, 5:10}[field], Decimal(0))/100)
                    from .skill_insight import hp_percent
                    passive_rates['hp'] += hp_percent(item) / 100
        record(trace, 'equipment', values)
        for stat in STATS:
            values[stat] *= 1 + passive_rates[stat]
        record(trace, 'passive_skills', values)
        reborn.bonuses(role, c, values, equipped)
        record(trace, 'rebirth', values)
        reborn_stars.bonuses(role, c, values)
        fate_rebuild.bonuses(c, values)
        record(trace, 'awakening_and_stars', values)
        rates = {s: 0 for s in STATS}
        if c.get('order', 0):
            for fate in FATES:
                if int(fate['cortege_type[effected_cortege]']) != c['type']:
                    continue
                targets = set(map(int, fate['target_object_type[1/2/3]'].split('/')))
                kind = int(fate['tartege_type[4-cortege/5-equip/6-skill]'])
                available = active_types if kind == 4 else {i['type_id'] for i in equipped if i['attach_type'] == kind}
                if targets <= available:
                    s = {1: 'hp', 2: 'magic', 3: 'gongji', 4: 'fangyu'}[int(fate['effect_field[1-maxhp/2-maxmagic/3-gongji/4-fangyu]'])]
                    rates[s] += int(fate['effect_value'])
        trace['advance_extra_base'] = {s: str(values[s]) for s in STATS}
        trace['advance_extra_rates'] = {s: str(extra_rates[s]) for s in STATS}
        for s in STATS:
            values[s] *= 1 + Decimal(rates[s]) / 100 + extra_rates[s]
        record(trace, 'fates_and_advance', values)
        pending[c['id']] = values
        reports[str(c['id'])] = trace
    # Two passes: support never reads last settlement's panel or other support output.
    for c in role['corteges']:
        if c['id'] not in pending:
            continue
        values = pending[c['id']].copy()
        trace = reports[str(c['id'])]
        for s in STATS:
            values[s] = Decimal(floor(values[s]))
            values[s] += role.get('collection_bonuses', {}).get(s, 0)
            values[s] += role.get({'hp':'max_hp_plus','magic':'max_magic_plus'}.get(s,s+'_plus'), 0)
        values['hp'] += role.get('hole_hp_plus', 0)
        record(trace, 'collection_role_and_home', values)
        if policy['title']:
            add_title(role, values, now)
        record(trace, 'title', values)
        # [A] newbie_content17 rows 11–14 describe damage modifiers, not panel
        # attack/defence. All four cultivation effects are applied in combat;
        # applying the first two here would count them twice and alter spells.
        record(trace, 'home_training', values)
        if policy['pet']:
            add_pet(role, c, values)
        record(trace, 'pet', values)
        if policy['cheer'] and 1 <= c.get('order', 0) <= 8:
            add_cheer(role, c, values, pending)
        record(trace, 'cheer', values)
        if policy['explicit_channels']:
            add_channels(role, c, values)
        record(trace, 'explicit_channels', values)
        spirit_array.final_bonuses(role, c, values)
        record(trace, 'spirit_array', values)
        trace['source_inputs'] = copy.deepcopy({'role': role.get('combat_sources', {}),
                                                 'companion': c.get('combat_sources', {})})
        for s in STATS:
            c[s] = bounded(values[s])
        trace['essence'] = essence_score(role, c)
        c['combat_power'] = score_panel(c, rules['combat_weights'], trace['essence']['total'])
        trace['panel'] = {s: c[s] for s in STATS}
        trace['combat_power'] = c['combat_power']
    members = [c for c in role['corteges'] if 1 <= c.get('order', 0) <= 8]
    role['role_combat_power'] = bounded(sum(c.get('combat_power', 0) for c in members))
    role['max_combat_power'] = max(bounded(role.get('max_combat_power', 0)), role['role_combat_power'])
    role['combat_power_breakdown'] = dict(mode='inferred', version=2, attribute_policy=copy.deepcopy(rules['attribute_policy']), scoring_version=SCORE_VERSION, companions=reports,
        member_ids=[c['id'] for c in members], total=role['role_combat_power'],
        maximum=role['max_combat_power'], weights=dict(rules['combat_weights']))
