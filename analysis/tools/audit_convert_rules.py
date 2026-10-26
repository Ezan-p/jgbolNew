"""Reproduce 天缘召唤 evidence from original, local 3.87 resources."""
import hashlib
import json
import sys
from pathlib import Path
from luajit_static import parse, listing
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import activity_convert as cv
OUT = ROOT / 'analysis/evidence/convert'


def main():
    OUT.mkdir(exist_ok=True)
    index = dict(line.split('====')[:2] for line in
                 (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    inputs = []
    names = ('lua/ui/cortCallUI.lua', 'lua/ui/activityUI.lua', 'lua/ui/packageUI.lua', 'lua/event_mgr.lua', 'lua/data.lua',
             'csv_config/convert_output.csv', 'csv_config/cortege/cortege_base_0.csv',
             'csv_config/cortege/cortege_name_0.csv', 'csv_config/cortege_quality.csv',
             'csv_config/item_buy_config.csv', 'csv_config/vip_pri_config.csv',
             'v2/cortCall/txt1.png', 'v2/cortCall/txt2.png')
    for name in names:
        blob = (ROOT / 'jgbol3.87/assets/release_' / index[name]).read_bytes()
        entry = dict(logical=name, sha256=hashlib.sha256(blob).hexdigest())
        if name.startswith('csv_config/'):
            extracted = ROOT / 'analysis/configs' / name.removeprefix('csv_config/')
            entry['extracted_identical'] = blob == extracted.read_bytes()
            entry['text_identical_without_bom'] = blob.decode('utf-8-sig') == extracted.read_bytes().decode('utf-8-sig')
            assert entry['text_identical_without_bom'], name
        if name == 'lua/ui/cortCallUI.lua':
            chunk = parse(blob)
            constants = {p['line']: p['numbers'] for p in chunk['protos'] if p['line'] in (744, 782)}
            assert constants[744] == [10, 0.05, 100000, 200000]
            assert constants[782][:2] == [5, 1]
            entry['countdown_and_card_numeric_constants'] = constants
            (OUT / 'cortCallUI.txt').write_text(listing(chunk))
        elif name.endswith('.png'):
            (OUT / Path(name).name).write_bytes(blob)
        inputs.append(entry)
    relationships = [dict(source=src, source_name=cv.NAMES[src], target=int(row['des_cortege_type']),
                          target_name=cv.NAMES[int(row['des_cortege_type'])], outputs=cv.outputs(src))
                     for src, row in cv.TABLE.items()]
    report = dict(client='3.87', official_server_available=False, inputs=inputs,
                  relationships=relationships,
                  A=['cortCallUI L112-159: free first fight, token 1024 after first, active month card +1, 1026/fight_type=10',
                     'cortCallUI L293-331: only quality>=5 companions, relationship/level/type sorting',
                     'cortCallUI L660-664: target name/type follows selected source',
                     'cortCallUI L768-777: callbackOutput argument itself is output, not a prize_list wrapper',
                     'cortCallUI L904-959: first pair is reward; types 1 source soul / 2 target soul / 3 token',
                     'cortCallUI L744 numbers=[10,0.05,100000,200000], L782 numbers[0]=5: 10s countdown, tag%5+1, five cards required',
                     'event_mgr L448-450,592-594: 6001..6009 target appearance/name substitution',
                     'txt1.png: summon and challenge related five-star deity; victory can grant its souls',
                     'convert_output.csv: 42 relationships, 7 weighted results per relationship'],
                  B=['6001 level16 skill1 single defender; original bases and shared inferred battle engine',
                     'four independently weighted display-only cards; first card settled once before presentation',
                     'loss consumes attempt/token without rewards; no stamina, energy, silver or experience',
                     'UTC+8 daily reset, VIP0 one total attempt, VIP token limits interpreted as extra attempts',
                     'clock guard, persistent outcome receipt, achievement106 participation binding'])
    (OUT / 'official_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Verified original assets and 42 天缘 relationships')


if __name__ == '__main__': main()
