"""Server-side inferred rules, explicitly distinct from recovered client facts."""
import csv
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import secrets

from .protocol import encode

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / 'server_config/summon_rules.json'


def rows(name):
    with (ROOT / 'analysis/configs' / name).open(encoding='utf-8-sig', newline='') as source:
        return list(csv.DictReader(source))


BASES = {int(r['type_id']): r for r in rows('cortege/cortege_base_0.csv')}
POOLS = {'normal_base_2_to_4': [k for k, r in BASES.items()
                              if 2000 <= k < 5000 and 2 <= int(r['quality']) <= 4]}
POOLS.update({'preview_' + r['index']: list(map(int, r['type_set(id1/id2/id3...)'].split('/')))
              for r in rows('summon_cortege_set.csv')})
CONVERT = {int(r['cortege_quality']): int(r['spirit_convert_count'])
           for r in rows('cortege_quality.csv')}
EXPERIENCE = {int(r['quality']): int(r['experience'])
              for r in rows('cortege_experience.csv') if r['level'] == '1'}
TIME_FIELDS = {1: 'normal_time', 2: 'advanced_time', 3: 'super_time'}
FIRST_FIELDS = {2: 'advanced_first_pick_time', 3: 'super_first_pick_time'}


class SummonRejected(ValueError):
    pass


def load_rules(path=RULES_PATH):
    rules = json.loads(Path(path).read_text(encoding='utf-8'))
    def require(condition, message):
        if not condition:
            raise ValueError('召唤配置无效：' + message)
    def integer(value, low=0, high=2147483647):
        return type(value) is int and low <= value <= high
    require(isinstance(rules, dict), '顶层须为对象')
    require(rules.get('schema_version') == 1 and rules.get('mode') == 'inferred', '须明确标记为 inferred')
    require(integer(rules.get('reset_utc_offset_hours'), -12, 14), '重置时区')
    # Five is embedded in this client's UI. Do not silently diverge from it.
    require(rules.get('normal_free_daily_limit') == 5, '当前客户端普通免费次数必须为 5')
    require(type(rules.get('duplicate_conversion')) is bool, '转魂开关')
    news = rules.get('news', {})
    require(isinstance(news, dict) and integer(news.get('min_quality'), 2, 5)
            and integer(news.get('limit'), 1, 6), '喜讯品质或条数')
    activity = rules.get('activity', {})
    require(isinstance(activity, dict), '活动配置须为对象')
    require(type(activity.get('enabled')) is bool, '活动开关')
    require(integer(activity.get('starts_at')) and integer(activity.get('ends_at')), '活动时间')
    require(not activity['ends_at'] or activity['ends_at'] > activity['starts_at'], '活动结束时间')
    require(isinstance(rules.get('grades'), dict) and set(rules['grades']) == {'1', '2', '3'}, '三档配置')
    for key, config in rules['grades'].items():
        require(isinstance(config, dict), '档次配置须为对象')
        require(config.get('pool') == {'1': 'normal_base_2_to_4', '2': 'preview_1', '3': 'preview_2'}[key], '客户端档次奖池')
        weights = config.get('quality_weights', {})
        allowed = {'1': ('2', '3', '4'), '2': ('3', '4', '5'), '3': ('4', '5')}[key]
        require(isinstance(weights, dict) and bool(weights) and
                all(q in allowed and integer(w, 1, 10000) for q, w in weights.items()), '品质权重')
        for quality in weights:
            require(any(int(BASES[t]['quality']) == int(quality) for t in POOLS[config['pool']]), '品质无候选')
        for field in ('free_cooldown_seconds', 'gold_cost', 'pity_after', 'paid_daily_limit',
                      'activity_soul_count', 'first_guarantee_quality', 'pity_quality'):
            require(integer(config.get(field), 0, 1000000), field)
        require(config['free_cooldown_seconds'] > 0 and config['gold_cost'] > 0, '冷却与价格须大于零')
        require(config.get('token_id') == {'1': 0, '2': 1006, '3': 1007}[key], '客户端召唤符编号')
        require(config.get('token_reward_id') in (0, 1006, 1007), '召唤符奖励编号')
        require(integer(config.get('token_reward_basis_points'), 0, 9999), '召唤符奖励概率')
        require(not config['token_reward_basis_points'] or config['token_reward_id'], '缺少召唤符奖励编号')
        require(bool(config['pity_after']) == bool(config['pity_quality']), '保底品质/次数须同时设置')
        for field in ('first_guarantee_quality', 'pity_quality'):
            q = config[field]
            require(q == 0 or (2 <= q <= 5 and any(int(k) >= q for k in weights)), '保底无可用候选')
    return rules


