"""Run five independent groups of 100 maps with the production OS random source."""
from collections import Counter
import argparse
import hashlib
from itertools import permutations
import json
from pathlib import Path
import secrets
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity_treasure as treasure, formation, summon
from analysis.tools.analyze_abyss_output import inclusion, pack

MAPS = 100
GROUPS = 5
REPORT = ROOT / 'docs/九幽宝图产出分析.md'
EVIDENCE = ROOT / 'analysis/evidence/abyss/treasure_100_maps_5_groups_20261113.json'


def analyze():
    rules = json.loads((ROOT / 'server_config/activity_rules.json').read_text())
    treasure.validate(rules)
    weights = rules['abyss_map_weights']
    assert weights == [100, 280, 100, 50, 30, 70, 70, 69, 10, 70, 1, 150]
    probabilities = {d: inclusion(weights, d) for d in (1, 5)}
    check = [0.0] * 12
    for path in permutations(range(12), 5):
        probability = 1.0
        remaining = sum(weights)
        for i in path:
            probability *= weights[i] / remaining
            remaining -= weights[i]
        for i in path:
            check[i] += probability
    assert all(abs(float(p) - q) < 1e-12 for p, q in zip(probabilities[5], check))
    names = {int(row['Ftype_id']): row['name'] for row in summon.rows('item_name.csv')}
    tiers = []
    for tier in range(1, 11):
        goods = treasure.pool(1430 + tier, rules)
        modes = {}
        for draws in (1, 5):
            groups = []
            for group in range(1, GROUPS + 1):
                hits = Counter()
                paths = []
                for _ in range(MAPS):
                    board = treasure.new_board(1430 + tier, rules)
                    # Use the real secrets.randbelow inside draw, without patching or seeding.
                    path = [treasure.draw(board) for _ in range(draws)]
                    assert len(set(path)) == draws
                    paths.append([index + 1 for index in path])
                    hits.update(path)
                assert sum(hits.values()) == MAPS * draws
                results = [dict(slot=i + 1, id=p['attach_type'], name=names[p['attach_type']],
                                hit_count=hits[i], quantity=hits[i] * p['attach_count'])
                           for i, p in enumerate(goods)]
                nominal_xp = sum(p['quantity'] * int(formation.ITEMS[p['id']]['experience_plus'])
                                 for p in results if p['slot'] in (3, 4, 5))
                groups.append(dict(group=group, maps=MAPS, results=results, nominal_xp=nominal_xp,
                                   selected_slots_by_map=paths))
            average = [dict(slot=i + 1, id=p['attach_type'], name=names[p['attach_type']],
                            quantity=sum(g['results'][i]['quantity'] for g in groups) / GROUPS,
                            hit_count=sum(g['results'][i]['hit_count'] for g in groups) / GROUPS)
                       for i, p in enumerate(goods)]
            modes[str(draws)] = dict(draws=draws, maps_per_group=MAPS,
                                     gold_per_group=MAPS * (draws - 1) * rules['abyss_map_gold'],
                                     groups=groups, average_results=average,
                                     average_nominal_xp=sum(g['nominal_xp'] for g in groups) / GROUPS)
        tiers.append(dict(tier=tier, map_id=1430 + tier,
                          goods=[dict(slot=i + 1, id=p['attach_type'], name=names[p['attach_type']],
                                      quantity=p['attach_count'], level=p['attach_level'])
                                 for i, p in enumerate(goods)], modes=modes))
    sources = ['server_config/activity_rules.json', 'network_redirect/activity_treasure.py',
               'network_redirect/activity_abyss.py', 'analysis/configs/item_name.csv',
               'analysis/configs/item_base.csv', 'analysis/tools/analyze_abyss_treasure.py',
               'analysis/tools/analyze_abyss_output.py']
    return dict(date='2026-11-13', revision=rules['abyss_map_revision'], run_id=secrets.token_hex(8),
                maps_per_group=MAPS, groups_per_mode=GROUPS, total_maps=10000, total_draws=30000,
                random_source='production secrets.randbelow; OS randomness; no fixed seed',
                removed_slots=[], weights=weights,
                probabilities={str(d): [pack(p) for p in probs] for d, probs in probabilities.items()},
                tiers=tiers, source_sha256={s: hashlib.sha256((ROOT / s).read_bytes()).hexdigest()
                                           for s in sources})


