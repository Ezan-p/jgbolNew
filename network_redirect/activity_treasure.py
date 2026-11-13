"""九幽宝图：原版操作协议 [A]，持久化奖盘及缺失价格/奖池 [B]。"""
import copy
import secrets
from pathlib import Path
from . import activity as a


def validate(r):
    a.require(isinstance(r.get('abyss_map_revision'), str) and bool(r['abyss_map_revision']), '宝图配置版本缺失')
    weights = r.get('abyss_map_weights')
    a.require(isinstance(weights, list) and len(weights) == 12 and
              all(type(w) is int and 0 < w <= 1000000 for w in weights), '宝图奖励权重无效')
    a.require(r['abyss_map_paid_draws'] == 4, '原版批量宝图界面固定最多5抽')
    a.require(type(r.get('abyss_map_batch_limit')) is int and 1 <= r['abyss_map_batch_limit'] <= 99,
              '宝图批量上限无效')
    expected = [1001, 1441, 1401, 1411, 1421, 1249, 1343, 1329, 1331, 1330, 1332, 10000]
    rewards = r.get('abyss_map_rewards')
    a.require(isinstance(rewards, list) and len(rewards) == 12 and
              all(isinstance(p, list) and len(p) == 4 and all(type(v) is int for v in p)
                  and p[0] == 5 and p[1] in expected and 0 < p[2] <= 1000000 and p[3] == 1
                  for p in rewards) and [p[1] for p in rewards] == expected,
              '宝图养成奖池缺失或格子配置无效')
    quantities = r.get('abyss_map_quantity_by_tier')
    a.require(isinstance(quantities, list) and len(quantities) == 12 and
              all(isinstance(row, list) and len(row) == 10 and
                  all(type(v) is int and 0 < v <= 1000000 for v in row) and row[0] == p[2]
                  for p, row in zip(rewards, quantities)), '宝图各阶奖励数量无效')
    steps = r.get('abyss_map_item_id_steps')
    a.require(isinstance(steps, list) and len(steps) == 12 and
              all(type(v) is int for v in steps) and steps == [0,0,1,1,1,0,0,0,0,0,0,0],
              '宝图丹药档位配置无效')
    a.require(all(p[1] + step * tier in a.formation.ITEMS
                  for p, step in zip(rewards, steps) for tier in range(10)), '宝图奖励道具不存在')


def client_source(r):
    costs = [i * r['abyss_map_gold'] for i in range(r['abyss_map_paid_draws'] + 1)]
    return Path(__file__).with_name('treasure_client.lua').read_text(encoding='utf-8').replace(
        '__TREASURE_COSTS__', a.summon.lua(costs)).replace('__TREASURE_BATCH_LIMIT__', str(r['abyss_map_batch_limit']))


def pool(tid, r):
    tier = tid - 1431
    # Pill strength changes by item ID; every pill hit still awards one item.
    return [a.prize_spec([p[0], p[1] + step * tier, quantities[tier], p[3]])
            for p, quantities, step in zip(r['abyss_map_rewards'], r['abyss_map_quantity_by_tier'],
                                           r['abyss_map_item_id_steps'])]


def new_board(tid, r, quick=False):
    return dict(draws=0, goods=pool(tid, r), quick=quick, weights=list(r['abyss_map_weights']),
                paid_draws=r['abyss_map_paid_draws'], gold=r['abyss_map_gold'],
                remove_count=r['abyss_map_remove_count'], revision=r['abyss_map_revision'])


def migrate(board):
    # Old boards promised four total draws at 20 gold, with uniform odds.
    # Preserve their goods, removed/won slots and economic terms until closed.
    board.setdefault('weights', [1] * len(board['goods']))
    board.setdefault('paid_draws', 3)
    board.setdefault('gold', 20)
    board.setdefault('remove_count', 2)
    board.setdefault('revision', 'legacy-uniform-v1')


def view(tid, board, op):
    return dict(op_type=op, type_id=tid, shop_list=copy.deepcopy(board['goods']),
                free_times=0 if board['draws'] else 1, pay_times=max(0, board['draws'] - 1),
                max_pay_times=board['paid_draws'], had_hunt=bool(board['draws']),
                pay_gold_count=board['gold'], remove_count=board['remove_count'], mark_flag=board['quick'])


def draw(board):
    available = [i for i, p in enumerate(board['goods']) if not p.get('rm') and not p.get('got')]
    a.require(available, '宝图奖励已用完')
    roll = secrets.randbelow(sum(board['weights'][i] for i in available))
    for index in available:
        roll -= board['weights'][index]
        if roll < 0:
            board['goods'][index]['got'] = True
            board['draws'] += 1
            return index