def rule_status(path=RULES_PATH):
    rules = load_rules(path)
    return dict(mode=rules['mode'], ready=True, revision=rules.get('revision'),
                config_path=str(Path(path).resolve()), official_verified=False,
                message='已启用用户授权的推测规则；不是官方服务端规则')


def client_source(rules):
    """Use the same validated prices for the UI, affordability check and debit."""
    prices = [rules['grades'][str(grade)]['gold_cost'] for grade in (1, 2, 3)]
    template = Path(__file__).with_name('summon_client.lua').read_text(encoding='utf-8')
    from . import vip
    vip_source = Path(__file__).with_name('vip_client.lua').read_text(encoding='utf-8')
    vip_source = vip_source.replace('__VIP_PRODUCTS__', lua(vip.load_rules()['products']))
    welfare_source = Path(__file__).with_name('welfare_client.lua').read_text(encoding='utf-8')
    monument_source = Path(__file__).with_name('monument_client.lua').read_text(encoding='utf-8')
    equipment_source = Path(__file__).with_name('equipment_client.lua').read_text(encoding='utf-8')
    reborn_source = Path(__file__).with_name('reborn_client.lua').read_text(encoding='utf-8')
    pray_source = Path(__file__).with_name('pray_client.lua').read_text(encoding='utf-8')
    pray_source = pray_source.replace('__PRAY_COSTS__', lua([int(r['spirit_coins']) for r in rows('pray_spirit_config.csv')]))
    rape_source = Path(__file__).with_name('rape_client.lua').read_text(encoding='utf-8')
    rank_source = Path(__file__).with_name('rank_client.lua').read_text(encoding='utf-8')
    pet_source = Path(__file__).with_name('pet_client.lua').read_text(encoding='utf-8')
    taixu_source = Path(__file__).with_name('taixu_client.lua').read_text(encoding='utf-8')
    babel_source = Path(__file__).with_name('babel_client.lua').read_text(encoding='utf-8')
    home_source = Path(__file__).with_name('home_client.lua').read_text(encoding='utf-8')
    pavilion_source = Path(__file__).with_name('pavilion_client.lua').read_text(encoding='utf-8')
    from . import activity_pavilion
    pavilion_source = pavilion_source.replace('__PAVILION_TABLES__', lua(activity_pavilion.client_tables()))
    return pavilion_source + '\n' + babel_source + '\n' + pray_source + '\n' + home_source + '\n' + taixu_source + '\n' + pet_source + '\n' + rape_source + '\n' + rank_source + '\n' + reborn_source + '\n' + equipment_source + '\n' + vip_source + '\n' + monument_source + '\n' + welfare_source + '\n' + template.replace('__SUMMON_GOLD_PRICES__', lua(prices))


def lua(value):
    """Serialize our own protocol data as literal Lua."""
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return '{' + ','.join(lua(v) for v in value) + '}'
    if isinstance(value, dict):
        return '{' + ','.join('[' + lua(k) + ']=' + lua(v) for k, v in value.items()) + '}'
    raise TypeError(type(value))


def event(kind, data):
    return encode(2998, dict(id=kind, data=lua(data)))


def normalize_request(request):
    grade, payment, count = request['pick_grade'], request['pick_type'], request['ten_pick']
    count = 1 if count == 0 else count
    if grade not in (1, 2, 3) or payment not in (1, 2, 3) or count not in (1, 10):
        raise SummonRejected('召唤参数无效')
    if count == 10 and (payment not in (2, 3) or grade not in (2, 3)):
        raise SummonRejected('十连仅支持高级或超级召唤，使用召唤符或元宝支付')
    if payment == 2 and grade == 1:
        raise SummonRejected('客户端没有普通召唤符请求')
    return grade, payment, count


