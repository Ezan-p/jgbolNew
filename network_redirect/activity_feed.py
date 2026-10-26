"""1040 / event 43: original click score, explicit offline reward tiers."""
from . import formation, summon


def validate(rules):
    tiers = rules.get('feed_reward_tiers')
    formation.require(isinstance(tiers, list) and bool(tiers), '包子奖励档位缺失')
    previous_count = previous_strength = 0
    for row in tiers:
        formation.require(isinstance(row, dict) and set(row) == {'min_count', 'strength'}, '包子奖励档位格式错误')
        count, strength = row['min_count'], row['strength']
        formation.require(type(count) is int and previous_count < count <= rules['feed_max_count']
                          and type(strength) is int and previous_strength < strength <= 1000000,
                          '包子奖励档位必须递增且在有效范围内')
        previous_count, previous_strength = count, strength
    formation.require(tiers[0]['min_count'] == 1, '包子奖励须从一次有效点击开始')


def reward(count, rules):
    return next((row['strength'] for row in reversed(rules['feed_reward_tiers'])
                 if count >= row['min_count']), 0)


def best(role):
    return max(role.get('activity', {}).get('feed', {}).values(),
               key=lambda row: row['count'], default={'count': 0, 'strength': 0})


def champion_role(role, peers, today):
    # Only actual saves for this server day; never invent scores for NPCs.
    candidates = [p for p in [role] + list(peers or [])
                  if p.get('activity', {}).get('day') == today and best(p)['count'] > 0]
    if not candidates:
        return None
    def order(p):
        count = best(p)['count']
        times = [p.get('feed_time' + slot, 2147483647)
                 for slot, row in p['activity']['feed'].items() if row['count'] == count]
        return (-count, min(times), p['role_id'])
    return min(candidates, key=order)


def settle(role, req, now, rules, peers=None):
    from .activity import day, feed_data
    count = req['feed_count']
    formation.require(type(count) is int and 0 <= count <= rules['feed_max_count'], '包子数量超出有效范围')
    state = role['activity']
    result, strength = 1, best(role)['strength']
    if count:
        formation.require(state['day'] == day(now, rules), '包子活动日期已回退，请恢复本地时间')
        strength = 0
        second = (now + rules['timezone_offset_hours'] * 3600) % 86400
        slot = next((str(i) for i, (a, b) in enumerate(rules['feed_periods'], 1) if a <= second < b), None)
        if slot is None:
            result = 3
        elif slot in state['feed']:
            result = 4
        else:
            strength = reward(count, rules)
            role['strength'] += strength  # Original description: may exceed natural cap.
            state['feed'][slot] = dict(count=count, strength=strength)
            role['feed_time' + slot] = now
            result = 2
    winner = champion_role(role, peers, day(now, rules))
    if result == 2 and winner is role:
        # [B] The original 445 description names the board, but its award
        # timing is server-side. Local successful entry into first place counts.
        from . import achievements
        achievements.observe(role, 445, 1)
    return [summon.event(43, dict(
        feed_result=result, server_time=now, strength=strength,
        feed_data=feed_data(role, rules),
        feed_time=[dict(begin_seconds=a, end_seconds=b) for a, b in rules['feed_periods']],
        feed_champion=dict(name=winner['role_name'], count=best(winner)['count'])
            if winner else dict(name='', count=0),
        # Native strength means this settlement; personal-best display must
        # retain its own earned strength when the second run scores lower.
        personal_best_strength=best(role)['strength']))]
