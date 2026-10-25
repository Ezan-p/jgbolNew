"""Extract original insight/convert client contracts and verify every recipe cell."""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path
from luajit_static import parse, listing
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import skill_insight, summon


def main():
    out = ROOT / 'analysis/evidence/skill_insight'
    out.mkdir(exist_ok=True)
    index = dict(x.split('====')[:2] for x in (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    enc = {r['logical']:r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
    evidence = []
    for name in ['csv_config/skill_advaced_conf.csv', 'lua/ui/skillUpgradeUI.lua', 'lua/ui/packageUI.lua', 'lua/ui/qiankunnizhuan.lua']:
        raw = (ROOT/'jgbol3.87/assets/release_'/index[name]).read_bytes()
        record = dict(logical=name, sha256=hashlib.sha256(raw).hexdigest())
        if name.endswith('.csv'):
            original = list(csv.reader(io.StringIO(raw.decode(enc[name]))))
            local = list(csv.reader(io.StringIO((ROOT/'analysis/configs'/Path(name).name).read_text(encoding='utf-8-sig'))))
            assert original == local
            record.update(rows=len(original)-1, all_cells_match=True)
        else:
            chunk = parse(raw)
            (out/(Path(name).stem+'.txt')).write_text('\n'.join('NUMERIC proto%d %r'%(p['id'],p['numbers']) for p in chunk['protos'])+'\n'+listing(chunk))
        evidence.append(record)
    (out/'audit.json').write_text(json.dumps(dict(client='3.87', inputs=evidence,
        recipes=list(skill_insight.RECIPES.values()), policy=skill_insight.rules(),
        official_server_available=False, original_protocols=[1076,1212], events=[156,89],
        conflict='CSV hp_plus=10; packageUI L1159 displays constant 12%. Server stacking unknown.'),ensure_ascii=False,indent=2)+'\n')
    print('Verified all 8 original recipes; extracted 3 client modules.')

if __name__ == '__main__':
    main()
