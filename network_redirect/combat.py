"""Shared damage reconstruction [B], based on 普通攻击与主动法术 V1.1.

Original skill/essence tables supply coefficients [A], not a proven server formula.
Fraction arithmetic avoids intermediate rounding (including the final floor).
"""
from fractions import Fraction as F
import secrets
from . import formation, summon, reborn_stars

ESSENCES = {int(r['id']): r for r in summon.rows('ext_skill.csv')}


def roll(percent):
    return percent > 0 and secrets.randbelow(1000000) < percent * 10000


def attach_essences(role, units):
    for unit in units:
        c = next((c for c in role.get('corteges', [])
                  if (c['id'] == unit['companion_id'] if unit.get('companion_id') else
                      c.get('order') == unit['order'] and c['type'] == unit['type'])), None)
        if not c:
            continue
        effects = unit.setdefault('essences', {})
        for item in role.get('attachments', []):
            row = ESSENCES.get(item['type_id'])
            if row and item.get('attach_type') == 5 and item.get('owner_id') == c['id']:
                unit.setdefault('essence_ids', {})[item['type_id'] % 100] = item['type_id']
                effects[item['type_id'] % 100] = tuple(
                    F(part.split('|')[item['level'] - 1].rstrip('%'))
                    for part in row['parameter'].split('/'))


def effect(unit, kind):
    values = unit.get('essences', {}).get(kind)
    if values is not None:
        return tuple(F(str(v)) for v in values)
    value = unit.get('extras', {}).get(10100 + kind, 0)
    if kind == 15:
        return F(value), F(100 if value else 0)
    if kind == 19:
        return F(100 if value else 0), F(value)
    if kind in (1, 4, 14, 16, 18):
        return F(0), F(0), F(0)
    return (F(100), F(value)) if kind in (2, 3, 6, 7, 10, 11) else (F(value),)


def target_count(skill_id, rules):
    skill = formation.SKILLS[skill_id]
    configured = rules['skill_target_limits'].get(str(skill_id),
        rules['multi_target_limit'] if int(skill['effect_target(1-single，2-multi)']) == 2 else 1)
    return min(configured, rules['multi_target_limit'])


def select_skill(actor, rules=None):
    for tid, level in actor['skills']:
        skill = formation.SKILLS[tid]
        if tid != 1 and int(skill['use_mode(1-active，2-passive)']) == 1:
            probability = actor.get('skill_probabilities', {}).get(tid, int(skill['use_probability']))
            if probability <= 0:
                continue  # Keep disabled/placeholder skills disabled, even with penetration.
            bonus = 0
            if rules and effect(actor, 9)[0]:
                tier = 'advanced' if actor.get('essence_ids', {}).get(9, 10109) >= 10200 else 'normal'
                bonus = rules['mechanics']['penetration_proc_bonus'][tier]
            if roll(min(100, probability + bonus)):
                return tid, level
    return 1, 1


def damage(actor, target, skill_id, level, rules, scale=100, *, settle=True):
    normal = skill_id == 1 or int(formation.SKILLS[skill_id]['formula']) == 1
    attack = F(actor['gongji'])
    power = attack if normal else attack * F(str(rules['spell_attack_ratio'])) + F(actor['magic']) * F(str(rules['spell_magic_ratio']))
    buffs = actor.get('training_bonuses', [(0, 0)] * 4)
    guards = target.get('training_bonuses', [(0, 0)] * 4)
    attack_rate, attack_flat = map(lambda v: F(str(v)), buffs[0 if normal else 2])
    guard_rate, guard_flat = map(lambda v: F(str(v)), guards[1 if normal else 3])
    if not normal:
        # Original tutorial limits spell training to the magic contribution [A].
        magic_power = F(actor['magic']) * F(str(rules['spell_magic_ratio']))
        trained_magic = max(0, magic_power * (1 + attack_rate / 100)
                            * max(0, 1 - guard_rate / 100) + attack_flat - guard_flat)
        power += trained_magic - magic_power
    defense = F(target['fangyu'])
    raw = max(power * F(rules['minimum_damage_percent'], 100), power - defense)
    if normal:
        chance, bonus = effect(actor, 11)
        if bonus and roll(chance):
            intimidation = effect(target, 1)
            bonus *= 1 - (intimidation[2] / 100 if len(intimidation) > 2 else 0)
            parry = effect(actor, 4)
            if effect(target, 3)[1] and len(parry) > 1:
                bonus *= 1 + parry[1] / 100
            raw *= 1 + bonus / 100
        chance, reduction = effect(target, 6)
        if reduction and roll(chance):
            raw *= 1 - reduction / 100
    else:
        skill = formation.SKILLS[skill_id]
        intensity = F(skill['intensity']) + F(skill['upgrade_plus']) * (level - 1)
        traits = actor.get('reborn_traits', {})
        intensity *= 1 + F(str(traits.get('awake_skills', {}).get(skill_id, 0))) / 100
        intensity = intensity * (1 + F(str(traits.get('spell_rate', 0))) / 100) + F(str(traits.get('spell_flat', 0)))
        curve = rules['intensity_curve']
        multiplier = F(str(curve['low_multiplier'])) + (intensity - curve['low']) * (F(str(curve['high_multiplier'])) - F(str(curve['low_multiplier']))) / (curve['high'] - curve['low'])
        raw *= max(0, multiplier) * F(2, target_count(skill_id, rules) + 1)
        resist = min(F(1), max(0, effect(target, 8)[0] / 100))
        pierce = min(F(1), max(0, effect(actor, 9)[0] / 100))
        raw *= 1 - resist * (1 - pierce)
    if normal:
        # Physical training modifies damage, not the attack/defense stats [A].
        raw = max(0, raw * (1 + attack_rate / 100) * max(0, 1 - guard_rate / 100)
                  + attack_flat - guard_flat)
    # Star critical/survival and HP clamp are applied before the single final floor.
    defend = target.get('reborn_traits', {})
    if not settle:
        defend = dict(defend, survival_count=0)
    return reborn_stars.combat_hit(max(0, raw * F(scale, 100)), target['hp'] if settle else 2147483647, normal,
        actor.get('reborn_traits', {}), defend)


