"""Passive spell insight and conversion; evidence and policy in docs/法术参悟规则与调试.md."""
from collections import Counter
from decimal import Decimal
from functools import lru_cache
import json
import secrets
from . import formation as f, summon

RECIPES = {int(r['type_id']): r for r in summon.rows('skill_advaced_conf.csv')}


@lru_cache(maxsize=1)
def rules():
    r = json.loads((f.ROOT / 'server_config/skill_insight_rules.json').read_text())
    f.require(r['mode'] == 'inferred' and r['schema_version'] == 1, '参悟配置来源无效')
    f.require(type(r['hp_percent']) is int and 0 < r['hp_percent'] <= 100, '参悟生命加成配置无效')
    return r


def hp_percent(item):
    return Decimal(rules()['hp_percent']) if item.get('upgrade_level', 0) > 0 and item['type_id'] in RECIPES else Decimal(0)


def materials(tid):
    # Original format: object_type | type_id | count | minimum level.
    return [tuple(map(int, part.split('|'))) for part in RECIPES[tid]['material_list'].split('/')]


def insight(role, req):
    f.require(req['upgrade_type'] == 6, '参悟类型无效')
    target = f.lookup(role, 'attachments', req['des_id'])
    recipe = RECIPES.get(target['type_id'])
    f.require(target['attach_type'] == 6 and recipe, '该法术不能参悟')
    f.require(target['level'] >= int(recipe['min_level']), '五星被动法术达到10级后可参悟')
    f.require(not target.get('upgrade_level'), '该法术已参悟')
    entries = req['material_list']
    ids = [x['id'] for x in entries]
    needed = materials(target['type_id'])
    f.require(req['material_count'] == len(ids) == sum(x[2] for x in needed)
              and len(set(ids)) == len(ids) and target['id'] not in ids, '参悟材料数量无效或重复')
    items = [f.lookup(role, 'attachments', i) for i in ids]
    f.require(Counter((x['attach_type'], x['type_id']) for x in items) ==
              Counter({(kind, tid): count for kind, tid, count, level in needed}), '参悟材料种类不符')
    from .equipment_crafting import free
    for item in items:
        free(item)
        f.require(not item.get('upgrade_level') and not item.get('awaken'), '已参悟或觉醒法术不能作为材料')
        minimum = next(x[3] for x in needed if x[1] == item['type_id'])
        f.require(minimum <= item['level'] <= int(f.SKILLS[item['type_id']]['top_level']), '材料法术等级无效')
    role['attachments'] = [x for x in role['attachments'] if x['id'] not in ids]
    target['upgrade_level'] = 1
    return [(156, dict(result=0, des_id=target['id'], ret_list=[]))]


def convert(role, req):
    from .equipment_crafting import free, grant
    target = f.lookup(role, 'attachments', req['skill_id'])
    cfg = f.SKILLS.get(target['type_id'], {})
    f.require(target['attach_type'] == 6 and cfg.get('quality') == '5'
              and cfg.get('use_mode(1-active，2-passive)') == '2', '只能转换五星被动法术')
    free(target)
    state = req['state']
    f.require(state in (0, 4, 5, 6), '法术转换类型无效')
    field = 'effect_field(1-gongji，2-fangyu，3-magic，4-intensity，5-hp)'
    choices = [tid for tid, c in f.SKILLS.items() if c['quality'] == '5'
               and c['use_mode(1-active，2-passive)'] == '2' and tid != target['type_id']
               and (state == 0 or int(c[field]) == state - 3)]
    f.require(choices, '没有可转换的法术')
    f.require(not target.get('upgrade_level') or target['type_id'] in RECIPES, '参悟返还配方不存在')
    f.debit_item(role, 1095, 1)
    if state:
        f.debit_money(role, 'gold_coin', 200)
    refunds = [(kind, tid, 1, count) for kind, tid, count, level in materials(target['type_id'])] if target.get('upgrade_level') else []
    old_id = target['id']
    role['attachments'].remove(target)
    target.update(id=f.new_id(role), type_id=secrets.choice(choices), upgrade_level=0, equip_order=0, equip_pos=0)
    role['attachments'].append(target)
    prizes = grant(role, refunds)
    return [(89, dict(result=0, skill_id=target['id'], old_skill_id=old_id,
                     skill_type=target['type_id'], skill_level=target['level'], ret_list=prizes))]
