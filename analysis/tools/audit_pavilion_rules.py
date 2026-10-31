"""Audit retained base evidence and final-resource pavilion catalog offline."""
import csv
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_pavilion as p


def main():
    index=dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    inputs=[]
    for name in ('csv_config/exchange_zone.csv','csv_config/gift_config.csv','csv_config/item_name.csv',
                 'csv_config/stone_cost_worth.csv','lua/ui/destinyUI.lua','lua/ui/activityUI.lua','lua/common/common_def.lua'):
        path=ROOT/'jgbol3.87/assets/release_'/index[name];blob=path.read_bytes()
        row=dict(logical=name,original=str(path.relative_to(ROOT)),sha256=hashlib.sha256(blob).hexdigest())
        if name.startswith('csv_config/'):
            row['extracted_identical']=blob.decode('utf-8-sig')==(ROOT/'analysis/configs'/name[len('csv_config/'):]).read_bytes().decode('utf-8-sig')
            assert row['extracted_identical'],name
        inputs.append(row)
    out=ROOT/'analysis/evidence/pavilion';out.mkdir(exist_ok=True)
    final_path=ROOT/'analysis/evidence/hotupdate_gap_20261031/official_csv/exchange_zone.csv'
    with final_path.open(encoding='utf-8-sig') as source:
        official={int(row['index']): row for row in csv.DictReader(source)}
    assert {i:p.SHOP[i] for i in range(1,10)}==official
    assert set(p.SHOP)==set(range(1,11))
    assert (p.SHOP[10]['goldon_count'],p.SHOP[10]['max_buy_count'])==('150','3')
    p.load_rules()
    report=dict(client='3.87/resource1263',official_server_available=False,inputs=inputs,
        final_catalog_source=str(final_path.relative_to(ROOT)),
        final_catalog_sha256=hashlib.sha256(final_path.read_bytes()).hexdigest(),
        final_nine_rows_identical=True,catalog_revision=p.CATALOG_REVISION,
        A=['1227 serial_num:I flag:B count/index/ten_card/five_card:I; event195 flags1/2/3',
           'activityUI L263 pavilion_data; destinyUI L102-109 begin_time<now<end_time',
           'destinyUI L155 item1141, L621/623 cards1142=5/1143=10, L840 total cards<=gift count',
           'destinyUI L368: 1 RMB = 1 brick; String2 destiny12 first exchange bonus delivered by mail',
           'resource1263 exchange_zone: first 9 goods match final prices/limits/attachments/gifts; last changed in1262',
           'gift_config type1 six recharge bonus rows; type2 four thresholds based on server-wide bricks (destinyUI L441)',
           'destinyUI L902-907 clamps discounted total to zero; L955 decrements count after reward dismissal',
           'destinyUI L509-511 shows need_charge and plus_times only after quota exhaustion; destiny14 means next purchase-limit increase, not increases already earned'],
        B=['local gem package at index10: 150 bricks, limit3; retained original gem rewards and first gift',
           'legacy purchases migrate by product identity; no price refunds or first-gift supplements; pending mail retained',
           'permanent 14-day recurring local period anchored at 1970-01-05 Monday UTC+8; principal/10 RMB; no history retroactivity',
           'type1 milestones paid once each per period; base and bonus delivered together by permanent mail',
           'server total uses actual current-period local-account bricks earned (including unclaimed mail), no simulated strangers',
           'each account may claim four public gifts once, including non-paying accounts',
           'index1 gains one extra purchase per 300 RMB, max10; all counters reset each period; coupons persist',
           'all remaining bricks, including unclaimed mail, convert 1:1 to item1001 peaches in permanent refund mail; legacy seven-day saves migrate once',
           'no global gift escalation invented because original shipped table has no threshold or alternative reward'],
        shop=p.SHOP,gifts=p.GIFTS)
    (out/'catalog_1263_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Verified final 9 goods + local gem package, 6 bonus tiers, 4 public gifts')

if __name__=='__main__':main()
