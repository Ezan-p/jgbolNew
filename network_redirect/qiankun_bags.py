"""Four offline bags: quality -> weighted category -> uniform original template.

User supplied quality rates; category weights/counts are local balance, not a
recovered official loot table. Backend.vips owns encoding, commit and replay.
"""
import json
from pathlib import Path
import secrets

from . import formation as f, summon

PATH = f.ROOT / 'server_config/qiankun_bag_rules.json'
BAGS = frozenset((1031, 1032, 1033, 1034))
TIERS = ('low', 'medium', 'high')
USE_MODE = 'use_mode(1-active，2-passive)'


def catalog():
    """Include ALL templates of the requested type/star, including VIP gear."""
    singles = dict(small_bun=1020, bun=1022, pill=1023, peach=1001,
                   ginseng=1002, soul_pill=1024, summon_advanced=1006,
                   summon_super=1007, diamond=1093, fruit=1246,
                   holy_peach=1343, soul_stone=10000, purple_shard=10001,
                   realm_box=1249, weapon_shard=6002, armor_shard=6003,
                   treasure_shard=6004, passive_shard=6005)
    pools = {key: [(5, tid)] for key, tid in singles.items()}
    pools.update(silver=[(12, 1)], gold=[(11, 1)], mahayana=[(6, 21)])
    names = {int(row['Ftype_id']): row['name'] for row in summon.rows('item_name.csv')}
    for key, name in (('manual', '仙佛密卷'), ('manual_advanced', '高级仙佛密卷')):
        pools[key] = [(5, t) for t in sorted(f.ITEMS) if names.get(t) == name]
    for star in range(2, 6):
        for key, main in (('weapon', 1), ('armor', 2), ('treasure', 3)):
            pools[f'{key}_{star}'] = [(5, t) for t, row in sorted(f.ITEMS.items())
                                     if int(row['main_type']) == main and int(row['quality']) == star]
        pools[f'skill_{star}'] = [(6, t) for t, row in sorted(f.SKILLS.items())
                                 if int(row['quality']) == star]
    pools['active_5'] = [(6, t) for t, row in sorted(f.SKILLS.items())
                         if row['quality'] == '5' and row[USE_MODE] == '1']
    # 大乘经 is a five-star passive too; separate it to avoid double probability.
    pools['passive_5'] = [(6, t) for t, row in sorted(f.SKILLS.items())
                          if row['quality'] == '5' and row[USE_MODE] == '2' and t != 21]
    return pools


CATALOG = catalog()


def load_rules(path=PATH):
    rules = json.loads(Path(path).read_text(encoding='utf-8'))
    f.require(rules.get('schema_version') == 1 and rules.get('mode') == 'inferred'
              and bool(rules.get('revision')) and bool(rules.get('reason')), '乾坤袋配置来源无效')
    f.require(set(rules['bags']) == set(map(str, BAGS)), '乾坤袋配置必须完整覆盖四种袋子')
    for tid, bag in rules['bags'].items():
        f.require(type(bag['min_vip']) is int and bag['min_vip'] == int(tid == '1031'), '乾坤袋VIP门槛无效')
        f.require(set(bag['tiers']) == set(TIERS), '乾坤袋品质池缺失')
        f.require(all(type(t['weight']) is int and 0 < t['weight'] <= 100
                      for t in bag['tiers'].values())
                  and sum(t['weight'] for t in bag['tiers'].values()) == 100, '乾坤袋品质概率总和须为100')
        for tier in bag['tiers'].values():
            groups = tier['groups']
            f.require(isinstance(groups, list) and groups, '乾坤袋品质池不能为空')
            seen = set()
            for group in groups:
                pool, weight, count = group['pool'], group['weight'], group['count']
                f.require(pool in CATALOG and bool(CATALOG[pool]), '乾坤袋奖励类别不存在或为空')
                f.require(type(weight) is int and 0 < weight <= 100
                          and type(count) is int and 0 < count <= 1000000, '乾坤袋权重或数量无效')
                for kind, target in CATALOG[pool]:
                    f.require((kind, target, count) not in seen, '乾坤袋同档奖励重复')
                    seen.add((kind, target, count))
                    f.require(kind in (11, 12) and target == 1 or
                              kind == 5 and target in f.ITEMS and target not in BAGS or
                              kind == 6 and target in f.SKILLS, '乾坤袋奖励编号无效')
                    if kind == 6 or kind == 5 and (int(f.ITEMS[target]['main_type']) in (1, 2, 3)
                                                  or target in (1006, 1007)):
                        f.require(count == 1, '乾坤袋装备、法术和召唤符每次须为1件')
                    if target in (6002, 6003, 6004, 6005, 10001) and kind == 5:
                        f.require(count == 5, '乾坤袋碎片每次须为5个')
            f.require(sum(g['weight'] for g in groups) == 100, '乾坤袋类别权重总和须为100')
    return rules


def draw(bag):
    tier_name = summon.weighted_choice({key: bag['tiers'][key]['weight'] for key in TIERS})
    groups = bag['tiers'][tier_name]['groups']
    group = groups[summon.weighted_choice({i: g['weight'] for i, g in enumerate(groups)})]
    kind, target = secrets.choice(CATALOG[group['pool']])
    return [kind, target, group['count'], 1]


def use(role, req):
    tid, count = req['item_type'], req['item_count']
    f.require(tid in BAGS and type(count) is int and 1 <= count <= 15, '乾坤袋每批可开启1至15个')
    f.require(req['des_type'] == 1 and req['des_id'] in (0, role['role_id']), '乾坤袋使用目标无效')
    rules = load_rules()
    bag = rules['bags'][str(tid)]
    f.require(int(role.get('vip_level', 0)) >= bag['min_vip'], 'VIP1可开启VIP乾坤袋')
    item = f.lookup(role, 'attachments', req['item_id'])
    f.require(item['attach_type'] == 5 and item['type_id'] == tid and item.get('level', 1) == 1
              and item['count'] >= count and not any(item.get(k) for k in
              ('is_lock', 'owner_id', 'equip_pos', 'equip_order')), '乾坤袋不足、已锁定或不可使用')
    # VIP batches use the same independent draws as single bags: no forced
    # high-tier reward, including the last bag of a full 15-bag batch.
    specs = [draw(bag) for _ in range(count)]
    for kind, field in ((11, 'gold_coin'), (12, 'silver_coin')):
        f.require(role.get(field, 0) + sum(p[2] for p in specs if p[0] == kind)
                  <= 2147483647, '乾坤袋货币奖励超出上限')
    item['count'] -= count
    if not item['count']:
        role['attachments'].remove(item)
    from .item_rewards import grant
    # One entry per bag matches the original batch callback; each item still has
    # its own inventory instance when can_stack=0 or object_type=6.
    prizes = [grant(role, spec) for spec in specs]
    return [summon.event(21, dict(result=1, type_id=tid, count=count, attach_list=prizes))]