def validate_rules(rules):
    import math
    require = formation.require
    require(rules.get('formula_revision') == 'candidate-v1.1', '未知战斗公式版本')
    for key in ('spell_attack_ratio', 'spell_magic_ratio'):
        value = rules.get(key)
        require(type(value) in (int, float) and math.isfinite(value) and value >= 0, '战斗配置无效：' + key)
    curve = rules.get('intensity_curve', {})
    require(all(type(curve.get(k)) in (int, float) and math.isfinite(curve[k]) for k in
                ('low', 'high', 'low_multiplier', 'high_multiplier')), '强度曲线配置无效')
    require(curve['high'] > curve['low'] and 0 <= curve['low_multiplier'] <= curve['high_multiplier'], '强度曲线范围无效')
    policy = rules.get('mechanics', {})
    require(policy.get('revision') == 'inferred-v2', '战斗事件配置版本无效')
    for key, lo, hi in [('poison_max_damage', 1, 10000), ('rulai_shield_probability', 0, 100),
                        ('normal_revive_limit', 1, 1), ('advanced_revive_limit', 2, 2),
                        ('event_budget_bytes', 1000, 12000)]:
        require(type(policy.get(key)) is int and lo <= policy[key] <= hi, '战斗事件配置无效：' + key)
    bonuses = policy.get('penetration_proc_bonus', {})
    require(set(bonuses) == {'normal', 'advanced'} and all(type(v) is int and 0 <= v <= 100
            for v in bonuses.values()), '破法概率配置无效')
    formations = rules.get('formation_target_limits', {})
    require(set(formations) == {'8', '9'} and all(type(v) is int and 1 <= v <= (4 if k == '8' else 9)
            for k, v in formations.items()), '阵容目标上限配置无效')
    limits = rules.get('skill_target_limits')
    require(isinstance(limits, dict) and all(str(k).isdigit() and int(k) in formation.SKILLS
        and type(v) is int and 1 <= v <= 9 for k, v in limits.items()), '技能目标上限配置无效')


def begin_action(actor, round_no):
    """[B] War intent uses completed pairs of rounds; intimidation lasts one action."""
    base = actor.setdefault('base_gongji', actor['gongji'])
    actor['gongji'] = max(0, F(base) * (1 + (round_no // 2) * effect(actor, 12)[0] / 100)
                          - F(base) * actor.pop('attack_reduction', 0) / 100)


def after_hit(actor, target):
    """[B] Apply pre-hit debuffs; strongest armor break refreshes without stacking."""
    intimidate = effect(actor, 1)
    if len(intimidate) > 1 and roll(intimidate[0]):
        target['attack_reduction'] = max(target.get('attack_reduction', 0), intimidate[1])
    chance, reduction = effect(actor, 2)
    if reduction and roll(chance):
        base = target.setdefault('base_fangyu', target['fangyu'])
        target['armor_break'] = max(target.get('armor_break', 0), reduction)
        target['fangyu'] = max(0, F(base) * (1 - target['armor_break'] / 100))
