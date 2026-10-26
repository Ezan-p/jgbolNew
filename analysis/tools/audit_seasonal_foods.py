"""Audit original seasonal recipes and text; do not infer server probabilities."""
import csv
import hashlib
import io
import json
import plistlib
import re
from pathlib import Path
from luajit_static import parse, listing

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'analysis/evidence/seasonal_foods'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    enc = {r['logical']: r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
    inputs, hits, mentions = [], [], []
    def original(logical):
        raw = (ROOT/'jgbol3.87/assets/release_'/index[logical]).read_bytes()
        inputs.append(dict(logical=logical, asset=index[logical], sha256=hashlib.sha256(raw).hexdigest()))
        return raw
    tables = {}
    for path in sorted((ROOT/'analysis/configs').rglob('*.csv')):
        name = str(path.relative_to(ROOT/'analysis/configs'))
        rows = list(csv.DictReader(io.StringIO(path.read_text(encoding='utf-8-sig'))))
        tables[name] = rows
        for line, row in enumerate(rows, 2):
            for col, value in row.items():
                if isinstance(value, str) and re.search(r'(?:^|/)5\|(?:113[0-8]|120[89]|121[0-7])\|', value):
                    hits.append(dict(table=name, line=line, column=col, value=value))
            if any(word in (row.get('product_desc') or '') for word in ('月饼', '粽子')):
                mentions.append(dict(table=name, line=line, row=row))
    selected = {'compose_monthcake.csv', 'zongzi_formula.csv', 'item_name.csv', 'item_base.csv', 'skill_name.csv'} | {h['table'] for h in hits}
    for name in sorted(selected):
        logical = 'csv_config/'+name
        raw = original(logical)
        assert list(csv.reader(io.StringIO(raw.decode(enc[logical])))) == list(csv.reader(io.StringIO((ROOT/'analysis/configs'/name).read_text(encoding='utf-8-sig')))), name
        inputs[-1]['csv_matches'] = True
    strings = {}
    def collect(obj):
        if isinstance(obj, dict):
            for key, val in obj.items():
                if isinstance(val, str) and any(w in val for w in ('月饼', '粽子', '中秋', '粽叶')):
                    strings[key] = val
                elif isinstance(val, dict): collect(val)
    collect(plistlib.loads(original('v2/String.plist')))
    collect(plistlib.loads(original('v2/String2.plist')))
    for module in ('ui/ricePuddingUI', 'ui/moonCakeUI'):
        (OUT/(module.replace('/', '_')+'.txt')).write_text(listing(parse(original('lua/'+module+'.lua'))))
    ids = set(range(1130,1139)) | set(range(1208,1218))
    report = dict(client='3.87', official_server_probabilities=None, scanned_csv_count=len(tables), inputs=inputs,
                  items=[r for r in tables['item_name.csv'] if int(r['Ftype_id']) in ids],
                  recipes={n:tables[n] for n in ('compose_monthcake.csv','zongzi_formula.csv')},
                  item_tuple_hits=hits, reward_source_mentions=mentions, strings=strings)
    (OUT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(verified_csv_count=len(selected), scanned_csv_count=len(tables), tuple_hits=hits, reward_source_mentions=mentions, strings=strings),ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
