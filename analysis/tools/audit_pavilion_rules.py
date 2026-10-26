"""Reproduce original 3.87 pavilion rules without contacting a former server."""
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
    report=dict(client='3.87',official_server_available=False,inputs=inputs,
        A=['1227 serial_num:I flag:B count/index/ten_card/five_card:I; event195 flags1/2/3',
           'activityUI L263 pavilion_data; destinyUI L102-109 begin_time<now<end_time',
           'destinyUI L155 item1141, L621/623 cards1142=5/1143=10, L840 total cards<=gift count',
           'destinyUI L368: 1 RMB = 1 brick; String2 destiny12 first exchange bonus delivered by mail',
           'exchange_zone: 9 goods, native prices/limits/attachments/gifts; no nonempty first_prize or second_prize; need_buy_count=0',
           'gift_config type1 six recharge bonus rows; type2 four thresholds based on server-wide bricks (destinyUI L441)',
           'destinyUI L902-907 clamps discounted total to zero; L955 decrements count after reward dismissal'],
        B=['7-day recurring local period starting Monday UTC+8; principal/10 RMB; no history retroactivity',
           'type1 milestones paid once each per period; base and bonus delivered together by permanent mail',
           'server total uses actual current-period local-account bricks earned (including unclaimed mail), no simulated strangers',
           'each account may claim four public gifts once, including non-paying accounts',
           'index1 gains one extra purchase per 300 RMB, max10; all counters reset each period; currency/cards persist',
           'no global gift escalation invented because original shipped table has no threshold or alternative reward'],
        shop=p.SHOP,gifts=p.GIFTS)
    (out/'official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Verified original tables: 9 shop entries, 6 bonus tiers, 4 public gifts')

if __name__=='__main__':main()
