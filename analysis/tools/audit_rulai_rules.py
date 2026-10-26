"""Reproduce Rulai evidence directly from shipped 3.87 resources."""
import csv
import hashlib
import io
import json
import plistlib
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analysis.tools.luajit_static import parse,listing
from network_redirect import activity_rulai as r
from network_redirect.protocol import DEFS


def main():
    idx=dict(l.split('====')[:2] for l in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    out=ROOT/'analysis/evidence/rulai';out.mkdir(parents=True,exist_ok=True)
    sources=[];strings={}
    for name in ('lua/ui/turntableUI.lua','lua/ui/activityUI.lua','lua/ui/funUI.lua','lua/event_mgr.lua',
                 'lua/common/common_def.lua','lua/common/msg_def.lua','lua/ui/packageUI.lua','lua/data.lua',
                 'v2/String.plist','v2/String2.plist','csv_config/happiness_bag_config.csv','csv_config/item_base.csv','csv_config/item_name.csv'):
        path=ROOT/'jgbol3.87/assets/release_'/idx[name];raw=path.read_bytes()
        row=dict(logical=name,path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest())
        if name.endswith('.lua'):
            (out/(Path(name).stem+'.asm')).write_text(listing(parse(raw)))
        if name.endswith('.csv'):
            try:text=raw.decode('utf-8-sig')
            except UnicodeDecodeError:text=raw.decode('gb18030')
            row['csv_values_match']=list(csv.reader(io.StringIO(text)))==list(csv.reader(io.StringIO((ROOT/'analysis/configs'/Path(name).name).read_text(encoding='utf-8-sig'))))
            assert row['csv_values_match'],name
        if name.endswith('.plist'):
            strings.update({k:v for k,v in plistlib.loads(raw).items() if k.startswith('turntable_') or k=='dream20'})
        sources.append(row)
    report=dict(client='3.87',official_server_available=False,sources=sources,strings=strings,
        request=dict(id=1351,fields=DEFS[1351],operations={'enter':0,'draw':1,'bonus':2}),event=200,
        A=['activityID49; funUI gated by native start_time<now<end_time; activity_type73/event113 schedule',
           'eight wheel slots; each request draws one random item; original animation lasts5seconds',
           'recharge grants draws, cumulative recharge unlocks extra gift; thresholds and prizes supplied by server',
           'prize_status1=unavailable,2=claimable,3=claimed; callback flag drives hint',
           'happiness_bag_config:1367 -> 5 souls5053 OR50 boxes1249;1368 ->20 souls OR200 boxes',
           'native bag picker maximum15 per use; request1051 target object_type10/5 and type ID',
           'large bag short description mistakenly repeats small bag; full description and CSV agree20/200'],
        B=['weekly season at Monday00:00UTC+8, no historical schedule available',
           'cumulative each30RMB earns one draw;300RMB extra big bag once; no daily free/guarantee',
           '10base gold per simulated RMB, bonus gold excluded, partial amounts carry within season',
           'eight rewards/weights from local configuration; not certified official probability',
           'award and debit in same transaction before animation; replay cache and persisted account balances',
           'new season clears charge/draw/claim counters; inventory/souls remain; bag usage independent of season',
           'recharge close refreshes native UI; login/status updates schedule and hint'],
        inferred_config=r.load_rules())
    (out/'official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'Verified {len(sources)} original assets and {len(strings)} strings')

if __name__=='__main__':main()