def prepare(role, now, rules):
    """Migrate once; absolute deadlines survive logins and server restarts."""
    state = role.setdefault('summon', {})
    deadlines = state.setdefault('ready_at', {})
    for grade, field in TIME_FIELDS.items():
        deadlines.setdefault(str(grade), now + max(0, role.get(field, 0)))
    day = datetime.fromtimestamp(now, timezone(timedelta(hours=rules['reset_utc_offset_hours']))).date().isoformat()
    if state.get('day', day) != day:
        role['normal_count'] = 0
        state['paid_count'] = {}
    state['day'] = day
    role.setdefault('normal_count', 0)
    state.setdefault('paid_count', {})
    state.setdefault('pity', {})
    state['next_id'] = max([int(state.get('next_id', 1)), 1] +
                           [int(r['id']) + 1 for r in role.get('corteges', []) + role.get('attachments', [])])
    if 'draw_count' not in state:
        # Only an explicit legacy last result proves a past draw of that grade.
        last = state.get('last_result', {})
        state['draw_count'] = {}
        for grade, field in FIRST_FIELDS.items():
            if role.get(field, 0) or last.get('pick_grade') == grade:
                state['draw_count'][str(grade)] = 1
                role.setdefault(field, 0)
                role[field] = role[field] or max(1, min(now, deadlines[str(grade)] - rules['grades'][str(grade)]['free_cooldown_seconds']))
    state['rules_revision'] = rules.get('revision')
    return state


def remaining(role, now):
    return {field: max(0, int(role['summon']['ready_at'][str(grade)] - now))
            for grade, field in TIME_FIELDS.items()}


def next_id(role):
    state = role['summon']
    result = max([int(state.get('next_id', 1)), 1] +
                 [int(r['id']) + 1 for r in role.get('corteges', []) + role.get('attachments', [])])
    state['next_id'] = result + 1
    return float(result)


def add_item(role, type_id, count):
    # Original stones are individual objects (can_stack=0); material selection
    # transmits one ID per stone, with no quantity field.
    if type_id in (1090, 1091, 1092):
        for _ in range(count):
            role['attachments'].append(dict(id=next_id(role), attach_type=5, type_id=type_id, count=1, level=1))
        return
    for item in role['attachments']:
        if (item['attach_type'] == 5 and item['type_id'] == type_id
                and not item.get('owner_id') and not item.get('is_lock')
                and item.get('level', 1) <= 1 and not item.get('prob_compen')):
            item['count'] += count
            return
    role['attachments'].append(dict(id=next_id(role), attach_type=5, type_id=type_id, count=count, level=1))


def companion(role, type_id):
    base = BASES[type_id]
    stats = {name: int(base[column]) for name, column in
             dict(hp='base_max_hp', magic='base_max_magic', gongji='base_gongji', fangyu='base_fangyu').items()}
    return dict(id=next_id(role), type=type_id, order=0, level=1,
                next_exp=EXPERIENCE[int(base['quality'])], equiped_ext_skill_limit=1,
                combat_power=sum(stats.values()), **stats)


def weighted_choice(weights):
    roll = secrets.randbelow(sum(weights.values()))
    for value, weight in weights.items():
        if roll < weight:
            return value
        roll -= weight
    raise AssertionError('empty weights')


def choose_reward(config, minimum_quality=0):
    if not minimum_quality and secrets.randbelow(10000) < config['token_reward_basis_points']:
        return None, config['token_reward_id']
    weights = {int(q): w for q, w in config['quality_weights'].items() if int(q) >= minimum_quality}
    quality = weighted_choice(weights)
    candidates = [t for t in POOLS[config['pool']] if int(BASES[t]['quality']) == quality]
    return secrets.choice(candidates), None


