"""Reproduce anniversary evidence from the shipped 3.87 assets, not local rules."""
import csv
import hashlib
import io
import json
import plistlib
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from analysis.tools.luajit_static import parse, listing
from network_redirect import activity_yuanshi as y


def main():
    index = dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    out = ROOT/'analysis/evidence/yuanshi'; out.mkdir(parents=True, exist_ok=True)
    sources = []
    for name in ('lua/ui/twoYearsCelebrateUI.lua', 'lua/ui/activityUI.lua', 'lua/ui/funUI.lua', 'lua/event_mgr.lua',
                 'lua/common/common_def.lua', 'v2/String2.plist', 'csv_config/item_name.csv',
                 'csv_config/item_base.csv', 'csv_config/cortege_quality.csv'):
        path = ROOT/'jgbol3.87/assets/release_'/index[name]; raw = path.read_bytes()
        row = dict(logical=name, path=str(path.relative_to(ROOT)), sha256=hashlib.sha256(raw).hexdigest())
        if name.endswith('twoYearsCelebrateUI.lua'):
            asm = listing(parse(raw)); (out/'twoYearsCelebrateUI.asm').write_text(asm)
        if name.endswith('.csv'):
            try: text = raw.decode('utf-8-sig')
            except UnicodeDecodeError: text = raw.decode('gb18030')
            row['csv_values_match'] = list(csv.reader(io.StringIO(text))) == list(csv.reader(io.StringIO((ROOT/'analysis/configs'/Path(name).name).read_text(encoding='utf-8-sig'))))
            assert row['csv_values_match'], name
        if name.endswith('String2.plist'):
            strings = {k:v for k,v in plistlib.loads(raw).items() if k.startswith('twoyears_')}
        sources.append(row)
    # The absent binding is significant: getChar occurs only at its declaration.
    assert asm.count("'getChar'") == 1
    report = dict(client='3.87', official_server_available=False, sources=sources, strings=strings,
        request=dict(id=1334, fields='serial_num=I,flag=B,index=B'), event=179,
        operations=dict(enter_activity=0, take_prize=1, wish_yuanshi=2, enter_shop=3, buy_shop=4),
        A=['activityID.twoyears=46; common_config=24; begin_time/end_time gate; funUI L490-491 includes native menu',
           'gift_config has five positions; gift_list absent=locked, 0=empty, positive=claimable count',
           'activation labels: any/30/30/50/50 RMB; previous gift must activate on an earlier day',
           'two shop positions, need_gold and remaining buy_times; wish_times label is days',
           '1807 grants one extra prayer; 1808 gives level=role*2 Yuanshi; after receiving, prayer yields souls',
           'getChar and pray both send flag2,index0; native getChar lacks a widget binding'],
        B=['28-day repeating local season; no official historical schedule',
           'enroll on first entry/recharge; 1 free prayer/day, +10 percent, 1 soul after claim',
           'full progress next flag2 claims for free; duplicate grants40 souls; max original experience table level',
           'missed enrolled days accumulate supply stock; first day0; 100 gold/offering',
           'second shop slot chosen as1808 at1980 gold, daily1; inferred, not official shop evidence',
           'recharge uses existing local simulation; 10 gold/RMB, cumulative base gold excludes bonus',
           'one activation/day; any daily recharge grants each previously activated gift once; claims carry in season',
           'one click claims all copies of one gift; gift contents in configuration',
           'season rollover clears event progress/unclaimed gifts/stock, retains inventory and gods',
           'use native funUI entry; restore missing portrait button, refresh cached shop and recharge status'],
        inferred_config=y.load_rules())
    (out/'official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'Verified {len(sources)} original assets and {len(strings)} anniversary strings')


if __name__ == '__main__': main()