def grant(role, goods):
    from .activity_abyss import grant as award
    return award(role, role['activity']['abyss'],
                 [[p['object_type'], p['attach_type'], p['attach_count'], p['attach_level']] for p in goods])


def merge(goods):
    merged = {}
    for p in goods:
        key = (p['object_type'], p['attach_type'], p['attach_level'])
        if key not in merged:
            merged[key] = a.prize_spec([key[0], key[1], 0, key[2]])
        merged[key]['attach_count'] += p['attach_count']
    return list(merged.values())


def settle(role, s, op, d, now, r):
    from .activity_abyss import response
    maps = s.setdefault('maps', {}); marks = s.setdefault('map_quick', {})
    tid = d.get('map_type') if op == 24 else d.get('type_id')
    a.require(type(tid) is int and 1431 <= tid <= 1440, '九幽宝图类型无效')
    key = str(tid); board = maps.get(key)
    if board:
        migrate(board)
    if op == 24:
        # Native treasureMapUI L683: treasure_count=draws/map, open_count=maps.
        n, draws = d.get('open_count'), d.get('treasure_count')
        a.require(type(n) is int and 1 <= n <= r['abyss_map_batch_limit'] and
                  type(draws) is int and 1 <= draws <= 1 + r['abyss_map_paid_draws'], '批量寻宝次数无效')
        a.require(not board or not board['draws'] or board['draws'] > board['paid_draws'],
                  '请先完成或放弃当前宝图，再批量使用')
        cost = n * (draws - 1) * r['abyss_map_gold']
        a.require(role.get('gold_coin', 0) >= cost, '元宝不足')
        a.consume(role, tid, n); a.spend(role, 'gold_coin', cost)
        goods = []
        for _ in range(n):
            current = new_board(tid, r)
            for _ in range(draws):
                goods.append(current['goods'][draw(current)])
        gains = grant(role, merge(goods))
        maps.pop(key, None)
        return [response(24, map_type=tid, prize_list=gains)]
    operation = d.get('op_type')
    a.require(type(operation) is int and operation in (1, 2, 3, 5, 6), '宝图操作无效')
    if operation == 1:
        if not board or board['draws'] > board['paid_draws'] or (
                board['draws'] == 0 and board['revision'] != r['abyss_map_revision']):
            a.require(any(i['attach_type'] == 5 and i['type_id'] == tid and i['count'] > 0 and
                          not i.get('owner_id') and not i.get('equip_pos') and not i.get('is_lock')
                          for i in role['attachments']), '九幽宝图不足')
            board = new_board(tid, r, marks.get(key, False)); maps[key] = board
    a.require(board is not None, '请先打开宝图')
    if role.get('month_card_time', 0) <= now:
        board['quick'] = False; marks[key] = False
    if operation == 1:
        return [response(3, event_data=view(tid, board, 1))]
    if operation in (5, 6):
        a.require(operation == 6 or role.get('month_card_time', 0) > now, '快速寻宝需要有效月卡')
        board['quick'] = operation == 5; marks[key] = board['quick']
        return [response(3, event_data=view(tid, board, operation))]
    if operation == 3:
        maps.pop(key)
        return [response(3, event_data=dict(op_type=3, type_id=tid))]
    a.require(board['draws'] <= board['paid_draws'], '该宝图寻宝次数已用完')
    a.require(board['draws'] > 0 or board['revision'] == r['abyss_map_revision'],
              '宝图奖励已更新，请重新打开宝图查看后再寻宝')
    removed = d.get('index_list', [])
    if isinstance(removed, dict):
        a.require(all(type(k) is int for k in removed) and set(removed) == set(range(1, len(removed) + 1)),
                  '移除选项无效')
        removed = [removed[i] for i in range(1, len(removed) + 1)]
    a.require(isinstance(removed, list) and len(removed) <= board['remove_count'] and
              all(type(i) is int and 1 <= i <= len(board['goods']) for i in removed) and
              len(set(removed)) == len(removed), '移除选项无效')
    a.require(not removed or board['draws'] == 0, '开始寻宝后不能更换移除项')
    if board['draws'] == 0:
        a.consume(role, tid, 1)
        for index in removed:
            board['goods'][index - 1]['rm'] = True
    else:
        a.spend(role, 'gold_coin', board['gold'])
    index = draw(board)
    gain = grant(role, [board['goods'][index]])
    return [response(3, event_data=dict(view(tid, board, 2), des_index=index + 1, prize_list=gain))]


# Guard automatic settlement as well as direct activity operations.
from .time_guard import protect as _protect_time_rewards
_protect_time_rewards(globals())
