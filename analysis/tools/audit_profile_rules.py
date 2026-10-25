"""Rebuild profile contracts from original APK resources (no original server data)."""
import csv
import hashlib
import io
import json
import plistlib
from pathlib import Path
from luajit_static import parse, listing
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence/profile'
OUT.mkdir(parents=True, exist_ok=True)
index = dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
enc = {r['logical']: r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
inputs = []
for name in ['lua/'+n+'.lua' for n in ('ui/runeUI','ui/mainUI','ui/honorUI','ui/commonLayerUI','ui/fightUI','event_mgr','common/common_def')]+['csv_config/'+n+'.csv' for n in ('rune','title_config','item_name','item_buy_config')]:
    path = ROOT/'jgbol3.87/assets/release_'/index[name]
    inputs.append(dict(logical=name, physical=str(path.relative_to(ROOT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    if name.endswith('.lua'):
        chunk = parse(path.read_bytes())
        (OUT/(name[4:-4].replace('/','_')+'.txt')).write_text('\n'.join('NUMERIC proto%d %r'%(p['id'],p['numbers']) for p in chunk['protos'])+'\n'+listing(chunk))
    else:
        original = list(csv.reader(io.StringIO(path.read_bytes().decode(enc[name]).replace('\r',''))))
        extracted = list(csv.reader(io.StringIO((ROOT/'analysis/configs'/Path(name).name).read_bytes().decode('utf-8-sig').replace('\r',''))))
        assert original == extracted, name
        inputs[-1]['csv_values_match'] = True
path = ROOT/'jgbol3.87/assets/release_/e926a25accffd37afafb015933e815d4.data'
strings = plistlib.loads(path.read_bytes().lstrip(b'\xef\xbb\xbf'))
inputs.append(dict(physical=str(path.relative_to(ROOT)), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(OUT/'strings.json').write_text(json.dumps({k:v for k,v in strings.items() if 'modify_name' in k or 'change_head' in k}, ensure_ascii=False, indent=2)+'\n')
(OUT/'audit.json').write_text(json.dumps(dict(client='3.87', official_server_available=False, inputs=inputs,
    requests=[1031,1069,1070,1078,1307], replies=[1032,1077,1106], events=[12,99,109,159,175],
    rules='server_config/profile_rules.json'), ensure_ascii=False, indent=2)+'\n')
print('Verified 7 original Lua modules, 4 CSV tables and original localization.')
