#!/usr/bin/env python3
"""Persist reproducible random identities for both original NPC batches."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import npc_players as players, role_profile, combat_power, formation
from analysis.tools.build_npc_catalog import csv_text,json_text,NAMES


def source_npcs():
    paths=[ROOT/'analysis/npc_design/v1/catalog.json']
    index=ROOT/'analysis/npc_design/v2/catalog.json'
    paths += [index.parent/f for f in json.loads(index.read_text())['files']]
    for path in paths:
        version='v1' if path==paths[0] else 'v2'
        for npc in json.loads(path.read_text())['npcs']:
            yield version,path,npc


def build(check=False):
    r=players.rules(); out=ROOT/'analysis/npc_design/players'
    entries=[]; ids=set(); names=set(); sources={}
    snapshots=list(source_npcs())
    for version,path,n in sorted(snapshots,key=lambda x:x[2]['npc_id']):
        role=n['role']; key=n['npc_id']
        seed=int.from_bytes(hashlib.sha256(f"{r['seed']}:{key}".encode()).digest()[:8],'big')
        rng=random.Random(seed)
        identity=rng.randint(r['id_min'],r['id_max'])
        while identity in ids: identity=rng.randint(r['id_min'],r['id_max'])
        ids.add(identity)
        name=rng.choice(r['name_prefixes'])+''.join(rng.sample(r['name_chars'],2))
        while name in names: name=rng.choice(r['name_prefixes'])+''.join(rng.sample(r['name_chars'],2))
        names.add(name)
        head=rng.choice(r['heads'])
        p=dict(role_id=identity,role_name=name,head_type=head,gender='男' if head<200 else '女',
               vip_level=rng.randint(*r['vip_ranges'][n['tier']]),level=role['level'],tier=n['tier'],
               role_combat_power=role['role_combat_power'],reborn_layer=role.get('reborn_layer',0),
               cur_genius_type=rng.choice(sorted(t for t,row in role_profile.RUNES.items() if int(row['open_level'])<=role['level'])),
               region=rng.choice(r['regions']),personality=rng.choice(r['personalities']),
               active_period=rng.choice(r['active_periods']),signature=rng.choice(r['signatures']),
               preferred_archetype=n['archetype'],union_id=0,union_name='',title_id=0,is_npc=True)
        e=dict(npc_id=key,version=version,legacy_role_id=int(role['role_id']),
               source_file=str(path.relative_to(ROOT)),profile=p)
        entries.append(e)
        relative=str(path.relative_to(ROOT))
        if relative not in sources:
            sources[relative]=hashlib.sha256(path.read_bytes()).hexdigest()
    data=dict(schema_version=1,revision=r['revision'],players=entries)
    rendered=json_text(data)
    if not check:
        out.mkdir(parents=True,exist_ok=True)
        (out/'catalog.json').write_text(rendered)
    else:
        assert (out/'catalog.json').read_text()==rendered,'NPC身份资料不可复现'
    players.clear_cache()
    stats=[]; max_packet=0
    for version,path,n in snapshots:
        enriched=players.decorate(n)
        report=combat_power.explain(enriched['role'],formation.load_rules())
        assert report['total']==n['role']['role_combat_power'],n['npc_id']
        packet=players.summon.event(11,players.inspection_data(enriched))
        max_packet=max(max_packet,len(packet))
        profile=players.catalog()[n['npc_id']]['profile']
        stats.append(dict(npc_id=n['npc_id'],version=version,**profile,
                          lineup=' / '.join(f"{c['order']}:{NAMES[c['type']]}" for c in sorted(n['role']['corteges'],key=lambda c:c['order']) if c['order'])))
    stats.sort(key=lambda x:(x['version'],x['level'],x['tier'],x['npc_id']))
    summary=dict(player_count=len(entries),versions=dict(Counter(e['version'] for e in entries)),
                 unique_ids=len(ids),unique_names=len(names),head_counts=dict(Counter(e['profile']['head_type'] for e in entries)),
                 unchanged_combat_power=len(stats),encoded_lineup_packets=len(stats),maximum_lineup_packet_bytes=max_packet,
                 native_packet_limit=32768,source_snapshots_modified=False)
    files={'catalog.json':rendered,'overview.csv':csv_text(stats),'validation.json':json_text(summary),
           'sources.json':json_text(sources)}
    lines=['# NPC玩家资料目录','', '游戏内进入好友／关注的“其他玩家”，搜索下表姓名或数字玩家ID，点击名字选择查看阵容。',
           '也可按自身等级浏览同等级NPC。头像、VIP为离线角色设计资料，籍贯和签名为虚构背景。',
           '本目录的随机玩家ID为正式查询ID，V1/V2原角色编号仅为兼容别名。','']
    for version in ('v1','v2'):
        lines += [f'## {version.upper()}','', '| NPC | 玩家ID | 姓名 | 头像 | 等级／档位 | VIP | 战力 | 籍贯／性格 | 阵容 |',
                  '|---|---:|---|---:|---|---:|---:|---|---|']
        for row in stats:
            if row['version']==version:
                lines.append(f"| {row['npc_id']} | {row['role_id']} | {row['role_name']} | {row['head_type']} | {row['level']}／{row['tier']} | {row['vip_level']} | {row['role_combat_power']:,} | {row['region']}／{row['personality']} | {row['lineup']} |")
        lines.append('')
    files['玩家资料目录.md']='\n'.join(lines)+'\n'
    for name,value in files.items():
        if check:
            assert (out/name).read_bytes()==value.encode(),name+'发生变化'
        else:
            (out/name).write_bytes(value.encode())
    assert all(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha for path,sha in sources.items())
    print(json_text(summary))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args();build(args.check)
