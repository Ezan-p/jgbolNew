"""Bounded, authoritative battle/event engine. All timing policies are inferred [B]."""
import copy
from fractions import Fraction as F
from . import combat as c, formation, summon, reborn_stars

RULAI = {int(r['level']): r for r in summon.rows('rulai_skill_base.csv')}


class Actions(list):
    def __init__(self):
        super().__init__()
        self.events = []
        self.damage_totals = {1: 0, 2: 0}
        self.final_hp = {}
        self.stop_reason = 'elimination'


def event_data(actions, fight_id):
    return dict({i: e for i, e in enumerate(getattr(actions, 'events', []), 1)}, fight_id=fight_id)


def event_packets(actions, fight_id):
    # Also clear the client's previous event cache when this fight has no effects.
    return [summon.event(121, event_data(actions, fight_id))]


def total_damage(actions, side=1):
    if isinstance(actions, Actions):
        return actions.damage_totals[side]
    return sum(sum(max(0, d) for d in a['damage_list']) for a in actions
               if a['is_src'] == (side == 1) and not a.get('self_use'))


class Battle:
    def __init__(self, role, units, rules, slots=8, extras=None, max_actions=None):
        self.sides = copy.deepcopy(units)
        self.rules = copy.deepcopy(rules['battle'])
        self.rules['multi_target_limit'] = self.rules['formation_target_limits'].get(str(slots), self.rules['multi_target_limit'])
        self.policy = self.rules['mechanics']
        self.slots = slots
        self.limit = min(max_actions or self.rules['max_actions'], self.rules['max_actions'])
        self.actions = Actions()
        self.round = 0
        self.event_bytes = 0
        for side_no, side in enumerate(self.sides, 1):
            side.sort(key=lambda u: u['order'])
            for u in side:
                u.update(side=side_no, shield=0, armor_break=0, revive_count=0)
                u['base_hp'] = u['max_hp']
                for stat in ('gongji', 'fangyu', 'magic'):
                    u['base_' + stat] = u[stat]
                if extras is not None and side_no == 2:
                    u['extras'] = extras.copy()
        reborn_stars.attach_combat_traits(role, self.sides[0])
        c.attach_essences(role, self.sides[0])
        home = role.get('activity', {}).get('home', {}).get('train', {})
        if home:
            from .activity_home import TRAIN
            bonuses = [tuple(map(F, TRAIN[i, home.get(str(i), {}).get('level', 0)]['worth'].split('|')))
                       if home.get(str(i), {}).get('level', 0) else (0, 0) for i in range(1, 5)]
            for u in self.sides[0]:
                u['training_bonuses'] = bonuses
        self.entry()
        self.initial = copy.deepcopy(self.sides)

    def entry(self):
        for side in self.sides:
            blessings = {}
            for u in side:
                if u['hp'] <= 0:
                    continue
                chance, rate, *_ = c.effect(u, 18)
                if rate and c.roll(chance):
                    alive = [v for v in side if v['hp'] > 0]
                    if alive:
                        target = alive[c.secrets.randbelow(len(alive))]
                        blessings[target['order']] = max(blessings.get(target['order'], 0), rate)
            for u in side:
                bonus = blessings.get(u['order'], 0)
                for stat in ('gongji', 'fangyu', 'magic'):
                    u[stat] = int(F(u['base_' + stat]) * (1 + bonus / 100))
                    u['base_' + stat] = u[stat]
                extra = int(F(u['base_hp']) * (bonus + c.effect(u, 13)[0]) / 100)
                if u['hp'] > 0:
                    u['max_hp'] += extra
                    u['hp'] += extra

    def alive(self, side):
        return [u for u in self.sides[side - 1] if u['hp'] > 0]

    def can_act(self):
        if len(self.actions) >= self.limit:
            self.actions.stop_reason = 'action_limit'
            return False
        if self.event_bytes >= self.policy['event_budget_bytes']:
            self.actions.stop_reason = 'event_budget'
            return False
        return True

    def logic(self, unit, kind):
        return unit.get('essence_ids', {}).get(kind, 10100 + kind) * 10 + 1

    def event(self, unit, logic, delta, index, field=65):
        if not delta:
            return
        event = dict(cur_action=index, logic_type=logic, who_use=unit['side'], self_use=True,
                     src_order=unit['order'], des_order=unit['order'], speak='',
                     skill_result_list=[dict(field=field, field_plus=int(delta), des_order=unit['order'])])
        self.actions.events.append(event)
        self.event_bytes += len(summon.lua(event).encode('utf-8')) + 10

    def row(self, actor, targets, skill=1, self_use=False):
        row = dict(self_use=self_use, skill_type=skill, is_src=actor['side'] == 1, result=0,
                   src_order=actor['order'], des_order=targets[0]['order'], cur_round=self.round,
                   damage_count=self.slots, damage_list=[0] * self.slots)
        self.actions.append(row)
        return row, len(self.actions)

    def heal(self, unit, amount, kind, index):
        if unit['hp'] <= 0:
            return
        gain = min(max(0, int(amount)), unit['max_hp'] - unit['hp'])
        unit['hp'] += gain
        self.event(unit, self.logic(unit, kind), gain, index)

    def revive(self, unit, index):
        if unit['hp']:
            return
        # Death clears temporary negative states whether or not resurrection succeeds.
        unit.pop('poison', None)
        unit.pop('attack_reduction', None)
        unit['armor_break'] = unit['shield'] = 0
        unit['fangyu'] = unit['base_fangyu']
        unit['gongji'] = unit['base_gongji']
        chance, rate = c.effect(unit, 19)
        tier = 'advanced' if unit.get('essence_ids', {}).get(19, 10119) >= 10200 else 'normal'
        if rate and unit['revive_count'] < self.policy[tier + '_revive_limit'] and c.roll(chance):
            unit['revive_count'] += 1
            unit['hp'] = max(1, int(F(unit['max_hp']) * rate / 100))
            self.event(unit, self.logic(unit, 19), unit['hp'], index)

    def lose_hp(self, unit, amount, source_side, index):
        hit = reborn_stars.combat_hit(max(0, int(amount)), unit['hp'], False, {}, unit.get('reborn_traits', {}))
        unit['hp'] -= hit
        self.actions.damage_totals[source_side] += hit
        return hit

    def shield_absorb(self, target, amount, index):
        absorbed = min(target['shield'], amount)
        target['shield'] -= absorbed
        if absorbed:
            self.event(target, 101203, absorbed, index, field=0)
            if not target['shield']:
                self.event(target, 101202, 1, index, field=0)
        return amount - absorbed

    def rulai(self, unit):
        level = max((lv for sk, lv in unit.get('skills', []) if sk == 21), default=0)
        return RULAI.get(level)

    def receive(self, target, amount, actor, row, index, fallen):
        amount = self.shield_absorb(target, amount, index)
        protectors = [u for u in self.alive(target['side']) if u is not target and self.rulai(u)]
        total = 0
        if protectors and amount:
            protector = max(protectors, key=lambda u: (int(self.rulai(u)['absorb_rate']), -u['order']))
            shared = int(F(amount) * int(self.rulai(protector)['absorb_rate']) / 100)
            amount -= shared
            loss = self.lose_hp(protector, self.shield_absorb(protector, shared, index), actor['side'], index)
            # Sharing is represented in the same target-side damage array: no double HP event.
            row['damage_list'][protector['order'] - 1] += loss
            total += loss
            if loss:
                self.event(protector, 101201, loss, index, field=0)
            if not protector['hp']:
                fallen.append(protector)
        hit = self.lose_hp(target, amount, actor['side'], index)
        row['damage_list'][target['order'] - 1] += hit
        total += hit
        was_dead = target['hp'] == 0
        if was_dead:
            fallen.append(target)
        # Resurrection is not a new received-hit trigger.
        cfg = self.rulai(target)
        if not was_dead and cfg and c.roll(self.policy['rulai_shield_probability']):
            weak = min(self.alive(target['side']), key=lambda u: (F(u['hp'], u['max_hp']), u['order']))
            # shield_rate is interpreted as HP capacity percent; duration is until consumed.
            capacity = int(F(weak['max_hp']) * int(cfg['shield_rate']) / 100)
            if capacity > weak['shield']:
                weak['shield'] = capacity
                self.event(weak, 101200, capacity, index, field=0)
        return total, was_dead

    def attack(self, actor, targets, skill=1, level=1, scale=100, kind='main'):
        targets = [u for u in targets if u['hp'] > 0]
        if not actor['hp'] or not targets or not self.can_act():
            return
        c.begin_action(actor, self.round)
        generation = actor['revive_count']
        row, index = self.row(actor, targets, skill)
        reactions = []
        fallen = []
        total = 0
        for target in targets:
            if not target['hp']:
                continue
            if kind == 'execute' and c.roll(c.effect(target, 14)[1]):
                continue
            # Debuffs precede damage; strongest armor break refreshes without stacking.
            c.after_hit(actor, target)
            raw = c.damage(actor, target, skill, level, self.rules, scale, settle=False)
            loss, died = self.receive(target, raw, actor, row, index, fallen)
            total += loss
            if not died and target['hp']:
                chance, rate, *_ = c.effect(actor, 16)
                if rate and c.roll(chance):
                    old = target.get('poison')
                    if old is None or rate >= old['rate']:
                        target['poison'] = dict(rate=rate, source_side=actor['side'], logic=self.logic(actor, 16) + 1)
                # Secondary actions never recurse into counter/combo/execute chains.
                chance, scale_back = c.effect(target, 3)
                if kind == 'main' and scale_back and c.roll(chance) and not c.roll(c.effect(actor, 4)[0]):
                    reactions.append((target, scale_back))
        # Resolve every target's damage before any resurrection, so one action's
        # wire damage array never exceeds that target's starting HP.
        for target in fallen:
            self.revive(target, index)
        self.heal(actor, F(total) * c.effect(actor, 5)[0] / 100, 5, index)
        for target, back_scale in reactions:
            if any(target is dead for dead in fallen):
                continue
            self.attack(target, [actor], scale=back_scale, kind='counter')
        if kind != 'main' or not actor['hp'] or actor['revive_count'] != generation:
            return
        alive = self.alive(3 - actor['side'])
        if not alive:
            return
        chance, combo_scale = c.effect(actor, 7)
        if combo_scale and c.roll(chance):
            self.attack(actor, alive[:1], scale=combo_scale, kind='combo')
        else:
            threshold, chance = c.effect(actor, 15)
            # Execute follows the original primary target; never retarget a dead one.
            target = targets[0]
            if target['hp'] and target['hp'] * 100 < target['max_hp'] * threshold and c.roll(chance):
                self.attack(actor, [target], kind='execute')

    def healing_spell(self, actor, skill, level):
        """[B] Placeholder formula 6 heals living allies; CSV probability stays zero."""
        if not self.can_act():
            return
        targets = self.alive(actor['side'])[:c.target_count(skill, self.rules)]
        _, index = self.row(actor, targets, skill, self_use=True)
        cfg = formation.SKILLS[skill]
        intensity = F(cfg['intensity']) + F(cfg['upgrade_plus']) * (level - 1)
        curve = self.rules['intensity_curve']
        k = F(str(curve['low_multiplier'])) + (intensity - curve['low']) * (
            F(str(curve['high_multiplier'])) - F(str(curve['low_multiplier']))) / (curve['high'] - curve['low'])
        amount = max(0, int(F(actor['magic']) * F(str(self.rules['spell_magic_ratio'])) * k
                            * F(2, c.target_count(skill, self.rules) + 1)))
        for target in targets:
            gain = min(amount, target['max_hp'] - target['hp'])
            target['hp'] += gain
            self.event(target, 0, gain, index)

    def upkeep(self):
        # Snapshot prevents a revived unit from receiving a second upkeep this round.
        for unit in [u for side in self.sides for u in side if u['hp'] > 0]:
            if not self.can_act() or not all(self.alive(s) for s in (1, 2)):
                return
            poison = unit.get('poison')
            if poison and c.roll(c.effect(unit, 17)[0]):
                unit.pop('poison')
                poison = None
            chance, rate = c.effect(unit, 10)
            healing = self.round >= 2 and unit['hp'] < unit['max_hp'] and rate and c.roll(chance)
            if not poison and not healing:
                continue
            # Dedicated zero-damage action anchors pre-turn HP events, including lethal poison.
            _, index = self.row(unit, [unit], self_use=True)
            if poison:
                amount = min(self.policy['poison_max_damage'], int(F(unit['base_hp']) * poison['rate'] / 100))
                loss = self.lose_hp(unit, amount, poison['source_side'], index)
                self.event(unit, poison['logic'], -loss, index)
                died = unit['hp'] == 0
                self.revive(unit, index)
                if died:
                    continue
            if healing:
                amount = F(unit['base_hp']) * rate / 100 * (1 + c.effect(unit, 14)[0] / 100)
                self.heal(unit, amount, 10, index)

    def run(self):
        while all(self.alive(s) for s in (1, 2)) and self.can_act():
            self.round += 1
            self.upkeep()
            for order in range(1, self.slots + 1):
                for side in (1, 2):
                    if not all(self.alive(s) for s in (1, 2)) or not self.can_act():
                        break
                    actor = next((u for u in self.alive(side) if u['order'] == order), None)
                    if actor:
                        sk, lv = c.select_skill(actor, self.rules)
                        if int(formation.SKILLS[sk]['formula']) == 6:
                            self.healing_spell(actor, sk, lv)
                        else:
                            self.attack(actor, self.alive(3 - side)[:c.target_count(sk, self.rules)], sk, lv)
        self.actions.final_hp = {s: {u['order']: u['hp'] for u in self.sides[s - 1]} for s in (1, 2)}
        hp = [sum(u['hp'] for u in side) for side in self.sides]
        maximum = [sum(u['max_hp'] for u in side) for side in self.sides]
        def stars(h, m):
            return 3 if h * 10 >= m * 7 else 2 if h * 10 >= m * 4 else 1
        compare = hp[0] * maximum[1] - hp[1] * maximum[0]
        if not hp[0] and not hp[1]:
            result = 0
        elif not hp[1]:
            result = stars(hp[0], maximum[0])
        elif not hp[0]:
            result = 7 - stars(hp[1], maximum[1])
        else:
            result = stars(hp[0], maximum[0]) if compare > 0 else 7 - stars(hp[1], maximum[1]) if compare < 0 else 0
        lineup = []
        for order in range(1, max((u['order'] for side in self.initial for u in side), default=0) + 1):
            row = {}
            for prefix, side in zip(('src', 'des'), self.initial):
                u = next((u for u in side if u['order'] == order), None)
                if u:
                    row.update({prefix + '_' + key: u[key] for key in ('type', 'evolve', 'hp', 'max_hp', 'magic', 'reborn')})
                    if prefix == 'des':
                        row['des_level'] = u['level']
            lineup.append(row)
        return result, lineup, self.actions
