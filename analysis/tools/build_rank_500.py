"""Build a reproducible 500-NPC ladder without editing source designs or old identities."""
import argparse
import copy
import csv
import hashlib
import io
import json
from collections import defaultdict, Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import combat_power, formation, npc_players, role_profile
from analysis.tools.build_npc_catalog import NAMES

OUT = ROOT / 'analysis/npc_design/rank_500'
NOW = 1793707200


def read(path):
    return json.loads((ROOT / path).read_text())


def render(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def power(n):
    return n['role']['role_combat_power']


def team(n):
    return sorted((c for c in n['role']['corteges'] if c.get('order')), key=lambda c: c['order'])


def signature(n):
    return tuple(sorted(c['type'] for c in team(n)))


def candidates():
    sources = ['analysis/npc_design/extreme/catalog.json']
    index = 'analysis/npc_design/extreme_expansion/catalog.json'
    sources += [str(Path(index).parent / n['file']) for n in read(index)['npcs']]
    sources += ['analysis/npc_design/v1/catalog.json']
    index = 'analysis/npc_design/v2/catalog.json'
    sources += [str(Path(index).parent / f) for f in read(index)['files']]
    for source in sources:
        data = read(source)
        for n in ([data] if 'role' in data else data['npcs']):
            n = copy.deepcopy(n)
            combat_power.recalculate(n['role'], formation.load_rules(), now=NOW)
            yield source, n


def select():
    all_rows = list(candidates())
    extreme = sorted((r for r in all_rows if r[1]['tier'].startswith('E')),
                     key=lambda r: (-power(r[1]), r[1]['npc_id']))
    unique, seen = [], set()
    for row in extreme:
        sig = signature(row[1])
        if sig not in seen:
            unique.append(row); seen.add(sig)
    assert len(unique) >= 100
    by_level = defaultdict(list)
    for row in all_rows:
        n = row[1]
        if n['tier'].startswith('T') and n.get('battle_validation', {}).get('status') != 'replay_limit_observed':
            by_level[n['role']['level']].append(row)
    ordinary = []
    assert set(by_level) == set(range(1, 100))
    for level, rows in sorted(by_level.items()):
        tiers = defaultdict(list)
        for row in rows:
            tiers[row[1]['tier']].append(row)
        omitted = None if level in (25, 50, 75, 99) else ('T2', 'T3', 'T4')[(level-1) % 3]
        for tier in ('T1', 'T2', 'T3', 'T4', 'T5'):
            if tier == omitted:
                continue
            pool = sorted(tiers[tier], key=lambda r: (-power(r[1]), r[1]['npc_id']))
            index = 0 if tier == 'T1' else len(pool)-1 if tier == 'T5' else (level-1) % len(pool)
            ordinary.append(pool[index])
    ordinary.sort(key=lambda r: (-power(r[1]), r[1]['npc_id']))
    result = unique[:100] + ordinary
    assert len(result) == len({n['npc_id'] for _, n in result}) == 500
    assert [power(n) for _, n in result] == sorted((power(n) for _, n in result), reverse=True)
    return result


def profiles(selected):
    old = read('analysis/npc_design/players/catalog.json')['players']
    used_ids = {e['profile']['role_id'] for e in old} | {e['legacy_role_id'] for e in old}
    used_names = {e['profile']['role_name'] for e in old}
    result = []
    rules = npc_players.rules()
    for source, n in sorted(selected[:100], key=lambda row: row[1]['npc_id']):
        role = n['role']; key = n['npc_id']
        ident = rules['id_min'] + int.from_bytes(hashlib.sha256(('rank500:' + key).encode()).digest()[:8], 'big') % (rules['id_max']-rules['id_min']+1)
        while ident in used_ids:
            ident = rules['id_min'] + (ident-rules['id_min']+1) % (rules['id_max']-rules['id_min']+1)
        name = role['name']
        assert name not in used_names and role['role_id'] not in used_ids
        used_ids.update((ident, role['role_id'])); used_names.add(name)
        head = rules['heads'][len(result) % len(rules['heads'])]
        profile = dict(role_id=ident, role_name=name, head_type=head, gender='男' if head < 200 else '女',
                       vip_level=0, level=role['level'], tier=n['tier'], role_combat_power=power(n),
                       reborn_layer=role.get('reborn_layer', 0), cur_genius_type=min(role_profile.RUNES),
                       region='蓬莱岛', personality='执着', active_period='夜间', signature='以剑会友，以诚相待。',
                       preferred_archetype=n.get('archetype', n.get('theme')), union_id=0, union_name='', title_id=0, is_npc=True)
        result.append(dict(npc_id=key, version='extreme_rank', legacy_role_id=role['role_id'], source_file=source, profile=profile))
    return dict(schema_version=1, revision='rank-500-2026-11-03-v1', players=result)


def build(check=False):
    selected = select(); extra = profiles(selected)
    identities = {e['npc_id']: e['profile'] for e in read('analysis/npc_design/players/catalog.json')['players'] + extra['players']}
    rows = []
    for order, (source, n) in enumerate(selected, 1):
        p = identities[n['npc_id']]; members = team(n)
        levels = sorted({c['level'] for c in members}); evolves = sorted({c['evolve_level'] for c in members})
        span = lambda values: str(values[0]) if len(values) == 1 else f'{values[0]}～{values[-1]}'
        rows.append(dict(order=order, scene_id=930000+order, npc_id=n['npc_id'], name=p['role_name'],
                         player_id=p['role_id'], power=power(n), role_level=n['role']['level'],
                         companion_levels=span(levels), evolve_levels=span(evolves), tier=n['tier'],
                         stage=n.get('stage', ''), archetype=n.get('theme_name', {'attack':'强袭','magic':'法术','endurance':'固守'}.get(n.get('archetype'))),
                         lineup=' / '.join(f"{c['order']}:{NAMES[c['type']]}" for c in members), source_file=source))
    manifest = dict(schema_version=1, revision='rank-500-2026-11-03-v1', npc_count=500,
                    selection='极高战力八人集合去重取最强100；普通库每角色等级取4名、25/50/75/99级取5名，按等级与T档分层取样后降序排列', npcs=rows)
    buf = io.StringIO(); writer = csv.DictWriter(buf, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    lines = ['# 封神榜前500名战力与等级明细', '', '更新：2026-11-03。此表为初始NPC席位；玩家胜负换位后，以存档中的实时名次为准。500名NPC＋玩家，共501席；新角色初始第501名。旧存档在更新后首次打开封神榜时重置到第501名，并提示“玩法更新，排名重置”；重置标记持久保存，后续打开或重启不再重置。排名重置同时清空梯度奖励的历史达成名次和已领记录；已做过上一版排名重置的旧档只补清梯度数据，不再次退回501名，需新的胜利解锁。', '',
             '前100名来自本地118名极高战力设计。先按八人神仙类型集合去重，同集合只留实算战力最高者，再取最强100名；前十名也按此规则取最高十名。站位不同不算新阵容。未入选者保留原设计。', '',
             '第101～500名来自V1/V2：覆盖角色1～99级，每级4名，25／50／75／99级各5名；各级保留最强T1与最低T5，T2～T4轮换选两档（上述四个节点等级五档全选），再统一降序排列。角色等级与出战神仙等级分列；等级不强制随名次单调。', '',
             '战力由生产结算器重算，包含出战替补，助威经属性计入；不缩放面板、不修改源快照。来源与查询ID见同目录overview.csv及catalog.json。', '',
             '| 名次 | NPC | 战力 | 角色等级 | 出战神仙等级 | 飞升次数 | 档位／阶段 | 流派 | 八人阵容（1～4首发，5～8替补） |',
             '|---:|---|---:|---:|---|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['order']} | {r['name']} | {r['power']:,} | {r['role_level']} | {r['companion_levels']} | {r['evolve_levels']} | {r['tier']}/{r['stage'] or '常规'} | {r['archetype']} | {r['lineup']} |")
    sources = {source: hashlib.sha256((ROOT/source).read_bytes()).hexdigest() for source, _ in selected}
    files = {'catalog.json':render(manifest), 'profiles.json':render(extra), 'overview.csv':buf.getvalue(),
             '前500名战力等级明细.md':'\n'.join(lines)+'\n', 'sources.json':render(sources)}
    OUT.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        if check:
            assert (OUT/name).read_bytes() == text.encode(), name
        else:
            (OUT/name).write_bytes(text.encode())
    print(render(dict(count=len(rows), tiers=dict(Counter(r['tier'] for r in rows)), highest=rows[0]['power'], lowest=rows[-1]['power'], top10=[(r['name'],r['power']) for r in rows[:10]])))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--check', action='store_true')
    build(parser.parse_args().check)
