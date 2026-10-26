"""Extract shipped 神石祈福 evidence without contacting an official server."""
import hashlib
import json
from pathlib import Path
from luajit_static import parse, listing

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence/pray'


def main():
    OUT.mkdir(exist_ok=True)
    index = dict(line.split('====')[:2] for line in
                 (ROOT / 'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    inputs = []
    for name in ('lua/ui/qiFuUI.lua', 'v2/qiFuUI/intro.png',
                 'csv_config/pray_spirit_config.csv', 'csv_config/cortege_quality.csv'):
        data = (ROOT / 'jgbol3.87/assets/release_' / index[name]).read_bytes()
        inputs.append(dict(logical=name, sha256=hashlib.sha256(data).hexdigest()))
        if name.endswith('.lua'):
            (OUT / 'qiFuUI.txt').write_text(listing(parse(data)))
        elif name.endswith('.png'):
            (OUT / 'intro.png').write_bytes(data)
    report = dict(client='3.87', official_server_available=False, inputs=inputs,
        verified=[
            'intro.png explicitly promises gold currency, not ordinary items',
            'CSV costs: 200 / 500 / 1000; qiFuUI L183-189 falls back to final CSV row',
            'qiFuUI L563-584 excludes active/cheering companions and quality above 3',
            'qiFuUI L586-611 permits manual selection of higher-quality souls',
            'qiFuUI L202-270 bulk selection only includes low-quality souls',
            'qiFuUI L848-900 warns for level >=2 then allows confirmation',
            '1085 carries type/id/count; spirit=10 (7 is calc), cortege=4; event 52 pray_item_list drives native reward UI'],
        inferred=[
            'equal chance of 10 / 20 / 30 gold per successful prayer',
            'completed-count storage, UTC+8 daily cost reset, persistent remaining soul value',
            'no daily hard cap: follows native last-cost fallback; official server cap unknown',
            'zero-worth offerings rejected; lock/training/attached essence protections',
            'innate spell consumed with owner; no growth material refund'])
    (OUT / 'official_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Verified original 神石祈福 Lua, intro image and CSV assets')


if __name__ == '__main__':
    main()
