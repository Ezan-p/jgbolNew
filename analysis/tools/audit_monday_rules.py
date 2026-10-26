"""Audit the two distinct activities against original 3.87 bytes."""
import hashlib
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from network_redirect import activity_monday as m


def main():
    index=dict(line.split('====')[:2] for line in (ROOT/'analysis/evidence/resource_index.decoded.txt').read_text().splitlines())
    out=ROOT/'analysis/evidence/monday';out.mkdir(exist_ok=True)
    files=['v2/funUI/pic32.png','v2/funUI/title32.png','v2/funUI/pic47.png','v2/funUI/title47.png',
           'lua/ui/mondayUI.lua','lua/ui/activityUI.lua','lua/ui/funUI.lua','lua/common/common_def.lua',
           'v2/String.plist','v2/String2.plist','csv_config/achievements_config.csv']
    records=[]
    for name in files:
        path=ROOT/'jgbol3.87/assets/release_'/index[name];blob=path.read_bytes()
        records.append(dict(logical=name,original=str(path.relative_to(ROOT)),sha256=hashlib.sha256(blob).hexdigest()))
        if name.startswith('v2/funUI/'):(out/name.split('/')[-1]).write_bytes(blob)
    report=dict(client='3.87',inputs=records,
        identity={'32':'天工制物阁 / mondayUI / 1219 + 1243 / 112 + 142',
                  '47':'天机阁 / destinyUI / 1227 / 195'},
        A=['Original pic32/title32 match the supplied chest/peaches banner; pic47/title47 depict 天机阁',
           'mondayUI L53: four slots; L68-93: weekday keyed reward and separate open/closed catalog shapes',
           'mondayUI L181-188,237-252: 1219 flags1/2/3, op_type0, level1..4; 1243 index1..4',
           'mondayUI L57: event112 success=1; L128/common_op_result: event142 success=0',
           'String monday1/4/5/6/7: Monday opening, jade usable on opening day, leftovers recycled',
           'mondayUI L418-421 VIP icon with monday9: VIP receives double opening jade',
           'String monday22 and mondayUI L528-545: each preview slot may change once per closed day',
           'week_task_def: nine tasks, strength/energy/duty/raid/raid refresh/train/three blessings/fated summon/journey',
           'mondayUI L215-221: pending claim count, finished unclaimed task, Monday daily claim',
           'achievements_config 125: exchange any item at 天工制物阁, one-time 10 道行'],
        B=['UTC+8 Tuesday-through-Monday cycle; 10 jade per closed-day task, 20 Monday free (VIP40)',
           'Nine tasks rotate by local epoch day modulo nine; only committed actual gameplay completes one task',
           'Four pools and prices are server configuration missing from shipped CSV; uniform draws excluding current item on refresh',
           'Retain changed preview until Monday, repeated exchange while jade suffices, new pool Tuesday',
           'Completed unclaimed daily rewards accumulate within cycle; no credit for absent/uncompleted tasks',
           '1 jade -> 1000 silver via permanent idempotent mail at closure; unclaimed qualification expires',
           'Persist clock high-water, do not migrate unrelated pavilion bricks or historical 125 achievement'],
        inferred_rules=m.load_rules())
    (out/'official_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Audited distinct menu32/menu47 assets, native callbacks, nine tasks and four slots')

if __name__=='__main__':main()
