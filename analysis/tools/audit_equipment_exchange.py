"""Compare exchange evidence against untouched original 3.87 assets."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import equipment_crafting as c


def main():
    index=dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    enc={r['logical']:r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
    records=[]
    for logical in ('lua/ui/forgeUI.lua','lua/ui/funUI.lua','lua/ui/activityUI.lua',
                    'lua/ui/packageUI.lua','csv_config/item_buy_config.csv','csv_config/material_transform.csv'):
        path=ROOT/'jgbol3.87/assets/release_'/index[logical];raw=path.read_bytes()
        record=dict(logical=logical,asset=index[logical],sha256=hashlib.sha256(raw).hexdigest())
        if logical.endswith('.csv'):
            original=list(csv.reader(io.StringIO(raw.decode(enc[logical]))))
            local=list(csv.reader(io.StringIO((ROOT/'analysis/configs'/Path(logical).name).read_text(encoding='utf-8-sig'))))
            assert original==local,logical
            record.update(csv_values_match=True,rows=len(original)-1)
        records.append(record)
    report=dict(inputs=records,verified_original={
        'wire':'1055 query; 1053 compose_type 1/2/3; events 7 and 6',
        'forgeUI:579-581':'returnBack calls activityUI.returnBack without removing its own layer',
        'forgeUI:734-782':'getForgeResult subtracts reward count from left_times at L755',
        'forgeUI:785-818':'query left_times=count_limit-exchanged_count; flag=1 means forged',
        'forgeUI:141-155':'materials iterate main_type weapon through guard, matching quality and equip_order=0',
        'forgeUI:640-663':'enhanced equipment above level 10 triggers confirmation in original UI',
        'forgeUI:488,544':'both target/name loops are fixed at three slots',
        'forgeUI:77-81':'5-star tokens 1008/1009/1010; 4-star tokens 1011/1012/1013',
        'item_buy_config':'six token prices 1500/1500/2000/200/200/500, count=1, VIP=0',
        'packageUI:1903-1904':'using item 1003 calls forgeUI.show',
        'funUI':'forge entry absent from funConfig and activity list'},
        inferred_local=dict(rules=c.load_rules(),
            offered_equipment=len(c.compose_list({},c.load_rules())['equip_compose']['appoint']),
            details='Local catalog, 5 non-advanced 4-star weapons/armor, 40 shards per transaction, level 5, no enhancement silver refund, protection of advanced/reborn materials, ongoing activity and token sale period are server-policy completions, not verified original server values. User-requested weekly policy: one shared equipment/shard exchange per role, resetting Monday 00:00 UTC+8 without carryover; same equipment may be exchanged again next week.'))
    path=ROOT/'analysis/evidence/equipment_exchange/official_audit.json';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Original assets hashed; both CSV tables match; original/local policy recorded.')


if __name__=='__main__':main()
