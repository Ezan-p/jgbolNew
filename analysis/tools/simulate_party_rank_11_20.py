"""Reproducible, detached simulations using the production party combat path."""
import copy
import hashlib
import json
import random
import statistics
import sys
import time
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_party as party, activity_rank as rank
from network_redirect import formation, journey

OUT = ROOT / 'analysis/evidence/party/rank_11_20_simulation_20261110'
REPORT = ROOT / 'docs/封神榜11至20名蟠桃大会伤害模拟.md'
DETAIL = ROOT / 'docs/封神榜11至20名蟠桃大会逐场伤害明细.md'
SEED = 20261110
REPEATS = 30


def battle_seed(order, boss_type, repeat, attempt):
    # Use matching seeds across encouragement settings, without forcing procs.
    return party.stable('party-rank-simulation', SEED, order, boss_type, repeat, attempt)


def simulate(role, order, boss, bonus, repeat, ar, jr):
    role = copy.deepcopy(role)
    original = copy.deepcopy(role)
    hp_cap = party.rules()['boss_hp']
    free_count = ar['party_free_count']
    total, rows = 0, []
    cfg = dict(cortege_list=f"{boss['type']}|{ar['battle_level']}")
    for attempt in range(1, free_count + ar['party_paid_count'] + 1):
        hp = hp_cap - total % hp_cap
        units = journey.fighters(role, cfg)
        for unit in units[0]:
            unit['gongji'] = unit['gongji'] * (100 + bonus * 10) // 100
        party.prepare_boss(units[1][0], dict(boss_type=boss['type'], cur_hp=hp))
        seed = battle_seed(order, boss['type'], repeat, attempt)
        with patch('secrets.randbelow', side_effect=random.Random(seed).randrange):
            result, lineup, actions = journey.battle(role, cfg, jr, units=units)
        damage = min(hp, journey.combat_engine.total_damage(actions))
        assert 0 <= damage <= hp
        total += damage
        row = dict(rank=order, name=role['role_name'], boss=boss['name'], boss_type=boss['type'],
                   bonus=bonus, repeat=repeat, attempt=attempt, paid=attempt > free_count,
                   seed=seed, hp_before=hp, damage=damage, cumulative_damage=total,
                   hp_after=hp-damage, next_hp=hp_cap-total % hp_cap,
                   peaches=min(party.rules()['peach_cap'], damage // party.rules()['damage_per_peach']),
                   result=result, rounds=actions.rounds, stop_reason=actions.stop_reason,
                   boss_finisher=any(not a['is_src'] and a['skill_type']==boss['aoe_skill'] for a in actions))
        if repeat == 0:
            row.update(actions=list(actions), effects=actions.events, final_hp=actions.final_hp)
        rows.append(row)
    assert role == original, 'Combat simulation mutated the source role'
    return rows


def validate_production(role, boss, bonus, sample, ar, jr):
    """Compare a complete 15-attempt session with activity.battle itself."""
    role = copy.deepcopy(role)
    day = 20767  # Search a local date with the required naturally selected boss.
    pool = party.rules()['boss_pool']
    while pool[party.stable('party-boss', day) % len(pool)]['type'] != boss['type']:
        day += 1
    now = day*86400 + 12*3600 - ar['timezone_offset_hours']*3600
    role['gold_coin'] = 10000
    role.setdefault('activity', {}).update(party_count=0, party_paid=0, party_bonus=bonus, fight_id=0,
                                          party=dict(day=day, clock=now, count=0, damage=0, peaches=0, lucky=0))
    # Item drops cannot alter combat. Suppress them to avoid unrelated inventory
    # and seasonal state initialization; real quotas, fees and damage still run.
    with patch.object(party, 'fight_rewards', return_value=[]), patch.object(party, 'seasonal_rewards', return_value=[]):
        for row in sample:
            with patch('secrets.randbelow', side_effect=random.Random(row['seed']).randrange):
                activity.battle(role, dict(fight_type=6, des_value=int(row['paid'])), now,
                                ar, jr, formation.load_rules())
            assert role['activity']['party']['damage'] == row['cumulative_damage']
            assert party.info(role, ar)['cur_hp'] == row['next_hp']
    assert role['activity']['party_count'] == ar['party_free_count']
    assert role['activity']['party_paid'] == ar['party_paid_count']
    assert role['gold_coin'] == 10000-ar['party_paid_count']*ar['party_fight_gold']


def number(value):
    return f'{value:,.0f}'


def table(headers, rows):
    return ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---']*len(headers)) + ' |',
            *['| ' + ' | '.join(map(str, row)) + ' |' for row in rows], '']


