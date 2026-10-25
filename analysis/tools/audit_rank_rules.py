"""Verify preserved original rank CSVs and record reproducible offline roster."""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_rank as rank

def main():
    index=dict(l.split('====')[:2] for l in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    enc={v['logical']:v['encoding'] for v in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
    sources=[]
    for name in ('top_score','top_score_exchange'):
        logical='csv_config/'+name+'.csv';p=ROOT/'jgbol3.87/assets/release_'/index[logical]
        original=list(csv.reader(io.StringIO(p.read_bytes().decode(enc[logical]))))
        extracted=list(csv.reader(io.StringIO((ROOT/'analysis/configs'/ (name+'.csv')).read_text(encoding='utf-8-sig'))))
        assert original==extracted
        sources.append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),csv_values_match=True))
    for name in ('ui/rankUI','ui/checkLineupUI','ui/fightrecordUI','event_mgr','common/common_def'):
        p=ROOT/'jgbol3.87/assets/release_'/index['lua/'+name+'.lua']
        sources.append(dict(logical=name,path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    for name in ('analysis/npc_design/v1/catalog.json','server_config/rank_rules.json'):
        p=ROOT/name;sources.append(dict(path=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    rows=[dict(identity=ident,initial_order=ident-930000,npc_id=n['npc_id'],level=n['role']['level'],tier=n['tier'],archetype=n['archetype'],power=n['role']['role_combat_power']) for ident,n in rank.catalog().items()]
    out=ROOT/'analysis/evidence/rank';out.mkdir(exist_ok=True)
    (out/'audit.json').write_text(json.dumps(dict(original_server_available=False,source_policy='A=original client/CSV; B=offline inferred rules; C=NPC design',sources=sources,ladder=rows),ensure_ascii=False,indent=2)+'\n')
    print('Verified original rank tables; recorded 99 NPC identities and powers')
if __name__=='__main__':main()
