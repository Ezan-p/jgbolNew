"""Export exact live bag probabilities and refresh the implementation document."""
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import qiankun_bags as q, summon, formation as f

OUT = ROOT / 'analysis/evidence/qiankun_bag_pools'
DOC = ROOT / 'docs/四种乾坤袋概率池实现说明.md'
LABELS = dict(silver='银两', gold='元宝', small_bun='小包子', bun='包子', pill='仙丹',
              peach='蟠桃', ginseng='人参果', soul_pill='魂缘丹', manual='仙佛密卷',
              manual_advanced='高级仙佛密卷', summon_advanced='高级召唤符', summon_super='超级召唤符',
              diamond='金刚钻', fruit='仙缘果', holy_peach='圣母蟠桃', soul_stone='精魄石',
              purple_shard='紫色精魄碎片', realm_box='五法界魂箱', weapon_shard='五星武器碎片',
              armor_shard='五星防具碎片', treasure_shard='五星法宝碎片', passive_shard='五星被动碎片',
              active_5='五星主动法术', passive_5='五星普通被动法术（不含大乘经）', mahayana='大乘经')
for star in range(2, 6):
    for key, label in (('weapon','武器'),('armor','防具'),('treasure','法宝'),('skill','法术（主动＋被动）')):
        LABELS[f'{key}_{star}'] = f'{star}星{label}'
NAMES = {int(r['Ftype_id']): r['name'] for r in summon.rows('item_name.csv')}
SKILLS = {int(r['type_id']): r['name'] for r in summon.rows('skill_name.csv')}
TIER_NAMES = dict(low='低品质',medium='中品质',high='高品质')


def name(kind, tid):
    return {11:'元宝',12:'银两'}.get(kind) or (SKILLS if kind==6 else NAMES)[tid]


def percent(p):
    return f'{float(p)*100:.8f}'.rstrip('0').rstrip('.')+'%'


