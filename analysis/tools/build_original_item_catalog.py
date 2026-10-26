"""Build a complete, original-asset-backed item reference; no local game rules used."""
import csv
import hashlib
import html
import io
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / 'analysis/configs'
DOC = ROOT / 'docs/原版游戏全道具图鉴与获取来源.md'
AUDIT = ROOT / 'analysis/evidence/original_item_catalog.json'

GROUPS = {
    1: '武器', 2: '防具', 3: '法宝', 4: '功能道具、活动材料与专用资源',
    5: '恢复、经验及养成消耗品', 6: '宝袋、宝箱与随机容器',
    7: '活动礼包与节日成品', 8: 'VIP等级礼包', 9: '装备注灵材料',
    10: '御制金牌', 11: '四星与五星界魂', 12: '通用装备／法术碎片',
    13: '经书残卷', 14: '指定装备碎片', 15: '金色与紫色精魄',
    16: '九幽药品与药材', 17: '宠物镇魂符', 18: '雷区寻宝卡',
    19: '星宿仙术／命星', 20: '金砖辅助卡', 21: '金丹、银丹与铜丹',
}

# Explicit output-column allowlist. Costs, enemy equipment, generic numerical
# arrays and input materials must never become acquisition sources.
SOURCES = {
    'all_rank_prize.csv': ('跨服个人榜奖励', ['prize_list']),
    'babel_tower_floor_prize.csv': ('通天塔层段奖励候选', ['daoju']),
    'charge_gift_config.csv': ('充值礼包配置', ['charge_gift']),
    'compose_monthcake.csv': ('月饼制作成品', ['des_type']),
    'cross_match_prize.csv': ('跨服争霸奖励配置', ['contrib1']),
    'cross_server/camp_top_prize.csv': ('跨服战场阵营榜奖', ['prize_list']),
    'cross_server/rank_config.csv': ('跨服战场排行奖', ['prize_list']),
    'dream_prize_config.csv': ('梦境／许愿奖励配置', ['dream_prizes', 'own_wish_prizes', 'other_wish_prizes']),
    'elite/elite_tollgate_config.csv': ('释厄精英关卡奖励', ['random_prize', 'com_win_prize', 'first_random_prize']),
    'exam_rank_prize.csv': ('科举排行奖励', ['prize_list']),
    'exchange_zone.csv': ('仙灵店铺礼包及赠品', ['attach_list', 'gift_prize']),
    'friends_lv_reward.csv': ('邀友升级奖励', ['attach_list']),
    'gift_config.csv': ('活动礼包配置', ['gift_list']),
    'hill_top_prize.csv': ('洞府修炼排行奖励', ['prize_list']),
    'hole/garden_seed_config.csv': ('洞府种植收获', ['worth']),
    'hole/temple_ext_prize.csv': ('洞府神庙额外奖励候选', ['ext_list']),
    'hunt_day_prize.csv': ('捕魂达人日榜奖励', ['attach_list']),
    'hunt_week_prize.csv': ('捕魂达人周榜奖励', ['attach_list']),
    'item_buy_config.csv': ('集市商品／附赠', ['type_id', 'attach_list']),
    'item_exchange_config.csv': ('装备兑换输出候选', ['output']),
    'item_receive_config.csv': ('VIP等级礼包附件', ['attach_data']),
    'jingpo_transform.csv': ('精魄转换候选', ['des_material']),
    'map_config.csv': ('旅途地图奖励', ['pass_map_prize']),
    'material_transform.csv': ('材料合成／分解输出', ['des_material']),
    'monster_food_prize.csv': ('年兽全民奖励', ['prize_list']),
    'monster_top_prize.csv': ('年兽排行奖励', ['prize_list']),
    'old_task_prize.csv': ('任务奖励配置', ['prize_list']),
    'prey_week_rank.csv': ('猎魂之地周榜奖励', ['attach_list']),
    'rank_prize.csv': ('排行奖励配置', ['prize']),
    'reward_over_time.csv': ('在线时长奖励', ['attach_list']),
    'specter_boss_config.csv': ('九幽层数奖励', ['prirze_list']),
    'specter_hang_ouput.csv': ('九幽挂机随机产出候选', ['rand_ouput']),
    'specter_material_transform.csv': ('九幽材料合成／分解输出', ['des_material']),
    'specter_top_prize.csv': ('九幽通幽榜奖励', ['prize_list']),
    'skill_material_transform.csv': ('法术合成／还原输出配置', ['des_material']),
    'star_config.csv': ('占星产出候选', ['item_list']),
    'task_guide_prize.csv': ('新手阶段任务奖励', ['gold_count']),
    'tollgate_config.csv': ('旅途关卡奖励', ['random_prize', 'com_win_prize', 'first_random_prize']),
    'top_score_exchange.csv': ('封神榜积分兑换', ['prize_list']),
    'undergo_ordeal/elite_tollgate_config.csv': ('太虚幻境精英关卡奖励', ['random_prize', 'com_win_prize', 'first_random_prize']),
    'undergo_ordeal/map_config.csv': ('太虚幻境地图奖励', ['pass_map_prize']),
    'undergo_ordeal/tollgate_config.csv': ('太虚幻境关卡奖励', ['com_win_prize', 'com_win_prize_lijie']),
    'union_feast_award.csv': ('仙盟盛宴奖励', ['attach_data']),
    'union_match_prize.csv': ('仙盟战争奖励', ['prize_list']),
    'zongzi_formula.csv': ('粽子制作成品', ['sub_type']),
}


