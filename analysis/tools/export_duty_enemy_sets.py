"""Export the three duty schedules and regenerate their documented examples."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import duty_balance as balance, npc_players


def export():
    names = {}
    for path in sorted((ROOT/'analysis/configs/cortege').glob('cortege_name_*.csv')):
        for row in csv.DictReader(path.open(encoding='utf-8-sig')):
            names[int(row['type_id'])] = row['name']
    rows = []
    examples = {g: [] for g in range(4, 9)}
    for group in range(4, 9):
        for enemy_set in range(3):
            for number in range(1, 121):
                plan = balance.stage(group, number, enemy_set)
                role = npc_players.get(plan['npc_id'])['role']
                members = sorted((c for c in role['corteges'] if 1 <= c.get('order', 0) <= 8), key=lambda c: c['order'])
                lineup = '、'.join(f"{names[c['type']]}({c['type']})" for c in members)
                details = '; '.join(f"{c['order']}:{names[c['type']]}({c['type']})/等级{c['level']}/进化{c.get('evolve_level',0)}/转生{c.get('reborn_layer',0)}" for c in members)
                for difficulty, power in enumerate(plan['targets'], 1):
                    rows.append(dict(enemy_set=enemy_set+1, group=group, stage=number,
                        difficulty=difficulty, npc_id=plan['npc_id'], name=plan['name'],
                        archetype=plan['archetype'], source_level=plan['level'],
                        source_power=plan['power'], target_power=power,
                        stat_scale=round(power/plan['power'], 6), members_by_order=details,
                        source_file=npc_players.catalog()[plan['npc_id']]['source_file']))
                if number in (1, 2, 3, 30, 60, 100):
                    examples[group].append(f"| {enemy_set+1} | {number} | `{plan['npc_id']}` / {plan['name']} | {plan['power']:,} → {plan['base_power']:,} | {lineup} |")
    out = ROOT/'analysis/evidence/duty/stage_schedule.csv'
    with out.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); writer.writeheader(); writer.writerows(rows)
    doc = ROOT/'docs/天命之战实现与调试说明.md'
    content = doc.read_text()
    begin, end = '<!-- duty-enemy-sets:start -->', '<!-- duty-enemy-sets:end -->'
    lines = [begin, '### 2.3 三套逐关敌阵配置', '',
        '三套是三条逐关阵容安排，不是一套固定队伍从第1关打到最后。每关流派依次为攻击、耐久、法术（第1／2／3关，之后循环）。', '',
        '| 套号（存档值） | 候选选择 | 强度、技能与养成要求 |',
        '|---|---|---|',
        '| 第一套（0） | 保留原逐关选择：同流派最接近目标战力的前三名，按 `floor((关号-1)/3) % 3` 轮换 | 原标准完整 NPC 阵容 |',
        '| 第二套（1） | 从第一套候选之后循环选择下一支不同组合 | 与第一套相同人数、流派和目标曲线；保留所选 NPC 的全部战斗配置 |',
        '| 第三套（2） | 继续选择第三支不同组合 | 与第一套相同标准，不额外加难度或削减技能 |', '',
        '接近度为 `abs(log(原NPC战力 / 当前标准档基准))`，并以 NPC ID 稳定排序。若前三名存在相同的按站位神仙编号序列，第二／三套继续向后选择最近的不同组合；第一套不变。三套的站位、神仙等级、进化、转生、法术、精魄和觉醒来自各自源 NPC，四维按2.2节同一公式缩放。原模板及装备不会被改写。', '',
        '首次开始三套各1/3概率；已有上一轮套号时，从另外两套等概率选择（各1/2），避免连续从头重开遇到相同套。套号保存为 `activity.duty.enemy_set`，上轮套号保存在 `duty_meta.last_enemy_set`，跨日保留。查询、重连、切换难度、当前关续关与昨日续关均保持保存的套号。旧存档缺少套号时按第一套迁移，不改变进行中的敌阵；从头重开才抽取其他套。', '',
        '以下列出各套第1／2／3关，以及第30／60／100关。神仙按战斗站位排列，括号内为类型 ID；“原→标准”是源 NPC 资料战力与本关标准档缩放目标，不代表精确重算后的战斗力。三档目标始终为同一基准的80%／100%／125%。完整前120关共5,400条配置（5人数×3套×120关×3难度），含源文件、神仙等级、进化、转生及缩放倍率，见 [逐关配置表](../analysis/evidence/duty/stage_schedule.csv)。装备、法术、精魄与觉醒可用表中的 NPC ID 在对应 `source_file` 的 `role` 下逐项追溯。', '']
    for group in range(4, 9):
        lines += [f'#### {group}人组', '', '| 套 | 关 | 源 NPC / 名字 | 原战力 → 标准目标 | 按站位神仙（类型 ID） |', '|---:|---:|---|---:|---|', *examples[group], '']
    lines += [end]
    section = '\n'.join(lines)
    if begin in content:
        content = content[:content.index(begin)] + section + content[content.index(end)+len(end):]
    else:
        content = content.replace('## 3. 关卡掉落与领奖【B】', section+'\n\n## 3. 关卡掉落与领奖【B】')
    doc.write_text(content)
    print(f'Exported {len(rows)} stage/difficulty configurations and 90 documented lineups')
    return rows


if __name__ == '__main__':
    export()
