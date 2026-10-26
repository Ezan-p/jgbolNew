"""神石祈福: original CSV costs/values and explicitly inferred gold rewards.

The persisted counter counts completed prayers; native UI indexes the NEXT one.
The last CSV cost repeats. All validation precedes consumption on a detached role.
"""
import math
import secrets
from . import formation as f, journey, summon

COSTS = {int(row['pray_times']): int(row['spirit_coins'])
         for row in summon.rows('pray_spirit_config.csv')}
QUALITY = {int(row['cortege_quality']): row for row in summon.rows('cortege_quality.csv')}
MAX_VALUE = 2147483647


def cost(completed):
    f.require(type(completed) is int and 0 <= completed < MAX_VALUE, '祈福次数数据无效')
    return COSTS[min(completed + 1, max(COSTS))]


def settle(role, req, rules):
    f.require(role['level'] >= 15, '祈福需15级')
    completed = role.get('pray_spirit_times', 0)
    needed = cost(completed)
    rows = req.get('object_list')
    f.require(isinstance(rows, list) and len(rows) <= 255 and
              type(req.get('object_count')) is int and req['object_count'] == len(rows), '祭品数量无效')
    retained = role.get('spirit_retain', 0)
    f.require(type(retained) is int and 0 <= retained <= MAX_VALUE, '留存魂元数据无效')
    seen, consumed, souls = set(), set(), {}
    value = retained
    for row in rows:
        typ, ident, n = row['object_type'], row['object_id'], row['count']
        f.require(type(typ) is int and type(ident) in (int, float) and math.isfinite(ident)
                  and ident > 0 and ident == int(ident), '祭品编号无效')
        ident = int(ident)
        f.require((typ, ident) not in seen and type(n) is int and n > 0, '祭品重复或数量无效')
        seen.add((typ, ident))
        if typ == 10:
            f.require(ident in f.BASES, '未知魂魄')
            worth = int(QUALITY[int(f.BASES[ident]['quality'])]['spirit_worth'])
            f.require(worth > 0, '该魂魄不能用于祈福')
            f.require(role.get('souls', {}).get(str(ident), 0) >= n, '魂魄不足')
            souls[str(ident)] = n
            value += n * worth
        else:
            f.require(typ == 4 and n == 1, '祭品类型无效')
            c = next((c for c in role['corteges'] if c['id'] == ident), None)
            f.require(c is not None, '该神仙不存在')
            q = int(f.BASES[c['type']]['quality'])
            f.require(q in (2, 3), '只能献祭二、三星神仙')
            f.require(not c.get('order') and not c.get('cheer_order') and not c.get('is_lock'),
                      '上阵、助威或锁定神仙不能献祭')
            f.require(not c.get('pending_training'), '请先处理该神仙的培养结果')
            # Every companion has an innate spell: it is removed with its owner,
            # not mistaken for an engraved essence that the player must detach.
            f.require(not any(i.get('owner_id') == ident and i.get('innate_owner_id') != ident
                              for i in role['attachments']), '请先卸下该神仙携带的精魄或物品')
            consumed.add(ident)
            value += int(QUALITY[q]['cortage_worth'])
    f.require(value >= needed, '祭品魂元不足')
    f.require(value - needed <= MAX_VALUE, '留存魂元超过上限，请减少祭品')
    reward = secrets.choice(rules['pray_rewards'])
    f.require(role['gold_coin'] + reward[2] <= MAX_VALUE, '元宝已达上限')
    for tid, n in souls.items():
        role['souls'][tid] -= n
    role['corteges'] = [c for c in role['corteges'] if c['id'] not in consumed]
    role['attachments'] = [i for i in role['attachments'] if i.get('innate_owner_id') not in consumed]
    role.update(spirit_retain=value - needed, pray_spirit_times=completed + 1)
    # A lifetime receipt also makes achievement 109 reliable across midnight.
    s = role['activity']
    s['pray_total'] = s.get('pray_total', 0) + 1
    return [summon.event(52, dict(pray_item_list=[journey.grant(role, reward)]))]
