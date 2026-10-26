"""1088 ordinary-item sale: original prices [A], server validation [B]."""
from . import formation as f, summon


# This is NOT item_sell_config.csv (1056 equipment sale).
PRICES = {int(row['item_type']): int(row['silver_count'])
          for row in summon.rows('item_price_config.csv')}
MAX_INT = 2147483647  # 1032 attribute values are signed int32.


def available(item):
    """Only ordinary, unbound, unlocked stacks can be consumed by type ID."""
    return (item.get('attach_type') == 5 and item.get('level', 1) == 1
            and not any(item.get(key, 0) for key in (
                'is_lock', 'owner_id', 'equip_order', 'equip_pos', 'ext_skill_pos',
                'ext_awaken_pos', 'advance_level', 'star_level', 'star_count',
                'reborn_bit', 'cast_level', 'prob_compen', 'cur_spirit_count',
                'drill_count', 'stone1_level', 'stone2_level', 'stone3_level', 'stone4_level')))


def settle(role, req, parse):
    data = parse(req.get('data', ''))
    f.require(isinstance(data, dict) and set(data) == {'item_list'}, '出售参数无效')
    items = data['item_list']
    f.require(isinstance(items, dict) and 1 <= len(items) <= len(PRICES), '请选择有效的出售道具')
    for tid, count in items.items():
        f.require(type(tid) is int and tid in PRICES, '该道具不可出售')
        f.require(type(count) is int and 1 <= count <= MAX_INT, '出售数量必须为正整数')
    total = sum(PRICES[tid] * count for tid, count in items.items())
    balance = role.get('silver_coin', 0)
    f.require(type(balance) is int and 0 <= balance <= MAX_INT - total, '银两超过可同步上限，请减少出售数量')
    plan = []
    seen = set()
    for tid, count in sorted(items.items()):
        stacks = sorted((i for i in role['attachments'] if i.get('type_id') == tid
                         and available(i)), key=lambda i: i['id'])
        for item in stacks:
            # Object IDs use the original protocol's double field.
            f.require(type(item['id']) in (int, float) and 0 < item['id'] <= 2**53 - 1
                      and item['id'] == int(item['id']) and item['id'] not in seen
                      and sum(i['id'] == item['id'] for i in role['attachments']) == 1,
                      '背包道具编号异常，请刷新后重试')
            seen.add(item['id'])
            f.require(type(item.get('count')) is int and 0 < item['count'] <= MAX_INT,
                      '背包道具数量异常，请刷新后重试')
        f.require(sum(i['count'] for i in stacks) >= count, '可出售数量不足（锁定或已绑定的道具不可出售）')
        for item in stacks:
            take = min(count, item['count'])
            if take:
                plan.append((item, take))
                count -= take
            if not count:
                break
    # Validate the whole batch before changing any stack or currency.
    for item, count in plan:
        item['count'] -= count
    removed = {item['id'] for item, _ in plan if item['count'] == 0}
    role['attachments'] = [i for i in role['attachments'] if i['id'] not in removed]
    role['silver_coin'] = balance + total
    return [(153, dict(silver_count=total))]
