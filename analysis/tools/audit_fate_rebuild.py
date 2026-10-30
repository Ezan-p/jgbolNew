"""Extract only the active, frozen hot-update resources required by fate rebuilding."""
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'analysis/tools'))
from luajit_static import parse, listing, static_tables
SOURCE = ROOT / '.runtime/offline-toolchain/device-release_w'
OUT = ROOT / 'analysis/evidence/fate_rebuild'
CONFIG = ROOT / 'analysis/configs/fate_rebuild'
TABLES = ['faterebuild_cort_active', 'rebuild_material_costs', 'stars_effect_config',
          'level_effect_config', 'select_effect_config', 'rebuild_material_zs_costs',
          'faterebuild_cort_property', 'faterebuild_unblock_effect',
          'cor_level_effect_config', 'jp_level_effect_config']
MODULES = ['ui/ascensionUI', 'ui/fateRebuildUI', 'ui/soulUI', 'ui/soulSevenUI', 'common/common_def', 'common/msg_def', 'event_mgr']

def main():
    OUT.mkdir(exist_ok=True); CONFIG.mkdir(parents=True, exist_ok=True)
    version, encoded = (SOURCE / 'index.txt').read_text().split('\n', 1)
    alphabet = 'yfglmnovwxapzdechijkqrstbuHOMICDJPQRSTUVWXYZABKEFGLN39+0126-4785'
    decoded = base64.b64decode(encoded.translate(str.maketrans(alphabet + '_',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='))).decode('gb18030')
    index = dict(line.split('====')[:2] for line in decoded.splitlines())
    inputs = []
    def read(name):
        path = SOURCE / index[name]
        data = path.read_bytes()
        inputs.append(dict(logical=name, physical=index[name], sha256=hashlib.sha256(data).hexdigest()))
        return data
    for name in TABLES + ['item_base', 'item_name', 'exchange_zone']:
        raw = read('csv_config/' + name + '.csv')
        try: text = raw.decode('utf-8-sig')
        except UnicodeDecodeError: text = raw.decode('gb18030')
        rows = list(csv.reader(io.StringIO(text)))
        if name in ('item_base', 'item_name'):
            # Keep all original shipped rows untouched. These six material IDs
            # were introduced by this hot-update, including the three soul stones.
            rows = rows[:1] + [r for r in rows[1:] if 1370 <= int(r[0]) <= 1375]
        elif name == 'exchange_zone':
            rows = rows[:1] + [r for r in rows[1:] if r[-1] == 'nitian']
            # Append after existing nine products: never reassign persisted IDs.
            rows[1][0] = '10'
        with (CONFIG / (name + '.csv')).open('w', newline='') as f:
            csv.writer(f).writerows(rows)
    for name in MODULES:
        chunk = parse(read('lua/' + name + '.lua'))
        (OUT / (Path(name).stem + '.txt')).write_text(
            '\n'.join('NUMERIC proto%d %r' % (p['id'], p['numbers']) for p in chunk['protos']) + '\n' + listing(chunk))
        if name == 'common/common_def':
            attrs = next(t['value'] for p in chunk['protos'] for t in p['kgc']
                         if isinstance(t, dict) and t.get('kind') == 'table' and 'fate_rebullding_state' in t['value'])
            attrs = {k:v for k,v in attrs.items() if 340 <= v <= 391}
            (ROOT/'server_config/fate_rebuild_attributes.json').write_text(json.dumps(attrs,indent=2)+'\n')
    report = dict(source_version=version, inputs=inputs, activation=dict(realm=4,item=1371,count=20),
                  request=dict(id=1357, definition='serial_num=I,id=B,data=s'),
                  catalog_policy='append nitian as index 10; existing IDs and progress preserved',
                  formula_policy='Original node/milestone values; server stacking order is locally reconstructed')
    (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Extracted active fate resources and six material definitions; original base CSVs preserved.')

if __name__ == '__main__': main()