def verify(data):
    rules = json.loads((ROOT / 'server_config/activity_rules.json').read_text())
    assert data['revision'] == rules['abyss_map_revision']
    assert data['weights'] == rules['abyss_map_weights']
    assert len(data['tiers']) == 10
    total_maps = total_draws = 0
    for tier in data['tiers']:
        goods = treasure.pool(tier['map_id'], rules)
        assert len(goods) == len(tier['goods']) == 12
        for i, p in enumerate(goods):
            assert p['attach_type'] == tier['goods'][i]['id']
            assert p['attach_count'] == tier['goods'][i]['quantity']
        for d, mode in tier['modes'].items():
            assert len(mode['groups']) == GROUPS
            for g in mode['groups']:
                assert len(g['selected_slots_by_map']) == MAPS
                counts = Counter()
                for path in g['selected_slots_by_map']:
                    assert len(path) == len(set(path)) == int(d)
                    assert all(type(i) is int and 1 <= i <= 12 for i in path)
                    counts.update(path)
                total_maps += MAPS
                total_draws += sum(counts.values())
                for i, p in enumerate(goods):
                    result = g['results'][i]
                    assert result['id'] == p['attach_type'] and result['slot'] == i + 1
                    assert result['hit_count'] == counts[i + 1]
                    assert result['quantity'] == counts[i + 1] * p['attach_count']
            for i in range(12):
                assert mode['average_results'][i]['quantity'] == sum(
                    g['results'][i]['quantity'] for g in mode['groups']) / GROUPS
    assert total_maps == data['total_maps'] == 10000
    assert total_draws == data['total_draws'] == 30000


def table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join(['---'] + ['---:'] * (len(headers) - 1)) + ' |'] +
                     ['| ' + ' | '.join(map(str, row)) + ' |' for row in rows])


def mean(value):
    return f'{value:,.2f}'