def main():
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    ar, jr = activity.load_rules(), journey.load_rules()
    ladder = rank.catalog()
    roster, summaries, samples = [], [], []
    for order in range(11, 21):
        npc = ladder[930000+order]
        role = npc['role']
        roster.append(dict(rank=order, npc_id=npc['npc_id'], name=role['role_name'],
                           level=role['level'], power=role['role_combat_power'],
                           lineup=[dict(order=c['order'], type=c['type'], level=c['level'],
                                        evolve=c.get('evolve_level', 0), power=c['combat_power'])
                                   for c in sorted(role['corteges'], key=lambda c:c.get('order',0))
                                   if 1 <= c.get('order',0) <= 8]))
        for boss in party.rules()['boss_pool']:
            for bonus in (0, ar['party_bonus_limit']):
                runs = []
                for repeat in range(REPEATS):
                    rows = simulate(role, order, boss, bonus, repeat, ar, jr)
                    runs.append(dict(repeat=repeat, free=sum(x['damage'] for x in rows if not x['paid']),
                                     paid=sum(x['damage'] for x in rows if x['paid']),
                                     total=rows[-1]['cumulative_damage'],
                                     kills=sum(x['hp_after']==0 for x in rows),
                                     finishers=sum(x['boss_finisher'] for x in rows),
                                     peaches=sum(x['peaches'] for x in rows)))
                    if repeat == 0:
                        samples.extend(rows)
                        if order == 11:
                            validate_production(role, boss, bonus, rows, ar, jr)
                totals = [x['total'] for x in runs]
                summaries.append(dict(rank=order, name=role['role_name'], boss=boss['name'],
                                      boss_type=boss['type'], bonus=bonus, runs=runs,
                                      mean=statistics.mean(totals), median=statistics.median(totals),
                                      minimum=min(totals), maximum=max(totals),
                                      mean_free=statistics.mean(x['free'] for x in runs),
                                      mean_paid=statistics.mean(x['paid'] for x in runs)))
        print(f'Completed rank {order}: {role["role_name"]}; {time.monotonic()-started:.1f}s', flush=True)

    paths = {p.relative_to(ROOT) for p in (ROOT/'network_redirect').glob('*.py')}
    paths.update(p.relative_to(ROOT) for p in (ROOT/'server_config').glob('*.json'))
    paths.update(p.relative_to(ROOT) for p in (ROOT/'analysis/configs').rglob('*.csv'))
    paths.add(Path('analysis/tools/simulate_party_rank_11_20.py'))
    paths.add(Path(rank.rules()['ladder_catalog']))
    paths.add(Path('analysis/npc_design/players/catalog.json'))
    from network_redirect import npc_players
    paths.update(Path(p) for p in npc_players.rules().get('additional_catalogs', []))
    paths.update(Path(npc_players.catalog()[row['npc_id']]['source_file']) for row in roster)
    manifest = {str(p):hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(paths)}
    metadata = dict(date='2026-11-10', python_version=sys.version, base_seed=SEED, repeats=REPEATS,
                    total_simulated_fights=len(summaries)*REPEATS*15,
                    production_validation_fights=90, boss_level=ar['battle_level'],
                    free_count=ar['party_free_count'], paid_count=ar['party_paid_count'],
                    boss_hp=party.rules()['boss_hp'], boss_skill_probability=party.rules()['boss_skill_probability'],
                    roster=roster, summaries=summaries, input_sha256=manifest)
    (OUT/'summary.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+'\n')
    (OUT/'sample_fights.json').write_text(json.dumps(samples, ensure_ascii=False, indent=2)+'\n')
    write_docs(metadata, samples, ar)
    print(f'Wrote {REPORT.relative_to(ROOT)} and {DETAIL.relative_to(ROOT)}; {time.monotonic()-started:.1f}s', flush=True)


def write_docs(meta, samples, ar):
    summaries = meta['summaries']
    ladder_rows = {r['order']:r for r in json.loads((ROOT/rank.rules()['ladder_catalog']).read_text())['npcs']}
    ranges = {bonus:(min(s['mean'] for s in summaries if s['bonus']==bonus),
                     max(s['mean'] for s in summaries if s['bonus']==bonus)) for bonus in (0, ar['party_bonus_limit'])}
    doc = ['# 封神榜第11—20名蟠桃大会伤害模拟', '', '模拟日期：2026-11-10。使用当前工作区本地服务端规则与固定 NPC 模板。', '',
           f'打满10次免费＋5次付费后，各 NPC／首领组合的日累计伤害均值：**不鼓舞 {ranges[0][0]/10000:,.2f}万—{ranges[0][1]/10000:,.2f}万；满鼓舞 {ranges[10][0]/10000:,.2f}万—{ranges[10][1]/10000:,.2f}万**。这是每种场景30次完整模拟的统计均值范围，单日结果会波动。', '',
           '## 模拟口径', '',
           '- 对象为封神榜**初始第11—20名**，即当前蟠桃大会 NPC 前十名使用的完整模板；不使用玩家换位后的实时席位。',
           '- 每名 NPC 独立挑战同一首领 **10 次免费＋5 次付费**，共15场；每个模拟日从首领满血开始。每场恢复己方阵容，首领剩余生命跨场继承，被击败后下场补满。NPC 之间不共用首领血量。',
           f'- 三位首领分别模拟；实际游戏每天只出现其中一位。首领等级沿用活动配置 **{meta["boss_level"]}级**，每轮生命1000万、法力2,147,483,647，群攻触发概率20%，触发即击败全队。',
           '- 对比不鼓舞与开打前买满10次鼓舞（攻击＋100%）。5次付费挑战共100元宝；满鼓舞另需275元宝，共375元宝。鼓舞只按实际代码提高攻击，不将全部伤害简单乘二。',
           f'- 每个“NPC×首领×鼓舞”组合模拟{REPEATS}个独立随机样本，共60组、{meta["total_simulated_fights"]:,}场。表中均值是30次完整15场日程的样本平均；最小/最大是样本观察值，不是理论上下限或保证结果。',
           '- 采用正式 `journey.fighters → party.prepare_boss → journey.battle` 路径，保留技能、装备、精华、替补、转生等实际机制。累计伤害使用正式统计并限制为开战时剩余生命。没有强制技能触发或胜负。',
           '- 通过固定种子的伪随机数替代 `secrets.randbelow`，便于复现；真实游戏使用系统随机数，具体单日结果会变化。同一 NPC／首领／场次的两档鼓舞使用相同初始种子，但战斗分支可能不同。',
           '- 本报告仅记录战斗模拟结果，不写入玩家存档。后续按用户要求，前十名排行榜已采用7915万—1.177亿的十档固定候选池，每档5选1；具体数值见[蟠桃会规则](蟠桃会离线活动实现说明.md)。该榜单按候选池每日抽取，不会实时运行本报告的战斗模拟。', '',
           '## 阵容概况', '']
    doc += table(['封神榜初始名次','NPC','角色等级','神仙等级','飞升等级','战力'],
                 [[r['rank'],r['name'],r['level'],
                   '／'.join(map(str,sorted({c['level'] for c in r['lineup']}))),
                   '／'.join(map(str,sorted({c['evolve'] for c in r['lineup']}))),number(r['power'])] for r in meta['roster']])
    doc += ['位置1—4为首发，5—8为替补；完整装备、法术、精华等保留原模板。', '']
    doc += table(['名次','完整阵容（位置:神仙）'],
                 [[r['rank'],ladder_rows[r['rank']]['lineup']] for r in meta['roster']])
    for bonus, label in ((0,'不鼓舞'),(ar['party_bonus_limit'],'鼓舞买满（攻击＋100%）')):
        doc += [f'## {label}：15场累计伤害均值', '', '单位：实际伤害值；括号为30个模拟日的最小—最大累计伤害。三列是不同首领场景，不能相加为一天伤害。', '']
        rows=[]
        for r in meta['roster']:
            group=[s for s in summaries if s['rank']==r['rank'] and s['bonus']==bonus]
            rows.append([r['rank'],r['name'],*[f"{number(s['mean'])}（{number(s['minimum'])}—{number(s['maximum'])}）" for s in group]])
        doc += table(['名次','NPC','风伯','太上老君','福星'],rows)
    doc += ['## 免费与付费伤害拆分', '', '以下均为30个模拟日的平均伤害。付费伤害是最后5场在前10场留下的首领血量基础上继续挑战的结果。均值四舍五入至整数，免费与付费显示值相加可能与总均值相差1；原始数据保留精度。', '']
    doc += table(['名次','NPC','首领','鼓舞次数','前10次免费均值','后5次付费均值','15次总均值'],
                 [[s['rank'],s['name'],s['boss'],s['bonus'],number(s['mean_free']),number(s['mean_paid']),number(s['mean'])] for s in summaries])
    doc += ['## 结果解读', '']
    for bonus,label in ((0,'不鼓舞'),(ar['party_bonus_limit'],'满鼓舞')):
        group=[s for s in summaries if s['bonus']==bonus]
        low=min(group,key=lambda s:s['mean']);high=max(group,key=lambda s:s['mean'])
        doc += [f'- {label}时，30组场景的日均累计伤害范围为 **{number(low["mean"])}—{number(high["mean"])}**；最低为第{low["rank"]}名{low["name"]}对{low["boss"]}，最高为第{high["rank"]}名{high["name"]}对{high["boss"]}。']
    doc += ['- 首领群攻、己方技能触发与跨场余血使总伤害存在波动。更高面板战力不保证在每位首领或每次样本中伤害更高。',
            '- 单场伤害最多等于开战时的首领剩余生命，理论上15场最多累计1.5亿；击杀剩余低血首领也会占用一次挑战。', '',
            '## 逐场明细、验证与复现', '',
            '- [逐场伤害明细](封神榜11至20名蟠桃大会逐场伤害明细.md)：每组第1个固定种子样本，共900场，含逐场伤害、累计值、首领开战血量、回合与终结群攻。',
            '- [完整统计及输入指纹](../analysis/evidence/party/rank_11_20_simulation_20261110/summary.json)：1800个模拟日的免费、付费、总伤害、击杀数与蟠桃数量。',
            '- [逐场原始数据及动作](../analysis/evidence/party/rank_11_20_simulation_20261110/sample_fights.json)：900场明细与战斗动作／效果日志。',
            '- 第11名的三位首领×两档鼓舞共90场，另用正式 `activity.battle` 连续挑战核对，累计伤害、剩余生命、10＋5次配额及100元宝付费扣款全部一致。该验证仅屏蔽物品奖励入包，未屏蔽战斗或次数／费用计算。',
            '- 所有模拟均检查伤害不超过剩余生命、源角色模板未被改写；生成结果保留代码、配置、数值表及模板文件的 SHA-256。', '',
            '复现命令（工作区根目录）：', '', '```sh', '.runtime/venv/bin/python analysis/tools/simulate_party_rank_11_20.py', '```', '']
    REPORT.write_text('\n'.join(doc))

    detail=['# 封神榜第11—20名蟠桃大会逐场伤害明细', '',
            '模拟日期：2026-11-10。[模拟规则与30次重复统计](封神榜11至20名蟠桃大会伤害模拟.md)。', '',
            '以下为各场景的第1个固定种子模拟日，不能视作保证结果。每节分别列出不鼓舞与满鼓舞的15场；两组各自继承首领余血。第1—10场免费，第11—15场付费。血量与伤害均为整数；“群攻”表示本场首领触发全队终结技能。', '']
    for r in meta['roster']:
        for boss in party.rules()['boss_pool']:
            detail += [f"## 第{r['rank']}名 {r['name']} · {boss['name']}", '']
            for bonus,label in ((0,'不鼓舞'),(ar['party_bonus_limit'],'满鼓舞')):
                group=[x for x in samples if x['rank']==r['rank'] and x['boss_type']==boss['type'] and x['bonus']==bonus]
                detail += [f'### {label}', '']
                detail += table(['场次','方式','首领开战血量','本场伤害','累计伤害','回合','首领群攻','首领被击败'],
                                [[x['attempt'],'付费' if x['paid'] else '免费',number(x['hp_before']),number(x['damage']),
                                  number(x['cumulative_damage']),x['rounds'],'是' if x['boss_finisher'] else '否',
                                  '是' if x['hp_after']==0 else '否'] for x in group])
                detail += [f"免费10场合计 **{number(sum(x['damage'] for x in group if not x['paid']))}**；付费5场合计 **{number(sum(x['damage'] for x in group if x['paid']))}**；总计 **{number(group[-1]['cumulative_damage'])}**。", '']
    DETAIL.write_text('\n'.join(detail))


if __name__ == '__main__':
    main()
