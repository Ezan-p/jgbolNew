"""天缘召唤: native CSV and event-70 array [A], offline enemy policy [B]."""
import json
import secrets
from pathlib import Path

from . import formation as f, journey, summon
from . import battle_replay
from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
TABLE = {int(row['src_cortege_type']): row for row in summon.rows('convert_output.csv')}
NAMES = {int(row['type_id']): row['name'] for row in summon.rows('cortege/cortege_name_0.csv')}


def outputs(source):
    row = TABLE[source]
    return [list(map(int, token.split('/'))) for token in
            row[next(k for k in row if k.startswith('output('))].split('|')]


def load_rules(path=ROOT / 'server_config/convert_rules.json'):
    r = json.loads(Path(path).read_text())
    f.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred'
              and isinstance(r.get('revision'), str) and bool(r['revision']), '天缘配置来源无效')
    for key, high in (('enemy_level', 200), ('enemy_skill_level', 10)):
        f.require(type(r.get(key)) is int and 1 <= r[key] <= high, '天缘守卫等级无效')
    f.require(type(r.get('card_count')) is int and r['card_count'] == 5, '原版天缘翻牌须为五张')
    f.require(type(r.get('enemy_type')) is int and r['enemy_type'] in (6001, 6002, 6003), '天缘守卫模板无效')
    for source, row in TABLE.items():
        target = int(row['des_cortege_type'])
        f.require(source in f.BASES and int(f.BASES[source]['quality']) >= 5
                  and target in journey.NPCS and target in f.BASES, '天缘关系无效')
        f.require(all(kind in (1, 2, 3) and 0 < n <= 1000 and w > 0
                      for kind, n, w in outputs(source)), '天缘产出无效')
    return r


def draw(source):
    entries = outputs(source)
    roll = secrets.randbelow(sum(entry[2] for entry in entries))
    for kind, count, weight in entries:
        if roll < weight:
            return [kind, count]
        roll -= weight
    raise AssertionError('unreachable weighted draw')


def battle(role, req, now, rules, jrules):
    from . import activity
    r = load_rules()
    s = role['activity']
    f.require(role['level'] >= 16, '达到16级才能参加天缘召唤活动')
    f.require(s['day'] == activity.day(now, rules)
              and now >= s.get('convert_clock', role.get('convert_fight_time', 0)),
              '天缘召唤时钟已回退，请恢复本地时间')
    source = req['des_value']
    f.require(req.get('des_type', 0) == 0 and req.get('des_id', 0) == 0, '天缘挑战目标无效')
    f.require(type(source) is int and source in TABLE
              and any(c['type'] == source for c in role['corteges']), '请选择拥有召唤天缘的神仙')
    f.require(any(1 <= c.get('order', 0) <= 8 for c in role['corteges']), '请先上阵神仙')
    count = role['convert_fight_count']
    f.require(type(count) is int and count >= 0, '天缘次数无效')
    limit = role['convert_fight_limit'] + int(role.get('month_card_time', 0) > now)
    f.require(count < limit, '今日天缘召唤次数已用完')
    # Backend operates on a detached role; rejection/encoding failure commits nothing.
    if count:
        activity.consume(role, 1024, 1)
    target = int(TABLE[source]['des_cortege_type'])
    # Native event_mgr replaces 6001..6009 with the selected right-hand deity.
    # Preserve that original appearance substitution and original NPC base stats.
    cfg = dict(cortege_list=f"{r['enemy_type']}|{r['enemy_level']}", skill_level=r['enemy_skill_level'])
    result, lineup, actions = journey.battle(role, cfg, jrules)
    role.update(convert_fight_count=count + 1, convert_fight_time=now)
    s.update(last_convert_type=source, convert_clock=now,
             convert_total=s.get('convert_total', 0) + 1, fight_id=s['fight_id'] + 1)
    fid = s['fight_id']
    cards, gain = [], []
    if 1 <= result <= 3:
        cards = [draw(source) for _ in range(r['card_count'])]
        kind, n = cards[0]
        spec = [5, 1024, n, 1] if kind == 3 else [10, target if kind == 2 else source, n, 1]
        gain = [journey.grant(role, spec)]
    s['convert_last_result'] = dict(fight_id=fid, source=source, target=target, result=result,
                                    time=now, cards=cards, rewards=gain, revision=r['revision'])
    # callbackOutput stores its argument verbatim; show() checks #output > 0.
    # A keyed {prize_list=...} wrapper silently skips the native reward screen.
    return journey.combat_engine.event_packets(actions, fid) + [
        encode(1028, dict(fight_id=fid, first_hand=1, des_name=NAMES.get(target, '缘神仙'),
                         lineup_count=len(lineup), lineup=lineup)),
        *battle_replay.result_packets(1027, dict(fight_id=fid, fight_type=10, final_result=result,
                         fight_round=len(actions), fight_result=actions)),
        summon.event(70, cards), summon.event(44, dict(fight_id=fid, fight_type=10))]