def report(data):
    tiers = data['tiers']
    names = [p['name'] for p in tiers[0]['goods']]
    modes = tiers[0]['modes']
    five = modes['5']
    per_map_gold = five['gold_per_group'] // five['maps_per_group']
    per_paid_draw = per_map_gold // (five['draws'] - 1)
    per_tier_gold = sum(mode['gold_per_group'] * len(mode['groups']) for mode in modes.values())
    total_gold = sum(mode['gold_per_group'] * len(mode['groups'])
                     for tier in tiers for mode in tier['modes'].values())
    parts = ['# 九幽宝图产出分析',
             '更新日期：2026-11-13。奖池版本：`' + data['revision'] + '`。',
             '1—10阶宝图分别模拟免费首抽与每张五抽，每种模式独立运行5组，每组消耗100张新图。'
             '合计实际随机抽取10,000张宝图、30,000个中奖格，所有格子均不主动移除，同张中奖格不再参与后续抽取。',
             '每组数量为实际随机抽取后汇总的整数；五组平均为这5组数量之和除以5，表示每100张的样本平均产出。'
             '魂晶直接计入九幽货币余额，其余奖励进入背包。三类丹药每次命中1颗，宝图阶数决定丹药档位。',
             '## 当前奖池',
             table(['格子','奖品','1阶ID','10阶ID','1阶命中数量','10阶命中数量','首抽概率','五抽入选概率'],
                   [[i+1,names[i],tiers[0]['goods'][i]['id'],tiers[-1]['goods'][i]['id'],
                     tiers[0]['goods'][i]['quantity'],tiers[-1]['goods'][i]['quantity'],
                     f"{data['probabilities']['1'][i]['value']*100:g}%",
                     f"{data['probabilities']['5'][i]['value']*100:.4f}%"] for i in range(12)]),
             '首抽概率合计100%；末列按加权不放回抽取重新计算，各格入选概率合计500%。',
             '## 各阶命中数量和丹药档位',
             '魂晶每阶增加20；精魄石从1阶20起、每阶增加10；无上转生石每两阶增加1个。'
             '“五类材料”指五法界魂箱、圣母蟠桃、轮回舍利、明心转生石、伏心转生石，每类命中数量均为阶数个。',
             table(['宝图阶数','蟠桃','魂晶','五类材料各自数量','无上转生石','精魄石','每类丹药数量'],
                   [[t['tier'],t['goods'][0]['quantity'],t['goods'][1]['quantity'],
                     t['goods'][5]['quantity'],t['goods'][10]['quantity'],t['goods'][11]['quantity'],1]
                    for t in tiers]),
             table(['宝图阶数','培元丹ID','玄元丹ID','破障丹ID'],
                   [[t['tier'],*[t['goods'][i]['id'] for i in (2,3,4)]] for t in tiers]),
             '## 模拟消耗',
             f'单张宝图首抽免费，续抽4次各{per_paid_draw}元宝，抽满5次共{per_map_gold}元宝。'
             f'每组100张五抽共消耗{five["gold_per_group"]:,}元宝；每阶五组共消耗{per_tier_gold:,}元宝。',
             table(['模式','每张元宝','每组宝图','每组元宝','每组中奖格','每阶五组宝图','每阶五组元宝'],
                   [[title,mode['gold_per_group'] // mode['maps_per_group'],mode['maps_per_group'],
                     f"{mode['gold_per_group']:,}",mode['maps_per_group'] * mode['draws'],
                     mode['maps_per_group'] * len(mode['groups']),
                     f"{mode['gold_per_group'] * len(mode['groups']):,}"]
                    for d,title in (('1','免费首抽'),('5','每张五抽')) for mode in [modes[d]]]),
             f'单阶两种模式合计消耗1,000张宝图和{per_tier_gold:,}元宝；'
             f'全部10阶合计10,000张宝图和{total_gold:,}元宝。'
             '这些是模拟资源消耗，不读取或扣减玩家存档。']
    for t in tiers:
        parts.append(f"## {t['tier']}阶宝图五组随机结果")
        parts.append(f"宝图ID为{t['map_id']}。数量单位为个或颗，魂晶为货币单位；五组平均保留两位小数。")
        for draws, title in ((1, '免费首抽'), (5, '每张五抽')):
            mode = t['modes'][str(draws)]
            parts.append('### ' + title)
            parts.append(f"每组消耗{mode['maps_per_group']}张宝图、{mode['gold_per_group']:,}元宝；"
                         f"五组共消耗{mode['maps_per_group'] * len(mode['groups'])}张宝图、"
                         f"{mode['gold_per_group'] * len(mode['groups']):,}元宝。")
            parts.append(table(['奖品','道具ID','第1组','第2组','第3组','第4组','第5组','五组平均'],
                               [[p['name'],p['id']] +
                                [f"{g['results'][i]['quantity']:,}" for g in mode['groups']] +
                                [mean(mode['average_results'][i]['quantity'])]
                                for i, p in enumerate(t['goods'])]))
    parts.append('## 五组平均产出汇总')
    parts.append('每行仍以100张为单位，数值来自上方对应阶数和模式的五组实际产出平均。')
    for draws, title in ((1, '免费首抽平均'), (5, '每张五抽平均')):
        parts.append('### ' + title)
        parts.append(f"每行平均产出对应100张宝图，元宝消耗为{modes[str(draws)]['gold_per_group']:,}。")
        for indexes in (range(6), range(6,12)):
            parts.append(table(['宝图阶数'] + [names[i] for i in indexes],
                               [[t['tier']] + [mean(t['modes'][str(draws)]['average_results'][i]['quantity'])
                                              for i in indexes] for t in tiers]))
    parts += ['## 本轮无上转生石的实际命中情况',
              '“零产出组数”直接统计本轮五组中未获得无上转生石的组数。下列最大、最小及平均均为实际数量。',
              table(['宝图阶数','首抽零产出组数','首抽最少','首抽最多','首抽平均','五抽零产出组数','五抽最少','五抽最多','五抽平均'],
                    [[t['tier']] + [value for d in ('1','5')
                                    for quantities in [[g['results'][10]['quantity'] for g in t['modes'][d]['groups']]]
                                    for value in [f'{quantities.count(0)}/5',min(quantities),max(quantities),
                                                  mean(sum(quantities)/GROUPS)]] for t in tiers]),
              '## 模拟记录与复核',
              '本轮直接调用服务端`new_board`和`draw`，由游戏原用的`secrets.randbelow`从系统随机源取票；'
              '没有设置固定种子、强制中奖或按预设比例填数。五组之间使用全新奖盘，不共享已中奖或移除标志。',
              '100张在原生批量界面需要分成99张和1张，两批均使用相同新池。已开始的旧奖盘保留原有奖品、数量及权重。',
              '完整记录保存每阶、每种模式、每组100张的逐张中奖格，以及12种奖品的命中次数、实际数量和五组均值。'
              '重新随机模拟会得到新结果；使用下面的回放命令仅从已保存记录重建本轮文档，不重新抽样。',
              '```sh\n# 保存新一轮随机样本并更新文档\npython3 analysis/tools/analyze_abyss_treasure.py\n\n'
              '# 根据当前已保存样本重新生成同一份文档\npython3 analysis/tools/analyze_abyss_treasure.py --replay\n```',
              '[完整五组随机记录](../analysis/evidence/abyss/treasure_100_maps_5_groups_20261113.json)、'
              '[模拟与文档脚本](../analysis/tools/analyze_abyss_treasure.py)、'
              '[奖池配置](../server_config/activity_rules.json)、'
              '[使用与概率说明](九幽宝图使用与奖励概率说明.md)。']
    return '\n\n'.join(parts) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true', help='render the saved samples without drawing again')
    args = parser.parse_args()
    if args.replay:
        result = json.loads(EVIDENCE.read_text())
    else:
        result = analyze()
    verify(result)
    if not args.replay:
        EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
        EVIDENCE.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    REPORT.write_text(report(result))
    print(f"Verified {result['total_maps']:,} maps / {result['total_draws']:,} selected slots; "
          f"five groups per tier and mode; wrote {REPORT.relative_to(ROOT)}")