def settle(role, request, now, rules):
    """Mutate only a detached profile; caller encodes all replies before saving."""
    grade, payment, count = normalize_request(request)
    state = prepare(role, now, rules)
    key = str(grade)
    config = rules['grades'][key]
    if payment == 1:
        if state['ready_at'][key] > now:
            raise SummonRejected('免费召唤冷却尚未结束')
        if grade == 1 and role['normal_count'] >= rules['normal_free_daily_limit']:
            raise SummonRejected('今日普通免费召唤次数已用完')
        state['last_payment'] = dict(token_id=config['token_id'], tokens_used=0, gold_spent=0, count=count)
        state['ready_at'][key] = now + config['free_cooldown_seconds']
        if grade == 1:
            role['normal_count'] += 1
    else:
        used = state['paid_count'].get(key, 0)
        if config['paid_daily_limit'] and used + count > config['paid_daily_limit']:
            raise SummonRejected('今日该档付费召唤次数已用完')
        state['paid_count'][key] = used + count
        stacks = [r for r in role['attachments'] if r['attach_type'] == 5 and r['type_id'] == config['token_id']]
        available = sum(r['count'] for r in stacks)
        # Both ten-pick request types use the authoritative pre-draw inventory.
        # Rewards from this transaction cannot pay for the transaction itself.
        tokens = min(available, count) if count == 10 else (1 if payment == 2 else 0)
        if available < tokens:
            raise SummonRejected('召唤符不足')
        cost = (count - tokens) * config['gold_cost']
        if role.get('gold_coin', 0) < cost:
            raise SummonRejected('元宝不足，还需 %d 元宝' % cost)
        role['gold_coin'] -= cost
        if tokens:
            needed = tokens
            for item in stacks:
                used = min(needed, item['count'])
                item['count'] -= used
                needed -= used
            role['attachments'] = [r for r in role['attachments'] if r['attach_type'] == 6 or r['count'] > 0]
        state['last_payment'] = dict(token_id=config['token_id'], tokens_used=tokens, gold_spent=cost, count=count)
    results = []
    for _ in range(count):
        minimum = config['first_guarantee_quality'] if state['draw_count'].get(key, 0) == 0 else 0
        if config['pity_after'] and state['pity'].get(key, 0) >= config['pity_after'] - 1:
            minimum = max(minimum, config['pity_quality'])
        type_id, token_id = choose_reward(config, minimum)
        quality = int(BASES[type_id]['quality']) if type_id else 0
        result = dict(pick_grade=grade, time=remaining(role, now)[TIME_FIELDS[grade]], count=role['normal_count'])
        if type_id:
            duplicate = rules['duplicate_conversion'] and any(c['type'] == type_id for c in role['corteges'])
            convert_count = CONVERT[quality] if duplicate else 0
            if duplicate:
                souls = role.setdefault('souls', {})
                souls[str(type_id)] = souls.get(str(type_id), 0) + convert_count
            else:
                role['corteges'].append(companion(role, type_id))
            result.update(cortege_type=type_id, convert_count=convert_count)
            if quality >= rules['news']['min_quality']:
                news = state.setdefault('news', [])
                news.insert(0, dict(type_id=type_id, time=now, name=role['role_name']))
                del news[rules['news']['limit']:]
        else:
            add_item(role, token_id, 1)
            result['token_type'] = token_id
        activity = rules['activity']
        if (activity['enabled'] and now >= activity['starts_at'] and
                (not activity['ends_at'] or now < activity['ends_at']) and config['activity_soul_count']):
            category = int(BASES[type_id]['category']) if type_id else secrets.choice((1, 2, 3, 4, 5))
            item_id = 5000 + category
            add_item(role, item_id, config['activity_soul_count'])
            result['prize_info'] = [dict(object_type=5, attach_type=item_id, attach_count=config['activity_soul_count'])]
        state['draw_count'][key] = state['draw_count'].get(key, 0) + 1
        if config['pity_after']:
            state['pity'][key] = 0 if quality >= config['pity_quality'] else state['pity'].get(key, 0) + 1
        if grade in FIRST_FIELDS:
            field = FIRST_FIELDS[grade]
            role[field] = role.get(field) or now
            result['first_pick_time'] = role[field]
        results.append(result)
    outcome = results[0] if count == 1 else dict(ten_pick=True, pick_grade=grade, event_data=results)
    state['last_result'] = results[-1]
    role.update(remaining(role, now))
    return outcome


def soul_snapshots(role):
    # [A] data.lua:2300-2345 clears on first_send and appends later chunks.
    spirits = [dict(type_id=int(t), count=n)
               for t, n in sorted(role.get('souls', {}).items(), key=lambda x: int(x[0])) if n > 0]
    return [encode(1046, dict(first_send=start == 0, spirit_count=len(spirits[start:start + 128]),
                             spirit_list=spirits[start:start + 128]))
            for start in range(0, max(1, len(spirits)), 128)]


def soul_snapshot(role):
    packets = soul_snapshots(role)
    if len(packets) != 1:
        raise ValueError('Use soul_snapshots for a large soul inventory')
    return packets[0]


def news_snapshot(role, rules):
    news = role.get('summon', {}).get('news', [])[:rules['news']['limit']]
    return encode(1047, dict(first_send=True, lottery_count=len(news), lottery_list=news))
