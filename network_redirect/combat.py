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
                  if c.get('order') == unit['order'] and c['type'] == unit['type']), None)
        if not c:
            continue
        effects = unit.setdefault('essences', {})
        for item in role.get('attachments', []):
            row = ESSENCES.get(item['type_id'])
            if row and item.get('attach_type') == 5 and item.get('owner_id') == c['id']:
                effects[item['type_id'] % 100] = tuple(
                    F(part.split('|')[item['level'] - 1].rstrip('%'))
                    for part in row['parameter'].split('/'))


def effect(unit, kind):
    values = unit.get('essences', {}).get(kind)
    if values is not None:
        return values
    value = unit.get('extras', {}).get(10100 + kind, 0)
    return (F(100), F(value)) if kind in (2, 3, 6, 7, 10, 11) else (F(value),)


def target_count(skill_id, rules):
    skill = formation.SKILLS[skill_id]
    return rules['skill_target_limits'].get(str(skill_id),
        rules['multi_target_limit'] if int(skill['effect_target(1-single，2-multi)']) == 2 else 1)


def select_skill(actor):
    for tid, level in actor['skills']:
        skill = formation.SKILLS[tid]
        if tid != 1 and int(skill['use_mode(1-active，2-passive)']) == 1:
            if roll(actor.get('skill_probabilities', {}).get(tid, int(skill['use_probability']))):
                return tid, level
    return 1, 1


def damage(actor, target, skill_id, level, rules, scale=100):
    normal = skill_id == 1
    attack = F(actor['gongji'])
    power = attack if normal else attack * F(str(rules['spell_attack_ratio'])) + F(actor['magic']) * F(str(rules['spell_magic_ratio']))
    buffs = actor.get('training_bonuses', [(0, 0)] * 4)
    guards = target.get('training_bonuses', [(0, 0)] * 4)
    rate, flat = buffs[0 if normal else 2]
    power = power * (1 + F(rate, 100)) + flat
    defense = F(target['fangyu'])
    rate, flat = guards[1 if normal else 3]
    defense = defense * (1 + F(rate, 100)) + flat
    raw = max(power * F(rules['minimum_damage_percent'], 100), power - defense)
    if normal:
        chance, bonus = effect(actor, 11)
        if roll(chance):
            intimidation = effect(target, 1)
            bonus *= 1 - (intimidation[2] / 100 if len(intimidation) > 2 else 0)
            parry = effect(actor, 4)
            if effect(target, 3)[1] and len(parry) > 1:
                bonus *= 1 + parry[1] / 100
            raw *= 1 + bonus / 100
        chance, reduction = effect(target, 6)
        if roll(chance):
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
    # Star critical/survival and HP clamp are applied before the single final floor.
    return reborn_stars.combat_hit(max(0, raw * F(scale, 100)), target['hp'], normal,
        actor.get('reborn_traits', {}), target.get('reborn_traits', {}))


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
    limits = rules.get('skill_target_limits')
    require(isinstance(limits, dict) and all(str(k).isdigit() and int(k) in formation.SKILLS
        and type(v) is int and 1 <= v <= 8 for k, v in limits.items()), '技能目标上限配置无效')


def begin_action(actor, round_no):
    """[B] War intent uses completed pairs of rounds; intimidation lasts one action."""
    base = actor.setdefault('base_gongji', actor['gongji'])
    actor['gongji'] = max(0, F(base) * (1 + (round_no // 2) * effect(actor, 12)[0] / 100)
                          - F(base) * actor.pop('attack_reduction', 0) / 100)


def after_hit(actor, target):
    """[B] Debuffs apply to subsequent actions; strongest armor break refreshes."""
    intimidate = effect(actor, 1)
    if len(intimidate) > 1 and roll(intimidate[0]):
        target['attack_reduction'] = max(target.get('attack_reduction', 0), intimidate[1])
    chance, reduction = effect(actor, 2)
    if reduction and roll(chance):
        base = target.setdefault('base_fangyu', target['fangyu'])
        target['armor_break'] = max(target.get('armor_break', 0), reduction)
        target['fangyu'] = max(0, F(base) * (1 - target['armor_break'] / 100))
