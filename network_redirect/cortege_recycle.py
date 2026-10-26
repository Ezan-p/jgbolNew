"""3.87 five-companion recycling [A], explicit offline reward policy [B]."""
import json
import secrets
from . import formation as f, summon

RULES_PATH = f.ROOT / 'server_config/cortege_recycle_rules.json'
BOOKS = {(int(row['show_level']), row['resource'] == '21'): tid
         for tid, row in f.ITEMS.items() if row['sub_type'] == '99'}


def load_rules(path=RULES_PATH):
    r = json.loads(path.read_text())
    f.require(r.get('schema_version') == 1 and r.get('mode') == 'inferred', '回收配置来源无效')
    f.require(type(r.get('fate_advanced_percent')) is int and 0 <= r['fate_advanced_percent'] <= 100,
              '仙缘高级密卷概率无效')
    f.require(r.get('growth_policy') == 'consume_without_refund' and
              r.get('bound_items_policy') == 'return_except_innate', '回收物品策略无效')
    return r


def has_fate(types):
    """cortegeRecycleUI:803-883: owner + every target, target count < 5."""
    for row in f.FATES:
        if int(row['tartege_type[4-cortege/5-equip/6-skill]']) != 4:
            continue
        owner = int(row['cortege_type[effected_cortege]'])
        targets = {int(t) for t in row['target_object_type[1/2/3]'].split('/') if t}
        if owner in types and 0 < len(targets) < 5 and targets <= types:
            return True
    return False


def settle(role, req):
    rules = load_rules()
    f.require(role['level'] >= 15, '角色15级开放神仙回收')
    f.require(req['flag'] == 0, '神仙回收参数无效')
    ids = [req['c%d' % n] for n in range(1, 6)]
    f.require(len(set(ids)) == 5 and all(i > 0 for i in ids), '需要选择5个不同的四星神仙')
    chosen = [f.lookup(role, 'corteges', i) for i in ids]
    for c in chosen:
        f.require(int(f.BASES[c['type']]['quality']) == 4, '只能回收四星神仙')
        f.require(not c.get('order') and not c.get('cheer_order'), '上阵或助威神仙不能回收')
        f.require(not c.get('is_lock') and not c.get('pending_training'), '请先解锁或处理培养结果')
    # [A] Preview is floor(role level / 15)*15, six rolls. The catalog ends at 100.
    level = min(max(l for l, advanced in BOOKS), role['level'] // 15 * 15)
    fate = has_fate({c['type'] for c in chosen})
    advanced = fate and secrets.randbelow(100) < rules['fate_advanced_percent']
    tid = BOOKS[level, bool(advanced)]
    consumed = set(ids)
    # Never leave orphan innate spells or lose engraved essences silently.
    role['attachments'] = [i for i in role['attachments']
                           if i.get('innate_owner_id') not in consumed]
    for item in role['attachments']:
        if item.get('owner_id') in consumed:
            item.update(owner_id=0, equip_order=0, equip_pos=0, ext_skill_pos=0)
    role['corteges'] = [c for c in role['corteges'] if c['id'] not in consumed]
    summon.add_item(role, tid, 6)
    # roll.level is the item instance level; display level comes from item_base.
    return [(64, dict(roll_list=[dict(type_id=tid, level=1, count=6)]))]
