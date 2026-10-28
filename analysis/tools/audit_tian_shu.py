"""Hash untouched original assets and verify novice book reward extraction."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from network_redirect import tian_shu


def main():
    index = dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    enc = {r['logical']: r['encoding'] for r in json.loads((ROOT/'analysis/evidence/config_inventory.json').read_text())}
    files = []
    for logical in ('csv_config/task_guide_prize.csv', 'csv_config/guide_schedule.csv',
                    'lua/ui/tianShuUI.lua', 'lua/ui/guideUI.lua', 'lua/data.lua',
                    'lua/event_mgr.lua', 'lua/common/common_def.lua', 'lua/common/msg_def.lua'):
        raw = (ROOT/'jgbol3.87/assets/release_'/index[logical]).read_bytes()
        entry = dict(logical=logical, asset=index[logical], sha256=hashlib.sha256(raw).hexdigest())
        if logical.endswith('.csv'):
            original = list(csv.reader(io.StringIO(raw.decode(enc[logical]))))
            extracted = list(csv.reader(io.StringIO((ROOT/'analysis/configs'/Path(logical).name).read_text(encoding='utf-8-sig'))))
            assert original == extracted, logical
            entry.update(csv_values_match=True, rows=len(original)-1)
        files.append(entry)
    report = dict(inputs=files, original_contracts={
        'task_guide_prize': '14 rows; preserve CSV order; type|id|level|count, two &-separated variants',
        'tianShuUI:395-415': '1201 flag=4 id=stage; tutorial uses 1204 stage=13',
        'tianShuUI:417-459': 'event 57 task_stage/prize_list; stage12 opens monthCardUI',
        'tianShuUI:636-645,724-745': 'ordered claim progression',
        'tianShuUI:647-672': 'bit zero removed: stage n maps to 1<<n',
        'tianShuUI:674-685': 'CSV task order and stage12 month card special case',
        'data:3942-3945': 'client config key 2 -> tianShuUI.goldConfig',
        'event_mgr:2042-2044': 'attribute12 updates task_progress and redraws hint; attribute13 missing',
        'text:month_exp': '三天月卡',
        'tianShuUI:702-722': 'all rewards claimed hides book; completion is cached'},
        inferred_policies=tian_shu.load_rules(),
        rewards=[dict(stage=s, name=r['desc'], original_raw=r['gold_count'],
                      local_specs=tian_shu.reward_specs(s,tian_shu.load_rules())) for s,r in tian_shu.CATALOG.items()])
    path = ROOT/'analysis/evidence/tian_shu/official_audit.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('8 original assets hashed; both extracted CSVs match; 14 rewards and contracts recorded.')


if __name__ == '__main__': main()
