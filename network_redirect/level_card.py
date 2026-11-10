"""User-requested offline role level card [B], settled on a detached role."""
from pathlib import Path
from contextvars import ContextVar

from . import formation as f, item_sale, progression, summon

ITEM = 1901
_code_recipient = ContextVar('level_card_code_recipient', default=None)


def require_grant(role, kind, tid):
    if kind == 5 and tid == ITEM:
        f.require(_code_recipient.get() is role, '等级卡只能通过激活码礼包获取')


def grant_code_prize(role, prize):
    """Called only after gift_codes.settle has checked redemption eligibility."""
    from . import item_rewards
    token = _code_recipient.set(role)
    try:
        return item_rewards.grant(role, prize)
    finally:
        _code_recipient.reset(token)


def inventory_count(role):
    return sum(i.get('count', 0) for i in (role or {}).get('attachments', [])
               if i.get('attach_type') == 5 and i.get('type_id') == ITEM)


def check_save(before, role, allowance=0):
    # Also catch code paths which append inventory directly instead of using
    # the reward allocators. Existing stacks and card consumption remain valid.
    f.require(type(allowance) is int and allowance >= 0
              and inventory_count(role) <= inventory_count(before) + allowance,
              '等级卡只能通过激活码礼包获取')


def use(role, req, now):
    f.require(req['item_type'] == ITEM and type(req['item_count']) is int
              and req['item_count'] == 1, '等级卡每次只能使用1张')
    f.require(req['des_type'] == 1 and req['des_id'] in (0, role['role_id']),
              '等级卡只能对当前主角使用')
    level = role['level']
    f.require(type(level) is int and level in f.LEVELS, '主角等级无效')
    f.require(level < max(f.LEVELS), '主角已达等级上限，等级卡未消耗')
    item = f.lookup(role, 'attachments', req['item_id'])
    f.require(item['type_id'] == ITEM and item_sale.available(item)
              and type(item.get('count')) is int and item['count'] >= 1
              and sum(i['id'] == item['id'] for i in role['attachments']) == 1,
              '等级卡不足、已锁定或不可使用')
    need = int(f.LEVELS[level]['upgrade_exp'])
    exp = role.get('cur_exp', 0)
    f.require(type(exp) is int and 0 <= exp < need, '主角修为异常，请重新登录后重试')
    # Adding the current level's full threshold preserves the absolute remainder.
    # Guard the table relationship so a future balance edit cannot grant two levels.
    f.require(exp < int(f.LEVELS[level + 1]['upgrade_exp']), '下级修为配置异常')
    progression.add_exp(role, need, now)
    item['count'] -= 1
    if not item['count']:
        role['attachments'].remove(item)
    return [summon.event(21, dict(result=1, type_id=ITEM, count=1, effect_value=1))]


def client_source():
    info = next(r for r in summon.rows('local_items/item_name.csv') if int(r['Ftype_id']) == ITEM)
    config = dict(id=ITEM, max_level=max(f.LEVELS), name=info['name'],
                  description=info['desc'], introduction=info['introduce'],
                  sortOrder=int(info['order']), product_desc=info['product_desc'])
    return Path(__file__).with_name('level_card_client.lua').read_text(encoding='utf-8').replace(
        '__LEVEL_CARD__', summon.lua(config))
