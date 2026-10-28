"""Build the five fixed rank elites from local, validated NPC snapshots."""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools import build_npc_catalog as design
from network_redirect import npc_players, combat_power, formation

KEYS = ('npc_v1_l99_t1_attack', 'npc_v2_l99_t1_attack',
        'npc_v1_l90_t1_attack', 'npc_v2_l99_t1_endurance', 'npc_v2_l99_t1_magic')
OUT = ROOT / 'analysis/npc_design/rank_elite'


def write_details(npcs):
    old = [4446103, 2005121, 1726747, 1281223, 1197265]
    lines = ['# 封神榜前五强化配置（2026-10-28）', '',
             '使用本地V1/V2快照，榜首出战神仙提升至99次飞升，并按原培养方向分配95%合法潜力。所有战力由当前统一结算器计算。', '',
             '场景ID保持930001～930005，旧存档换位继续有效；第6～99名不变。以下排名是这五个固定NPC的初始名次。', '',
             '| 名次 | NPC | 角色等级 | 流派 | 原战力 | 新战力 | 增幅 |',
             '|---|---|---|---|---|---|---|']
    for order, n in enumerate(npcs, 1):
        role = npc_players.decorate(n)['role']
        power = role['role_combat_power']
        lines.append(f"| {order} | {role['role_name']} | {role['level']} | {design.DESIGN['archetypes'][n['archetype']]['name']} | {old[order-1]:,} | {power:,} | {(power/old[order-1]-1)*100:.1f}% |")
    lines += ['', '全部T1档，8名五星出战神仙、16名助威。1～4号首发；5～8号分别替补1～4号。战力包含替补，助威通过属性加成计入。', '',
              '验证脚本：`analysis/tools/verify_rank_elite.py`；战斗与回放结果：`analysis/evidence/rank/elite_validation.json`。', '']
    for order, n in enumerate(npcs, 1):
        role = npc_players.decorate(n)['role']
        lines += [f"## 第{order}名：{role['role_name']}（{role['role_combat_power']:,}）", '',
                  f"来源：`{n['rank_source']['file']}`，模板：`{n['npc_id']}`。", '',
                  '| 阵位 | 神仙 | 等级 | 飞升 | 转生 | 生命 | 攻击 | 防御 | 法力 | 战力 |',
                  '|---|---|---|---|---|---|---|---|---|---|']
        team = sorted((c for c in role['corteges'] if c['order']), key=lambda c:c['order'])
        for c in team:
            values = [c['order'], design.NAMES[c['type']], c['level'], c['evolve_level'], c['reborn_layer'],
                      c['hp'], c['gongji'], c['fangyu'], c['magic'], c['combat_power']]
            lines.append('| ' + ' | '.join(map(str, values)) + ' |')
        lines += ['', '### 逐仙装备与法术', '']
        for c in team:
            items = [i for i in role['attachments'] if i.get('innate_owner_id')==c['id'] or
                     i.get('equip_order')==c['order'] or i.get('owner_id')==c['id']]
            def item_name(i):
                names = design.SKILL_NAMES if i['attach_type']==6 else design.ITEM_NAMES
                return f"{names.get(i['type_id'], str(i['type_id']))} Lv{i['level']}"
            gear = [i for i in items if i['attach_type']==5 and int(formation.ITEMS[i['type_id']]['main_type']) in (1,2,3)]
            skills = [i for i in items if i['attach_type']==6]
            essences = [i for i in items if i['type_id'] in combat_power.ESSENCE_SCORES]
            stars = [i for i in items if i['type_id'] in design.reborn_stars.STARS]
            lines += [f"**{c['order']}号位 {design.NAMES[c['type']]}**", '',
                      '- 装备：' + '；'.join(item_name(i)+f"，进阶{i.get('advance_level',0)}，铸造{i.get('cast_level',0)}，六星{i.get('star_level',0)}，灵石{i.get('stone1_level',0)}级" for i in gear),
                      '- 法术：' + '；'.join(item_name(i)+f"（觉醒方向{i.get('awaken',0)}）" for i in skills),
                      '- 精魄：' + '；'.join(map(item_name, essences)),
                      '- 命星：' + ('；'.join(map(item_name, stars)) or '无'),
                      f"- 培养加点（生命／攻击／防御／法力）：{'／'.join(str(c[s+'_plus']) for s in formation.STATS)}；剩余潜力：{c['culture_point']}。", '']
        lines += ['### 助威', '', '| 位置 | 神仙 | 等级 | 飞升 | 八卦等级 | 受益阵位 |', '|---|---|---|---|---|---|']
        for c in sorted((c for c in role['corteges'] if c['cheer_order']), key=lambda c:c['cheer_order']):
            pos = c['cheer_order']; name = design.cheer.NAMES[pos-1]
            lines.append(f"| {pos} | {design.NAMES[c['type']]} | {c['level']} | {c['evolve_level']} | {role['cheer_'+name+'_level']} | {role['cheer_'+name+'_effect']} |")
        lines.append('')
    (OUT / 'details.md').write_text('\n'.join(lines)+'\n')


def build():
    npcs = []
    for order, key in enumerate(KEYS, 1):
        source = npc_players.catalog()[key]['source_file']
        npc = copy.deepcopy(npc_players.source_file(source)[key])
        npc['rank_source'] = dict(file=source, npc_id=key, initial_order=order)
        role = npc['role']
        if order == 1:
            # Normal ascension and conserved cultivation inputs, no panel multiplier.
            for c in role['corteges']:
                if not c['order']:
                    continue
                c['evolve_level'] = 99
                total = design.budget(c)
                spent = total * 95 // 100
                weights = ([35, 15, 45, 5] if c['order'] in (2, 6)
                           else design.DESIGN['archetypes']['attack']['culture_weights'])
                values = [spent * weight // 100 for weight in weights]
                values[weights.index(max(weights))] += spent - sum(values)
                c.update({stat + '_plus': value for stat, value in zip(formation.STATS, values)})
                c['culture_point'] = total - spent
            npc['rank_source']['upgrade'] = '出战八仙飞升99次，按原方向使用95%合法潜力'
            npc['battle_validation'] = dict(status='not_sampled', checked_battles=0, replay_limited_battles=0)
        combat_power.recalculate(role, formation.load_rules(), now=design.NOW)
        design.validate(npc)
        npc['settlement'] = dict(scoring_version=combat_power.SCORE_VERSION,
                                 total=role['role_combat_power'])
        role.pop('combat_power_breakdown', None)
        npcs.append(npc)
    powers = [n['role']['role_combat_power'] for n in npcs]
    assert powers == sorted(powers, reverse=True)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'catalog.json').write_text(design.json_text(dict(
        schema_version=1, revision='rank-elite-2026-10-28-v1', mode='inferred', npcs=npcs)))
    write_details(npcs)
    print(list(zip(KEYS, powers)))


if __name__ == '__main__':
    build()
