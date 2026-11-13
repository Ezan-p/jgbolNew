"""Refresh runtime reward tables while preserving authored Dragon Boat notes."""
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity, activity_rice as rice, summon
from write_moon_doc import percent


def replace_section(document, heading, following, content):
    start = document.index(heading)
    end = document.index(following, start)
    return document[:start] + content.rstrip() + '\n\n' + document[end:]


def main():
    shared = activity.load_rules()
    rules = shared['rice_rules']
    names = {int(r['Ftype_id']): r['name'] for r in summon.rows('item_name.csv')}
    skills = {int(r['type_id']): r['name'] for r in summon.rows('skill_name.csv')}
    path = ROOT/'docs/粽叶飘香离线活动实现说明.md'
    document = path.read_text()

    def name(p):
        return {11: '元宝', 12: '银两'}.get(p[0]) or (skills if p[0] == 6 else names)[p[1]]

    def table(pool):
        lines = ['| 组 | 具体奖励 | 对象类型／模板ID | 中奖数量 | 组权重 | 整组概率 | 候选数 | 该候选最终概率 |\n',
                 '|---|---|---|---:|---:|---:|---:|---:|\n']
        total = Fraction(0)
        for index, group in enumerate(pool['groups'], 1):
            size = len(group['candidates'])
            chance = Fraction(group['weight'], 100*size)
            for prize in group['candidates']:
                total += chance
                lines.append(f'| {index:02} | {name(prize)} | {prize[0]}／{prize[1]} | {prize[2]:,} | '
                             f"{group['weight']} | {percent(Fraction(group['weight'],100))} | {size} | {percent(chance)} |\n")
        assert total == 100
        return ''.join(lines) + '\n该池所有具体候选最终概率精确合计100%；循环小数以表内分数为准。\n'

    # Only replace reward sections; release notes and verification history survive.
    notes = {
        1213: '日常消耗池。包子1022×2、仙丹1023×2；乾坤袋作为完整道具发到背包。',
        1214: '装备池。三类一级灵石每次2颗，三类精华每次20个，三类五星碎片每次5片。原有普通五星武器／防具成品共10种，总概率0.1%，每种0.01%。四／五星灵器为材料，不是装备成品。',
        1215: '养成与法术池。2—4星法术共34种，不发普通攻击及内部占位技能。五星主动法术11种合计0.5%；五星被动碎片6005每次5片。五法界魂箱每次5个。',
        1216: '财富池。银两三档，元宝四档；仙晶1366每次100个，概率6.5%，作为背包道具；不再产出仙币1361。',
    }
    for section, (tid, mid) in enumerate(list(rice.FOOD_POOLS.items())[:4], 5):
        content = f'## {section}. {names[tid]}完整奖励池\n\n{notes[tid]}另有五星粽子1217×1，不自动开启。\n\n'
        content += table(rules['pools'][str(mid)])
        document = replace_section(document, f'## {section}.', f'## {section+1}.', content)

    heading = '| 粽子／ID | 对应月饼／ID |'
    start = document.index(heading)
    end = document.index('\n\n', start)
    lines = ['| 粽子／ID | 基础月饼池／ID | 奖励主题 | 奖励组数 | 具体结果数 |\n',
             '|---|---|---|---:|---:|\n']
    themes = ['日常道具、乾坤袋、货币、金卡、五星粽子', '装备材料、五星碎片、稀有成品、货币、金卡、五星粽子',
              '养成、召唤、法术、货币、金卡、五星粽子', '银两、元宝、仙晶、金卡、五星粽子']
    for (tid, mid), theme in zip(rice.FOOD_POOLS.items(), themes):
        groups = rules['pools'][str(mid)]['groups']
        lines.append(f'| {names[tid]}{tid} | {names[mid]}{mid} | {theme} | {len(groups)} | {sum(len(g["candidates"]) for g in groups)} |\n')
    document = document[:start] + ''.join(lines).rstrip() + document[end:]
    document = document.replace('| 基础月饼池／ID |', '| 对应月饼／ID |')

    start = document.index('| 粽子 | 每个直接元宝期望 |')
    end = document.index('\n\n', start)
    lines = ['| 粽子 | 每个直接元宝期望 | 每个直接银两期望 | 其他重点期望 |\n',
             '|---|---:|---:|---|\n']
    more = {1213: '包子0.4个，仙丹0.36个；五星粽子0.0025个',
            1214: '三类五星碎片合计0.0455片；五星粽子0.0025个',
            1215: '蟠桃2个，五法界魂箱0.15个；五星粽子0.0025个',
            1216: '仙晶6.5个；五星粽子0.0025个',
            1217: '大传世金卡0.3张；五星成品合计0.3件'}
    for tid, mid in rice.FOOD_POOLS.items():
        sums = {11: Fraction(0), 12: Fraction(0)}
        for group in rules['pools'][str(mid)]['groups']:
            for p in group['candidates']:
                if p[0] in sums:
                    sums[p[0]] += Fraction(group['weight']*p[2], 10000*len(group['candidates']))
        lines.append(f'| {names[tid]} | {float(sums[11]):g} | {float(sums[12]):g} | {more[tid]} |\n')
    document = document[:start] + ''.join(lines).rstrip() + document[end:]

    heading = '## 13. 五星粽子1217：获取、使用与完整奖励池'
    tail = ''
    if heading in document:
        start = document.index(heading)
        following = document.find('\n## ', start+len(heading))
        if following != -1:
            tail = document[following:]
        document = document[:start].rstrip() + '\n\n'
    document += heading + '''

原版道具1217，名称为“五星粽子”（原表quality=0），资源编号86，沿用原图标、名称和“使用后可开出神秘奖品”的说明。无需新增模板或替换原始CSV。四种普通粽子每次开启有0.25%概率得到五星粽子×1，作为本次唯一奖励入包；不会同时发原普通奖励，也不会自动开启五星粽子。制作仍确定产出所选普通粽子，五星粽子不占配方、不通过制作额外掉落。

普通池总权重仍为10000：从该基础池权重最高的银两组扣25，新增五星粽子权重25。碱水银两10万由22%降为21.75%；红豆银两10万由24.25%降为24%；咸肉银两10万由20%降为19.75%；五仁银两5万由30%降为29.75%。其他奖励数量及概率不变，月饼池不受影响。既有五星粽子库存统一使用新池，旧“固定圣母蟠桃×1”规则停用。

每个五星粽子独立抽取下表一项，元宝40%、大传世金卡30%、五星武器9%、五星防具9%、五星法宝6%、五星被动法术6%。每种装备／被动成品每次1件／本，等级1；同类中等概率。候选取自原版五星模板：武器10种、防具8种、法宝9种、被动法术8种（排除大乘经21）。发放成品实例，不发碎片，不含五星主动法术；金卡入包后由玩家主动使用。

背包支持单个所选堆叠1—100个独立开启，至少2个时显示数量选择框。沿用1051请求、21奖励响应以及原生粽子弹窗。关闭活动仍可开既有库存；周刷新保留普通及五星粽子。库存锁定／占用、数量或目标错误、元宝超限、发奖或编码失败整次回滚；重复请求不重抽、不重复扣除。

'''
    document += table(rules['pools']['1217'])
    document += '''
四种普通粽子经五星粽子这一条路径的最终概率相同：元宝1000为0.1%、大传世金卡为0.075%、五星武器为0.0225%、防具为0.0225%、法宝为0.015%、被动法术为0.015%。具体单模板再除以本类候选数。以上不含普通池直接发放的金卡或装备，两次开奖分别独立进行；400次普通开箱平均得到1个五星粽子，不是400次必出。

仅经此路径，每个普通粽子额外长期期望为元宝1、大传世金卡0.00075张、五星成品合计0.00075件。每个五星粽子的直接元宝期望为400、大传世金卡0.3张、五星成品0.3件；金卡不折算为元宝。这些是长期期望，短期开箱没有保底。
'''
    path.write_text(document + tail)
    print(path)


if __name__ == '__main__':
    main()
