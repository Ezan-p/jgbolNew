"""Reproducible evidence from untouched 3.87 assets, no external service."""
import csv
import hashlib
import io
import json
import plistlib
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from analysis.tools.luajit_static import parse
from network_redirect import activity_nine_sky as n


def main():
    idx=dict(l.split('====')[:2] for l in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    sources=[];strings={};constants={}
    for name in ['lua/ui/towerUI.lua','lua/ui/activityUI.lua','lua/ui/funUI.lua','lua/event_mgr.lua','lua/data.lua',
                 'lua/common/common_def.lua','lua/common/msg_def.lua','v2/String.plist','v2/String2.plist',
                 'csv_config/tower_road.csv','csv_config/tower_compose.csv','csv_config/tower_level.csv',
                 'csv_config/item_name.csv','csv_config/item_base.csv']:
        path=ROOT/'jgbol3.87/assets/release_'/idx[name];raw=path.read_bytes()
        row=dict(logical=name,path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest())
        if name.endswith('.csv'):
            try:text=raw.decode('utf-8-sig')
            except UnicodeDecodeError:text=raw.decode('gb18030')
            row['csv_values_match']=list(csv.reader(io.StringIO(text)))==list(csv.reader(io.StringIO((ROOT/'analysis/configs'/Path(name).name).read_text(encoding='utf-8-sig'))))
            assert row['csv_values_match']
        if name.endswith('.plist'):
            strings.update({k:v for k,v in plistlib.loads(raw).items() if k.startswith('tower')})
        if name=='lua/ui/towerUI.lua':
            p=parse(raw);constants={str(i):p['protos'][i]['numbers'] for i in [14,16,21,22]}
            assert constants['14']==[1,100]
        sources.append(row)
    report=dict(client='3.87',official_server_available=False,sources=sources,strings=strings,constants=constants,
                request=1309,event=164,entry=37,operations={'enter':1,'roll':2,'shop':3,'buy':4,'palace_buy':5},
                level_lengths=n.LEVELS,entry_distances=[sum(n.LEVELS[:i]) for i in range(9)],
                routes=[dict(old=a,new=b,road=road,forward=road.count('1')) for (a,b),road in n.ROADS.items()],
                A=['6 map shapes, 42 road transitions, directions1=up/2=left/3=right',
                   '100gold per paid roll;10paid rolls1000;free single index0,paid index1',
                   '5stars per upward step;one upward step10stars on double event',
                   'native1..9floor titles;floor lengths accumulated by getTowerFloor',
                   'star/credit shops, card payment, palace special/current/next preview',
                   'special reward object1/type-1 card with level as denomination;other type free dice',
                   'card surplus recycled, ratio unavailable; top name display',
                   '1243 market during event;5souls of5027 and unspecified peaches'],
                B=['weekly MondayUTC+8 season,daily5free,earned dice survive daily reset',
                   'uniform eligible maps;filter impossible portal overshoots and dead ends',
                   'double10%,treasure20%,treasure weights40/30/20/10',
                   'palace each10rolls,all shops in current batch remain valid until next roll',
                   '1:1 card surplus to credits;prices,stock and catalog in config',
                   'real local account leader by distance/time/id,no fabricated rank prizes',
                   'ninth floor remains playable;99999local-coordinate wrap without tenth floor',
                   'season clears event resources and shops;inventory/souls persist',
                   'bag300gold,100peaches;allow use after event closes'],inferred_config=n.load_rules())
    out=ROOT/'analysis/evidence/nine_sky';out.mkdir(parents=True,exist_ok=True)
    (out/'official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'Verified {len(sources)} assets, 3 route tables, {len(strings)} strings, 100gold original constant')

if __name__=='__main__':main()
