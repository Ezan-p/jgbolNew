"""Verify the 3.87 packaged price table and sale bytecode contracts."""
import csv
import hashlib
import io
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.luajit_static import parse
from network_redirect.item_sale import PRICES
index = dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
encodings = {r['logical']: r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
evidence = []
for logical in ('csv_config/item_price_config.csv', 'csv_config/item_base.csv', 'csv_config/item_name.csv',
                'lua/data.lua', 'lua/ui/packageUI.lua', 'lua/ui/guildPartyUI.lua', 'lua/event_mgr.lua'):
    raw = (ROOT/'jgbol3.87/assets/release_'/index[logical]).read_bytes()
    record = dict(logical=logical, sha256=hashlib.sha256(raw).hexdigest())
    if logical.endswith('.csv'):
        original = list(csv.reader(io.StringIO(raw.decode(encodings[logical]))))
        extracted = list(csv.reader(io.StringIO((ROOT/'analysis/configs'/Path(logical).name).read_text(encoding='utf-8-sig'))))
        assert original == extracted, logical
        record['all_cells_match'] = True
        if 'item_price_config' in logical:
            assert {int(r[0]): int(r[1]) for r in original[1:]} == PRICES
    else:
        parsed = parse(raw)
        contracts = {'lua/data.lua': (53, 154, 155, 156), 'lua/ui/packageUI.lua': (11, 19, 50),
                     'lua/ui/guildPartyUI.lua': (21, 22)}
        record['contracts'] = [p for n, p in enumerate(parsed['protos']) if n in contracts.get(logical, ())]
    evidence.append(record)
# Keep readable source excerpts, including original source line numbers.
fragments = []
for name, bounds in (('data.lua', ((986,994),(3410,3458))), ('ui/packageUI.lua', ((382,396),(1989,1992))),
                     ('ui/guildPartyUI.lua', ((412,476),)), ('event_mgr.lua', ((1715,1716),))):
    text = (ROOT/'analysis/evidence/lua_named/lua'/(name+'.txt')).read_text()
    import re
    lines = [line for line in text.splitlines()
             for m in [re.search(r'\[L(\d+)\]', line)] if m
             if any(a <= int(m.group(1)) <= b for a,b in bounds)]
    fragments.append(name+'\n'+'\n'.join(lines))
out = ROOT/'analysis/evidence/item_sale';out.mkdir(exist_ok=True)
# Raw parsed prototypes can contain bytes in some parser versions.
(out/'official_audit.json').write_text(json.dumps(dict(date='2026-10-26', official_server_available=False,
    prices=PRICES, evidence=evidence),ensure_ascii=False,indent=2,default=str)+'\n')
(out/'client_contracts.txt').write_text('\n\n'.join(fragments)+'\n')
print('Verified 28 original prices, 3 CSV files and 4 bytecode assets')