def field(row, prefix):
    return next((v or '' for k, v in row.items() if k and k.split('(')[0] == prefix), '')


def escape(value):
    return html.escape(str(value or ''), quote=False).replace('|', '&#124;').replace('\r', '').replace('\n', '<br>')


def link(table, text=None):
    return f'[{text or table}](../analysis/configs/{table})'


def load_original():
    index = dict(line.split('====')[:2] for line in
                 (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    encodings = {r['logical']: r['encoding'] for r in json.loads(
        (ROOT / 'analysis/evidence/config_inventory.json').read_text())}
    tables, inputs = {}, []
    for path in sorted(CONFIG.rglob('*.csv')):
        name = path.relative_to(CONFIG).as_posix()
        logical = 'csv_config/' + name
        raw = (ROOT / 'jgbol3.87/assets/release_' / index[logical]).read_bytes()
        original = raw.decode(encodings[logical])
        local = path.read_text(encoding='utf-8-sig')
        matrix = list(csv.reader(io.StringIO(original, newline=None)))
        assert matrix == list(csv.reader(io.StringIO(local, newline=None))), name
        # Preserve duplicate columns, especially all four specter drop groups.
        seen = set()
        headers = []
        for column, header in enumerate(matrix[0], 1):
            unique = header if header not in seen else f'{header}__column_{column}'
            headers.append(unique)
            seen.add(header)
        tables[name] = [{header: row[i] if i < len(row) else None for i, header in enumerate(headers)}
                        for row in matrix[1:] if row]
        inputs.append({'table': name, 'asset': index[logical], 'sha256': hashlib.sha256(raw).hexdigest(),
                       'matches_original': True, 'duplicate_headers': [h for h, n in Counter(matrix[0]).items() if n > 1]})
    return tables, inputs


def tuple_objects(value, weighted=False):
    for part in value.split('/'):
        bits = part.strip().split('|')
        offset = 1 if weighted else 0
        if len(bits) < offset + 3 or not all(x.isdigit() for x in bits):
            continue
        obj, tid = map(int, bits[offset:offset + 2])
        if obj in (5, 6):
            yield obj, tid, part


def build_sources(tables):
    refs = defaultdict(list)
    for table, (label, columns) in SOURCES.items():
        for line, row in enumerate(tables[table], 2):
            for column, value in row.items():
                if not column or column.split('(')[0] not in columns or not isinstance(value, str):
                    continue
                weighted = column.startswith(('item_list(weight', 'ext_list(weight'))
                # Task guide has two alternatives separated by &, not /.
                parse_value = value.replace('&', '/') if table == 'task_guide_prize.csv' else value
                for obj, tid, raw_tuple in tuple_objects(parse_value, weighted):
                    refs[obj, tid].append({'table': table, 'line': line, 'column': column,
                        'label': label, 'tuple': raw_tuple, 'row': row})
    # This table stores container, object type and item/count in separate columns.
    for line, row in enumerate(tables['happiness_bag_config.csv'], 2):
        obj = int(row['object_type'])
        tid, count = map(int, row['attach_type|attach_count'].split('|'))
        if obj in (5, 6):
            refs[obj, tid].append({'table': 'happiness_bag_config.csv', 'line': line,
                'column': 'attach_type|attach_count', 'label': '如来福袋内容配置',
                'tuple': f'{obj}|{tid}|{count}', 'row': row})
    # Equipment reincarnation has scalar target IDs, unlike reward-list tables.
    for line, row in enumerate(tables['equip_transfer_config.csv'], 2):
        for column, value in row.items():
            if column == 'des_type':
                refs[5, int(value)].append({'table': 'equip_transfer_config.csv', 'line': line,
                    'column': column, 'label': '装备轮回输出', 'tuple': value, 'row': row})
            elif column in ('attach_list', 'is_fabao'):
                for obj, tid, raw_tuple in tuple_objects(value):
                    refs[obj, tid].append({'table': 'equip_transfer_config.csv', 'line': line,
                        'column': column, 'label': '装备轮回分支输出', 'tuple': raw_tuple, 'row': row})
    return refs


def source_summary(obj, tid, refs, names, tables):
    groups = defaultdict(list)
    for ref in refs.get((obj, tid), []):
        groups[ref['table'], ref['label']].append(ref)
    result = []
    for (table, label), entries in sorted(groups.items()):
        lines = sorted({r['line'] for r in entries})
        if table == 'item_receive_config.csv':
            bags = sorted({int(r['row']['type_id']) for r in entries})
            label = '、'.join(names[b]['name'] for b in bags)
        if table == 'happiness_bag_config.csv':
            bags = sorted({int(r['row']['item_type']) for r in entries})
            label = '、'.join(names[b]['name'] for b in bags) + '内容'
        contexts = []
        for entry in entries:
            row = entry['row']
            context = ''
            if table.endswith('tollgate_config.csv'):
                name_table = table.replace('tollgate_config.csv', 'tollgate_name.csv')
                gate_id = row.get('id') or row.get('tollgate_id')
                gate = next((r['name'] for r in tables[name_table] if r['id'] == gate_id), '')
                column = entry['column'].split('(')[0]
                kind = {'random_prize': '随机', 'first_random_prize': '首次随机',
                        'com_win_prize': '三星', 'com_win_prize_lijie': '历劫三星'}.get(column, column)
                context = f'{gate_id}{gate}·{kind}'
            elif table.endswith('map_config.csv'):
                name_table = table.replace('map_config.csv', 'map_name.csv')
                gate = next((r.get('name', '') for r in tables[name_table] if r['id'] == row['id']), '')
                context = f'地图{row["id"]}{gate}'
            elif table == 'babel_tower_floor_prize.csv':
                context = f'{row["floor_l"]}～{row["floor_r"]}层'
            elif table in ('specter_boss_config.csv', 'specter_hang_ouput.csv'):
                context = f'{row["layer"]}层'
            elif table == 'star_config.csv':
                context = row['star_name']
            elif table == 'hole/garden_seed_config.csv':
                context = row['seed_name']
            elif table == 'task_guide_prize.csv':
                context = row['desc']
            if context and context not in contexts:
                contexts.append(context)
        if contexts:
            label += '：' + '、'.join(contexts[:3]) + (f'等{len(contexts)}处' if len(contexts) > 3 else '')
        line_text = '、'.join(map(str, lines[:5]))
        if len(lines) > 5:
            line_text += f'等{len(lines)}行'
        result.append(f'{link(table, escape(label))}（L{line_text}）')
    return '；'.join(result)


def quality(base):
    q, main = int(base['quality']), int(base.get('main_type', 0))
    if not q:
        return '未设星级（0）'
    if main in (15, 19):
        return f'{dict(enumerate(["", "白", "绿", "蓝", "金", "紫"]))[q]}色（{q}）'
    return f'{q}星（{q}）'


def fill_template(template, values):
    for value in values:
        template = template.replace('%s', value, 1)
    return template


def main():
    tables, inputs = load_original()
    names = {int(r['Ftype_id']): r for r in tables['item_name.csv']}
    bases = {int(r['type_id']): r for r in tables['item_base.csv']}
    skills = {int(r['type_id']): r for r in tables['skill_name.csv']}
    skill_bases = {int(r['type_id']): r for r in tables['skill_base.csv']}
    assert len(names) == len(bases) == 820 and names.keys() == bases.keys()
    assert len(skills) == len(skill_bases) == 64 and skills.keys() == skill_bases.keys()
    refs = build_sources(tables)
    unresolved = [{'object_type': obj, 'id': tid, 'references': rows}
                  for (obj, tid), rows in refs.items() if tid not in (names if obj == 5 else skills)]
    ext = {int(r['id']): r for r in tables['ext_skill.csv']}
    drug = {int(r['item_type']): r for r in tables['specter_pill_config.csv']}
    ext_drug = {int(r['drug_type']): r for r in tables['specter_extr_skill_drug.csv']}
    price = {int(r['item_type']): r['silver_count'] for r in tables['item_price_config.csv']}
    groups = defaultdict(list)
    for tid, base in bases.items():
        groups[int(base['main_type'])].append(tid)
    no_text = [tid for tid in names if not (names[tid]['product_desc'] or '').strip()]
    unknown = [tid for tid in no_text if not refs.get((5, tid))]
    lines = [
        '# 金箍棒 3.87 原版游戏全道具图鉴与获取来源', '',
        '整理日期：2026-10-26。依据：本仓库保存的 **3.87 原版安装包**及其静态配置。', '',
        '本图鉴逐项收录原版 `item_base.csv` 与 `item_name.csv` 的 **820种物品**，另附 '
        '**54种正式法术及10条通用／占位技能记录**。同名不同ID、不同品质、不同经验档位均独立保留，不按名字合并。', '',
        '“全”指现存原版客户端物品表的完整覆盖，不代表拿到了官方服务端的所有活动奖池。'
        '神仙整卡、神仙魂魄、宠物实体和角色称号属于其他对象体系，不计入820种物品；'
        '银两、元宝在专节说明。本文没有使用本地离线后端推测奖池填补原版来源。', '',
        '## 阅读方法与证据边界', '',
        '- **文案**：原 `product_desc` 所写的获取渠道，保留原意；只写“活动产出”时不擅自指定活动。',
        '- **配置**：明确列在奖励、商品、合成输出或转换输出字段中；链接及 L 行号供复核。'
        '候选配置不等于必掉，也不证明活动当时实际开放。',
        '- **未确认**：名称表未写来源，且本次已识别的产出字段没有匹配。不能据此断言绝版、无法获取或掉率为零。',
        '- **用途**：保留原介绍与原说明，并补入基础属性、经验数值、精魄效果或药品参数。'
        '纯故事性描述本身不证明存在额外战斗效果。',
        '- 同一表中 `数量／等级／权重` 的排列不统一；本文只按明确对象类型和ID关联来源，'
        '不把未核实的第三／第四个数一律当数量，不把权重直接写成全局掉率。',
        '- 来源汇总为当前静态资料可确认的范围；服务端动态商店、邮件、运营礼包及活动时期差异可能补充渠道。', '',
        '### 品质、等级与字段口径', '',
        '| 数据 | 本文解释 |', '|---|---|',
        '| `quality=0` | 未设星级；不等于“白色低品质”，也不表示没有价值。 |',
        '| 装备、界魂、碎片、正式法术的 `quality=2/3/4/5` | 依原表记为二／三／四／五星。 |',
        '| 精魄与命星 | 精魄4＝金、5＝紫；命星1～5＝白、绿、蓝、金、紫，不能套用其他游戏的橙色梯度。命星颜色在原介绍中可直接核对。 |',
        '| 药品名称中的下品、中品、上品、极品 | 药品自身档位；这些条目的基础品质仍为0。 |',
        '| `top_level` | 原基础表等级参数；不直接视为玩家使用等级或专属系统的实际满级。 |',
        '| `show_level` | 原显示参数。经验物品可用于区分档位；药品中有7981等编码，不应读成角色等级限制。 |',
        '| `can_stack` | 原表是否允许堆叠；不包含实际堆叠上限。 |',
        '| `use_limit`、`use_target` | 原字段值；未经对应脚本解读，不擅自转换成“每天几次／给谁使用”。 |',
        '| `random_weigth` | 保留原表拼写。缺少奖池与归一化上下文，不能视为乾坤袋概率。 |', '',
        '命星基础表 `top_level=5`，但专属升级表另有更高等级数据；精魄基础表等级参数与 '
        '`ext_skill.csv` 的五档描述也不完全一致。因此下面明确标注为“基础表等级参数”，效果表仅呈现配置数值，'
        '不凭一个字段确定系统最终上限。', '',
        '## 分类目录与数量', '',
        '| 类别（按原main_type分组） | 数量 |', '|---|---:|',
    ]
    for main_type in sorted(groups):
        lines.append(f'| [{main_type}. {GROUPS[main_type]}](#category-{main_type}) | {len(groups[main_type])} |')
    lines += ['| **物品合计** | **820** |', '| [正式法术附录](#spells) | 54 |',
              '| [通用／占位技能附录](#internal-skills) | 10 |', '',
              '附加索引：[合成配方](#recipes) · [VIP礼包内容](#vip-gifts) · [集市商品](#market) · '
              '[来源未确认清单](#unknown) · [核验说明](#verification)。可直接搜索物品名称或ID。', '']
    entries = []
    for main_type in sorted(groups):
        lines += [f'<a id="category-{main_type}"></a>', '', f'## {main_type}. {GROUPS[main_type]}（{len(groups[main_type])}种）', '']
        if main_type in (1, 2, 3):
            lines += ['属性为 `item_base.csv` 的基础值；不包含强化、注灵、升阶、缘分和战斗修正。', '']
        if main_type == 6:
            lines += ['容器的“获取方式”和“打开后内容”是两个方向。原说明只写“珍贵宝物”时，'
                      '不能据此补造奖池；四种乾坤袋的分袋概率仍未知，详见[乾坤袋专项分析](四种乾坤袋原版获取方式与产出推测.md)。', '']
        if main_type == 15:
            lines += ['物品名称表未写具体效果，因此关联原 `ext_skill.csv`。表内分别给出五档中的首档和末档效果；'
                      '全部中间档数值见该表及机器可读附件。金色／紫色为独立ID，不能合并。', '']
        if main_type == 16:
            lines += ['九幽属性药补充 `specter_pill_config.csv` 的“属性编号／减益值／比例标记”；'
                      '1攻、2防、3生命、4法力。比例标记为0的值是定值参数；其余比例尺度需结合客户端逻辑，'
                      '不直接加百分号。精魄药另按原描述模板填入百分比。', '']
        lines += ['| ID／名称 | 品质与基础参数 | 用处、原说明及数值 | 获取来源 |', '|---|---|---|---|']
        for tid in sorted(groups[main_type]):
            name, base = names[tid], bases[tid]
            meta = [quality(base), f'子类{base["sub_type"]}', '可堆叠' if base['can_stack'] == '1' else '不堆叠',
                    f'基础表等级参数{base["top_level"]}']
            if base['show_level'] != '0':
                meta.append(f'显示参数{base["show_level"]}')
            if base['use_limit'] != '0':
                meta.append(f'use_limit={base["use_limit"]}')
            usage = []
            for value in [name['introduce'], name['desc']]:
                if value and value.strip() not in usage:
                    usage.append(value.strip())
            stats = []
            for col, label in [('gongji_plus', '基础攻击'), ('fangyu_plus', '基础防御'), ('maxhp_plus', '基础生命'),
                               ('strength_plus', '体力参数'), ('energy_plus', '精力参数'),
                               ('top_fight_count_plus', '战斗次数参数'), ('experience_plus', '经验参数'),
                               ('contrib_plus', '贡献加成参数'), ('upgrade_plus', '成长参数')]:
                if base[col] != '0':
                    stats.append(f'{label}={base[col]}')
            if stats:
                usage.append('；'.join(stats))
            if tid in ext:
                r = ext[tid]
                parameters = [v.split('|') for v in r['parameter'].split('/')]
                usage += ['精魄首档：' + fill_template(r['introduction'], [v[0] for v in parameters]),
                          '精魄末档：' + fill_template(r['introduction'], [v[-1] for v in parameters])]
            if tid in drug:
                usage.append('九幽减益参数：' + field(drug[tid], 'decrease_list'))
            if tid in ext_drug:
                r = ext_drug[tid]
                usage.append(fill_template(r['desc'], r['desc_value'].split('|')))
            if tid in price:
                usage.append(f'普通道具出售表：每个{price[tid]}银两')
            source = (name['product_desc'] or '').strip()
            supplements = source_summary(5, tid, refs, names, tables)
            source_cell = ('文案：' + escape(source)) if source else '文案：未填写'
            if supplements:
                source_cell += '<br>配置：' + supplements
            elif not source:
                source_cell += '<br>获取来源未确认'
            lines.append(f'| <a id="item-{tid}"></a>**{tid} {escape(name["name"])}** | '
                         + '<br>'.join(map(escape, meta)) + ' | ' + '<br>'.join(map(escape, usage)) + ' | ' + source_cell + ' |')
            entries.append({'id': tid, 'name': name, 'base': base, 'source_references': refs.get((5, tid), []),
                            'extra_skill_effect': ext.get(tid), 'drug_effect': drug.get(tid) or ext_drug.get(tid),
                            'fixed_sell_price': price.get(tid)})
        lines.append('')

    lines += ['<a id="spells"></a>', '', '## 独立法术附录（54种）', '',
              '法术属于 `object_type=6`，与物品的 `object_type=5` 分开编号。'
              '主动法术列基础强度及成长；被动法术的 `intensity` 是效果参数，不能直接理解成伤害。'
              '完整战斗解释见[法术图鉴与威力数据](法术图鉴与威力数据.md)。', '',
              '| ID／名称 | 星级／类型／等级 | 原说明与参数 | 获取来源 |', '|---|---|---|---|']
    for tid in sorted(k for k in skills if k > 10):
        r, b = skills[tid], skill_bases[tid]
        mode = '主动' if field(b, 'use_mode') == '1' else '被动'
        target = '单体' if field(b, 'effect_target') == '1' else '群体'
        source = '文案：' + escape(r['product_desc'] or '未填写')
        supplement = source_summary(6, tid, refs, names, tables)
        if supplement:
            source += '<br>配置：' + supplement
        details = escape(r['desc']) + f'<br>intensity={b["intensity"]}；成长={b["upgrade_plus"]}；触发参数={b["use_probability"]}'
        lines.append(f'| <a id="skill-{tid}"></a>**{tid} {escape(r["name"])}** | {b["quality"]}星；{mode}／{target}；'
                     f'{b["begin_level"]}～{b["top_level"]}级 | {details} | {source} |')
    lines += ['', '<a id="internal-skills"></a>', '', '### 通用／占位技能记录（10条，单独列出以免误作可掉落法术）', '',
              '| ID | 原名称 | 原说明 | product_desc原字段 |', '|---|---|---|---|']
    for tid in range(1, 11):
        r = skills[tid]
        lines.append(f'| {tid} | {escape(r["name"])} | {escape(r["desc"])} | {escape(r["product_desc"])} |')
    lines += ['', '这些记录含普通攻击、内部效果、废弃和占位文案；即使字段名是 `product_desc`，'
              '其中“1”“群体治疗”“废弃”等也不是获取途径。', '',
              '## 货币与其他对象的边界', '',
              '| 对象 | 主要用途 | 原版来源线索及边界 |', '|---|---|---|',
              '| 元宝（奖励对象11） | 集市、召唤及各玩法付费消耗 | 多张原表存在元宝奖励／成本；充值和活动涉及服务端配置，本文不推定完整投放量。 |',
              '| 银两（奖励对象12） | 强化、合成、转换等 | 关卡money字段、VIP礼包附件、材料配方成本、装备出售及28种普通碎片固定售价。 |',
              '| 专用道具货币 | 在对应玩法兑换或升级 | 通天币20000、魂晶1441、仙币1361、仙木1362、仙晶1366、星尘10300等已经按物品ID收录，不重复计数。 |',
              '| 神仙整卡、魂魄、宠物、称号 | 各自的收集、培养或属性系统 | 不属于item_base物品表。界魂、魂箱、精魄与宠物材料则属于物品，已全量列入。 |', '',
              '<a id="recipes"></a>', '', '## 常规材料合成／分解与转换配方（80条）', '',
              '逐条来自 ' + link('material_transform.csv') + '。明确标出输入和输出，避免把消耗某材料误写成获取该材料。'
              '随机行只表示配置候选；额外权重字段原样保留，不据此补造概率。九幽184条配方另见 '
              + link('specter_material_transform.csv') + '，其输出已计入上面的逐物品来源。', '',
              '| 原表行 | 输入材料 | 额外消耗 | 输出 | 随机／最低角色等级 |', '|---|---|---|---|---|']

    def describe_list(value):
        out = []
        for segment in value.split('/'):
            if not segment:
                continue
            bits = segment.split('|')
            if len(bits) < 4:
                out.append(escape(segment))
                continue
            obj, tid, level, count, *tail = bits
            if obj == '5' and int(tid) in names:
                title = f'{names[int(tid)]["name"]}({tid})'
            elif obj == '6' and int(tid) in skills:
                title = f'{skills[int(tid)]["name"]}({tid})'
            elif obj in ('11', '12'):
                title = {'11': '元宝', '12': '银两'}[obj]
            else:
                title = f'对象{obj}/ID{tid}'
            text = f'{title}×{count}'
            if obj in ('5', '6') and level != '1':
                text += f'（等级{level}）'
            if tail:
                text += '（附加字段=' + '|'.join(tail) + '）'
            out.append(escape(text))
        return '；'.join(out) or '无'

    for line, row in enumerate(tables['material_transform.csv'], 2):
        src = describe_list(field(row, 'src_material'))
        if row['category'] in ('102', '103'):
            src = '以下精魄任选一种单独分解：' + src
        lines.append(f'| {line} | {src} | '
                     f'{describe_list(field(row, "cost_material"))} | {describe_list(field(row, "des_material"))} | '
                     f'{"随机" if row["is_random"] == "1" else "固定"}；{row["min_role_level"]}级 |')
    lines += ['', '<a id="vip-gifts"></a>', '', '## VIP等级礼包明确附件（10档）', '',
              '来自 ' + link('item_receive_config.csv') + '。这些是VIP等级礼包1101～1110的附件，'
              '**不是VIP乾坤袋1031的奖池**。领取资格和开袋机制须区分。', '',
              '| 礼包 | VIP等级条件 | 原表附件 |', '|---|---:|---|']
    for row in tables['item_receive_config.csv']:
        tid = int(row['type_id'])
        lines.append(f'| {tid} {names[tid]["name"]} | {row["vip_level"]} | {describe_list(row["attach_data"])} |')
    lines += ['', '<a id="market"></a>', '', '## 集市静态商品与价格字段（23条）', '',
              '来自 ' + link('item_buy_config.csv') + '。`buy_price` 是表内价格值；商品币种、折扣、库存、'
              '抢购及动态活动条件还依赖客户端或服务端逻辑，因此下面不统一补写“元宝”。'
              '时间原值0也不直接断言永久开放。三字段商品串不含本表明确声明的数量，按原串保留。', '',
              '| index／页 | 商品 | buy_price | VIP条件 | begin_time／end_time | 附赠 |', '|---|---|---:|---:|---|---|']
    for row in tables['item_buy_config.csv']:
        obj, tid, *_ = row['type_id'].split('|')
        title = names.get(int(tid), {}).get('name', '未命名')
        lines.append(f'| {row["index"]}／{row["page_id"]} | {escape(title)}（{escape(row["type_id"])}） | '
                     f'{row["buy_price"]} | {row["vip_level"]} | {row["begin_time"]}／{row["end_time"]} | '
                     f'{describe_list(row["attach_list"])} |')
    lines += ['', '## 使用与获取时容易混淆的事项', '',
              '1. **同名不等于同物品。** 仙佛密卷40条、九幽经验丹30条、药灵丹10条分别保留ID与经验参数；'
              '命星15类×5色共75条，按独立ID列出。',
              '2. **开袋来源未分袋。** 来源只写“开启乾坤袋”的装备、法术或材料，不能直接分配给棉布、银绸、金丝或VIP袋。',
              '3. **精魄的敌方佩戴配置不是掉落。** `specter_boss_config.ext_skill_list` 表示冥仙技能，'
              '本次来源只识别 `prirze_list`，不把敌人带什么写成奖励什么。',
              '4. **转换需要先有材料。** 精魄转换、装备兑换及碎片合成能证明“如何得到目标”，'
              '未必能证明输入材料本身如何首次获得。',
              '5. **普通道具出售仅有28种固定价格记录。** 每种1000银两；其余条目没列固定售价不等于一概不可出售，'
              '装备等另走其他规则。见[普通道具出售说明](普通道具出售模块规则与修复说明.md)。',
              '6. **有表不等于正在开放。** 历史节日礼物、金卡、活动卡和占位技能都保留原记录；'
              '未获得原服时间表，不能标为当前可领。', '',
              '<a id="unknown"></a>', '', '## 来源仍未确认的物品', '',
              f'820条中，**{len(no_text)}条**原来源文案为空；其中**{len(no_text) - len(unknown)}条**可补充明确的输出配置引用，'
              f'余下**{len(unknown)}条**未找到上述两类来源。以下为后一组完整清单。'
              '这只是本次检索边界，不是官方绝版清单；代码专用产出、动态商店或其他非标准配置仍可能补充证据。', '',
              '| ID | 名称 | 类别 |', '|---|---|---|']
    for tid in sorted(unknown):
        lines.append(f'| [{tid}](#item-{tid}) | {escape(names[tid]["name"])} | {GROUPS[int(bases[tid]["main_type"])]} |')
    lines += ['', '<a id="verification"></a>', '', '## 核验方法、覆盖范围与附件', '',
              f'- 对 **{len(inputs)}张CSV**逐单元格核对提取版与原包散列资源，全部一致；每个原资源SHA-256已保存。',
              '- 物品基础／名称表一一对应820个唯一ID；正式法术54条与通用／占位技能10条一一对应。'
              '正文每个物品均有独立锚点，未按同名合并，未补造缺号。',
              f'- 来源检索对 **{len(SOURCES) + 2}张表**使用明确的产出字段解释（含分列福袋和装备轮回表），'
              '排除输入、成本、敌方技能及普通数值数组。不能将它理解为穷尽所有原服渠道。',
              '- 所有原始介绍、说明、基础字段、逐条来源行与元组、精魄／药品效果都保存在'
              '[机器可读附件](../analysis/evidence/original_item_catalog.json)。正文来源行号采用CSV逻辑记录号（首行为表头）；'
              '大量同类记录只在正文展示前5个行号，附件保留全部记录。',
              '- 九幽挂机表的四组同名掉落列分别读取，不使用会覆盖前列的普通字典读取方式；'
              '附件同名列追加 `__column_列序号`，对应原表真实列位置。',
              '- 合成和VIP附件专表按其已声明的“对象／ID／等级／数量”格式展开；'
              '不同顺序的关卡与排行奖励不套用同一解码器。',
              '- 未关联到现有物品／法术ID的输出引用保留在附件 `unresolved_output_references`，'
              '不凭引用虚构名称或塞进820种物品总数。', '',
              '主要原表：' + '、'.join(link(t) for t in ['item_name.csv', 'item_base.csv', 'skill_name.csv', 'skill_base.csv',
                  'ext_skill.csv', 'specter_pill_config.csv', 'specter_extr_skill_drug.csv', 'item_price_config.csv']) + '。', '',
              '可重复生成与核验：', '', '```sh', 'python3 analysis/tools/build_original_item_catalog.py', '```', '',
              '生成器只写本图鉴与对应审计附件，不修改游戏代码、服务端规则、奖池或玩家存档。', '']
    document = '\n'.join(lines)
    assert len(re.findall(r'<a id="item-\d+"></a>', document)) == 820
    assert len(re.findall(r'<a id="skill-\d+"></a>', document)) == 54
    DOC.write_text(document, encoding='utf-8')
    report = {'client': '3.87', 'date': '2026-10-26', 'original_server_tables_available': False,
              'counts': {'items': 820, 'formal_spells': 54, 'internal_skills': 10,
                         'csv_verified': len(inputs), 'blank_source_text': len(no_text),
                         'blank_source_supplemented': len(no_text) - len(unknown), 'unknown_source': len(unknown),
                         'output_references': sum(map(len, refs.values()))},
              'inputs': inputs, 'source_schema': SOURCES, 'items': entries,
              'skills': [{'id': tid, 'name': r, 'base': skill_bases[tid], 'source_references': refs.get((6, tid), [])}
                         for tid, r in sorted(skills.items())],
              'unknown_source_ids': sorted(unknown), 'unresolved_output_references': unresolved}
    AUDIT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report['counts'], ensure_ascii=False))
    print(f'Document: {DOC.relative_to(ROOT)} ({len(document):,} characters)')


if __name__ == '__main__':
    main()
