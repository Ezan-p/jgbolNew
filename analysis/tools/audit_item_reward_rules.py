"""Verify original assets, enumerate every container/shard and export exact pools."""
import csv
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import item_rewards as r, equipment_crafting as c, summon
from luajit_static import parse, listing, decode

OUT = ROOT / 'analysis/evidence/item_rewards'


def main():
    OUT.mkdir(exist_ok=True)
    index = dict(line.split('====')[:2] for line in
                 (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    encodings = {row['logical']: row['encoding'] for row in json.loads(
        (ROOT/'analysis/evidence/config_inventory.json').read_text())}
    inputs = []
    for name in ('item_base', 'item_name', 'skill_base', 'skill_name', 'material_transform',
                 'item_receive_config', 'happiness_bag_config', 'babel_tower_floor_prize'):
        logical = 'csv_config/'+name+'.csv'
        raw = (ROOT/'jgbol3.87/assets/release_'/index[logical]).read_bytes()
        original = list(csv.reader(io.StringIO(raw.decode(encodings[logical]))))
        local = list(csv.reader(io.StringIO((ROOT/'analysis/configs'/(name+'.csv')).read_text(encoding='utf-8-sig'))))
        assert original == local, logical
        inputs.append(dict(logical=logical, asset=index[logical], sha256=hashlib.sha256(raw).hexdigest(), csv_matches=True))
    for name in ('ui/packageUI', 'ui/equipPieceUI', 'ui/smithUI', 'data'):
        logical = 'lua/'+name+'.lua'
        raw = (ROOT/'jgbol3.87/assets/release_'/index[logical]).read_bytes()
        chunk = parse(raw)
        if name == 'data':
            names = {}
            for proto in chunk['protos']:
                for first, second in zip(proto['code'], proto['code'][1:]):
                    op, _, _, _, d = decode(first)
                    op2, _, _, _, d2 = decode(second)
                    if op == 'FNEW' and op2 == 'GSET':
                        names[proto['kgc'][d]['id']] = proto['kgc'][d2]
            chunk = dict(chunk, protos=[p for p in chunk['protos'] if names.get(p['id']) in
                         ('getItemFromStr', 'getItemListFromStr', 'getTransInfoByTypeid')])
        (OUT/(name.replace('/','_')+'.txt')).write_text(listing(chunk))
        inputs.append(dict(logical=logical, asset=index[logical], sha256=hashlib.sha256(raw).hexdigest()))
    rules = r.load_rules()
    containers = []
    delegates = {
        **{tid:'qiankun_bags.py / qiankun_bag_rules.json (B user design)' for tid in (1031,1032,1033,1034)},
        1037:'activity_hunt.py / hunt_rules.json soul_box_pool (B equal weights)',
        1120:'guild_feast.py / guild_rules.json feast_box_rewards (B fixed)',
        1121:'guild_feast.py / guild_rules.json feast_box_rewards (B fixed)',
        1243:'activity_nine_sky.py / nine_sky_rules.json (A soul 5; B peaches)',
        1249:'xianling.py / xianling_rules.json (A chosen target; B cost)',
        1324:'activity_hunt.py / hunt_rules.json upgrade_box_pool (B equal weights)',
        1346:'pets.py / pet_rules.json training_box_count (A training pills; B fixed amount)',
        1367:'activity_rulai.py / happiness_bag_config.csv (A choice)',
        1368:'activity_rulai.py / happiness_bag_config.csv (A choice)',
        1808:'activity_yuanshi.py (A named companion at role level * 2; B duplicate conversion)',
    }
    delegates.update({t:'vip.py / item_receive_config.csv (A fixed contents)' for t in range(1101,1111)})
    delegates.update({t:'activity_rice.py / moon_rules.json (B shared weighted pools, independent draws)' for t in range(1213,1217)})
    delegates[1217]='activity_seasonal.py / activity_rules.json seasonal_food_rewards (B legacy fixed)'
    assert set(delegates) == r.SPECIAL
    for tid in sorted(r.CONTAINERS):
        entry=dict(id=tid, original=r.NAMES[tid], handler=delegates.get(tid,'item_rewards.py'),
                   rule=rules['items'].get(str(tid)))
        containers.append(entry)
    fragments=[]
    for tid, name in r.NAMES.items():
        if '碎片' not in name['name']: continue
        row, src = c.recipe_for(dict(attach_type=5,type_id=tid,level=1),2)
        original=c.parts(row[c.DEST]);effective=r.recipe_destinations(row,tid)
        total=sum(p[4] for p in effective) if row['is_random']=='1' else 1
        fragments.append(dict(id=tid,name=name['name'],source=src,cost=c.parts(row[c.COST]),
            min_level=int(row['min_role_level']),is_random=int(row['is_random']),
            original_destinations=original,effective_destinations=effective,
            probabilities=[dict(reward=p[:4],probability=str(Fraction(p[4],total)) if row['is_random']=='1' else '1') for p in effective],
            classification='B: documented duplicate correction' if original!=effective else 'A: original candidates and weights; B: normalized one-result settlement'))
    pools={}
    for name,groups in rules['pools'].items():
        total=sum(g['weight'] for g in groups)
        pools[name]=[dict(reward=p,probability=str(Fraction(g['weight'],total*len(g['candidates']))))
                     for g in groups for p in g['candidates']]
    report=dict(official_server_available=False,inputs=inputs,container_count=len(containers),
                fragment_count=len(fragments),containers=containers,fragments=fragments,effective_box_pools=pools,
                map_only_boxes=[dict(id=t,handler='activity_babel.py / 1353 op=2; matching key required; floor pool',
                                    classification='A: map identity; B: equal CSV-entry weights, not inventory 1051') for t in (20007,20008,20009)],
                excluded_same_main_type=sorted(r.NON_CONTAINERS))
    (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'Verified 8 original CSVs, 4 original Lua modules; {len(containers)} containers, {len(fragments)} fragments, 3 map boxes.')


if __name__=='__main__':
    main()
