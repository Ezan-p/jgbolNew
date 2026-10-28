"""Original novice book catalogue/protocol [A], explicit offline policies [B]."""
import json
from pathlib import Path
from . import formation, journey, summon
from .protocol import decode, encode

ROOT = Path(__file__).resolve().parents[1]
CATALOG = {int(row['stage']): row for row in summon.rows('task_guide_prize.csv')}
ORDER = tuple(CATALOG)
LEVELS = {10: 3, 2: 5, 13: 7, 12: 9, 6: 12}


def load_rules(path=ROOT / 'server_config/tian_shu_rules.json'):
    rules = json.loads(Path(path).read_text())
    formation.require(rules.get('schema_version') == 1 and rules.get('reward_variant') in (1, 2)
                      and type(rules.get('level9_gold')) is int and rules['level9_gold'] == 50
                      and rules.get('account_policy') == 'local_account', '新手天书配置无效')
    return rules


def has(role, field, stage):
    return bool(role.get(field, 0) & (1 << stage))


def mark(role, stage):
    role['task_progress'] = role.get('task_progress', 0) | (1 << stage)


def refresh(role):
    """Monotonic facts only; never infer victories from level, rank or ownership."""
    fresh = 'tian_shu' not in role
    state = role.setdefault('tian_shu', dict(version=1, party_count=0, party_seen={}))
    role.setdefault('task_progress', 0)
    role.setdefault('task_prize', 0)
    guide = role.get('guide_progress', 0)
    # Earlier 1204 implementation paid 20 gold without recording task_prize.
    # The legacy all-bits bootstrap sentinel does NOT prove that payment.
    if fresh and guide != 0x7fffffff and guide & (1 << 13):
        role['task_prize'] |= 1 << 1
    role['task_progress'] |= role['task_prize']
    for stage, level in LEVELS.items():
        if role.get('level', 1) >= level:
            mark(role, stage)
    for key, gate in role.get('journey', {}).get('gates', {}).items():
        kind, gid = map(int, key.split(':'))
        cfg = journey.GATES.get(kind, {}).get(gid, {})
        if kind == 1 and int(cfg.get('boss_type', 0)) == 2 and gate.get('pass_star', 0) >= 3:
            mark(role, 1)
    if role.get('rule_index', 0) > 0:
        mark(role, 3)
    for item in role.get('attachments', []):
        if item.get('attach_type') == 6 and item.get('level', 1) >= 3:
            mark(role, 8)
        if (item.get('attach_type') == 5 and item.get('level', 1) > 1
                and int(formation.ITEMS.get(item['type_id'], {}).get('main_type', 0)) in (1, 2, 3)):
            mark(role, 11)
    activity = role.get('activity', {})
    if activity.get('duty_best', 0) >= 10:
        mark(role, 7)
    if any(not r.get('defence') and 1 <= r.get('fight_result_msg', {}).get('final_result', 0) <= 3
           for r in activity.get('rank_records', [])):
        mark(role, 4)
    for board in activity.get('rape_boards') or []:
        if any(t.get('has_win') for rows in board.get('form_list', {}).values() for t in rows.values()):
            mark(role, 5)
    if any(t.get('has_win') for t in activity.get('rape_revenge', {}).values()):
        mark(role, 5)
    # Count each observed day's committed fights once, including across restarts.
    party = activity.get('party', {})
    if 'day' in party:
        day, count = str(party['day']), max(0, party.get('count', 0))
        seen = state['party_seen']
        # Party's clock never rewinds. Retain only the current day's watermark.
        if not seen or int(day) >= max(map(int, seen)):
            state['party_count'] = min(20, state['party_count'] + max(0, count - seen.get(day, 0)))
            state['party_seen'] = {day: max(count, seen.get(day, 0))}
    if state['party_count'] >= 20:
        mark(role, 9)
    # Explicit local replacement; do not claim to perform real-name verification.
    if role.get('register_account'):
        mark(role, 14)
    return state


def record_events(role, events):
    """Called only with successful, authoritative activity settlement output."""
    for packet in events:
        mid, _, data = decode(packet)
        if mid == 1027 and 1 <= data.get('final_result', 0) <= 3:
            stage = {2: 4, 3: 5, 4: 3, 12: 5}.get(data.get('fight_type'))
            if stage:
                mark(role, stage)


def reward_specs(stage, rules):
    if stage == 12:
        return [(11, 1, rules['level9_gold'], 1)]
    # Original guide table uses type|id|level|count, unlike journey's spec order.
    text = CATALOG[stage]['gold_count'].split('&')[rules['reward_variant'] - 1]
    if not text:
        return []
    typ, tid, level, count = map(int, text.split('|'))
    return [(typ, tid, count, level)]


def client_config(rules):
    return {stage: [dict(object_type=t, attach_type=i, attach_count=n, attach_level=l)
                    for t, i, n, l in reward_specs(stage, rules)] for stage in ORDER}


def sync(role):
    # Original 1032 handles task_progress but omits task_prize; the adapter applies
    # both fields before the native progress callback rebuilds the book hint.
    return [summon.event(80, dict(local_tian_shu=dict(task_progress=role['task_progress'],
                                                    task_prize=role['task_prize']))),
            encode(1032, dict(id=role['role_id'], unit_type=1, attr_count=1,
                             attr_list=[dict(type=12, value=role['task_progress'])]))]


def claim(role, stage, now, rules):
    formation.require(type(stage) is int and stage in CATALOG, '未知的天书任务')
    refresh(role)
    formation.require(not has(role, 'task_prize', stage), '该天书奖励已经领取')
    formation.require(has(role, 'task_progress', stage), '尚未完成该天书任务')
    index = ORDER.index(stage)
    formation.require(all(has(role, 'task_prize', s) for s in ORDER[:index]), '请先领取前面的天书奖励')
    prizes = [journey.grant(role, spec) for spec in reward_specs(stage, rules)]
    role['task_prize'] |= 1 << stage
    return summon.event(57, dict(task_stage=stage, prize_list=prizes))