def main():
    rules = q.load_rules()
    lines = ['## 6. 十二个品质池的规模', '',
             '下表具体结果数按“类型＋ID＋数量”去重；不同品质池可出现同一模板，跨池不能简单相加为全袋物品种数。', '',
             '| 袋子 | 品质池 | 奖励组数 | 具体结果数 | 模板／货币种数 |',
             '| --- | --- | ---: | ---: | ---: |']
    results, summaries, used = {}, {}, set()
    for tid, bag in rules['bags'].items():
        results[tid] = []
        for key in q.TIERS:
            tier = bag['tiers'][key]
            entries = []
            for group in tier['groups']:
                pool = group['pool']; used.add(pool)
                candidates = q.CATALOG[pool]
                p = Fraction(tier['weight'] * group['weight'], 10000*len(candidates))
                for kind, target in candidates:
                    entries.append(dict(tier=key, pool=pool, kind=kind, id=target,
                                        name=name(kind,target), count=group['count'], level=1,
                                        probability=str(p), percent=percent(p)))
            results[tid].extend(entries)
            lines.append(f"| {bag['name']} | {TIER_NAMES[key]} | {len(tier['groups'])} | {len(entries)} | {len({(e['kind'],e['id']) for e in entries})} |")
        assert sum(Fraction(e['probability']) for e in results[tid]) == 1
    lines += ['', '## 7. 各池完整组表、数量和概率', '',
              '“档内概率”是已抽中该品质档之后的条件概率；“单袋整组概率”含品质概率；“单袋每个候选概率”再除以候选数。所有行只选一个具体候选；固定数量不是随机区间。', '']
    for tid, bag in rules['bags'].items():
        for key in q.TIERS:
            tier = bag['tiers'][key]
            lines += [f"### {bag['name']}（{tid}）／{TIER_NAMES[key]}：{tier['weight']}%", '',
                      '| 奖励类别／目录键 | 候选数 | 每个候选命中时数量 | 组权重／档内概率 | 单袋整组概率 | 单袋每个候选概率 |',
                      '| --- | ---: | ---: | ---: | ---: | ---: |']
            for g in tier['groups']:
                p=Fraction(tier['weight']*g['weight'],10000); n=len(q.CATALOG[g['pool']])
                lines.append(f"| {LABELS[g['pool']]} `{g['pool']}` | {n} | {g['count']:,} | {g['weight']}／{g['weight']}% | {percent(p)} | {percent(p/n)} |")
            lines.append('')
    lines += ['## 8. 全量候选目录（ID不省略）', '',
              '同一类别在不同池中共享这份候选目录，但数量和权重以第7节该池对应行独立定义。每个候选的单袋概率就是该行最后一列；协议对象5为道具／装备，6为法术，11为元宝，12为银两。', '']
    for pool in sorted(used):
        lines += [f"### {LABELS[pool]} `{pool}`：{len(q.CATALOG[pool])}种", '',
                  '| 对象类型 | ID | 原表名称 | 说明 |', '| ---: | ---: | --- | --- |']
        for kind, tid in q.CATALOG[pool]:
            detail = ''
            if pool in ('manual','manual_advanced'):
                detail = f"使用提供神仙经验{int(f.ITEMS[tid]['experience_plus']):,}"
            elif kind==5 and f.ITEMS[tid]['main_type'] in ('1','2','3'):
                detail = f"{f.ITEMS[tid]['quality']}星；每次1件"
            elif kind==6:
                detail = f"{f.SKILLS[tid]['quality']}星；{'主动' if f.SKILLS[tid][q.USE_MODE]=='1' else '被动'}；每次1部"
            elif pool.endswith('_shard'):
                detail = '每次5个'
            else:
                detail = '数量见第7节对应池'
            lines.append(f'| {kind} | {tid} | {name(kind,tid)} | {detail} |')
        lines.append('')
    lines += ['## 9. 同名模板跨档汇总与资源期望', '',
              '下表合并同一模板的所有路径。命中率是“每袋获得该模板任意数量”的概率，期望数量是长期每袋平均产量，不是单次必得数量。其余全部模板汇总见JSON附件`aggregate_by_template`。', '',
              '| 袋子 | 资源 | 合并命中率 | 期望数量／袋（精确分数） | 期望数量／袋（小数） |',
              '| --- | --- | ---: | ---: | ---: |']
    all_aggregate = {}
    for tid, entries in results.items():
        probability, expectation = defaultdict(Fraction), defaultdict(Fraction)
        for entry in entries:
            key=(entry['kind'],entry['id']); p=Fraction(entry['probability'])
            probability[key]+=p; expectation[key]+=p*entry['count']
        aggregate=[dict(kind=k,id=t,name=name(k,t),probability=str(p),percent=percent(p),
                        expected_count=str(expectation[k,t])) for (k,t),p in sorted(probability.items())]
        all_aggregate[tid]=aggregate
        for k,t in [(12,1),(11,1),(5,1006),(5,1007),(5,10001),(5,6002),(5,6003),(5,6004),(5,6005)]:
            if (k,t) not in probability:continue
            e=expectation[k,t]
            lines.append(f"| {rules['bags'][tid]['name']} | {name(k,t)} | {percent(probability[k,t])} | {e} | {float(e):.8f} |")
        summaries[tid]=dict(path_count=len(entries),distinct_outcomes=len({(e['kind'],e['id'],e['count']) for e in entries}),
                            distinct_templates=len(probability),total_probability=str(sum(probability.values())))
    lines += ['', '## 10. 审计附件与验证边界', '',
              '[机器可读全量概率](../analysis/evidence/qiankun_bag_pools/probabilities.json)记录每条路径的对象、ID、数量、精确概率与合并期望，并保存配置和原表SHA-256以便复核。此文件由实际配置生成，不是手写第二套奖池。', '',
              '专项测试穷举全部整数票验证品质／组概率质量，逐个验证所有候选的首尾路径；真实1051报文逐组检验奖励、数量、货币和实例，验证15次独立抽取、所选堆叠扣除、VIP门槛、非法目标／数量／状态、货币上限、编码／发奖失败回滚、请求重放及重启后的存档持久性。测试使用临时SQLite账号，不修改玩家实际存档。', '',
              '精确区间与候选概率验证不依赖大样本恰好接近期望值；有限次真实随机结果允许统计波动，不保证每100袋恰好按65／30／5分配。客户端可见动画和全部物品图标仍需实际游戏目视验收。', '']
    paths=[q.PATH]+[ROOT/'analysis/configs'/n for n in ('item_base.csv','item_name.csv','skill_base.csv','skill_name.csv')]
    report=dict(revision=rules['revision'],official_server_probability=False,
                inputs=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths],
                summary=summaries,paths=results,aggregate_by_template=all_aggregate)
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'probabilities.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    start='<!-- BEGIN GENERATED QIANKUN POOLS -->';end='<!-- END GENERATED QIANKUN POOLS -->'
    old=DOC.read_text();head,tail=old.split(start);_,tail=tail.split(end)
    DOC.write_text(head+start+'\n\n'+'\n'.join(lines)+'\n'+end+tail)
    print(json.dumps(summaries,ensure_ascii=False))


if __name__ == '__main__':
    main()
